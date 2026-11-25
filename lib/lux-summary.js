const DAY=86400000, ANCHOR=Date.parse('2026-11-25T00:00:00Z');
function due(date=new Date()){return Math.floor((date-ANCHOR)/DAY)%3===0;}
function summary(records,now=Date.now()){
  const recent=records.filter(r=>Date.parse(r.submittedAt)>now-3*DAY);
  const names=[...new Set(records.map(r=>r.answers.q1.trim()))];
  const tally=key=>{const m=new Map();for(const r of records)for(const v of (r.answers[key]||'').split('；'))if(v)m.set(v,(m.get(v)||0)+1);return [...m].sort((a,b)=>b[1]-a[1]).map(([k,v])=>`${k}: ${v}`).join('; ');};
  return [
    'Lux × Arena winter bootcamp · questionnaire update',
    `${records.length} total submissions; ${names.length} distinct self-reported names.`,
    `${recent.length} new submissions in the last three days.`,
    recent.length?'New respondent names: '+[...new Set(recent.map(r=>r.answers.q1))].join(', '):'No new submissions in this period.',
    records.length?'AI use: '+tally('q10'):'',
    records.length?'Interests: '+tally('q4'):'',
    'Names are self-reported; duplicate names or nicknames can affect the count. A cohort roster is needed to identify nonrespondents.',
    'Full answers and CSV export: https://arenaschool.org/zero-to-launch/lux-scholar/results',
  ].filter(Boolean).join('\n\n');
}
module.exports={due,summary};
