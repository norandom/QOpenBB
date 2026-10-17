import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';

const base = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(base, '../..');
const prefix = 'artifacts/ui-parity-legend-fixed-relay-plan/';
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const read = relative => fs.readFileSync(path.join(root, relative));
const json = relative => JSON.parse(read(relative));
const checks = [];
function check(name, action) { action(); checks.push(name); }
function verify(entry) {
  assert(!path.isAbsolute(entry.sourcePath));
  assert(!entry.sourcePath.split('/').includes('..'));
  assert(!fs.lstatSync(path.join(root, entry.sourcePath)).isSymbolicLink());
  const bytes = read(entry.sourcePath);
  assert.equal(hash(bytes), entry.sha256, entry.sourcePath);
  assert.equal(bytes.length, entry.bytes, entry.sourcePath);
}
check('Exact controller-supplied plan, manifest and allowlist hashes', () => {
  assert.equal(hash(read(prefix + 'plan.md')), '1c9a0e527acb77b808aab703df19ef8f6f8eacb1ed325987e51a5ea071703e65');
  assert.equal(hash(read(prefix + 'source-hashes.json')), '98360c3c412f13396f548c9b9af27fa2b20eb64f8a4f05b6b71d3886218fe13a');
  assert.equal(hash(read(prefix + 'publication-allowlist.json')), 'ad082fed6d7ee2aeeda18bc7b4e317c3d8645933bab1f9c03b830ee54f3aa819');
});
const manifest = json(prefix + 'source-hashes.json');
const selection = json(prefix + 'publication-allowlist.json');
check('All six publication files and fourteen frozen local references', () => {
  assert.equal(selection.length, 6);
  assert.equal(new Set(selection.map(e => e.sourcePath)).size, 6);
  assert.equal(manifest.sourceFiles.length + manifest.inputs.length, 14);
  [...selection, ...manifest.sourceFiles, ...manifest.inputs].forEach(verify);
  assert(selection.every(e => e.sourcePath.startsWith(prefix)));
  assert.deepEqual(selection.slice(0, 5), manifest.sourceFiles);
});
let dockerfile, supervisor;
check('Two immutable Git blobs and supported Python runtime candidate', () => {
  const texts = manifest.gitSources.map(entry => {
    assert.equal(entry.repository, 'vendor/workspace');
    assert.equal(entry.revision, '38dffc33389aca0e4a87e0e88d42f7067aa220df');
    assert(['lite/Dockerfile', 'lite/supervisord.conf'].includes(entry.path));
    const bytes = execFileSync('git', ['-C', path.join(root, entry.repository), 'show', entry.revision + ':' + entry.path], {windowsHide: true, maxBuffer: 262144});
    assert.equal(hash(bytes), entry.sha256);
    assert.equal(bytes.length, entry.bytes);
    return bytes.toString('utf8');
  });
  assert.equal(texts.length, 2);
  [dockerfile, supervisor] = texts;
  assert(dockerfile.includes('FROM docker.io/library/python:3.13.15-slim-bookworm@sha256:'));
  const finalStage = dockerfile.split('FROM python-base AS runtime')[1];
  assert(finalStage.includes('COPY --from=backend-compile $VENV_PATH $VENV_PATH'));
  assert(finalStage.includes('COPY --from=frontend-build /app/dist /usr/share/nginx/html'));
  assert(!finalStage.includes('/usr/local/bin/node'));
  assert(supervisor.includes('command=/opt/.venv/bin/python -m uvicorn'));
  assert.deepEqual(json(prefix + 'runtime-evaluation.json').gitSources, manifest.gitSources);
});
const contract = json(prefix + 'probe-contract.json');
check('Single-instance no-browser topology and unchanged image identity', () => {
  assert.deepEqual(contract.resources, {appContainers: 1, relayContainers: 1, internalNetworks: 1, ordinaryIngressNetworks: 1, browserProcesses: 0, restarts: 0, recreations: 0});
  assert.equal(contract.network.appAttachedNetworks, 1);
  assert.equal(contract.network.relayAttachedNetworks, 2);
  assert.equal(contract.network.appPublishedPorts, 0);
  assert.equal(contract.network.relayHostIp, '127.0.0.1');
  assert.equal(contract.network.fixedUpstreamPort, 3000);
  for (const key of ['ipv6', 'ipForwarding', 'dnsForUpstream']) assert.equal(contract.network[key], false);
  const observed = json('artifacts/ui-parity-legend-startup-diagnostic/analysis-attempt-20261017T1615437-672fb2a3/observations.json');
  assert.equal(contract.image, observed.rawResult.image);
  assert.equal(contract.originalSource, observed.rawResult.originalSource);
});
check('Exact finite probe limits and readiness arithmetic', () => {
  assert.deepEqual(contract.relayProbeLimits, {maximumConcurrentPairs: 4, maximumAcceptedPairs: 16, maximumProcessSocketsIncludingListener: 9, bufferBytesPerDirection: 65536, maximumBytesPerPair: 4194304, maximumTotalForwardedBytesBothDirections: 33554432, connectTimeoutMs: 2000});
  assert.deepEqual(contract.deadlinesMs, {input: 90000, cleanup: 60000, hard: 150000});
  const r = contract.readiness;
  assert.deepEqual(r, {maximumHealthGets: 10, minimumStartSpacingMs: 3000, windowMsAfterRelayPublication: 30000, requestMs: 2000, endpoint: '/api/health', redirects: 0, rejectAny3xxOrLocation: true, sameInstanceOnly: true});
  assert((r.maximumHealthGets - 1) * r.minimumStartSpacingMs + r.requestMs <= r.windowMsAfterRelayPublication);
  assert.equal(2 * contract.relayProbeLimits.maximumConcurrentPairs + 1, 9);
  assert.deepEqual(contract.outputs, {files: 32, retainedBytes: 2097152, publicJsonBytes: 524288, publicJsonFileBytes: 65536, stringChars: 128});
  assert.equal(contract.runtimeExecuted, false);
  assert.equal(contract.runtimeCandidate.exactImageInterpreterAdmission, 'unverified');
});
check('Plan local links resolve and selected public files have no concrete common secret markers', () => {
  const plan = read(prefix + 'plan.md').toString('utf8');
  for (const match of plan.matchAll(/\]\(([^)]+)\)/g)) {
    if (/^https:\/\//.test(match[1])) continue;
    assert(fs.existsSync(path.resolve(root, prefix, match[1])), match[1]);
  }
  for (const item of selection) {
    const value = read(item.sourcePath).toString('utf8');
    assert(!/\b(?:TODO|TBD|FIXME|HACK|XXX)\b/.test(value), item.sourcePath);
    assert(!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/.test(value), item.sourcePath);
    assert(!/\b(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}|AKIA[A-Z0-9]{16})\b/.test(value), item.sourcePath);
  }
});
check('Reviewed plan allowlist is byte-identical and review links resolve', () => {
  assert(fs.readFileSync(path.join(base, 'reviewed-plan-publication-allowlist.json')).equals(read(prefix + 'publication-allowlist.json')));
  for (const match of fs.readFileSync(path.join(base, 'review.md'), 'utf8').matchAll(/\]\(([^)]+)\)/g)) {
    if (/^https:\/\//.test(match[1])) continue;
    if (match[1] === 'verification.json' && process.argv.includes('--write-receipt')) continue;
    assert(fs.existsSync(path.resolve(base, match[1])), match[1]);
  }
});
const receipt = {status: 'passed-source-only-plan-review-checks', node: process.version, checks, groupedChecks: checks.length, runtimeExecuted: false, suppliedFreezeScriptExecuted: false, externalDocumentationFetched: false, secretScanScope: 'Six selected files; bounded common-token and private-key markers plus manual review, not proof against every secret format', productionCaps: 'Research exclusion; future maintained 400 physical/file, 300 logical/file, 50/function with inventory/checker', command: 'node artifacts/ui-parity-legend-fixed-relay-plan-review/audit.mjs', exitCode: 0};
if (process.argv.includes('--write-receipt')) fs.writeFileSync(path.join(base, 'verification.json'), JSON.stringify(receipt, null, 2) + '\n');
else assert.deepEqual(JSON.parse(fs.readFileSync(path.join(base, 'verification.json'))), receipt);
console.log(JSON.stringify(receipt));
