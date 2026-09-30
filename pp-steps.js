/* Program pages · "How it runs" step selector.
   A large stage crossfades between each step's photo or clip. Steps change on click, tap, hover
   (mouse), arrow keys, a swipe on the stage or the step row (phones), or auto-advance while the
   section is on screen. Auto-advance pauses on hover and keyboard focus, has a pause button, and is
   off under reduced motion. Without JS the markup is a plain list with the first photo shown. */
(function () {
  var roots = [].slice.call(document.querySelectorAll('[data-pc-sel]'));
  if (!roots.length) return;
  var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var DUR = 6500;

  function pad(i) { return (i < 10 ? '0' : '') + i; }

  function init(root) {
    var tabs = [].slice.call(root.querySelectorAll('.pc-sel-tab'));
    var slides = [].slice.call(root.querySelectorAll('.pc-sel-slide'));
    var list = root.querySelector('.pc-sel-list');
    var stage = root.querySelector('.pc-sel-stage');
    var count = root.querySelector('.pc-sel-count b');
    var pp = root.querySelector('.pc-sel-pp');
    var n = tabs.length;
    if (!n || n !== slides.length) return;
    var cur = 0, inView = false, hover = false, kbd = false, stopped = mq.matches, userStopped = false;
    var hoverTimer = 0, scrollTimer = 0, programmatic = false;

    root.classList.add('is-js');
    root.style.setProperty('--pc-dur', DUR + 'ms');
    if (pp && !mq.matches) pp.hidden = false;

    function isRow() { return getComputedStyle(list).flexDirection === 'row'; }
    function running() { return !stopped && inView && !document.hidden; }

    function media() {
      slides.forEach(function (s, k) {
        var v = s.querySelector('video');
        if (!v) return;
        if (k === cur && running()) {
          v.preload = 'auto';
          var p = v.play(); if (p && p.catch) p.catch(function () {});
        } else if (!v.paused) v.pause();
      });
    }

    function update() {
      root.classList.toggle('is-auto', running());
      root.classList.toggle('is-paused', hover || kbd);
      media();
    }

    function restart() {
      root.classList.remove('is-auto');
      void root.offsetWidth; // reflow so the active progress bar starts from zero
      update();
    }

    function scrollRow(i) {
      if (!isRow()) return;
      var li = tabs[i].parentNode;
      var padL = parseFloat(getComputedStyle(list).scrollPaddingLeft) || 0;
      programmatic = true;
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(function () { programmatic = false; }, 700);
      list.scrollTo({ left: li.offsetLeft - padL, behavior: mq.matches ? 'auto' : 'smooth' });
    }

    function set(i, scroll) {
      i = (i + n) % n;
      tabs.forEach(function (t, k) {
        var on = k === i;
        t.classList.toggle('is-on', on);
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.tabIndex = on ? 0 : -1;
      });
      slides.forEach(function (s, k) {
        var on = k === i;
        s.classList.toggle('is-on', on);
        if (on) s.removeAttribute('aria-hidden'); else s.setAttribute('aria-hidden', 'true');
      });
      if (count) count.textContent = pad(i + 1);
      cur = i;
      if (scroll) scrollRow(i);
      restart();
    }

    // Warm the next photo so the crossfade never shows an empty frame.
    function warm() {
      slides.forEach(function (s) { var im = s.querySelector('img'); if (im) im.loading = 'eager'; });
    }

    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { set(k, true); });
      t.addEventListener('pointerenter', function (e) {
        if (e.pointerType !== 'mouse' || isRow()) return;
        clearTimeout(hoverTimer);
        hoverTimer = setTimeout(function () { if (k !== cur) set(k, false); }, 90);
      });
      t.addEventListener('pointerleave', function () { clearTimeout(hoverTimer); });
    });

    list.addEventListener('keydown', function (e) {
      var k = e.key, to = -1;
      if (k === 'ArrowRight' || k === 'ArrowDown') to = cur + 1;
      else if (k === 'ArrowLeft' || k === 'ArrowUp') to = cur - 1;
      else if (k === 'Home') to = 0;
      else if (k === 'End') to = n - 1;
      if (to < 0 && k !== 'ArrowLeft' && k !== 'ArrowUp') return;
      e.preventDefault();
      set(to, true);
      tabs[cur].focus({ preventScroll: true });
    });

    root.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') { hover = true; update(); } });
    root.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') { hover = false; update(); } });
    root.addEventListener('focusin', function (e) {
      var fv = false; try { fv = e.target.matches(':focus-visible'); } catch (x) {}
      kbd = fv; update();
    });
    root.addEventListener('focusout', function () {
      setTimeout(function () { if (!root.contains(document.activeElement)) { kbd = false; update(); } }, 0);
    });

    // Auto-advance: the active bar's CSS animation is the timer, so hover-pause stops both at once.
    root.addEventListener('animationend', function (e) {
      if (!/^pcSel/.test(e.animationName)) return;
      if (e.target.closest('.pc-sel-tab') !== tabs[cur]) return;
      set(cur + 1, true);
    });

    if (pp) pp.addEventListener('click', function () {
      userStopped = !userStopped;
      stopped = userStopped || mq.matches;
      pp.classList.toggle('is-stopped', userStopped);
      pp.setAttribute('aria-label', userStopped ? root.getAttribute('data-label-play') : root.getAttribute('data-label-pause'));
      restart();
    });

    // Phones: the step row is swipeable; whichever card settles first becomes the active step.
    list.addEventListener('scroll', function () {
      if (!isRow()) return;
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(function () {
        if (programmatic) { programmatic = false; return; }
        var padL = parseFloat(getComputedStyle(list).scrollPaddingLeft) || 0;
        var best = cur, bestD = Infinity;
        tabs.forEach(function (t, k) {
          var d = Math.abs(t.parentNode.offsetLeft - padL - list.scrollLeft);
          if (d < bestD) { bestD = d; best = k; }
        });
        if (best !== cur) set(best, false);
      }, 140);
    }, { passive: true });

    // Swipe on the photo itself.
    var sx = 0, sy = 0, tracking = false;
    stage.addEventListener('touchstart', function (e) {
      if (e.touches.length !== 1) return;
      tracking = true; sx = e.touches[0].clientX; sy = e.touches[0].clientY;
    }, { passive: true });
    stage.addEventListener('touchend', function (e) {
      if (!tracking) return; tracking = false;
      var t = e.changedTouches[0], dx = t.clientX - sx, dy = t.clientY - sy;
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.3) set(cur + (dx < 0 ? 1 : -1), true);
    }, { passive: true });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          var was = inView;
          inView = en.isIntersecting;
          if (inView && !was) { warm(); restart(); } else update();
        });
      }, { threshold: 0.35 }).observe(root);
    }
    document.addEventListener('visibilitychange', update);
    if (mq.addEventListener) mq.addEventListener('change', function () {
      stopped = userStopped || mq.matches;
      if (pp) pp.hidden = mq.matches;
      restart();
    });
  }

  roots.forEach(init);
})();
