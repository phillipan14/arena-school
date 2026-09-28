var ZHL = (document.documentElement.lang || '').toLowerCase().indexOf('zh') === 0;
/* Program pages: interaction layer. Scroll progress, notes<->pins highlighting,
   pathway bars that grow in, and smooth FAQ open/close. Reduced motion is respected. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Scroll progress bar
  var bar = document.createElement('div'); bar.className = 'pp-progress'; bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  var ticking = false;
  function paint() { var h = document.documentElement; var p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight); bar.style.transform = 'scaleX(' + p.toFixed(4) + ')'; ticking = false; }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(paint); } }, { passive: true });
  paint();

  // Notes and numbered pins light each other up
  document.querySelectorAll('.pp-example').forEach(function (ex) {
    var pins = [].slice.call(ex.querySelectorAll('.pp-pin'));
    var notes = [].slice.call(ex.querySelectorAll('.pp-notes li'));
    function set(n, on) {
      pins.forEach(function (p) { if (p.textContent.trim() === String(n)) p.classList.toggle('is-on', on); });
      if (notes[n - 1]) notes[n - 1].classList.toggle('is-on', on);
    }
    notes.forEach(function (li, i) {
      li.addEventListener('mouseenter', function () { set(i + 1, true); });
      li.addEventListener('mouseleave', function () { set(i + 1, false); });
    });
    pins.forEach(function (p) {
      var n = +p.textContent.trim();
      p.addEventListener('mouseenter', function () { set(n, true); });
      p.addEventListener('mouseleave', function () { set(n, false); });
    });
  });

  // Pathway bars grow in when scrolled into view
  var pw = [].slice.call(document.querySelectorAll('.pp-pw'));
  if (!reduce && 'IntersectionObserver' in window) {
    pw.forEach(function (el) { el.classList.add('is-hidden'); });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.remove('is-hidden'); io.unobserve(e.target); } });
    }, { threshold: 0.3 });
    pw.forEach(function (el) { io.observe(el); });
  }

  // FAQ: animate height on open/close
  if (!reduce) document.querySelectorAll('.faq-item').forEach(function (d) {
    var s = d.querySelector('summary'); var a = d.querySelector('.faq-a'); if (!s || !a) return;
    s.addEventListener('click', function (e) {
      e.preventDefault();
      if (d.open) {
        a.animate([{ opacity: 1, transform: 'none' }, { opacity: 0, transform: 'translateY(-4px)' }], { duration: 160 }).onfinish = function () { d.open = false; };
      } else {
        d.open = true;
        a.animate([{ opacity: 0, transform: 'translateY(-6px)' }, { opacity: 1, transform: 'none' }], { duration: 260, easing: 'cubic-bezier(.2,.7,.2,1)' });
      }
    });
  });
})();

/* Live sample portfolio: tabs, video player, depth explorer */
(function () {
  document.querySelectorAll('[data-live]').forEach(function (root) {
    var tabs = [].slice.call(root.querySelectorAll('.pp-tabs button'));
    var panels = [].slice.call(root.querySelectorAll('.pp-panel'));
    var path = root.querySelector('.pp-url-path');
    function show(name) {
      tabs.forEach(function (t) { t.setAttribute('aria-selected', String(t.dataset.tab === name)); });
      panels.forEach(function (p) { var on = p.dataset.panel === name; p.hidden = !on; if (on) { p.style.animation = 'none'; p.offsetHeight; p.style.animation = ''; } });
      if (path) path.textContent = name === 'projects' ? '' : '/' + name;
    }
    tabs.forEach(function (t) { t.addEventListener('click', function () { show(t.dataset.tab); }); });
    root.querySelectorAll('[data-tab-go]').forEach(function (b) { b.addEventListener('click', function () { show(b.dataset.tabGo); }); });

    // Video: a simulated player over the field survey still
    var video = root.querySelector('.pp-video'); var raf = null; var t0 = 0; var elapsed = 0; var DUR = 135;
    var track = video && video.querySelector('.pp-video-track i'); var time = video && video.querySelector('.pp-video-t'); var pp = video && video.querySelector('.pp-video-pp');
    function fmt(s) { s = Math.floor(s); return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2); }
    function tick(now) { var e = elapsed + (now - t0) / 1000 * 6; if (e >= DUR) e = 0; track.style.width = (e / DUR * 100) + '%'; time.textContent = fmt(e) + ' / 2:15'; raf = requestAnimationFrame(tick); video._e = e; }
    function play() { video.classList.add('is-playing'); t0 = performance.now(); raf = requestAnimationFrame(tick); pp.textContent = '❚❚'; pp.setAttribute('aria-label', ZHL ? '暂停' : 'Pause'); }
    function pause() { video.classList.remove('is-playing'); cancelAnimationFrame(raf); elapsed = video._e || 0; pp.textContent = '▶'; pp.setAttribute('aria-label', ZHL ? '播放' : 'Play'); }
    if (video) {
      root.querySelector('[data-open="video"]').addEventListener('click', function () { video.hidden = false; elapsed = 0; play(); });
      video.querySelector('.pp-video-x').addEventListener('click', function () { pause(); video.hidden = true; });
      pp.addEventListener('click', function () { video.classList.contains('is-playing') ? pause() : play(); });
      root.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !video.hidden) { pause(); video.hidden = true; } });
    }

    // Depth explorer: slider moves the marker along the curve
    var range = root.querySelector('.pp-dx input'); var out = root.querySelector('.pp-dx output');
    var line = root.querySelector('.dx-line'); var dot = root.querySelector('.dx-dot'); var guide = root.querySelector('.dx-guide');
    var readD = root.querySelector('.pp-dx-read b'); var readN = root.querySelector('.pp-dx-read span');
    if (range && line) {
      var L = line.getTotalLength();
      function yAt(x) { var lo = 0, hi = L; for (var i = 0; i < 24; i++) { var mid = (lo + hi) / 2; if (line.getPointAtLength(mid).x < x) lo = mid; else hi = mid; } return line.getPointAtLength(lo).y; }
      function update() {
        var d = +range.value; var x = d / 30 * 300; var y = yAt(x);
        dot.setAttribute('cx', x); dot.setAttribute('cy', y); guide.setAttribute('x1', x); guide.setAttribute('x2', x);
        var n = Math.round((150 - y) / 150 * 60);
        out.textContent = d + ' m'; readD.textContent = d + ' m'; readN.textContent = n;
      }
      range.addEventListener('input', update); update();
    }
  });
})();

/* Osmosis demo: more salt outside, the cell shrinks */
document.querySelectorAll('[data-osmo]').forEach(function (el) {
  var r = el.querySelector('input'), o = el.querySelector('output'), c = el.querySelector('.pp-osmo-cell');
  function u() { var v = +r.value; o.textContent = v + '%'; c.style.setProperty('--k', (1.25 - v / 100 * 0.75).toFixed(3)); }
  r.addEventListener('input', u); u();
});
