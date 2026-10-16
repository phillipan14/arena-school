// POST /api/interest: one-page overview requests and program interest registrations -> Arena Slack.
// Email notification also goes via FormSubmit on the client. Either channel succeeding
// is enough for the visitor. Env: ARENA_SLACK_BOT_TOKEN (preferred),
// ARENA_SLACK_CHANNEL (optional, defaults to #schools).
// If Slack is unset or fails, falls back to emailing contact@ via Resend when
// RESEND_API_KEY and RESEND_FROM are set (typical on Preview).
const DEFAULT_CHANNEL = 'C0C4KRP3WDR'; // #schools in the Arena School workspace
const LIMITS = { name: 120, email: 200, role: 60, school: 160, program: 80, page: 200, kind: 20, contact: 120, grade: 80, lang: 8 };
const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_WINDOW = 5;
const hits = new Map(); // best-effort, per warm instance

const clean = (v, max) => String(v == null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, max);
// Escape Slack control characters so input can't ping @channel or inject links.
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const isEmail = (s) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(s);

function parseBody(body) {
  if (body && typeof body === 'object') return body;
  try { return JSON.parse(body || '{}'); } catch { return {}; }
}

function rateLimited(ip, now = Date.now()) {
  const recent = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  hits.set(ip, [...recent, now]);
  return recent.length >= MAX_PER_WINDOW;
}

function slackText(d) {
  const lines = [
    `*${d.kind === 'interest' ? 'New interest registration' : 'New one-pager request'}* · ${esc(d.program || 'Program page')}`,
    `*${esc(d.name)}* · ${esc(d.email)}`,
    d.role && `Role: ${esc(d.role)}`,
    d.school && `School: ${esc(d.school)}`,
    d.grade && `Grade: ${esc(d.grade)}`,
    d.contact && `WeChat/phone: ${esc(d.contact)}`,
    d.lang && `Language: ${esc(d.lang)}`,
    d.page && `From: ${esc(d.page)}`,
  ];
  return lines.filter(Boolean).join('\n');
}


async function emailTeam(d) {
  const key = process.env.RESEND_API_KEY;
  // Prefer RESEND_FROM; fall back to the documented notes@ address used by /api/subscribe.
  const from = process.env.RESEND_FROM || 'Arena School <notes@arenaschool.org>';
  if (!key) return false;
  const subject = `${d.kind === 'interest' ? 'Interest' : 'One-pager'} · ${d.program || 'Program'} · ${d.name}`;
  const lines = [
    d.kind === 'interest' ? 'New interest registration' : 'New one-pager request',
    `Name: ${d.name}`,
    `Email: ${d.email}`,
    d.role && `Role: ${d.role}`,
    d.school && `School: ${d.school}`,
    d.grade && `Grade: ${d.grade}`,
    d.contact && `WeChat/phone: ${d.contact}`,
    d.lang && `Language: ${d.lang}`,
    d.page && `From: ${d.page}`,
  ].filter(Boolean);
  const text = lines.join('\n');
  const html = `<pre style="font:14px/1.5 ui-monospace,Menlo,monospace;white-space:pre-wrap">${esc(text)}</pre>`;
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from, to: ['contact@arenaschool.org'], reply_to: d.email || 'contact@arenaschool.org', subject: subject.slice(0, 200), html, text }),
    });
    if (!r.ok) {
      const body = await r.text().catch(() => '');
      console.error('interest: resend email failed', r.status, body.slice(0, 200));
      return false;
    }
    return true;
  } catch (err) {
    console.error('interest: resend request failed', err && err.message);
    return false;
  }
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }
  const body = parseBody(req.body);
  if (body._honey) return res.status(200).json({ ok: true }); // bot: pretend success

  const ip = clean(String(req.headers['x-forwarded-for'] || '').split(',')[0], 64) || 'unknown';
  if (rateLimited(ip)) return res.status(429).json({ ok: false, error: 'Too many requests. Please try again later.' });

  const d = Object.fromEntries(Object.entries(LIMITS).map(([k, max]) => [k, clean(body[k], max)]));
  if (!d.name || !isEmail(d.email)) {
    return res.status(400).json({ ok: false, error: 'Please add your name and a valid email.' });
  }

  const token = process.env.ARENA_SLACK_BOT_TOKEN;
  // Preview deployments often lack the Slack token. Email contact@ via Resend when
  // configured so one delivery channel still succeeds (client also posts FormSubmit).
  if (!token) {
    const mailed = await emailTeam(d);
    if (mailed) return res.status(200).json({ ok: true, via: 'email' });
    console.error('interest: ARENA_SLACK_BOT_TOKEN is not set and Resend email fallback failed or is unset');
    return res.status(500).json({ ok: false, error: 'Notification is not configured.' });
  }

  try {
    const r = await fetch('https://slack.com/api/chat.postMessage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ channel: process.env.ARENA_SLACK_CHANNEL || DEFAULT_CHANNEL, text: slackText(d), unfurl_links: false }),
    });
    const out = await r.json();
    if (!out.ok) {
      console.error('interest: slack error', out.error);
      const mailed = await emailTeam(d);
      if (mailed) return res.status(200).json({ ok: true, via: 'email' });
      return res.status(502).json({ ok: false, error: 'Could not notify the team.' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('interest: slack request failed', err && err.message);
    const mailed = await emailTeam(d);
    if (mailed) return res.status(200).json({ ok: true, via: 'email' });
    return res.status(502).json({ ok: false, error: 'Could not notify the team.' });
  }
};

module.exports._test = { clean, esc, isEmail, rateLimited, slackText };
