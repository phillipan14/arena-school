const crypto = require('node:crypto');
const COOKIE = '__Host-lux_results';
const AGE = 8 * 3600;
function equal(a,b) {
  const x = Buffer.from(a || ''), y = Buffer.from(b || '');
  return x.length === y.length && crypto.timingSafeEqual(x,y);
}
function passwordMatches(password) {
  if (typeof password !== 'string' || password.length > 200) return false;
  const [salt, expected] = (process.env.LUX_RESULTS_PASSWORD_HASH || '').split(':');
  if (!salt || !expected) return false;
  return equal(crypto.scryptSync(password, salt, 32).toString('hex'), expected);
}
function sign(payload) {
  if (!process.env.LUX_SESSION_SECRET) throw new Error('Session secret missing');
  return crypto.createHmac('sha256', process.env.LUX_SESSION_SECRET).update(payload).digest('base64url');
}
function sessionCookie(now = Date.now()) {
  const payload = Buffer.from(JSON.stringify({ expires: now + AGE * 1000, nonce: crypto.randomBytes(12).toString('hex') })).toString('base64url');
  return `${COOKIE}=${payload}.${sign(payload)}; Path=/; Max-Age=${AGE}; HttpOnly; Secure; SameSite=Strict`;
}
function authorized(req, now = Date.now()) {
  if (!process.env.LUX_SESSION_SECRET) return false;
  const raw = (req.headers.cookie || '').split(';').map(x=>x.trim()).find(x=>x.startsWith(COOKIE+'='));
  if (!raw) return false;
  const [payload, signature, extra] = raw.slice(COOKIE.length+1).split('.');
  if (!payload || extra || !equal(signature, sign(payload))) return false;
  try { const exp = JSON.parse(Buffer.from(payload,'base64url')).expires; return Number.isFinite(exp) && exp > now && exp <= now + AGE * 1000; } catch { return false; }
}
function logoutCookie() { return `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Strict`; }
function sameOrigin(req) { return req.headers.origin === 'https://arenaschool.org' || req.headers.origin === 'https://www.arenaschool.org'; }
module.exports = { authorized, passwordMatches, sessionCookie, logoutCookie, sameOrigin };
