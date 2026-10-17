/* AI fluency self-assessment (FLUENCY-BRIEF): pick a statement, see your level and the next step, in place.
   Client-side only: nothing is sent or stored. Native radio buttons, so it works with the keyboard. */
(() => {
  document.querySelectorAll('[data-fluency]').forEach((form) => {
    const d = JSON.parse(form.querySelector('.fl-data').textContent);
    const out = form.querySelector('.fl-result');
    const fill = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => o[k]);
    form.addEventListener('change', (e) => {
      if (!e.target.matches('input[name="fl-level"]')) return;
      const n = +e.target.value, cur = d.levels[n - 1], next = d.levels[n];
      form.querySelectorAll('.fl-opt').forEach((l) => l.classList.toggle('is-on', l.contains(e.target)));
      out.textContent = fill(d.res, { n, name: cur.name }) + ' ' + (next ? fill(d.nxt, { n: n + 1, name: next.name, desc: next.desc }) : d.top);
      out.classList.add('is-shown');
    });
  });
})();
