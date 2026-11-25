const auth = require('../lib/lux-auth');
const { readResponses } = require('../lib/lux-store');
const questions = require('./lux-questionnaire-schema.json');
const attempts = new Map();
module.exports = async function handler(req,res) {
  res.setHeader('Cache-Control','private, no-store, max-age=0');
  res.setHeader('X-Robots-Tag','noindex, nofollow');
  res.setHeader('Vary','Cookie');
  if (req.method === 'POST') {
    if (!auth.sameOrigin(req)) return res.status(403).json({ ok:false, error:'请从问卷结果页面登录。' });
    let body;
    try { body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body; } catch { return res.status(400).json({ok:false}); }
    if (body?.action === 'logout') { res.setHeader('Set-Cookie',auth.logoutCookie()); return res.status(200).json({ok:true}); }
    if (!process.env.LUX_RESULTS_PASSWORD_HASH || !process.env.LUX_SESSION_SECRET) return res.status(503).json({ok:false,error:'访问尚未配置。'});
    const ip = String(req.headers['x-forwarded-for'] || 'unknown').split(',')[0], now=Date.now();
    for(const [k,v] of attempts) if(now-v.start>900000) attempts.delete(k);
    const attempt = attempts.get(ip) || { start:now, n:0 };
    if (attempt.n >= 10) return res.status(429).json({ok:false,error:'尝试次数较多，请 15 分钟后重试。'});
    attempt.n++; attempts.set(ip,attempt);
    if(!auth.passwordMatches(body?.password)) return res.status(401).json({ok:false,error:'密码不正确。'});
    attempts.delete(ip); res.setHeader('Set-Cookie',auth.sessionCookie());
    return res.status(200).json({ok:true});
  }
  if (req.method !== 'GET') { res.setHeader('Allow','GET, POST'); return res.status(405).json({ok:false}); }
  if (!auth.authorized(req)) return res.status(401).json({ok:false,error:'请先登录。'});
  try {
    const responses = await readResponses();
    return res.status(200).json({ ok:true, responses, questions, updatedAt:new Date().toISOString() });
  } catch { return res.status(503).json({ok:false,error:'暂时无法读取结果，请稍后刷新。'}); }
};
