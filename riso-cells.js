/* ============================================================
   Arena — riso-cells.js
   Animates a risograph print dot by dot. A cell map splits the print
   into one small cell per real dot (or paper gap in dark areas); each
   cell carries its own original pixels and moves on its own, so every
   dot keeps its exact look and colour. The cell map's blue channel is
   the shape mask: background cells never move.

   <div data-cells="/art/x.webp" data-cells-map="/art/x-cells.png"
        data-dist="1.5" data-speed="1.2" data-focus="0.25,0.5">
     <img src="/art/x.webp" alt="">    still fallback
   </div>
   Reduced motion or no WebGL: the still image stays.
   ============================================================ */
(function () {
  'use strict';
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var VS = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  var FS = [
    'precision highp float;',
    'uniform sampler2D I,C;uniform vec2 R,IR,O;uniform float SC,t,D,SP;',
    'void main(){',
    '  vec2 ip=vec2(gl_FragCoord.x,R.y-gl_FragCoord.y)/SC+O;',
    '  vec4 cell=texture2D(C,(floor(ip)+0.5)/IR); float ph=cell.r*6.2832, f=(0.6+0.9*cell.g)*SP*2.0, m=cell.b;',
    '  vec2 off=D*m*vec2(0.7*sin(t*f+ph)+0.3*sin(t*f*1.7+ph*2.3),0.7*cos(t*f*0.93+ph*1.3)+0.3*cos(t*f*1.41+ph));',
    '  gl_FragColor=vec4(texture2D(I,(ip-off)/IR).rgb,1.);',
    '}'
  ].join('\n');
  function sh(gl, t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; }
  function load(src) { return new Promise(function (ok, no) { var i = new Image(); i.decoding = 'async'; i.onload = function () { ok(i); }; i.onerror = no; i.src = src; }); }
  function init(el) {
    var d = el.dataset, dist = parseFloat(d.dist || '1.5'), speed = parseFloat(d.speed || '1.2'), focus = (d.focus || '0.5,0.5').split(',').map(parseFloat);
    var c = document.createElement('canvas'); c.className = 'shimmer-canvas'; c.setAttribute('aria-hidden', 'true');
    var gl = c.getContext('webgl', { antialias: false, alpha: false }); if (!gl) return;
    var prog;
    try { prog = gl.createProgram(); gl.attachShader(prog, sh(gl, gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl, gl.FRAGMENT_SHADER, FS)); gl.bindAttribLocation(prog, 0, 'p'); gl.linkProgram(prog); if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return; } catch (e) { return; }
    gl.useProgram(prog);
    var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    var u = {}; ['I', 'C', 'R', 'IR', 'O', 'SC', 't', 'D', 'SP'].forEach(function (n) { u[n] = gl.getUniformLocation(prog, n); });
    function tex(img, unit, filt) { var x = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, x); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, filt); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, filt);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); }
    var raf = 0, visible = true, t0 = performance.now(), ready = false, iw = 1, ih = 1;
    function resize() { var r = el.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.max(2, Math.round(r.width * dpr)), h = Math.max(2, Math.round(r.height * dpr));
      if (c.width !== w || c.height !== h) { c.width = w; c.height = h; gl.viewport(0, 0, w, h); gl.uniform2f(u.R, w, h); }
      var sc = Math.max(w / iw, h / ih); gl.uniform1f(u.SC, sc); gl.uniform2f(u.O, (iw - w / sc) * focus[0], (ih - h / sc) * focus[1]); }
    function frame(now) { raf = 0; if (!visible || document.hidden) return; gl.uniform1f(u.t, (now - t0) / 1000); gl.drawArrays(gl.TRIANGLES, 0, 3); raf = requestAnimationFrame(frame); }
    function start() { if (ready && !raf) raf = requestAnimationFrame(frame); }
    Promise.all([load(d.cells), load(d.cellsMap)]).then(function (imgs) {
      tex(imgs[0], 0, gl.LINEAR); tex(imgs[1], 1, gl.NEAREST); gl.uniform1i(u.I, 0); gl.uniform1i(u.C, 1);
      iw = imgs[0].naturalWidth; ih = imgs[0].naturalHeight; gl.uniform2f(u.IR, iw, ih); gl.uniform1f(u.D, dist); gl.uniform1f(u.SP, speed);
      el.appendChild(c); resize(); ready = true; start();
      requestAnimationFrame(function () { el.classList.add('shimmer-live'); });
    }).catch(function () {});
    if ('ResizeObserver' in window) new ResizeObserver(function () { if (ready) resize(); }).observe(el); else window.addEventListener('resize', resize);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) start(); }, { rootMargin: '80px' }).observe(el);
    document.addEventListener('visibilitychange', function () { if (!document.hidden) start(); });
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-cells]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
