/* Homepage gallery: rows drift apart as the page scrolls (on top of their loop). Videos play only on screen. */
(function () {
  var g = document.querySelector('.gal2'); if (!g) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var l = g.querySelector('.gal-l'), r = g.querySelector('.gal-r'), tick = false;
  function paint() {
    var rect = g.getBoundingClientRect(); var p = (innerHeight - rect.top) / (innerHeight + rect.height);
    p = Math.max(0, Math.min(1, p)); var d = (p - 0.5) * 160;
    l.style.setProperty('--gx', (-d).toFixed(1) + 'px'); r.style.setProperty('--gx', d.toFixed(1) + 'px'); tick = false;
  }
  if (!reduce) { addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(paint); } }, { passive: true }); paint(); }
  var vids = [].slice.call(g.querySelectorAll('video'));
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.preload = 'auto'; e.target.play().catch(function () {}); } else e.target.pause(); }); });
    vids.forEach(function (v) { io.observe(v); });
  }
})();
