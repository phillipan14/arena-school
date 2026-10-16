/* cine.js: the site hero (cine4, approved Oct 16, 2026). tools/hero_markup.py writes the markup:
   section.cine-hero > .cine-media (photo slides; the first loads eagerly), .cine-shade, .cine-field-light,
   and the crest in the hero copy. This file loads the remaining slides once the first has loaded,
   starts the slow crossfade, draws the faint light particle field (riso-particles.js, loaded on demand),
   and centers the crest when the hero copy is centered (phones). Under prefers-reduced-motion the
   first photo stays still and the dots do not move. */
(function () {
  'use strict';
  var hero = document.querySelector('main section.cine-hero');
  if (!hero) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var media = hero.querySelector('.cine-media');
  var first = media && media.querySelector('img');
  function rest() {
    [].forEach.call(media.querySelectorAll('img[data-src]'), function (img) {
      if (img.getAttribute('data-srcset')) img.srcset = img.getAttribute('data-srcset');
      img.src = img.getAttribute('data-src');
      img.removeAttribute('data-src'); img.removeAttribute('data-srcset');
    });
    if (media.querySelectorAll('.cine-slide').length > 1) media.classList.add('is-cycling');
  }
  if (first && !reduce) { if (first.complete) rest(); else first.addEventListener('load', rest, { once: true }); }

  var dots = hero.querySelector('.cine-field-light');
  if (dots) {
    // light dots on black paper, screen-blended over the photo: the black drops out, the dots stay faint
    var opts = { paper: '#000000', paper2: '#000000', ink: '#A9BEEA', ink2: '#FFFFFF', mix: 0.6, ambient: 0.24, calm: 0.95, top: 0.6, fadeB: 0.15,
      calmSel: '.hero-riso-copy, .hero-copy, .el-hero-grid > div:first-child' };
    var start = function () { if (window.RisoParticles) window.RisoParticles(dots, opts); };
    if (window.RisoParticles) start();
    else { var s = document.createElement('script'); s.src = '/riso-particles.js'; s.onload = start; document.head.appendChild(s); }
  }

  var crest = hero.querySelector('.cine-crest');
  function align() { if (crest) crest.classList.toggle('is-centered', getComputedStyle(crest.parentElement).textAlign === 'center'); }
  align(); window.addEventListener('resize', align);
})();
