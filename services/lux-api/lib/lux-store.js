const { put, list, get } = require('@vercel/blob');
const { randomUUID } = require('node:crypto');
const PREFIX = 'lux-winter-2026/responses/';
function options() {
  const token = process.env.LUX_BLOB_READ_WRITE_TOKEN;
  if (!token) throw new Error('Lux response storage is not configured');
  return { token };
}
async function saveResponse(answers, metadata = {}) {
  const record = { version: 1, id: metadata.id || randomUUID(), submittedAt: metadata.submittedAt || new Date().toISOString(), answers };
  await put(PREFIX + record.id + '.json', JSON.stringify(record), {
    ...options(), access: 'private', addRandomSuffix: false,
    contentType: 'application/json', allowOverwrite: false,
  });
  return record;
}
async function readResponses() {
  const blobs = []; let cursor;
  do {
    const page = await list({ ...options(), prefix: PREFIX, limit: 1000, cursor });
    blobs.push(...page.blobs); cursor = page.hasMore ? page.cursor : undefined;
  } while (cursor);
  const records = [];
  // Bounded concurrency avoids a burst of one request per student.
  for (let i = 0; i < blobs.length; i += 10) {
    records.push(...await Promise.all(blobs.slice(i, i + 10).map(async b => {
      const result = await get(b.pathname, { ...options(), access: 'private', useCache: false });
      if (!result || result.statusCode !== 200) throw new Error('A response could not be loaded');
      const record = await new Response(result.stream).json();
      if (record.version !== 1 || !record.answers || !record.submittedAt) throw new Error('Invalid stored response');
      return record;
    })));
  }
  return records.sort((a,b) => b.submittedAt.localeCompare(a.submittedAt));
}
module.exports = { saveResponse, readResponses, PREFIX };
