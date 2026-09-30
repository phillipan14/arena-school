/* FAQ items: with a mouse, open on hover and close on leave (same feel as the co-founder cards).
   Touch and keyboard keep the native toggle. Height animates both ways; reduced motion snaps. */
(() => {
  const items = [...document.querySelectorAll('details.faq-item')];
  if (!items.length) return;
  const mouse = matchMedia('(hover: hover) and (pointer: fine)');
  const still = matchMedia('(prefers-reduced-motion: reduce)');

  items.forEach((d) => {
    const summary = d.querySelector('summary');
    let anim = null;
    let closing = false;
    let timer;

    const animate = (from, to, done) => {
      if (anim) anim.cancel();
      if (still.matches || from === to) { done && done(); return; }
      d.style.overflow = 'hidden';
      anim = d.animate({ height: [from + 'px', to + 'px'] }, { duration: 340, easing: 'cubic-bezier(.2,.7,.2,1)' });
      anim.onfinish = () => { anim = null; d.style.overflow = ''; done && done(); };
      anim.oncancel = () => { anim = null; d.style.overflow = ''; };
    };
    const open = () => {
      if (d.open && !closing) return;
      const from = d.getBoundingClientRect().height;
      closing = false;
      d.open = true;
      animate(from, d.getBoundingClientRect().height);
    };
    const close = () => {
      if (!d.open || closing) return;
      const from = d.getBoundingClientRect().height;
      d.open = false;
      const to = d.getBoundingClientRect().height;
      d.open = true;
      closing = true;
      animate(from, to, () => { d.open = false; closing = false; });
    };

    d.addEventListener('mouseenter', () => { if (!mouse.matches) return; clearTimeout(timer); timer = setTimeout(open, 110); });
    d.addEventListener('mouseleave', () => { if (!mouse.matches) return; clearTimeout(timer); timer = setTimeout(close, 140); });
    // Mouse clicks are owned by hover; keyboard (detail 0) and touch still toggle. Capture phase so
    // older click handlers on the summary (pp-interact.js) never toggle it against the hover state.
    d.addEventListener('click', (e) => {
      if (!mouse.matches || e.detail === 0 || !summary.contains(e.target)) return;
      e.preventDefault();
      e.stopPropagation();
      open();
    }, true);
  });
})();
