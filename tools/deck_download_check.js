// Offline check for api/deck-download.js: mock req/res, Slack stubbed. Usage: node tools/deck_download_check.js
const assert = require('assert');
const path = require('path');

let slackCalls = [];
let slackReply = { ok: true };
global.fetch = async (url, opts) => {
  slackCalls.push({ url, body: JSON.parse(opts.body), auth: opts.headers.Authorization });
  if (slackReply instanceof Error) throw slackReply;
  return { json: async () => slackReply };
};

const handler = require(path.join(__dirname, '..', 'api', 'deck-download.js'));
const { hits } = handler._test;

function call(body, { method = 'POST', ip = '203.0.113.7' } = {}) {
  return new Promise((resolve) => {
    const res = {
      code: 200, headers: {},
      setHeader(k, v) { this.headers[k] = v; },
      status(c) { this.code = c; return this; },
      json(j) { resolve({ code: this.code, body: j, headers: this.headers }); },
    };
    handler({ method, body, headers: { 'x-forwarded-for': ip } }, res);
  });
}

const valid = { name: 'Ada Lovelace', institution: 'International School of Beijing', email: 'ada@example.org', talk: '2026-10-acamis-tech-workshop' };
const reset = () => { slackCalls = []; slackReply = { ok: true }; hits.clear(); };

(async () => {
  process.env.ARENA_SLACK_BOT_TOKEN = 'xoxb-test';
  delete process.env.ARENA_LEADS_CHANNEL;

  reset();
  let r = await call(valid);
  assert.strictEqual(r.code, 200); assert.strictEqual(r.body.ok, true); assert.strictEqual(r.body.notified, true);
  assert.deepStrictEqual(r.body.links.map((l) => l.id), ['slides', 'guide', 'deck', 'reader', 'build', 'session']);
  assert.strictEqual(slackCalls.length, 1);
  assert.strictEqual(slackCalls[0].body.channel, 'C0C4VSSDZK6');
  for (const s of ['Ada Lovelace', 'International School of Beijing', 'ada@example.org', '2026-10-acamis-tech-workshop', 'Beijing (20']) assert.ok(slackCalls[0].body.text.includes(s), s);
  console.log('ok  valid submit posts to #conferences and returns 6 links');

  reset(); process.env.ARENA_LEADS_CHANNEL = 'C_OVERRIDE';
  await call(valid); assert.strictEqual(slackCalls[0].body.channel, 'C_OVERRIDE'); delete process.env.ARENA_LEADS_CHANNEL;
  console.log('ok  ARENA_LEADS_CHANNEL overrides the channel');

  for (const miss of ['name', 'institution', 'email']) {
    reset();
    r = await call({ ...valid, [miss]: '  ' });
    assert.strictEqual(r.code, 400, miss); assert.strictEqual(r.body.ok, false); assert.strictEqual(slackCalls.length, 0);
  }
  console.log('ok  missing name / institution / email -> 400, no Slack post');

  for (const bad of ['ada', 'ada@', 'ada@example', 'a da@example.org', '@example.org']) {
    reset(); r = await call({ ...valid, email: bad });
    assert.strictEqual(r.code, 400, bad); assert.strictEqual(slackCalls.length, 0);
  }
  console.log('ok  bad emails -> 400');

  reset(); r = await call({ ...valid, _honey: 'http://spam.example' });
  assert.strictEqual(r.code, 200); assert.strictEqual(r.body.ok, true); assert.strictEqual(slackCalls.length, 0);
  console.log('ok  honeypot -> silent 200, no Slack post');

  reset(); r = await call({ ...valid, talk: 'not-a-talk' });
  assert.strictEqual(r.code, 400);
  console.log('ok  unknown talk -> 400');

  reset(); r = await call({ ...valid, name: '<!channel> <https://evil.example|click> & co' });
  assert.ok(!slackCalls[0].body.text.includes('<!channel>')); assert.ok(slackCalls[0].body.text.includes('&lt;!channel&gt;'));
  console.log('ok  Slack control characters escaped');

  reset(); r = await call(JSON.stringify(valid));
  assert.strictEqual(r.code, 200);
  console.log('ok  string JSON body parsed');

  reset(); r = await call(valid, { method: 'GET' });
  assert.strictEqual(r.code, 405); assert.strictEqual(r.headers.Allow, 'POST');
  console.log('ok  GET -> 405');

  reset(); slackReply = { ok: false, error: 'channel_not_found' };
  r = await call(valid); assert.strictEqual(r.code, 200); assert.strictEqual(r.body.ok, true); assert.strictEqual(r.body.notified, false); assert.ok(r.body.links.length);
  reset(); slackReply = new Error('ECONNRESET');
  r = await call(valid); assert.strictEqual(r.code, 200); assert.strictEqual(r.body.notified, false);
  reset(); delete process.env.ARENA_SLACK_BOT_TOKEN;
  r = await call(valid); assert.strictEqual(r.code, 200); assert.strictEqual(r.body.notified, false); assert.strictEqual(slackCalls.length, 0);
  process.env.ARENA_SLACK_BOT_TOKEN = 'xoxb-test';
  console.log('ok  Slack error / network failure / missing token -> still 200 with links (notified:false)');

  reset();
  const codes = [];
  for (let i = 0; i < 6; i++) codes.push((await call(valid)).code);
  assert.deepStrictEqual(codes, [200, 200, 200, 200, 200, 429]);
  r = await call({ ...valid, email: 'colleague@example.org' });
  assert.strictEqual(r.code, 200);
  console.log('ok  rate limit is per person: 6th from same email -> 429, a colleague on the same Wi-Fi still gets in');

  reset();
  for (let i = 0; i < 60; i++) await call({ ...valid, email: `p${i}@example.org` });
  r = await call({ ...valid, email: 'p61@example.org' });
  assert.strictEqual(r.code, 429);
  console.log('ok  per-IP cap (60 per 10 min) -> 429');

  console.log('\nall deck-download checks passed');
})().catch((e) => { console.error('FAIL', e); process.exit(1); });
