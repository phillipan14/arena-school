/* Homepage grade map: draw the bars when the chart scrolls into view (once), and spotlight lanes.
   Hovering a program card lights all of its lanes; hovering one program link (or a lane) lights just
   that lane. Other lanes fade to grey and slim down; everything reverts when the pointer leaves. */
(() => {
  const map = document.querySelector('[data-gmap]');
  if (!map) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!('IntersectionObserver' in window) || reduce) map.classList.add('is-in');
  else {
    const io = new IntersectionObserver((entries) => {
      if (entries.some((e) => e.isIntersecting)) { map.classList.add('is-in'); io.disconnect(); }
    }, { threshold: 0.35 });
    io.observe(map);
  }

  const lanes = [...map.querySelectorAll('.gm-lane')];
  let clearTimer;
  // FLIP: remember where each lane is, change state (focused lanes jump to the top via CSS order),
  // then animate every lane from its old position to its new one.
  const flip = (change) => {
    const before = new Map(lanes.map((l) => [l, l.getBoundingClientRect().top]));
    change();
    if (reduce) return;
    lanes.forEach((l) => {
      const dy = before.get(l) - l.getBoundingClientRect().top;
      if (Math.abs(dy) > 1) l.animate([{ transform: `translateY(${dy}px)` }, { transform: 'none' }], { duration: 520, easing: 'cubic-bezier(.2,.7,.2,1)' });
    });
  };
  const key = (progs) => progs.join(',');
  let current = '';
  const spotlight = (progs) => {
    clearTimeout(clearTimer);
    if (current === key(progs)) return;
    current = key(progs);
    flip(() => {
      map.classList.add('has-focus');
      lanes.forEach((l) => l.classList.toggle('is-focus', progs.includes(l.dataset.prog)));
    });
  };
  // Small delay on clear so moving between a card and its links doesn't flicker.
  const clear = () => {
    clearTimeout(clearTimer);
    clearTimer = setTimeout(() => {
      current = '';
      flip(() => {
        map.classList.remove('has-focus');
        lanes.forEach((l) => l.classList.remove('is-focus'));
      });
    }, 90);
  };
  const bind = (el, progs, onLeave) => {
    el.addEventListener('mouseenter', () => spotlight(progs));
    el.addEventListener('mouseleave', onLeave || clear);
    el.addEventListener('focus', () => spotlight(progs));
    el.addEventListener('blur', clear);
  };

  lanes.forEach((l) => bind(l, [l.dataset.prog]));
  document.querySelectorAll('#programs .prog-card').forEach((card) => {
    const links = [...card.querySelectorAll('[data-prog]')];
    const progs = links.map((a) => a.dataset.prog);
    if (!progs.length) return;
    bind(card, progs);
    // Inside a card, one link narrows the spotlight; leaving the link returns to the card's set.
    links.forEach((a) => bind(a, [a.dataset.prog], () => spotlight(progs)));
  });
})();
