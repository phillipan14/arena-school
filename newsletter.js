/* newsletter.js: "Arena Notes" sign-ups (posts to /api/subscribe -> Resend). Desktop + phone, EN + 中文.
   - Bands: fills every <section class="nl-band" data-nl="KEY"> placeholder (inserted by tools/newsletter_markup.py).
   - Footer: a slim email field under the desktop footer tagline.
   - Program closing blocks: adds a quiet "Get Arena Notes" button (phones turn it into a row).
   - Sheet: one dialog (a centered modal card at every width) opened by any a[href="#nl"],
     and once on the homepage when the programs section is reached after 15s (rules in maybeAuto()).
   Loaded before phone.js so the phone layer can restyle what this adds. */
(function () {
  var doc = document.documentElement, zh = (doc.lang || '').indexOf('zh') === 0, L = zh ? 'zh' : 'en';
  var T = zh ? {
    name: 'Arena 通讯',
    promise: '我们新开的项目、即将举办的讲座，以及关于孩子与AI的观察。',
    fine: '可随时退订，我们不会分享您的邮箱。',
    iam: '我是', roles: [['parent', '家长'], ['student', '学生'], ['educator', '教育者'], ['other', '其他']],
    email: '您的邮箱', btn: '订阅', sending: '正在订阅…', ok: '订阅成功，欢迎邮件马上就到。', notnow: '暂不需要', close: '关闭', done: '好的',
    sheetH: '新项目和讲座，第一时间知道。', footer: '订阅 Arena 通讯', closing: '订阅 Arena 通讯', bar: '新项目、讲座，以及我们对孩子与AI的观察', barGo: '订阅', barClose: '关闭横幅',
    bad: '请填写有效的邮箱。', pick: '请选择一项。', fail: '暂时无法订阅，请稍后再试。',
    heads: { home: '新项目和讲座，第一时间知道。', about: '关注 Arena 的近况。', approach: '关注 Arena 的近况。', results: '关注下一期学员的进展。', parents: '下一场讲座开放时通知您。', conferences: '获取近期会议与工作坊信息。' }
  } : {
    name: 'Arena Notes',
    promise: 'Programs we’re opening, talks we’re giving, and what we’re learning about kids and AI.',
    fine: 'Unsubscribe anytime. We never share your email.',
    iam: 'I’m a…', roles: [['parent', 'Parent'], ['student', 'Student'], ['educator', 'Educator'], ['other', 'Other']],
    email: 'Your email', btn: 'Subscribe', sending: 'Subscribing…', ok: 'You’re on the list. A short welcome is on its way.', notnow: 'Not now', close: 'Close', done: 'Done',
    sheetH: 'Hear about new programs and talks first.', footer: 'Get Arena Notes', closing: 'Get Arena Notes', bar: 'New programs, talks, and what we’re learning about kids and AI', barGo: 'Subscribe', barClose: 'Close banner',
    bad: 'Please add a valid email.', pick: 'Please choose one.', fail: 'Could not subscribe right now. Please try again.',
    heads: { home: 'Hear about the next ones first.', about: 'Follow along with Arena.', approach: 'Follow along with Arena.', results: 'Follow the next cohorts.', parents: 'Get notified about the next talk.', conferences: 'Hear about upcoming sessions.' }
  };
  var store = {
    get: function (k) { try { return localStorage.getItem('arena.nl.' + k) } catch (e) { return null } },
    set: function (k, v) { try { localStorage.setItem('arena.nl.' + k, v) } catch (e) {} }
  };
  var uid = 0;
  function h(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] }) }

  /* one form, used by bands, the sheet, and (compact) the footer */
  function form(source, compact) {
    var id = 'nl' + (++uid), f = h('form', 'nl-form' + (compact ? ' nl-compact' : ''));
    f.noValidate = true; f.setAttribute('data-source', source);
    var roles = compact ? '' : '<fieldset class="nl-roles"><legend>' + esc(T.iam) + '</legend><div class="nl-chips">' +
      T.roles.map(function (r) { return '<label class="nl-chip"><input type="radio" name="role" value="' + r[0] + '"><span>' + esc(r[1]) + '</span></label>' }).join('') + '</div></fieldset>';
    f.innerHTML = roles +
      '<div class="nl-row"><label class="nl-sr" for="' + id + '">' + esc(T.email) + '</label>' +
      '<input id="' + id + '" class="nl-email" type="email" name="email" inputmode="email" autocomplete="email" placeholder="' + esc(T.email) + '" required>' +
      '<button class="btn btn-primary nl-btn" type="submit">' + esc(T.btn) + '</button></div>' +
      '<input class="nl-hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">' +
      '<p class="nl-msg" role="status" aria-live="polite"></p>' + (compact ? '' : '<p class="nl-fine">' + esc(T.fine) + '</p>');
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var em = f.querySelector('.nl-email'), msg = f.querySelector('.nl-msg'), b = f.querySelector('.nl-btn');
      var v = (em.value || '').trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) { msg.textContent = T.bad; msg.className = 'nl-msg nl-err'; em.focus(); return }
      var r = f.querySelector('input[name=role]:checked');
      var rl = f.querySelector('.nl-roles'); if (rl && rl.offsetParent !== null && !r) { msg.textContent = T.pick; msg.className = 'nl-msg nl-err'; f.querySelector('input[name=role]').focus(); return }
      b.disabled = true; b.textContent = T.sending; msg.textContent = ''; msg.className = 'nl-msg';
      fetch('/api/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: v, role: r ? r.value : '', lang: L, source: source, page: location.pathname, _honey: f.querySelector('.nl-hp').value }) })
        .then(function (res) { return res.json().catch(function () { return {} }).then(function (o) { return { ok: res.ok && o.ok, o: o } }) })
        .then(function (x) {
          if (!x.ok) throw new Error(x.o && x.o.error);
          store.set('sub', '1'); removeBar();
          var okBox = h('div', 'nl-done', '<p class="nl-ok">' + esc(T.ok) + '</p>');
          f.replaceWith(okBox);
          if (okBox.closest('.nl-sheet.nl-is-promo')) { okBox.tabIndex = -1; okBox.focus({ preventScroll: true }) } // promo: closes with the X only
          else if (okBox.closest('.nl-sheet')) { var d = h('button', 'btn btn-primary nl-btn nl-donebtn', esc(T.done)); d.type = 'button'; d.addEventListener('click', closeSheet); okBox.appendChild(d); d.focus() }
        })
        .catch(function (err) { msg.textContent = (err && err.message) || T.fail; msg.className = 'nl-msg nl-err'; b.disabled = false; b.textContent = T.btn });
    });
    return f;
  }

  /* Sign-up shows only when /api/subscribe says Resend is configured (until then nothing appears).
     The closing-block button is added now (hidden by CSS until html.nl-on) so phone.js can turn it into a row. */
  document.querySelectorAll('main.pc section.pp-final .pp-close-cta, body:not(.home) section.pp-final.pc-final .pp-close-cta').forEach(function (cta) {
    if (cta.querySelector('a[href="#nl"]') || document.querySelector('section.nl-band')) return;
    var a = h('a', 'btn btn-ghost nl-cta', esc(T.closing)); a.href = '#nl'; cta.appendChild(a);
  });
  var preview = /[?&]nl=(now|reset)\b/.test(location.search);
  fetch('/api/subscribe', { cache: 'no-store' }).then(function (r) { return r.json() }).then(function (o) { if (o && o.configured) start(true); else if (window.__arenaPromo) start(false) }).catch(function () {});

  /* homepage top banner: thin navy strip above the nav; the whole strip opens the sheet.
     If the text doesn't fit, it scrolls as a ticker (still under reduced motion). */
  var bar = null, barH = 0;
  function removeBar() { if (!bar) return; bar.remove(); bar = null; doc.classList.remove('nl-bar-on'); doc.style.removeProperty('--nlb-off') }
  function placeNav() { if (!bar) return; var off = Math.max(0, barH - window.scrollY); doc.style.setProperty('--nlb-off', off + 'px') }
  function buildBar() {
    if (!doc.querySelector('body.home') || store.get('sub') === '1' || document.querySelector('.promo-bar')) return; // promo.js owns the top strip while it runs
    var bd = +store.get('bar') || 0; if (bd && Date.now() - bd < 30 * 864e5) return;
    bar = h('div', 'nl-bar'); bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', T.name);
    var item = '<span class="nl-bar-item"><b>' + esc(T.name) + '</b><span class="nl-bar-dot" aria-hidden="true">·</span>' + esc(T.bar) + '<span class="nl-bar-go">' + esc(T.barGo) + ' →</span></span>';
    bar.innerHTML = '<a class="nl-bar-link" href="#nl"><span class="nl-bar-track">' + item + '</span></a>' +
      '<button type="button" class="nl-bar-x" aria-label="' + esc(T.barClose) + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7 7 17"/></svg></button>';
    document.body.insertBefore(bar, document.body.firstChild);
    doc.classList.add('nl-bar-on');
    bar.querySelector('.nl-bar-x').addEventListener('click', function () { store.set('bar', String(Date.now())); removeBar() });
    function fit() {
      if (!bar) return; var link = bar.querySelector('.nl-bar-link'), tr = bar.querySelector('.nl-bar-track');
      tr.classList.remove('nl-run'); tr.innerHTML = item;
      if (tr.scrollWidth > link.clientWidth - 8) {
        tr.innerHTML = item + '<span class="nl-bar-gap" aria-hidden="true"></span>' + item.replace('class="nl-bar-item"', 'class="nl-bar-item" aria-hidden="true"') + '<span class="nl-bar-gap" aria-hidden="true"></span>';
        var w = tr.scrollWidth / 2; tr.style.setProperty('--nlb-dur', Math.max(12, w / 45) + 's'); tr.classList.add('nl-run');
      }
      barH = bar.offsetHeight; placeNav();
    }
    fit(); window.addEventListener('resize', fit); if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
    window.addEventListener('scroll', function () { requestAnimationFrame(placeNav) }, { passive: true });
  }

  /* cfg=false: sign-up is not configured but a program is being promoted, so only the popup runs (without the email field). */
  function start(cfg) {
  var P = window.__arenaPromo || null;
  if (cfg) {
  doc.classList.add('nl-on');
  buildBar();
  /* bands */
  document.querySelectorAll('section.nl-band[data-nl]').forEach(function (s) {
    var key = s.getAttribute('data-nl');
    s.setAttribute('aria-label', T.name);
    var c = h('div', 'container'), card = h('div', 'nl-card');
    var copy = h('div', 'nl-copy', '<span class="nl-k">' + esc(T.name) + '</span><h2 class="nl-h">' + esc(T.heads[key] || T.heads.about) + '</h2><p class="nl-p">' + esc(T.promise) + '</p>');
    card.appendChild(copy); card.appendChild(form('band-' + key)); c.appendChild(card); s.appendChild(c);
  });

  /* desktop footer field */
  var fb = document.querySelector('footer.footer .footer-brand');
  if (fb && !fb.querySelector('.nl-foot')) { var ff = h('div', 'nl-foot', '<span class="nl-foot-k">' + esc(T.footer) + '</span>'); ff.appendChild(form('footer', true)); fb.appendChild(ff) }

  }

  /* the sheet */
  var sheet = null, lastFocus = null;
  function build() {
    sheet = h('div', 'nl-sheet'); sheet.hidden = true;
    sheet.setAttribute('role', 'dialog'); sheet.setAttribute('aria-modal', 'true'); sheet.setAttribute('aria-labelledby', 'nl-sheet-h');
    sheet.innerHTML = '<div class="nl-sheet-bg"></div><div class="nl-sheet-panel" tabindex="-1"><div class="nl-sheet-top">' +
      '<button type="button" class="nl-x" aria-label="' + esc(T.close) + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button></div>' +
      '<div class="nl-std"><span class="nl-k">' + esc(T.name) + '</span><h2 class="nl-h" id="nl-sheet-h">' + esc(T.sheetH) + '</h2><p class="nl-p">' + esc(T.promise) + '</p></div></div>';
    var pn = sheet.querySelector('.nl-sheet-panel');
    if (P) {
      /* program promo (promo.js): seal, label, heading, date line, copy, one primary link, then a compact Arena Notes field */
      var pb = h('div', 'nl-promo', '<img class="nl-seal" src="/logos/arena/seal-navy-256.png" alt="" width="48" height="48">' +
        '<span class="nl-k">' + esc(P.k) + '</span><h2 class="nl-h" id="nl-promo-h">' + esc(P.h) + '</h2>' +
        (P.d ? '<p class="nl-promo-d"><span>' + esc(P.d) + '</span></p>' : '') + '<p class="nl-p">' + esc(P.p) + '</p>' +
        (P.note ? '<p class="nl-promo-note">' + esc(P.note) + '</p>' : '') +
        '<div class="nl-promo-cta"><a class="btn btn-primary nl-btn" href="' + esc(P.regHref) + '">' + esc(P.reg) + ' <span class="arr">→</span></a></div>' +
        (cfg ? '<p class="nl-promo-or">' + esc(P.or) + '</p>' : ''));
      pn.insertBefore(pb, pn.querySelector('.nl-std'));
      pb.querySelectorAll('.nl-promo-cta a').forEach(function (a) { a.addEventListener('click', function () { P.done() }) });
    }
    if (cfg) pn.appendChild(form('sheet'));
    var nn = h('button', 'nl-notnow', esc(T.notnow)); nn.type = 'button'; pn.appendChild(nn);
    document.body.appendChild(sheet);
    sheet.querySelector('.nl-sheet-bg').addEventListener('click', dismiss);
    sheet.querySelector('.nl-x').addEventListener('click', dismiss);
    nn.addEventListener('click', dismiss);
    sheet.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); dismiss() }
      if (e.key === 'Tab') { var f = [].filter.call(pn.querySelectorAll('button,input,a[href]'), function (x) { return !x.disabled && x.offsetParent !== null && x.tabIndex !== -1 }); if (!f.length) return;
        var a = f[0], z = f[f.length - 1]; if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus() } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus() } }
    });
  }
  function busy() { return doc.classList.contains('nav-open') || doc.classList.contains('php-lock') || (document.activeElement && /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) }
  var mode = 'nl';
  function openSheet(m) {
    if (!sheet) build(); if (!sheet.hidden) return;
    mode = (m === 'promo' && P) ? 'promo' : 'nl';
    sheet.classList.toggle('nl-is-promo', mode === 'promo');
    sheet.setAttribute('aria-labelledby', mode === 'promo' ? 'nl-promo-h' : 'nl-sheet-h');
    if (!cfg && mode === 'nl') return;
    lastFocus = document.activeElement; sheet.hidden = false; doc.classList.add('nl-lock');
    requestAnimationFrame(function () { requestAnimationFrame(function () { sheet.classList.add('on'); sheet.querySelector('.nl-sheet-panel').focus({ preventScroll: true }) }) });
  }
  function closeSheet() {
    if (!sheet || sheet.hidden) return; sheet.classList.remove('on'); doc.classList.remove('nl-lock');
    setTimeout(function () { sheet.hidden = true }, 260);
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }
  var forced = /[?&]nl=now\b/.test(location.search);
  function dismiss() { if (mode === 'promo') P.dismissed(); else if (!forced && store.get('sub') !== '1') store.set('dismissed', String(Date.now())); closeSheet() }
  document.addEventListener('click', function (e) { var a = e.target.closest && e.target.closest('a[href="#nl"]'); if (!a) return; e.preventDefault(); openSheet('nl') });

  /* homepage: once, when the programs section is reached after 15s; never after subscribing; 60 days after "Not now" */
  function maybeAuto() {
    if (/[?&]nl=reset\b/.test(location.search)) { try { localStorage.removeItem('arena.nl.sub'); localStorage.removeItem('arena.nl.dismissed') } catch (e) {} }
    if (forced) { setTimeout(openSheet, 400); return }
    if (P) { P.schedule(function () { if (busy() || (sheet && !sheet.hidden)) return false; openSheet('promo'); return true }); return } // 30s, 5 min, 10 min (promo.js)
    if (!cfg) return;
    if (!doc.querySelector('body.home') || /[?&]nl=0\b/.test(location.search)) return;
    if (store.get('sub') === '1') return;
    var d = +store.get('dismissed') || 0; if (d && Date.now() - d < 60 * 864e5) return;
    var shown = false;
    function tryShow() { if (shown) return; if (busy()) { setTimeout(tryShow, 2000); return } shown = true; openSheet() }
    setTimeout(tryShow, 3000);   // three seconds into the visit
  }
  maybeAuto();
  }
})();
