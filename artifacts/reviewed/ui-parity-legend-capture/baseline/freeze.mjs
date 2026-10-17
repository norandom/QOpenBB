import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const base=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const entry=name=>({path:name,bytes:fs.statSync(path.join(base,name)).size,sha256:hash(path.join(base,name))});
const old=JSON.parse(fs.readFileSync(path.join(base,'frozen/executed-source-manifest.json')));
for(const f of old.files)if(hash(path.join(base,'frozen',f.path))!==f.sha256)throw Error('Frozen source changed '+f.path);
const files=fs.readdirSync(path.join(base,'harness')).sort().map(n=>entry('harness/'+n));
const plan=entry('plan.md');
const manifest={schemaVersion:1,plan:{path:'artifacts/ui-parity-axis-followup/plan.md',sha256:plan.sha256},originalSource:old.originalSource,image:old.image,candidateExecuted:false,runtimeExecuted:false,files,
  baseline:{attempt:'attempt-20261017T1422580-7c412f5c',manifestSha256:hash(path.join(base,'frozen/executed-source-manifest.json'))},
  productionCaps:'Research excluded; future production remains 400 physical/file,300 logical/file,50/function'};
fs.writeFileSync(path.join(base,'harness-manifest.json'),JSON.stringify(manifest,null,2));
const sourceFiles=[plan,...files,entry('verify-offline.mjs'),entry('prepare-run.mjs'),entry('frozen/executed-source-manifest.json'),...old.files.map(f=>entry('frozen/'+f.path))];
const evidence=['offline-verification.json','static-verification.json'].map(entry);
fs.writeFileSync(path.join(base,'source-hashes.json'),JSON.stringify({schemaVersion:1,scope:'Source-only follow-up; no runtime grant',baseline:manifest.baseline,originalSource:old.originalSource,image:old.image,sourceFiles,evidence,harnessManifest:entry('harness-manifest.json')},null,2));
console.log(JSON.stringify({status:'frozen-source-only',sourceFiles:sourceFiles.length,harnessFiles:files.length,manifestSha256:hash(path.join(base,'harness-manifest.json')),sourceHashesSha256:hash(path.join(base,'source-hashes.json'))}));
