/* Phone reader for the parent-talk deck. See reader.css for the layout; build.py fills __TOOLS__ with the
   market-map tool list from shared.js so the two views never drift.
   One slide per screen, swiped sideways (native scroll-snap) or moved with the Next / Previous buttons and the keys.
   Each slide builds once, the first time it is reached; reduced motion shows every slide fully built. */
(function(){
var H=document.documentElement,deck=document.getElementById('deck'),S=[].slice.call(deck.querySelectorAll('.s')),N=S.length;
/* END: the closing slide (last one before the source appendix); Next there goes back to the talk's landing page */
var END=(function(){for(var j=N-1;j>=0;j--)if(!S[j].classList.contains('s-src'))return j;return N-1})();
var ZH=H.lang!=='en',KEY=ZH?'cn':'en',T=ZH?
 {next:'下一页',start:'开始',done:'返回首页',prev:'上一页',all:'全部幻灯片',close:'关闭',appx:'附录',intro:'开场',tip:'左右滑动或点“下一页”翻页',slide:'第{n}页'}:
 {next:'Next',start:'Start',done:'Back to start',prev:'Previous slide',all:'All slides',close:'Close',appx:'Appendix',intro:'Opening',tip:'Swipe or tap Next to turn the page',slide:'Slide {n}'};
var motion=!matchMedia('(prefers-reduced-motion: reduce)').matches;
var $=function(s,r){return (r||document).querySelector(s)};
var nx=$('.nx'),pv=$('.pv'),ctr=$('.ctr'),bar=$('.prog'),lng=$('.lng'),cue=$('.more-cue');

/* ---- sections: part titles from the navy chapter slides, so the counter can say where you are ---- */
var part=[],cur='';
S.forEach(function(s,i){
 if(s.classList.contains('sec')){var on=s.querySelector('.trk li.on b');cur=on?on.textContent.trim():''}
 if(s.classList.contains('s-src'))cur=T.appx;
 part[i]=cur||T.intro});
S.forEach(function(s,i){if(s.classList.contains('sec')){var t=document.createElement('b');t.style.left=(i/N*100)+'%';bar.appendChild(t)}});

/* ---- build units: every [data-s] step; a slide with none builds its body as one step ---- */
var units=S.map(function(s){var u=[].slice.call(s.querySelectorAll('[data-s]'));
 if(!u.length){var bd=s.querySelector('.bd');if(bd&&!bd.querySelector('.mk')){bd.dataset.s=1;u=[bd]}}
 return u});
[].forEach.call(document.querySelectorAll('.tln,.agx,.sk-tools'),function(g){[].forEach.call(g.children,function(c,i){c.style.setProperty('--i',i)})});

/* statement titles build word by word in English and phrase by phrase in Chinese */
if(motion)[].forEach.call(document.querySelectorAll('.st h2,.sec h2,.tk h2,.bq h2,.cl h2,.cover h1'),function(h){var i=0;
 (function walk(n){[].slice.call(n.childNodes).forEach(function(c){
  if(c.nodeType===3){var f=document.createDocumentFragment(),parts=ZH?c.nodeValue.replace(/([，。、：；？！])/g,'$1\u0001').split('\u0001'):c.nodeValue.split(/(\s+)/);
   parts.forEach(function(p){if(!p)return;if(!ZH&&/^\s+$/.test(p)){f.appendChild(document.createTextNode(p));return}
    var w=document.createElement('span');w.className=ZH?'phr':'wd';w.style.setProperty('--i',i++);w.textContent=p;f.appendChild(w)});
   n.replaceChild(f,c)}else if(c.nodeType===1&&c.tagName!=='BR'&&!c.classList.contains('rot'))walk(c)})})(h)});

/* ---- market map: the same named tools as the deck, lit in a scattered order on an accelerating curve ---- */
var TOOLS='__TOOLS__'.split('|');
[].forEach.call(document.querySelectorAll('.mk'),function(mk){var box=mk.querySelector('.mk-field');if(!box)return;
 var n=TOOLS.length,ord=TOOLS.map(function(x,i){return i}),seed=7,TF=2200,frag=document.createDocumentFragment();
 for(var i=n-1;i>0;i--){seed=(seed*16807)%2147483647;var j=seed%(i+1),x=ord[i];ord[i]=ord[j];ord[j]=x}
 TOOLS.forEach(function(x,i){var p=x.split(':'),el=document.createElement('span'),t=Math.round(TF*Math.pow((ord[i]+1)/n,.6));
  el.textContent=ZH&&p[1]?p[1]:p[0];el.dataset.t=t;el.style.setProperty('--d',t+'ms');frag.appendChild(el);frag.appendChild(document.createTextNode(' '))});
 box.appendChild(frag);mk.dataset.tf=TF;var big=mk.querySelector('.mk-big');if(big)mk.dataset.big=big.textContent.replace(/\D/g,'');
 var c=mk.querySelector('.mk-n');if(c)c.textContent=n});

/* ---- counters: the first number in each .big / .cnt counts up, keeping its prefix, commas, decimals, and unit ---- */
function firstNum(el){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);while(w.nextNode())if(/\d/.test(w.currentNode.nodeValue))return w.currentNode;return null}
function countUp(roots){if(!motion)return;var els=[];
 roots.forEach(function(r){if(r.matches('.big,.cnt'))els.push(r);[].push.apply(els,r.querySelectorAll('.big,.cnt'))});
 els.forEach(function(el){if(el.dataset.run||el.classList.contains('nc')||el.closest('.mk'))return;
  var t=firstNum(el);if(!t)return;var full=t.nodeValue,m=full.match(/^([^\d]*)(\d[\d,]*(?:\.\d+)?)([\s\S]*)$/);if(!m)return;
  var raw=m[2],to=parseFloat(raw.replace(/,/g,'')),dec=(raw.split('.')[1]||'').length,cm=raw.indexOf(',')>=0,t0=0,D=to>=1000?1500:1100;
  el.dataset.run=1;el.style.minWidth=el.getBoundingClientRect().width+'px';
  requestAnimationFrame(function f(ts){if(!t0)t0=ts;var p=Math.min(1,(ts-t0)/D),v=to*(1-Math.pow(1-p,4));
   if(p>=1){t.nodeValue=full;el.style.minWidth='';return}
   t.nodeValue=m[1]+(cm?Math.round(v).toLocaleString('en-US'):v.toFixed(dec))+m[3];requestAnimationFrame(f)})})}

/* ---- builds ---- */
var timers=[],mkRaf=0,building=-1;
function clearT(){timers.forEach(clearTimeout);timers=[];cancelAnimationFrame(mkRaf)}
function settle(s){s.classList.remove('arm','go');s.classList.add('seen')}
function mkSet(mk,n,v){var c=mk.querySelector('.mk-n'),b=mk.querySelector('.mk-big');if(c)c.textContent=n;if(b)b.textContent=v.toLocaleString('en-US')}
function finish(i){if(i<0)return;var s=S[i];if(!s.classList.contains('arm'))return;clearT();
 s.classList.add('go');units[i].forEach(function(u){u.classList.add('vis')});
 [].forEach.call(s.querySelectorAll('.mk'),function(mk){mk.classList.add('stat');mkSet(mk,TOOLS.length,+mk.dataset.big||0)});
 setTimeout(function(){settle(s)},700);if(building===i)building=-1}
function play(i){var s=S[i];if(!motion||!s.classList.contains('arm')||s.classList.contains('go'))return;
 clearT();building=i;void s.offsetWidth;s.classList.add('go');
 var u=units[i],groups={};u.forEach(function(e){var k=+e.dataset.s||1;(groups[k]=groups[k]||[]).push(e)});
 var ks=Object.keys(groups).map(Number).sort(function(a,b){return a-b}),hero=s.querySelector('.wd,.phr'),
  t0=hero?Math.min(900,s.querySelectorAll('.wd,.phr').length*55+250):280,gap=ks.length>3?320:420;
 ks.forEach(function(k,j){timers.push(setTimeout(function(){groups[k].forEach(function(e){e.classList.add('vis')});countUp(groups[k])},t0+j*gap))});
 var mk=s.querySelector('.mk'),end=t0+ks.length*gap+900;
 if(mk){var sp=[].slice.call(mk.querySelectorAll('.mk-field span')),TF=+mk.dataset.tf,big=+mk.dataset.big||0,TS=TF+600,TB=900,st=performance.now();mkSet(mk,0,0);
  (function f(now){var e=now-st,n=0;for(var q=0;q<sp.length;q++)if(+sp[q].dataset.t<=e)n++;
   if(e>TS-250)mk.classList.add('stat');var b=e<TS?0:Math.min(1,(e-TS)/TB);mkSet(mk,n,Math.round(big*(1-Math.pow(1-b,3))));
   if(e<TS+TB+40)mkRaf=requestAnimationFrame(f)})(st);end=Math.max(end,TS+TB+400)}
 timers.push(setTimeout(function(){settle(s);building=-1},end+400))}
if(motion)S.forEach(function(s){s.classList.add('arm')});

/* ---- navigation ---- */
var idx=-1,shown=-1;
function w(){return deck.clientWidth||1}
function at(){return Math.max(0,Math.min(N-1,Math.round(deck.scrollLeft/w())))}
function go(i,instant){i=Math.max(0,Math.min(N-1,i));
 deck.scrollTo({left:i*w(),behavior:instant||!motion?'instant':'smooth'})}
function label(i){var tp=$('.tip');if(tp&&i>0)tp.classList.remove('on');
 nx.querySelector('span').textContent=i===0?T.start:i===END||i===N-1?T.done:T.next;
 nx.setAttribute('aria-label',i===END||i===N-1?T.done:T.next);
 pv.disabled=i===0;
 ctr.querySelector('b').innerHTML=(i+1)+' <span>/ '+N+'</span>';
 ctr.querySelector('small').textContent=part[i];
 bar.style.setProperty('--p',(i+1)/N);
 var s=S[i];H.classList.toggle('dk',s.classList.contains('nv')||s.classList.contains('p6-hero')||s.classList.contains('p7-ph'));H.classList.toggle('bg-alt',s.classList.contains('alt'));
 var m=document.querySelector('meta[name=theme-color]');if(m)m.content=s.classList.contains('nv')||s.classList.contains('p6-hero')||s.classList.contains('p7-ph')?'#0B1A4A':s.classList.contains('alt')||s.classList.contains('p6-sec')?'#F5F7FA':'#FFFFFF';
 if(lng)lng.href=lng.getAttribute('data-base')+'#'+(i+1)}
function arrive(i){if(i===shown)return;
 if(building>=0&&building!==i)finish(building);
 shown=i;play(i);moreCue();
 try{history.replaceState(null,'','#'+(i+1));localStorage.setItem('arena-talk-slide-__HOME__-'+KEY,i+1)}catch(e){}}
function onScroll(){var i=at();if(i!==idx){idx=i;label(i)}
 if(Math.abs(deck.scrollLeft-i*w())<w()*.12)arrive(i)}
var raf=0;deck.addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(function(){raf=0;onScroll()})},{passive:true});

nx.addEventListener('click',function(){if(idx===END||idx===N-1){location.href='__HOME__';return}finish(idx);go(idx+1)});
pv.addEventListener('click',function(){go(idx-1)});
addEventListener('keydown',function(e){if(sheet.classList.contains('open')){if(e.key==='Escape')closeList();return}
 if(e.altKey||e.ctrlKey||e.metaKey)return;
 if(['ArrowRight','PageDown',' '].indexOf(e.key)>=0){e.preventDefault();if(idx===END||idx===N-1){location.href='__HOME__';return}finish(idx);go(idx+1)}
 else if(['ArrowLeft','PageUp'].indexOf(e.key)>=0){e.preventDefault();go(idx-1)}
 else if(e.key==='Home'){e.preventDefault();go(0)}else if(e.key==='End'){e.preventDefault();go(N-1)}});
[].forEach.call(document.querySelectorAll('[data-go]'),function(a){a.addEventListener('click',function(e){e.preventDefault();go(+a.dataset.go)})});
/* keep the same slide in view through rotation and resizes */
var keep=0;addEventListener('resize',function(){var i=idx;clearTimeout(keep);deck.scrollLeft=i*w();keep=setTimeout(function(){deck.scrollLeft=i*w();moreCue()},150)});

/* ---- "more below": a quiet arrow when the current slide is taller than the screen ---- */
function moreCue(){var s=S[shown];if(!s||!cue)return;var m=s.scrollHeight-s.clientHeight-s.scrollTop>8;cue.classList.toggle('on',m);H.classList.toggle('more',m)}
S.forEach(function(s){s.addEventListener('scroll',function(){if(S[shown]===s)moreCue()},{passive:true})});
if(cue)cue.addEventListener('click',function(){var s=S[shown];s.scrollBy({top:s.clientHeight*.7,behavior:motion?'smooth':'instant'})});

/* ---- slide list ---- */
var sheet=$('.sheet'),list=$('.sh-l'),lastFocus=null;
(function(){var g='',html='';S.forEach(function(s,i){
 if(part[i]!==g){g=part[i];html+='<p class="sh-g">'+esc(g)+'</p>'}
 var h=s.querySelector('h1,h2'),t=h?h.cloneNode(true):null;
 if(t){[].forEach.call(t.querySelectorAll('.sub,br'),function(x){x.replaceWith(' ')});}
 var txt=t?t.innerHTML.replace(/<(?!\/?em\b)[^>]+>/g,'').replace(/\s+/g,' ').trim():'';
 html+='<a href="#'+(i+1)+'" data-i="'+i+'"><i>'+(i+1)+'</i><span>'+txt+'</span></a>'});
 list.innerHTML=html})();
function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function openList(){lastFocus=document.activeElement;sheet.hidden=false;
 [].forEach.call(list.querySelectorAll('a'),function(a){if(+a.dataset.i===idx)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
 requestAnimationFrame(function(){sheet.classList.add('open');var a=list.querySelector('[aria-current]');if(a)a.scrollIntoView({block:'center'});$('.sh-x').focus()})}
function closeList(){sheet.classList.remove('open');setTimeout(function(){sheet.hidden=true},380);if(lastFocus)lastFocus.focus()}
$('.lst').addEventListener('click',openList);ctr.addEventListener('click',openList);
$('.sh-x').addEventListener('click',closeList);
sheet.addEventListener('click',function(e){if(e.target===sheet)closeList()});
list.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;e.preventDefault();var i=+a.dataset.i;
 if(i!==idx)finish(idx);closeList();go(i,true)});

/* ---- start: #n opens slide n; save the language for the landing page ---- */
try{localStorage.setItem('arena-talk-lang',ZH?'zh':'en')}catch(e){}
var h=parseInt((location.hash||'').slice(1),10),start=h>=1&&h<=N?h-1:0;
idx=start;label(start);
requestAnimationFrame(function(){deck.scrollLeft=start*w();idx=at();label(idx);setTimeout(function(){arrive(idx)},motion?250:0)});
if(start===0){var tip=$('.tip');if(tip){var seenTip=false;try{seenTip=!!localStorage.getItem('arena-talk-tip')}catch(e){}
 if(!seenTip){tip.textContent=T.tip;setTimeout(function(){tip.classList.add('on')},1600);setTimeout(function(){tip.classList.remove('on')},6200);
  deck.addEventListener('scroll',function(){tip.classList.remove('on')},{passive:true,once:true});try{localStorage.setItem('arena-talk-tip','1')}catch(e){}}}}
})();
