/* phone.js: behavior for the phone layer (phone.css). Does nothing above 760px.
   1. Bottom action bar, built from the hero's primary button; shown once that button scrolls away.
   2. (Retired Oct 16: the nav is plain CSS sticky; nothing hides it on scroll.)
   3. Orphans: the last two words (English) or last few characters (Chinese) of headings and short
      paragraphs are kept together with a phone-only no-break span.
   4. Footer "All programs" row opens the menu. */
(function(){
  var mq=window.matchMedia('(max-width:760px)');
  if(!mq.matches)return;
  var doc=document.documentElement,zh=(doc.lang||'').indexOf('zh')===0;

  /* ---- 1. bottom bar ---- */
  var heroBtn=document.querySelector('main section.hero .btn-primary, main section.hero-riso .btn-primary')||document.querySelector('main .pp-final .btn-primary, main .pp-close-cta .btn-primary');
  var heroTrigger=document.querySelector('main section.hero, main section.hero-riso');
  var bar=null;
  if(heroBtn){
    bar=document.createElement('div');bar.className='ph-bar';bar.setAttribute('data-phone','');
    if(/^#/.test(heroBtn.getAttribute('href')||'')){var alt=[].find.call(heroBtn.parentElement.querySelectorAll('a.btn'),function(x){return !/^#/.test(x.getAttribute('href')||'#')});heroBtn=alt||heroBtn}
    var a=document.createElement('a');a.className='ph-bar-btn';a.href=heroBtn.getAttribute('href');
    a.textContent=(heroBtn.childNodes[0]&&heroBtn.childNodes[0].nodeType===3?heroBtn.childNodes[0].nodeValue:heroBtn.textContent).replace(/[→›]/g,'').trim();
    bar.appendChild(a);document.body.appendChild(bar);
    var heroGone=false,endSeen=false,typing=false;
    var ends=[].slice.call(document.querySelectorAll('.pp-final, .partners-grid, .ph-foot, .pg-enroll-form, form'));
    function upd(){var on=heroGone&&!endSeen&&!typing;bar.classList.toggle('on',on);doc.style.setProperty('--ph-barh',on?'72px':'0px')}
    var trig=(heroBtn.closest('section.hero, section.hero-riso'))?heroBtn:(heroTrigger||heroBtn);
    new IntersectionObserver(function(es){heroGone=!es[0].isIntersecting&&es[0].boundingClientRect.top<0;upd()}).observe(trig);
    var vis=new Set();
    var io=new IntersectionObserver(function(es){es.forEach(function(e){e.isIntersecting?vis.add(e.target):vis.delete(e.target)});endSeen=vis.size>0;upd()},{rootMargin:'0px 0px 0px 0px'});
    ends.forEach(function(e){io.observe(e)});
    document.addEventListener('focusin',function(e){if(/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)){typing=true;upd()}});
    document.addEventListener('focusout',function(){typing=false;setTimeout(upd,50)});
  }

  /* ---- 2. nav: plain CSS position:sticky (pro.css); no hide/show on scroll (RES-BRIEF, Oct 16) ---- */

  /* ---- 3. orphans ---- */
  var CJK=/[㐀-鿿]/;
  function lastText(el){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT,{acceptNode:function(n){return n.nodeValue.trim()&&!n.parentElement.closest('.sr-only,svg,[aria-hidden="true"] .hr-rot,.hr-rot')?1:3}}),n,last=null;while(n=w.nextNode())last=n;return last}
  function glue(el){
    if(el.dataset.phNb||el.closest('.ph-bar,.ph-foot,nav,a,button,label,.btn'))return;var t=lastText(el);if(!t)return;
    var par=t.parentElement;if(par.closest('a,button,label,.btn'))return;var pd=getComputedStyle(par).display;if(/flex|grid/.test(pd))return;
    var v=t.nodeValue.replace(/\s+$/,''),cut;
    if(CJK.test(v)){var core=v.replace(/[。，、；：！？”’）》.,!?]+$/,'');var k=Math.max(0,core.length-3);cut=k}
    else{var m=v.match(/(\S+\s+\S+)$/);if(!m)return;cut=v.length-m[1].length;if(m[1].length>24)return}
    if(cut<=0&&t.previousSibling==null&&t.parentElement===el)return;
    var keep=v.slice(cut),head=v.slice(0,cut),tail=t.nodeValue.slice(v.length);
    var sp=document.createElement('ph-nb');sp.className='nb';sp.textContent=keep;
    var p=t.parentNode;p.insertBefore(document.createTextNode(head),t);p.insertBefore(sp,t);if(tail)p.insertBefore(document.createTextNode(tail),t);p.removeChild(t);
    el.dataset.phNb='1';
  }
  document.querySelectorAll('main h1, main h2, main h3, main .lede, main .sec-head p, main .pc-intro, main p').forEach(function(el){
    if(el.tagName==='P'&&(el.textContent||'').length>420)return;glue(el)});

  /* ---- 5. no hover on phones: drop every :hover style rule and block mouse-hover listeners ----
     Phones have no hover (iOS also leaves a "sticky" hover after a tap), and the user wants the phone
     version to behave the same under a mouse in the preview. Clicks/taps still work normally. */
  function splitSel(sel){var out=[],d=0,cur='';for(var i=0;i<sel.length;i++){var c=sel[i];if(c==='('||c==='[')d++;else if(c===')'||c===']')d--;if(c===','&&d===0){out.push(cur);cur=''}else cur+=c}out.push(cur);return out}
  function strip(list){for(var i=list.length-1;i>=0;i--){var r=list[i];
    if(r.cssRules&&!r.selectorText){strip(r.cssRules);continue}
    if(r.selectorText&&r.selectorText.indexOf(':hover')>-1){var keep=splitSel(r.selectorText).filter(function(x){return x.indexOf(':hover')<0});
      try{if(keep.length)r.selectorText=keep.join(',');else (r.parentRule||r.parentStyleSheet).deleteRule(i)}catch(e){}}}}
  [].forEach.call(document.styleSheets,function(sh){try{strip(sh.cssRules)}catch(e){}});
  ['mouseenter','mouseover','mouseleave','mouseout','mousemove','pointerenter','pointerover','pointerleave','pointerout'].forEach(function(t){
    window.addEventListener(t,function(e){if(e.pointerType==='touch')return;e.stopImmediatePropagation()},true)});
  mq.addEventListener&&mq.addEventListener('change',function(e){if(!e.matches)location.reload()});

  /* ---- 6. About: per-founder anchors (#jing-jing-yang, #phillip-an) so phone rows land on the right bio ---- */
  var fs=document.querySelectorAll('.pg-founders .pg-founder'),ids=['jing-jing-yang','phillip-an'];
  if(fs.length===2){fs.forEach(function(f,i){if(!f.id)f.id=ids[i]});
    var h=location.hash.slice(1);if(ids.indexOf(h)>-1){var go=function(){var el=document.getElementById(h);if(el)window.scrollTo({top:el.getBoundingClientRect().top+window.scrollY-72,behavior:'instant'})};go();window.addEventListener('load',function(){setTimeout(go,60)})}}

  /* ---- 4. footer: All programs opens the menu ---- */
  document.querySelectorAll('a[href="#ph-menu"]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();e.stopImmediatePropagation();e.stopPropagation();
    var t=document.getElementById('navToggle');window.scrollTo({top:0,behavior:'instant'});doc.classList.remove('ph-nav-hide');
    setTimeout(function(){if(t&&!doc.classList.contains('nav-open'))t.click();
      setTimeout(function(){var g=document.querySelector('.nav-dd .nav-dd-btn');if(g&&g.getAttribute('aria-expanded')!=='true')g.click()},80)},50)},true)});
})();
