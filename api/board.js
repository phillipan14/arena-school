// /api/board: anonymous shared boards for the ACAMIS Teacher Toolbox (feedback, exit tickets, polls, Q&A).
// GET  /api/board?b=<board>          -> { ok, durable, items: [{ id, t, text, tag }] } newest first
// POST /api/board { b, text, tag? }  -> { ok, item }
// Text only: no names, emails, or logins. Each board keeps its newest 500 entries and expires
// 3 days after its last post. Storage: Upstash Redis REST (Vercel Storage integration) via
// KV_REST_API_URL + KV_REST_API_TOKEN (or UPSTASH_REDIS_REST_URL + UPSTASH_REDIS_REST_TOKEN).
// Without those env vars it falls back to memory in the warm instance (best effort, not durable).
const MAX_TEXT = 500, MAX_TAG = 40, MAX_ITEMS = 500, TTL_S = 3 * 24 * 3600;
const WINDOW_MS = 60 * 1000;
const MAX_PER_WINDOW = 120; // generous: a whole conference room can share one public IP
const hits = new Map(); // best-effort, per warm instance
const mem = new Map(); // fallback store when Redis isn't configured

const clean = (v, max) => String(v == null ? '' : v).replace(/[\u0000-\u0008\u000B-\u001F\u007F]/g, '').replace(/[ \t]+/g, ' ').trim().slice(0, max);
const boardOk = (b) => /^[a-z0-9][a-z0-9-]{1,39}$/.test(b);

function parseBody(body) {
  if (body && typeof body === 'object') return body;
  try { return JSON.parse(body || '{}'); } catch { return {}; }
}

function rateLimited(ip, now = Date.now()) {
  const recent = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  hits.set(ip, [...recent, now]);
  return recent.length >= MAX_PER_WINDOW;
}

function redisConfig() {
  const url = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
  return url && token ? { url: url.replace(/\/$/, ''), token } : null;
}

async function pipeline(cfg, cmds) {
  const r = await fetch(cfg.url + '/pipeline', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + cfg.token, 'Content-Type': 'application/json' },
    body: JSON.stringify(cmds),
  });
  if (!r.ok) throw new Error('redis ' + r.status);
  return r.json();
}

async function read(b) {
  const cfg = redisConfig(), key = 'toolbox:board:' + b;
  if (!cfg) return (mem.get(key) || []).slice(0, MAX_ITEMS);
  const [res] = await pipeline(cfg, [['LRANGE', key, '0', String(MAX_ITEMS - 1)]]);
  return (res.result || []).map((s) => { try { return JSON.parse(s); } catch { return null; } }).filter(Boolean);
}

async function write(b, item) {
  const cfg = redisConfig(), key = 'toolbox:board:' + b;
  if (!cfg) { mem.set(key, [item, ...(mem.get(key) || [])].slice(0, MAX_ITEMS)); return; }
  await pipeline(cfg, [['LPUSH', key, JSON.stringify(item)], ['LTRIM', key, '0', String(MAX_ITEMS - 1)], ['EXPIRE', key, String(TTL_S)]]);
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  const q = req.query || {};
  if (req.method === 'GET') {
    const b = clean(q.b, 40).toLowerCase();
    if (!boardOk(b)) return res.status(400).json({ ok: false, error: 'Unknown board.' });
    try { return res.status(200).json({ ok: true, durable: !!redisConfig(), items: await read(b) }); }
    catch (e) { return res.status(502).json({ ok: false, error: 'Board storage is unavailable.' }); }
  }
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'GET, POST');
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }
  const body = parseBody(req.body);
  if (body._honey) return res.status(200).json({ ok: true }); // bot: pretend success
  const ip = clean(String(req.headers['x-forwarded-for'] || '').split(',')[0], 64) || 'unknown';
  if (rateLimited(ip)) return res.status(429).json({ ok: false, error: 'Too many posts. Try again in a minute.' });
  const b = clean(body.b, 40).toLowerCase(), text = clean(body.text, MAX_TEXT), tag = clean(body.tag, MAX_TAG);
  if (!boardOk(b)) return res.status(400).json({ ok: false, error: 'Unknown board.' });
  if (!text) return res.status(400).json({ ok: false, error: 'Please write something first.' });
  const item = { id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), t: Date.now(), text, tag };
  try { await write(b, item); return res.status(200).json({ ok: true, durable: !!redisConfig(), item }); }
  catch (e) { return res.status(502).json({ ok: false, error: 'Board storage is unavailable.' }); }
};

module.exports._test = { clean, boardOk, rateLimited, hits, mem };
