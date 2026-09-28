/* Program pages: pinned scroll story. Progress through each [data-scrolly] block picks
   which beat and visual are showing; the activity line types itself on beat 2.
   Below 900px or with reduced motion, CSS stacks everything and this only fills content. */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var narrow = window.matchMedia('(max-width: 900px)');
  document.querySelectorAll('[data-scrolly]').forEach(function (root) {
    var field = root.querySelector('.pp-dotfield');
    if (field) {
      var n = 32 * 9, you = 32 * 4 + 21, html = '';
      for (var i = 0; i < n; i++) html += '<i' + (i === you ? ' class="is-you"' : '') + ' style="transition-delay:' + ((i % 32) * 12 + Math.floor(i / 32) * 20) + 'ms"></i>';
      field.innerHTML = html;
    }
    var beats = [].slice.call(root.querySelectorAll('.pp-sc-beat'));
    var vis = [].slice.call(root.querySelectorAll('.pp-sc-v'));
    var dots = [].slice.call(root.querySelectorAll('.pp-sc-dots li'));
    var typeEl = root.querySelector('[data-sc-type]'); var typed = false;
    function type() {
      if (!typeEl || typed) return; typed = true;
      var text = typeEl.getAttribute('data-sc-type'); var num = typeEl.parentElement.querySelector('.pp-count i'); var box = typeEl.parentElement.querySelector('.pp-count');
      if (reduce) { typeEl.textContent = text; if (num) num.textContent = text.length; return; }
      var i = 0; typeEl.classList.add('is-typing');
      (function tick() { i++; typeEl.textContent = text.slice(0, i); if (num) num.textContent = i; if (i < text.length) setTimeout(tick, 18); else { typeEl.classList.remove('is-typing'); box && box.classList.add('is-full'); } })();
    }
    if (typeEl) typeEl.textContent = '';
    var cur = -1;
    function set(k) {
      if (k === cur) return; cur = k;
      beats.forEach(function (b, i) { b.classList.toggle('is-on', i === k); b.classList.toggle('is-past', i < k); });
      vis.forEach(function (v, i) { v.classList.toggle('is-on', i === k); v.classList.toggle('is-past', i < k); });
      if (k >= 1) type();
    }
    function onScroll() {
      if (narrow.matches || reduce) { set(2); vis.forEach(function (v) { v.classList.add('is-on'); }); type(); return; }
      var r = root.getBoundingClientRect(); var total = r.height - window.innerHeight;
      var p = Math.min(1, Math.max(0, -r.top / Math.max(1, total)));
      var k = Math.min(2, Math.floor(p * 3));
      set(k);
      dots.forEach(function (d, i) { d.style.setProperty('--f', Math.min(1, Math.max(0, p * 3 - i)).toFixed(3)); });
    }
    var ticking = false;
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { onScroll(); ticking = false; }); } }, { passive: true });
    window.addEventListener('resize', onScroll);
    onScroll();
  });
  // Reel videos play only while visible
  var vids = [].slice.call(document.querySelectorAll('video[data-autoplay]'));
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.preload = 'auto'; e.target.play().catch(function () {}); } else e.target.pause(); }); }, { threshold: 0.2 });
    vids.forEach(function (v) { io.observe(v); });
  }
})();
