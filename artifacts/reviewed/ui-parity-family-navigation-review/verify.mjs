import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';

const root = process.cwd();
const lane = 'artifacts/ui-parity-family-navigation-review';
const planLane = 'artifacts/ui-parity-family-navigation-plan';
const read = name => fs.readFileSync(path.join(root, name));
const json = name => JSON.parse(read(name));
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const identity = name => {
  const bytes = read(name);
  return { sourcePath: name, sha256: sha(bytes), bytes: bytes.length };
};
const manifest = json(`${planLane}/source-hashes.json`);
const planAllowlist = json(`${planLane}/publication-allowlist.json`);
const checks = [];
for (const bucket of ['inputs', 'originalSource', 'installedSourceClues']) {
  for (const input of manifest[bucket]) {
    const bytes = bucket === 'originalSource'
      ? execFileSync('git', ['-C', input.repository, 'show', `${input.revision}:${input.path}`])
      : read(input.path);
    assert.equal(sha(bytes), input.sha256, input.path);
    assert.equal(bytes.length, input.bytes, input.path);
    checks.push({ path: input.path, kind: input.kind, sha256: sha(bytes), bytes: bytes.length });
  }
}
for (const entry of planAllowlist.entries) {
  assert.deepEqual(identity(entry.sourcePath), {
    sourcePath: entry.sourcePath, sha256: entry.sha256, bytes: entry.bytes,
  });
}
const plan = read(`${planLane}/plan.md`).toString('utf8');
const rows = plan.split(/\r?\n/).filter(line => /^\| (Column|Bar|Pie|Line|Area|X Y \(Scatter\)|Polar|Statistical|Hierarchical|Specialized|Funnel|Combination) \|/.test(line));
const plannedButtons = rows.flatMap(line => line.split('|')[2].trim().split('; '));
const inventory = json('artifacts/reviewed/parity/chart-editor-capture/control-inventory.json');
const buttons = inventory['chart-panel'].controls.filter(control => control.type === 'button');
assert.equal(rows.length, 12);
assert.equal(buttons.length, 34);
assert.deepEqual(plannedButtons, buttons.map(button => button.label));
assert(buttons.every(button => button.visible === true));
const entered = json('artifacts/reviewed/ui-parity-navigation/run-20261017-r1-a4/N01-chart-entered.json');
const range = entered.chart.model.cellRange;
for (const key of ['rowStartIndex', 'rowStartPinned', 'rowEndIndex', 'rowEndPinned']) {
  assert(Object.hasOwn(range, key));
  assert.equal(range[key], null);
}
assert.deepEqual(range.columns, ['period', 'revenue', 'operatingIncome']);
assert.deepEqual([...plan.matchAll(/^\| (F0[1-8]) \|/gm)].map(match => match[1]),
  ['F01', 'F02', 'F03', 'F04', 'F05', 'F06', 'F07', 'F08']);
assert.equal(json('.kiro/specs/openbb-self-service/spec.json').language, 'en');
for (const name of manifest.coreSteeringAbsent) {
  assert.equal(fs.existsSync(path.join(root, '.kiro/steering', name)), false);
}
const ownPayloads = ['review.md', 'verify.mjs', 'verification.json'];
const proposed = new Map(planAllowlist.entries.map(entry => [entry.publishedPath, entry.sourcePath]));
proposed.set(`artifacts/reviewed/ui-parity-family-navigation-plan/publication-allowlist.json`, `${planLane}/publication-allowlist.json`);
for (const name of [...ownPayloads, 'publication-allowlist.json']) {
  proposed.set(`artifacts/reviewed/ui-parity-family-navigation-review/${name}`, `${lane}/${name}`);
}
const links = [];
for (const [file, published] of [
  [`${planLane}/plan.md`, 'artifacts/reviewed/ui-parity-family-navigation-plan/plan.md'],
  [`${lane}/review.md`, 'artifacts/reviewed/ui-parity-family-navigation-review/review.md'],
]) {
  for (const match of read(file).toString('utf8').matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
    const resolved = path.posix.normalize(path.posix.join(path.posix.dirname(published), match[1]));
    const source = proposed.get(resolved) ?? resolved;
    const pendingOwnMetadata = [`${lane}/verification.json`, `${lane}/publication-allowlist.json`].includes(source);
    assert(pendingOwnMetadata || fs.existsSync(path.join(root, source)), `${file}: ${resolved}`);
    links.push({ file, target: match[1], resolved, source, pendingOwnMetadata });
  }
}
const receipt = {
  schemaVersion: 1, date: '2026-10-17', status: 'pass-source-only',
  verdict: 'accept-for-collector-preparation', runtimeExecuted: false,
  command: `node ${lane}/verify.mjs`, exitCode: 0,
  originalRevision: manifest.original,
  maintainedClaimScopeInputs: ['.kiro/specs/openbb-self-service/chart-family-navigation-plan.md', '.kiro/specs/openbb-self-service/research.md', 'docs/index.md', '.kiro/breadth.toml'].map(identity),
  reviewedPlan: ['plan.md', 'source-hashes.json', 'publication-allowlist.json'].map(name => identity(`${planLane}/${name}`)),
  checks, inventory: { observedGroups: rows.length, observedButtons: buttons.length, exactNamesOrderVisible: true },
  sourceRange: range, futureCaseRows: 8, links,
  limits: 'Static evidence only; collector fit, seed admission, runtime behavior and cleanup remain unverified.',
  environmentNote: 'Initial python command could not run because python was unavailable; equivalent read-only checks used installed Node. First Node verifier run failed because its prospective-link mapping omitted the plan publication metadata; the mapping was corrected without changing frozen inputs. No application attempt occurred.',
};
fs.writeFileSync(path.join(root, lane, 'verification.json'), `${JSON.stringify(receipt, null, 2)}\n`);
const allowlist = {
  schemaVersion: 1, status: 'completed-independent-source-review; controller-publication-required',
  entries: ownPayloads.map(name => ({
    ...identity(`${lane}/${name}`), publishedPath: `artifacts/reviewed/ui-parity-family-navigation-review/${name}`,
    sanitization: 'none; source-only review and offline verification',
  })),
  excluded: ['publication-allowlist.json is metadata, not a recursively hashed payload', 'all runtime/private evidence', 'all dependency source payloads'],
};
fs.writeFileSync(path.join(root, lane, 'publication-allowlist.json'), `${JSON.stringify(allowlist, null, 2)}\n`);
console.log(JSON.stringify({ status: receipt.status, inputs: checks.length, planPayloads: planAllowlist.entries.length, links: links.length, buttons: buttons.length }));
