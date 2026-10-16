/* Homepage hero: rotate the audience word (students, families, educators, schools).
   The words share one fixed-width slot (the widest word, EN or CN), so the sentence never reflows. The
   outgoing word fades out first, then the next fades in: two words are never visible at once.
   Static under reduced motion. Styles: css/pillars.css (.hr-rot) and css/cine.css. */
(() => {
  const rot = document.querySelector('[data-rot]');
  if (!rot || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const words = [...rot.children];
  let i = 0;
  rot.classList.add('is-live');
  setInterval(() => {
    if (document.hidden) return;
    const prev = words[i];
    i = (i + 1) % words.length;
    const next = words[i];
    prev.classList.remove('is-on');
    prev.classList.add('is-out');
    setTimeout(() => { prev.classList.remove('is-out'); next.classList.add('is-on'); }, 320);
  }, 2600);
})();
