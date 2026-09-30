/* Sample portfolio: an accordion of callouts (one open at a time, first open by
   default) that drives the mock's region highlight/pins; a JS-reinforced sticky
   so the column tracks the mock as the page scrolls; a cinematic one-time
   entrance; the depth chart drawing itself in; and a short auto-tour of the
   tabs that stops on any interaction.
   Reduced-motion safe throughout: entrance/tour/draw-in are skipped entirely
   and content is shown at full opacity immediately. Accordion open/close and
   sticky tracking are positional, not decorative, so they still run either way. */
(function () {
  var REDUCE = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('.sf-wrap').forEach(function (wrap) {
    initAccordion(wrap);
    initSticky(wrap);
    initEntrance(wrap);
  });

  /* Callouts: exactly one open at a time (first open by default, set in markup).
     Opening a callout (click, Enter/Space, or a brief hover pause) sets the
     mock's region highlight/pins to match. */
  function initAccordion(wrap) {
    var items = [].slice.call(wrap.querySelectorAll('.sf-note'));
    if (!items.length) return;
    function targets(key) { return [].slice.call(wrap.querySelectorAll('[data-hl="' + key + '"]')); }
    function setGroup(key, on) { targets(key).forEach(function (el) { el.classList.toggle('is-hl', on); }); }

    // Opening/closing an item changes the column's height, which can shift a
    // lower row under a mouse that never actually moved. Browsers still fire
    // a genuine mouseenter for that, so hover-intent is suppressed briefly
    // after any open() (click, focus, or a completed hover) to avoid the
    // column silently stealing focus to whatever row drifted under the cursor.
    var suppressUntil = 0;
    function open(li) {
      suppressUntil = Date.now() + 420;
      items.forEach(function (other) {
        var h = other.querySelector('.sf-note-h');
        var panel = other.querySelector('.sf-note-panel');
        var isThis = other === li;
        if (h) h.setAttribute('aria-expanded', String(isThis));
        if (panel) panel.classList.toggle('is-open', isThis);
        setGroup(other.getAttribute('data-hl'), isThis && !!other.getAttribute('data-hl'));
      });
    }

    items.forEach(function (li) {
      var h = li.querySelector('.sf-note-h');
      if (!h) return;
      var hoverTimer = null;
      h.addEventListener('click', function () { open(li); });
      h.addEventListener('focus', function () { open(li); });
      h.addEventListener('mouseenter', function () {
        hoverTimer = setTimeout(function () {
          if (Date.now() < suppressUntil) return;
          open(li);
        }, 180);
      });
      h.addEventListener('mouseleave', function () {
        if (hoverTimer) { clearTimeout(hoverTimer); hoverTimer = null; }
      });
    });

    // Sync the mock highlight to whichever item is already open in the markup
    // (the first one, by default), so the region is lit from the very start.
    var already = items.filter(function (li) {
      var h = li.querySelector('.sf-note-h');
      return h && h.getAttribute('aria-expanded') === 'true';
    })[0] || items[0];
    open(already);
  }

  /* Reinforces position:sticky with a manual fixed/absolute fallback, because
     body/html carry `overflow-x: hidden` site-wide, which makes some engines
     compute the wrong containing block for native sticky. Desktop only
     (matches the CSS breakpoint where the column goes static on mobile). */
  function initSticky(wrap) {
    var mock = wrap.querySelector('.sf-mock');
    var notes = wrap.querySelector('.sf-notes');
    if (!mock || !notes) return;
    var mq = window.matchMedia('(min-width: 981px)');
    var TOP = 96;
    var mode = 'static'; // 'static' | 'fixed' | 'bottom'
    var naturalLeft = 0, naturalWidth = 0, wrapLeft = 0;

    function clear() { notes.style.position = ''; notes.style.top = ''; notes.style.left = ''; notes.style.width = ''; }
    function measure() {
      var wasSet = mode !== 'static';
      if (wasSet) clear();
      var r = notes.getBoundingClientRect();
      var wr = wrap.getBoundingClientRect();
      naturalWidth = r.width; naturalLeft = r.left; wrapLeft = wr.left;
    }
    function update() {
      if (!mq.matches) { if (mode !== 'static') { clear(); mode = 'static'; } return; }
      var mockBox = mock.getBoundingClientRect();
      if (mode === 'static') measure();
      var notesH = notes.offsetHeight;
      if (mockBox.top > TOP) {
        if (mode !== 'static') { clear(); mode = 'static'; }
        return;
      }
      var room = mockBox.bottom - TOP;
      if (room <= notesH) {
        notes.style.position = 'absolute';
        notes.style.top = (mock.offsetTop + mock.offsetHeight - notesH) + 'px';
        notes.style.left = (naturalLeft - wrapLeft) + 'px';
        notes.style.width = naturalWidth + 'px';
        mode = 'bottom';
      } else {
        notes.style.position = 'fixed';
        notes.style.top = TOP + 'px';
        notes.style.left = naturalLeft + 'px';
        notes.style.width = naturalWidth + 'px';
        mode = 'fixed';
      }
    }
    var ticking = false;
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(function () { update(); ticking = false; }); } }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { mode = 'static'; clear(); update(); });
    update();
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
