<script>
/* player: every screen shows the real 1920×1080 slide, scaled uniformly and letterboxed. The page loads itself
   into a fixed 1920×1080 frame (?stage), so vw, vh, and media queries resolve exactly as on desktop and in the PDF. */
(function(){var H=document.documentElement;if(!H.classList.contains('player'))return;
 var f=document.getElementById('frame'),st=document.getElementById('stage'),ph=document.querySelector('.phint'),q=location.search.replace(/^\?/,'');
 f.src=location.pathname+'?stage'+(q?'&'+q:'')+location.hash;
 function fw(){try{return f.contentWindow.__step?f.contentWindow:null}catch(e){return null}}
 function fit(){var v=window.visualViewport,W=innerWidth,Hh=innerHeight,s=Math.min(W/1920,Hh/1080);
  f.style.transform='translate(-50%,-50%) scale('+s+')';window.__ps=s;
  /* no letterbox above or below for the language pill: stand it in the side letterbox if the upright pill (about 40px) fits there,
     otherwise dock it in the slide's right margin, clear of the corner logo */
  var band=(Hh-1080*s)/2,side=(W-1920*s)/2,low=band<45;H.classList.toggle('side',low&&side>=56);H.classList.toggle('dock',low&&side<56);
  H.style.setProperty('--ps',s);H.style.setProperty('--pk',Math.max(s,.8));H.style.setProperty('--band',band+'px');H.style.setProperty('--side',side+'px');
  ph.classList.toggle('on',matchMedia('(pointer:coarse)').matches&&(Hh-1080*s)/2>=48);
  var w=fw();if(w){w.__ps=s;w.document.documentElement.classList.toggle('tiny',s<.6)}}
 f.addEventListener('load',function(){fit();try{f.contentWindow.focus()}catch(e){}});
 fit();addEventListener('resize',fit);addEventListener('orientationchange',function(){setTimeout(fit,120)});
 addEventListener('keydown',function(e){var w=fw();if(!w)return;
  if(['ArrowDown','ArrowRight','PageDown',' '].indexOf(e.key)>=0){e.preventDefault();w.__step(1)}if(['ArrowUp','ArrowLeft','PageUp'].indexOf(e.key)>=0){e.preventDefault();w.__step(-1)}});
 /* swipes and taps on the letterbox around the slide */
 var t0=null;st.addEventListener('touchstart',function(e){t0=e.touches.length===1?{x:e.touches[0].clientX,y:e.touches[0].clientY}:null},{passive:true});
 st.addEventListener('touchend',function(e){if(!t0)return;var t=e.changedTouches[0],dx=t.clientX-t0.x,dy=t.clientY-t0.y,w=fw();t0=null;
  if(!w||(window.visualViewport&&visualViewport.scale>1.05))return;
  var d=Math.abs(dx)>Math.abs(dy)?dx:dy;if(Math.abs(d)>30)w.__step(d<0?1:-1);else w.__step(t.clientX>innerWidth/3?1:-1)});
})();
if(!document.documentElement.classList.contains('player')&&!matchMedia('(max-width:700px)').matches)[].forEach.call(document.querySelectorAll('video'),function(v){v.preload='auto'});
if(/[?&]read\b/.test(location.search))document.documentElement.classList.add('noqr');
if(/[?&]notes\b/.test(location.search))document.documentElement.classList.add('shownotes');
/* navigation: dot nav, arrow keys, agenda links */
var deck=document.getElementById('deck'),S=[].slice.call(document.querySelectorAll('.s')),nav=document.getElementById('nav');
S.forEach(function(s,i){var a=document.createElement('a');a.href='#';a.setAttribute('aria-label','Slide '+(i+1));a.onclick=function(e){e.preventDefault();go(i)};nav.appendChild(a)});
function cur(){var y=deck.scrollTop+innerHeight/2;for(var i=0;i<S.length;i++){if(S[i].offsetTop+S[i].offsetHeight>y)return i}return S.length-1}
/* with motion on, moving between slides is choreographed rather than scrolled (css/s60-motion.css), with nothing but opacity and
   transform so a phone composites every frame: the slide's content fades out, the deck jumps, and the next slide's content settles in.
   Going into a navy chapter slide, a navy panel rises over the page first; leaving one, the panel lifts away.
   Only one move runs at a time. A new press finishes the current jump immediately (no stacked curtains or half-fades),
   then starts the next. Images are decoded up front so the arriving slide never paints empty. */
var gT=[],moving=false,dest=-1;
function land(i){if(i<0||i>=S.length)return;deck.scrollTop=S[i].offsetTop;S[i].classList.add('in');warmSlide(i);warmSlide(i+1)}
function finishMove(){gT.forEach(function(t){clearTimeout(t)});gT=[];[].forEach.call(document.querySelectorAll('.curtain'),function(c){c.remove()});S.forEach(function(s){s.classList.remove('out')});if(dest>=0)land(dest);dest=-1;moving=false}
function go(i){i=Math.max(0,Math.min(S.length-1,i));var H=document.documentElement;
 if(!H.classList.contains('motion')){deck.scrollTo({top:S[i].offsetTop,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});return}
 if(moving)finishMove();
 var from=cur();if(from===i)return;
 moving=true;dest=i;var t=S[i],f=S[from],nv=function(s){return s.classList.contains('nv')};
 function jump(keep){var n=dest;dest=-1;moving=false;S.forEach(function(s){s.classList.remove('out')});if(!keep)[].forEach.call(document.querySelectorAll('.curtain'),function(c){c.remove()});if(n>=0)land(n)}
 function panel(cls){var c=document.createElement('div');c.className='curtain'+cls;document.body.appendChild(c);void c.offsetWidth;return c}
 f.classList.add('out');warmSlide(i);
 if(i>from&&nv(t)&&!nv(f)){var c=panel('');c.classList.add('up');gT.push(setTimeout(jump,680));return}
 if(i>from&&nv(f)&&!nv(t)){gT.push(setTimeout(function(){var c=panel(' on');jump(true);c.classList.add('lift');gT.push(setTimeout(function(){c.remove()},720))},220));return}
 gT.push(setTimeout(jump,i<from?150:t.matches('.st,.bq')?320:230))}
[].forEach.call(document.querySelectorAll('[data-go]'),function(a){a.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();go(+a.dataset.go)})});
/* builds: a slide reached with the keys opens on its title, and each press shows its next [data-s] step; back hides them again.
   Slides reached any other way (scroll, dots, agenda, export, phone, ?read) are always fully built. */
var B=S.map(function(s){return [].reduce.call(s.querySelectorAll('[data-s]'),function(m,e){return Math.max(m,+e.dataset.s)},0)}),armed=-1;
function canBuild(){return !document.documentElement.classList.contains('export')&&!/[?&]read\b/.test(location.search)&&!matchMedia('(max-width:700px)').matches}
function build(i,k,quiet){var s=S[i];s.dataset.k=k;if(quiet)s.classList.add('nt');s.classList.toggle('bld',k<B[i]);
 [].forEach.call(s.querySelectorAll('[data-s]'),function(e){e.classList.toggle('vis',+e.dataset.s<=k)});if(quiet){void s.offsetWidth;s.classList.remove('nt')}
 else if(window.__count)setTimeout(function(){__count(s)},150)}
function step(d){if(moving)finishMove();
 var c=armed>=0&&Math.abs(S[armed].offsetTop-deck.scrollTop)<innerHeight*.75?armed:cur();
 if(!canBuild()){go(c+d);return}
 var k=S[c].dataset.k===undefined?B[c]:+S[c].dataset.k;
 if(d>0){if(k<B[c]){build(c,k+1);return}if(c<S.length-1){armed=c+1;build(c+1,0,true);go(c+1)}}
 else{if(k>0){build(c,k-1);return}if(c>0){armed=c-1;build(c-1,B[c-1],true);go(c-1)}}}
deck.addEventListener('scroll',function(){var c=cur();[].forEach.call(nav.children,function(a,i){a.classList.toggle('on',i===c)});document.body.classList.toggle('nvon',S[c].classList.contains('nv'));
 if(armed>=0&&Math.abs(S[armed].offsetTop-deck.scrollTop)>innerHeight*1.5)armed=-1;
 S.forEach(function(s,j){if(j!==armed&&s.classList.contains('bld')&&Math.abs(s.offsetTop-deck.scrollTop)>=innerHeight)build(j,B[j],true)})},{passive:true});
window.__step=step;
addEventListener('keydown',function(e){if(document.documentElement.classList.contains('player'))return;if(e.target.closest&&e.target.closest('.rv,.step,[data-go]')&&(e.key===' '||e.key==='Enter'))return;
 if(['ArrowDown','ArrowRight','PageDown',' '].indexOf(e.key)>=0){e.preventDefault();step(1)}if(['ArrowUp','ArrowLeft','PageUp'].indexOf(e.key)>=0){e.preventDefault();step(-1)}});
nav.children[0].classList.add('on');document.body.classList.toggle('nvon',S[cur()].classList.contains('nv'));
/* touch, inside the player's frame: a swipe either way or a tap moves one step (left third of the slide goes back).
   The frame never scrolls by touch, so a slide never slides half away. Links, videos, and the agenda keep their own taps. */
if(self!==top&&matchMedia('(pointer:coarse)').matches){document.documentElement.classList.add('touch');var t0=null;
 deck.addEventListener('touchstart',function(e){t0=e.touches.length===1?{x:e.touches[0].clientX,y:e.touches[0].clientY}:null},{passive:true});
 deck.addEventListener('touchmove',function(e){var z=1;try{z=parent.visualViewport?parent.visualViewport.scale:1}catch(x){}if(z<1.05&&e.touches.length===1&&e.cancelable)e.preventDefault()},{passive:false});
 deck.addEventListener('touchend',function(e){if(!t0)return;var t=e.changedTouches[0],dx=t.clientX-t0.x,dy=t.clientY-t0.y,z=1,k=30/(window.__ps||1);t0=null;
  try{z=parent.visualViewport?parent.visualViewport.scale:1}catch(x){}if(z>1.05)return;
  var d=Math.abs(dx)>Math.abs(dy)?dx:dy;if(Math.abs(d)>k){step(d<0?1:-1);return}
  if(e.target.closest('a,button,video,[data-go],.rv,.step'))return;e.preventDefault();step(t.clientX>innerWidth/3?1:-1)},{passive:false})}
/* motion (see css/s60-motion.css): on only on screen, never for export, ?read, the player shell, or reduced motion.
   The HTML always holds the final text, so a counter or a split headline that never runs still reads correctly. */
var HM=document.documentElement;
if(!HM.classList.contains('player')&&!HM.classList.contains('export')&&!/[?&]read\b/.test(location.search)&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
 HM.classList.add('motion');
 new MutationObserver(function(){if(HM.classList.contains('export')&&HM.classList.contains('motion')){HM.classList.remove('motion');
  /* a transition already under way keeps running when its rule goes away, so jump every one to its end */
  if(document.getAnimations)document.getAnimations().forEach(function(a){try{a.finish()}catch(e){}})}}).observe(HM,{attributes:true,attributeFilter:['class']});
 /* hero headlines (statements, quotes, chapters, takeaways, the cover) build word by word in English and phrase by phrase in Chinese;
    content-slide titles rise as one block so they read at once */
 var HERO='.ae.st h2,.ae.bq h2,.ae.sec h2,.ae.tk h2,.cover h1';
 if(HM.lang==='en')[].forEach.call(document.querySelectorAll(HERO),function(h){var i=0;
  (function walk(n){[].slice.call(n.childNodes).forEach(function(c){
   if(c.nodeType===3){var f=document.createDocumentFragment();c.nodeValue.split(/(\s+)/).forEach(function(p){if(!p)return;
     if(/^\s+$/.test(p)){f.appendChild(document.createTextNode(p));return}var w=document.createElement('span');w.className='wd';w.style.setProperty('--i',i++);w.textContent=p;f.appendChild(w)});
    n.replaceChild(f,c)}else if(c.nodeType===1&&c.tagName!=='BR')walk(c)})})(h);h.classList.add('wsplit')});
 else [].forEach.call(document.querySelectorAll(HERO),function(h){var i=0;
  /* phrases stay inline (opacity only), so the Chinese line breaks are exactly those of the static slide */
  (function walk(n){[].slice.call(n.childNodes).forEach(function(c){
   if(c.nodeType===3){var f=document.createDocumentFragment();c.nodeValue.replace(/([，。、：；？！])/g,'$1\u0001').split('\u0001').forEach(function(p){if(!p)return;
     var w=document.createElement('span');w.className='phr';w.style.setProperty('--i',i++);w.textContent=p;f.appendChild(w)});
    n.replaceChild(f,c)}else if(c.nodeType===1&&c.tagName!=='BR')walk(c)})})(h);h.classList.add('psplit')});
}
[].forEach.call(document.querySelectorAll('.mmap'),function(g){[].forEach.call(g.querySelectorAll('.mm-c'),function(c,k){c.style.setProperty('--c',k)});[].forEach.call(g.querySelectorAll('.mm li'),function(c,k){c.style.setProperty('--i',k)})});
[].forEach.call(document.querySelectorAll('.tln,.apps,.tbl,.trk,.paths,.tk-prog,.pg-m,.trio,.proj,.agx,.spine'),function(g){
 [].slice.call(g.children).forEach(function(c,i){c.style.setProperty('--i',i);if(g.classList.contains('tbl'))[].forEach.call(c.children,function(x){x.style.setProperty('--i',i)})});
 if(g.classList.contains('pg-m')){var j=0;[].forEach.call(g.children,function(c){if(c.classList.contains('f'))c.style.setProperty('--i',j++)})}});
/* counters: the first number in each .big or .cnt counts up from zero, keeping its prefix, commas, decimals, and unit */
function firstNum(el){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);while(w.nextNode())if(/\d/.test(w.currentNode.nodeValue))return w.currentNode;return null}
function countUp(s){if(!HM.classList.contains('motion'))return;
 [].forEach.call(s.querySelectorAll('.big,.cnt'),function(el){if(el.dataset.run||el.classList.contains('nc')||(s.classList.contains('bld')&&el.closest('[data-s]:not(.vis)')))return;
  var t=firstNum(el);if(!t)return;var full=t.nodeValue,m=full.match(/^([^\d]*)(\d[\d,]*(?:\.\d+)?)([\s\S]*)$/);if(!m)return;
  var raw=m[2],to=parseFloat(raw.replace(/,/g,'')),dec=(raw.split('.')[1]||'').length,cm=raw.indexOf(',')>=0,t0=0,D=to>=1000?1500:1200;
  el.dataset.run=1;el.style.minWidth=getComputedStyle(el).width;
  requestAnimationFrame(function f(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/D),v=to*(1-Math.pow(1-p,4));
   if(p>=1||!HM.classList.contains('motion')){t.nodeValue=full;el.style.minWidth='';return}
   t.nodeValue=m[1]+(cm?Math.round(v).toLocaleString('en-US'):v.toFixed(dec))+m[3];requestAnimationFrame(f)})})}
window.__count=countUp;
var io=new IntersectionObserver(function(es){es.forEach(function(e){var s=e.target;
 if(e.intersectionRatio>=.35){if(!s.classList.contains('in')){s.classList.add('in');setTimeout(function(){countUp(s)},420)}}
 else if(!e.isIntersecting&&HM.classList.contains('motion')){s.classList.remove('in');[].forEach.call(s.querySelectorAll('[data-run]'),function(x){delete x.dataset.run})}})},{threshold:[0,.35]});
S.forEach(function(s){io.observe(s)});
/* decode every slide image (and the next slide's) so a transition never paints an empty box */
function warmSlide(i){if(i<0||i>=S.length)return;[].forEach.call(S[i].querySelectorAll('img[src]'),function(img){
  if(img.decode)img.decode().catch(function(){});else{var x=new Image();x.src=img.currentSrc||img.src}})}
function warmAll(){S.forEach(function(_,i){warmSlide(i)})}
if(document.readyState==='complete')warmAll();else addEventListener('load',warmAll);
if(document.fonts)document.fonts.ready.then(warmAll);
</script><script>
/* detail on demand: hover, click, or Enter/Space opens the detail inside its own card; Esc closes */
(function(){var R=[].slice.call(document.querySelectorAll('.rv'));
function set(el,o){el.classList.toggle('open',o);el.setAttribute('aria-expanded',o?'true':'false')}
function close(ex){R.forEach(function(x){if(x!==ex)set(x,false)})}
R.forEach(function(el){
 el.addEventListener('click',function(e){e.stopPropagation();var o=!el.classList.contains('open');close(el);set(el,o);el.classList.toggle('shut',!o)});
 el.addEventListener('pointerleave',function(){el.classList.remove('shut')});
 el.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();el.click()}if(e.key==='Escape'){close();el.blur()}})});
document.addEventListener('click',function(){close()});addEventListener('keydown',function(e){if(e.key==='Escape')close()});
var last=0;deck.addEventListener('scroll',function(){var c=cur();if(c!==last){last=c;close()}},{passive:true});
window.__close=close})();
/* steps: the line fills to the active step; its text shows in a panel that follows it */
(function(){[].forEach.call(document.querySelectorAll('.steps'),function(g){
 var st=[].slice.call(g.querySelectorAll('.step')),sd=[].slice.call(g.querySelectorAll('.sd')),fill=g.querySelector('.rail i'),panel=g.querySelector('.step-panel'),pin=0,n=st.length;
 function show(i){st.forEach(function(x,j){x.classList.toggle('on',j===i);x.classList.toggle('done',j<i);x.setAttribute('aria-selected',j===i?'true':'false')});
  sd.forEach(function(x,j){x.classList.toggle('on',j===i)});fill.style.width=(i/(n-1)*100)+'%';
  var PW=50,c=(100/n)*(i+.5),L=Math.max(0,Math.min(100-PW,c-PW/2));panel.style.marginLeft=L+'%';panel.style.setProperty('--caret',((c-L)/PW*100)+'%')}
 st.forEach(function(x,i){x.addEventListener('pointerenter',function(){show(i)});x.addEventListener('click',function(e){e.stopPropagation();pin=i;show(i)});
  x.addEventListener('focus',function(){pin=i;show(i)});x.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();pin=i;show(i)}})});
 g.addEventListener('pointerleave',function(){show(pin)});show(0)})})();
</script>
<script>
/* layout: size each slide for its fully opened state, so opening a card never moves anything else,
   fit the screenshots to the height, then spread spare height into the gaps (type size never changes) */
(function(){
function lay(){var X=document.documentElement.classList.contains('export');if(matchMedia('(max-width:700px)').matches&&!X){[].forEach.call(document.querySelectorAll('#deck *'),function(e){if(e.style.minHeight)e.style.minHeight='';if(e.style.marginTop&&e.dataset&&e.dataset.mt!==undefined)e.style.marginTop='';if(e.style.marginBottom==='auto')e.style.marginBottom=''});return}
 S.forEach(function(s){var w=s.querySelector('.w');if(!w||s.classList.contains('ae'))return;var kids=[].slice.call(w.children);
  kids.forEach(function(k){k.style.marginTop='';k.style.marginBottom=''});w.style.minHeight='';w.style.paddingTop=w.style.paddingBottom='';
  var RG=[].slice.call(s.querySelectorAll('.pillars,.habits'));RG.forEach(function(g){[].forEach.call(g.children,function(c){c.style.minHeight=''})});
  var vx=s.querySelector('.vx');if(vx){vx.style.removeProperty('--vw');
   [].forEach.call(vx.querySelectorAll('.cmpcol'),function(c){var m=null,ml=-1;[].forEach.call(c.querySelectorAll('.mc'),function(x){x.classList.remove('mx');var l=x.textContent.length;if(l>ml){ml=l;m=x}});if(m)m.classList.add('mx')})}
  var st=s.querySelector('.stills');if(st)st.style.removeProperty('--iw');
  s.classList.add('measure');
  var Z=parseFloat(getComputedStyle(w).zoom)||1,avail=(innerHeight-(X?4:24))/Z;
  /* a dense slide may use the outer padding, but never the strip the key hint lives in */
  if(w.offsetHeight>avail){w.style.paddingTop=(X?26:22)/Z+'px';w.style.paddingBottom=(X?26:34)/Z+'px'}
  if(st){var gap=parseFloat(getComputedStyle(st).columnGap)||0,lo=160,hi=(st.clientWidth-gap)/2;
   if(w.offsetHeight>avail){for(var t=0;t<14;t++){var mid=(lo+hi)/2;st.style.setProperty('--iw',mid+'px');if(w.offsetHeight>avail)hi=mid;else lo=mid}st.style.setProperty('--iw',lo+'px')}
   var fg=st.querySelectorAll('figure');st.classList.toggle('wide',fg.length===2&&fg[1].offsetLeft-(fg[0].offsetLeft+fg[0].offsetWidth)>72)}
  if(vx){var fig=vx.querySelector('.vid'),col=vx.querySelector('.vcol'),best=38;
   var colH=function(){var k=[].slice.call(col.children),g=parseFloat(getComputedStyle(col).rowGap)||0;return k.reduce(function(a,c){return a+c.offsetHeight},0)+g*(k.length-1)};
   for(var f=72;f>=38;f--){vx.style.setProperty('--vw',f+'%');if(w.offsetHeight<=avail&&colH()<=fig.offsetHeight+2){best=f;break}}
   vx.style.setProperty('--vw',best+'%')}
  if(!s.classList.contains('split-s')&&!s.classList.contains('ask')){
   var hi2=kids.findIndex(function(k){return /^H[12]$/.test(k.tagName)||k.classList.contains('hd')});
   var after=hi2<0?[]:kids.slice(hi2+1).filter(function(k){return k.offsetHeight>0&&!k.classList.contains('take')});
   if(after.length){after.forEach(function(k){k.dataset.mt=parseFloat(getComputedStyle(k).marginTop)||0});
    var extra=avail*.9-w.offsetHeight;
    if(extra>4){var n=after.length>1?after.length-1:1,per=Math.min(extra/(n+.6),64);
     after.forEach(function(k,i){k.style.marginTop=(+k.dataset.mt+(i===0?Math.min(per,after.length>1?16:28):per))+'px'})}}}
  var H=w.offsetHeight;s.classList.remove('measure');
  /* reveal rows: closed cards share one height; an opened card grows below it, into room reserved above */
  if(!X)RG.forEach(function(g){var cs=[].slice.call(g.children),m=0;cs.forEach(function(c){var d=c.querySelector('.rv-d');m=Math.max(m,c.offsetHeight-(d?d.offsetHeight:0))});cs.forEach(function(c){c.style.minHeight=m+'px'})});
  if(!X){w.style.minHeight=H+'px';
   /* spare room (for opening) sits right after the last interactive block, so what follows stays put */
   /* ...unless what follows is a takeaway (11: the Cornell quote), which stays right under the cards and slides down as one opens (the spare room sits at the bottom) */
   for(var i=kids.length-1;i>=0;i--){if(kids[i].querySelector('.rv')){var rest=kids.slice(i+1).filter(function(k){return k.offsetHeight>0});
    if(rest.length&&!rest.every(function(k){return k.classList.contains('take')}))kids[i].style.marginBottom='auto';break}}}
 })}
lay();addEventListener('resize',lay);[].forEach.call(document.querySelectorAll('video'),function(v){v.addEventListener('loadedmetadata',lay,{once:true})});addEventListener('load',lay);if(document.fonts)document.fonts.ready.then(lay);window.__space=lay})();

/* walkthrough videos: play only while their slide is on screen; posters for reduced motion and print */
(function(){var V=[].slice.call(document.querySelectorAll('video')),H=document.documentElement,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
 V.forEach(function(v){if(rm){v.removeAttribute('autoplay');v.pause();v.controls=true}});
 var vio=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;
  if(e.isIntersecting&&e.intersectionRatio>=.5&&!rm&&!H.classList.contains('export')){var p=v.play();if(p&&p.catch)p.catch(function(){})}else v.pause()})},{threshold:[0,.5,1]});
 V.forEach(function(v){vio.observe(v)})})();
</script>
