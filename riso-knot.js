/* ============================================================
   Arena — riso-knot.js
   A thick, folding tube (torus knot) printed as a risograph.
   - Real 3D mesh, perspective camera, soft key light with
     self-shadowing, so highlights clip to paper and shadows
     clip to solid ink.
   - Dots are laid out in the tube's own surface coordinates, so
     rows of dots curve around the form like thread on fabric,
     and travel with the fabric when it moves. The paper and its
     background stipple stay still.

   <div data-knot
        data-knot-pq="2,3"        knot type
        data-knot-tube="0.46"     tube thickness
        data-knot-zoom="1"        >1 = closer
        data-knot-shift="0,0"     move the form in view (x,y)
        data-knot-tilt="0.4,0.2"  starting rotation (x,y radians)
        data-knot-duo             add coral second ink
        data-knot-bg="1"          stippled background (0 = transparent)
        data-knot-dot="2.6"       dot pitch in CSS px
        data-knot-speed="1">
   Reduced motion: one still frame.
   ============================================================ */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------- tiny mat4 ---------------- */
  function mul(a, b) { var o = new Float32Array(16); for (var i = 0; i < 4; i++) for (var j = 0; j < 4; j++) { var s = 0; for (var k = 0; k < 4; k++) s += a[k * 4 + j] * b[i * 4 + k]; o[i * 4 + j] = s; } return o; }
  function persp(fov, asp, n, f) { var t = 1 / Math.tan(fov / 2), o = new Float32Array(16); o[0] = t / asp; o[5] = t; o[10] = (f + n) / (n - f); o[11] = -1; o[14] = 2 * f * n / (n - f); return o; }
  function ortho(l, r, b, t, n, f) { var o = new Float32Array(16); o[0] = 2 / (r - l); o[5] = 2 / (t - b); o[10] = -2 / (f - n); o[12] = -(r + l) / (r - l); o[13] = -(t + b) / (t - b); o[14] = -(f + n) / (f - n); o[15] = 1; return o; }
  function norm(v) { var l = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / l, v[1] / l, v[2] / l]; }
  function cross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function lookAt(e, c, up) {
    var z = norm([e[0] - c[0], e[1] - c[1], e[2] - c[2]]), x = norm(cross(up, z)), y = cross(z, x), o = new Float32Array(16);
    o[0] = x[0]; o[4] = x[1]; o[8] = x[2]; o[1] = y[0]; o[5] = y[1]; o[9] = y[2]; o[2] = z[0]; o[6] = z[1]; o[10] = z[2];
    o[12] = -dot(x, e); o[13] = -dot(y, e); o[14] = -dot(z, e); o[15] = 1; return o;
  }
  function rotX(a) { var c = Math.cos(a), s = Math.sin(a); return new Float32Array([1, 0, 0, 0, 0, c, s, 0, 0, -s, c, 0, 0, 0, 0, 1]); }
  function rotY(a) { var c = Math.cos(a), s = Math.sin(a); return new Float32Array([c, 0, -s, 0, 0, 1, 0, 0, s, 0, c, 0, 0, 0, 0, 1]); }
  function rotZ(a) { var c = Math.cos(a), s = Math.sin(a); return new Float32Array([c, s, 0, 0, -s, c, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]); }

  /* ---------------- knot geometry with rotation-minimising frames ---------------- */
  function knot(p, q, US, VS) {
    var R = 1.0, r = 0.42, C = [], T = [];
    function pt(t) { var a = p * t, b = q * t, rr = R + r * Math.cos(b); return [rr * Math.cos(a), rr * Math.sin(a), r * Math.sin(b) * 1.6]; }
    for (var i = 0; i <= US; i++) { var t = i / US * Math.PI * 2; C.push(pt(t)); }
    for (i = 0; i <= US; i++) { var a = C[(i + US - 1) % US], b = C[(i + 1) % US]; T.push(norm([b[0] - a[0], b[1] - a[1], b[2] - a[2]])); }
    var N = [], B = [], n0 = norm(cross(T[0], [0, 0, 1])); if (!isFinite(n0[0])) n0 = [1, 0, 0];
    N[0] = n0; B[0] = cross(T[0], n0);
    for (i = 1; i <= US; i++) { var n = N[i - 1], tt = T[i]; var d = dot(n, tt); var nn = norm([n[0] - tt[0] * d, n[1] - tt[1] * d, n[2] - tt[2] * d]); N[i] = nn; B[i] = cross(tt, nn); }
    var tw = Math.atan2(dot(B[US], N[0]), dot(N[US], N[0])); // closure twist, spread along the tube
    var len = 0; for (i = 1; i <= US; i++) len += Math.hypot(C[i][0] - C[i - 1][0], C[i][1] - C[i - 1][1], C[i][2] - C[i - 1][2]);
    var nv = (US + 1) * (VS + 1), c = new Float32Array(nv * 3), nb = new Float32Array(nv * 6), uv = new Float32Array(nv * 2), k = 0;
    for (i = 0; i <= US; i++) {
      var ang = -tw * i / US, ca = Math.cos(ang), sa = Math.sin(ang);
      var Ni = [N[i][0] * ca + B[i][0] * sa, N[i][1] * ca + B[i][1] * sa, N[i][2] * ca + B[i][2] * sa], Bi = cross(T[i], Ni);
      for (var j = 0; j <= VS; j++, k++) {
        c.set(C[i], k * 3); nb.set(Ni, k * 6); nb.set(Bi, k * 6 + 3); uv[k * 2] = i / US; uv[k * 2 + 1] = j / VS;
      }
    }
    var idx = new Uint16Array(US * VS * 6), m = 0;
    for (i = 0; i < US; i++) for (j = 0; j < VS; j++) { var a0 = i * (VS + 1) + j, a1 = a0 + VS + 1; idx[m++] = a0; idx[m++] = a1; idx[m++] = a0 + 1; idx[m++] = a1; idx[m++] = a1 + 1; idx[m++] = a0 + 1; }
    return { c: c, nb: nb, uv: uv, idx: idx, len: len };
  }

  var VS_MESH = [
    'attribute vec3 a_c; attribute vec3 a_n; attribute vec3 a_b; attribute vec2 a_uv;',
    'uniform mat4 u_model, u_vp, u_lvp; uniform float u_tube, u_t;',
    'varying vec2 v_uv; varying vec3 v_nrm; varying vec3 v_wp; varying vec4 v_lp;',
    'void main(){',
    '  float u=a_uv.x*6.2831853, a=a_uv.y*6.2831853;',
    '  float r=u_tube*(1.0+0.30*sin(u*3.0+u_t*0.55)+0.14*sin(u*5.0-u_t*0.8)+0.06*sin(u*11.0+u_t*1.1));',
    '  vec3 dir=a_n*cos(a)+a_b*sin(a);',
    '  vec4 w=u_model*vec4(a_c+dir*r,1.0);',
    '  v_uv=a_uv; v_nrm=mat3(u_model)*dir; v_wp=w.xyz; v_lp=u_lvp*w;',
    '  gl_Position=u_vp*w;',
    '}'
  ].join('\n');

  var FS_SHADOW = [
    'precision highp float;',
    'vec4 pack(float d){vec4 e=fract(d*vec4(1.0,255.0,65025.0,16581375.0));e-=e.yzww*vec4(1.0/255.0,1.0/255.0,1.0/255.0,0.0);return e;}',
    'void main(){gl_FragColor=pack(gl_FragCoord.z);}'
  ].join('\n');

  var FS_MESH = [
    '#extension GL_OES_standard_derivatives : enable',
    'precision highp float;',
    'uniform sampler2D u_sm; uniform vec3 u_light; uniform vec3 u_eye; uniform vec2 u_cells; uniform float u_smres;',
    'uniform vec3 u_ink; uniform vec3 u_ink2; uniform vec3 u_paper; uniform float u_duo;',
    'varying vec2 v_uv; varying vec3 v_nrm; varying vec3 v_wp; varying vec4 v_lp;',
    'float unpack(vec4 c){return dot(c,vec4(1.0,1.0/255.0,1.0/65025.0,1.0/16581375.0));}',
    'vec2 h2(vec2 p){p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3)));return fract(sin(p)*43758.5453);}',
    'float shadow(){',
    '  vec3 p=v_lp.xyz/v_lp.w*0.5+0.5; float s=0.0;',
    '  for(int i=-1;i<=1;i++)for(int j=-1;j<=1;j++){',
    '    float d=unpack(texture2D(u_sm,p.xy+vec2(float(i),float(j))*1.5/u_smres));',
    '    s+=step(p.z-0.0035,d);',
    '  }',
    '  return s/9.0;',
    '}',
    'float dots(vec2 g, float tone, float seed){',
    '  float row=floor(g.y); g.x+=mod(row,2.0)*0.5;',
    '  vec2 id=floor(g); vec2 h=h2(id+seed); vec2 f=fract(g)-0.5-(h-0.5)*0.16;',
    '  float r=sqrt(tone)*0.76*(0.9+0.2*h.x); float d=length(f);',
    '  float aa=max(fwidth(d),0.0001)*0.85;',
    '  float cov=smoothstep(r+aa,r-aa,d);',
    '  float tiny=max(length(fwidth(g)),0.0);',
    '  return mix(cov,tone,smoothstep(0.55,1.1,tiny));',
    '}',
    'void main(){',
    '  vec3 N=normalize(v_nrm); vec3 V=normalize(u_eye-v_wp); if(dot(N,V)<0.0) N=-N;',
    '  vec3 L=normalize(u_light);',
    '  float dif=dot(N,L); float wrap=clamp((dif+0.18)/1.18,0.0,1.0);',
    '  float sh=shadow(); float sky=0.5+0.5*N.y;',
    '  float light=wrap*mix(0.22,1.0,sh)*1.0+0.16*sky;',
    '  float tone=smoothstep(0.2,0.95,1.0-light); tone=pow(tone,1.15);',
    '  float t1=tone; float t2=0.0;',
    '  if(u_duo>0.5){ vec3 L2=normalize(vec3(0.8,-0.25,0.5)); t2=pow(clamp(dot(N,L2),0.0,1.0),1.6)*0.85*(1.0-tone*0.6); t1*=1.0-0.5*t2; }',
    '  vec2 g=v_uv*u_cells;',
    '  float c1=dots(g,t1,0.0);',
    '  vec3 col=mix(u_paper,u_ink,c1);',
    '  if(u_duo>0.5){ float c2=dots(g+vec2(0.37,0.5),t2,7.0); col*=mix(vec3(1.0),u_ink2,c2); }',
    '  gl_FragColor=vec4(col,1.0);',
    '}'
  ].join('\n');

  var VS_QUAD = 'attribute vec2 p;void main(){gl_Position=vec4(p,0.999,1.0);}';
  var FS_BG = [
    'precision highp float;',
    'uniform vec3 u_ink; uniform vec3 u_paper; uniform float u_cell; uniform vec2 u_res; uniform float u_bg;',
    'vec2 h2(vec2 p){p=vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3)));return fract(sin(p)*43758.5453);}',
    'void main(){',
    '  vec2 px=gl_FragCoord.xy; vec2 b=floor(px/u_cell); float c=0.0;',
    '  vec2 q=px/u_res; float tone=u_bg*(0.25+0.06*sin(q.x*5.0+q.y*3.0)+0.05*sin(q.y*9.0-q.x*2.0));',
    '  for(int j=-1;j<=1;j++)for(int i=-1;i<=1;i++){',
    '    vec2 id=b+vec2(float(i),float(j)); vec2 h=h2(id); if(h.y>tone*2.2) continue;',
    '    vec2 cc=(id+0.5+(h-0.5)*0.9)*u_cell; float r=u_cell*(0.2+0.12*h.x);',
    '    c=max(c,clamp(r-length(px-cc)+0.5,0.0,1.0));',
    '  }',
    '  gl_FragColor=vec4(mix(u_paper,u_ink,c*0.85),1.0);',
    '}'
  ].join('\n');

  function hex(h) { h = h.replace('#', ''); return [parseInt(h.slice(0, 2), 16) / 255, parseInt(h.slice(2, 4), 16) / 255, parseInt(h.slice(4, 6), 16) / 255]; }
  function sh(gl, t, s) { var o = gl.createShader(t); gl.shaderSource(o, s); gl.compileShader(o); if (!gl.getShaderParameter(o, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; }
  function prog(gl, vs, fs, attrs) {
    var p = gl.createProgram(); gl.attachShader(p, sh(gl, gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl, gl.FRAGMENT_SHADER, fs));
    attrs.forEach(function (a, i) { gl.bindAttribLocation(p, i, a); }); gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p)); return p;
  }
  function U(gl, p, ns) { var o = {}; ns.forEach(function (n) { o[n] = gl.getUniformLocation(p, n); }); return o; }

  function init(el) {
    var d = el.dataset, pq = (d.knotPq || '2,3').split(',').map(Number), tube = parseFloat(d.knotTube || '0.46');
    var zoom = parseFloat(d.knotZoom || '1'), shift = (d.knotShift || '0,0').split(',').map(Number), tilt = (d.knotTilt || '0.4,0.2').split(',').map(Number);
    var duo = d.knotDuo !== undefined ? 1 : 0, bgOn = parseFloat(d.knotBg == null ? '1' : d.knotBg), dotCss = parseFloat(d.knotDot || '2.6'), speed = parseFloat(d.knotSpeed || '1');
    var ink = hex(d.knotInk || '#1B2A6B'), ink2 = hex('#E8906F'), paper = hex(d.knotPaper || '#F4EEE3');

    var canvas = document.createElement('canvas'); canvas.className = 'dots-canvas'; canvas.setAttribute('aria-hidden', 'true');
    var gl = canvas.getContext('webgl', { antialias: true, alpha: false }) || canvas.getContext('experimental-webgl');
    if (!gl || !gl.getExtension('OES_standard_derivatives')) return;
    var PM, PS, PB, um, us, ub;
    try {
      PM = prog(gl, VS_MESH, FS_MESH, ['a_c', 'a_n', 'a_b', 'a_uv']);
      PS = prog(gl, VS_MESH, FS_SHADOW, ['a_c', 'a_n', 'a_b', 'a_uv']);
      PB = prog(gl, VS_QUAD, FS_BG, ['p']);
    } catch (e) { if (window.console) console.warn('riso-knot', e); return; }
    um = U(gl, PM, ['u_model', 'u_vp', 'u_lvp', 'u_tube', 'u_t', 'u_sm', 'u_light', 'u_eye', 'u_cells', 'u_smres', 'u_ink', 'u_ink2', 'u_paper', 'u_duo']);
    us = U(gl, PS, ['u_model', 'u_vp', 'u_lvp', 'u_tube', 'u_t']);
    ub = U(gl, PB, ['u_ink', 'u_paper', 'u_cell', 'u_res', 'u_bg']);

    var US = 720, VSG = 88, G = knot(pq[0], pq[1], US, VSG);
    function vbo(data) { var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW); return b; }
    var bC = vbo(G.c), bNB = vbo(G.nb), bUV = vbo(G.uv), bQ = vbo(new Float32Array([-1, -1, 3, -1, -1, 3]));
    var bI = gl.createBuffer(); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, bI); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, G.idx, gl.STATIC_DRAW);
    function bindMesh() {
      gl.bindBuffer(gl.ARRAY_BUFFER, bC); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ARRAY_BUFFER, bNB); gl.enableVertexAttribArray(1); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 24, 0);
      gl.enableVertexAttribArray(2); gl.vertexAttribPointer(2, 3, gl.FLOAT, false, 24, 12);
      gl.bindBuffer(gl.ARRAY_BUFFER, bUV); gl.enableVertexAttribArray(3); gl.vertexAttribPointer(3, 2, gl.FLOAT, false, 0, 0);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, bI);
    }
    var SM = 1024, smTex = gl.createTexture(), smFbo = gl.createFramebuffer(), smDepth = gl.createRenderbuffer();
    gl.bindTexture(gl.TEXTURE_2D, smTex); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, SM, SM, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.bindRenderbuffer(gl.RENDERBUFFER, smDepth); gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT16, SM, SM);
    gl.bindFramebuffer(gl.FRAMEBUFFER, smFbo); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, smTex, 0);
    gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, smDepth); gl.bindFramebuffer(gl.FRAMEBUFFER, null);

    var light = norm([-0.62, 0.72, 0.42]);
    var lvp = mul(ortho(-2.3, 2.3, -2.3, 2.3, 0.1, 10), lookAt([light[0] * 5, light[1] * 5, light[2] * 5], [0, 0, 0], [0, 1, 0]));
    var W = 0, H = 0, dpr = 1, raf = 0, visible = true, t0 = performance.now(), cells = [1, 1], vp, eye;

    function resize() {
      var r = el.getBoundingClientRect(); dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = Math.max(2, Math.round(r.width * dpr)), h = Math.max(2, Math.round(r.height * dpr));
      if (w === W && h === H) return; W = canvas.width = w; H = canvas.height = h;
      var fov = 0.62, dist = 5.2 / zoom; eye = [0, 0, dist];
      var proj = persp(fov, W / H, 0.1, 30);
      var view = lookAt(eye, [0, 0, 0], [0, 1, 0]); view[12] -= shift[0]; view[13] -= shift[1];
      vp = mul(proj, view);
      var worldPerPx = 2 * dist * Math.tan(fov / 2) / H;               // at the knot's depth
      var cellWorld = dotCss * dpr * worldPerPx;
      cells = [Math.max(8, Math.round(G.len / cellWorld)), 2 * Math.max(4, Math.round(Math.PI * 2 * tube / cellWorld / 2))];
      if (reduce || !raf) draw(reduce ? 14 : (performance.now() - t0) / 1000);
    }

    function model(t) {
      var m = mul(rotY(tilt[1] + 0.35 * Math.sin(t * 0.07)), rotX(tilt[0] + 0.22 * Math.sin(t * 0.05 + 1.3)));
      return mul(m, rotZ(t * 0.045));
    }

    function draw(t) {
      if (!vp) return; t = t * speed; var M = model(t);
      // shadow map
      gl.bindFramebuffer(gl.FRAMEBUFFER, smFbo); gl.viewport(0, 0, SM, SM); gl.clearColor(1, 1, 1, 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      gl.enable(gl.DEPTH_TEST); gl.disable(gl.CULL_FACE); gl.useProgram(PS); bindMesh();
      gl.uniformMatrix4fv(us.u_model, false, M); gl.uniformMatrix4fv(us.u_vp, false, lvp); gl.uniformMatrix4fv(us.u_lvp, false, lvp);
      gl.uniform1f(us.u_tube, tube); gl.uniform1f(us.u_t, t);
      gl.drawElements(gl.TRIANGLES, G.idx.length, gl.UNSIGNED_SHORT, 0);
      // background stipple
      gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, W, H); gl.clearColor(paper[0], paper[1], paper[2], 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      gl.disable(gl.DEPTH_TEST); gl.useProgram(PB); gl.bindBuffer(gl.ARRAY_BUFFER, bQ);
      for (var i = 1; i < 4; i++) gl.disableVertexAttribArray(i);
      gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
      gl.uniform3fv(ub.u_ink, ink); gl.uniform3fv(ub.u_paper, paper); gl.uniform1f(ub.u_cell, 1.9 * dpr); gl.uniform2f(ub.u_res, W, H); gl.uniform1f(ub.u_bg, bgOn);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      // the print
      gl.enable(gl.DEPTH_TEST); gl.useProgram(PM); bindMesh();
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, smTex); gl.uniform1i(um.u_sm, 0); gl.uniform1f(um.u_smres, SM);
      gl.uniformMatrix4fv(um.u_model, false, M); gl.uniformMatrix4fv(um.u_vp, false, vp); gl.uniformMatrix4fv(um.u_lvp, false, lvp);
      gl.uniform1f(um.u_tube, tube); gl.uniform1f(um.u_t, t); gl.uniform3fv(um.u_light, light); gl.uniform3fv(um.u_eye, [eye[0] + shift[0], eye[1] + shift[1], eye[2]]);
      gl.uniform2f(um.u_cells, cells[0], cells[1]); gl.uniform3fv(um.u_ink, ink); gl.uniform3fv(um.u_ink2, ink2); gl.uniform3fv(um.u_paper, paper); gl.uniform1f(um.u_duo, duo);
      gl.drawElements(gl.TRIANGLES, G.idx.length, gl.UNSIGNED_SHORT, 0);
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

  function boot() { [].forEach.call(document.querySelectorAll('[data-knot]'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
