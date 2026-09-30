/* Card -> inline panel pattern, shared by the homepage co-founders and pillars.
   Markup: a grid [data-xp="<wide breakpoint px>"] holding buttons [data-xp-card="<id>"]
   (optionally wrapped in [data-xp-slot]) and one [data-xp-panel] whose [data-xp-box] holds
   [data-xp-for="<id>"] sections. Hover (with intent delay) or click opens the panel in the flow,
   so the section grows. Wide: panel spans the row under all cards, notch points at the active card.
   Narrow: panel moves directly under the tapped card. Pointer-leave keeps it open; the active card
   or Esc closes it. */
(() => {
  const canHover = matchMedia('(hover: hover)');
  document.querySelectorAll('[data-xp]').forEach((group) => {
    const panel = group.querySelector('[data-xp-panel]');
    if (!panel) return;
    const cards = [...group.querySelectorAll('[data-xp-card]')];
    const secs = [...panel.querySelectorAll('[data-xp-for]')];
    const box = panel.querySelector('[data-xp-box]') || panel;
    const wide = matchMedia(`(min-width: ${group.dataset.xp || 701}px)`);
    let active = null;
    let timer;

    const isOpen = () => panel.classList.contains('is-open');
    const slotOf = (card) => card.closest('[data-xp-slot]') || card;
    const place = () => {
      if (wide.matches || !active) { if (group.lastElementChild !== panel) group.appendChild(panel); return; }
      const slot = slotOf(active);
      if (slot.nextElementSibling !== panel) slot.after(panel);
    };
    const pointNotch = () => {
      if (!active) return;
      const t = (active.querySelector('[data-xp-notch]') || active).getBoundingClientRect();
      const b = box.getBoundingClientRect();
      box.style.setProperty('--nx', Math.round(t.left + t.width / 2 - b.left - 7) + 'px');
    };
    const show = (card) => {
      const id = card.dataset.xpCard;
      secs.forEach((s) => (s.hidden = s.dataset.xpFor !== id));
      cards.forEach((c) => c.setAttribute('aria-expanded', String(c === card)));
      active = card;
      group.classList.add('has-open');
      place();
      panel.classList.add('is-open');
      requestAnimationFrame(pointNotch);
    };
    const open = (card) => {
      if (active === card && isOpen()) return;
      if (!wide.matches && active && active !== card && isOpen()) {
        // Narrow: the panel moves between cards, so close, move, reopen.
        panel.classList.remove('is-open');
        setTimeout(() => show(card), 280);
        return;
      }
      show(card);
    };
    const close = () => {
      panel.classList.remove('is-open');
      cards.forEach((c) => c.setAttribute('aria-expanded', 'false'));
      group.classList.remove('has-open');
      active = null;
    };

    cards.forEach((card) => {
      card.addEventListener('mouseenter', () => {
        if (!canHover.matches || !wide.matches) return;
        clearTimeout(timer);
        timer = setTimeout(() => open(card), 220);
      });
      card.addEventListener('mouseleave', () => clearTimeout(timer));
      card.addEventListener('click', () => {
        clearTimeout(timer);
        if (active === card && isOpen()) close();
        else open(card);
      });
    });
    document.addEventListener('keydown', (e) => {
      if (e.key !== 'Escape' || !active) return;
      const was = active;
      close();
      was.focus();
    });
    const sync = () => { if (active) { place(); pointNotch(); } };
    addEventListener('resize', sync, { passive: true });
    wide.addEventListener?.('change', sync);
  });
})();
