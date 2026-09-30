/* Program pages: count-up stats ([data-count]) and a typed activity line ([data-type])
   that fills its 150-character box. Runs once when scrolled into view; with reduced
   motion (or no IntersectionObserver) everything shows in its final state. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function fmt(el, v) {
    var dec = +(el.getAttribute('data-dec') || 0);
    el.firstChild.nodeValue = v.toFixed(dec);
  }
  function countUp(el) {
    var end = parseFloat(el.getAttribute('data-count')); var t0 = null; var dur = 1100;
    function step(t) { t0 = t0 || t; var p = Math.min(1, (t - t0) / dur); fmt(el, end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); }
    requestAnimationFrame(step);
  }
  function type(el) {
    var text = el.getAttribute('data-type'); var box = el.parentElement.querySelector('.pp-count');
    var num = box && box.querySelector('i'); var max = +(el.getAttribute('data-max') || 150); var i = 0;
    el.classList.add('is-typing');
    (function tick() {
      i++; el.textContent = text.slice(0, i); if (num) num.textContent = i;
      if (i < text.length) { setTimeout(tick, 22); } else { el.classList.remove('is-typing'); if (box && i >= max - 25) box.classList.add('is-full'); }
    })();
  }
  var counts = [].slice.call(document.querySelectorAll('[data-count]'));
  var typed = [].slice.call(document.querySelectorAll('[data-type]'));
  function finish() {
    counts.forEach(function (el) { fmt(el, parseFloat(el.getAttribute('data-count'))); });
    typed.forEach(function (el) {
      var t = el.getAttribute('data-type'); el.textContent = t;
      var box = el.parentElement.querySelector('.pp-count i'); if (box) box.textContent = t.length;
    });
  }
  if (reduce || !('IntersectionObserver' in window)) { finish(); return; }
  counts.forEach(function (el) { fmt(el, 0); });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return; io.unobserve(e.target);
      if (e.target.hasAttribute('data-count')) countUp(e.target); else type(e.target);
    });
  }, { threshold: 0.5 });
  counts.concat(typed).forEach(function (el) { io.observe(el); });
})();
