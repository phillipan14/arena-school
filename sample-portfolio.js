/* Sample portfolio callouts: hovering or focusing a callout highlights the
   matching part of the mock (data-hl groups: work, thinking, follow).
   Reduced-motion safe (only toggles classes; no motion of its own). */
(function () {
  document.querySelectorAll('.sf-wrap').forEach(function (wrap) {
    var notes = [].slice.call(wrap.querySelectorAll('.sf-note'));
    if (!notes.length) return;

    function targets(key) {
      return [].slice.call(wrap.querySelectorAll('[data-hl="' + key + '"]'));
    }
    function setGroup(key, on) {
      targets(key).forEach(function (el) { el.classList.toggle('is-hl', on); });
    }

    notes.forEach(function (li) {
      var key = li.getAttribute('data-hl');
      if (!key) return;
      function on() { setGroup(key, true); li.classList.add('is-active'); }
      function off() { setGroup(key, false); li.classList.remove('is-active'); }
      li.addEventListener('mouseenter', on);
      li.addEventListener('mouseleave', off);
      li.addEventListener('focus', on);
      li.addEventListener('blur', off);
    });
  });
})();
