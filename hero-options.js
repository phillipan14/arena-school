/* Arena: header options preview (A social kit · B light print · C animated words · D network).
   Choose with ?hero=A|B|C|D|navy or the chooser panel; the choice is remembered while browsing. */
(function () {
  'use strict';
  // Chosen design (Sept 28): A, the social-kit header. ?hero=B|C|D|navy still previews the alternatives.
  var v = (location.search.match(/[?&]hero=([A-Dn][a-z]*)/) || [])[1] || 'A';
  var hero = document.querySelector('section.hero-inv, section.hero.hero-inv, section.curr-hero.hero-inv');
  if (!hero) return;
  if (v !== 'navy') {
    document.body.setAttribute('data-hero', v);
    hero.classList.remove('hero-inv'); hero.classList.add('hero-opt', 'hero-opt-' + v);
    document.body.classList.remove('zl-page');
  }
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var h1 = hero.querySelector('h1');

  /* marker words: the h1's italic words (em) are the key words */
  function splitWords(el) {
    var out = [];
    [].slice.call(el.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        var frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(function (w) {
          if (!w) return;
          if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(w)); return; }
          var s = document.createElement('span'); s.className = 'hw'; s.textContent = w; frag.appendChild(s); out.push(s);
        });
        n.parentNode.replaceChild(frag, n);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') {
        var inner = splitWords(n); inner.forEach(function (s) { if (n.tagName === 'EM') s.classList.add('hw-key'); }); out = out.concat(inner);
      }
    });
    return out;
  }
  if ((v === 'A' || v === 'B') && h1) {   // key words: a riso marker sweeps under each word, then repeats
    var all = splitWords(h1), keysA = all.filter(function (w) { return w.classList.contains('hw-key'); });
    if (!keysA.length) keysA = [all[all.length - 1]];
    keysA.forEach(function (w) { w.classList.add('hw-key', 'hw-m'); });
    var timers = [];
    function sweep() {
      timers.forEach(clearTimeout); timers = [];
      keysA.forEach(function (w) { w.classList.remove('hw-on'); });
      keysA.forEach(function (w, k) { timers.push(setTimeout(function () { w.classList.add('hw-on'); }, 380 + k * 230)); });
    }
    if (reduce) keysA.forEach(function (w) { w.classList.add('hw-on'); });
    else {
      setTimeout(sweep, 350);
      setInterval(function () { if (!document.hidden) sweep(); }, 7000);
      h1.addEventListener('pointerenter', sweep);
    }
  }
  if (v === 'C' && h1) {   // the marker travels across the headline, then settles on the key words
    var words = splitWords(h1), keysC = words.filter(function (s) { return s.classList.contains('hw-key'); });
    if (!keysC.length) keysC = [words[words.length - 1]];
    keysC.forEach(function (k) { k.classList.add('hw-key'); });
    if (reduce) { keysC.forEach(function (k) { k.classList.add('hw-on'); }); }
    else {
      var i = 0, settle = function () { words.forEach(function (s) { s.classList.remove('hw-on', 'hw-pass'); }); keysC.forEach(function (k) { k.classList.add('hw-on'); }); };
      var run = function () {
        words.forEach(function (s) { s.classList.remove('hw-on'); }); i = 0;
        var t = setInterval(function () {
          words.forEach(function (s) { s.classList.remove('hw-pass'); });
          if (i >= words.length) { clearInterval(t); settle(); setTimeout(run, 6500); return; }
          words[i].classList.add('hw-pass'); i++;
        }, 170);
      };
      setTimeout(run, 500);
    }
  }
  if (v === 'D') {   // a quiet network on the dot grid, right side only
    var c = document.createElement('canvas'); c.className = 'hero-net'; c.setAttribute('aria-hidden', 'true'); hero.insertBefore(c, hero.firstChild);
    var ctx = c.getContext('2d'), P = 24, nodes = [], edges = [], W = 0, H = 0, dpr = Math.min(window.devicePixelRatio || 1, 2), t0 = performance.now();
    function rnd(n) { var x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); }
    function build() {
      var r = hero.getBoundingClientRect(); W = r.width; H = r.height; c.width = W * dpr; c.height = H * dpr; c.style.width = W + 'px'; c.style.height = H + 'px';
      nodes = []; edges = [];
      var cols = Math.floor(W / P), rows = Math.floor(H / P), n = 0;
      var cp = hero.querySelector('.container h1'), cpx = cp ? Math.max.apply(null, [].map.call(hero.querySelectorAll('.container h1, .container .lede, .container p, .container .hero-cta, .container .zl-hero-cta'), function (e) { var rr = e.getBoundingClientRect(); return rr.width ? rr.right - r.left : 0; })) : W * 0.55;
      var x0 = Math.min(W - P * 8, cpx + P * 3) / W;
      for (var k = 0; k < Math.round(30 + 40 * (0.98 - x0)); k++) {
        var gx = Math.floor(cols * (x0 + (0.98 - x0) * rnd(k + 1))), gy = Math.floor(rows * (0.14 + 0.72 * rnd(k + 51)));
        nodes.push({ x: gx * P + P / 2, y: gy * P + P / 2, ph: rnd(k + 9) * 6.28, big: rnd(k + 3) < 0.25 });
      }
      nodes.forEach(function (a, i) {
        var near = nodes.map(function (b, j) { return [Math.hypot(a.x - b.x, a.y - b.y), j]; }).filter(function (d) { return d[1] !== i; }).sort(function (x, y) { return x[0] - y[0]; }).slice(0, 2);
        near.forEach(function (d) { if (d[0] < P * 9 && i < d[1]) edges.push([i, d[1], rnd(i * 7 + d[1]) * 6.28]); });
      });
    }
    function dotted(ax, ay, bx, by, alpha) {
      var len = Math.hypot(bx - ax, by - ay), steps = Math.floor(len / 5);
      for (var s = 0; s <= steps; s++) { var u = s / steps; ctx.globalAlpha = alpha; ctx.beginPath(); ctx.arc(ax + (bx - ax) * u, ay + (by - ay) * u, 1.05, 0, 6.283); ctx.fill(); }
    }
    function draw(now) {
      var t = reduce ? 0 : (now - t0) / 1000;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#2F55A8';
      edges.forEach(function (e) {
        var a = nodes[e[0]], b = nodes[e[1]], on = 0.5 + 0.5 * Math.sin(t * 0.35 + e[2]);
        if (on < 0.25) return; dotted(a.x, a.y, b.x, b.y, 0.18 + 0.5 * (on - 0.25));
        var u = (t * 0.12 + e[2] / 6.28) % 1; ctx.globalAlpha = 0.85 * on; ctx.beginPath(); ctx.arc(a.x + (b.x - a.x) * u, a.y + (b.y - a.y) * u, 2.2, 0, 6.283); ctx.fill();
      });
      ctx.fillStyle = '#0B1A4A';
      nodes.forEach(function (nd) { ctx.globalAlpha = 0.9; ctx.beginPath(); ctx.arc(nd.x, nd.y, nd.big ? 4.2 : 2.6 + 0.4 * Math.sin(t * 1.2 + nd.ph), 0, 6.283); ctx.fill(); });
      ctx.globalAlpha = 1; if (!reduce) requestAnimationFrame(draw);
    }
    build(); requestAnimationFrame(draw); window.addEventListener('resize', build);
  }

})();
