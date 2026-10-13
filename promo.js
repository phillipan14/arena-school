/* promo.js: ISB winter program promotion (EN + 中文). Not loaded on /decks or /talk; off after Jan 8, 2027.
   - Banner: a static navy strip above the nav linking to the program page; close hides it for the session.
   - Popup: newsletter.js shows the program in its Arena Notes sheet (same design, plus the email sign-up)
     after 30s of cumulative time on the site in this session, then at 5 and 10 minutes if dismissed.
     Never on the program page itself. This file supplies the copy and the schedule via window.__arenaPromo.
   Testing: ?promo=now opens the popup at once; ?promo=reset clears the session counters. */
(function () {
  if (/^\/(decks|talk)(\/|$)/.test(location.pathname)) return;
  var doc = document.documentElement, zh = (doc.lang || '').indexOf('zh') === 0;
  var END = '2027-01-08', today = new Date(Date.now() + 8 * 3600e3).toISOString().slice(0, 10);
  if (today > END) return;
  var WIN = '/events/isb-winter-2027' + (zh ? '-cn' : '');
  var onWin = location.pathname.indexOf('/events/isb-winter-2027') === 0;
  var T = zh ? {
    region: '近期公告', close: '关闭', bt: 'ISB 冬季项目 · 2027年1月5–8日', bm: 'ISB 冬季项目 · 1月5–8日', bgo: '登记意向',
    k: 'ISB 冬季项目', h: '这个冬天，\n让孩子做出真正能用的产品', d: '2027年1月5日至8日',
    p: '在北京顺义国际学校（ISB），\n学生选定一个真实问题，\n借助AI做出可用的产品，并现场展示。',
    note: '2026年，已有 ISB 学生在 Arena 北京五天集训中\n做出了自己的网站和应用。',
    reg: '登记意向', or: '还在考虑？先订阅 Arena 通讯。'
  } : {
    region: 'Announcement', close: 'Close', bt: 'Winter Program @ ISB · Jan 5–8, 2027', bm: 'Winter Program @ ISB · Jan 5–8', bgo: 'Register',
    k: 'Winter Program @ ISB', h: 'This winter, your child builds something real.', d: 'January 5–8, 2027',
    p: 'At the International School of Beijing, students choose a real problem, build a working product with AI, and demo it.',
    note: 'In 2026, ISB students built websites and apps in Arena’s five-day intensive in Beijing.',
    reg: 'Register interest', or: 'Not ready yet? Get Arena Notes by email.'
  };
  var ss = {
    get: function (k) { try { return sessionStorage.getItem('arena.promo.' + k) } catch (e) { return null } },
    set: function (k, v) { try { sessionStorage.setItem('arena.promo.' + k, v) } catch (e) {} }
  };
  if (/[?&]promo=reset\b/.test(location.search)) ['t', 'stage', 'bar'].forEach(function (k) { try { sessionStorage.removeItem('arena.promo.' + k) } catch (e) {} });
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c] }) }

  /* ---------- banner (static, one message) ---------- */
  var bar = null, barH = 0;
  function placeNav() { if (bar) doc.style.setProperty('--nlb-off', Math.max(0, barH - window.scrollY) + 'px') }
  if (ss.get('bar') !== 'x') {
    bar = document.createElement('div'); bar.className = 'promo-bar'; bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', T.region);
    bar.innerHTML = '<a class="promo-link" href="' + esc(WIN) + '"><span class="promo-t"><span class="promo-td">' + esc(T.bt) + '</span><span class="promo-tm">' + esc(T.bm) + '</span></span><span class="promo-go">' + esc(T.bgo) + '<span class="promo-arr" aria-hidden="true">→</span></span></a>' +
      '<button type="button" class="promo-x" aria-label="' + esc(T.close) + '"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7l10 10M17 7 7 17"/></svg></button>';
    document.body.insertBefore(bar, document.body.firstChild);
    doc.classList.add('nl-bar-on', 'promo-bar-on');
    bar.querySelector('.promo-x').addEventListener('click', function () {
      ss.set('bar', 'x'); bar.remove(); bar = null; doc.classList.remove('nl-bar-on', 'promo-bar-on'); doc.style.removeProperty('--nlb-off')
    });
    var fit = function () { if (bar) { barH = bar.offsetHeight; placeNav() } };
    fit(); window.addEventListener('resize', fit);
    window.addEventListener('scroll', function () { requestAnimationFrame(placeNav) }, { passive: true });
  }

  /* ---------- popup copy + schedule, shown by newsletter.js ---------- */
  if (onWin) return;
  var STEPS = [30, 300, 600]; // seconds of cumulative time on site this session
  window.__arenaPromo = {
    k: T.k, h: T.h, d: T.d, p: T.p, note: T.note, reg: T.reg, regHref: WIN + '#register', or: T.or,
    dismissed: function () { ss.set('stage', String((+ss.get('stage') || 0) + 1)) },
    done: function () { ss.set('stage', '9') },
    schedule: function (show) {
      if (/[?&]promo=now\b/.test(location.search)) { setTimeout(show, 400); return }
      setInterval(function () {
        if (document.hidden) return;
        var t = (+ss.get('t') || 0) + 1; ss.set('t', String(t));
        var st = +ss.get('stage') || 0;
        if (st < STEPS.length && t >= STEPS[st]) show();
      }, 1000);
    }
  };
})();
