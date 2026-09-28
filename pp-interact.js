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
