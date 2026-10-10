<script>
if(!matchMedia('(max-width:700px)').matches)[].forEach.call(document.querySelectorAll('video'),function(v){v.preload='auto'});
if(/[?&]read\b/.test(location.search))document.documentElement.classList.add('noqr');
/* navigation: dot nav, arrow keys, agenda links */
var deck=document.getElementById('deck'),S=[].slice.call(document.querySelectorAll('.s')),nav=document.getElementById('nav');
S.forEach(function(s,i){var a=document.createElement('a');a.href='#';a.setAttribute('aria-label','Slide '+(i+1));a.onclick=function(e){e.preventDefault();go(i)};nav.appendChild(a)});
function cur(){var y=deck.scrollTop+innerHeight/2;for(var i=0;i<S.length;i++){if(S[i].offsetTop+S[i].offsetHeight>y)return i}return S.length-1}
function go(i){i=Math.max(0,Math.min(S.length-1,i));deck.scrollTo({top:S[i].offsetTop,behavior:'smooth'})}
[].forEach.call(document.querySelectorAll('[data-go]'),function(a){a.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();go(+a.dataset.go)})});
deck.addEventListener('scroll',function(){var c=cur();[].forEach.call(nav.children,function(a,i){a.classList.toggle('on',i===c)})});
addEventListener('keydown',function(e){if(e.target.closest&&e.target.closest('.rv,.step,[data-go]')&&(e.key===' '||e.key==='Enter'))return;
 if(['ArrowDown','ArrowRight','PageDown',' '].indexOf(e.key)>=0){e.preventDefault();go(cur()+1)}if(['ArrowUp','ArrowLeft','PageUp'].indexOf(e.key)>=0){e.preventDefault();go(cur()-1)}});
nav.children[0].classList.add('on');
/* entrance + stat count-up */
var still=function(){var h=document.documentElement.classList;return h.contains('export')||h.contains('still')||matchMedia('(prefers-reduced-motion: reduce)').matches};
function countUp(s){if(still())return;[].forEach.call(s.querySelectorAll('.count'),function(el){if(el.dataset.done)return;el.dataset.done=1;
 var t=el.textContent,m=t.match(/^(\D*)(\d+(?:\.\d+)?)(.*)$/);if(!m)return;var to=parseFloat(m[2]),dec=(m[2].split('.')[1]||'').length,t0=0;
 el.style.minWidth=el.offsetWidth+'px';
 (function f(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/900),e=1-Math.pow(1-p,3);el.textContent=m[1]+(to*e).toFixed(dec)+m[3];if(p<1)requestAnimationFrame(f);else el.textContent=t})(performance.now())})}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');setTimeout(function(){countUp(e.target)},350)}})},{threshold:.35});
S.forEach(function(s){io.observe(s)});
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
 S.forEach(function(s){var w=s.querySelector('.w');if(!w)return;var kids=[].slice.call(w.children);
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
