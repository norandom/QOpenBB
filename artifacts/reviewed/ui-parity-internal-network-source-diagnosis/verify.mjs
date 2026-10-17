import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const dir = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const root = path.resolve(dir, '../..');
const read = p => fs.readFileSync(path.join(root, p));
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const checks = [];
function check(name, fn) { fn(); checks.push({ name, passed: true }); }
const manifest = JSON.parse(fs.readFileSync(path.join(dir, 'source-hashes.json')));
for (const f of manifest.files) check(`hash and bytes: ${f.sourcePath}`, () => {
  const b = read(f.sourcePath); assert.equal(sha(b), f.sha256); assert.equal(b.length, f.bytes);
});
const linkage = JSON.parse(fs.readFileSync(path.join(dir, 'version-linkage.json')));
check('official tag object resolves matching full commit', () => {
  const ref = JSON.parse(fs.readFileSync(path.join(dir, 'tag-ref.json')));
  const tag = JSON.parse(fs.readFileSync(path.join(dir, 'tag-object.json')));
  const release = JSON.parse(fs.readFileSync(path.join(dir, 'release.json')));
  assert.equal(ref.object.sha, linkage.tagObjectSha);
  assert.equal(tag.sha, linkage.tagObjectSha);
  assert.equal(tag.object.sha, linkage.commit);
  assert.equal(tag.object.type, 'commit');
  assert.equal(release.tag_name, linkage.tag);
  assert.equal(linkage.tag, 'docker-v29.7.2');
  assert.equal(linkage.tagObjectSha, 'd681cdaead9340bd36c513c7f5413a21bc679cfa');
  assert.equal(linkage.commit, '6a43e3d5afddf4111da0f864bbc7cae5d7e95001');
  assert.ok(linkage.commit.startsWith(linkage.controllerReportedDaemon.gitCommit));
});
const source = p => fs.readFileSync(path.join(dir, 'source', p), 'utf8');
const anchors = [
  ['daemon/network.go', 'if n.Internal() || len(getPortMapInfo(sb)) > 0 {'],
  ['daemon/network.go', 'pm[natPort] = nil'],
  ['daemon/container_operations.go', 'libnetwork.OptionPortMapping(publishedPorts)'],
  ['daemon/container_operations.go', 'ctr.NetworkSettings.Ports = getPortMapInfo(sb)'],
  ['daemon/libnetwork/default_gateway.go', 'if ep.getNetwork().Internal() {'],
  ['daemon/libnetwork/default_gateway.go', 'gw4, gw6 := ep.hasGatewayOrDefaultRoute()'],
  ['daemon/libnetwork/endpoint.go', 'ep.programExternalConnectivity(ctx, gwepAfter4, gwepAfter6)'],
  ['daemon/libnetwork/drivers/bridge/bridge_linux.go', 'if !network.config.Internal {'],
  ['daemon/libnetwork/drivers/bridge/bridge_linux.go', 'pbmReq := portBindingMode{routed: true}'],
  ['daemon/libnetwork/drivers/bridge/bridge_linux.go', 'if gw6Id == eid || (gw6Id == "" && gw4Id == eid) {'],
  ['daemon/libnetwork/drivers/bridge/port_mapping_linux.go', 'add4 := !ep.portBindingState.ipv4 && pbmReq.ipv4 || (disableNAT4 && !ep.portBindingState.routed && pbmReq.routed)'],
  ['daemon/libnetwork/drivers/bridge/port_mapping_linux.go', 'add6 := !ep.portBindingState.ipv6 && pbmReq.ipv6 || (disableNAT6 && !ep.portBindingState.routed && pbmReq.routed)'],
];
for (const [p, text] of anchors) check(`source anchor: ${p}: ${text}`, () => assert.ok(source(p).includes(text)));
const predicate = (old, requested, routed, oldRouted = false) => !old && requested || routed && !oldRouted;
for (const old of [false, true]) check(`internal-only NAT does not add binding; old=${old}`, () => assert.equal(predicate(old, false, false), false));
check('selected normal gateway can request NAT binding', () => assert.equal(predicate(false, true, false), true));
check('routed mode differs and is outside default-NAT conclusion', () => assert.equal(predicate(false, false, true), true));
const report = fs.readFileSync(path.join(dir, 'report.md'), 'utf8');
let localLinks = 0;
for (const match of report.matchAll(/\]\(([^)]+)\)/g)) {
  if (/^https?:/.test(match[1])) continue;
  const target = path.resolve(dir, match[1].split('#')[0]);
  check(`local report link: ${match[1]}`, () => assert.ok(fs.existsSync(target))); localLinks++;
}
const result = { schemaVersion: 1, scope: 'Offline source diagnosis only; no runtime or source execution', passed: true, checksCount: checks.length, localLinks, checks };
fs.writeFileSync(path.join(dir, 'verification.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({ passed: true, checks: checks.length, localLinks }));
