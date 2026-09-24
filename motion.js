/* ============================================================
   Arena — motion.js
   Reveal-on-scroll · number count-ups · cohort-path draw ·
   nav scroll state · mobile menu.
   Rect-based reveal (robust across all environments) with
   IntersectionObserver as a progressive enhancement.
   All guarded by prefers-reduced-motion.
   ============================================================ */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Status ticker (dismiss + retract on scroll) ---------- */
  var tickerX = document.getElementById('tickerX');
  var tickerDismissed = false;
  function syncTicker() {
    document.body.classList.toggle('ticker-up', tickerDismissed || window.scrollY > 24);
  }
  if (tickerX) tickerX.addEventListener('click', function () { tickerDismissed = true; syncTicker(); });

  /* ---------- Ticker carousel (rotates announcements every 4.5s) ---------- */
  var carousel = document.querySelector('.ticker-carousel');
  if (carousel && !reduce) {
    var slides = carousel.querySelectorAll('.ticker-slide');
    if (slides.length > 1) {
      var idx = 0;
      var cycle = setInterval(function () {
        slides[idx].classList.remove('is-active');
        idx = (idx + 1) % slides.length;
        slides[idx].classList.add('is-active');
      }, 4500);
      // Pause cycling on hover (so users can read or click)
      carousel.addEventListener('mouseenter', function () { clearInterval(cycle); });
    }
  }

  /* ---------- Nav: scrolled state + mobile toggle ---------- */
  var nav = document.getElementById('nav');
  function onNavScroll() {
    if (window.scrollY > 24) nav.classList.add('scrolled');
    else nav.classList.remove('scrolled');
    syncTicker();
  }
  window.addEventListener('scroll', onNavScroll, { passive: true });
  onNavScroll();

  var toggle = document.getElementById('navToggle');
  var navLinks = document.getElementById('navLinks');
  if (toggle) {
    toggle.addEventListener('click', function () { navLinks.classList.toggle('open'); });
    navLinks.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') navLinks.classList.remove('open');
    });
  }

  /* ---------- Nav dropdowns: hover on desktop, click/tap everywhere ---------- */
  var dds = [].slice.call(document.querySelectorAll('.nav-dd'));
  function closeDDs(except) {
    dds.forEach(function (d) {
      if (d === except) return;
      d.classList.remove('open');
      var b = d.querySelector('.nav-dd-btn'); if (b) b.setAttribute('aria-expanded', 'false');
    });
  }
  dds.forEach(function (d) {
    var b = d.querySelector('.nav-dd-btn');
    if (!b) return;
    b.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = !d.classList.contains('open');
      closeDDs(d);
      d.classList.toggle('open', open);
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('click', function () { closeDDs(null); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeDDs(null); });

  /* ---------- Count-up ---------- */
  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
  function runCount(el) {
    var to = parseFloat(el.getAttribute('data-to'));
    var decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
    if (reduce) { el.textContent = to.toFixed(decimals); return; }
    var dur = 1200, start = null;
    function frame(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = (to * easeOutCubic(p)).toFixed(decimals);
      if (p < 1) requestAnimationFrame(frame);
      else el.textContent = to.toFixed(decimals);
    }
    requestAnimationFrame(frame);
  }

  /* ---------- Reveal ---------- */
  var revealEls = [].slice.call(document.querySelectorAll('.reveal'));
  var drawEls = [document.getElementById('cohortPath'), document.getElementById('hubLine')].filter(Boolean);
  function drawAll() { drawEls.forEach(function (e) { e.classList.add('drawn'); }); }

  function revealNow(el) {
    if (el.classList.contains('in')) return;
    el.classList.add('in');
    var counts = el.querySelectorAll('.countup');
    for (var i = 0; i < counts.length; i++) {
      if (!counts[i].dataset.done) { counts[i].dataset.done = '1'; runCount(counts[i]); }
    }
  }

  function inView(el, margin) {
    var r = el.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight;
    return r.top < vh - (margin || 0) && r.bottom > 0;
  }

  if (reduce) {
    revealEls.forEach(function (el) { el.classList.add('in'); revealNow(el); });
    drawAll();
    wireForm('cohortForm',  'cfStatus', 'Cohort Zero interest');
    wireForm('partnerForm', 'pfStatus', 'Arena School partnership inquiry');
    return;
  }

  // Rect-based pass: reveal everything currently in view, with a small
  // stagger among newly-revealed siblings. Runs on load + scroll + resize.
  function sweep() {
    var newlyByParent = new Map();
    revealEls.forEach(function (el) {
      if (el.classList.contains('in')) return;
      if (inView(el, 60)) {
        var arr = newlyByParent.get(el.parentNode) || [];
        arr.push(el);
        newlyByParent.set(el.parentNode, arr);
      }
    });
    newlyByParent.forEach(function (arr) {
      arr.forEach(function (el, i) {
        setTimeout(function () { revealNow(el); }, Math.min(i, 6) * 80);
      });
    });
    if (drawEls.length) {
      drawEls.forEach(function (d) {
        if (!d.classList.contains('drawn') && inView(d, 120)) d.classList.add('drawn');
      });
    }
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { sweep(); ticking = false; });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);

  // IntersectionObserver — primary reveal trigger in real browsers
  // (fires on scroll AND on hash/anchor jumps). The rect-sweep above is
  // a fallback for environments where IO or programmatic scroll is inert.
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        if (drawEls.indexOf(el) > -1) { el.classList.add('drawn'); io.unobserve(el); return; }
        var sibs = [].slice.call(el.parentNode.querySelectorAll(':scope > .reveal'));
        var idx = sibs.indexOf(el);
        setTimeout(function () { revealNow(el); }, idx > 0 ? Math.min(idx, 6) * 80 : 0);
        io.unobserve(el);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    revealEls.forEach(function (el) { io.observe(el); });
    drawEls.forEach(function (d) { io.observe(d); });
  }

  // Initial passes (cover late layout / font load / inert-IO sandboxes).
  sweep();
  requestAnimationFrame(sweep);
  setTimeout(sweep, 120);
  window.addEventListener('load', sweep);

  /* ---------- Footer countdown — days until Cohort Zero closes ---------- */
  var COHORT_CLOSE = new Date('2026-08-15T23:59:59-07:00');
  var cd = document.getElementById('footerCountdown');
  function renderCountdown() {
    if (!cd) return;
    var msPerDay = 86400000;
    var diff = COHORT_CLOSE.getTime() - Date.now();
    var num = cd.querySelector('.fc-num');
    var cap = cd.querySelector('.fc-cap');
    if (!num || !cap) return;
    if (diff <= 0) {
      num.textContent = 'Closed';
      cap.textContent = 'Cohort Zero applications have closed. Stay tuned for Cohort One.';
      return;
    }
    var days = Math.ceil(diff / msPerDay);
    num.textContent = days;
    cap.textContent = days === 1
      ? 'day until Cohort Zero applications close'
      : 'days until Cohort Zero applications close';
  }
  renderCountdown();
  setInterval(renderCountdown, 60 * 60 * 1000); // hourly is plenty

  /* ---------- Interest forms — FormSubmit AJAX primary, mailto fallback if the network's gone ---------- */
  function wireForm(formId, statusId, subjectPrefix) {
    var form = document.getElementById(formId);
    var statusEl = document.getElementById(statusId);
    if (!form) return;

    function setStatus(msg, kind) {
      if (!statusEl) return;
      statusEl.textContent = msg;
      statusEl.className = 'cf-status' + (kind ? ' cf-status-' + kind : '');
    }

    function setLoading(loading) {
      form.classList.toggle('is-loading', loading);
      var btn = form.querySelector('.cf-submit');
      if (btn) btn.disabled = !!loading;
    }

    function collect() {
      var data = {};
      var inputs = form.querySelectorAll('input[name], select[name], textarea[name]');
      inputs.forEach(function (el) {
        data[el.name] = (el.value || '').trim();
      });
      return data;
    }

    function mailtoFallback(data, to) {
      var who = data.name || data.school || 'someone';
      var subject = subjectPrefix + ' — ' + who;
      // Strip FormSubmit's internal fields from the mailto body
      var lines = Object.keys(data)
        .filter(function (k) { return k.charAt(0) !== '_'; })
        .map(function (k) { return k + ': ' + data[k]; })
        .join('\n');
      window.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines);
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = collect();
      var action = form.getAttribute('action') || '';
      var fallback = form.getAttribute('data-fallback-email') || '';

      // Spam honeypot — if the hidden _honey field has anything, silently "succeed"
      if (data._honey) {
        form.reset();
        setStatus("Thank you. We'll be in touch.", 'ok');
        return;
      }

      // No real endpoint? Open the user's mail client as a fallback.
      if (!action || action.indexOf('REPLACE_WITH') !== -1) {
        mailtoFallback(data, fallback);
        setStatus('Opening your email client to finish sending…', 'ok');
        return;
      }

      setLoading(true);
      setStatus('Sending…');

      fetch(action, {
        method: 'POST',
        headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (res) {
        return res.json().then(function (j) { return { ok: res.ok, body: j }; })
          .catch(function () { return { ok: res.ok, body: null }; });
      }).then(function (r) {
        setLoading(false);
        // FormSubmit returns { success: "true" | "false", message: "..." }
        // Formspree returns { ok: true } or { errors: [...] }
        var body = r.body || {};
        var successful = r.ok && (body.success === 'true' || body.success === true || body.ok === true || !body.errors);
        if (successful) {
          form.reset();
          setStatus(body.message || "Thank you. We'll be in touch.", 'ok');
        } else {
          var err = body.message
            || (body.errors && body.errors[0] && body.errors[0].message)
            || 'Something went wrong. Please try again.';
          setStatus(err, 'err');
        }
      }).catch(function () {
        setLoading(false);
        setStatus("Couldn't reach the server. Opening email as a fallback…", 'err');
        setTimeout(function () { mailtoFallback(data, fallback); }, 600);
      });
    });
  }

  wireForm('cohortForm',  'cfStatus', 'Cohort Zero interest');
  wireForm('partnerForm', 'pfStatus', 'Arena School partnership inquiry');
})();
