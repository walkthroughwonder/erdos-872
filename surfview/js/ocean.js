// OceanSim — first-person WebGL surf scene, raymarched in a fragment shader.
//
// The scene is a full 3D signed-distance field (not just a heightfield), so
// the breaking wave can genuinely curl: in the breaking window the crest
// gains a thrown lip (a solid tube of water blended onto the crest) and a
// carved barrel cavity beneath it, both phase-locked to the moving swell.
//
// The wave field is an original sum of directional components — swell
// sidebands around the real swell direction plus wind chop — riding over a
// parametric bathymetry per break type (reef slab and channel, angled point
// contours, sandbars with rip gaps, river-mouth wedge, big-wave ledge).
// Surf physics shape it: shoaling amplification, crests pitching forward,
// breaking where height exceeds ~0.78x depth, whitewater rolling shoreward,
// turquoise flats over the shallows. The seabed rises through the waterline
// into a sand beach with dunes and foam runup, so turning around shows the
// shore. Sets arrive as wave groups travelling at the group velocity.
//
// A second pass keeps a persistent surf-state map (a ping-pong RGBA texture
// over the break, updated every frame): fresh foam and old foam that are
// ADVECTED shoreward at the bore speed and decay over seconds, plus sand
// wetness and a fast-draining surface film. That is what makes whitewater
// trail behind a broken wave and the beach darken where the last runup
// reached, instead of foam being painted instantaneously from the wave
// shape. The two-population foam model, the advect-decay-source structure
// and the decay constants follow the approach in the MIT-licensed
// coastal-simulation project (github.com/iamtechartist/coastal-simulation);
// the implementation here is our own, driven by the analytic breaking field
// rather than a shallow-water solver.
//
// The camera is free: drag to look, WASD to move, Q/E for height — paddle
// into the barrel or climb above the reef and watch it peel. The sun sits
// where it really is at the spot right now.

const OCEAN_VS = `
attribute vec2 aPos;
void main() { gl_Position = vec4(aPos, 0.0, 1.0); }
`;

// Shared declarations and wave model, compiled into both fragment programs.
const OCEAN_COMMON = `
precision highp float;

uniform float uTime;
uniform float uAmp;       // deep-water swell amplitude (m) — half the height
uniform float uK;         // primary wavenumber, 2*pi / wavelength
uniform vec2  uSwellDir;  // unit vector, direction swell TRAVELS (camera frame, +z = out to sea)
uniform vec2  uWindDir;   // unit vector, direction wind blows toward (camera frame)
uniform float uChop;      // 0..1 wind-chop energy
uniform float uBreakType; // 0 reef, 1 point, 2 beach, 3 river-mouth, 4 big-wave
uniform float uShallow;   // shallowest depth over the break (m), scaled to swell
uniform float uSet;       // global swell gain
uniform float uHand;      // +1 right-hander, -1 left-hander (mirrors the seabed)
uniform vec2  uFoamOrigin;
uniform vec2  uFoamSize;

const float G = 9.81;

float hash21(vec2 p) {
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}

float vnoise(vec2 p) {
  vec2 i = floor(p), f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  float a = hash21(i);
  float b = hash21(i + vec2(1.0, 0.0));
  float c = hash21(i + vec2(0.0, 1.0));
  float d = hash21(i + vec2(1.0, 1.0));
  return mix(mix(a, b, f.x), mix(c, d, f.x), f.y) * 2.0 - 1.0;
}

vec2 rot2(vec2 v, float a) {
  float c = cos(a), s = sin(a);
  return vec2(c * v.x - s * v.y, s * v.x + c * v.y);
}

float smin2(float a, float b, float k) {
  float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
  return mix(b, a, h) - k * h * (1.0 - h);
}
float smax2(float a, float b, float k) { return -smin2(-a, -b, k); }

// Signed water depth (m); negative means land above sea level. The base
// slope runs from dunes behind the camera down to open ocean, with a wavy
// shoreline; each break type then sculpts its own feature.
float bathyRaw(vec2 p) {
  float x = p.x * uHand, z = p.y;               // lefts are the mirror of rights
  float zEff = z + 16.0 * vnoise(vec2(x * 0.009, 2.7)); // shoreline waviness
  float d = 6.5 + 0.095 * zEff;                          // shore ~68 m behind camera
  if (uBreakType < 0.5) {
    // Reef pass: shallow slab just ahead-left, deep channel under the camera.
    float slab = exp(-pow(x + 14.0, 2.0) / 5200.0 - pow(z - 42.0, 2.0) / 3400.0);
    d = mix(d, uShallow, slab);
  } else if (uBreakType < 1.5) {
    // Point: depth contours angled ~35 deg so the break peels across view.
    float u = z * 0.82 + x * 0.57;
    d = mix(uShallow - 7.0, 32.0, smoothstep(-110.0, 210.0, u + 12.0 * vnoise(vec2(u * 0.01, 5.1))));
  } else if (uBreakType < 2.5) {
    // Beach: outer sandbar with rip-channel gaps, shallower trough inside.
    float bar = exp(-pow(z - 48.0, 2.0) / 2200.0) * (0.62 + 0.38 * sin(x * 0.045 + 1.3));
    d = mix(d, uShallow, bar);
  } else if (uBreakType < 3.5) {
    // River mouth: tapered wedge of sand raked off the rivermouth.
    float u = (z - 20.0) + abs(x - 15.0) * 0.6;
    d = mix(uShallow - 7.0, 32.0, smoothstep(-115.0, 205.0, u));
  } else {
    // Big-wave ledge: deep ocean jumping onto a shelf far out.
    d = 8.0 + 0.16 * zEff;
    float ledge = exp(-pow(z - 80.0, 2.0) / 4200.0);
    d = mix(d, uShallow + 2.5, ledge);
  }
  return d;
}

float shoalGain(float d) {
  return pow(clamp(18.0 / d, 1.0, 10.0), 0.42);
}

// One directional wave with a sharpened crest; the lean parameter pitches
// the crest forward (second harmonic) the way a shoaling wave throws its lip.
float dwave(vec2 p, vec2 dir, float k, float amp, float sharp, float phase, float lean) {
  float w = sqrt(G * k);
  float x = dot(p, dir) * k - uTime * w + phase;
  float s = 0.5 + 0.5 * sin(x);
  float h = pow(s, sharp) * 2.0 - 0.7;
  h += lean * 1.0 * pow(s, sharp * 0.6) * sin(1.1 - x * 2.0);
  return amp * h;
}

// Shoaled swell amplitude and breaking parameter at a point. Sets arrive
// as wave GROUPS: a long spatial envelope travelling at the group velocity
// (c/2 in deep water), so lulls and bombs march through the lineup instead
// of the whole ocean breathing in unison.
void surfState(vec2 p, float d, out float aSw, out float gam, out float steep) {
  float dw = max(d, 0.7);
  float grp = dot(p, uSwellDir) * uK / 6.0 - uTime * sqrt(G * uK) / 12.0;
  float env = 0.78 + 0.22 * sin(grp + 1.0);
  aSw = uAmp * uSet * env * shoalGain(dw) * smoothstep(0.0, 1.5, d);
  gam = 2.0 * aSw / dw;
  // Waves jack up hard right at the brink, then dump energy shoreward.
  aSw *= 1.0 + 1.0 * smoothstep(0.5, 0.85, gam) * (1.0 - smoothstep(1.05, 1.5, gam));
  aSw *= mix(1.0, 0.42, smoothstep(1.15, 2.0, gam));
  steep = smoothstep(0.35, 0.85, gam);
}

// Phase of the primary swell relative to its crest (radians, -pi..pi).
float crestPhase(vec2 p) {
  float x = dot(p, uSwellDir) * uK - uTime * sqrt(G * uK);
  return (fract((x - 1.5708) / 6.28318 + 0.5) - 0.5) * 6.28318;
}

float waveField(vec2 p, float d, bool detail, out float aSw, out float gam) {
  float steep;
  surfState(p, d, aSw, gam, steep);
  float h = 0.0;
  h += dwave(p, uSwellDir,              uK,        aSw  * 0.62, 2.8 + 3.6 * steep, 0.0, steep);
  h += dwave(p, rot2(uSwellDir,  0.26), uK * 1.31, aSw  * 0.22, 2.2 + 2.2 * steep, 1.7, steep * 0.7);
  h += dwave(p, rot2(uSwellDir, -0.33), uK * 0.77, uAmp * 0.16 * smoothstep(0.0, 1.2, d), 2.0, 4.1, 0.0);
  // Wind chop also dies at the waterline instead of rippling up the sand.
  float ct = smoothstep(0.0, 0.5, d);
  float ca = uChop * ct;
  h += dwave(p, uWindDir,               uK * 4.1,  (uAmp * 0.09 + 0.03) * ca, 1.7, 2.3, 0.0);
  h += dwave(p, rot2(uWindDir,  0.85),  uK * 7.7,  (uAmp * 0.05 + 0.02) * ca, 1.5, 5.9, 0.0);
  if (detail) {
    h += dwave(p, rot2(uWindDir, -1.2), uK * 14.3, (uAmp * 0.025 + 0.012) * ca, 1.3, 3.3, 0.0);
    h += 0.018 * (0.4 + ca) * ct * vnoise(p * 2.7 + uTime * 0.6);
    h += 0.010 * (0.4 + ca) * ct * vnoise(p * 6.3 - uTime * 0.9);
  }
  return h;
}

// Beach terrain: the seabed continued through the waterline, steepened
// ashore and topped with dunes.
float terrainH(vec2 p) {
  float g = -bathyRaw(p);
  float up = max(g, 0.0);
  g += up * 0.8;
  g += (0.9 * vnoise(p * 0.045) + 0.35 * vnoise(p * 0.11)) * smoothstep(0.5, 5.0, up);
  return g;
}

// Material coordinates ride with the water so foam TEXTURE flows and
// stretches instead of sitting still under a moving foam mask. They are
// stored as unit vectors (cos, sin) of the coordinate on a 20 m tile so
// bilinear filtering never sees a wrap seam.
const float FLOW_TILE = 20.0;
vec4 encodeFlow(vec2 m) {
  vec2 a = m / FLOW_TILE * 6.28318;
  return vec4(cos(a.x), sin(a.x), cos(a.y), sin(a.y)) * 0.5 + 0.5;
}
vec2 decodeFlow(vec4 e) {
  e = e * 2.0 - 1.0;
  return vec2(atan(e.y, e.x), atan(e.w, e.z)) / 6.28318 * FLOW_TILE;
}
`;

// Pass 1b — advect material coordinates with the bore, relaxing slowly
// back to the resting grid so the field never tears.
const FLOW_FS = OCEAN_COMMON + `
uniform sampler2D uFlowPrev;
uniform vec2  uFoamRes;
uniform float uDt;
uniform float uReset;   // 1: write the resting grid instead of advecting

void main() {
  vec2 uv = gl_FragCoord.xy / uFoamRes;
  vec2 p = uFoamOrigin + uv * uFoamSize;
  if (uReset > 0.5) { gl_FragColor = encodeFlow(p); return; }
  float d = bathyRaw(p);
  float aSw, gam, steep;
  surfState(p, d, aSw, gam, steep);
  // Only broken water carries the texture; unbroken swell leaves it alone.
  float carry = smoothstep(0.9, 1.4, gam) * smoothstep(0.0, 0.4, d);
  float c = sqrt(G * max(d, 0.4)) * 0.55 * carry;
  vec2 prevUV = (p - uSwellDir * c * uDt - uFoamOrigin) / uFoamSize;
  vec4 e = texture2D(uFlowPrev, clamp(prevUV, 0.0, 1.0)) * 2.0 - 1.0;
  vec4 rest = encodeFlow(p) * 2.0 - 1.0;
  float k = 1.0 - exp(-uDt * 0.05);
  e = mix(e, rest, k);
  e.xy = normalize(e.xy + 1e-4); e.zw = normalize(e.zw + 1e-4);
  gl_FragColor = e * 0.5 + 0.5;
}
`;

// Pass 1 — persistent surf state. R fresh foam, G old foam, B sand wetness,
// A surface film. Foam advects shoreward with the bore and decays; wetness
// and film stay with the sand.
const FOAM_FS = OCEAN_COMMON + `
uniform sampler2D uFoamPrev;
uniform vec2  uFoamRes;
uniform float uDt;

void main() {
  vec2 uv = gl_FragCoord.xy / uFoamRes;
  vec2 p = uFoamOrigin + uv * uFoamSize;
  float dt = uDt;

  float d = bathyRaw(p);
  float aSw, gam, steep;
  surfState(p, d, aSw, gam, steep);

  // Broken water surges shoreward at roughly the bore celerity sqrt(g d).
  float c = sqrt(G * max(d, 0.4)) * 0.55;
  vec2 prevP = p - uSwellDir * c * dt;
  vec2 prevUV = (prevP - uFoamOrigin) / uFoamSize;
  vec4 adv = texture2D(uFoamPrev, clamp(prevUV, 0.0, 1.0));
  vec4 here = texture2D(uFoamPrev, uv);

  float fresh = adv.r, old = adv.g, wet = here.b, film = here.a;

  // Source: the lip explodes near the crest once the wave passes the
  // breaking limit, and broken whitewater keeps churning shoreward of it.
  float pd = crestPhase(p);
  float nearCrest = exp(-pd * pd * 1.6);
  float lip = smoothstep(0.74, 1.02, gam) * nearCrest;
  float churn = smoothstep(1.10, 1.55, gam) * 0.30;
  float source = (lip * 1.4 + churn) * smoothstep(0.0, 0.4, d);

  // Foam dissipates fast once the bore runs into deep water and stops
  // breaking; over the shallows it lingers.
  float diss = 1.0 + 2.5 * smoothstep(2.5, 7.0, d);
  fresh = clamp(fresh * exp(-dt * 0.65 * diss) + dt * source, 0.0, 1.0);
  old   = clamp(old * exp(-dt * 0.145 * diss) + fresh * dt * 0.18, 0.0, 0.85);

  // Wetness and film: is there water standing here right now?
  float aS2, gm2;
  float eta = waveField(p, d, false, aS2, gm2);
  float bedElev = -d;
  float cover = eta - bedElev;            // water depth above the bed
  if (cover > 0.01) {
    wet = min(1.0, wet + dt * 2.5);
    film = max(film, min(1.0, cover * 5.0));
  } else {
    wet *= exp(-dt * 0.011);              // absorbed moisture lingers ~90 s
    film *= exp(-dt * 0.31);              // sheen drains in a few seconds
  }

  // The targets are 8-bit: a slow per-frame decay would round back to the
  // same byte and never fade. Stochastic rounding keeps the mean exact.
  vec2 fc = gl_FragCoord.xy;
  float jt = fract(uTime * 7.31) * 41.0;
  vec4 dither = vec4(hash21(fc + jt), hash21(fc * 1.7 + 3.0 + jt),
                     hash21(fc * 0.7 + 11.0 + jt), hash21(fc * 1.3 + 19.0 + jt)) - 0.5;
  gl_FragColor = clamp(vec4(fresh, old, wet, film) + dither / 255.0, 0.0, 1.0);
}
`;

// Pass 2 — the scene itself.
const OCEAN_FS = OCEAN_COMMON + `
uniform vec2  uRes;
uniform vec2  uLook;      // yaw, pitch in radians
uniform vec3  uCamPos;    // camera position (m); origin is the takeoff zone
uniform vec3  uSunDir;    // unit vector toward the sun (camera frame)
uniform float uCloud;     // 0..1 cloud cover
uniform sampler2D uFoamTex;
uniform sampler2D uFlowTex;

// The main march runs from above or from below the surface; gSign flips
// the water SDF when the camera is submerged.
float gSign = 1.0;

// Persistent surf state, faded out beyond the tracked domain.
vec4 surfMemory(vec2 p) {
  vec2 uv = (p - uFoamOrigin) / uFoamSize;
  vec2 g = min(uv, 1.0 - uv);
  float m = smoothstep(0.0, 0.03, min(g.x, g.y));
  if (m <= 0.0) return vec4(0.0);
  return texture2D(uFoamTex, clamp(uv, 0.0, 1.0)) * m;
}

// World position of the water parcel now at p (for flowing textures).
vec2 flowCoord(vec2 p) {
  vec2 uv = (p - uFoamOrigin) / uFoamSize;
  if (uv.x <= 0.0 || uv.y <= 0.0 || uv.x >= 1.0 || uv.y >= 1.0) return p;
  vec2 m = decodeFlow(texture2D(uFlowTex, uv));
  // Reattach the tile-relative coordinate to the tile p sits in.
  vec2 base = floor(p / FLOW_TILE) * FLOW_TILE;
  vec2 rel = p - base;
  vec2 off = m - rel;
  off -= FLOW_TILE * floor(off / FLOW_TILE + 0.5);
  return p + off;
}

// Water surface as a 3D SDF. In the breaking window a thrown lip (solid
// tube of water) is blended onto the crest and a barrel cavity is carved
// beneath it, both phase-locked to the moving primary swell, so the wave
// visibly curls over a hollow tube where the bottom says it should.
float waterSDF(vec3 p, bool detail) {
  float d = bathyRaw(p.xz);
  float aSw, gam;
  float f = p.y - waveField(p.xz, d, detail, aSw, gam);

  float brl = smoothstep(0.60, 0.85, gam) * (1.0 - smoothstep(1.25, 1.6, gam));
  if (brl > 0.02) {
    float ds = crestPhase(p.xz) / uK;                 // meters ahead of crest
    float R  = max(aSw * 0.85 * brl, 0.02);           // barrel radius
    float yc = aSw * 0.95;                            // crest height estimate
    vec2 q = vec2(ds, p.y);
    float cav = length(q - vec2(R * 0.60, yc - R * 0.90)) - R;
    float lip = length(q - vec2(R * 1.10, yc - R * 0.18)) - R * 0.45;
    f = smin2(f, lip, R * 0.35);
    f = smax2(f, -cav, R * 0.30);
  }
  return f;
}

// Scene SDF: water or sand, whichever is closer. Distances are damped to
// stay conservative against steep wave faces.
float mapScene(vec3 p, bool detail, out float mat) {
  float fw = waterSDF(p, detail) * 0.42 * gSign;
  float ft = (p.y - terrainH(p.xz)) * 0.55;
  if (ft < fw) { mat = 1.0; return ft; }
  mat = 0.0;
  return fw;
}

vec2 traceScene(vec3 ro, vec3 rd) {
  float t = 0.06;
  float mat = 0.0;
  for (int i = 0; i < 150; i++) {
    vec3 p = ro + rd * t;
    if (p.y > 65.0 && rd.y > 0.0) return vec2(-1.0, 0.0);
    float f = mapScene(p, false, mat);
    if (f < 0.0015 * t + 0.0008) return vec2(t, mat);
    t += f;
    if (t > 1700.0) break;
  }
  if (rd.y < -0.03) return vec2(t, 0.0); // grazing water toward the horizon
  return vec2(-1.0, 0.0);
}

vec3 calcNormal(vec3 p, float t) {
  float e = 0.04 + t * t * 1.1e-4;
  float m;
  vec2 k = vec2(1.0, -1.0);
  return normalize(k.xyy * mapScene(p + k.xyy * e, true, m) +
                   k.yyx * mapScene(p + k.yyx * e, true, m) +
                   k.yxy * mapScene(p + k.yxy * e, true, m) +
                   k.xxx * mapScene(p + k.xxx * e, true, m));
}

vec3 skyColor(vec3 rd) {
  float elev = uSunDir.y;                                   // sun elevation, -1..1
  float day    = smoothstep(-0.10, 0.20, elev);             // 0 night .. 1 day
  float sunset = smoothstep(0.35, 0.05, abs(elev)) * step(-0.12, elev);

  vec3 zenDay = vec3(0.16, 0.38, 0.65), zenNight = vec3(0.015, 0.03, 0.08);
  vec3 horDay = vec3(0.66, 0.78, 0.86), horNight = vec3(0.05, 0.07, 0.13);
  vec3 zen = mix(zenNight, zenDay, day);
  vec3 hor = mix(horNight, horDay, day);
  hor = mix(hor, vec3(0.95, 0.55, 0.28), sunset * 0.8);     // dawn/dusk band

  float up = clamp(rd.y, 0.0, 1.0);
  vec3 sky = mix(hor, zen, pow(up, 0.6));

  // Sun disk and glow.
  float sunAmt = max(dot(rd, uSunDir), 0.0);
  vec3 sunTint = mix(vec3(1.0, 0.55, 0.25), vec3(1.0, 0.95, 0.85), day);
  sky += sunTint * (pow(sunAmt, 1600.0) * 8.0 + pow(sunAmt, 12.0) * 0.35) * smoothstep(-0.1, 0.0, elev);

  // Clouds: two octaves of value noise on the sky dome, blended by cover.
  if (rd.y > 0.02) {
    vec2 cp = rd.xz / (rd.y + 0.15);
    float cl = 0.6 * vnoise(cp * 1.4 + uTime * 0.008) + 0.4 * vnoise(cp * 3.1 - uTime * 0.011);
    float cover = smoothstep(0.55 - uCloud, 1.05 - uCloud, cl * 0.5 + 0.5);
    vec3 cloudCol = mix(vec3(0.06, 0.07, 0.10), mix(vec3(0.75), vec3(1.0, 0.9, 0.8), sunset), day);
    sky = mix(sky, cloudCol, cover * smoothstep(0.02, 0.12, rd.y) * 0.9);
  }
  // Overcast mutes everything.
  sky = mix(sky, vec3(dot(sky, vec3(0.33))) * 0.9, uCloud * 0.35);

  // A few stars, only once it is properly dark.
  float night = smoothstep(0.75, 1.0, 1.0 - day);
  if (night > 0.0 && rd.y > 0.05) {
    vec2 sp = floor(rd.xz / rd.y * 180.0);
    float st = step(0.997, hash21(sp));
    sky += vec3(st) * night * 0.8 * hash21(sp + 7.0);
  }
  return sky;
}

vec3 waterColor(vec3 p, vec3 n, vec3 rd, float dist) {
  float elev = uSunDir.y;
  float day = smoothstep(-0.10, 0.20, elev);
  float light = 0.06 + 0.94 * day;

  float fres = 0.04 + 0.96 * pow(1.0 - max(dot(n, -rd), 0.0), 5.0);
  fres = min(fres, 0.9);

  vec3 refl = skyColor(reflect(rd, n));

  // Bottom-aware water body color: turquoise flats, dark channels.
  float d = bathyRaw(p.xz);
  float aSw, gam, steep;
  surfState(p.xz, d, aSw, gam, steep);

  vec3 deep = vec3(0.015, 0.075, 0.11) * light;
  vec3 sub  = vec3(0.06, 0.32, 0.30) * light;
  float dif = max(dot(n, uSunDir), 0.0);
  float hFac = clamp((p.y + uAmp) / max(2.0 * uAmp, 0.4), 0.0, 1.0);
  vec3 body = mix(deep, sub, hFac * (0.35 + 0.65 * dif));
  vec3 flats = vec3(0.05, 0.38, 0.38) * light;
  body = mix(body, flats, smoothstep(9.0, 2.0, d) * 0.75);

  // Light bleeds through the thin thrown lip: green glow near the curl.
  float thin = smoothstep(0.0, -0.5, n.y) * smoothstep(0.4, 1.0, gam);
  body += vec3(0.05, 0.30, 0.24) * light * thin;

  vec3 col = mix(body, refl, fres);

  // Sun glint.
  float spec = pow(max(dot(reflect(rd, n), uSunDir), 0.0), 220.0);
  vec3 sunTint = mix(vec3(1.0, 0.6, 0.3), vec3(1.0, 0.97, 0.9), day);
  col += sunTint * spec * (1.5 + dist * 0.02) * smoothstep(-0.06, 0.02, elev);

  // Foam. Instantaneous sources (crest, breaking lip, curl underside) plus
  // the persistent advected foam that trails behind a wave that has broken,
  // broken up into lace as it ages.
  vec4 mem = surfMemory(p.xz);
  vec2 fc = flowCoord(p.xz);
  float lace = smoothstep(0.15, 0.85, 0.5 + 0.5 * vnoise(fc * 1.8 + uTime * 0.05));
  float fil = 0.5 + 0.5 * vnoise(fc * vec2(0.9, 4.5) + 3.0);   // filaments along the flow
  float trail = clamp(mem.r * 0.75 * (0.55 + 0.45 * lace) + mem.g * 0.5 * (0.2 + 0.8 * lace * fil), 0.0, 1.0);
  float crest = smoothstep(uAmp * 0.45, uAmp * 1.05, p.y) * smoothstep(0.88, 0.55, n.y);
  // Forward face: n.xz = -grad(h), which points ALONG travel on the shoreward face.
  float front = clamp(dot(vec2(n.x, n.z), uSwellDir) * 3.0 + 0.4, 0.0, 1.0);
  float lipF = smoothstep(0.68, 0.98, gam) * smoothstep(aSw * 0.2, aSw * 0.75, p.y) * front;
  float under = smoothstep(0.05, -0.45, n.y) * smoothstep(0.55, 0.9, gam); // curl underside
  float streaks = uChop * 0.25 * smoothstep(0.3, 0.9, vnoise(p.xz * 0.9 + uTime * 0.2));
  float tex = 0.55 + 0.45 * vnoise(fc * 6.0 + uTime * 0.2);
  float foam = clamp((crest + streaks * crest) * tex
                   + (lipF + under * 0.8) * (0.6 + 0.6 * tex)
                   + trail * (0.55 + 0.55 * tex), 0.0, 1.0);
  foam *= exp(-dist * 0.003);
  col = mix(col, vec3(0.92, 0.95, 0.97) * (0.15 + 0.85 * light), foam);

  // Spray glow on the exploding lip.
  col += vec3(0.25) * light * lipF * smoothstep(0.5, 1.0, tex) * exp(-dist * 0.008);

  return col;
}

vec3 sandColor(vec3 p, vec3 n, float dist) {
  float elev = uSunDir.y;
  float day = smoothstep(-0.10, 0.20, elev);
  float light = 0.06 + 0.94 * day;

  vec4 mem = surfMemory(p.xz);

  vec3 dry = vec3(0.78, 0.68, 0.52), wet = vec3(0.42, 0.36, 0.29);
  // Darkening follows the remembered runup, not just height above the water.
  float wetBand = clamp(mem.b * 0.85 + smoothstep(1.2, 0.15, p.y) * 0.35, 0.0, 1.0);
  vec3 c = mix(dry, wet, wetBand);
  // Dune grass creeping over the higher sand.
  float grass = smoothstep(4.0, 9.0, p.y) * smoothstep(0.55, 0.9, n.y) * (1.0 - wetBand);
  c = mix(c, vec3(0.30, 0.38, 0.22), grass * 0.8);
  c *= 0.85 + 0.15 * vnoise(p.xz * 0.9);

  float dif = clamp(dot(n, uSunDir), 0.0, 1.0);
  vec3 col = c * light * (0.35 + 0.75 * dif);

  // Wet film still on the surface reflects the sky for a few seconds.
  float film = mem.a;
  if (film > 0.01) {
    float fres = 0.03 + 0.55 * pow(1.0 - clamp(n.y, 0.0, 1.0), 3.0);
    col = mix(col, skyColor(vec3(0.0, 0.35, 1.0)) * 0.9, film * (0.18 + fres));
  }

  // Sheets of foam left on the sand by the last runup.
  float tex = 0.5 + 0.5 * vnoise(p.xz * 5.0 + uTime * 0.25);
  float lace = smoothstep(0.2, 0.8, 0.5 + 0.5 * vnoise(p.xz * 2.2));
  float sheet = clamp(mem.r * 1.0 + mem.g * 0.4, 0.0, 1.0) * (0.3 + 0.7 * lace) * (0.55 + 0.6 * tex);
  col = mix(col, vec3(0.9, 0.93, 0.94) * light, clamp(sheet, 0.0, 0.9));
  return col;
}

void main() {
  vec2 uv = (gl_FragCoord.xy * 2.0 - uRes) / uRes.y;

  float yaw = uLook.x, pitch = uLook.y;
  vec3 fwd = vec3(sin(yaw) * cos(pitch), sin(pitch), cos(yaw) * cos(pitch));
  vec3 right = normalize(vec3(cos(yaw), 0.0, -sin(yaw)));
  vec3 up = cross(fwd, right);
  vec3 rd = normalize(fwd + uv.x * right * 0.9 + uv.y * up * 0.9);
  vec3 ro = uCamPos;

  // Duck dive: if the camera is under the surface, march the inverted
  // water SDF and look up at the underside through green murk.
  float dCam = bathyRaw(ro.xz);
  float aC, gC;
  float hCam = waveField(ro.xz, dCam, false, aC, gC);
  bool under = ro.y < hCam - 0.05;
  gSign = under ? -1.0 : 1.0;

  vec3 col;
  vec2 hit = (!under && rd.y > 0.45 && ro.y < 40.0) ? vec2(-1.0, 0.0) : traceScene(ro, rd);
  if (under) {
    float day = smoothstep(-0.10, 0.20, uSunDir.y);
    float light = 0.06 + 0.94 * day;
    vec3 murk = vec3(0.02, 0.22, 0.26) * light;
    if (hit.x < 0.0) {
      col = murk;
    } else {
      vec3 p = ro + rd * hit.x;
      vec3 n = calcNormal(p, hit.x);
      if (hit.y > 0.5) {
        col = sandColor(p, n, hit.x) * vec3(0.5, 0.8, 0.85);
      } else {
        // Underside of the surface: sky through the window, foam as bright caps.
        vec3 sky = skyColor(normalize(vec3(rd.x, abs(rd.y) + 0.2, rd.z)));
        float caps = clamp(surfMemory(p.xz).r + surfMemory(p.xz).g * 0.6, 0.0, 1.0);
        col = mix(sky * vec3(0.6, 0.9, 0.95), vec3(0.9) * light, caps * 0.7);
        float shafts = 0.5 + 0.5 * vnoise(p.xz * 0.8 + uTime * 0.4);
        col *= 0.7 + 0.5 * shafts * day;
      }
      col = mix(col, murk, 1.0 - exp(-hit.x * 0.09));
    }
    col *= 1.0 - 0.25 * dot(uv * 0.55, uv * 0.55);
    col = pow(max(col, 0.0), vec3(0.4545));
    gl_FragColor = vec4(col, 1.0);
    return;
  }

  if (hit.x < 0.0) {
    col = skyColor(rd);
  } else {
    vec3 p = ro + rd * hit.x;
    vec3 n = calcNormal(p, hit.x);
    col = (hit.y > 0.5) ? sandColor(p, n, hit.x) : waterColor(p, n, rd, hit.x);
    // Aerial perspective toward the horizon.
    float fog = 1.0 - exp(-hit.x * 0.0011);
    col = mix(col, skyColor(normalize(vec3(rd.x, abs(rd.y) * 0.15, rd.z))), fog);
  }

  // Vignette + gamma.
  col *= 1.0 - 0.25 * dot(uv * 0.55, uv * 0.55);
  col = pow(max(col, 0.0), vec3(0.4545));
  gl_FragColor = vec4(col, 1.0);
}
`;

const BREAK_TYPE_IDS = { "reef": 0, "point": 1, "beach": 2, "river-mouth": 3, "big-wave": 4 };

// The surf-state map covers the break and the beach behind it.
const FOAM_ORIGIN = [-150, -90];
const FOAM_SIZE = [300, 360];
const FOAM_RES = 512;

// --- JS mirror of the shader's terrain, for camera collision. ---
const fract1 = (x) => x - Math.floor(x);
function jsHash21(x, y) {
  let px = fract1(x * 123.34), py = fract1(y * 456.21);
  const d = px * (px + 45.32) + py * (py + 45.32);
  px += d; py += d;
  return fract1(px * py);
}
function jsVnoise(x, y) {
  const ix = Math.floor(x), iy = Math.floor(y);
  let fx = x - ix, fy = y - iy;
  fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy);
  const a = jsHash21(ix, iy), b = jsHash21(ix + 1, iy);
  const c = jsHash21(ix, iy + 1), d = jsHash21(ix + 1, iy + 1);
  const top = a + (b - a) * fx, bot = c + (d - c) * fx;
  return (top + (bot - top) * fy) * 2 - 1;
}
const jsSmoothstep = (a, b, v) => {
  const t = Math.max(0, Math.min(1, (v - a) / (b - a)));
  return t * t * (3 - 2 * t);
};
const jsMix = (a, b, t) => a + (b - a) * t;

function jsBathyRaw(x, z, breakType, shallow, hand) {
  x *= hand;
  const zEff = z + 16 * jsVnoise(x * 0.009, 2.7);
  let d = 6.5 + 0.095 * zEff;
  if (breakType < 0.5) {
    const slab = Math.exp(-Math.pow(x + 14, 2) / 5200 - Math.pow(z - 42, 2) / 3400);
    d = jsMix(d, shallow, slab);
  } else if (breakType < 1.5) {
    const u = z * 0.82 + x * 0.57;
    d = jsMix(shallow - 7, 32, jsSmoothstep(-110, 210, u + 12 * jsVnoise(u * 0.01, 5.1)));
  } else if (breakType < 2.5) {
    const bar = Math.exp(-Math.pow(z - 48, 2) / 2200) * (0.62 + 0.38 * Math.sin(x * 0.045 + 1.3));
    d = jsMix(d, shallow, bar);
  } else if (breakType < 3.5) {
    const u = (z - 20) + Math.abs(x - 15) * 0.6;
    d = jsMix(shallow - 7, 32, jsSmoothstep(-115, 205, u));
  } else {
    d = 8 + 0.16 * zEff;
    const ledge = Math.exp(-Math.pow(z - 80, 2) / 4200);
    d = jsMix(d, shallow + 2.5, ledge);
  }
  return d;
}

function jsTerrainH(x, z, breakType, shallow, hand) {
  let g = -jsBathyRaw(x, z, breakType, shallow, hand);
  const up = Math.max(g, 0);
  g += up * 0.8;
  g += (0.9 * jsVnoise(x * 0.045, z * 0.045) + 0.35 * jsVnoise(x * 0.11, z * 0.11))
     * jsSmoothstep(0.5, 5.0, up);
  return g;
}

class OceanSim {
  constructor(canvas) {
    this.canvas = canvas;
    this.gl = canvas.getContext("webgl", { antialias: false, alpha: false })
           || canvas.getContext("experimental-webgl");
    if (!this.gl) throw new Error("WebGL is not available in this browser");
    this.yaw = 0;
    this.pitch = -0.05;
    this.pos = [0, 2.0, 0];
    this.keys = {};
    this.mv = {};             // touch/on-screen pad state
    this.resScale = 0.75;     // adaptive render resolution
    this.ftEMA = 16;
    this.frameCount = 0;
    this.lastFrame = 0;
    this.running = false;
    this.t0 = performance.now();
    this.cond = null;
    this._build();
    this._buildFoam();
    this._bindInput();
    this._onResize = () => this.resize();
    window.addEventListener("resize", this._onResize);
    this.resize();
  }

  _compile(type, src) {
    const gl = this.gl;
    const sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      throw new Error("Shader compile error: " + gl.getShaderInfoLog(sh));
    }
    return sh;
  }

  _program(fsSrc, names) {
    const gl = this.gl;
    const prog = gl.createProgram();
    gl.attachShader(prog, this._compile(gl.VERTEX_SHADER, OCEAN_VS));
    gl.attachShader(prog, this._compile(gl.FRAGMENT_SHADER, fsSrc));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      throw new Error("Shader link error: " + gl.getProgramInfoLog(prog));
    }
    const u = {};
    for (const n of names) u[n] = gl.getUniformLocation(prog, n);
    return { prog, u };
  }

  _build() {
    const gl = this.gl;
    const common = ["uTime", "uAmp", "uK", "uSwellDir", "uWindDir", "uChop",
                    "uBreakType", "uShallow", "uSet", "uHand", "uFoamOrigin", "uFoamSize"];
    this.main = this._program(OCEAN_FS,
      common.concat(["uRes", "uLook", "uCamPos", "uSunDir", "uCloud", "uFoamTex", "uFlowTex"]));
    this.foam = this._program(FOAM_FS,
      common.concat(["uFoamPrev", "uFoamRes", "uDt"]));
    this.flow = this._program(FLOW_FS,
      common.concat(["uFlowPrev", "uFoamRes", "uDt", "uReset"]));

    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    for (const p of [this.main.prog, this.foam.prog, this.flow.prog]) {
      gl.useProgram(p);
      const loc = gl.getAttribLocation(p, "aPos");
      gl.enableVertexAttribArray(loc);
      gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    }
    // Kept for callers that probe whether the shader built.
    this.prog = this.main.prog;
  }

  // Ping-pong RGBA8 targets: [0..1] surf state (foam/wetness), [2..3] flow.
  _buildFoam() {
    const gl = this.gl;
    this.fbo = [];
    this.tex = [];
    for (let i = 0; i < 4; i++) {
      const t = gl.createTexture();
      gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, FOAM_RES, FOAM_RES, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      const f = gl.createFramebuffer();
      gl.bindFramebuffer(gl.FRAMEBUFFER, f);
      gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0);
      if (gl.checkFramebufferStatus(gl.FRAMEBUFFER) !== gl.FRAMEBUFFER_COMPLETE) {
        this.foamOk = false;
        gl.bindFramebuffer(gl.FRAMEBUFFER, null);
        return;
      }
      this.tex.push(t);
      this.fbo.push(f);
    }
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    this.foamOk = true;
    this.src = 0;
    this.fsrc = 2;
  }

  _clearFoam() {
    if (!this.foamOk) return;
    const gl = this.gl;
    for (let i = 0; i < 2; i++) {
      gl.bindFramebuffer(gl.FRAMEBUFFER, this.fbo[i]);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
    }
    // Flow targets start at the resting grid (needs the shader to encode it).
    const fl = this.flow;
    gl.useProgram(fl.prog);
    gl.viewport(0, 0, FOAM_RES, FOAM_RES);
    this._setCommon(fl.u, this._params(0));
    gl.uniform2f(fl.u.uFoamRes, FOAM_RES, FOAM_RES);
    gl.uniform1f(fl.u.uReset, 1.0);
    for (let i = 2; i < 4; i++) {
      gl.bindFramebuffer(gl.FRAMEBUFFER, this.fbo[i]);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
    gl.uniform1f(fl.u.uReset, 0.0);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  }

  _bindInput() {
    const el = this.canvas;
    let dragging = false, lx = 0, ly = 0;
    const down = (x, y) => { dragging = true; lx = x; ly = y; };
    const move = (x, y) => {
      if (!dragging) return;
      this.yaw -= (x - lx) * 0.004;
      this.pitch += (y - ly) * 0.004;
      this.pitch = Math.max(-1.2, Math.min(0.7, this.pitch));
      lx = x; ly = y;
    };
    el.addEventListener("mousedown", e => down(e.clientX, e.clientY));
    window.addEventListener("mousemove", e => move(e.clientX, e.clientY));
    window.addEventListener("mouseup", () => { dragging = false; });
    el.addEventListener("touchstart", e => { const t = e.touches[0]; down(t.clientX, t.clientY); }, { passive: true });
    el.addEventListener("touchmove", e => { const t = e.touches[0]; move(t.clientX, t.clientY); }, { passive: true });
    el.addEventListener("touchend", () => { dragging = false; });

    const KEYS = ["KeyW", "KeyA", "KeyS", "KeyD", "KeyQ", "KeyE",
                  "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "ShiftLeft", "ShiftRight"];
    window.addEventListener("keydown", e => {
      if (!this.running) return;
      if (KEYS.includes(e.code)) { this.keys[e.code] = true; e.preventDefault(); }
    });
    window.addEventListener("keyup", e => { this.keys[e.code] = false; });
  }

  // On-screen pad hook: name in {fwd, back, left, right, up, down}.
  setMove(name, on) { this.mv[name] = on; }

  // cond: { waveHeightM, wavePeriodS, swellRelDeg (travel dir rel. to camera
  // forward), windRelDeg (blowing-toward, rel.), windSpeedMs, offshore,
  // sunElevRad, sunAzimRelRad, cloudCover (0..1), breakType (spot type) }
  setConditions(cond) {
    this.updateConditions(cond);
    const amp = Math.max(0.15, cond.waveHeightM / 2);
    // Surfer's-eye default vantage; fly with Q/E for the drone view.
    this.pos = [0, Math.max(1.5, amp * 1.1 + 0.7), 0];
    this.keys = {};
    this.mv = {};
    this._clearFoam();
    this.warmup = 90;   // seed the surf state so foam exists on the first frame
  }

  // Swap the sea state without moving the camera or wiping foam history —
  // used when scrubbing the forecast.
  updateConditions(cond) {
    this.cond = cond;
    this.breakId = BREAK_TYPE_IDS[cond.breakType] ?? 2;
    this.shallow = Math.max(0.8, Math.min(5.0, cond.waveHeightM * 0.9));
    this.hand = cond.hand === "left" ? -1 : 1;
  }

  resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    const w = Math.round(this.canvas.clientWidth * dpr * this.resScale);
    const h = Math.round(this.canvas.clientHeight * dpr * this.resScale);
    if (w && h && (this.canvas.width !== w || this.canvas.height !== h)) {
      this.canvas.width = w;
      this.canvas.height = h;
    }
  }

  start() {
    if (this.running) return;
    this.running = true;
    this.lastFrame = performance.now();
    const loop = () => {
      if (!this.running) return;
      this._frame();
      this.raf = requestAnimationFrame(loop);
    };
    this.raf = requestAnimationFrame(loop);
  }

  stop() {
    this.running = false;
    if (this.raf) cancelAnimationFrame(this.raf);
  }

  destroy() {
    this.stop();
    window.removeEventListener("resize", this._onResize);
  }

  _updateCamera(dt) {
    const k = this.keys, m = this.mv;
    const fwd = (k.KeyW || k.ArrowUp || m.fwd ? 1 : 0) - (k.KeyS || k.ArrowDown || m.back ? 1 : 0);
    const str = (k.KeyD || k.ArrowRight || m.right ? 1 : 0) - (k.KeyA || k.ArrowLeft || m.left ? 1 : 0);
    const ver = (k.KeyE || m.up ? 1 : 0) - (k.KeyQ || m.down ? 1 : 0);
    if (!fwd && !str && !ver) return;
    const speed = (k.ShiftLeft || k.ShiftRight ? 21 : 7) * dt;
    const sy = Math.sin(this.yaw), cy = Math.cos(this.yaw);
    this.pos[0] += (sy * fwd + cy * str) * speed;
    this.pos[2] += (cy * fwd - sy * str) * speed;
    this.pos[1] = Math.max(1.2, Math.min(80, this.pos[1] + ver * speed));
    // Never sink into the sand: stay a head above the beach and dunes.
    const ground = jsTerrainH(this.pos[0], this.pos[2], this.breakId, this.shallow, this.hand);
    if (this.pos[1] < ground + 1.6) this.pos[1] = ground + 1.6;
  }

  _adaptQuality(dtMs) {
    this.ftEMA = this.ftEMA * 0.95 + dtMs * 0.05;
    if (++this.frameCount % 60 !== 0) return;
    if (this.ftEMA > 30 && this.resScale > 0.45) { this.resScale -= 0.1; this.resize(); }
    else if (this.ftEMA < 14 && this.resScale < 0.85) { this.resScale += 0.05; this.resize(); }
  }

  // Wave/scene parameters shared by both passes.
  _params(now) {
    const c = this.cond;
    const amp = Math.max(0.15, c.waveHeightM / 2);
    // Deep-water wavelength L = g T^2 / 2pi, shoaled to 45% so long-period
    // swell reads as surfable walls instead of near-flat rollers.
    const T = Math.max(4, Math.min(22, c.wavePeriodS || 10));
    const L = Math.max(18, Math.min(240, 1.561 * T * T * 0.45));
    const k = (2 * Math.PI) / L;
    const swellRad = (c.swellRelDeg * Math.PI) / 180;
    const windRad = (c.windRelDeg * Math.PI) / 180;
    let chop = Math.min(1, (c.windSpeedMs || 0) / 13);
    if (c.offshore) chop *= 0.35; // offshore wind grooms the face
    return { amp, k, swellRad, windRad, chop, now };
  }

  _setCommon(u, p) {
    const gl = this.gl;
    gl.uniform1f(u.uTime, p.now);
    gl.uniform1f(u.uAmp, p.amp);
    gl.uniform1f(u.uK, p.k);
    gl.uniform2f(u.uSwellDir, Math.sin(p.swellRad), Math.cos(p.swellRad));
    gl.uniform2f(u.uWindDir, Math.sin(p.windRad), Math.cos(p.windRad));
    gl.uniform1f(u.uChop, p.chop);
    gl.uniform1f(u.uBreakType, this.breakId);
    gl.uniform1f(u.uShallow, this.shallow);
    gl.uniform1f(u.uSet, 1.0);
    gl.uniform1f(u.uHand, this.hand);
    gl.uniform2f(u.uFoamOrigin, FOAM_ORIGIN[0], FOAM_ORIGIN[1]);
    gl.uniform2f(u.uFoamSize, FOAM_SIZE[0], FOAM_SIZE[1]);
  }

  // One surf-state step. `atTime` lets the warm-up march the state forward
  // before the first visible frame.
  _foamStep(dt, atTime) {
    const gl = this.gl;
    const { prog, u } = this.foam;
    gl.useProgram(prog);
    gl.bindFramebuffer(gl.FRAMEBUFFER, this.fbo[1 - this.src]);
    gl.viewport(0, 0, FOAM_RES, FOAM_RES);
    this._setCommon(u, this._params(atTime));
    gl.uniform2f(u.uFoamRes, FOAM_RES, FOAM_RES);
    gl.uniform1f(u.uDt, dt);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, this.tex[this.src]);
    gl.uniform1i(u.uFoamPrev, 0);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    this.src = 1 - this.src;

    const fl = this.flow;
    gl.useProgram(fl.prog);
    const fdst = this.fsrc === 2 ? 3 : 2;
    gl.bindFramebuffer(gl.FRAMEBUFFER, this.fbo[fdst]);
    this._setCommon(fl.u, this._params(atTime));
    gl.uniform2f(fl.u.uFoamRes, FOAM_RES, FOAM_RES);
    gl.uniform1f(fl.u.uDt, dt);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, this.tex[this.fsrc]);
    gl.uniform1i(fl.u.uFlowPrev, 0);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
    this.fsrc = fdst;
  }

  _frame() {
    const gl = this.gl, c = this.cond;
    if (!c) return;
    const nowMs = performance.now();
    const dt = Math.min(0.05, (nowMs - this.lastFrame) / 1000);
    this._adaptQuality(nowMs - this.lastFrame);
    this.lastFrame = nowMs;
    this._updateCamera(dt);
    this.resize();

    const now = (nowMs - this.t0) / 1000;

    if (this.foamOk) {
      if (this.warmup > 0) {
        // March the surf state forward so the first frame already has foam.
        const step = 1 / 20;
        for (let i = this.warmup; i > 0; i--) this._foamStep(step, now - i * step);
        this.warmup = 0;
      }
      this._foamStep(Math.max(dt, 1 / 120), now);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    }

    const { prog, u } = this.main;
    gl.useProgram(prog);
    gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    this._setCommon(u, this._params(now));

    const se = c.sunElevRad, sa = c.sunAzimRelRad;
    const sun = [Math.sin(sa) * Math.cos(se), Math.sin(se), Math.cos(sa) * Math.cos(se)];
    gl.uniform2f(u.uRes, this.canvas.width, this.canvas.height);
    gl.uniform2f(u.uLook, this.yaw, this.pitch);
    gl.uniform3f(u.uCamPos, this.pos[0], this.pos[1], this.pos[2]);
    gl.uniform3f(u.uSunDir, sun[0], sun[1], sun[2]);
    gl.uniform1f(u.uCloud, Math.max(0, Math.min(1, c.cloudCover || 0)));
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, this.foamOk ? this.tex[this.src] : null);
    gl.uniform1i(u.uFoamTex, 0);
    gl.activeTexture(gl.TEXTURE1);
    gl.bindTexture(gl.TEXTURE_2D, this.foamOk ? this.tex[this.fsrc] : null);
    gl.uniform1i(u.uFlowTex, 1);

    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
}
