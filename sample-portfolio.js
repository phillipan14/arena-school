/* Sample portfolio: callout <-> mock hover highlighting, a cinematic one-time
   entrance when the section first scrolls into view, the depth chart drawing
   itself in, and a short auto-tour of the tabs that stops on any interaction.
   Reduced-motion safe throughout: entrance/tour/draw-in are skipped entirely
   and content is shown at full opacity immediately. */
(function () {
  var REDUCE = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('.sf-wrap').forEach(function (wrap) {
    initHighlights(wrap);
    initEntrance(wrap);
  });

  /* Callouts <-> mock hover/focus highlight */
  function initHighlights(wrap) {
    var notes = [].slice.call(wrap.querySelectorAll('.sf-note'));
    if (!notes.length) return;
    function targets(key) { return [].slice.call(wrap.querySelectorAll('[data-hl="' + key + '"]')); }
    function setGroup(key, on) { targets(key).forEach(function (el) { el.classList.toggle('is-hl', on); }); }
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
  }

  /* One-time cinematic entrance + chart draw-in + auto-tour, triggered together
     the first time the mock scrolls into view. */
  function initEntrance(wrap) {
    var mock = wrap.querySelector('.sf-mock');
    if (!mock || REDUCE) return; // reduced motion: leave content at full opacity, no tour
    wrap.classList.add('sf-pending');
    if (!('IntersectionObserver' in window)) { wrap.classList.add('sf-revealed'); drawChart(wrap); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        wrap.classList.add('sf-revealed');
        drawChart(wrap);
        startTour(wrap);
        io.unobserve(entry.target);
      });
    }, { threshold: 0.3 });
    io.observe(mock);
  }

  /* The depth-explorer line draws itself in on reveal. Only the stroke's dash
     animation changes; the path geometry (and so the slider's math in
     pp-interact.js) is untouched. */
  function drawChart(wrap) {
    var line = wrap.querySelector('.dx-line');
    if (!line || typeof line.getTotalLength !== 'function') return;
    var len = line.getTotalLength();
    line.style.strokeDasharray = len;
    line.style.strokeDashoffset = len;
    line.getBoundingClientRect(); // force layout before animating
    requestAnimationFrame(function () {
      line.style.transition = 'stroke-dashoffset 1.2s cubic-bezier(.16,1,.3,1) .3s';
      line.style.strokeDashoffset = '0';
    });
  }

  /* A short, gentle tour: Projects (start) -> Research -> Awards -> back to
     Projects, once. Stops immediately on any pointer/keyboard/scroll
     interaction with the mock, and never restarts. */
  function startTour(wrap) {
    var tabs = [].slice.call(wrap.querySelectorAll('.sf-tabs button'));
    if (tabs.length < 3) return;
    var order = ['research', 'awards', 'projects'];
    var i = -1, timer = null, stopped = false;
    function stop() {
      if (stopped) return;
      stopped = true;
      if (timer) clearTimeout(timer);
    }
    ['pointerdown', 'wheel', 'touchstart', 'keydown', 'mouseenter'].forEach(function (ev) {
      wrap.addEventListener(ev, stop, { once: true, passive: true });
    });
    function step() {
      if (stopped) return;
      i++;
      if (i >= order.length) return;
      var btn = wrap.querySelector('.sf-tabs button[data-tab="' + order[i] + '"]');
      if (btn) btn.click();
      timer = setTimeout(step, 2400);
    }
    timer = setTimeout(step, 2000);
  }
})();
