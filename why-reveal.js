/* "Why it matters" reveals: hover is pure CSS; on touch screens a tap toggles the point open. */
(() => {
  if (matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  document.querySelectorAll('.has-wr > li').forEach((li) => {
    li.addEventListener('click', (e) => {
      if (e.target.closest('a')) return;
      li.classList.toggle('wr-open');
    });
  });
})();
