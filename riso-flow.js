/* ============================================================
   Arena — riso-flow.js
   Animates risograph artwork without redrawing it: the printed
   image is used as a WebGL texture and gently displaced, so every
   dot and grain of the original moves with the "fabric".
     data-riso="/art/x.webp"          image to animate (required)
     data-riso-sm="/art/x-sm.webp"    smaller image for narrow screens
     data-riso-mode="fabric|drift"    fabric ripple (default) or slow drift
     data-riso-focus="0.5,0.5"        crop focus, like background-position
     data-riso-amp="1"                motion strength
   The element keeps a static CSS background as the fallback, so the
   page looks right with WebGL off, before load, and for visitors who
   prefer reduced motion (they get one still frame).
   ============================================================ */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var VS = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.0,1.0);}';
  var FS = [
    'precision mediump float;',
    'uniform sampler2D u_img;uniform vec2 u_res;uniform vec2 u_imgRes;uniform vec2 u_focus;',
    'uniform float u_t;uniform float u_amp;uniform float u_mode;uniform float u_grain;uniform float u_zoom;',
    'float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}',
    'float lum(vec3 c){return dot(c,vec3(0.299,0.587,0.114));}',
    'void main(){',
    '  vec2 frag=vec2(gl_FragCoord.x,u_res.y-gl_FragCoord.y);',
    '  float s=max(u_res.x/u_imgRes.x,u_res.y/u_imgRes.y)*u_zoom;',
    '  vec2 shown=u_res/s; vec2 off=(u_imgRes-shown)*u_focus;',
    '  vec2 uv=(off+frag/s)/u_imgRes; float t=u_t; vec2 d;',
    '  if(u_mode<0.5){',
    '    float w1=sin(uv.x*7.0+t*0.55+sin(uv.y*3.1+t*0.23)*1.2);',
    '    float w2=sin(uv.x*3.3-t*0.37+uv.y*2.4);',
    '    float w3=sin((uv.x+uv.y)*11.0+t*0.8);',
    '    d=vec2(0.0035*sin(uv.y*8.0+t*0.45)+0.0015*w3, 0.011*w1+0.007*w2+0.002*w3);',
    '    float base=lum(texture2D(u_img,uv).rgb);',
    '    d*=mix(0.25,1.0,smoothstep(0.85,0.35,base));',
    '  } else {',
    '    d=vec2(0.006*sin(uv.y*4.0+t*0.3), 0.045*sin(t*0.11)+0.01*sin(uv.x*5.0+t*0.4));',
    '  }',
    '  vec2 q=clamp(uv+d*u_amp,0.001,0.999);',
    '  vec3 col=texture2D(u_img,q).rgb;',
    '  float l=lum(col);',
    '  float mid=smoothstep(0.08,0.45,l)*(1.0-smoothstep(0.72,0.95,l));',
    '  float band=0.5+0.5*sin((uv.x*0.8-uv.y*0.5)*6.2831-t*0.22);',
    '  vec3 coral=vec3(0.898,0.576,0.459);',
    '  col=mix(col,col*0.55+coral*0.55,band*mid*0.28);',
    '  col*=0.97+0.03*sin(t*0.4+uv.x*2.0);',
    '  float n=hash(floor(frag)+floor(t*12.0)*vec2(17.0,31.0));',
    '  col+=(n-0.5)*u_grain;',
    '  gl_FragColor=vec4(col,1.0);',
    '}'
  ].join('\n');

  function compile(gl, type, src) {
    var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { throw new Error(gl.getShaderInfoLog(s)); }
    return s;
  }

  function init(el) {
    var src = el.getAttribute('data-riso');
    var sm = el.getAttribute('data-riso-sm');
    if (sm && window.innerWidth < 760) src = sm;
    var mode = el.getAttribute('data-riso-mode') === 'drift' ? 1 : 0;
    var focus = (el.getAttribute('data-riso-focus') || '0.5,0.5').split(',').map(parseFloat);
    var amp = parseFloat(el.getAttribute('data-riso-amp') || '1');
    var canvas = document.createElement('canvas');
    canvas.className = 'riso-canvas'; canvas.setAttribute('aria-hidden', 'true');
    var gl = canvas.getContext('webgl', { antialias: false, premultipliedAlpha: false, alpha: false }) ||
             canvas.getContext('experimental-webgl');
    if (!gl) return;
    var prog, loc = {};
    try {
      prog = gl.createProgram();
      gl.attachShader(prog, compile(gl, gl.VERTEX_SHADER, VS));
      gl.attachShader(prog, compile(gl, gl.FRAGMENT_SHADER, FS));
      gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
    } catch (e) { return; }
    gl.useProgram(prog);
    var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    var pa = gl.getAttribLocation(prog, 'p'); gl.enableVertexAttribArray(pa); gl.vertexAttribPointer(pa, 2, gl.FLOAT, false, 0, 0);
    ['u_img', 'u_res', 'u_imgRes', 'u_focus', 'u_t', 'u_amp', 'u_mode', 'u_grain', 'u_zoom'].forEach(function (n) { loc[n] = gl.getUniformLocation(prog, n); });

    var img = new Image(); var ready = false, visible = true, raf = 0, t0 = performance.now();
    img.decoding = 'async';
    img.onload = function () {
      var tex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, img);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.uniform1i(loc.u_img, 0);
      gl.uniform2f(loc.u_imgRes, img.naturalWidth, img.naturalHeight);
      gl.uniform2f(loc.u_focus, focus[0] || 0.5, isNaN(focus[1]) ? 0.5 : focus[1]);
      gl.uniform1f(loc.u_amp, amp); gl.uniform1f(loc.u_mode, mode);
      gl.uniform1f(loc.u_grain, 0.045); gl.uniform1f(loc.u_zoom, 1.035);
      el.appendChild(canvas); ready = true; resize();
      requestAnimationFrame(function () { el.classList.add('riso-live'); });
      if (reduce) draw(6); else start();
    };
    img.src = src;

    function resize() {
      var r = el.getBoundingClientRect(); var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      var w = Math.max(1, Math.round(r.width * dpr)), h = Math.max(1, Math.round(r.height * dpr));
      if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
      gl.viewport(0, 0, w, h); gl.uniform2f(loc.u_res, w, h);
      if (ready && (reduce || !raf)) draw(reduce ? 6 : (performance.now() - t0) / 1000);
    }
    function draw(t) { gl.uniform1f(loc.u_t, t); gl.drawArrays(gl.TRIANGLES, 0, 3); }
    function frame(now) { raf = 0; if (!visible || document.hidden) return; draw((now - t0) / 1000); raf = requestAnimationFrame(frame); }
    function start() { if (!raf && ready && !reduce) raf = requestAnimationFrame(frame); }

    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(el); else window.addEventListener('resize', resize);
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) start(); }, { rootMargin: '120px' }).observe(el);
    }
    document.addEventListener('visibilitychange', function () { if (!document.hidden) start(); });
  }

  function boot() { [].forEach.call(document.querySelectorAll('[data-riso]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
