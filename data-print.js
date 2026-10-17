/* Student data checklist: "Print the checklist" prints only the checklist (DATA-BRIEF; print rules in css/ds.css). */
(() => {
  document.querySelectorAll('[data-print-checklist]').forEach((b) => b.addEventListener('click', () => {
    document.documentElement.classList.add('print-checklist');
    const done = () => { document.documentElement.classList.remove('print-checklist'); removeEventListener('afterprint', done); };
    addEventListener('afterprint', done);
    window.print();
    setTimeout(done, 1500);
  }));
})();
