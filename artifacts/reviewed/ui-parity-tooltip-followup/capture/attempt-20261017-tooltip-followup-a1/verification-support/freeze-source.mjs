import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../../..');
const hash=b=>createHash('sha256').update(b).digest('hex');
const read=p=>fs.readFileSync(path.join(root,p));
const old='artifacts/ui-parity-tooltip-plan/capture/attempt-20261017-r4-a2';
const base='artifacts/ui-parity-tooltip-followup',manifest=JSON.parse(read(old+'/static-verification.json'));
if(hash(read(old+'/static-verification.json'))!=='c098553db7a38c72eafec8ab0fc3a7e06c41ce74396f9062e44c794b8f6cb123')throw Error('Frozen source manifest mismatch');
if(manifest.files.length!==12)throw Error('Baseline file count');
for(const f of manifest.files)for(const p of [old+'/harness/'+f.name,base+'/capture/baseline/harness/'+f.name])
  if(hash(read(p))!==f.sha256)throw Error('Baseline identity '+p);
const plan=base+'/plan.md',planHash=hash(read(plan)),contract=path.join(here,'harness/contract.mjs');
fs.writeFileSync(contract,fs.readFileSync(contract,'utf8').replace(/export const planHash='[a-f0-9]{64}';/,"export const planHash='"+planHash+"';"));
const names=manifest.files.map(f=>f.name).sort();let diff='';
for(const name of names){const a=here+'/baseline/harness/'+name,b=here+'/harness/'+name;
  try{diff+=execFileSync('diff',['-u','--label','baseline/harness/'+name,'--label','harness/'+name,a,b],{encoding:'utf8'});}
  catch(e){if(e.status!==1)throw e;diff+=e.stdout;}}
fs.writeFileSync(here+'/source-diff.patch',diff);
const receipt=(p,kind)=>({path:p,kind,bytes:read(p).length,sha256:hash(read(p))});
const inputs=[
  'AGENTS.md','.kiro/steering/delegation.md','.kiro/steering/testing.md','.kiro/steering/complexity.md','.kiro/steering/documentation.md','.kiro/steering/ci.md',
  'artifacts/ui-parity-tooltip-plan/plan.md','artifacts/ui-parity-tooltip-plan/source-hashes.json',
  'artifacts/ui-parity-tooltip-plan/capture/report.md','artifacts/ui-parity-tooltip-plan/capture/correction-2-proposal.md',
  'artifacts/ui-parity-tooltip-review/harness-review.md','artifacts/ui-parity-tooltip-review/correction-1-review.md',
  'artifacts/ui-parity-tooltip-review/runtime-review.md',
  'artifacts/reviewed/ui-parity-captions/capture/journey.mjs',
  old+'/static-verification.json',old+'/executed-source-verification.json',
];
const support=['capture/followup-static.mjs','capture/freeze-source.mjs','capture/verify-offline.mjs','capture/source-diff.patch'];
const value={schemaVersion:1,date:'2026-10-17',status:'source-only proposal; independent review and controller grant required; no runtime acceptance',
  runtimeExecuted:false,original:'38dffc33389aca0e4a87e0e88d42f7067aa220df',image:'sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f',
  fixtureCanonicalSha256:'bda68b15aee2192684d67086c4a599f852943a3079882d4aeb744e6efab262ad',
  inputs:inputs.map(p=>receipt(p,'immutable-input')),
  baseline:names.map(n=>({...receipt(base+'/capture/baseline/harness/'+n,'byte-identical-executed-copy'),sourcePath:old+'/harness/'+n})),
  proposed:names.map(n=>receipt(base+'/capture/harness/'+n,'proposed-not-executed')),
  support:support.map(p=>receipt(base+'/'+p,'offline-support')),plan:receipt(plan,'follow-up-plan')};
fs.writeFileSync(path.join(root,base,'source-hashes.json'),JSON.stringify(value,null,2)+'\n');
console.log(JSON.stringify({planHash,manifestHash:hash(read(base+'/source-hashes.json')),baselineFiles:names.length,proposedFiles:names.length,runtimeExecuted:false}));
