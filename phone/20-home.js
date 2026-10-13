/* 20-home.js: homepage body components on phones (pairs with 20-home.css). Tap-only.
   1. Text links that become rows (program links, grade-map lanes, events, contact rows, section-end links):
      the trailing "→" glyph is set aside (kept in the DOM, hidden) and an iOS chevron is appended.
   2. Event rows: the round arrow becomes a chevron.
   3. Contact: the "What happens next" steps, email and LinkedIn rows read as grouped lists (CSS only). */
(function(){
  if(!matchMedia('(max-width:760px)').matches)return;
  if(!document.body.classList.contains('home'))return;
  var NS='http://www.w3.org/2000/svg';
  function chev(){var s=document.createElementNS(NS,'svg');s.setAttribute('viewBox','0 0 24 24');s.setAttribute('aria-hidden','true');s.setAttribute('class','ph-chev');
    var p=document.createElementNS(NS,'path');p.setAttribute('d','M9 5l7 7-7 7');s.appendChild(p);return s}
  function rowify(a){
    if(a.dataset.phRow)return;a.dataset.phRow='1';
    // hide a trailing arrow, whether it is a .arr span or the end of the last text node
    a.querySelectorAll('.arr').forEach(function(x){x.classList.add('ph-arr')});
    var n=a.lastChild;while(n&&n.nodeType===3&&!n.nodeValue.trim())n=n.previousSibling;
    if(n&&n.nodeType===3&&/\s*[→›]\s*$/.test(n.nodeValue)){
      var m=n.nodeValue.match(/^([\s\S]*?)(\s*[→›]\s*)$/);
      var t=document.createElement('span');t.className='ph-lt';t.textContent=m[1];
      var h=document.createElement('span');h.className='ph-arr';h.setAttribute('aria-hidden','true');h.textContent=m[2];
      a.replaceChild(h,n);a.insertBefore(t,h);
    }else{
      // wrap the label text so it can take the free width
      var kids=[].filter.call(a.childNodes,function(k){return !(k.nodeType===1&&k.classList.contains('ph-arr'))&&!(k.nodeType===1&&k.tagName.toLowerCase()==='svg')});
      if(kids.length){var w=document.createElement('span');w.className='ph-lt';a.insertBefore(w,kids[0]);kids.forEach(function(k){w.appendChild(k)})}
    }
    a.appendChild(chev());
  }
  document.querySelectorAll('#programs .prog-links a, #programs .gm-partner a, .pillars-more a, .hp-next .cf-ev .tlink, .partners-lede .hc-direct a').forEach(rowify);

  // events: the round arrow becomes a chevron
  document.querySelectorAll('.hp-next .cf-go').forEach(function(g){g.textContent='';g.appendChild(chev())});

  // pillars: no expanding panel on phones; each row links to its section of the approach page
  var appr=(document.querySelector('.pillars-more a')||{}).getAttribute?document.querySelector('.pillars-more a').getAttribute('href'):'/approach';
  document.querySelectorAll('.pillars [data-xp-card]').forEach(function(btn){
    var a=document.createElement('a');a.className=btn.className+' ph-pl-link';a.href=appr+'#'+btn.dataset.xpCard;
    while(btn.firstChild)a.appendChild(btn.firstChild);
    var plus=a.querySelector('.pl-plus');if(plus)plus.parentNode.replaceChild(chev(),plus);
    btn.parentNode.replaceChild(a,btn);
  });

  // Chinese: keep the last three characters of short step lines together (no 1 to 2 character last line)
  if((document.documentElement.lang||'').indexOf('zh')===0)document.querySelectorAll('.hc-steps li b, .hc-steps li div > span').forEach(function(el){
    var t=el.lastChild;if(!t||t.nodeType!==3)return;var v=t.nodeValue,core=v.replace(/[。，、；：！？.]+$/,''),k=Math.max(0,core.length-3);if(k<=0)return;
    var sp=document.createElement('ph-nb');sp.className='nb';sp.textContent=v.slice(k);t.nodeValue=v.slice(0,k);el.appendChild(sp)});

  // grade map lanes: chevron at the row end (the "→" em stays, hidden by CSS)
  document.querySelectorAll('.gmap .gm-lane').forEach(function(l){var c=chev();c.classList.add('gm-chev');l.appendChild(c)});

})();
