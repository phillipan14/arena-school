/* Live updates for the ACAMIS Teacher Toolbox: when the room ships a change, every open page offers a refresh. */
(function () {
  var base = document.currentScript.src.replace(/live\.js.*$/, '');
  var seen = null;
  var hub = typeof window.onToolboxChange === 'function'; // the hub refreshes itself; tool pages offer a reload
  function lines(t) { return t.split('\n').filter(function (l) { return l.split('|').length >= 3; }); }
  function toast(line) {
    var p = line.split('|'), el = document.getElementById('live-toast');
    if (!el) {
      el = document.createElement('button'); el.id = 'live-toast'; el.type = 'button';
      el.setAttribute('style', 'position:fixed;left:16px;right:16px;bottom:20px;margin:0 auto;width:fit-content;max-width:560px;z-index:9999;' +
        'display:flex;align-items:center;gap:12px;padding:14px 20px;border:0;border-radius:999px;background:#0B1A4A;color:#fff;' +
        'font:600 16px/1.3 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;box-shadow:0 14px 30px -12px rgba(11,26,74,.55);cursor:pointer;text-align:left');
      el.onclick = function () { location.reload(); };
      document.body.appendChild(el);
    }
    el.innerHTML = '<span style="width:10px;height:10px;border-radius:50%;background:#7FD1A8;flex:none"></span>' +
      '<span>Just shipped: ' + (p[2] || 'an update').replace(/</g, '&lt;') + (hub ? '' : ' <u>Tap to refresh</u>') + '</span>';
    if (hub) { clearTimeout(el._t); el.style.display = 'flex'; el._t = setTimeout(function () { el.style.display = 'none'; }, 8000); }
  }
  function check() {
    fetch(base + 'changes.txt?t=' + Date.now(), { cache: 'no-store' }).then(function (r) { return r.text(); }).then(function (t) {
      var n = lines(t);
      if (seen === null) { seen = n.length; return; }
      if (n.length > seen) { toast(n[n.length - 1]); if (hub) { seen = n.length; window.onToolboxChange(t); } }
    }).catch(function () {});
  }
  check(); setInterval(check, 8000);
})();
