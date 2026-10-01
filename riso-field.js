/* ============================================================
   Arena — riso-field.js
   A living risograph halftone field. Navy ink on cream paper.
   Wherever the cursor (or a finger) moves, the ink deepens in a soft
   ombre that slowly fades; with no cursor, a faint ambient gradient
   drifts so the page is never flat. One WebGL pass, no libraries.

   <div class="hero-bg" data-riso-field></div>
   RisoField(el, opts) -> { set(key, value) }
   ============================================================ */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var FS = [
    'precision highp float;',
    'uniform vec2 u_res; uniform sampler2D u_field; uniform float u_t, u_pitch, u_ang, u_amb, u_max, u_dpr, u_calmS, u_top, u_navH, u_navF; uniform vec4 u_calm;',
    'uniform vec3 u_ink, u_ink2, u_paper, u_paper2, u_grain; uniform float u_mix, u_fadeB, u_grainA, u_flip, u_floor, u_jig; uniform vec2 u_fo;',
    'float h1(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }',
    'vec2 h2(vec2 p){ return fract(sin(vec2(dot(p, vec2(127.1, 311.7)), dot(p, vec2(269.5, 183.3)))) * 43758.5453); }',
    'float tone(vec2 px){',
    '  vec2 uv = px / u_res; if (u_flip > 0.5) uv.x = 1.0 - uv.x;',
    // ambient ombre: soft diagonal falloff + two slow drifting swells
    '  float a = 0.55 * (1.0 - smoothstep(-0.1, 1.15, uv.x * 0.8 + (1.0 - uv.y) * 0.5));',
    '  a += 0.30 * (0.5 + 0.5 * sin(uv.x * 2.3 + uv.y * 1.7 + u_t * 0.07));',
    '  a += 0.20 * (0.5 + 0.5 * sin(uv.x * -1.4 + uv.y * 3.1 - u_t * 0.05 + 1.3));',
    '  float f = texture2D(u_field, vec2(uv.x, 1.0 - uv.y)).r;',
    '  float T = u_amb * a + f * u_max;',
    // quiet zones: the ink thins to bare paper around the headline and under the nav, like space left for type
    '  vec2 hb = u_calm.zw * 0.5; float rad = 0.6 * min(hb.x, hb.y); vec2 dq = abs(px - u_calm.xy) - (hb - rad); float sd = length(max(dq, 0.0)) + min(max(dq.x, dq.y), 0.0) - rad;',
    '  float feather = 0.40 * u_res.y; float calm = u_calmS * (1.0 - smoothstep(-0.06 * u_res.y, feather, sd + 0.04 * u_res.y * sin(px.x * 0.004 + px.y * 0.006)));',
    '  float topc = u_navH > 0.0 ? smoothstep(u_res.y - u_navH - u_navF, u_res.y, px.y) : smoothstep(u_res.y * 0.84, u_res.y * 0.95, px.y);',
    '  calm = max(calm, u_top * topc);',
    '  float fb = smoothstep(0.0, u_fadeB * u_res.y, px.y);',   /* ink thins out toward the bottom edge */
    '  return clamp(max(T * (1.0 - calm) * fb, u_floor * (1.0 - 0.85 * calm)), 0.0, 0.97);',
    '}',
    'void main(){',
    '  vec2 px = gl_FragCoord.xy;',
    '  float c = cos(u_ang), s = sin(u_ang); mat2 R = mat2(c, -s, s, c);',
    '  vec2 q = R * (px - u_fo) / u_pitch; vec2 b = floor(q); float cov = 0.0; float blue = 0.0;',   /* u_fo: the whole print drifts across the page */
    '  for (int j = -1; j <= 1; j++) for (int i = -1; i <= 1; i++) {',
    '    vec2 id = b + vec2(float(i), float(j)); vec2 jt = (h2(id) - 0.5) * 0.24;',
    '    vec2 cc = id + 0.5 + jt + u_jig * vec2(sin(u_t * (2.3 + h1(id + 2.1) * 2.2) + h1(id + 5.3) * 6.2832), cos(u_t * (2.0 + h1(id + 8.9) * 2.2) + h1(id + 1.7) * 6.2832));',
    '    float T = tone((cc * u_pitch) * R + u_fo);',
    '    float keep = smoothstep(h1(id + 7.1) * 0.16, h1(id + 7.1) * 0.16 + 0.02, T);',
    '    float r = max(sqrt(T / 3.14159), 0.17) * (0.94 + 0.12 * h1(id + 3.3));',
    '    float d = length(q - cc);',
    '    float aa = 0.75 / (u_pitch);',
    '    float cv = keep * smoothstep(r + aa, r - aa, d);',
    '    if (cv > cov) { cov = cv; blue = step(h1(id + 11.7), u_mix); }',   /* each dot is printed in one of the two inks */
    '  }',
    '  float T0 = tone(px);',
    '  vec2 hc = fract(q) - 0.5; float hole = sqrt(max(0.0, 1.0 - T0) / 3.14159) * 0.9;',
    '  float solid = smoothstep(0.55, 0.8, T0) * smoothstep(hole - 0.08, hole + 0.08, length(abs(hc) - 0.5));',
    '  if (solid > cov) { cov = solid; blue = step(h1(floor(q) + 11.7), u_mix); }',
    '  float mott = 0.94 + 0.06 * sin(px.x * 0.013 + sin(px.y * 0.011) * 2.0) * sin(px.y * 0.017 + 1.7);',
    '  vec3 ink = mix(u_ink, u_ink2, blue) * mott;',
    '  vec3 paper = mix(u_paper2, u_paper, smoothstep(0.0, u_fadeB * u_res.y, px.y));',   /* hero paper melts into the page beige */
    '  vec3 col = mix(paper, ink, cov);',
    '  vec2 gp = floor(px / u_dpr); float g = h1(gp);',
    '  vec3 gc = mix(u_ink, u_ink2, step(0.5, h1(gp + 3.7)));',
    '  col = mix(col, gc, step(0.94, g) * (1.0 - cov) * u_grainA);',
    '  gl_FragColor = vec4(col, 1.0);',
    '}'].join('\n');
  var VS = 'attribute vec2 p; void main(){ gl_Position = vec4(p, 0.0, 1.0); }';

  function hex(h) { h = h.replace('#', ''); return [0, 2, 4].map(function (i) { return parseInt(h.substr(i, 2), 16) / 255; }); }
  function sh(gl, t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; }

  window.RisoField = function (el, opts) {
    var o = Object.assign({
      pitch: 2.5,      // dot spacing in CSS px
      angle: 18,       // screen angle, degrees
      ambient: 0.25,   // strength of the resting ombre
      max: 0.3,       // how dark the cursor can push the ink
      brush: 210,      // cursor glow radius, CSS px
      strength: 1.2,   // how fast ink builds under the cursor
      fade: 1.2,       // seconds for the trail to fade
      spread: 0.88,    // how much the trail softly bleeds outward
      ghost: 1,        // 1 = a slow invisible "cursor" drifts when nobody is moving the mouse
      calm: 0.78,      // how strongly the ink clears around the headline (0 = not at all)
      top: 1,        // how strongly the ink clears under the nav bar
      mix: 0.82,       // share of dots printed in the brighter blue ink
      fadeB: 0.22,     // bottom share of the section where ink and paper fade into the page beige
      grainA: 0.0,      // random paper grain (off: the riso tint below replaces it)
      floor: 0.014,     // faint halftone tint everywhere, matching the page's riso paper
      flip: false,     // mirror the resting ombre (inner pages: text sits left, ink sits right)    // strength of the paper speckle
      jig: 0,          // how far each dot bounces around its home (fraction of the dot spacing)
      animate: false,  // animate a non-interactive print (the dots bounce in place)
      speed: 1,        // time scale for the drifting ombre (animated prints)
      navFade: 0,      // >0 = clear all ink under the fixed nav and fade it in over this many CSS px below it
      interactive: true, // false = a still print (inner pages): no cursor, no drift, drawn once
      ghostSpeed: 1,   // time scale of the ghost brush
      ghostWide: 1,    // how far the ghost roams (1 = the middle two thirds)
      flow: [0, 0],    // CSS px per second the whole dot print drifts (0 = dots stay put)
      follow: true,    // false = keep the flowing ink but ignore the real cursor (the ghost drifts all the time)
      calmSel: '.hero-riso-copy, .hero-copy, .zl-hero-copy, .curr-hero .reveal',
      ink: '#0B1A4A', ink2: '#2F55A8', paper: '#FCF3ED', paper2: '#EFE3D4', grain: '#A2A6B5'
    }, opts || {});
    var c = document.createElement('canvas'); c.setAttribute('aria-hidden', 'true');
    c.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block;';
    el.appendChild(c);
    var gl = c.getContext('webgl', { alpha: false, antialias: false, preserveDrawingBuffer: /[?&]cap/.test(location.search) });
    if (!gl) return null;
    var P = gl.createProgram(); gl.attachShader(P, sh(gl, gl.VERTEX_SHADER, VS)); gl.attachShader(P, sh(gl, gl.FRAGMENT_SHADER, FS)); gl.linkProgram(P); gl.useProgram(P);
    var U = {}; ['u_fo', 'u_res', 'u_field', 'u_t', 'u_pitch', 'u_ang', 'u_amb', 'u_max', 'u_dpr', 'u_calm', 'u_calmS', 'u_top', 'u_navH', 'u_navF', 'u_ink', 'u_ink2', 'u_paper', 'u_paper2', 'u_grain', 'u_mix', 'u_fadeB', 'u_grainA', 'u_flip', 'u_floor', 'u_jig'].forEach(function (n) { U[n] = gl.getUniformLocation(P, n); });
    var qb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, qb); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);

    // ---- the ink field: a coarse grid (1 cell = CELL css px), smoothed by linear texture filtering
    var CELL = 10, GW = 0, GH = 0, F = null, F2 = null, bytes = null, tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.pixelStorei(gl.UNPACK_ALIGNMENT, 1);

    var W = 0, H = 0, dpr = 1, cssW = 0, cssH = 0;
    function resize() {
      var r = el.getBoundingClientRect(); dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.max(2, Math.round(r.width * dpr)), h = Math.max(2, Math.round(r.height * dpr));
      if (w === W && h === H) return;
      W = c.width = w; H = c.height = h; cssW = r.width; cssH = r.height;
      var gw = Math.ceil(cssW / CELL) + 1, gh = Math.ceil(cssH / CELL) + 1;
      if (gw !== GW || gh !== GH) { GW = gw; GH = gh; F = new Float32Array(GW * GH); F2 = new Float32Array(GW * GH); bytes = new Uint8Array(GW * GH); }
    }

    // stamp a soft gaussian of ink at (x, y) in CSS px
    function stamp(x, y, amt) {
      var R = o.brush / CELL, r2 = R * R, cx = x / CELL, cy = y / CELL;
      var x0 = Math.max(0, Math.floor(cx - R * 1.6)), x1 = Math.min(GW - 1, Math.ceil(cx + R * 1.6));
      var y0 = Math.max(0, Math.floor(cy - R * 1.6)), y1 = Math.min(GH - 1, Math.ceil(cy + R * 1.6));
      for (var j = y0; j <= y1; j++) for (var i = x0; i <= x1; i++) {
        var dx = i - cx, dy = j - cy, g = Math.exp(-(dx * dx + dy * dy) / (0.5 * r2)), k = j * GW + i;
        F[k] = F[k] + (1 - F[k]) * amt * g;
      }
    }
    var last = null, lastMove = -1e9, ghostOn = false;
    function move(x, y, now, weight) {
      if (last) {   // stamp along the path so fast strokes stay continuous
        var dx = x - last[0], dy = y - last[1], dist = Math.sqrt(dx * dx + dy * dy), steps = Math.min(24, Math.ceil(dist / (o.brush * 0.25)));
        var amt = Math.min(1, 0.05 + dist * 0.004) * o.strength * weight;
        for (var s = 1; s <= steps; s++) stamp(last[0] + dx * s / steps, last[1] + dy * s / steps, amt / steps * 2.2);
      }
      last = [x, y];
    }
    function local(e) { var r = el.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top, r]; }
    function onMove(e) {
      var p = local(e); if (p[0] < -40 || p[1] < -40 || p[0] > p[2].width + 40 || p[1] > p[2].height + 40) { last = null; return; }
      if (ghostOn) { last = null; ghostOn = false; }
      lastMove = performance.now(); move(p[0], p[1], lastMove, 1); kick();
    }
    if (o.interactive && o.follow) { window.addEventListener('pointermove', onMove, { passive: true }); window.addEventListener('pointerdown', onMove, { passive: true }); }

    // ---- per-frame: fade + soft bleed, then upload
    var prevT = 0;
    function step(dt) {
      var k = Math.exp(-dt / Math.max(0.2, o.fade / 3)), sp = Math.min(0.5, o.spread * dt * 4), any = false;
      for (var j = 0; j < GH; j++) for (var i = 0; i < GW; i++) {
        var n = j * GW + i, v = F[n];
        if (sp > 0) {
          var l = F[i > 0 ? n - 1 : n], r = F[i < GW - 1 ? n + 1 : n], u = F[j > 0 ? n - GW : n], d = F[j < GH - 1 ? n + GW : n];
          v = v + ((l + r + u + d) * 0.25 - v) * sp;
        }
        v *= k; if (v < 0.002) v = 0; else any = true;
        F2[n] = v;
      }
      var t = F; F = F2; F2 = t;
      for (var m = 0; m < F.length; m++) bytes[m] = Math.min(255, F[m] * 255 + 0.5);
      gl.bindTexture(gl.TEXTURE_2D, tex); gl.texImage2D(gl.TEXTURE_2D, 0, gl.LUMINANCE, GW, GH, 0, gl.LUMINANCE, gl.UNSIGNED_BYTE, bytes);
      return any;
    }
    function ghost(t) {   // a slow invisible cursor for idle screens and phones
      t *= o.ghostSpeed; var gw = o.ghostWide;
      var x = cssW * (0.5 + 0.34 * gw * Math.sin(t * 0.11) + 0.08 * Math.sin(t * 0.29 + 1.0));
      var y = cssH * (0.5 + 0.30 * gw * Math.sin(t * 0.083 + 2.0) + 0.08 * Math.cos(t * 0.23));
      if (!ghostOn) { last = null; ghostOn = true; }
      move(x, y, t, 0.55);
    }

    var raf = 0, visible = true, t0 = performance.now();
    function draw(now) {
      resize();
      var t = (now - t0) / 1000, dt = Math.min(0.05, prevT ? (now - prevT) / 1000 : 0.016); prevT = now;
      if (!o.interactive && !o.animate) t = 7.0;
      if (o.interactive && o.ghost && !reduce && (!o.follow || now - lastMove > 2500)) ghost(t);
      step(dt);
      gl.viewport(0, 0, W, H);
      gl.uniform2f(U.u_fo, reduce ? 0 : o.flow[0] * t * dpr, reduce ? 0 : -o.flow[1] * t * dpr); gl.uniform2f(U.u_res, W, H); gl.uniform1f(U.u_t, reduce ? 0 : t * o.speed); gl.uniform1f(U.u_pitch, o.pitch * dpr); gl.uniform1f(U.u_ang, o.angle * Math.PI / 180);
      var cz = [0, 0, 0, 0], cp = el.parentElement && el.parentElement.querySelector(o.calmSel || '.hero-riso-copy');
      if (cp) { var er = el.getBoundingClientRect(), cr = cp.getBoundingClientRect();
        cz = [((cr.left + cr.right) / 2 - er.left) * dpr, (er.bottom - (cr.top + cr.bottom) / 2) * dpr, (cr.width - 40) * dpr, (cr.height - 20) * dpr]; }
      var nh = 0, nv = o.navFade ? document.getElementById('nav') : null;
      if (nv) { var nr = nv.getBoundingClientRect(), er2 = el.getBoundingClientRect(); nh = Math.max(0, nr.bottom - er2.top) * dpr; }
      gl.uniform1f(U.u_navH, nh); gl.uniform1f(U.u_navF, (o.navFade || 1) * dpr);
      gl.uniform4fv(U.u_calm, cz); gl.uniform1f(U.u_calmS, cp ? o.calm : 0); gl.uniform1f(U.u_top, o.top);
      gl.uniform1f(U.u_amb, o.ambient); gl.uniform1f(U.u_max, o.max); gl.uniform1f(U.u_dpr, dpr);
      gl.uniform3fv(U.u_ink, hex(o.ink)); gl.uniform3fv(U.u_ink2, hex(o.ink2)); gl.uniform3fv(U.u_paper, hex(o.paper)); gl.uniform3fv(U.u_paper2, hex(o.paper2)); gl.uniform3fv(U.u_grain, hex(o.grain));
      gl.uniform1f(U.u_mix, o.mix); gl.uniform1f(U.u_flip, o.flip ? 1 : 0); gl.uniform1f(U.u_floor, o.floor); gl.uniform1f(U.u_jig, reduce ? 0 : o.jig); gl.uniform1f(U.u_fadeB, Math.max(o.fadeB, 0.0001)); gl.uniform1f(U.u_grainA, o.grainA);
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex); gl.uniform1i(U.u_field, 0);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
    var lastDraw = 0;
    function frame(now) { raf = 0; if (!visible || document.hidden) return;
      if (o.interactive || now - lastDraw > 32) { draw(now); lastDraw = now; }   // animated still prints run at ~30fps
      if (!reduce && (o.interactive || o.animate)) raf = requestAnimationFrame(frame); }
    function kick() { if (!raf && visible) raf = requestAnimationFrame(frame); }
    // test hook: ?cap&t=..&cx=..&cy=.. renders one deterministic frame with a stroke through (cx, cy)
    window.__rfRender = function (t, pts) { resize(); lastMove = performance.now(); last = null; (pts || []).forEach(function (p) { move(p[0], p[1], 0, 1); }); step(0.016); prevT = 0; t0 = performance.now() - t * 1000; draw(performance.now()); };
    draw(performance.now()); kick();
    if (!o.interactive) window.addEventListener('resize', function () { kick(); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) kick(); }).observe(el);
    return { set: function (k, v) { o[k] = v; kick(); }, opts: o };
  };

  function boot() {
    [].forEach.call(document.querySelectorAll('[data-riso-field]'), function (el) {
      var mode = el.getAttribute('data-riso-field'), st = mode === 'static', hv = document.body.getAttribute('data-hero');
      if (mode === 'still') { var sInst = window.RisoField(el, { interactive: true, follow: false, speed: 5, ghostSpeed: 1.6, ghostWide: 1.25, jig: 0, navFade: 260, top: 0.94, flow: [14, -5] }); if (sInst) el.classList.add('is-live'); return; }   // homepage: the ink flows on its own (a drifting ghost brush, never the real cursor) and thins out gradually up into the nav
      if (st && hv && hv !== 'B') return;   // header options A, C, D draw no print
      var inst = window.RisoField(el, st && hv === 'B' ? { interactive: false, animate: true, jig: 0.2, ambient: 0.30, fadeB: 0.35, flip: true, calm: 1, top: 1,
        paper: '#FCF3ED', paper2: '#EFE3D4', ink: '#0B1A4A', ink2: '#2F55A8', mix: 0.45, floor: 0.012, grainA: 0 } : st ? { interactive: false, animate: true, jig: 0.24, ambient: 0.36, fadeB: 0, flip: true, calm: 1, top: 0.6,
        paper: '#0B1A4A', ink: '#EFE3D4', ink2: '#B8895C', mix: 0.42, floor: 0.012, grainA: 0 } : null); if (inst) { el.classList.add('is-live'); if (!st) window.__risoField = inst; }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
