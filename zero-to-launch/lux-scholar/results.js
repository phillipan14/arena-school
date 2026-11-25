(() => {
  'use strict';
  const $ = s => document.querySelector(s), endpoint='/api/lux-results';
  let records=[], questions=[], loading=false;
  const time = value => new Date(value).toLocaleString('zh-CN',{timeZone:'Asia/Shanghai',hour12:false});
  function el(tag,text){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;}
  function locked(){records=[];questions=[];$('#responses').replaceChildren();$('#charts').replaceChildren();$('#dashboard').hidden=true;$('#login').hidden=false;}
  async function api(options={}){const response=await fetch(endpoint,{...options,cache:'no-store',credentials:'same-origin'});const data=await response.json();if(response.status===401){locked();throw Error(data.error||'请重新登录。');}if(!response.ok)throw Error(data.error||'暂时无法读取结果。');return data;}
  function counts(key,multi=false){const counts=new Map();for(const r of records){for(const a of multi?(r.answers[key]||'').split('；'):[r.answers[key]])if(a)counts.set(a,(counts.get(a)||0)+1);}return [...counts].sort((a,b)=>b[1]-a[1]);}
  function overview(){
    $('#total').textContent=records.length;$('#names').textContent=new Set(records.map(r=>r.answers.q1.trim().toLocaleLowerCase())).size;
    $('#recent').textContent=records.filter(r=>Date.now()-new Date(r.submittedAt).getTime()<=3*86400000).length;
    $('#charts').replaceChildren();
    for(const [title,key,multi] of [['AI 使用频率','q10',false],['编程与制作经验','q12',false],['兴趣领域（多选）','q4',true],['营期期待（多选）','q13',true]]){
      const section=el('div');section.className='chart';section.append(el('h3',title));
      const items=counts(key,multi);if(!items.length)section.append(el('p','暂无回答'));
      for(const [label,n] of items){const p=el('p');p.append(el('span',label),el('span',n+' 份'));section.append(p);}$('#charts').append(section);
    }
  }
  function render(){const query=$('#search').value.trim().toLocaleLowerCase();const visible=records.filter(r=>Object.values(r.answers).join(' ').toLocaleLowerCase().includes(query));$('#shown').textContent=`显示 ${visible.length} / ${records.length} 份提交（最新在前）`;$('#responses').replaceChildren();if(!visible.length)$('#responses').append(el('p',records.length?'没有匹配的回答。':'还没有收到问卷。学生提交后会显示在这里。'));
    for(const r of visible){const detail=el('details'),summary=el('summary',r.answers.q1||'未填写姓名');summary.append(el('small',`${r.answers.q3||''} · ${time(r.submittedAt)}`));detail.append(summary);const dl=el('dl');for(const q of questions){const key='q'+q.id;dl.append(el('dt',`${q.id}. ${q.title}`),el('dd',r.answers[key]|| (q.id===11?'未填写／跳过':'未填写')));if(r.answers[key+'_other'])dl.append(el('dd','补充：'+r.answers[key+'_other']));if(q.id===11&&r.answers.q11_example)dl.append(el('dd','使用例子：'+r.answers.q11_example));}detail.append(dl);$('#responses').append(detail);}
  }
  async function load(silent=false){if(loading)return;loading=true;$('#refresh').disabled=true;try{const data=await api();records=data.responses;questions=data.questions;$('#login').hidden=true;$('#dashboard').hidden=false;$('#message').textContent='';$('#updated').textContent='最近更新：'+time(data.updatedAt);overview();render();}catch(e){if(!silent||!$('#dashboard').hidden)$('#message').textContent=e.message;}finally{loading=false;$('#refresh').disabled=false;}}
  $('#login-form').addEventListener('submit',async e=>{e.preventDefault();const button=e.currentTarget.querySelector('button');button.disabled=true;try{await api({method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:$('#password').value})});$('#password').value='';await load();}catch(e){$('#message').textContent=e.message;}finally{button.disabled=false;}});
  $('#logout').addEventListener('click',async()=>{try{await api({method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'logout'})});locked();$('#message').textContent='已退出。';}catch(e){$('#message').textContent=e.message;}});
  $('#refresh').addEventListener('click',()=>load());$('#search').addEventListener('input',render);
  $('#export').addEventListener('click',()=>{const cell=value=>'"'+String(value??'').replace(/^[=+@\-\t\r]/,"'$&").replace(/"/g,'""')+'"';const headers=['提交时间（北京时间）',...questions.map(q=>q.id+'. '+q.title),'AI 使用例子'];const rows=records.map(r=>[time(r.submittedAt),...questions.map(q=>(r.answers['q'+q.id]||'')+(r.answers['q'+q.id+'_other']?'；补充：'+r.answers['q'+q.id+'_other']:'')),r.answers.q11_example||'']);const blob=new Blob(['\ufeff'+[headers,...rows].map(row=>row.map(cell).join(',')).join('\r\n')],{type:'text/csv;charset=utf-8'});const url=URL.createObjectURL(blob),a=el('a');a.href=url;a.download='Lux-Arena-Questionnaire-'+new Date().toISOString().slice(0,10)+'.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
  load(true);setInterval(()=>{if(!$('#dashboard').hidden&&!document.hidden)load(true);},60000);
})();
