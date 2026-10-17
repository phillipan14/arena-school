/* Shared anonymous boards for Teacher Toolbox tools (feedback, exit tickets, polls, Q&A).
   Usage:  var fb = Board('exit-ticket');                       // board name: lowercase letters, digits, dashes
           fb.post('It was clear', 'thumbs-up').then(...);      // text (max 500 chars) + optional tag (max 40)
           fb.watch(function (items) { ... }, 3000);            // items newest first: {id, t, text, tag}
   Anonymous by design: never send names, emails, or anything that identifies a student. */
(function () {
  var API = '/api/board';
  window.Board = function (name) {
    var b = String(name || '').toLowerCase().replace(/[^a-z0-9-]/g, '-').slice(0, 40);
    function list() {
      return fetch(API + '?b=' + encodeURIComponent(b) + '&t=' + Date.now(), { cache: 'no-store' })
        .then(function (r) { return r.json(); })
        .then(function (d) { return d.ok ? d.items : []; })
        .catch(function () { return []; });
    }
    return {
      name: b,
      post: function (text, tag) {
        return fetch(API, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ b: b, text: text, tag: tag || '' }) })
          .then(function (r) { return r.json(); })
          .catch(function () { return { ok: false, error: 'No connection. Try again.' }; });
      },
      list: list,
      watch: function (cb, ms) {
        var stop = false;
        (function tick() { if (stop) return; list().then(function (items) { cb(items); setTimeout(tick, ms || 3000); }); })();
        return function () { stop = true; };
      }
    };
  };
})();
