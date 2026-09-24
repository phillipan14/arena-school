/* ============================================================
   Arena — riso-dots.js
   Risograph artwork drawn live, one dot at a time.
   Pass 1 lights a soft 3D "fabric" form (ray-marched) at one
   sample per dot cell. Pass 2 stipples: every cell gets a single
   ink dot, slightly jittered like a riso screen, sized by that
   tone. The paper and the dot screen never move; only the fabric
   underneath does, so the print stays crisp at any resolution.

   <div data-dots="blob"              blob | band
        data-dots-seed="2"            shape variation
        data-dots-center="0.3,0.55"   form centre, fraction of the box
        data-dots-scale="0.8"         form size relative to box height
        data-dots-bg="0.07"           background stipple density (0-1)
        data-dots-duo                 add a coral second ink
        data-dots-ink="#16226A"       first ink
        data-dots-cell="2.4"          dot pitch in CSS px
        data-dots-speed="1">
   Visitors who prefer reduced motion get a single still frame.
   ============================================================ */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var VS = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.0,1.0);}';

  var TONE = [
    'precision highp float;',
    'uniform vec2 u_grid;uniform float u_aspect;uniform float u_t;uniform vec2 u_center;uniform float u_scale;',
    'uniform float u_seed;uniform float u_bg;uniform float u_duo;uniform float u_mode;',
    'mat2 rot(float a){float c=cos(a),s=sin(a);return mat2(c,-s,s,c);}',
    'float smin(float a,float b,float k){float h=clamp(0.5+0.5*(b-a)/k,0.0,1.0);return mix(b,a,h)-k*h*(1.0-h);}',
    'float sdTorus(vec3 p,vec2 t){vec2 q=vec2(length(p.xz)-t.x,p.y);return length(q)-t.y;}',
    'float map(vec3 p){',
    '  float t=u_t; p-=vec3(u_center,0.0); p/=u_scale;',
    '  p.xy*=rot(0.55+0.25*sin(t*0.11+u_seed*1.7));',
    '  p.yz*=rot(0.9+0.35*sin(t*0.07+u_seed));',
    '  p.xz*=rot(0.7*sin(t*0.06)+u_seed*0.8);',
    '  vec3 q=p+0.34*sin(p.yzx*1.7+vec3(t*0.45,t*0.33+u_seed,t*0.39+u_seed*2.0));',
    '  q+=0.10*sin(q.zxy*3.1+t*0.55);',
    '  vec2 qq=vec2(length(q.xz)-1.0,q.y); float d=(length(qq/vec2(0.2,0.62))-1.0)*0.2;',
    '  float d2=length((q-vec3(0.5*sin(t*0.17+u_seed),0.35,0.2))*vec3(1.0,0.8,1.6))-0.42;',
    '  d=smin(d,d2,0.5);',
    '  return d*0.45*u_scale;',
    '}',
    'vec3 nrm(vec3 p){vec2 e=vec2(0.0025,-0.0025);',
    '  return normalize(e.xyy*map(p+e.xyy)+e.yyx*map(p+e.yyx)+e.yxy*map(p+e.yxy)+e.xxx*map(p+e.xxx));}',
    'void main(){',
    '  vec2 uv=gl_FragCoord.xy/u_grid; ',
    '  if(u_mode>0.5){',
    '    float gc=0.52+0.2*sin(u_t*0.09); float y=1.0-uv.y;',
    '    float f=exp(-pow((y-gc)/0.24,2.0))*(0.78+0.22*sin(uv.x*3.0+u_t*0.13));',
    '    gl_FragColor=vec4(0.05+0.62*f,0.0,0.0,1.0); return;',
    '  }',
    '  vec2 w=vec2((uv.x*2.0-1.0)*u_aspect,uv.y*2.0-1.0);',
    '  vec3 ro=vec3(w,4.0); vec3 rd=vec3(0.0,0.0,-1.0);',
    '  float z=0.0; float hit=0.0; vec3 p;',
    '  for(int i=0;i<80;i++){p=ro+rd*z; float d=map(p); if(d<0.0015){hit=1.0;break;} z+=d; if(z>8.0)break;}',
    '  float ink1=u_bg*(0.8+0.2*sin(w.x*1.3+w.y*0.9)); float ink2=0.0;',
    '  if(hit>0.5){',
    '    vec3 n=nrm(p);',
    '    vec3 L=normalize(vec3(-0.78,0.55,0.3));',
    '    float dif=max(dot(n,L),0.0);',
    '    float ao=clamp(map(p+n*0.16)/0.16,0.0,1.0);',
    '    float light=pow(dif,1.35);',
    '    light*=mix(0.35,1.0,ao);',
    '    float rim=smoothstep(0.32,0.0,abs(n.z));',
    '    ink1=smoothstep(0.08,0.92,1.0-light);',
    '    ink1=clamp(max(ink1,rim*0.7)+0.04,0.0,1.0);',
    '    if(u_duo>0.5){',
    '      vec3 L2=normalize(vec3(0.75,-0.3,0.6));',
    '      ink2=pow(max(dot(n,L2),0.0),1.7)*0.9;',
    '      ink1*=1.0-0.55*ink2;',
    '    }',
    '  }',
    '  gl_FragColor=vec4(clamp(ink1,0.0,1.0),clamp(ink2,0.0,1.0),0.0,1.0);',
    '}'
  ].join('\n');

  var STIPPLE = [
    'precision highp float;',
    'uniform sampler2D u_tone;uniform vec2 u_grid;uniform float u_cell;uniform float u_jit;',
    'uniform vec4 u_ink1;uniform vec4 u_ink2;uniform float u_seed;',
    'vec2 h2(vec2 p){p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3)));return fract(sin(p+u_seed)*43758.5453);}',
    'void main(){',
    '  vec2 px=gl_FragCoord.xy; vec2 base=floor(px/u_cell);',
    '  float c1=0.0,c2=0.0;',
    '  for(int j=-1;j<=1;j++){for(int i=-1;i<=1;i++){',
    '    vec2 id=base+vec2(float(i),float(j));',
    '    vec2 tc=(id+0.5)/u_grid; if(tc.x<0.0||tc.y<0.0||tc.x>1.0||tc.y>1.0) continue;',
    '    vec4 tone=texture2D(u_tone,tc); vec2 h=h2(id);',
    '    float t1=tone.r*(0.82+0.36*h.x);',
    '    if(t1>0.004){',
    '      vec2 c=(id+0.5+(h-0.5)*u_jit)*u_cell; float r=u_cell*0.5*sqrt(t1)*1.32;',
    '      float d=length(px-c); c1=max(c1,clamp(r-d+0.5,0.0,1.0));',
    '    }',
    '    float t2=tone.g*(0.82+0.36*h.y);',
    '    if(t2>0.004){',
    '      vec2 c=(id+0.5+(h.yx-0.5)*u_jit+vec2(0.31,0.19))*u_cell; float r=u_cell*0.5*sqrt(t2)*1.25;',
    '      float d=length(px-c); c2=max(c2,clamp(r-d+0.5,0.0,1.0));',
    '    }',
    '  }}',
    '  float a1=c1*u_ink1.a, a2=c2*u_ink2.a;',
    '  vec3 rgb=u_ink1.rgb*a1+u_ink2.rgb*a2*(1.0-a1); float a=a1+a2*(1.0-a1);',
    '  gl_FragColor=vec4(rgb,a);',
    '}'
  ].join('\n');

  function hex(h, a) {
    h = (h || '').replace('#', '');
    if (h.length !== 6) return [0.09, 0.13, 0.42, a == null ? 1 : a];
    return [parseInt(h.slice(0, 2), 16) / 255, parseInt(h.slice(2, 4), 16) / 255, parseInt(h.slice(4, 6), 16) / 255, a == null ? 1 : a];
  }
  function sh(gl, type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; }
  function prog(gl, fs) {
    var p = gl.createProgram(); gl.attachShader(p, sh(gl, gl.VERTEX_SHADER, VS)); gl.attachShader(p, sh(gl, gl.FRAGMENT_SHADER, fs));
    gl.bindAttribLocation(p, 0, 'p'); gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error('link'); return p;
  }
  function U(gl, p, names) { var o = {}; names.forEach(function (n) { o[n] = gl.getUniformLocation(p, n); }); return o; }

  function init(el) {
    var d = el.dataset;
    var mode = d.dots === 'band' ? 1 : 0;
    var seed = parseFloat(d.dotsSeed || '0');
    var cenL = (d.dotsCenter || '0.5,0.5').split(',').map(parseFloat), scaleL = parseFloat(d.dotsScale || '0.8');
    var cenS = d.dotsCenterSm ? d.dotsCenterSm.split(',').map(parseFloat) : cenL, scaleS = parseFloat(d.dotsScaleSm || scaleL);
    var cen = cenL, scale = scaleL;
    var bg = parseFloat(d.dotsBg || '0');
    var duo = d.dotsDuo !== undefined ? 1 : 0;
    var cellCss = parseFloat(d.dotsCell || (mode ? '7' : '2.4'));
    var speed = parseFloat(d.dotsSpeed || '1');
    var ink1 = mode ? hex(d.dotsInk || '#F4ECE0', parseFloat(d.dotsAlpha || '0.55')) : hex(d.dotsInk || '#16226A', 1);
    var ink2 = hex(d.dotsInk2 || '#E8886A', 0.95);
    var jit = mode ? 0.0 : 0.62;

    var canvas = document.createElement('canvas');
    canvas.className = 'dots-canvas'; canvas.setAttribute('aria-hidden', 'true');
    var gl = canvas.getContext('webgl', { premultipliedAlpha: true, alpha: true, antialias: false }) || canvas.getContext('experimental-webgl');
    if (!gl) return;
    var P1, P2, u1, u2;
    try {
      P1 = prog(gl, TONE); P2 = prog(gl, STIPPLE);
    } catch (e) { if (window.console) console.warn('riso-dots', e); return; }
    u1 = U(gl, P1, ['u_grid', 'u_aspect', 'u_t', 'u_center', 'u_scale', 'u_seed', 'u_bg', 'u_duo', 'u_mode']);
    u2 = U(gl, P2, ['u_tone', 'u_grid', 'u_cell', 'u_jit', 'u_ink1', 'u_ink2', 'u_seed']);
    var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    var tex = gl.createTexture(), fbo = gl.createFramebuffer();
    var W = 0, H = 0, GW = 0, GH = 0, cell = 1, raf = 0, visible = true, t0 = performance.now();

    function resize() {
      var r = el.getBoundingClientRect(); var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.max(2, Math.round(r.width * dpr)), h = Math.max(2, Math.round(r.height * dpr));
      if (w === W && h === H) return;
      W = canvas.width = w; H = canvas.height = h; cell = cellCss * dpr;
      var narrow = r.width < 760; cen = narrow ? cenS : cenL; scale = narrow ? scaleS : scaleL;
      GW = Math.ceil(W / cell); GH = Math.ceil(H / cell);
      gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, GW, GH, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.bindFramebuffer(gl.FRAMEBUFFER, fbo); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      if (reduce || !raf) draw(reduce ? 12 : (performance.now() - t0) / 1000);
    }
    function draw(t) {
      if (!GW) return;
      var aspect = W / H;
      gl.bindFramebuffer(gl.FRAMEBUFFER, fbo); gl.viewport(0, 0, GW, GH); gl.useProgram(P1);
      gl.uniform2f(u1.u_grid, GW, GH); gl.uniform1f(u1.u_aspect, aspect); gl.uniform1f(u1.u_t, t * speed + seed * 7.0);
      gl.uniform2f(u1.u_center, ((cen[0] || 0.5) * 2 - 1) * aspect, 1 - (isNaN(cen[1]) ? 0.5 : cen[1]) * 2);
      gl.uniform1f(u1.u_scale, scale); gl.uniform1f(u1.u_seed, seed); gl.uniform1f(u1.u_bg, bg); gl.uniform1f(u1.u_duo, duo); gl.uniform1f(u1.u_mode, mode);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, W, H); gl.useProgram(P2);
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex); gl.uniform1i(u2.u_tone, 0);
      gl.uniform2f(u2.u_grid, GW, GH); gl.uniform1f(u2.u_cell, cell); gl.uniform1f(u2.u_jit, jit); gl.uniform1f(u2.u_seed, seed);
      gl.uniform4fv(u2.u_ink1, ink1); gl.uniform4fv(u2.u_ink2, ink2);
      gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
    }
    function frame(now) { raf = 0; if (!visible || document.hidden) return; draw((now - t0) / 1000); raf = requestAnimationFrame(frame); }
    function start() { if (!raf && !reduce) raf = requestAnimationFrame(frame); }

    el.appendChild(canvas); resize();
    requestAnimationFrame(function () { el.classList.add('dots-live'); });
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(el); else window.addEventListener('resize', resize);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) start(); }, { rootMargin: '100px' }).observe(el);
    document.addEventListener('visibilitychange', function () { if (!document.hidden) start(); });
    start();
  }

  function boot() {
    [].forEach.call(document.querySelectorAll('.dark-band, .footer'), function (host) {
      if (host.querySelector(':scope > .dots-layer')) return;
      var l = document.createElement('div'); l.className = 'dots-layer'; l.setAttribute('data-dots', 'band');
      l.setAttribute('data-dots-alpha', host.classList.contains('footer') ? '0.3' : '0.5');
      host.insertBefore(l, host.firstChild);
    });
    [].forEach.call(document.querySelectorAll('[data-dots]'), init);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
