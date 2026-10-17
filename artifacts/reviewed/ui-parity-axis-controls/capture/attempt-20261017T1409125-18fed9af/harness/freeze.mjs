import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const base=path.resolve(new URL('..',import.meta.url).pathname),repo='/mnt/d/Source/QOpenBB';
const hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const plan=repo+'/artifacts/ui-parity-axis-controls/plan.md';
if(hash(plan)!=='f4247a1eb9447f5dd2bd8d3faab6013655ddca95039863b565958a7e09952cb8')throw Error('Plan identity changed');
const files=fs.readdirSync(base+'/harness').filter(n=>/\.(mjs|sh|json)$/.test(n)).sort().map(n=>({path:'harness/'+n,bytes:fs.statSync(base+'/harness/'+n).size,sha256:hash(base+'/harness/'+n)}));
const reused=['start.mjs','cleanup.mjs','fixture.json'].map(n=>({source:'artifacts/ui-parity-color-shadow/capture/harness/'+n,sha256:hash(repo+'/artifacts/ui-parity-color-shadow/capture/harness/'+n),adapted:n!=='fixture.json',destination:n==='fixture.json'?'harness/dashboard.json':'harness/'+n}));
fs.writeFileSync(base+'/harness-manifest.json',JSON.stringify({schemaVersion:1,plan:{path:'artifacts/ui-parity-axis-controls/plan.md',sha256:hash(plan)},
  originalSource:'38dffc33389aca0e4a87e0e88d42f7067aa220df',image:'sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f',
  candidateExecuted:false,files,reused,productionCaps:'Evidence scripts excluded; future production remains 400 physical/file,300 logical/file,50/function'},null,2));
console.log(JSON.stringify({status:'frozen',files:files.length,manifestSha256:hash(base+'/harness-manifest.json')}));
