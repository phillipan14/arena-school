/* ============================================================
   Arena — riso-interact.js  (design system: interactive graphics)
   Sequences (timeline, week overview, steps, milestones, rhythm, daily
   cascade) are explorable: hover, focus or tap a point to spotlight it
   and read what it means (item's data-detail).
   - Horizontal tracks: one detail panel under the track, fixed height,
     starts on the first point, text cross-fades (no layout jumps).
   - Vertical lists: the detail opens softly under the item.
   Motion is deliberately quiet: no sliding, only color and a fade.
   Curriculum icons draw in and act out their idea once, and on hover.
   ============================================================ */
(function () {
  'use strict';
  var CN = /^zh/i.test(document.documentElement.lang || '') || /-cn(\.html)?$/.test(location.pathname);
  var HINT = CN ? '悬停或轻点任一节点，查看详情' : 'Hover or tap any point to see what it means';
  var GROUPS = [
    { box: '.timeline', item: '.tl-row', mode: 'panel', key: ['.tl-day', '.tl-title'], desc: '.tl-desc' },
    { box: '.week-track', item: '.structure-row', mode: 'panel', key: ['.rtitle'], desc: '.rbody' },
    { box: '.fp-ladder-track', item: '.fp-rung', mode: 'panel', key: ['.fp-rung-title'] },
    { box: '.fp-rhythm-track', item: '.fp-rhythm-node', mode: 'panel', key: ['.fp-rhythm-label'] },
    { box: '.cascade-list', item: '.cascade-row', mode: 'inline', body: '.cr-text' }
  ];
  var hoverable = window.matchMedia && window.matchMedia('(hover: hover)').matches;

  function txt(it, sels) {
    return sels.map(function (s) { var e = it.querySelector(s); return e ? e.textContent.trim() : ''; }).filter(Boolean).join(' · ');
  }

  function setup(box, g) {
    if (box.__rx) return; box.__rx = true;
    var items = [].slice.call(box.querySelectorAll(g.item));
    if (!items.length) return;
    box.classList.add('rx-group', 'rx-mode-' + g.mode);
    if (items.length > 1) {
      var hint = document.createElement('p'); hint.className = 'rx-hint'; hint.textContent = HINT;
      var anchor = g.mode === 'inline' && g.item === '.structure-row' ? items[0] : box; anchor.parentNode.insertBefore(hint, anchor);
    }
    var panel = null;
    if (g.mode === 'panel') {
      panel = document.createElement('div'); panel.className = 'rx-panel'; panel.setAttribute('aria-live', 'polite');
      panel.innerHTML = '<div class="rx-panel-in"><span class="rx-panel-k"></span><div class="rx-panel-d"></div><p class="rx-panel-t"></p></div>';
      box.parentNode.insertBefore(panel, box.nextSibling);
    }
    items.forEach(function (it, i) {
      it.classList.add('rx-item'); it.style.setProperty('--rx-i', i);
      it.setAttribute('tabindex', '0'); it.setAttribute('aria-expanded', 'false');
      var d = it.getAttribute('data-detail');
      if (g.mode === 'inline' && d) {
        var host = (g.body && it.querySelector(g.body)) || (it.querySelector('.rbody') && it.querySelector('.rbody').parentNode) || it;
        var x = document.createElement('div'); x.className = 'rx-detail';
        x.innerHTML = '<div class="rx-detail-in"><p></p></div>'; x.querySelector('p').textContent = d;
        host.appendChild(x);
      }
      function on() { activate(i); }
      if (hoverable) it.addEventListener('pointerenter', on);
      it.addEventListener('focus', on);
      it.addEventListener('click', function () { if (g.mode === 'inline' && !hoverable && it.classList.contains('is-active')) clear(); else activate(i); });
      it.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); (items[i + 1] || it).focus(); }
        if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); (items[i - 1] || it).focus(); }
        if (e.key === 'Escape' && g.mode === 'inline') { clear(); it.blur(); }
      });
    });
    // inline lists close when the pointer leaves; panels keep the last point shown
    if (hoverable && g.mode === 'inline') box.addEventListener('pointerleave', function () { if (!box.contains(document.activeElement)) clear(); });
    var current = -1, swapT = 0;
    function activate(n) {
      if (n === current) return; current = n;
      box.classList.add('has-active');
      items.forEach(function (it, i) {
        it.classList.toggle('is-active', i === n); it.classList.toggle('is-past', i < n);
        it.setAttribute('aria-expanded', i === n ? 'true' : 'false');
      });
      box.style.setProperty('--rx-n', n); box.style.setProperty('--rx-count', items.length);
      if (panel) {
        var it = items[n], desc = g.desc && it.querySelector(g.desc);
        panel.classList.add('is-swapping'); clearTimeout(swapT);
        swapT = setTimeout(function () {
          panel.querySelector('.rx-panel-k').textContent = txt(it, g.key || []);
          panel.querySelector('.rx-panel-d').innerHTML = desc ? desc.innerHTML : '';
          panel.querySelector('.rx-panel-t').textContent = it.getAttribute('data-detail') || '';
          panel.classList.remove('is-swapping');
        }, 140);
      }
    }
    function clear() {
      current = -1; box.classList.remove('has-active');
      items.forEach(function (it) { it.classList.remove('is-active', 'is-past'); it.setAttribute('aria-expanded', 'false'); });
    }
    if (panel) {   // reserve exactly the tallest item's height: no jumping, no empty space
      var pin = panel.querySelector('.rx-panel-in'), k = panel.querySelector('.rx-panel-k'), dd = panel.querySelector('.rx-panel-d'), tt = panel.querySelector('.rx-panel-t'), mx = 0;
      function fit() { pin.style.minHeight = ''; mx = 0;
        items.forEach(function (it) { var d0 = g.desc && it.querySelector(g.desc);
          k.textContent = txt(it, g.key || []); dd.innerHTML = d0 ? d0.innerHTML : ''; tt.textContent = it.getAttribute('data-detail') || '';
          mx = Math.max(mx, pin.offsetHeight); });
        pin.style.minHeight = mx + 'px'; var c = current; current = -1; activate(c < 0 ? 0 : c); }
      fit(); window.addEventListener('resize', function () { clearTimeout(panel.__rt); panel.__rt = setTimeout(fit, 200); });
    } else if (g.mode === 'panel') activate(0);
  }

  /* numbered steps elsewhere (.structure-row outside a .week-track) stay vertical, detail opens in place */
  function setupStructure() {
    var seen = [];
    [].forEach.call(document.querySelectorAll('.structure-row'), function (row) {
      var p = row.parentNode; if (p.__rx || seen.indexOf(p) >= 0) return; seen.push(p);
      p.classList.add('rx-steps-box');
      setup(p, { item: '.structure-row', mode: 'inline' });
    });
  }

  /* curriculum icons: draw in when first seen, act out their meaning once, then again on hover */
  function setupIcons() {
    var icons = [].slice.call(document.querySelectorAll('svg.ic'));
    icons.forEach(function (ic) {
      var host = ic.closest('a, .cascade-row, .principle-head, .principle, .glance-card') || ic.parentNode;
      host.classList.add('ic-host');
    });
    if (!('IntersectionObserver' in window)) { icons.forEach(function (ic) { ic.classList.add('ic-in'); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; var ic = e.target; io.unobserve(ic);
        ic.classList.add('ic-in');
        setTimeout(function () { ic.classList.add('ic-play'); setTimeout(function () { ic.classList.remove('ic-play'); }, 2400); }, 900);
      });
    }, { threshold: 0.5 });
    icons.forEach(function (ic) { io.observe(ic); });
  }

  function boot() {
    setupIcons();
    GROUPS.forEach(function (g) { [].forEach.call(document.querySelectorAll(g.box), function (b) { setup(b, g); }); });
    setupStructure();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();

/* homepage gallery: clips play only while visible */
(function () {
  var vids = document.querySelectorAll('.gal-tile video'); if (!vids.length || !('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.preload = 'auto'; e.target.play().catch(function () {}); } else e.target.pause(); }); }, { threshold: 0.2 });
  [].forEach.call(vids, function (v) { io.observe(v); });
})();
