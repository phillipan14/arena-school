/* Homepage hero: rotate the audience word (students, families, educators, schools).
   The wrapper's width eases to each word so the sentence reflows smoothly. Static under reduced motion. */
(() => {
  const rot = document.querySelector('[data-rot]');
  if (!rot || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const words = [...rot.children];
  let i = 0;
  const fit = (el) => { rot.style.width = el.offsetWidth + 'px'; };
  rot.classList.add('is-live'); // words stop stretching to the widest before we measure
  fit(words[0]);
  setInterval(() => {
    if (document.hidden) return;
    const prev = words[i];
    i = (i + 1) % words.length;
    prev.classList.remove('is-on');
    prev.classList.add('is-out');
    setTimeout(() => prev.classList.remove('is-out'), 600);
    words[i].classList.add('is-on');
    fit(words[i]);
  }, 2600);
  addEventListener('resize', () => fit(words[i]), { passive: true });
})();
