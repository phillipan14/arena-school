/* Logo rows: every logo strip on the site becomes a slow, seamless marquee; stacked rows drift in opposite directions.
   Markup it upgrades:
     - team credential rows ("Studied at" / "Worked at"): .hp-cred-row (home, about, programs, mentorship,
       zero-to-launch) and .pro-logos (schools, technology, events), both <label><ul><li><img></li></ul>. The label
       column stays put; only the logos move.
     - tool rows ("What students use"): ul.ds-tools (programs, mentorship, partnerships, schools, technology,
       zero-to-launch). The hairline frame stays put; only the logos move.
   Rows of 3 logos or fewer (the Anthropic + OpenAI "A member of" row, the results jury row) stay static and centered:
   a 2-logo loop reads as broken. Opt any row out with data-marquee="off".
   The original <ul> keeps its alt text; copies are aria-hidden with empty alt. The track is translated by exactly one
   set (list width + gap), so the loop is seamless at any width; it is re-measured when logos load or the row resizes.
   Styles: tools/cred_css.py (.cred-marq). Reduced motion: nothing runs, the rows stay as a still, wrapping row. */
(() => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const rows = [...document.querySelectorAll('main :is(.hp-cred-row, .pro-logos, ul.ds-tools):not([data-marquee="off"])')];
  const MIN_S = 35, MAX_S = 50, PX_PER_S = 24, MIN_LOGOS = 4;

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
    const isList = row.matches('ul');
    const ul = isList ? row : row.querySelector(':scope > ul');
    if (!ul || ul.children.length < MIN_LOGOS || ul.closest('.cred-marq')) return;
    const siblings = [...row.parentElement.children].filter((el) => rows.includes(el));
    const wrap = document.createElement('div');
    wrap.className = 'cred-marq';
    const track = document.createElement('div');
    track.className = 'cred-marq-track' + (siblings.indexOf(row) % 2 ? ' is-rev' : '');
    if (isList) {
      // a bare list (tools): a still frame carries its hairlines, so the edge fade never touches them
      const frame = document.createElement('div');
      frame.className = 'cred-marq-frame';
      ul.before(frame);
      frame.appendChild(wrap);
    } else {
      ul.before(wrap);
    }
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
