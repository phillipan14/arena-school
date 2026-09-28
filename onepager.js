/* One-page overview form (program pages).
   On submit: email the team (FormSubmit) and alert Slack (/api/interest) in parallel.
   Either one succeeding counts; then the download unlocks. Set the PDF link on the
   form's data-download attribute; while it's empty, visitors are told it's emailed. */
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
        var url = form.getAttribute('data-download') || '';
        var link = done && done.querySelector('.pp-lead-dl');
        var later = done && done.querySelector('.pp-lead-later');
        if (link) { link.hidden = !url; if (url) link.href = url; }
        if (later) later.hidden = !!url;
        form.hidden = true; if (done) { done.hidden = false; done.focus(); }
      });
    });
  }
  document.querySelectorAll('form.pp-lead-form').forEach(wire);
})();
