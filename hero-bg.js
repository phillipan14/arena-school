/* hero-bg.js: picks the homepage hero background (css/hero-bg.css). ?hero=A|B|C chooses one for review
   and screenshots; anything else (or no parameter) keeps the default, A. */
(function () {
  var bg = document.querySelector('[data-hero-bg]');
  if (!bg) return;
  var m = /[?&]hero=([abc])\b/i.exec(location.search);
  bg.setAttribute('data-variant', m ? m[1].toUpperCase() : 'A');
})();
