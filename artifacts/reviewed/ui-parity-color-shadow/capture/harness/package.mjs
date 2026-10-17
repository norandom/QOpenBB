import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const repo='/mnt/d/Source/QOpenBB',base=repo+'/artifacts/ui-parity-color-shadow/capture';
const hash=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const json=(name,value)=>fs.writeFileSync(base+'/'+name+'.json',JSON.stringify(value,null,2));
const files=[];
const add=(file,destination)=>files.push({source:path.relative(repo,file),destination,sha256:hash(file),bytes:fs.statSync(file).size});
const addCapture=relative=>add(base+'/'+relative,'ui-parity-color-shadow/capture/'+relative);
for(const name of fs.readdirSync(base+'/harness'))if(/\.mjs$|\.sh$|^fixture\.json$/.test(name))addCapture('harness/'+name);
for(const attempt of ['attempt-20261017-r3-a1','attempt-20261017-r3-a2']){
  const names=fs.readdirSync(base+'/'+attempt);
  for(const name of fs.readdirSync(base+'/'+attempt+'/harness'))if(/\.mjs$|\.sh$|^fixture\.json$/.test(name))addCapture(attempt+'/harness/'+name);
  for(const name of names){
    const receipts=['failure.json','browser-cleanup.json','cleanup-report.json','cleanup-status.json','run-status.json','runtime-identity.json','start-status.json','journey-status.json','onboarding-receipt.json'];
    const observed=attempt.endsWith('a2')&&(/^C\d\d.*\.(json|png)$/.test(name)||/^setup\.s\d+-(before|after)\.json$/.test(name)||
      ['summary.json','cases.json','screenshots.json','events.json','model-deltas.json','diagnostic-summary.json','action-ledger-public.json','retained-bytes.json','verification.json','raster-measurements.json'].includes(name));
    if(receipts.includes(name)||observed)addCapture(attempt+'/'+name);
  }
}
for(const name of ['report.md','commands.json'])addCapture(name);
for(const name of ['plan.md','source-hashes.json'])add(repo+'/artifacts/ui-parity-color-shadow/'+name,'ui-parity-color-shadow/'+name);
for(const name of ['plan-review.md','verification.json','audit.mjs'])add(repo+'/artifacts/ui-parity-color-shadow-review/'+name,'ui-parity-color-shadow-review/'+name);
files.sort((a,b)=>a.destination.localeCompare(b.destination));
json('publication-allowlist',{schemaVersion:1,status:'selected-for-independent-review',destinationRoot:'artifacts/reviewed',files,
  derivatives:[{source:'attempt-20261017-r3-a2/action-ledger.json',published:'attempt-20261017-r3-a2/action-ledger-public.json',change:'Omitted authentication setup entries; retained all before/after-referenced application actions'},
    {source:'attempt-20261017-r3-a2/diagnostics.json',published:'attempt-20261017-r3-a2/diagnostic-summary.json',change:'Removed raw HTTP/auth inventory; retained error records, counts and diagnosis'},
    {source:'viewport PNG checkpoints',published:'*-region-[0-3].png',change:'Lossless finite crops of the same screenshot, with recorded coordinates and independent hashes'}],
  metadataFiles:['publication-allowlist.json','output-manifest.json','link-verification.json'].map(name=>({source:'artifacts/ui-parity-color-shadow/capture/'+name,destination:'ui-parity-color-shadow/capture/'+name,
    hashPolicy:'Controller publication sync hashes actual metadata bytes; excluded from local cross-hashes to avoid a circular manifest'})),
  excluded:['runtime-private.json','credential-private.json','state-*','raw action-ledger.json authentication setup','raw diagnostics.json HTTP/auth inventories','logs','profiles','traces','environment files','dependency caches','image archives'],
  historicalEvidence:'Failed attempt1 setup receipt/scripts and successful cleanup included; its raw HTTP/auth inventories, byte ledger and auth action ledger stay local.'});
json('output-manifest',{schemaVersion:1,scope:'Selected finite synthetic capture inputs and outputs; metadata files excluded from local cross-hashes to avoid a circular manifest',files});
const destinationMap=new Map(files.map(f=>[f.destination,repo+'/'+f.source]));
destinationMap.set('ui-parity-color-shadow/capture/output-manifest.json',base+'/output-manifest.json');
destinationMap.set('ui-parity-color-shadow/capture/publication-allowlist.json',base+'/publication-allowlist.json');
const linkChecks=[];
for(const f of files.filter(f=>f.source.endsWith('.md'))){const text=fs.readFileSync(repo+'/'+f.source,'utf8');for(const match of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){
  const target=match[1];if(/^[a-z]+:|^#/.test(target))continue;
  const destination=path.posix.normalize(path.posix.join(path.posix.dirname(f.destination),target.split('#')[0]));
  const local=destinationMap.get(destination)||repo+'/artifacts/reviewed/'+destination;
  linkChecks.push({from:f.destination,target,resolved:destination,exists:fs.existsSync(local)});
}}
json('link-verification',{status:linkChecks.every(c=>c.exists)?'passed':'failed',checks:linkChecks});
console.log(JSON.stringify({files:files.length,bytes:files.reduce((a,b)=>a+b.bytes,0),linkCount:linkChecks.length,failedLinks:linkChecks.filter(c=>!c.exists)}));
if(linkChecks.some(c=>!c.exists))process.exitCode=1;
