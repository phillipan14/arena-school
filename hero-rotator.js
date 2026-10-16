/* Homepage hero: rotate the audience word (students, families, educators, schools) with a true crossfade
   (XFADE, Oct 17, 2026). Every word sits in the same grid cell (css/cine.css), so the slot is always as wide as
   the widest word and the headline never moves. On each change the outgoing word fades out while the incoming
   word fades in, in the same frame, over about 700ms: there is never an empty frame. With Reduce Motion it is a
   plain opacity crossfade (no slide or blur). */
(() => {
  const rot = document.querySelector('[data-rot]');
  if (!rot) return;
  const words = [...rot.children];
  let i = Math.max(0, words.findIndex((w) => w.classList.contains('is-on')));
  rot.classList.add('is-live', 'is-xfade');
  setInterval(() => {
    if (document.hidden) return;
    const prev = words[i];
    i = (i + 1) % words.length;
    const next = words[i];
    words.forEach((w) => { if (w !== prev) w.classList.remove('is-out'); });
    prev.classList.remove('is-on');
    prev.classList.add('is-out');      // fades out ...
    next.classList.add('is-on');       // ... while this fades in, same frame
    setTimeout(() => prev.classList.remove('is-out'), 900);
  }, 2800);
})();
