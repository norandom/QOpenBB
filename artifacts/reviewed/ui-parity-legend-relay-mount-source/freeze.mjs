import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
const base=path.dirname(fileURLToPath(import.meta.url)),project=path.resolve(base,'../..'),prior='artifacts/ui-parity-legend-fixed-relay-revised/';
const prefix='artifacts/ui-parity-legend-relay-mount-source/',hash=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const input=sourcePath=>({sourcePath,sha256:hash(project+'/'+sourcePath),bytes:fs.statSync(project+'/'+sourcePath).size});
const entry=relative=>({path:relative,sha256:hash(base+'/'+relative),bytes:fs.statSync(base+'/'+relative).size});
const priorManifest=JSON.parse(fs.readFileSync(project+'/'+prior+'source-hashes.json'));
for(const f of priorManifest.sourceFiles)if(hash(project+'/'+prior+f.path)!==f.sha256||fs.statSync(project+'/'+prior+f.path).size!==f.bytes)throw Error('Frozen baseline changed');
const plan=input('artifacts/ui-parity-legend-fixed-relay-plan/plan.md');
if(plan.sha256!=='1c9a0e527acb77b808aab703df19ef8f6f8eacb1ed325987e51a5ea071703e65')throw Error('Original plan changed');
const inputs=[prior+'source-hashes.json',prior+'harness-manifest.json',...priorManifest.sourceFiles.map(f=>prior+f.path),
  'artifacts/ui-parity-legend-relay-mount-correction/proposal.md','artifacts/ui-parity-legend-relay-mount-correction-review/review.md',
  'artifacts/ui-parity-legend-fixed-relay-plan-review/review.md',prior+'analysis-attempt-20261017T1700437-e5d5e603/report.md',
  prior+'analysis-attempt-20261017T1700437-e5d5e603/observations.json'].map(input);
if(inputs.find(v=>v.sourcePath.endsWith('mount-correction/proposal.md')).sha256!=='9207c923e3ae55aaa0e575a22e8057000cb0f6450a775931607254945ef9adab'||inputs.find(v=>v.sourcePath.endsWith('mount-correction-review/review.md')).sha256!=='9c48ba928e19660dfca64f27c2c2b019b38dcd2023231330815124d524f5a99e')throw Error('Approved correction changed');
const report=JSON.parse(fs.readFileSync(base+'/offline-verification.json'));
if(report.status!=='passed'||report.javascriptTests!==25||report.mountTests!==11||report.pythonTests!==10||report.runtimeExecuted!==false||report.baselineRED.exitCode!==1)throw Error('Fresh offline evidence required');
for(const f of report.sourceFiles)if(hash(base+'/'+f.path)!==f.sha256)throw Error('Stale offline evidence');
for(const relative of ['harness/relay.py','harness/cleanup.mjs','harness/finalize.mjs','harness/io.mjs','harness/run.sh','test-relay.py','probe-contract.json'])if(hash(base+'/'+relative)!==hash(project+'/'+prior+relative))throw Error('Unrelated source changed: '+relative);
const diffs=[];
for(const relative of ['harness','supervise.sh','prepare-run.mjs','verify-offline.mjs']){
  const diff=spawnSync('git',['diff','--no-index','--no-ext-diff','--',project+'/'+prior+relative,base+'/'+relative],{encoding:'utf8',windowsHide:true,maxBuffer:2097152});
  if(![0,1].includes(diff.status))throw Error('Source comparison failed');diffs.push(diff.stdout);
}
fs.writeFileSync(base+'/relay-source-diff.patch',diffs.join('\n'));
const files=[...fs.readdirSync(base+'/harness').sort().map(v=>entry('harness/'+v)),entry('supervise.sh')];
if(files.length!==8)throw Error('Runtime inventory changed');
const manifest={status:'source-only-ready-for-independent-review',runtimeExecuted:false,plan,sourceInputs:inputs,files,
  originalSource:'38dffc33389aca0e4a87e0e88d42f7067aa220df',image:'sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f',browserCreated:false,attemptsGranted:0};
fs.writeFileSync(base+'/harness-manifest.json',JSON.stringify(manifest,null,2));
const sources=[...files,...['probe-contract.json','handoff.md','prepare-run.mjs','verify-offline.mjs','verify-freeze.mjs','test-relay.py','test-mounts.mjs','freeze.mjs','offline-verification.json','relay-source-diff.patch','harness-manifest.json'].map(entry)];
fs.writeFileSync(base+'/source-hashes.json',JSON.stringify({status:'source-only-frozen',runtimeExecuted:false,sourceFiles:sources,sourceInputs:[plan,...inputs],
  scope:'Exact3binds/soleconfiguredTmpfs correction and path references; research exclusion with future maintained400/300/50'},null,2));
const allowlist=[...sources,entry('source-hashes.json')].map(f=>({sourcePath:prefix+f.path,sha256:f.sha256,bytes:f.bytes}));
fs.writeFileSync(base+'/publication-allowlist.json',JSON.stringify(allowlist,null,2));
console.log(JSON.stringify({status:'source-only-frozen',runtimeFiles:files.length,publicationFiles:allowlist.length,manifestSha256:hash(base+'/harness-manifest.json'),sourceSha256:hash(base+'/source-hashes.json'),allowlistSha256:hash(base+'/publication-allowlist.json')}));
