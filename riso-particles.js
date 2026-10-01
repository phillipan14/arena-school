/* ============================================================
   Arena — riso-particles.js  (homepage hero)
   The risograph print as free particles: every dot wanders on its own,
   with its own heading, speed and meander, and wraps around the edges.
   A dot's size (and whether it prints at all) comes from the ink tone
   where it is right now, so the ombre, the quiet zone around the
   headline and the fade up into the nav keep their shape while the
   dots themselves keep moving. Navy and blue ink on cream paper.
   One WebGL context, two passes (paper, then dots as points). No libraries.

   RisoParticles(el, opts) -> { set(key, value) } | null (no WebGL)
   ============================================================ */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // the ink tone at a point (device px, y up), shared by both passes
  var TONE = [
    'uniform vec2 u_res; uniform float u_ts, u_amb, u_calmS, u_top, u_navH, u_navF, u_fadeB, u_floor; uniform vec4 u_calm;',
    'float h1(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }',
    'float tone(vec2 px){',
    '  vec2 uv = px / u_res;',
    '  float a = 0.55 * (1.0 - smoothstep(-0.1, 1.15, uv.x * 0.8 + (1.0 - uv.y) * 0.5));',
    '  a += 0.30 * (0.5 + 0.5 * sin(uv.x * 2.3 + uv.y * 1.7 + u_ts * 0.07));',
    '  a += 0.20 * (0.5 + 0.5 * sin(uv.x * -1.4 + uv.y * 3.1 - u_ts * 0.05 + 1.3));',
    '  float T = u_amb * a;',
    '  vec2 hb = u_calm.zw * 0.5; float rad = 0.6 * min(hb.x, hb.y); vec2 dq = abs(px - u_calm.xy) - (hb - rad); float sd = length(max(dq, 0.0)) + min(max(dq.x, dq.y), 0.0) - rad;',
    '  float feather = 0.40 * u_res.y; float calm = u_calmS * (1.0 - smoothstep(-0.06 * u_res.y, feather, sd + 0.04 * u_res.y * sin(px.x * 0.004 + px.y * 0.006)));',
    '  float topc = u_navH > 0.0 ? smoothstep(u_res.y - u_navH - u_navF, u_res.y, px.y) : 0.0;',
    '  calm = max(calm, u_top * topc);',
    '  float fb = smoothstep(0.0, u_fadeB * u_res.y, px.y);',
    '  return clamp(max(T * (1.0 - calm) * fb, u_floor * (1.0 - 0.85 * calm)), 0.0, 0.97);',
    '}'].join('\n');

  // dots: one point per particle
  var DOT_VS = ['precision highp float;', TONE,
    'attribute vec4 a_h; attribute vec4 a_r;',   // a_h.xy = start (0..1 of the wrap box), a_h.zw / a_r = per-dot randoms
    'uniform float u_t, u_pitch, u_dot, u_dpr, u_mix, u_marg, u_vmin, u_vmax;',
    'varying float v_r, v_keep, v_blue, v_size;',
    'void main(){',
    '  vec2 box = u_res + 2.0 * u_marg;',
    '  float th = a_r.x * 6.2832;',                                     // own heading
    '  float spd = mix(u_vmin, u_vmax, a_r.y * a_r.y) * u_dpr;',          // own speed, most dots slow, a few quicker
    '  float om = (0.12 + 0.38 * a_r.z) * (a_h.w < 0.5 ? -1.0 : 1.0);',  // own meander rate and direction
    '  float R = (8.0 + 32.0 * a_h.z) * u_dpr;',                          // own meander radius
    '  float ph = a_r.w * 6.2832;',
    '  vec2 p = a_h.xy * box + vec2(cos(th), sin(th)) * spd * u_t',
    '         + R * vec2(sin(ph + om * u_t) - sin(ph), cos(ph) - cos(ph + om * u_t))',
    '         + 1.6 * u_dpr * vec2(sin(u_t * (1.1 + a_r.z) + ph * 3.0), cos(u_t * (0.9 + a_r.y) + ph * 2.0));',
    '  p = mod(p, box) - u_marg;',                                         // wrap around the edges
    '  float T = tone(p);',
    '  float hk = fract(a_r.w * 91.7 + a_h.z * 13.1);',
    '  v_keep = smoothstep(hk * 0.16, hk * 0.16 + 0.02, T);',
    '  v_r = max(sqrt(T / 3.14159), 0.17) * (0.94 + 0.12 * fract(a_r.y * 57.3)) * u_dot;',
    '  v_blue = step(fract(a_r.x * 73.1 + a_h.w * 5.3), u_mix);',
    '  v_size = v_keep > 0.01 ? ceil(2.0 * v_r + 2.0) : 0.0;',
    '  gl_PointSize = v_size;',
    '  gl_Position = v_keep > 0.01 ? vec4(p / u_res * 2.0 - 1.0, 0.0, 1.0) : vec4(2.0, 2.0, 0.0, 1.0);',
    '}'].join('\n');
  var DOT_FS = ['precision mediump float;',
    'uniform vec3 u_ink, u_ink2;',
    'varying float v_r, v_keep, v_blue, v_size;',
    'void main(){',
    '  float d = length(gl_PointCoord - 0.5) * v_size;',
    '  float a = v_keep * smoothstep(v_r + 0.75, v_r - 0.75, d);',
    '  if (a < 0.01) discard;',
    '  vec2 px = gl_FragCoord.xy;',
    '  float mott = 0.94 + 0.06 * sin(px.x * 0.013 + sin(px.y * 0.011) * 2.0) * sin(px.y * 0.017 + 1.7);',
    '  gl_FragColor = vec4(mix(u_ink, u_ink2, v_blue) * mott, a);',
    '}'].join('\n');

  // paper: a full-screen triangle, cream melting into the page beige at the bottom
  var PAPER_VS = 'attribute vec2 a_p; void main(){ gl_Position = vec4(a_p, 0.0, 1.0); }';
  var PAPER_FS = ['precision mediump float;',
    'uniform vec2 u_res; uniform vec3 u_paper, u_paper2; uniform float u_fadeB;',
    'void main(){ gl_FragColor = vec4(mix(u_paper2, u_paper, smoothstep(0.0, u_fadeB * u_res.y, gl_FragCoord.y)), 1.0); }'].join('\n');

  function hex(h) { h = h.replace('#', ''); return [0, 2, 4].map(function (i) { return parseInt(h.substr(i, 2), 16) / 255; }); }
  function prog(gl, vs, fs) {
    function sh(t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; }
    var p = gl.createProgram(); gl.attachShader(p, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
    return p;
  }

  window.RisoParticles = function (el, opts) {
    var o = Object.assign({
      pitch: 3.6,        // average dot spacing in CSS px (one particle per pitch x pitch)
      dot: 2.5,          // dot size scale in CSS px (independent of spacing: wider pitch = fewer dots, same size)
      ambient: 0.27,     // strength of the ombre
      speed: 5,          // time scale of the ombre's slow swells
      vmin: 3, vmax: 12, // each dot's own drift speed range, CSS px per second
      calm: 0.78,        // how strongly the ink clears around the headline
      top: 0.94,         // how far the ink thins toward the top of the page
      navFade: 260,      // CSS px below the nav over which the ink thins out
      mix: 0.82,         // share of dots in the brighter blue ink
      fadeB: 0.22,       // bottom share where ink and paper fade into the page beige
      floor: 0.014,
      calmSel: '.hero-riso-copy, .hero-copy',
      ink: '#0B1A4A', ink2: '#2F55A8', paper: '#FCF3ED', paper2: '#EFE3D4'
    }, opts || {});
    var c = document.createElement('canvas'); c.setAttribute('aria-hidden', 'true');
    c.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block;';
    var gl = c.getContext('webgl', { alpha: false, antialias: false, premultipliedAlpha: false, preserveDrawingBuffer: /[?&]cap/.test(location.search) });
    if (!gl) return null;
    var DP, PP;
    try { DP = prog(gl, DOT_VS, DOT_FS); PP = prog(gl, PAPER_VS, PAPER_FS); } catch (e) { return null; }
    el.appendChild(c);
    function locs(p, names) { var u = {}; names.forEach(function (n) { u[n] = gl.getUniformLocation(p, n); }); return u; }
    var UD = locs(DP, ['u_res', 'u_ts', 'u_amb', 'u_calmS', 'u_top', 'u_navH', 'u_navF', 'u_fadeB', 'u_floor', 'u_calm', 'u_t', 'u_pitch', 'u_dot', 'u_dpr', 'u_mix', 'u_marg', 'u_vmin', 'u_vmax', 'u_ink', 'u_ink2']);
    var UP = locs(PP, ['u_res', 'u_paper', 'u_paper2', 'u_fadeB']);
    var aH = gl.getAttribLocation(DP, 'a_h'), aR = gl.getAttribLocation(DP, 'a_r'), aP = gl.getAttribLocation(PP, 'a_p');
    var tri = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, tri); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var dots = gl.createBuffer(), N = 0;

    var W = 0, H = 0, dpr = 1, MARG = 24;
    function resize() {
      var r = el.getBoundingClientRect(); dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.max(2, Math.round(r.width * dpr)), h = Math.max(2, Math.round(r.height * dpr));
      if (w === W && h === H) return;
      W = c.width = w; H = c.height = h;
      // one particle per pitch x pitch of the wrap box, started on a jittered grid so the print begins even
      var bw = r.width + 2 * MARG, bh = r.height + 2 * MARG, nx = Math.ceil(bw / o.pitch), ny = Math.ceil(bh / o.pitch);
      N = nx * ny; var a = new Float32Array(N * 8), k = 0, s = 1;
      function rnd() { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }
      for (var j = 0; j < ny; j++) for (var i = 0; i < nx; i++) {
        a[k++] = (i + 0.5 + (rnd() - 0.5) * 0.6) / nx; a[k++] = (j + 0.5 + (rnd() - 0.5) * 0.6) / ny; a[k++] = rnd(); a[k++] = rnd();
        a[k++] = rnd(); a[k++] = rnd(); a[k++] = rnd(); a[k++] = rnd();
      }
      gl.bindBuffer(gl.ARRAY_BUFFER, dots); gl.bufferData(gl.ARRAY_BUFFER, a, gl.STATIC_DRAW);
    }

    var t0 = performance.now(), raf = 0, visible = true, last = 0;
    function draw(now) {
      resize();
      var t = reduce ? 0 : (now - t0) / 1000;
      gl.viewport(0, 0, W, H);
      gl.disable(gl.BLEND);
      gl.useProgram(PP);
      gl.uniform2f(UP.u_res, W, H); gl.uniform3fv(UP.u_paper, hex(o.paper)); gl.uniform3fv(UP.u_paper2, hex(o.paper2)); gl.uniform1f(UP.u_fadeB, Math.max(o.fadeB, 0.0001));
      gl.bindBuffer(gl.ARRAY_BUFFER, tri); gl.enableVertexAttribArray(aP); gl.vertexAttribPointer(aP, 2, gl.FLOAT, false, 0, 0);
      gl.drawArrays(gl.TRIANGLES, 0, 3); gl.disableVertexAttribArray(aP);

      gl.useProgram(DP);
      var er = el.getBoundingClientRect(), cz = [0, 0, 0, 0], cp = el.parentElement && el.parentElement.querySelector(o.calmSel);
      if (cp) { var cr = cp.getBoundingClientRect(); cz = [((cr.left + cr.right) / 2 - er.left) * dpr, (er.bottom - (cr.top + cr.bottom) / 2) * dpr, (cr.width - 40) * dpr, (cr.height - 20) * dpr]; }
      var nh = 0, nv = o.navFade ? document.getElementById('nav') : null;
      if (nv) { var nr = nv.getBoundingClientRect(); nh = Math.max(0, nr.bottom - er.top) * dpr; }
      gl.uniform2f(UD.u_res, W, H); gl.uniform1f(UD.u_ts, t * o.speed); gl.uniform1f(UD.u_t, t);
      gl.uniform1f(UD.u_amb, o.ambient); gl.uniform1f(UD.u_calmS, cp ? o.calm : 0); gl.uniform4fv(UD.u_calm, cz);
      gl.uniform1f(UD.u_top, o.top); gl.uniform1f(UD.u_navH, nh); gl.uniform1f(UD.u_navF, (o.navFade || 1) * dpr);
      gl.uniform1f(UD.u_fadeB, Math.max(o.fadeB, 0.0001)); gl.uniform1f(UD.u_floor, o.floor);
      gl.uniform1f(UD.u_pitch, o.pitch * dpr); gl.uniform1f(UD.u_dot, o.dot * dpr); gl.uniform1f(UD.u_dpr, dpr); gl.uniform1f(UD.u_mix, o.mix); gl.uniform1f(UD.u_marg, MARG * dpr);
      gl.uniform1f(UD.u_vmin, o.vmin); gl.uniform1f(UD.u_vmax, o.vmax);
      gl.uniform3fv(UD.u_ink, hex(o.ink)); gl.uniform3fv(UD.u_ink2, hex(o.ink2));
      gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
      gl.bindBuffer(gl.ARRAY_BUFFER, dots);
      gl.enableVertexAttribArray(aH); gl.vertexAttribPointer(aH, 4, gl.FLOAT, false, 32, 0);
      gl.enableVertexAttribArray(aR); gl.vertexAttribPointer(aR, 4, gl.FLOAT, false, 32, 16);
      gl.drawArrays(gl.POINTS, 0, N);
    }
    function frame(now) { raf = 0; if (!visible || document.hidden) return;
      if (now - last > 16) { draw(now); last = now; }
      if (!reduce) raf = requestAnimationFrame(frame); }
    function kick() { if (!raf && visible) raf = requestAnimationFrame(frame); }
    draw(performance.now()); kick();
    window.addEventListener('resize', kick);
    document.addEventListener('visibilitychange', kick);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) kick(); }).observe(el);
    return { set: function (k, v) { o[k] = v; kick(); }, opts: o };
  };
})();
