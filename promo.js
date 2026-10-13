/* promo.js: site-wide announcement banner + timed program popup (EN + 中文). Not loaded on /decks or /talk.
   - Banner: thin navy strip above the nav that rotates between announcements; links to the event pages.
     Close hides it for the rest of the browser session.
   - Popup: shows after 30s of cumulative time on the site (counted across page loads in this session),
     then again at 5 and 10 minutes if dismissed. Never on the winter-program page itself.
   Testing: ?promo=now opens the popup at once; ?promo=reset clears the session counters. */
(function () {
  if (/^\/(decks|talk)(\/|$)/.test(location.pathname)) return;
  var doc = document.documentElement, zh = (doc.lang || '').indexOf('zh') === 0;
  var END = '2027-01-08', today = new Date(Date.now() + 8 * 3600e3).toISOString().slice(0, 10);
  if (today > END) return;
  window.__arenaPromo = true;
  var cn = zh ? '-cn' : '', WIN = '/events/isb-winter-2027' + cn, ACA = '/events/acamis-tech-2026' + cn;
  var T = zh ? {
    region: '近期公告', close: '关闭', notnow: '暂不需要',
    items: [
      { until: '2026-10-18', b: '10月18日', t: 'Arena 将在 ACAMIS 2026 技术大会（北京鼎石学校）主讲专题分享', go: '了解详情', href: ACA },
      { b: '2027年1月', t: 'ISB 寒假项目：用AI做出一个真实的产品', go: '登记意向', href: WIN }
    ],
    k: 'ISB 寒假项目 · 2027年1月', h: '这个寒假，用AI做出一个真实的产品',
    p: '在 ISB 寒假的最后几天（暂定2027年1月5–8日），学生选择一个真实问题，借助AI做出可用的产品并展示。此前，ISB 学生已在2026年的五天集训营中做出了网站和应用。',
    reg: '登记意向', more: '查看全部项目', moreHref: '/index-cn#programs'
  } : {
    region: 'Announcements', close: 'Close', notnow: 'Not now',
    items: [
      { until: '2026-10-18', b: 'Oct 18', t: 'Arena is speaking at the ACAMIS Technology Conference 2026, Keystone Academy Beijing', go: 'Details', href: ACA },
      { b: 'Jan 2027', t: 'Winter Program at ISB: build a real product with AI', go: 'Register interest', href: WIN }
    ],
    k: 'Winter Program at ISB · January 2027', h: 'Spend the end of winter break building a real product with AI',
    p: 'In the last days of ISB’s winter break (planned for Jan 5–8, 2027), students choose a real problem, build a working product with AI, and demo it. ISB students already built websites and apps in our five-day intensive in 2026.',
    reg: 'Register interest', more: 'See all programs', moreHref: '/#programs'
  };
  var items = T.items.filter(function (i) { return !i.until || today <= i.until });
  var ss = {
    get: function (k) { try { return sessionStorage.getItem('arena.promo.' + k) } catch (e) { return null } },
    set: function (k, v) { try { sessionStorage.setItem('arena.promo.' + k, v) } catch (e) {} }
  };
  if (/[?&]promo=reset\b/.test(location.search)) ['t', 'stage', 'bar'].forEach(function (k) { try { sessionStorage.removeItem('arena.promo.' + k) } catch (e) {} });
  function h(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] }) }

  /* ---------- banner ---------- */
  var bar = null, barH = 0;
  function placeNav() { if (!bar) return; doc.style.setProperty('--nlb-off', Math.max(0, barH - window.scrollY) + 'px') }
  function removeBar() { if (!bar) return; bar.remove(); bar = null; doc.classList.remove('nl-bar-on', 'promo-bar-on'); doc.style.removeProperty('--nlb-off') }
  if (ss.get('bar') !== 'x' && items.length) {
    bar = h('div', 'promo-bar'); bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', T.region);
    bar.innerHTML = '<div class="promo-slides">' + items.map(function (i, n) {
      return '<a class="promo-slide' + (n ? '' : ' on') + '" href="' + esc(i.href) + '"' + (n ? ' tabindex="-1" aria-hidden="true"' : '') + '><b>' + esc(i.b) + '</b><span class="promo-t">' + esc(i.t) + '</span><span class="promo-go">' + esc(i.go) + ' →</span></a>'
    }).join('') + '</div><button type="button" class="promo-x" aria-label="' + esc(T.close) + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7 7 17"/></svg></button>';
    document.body.insertBefore(bar, document.body.firstChild);
    doc.classList.add('nl-bar-on', 'promo-bar-on');
    bar.querySelector('.promo-x').addEventListener('click', function () { ss.set('bar', 'x'); removeBar() });
    var slides = bar.querySelectorAll('.promo-slide'), cur = 0, paused = false;
    bar.addEventListener('mouseenter', function () { paused = true }); bar.addEventListener('mouseleave', function () { paused = false });
    bar.addEventListener('focusin', function () { paused = true }); bar.addEventListener('focusout', function () { paused = false });
    if (slides.length > 1) setInterval(function () {
      if (paused || !bar || document.hidden) return;
      slides[cur].classList.remove('on'); slides[cur].setAttribute('tabindex', '-1'); slides[cur].setAttribute('aria-hidden', 'true');
      cur = (cur + 1) % slides.length;
      slides[cur].classList.add('on'); slides[cur].removeAttribute('tabindex'); slides[cur].removeAttribute('aria-hidden');
    }, 5000);
    var fit = function () { if (bar) { barH = bar.offsetHeight; placeNav() } };
    fit(); window.addEventListener('resize', fit);
    window.addEventListener('scroll', function () { requestAnimationFrame(placeNav) }, { passive: true });
  }

  /* ---------- popup ---------- */
  var STEPS = [30, 300, 600]; // seconds of cumulative time on site
  var onWin = location.pathname.indexOf('/events/isb-winter-2027') === 0;
  var dlg = null, lastFocus = null;
  function build() {
    dlg = h('div', 'promo-pop'); dlg.hidden = true;
    dlg.setAttribute('role', 'dialog'); dlg.setAttribute('aria-modal', 'true'); dlg.setAttribute('aria-labelledby', 'promo-h');
    dlg.innerHTML = '<div class="promo-bg"></div><div class="promo-panel" tabindex="-1">' +
      '<button type="button" class="promo-px" aria-label="' + esc(T.close) + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg></button>' +
      '<span class="promo-k">' + esc(T.k) + '</span><h2 class="promo-h" id="promo-h">' + esc(T.h) + '</h2><p class="promo-p">' + esc(T.p) + '</p>' +
      '<div class="promo-ctas"><a class="btn btn-primary" href="' + esc(WIN) + '#register">' + esc(T.reg) + ' <span class="arr">→</span></a>' +
      '<a class="btn btn-ghost" href="' + esc(T.moreHref) + '">' + esc(T.more) + '</a></div>' +
      '<button type="button" class="promo-notnow">' + esc(T.notnow) + '</button></div>';
    document.body.appendChild(dlg);
    [dlg.querySelector('.promo-bg'), dlg.querySelector('.promo-px'), dlg.querySelector('.promo-notnow')].forEach(function (b) { b.addEventListener('click', dismiss) });
    dlg.querySelectorAll('.promo-ctas a').forEach(function (a) { a.addEventListener('click', function () { ss.set('stage', '9') }) });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); dismiss() }
      if (e.key === 'Tab') { var f = [].slice.call(dlg.querySelectorAll('a[href],button')); var a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus() } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus() } }
    });
  }
  function open() {
    if (!dlg) build(); if (!dlg.hidden) return;
    lastFocus = document.activeElement; dlg.hidden = false; doc.classList.add('promo-lock');
    requestAnimationFrame(function () { requestAnimationFrame(function () { dlg.classList.add('on'); dlg.querySelector('.promo-panel').focus({ preventScroll: true }) }) });
  }
  function dismiss() {
    ss.set('stage', String((+ss.get('stage') || 0) + 1));
    if (!dlg || dlg.hidden) return; dlg.classList.remove('on'); doc.classList.remove('promo-lock');
    setTimeout(function () { dlg.hidden = true }, 260);
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }
  function busy() {
    var nl = document.querySelector('.nl-sheet');
    return doc.classList.contains('nav-open') || doc.classList.contains('php-lock') || doc.classList.contains('nl-lock') || (nl && !nl.hidden) ||
      (document.activeElement && /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName));
  }
  if (/[?&]promo=now\b/.test(location.search)) { setTimeout(open, 400); return }
  if (onWin) return;
  setInterval(function () {
    if (document.hidden) return;
    var t = (+ss.get('t') || 0) + 1; ss.set('t', String(t));
    var st = +ss.get('stage') || 0;
    if (st < STEPS.length && t >= STEPS[st] && (!dlg || dlg.hidden) && !busy()) open();
  }, 1000);
})();
