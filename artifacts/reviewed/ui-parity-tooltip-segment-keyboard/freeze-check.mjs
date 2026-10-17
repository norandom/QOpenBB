import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,path.basename(path.dirname(here))==='reviewed'?'../../..':'../..');
const manifest=JSON.parse(fs.readFileSync(here+'/source-hashes.json'));
const allowlist=JSON.parse(fs.readFileSync(here+'/publication-allowlist.json'));
const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
let checked=0;
for(const item of [...manifest.inputs,...manifest.outputs,...allowlist.files]){
  const local=item.sourcePath.startsWith('artifacts/ui-parity-tooltip-segment-keyboard/');
  const file=local?path.join(here,item.sourcePath.slice('artifacts/ui-parity-tooltip-segment-keyboard/'.length)):path.join(root,item.sourcePath);
  if(fs.statSync(file).size!==item.bytes||hash(file)!==item.sha256)throw Error('Frozen bytes changed: '+item.sourcePath);
  checked++;
}
console.log(JSON.stringify({scope:'Frozen source/publication byte audit only',checked,passed:true}));
