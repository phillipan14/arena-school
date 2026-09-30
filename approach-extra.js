/* ============================================================
   Arena — approach-extra.js  (Approach page only)
   1. Pillar cards: row alignment (measures .ap-pcard-align and
      matches heights, so the three "principles" toggles start
      at the same baseline without CSS Grid row-sharing, which
      would otherwise stretch closed cards to match an open one).
      Hover lift + dim siblings is pure CSS; this opens/collapses
      "The principles behind it" (a native <details>) on hover
      intent, same rhythm as xpand.js. Click, keyboard (Enter/
      Space on <summary>) and touch keep the native toggle as-is.
   2. Day timeline: hover / focus / tap highlights one step and
      dims the rest. The connecting progress line's scroll-in
      draw is handled in CSS via the shared .reveal/.in class.
   ============================================================ */
(() => {
  'use strict';
  const canHover = () => matchMedia('(hover: hover)').matches;

  /* ---------- Pillar cards: match row heights across the three cards ---------- */
  document.querySelectorAll('.ap-pcards').forEach((group) => {
    const blocks = [...group.querySelectorAll('.ap-pcard-align')];
    if (blocks.length < 2) return;
    let raf;
    const sync = () => {
      blocks.forEach((b) => { b.style.minHeight = ''; });
      const max = Math.max(...blocks.map((b) => b.offsetHeight));
      blocks.forEach((b) => { b.style.minHeight = max + 'px'; });
    };
    const debounced = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(sync); };
    debounced();
    addEventListener('resize', debounced, { passive: true });
    addEventListener('load', debounced);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(debounced);
  });

  /* ---------- Pillar cards: hover-open principles ---------- */
  document.querySelectorAll('.ap-pcards').forEach((group) => {
    const cards = [...group.querySelectorAll('.ap-pcard')];
    cards.forEach((card) => {
      const details = card.querySelector('.gc-more');
      if (!details) return;
      let timer;
      card.addEventListener('mouseenter', () => {
        if (!canHover()) return;
        clearTimeout(timer);
        timer = setTimeout(() => { details.open = true; }, 160);
      });
      card.addEventListener('mouseleave', () => {
        if (!canHover()) return;
        clearTimeout(timer);
        timer = setTimeout(() => { details.open = false; }, 240);
      });
      card.addEventListener('focusout', (e) => {
        if (card.contains(e.relatedTarget)) return;
        clearTimeout(timer);
        if (canHover()) details.open = false;
      });
    });
  });

  /* ---------- Day timeline: hover / focus / tap highlight ---------- */
  document.querySelectorAll('.ap-timeline').forEach((tl) => {
    const items = [...tl.querySelectorAll('.ap-tl-item')];
    if (!items.length) return;
    items.forEach((it) => {
      it.setAttribute('tabindex', '0');
      const on = () => { tl.classList.add('has-hover'); items.forEach((o) => o.classList.toggle('is-hover', o === it)); };
      const off = () => { tl.classList.remove('has-hover'); items.forEach((o) => o.classList.remove('is-hover')); };
      it.addEventListener('mouseenter', on);
      it.addEventListener('mouseleave', off);
      it.addEventListener('focus', on);
      it.addEventListener('blur', off);
      it.addEventListener('click', () => {
        if (canHover()) return; // desktop: hover already owns this
        const active = it.classList.contains('is-hover');
        off();
        if (!active) on();
      });
    });
  });
})();
