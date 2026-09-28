/* One-page overview form (program pages).
   On submit: email the team (FormSubmit) and alert Slack (/api/interest) in parallel.
   Either one succeeding counts; then the download unlocks. Download links live in the
   success panel (.pp-lead-dl); with none, visitors are told it's emailed. */
(function () {
  function collect(form) {
    var data = {};
    form.querySelectorAll('input[name], select[name]').forEach(function (el) { data[el.name] = (el.value || '').trim(); });
    data.page = location.pathname;
    return data;
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
  function wire(form) {
    var status = form.querySelector('.cf-status');
    var done = form.parentElement.querySelector('.pp-lead-done');
    var setStatus = function (msg, kind) { if (status) { status.textContent = msg; status.className = 'cf-status' + (kind ? ' cf-status-' + kind : ''); } };
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = collect(form);
      if (data._honey) return;
      var btn = form.querySelector('.cf-submit');
      form.classList.add('is-loading'); if (btn) btn.disabled = true; setStatus('');
      Promise.allSettled([post(form.getAttribute('action'), data), post('/api/interest', data)]).then(function (res) {
        form.classList.remove('is-loading'); if (btn) btn.disabled = false;
        var anyOk = res.some(function (r) { return r.status === 'fulfilled'; });
        res.forEach(function (r) { if (r.status === 'rejected') console.warn('[onepager]', r.reason && r.reason.message); });
        if (!anyOk) {
          setStatus('Something went wrong. Please email contact@arenaschool.org and we will send it right away.', 'error');
          return;
        }
        // Downloads are the links in the success panel; a data-download on the form overrides the first.
        var url = form.getAttribute('data-download') || '';
        var links = done ? [].slice.call(done.querySelectorAll('.pp-lead-dl')) : [];
        if (url && links[0]) links[0].href = url;
        var ready = links.filter(function (l) { var h = l.getAttribute('href') || ''; return h && h !== '#'; });
        links.forEach(function (l) { l.hidden = ready.indexOf(l) < 0; });
        var later = done && done.querySelector('.pp-lead-later');
        if (later) later.hidden = ready.length > 0;
        form.hidden = true; if (done) { done.hidden = false; done.focus(); }
      });
    });
  }
  document.querySelectorAll('form.pp-lead-form').forEach(wire);
})();
