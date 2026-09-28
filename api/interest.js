// POST /api/interest: one-page overview requests from program pages -> Arena Slack.
// Email notification goes separately (client posts to FormSubmit), so Slack failing
// never blocks the visitor. Env: ARENA_SLACK_BOT_TOKEN (required),
// ARENA_SLACK_CHANNEL (optional, defaults to #schools).
const DEFAULT_CHANNEL = 'C0C4KRP3WDR'; // #schools in the Arena School workspace
const LIMITS = { name: 120, email: 200, role: 60, school: 160, program: 80, page: 200 };
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
    `*New one-pager request* · ${esc(d.program || 'Program page')}`,
    `*${esc(d.name)}* · ${esc(d.email)}`,
    d.role && `Role: ${esc(d.role)}`,
    d.school && `School: ${esc(d.school)}`,
    d.page && `From: ${esc(d.page)}`,
  ];
  return lines.filter(Boolean).join('\n');
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
  if (!token) {
    console.error('interest: ARENA_SLACK_BOT_TOKEN is not set');
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
      return res.status(502).json({ ok: false, error: 'Could not notify the team.' });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('interest: slack request failed', err && err.message);
    return res.status(502).json({ ok: false, error: 'Could not notify the team.' });
  }
};

module.exports._test = { clean, esc, isEmail, rateLimited, slackText };
