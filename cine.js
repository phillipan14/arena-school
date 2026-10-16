/* cine.js: cinematic hero previews (css/cine.css) on the homepage and /schools/technology.
   ?hero=cine1|cine2|cine3 picks one; with no parameter this file does nothing and the page keeps its
   default hero. Real repo photos only: the first photo loads eagerly, the rest after it has loaded.
   cine3 reuses the live homepage's particle field (riso-particles.js) on cool paper. Loaded with defer,
   after riso-particles.js where a page has it. */
(function () {
  'use strict';
  var m = /[?&]hero=(cine[123])\b/i.exec(location.search);
  if (!m) return;
  var v = m[1].toLowerCase();
  var root = document.documentElement;
  var zh = (root.lang || '').indexOf('zh') === 0;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hero = document.querySelector('main section.hero-full, main section.el-hero');
  if (!hero) return;
  root.setAttribute('data-hero', v);
  var isTech = /\/schools\/technology/.test(location.pathname);

  // [src 800, src large, focus, EN caption, CN caption]
  var HOME = [
    ['/photos/isb-hq/isb-cohort-800.webp', '/photos/isb-hq/isb-cohort-1400.webp', '50% 42%', 'The Beijing cohort, 2026', '北京学员，2026年'],
    ['/photos/isb-2026/demo-laptop-800.webp', '/photos/isb-2026/demo-laptop-1600.webp', '50% 35%', 'Demo day, Beijing 2026', '路演日，北京，2026年'],
    ['/photos/isb-hq/isb-team-stage-800.webp', '/photos/isb-hq/isb-team-stage-1400.webp', '50% 40%', 'Presenting on stage, Beijing 2026', '台上展示，北京，2026年'],
    ['/photos/isb-2026/mentor-feedback-800.webp', '/photos/isb-2026/mentor-feedback-1600.webp', '50% 40%', 'Mentor feedback, Beijing 2026', '导师反馈，北京，2026年']
  ];
  var TECH = [
    ['/photos/isb-2026/mentors-laptop-800.webp', '/photos/isb-2026/mentors-laptop-1600.webp', '50% 30%', 'Working through a task together, Beijing 2026', '一起研究一项任务，北京，2026年'],
    ['/photos/isb-2026/mentor-feedback-800.webp', '/photos/isb-2026/mentor-feedback-1600.webp', '50% 40%', 'Mentor feedback, Beijing 2026', '导师反馈，北京，2026年'],
    ['/photos/isb-2026/pitch-team-800.webp', '/photos/isb-2026/pitch-team-1600.webp', '50% 35%', 'Final pitch, Beijing 2026', '最终路演，北京，2026年']
  ];
  var SPLIT = isTech ? TECH[0] : ['/photos/isb-2026/pitch-team-800.webp', '/photos/isb-2026/pitch-team-1600.webp', '50% 35%', 'Final pitch, Beijing 2026', '最终路演，北京，2026年'];

  function el(tag, cls) { var e = document.createElement(tag); if (cls) e.className = cls; e.setAttribute('aria-hidden', 'true'); return e; }
  function caption(p) { var c = document.createElement('p'); c.className = 'cine-caption'; c.textContent = zh ? p[4] : p[3]; return c; }
  function slide(p, eager) {
    var s = el('div', 'cine-slide'), img = document.createElement('img');
    img.alt = ''; img.decoding = 'async'; img.style.setProperty('--focus', p[2]);
    img.sizes = '100vw';
    if (eager) { img.src = p[0]; img.srcset = p[0] + ' 800w, ' + p[1] + ' 1400w'; img.setAttribute('fetchpriority', 'high'); }
    else { img.setAttribute('data-src', p[0]); img.setAttribute('data-srcset', p[0] + ' 800w, ' + p[1] + ' 1400w'); }
    s.appendChild(img); return s;
  }
  function media(list) {
    var box = el('div', 'cine-media');
    list.forEach(function (p, i) { box.appendChild(slide(p, i === 0)); });
    var first = box.querySelector('img');
    function rest() {
      [].forEach.call(box.querySelectorAll('img[data-src]'), function (i) { i.srcset = i.getAttribute('data-srcset'); i.src = i.getAttribute('data-src'); });
      if (list.length > 1 && !reduce) box.classList.add('is-cycling');
    }
    if (first.complete) rest(); else first.addEventListener('load', rest, { once: true });
    return box;
  }

  if (v === 'cine1') {
    var list = isTech ? TECH : HOME;
    if (reduce) list = list.slice(0, 1);
    hero.insertBefore(el('div', 'cine-shade'), hero.firstChild);
    hero.insertBefore(media(list), hero.firstChild);
    hero.appendChild(caption(list[0]));
  } else if (v === 'cine2') {
    var panel = el('div', 'cine-panel');
    panel.appendChild(media([SPLIT]));
    panel.appendChild(el('div', 'cine-vignette'));
    if (!reduce) { panel.appendChild(el('div', 'cine-grain')); panel.appendChild(el('div', 'cine-leak')); }
    panel.appendChild(caption(SPLIT));
    hero.insertBefore(panel, hero.firstChild);
  } else {
    var field = el('div', 'cine-field');
    hero.insertBefore(field, hero.firstChild);
    var art = hero.querySelector('.hero-art');
    if (art) {  // homepage: the seal returns, as on the live hero
      var seal = el('div', 'cine-seal'), img = document.createElement('img');
      img.src = '/logos/arena/seal-halo-720.png'; img.alt = ''; img.width = 720; img.height = 720;
      seal.appendChild(img); art.insertBefore(seal, art.firstChild);
    }
    var opts = { paper: '#FFFFFF', paper2: '#F5F7FA', ink: '#0B1A4A', ink2: '#2F55A8',
      calmSel: '.hero-riso-copy, .el-hero-grid > div:first-child', ambient: isTech ? 0.17 : 0.27, calm: isTech ? 0.92 : 0.78, fadeB: 0.3 };
    var start = function () { if (window.RisoParticles) window.RisoParticles(field, opts); };
    if (window.RisoParticles) start();
    else { var s = document.createElement('script'); s.src = '/riso-particles.js'; s.onload = start; document.head.appendChild(s); }
  }
})();
