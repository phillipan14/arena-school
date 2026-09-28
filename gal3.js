/* Homepage collage: each photo drifts at its own speed while the section scrolls by. */
(function () {
  var stage = document.querySelector('.g3-stage'); if (!stage) return;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, wide = matchMedia('(min-width: 981px)');
  var tiles = [].slice.call(stage.querySelectorAll('.g3-tile')), tick = false;
  function paint() {
    tick = false; if (!wide.matches) { tiles.forEach(function (t) { t.style.removeProperty('--py'); }); return; }
    var r = stage.getBoundingClientRect(); var p = (innerHeight / 2 - (r.top + r.height / 2));
    tiles.forEach(function (t) { t.style.setProperty('--py', (p * +t.dataset.speed).toFixed(1) + 'px'); });
  }
  if (!reduce) { addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(paint); } }, { passive: true }); addEventListener('resize', paint); paint(); }
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.preload = 'auto'; e.target.play().catch(function () {}); } else e.target.pause(); }); });
    stage.querySelectorAll('video').forEach(function (v) { io.observe(v); });
  }
})();
