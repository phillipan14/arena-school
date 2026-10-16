/* 30-program.js: program-page template + shared closing components on phones (pairs with 30-program.css). Tap-only.
   1. "Why it matters": a reveal that repeats the next section (the day list = the step list) is dropped;
      rows that still reveal something get button semantics and aria-expanded.
   2. "How it runs" step selector: the hidden stage (photos and clips) is removed so nothing autoplays or downloads.
   3. Proof: stats, logos, events, and the results link become one grouped list of short rows + "See results".
   4. Team (.hp-cred, every page): two founder rows (photo, name, role) linking to /about#cofounders,
      plus the credential logos as one static wrap. The expanding profile panel never opens on phones.
   5. Closing (.pp-final, every page): heading, one line, one pill, then grouped rows (formats, one-pager,
      parent link, secondary buttons, all programs). The one-pager form moves (not cloned) into a bottom sheet.
   FAQ is CSS only. */
(function(){
  if(!matchMedia('(max-width:760px)').matches)return;
  var zh=(document.documentElement.lang||'').indexOf('zh')===0;
  var NS='http://www.w3.org/2000/svg';
  function chev(){var s=document.createElementNS(NS,'svg');s.setAttribute('viewBox','0 0 24 24');s.setAttribute('aria-hidden','true');s.setAttribute('class','ph-chev');
    var p=document.createElementNS(NS,'path');p.setAttribute('d','M9 5l7 7-7 7');s.appendChild(p);return s}
  function txt(el){return el?(el.textContent||'').replace(/\s*[→›↓]\s*$/,'').replace(/\s+/g,' ').trim():''}
  function el(tag,cls,text){var e=document.createElement(tag);if(cls)e.className=cls;if(text!=null)e.textContent=text;return e}
  /* one grouped row: {href|onClick, t1, t1html, t2, lead (node), cls} */
  function row(o){
    var li=el('div'),r;li.setAttribute('role','listitem');
    if(o.href){r=el('a','ph-row php-row');r.href=o.href;}
    else if(o.onClick){r=el('button','ph-row php-row');r.type='button';r.addEventListener('click',o.onClick);}
    else r=el('div','ph-row php-row php-static');
    if(o.cls)r.className+=' '+o.cls;
    if(o.lead)r.appendChild(o.lead);
    var t=el('span','ph-row-t');
    var a=el('span','php-t1');glueText(a,o.t1||'');t.appendChild(a);
    if(o.t2){var b2=el('span','php-t2');glueText(b2,o.t2);t.appendChild(b2)}
    r.appendChild(t);
    if(o.href||o.onClick)r.appendChild(chev());
    li.appendChild(r);return li;
  }
  /* keep the last two words (or last three CJK characters) together */
  function glueText(node,s){
    var cut;if(/[\u3400-\u9fff]/.test(s)){cut=Math.max(0,s.length-4)}else{var m=s.match(/(\S+\s+\S+)$/);if(!m||m[1].length>22){node.textContent=s;return}cut=s.length-m[1].length}
    if(cut<=0){node.textContent=s;return}
    node.textContent=s.slice(0,cut);node.appendChild(el('ph-nb','nb',s.slice(cut)));
  }
  function list(rows,dark){var u=el('div','ph-list php-list'+(dark?' ph-list-dark':''));u.setAttribute('role','list');rows.forEach(function(r){if(r)u.appendChild(r)});return u}
  function lab(text){return el('p','php-k',text)}

  /* ---- 0. FAQ questions: no orphan word / 1 to 2 CJK characters on the last line ---- */
  document.querySelectorAll('.faq .faq-q').forEach(function(q){
    if(q.querySelector('.nb,[style*="nowrap"]'))return;
    var w=document.createTreeWalker(q,NodeFilter.SHOW_TEXT),n,t=null;while(n=w.nextNode())if(n.nodeValue.trim())t=n;if(!t)return;
    var v=t.nodeValue,cut;
    if(/[\u3400-\u9fff]/.test(v)){cut=Math.max(0,v.replace(/\s+$/,'').length-4)}
    else{var m=v.match(/(\S+\s+\S+)\s*$/);if(!m||m[1].length>22)return;cut=v.length-m[0].length}
    if(cut<=0)return;
    var sp=el('ph-nb','nb',v.slice(cut));t.parentNode.insertBefore(document.createTextNode(v.slice(0,cut)),t);t.parentNode.insertBefore(sp,t);t.remove();
  });

  /* ---- 1. Why it matters ---- */
  document.querySelectorAll('.pc-why-list.has-wr > li').forEach(function(li){
    var wr=li.querySelector(':scope > .wr');if(!wr)return;
    if(!txt(wr)){li.classList.add('php-nowr');return}  /* no words: logos only, which repeat the row's text */
    var proc=wr.querySelector('.wr-proc');
    if(proc){
      var sec=li.closest('section'),nx=sec&&sec.nextElementSibling;
      var steps=nx?[].map.call(nx.querySelectorAll('.pc-sel-h, .pg-seq h3, .pg-seq b'),txt):[];
      var mine=[].map.call(proc.querySelectorAll('b'),txt);
      if(mine.every(function(m){return steps.indexOf(m)>=0})){li.classList.add('php-nowr');return}
    }
    /* the tool chips repeat the visible "Typical tools include…" line */
    if(wr.querySelector('.wr-marq')&&li.parentElement.parentElement.querySelector('.pc-why-extra')){li.classList.add('php-nowr');return}
    li.setAttribute('role','button');li.tabIndex=0;li.setAttribute('aria-expanded','false');
    li.addEventListener('click',function(){setTimeout(function(){li.setAttribute('aria-expanded',li.classList.contains('wr-open')?'true':'false')},0)});
    li.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();li.click()}});
  });

  /* ---- 2. Step selector: no stage on phones; step copy gets the same orphan glue ---- */
  document.querySelectorAll('[data-pc-sel] .pc-sel-p').forEach(function(p){if(p.children.length)return;glueText(p,p.textContent.replace(/\s+$/,''))});
  document.querySelectorAll('[data-pc-sel] .pc-sel-stage').forEach(function(st){
    st.querySelectorAll('video').forEach(function(v){try{v.pause()}catch(e){}v.removeAttribute('src');v.preload='none';try{v.load()}catch(e){}});
    st.remove();
  });

  /* ---- 3. Proof ---- */
  var CN={'Harvard':'哈佛','Stanford':'斯坦福'};
  function judges(imgs){var n=[].map.call(imgs,function(i){return zh?(CN[i.alt]||i.alt):i.alt});
    n=n.map(function(x){return x.replace(/ /g,'\u00a0')});
    return zh?'路演评委来自'+n.join('、')+'及AI实验室':'Demo-day judges from '+n.join(', ')+', and AI labs'}
  document.querySelectorAll('section.pc-proof').forEach(function(sec){
    var box=sec.querySelector('.container');if(!box)return;
    var rows=[],link=null;
    sec.querySelectorAll('.pc-stats > li').forEach(function(li){
      var b=li.querySelector(':scope > b'),s=li.querySelector(':scope > span'),sm=li.querySelector(':scope > small');
      var imgs=b?b.querySelectorAll('img'):[],t=txt(s);
      if(imgs.length&&/these institutions|以上机构/.test(t))t=judges(imgs);
      var r=row({t1:t,t2:txt(sm)});
      if(b&&!imgs.length){var t1=r.querySelector('.php-t1');t1.insertBefore(document.createTextNode(' '),t1.firstChild);t1.insertBefore(el('b','php-num',txt(b)),t1.firstChild)}
      rows.push(r);
    });
    sec.querySelectorAll('.pc-evs > li').forEach(function(li){
      var a=li.querySelector('a.tlink');if(a&&!link)link=a;
      rows.push(row({t1:txt(li.querySelector('h3')),t2:txt(li.querySelector('.pc-k'))}));
    });
    var line=sec.querySelector('.pc-proof-line');
    if(line){
      var a=line.querySelector('a');if(a&&!link)link=a;
      var c=line.cloneNode(true);c.querySelectorAll('a').forEach(function(x){x.remove()});var lt=txt(c);
      if(lt)rows.push(row({t1:lt}));
    }
    if(link)rows.push(row({href:link.getAttribute('href'),t1:txt(link),cls:'php-link'}));
    if(!rows.length){sec.classList.add('php-empty');return}
    sec.classList.add('php-proof');
    var head=sec.querySelector('.pc-proof-head');
    var wrap=el('div','php-proof-box');wrap.appendChild(list(rows));
    if(head)head.after(wrap);else box.prepend(wrap);
    /* mentorship: "What students finish with" as static rows */
    var nw=sec.querySelector('.pc-notes-wrap');
    if(nw){var k=nw.querySelector('.pc-k');var nr=[].map.call(nw.querySelectorAll('.pc-notes > li'),function(li){return row({t1:txt(li.querySelector('b')),t2:txt(li.querySelector('span'))})});
      var g=el('div','php-notes');if(k)g.appendChild(lab(txt(k)));g.appendChild(list(nr));wrap.after(g)}
  });

  /* ---- 4. Team ---- */
  document.querySelectorAll('section.hp-cred').forEach(function(sec){
    var cf=sec.querySelector('.hp-cf');if(!cf)return;
    var base=zh?'/about-cn#':'/about#',SLUG={jj:'jing-jing-yang',pa:'phillip-an'};
    var rows=[].map.call(cf.querySelectorAll('.hp-cf-card'),function(c){
      var href=base+(SLUG[c.getAttribute('data-xp-card')]||'cofounders');
      var im=c.querySelector('img'),lead=null;
      if(im){lead=el('img','php-ava');lead.src=im.getAttribute('src');lead.alt='';lead.width=40;lead.height=40;lead.loading='lazy';lead.decoding='async'}
      return row({href:href,lead:lead,t1:txt(c.querySelector('.hp-cf-t b')),t2:txt(c.querySelector('.hp-cf-r')),cls:'php-person'});
    });
    var box=el('div','php-team');box.appendChild(list(rows));
    /* credentials: the page's own logo grid stays (css/cred.css: one even grid, the same on every page; DEPTH-BRIEF) */
    cf.after(box);sec.classList.add('php-teamsec');
  });

  /* ---- 5. Closing + one-pager bottom sheet ---- */
  var sheet=null,lastFocus=null;
  function buildSheet(lead){
    sheet=el('div','php-sheet');sheet.setAttribute('role','dialog');sheet.setAttribute('aria-modal','true');sheet.hidden=true;
    var h=lead.querySelector('h3');sheet.setAttribute('aria-label',txt(h)||'One-pager');
    var bg=el('div','php-sheet-bg');var pn=el('div','php-sheet-panel');pn.tabIndex=-1;
    var top=el('div','php-sheet-top');top.appendChild(el('span','php-sheet-grab'));
    var x=el('button','php-sheet-x');x.type='button';x.setAttribute('aria-label',zh?'关闭':'Close');
    x.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';top.appendChild(x);
    pn.appendChild(top);pn.appendChild(lead);sheet.appendChild(bg);sheet.appendChild(pn);document.body.appendChild(sheet);
    lead.classList.add('in','is-in','revealed','visible');
    bg.addEventListener('click',closeSheet);x.addEventListener('click',closeSheet);
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&sheet.classList.contains('on'))closeSheet()});
    /* drag the grab bar down to dismiss */
    var y0=null,dy=0;
    top.addEventListener('touchstart',function(e){y0=e.touches[0].clientY;dy=0;pn.style.transition='none'},{passive:true});
    top.addEventListener('touchmove',function(e){if(y0==null)return;dy=Math.max(0,e.touches[0].clientY-y0);pn.style.transform='translateY('+dy+'px)'},{passive:true});
    top.addEventListener('touchend',function(){if(y0==null)return;y0=null;pn.style.transition='';pn.style.transform='';if(dy>90)closeSheet()});
  }
  function openSheet(){if(!sheet)return;lastFocus=document.activeElement;sheet.hidden=false;document.documentElement.classList.add('php-lock');
    requestAnimationFrame(function(){requestAnimationFrame(function(){sheet.classList.add('on');sheet.querySelector('.php-sheet-panel').focus({preventScroll:true})})})}
  function closeSheet(){if(!sheet)return;sheet.classList.remove('on');document.documentElement.classList.remove('php-lock');
    setTimeout(function(){sheet.hidden=true},280);if(document.activeElement&&sheet.contains(document.activeElement))document.activeElement.blur();if(lastFocus&&lastFocus.focus)lastFocus.focus({preventScroll:true})}
  document.querySelectorAll('a[href="#onepager"]').forEach(function(a){a.addEventListener('click',function(e){if(sheet){e.preventDefault();openSheet()}})});

  document.querySelectorAll('section.pp-final').forEach(function(sec){
    var box=sec.querySelector(':scope > .container');if(!box)return;
    var cta=sec.querySelector('.pp-close-cta');
    var main=cta&&cta.querySelector('.btn-primary');
    var formats=[],actions=[];
    /* formats as static rows */
    var fk=sec.querySelector('.pp-final-k'),fl=sec.querySelector('.pp-formats');
    if(fl)formats=[].map.call(fl.querySelectorAll(':scope > li'),function(li){return row({t1:txt(li.querySelector('b')),t2:txt(li.querySelector('small'))})});
    /* one-pager row opens the sheet */
    var lead=sec.querySelector('.pp-lead');
    if(lead&&lead.querySelector('form.pp-lead-form')){
      var lt=txt(lead.querySelector('h3'));
      actions.push(row({onClick:openSheet,t1:lt,t2:zh?'所有项目一页看完':'Every program on one page',cls:'php-op'}));
      buildSheet(lead);
    }
    /* secondary buttons in the CTA row */
    if(cta)cta.querySelectorAll('.btn:not(.btn-primary)').forEach(function(b){actions.push(row({href:b.getAttribute('href'),t1:txt(b)}))});
    /* parent / partner line */
    var par=sec.querySelector('.pp-close-parent');
    if(par){var a=par.querySelector('a');if(a){
      var pre=txt(par).replace(txt(a),'').trim(),lt2=txt(a);
      if(/^Tell us your school/.test(lt2))lt2='Tell us your school';
      if(/^告诉我们孩子/.test(lt2))lt2='告诉我们孩子的学校';
      actions.push(row({href:a.getAttribute('href'),t1:(pre?pre+(zh?'':' '):'')+lt2}));}}
    var all=sec.querySelector('.pp-final-all a');
    if(all)actions.push(row({href:all.getAttribute('href'),t1:txt(all)}));
    if(!formats.length&&!actions.length)return;
    var wrap=el('div','php-final');
    if(actions.length)wrap.appendChild(list(actions,true));
    if(formats.length){if(fk)wrap.appendChild(lab(txt(fk)));wrap.appendChild(list(formats,true))}
    var top=sec.querySelector('.pp-final-top, .pc-final-pair');
    (top||box.firstElementChild).after(wrap);
    sec.classList.add('php-closing');
  });
})();
