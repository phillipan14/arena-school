/* Homepage opening:
   1. The crest turns over to its navy face the first time the pointer rests on it, and stays (no flipping back).
   2. "See what we do" glides to the photo gallery, and so does the first downward scroll from the very top
      (wheel, trackpad, swipe, or keys), so the opening screen leads straight into the photos. */
(() => {
  const flip = document.querySelector('[data-seal-flip]');
  if (flip) {
    const turn = () => flip.classList.add('is-flipped');
    flip.addEventListener('mouseenter', turn, { once: true });
    flip.addEventListener('click', turn, { once: true });
  }

  const gallery = document.getElementById('gallery');
  const cue = document.querySelector('[data-hero-more]');
  if (!gallery) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let busy = false;
  const go = () => {
    busy = true;
    gallery.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    setTimeout(() => { busy = false; }, 1100);   // swallow the rest of a trackpad's momentum
  };
  if (cue) cue.addEventListener('click', (e) => { e.preventDefault(); go(); });

  const atTop = () => window.scrollY < 8;
  const menuOpen = () => document.body.classList.contains('menu-open') || document.documentElement.classList.contains('menu-open');
  window.addEventListener('wheel', (e) => {
    if (busy) { if (e.deltaY > 0 && window.scrollY < gallery.offsetTop) e.preventDefault(); return; }
    if (e.deltaY > 4 && atTop() && !menuOpen() && !e.ctrlKey) { e.preventDefault(); go(); }
  }, { passive: false });
  let y0 = null;
  window.addEventListener('touchstart', (e) => { y0 = atTop() ? e.touches[0].clientY : null; }, { passive: true });
  window.addEventListener('touchmove', (e) => {
    if (y0 === null || busy || menuOpen()) return;
    if (y0 - e.touches[0].clientY > 24) { e.preventDefault(); y0 = null; go(); }
  }, { passive: false });
  window.addEventListener('keydown', (e) => {
    if (!atTop() || busy || menuOpen()) return;
    const t = e.target, typing = t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName));
    if (typing) return;
    if (e.key === 'ArrowDown' || e.key === 'PageDown' || (e.key === ' ' && !e.shiftKey)) { e.preventDefault(); go(); }
  });
})();
