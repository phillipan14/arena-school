/* ============================================================
   Arena — riso-shimmer.js
   Shows a risograph print exactly as printed, then animates it very
   gently: the shape's surface drifts slowly and small groups of
   dots jiggle and twinkle. A mask limits all motion to the shape,
   so the paper background never moves.

   <div data-shimmer="/art/x.webp" data-shimmer-mask="/art/x-mask.png"
        data-dist="1.1" data-speed="0.9" data-group="3"
        data-twinkle="0.15" data-flow="15" data-flow-speed="1.3">
     <img src="/art/x.webp" alt="">   still image, also the fallback
   </div>
   Reduced motion or no WebGL: the still image stays.
   ============================================================ */
(function () {
  'use strict';
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var VS = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
  var FS = [
    'precision highp float;',
    'uniform sampler2D I,M;uniform vec2 R,IR;uniform float t,D,SP,CS,TW,FL,FS;',
    'vec2 h2(vec2 p){p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3)));return fract(sin(p)*43758.5453);}',
    'void main(){',
    '  vec2 uv=vec2(gl_FragCoord.x,R.y-gl_FragCoord.y)/R; vec2 ip=uv*IR;',
    '  float m0=texture2D(M,uv).r; vec2 q=uv*vec2(IR.x/IR.y,1.0); float ft=t*FS;',
    '  vec2 flow=FL*m0*vec2(sin(q.y*5.0+ft*0.9)+0.5*sin(q.x*3.1-ft*0.7+1.3),cos(q.x*4.2+ft*0.8)+0.5*cos(q.y*6.3+ft*0.6+2.1))/1.5;',
    '  vec2 e=min(ip,IR-ip); float edge=smoothstep(2.0,40.0,min(e.x,e.y)); ip+=flow*edge; float m=m0*edge;',
    '  vec2 cell=floor(ip/CS); vec2 h=h2(cell),g=h2(cell+17.3); vec2 f=(0.7+0.9*g)*SP*2.0; vec2 ph=h*6.2832;',
    '  vec2 off=D*m*vec2(0.65*sin(t*f.x+ph.x)+0.35*sin(t*f.y*1.7+ph.y),0.65*cos(t*f.y+ph.y)+0.35*cos(t*f.x*1.3+ph.x));',
    '  vec3 col=texture2D(I,(ip+off)/IR).rgb; vec3 pap=vec3(0.965,0.945,0.91);',
    '  float ink=1.0-dot(col,vec3(0.333));',
    '  float tw=pow(0.5+0.5*sin(t*SP*1.3+ph.x*1.7),10.0)*TW*m*smoothstep(0.12,0.5,ink)*(1.0-smoothstep(0.7,0.92,ink));',
    '  gl_FragColor=vec4(mix(col,pap,tw),1.);',
    '}'
  ].join('\n');
  function sh(gl, t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; }
  function load(src) { return new Promise(function (ok, no) { var i = new Image(); i.decoding = 'async'; i.onload = function () { ok(i); }; i.onerror = no; i.src = src; }); }

  function init(el) {
    var d = el.dataset, num = function (k, v) { var x = parseFloat(d[k]); return isNaN(x) ? v : x; };
    var P = { D: num('dist', 1.1), SP: num('speed', 0.9), CS: num('group', 3), TW: num('twinkle', 0.15), FL: num('flow', 15), FS: num('flowSpeed', 1.3) };
    var c = document.createElement('canvas'); c.className = 'shimmer-canvas'; c.setAttribute('aria-hidden', 'true');
    var gl = c.getContext('webgl', { antialias: false, alpha: false }); if (!gl) return;
    var prog;
    try { prog = gl.createProgram(); gl.attachShader(prog, sh(gl, gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl, gl.FRAGMENT_SHADER, FS)); gl.bindAttribLocation(prog, 0, 'p'); gl.linkProgram(prog); if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return; } catch (e) { return; }
    gl.useProgram(prog);
    var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    var u = {}; ['I', 'M', 'R', 'IR', 't', 'D', 'SP', 'CS', 'TW', 'FL', 'FS'].forEach(function (n) { u[n] = gl.getUniformLocation(prog, n); });
    function tex(img, unit) { var x = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, x); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
      [gl.TEXTURE_MIN_FILTER, gl.TEXTURE_MAG_FILTER].forEach(function (k) { gl.texParameteri(gl.TEXTURE_2D, k, gl.LINEAR); });
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); }
    var raf = 0, visible = true, t0 = performance.now(), ready = false;
    function resize() { var r = el.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.max(2, Math.round(r.width * dpr)), h = Math.max(2, Math.round(r.height * dpr));
      if (c.width !== w || c.height !== h) { c.width = w; c.height = h; gl.viewport(0, 0, w, h); gl.uniform2f(u.R, w, h); } }
    function frame(now) { raf = 0; if (!visible || document.hidden) return; gl.uniform1f(u.t, (now - t0) / 1000); gl.drawArrays(gl.TRIANGLES, 0, 3); raf = requestAnimationFrame(frame); }
    function start() { if (ready && !raf) raf = requestAnimationFrame(frame); }
    Promise.all([load(d.shimmer), load(d.shimmerMask)]).then(function (imgs) {
      tex(imgs[0], 0); tex(imgs[1], 1); gl.uniform1i(u.I, 0); gl.uniform1i(u.M, 1);
      gl.uniform2f(u.IR, imgs[0].naturalWidth, imgs[0].naturalHeight);
      Object.keys(P).forEach(function (k) { gl.uniform1f(u[k], P[k]); });
      el.appendChild(c); resize(); ready = true; start();
      requestAnimationFrame(function () { el.classList.add('shimmer-live'); });
    }).catch(function () {});
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(el); else window.addEventListener('resize', resize);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) start(); }, { rootMargin: '80px' }).observe(el);
    document.addEventListener('visibilitychange', function () { if (!document.hidden) start(); });
  }
  function boot() { [].forEach.call(document.querySelectorAll('[data-shimmer]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
