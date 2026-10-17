/* Team credential rows ("Studied at" / "Worked at"): every row becomes a slow, seamless marquee; neighbouring rows
   drift in opposite directions. The label column stays put; only the logos move.
   Markup it upgrades: .hp-cred-row (home, about, programs, mentorship, zero-to-launch) and .pro-logos (schools,
   technology, events), both <label><ul><li><img></li></ul>. Opt a row out with data-marquee="off".
   The original <ul> keeps its alt text; copies are aria-hidden with empty alt. The track is translated by exactly one
   set (list width + gap), so the loop is seamless at any width; it is re-measured when logos load or the row resizes.
   Styles: tools/cred_css.py (.cred-marq). Reduced motion: nothing runs, the rows stay as a still, wrapping row. */
(() => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const rows = [...document.querySelectorAll('main :is(.hp-cred-row, .pro-logos):not([data-marquee="off"])')];
  const MIN_S = 35, MAX_S = 50, PX_PER_S = 24;

  const copyOf = (ul) => {
    const c = ul.cloneNode(true);
    c.setAttribute('aria-hidden', 'true');
    // eager: clipped copies never intersect the viewport, so lazy ones would stay blank (same URLs, already cached)
    c.querySelectorAll('img').forEach((img) => { img.alt = ''; img.loading = 'eager'; });
    return c;
  };

  const fit = (wrap, track, ul) => {
    const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
    const shift = ul.getBoundingClientRect().width + gap;
    if (shift <= gap) return;
    // enough copies that the track still covers the window after moving one set left
    const need = Math.min(12, Math.max(2, Math.ceil(wrap.clientWidth / shift) + 1));
    while (track.children.length < need) track.appendChild(copyOf(ul));
    while (track.children.length > need) track.lastElementChild.remove();
    const dur = Math.min(MAX_S, Math.max(MIN_S, shift / PX_PER_S));
    track.style.setProperty('--marq-shift', shift.toFixed(2) + 'px');
    track.style.setProperty('--marq-dur', dur.toFixed(1) + 's');
    wrap.classList.add('is-on');
  };

  rows.forEach((row) => {
    const ul = row.querySelector(':scope > ul');
    if (!ul || ul.children.length < 3 || row.querySelector('.cred-marq')) return;
    const siblings = [...row.parentElement.children].filter((el) => rows.includes(el));
    const wrap = document.createElement('div');
    wrap.className = 'cred-marq';
    const track = document.createElement('div');
    track.className = 'cred-marq-track' + (siblings.indexOf(row) % 2 ? ' is-rev' : '');
    ul.before(wrap);
    wrap.appendChild(track);
    track.appendChild(ul);
    let raf = 0;
    const refit = () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(() => fit(wrap, track, ul)); };
    if ('ResizeObserver' in window) {
      const ro = new ResizeObserver(refit);
      ro.observe(wrap);
      ro.observe(ul);
    } else {
      addEventListener('resize', refit);
    }
    ul.querySelectorAll('img').forEach((img) => { if (!img.complete) img.addEventListener('load', refit, { once: true }); });
    refit();
  });
})();
