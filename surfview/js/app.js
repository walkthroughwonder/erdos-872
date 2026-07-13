// SurfView — spot map, live conditions and the drop-in simulation.

const state = {
  map: null,
  markers: {},
  selected: null,
  conditions: null,
  sim: null,
};

// ---------------------------------------------------------------- utilities

const $ = (sel) => document.querySelector(sel);

const COMPASS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                 "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
const compass = (deg) => COMPASS[Math.round(((deg % 360) + 360) % 360 / 22.5) % 16];

const mToFt = (m) => m * 3.28084;
const fmtHeight = (m) => `${mToFt(m).toFixed(1)} ft <span class="unit">(${m.toFixed(1)} m)</span>`;

function angleDiff(a, b) {
  let d = ((a - b) % 360 + 540) % 360 - 180;
  return d; // -180..180
}

// Approximate solar elevation/azimuth (radians) for a UTC date at lat/lon.
// Azimuth is compass bearing from north, clockwise. Good to ~0.5 degrees,
// plenty for placing a sun in the sky.
function sunPosition(date, lat, lon) {
  const rad = Math.PI / 180;
  const d = date.getTime() / 86400000 - 10957.5; // days since J2000.0
  const L = (280.460 + 0.9856474 * d) * rad;     // mean longitude
  const g = (357.528 + 0.9856003 * d) * rad;     // mean anomaly
  const lambda = L + (1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * rad;
  const eps = 23.439 * rad;
  const dec = Math.asin(Math.sin(eps) * Math.sin(lambda));
  const ra = Math.atan2(Math.cos(eps) * Math.sin(lambda), Math.cos(lambda));
  const gmst = (280.46061837 + 360.98564736629 * d) * rad;
  const H = gmst + lon * rad - ra; // hour angle
  const phi = lat * rad;
  const elev = Math.asin(Math.sin(phi) * Math.sin(dec) + Math.cos(phi) * Math.cos(dec) * Math.cos(H));
  let az = Math.atan2(Math.sin(H), Math.cos(H) * Math.sin(phi) - Math.tan(dec) * Math.cos(phi));
  az += Math.PI; // convert from "from south, westward" to compass bearing
  return { elev, az };
}

// ------------------------------------------------------------- data fetching

async function fetchConditions(spot) {
  const marineUrl = "https://marine-api.open-meteo.com/v1/marine" +
    `?latitude=${spot.lat}&longitude=${spot.lon}` +
    "&current=wave_height,wave_direction,wave_period," +
    "swell_wave_height,swell_wave_direction,swell_wave_period," +
    "wind_wave_height,sea_surface_temperature" +
    "&hourly=wave_height,wave_period&forecast_days=3&timezone=auto";
  const weatherUrl = "https://api.open-meteo.com/v1/forecast" +
    `?latitude=${spot.lat}&longitude=${spot.lon}` +
    "&current=temperature_2m,wind_speed_10m,wind_direction_10m,cloud_cover,weather_code" +
    "&timezone=auto";

  const [marine, weather] = await Promise.all([
    fetch(marineUrl).then(r => { if (!r.ok) throw new Error(`marine API ${r.status}`); return r.json(); }),
    fetch(weatherUrl).then(r => { if (!r.ok) throw new Error(`weather API ${r.status}`); return r.json(); }),
  ]);

  const m = marine.current, w = weather.current;
  // Prefer the groomed swell numbers; fall back to total sea state.
  const swellH = m.swell_wave_height ?? m.wave_height ?? 1.2;
  const usableSwell = swellH != null && swellH > 0.05;
  return {
    live: true,
    waveHeightM: m.wave_height ?? swellH ?? 1.2,
    swellHeightM: usableSwell ? swellH : (m.wave_height ?? 1.2),
    periodS: (usableSwell ? m.swell_wave_period : null) ?? m.wave_period ?? 10,
    swellFromDeg: (usableSwell ? m.swell_wave_direction : null) ?? m.wave_direction ?? ((spot.faces + 180) % 360),
    windWaveM: m.wind_wave_height ?? 0,
    waterTempC: m.sea_surface_temperature,
    airTempC: w.temperature_2m,
    windSpeedKmh: w.wind_speed_10m ?? 0,
    windFromDeg: w.wind_direction_10m ?? spot.faces, // meteorological: blowing FROM
    cloudCover: (w.cloud_cover ?? 20) / 100,
    utcOffsetSec: marine.utc_offset_seconds ?? weather.utc_offset_seconds ?? 0,
    hourly: {
      time: marine.hourly?.time ?? [],
      waveHeight: marine.hourly?.wave_height ?? [],
    },
  };
}

function fallbackConditions(spot) {
  return {
    live: false,
    waveHeightM: 1.4, swellHeightM: 1.4, periodS: 12,
    swellFromDeg: (spot.faces + 180) % 360,
    windWaveM: 0.2, waterTempC: null, airTempC: null,
    windSpeedKmh: 12, windFromDeg: (spot.faces + 180) % 360,
    cloudCover: 0.2, utcOffsetSec: 0,
    hourly: { time: [], waveHeight: [] },
  };
}

// Derived surf read: is the wind offshore, and a rough quality call.
function analyseConditions(spot, c) {
  // Offshore = wind blowing from land out to sea, i.e. its "from" bearing is
  // roughly opposite the direction the beach faces.
  const windToDeg = (c.windFromDeg + 180) % 360;
  const offshore = Math.abs(angleDiff(windToDeg, spot.faces)) < 65;
  const windKts = c.windSpeedKmh / 1.852;

  let quality, qualityClass;
  const h = c.waveHeightM, t = c.periodS;
  if (h < 0.4) { quality = "Flat — maybe grab a longboard"; qualityClass = "flat"; }
  else if (offshore && t >= 11 && h >= 0.9) { quality = "Firing — clean groundswell + offshore winds"; qualityClass = "firing"; }
  else if (offshore && h >= 0.5) { quality = "Clean — offshore and rideable"; qualityClass = "good"; }
  else if (!offshore && windKts > 15) { quality = "Blown out — strong onshore wind"; qualityClass = "poor"; }
  else if (t >= 11 && h >= 0.9) { quality = "Solid swell, wind could be kinder"; qualityClass = "fair"; }
  else { quality = "Surfable — nothing special"; qualityClass = "fair"; }

  return { offshore, windKts, quality, qualityClass };
}

// ------------------------------------------------------------------ map / UI

function initMap() {
  const map = L.map("map", { worldCopyJump: true, zoomControl: false }).setView([15, -30], 2.4);
  L.control.zoom({ position: "bottomright" }).addTo(map);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 17,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);
  state.map = map;

  for (const spot of SURF_SPOTS) {
    const icon = L.divIcon({
      className: "spot-marker-wrap",
      html: `<div class="spot-marker spot-${spot.type}"></div>`,
      iconSize: [16, 16],
      iconAnchor: [8, 8],
    });
    const marker = L.marker([spot.lat, spot.lon], { icon, title: spot.name })
      .addTo(map)
      .on("click", () => selectSpot(spot, { pan: false }));
    marker.bindTooltip(spot.name, { direction: "top", offset: [0, -8] });
    state.markers[spot.id] = marker;
  }
}

function renderSpotList(filter = "") {
  const q = filter.trim().toLowerCase();
  const list = $("#spot-list");
  const spots = SURF_SPOTS.filter(s =>
    !q || `${s.name} ${s.region} ${s.country} ${s.type}`.toLowerCase().includes(q));
  list.innerHTML = spots.map(s => `
    <li class="spot-item ${state.selected?.id === s.id ? "active" : ""}" data-id="${s.id}">
      <span class="spot-dot spot-${s.type}"></span>
      <span class="spot-item-text">
        <strong>${s.name}</strong>
        <small>${s.region}, ${s.country} · ${s.type.replace("-", " ")}</small>
      </span>
    </li>`).join("") || `<li class="spot-empty">No spots match “${filter}”</li>`;
  list.querySelectorAll(".spot-item").forEach(el =>
    el.addEventListener("click", () => {
      const spot = SURF_SPOTS.find(s => s.id === el.dataset.id);
      selectSpot(spot, { pan: true });
    }));
}

async function selectSpot(spot, { pan }) {
  state.selected = spot;
  renderSpotList($("#search").value);
  if (pan) state.map.flyTo([spot.lat, spot.lon], 9, { duration: 1.2 });

  const panel = $("#conditions");
  panel.classList.remove("hidden");
  panel.innerHTML = `
    <div class="cond-header">
      <div>
        <h2>${spot.name}</h2>
        <p class="cond-sub">${spot.region}, ${spot.country}</p>
      </div>
      <button id="close-cond" class="icon-btn" title="Close">✕</button>
    </div>
    <p class="cond-blurb">${spot.blurb}</p>
    <p class="loading">Fetching live ocean conditions…</p>`;
  $("#close-cond").addEventListener("click", closeConditions);

  let cond;
  try {
    cond = await fetchConditions(spot);
  } catch (err) {
    console.warn("Live data unavailable:", err);
    cond = fallbackConditions(spot);
  }
  if (state.selected?.id !== spot.id) return; // user moved on meanwhile
  state.conditions = cond;
  renderConditions(spot, cond);
}

function closeConditions() {
  state.selected = null;
  state.conditions = null;
  $("#conditions").classList.add("hidden");
  renderSpotList($("#search").value);
}

function sparklineSVG(cond) {
  const hs = cond.hourly.waveHeight.slice(0, 72).filter(v => v != null);
  if (hs.length < 8) return "";
  const w = 260, h = 46, max = Math.max(...hs, 0.5);
  const pts = hs.map((v, i) => `${(i / (hs.length - 1)) * w},${h - (v / max) * (h - 6)}`).join(" ");
  const nowLabel = "now";
  return `
    <div class="spark-wrap">
      <div class="spark-title">Next 72 h — wave height (peak ${mToFt(max).toFixed(1)} ft)</div>
      <svg viewBox="0 0 ${w} ${h}" class="spark" preserveAspectRatio="none">
        <polyline points="${pts}" fill="none" stroke="currentColor" stroke-width="2"/>
      </svg>
      <div class="spark-axis"><span>${nowLabel}</span><span>+24 h</span><span>+48 h</span><span>+72 h</span></div>
    </div>`;
}

function renderConditions(spot, c) {
  const a = analyseConditions(spot, c);
  const local = new Date(Date.now() + c.utcOffsetSec * 1000);
  const localHHMM = local.toISOString().slice(11, 16);

  $("#conditions").innerHTML = `
    <div class="cond-header">
      <div>
        <h2>${spot.name}</h2>
        <p class="cond-sub">${spot.region}, ${spot.country} · local time ${localHHMM}</p>
      </div>
      <button id="close-cond" class="icon-btn" title="Close">✕</button>
    </div>
    <p class="cond-blurb">${spot.blurb}</p>
    <div class="quality quality-${a.qualityClass}">${a.quality}</div>
    ${c.live ? "" : `<div class="offline-note">⚠ Live data unavailable right now — showing typical conditions.</div>`}
    <div class="cond-grid">
      <div class="cond-cell"><label>Surf</label><b>${fmtHeight(c.waveHeightM)}</b></div>
      <div class="cond-cell"><label>Swell</label><b>${fmtHeight(c.swellHeightM)} @ ${Math.round(c.periodS)}s</b></div>
      <div class="cond-cell"><label>Swell dir</label><b><span class="arrow" style="transform:rotate(${Math.round(c.swellFromDeg + 180)}deg)">➤</span> from ${compass(c.swellFromDeg)}</b></div>
      <div class="cond-cell"><label>Wind</label><b>${a.windKts.toFixed(0)} kts ${compass(c.windFromDeg)} · ${a.offshore ? "offshore ✓" : "onshore"}</b></div>
      ${c.waterTempC != null ? `<div class="cond-cell"><label>Water</label><b>${c.waterTempC.toFixed(0)}°C</b></div>` : ""}
      ${c.airTempC != null ? `<div class="cond-cell"><label>Air</label><b>${c.airTempC.toFixed(0)}°C</b></div>` : ""}
    </div>
    ${sparklineSVG(c)}
    <button id="drop-in" class="drop-btn">🏄 Drop in — live wave view</button>
    <p class="hint">Renders the ocean as it is at ${spot.name} right now: real swell size, period &amp; direction, wind chop, cloud cover and sun position.</p>`;

  $("#close-cond").addEventListener("click", closeConditions);
  $("#drop-in").addEventListener("click", () => enterSim(spot, c));
}

// ------------------------------------------------------------------ simulator

function enterSim(spot, c) {
  const overlay = $("#sim-overlay");
  overlay.classList.remove("hidden");

  const a = analyseConditions(spot, c);
  const sun = sunPosition(new Date(), spot.lat, spot.lon);
  const azDeg = (sun.az * 180) / Math.PI;

  // Everything in the shader is expressed in the camera frame:
  // +z looks straight out to sea along the spot's `faces` bearing.
  const rel = (bearing) => angleDiff(bearing, spot.faces);
  const cond = {
    waveHeightM: c.waveHeightM,
    wavePeriodS: c.periodS,
    swellRelDeg: rel((c.swellFromDeg + 180) % 360), // travel direction
    windRelDeg: rel((c.windFromDeg + 180) % 360),
    windSpeedMs: c.windSpeedKmh / 3.6,
    offshore: a.offshore,
    sunElevRad: sun.elev,
    sunAzimRelRad: (rel(azDeg) * Math.PI) / 180,
    cloudCover: c.cloudCover,
  };

  try {
    if (!state.sim) state.sim = new OceanSim($("#sim-canvas"));
  } catch (err) {
    overlay.classList.add("hidden");
    alert("Sorry — this browser doesn't support WebGL, which the wave view needs.\n" + err.message);
    return;
  }
  state.sim.yaw = 0;
  state.sim.pitch = -0.05;
  state.sim.setConditions(cond);
  state.sim.resize();
  state.sim.start();

  const local = new Date(Date.now() + c.utcOffsetSec * 1000);
  $("#sim-hud").innerHTML = `
    <div class="hud-top">
      <div class="hud-title">
        <h3>${spot.name}</h3>
        <span>${spot.region} · local ${local.toISOString().slice(11, 16)} · ${c.live ? "live conditions" : "typical conditions (offline)"}</span>
      </div>
      <button id="exit-sim" class="exit-btn">← Back to map</button>
    </div>
    <div class="hud-bottom">
      <span><b>${mToFt(c.waveHeightM).toFixed(1)} ft</b> @ ${Math.round(c.periodS)}s from ${compass(c.swellFromDeg)}</span>
      <span>wind <b>${a.windKts.toFixed(0)} kts</b> ${compass(c.windFromDeg)} (${a.offshore ? "offshore" : "onshore"})</span>
      ${c.waterTempC != null ? `<span>water <b>${c.waterTempC.toFixed(0)}°C</b></span>` : ""}
      <span class="hud-hint">drag to look around</span>
    </div>`;
  $("#exit-sim").addEventListener("click", exitSim);
}

function exitSim() {
  if (state.sim) state.sim.stop();
  $("#sim-overlay").classList.add("hidden");
}

// --------------------------------------------------------------------- boot

document.addEventListener("DOMContentLoaded", () => {
  initMap();
  renderSpotList();
  $("#search").addEventListener("input", (e) => renderSpotList(e.target.value));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !$("#sim-overlay").classList.contains("hidden")) exitSim();
  });
});
