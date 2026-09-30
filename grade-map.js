/* Homepage grade map: draw the bars when the chart scrolls into view (once). */
(() => {
  const map = document.querySelector('[data-gmap]');
  if (!map) return;
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) { map.classList.add('is-in'); return; }
  const io = new IntersectionObserver((entries) => {
    if (entries.some((e) => e.isIntersecting)) { map.classList.add('is-in'); io.disconnect(); }
  }, { threshold: 0.35 });
  io.observe(map);
})();
