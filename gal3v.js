/* Homepage carousel videos play only while on screen. */
(function () {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { var v = e.target; if (e.isIntersecting) { v.preload = 'auto'; v.play().catch(function () {}); } else v.pause(); }); }, { threshold: 0.1 });
  document.querySelectorAll('.gm video').forEach(function (v) { io.observe(v); });
})();
