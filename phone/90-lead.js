/* Lead fixes: word-level line breaking on phones.
   1. Chinese: Intl.Segmenter splits text into words; each multi-character word becomes a no-break span,
      so lines break only between words (no 审/美 or 整/个 splits) in headings, intros, rows, and labels.
   2. Both languages: names and brands stay on one line, and a "·" never starts a line (it stays with the
      word before it; the line may break after it, so "Lead instructor · Co-founder" never strands "Lead"). */
(function(){
  if(!matchMedia('(max-width:760px)').matches)return;
  var zh=(document.documentElement.lang||'').indexOf('zh')===0;
  var KEEP=['Forbes 30 Under 30','mini-PRD','project-based','Co-founder','co-founder','Y Combinator','Kimi Code','Schwarzman College','Schwarzman Scholars','羊筱涵','安广宁','苏世民学者','苏世民书院','Jing Jing Yang','Phillip An'];
  var SKIP='script,style,textarea,select,option,svg,.sr-only,.hr-rot,[data-rot],.wr-track,ph-w,.nb,.php-logos-set,code,.btn,.eyebrow';
  var seg=zh&&window.Intl&&Intl.Segmenter?new Intl.Segmenter('zh',{granularity:'word'}):null;
  var CJK=/[㐀-鿿]/;
  function nodes(root){var out=[],w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:function(n){
    if(!n.nodeValue.trim())return 3;var p=n.parentElement;if(!p||p.closest(SKIP))return 3;if(/flex|grid/.test(getComputedStyle(p).display))return 3;return 1}}),n;while(n=w.nextNode())out.push(n);return out}
  function wrapKeep(n){ // names/brands + " · " joiner, both languages
    var v=n.nodeValue,hit=false;
    v=v.replace(/ · /g,function(){hit=true;return '\u00a0\u00b7 '});
    if(hit)n.nodeValue=v;
    for(var i=0;i<KEEP.length;i++){var k=KEEP[i],ix=n.nodeValue.indexOf(k);if(ix<0)continue;
      var after=n.splitText(ix),rest=after.splitText(k.length),sp=document.createElement('ph-w');sp.textContent=k;after.parentNode.replaceChild(sp,after);
      wrapKeep(rest);return}
  }
  function wrapWords(n){
    var v=n.nodeValue;if(!CJK.test(v))return;var frag=document.createDocumentFragment(),buf='';
    var it=seg.segment(v)[Symbol.iterator](),s,parts=[];while(!(s=it.next()).done)parts.push(s.value);
    parts.forEach(function(p,i){var t=p.segment;
      // attach trailing punctuation to the word before it, so punctuation never starts a line
      var next=parts[i+1]&&parts[i+1].segment;
      if(p.isWordLike&&t.length>1||(next&&/^[。，、；：！？”’）》]$/.test(next)&&t.length>0&&!/^\s+$/.test(t))){
        if(buf){frag.appendChild(document.createTextNode(buf));buf=''}
        var sp=document.createElement('ph-w');sp.textContent=t;
        if(next&&/^[。，、；：！？”’）》]$/.test(next)){sp.textContent=t+next;parts[i+1].segment=''}
        frag.appendChild(sp)}
      else buf+=t});
    if(buf)frag.appendChild(document.createTextNode(buf));
    n.parentNode.replaceChild(frag,n);
  }
  /* repair: earlier orphan helpers cut a fixed number of characters; move each Chinese no-break tail back
     to the nearest word boundary so it never starts mid-word (学/生, 简/短) */
  if(seg)document.querySelectorAll('.nb').forEach(function(nb){var prev=nb.previousSibling;if(!prev||prev.nodeType!==3)return;
    var a=prev.nodeValue,t=nb.textContent;if(!CJK.test(a.slice(-1)+t.charAt(0)))return;var all=a+t,bnd=[0],acc=0,it3=seg.segment(all)[Symbol.iterator](),r;
    while(!(r=it3.next()).done){acc+=r.value.segment.length;bnd.push(acc)}if(bnd.indexOf(a.length)>-1)return;
    var cut=0;bnd.forEach(function(x){if(x<a.length&&x>cut)cut=x});nb.textContent=a.slice(cut)+t;prev.nodeValue=a.slice(0,cut)});

  var roots=document.querySelectorAll('main, .ph-foot, .ph-bar');
  roots.forEach(function(r){nodes(r).forEach(wrapKeep)});
  /* orphans everywhere: any short block whose own text sits directly inside it */
  var CJKe=/[㐀-鿿]/;
  document.querySelectorAll('main *').forEach(function(el){
    if(el.dataset.phNb||el.closest(SKIP+',a,button,label,.btn,nav'))return;var d=getComputedStyle(el).display;if(!/block|list-item/.test(d))return;
    var own=[].filter.call(el.childNodes,function(c){return c.nodeType===3&&c.nodeValue.trim()});if(!own.length)return;
    var txt=(el.textContent||'').trim();if(txt.length<8||txt.length>420)return;
    var last=null;for(var i=el.childNodes.length-1;i>=0;i--){var c=el.childNodes[i];if(c.nodeType===3&&c.nodeValue.trim()){last=c;break}if(c.nodeType===1&&c.textContent.trim())break}
    if(!last)return;var v=last.nodeValue.replace(/\s+$/,'');
    if(CJKe.test(v)){if(v.length<5)return;var core=v.replace(/[。，、；：！？”’）》.,!?]+$/,'');var k=Math.max(0,core.length-3);
      if(seg){var bounds=[0],acc=0,it2=seg.segment(v)[Symbol.iterator](),q;while(!(q=it2.next()).done){acc+=q.value.segment.length;bounds.push(acc)}
        var best=0;bounds.forEach(function(x){if(core.length-x>=3&&x>best)best=x});k=best}
      var sp=document.createElement('ph-nb');sp.className='nb';sp.textContent=v.slice(k);last.nodeValue=v.slice(0,k)+last.nodeValue.slice(v.length);el.insertBefore(sp,last.nextSibling)}
    else{var m=v.match(/(\S+\s+\S+)$/);if(!m||m[1].length>24||m[1].charAt(0)==='\u00b7')return; /* "· Co-founder" glued would strand the words before it */var cut=v.length-m[1].length;
      var sp2=document.createElement('ph-nb');sp2.className='nb';sp2.textContent=m[1];last.nodeValue=v.slice(0,cut)+last.nodeValue.slice(v.length);el.insertBefore(sp2,last.nextSibling)}
    el.dataset.phNb='1'});

  if(seg)roots.forEach(function(r){nodes(r).forEach(function(n){
    var blk=n.parentElement.closest('p,li,h1,h2,h3,h4,dd,dt,figcaption,blockquote,button,a,label,span,div');
    var len=blk?(blk.textContent||'').length:0;
    // body paragraphs over ~160 characters may break mid-word (normal in Chinese typesetting); short text never does
    if(len&&len<=160)wrapWords(n)})});

  /* event date rows: if the city wraps under the date, drop the leading dot */
  function dots(){document.querySelectorAll('.cf-date').forEach(function(d){var b=d.querySelector('b'),c=d.querySelector('span');if(!b||!c)return;
    d.classList.toggle('ph-wrap',c.getBoundingClientRect().top>b.getBoundingClientRect().top+4)})}
  dots();window.addEventListener('load',dots);window.addEventListener('resize',dots);if(document.fonts)document.fonts.ready.then(dots);

  /* very long section headings (quote-like sentences) get a slightly smaller size so they stay within 3 lines */
  document.querySelectorAll('main h2').forEach(function(h){var n=(h.textContent||'').trim().length;if(n>(zh?40:80))h.classList.add('ph-long')});

  /* homepage photo strip header + swipe cue (fades after the first swipe) */
  var gal=document.querySelector('body.home section.gallery-strip.gm'),trk=gal&&gal.querySelector('.gm-track');
  if(gal&&trk&&!gal.querySelector('.ph-gal-h')){var hd=document.createElement('div');hd.className='ph-gal-h';
    hd.innerHTML='<b>'+(zh?'项目现场':'From our programs')+'</b><span class="ph-swipe">'+(zh?'左右滑动':'Swipe')+'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6"/></svg></span>';
    gal.insertBefore(hd,gal.firstChild);var cue=hd.querySelector('.ph-swipe');
    trk.addEventListener('scroll',function(){if(trk.scrollLeft>30)cue.classList.add('gone')},{passive:true})}

  /* index-cn form: the long placeholder breaks words; use the contact page's three short lines */
  var ta=document.querySelector('body.home textarea[placeholder]');
  if(ta&&zh)ta.setAttribute('placeholder','几句话就好。\n学校项目？孩子咨询？\n讲座或工作坊？');
})();
