/* Homepage hero: the arch crossfades through program videos and photos. */
(function () {
  var f = document.querySelector('[data-arch]'); if (!f) return;
  var slides = [].slice.call(f.querySelectorAll('.arch-slide')), dots = [].slice.call(f.querySelectorAll('.arch-dots i'));
  var cap = f.querySelector('.arch-cap') || document.querySelector('.hero-photo-cap .arch-cap'), k = 0, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function show(n) {
    slides.forEach(function (s, i) {
      var on = i === n; s.classList.toggle('is-on', on);
      var v = s.querySelector('video');
      if (v) { if (on) { v.preload = 'auto'; v.currentTime = 0; v.play().catch(function () {}); } else v.pause(); }
      if (on) { var im = s.querySelector('img'); if (im) { im.style.animation = 'none'; im.offsetHeight; im.style.animation = ''; } }
    });
    dots.forEach(function (d, i) { d.classList.toggle('on', i === n); });
    if (cap) cap.textContent = slides[n].dataset.cap;
  }
  show(0);
  if (reduce) return;
  var t = setInterval(function () { k = (k + 1) % slides.length; show(k); }, 5000);
  document.addEventListener('visibilitychange', function () { if (document.hidden) clearInterval(t); else t = setInterval(function () { k = (k + 1) % slides.length; show(k); }, 5000); });
})();
