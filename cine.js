/* cine.js: cinematic hero previews (css/cine.css) on the homepage and /schools/technology.
   ?hero=cine1|cine2|cine3|cine4|cine5 picks one (cine4/5: cine1's photos with the crest and a light
   particle field over the photo; see PHOTO-PICKS.md for the photo choice); with no parameter this file does nothing and the page keeps its
   default hero. Real repo photos only: the first photo loads eagerly, the rest after it has loaded.
   cine3 reuses the live homepage's particle field (riso-particles.js) on cool paper. Loaded with defer,
   after riso-particles.js where a page has it. */
(function () {
  'use strict';
  var m = /[?&]hero=(cine[1-5])\b/i.exec(location.search);
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
  // The brightest, most energetic real photos (PHOTO-PICKS.md). The cohort group photo is out of rotation.
  var DUO = ['/photos/isb-2026/pitch-duo-800.webp', '/photos/isb-2026/pitch-duo-1600.webp', '62% 38%', 'Presenting at demo day, Beijing 2026', '路演日展示，北京，2026年'];
  var GESTURE = ['/photos/isb-hq/isb-pitch-gesture-800.webp', '/photos/isb-hq/isb-pitch-gesture-1400.webp', '60% 30%', 'Pitching to the panel, Beijing 2026', '向评委路演，北京，2026年'];
  var MENTORS = ['/photos/isb-2026/mentor-feedback-800.webp', '/photos/isb-2026/mentor-feedback-1600.webp', '50% 35%', 'Mentors react to a demo, Beijing 2026', '导师为学生展示叫好，北京，2026年'];
  var HANDS_ON = ['/photos/steps/collab-stage-poster.webp', '/photos/steps/collab-stage-poster.webp', '55% 45%', 'Building together, Hong Kong 2025', '一起动手做，香港，2025年'];
  var HOME = [DUO, GESTURE, MENTORS, HANDS_ON];
  var TECH = [HANDS_ON, MENTORS, DUO];
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

  function particles(field, opts) {
    var start = function () { if (window.RisoParticles) window.RisoParticles(field, opts); };
    if (window.RisoParticles) start();
    else { var s = document.createElement('script'); s.src = '/riso-particles.js'; s.onload = start; document.head.appendChild(s); }
  }
  function crest(cls, file) {
    var c = el('div', cls), img = document.createElement('img');
    img.src = file; img.alt = ''; img.decoding = 'async'; c.appendChild(img); return c;
  }

  if (v === 'cine1' || v === 'cine4' || v === 'cine5') {
    var list = isTech ? TECH : HOME;
    if (reduce) list = list.slice(0, 1);
    hero.insertBefore(el('div', 'cine-shade'), hero.firstChild);
    hero.insertBefore(media(list), hero.firstChild);
    hero.appendChild(caption(list[0]));
    if (v !== 'cine1') {
      // light dots on black paper, screened over the photo: the black drops out, the dots stay faint
      var dots = el('div', 'cine-field cine-field-light');
      hero.insertBefore(dots, hero.querySelector('.cine-shade').nextSibling);
      particles(dots, { paper: '#000000', paper2: '#000000', ink: '#A9BEEA', ink2: '#FFFFFF', mix: 0.6, ambient: 0.24, calm: 0.95, top: 0.6, fadeB: 0.15,
        calmSel: '.hero-riso-copy, .el-hero-grid > div:first-child' });
      if (v === 'cine4') {
        var copy = hero.querySelector('.hero-riso-copy, .el-hero-grid > div:first-child');
        copy.insertBefore(crest('cine-crest', '/logos/arena/seal-ivory-512.png'), copy.firstChild);
      } else {
        hero.insertBefore(crest('cine-watermark', '/logos/arena/seal-ivory-1024.png'), hero.querySelector('.cine-field-light').nextSibling);
      }
    }
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
    particles(field, { paper: '#FFFFFF', paper2: '#F5F7FA', ink: '#0B1A4A', ink2: '#2F55A8',
      calmSel: '.hero-riso-copy, .el-hero-grid > div:first-child', ambient: isTech ? 0.17 : 0.27, calm: isTech ? 0.92 : 0.78, fadeB: 0.3 });
  }
})();
