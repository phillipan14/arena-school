/* 50-pages.js: phone-only DOM for the general pages (pairs with 50-pages.css). Tap-only; nothing hover.
   1. About: each founder's schools and companies become a logo scroll (text credential lines hidden).
   2. Approach: a segmented control (Agency / Taste / Craft) shows one pillar at a time.
   3. Results: jump-index rows; inline text links become rows; Tsinghua facts become label/value rows.
   4. Contact: the email address becomes the last row of the routes list.
   5. Enroll: a check glyph for selected rows.
   6. Chinese H1s: phrases between punctuation never split mid-word. */
(function(){
  if(!matchMedia('(max-width:760px)').matches)return;
  var B=document.body,zh=(document.documentElement.lang||'').indexOf('zh')===0;
  var NS='http://www.w3.org/2000/svg';
  function chev(){var s=document.createElementNS(NS,'svg');s.setAttribute('viewBox','0 0 24 24');s.setAttribute('aria-hidden','true');s.setAttribute('class','ph-chev');
    var p=document.createElementNS(NS,'path');p.setAttribute('d','M9 5l7 7-7 7');s.appendChild(p);return s}
  function el(tag,cls,txt){var e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e}
  /* a text link inside a paragraph -> a row under the paragraph (the inline link reads as plain text) */
  function rowAfter(p,a){
    if(!p||!a||a.dataset.phX)return;a.dataset.phX='1';
    var ul=el('ul','ph-list ph-xlist'),li=el('li'),r=el('a','ph-xrow');r.href=a.getAttribute('href');
    r.appendChild(el('span','ph-row-t',a.textContent.replace(/[→›]/g,'').trim()));li.appendChild(r);ul.appendChild(li);
    p.after(ul);a.classList.add('ph-inlined');a.setAttribute('tabindex','-1');a.setAttribute('aria-hidden','true');
  }

  /* ---- 1. About: founder logo scroll ---- */
  if(B.classList.contains('pg-about')){
    var L=[ // pattern, file, alt, height (area rule: similar ink per mark)
      [/Brown|布朗/,'brown.png','Brown University',28],[/Caltech|加州理工/,'caltech.png','Caltech',18],
      [/Harvard|哈佛/,'harvard.png','Harvard University',24],[/Tsinghua|清华/,'tsinghua-lockup.png','Tsinghua University',27],
      [/Schwarzman|苏世民/,'schwarzman.png?v=2','Schwarzman Scholars',20],[/Apple|苹果/,'apple.png','Apple',28],
      [/Deloitte|德勤/,'deloitte.png','Deloitte',15],[/Kimi/,'kimi.png','Kimi (Moonshot AI)',17],
      [/McKinsey|麦肯锡/,'mckinsey.png','McKinsey & Company',16],[/Goldman|高盛/,'goldman.png','Goldman Sachs',26],
      [/Y\s*Combinator/,'yc.png','Y Combinator',26]];
    var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches,built=0;
    document.querySelectorAll('.pg-founder').forEach(function(f){
      var c=f.querySelector('.pg-founder-creds');if(!c||f.querySelector('.ph-flogos'))return;
      var parts=[];c.querySelectorAll(':scope > span').forEach(function(s){s.textContent.split(/\s*·\s*/).forEach(function(t){t=t.trim();if(t)parts.push(t)})});
      var marks=[];parts.forEach(function(t){for(var i=0;i<L.length;i++){if(L[i][0].test(t)){if(marks.indexOf(L[i])<0)marks.push(L[i]);return}}});
      if(marks.length<2)return;
      var wrap=el('div','ph-flogos'),ul=el('ul');wrap.setAttribute('role','img');
      wrap.setAttribute('aria-label',(zh?'学历与履历：':'Studied and worked at: ')+parts.join(zh?'、':', '));
      function set(hidden){marks.forEach(function(m){var li=el('li'),im=el('img');im.src='/logos/cred/'+m[1];im.alt=hidden?'':m[2];im.style.height=m[3]+'px';im.decoding='async';
        if(hidden)li.setAttribute('aria-hidden','true');li.appendChild(im);ul.appendChild(li)})}
      set(false);set(true);
      wrap.appendChild(ul);f.querySelector('.pg-founder-top').after(wrap);
      ul.style.setProperty('--fl-dur',Math.max(24,marks.length*6)+'s');
      // tap to pause / resume, like holding a ticker still to read it
      wrap.addEventListener('click',function(){wrap.classList.toggle('is-paused')});
      built++;
    });
    if(built)B.classList.add('ph-fl');
  }

  /* ---- 2. Approach: segmented control ---- */
  if(B.classList.contains('pg-approach')){
    var grp=document.querySelector('.ap-pcards'),cards=grp?[].slice.call(grp.querySelectorAll(':scope > .ap-pcard')):[];
    if(cards.length===3&&!document.querySelector('.ph-seg')){
      var seg=el('div','ph-seg');seg.setAttribute('role','tablist');seg.setAttribute('aria-label',zh?'三大支柱':'Three pillars');
      var btns=cards.map(function(c,i){var h=c.querySelector('h3'),b=el('button',null,h?h.textContent.trim():String(i+1));
        b.type='button';b.setAttribute('role','tab');b.id='ph-seg-'+i;b.setAttribute('aria-controls',c.id);c.setAttribute('role','tabpanel');c.setAttribute('aria-labelledby',b.id);
        b.addEventListener('click',function(){show(i,false)});seg.appendChild(b);return b});
      grp.before(seg);grp.classList.add('ph-segd');
      var cur=-1;
      function show(i,scroll){if(i===cur)return;cur=i;cards.forEach(function(c,k){c.classList.toggle('ph-on',k===i);c.classList.add('in')});
        btns.forEach(function(b,k){b.setAttribute('aria-selected',k===i?'true':'false');b.tabIndex=k===i?0:-1});
        if(scroll){var y=seg.getBoundingClientRect().top+scrollY-72;scrollTo({top:y,behavior:'instant'})}
        else if(seg.getBoundingClientRect().top<0){scrollTo({top:seg.getBoundingClientRect().top+scrollY-72})}}
      seg.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='ArrowLeft'){var n=(cur+(e.key==='ArrowRight'?1:2))%3;show(n);btns[n].focus()}});
      // swipe the card sideways to move between pillars
      var sx=0,sy=0;grp.addEventListener('touchstart',function(e){sx=e.touches[0].clientX;sy=e.touches[0].clientY},{passive:true});
      grp.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-sx,dy=e.changedTouches[0].clientY-sy;
        if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)*1.5){var n=cur+(dx<0?1:-1);if(n>=0&&n<3)show(n)}},{passive:true});
      function fromHash(){var h=location.hash.slice(1),k=cards.findIndex(function(c){return c.id===h});if(k>=0){show(k,true);return true}return false}
      if(!fromHash())show(0);
      addEventListener('hashchange',fromHash);
    }
  }

  /* ---- 3. Results ---- */
  if(B.classList.contains('pg-results')){
    document.querySelectorAll('.pg-gl > a').forEach(function(a){if(a.querySelector('.ph-gl-t'))return;
      var t=el('span','ph-gl-t'),b=a.querySelector('b'),s=a.querySelector('span');if(!b||!s)return;
      var b2=el('b',null,b.textContent);t.appendChild(b2);t.appendChild(s);b.setAttribute('aria-hidden','true');a.prepend(t)});
    document.querySelectorAll('.pg-case-copy .lede, .pg-inst .lede').forEach(function(p){var a=p.querySelector('a.tlink');if(a)rowAfter(p,a)});
    document.querySelectorAll('.pg-inst-card dl').forEach(function(dl){if(dl.querySelector('.ph-dlrow'))return;
      [].slice.call(dl.querySelectorAll(':scope > dt')).forEach(function(dt){var dd=dt.nextElementSibling,r=el('div','ph-dlrow');dt.before(r);r.appendChild(dt);if(dd&&dd.tagName==='DD')r.appendChild(dd)})});
  }

  /* ---- 4. Contact: email row ---- */
  if(B.classList.contains('pg-contact-page')){
    var routes=document.querySelector('.pg-routes'),mail=document.querySelector('.pg-hero-mail');
    if(routes&&mail&&!routes.querySelector('.ph-mailrow')){
      var li=el('li'),a=el('a','ph-mailrow');a.href=mail.getAttribute('href');
      a.appendChild(el('span','ph-row-t',zh?'邮件':'Email'));a.appendChild(el('span','ph-row-v',mail.textContent.trim()));a.appendChild(chev());
      li.appendChild(a);routes.appendChild(li);
      mail.classList.add('ph-inlined');mail.setAttribute('tabindex','-1');
    }
  }

  /* ---- 5. Enroll: check glyph ---- */
  if(B.classList.contains('pg-enroll-page')){
    document.querySelectorAll('.en-form .chk').forEach(function(l){if(!l.querySelector('.ph-tick')){var t=el('i','ph-tick');t.setAttribute('aria-hidden','true');l.appendChild(t)}});
  }

  /* ---- 5b. program row titles: the last two words stay together (no lone 'Mentorship') ---- */
  if(!zh)document.querySelectorAll('.pg-prog b, .pg-adult b').forEach(function(b){if(b.querySelector('.nb'))return;var t=b.lastChild;if(!t||t.nodeType!==3)return;
    var m=t.nodeValue.match(/^([\s\S]*?)(\S+\s+\S+)\s*$/);if(!m||!m[1].trim())return;t.nodeValue=m[1];b.appendChild(el('ph-nb','nb',m[2]))});

  /* ---- 5c. program row meta (grade · length): each part stays whole ---- */
  document.querySelectorAll('.pg-prog small').forEach(function(sm){if(sm.dataset.phM)return;sm.dataset.phM='1';var parts=sm.textContent.split(/\s*·\s*/);if(parts.length<2)return;
    sm.textContent='';parts.forEach(function(t,i){sm.appendChild(el('ph-nb','nb',t+(i<parts.length-1?' ·':'')));if(i<parts.length-1)sm.appendChild(document.createTextNode(' '))})});

  /* ---- 5d. Chinese timeline times: a long label breaks between words (一天的 / 大部分时间), never inside one ---- */
  if(zh)document.querySelectorAll('.ap-tl-time').forEach(function(t){var v=t.textContent.trim();if(v.length<7||t.querySelector('.nb'))return;
    t.textContent=v.slice(0,v.length-5);t.appendChild(el('ph-nb','nb',v.slice(-5)))});

  /* ---- 6. Chinese H1: keep each phrase whole ---- */
  if(zh&&/pg-(approach|schools|about|partnerships|results|contact-page|enroll-page)/.test(B.className)){
    var h=document.querySelector('main section.hero h1');
    if(h&&!h.dataset.phPh){h.dataset.phPh='1';
      var w=document.createTreeWalker(h,NodeFilter.SHOW_TEXT),ns=[],n;while(n=w.nextNode())ns.push(n);
      ns.forEach(function(t){if(t.parentElement.closest('.nb'))return;var v=t.nodeValue;if(!/[㐀-鿿]/.test(v))return;
        var segs=v.match(/[^、，。：；！？]+[、，。：；！？]*/g);if(!segs)return;
        var fr=document.createDocumentFragment();segs.forEach(function(s){var sp=el('ph-nb','nb',s);fr.appendChild(sp)});
        t.parentNode.replaceChild(fr,t)});
    }
  }
})();
