/* Homepage hero: rotate the audience word (students, families, educators, schools).
   The slot (.hr-rot, inline-grid) takes each word's measured width, animated over 400ms (css/cine.css),
   so the rest of the line glides along with no gap. Order: the old word fades out, the slot resizes,
   then the new word fades in; two words are never visible at once. Static under reduced motion. */
(() => {
  const rot = document.querySelector('[data-rot]');
  if (!rot || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const words = [...rot.children];
  let i = 0;
  const fit = () => { rot.style.width = words[i].getBoundingClientRect().width + 'px'; };
  const after = (el, prop, ms, fn) => {
    let done = false;
    const go = () => { if (done) return; done = true; el.removeEventListener('transitionend', on); fn(); };
    const on = (e) => { if (e.target === el && e.propertyName === prop) go(); };
    el.addEventListener('transitionend', on);
    setTimeout(go, ms);
  };
  rot.classList.add('is-live');
  fit();
  setInterval(() => {
    if (document.hidden) return;
    const prev = words[i];
    i = (i + 1) % words.length;
    const next = words[i];
    prev.classList.remove('is-on');
    prev.classList.add('is-out');
    // each step waits for the previous transition to finish (with a fallback), so a slow frame can
    // never leave the old word visible when the new one appears
    after(prev, 'opacity', 320, () => {
      prev.classList.remove('is-out');
      fit();
      after(rot, 'width', 480, () => next.classList.add('is-on'));
    });
  }, 2800);
  addEventListener('resize', fit, { passive: true });
})();
