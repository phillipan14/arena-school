/* Homepage journey: hovering a program lights its grade range on the axis. */
(function () {
  var j = document.querySelector('.pp-jr'); if (!j) return;
  var nodes = [].slice.call(j.querySelectorAll('.pp-jr-line li'));
  j.querySelectorAll('.pp-jr-card[data-from]').forEach(function (c) {
    var a = +c.dataset.from, b = +c.dataset.to;
    function on() { j.classList.add('dim'); c.classList.add('hot'); nodes.forEach(function (n, i) { n.classList.toggle('on', i + 6 >= a && i + 6 <= b); }); }
    function off() { j.classList.remove('dim'); c.classList.remove('hot'); nodes.forEach(function (n) { n.classList.remove('on'); }); }
    c.addEventListener('mouseenter', on); c.addEventListener('mouseleave', off); c.addEventListener('focus', on); c.addEventListener('blur', off);
  });
})();
