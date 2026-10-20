/* Talk recording gate: /talk/recording (EN) and /talk/recording-cn (CN).
   RECORDING-BRIEF; /schools gate markup since RECORDING-REDESIGN-BRIEF; per-language files and lock states since
   RECORDING-ROUND3-BRIEF (Oct 19, 2026).

   CONFIG: the recording files, one entry per language. Each page plays its own language:
     videoEn / downloadEn   used by recording.html     (e.g. '/talks/2026-10-isb-parent-coffee/recording-en.mp4')
     videoCn / downloadCn   used by recording-cn.html  (e.g. '/talks/2026-10-isb-parent-coffee/recording-cn.mp4')
   A download left empty falls back to that language's video. If a page's own language has no video but the other
   language does, the page shows "Watch the English version" / "观看中文版录像" linking to the other page (?src= kept).
   A page can still override its own pair with data-video-src / data-download-src on .rec.

   States (classes on .rec, styled in css/recording.css): is-locked / is-open, has-src. Locked: a lock icon on the
   cover slide. After submit: an open lock, then the player (has-src) or "Recording coming soon" plus a note that we
   will email; the Download button shows only when a file exists. Reduce Motion: no icon animation, no delay.

   This is a SOFT gate: once uploaded, the video and download URLs are ordinary public files. The form collects who is
   watching and remembers the unlock in this browser (shared by both pages); it does not protect the files. That is
   acceptable for this talk.
   On submit (same backends as onepager.js): FormSubmit email to contact@, POST /api/interest (kind 'recording', Slack),
   and a quiet /api/subscribe. Either of the first two succeeding unlocks the page. */
(function () {
  // One bilingual file (English + Chinese subtitles) serves both pages.
  var CONFIG = { videoEn: '/talks/2026-10-isb-parent-coffee/recording.mp4', downloadEn: '',
                 videoCn: '/talks/2026-10-isb-parent-coffee/recording.mp4', downloadCn: '' };

  var root = document.querySelector('.rec');
  if (!root) return;
  var ZH = (document.documentElement.lang || '').indexOf('zh') === 0;
  var KEY = 'arena-rec-2026-10-isb-parent-coffee';
  var own = ZH ? 'Cn' : 'En', other = ZH ? 'En' : 'Cn';
  var video = root.getAttribute('data-video-src') || CONFIG['video' + own];
  var download = root.getAttribute('data-download-src') || CONFIG['download' + own] || video;
  var otherVideo = CONFIG['video' + other];
  var form = root.querySelector('.rec-form');
  var done = root.querySelector('.pp-lead-done');
  var slot = root.querySelector('.rv');
  var status = form.querySelector('.cf-status');
  var calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  root.classList.toggle('has-src', !!video);

  // Only the other language has a file: point to it, keeping ?src= for tracking.
  if (!video && otherVideo) {
    [].forEach.call(document.querySelectorAll('.rc-alt'), function (p) {
      var a = p.querySelector('a');
      if (a) a.href = a.getAttribute('href').split('?')[0] + location.search;
      p.hidden = false;
    });
  }

  function src() {
    var m = location.search.match(/[?&]src=([^&#]*)/);
    var v = '';
    try { v = m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : ''; } catch (e) { v = ''; }
    v = v.replace(/[^\w .:\-]/g, '').trim().slice(0, 40);
    return v || 'direct';
  }
  function remembered() { try { return localStorage.getItem(KEY) === '1'; } catch (e) { return false; } }
  function remember() { try { localStorage.setItem(KEY, '1'); } catch (e) { /* private mode: unlock for this visit only */ } }

  function showVideo() {
    if (!video || slot.querySelector('video')) return;
    var v = document.createElement('video');
    v.controls = true; v.setAttribute('playsinline', ''); v.preload = 'none';
    v.poster = slot.getAttribute('data-poster') || '';
    v.src = video;
    slot.appendChild(v);
  }
  // fresh: just submitted, so the open lock shows for a moment before the player (none under Reduce Motion or on return)
  function unlock(fresh) {
    root.classList.remove('is-locked'); root.classList.add('is-open');
    if (fresh && !calm) root.classList.add('is-opening');
    if (video) setTimeout(showVideo, fresh && !calm ? 700 : 0);
    var dl = done.querySelector('.rec-dl'), later = done.querySelector('.pp-lead-later'), ready = done.querySelector('.rec-ready');
    if (dl) { dl.hidden = !video; if (video) dl.href = download; }
    if (ready) ready.hidden = !video;
    if (later) later.hidden = !!video;
    form.hidden = true; done.hidden = false;
    if (fresh) done.focus();
  }

  function post(url, data) {
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(data)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok || j.ok === false || j.success === 'false' || j.success === false) throw new Error(j.error || j.message || ('HTTP ' + r.status));
        return j;
      });
    });
  }
  function setStatus(msg, kind) { status.textContent = msg; status.className = 'cf-status' + (kind ? ' cf-status-' + kind : ''); }

  if (remembered()) unlock(false);

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.reportValidity()) return;
    var data = {};
    form.querySelectorAll('input[name], select[name]').forEach(function (el) { data[el.name] = (el.value || '').trim(); });
    if (data._honey) return;
    var from = src();
    var lead = { name: data.name, email: data.email, school: data.school, role: data.role, contact: data.wechat,
                 kind: 'recording', program: 'ISB parent talk recording', lang: ZH ? 'zh' : 'en', src: from, page: location.pathname };
    var btn = form.querySelector('.cf-submit');
    form.classList.add('is-loading'); btn.disabled = true; setStatus('');
    post('/api/subscribe', { email: data.email, role: data.role, lang: ZH ? 'zh' : 'en', source: ('recording: ' + from).slice(0, 60), page: location.pathname, quiet: true })
      .catch(function (err) { console.warn('[recording] newsletter', err && err.message); });
    var mail = { name: data.name, email: data.email, school: data.school, role: data.role, wechat: data.wechat, source: from,
                 _subject: data._subject, _template: 'box', _captcha: 'false' };
    Promise.allSettled([post(form.getAttribute('action'), mail), post('/api/interest', lead)]).then(function (res) {
      form.classList.remove('is-loading'); btn.disabled = false;
      res.forEach(function (r) { if (r.status === 'rejected') console.warn('[recording]', r.reason && r.reason.message); });
      if (!res.some(function (r) { return r.status === 'fulfilled'; })) {
        setStatus(ZH ? '提交失败。请发送邮件至 contact@arenaschool.org，我们会尽快回复。' : 'Something went wrong. Please email contact@arenaschool.org and we will reply right away.', 'error');
        return;
      }
      remember();
      unlock(true);
    });
  });
})();
