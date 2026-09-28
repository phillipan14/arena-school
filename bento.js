/* Homepage photo grid: each tile gently crossfades between two photos, staggered. */
(function () {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var tiles = [].slice.call(document.querySelectorAll('.bt')).filter(function (t) { return t.querySelector('.bt-alt'); });
  tiles.forEach(function (t, i) {
    var alt = t.querySelector('.bt-alt'), cap = t.querySelector('figcaption'), a = cap.innerHTML;
    var b = '<span>' + alt.dataset.loc + '</span>' + alt.dataset.cap;
    setTimeout(function () {
      setInterval(function () {
        t.classList.add('cap-fade');
        setTimeout(function () { var on = t.classList.toggle('swap'); cap.innerHTML = on ? b : a; t.classList.remove('cap-fade'); }, 450);
      }, 7000);
    }, 1200 + i * 1100);
  });
})();
