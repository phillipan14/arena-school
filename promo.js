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
    region: '近期公告', close: '关闭', bb: '2027年1月5–8日', bt: 'ISB 寒假项目：用AI做出一个真实的产品', bgo: '登记意向',
    k: 'ISB 寒假项目 · 2027年1月5–8日', h: '这个寒假，用AI做出一个真实的产品',
    p: '在 ISB 寒假的最后几天，学生选择一个真实问题，借助AI做出可用的产品并展示。',
    reg: '登记意向', more: '查看全部项目', moreHref: '/index-cn#programs', or: '或订阅 Arena 通讯，第一时间了解新项目和讲座：'
  } : {
    region: 'Announcement', close: 'Close', bb: 'Jan 5–8, 2027', bt: 'Winter Program at ISB: build a real product with AI', bgo: 'Register interest',
    k: 'Winter Program at ISB · Jan 5–8, 2027', h: 'Spend the end of winter break building a real product with AI',
    p: 'In the last days of ISB’s winter break, students choose a real problem, build a working product with AI, and demo it.',
    reg: 'Register interest', more: 'See all programs', moreHref: '/#programs', or: 'Or get Arena Notes: new programs and talks, first.'
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
    bar.innerHTML = '<a class="promo-link" href="' + esc(WIN) + '"><b>' + esc(T.bb) + '</b><span class="promo-t">' + esc(T.bt) + '</span><span class="promo-go">' + esc(T.bgo) + ' →</span></a>' +
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
    k: T.k, h: T.h, p: T.p, reg: T.reg, regHref: WIN + '#register', more: T.more, moreHref: T.moreHref, or: T.or,
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
