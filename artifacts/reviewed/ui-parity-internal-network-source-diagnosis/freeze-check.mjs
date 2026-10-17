import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
const dir = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(dir, '../..');
const allow = JSON.parse(fs.readFileSync(path.join(dir, 'publication-allowlist.json')));
const seen = new Set();
for (const f of allow.files) {
  assert.ok(!seen.has(f.sourcePath)); seen.add(f.sourcePath);
  const resolved = path.resolve(root, f.sourcePath);
  assert.ok(resolved.startsWith(dir + path.sep));
  const bytes = fs.readFileSync(resolved);
  assert.equal(bytes.length, f.bytes);
  assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'), f.sha256);
}
console.log(JSON.stringify({ passed: true, allowlistedFiles: seen.size, sha256AndBytesChecks: seen.size * 2 }));
