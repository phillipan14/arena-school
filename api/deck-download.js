// POST /api/deck-download: talk download gate (talks/<slug>/download) -> Arena Slack lead, then the file links.
// Body: { name, institution, email, talk, page, _honey }. All of name, institution, and a valid email are required.
// Env: ARENA_SLACK_BOT_TOKEN, ARENA_LEADS_CHANNEL (optional, defaults to #conferences).
// The visitor always gets the links once the form is valid: if Slack is unset or fails, the error is logged
// and the response is still ok (notified: false), so a talk audience is never locked out of the slides.
const DEFAULT_CHANNEL = 'C0C4VSSDZK6'; // #conferences in the Arena School workspace
const LIMITS = { name: 120, institution: 160, email: 200, talk: 80, page: 200 };
const WINDOW_MS = 10 * 60 * 1000;
// A conference room shares one Wi-Fi IP, so the tight cap is per person (IP + email) and the IP cap is loose.
const MAX_PER_PERSON = 5;
const MAX_PER_IP = 60;
const hits = new Map(); // best-effort, per warm instance

const TALKS = {
  '2026-10-acamis-tech-workshop': {
    title: 'From Lab to Classroom (ACAMIS Technology Conference, Oct 18, 2026)',
    links: [
      { id: 'slides', label: 'Slides (PDF)', href: '/talks/2026-10-acamis-tech-workshop/slides-en.pdf' },
      { id: 'guide', label: 'China AI tool guide (PDF)', href: '/talks/2026-10-acamis-tech-workshop/china-ai-tool-guide.pdf' },
      { id: 'deck', label: 'Web deck', href: '/talks/2026-10-acamis-tech-workshop/deck' },
      { id: 'reader', label: 'Phone reader', href: '/talks/2026-10-acamis-tech-workshop/read/en' },
      { id: 'build', label: 'What we built in the session', href: '/talks/2026-10-acamis-tech-workshop/build' },
      { id: 'session', label: 'Session page and planning checklist', href: '/talks/2026-10-acamis-tech-workshop' },
    ],
  },
};
const DEFAULT_TALK = '2026-10-acamis-tech-workshop';

const clean = (v, max) => String(v == null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, max);
// Escape Slack control characters so input can't ping @channel or inject links.
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const isEmail = (s) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(s);

function parseBody(body) {
  if (body && typeof body === 'object') return body;
  try { return JSON.parse(body || '{}'); } catch { return {}; }
}

function over(key, max, now) {
  const recent = (hits.get(key) || []).filter((t) => now - t < WINDOW_MS);
  hits.set(key, [...recent, now]);
  return recent.length >= max;
}

function rateLimited(ip, email, now = Date.now()) {
  const person = over(`p:${ip}:${email.toLowerCase()}`, MAX_PER_PERSON, now);
  const room = over(`ip:${ip}`, MAX_PER_IP, now);
  return person || room;
}

function stamp(date) {
  const bj = date.toLocaleString('en-US', { timeZone: 'Asia/Shanghai', dateStyle: 'medium', timeStyle: 'short' });
  return `${bj} Beijing (${date.toISOString()})`;
}

function slackText(d, talk, at) {
  return [
    `*New deck download* · ${esc(talk.title)}`,
    `*${esc(d.name)}* · ${esc(d.email)}`,
    `Institution: ${esc(d.institution)}`,
    `Talk: ${esc(d.talk)}`,
    `At: ${esc(stamp(at))}`,
  ].join('\n');
}

async function notifySlack(d, talk, at) {
  const token = process.env.ARENA_SLACK_BOT_TOKEN;
  if (!token) {
    console.error('deck-download: ARENA_SLACK_BOT_TOKEN is not set; lead not posted', d.talk);
    return false;
  }
  try {
    const r = await fetch('https://slack.com/api/chat.postMessage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ channel: process.env.ARENA_LEADS_CHANNEL || DEFAULT_CHANNEL, text: slackText(d, talk, at), unfurl_links: false }),
    });
    const out = await r.json();
    if (!out.ok) {
      console.error('deck-download: slack error', out.error);
      return false;
    }
    return true;
  } catch (err) {
    console.error('deck-download: slack request failed', err && err.message);
    return false;
  }
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }
  const body = parseBody(req.body);
  const d = Object.fromEntries(Object.entries(LIMITS).map(([k, max]) => [k, clean(body[k], max)]));
  d.talk = d.talk || DEFAULT_TALK;
  const talk = TALKS[d.talk];
  if (!talk) return res.status(400).json({ ok: false, error: 'Unknown talk.' });
  if (body._honey) return res.status(200).json({ ok: true, links: talk.links }); // bot: pretend success

  if (!d.name || !d.institution || !isEmail(d.email)) {
    return res.status(400).json({ ok: false, error: 'Please add your name, your institution, and a valid email.' });
  }

  const ip = clean(String(req.headers['x-forwarded-for'] || '').split(',')[0], 64) || 'unknown';
  if (rateLimited(ip, d.email)) return res.status(429).json({ ok: false, error: 'Too many requests. Please try again later.' });

  const notified = await notifySlack(d, talk, new Date());
  return res.status(200).json({ ok: true, notified, links: talk.links });
};

module.exports._test = { clean, esc, isEmail, rateLimited, slackText, stamp, hits, TALKS };
