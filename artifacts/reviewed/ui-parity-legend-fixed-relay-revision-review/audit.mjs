import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';
const base=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(base,'../..');
const revised=path.join(root,'artifacts/ui-parity-legend-fixed-relay-revised');
const baseline=path.join(root,'artifacts/ui-parity-legend-fixed-relay');
const hash=data=>createHash('sha256').update(data).digest('hex');
const bytes=file=>fs.readFileSync(file),text=file=>fs.readFileSync(file,'utf8'),json=file=>JSON.parse(bytes(file));
const expected={
  'harness-manifest.json':'dcb25a5a5bcadf2d5628b0f2ebd2077586c7bde325a063b4eb5bf72f266b8700',
  'source-hashes.json':'7d1dbfc86d2cef42d8b8e73eacf63c85dd0c3676938c95d10210976cd5d263fb',
  'publication-allowlist.json':'eba713d4981e22a8c18bcd490e19965f6e134f98dd92d7421fb09ce7f5b3bc41'};
function verify(file,digest,size){const data=bytes(file);assert.equal(hash(data),digest,file);if(size!==undefined)assert.equal(data.length,size,file);}
function frozen(){
  for(const [file,digest] of Object.entries(expected))verify(path.join(revised,file),digest);
  const manifest=json(path.join(revised,'source-hashes.json'));
  assert.equal(manifest.sourceFiles.length,17);assert.equal(manifest.sourceInputs.length,11);
  for(const file of manifest.sourceFiles)verify(path.join(revised,file.path),file.sha256,file.bytes);
  for(const file of manifest.sourceInputs)verify(path.join(root,file.sourcePath),file.sha256,file.bytes);
  const old=json(path.join(baseline,'source-hashes.json'));
  for(const file of old.sourceFiles)verify(path.join(baseline,file.path),file.sha256,file.bytes);
  for(const file of old.sourceInputs)verify(path.join(root,file.sourcePath),file.sha256,file.bytes);
  const selection=json(path.join(revised,'publication-allowlist.json'));
  assert.equal(selection.length,18);assert.equal(new Set(selection.map(file=>file.sourcePath)).size,18);
  for(const file of selection){
    assert(file.sourcePath.startsWith('artifacts/ui-parity-legend-fixed-relay-revised/'));
    assert(!file.sourcePath.includes('..'));assert(!fs.lstatSync(path.join(root,file.sourcePath)).isSymbolicLink());
    verify(path.join(root,file.sourcePath),file.sha256,file.bytes);
  }
  return manifest;
}
const manifest=frozen();
for(const source of manifest.gitSources){
  assert.equal(source.repository,'vendor/workspace');assert.equal(source.revision,'38dffc33389aca0e4a87e0e88d42f7067aa220df');
  assert(['lite/Dockerfile','lite/supervisord.conf'].includes(source.path));
  const value=execFileSync('git',['-C',path.join(root,source.repository),'show',source.revision+':'+source.path],{windowsHide:true,maxBuffer:262144});
  assert.equal(hash(value),source.sha256);assert.equal(value.length,source.bytes);
}
for(const file of ['harness/finalize.mjs','harness/io.mjs','harness/run.sh','probe-contract.json'])assert(bytes(path.join(revised,file)).equals(bytes(path.join(baseline,file))),file);
for(const file of ['supervise.sh','prepare-run.mjs'])assert.equal(text(path.join(revised,file)),text(path.join(baseline,file)).replaceAll('ui-parity-legend-fixed-relay/','ui-parity-legend-fixed-relay-revised/'),file);
assert.equal(text(path.join(revised,'harness/probe.mjs')),text(path.join(baseline,'harness/probe.mjs')).replaceAll("'ui-parity-legend-fixed-relay'","'ui-parity-legend-fixed-relay-revised'").replaceAll('allTrue','networkValid'));
const originalAdmission=text(path.join(baseline,'harness/admission.mjs')),currentAdmission=text(path.join(revised,'harness/admission.mjs'));
assert.equal(currentAdmission.slice(currentAdmission.indexOf('export function admitContainer')),originalAdmission.slice(originalAdmission.indexOf('export function admitContainer')));
assert(bytes(path.join(base,'reviewed-source-publication-allowlist.json')).equals(bytes(path.join(revised,'publication-allowlist.json'))));
const commands=[];
function run(program,args){
  const stdout=execFileSync(program,args,{cwd:root,encoding:'utf8',windowsHide:true,maxBuffer:262144}).trim();
  commands.push({program,args,exitCode:0,stdout});return JSON.parse(stdout);
}
const offline=run(process.execPath,[path.join(revised,'verify-offline.mjs')]);
assert.deepEqual(offline,{status:'passed',javascriptTests:25,pythonTests:10,syntaxFiles:8,runtimeExecuted:false});
const f1=run('py',['-3','-B',path.join(base,'f1-audit.py')]);assert.equal(f1.status,'F1-closed-source-only');
const control=run(process.execPath,[path.join(base,'control-audit.mjs')]);
assert(control.cleanup.every(item=>item.baseline.completed&&!item.revised.completed));
assert(control.partialRecovery.completed&&control.operands.revisedDistinct);
for(const item of json(path.join(revised,'publication-allowlist.json'))){
  const value=text(path.join(root,item.sourcePath));
  assert(!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/.test(value));
  assert(!/\b(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}|AKIA[A-Z0-9]{16})\b/.test(value));
  assert(!/\b(?:TODO|TBD|FIXME|HACK|XXX)\b/.test(value));
}
for(const report of [path.join(revised,'handoff.md'),path.join(base,'review.md'),path.join(base,'f1-review.md')]){
  for(const match of text(report).matchAll(/\]\(([^)]+)\)/g)){
    if(/^https:\/\//.test(match[1]))continue;
    if(process.argv.includes('--record')&&path.resolve(path.dirname(report),match[1])===path.join(base,'verification.json'))continue;
    assert(fs.existsSync(path.resolve(path.dirname(report),match[1])),match[1]);
  }
}
frozen();
const receipt={verdict:'APPROVED',scope:'Exact corrected source, F1/F2/F3 closure and publication; separate controller runtime grant required',inputHashes:expected,
  commands,sourceFiles:17,localInputs:11,publicationFiles:18,gitBlobs:2,
  lifecycleChecks:'Writer, finalizer, run script and contract byte-identical; supervisor/preparation differ only by revised path; probe differs only by revised path and network predicate; admission decisions/readiness/counters unchanged',
  closedFindings:['F1','F2','F3'],frozenInputsPreserved:true,runtimeExecuted:false,networkOpened:false,preparationOrFreezeExecuted:false,
  scanScope:'18 selected source/evidence files, bounded common-token/private-key and placeholder patterns plus manual review',
  productionCaps:'Research exclusion; future maintained 400 physical/file,300 logical/file,50/function with inventory/checker'};
if(process.argv.includes('--record'))fs.writeFileSync(path.join(base,'verification.json'),JSON.stringify(receipt,null,2)+'\n');
else assert.deepEqual(json(path.join(base,'verification.json')),receipt);
console.log(JSON.stringify({verdict:receipt.verdict,closedFindings:receipt.closedFindings,commands:commands.length,frozenInputsPreserved:true,runtimeExecuted:false}));
