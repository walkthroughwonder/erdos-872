// OceanSim — first-person WebGL ocean, raymarched in a fragment shader.
//
// The wave field is an original sum-of-directional-waves heightfield:
//   * three "swell" components clustered around the real swell direction,
//     with wavelength derived from the reported period via deep-water
//     dispersion (L = g*T^2 / 2pi, shoaled for visual realism),
//   * three high-frequency "chop" components aligned with the wind,
//     scaled by wind speed (suppressed when the wind blows offshore),
//   * a fine value-noise ripple for surface texture.
// Rays are intersected with the heightfield by bracketed bisection, then
// shaded with a fresnel mix of sky reflection, depth/subsurface color,
// sun glint and crest foam. The sun's screen position comes from the real
// solar elevation/azimuth at the spot, so dawn patrol looks like dawn.

const OCEAN_VS = `
attribute vec2 aPos;
void main() { gl_Position = vec4(aPos, 0.0, 1.0); }
`;

const OCEAN_FS = `
precision highp float;

uniform vec2  uRes;
uniform float uTime;
uniform vec2  uLook;     // yaw, pitch in radians
uniform float uCamH;     // camera height above mean sea level (m)
uniform float uAmp;      // swell amplitude (m) — half the significant height
uniform float uK;        // primary wavenumber, 2*pi / wavelength
uniform vec2  uSwellDir; // unit vector, direction swell TRAVELS (camera frame, +z = out to sea)
uniform vec2  uWindDir;  // unit vector, direction wind blows toward (camera frame)
uniform float uChop;     // 0..1 wind-chop energy
uniform vec3  uSunDir;   // unit vector toward the sun (camera frame)
uniform float uCloud;    // 0..1 cloud cover

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

// One directional wave with a sharpened (peaky) crest profile.
// Phase speed follows deep-water dispersion: omega = sqrt(g * k).
float dwave(vec2 p, vec2 dir, float k, float amp, float sharp, float phase) {
  float w = sqrt(G * k);
  float x = dot(p, dir) * k - uTime * w + phase;
  float s = 0.5 + 0.5 * sin(x);
  return amp * (pow(s, sharp) * 2.0 - 0.7);
}

float seaHeight(vec2 p, bool detail) {
  float h = 0.0;
  // Swell: dominant component plus two slightly rotated sidebands so the
  // lines aren't perfectly parallel corduroy.
  h += dwave(p, uSwellDir,              uK,        uAmp * 0.60, 2.8, 0.0);
  h += dwave(p, rot2(uSwellDir,  0.26), uK * 1.31, uAmp * 0.24, 2.2, 1.7);
  h += dwave(p, rot2(uSwellDir, -0.33), uK * 0.77, uAmp * 0.18, 2.0, 4.1);
  // Wind chop.
  float ca = uChop;
  h += dwave(p, uWindDir,               uK * 4.1,  (uAmp * 0.09 + 0.03) * ca, 1.7, 2.3);
  h += dwave(p, rot2(uWindDir,  0.85),  uK * 7.7,  (uAmp * 0.05 + 0.02) * ca, 1.5, 5.9);
  if (detail) {
    h += dwave(p, rot2(uWindDir, -1.2), uK * 14.3, (uAmp * 0.025 + 0.012) * ca, 1.3, 3.3);
    h += 0.018 * (0.4 + ca) * vnoise(p * 2.7 + uTime * 0.6);
    h += 0.010 * (0.4 + ca) * vnoise(p * 6.3 - uTime * 0.9);
  }
  return h;
}

// Bracketed bisection against the heightfield. Returns distance, or a
// negative value when the ray never reaches the water.
float traceWater(vec3 ro, vec3 rd, out vec3 hit) {
  float tNear = 0.1, tFar = 1600.0;
  vec3 pFar = ro + rd * tFar;
  float hFar = pFar.y - seaHeight(pFar.xz, false);
  if (hFar > 0.0) { hit = pFar; return -1.0; }
  float hNear = ro.y - seaHeight(ro.xz, false);
  float tMid = tNear;
  for (int i = 0; i < 12; i++) {
    tMid = mix(tNear, tFar, hNear / (hNear - hFar));
    hit = ro + rd * tMid;
    float hMid = hit.y - seaHeight(hit.xz, false);
    if (hMid < 0.0) { tFar = tMid; hFar = hMid; }
    else            { tNear = tMid; hNear = hMid; }
  }
  return tMid;
}

vec3 seaNormal(vec3 p, float eps) {
  float h  = seaHeight(p.xz, true);
  float hx = seaHeight(p.xz + vec2(eps, 0.0), true);
  float hz = seaHeight(p.xz + vec2(0.0, eps), true);
  return normalize(vec3(h - hx, eps, h - hz));
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

  vec3 deep = vec3(0.015, 0.075, 0.11) * light;
  vec3 sub  = vec3(0.06, 0.32, 0.30) * light;
  float dif = max(dot(n, uSunDir), 0.0);
  float hFac = clamp((p.y + uAmp) / max(2.0 * uAmp, 0.4), 0.0, 1.0);
  vec3 body = mix(deep, sub, hFac * (0.35 + 0.65 * dif));

  vec3 col = mix(body, refl, fres);

  // Sun glint.
  float spec = pow(max(dot(reflect(rd, n), uSunDir), 0.0), 220.0);
  vec3 sunTint = mix(vec3(1.0, 0.6, 0.3), vec3(1.0, 0.97, 0.9), day);
  col += sunTint * spec * (1.5 + dist * 0.02) * smoothstep(-0.06, 0.02, elev);

  // Crest foam: tall + steep, textured with noise, plus wind-driven streaks.
  float crest = smoothstep(uAmp * 0.45, uAmp * 1.05, p.y) * smoothstep(0.88, 0.55, n.y);
  float streaks = uChop * 0.25 * smoothstep(0.3, 0.9, vnoise(p.xz * 0.9 + uTime * 0.2));
  float foam = clamp(crest * (0.55 + 0.45 * vnoise(p.xz * 6.0 + uTime * 0.7)) + streaks * crest, 0.0, 1.0);
  foam *= exp(-dist * 0.004);
  col = mix(col, vec3(0.92, 0.95, 0.97) * (0.15 + 0.85 * light), foam);

  return col;
}

void main() {
  vec2 uv = (gl_FragCoord.xy * 2.0 - uRes) / uRes.y;

  float yaw = uLook.x, pitch = uLook.y;
  vec3 fwd = vec3(sin(yaw) * cos(pitch), sin(pitch), cos(yaw) * cos(pitch));
  vec3 right = normalize(vec3(cos(yaw), 0.0, -sin(yaw)));
  vec3 up = cross(fwd, right);
  vec3 rd = normalize(fwd + uv.x * right * 0.9 + uv.y * up * 0.9);
  vec3 ro = vec3(0.0, uCamH, 0.0);

  vec3 col;
  vec3 hit;
  float t = (rd.y > 0.12) ? -1.0 : traceWater(ro, rd, hit);
  if (t < 0.0) {
    col = skyColor(rd);
  } else {
    vec3 n = seaNormal(hit, 0.05 + t * t * 0.00012);
    col = waterColor(hit, n, rd, t);
    // Aerial perspective toward the horizon.
    float fog = 1.0 - exp(-t * 0.0016);
    col = mix(col, skyColor(vec3(rd.x, abs(rd.y) * 0.15, rd.z)), fog);
  }

  // Vignette + gamma.
  col *= 1.0 - 0.25 * dot(uv * 0.55, uv * 0.55);
  col = pow(max(col, 0.0), vec3(0.4545));
  gl_FragColor = vec4(col, 1.0);
}
`;

class OceanSim {
  constructor(canvas) {
    this.canvas = canvas;
    this.gl = canvas.getContext("webgl", { antialias: false, alpha: false })
           || canvas.getContext("experimental-webgl");
    if (!this.gl) throw new Error("WebGL is not available in this browser");
    this.yaw = 0;
    this.pitch = -0.05;
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

    for (const name of ["uRes", "uTime", "uLook", "uCamH", "uAmp", "uK",
                        "uSwellDir", "uWindDir", "uChop", "uSunDir", "uCloud"]) {
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
      this.pitch = Math.max(-0.9, Math.min(0.6, this.pitch));
      lx = x; ly = y;
    };
    el.addEventListener("mousedown", e => down(e.clientX, e.clientY));
    window.addEventListener("mousemove", e => move(e.clientX, e.clientY));
    window.addEventListener("mouseup", () => { dragging = false; });
    el.addEventListener("touchstart", e => { const t = e.touches[0]; down(t.clientX, t.clientY); }, { passive: true });
    el.addEventListener("touchmove", e => { const t = e.touches[0]; move(t.clientX, t.clientY); }, { passive: true });
    el.addEventListener("touchend", () => { dragging = false; });
  }

  // cond: { waveHeightM, wavePeriodS, swellRelDeg (travel dir rel. to camera
  // forward), windRelDeg (blowing-toward, rel.), windSpeedMs, offshore,
  // sunElevRad, sunAzimRelRad, cloudCover (0..1) }
  setConditions(cond) {
    this.cond = cond;
  }

  resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    // Render at 80% scale — the shader is the bottleneck, not fill quality.
    const w = Math.round(this.canvas.clientWidth * dpr * 0.8);
    const h = Math.round(this.canvas.clientHeight * dpr * 0.8);
    if (w && h && (this.canvas.width !== w || this.canvas.height !== h)) {
      this.canvas.width = w;
      this.canvas.height = h;
    }
  }

  start() {
    if (this.running) return;
    this.running = true;
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

  _frame() {
    const gl = this.gl, u = this.uniforms, c = this.cond;
    if (!c) return;
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

    gl.uniform2f(u.uRes, this.canvas.width, this.canvas.height);
    gl.uniform1f(u.uTime, (performance.now() - this.t0) / 1000);
    gl.uniform2f(u.uLook, this.yaw, this.pitch);
    gl.uniform1f(u.uCamH, Math.max(1.8, amp * 1.5 + 1.0));
    gl.uniform1f(u.uAmp, amp);
    gl.uniform1f(u.uK, k);
    gl.uniform2f(u.uSwellDir, Math.sin(swellRad), Math.cos(swellRad));
    gl.uniform2f(u.uWindDir, Math.sin(windRad), Math.cos(windRad));
    gl.uniform1f(u.uChop, chop);
    gl.uniform3f(u.uSunDir, sun[0], sun[1], sun[2]);
    gl.uniform1f(u.uCloud, Math.max(0, Math.min(1, c.cloudCover || 0)));

    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
}
