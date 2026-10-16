/* Homepage film: click (or Enter/Space) on the play button loads and plays the film with sound,
   then hands over to the native controls. No autoplay; the video downloads nothing before the click. */
(() => {
  for (const frame of document.querySelectorAll('[data-film]')) {
    const video = frame.querySelector('video');
    const btn = frame.querySelector('.film-play');
    if (!video || !btn) continue;
    btn.addEventListener('click', () => {
      frame.classList.add('is-playing');
      video.controls = true;
      video.muted = false;
      const p = video.play();
      if (p && p.catch) p.catch(() => { /* playback refused: the native controls stay available */ });
      video.focus({ preventScroll: true });
    });
  }
})();
