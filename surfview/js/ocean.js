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
// shore. Break depth scales with today's swell; sets arrive on a slow
// envelope with lulls between them.
//
// The camera is free: drag to look, WASD to move, Q/E for height — paddle
// into the barrel or climb above the reef and watch it peel. The sun sits
// where it really is at the spot right now.

const OCEAN_VS = `
attribute vec2 aPos;
void main() { gl_Position = vec4(aPos, 0.0, 1.0); }
`;

const OCEAN_FS = `
precision highp float;

uniform vec2  uRes;
uniform float uTime;
uniform vec2  uLook;      // yaw, pitch in radians
uniform vec3  uCamPos;    // camera position (m); origin is the takeoff zone
uniform float uAmp;       // deep-water swell amplitude (m) — half the height
uniform float uK;         // primary wavenumber, 2*pi / wavelength
uniform vec2  uSwellDir;  // unit vector, direction swell TRAVELS (camera frame, +z = out to sea)
uniform vec2  uWindDir;   // unit vector, direction wind blows toward (camera frame)
uniform float uChop;      // 0..1 wind-chop energy
uniform vec3  uSunDir;    // unit vector toward the sun (camera frame)
uniform float uCloud;     // 0..1 cloud cover
uniform float uBreakType; // 0 reef, 1 point, 2 beach, 3 river-mouth, 4 big-wave
uniform float uShallow;   // shallowest depth over the break (m), scaled to swell
uniform float uSet;       // slow set envelope, ~0.6..1.0

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
  float x = p.x, z = p.y;
  float zEff = z + 16.0 * vnoise(vec2(x * 0.009, 2.7)); // shoreline waviness
  float d = 6.5 + 0.095 * zEff;                          // shore ~68 m behind camera
  if (uBreakType < 0.5) {
    // Reef pass: shallow slab just ahead-left, deep channel under the camera.
    float slab = exp(-pow(x + 14.0, 2.0) / 5200.0 - pow(z - 42.0, 2.0) / 3400.0);
    d = mix(d, uShallow, slab);
  } else if (uBreakType < 1.5) {
    // Point: depth contours angled ~35 deg so the break peels across view.
    float u = z * 0.82 + x * 0.57;
    d = mix(uShallow - 7.0, 32.0, smoothstep(-52.0, 250.0, u + 12.0 * vnoise(vec2(u * 0.01, 5.1))));
  } else if (uBreakType < 2.5) {
    // Beach: outer sandbar with rip-channel gaps, shallower trough inside.
    float bar = exp(-pow(z - 48.0, 2.0) / 2200.0) * (0.62 + 0.38 * sin(x * 0.045 + 1.3));
    d = mix(d, uShallow, bar);
  } else if (uBreakType < 3.5) {
    // River mouth: tapered wedge of sand raked off the rivermouth.
    float u = (z - 20.0) + abs(x - 15.0) * 0.6;
    d = mix(uShallow - 7.0, 32.0, smoothstep(-60.0, 240.0, u));
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
  h += lean * 1.0 * pow(s, sharp * 0.6) * sin(x * 2.0 + 1.1);
  return amp * h;
}

// Shoaled swell amplitude and breaking parameter at a point.
void surfState(float d, out float aSw, out float gam, out float steep) {
  float dw = max(d, 0.7);
  aSw = uAmp * uSet * shoalGain(dw) * smoothstep(0.0, 1.5, d);
  gam = 2.0 * aSw / dw;
  // Waves jack up hard right at the brink, then dump energy shoreward.
  aSw *= 1.0 + 1.0 * smoothstep(0.5, 0.85, gam) * (1.0 - smoothstep(1.05, 1.5, gam));
  aSw *= mix(1.0, 0.42, smoothstep(1.15, 2.0, gam));
  steep = smoothstep(0.35, 0.85, gam);
}

float waveField(vec2 p, float d, bool detail) {
  float aSw, gam, steep;
  surfState(d, aSw, gam, steep);
  float h = 0.0;
  h += dwave(p, uSwellDir,              uK,        aSw  * 0.62, 2.8 + 3.6 * steep, 0.0, steep);
  h += dwave(p, rot2(uSwellDir,  0.26), uK * 1.31, aSw  * 0.22, 2.2 + 2.2 * steep, 1.7, steep * 0.7);
  h += dwave(p, rot2(uSwellDir, -0.33), uK * 0.77, uAmp * 0.16 * smoothstep(0.0, 1.2, d), 2.0, 4.1, 0.0);
  float ca = uChop;
  h += dwave(p, uWindDir,               uK * 4.1,  (uAmp * 0.09 + 0.03) * ca, 1.7, 2.3, 0.0);
  h += dwave(p, rot2(uWindDir,  0.85),  uK * 7.7,  (uAmp * 0.05 + 0.02) * ca, 1.5, 5.9, 0.0);
  if (detail) {
    h += dwave(p, rot2(uWindDir, -1.2), uK * 14.3, (uAmp * 0.025 + 0.012) * ca, 1.3, 3.3, 0.0);
    h += 0.018 * (0.4 + ca) * vnoise(p * 2.7 + uTime * 0.6);
    h += 0.010 * (0.4 + ca) * vnoise(p * 6.3 - uTime * 0.9);
  }
  return h;
}

// Water surface as a 3D SDF. In the breaking window a thrown lip (solid
// tube of water) is blended onto the crest and a barrel cavity is carved
// beneath it, both phase-locked to the moving primary swell, so the wave
// visibly curls over a hollow tube where the bottom says it should.
float waterSDF(vec3 p, bool detail) {
  float d = bathyRaw(p.xz);
  float f = p.y - waveField(p.xz, d, detail);

  float aSw, gam, steep;
  surfState(d, aSw, gam, steep);
  float brl = smoothstep(0.60, 0.85, gam) * (1.0 - smoothstep(1.25, 1.6, gam));
  if (brl > 0.02) {
    float s = dot(p.xz, uSwellDir);
    float x = s * uK - uTime * sqrt(G * uK);
    float pd = (fract((x - 1.5708) / 6.28318 + 0.5) - 0.5) * 6.28318; // phase offset from crest
    float ds = pd / uK;                                               // meters ahead of crest
    float R  = max(aSw * 0.85 * brl, 0.02);                           // barrel radius
    float yc = aSw * 0.95;                                            // crest height estimate
    vec2 q = vec2(ds, p.y);
    float cav = length(q - vec2(R * 0.60, yc - R * 0.90)) - R;
    float lip = length(q - vec2(R * 1.10, yc - R * 0.18)) - R * 0.45;
    f = smin2(f, lip, R * 0.35);
    f = smax2(f, -cav, R * 0.30);
  }
  return f;
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

// Scene SDF: water or sand, whichever is closer. Distances are damped to
// stay conservative against steep wave faces.
float mapScene(vec3 p, bool detail, out float mat) {
  float fw = waterSDF(p, detail) * 0.42;
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
  surfState(d, aSw, gam, steep);

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

  // Foam: crest foam on steep unbroken waves, the breaking lip on the
  // shoreward face (and the falling underside of the curl), rolling
  // whitewater shoreward of the break, wind streaks.
  float crest = smoothstep(uAmp * 0.45, uAmp * 1.05, p.y) * smoothstep(0.88, 0.55, n.y);
  float front = clamp(dot(vec2(n.x, n.z), -uSwellDir) * 3.0 + 0.4, 0.0, 1.0);
  float lipF = smoothstep(0.68, 0.98, gam) * smoothstep(aSw * 0.2, aSw * 0.75, p.y) * front;
  float under = smoothstep(0.05, -0.45, n.y) * smoothstep(0.55, 0.9, gam); // curl underside
  float white = smoothstep(1.05, 1.55, gam) * 0.85;
  float streaks = uChop * 0.25 * smoothstep(0.3, 0.9, vnoise(p.xz * 0.9 + uTime * 0.2));
  float tex = 0.55 + 0.45 * vnoise(p.xz * 6.0 + uTime * 0.7);
  float foam = clamp((crest + streaks * crest) * tex + (lipF + under * 0.8) * (0.6 + 0.6 * tex) + white * tex, 0.0, 1.0);
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

  vec3 dry = vec3(0.78, 0.68, 0.52), wet = vec3(0.42, 0.36, 0.29);
  float wetBand = smoothstep(1.5, 0.25, p.y);
  vec3 c = mix(dry, wet, wetBand);
  // Dune grass creeping over the higher sand.
  float grass = smoothstep(4.0, 9.0, p.y) * smoothstep(0.55, 0.9, n.y);
  c = mix(c, vec3(0.30, 0.38, 0.22), grass * 0.8);
  c *= 0.85 + 0.15 * vnoise(p.xz * 0.9);

  float dif = clamp(dot(n, uSunDir), 0.0, 1.0);
  vec3 col = c * light * (0.35 + 0.75 * dif);

  // Sheets of foam running up the wet sand.
  float ru = smoothstep(0.6, 0.05, abs(p.y - 0.12))
           * smoothstep(0.35, 0.9, vnoise(p.xz * 0.45 + vec2(0.0, uTime * 0.35)));
  col = mix(col, vec3(0.9) * light, ru * 0.8);
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

  vec3 col;
  vec2 hit = (rd.y > 0.45 && ro.y < 40.0) ? vec2(-1.0, 0.0) : traceScene(ro, rd);
  if (hit.x < 0.0) {
    col = skyColor(rd);
  } else {
    vec3 p = ro + rd * hit.x;
    vec3 n = calcNormal(p, hit.x);
    col = (hit.y > 0.5) ? sandColor(p, n, hit.x) : waterColor(p, n, rd, hit.x);
    // Aerial perspective toward the horizon.
    float fog = 1.0 - exp(-hit.x * 0.0011);
    col = mix(col, skyColor(vec3(rd.x, abs(rd.y) * 0.15, rd.z)), fog);
  }

  // Vignette + gamma.
  col *= 1.0 - 0.25 * dot(uv * 0.55, uv * 0.55);
  col = pow(max(col, 0.0), vec3(0.4545));
  gl_FragColor = vec4(col, 1.0);
}
`;

const BREAK_TYPE_IDS = { "reef": 0, "point": 1, "beach": 2, "river-mouth": 3, "big-wave": 4 };

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
    this.uniforms = {};
    this.cond = null;
    this._build();
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

  _build() {
    const gl = this.gl;
    const prog = gl.createProgram();
    gl.attachShader(prog, this._compile(gl.VERTEX_SHADER, OCEAN_VS));
    gl.attachShader(prog, this._compile(gl.FRAGMENT_SHADER, OCEAN_FS));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      throw new Error("Shader link error: " + gl.getProgramInfoLog(prog));
    }
    gl.useProgram(prog);
    this.prog = prog;

    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prog, "aPos");
    gl.enableVertexAttribArray(loc);
    gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);

    for (const name of ["uRes", "uTime", "uLook", "uCamPos", "uAmp", "uK",
                        "uSwellDir", "uWindDir", "uChop", "uSunDir", "uCloud",
                        "uBreakType", "uShallow", "uSet"]) {
      this.uniforms[name] = gl.getUniformLocation(prog, name);
    }
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
    this.cond = cond;
    const amp = Math.max(0.15, cond.waveHeightM / 2);
    // Surfer's-eye default vantage; fly with Q/E for the drone view.
    this.pos = [0, Math.max(1.5, amp * 1.1 + 0.7), 0];
    this.keys = {};
    this.mv = {};
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
  }

  _adaptQuality(dtMs) {
    this.ftEMA = this.ftEMA * 0.95 + dtMs * 0.05;
    if (++this.frameCount % 60 !== 0) return;
    if (this.ftEMA > 30 && this.resScale > 0.45) { this.resScale -= 0.1; this.resize(); }
    else if (this.ftEMA < 14 && this.resScale < 0.85) { this.resScale += 0.05; this.resize(); }
  }

  _frame() {
    const gl = this.gl, u = this.uniforms, c = this.cond;
    if (!c) return;
    const nowMs = performance.now();
    const dt = Math.min(0.05, (nowMs - this.lastFrame) / 1000);
    this._adaptQuality(nowMs - this.lastFrame);
    this.lastFrame = nowMs;
    this._updateCamera(dt);
    this.resize();
    gl.viewport(0, 0, this.canvas.width, this.canvas.height);

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

    const se = c.sunElevRad, sa = c.sunAzimRelRad;
    const sun = [Math.sin(sa) * Math.cos(se), Math.sin(se), Math.cos(sa) * Math.cos(se)];

    const now = (nowMs - this.t0) / 1000;
    // Sets roll through every ~26 s so a session shows lulls and bombs.
    const setEnv = 0.78 + 0.22 * Math.sin((now * 2 * Math.PI) / 26 + 1.0);
    // The break's shallowest depth tracks the swell so today's size breaks
    // over it — bigger days break wider and further out.
    const shallow = Math.max(0.8, Math.min(5.0, c.waveHeightM * 0.9));

    gl.uniform2f(u.uRes, this.canvas.width, this.canvas.height);
    gl.uniform1f(u.uTime, now);
    gl.uniform2f(u.uLook, this.yaw, this.pitch);
    gl.uniform3f(u.uCamPos, this.pos[0], this.pos[1], this.pos[2]);
    gl.uniform1f(u.uAmp, amp);
    gl.uniform1f(u.uK, k);
    gl.uniform2f(u.uSwellDir, Math.sin(swellRad), Math.cos(swellRad));
    gl.uniform2f(u.uWindDir, Math.sin(windRad), Math.cos(windRad));
    gl.uniform1f(u.uChop, chop);
    gl.uniform3f(u.uSunDir, sun[0], sun[1], sun[2]);
    gl.uniform1f(u.uCloud, Math.max(0, Math.min(1, c.cloudCover || 0)));
    gl.uniform1f(u.uBreakType, BREAK_TYPE_IDS[c.breakType] ?? 2);
    gl.uniform1f(u.uShallow, shallow);
    gl.uniform1f(u.uSet, setEnv);

    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
}
