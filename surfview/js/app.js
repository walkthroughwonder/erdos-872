// SurfView — spot map, live conditions and the drop-in simulation.

const state = {
  map: null,
  markers: {},
  selected: null,
  conditions: null,
  sim: null,
  cache: {},      // spot id -> { cond, at } (ms), reused for ~10 min
  ranked: false,  // list sorted by the live quality score
};
const CACHE_MS = 10 * 60 * 1000;

async function conditionsFor(spot) {
  const hit = state.cache[spot.id];
  if (hit && Date.now() - hit.at < CACHE_MS) return hit.cond;
  const cond = await fetchConditions(spot);
  state.cache[spot.id] = { cond, at: Date.now() };
  return cond;
}

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
    "&hourly=wave_height,wave_period,wave_direction,swell_wave_height,swell_wave_period,swell_wave_direction,wind_wave_height" +
    "&forecast_days=3&timezone=auto";
  const weatherUrl = "https://api.open-meteo.com/v1/forecast" +
    `?latitude=${spot.lat}&longitude=${spot.lon}` +
    "&current=temperature_2m,wind_speed_10m,wind_direction_10m,cloud_cover,weather_code" +
    "&hourly=wind_speed_10m,wind_direction_10m,cloud_cover,temperature_2m" +
    "&forecast_days=3&timezone=auto";

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
      wavePeriod: marine.hourly?.wave_period ?? [],
      waveDir: marine.hourly?.wave_direction ?? [],
      swellHeight: marine.hourly?.swell_wave_height ?? [],
      swellPeriod: marine.hourly?.swell_wave_period ?? [],
      swellDir: marine.hourly?.swell_wave_direction ?? [],
      windWave: marine.hourly?.wind_wave_height ?? [],
      windSpeed: weather.hourly?.wind_speed_10m ?? [],
      windDir: weather.hourly?.wind_direction_10m ?? [],
      cloud: weather.hourly?.cloud_cover ?? [],
    },
  };
}

// The conditions object as they will be at forecast hour `i` (local time
// strings from the API). Missing hourly fields fall back to "now".
function conditionsAtHour(c, i) {
  const h = c.hourly, pick = (arr, cur) => (arr[i] != null ? arr[i] : cur);
  const swellH = pick(h.swellHeight, c.swellHeightM);
  const usable = swellH != null && swellH > 0.05;
  return {
    ...c,
    waveHeightM: pick(h.waveHeight, c.waveHeightM),
    swellHeightM: usable ? swellH : pick(h.waveHeight, c.waveHeightM),
    periodS: (usable ? pick(h.swellPeriod, null) : null) ?? pick(h.wavePeriod, c.periodS),
    swellFromDeg: (usable ? pick(h.swellDir, null) : null) ?? pick(h.waveDir, c.swellFromDeg),
    windWaveM: pick(h.windWave, c.windWaveM),
    windSpeedKmh: pick(h.windSpeed, c.windSpeedKmh),
    windFromDeg: pick(h.windDir, c.windFromDeg),
    cloudCover: h.cloud[i] != null ? h.cloud[i] / 100 : c.cloudCover,
    at: h.time[i] ? new Date(Date.parse(h.time[i] + "Z") - c.utcOffsetSec * 1000) : new Date(),
    atLabel: h.time[i] ? h.time[i].slice(5, 16).replace("T", " ") : "now",
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
    hourly: { time: [], waveHeight: [], wavePeriod: [], waveDir: [], swellHeight: [], swellPeriod: [],
              swellDir: [], windWave: [], windSpeed: [], windDir: [], cloud: [] },
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

  // Numeric score for ranking spots: class first, then size x period.
  const rank = { firing: 4, good: 3, fair: 2, poor: 1, flat: 0 }[qualityClass];
  const score = rank * 100 + Math.min(99, h * t);
  return { offshore, windKts, quality, qualityClass, score };
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
  let spots = SURF_SPOTS.filter(s =>
    !q || `${s.name} ${s.region} ${s.country} ${s.type}`.toLowerCase().includes(q));
  const read = (s) => {
    const c = state.cache[s.id]?.cond;
    return c ? { c, a: analyseConditions(s, c) } : null;
  };
  if (state.ranked) {
    spots = spots.slice().sort((x, y) => (read(y)?.a.score ?? -1) - (read(x)?.a.score ?? -1));
  }
  list.innerHTML = spots.map(s => {
    const r = read(s);
    const badge = r ? `<span class="spot-badge badge-${r.a.qualityClass}" title="${r.a.quality}">${mToFt(r.c.waveHeightM).toFixed(0)} ft</span>` : "";
    return `
    <li class="spot-item ${state.selected?.id === s.id ? "active" : ""}" data-id="${s.id}">
      <span class="spot-dot spot-${s.type}"></span>
      <span class="spot-item-text">
        <strong>${s.name}</strong>
        <small>${s.region}, ${s.country} · ${s.type.replace("-", " ")}</small>
      </span>${badge}
    </li>`;
  }).join("") || `<li class="spot-empty">No spots match “${filter}”</li>`;
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
    cond = await conditionsFor(spot);
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

// Fetch every spot (a few at a time) and sort the list by how good it is.
async function scanAllSpots() {
  const btn = $("#firing");
  btn.disabled = true;
  let done = 0;
  const queue = SURF_SPOTS.slice();
  const worker = async () => {
    while (queue.length) {
      const spot = queue.shift();
      try { await conditionsFor(spot); } catch (e) { console.warn("scan failed", spot.id, e); }
      btn.textContent = `Checking spots… ${++done}/${SURF_SPOTS.length}`;
      renderSpotList($("#search").value);
    }
  };
  await Promise.all([worker(), worker(), worker(), worker()]);
  state.ranked = true;
  renderSpotList($("#search").value);
  btn.disabled = false;
  btn.textContent = "🔥 Ranked by conditions — rescan";
}

// ------------------------------------------------------------------ simulator

// Everything in the shader is expressed in the camera frame:
// +z looks straight out to sea along the spot's `faces` bearing.
function simConditions(spot, c, when) {
  const a = analyseConditions(spot, c);
  const sun = sunPosition(when, spot.lat, spot.lon);
  const azDeg = (sun.az * 180) / Math.PI;
  const rel = (bearing) => angleDiff(bearing, spot.faces);
  return {
    waveHeightM: c.waveHeightM,
    wavePeriodS: c.periodS,
    swellRelDeg: rel((c.swellFromDeg + 180) % 360), // travel direction
    windRelDeg: rel((c.windFromDeg + 180) % 360),
    windSpeedMs: c.windSpeedKmh / 3.6,
    offshore: a.offshore,
    sunElevRad: sun.elev,
    sunAzimRelRad: (rel(azDeg) * Math.PI) / 180,
    cloudCover: c.cloudCover,
    breakType: spot.type,
    hand: spot.hand,
  };
}

function hudNumbers(c, a) {
  return `
      <span><b>${mToFt(c.waveHeightM).toFixed(1)} ft</b> @ ${Math.round(c.periodS)}s from ${compass(c.swellFromDeg)}</span>
      <span>wind <b>${a.windKts.toFixed(0)} kts</b> ${compass(c.windFromDeg)} (${a.offshore ? "offshore" : "onshore"})</span>
      ${c.waterTempC != null ? `<span>water <b>${c.waterTempC.toFixed(0)}°C</b></span>` : ""}`;
}

function enterSim(spot, c) {
  const overlay = $("#sim-overlay");
  overlay.classList.remove("hidden");

  const a = analyseConditions(spot, c);

  try {
    if (!state.sim) state.sim = new OceanSim($("#sim-canvas"));
  } catch (err) {
    overlay.classList.add("hidden");
    alert("Sorry — this browser doesn't support WebGL, which the wave view needs.\n" + err.message);
    return;
  }
  state.sim.yaw = 0;
  state.sim.pitch = -0.05;
  state.sim.setConditions(simConditions(spot, c, new Date()));
  state.sim.resize();
  state.sim.start();

  const local = new Date(Date.now() + c.utcOffsetSec * 1000);
  const hours = c.hourly.time.length;
  // Index of the current hour in the forecast arrays (local time strings).
  const nowIdx = Math.max(0, c.hourly.time.findIndex(t => t >= local.toISOString().slice(0, 13)));
  $("#sim-hud").innerHTML = `
    <div class="hud-top">
      <div class="hud-title">
        <h3>${spot.name}</h3>
        <span id="hud-when">${spot.region} · local ${local.toISOString().slice(11, 16)} · ${c.live ? "live conditions" : "typical conditions (offline)"}</span>
      </div>
      <button id="exit-sim" class="exit-btn">← Back to map</button>
    </div>
    ${hours > 8 ? `
    <div class="hud-scrub">
      <label for="scrub">Forecast</label>
      <input id="scrub" type="range" min="${nowIdx}" max="${hours - 1}" value="${nowIdx}" step="1">
      <span id="scrub-label">now</span>
    </div>` : ""}
    <div class="hud-bottom">
      <span id="hud-nums">${hudNumbers(c, a)}</span>
      <span class="hud-hint">drag look · WASD move · Q/E height · Shift fast</span>
    </div>
    <div id="dpad">
      <button data-mv="fwd"   style="grid-area:f" aria-label="Forward">▲</button>
      <button data-mv="left"  style="grid-area:l" aria-label="Left">◀</button>
      <button data-mv="back"  style="grid-area:b" aria-label="Back">▼</button>
      <button data-mv="right" style="grid-area:r" aria-label="Right">▶</button>
      <button data-mv="up"    style="grid-area:u" aria-label="Rise">✚</button>
      <button data-mv="down"  style="grid-area:d" aria-label="Descend">▬</button>
    </div>`;
  $("#exit-sim").addEventListener("click", exitSim);

  // Scrub the forecast: swap the sea state and sun to that hour, keep the
  // camera where it is.
  const scrub = $("#scrub");
  if (scrub) {
    scrub.addEventListener("input", () => {
      const i = +scrub.value;
      const isNow = i === nowIdx;
      const hc = isNow ? c : conditionsAtHour(c, i);
      const when = isNow ? new Date() : hc.at;
      state.sim.updateConditions(simConditions(spot, hc, when));
      $("#scrub-label").textContent = isNow ? "now" : hc.atLabel;
      $("#hud-nums").innerHTML = hudNumbers(hc, analyseConditions(spot, hc));
      $("#hud-when").textContent = isNow
        ? `${spot.region} · local ${local.toISOString().slice(11, 16)} · ${c.live ? "live conditions" : "typical conditions (offline)"}`
        : `${spot.region} · forecast for ${hc.atLabel} local`;
    });
  }
  document.querySelectorAll("#dpad button").forEach(btn => {
    const mv = btn.dataset.mv;
    const on = (e) => { e.preventDefault(); state.sim.setMove(mv, true); };
    const off = () => state.sim.setMove(mv, false);
    btn.addEventListener("pointerdown", on);
    btn.addEventListener("pointerup", off);
    btn.addEventListener("pointerleave", off);
    btn.addEventListener("pointercancel", off);
  });
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
  $("#firing").addEventListener("click", scanAllSpots);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !$("#sim-overlay").classList.contains("hidden")) exitSim();
  });
});
