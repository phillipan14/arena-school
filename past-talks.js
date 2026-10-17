/* Past talks page: the audience filter (HERO2-BRIEF D). Each chip is a toggle button (aria-pressed); one is on at
   a time; cards whose data-aud does not match are hidden. Without JavaScript every card shows. */
(() => {
  const chips = [...document.querySelectorAll('.pt-chip')];
  const cards = [...document.querySelectorAll('.pt-card')];
  chips.forEach((c) => c.addEventListener('click', () => {
    chips.forEach((x) => x.setAttribute('aria-pressed', x === c ? 'true' : 'false'));
    const f = c.dataset.f;
    cards.forEach((k) => { k.hidden = f !== 'all' && k.dataset.aud !== f; });
  }));
})();
