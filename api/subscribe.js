// POST /api/subscribe: "Arena Notes" newsletter sign-ups -> Resend contact (+ segment), then a short
// bilingual welcome email once the sending domain is verified. Same shape as /api/interest.
// Program forms (one-pager / interest / contact) also post here with quiet: true, so every email we
// collect lands in the same Arena Notes list; quiet skips the welcome email and the Slack ping (those
// forms already notify the team). Env: RESEND_API_KEY (required, "Full access"), RESEND_SEGMENT_ID (required),
//      Resend contact properties role, lang, source must exist in the account (created 2026-10-13),
//      RESEND_FROM (optional; e.g. "Arena School <notes@arenaschool.org>"; no welcome email until set),
//      ARENA_SLACK_BOT_TOKEN + ARENA_NEWSLETTER_SLACK_CHANNEL (optional one-line ping; never includes the email).
const RESEND = 'https://api.resend.com';
const LIMITS = { email: 200, role: 20, lang: 5, source: 60, page: 200 };
const ROLES = ['parent', 'student', 'educator', 'other'];
const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_WINDOW = 5;
const hits = new Map(); // best-effort, per warm instance

// Program forms use their own role labels ("School leader", "Teacher or counselor", "家长", ...).
function mapRole(r) {
  const v = String(r || '').toLowerCase();
  if (ROLES.includes(v)) return v;
  if (!v) return '';
  if (/parent|家长/.test(v)) return 'parent';
  if (/student|学生/.test(v)) return 'student';
  if (/school|teacher|counsel|educator|organizer|board|老师|教师|学校|校长|教育/.test(v)) return 'educator';
  return 'other';
}

const clean = (v, max) => String(v == null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, max);
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

async function resend(path, method, key, payload) {
  const r = await fetch(RESEND + path, {
    method,
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: payload ? JSON.stringify(payload) : undefined,
  });
  let out = {};
  try { out = await r.json(); } catch {}
  return { status: r.status, ok: r.ok, out };
}

// Look the contact up first. Resend's POST /contacts updates an existing contact (and would flip
// "unsubscribed" back to false), so an existing contact is only added to the segment: someone who
// unsubscribed is never re-subscribed, and nobody gets a second welcome email.
async function saveContact(d, key, segment) {
  const props = { role: d.role || 'unknown', lang: d.lang, source: d.source || 'site' };
  const found = await resend(`/contacts/${encodeURIComponent(d.email)}`, 'GET', key);
  if (found.ok && found.out && found.out.email) {
    const add = await resend(`/contacts/${encodeURIComponent(d.email)}/segments/${encodeURIComponent(segment)}`, 'POST', key);
    if (add.ok || add.status === 409 || add.status === 422) return { created: false };
    throw new Error(`segment add failed ${add.status}`);
  }
  if (found.status !== 404) throw new Error(`contact lookup failed ${found.status}`);
  const made = await resend('/contacts', 'POST', key, { email: d.email, unsubscribed: false, properties: props, segments: [{ id: segment }] });
  if (made.ok) return { created: true };
  throw new Error(`contact create failed ${made.status} ${JSON.stringify(made.out).slice(0, 200)}`);
}

function welcome(lang) {
  const zh = lang === 'zh';
  const subject = zh ? '欢迎订阅 Arena 通讯' : 'Welcome to Arena Notes';
  const lines = zh
    ? ['感谢订阅 Arena 通讯。', '我们会在通讯里分享新开的项目、即将举办的讲座，以及我们对孩子与AI的观察。', '任何问题都可以直接回复这封邮件。每封通讯底部都有退订链接。', 'Arena School 团队']
    : ['Thanks for subscribing to Arena Notes.', 'We’ll write about the programs we’re opening, the talks we’re giving, and what we’re learning about kids and AI.', 'Questions? Just reply to this email. Every newsletter has an unsubscribe link at the bottom.', 'The Arena School team'];
  const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const html = `<div style="font:16px/1.6 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#1F2A44;max-width:520px">${lines
    .map((l, i) => `<p style="margin:0 0 14px${i === lines.length - 1 ? ';color:#4A5470' : ''}">${esc(l)}</p>`).join('')}
    <p style="margin:22px 0 0;font-size:13px;color:#6B7287"><a href="https://arenaschool.org${zh ? '/index-cn' : '/'}" style="color:#22458A">arenaschool.org</a></p></div>`;
  return { subject, html, text: lines.join('\n\n') + '\n\nhttps://arenaschool.org' };
}

async function ping(d) {
  const token = process.env.ARENA_SLACK_BOT_TOKEN, channel = process.env.ARENA_NEWSLETTER_SLACK_CHANNEL;
  if (!token || !channel) return;
  try {
    await fetch('https://slack.com/api/chat.postMessage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json; charset=utf-8', Authorization: `Bearer ${token}` },
      body: JSON.stringify({ channel, text: `New Arena Notes subscriber · ${d.role || 'no role'} · ${d.lang.toUpperCase()} · from ${d.source || d.page || 'site'}`, unfurl_links: false }),
    });
  } catch {}
}

module.exports = async function handler(req, res) {
  // GET: lets the page show the sign-up only once Resend is configured on this deployment
  if (req.method === 'GET') {
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ configured: !!(process.env.RESEND_API_KEY && process.env.RESEND_SEGMENT_ID) });
  }
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }
  const body = parseBody(req.body);
  if (body._honey) return res.status(200).json({ ok: true }); // bot: pretend success

  const ip = clean(String(req.headers['x-forwarded-for'] || '').split(',')[0], 64) || 'unknown';
  if (rateLimited(ip)) return res.status(429).json({ ok: false, error: 'Too many requests. Please try again later.' });

  const d = Object.fromEntries(Object.entries(LIMITS).map(([k, max]) => [k, clean(body[k], max)]));
  d.email = d.email.toLowerCase();
  d.lang = d.lang === 'zh' ? 'zh' : 'en';
  d.role = mapRole(body.role);
  const quiet = body.quiet === true || body.quiet === 1 || body.quiet === '1';
  if (!isEmail(d.email)) return res.status(400).json({ ok: false, error: d.lang === 'zh' ? '请填写有效的邮箱。' : 'Please add a valid email.' });

  const key = process.env.RESEND_API_KEY, segment = process.env.RESEND_SEGMENT_ID;
  if (!key || !segment) {
    console.error('subscribe: RESEND_API_KEY or RESEND_SEGMENT_ID is not set');
    return res.status(500).json({ ok: false, error: 'Sign-up is not configured yet.' });
  }

  try {
    const { created } = await saveContact(d, key, segment);
    const from = process.env.RESEND_FROM;
    if (created && from && !quiet) {
      const w = welcome(d.lang);
      const sent = await resend('/emails', 'POST', key, { from, to: [d.email], reply_to: 'contact@arenaschool.org', subject: w.subject, html: w.html, text: w.text });
      if (!sent.ok) console.error('subscribe: welcome failed', sent.status, JSON.stringify(sent.out).slice(0, 200));
    }
    if (!quiet) await ping(d);
    return res.status(200).json({ ok: true, created });
  } catch (err) {
    console.error('subscribe:', err && err.message);
    return res.status(502).json({ ok: false, error: d.lang === 'zh' ? '暂时无法订阅，请稍后再试。' : 'Could not subscribe right now. Please try again.' });
  }
};

module.exports._test = { clean, isEmail, rateLimited, welcome, saveContact, mapRole };
