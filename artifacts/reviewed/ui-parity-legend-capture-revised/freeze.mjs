import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
const base=path.dirname(fileURLToPath(import.meta.url)),sha=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const entry=name=>({path:name,bytes:fs.statSync(base+'/'+name).size,sha256:sha(base+'/'+name)});
const original=path.resolve(base,'../ui-parity-legend-capture');
if(sha(original+'/harness-manifest.json')!=='9c6400819ba8d711829ba6abcc1c8b6ace2da1cd554ca01db7ea2627cb9ae1b3'||sha(original+'/source-hashes.json')!=='f8c4ba54c233a97fbb3a7ab5ffc5331873ff1e49532735a1e403a9b76b2e2bf6')throw Error('Frozen initial manifests changed');
for(const f of JSON.parse(fs.readFileSync(original+'/source-hashes.json')).sourceFiles)if(sha(original+'/'+f.path)!==f.sha256||fs.statSync(original+'/'+f.path).size!==f.bytes)throw Error('Frozen initial source changed '+f.path);
const provenance=JSON.parse(fs.readFileSync(base+'/provenance.json'));
for(const f of provenance.localInputs){const input=path.resolve(base,'../..',f.path);if(sha(input)!==f.sha256||fs.statSync(input).size!==f.bytes)throw Error('Provenance changed '+f.path);}
const baseline=JSON.parse(fs.readFileSync(base+'/baseline-source-manifest.json'));
for(const f of baseline.files){const name=f.path.replace(/^harness\//,'');if(sha(base+'/baseline/'+name)!==f.sha256)throw Error('Frozen baseline mismatch '+name);}
const planFile=path.resolve(base,'../ui-parity-legend-plan-revised/plan.md'),reviewFile=path.resolve(base,'../ui-parity-legend-collector-review/review.md');
if(sha(planFile)!=='5a33a0237eb351df5a7a6060da2aff5c83379f89999c4a4ca82faa40c92e29ef')throw Error('Accepted plan hash changed');
for(const report of ['offline-verification.json','static-verification.json'])if(JSON.parse(fs.readFileSync(base+'/'+report)).status!=='passed')throw Error('Source verification did not pass');
const diff=spawnSync('git',['diff','--no-index','--no-ext-diff','--','baseline','harness'],{cwd:base,encoding:'utf8',windowsHide:true,maxBuffer:2097152});
if(![0,1].includes(diff.status))throw Error('Source diff failed '+diff.stderr);fs.writeFileSync(base+'/source-diff.patch',diff.stdout);
const files=fs.readdirSync(base+'/harness').sort().map(n=>entry('harness/'+n));
const manifest={schemaVersion:1,status:'source-only-ready-for-independent-review',runtimeExecuted:false,candidateExecuted:false,
  plan:{path:'artifacts/ui-parity-legend-plan-revised/plan.md',sha256:sha(planFile)},review:{path:'artifacts/ui-parity-legend-collector-review/review.md',sha256:sha(reviewFile)},
  baseline:{source:'artifacts/ui-parity-legend-capture/harness',manifest:entry('baseline-source-manifest.json')},
  originalSource:baseline.originalSource,image:baseline.image,initialFrozenUnchanged:true,sourceInputs:provenance.localInputs,files};
fs.writeFileSync(base+'/harness-manifest.json',JSON.stringify(manifest,null,2));
const roots=['plan.md','handoff.md','provenance.json','prepare-run.mjs','supervise.sh','offline-tests.mjs','static-check.mjs','freeze.mjs','baseline-source-manifest.json','source-diff.patch','offline-verification.json','static-verification.json'];
const sources=[...roots.map(entry),...files,...fs.readdirSync(base+'/baseline').sort().map(n=>entry('baseline/'+n)),entry('harness-manifest.json')];
fs.writeFileSync(base+'/source-hashes.json',JSON.stringify({schemaVersion:1,status:'source-only-frozen',runtimeExecuted:false,sourceFiles:sources,scope:'Only artifacts/ui-parity-legend-capture-revised; research excluded from production complexity caps'},null,2));
console.log(JSON.stringify({status:'source-only-frozen',files:sources.length,harnessManifestSha256:sha(base+'/harness-manifest.json'),sourceHashesSha256:sha(base+'/source-hashes.json')}));
