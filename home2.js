/* Homepage: program links and grade timeline highlight each other. */
(function () {
  var groups = {};
  document.querySelectorAll('[data-prog]').forEach(function (el) { (groups[el.dataset.prog] = groups[el.dataset.prog] || []).push(el); });
  Object.keys(groups).forEach(function (k) {
    var els = groups[k];
    function set(on) { els.forEach(function (e) { e.classList.toggle('on', on); }); }
    els.forEach(function (e) {
      e.addEventListener('mouseenter', function () { set(true); }); e.addEventListener('mouseleave', function () { set(false); });
      e.addEventListener('focus', function () { set(true); }); e.addEventListener('blur', function () { set(false); });
    });
  });
})();
