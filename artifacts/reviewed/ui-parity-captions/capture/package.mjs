import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root=path.dirname(fileURLToPath(import.meta.url));
const scripts=['limits.mjs','io.mjs','start.mjs','cleanup.mjs','projection.mjs','journey.mjs',
  'manifest.mjs','offline-check.mjs','offline-output-check.mjs','offline-output-check.json',
  'analyze.mjs','publication.mjs','package.mjs','run.sh','fixture.json','attempt-notes.md','report.md'];
const files=[];
function add(relative){
  const absolute=path.join(root,relative);if(!fs.existsSync(absolute))return;
  const bytes=fs.readFileSync(absolute);
  files.push({path:relative,sourcePath:'artifacts/ui-parity-captions/capture/'+relative,
    bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),
    sanitization:'Synthetic finite evidence or harness source; independent publication review required'});
}
for(const name of scripts)add(name);
for(const directory of fs.readdirSync(path.join(root,'runs'))){
  if(!/^attempt-[0-9]{8}T[0-9]{6}Z-[a-f0-9]{8}$/.test(directory))throw Error('Unexpected run directory');
  const run=path.join(root,'runs',directory),manifest=path.join(run,'publication-allowlist.json');
  if(!fs.existsSync(path.join(run,'run-status.json')))throw Error('Attempt still active '+directory);
  if(!fs.existsSync(manifest))throw Error('Attempt allowlist required '+directory);
  const allowlist=JSON.parse(fs.readFileSync(manifest));
  for(const file of allowlist.files){
    if(file.path.includes('..')||path.isAbsolute(file.path))throw Error('Unsafe attempt publication path');
    const actual=fs.readFileSync(path.join(run,file.path));
    if(createHash('sha256').update(actual).digest('hex')!==file.sha256)throw Error('Attempt bytes changed '+file.path);
    add('runs/'+directory+'/'+file.path);
  }
  add('runs/'+directory+'/publication-allowlist.json');
}
fs.writeFileSync(path.join(root,'publication-allowlist.json'),JSON.stringify({
  status:'Completed local outputs proposed for independent review; not published',files,
  originalRoot:'artifacts/ui-parity-captions/capture',
  exclusions:['runtime-private.json','credential-private.json','state-*','*.log','profiles','environment files','dependency caches'],
  historicalEvidence:'All completed attempts are listed separately, with incomplete attempts diagnosed in attempt-notes.md.'
},null,2));
console.log(JSON.stringify({files:files.length,bytes:files.reduce((sum,file)=>sum+file.bytes,0)}));
