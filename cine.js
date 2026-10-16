/* cine.js: the site hero (cine4, approved Oct 16, 2026). tools/hero_markup.py writes the markup:
   section.cine-hero > .cine-media (photo slots; each a <picture> with a desktop <source>; the first loads
   eagerly), .cine-shade, .cine-dots (a static CSS dot grid, no script), .cine-caps, and the crest in the hero copy.
   This file: starts the
   Ken Burns (.is-live), loads the remaining photos once the first has loaded and starts the crossfade
   (.is-cycling), and centers the crest when the copy is centered. Under Reduce Motion the photos still crossfade and move, gently (css/cine.css and
   the motion tokens in css/pro.css); only the timing changes, so nothing here checks the setting. */
(function () {
  'use strict';
  var hero = document.querySelector('main section.cine-hero');
  if (!hero) return;

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
  if (media && first) {
    media.classList.add('is-live');
    if (first.complete) rest(); else first.addEventListener('load', rest, { once: true });
  }

  var crest = hero.querySelector('.cine-crest');
  function align() { if (crest) crest.classList.toggle('is-centered', getComputedStyle(crest.parentElement).textAlign === 'center'); }
  align(); window.addEventListener('resize', align);
})();
