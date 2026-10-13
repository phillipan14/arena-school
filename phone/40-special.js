/* 40-special.js: phone-only DOM for the special pages (see 40-special.css). Does nothing above 760px.
   1. Conferences "three tracks": a segmented control above the tracks, one track shown at a time.
   2. Bootcamp week on Chinese pages: "Day 01" labels read 第1天.
   3. Portfolio: each extra sample site card gets its address as a title (data-url);
      the notes' accordion headers become plain rows (nothing expands on phones). */
(function(){
  if(!matchMedia('(max-width:760px)').matches)return;
  var zh=(document.documentElement.lang||'').indexOf('zh')===0;

  /* 1. segmented control */
  var SEG=zh?['课堂实践','教学评估','管理者与家长']:['Classroom','Assessment','Leadership'];
  document.querySelectorAll('main.pc-conf .cf-cols').forEach(function(box){
    var cols=[].slice.call(box.querySelectorAll(':scope > .cf-col'));if(cols.length<2)return;
    var seg=document.createElement('div');seg.className='ph-seg';seg.setAttribute('role','tablist');seg.setAttribute('data-phone','');
    seg.setAttribute('aria-label',zh?'选择方向':'Choose a track');
    var btns=cols.map(function(col,i){
      var h=col.querySelector('h3');var b=document.createElement('button');b.type='button';b.setAttribute('role','tab');
      b.textContent=SEG[i]||(h?h.textContent:String(i+1));if(h)b.setAttribute('aria-label',h.textContent.trim());
      col.id=col.id||('ph-track-'+i);col.setAttribute('role','tabpanel');b.setAttribute('aria-controls',col.id);
      b.addEventListener('click',function(){pick(i)});seg.appendChild(b);return b});
    function pick(n){cols.forEach(function(c,i){c.classList.toggle('ph-on',i===n)});btns.forEach(function(b,i){b.setAttribute('aria-selected',String(i===n))})}
    box.classList.add('ph-segd');box.parentNode.insertBefore(seg,box);pick(0);
    /* keep the section the same height whichever track is open, so the page never jumps */
    function fit(){box.style.minHeight='';var m=0;cols.forEach(function(c){var on=c.classList.contains('ph-on');c.classList.add('ph-on');m=Math.max(m,c.offsetHeight);if(!on)c.classList.remove('ph-on')});box.style.minHeight=''}
    fit();window.addEventListener('resize',fit);if(document.fonts)document.fonts.ready.then(fit);
  });

  /* 2. week labels: "Day 01" reads "Day 1" (EN) and 第1天 (CN) */
  document.querySelectorAll('body.pg-bootcamp #week .pg-seq small').forEach(function(s){
    var m=(s.textContent||'').match(/Day\s*0*(\d+)/i);if(m)s.textContent=zh?('第'+m[1]+'天'):('Day '+m[1])});

  /* 3. portfolio */
  document.querySelectorAll('.sf-sample .pp-site-card').forEach(function(li){
    var u=li.querySelector('.pp-url'),m=li.querySelector('.pp-site-meta');if(u&&m)m.setAttribute('data-url',u.textContent.trim())});
  document.querySelectorAll('.sf-sample .pp-hover-hint').forEach(function(h){h.textContent=zh?'左右滑动查看更多网站 →':'Swipe to see more sites →'});
  document.querySelectorAll('.sf-sample .sf-note-h').forEach(function(h){h.setAttribute('tabindex','-1');h.removeAttribute('aria-expanded')});
})();
