/* Homepage team logos: each row becomes a slow marquee; rows drift in opposite directions.
   Items are cloned (aria-hidden) until one set is wider than the row, then doubled for a seamless loop. */
(() => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const rows = [...document.querySelectorAll('body.home .hp-cred-row')];
  rows.forEach((row, i) => {
    const ul = row.querySelector('ul');
    if (!ul || ul.dataset.marq) return;
    ul.dataset.marq = '1';
    const wrap = document.createElement('div');
    wrap.className = 'hp-marq';
    ul.before(wrap);
    wrap.appendChild(ul);
    ul.classList.add('is-marq'); // max-content width first, so measurements are real
    const originals = [...ul.children];
    const cloneSet = () => originals.forEach((li) => {
      const c = li.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      c.querySelectorAll('img').forEach((img) => (img.alt = ''));
      ul.appendChild(c);
    });
    // Make one "set" at least as wide as the viewport, then double it.
    let guard = 0;
    while (ul.scrollWidth < wrap.clientWidth + 200 && guard++ < 4) cloneSet();
    const setCount = ul.children.length;
    [...ul.children].slice(0, setCount).forEach((li) => {
      const c = li.cloneNode(true);
      c.setAttribute('aria-hidden', 'true');
      c.querySelectorAll('img').forEach((img) => (img.alt = ''));
      ul.appendChild(c);
    });
    const pxPerSec = 22;
    ul.style.setProperty('--marq-dur', Math.round(ul.scrollWidth / 2 / pxPerSec) + 's');
    if (i % 2) ul.classList.add('is-rev');
  });
})();
