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
  // pin = the pointer is on the chart itself. Then the spotlight stays in place (no reordering, no
  // slimming): moving lanes under a still cursor would hand the hover to another lane, which moves
  // them again, an endless flicker. Cards and links outside the chart keep the reorder.
  const spotlight = (progs, pin) => {
    clearTimeout(clearTimer);
    const k = key(progs) + (pin ? '|pin' : '');
    if (current === k) return;
    current = k;
    const change = () => {
      map.classList.toggle('gm-pin', !!pin);
      map.classList.add('has-focus');
      lanes.forEach((l) => l.classList.toggle('is-focus', progs.includes(l.dataset.prog)));
    };
    if (pin) change(); else flip(change);
  };
  // Small delay on clear so moving between a card and its links doesn't flicker.
  const clear = () => {
    clearTimeout(clearTimer);
    clearTimer = setTimeout(() => {
      current = '';
      const change = () => {
        map.classList.remove('has-focus', 'gm-pin');
        lanes.forEach((l) => l.classList.remove('is-focus'));
      };
      if (map.classList.contains('gm-pin')) change(); else flip(change);
    }, 90);
  };
  const bind = (el, progs, onLeave, pin) => {
    el.addEventListener('mouseenter', () => spotlight(progs, pin));
    el.addEventListener('mouseleave', onLeave || clear);
    el.addEventListener('focus', () => spotlight(progs, pin));
    el.addEventListener('blur', clear);
  };

  lanes.forEach((l) => bind(l, [l.dataset.prog], null, true));
  document.querySelectorAll('#programs .prog-card').forEach((card) => {
    const links = [...card.querySelectorAll('[data-prog]')];
    const progs = links.map((a) => a.dataset.prog);
    if (!progs.length) return;
    bind(card, progs);
    // Inside a card, one link narrows the spotlight; leaving the link returns to the card's set.
    links.forEach((a) => bind(a, [a.dataset.prog], () => spotlight(progs)));
  });
})();
