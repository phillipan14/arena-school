/* elegance.js: tabs and carousel arrows for the elegance-pass pages (css/elegance.css).
   Tabs: [data-el-tabs] holds buttons with role="tab" and aria-controls; panels are toggled with `hidden`.
   Arrow keys move between tabs. Carousels: [data-el-car] holds a .el-car-track plus [data-el-prev]/[data-el-next]
   buttons; the track itself is a native scroll-snap row, so touch and trackpad swipes work without JS. */
(function () {
  function select(list, tab) {
    var tabs = [].slice.call(list.querySelectorAll('[role="tab"]'));
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      var panel = document.getElementById(t.getAttribute('aria-controls'));
      if (panel) {
        panel.hidden = !on;
        // content that was hidden when motion.js observed it would otherwise stay faded out
        if (on) panel.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('in'); });
      }
    });
  }

  document.querySelectorAll('[data-el-tabs]').forEach(function (list) {
    var tabs = [].slice.call(list.querySelectorAll('[role="tab"]'));
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(list, t); });
      t.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var next = tabs[(i + d + tabs.length) % tabs.length];
        select(list, next);
        next.focus();
      });
    });
  });

  document.querySelectorAll('[data-el-car]').forEach(function (car) {
    var track = car.querySelector('.el-car-track');
    var prev = car.querySelector('[data-el-prev]');
    var next = car.querySelector('[data-el-next]');
    if (!track) return;
    function step() {
      var first = track.firstElementChild;
      var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      return first ? first.getBoundingClientRect().width + gap : track.clientWidth;
    }
    function sync() {
      var max = track.scrollWidth - track.clientWidth - 2;
      if (prev) prev.disabled = track.scrollLeft <= 2;
      if (next) next.disabled = track.scrollLeft >= max;
    }
    if (prev) prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    if (next) next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
    track.addEventListener('scroll', function () { requestAnimationFrame(sync); }, { passive: true });
    window.addEventListener('resize', sync);
    sync();
  });
})();
