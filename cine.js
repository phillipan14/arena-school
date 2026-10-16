/* cine.js: the site hero (cine4, approved Oct 16, 2026). tools/hero_markup.py writes the markup:
   section.cine-hero > .cine-media (photo slots; each a <picture> with a desktop <source>; the first loads
   eagerly), .cine-shade, .cine-field-light, .cine-caps, and the crest in the hero copy.
   This file: starts the
   Ken Burns (.is-live), loads the remaining photos once the first has loaded and starts the crossfade
   (.is-cycling), draws the faint light particle field (riso-particles.js, started when the page is idle), and centers the
   crest when the copy is centered. Under prefers-reduced-motion: one still photo, no zoom or pan. */
(function () {
  'use strict';
  var hero = document.querySelector('main section.cine-hero');
  if (!hero) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var media = hero.querySelector('.cine-media');
  var caps = hero.querySelector('.cine-caps');
  var first = media && media.querySelector('img');
  function rest() {
    [].forEach.call(media.querySelectorAll('[data-srcset], img[data-src]'), function (el) {
      if (el.getAttribute('data-srcset')) { el.srcset = el.getAttribute('data-srcset'); el.removeAttribute('data-srcset'); }
      if (el.getAttribute('data-src')) { el.src = el.getAttribute('data-src'); el.removeAttribute('data-src'); }
    });
    if (media.querySelectorAll('.cine-slide').length > 1) { media.classList.add('is-cycling'); if (caps) caps.classList.add('is-cycling'); }
  }
  if (media && !reduce) {
    media.classList.add('is-live');
    if (first.complete) rest(); else first.addEventListener('load', rest, { once: true });
  }

  var dots = hero.querySelector('.cine-field-light');
  if (dots) {
    // light dots on black paper, screen-blended over the photo: the black drops out, the dots stay faint
    var opts = { paper: '#000000', paper2: '#000000', ink: '#A9BEEA', ink2: '#FFFFFF', mix: 0.6, ambient: 0.24, calm: 0.95, top: 0.6, fadeB: 0.15,
      calmSel: '.hero-riso-copy, .hero-copy, .el-hero-grid > div:first-child' };
    if (window.innerWidth <= 900) { opts.pitch = 5.5; opts.dot = 2.2; }   // phones: fewer dots, same look
    var start = function () { if (window.RisoParticles) window.RisoParticles(dots, opts); };
    var load = function () {
      if (window.RisoParticles) start();
      else { var s = document.createElement('script'); s.src = '/riso-particles.js'; s.onload = start; document.head.appendChild(s); }
    };
    // the dots are decoration: start them only after the page has loaded and the main thread is idle,
    // so they never compete with the first photo or the text for the first paint
    var idle = function () { (window.requestIdleCallback || function (f) { setTimeout(f, 200); })(load, { timeout: 2500 }); };
    if (navigator.connection && navigator.connection.saveData) { /* skip decoration on data saver */ }
    else if (document.readyState === 'complete') idle(); else window.addEventListener('load', idle, { once: true });
  }

  var crest = hero.querySelector('.cine-crest');
  function align() { if (crest) crest.classList.toggle('is-centered', getComputedStyle(crest.parentElement).textAlign === 'center'); }
  align(); window.addEventListener('resize', align);
})();
