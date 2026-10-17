import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const here=path.dirname(fileURLToPath(import.meta.url)),project=path.resolve(here,path.basename(path.dirname(here))==='reviewed'?'../../..':'../..');
const prefix='artifacts/ui-parity-legend-relay-mount-source/';
const hash=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const manifest=JSON.parse(fs.readFileSync(here+'/source-hashes.json')),allowlist=JSON.parse(fs.readFileSync(here+'/publication-allowlist.json'));
let checked=0;
for(const pin of [...manifest.sourceInputs,...manifest.sourceFiles.map(f=>({sourcePath:prefix+f.path,...f})),...allowlist]){
  const file=pin.sourcePath.startsWith(prefix)?here+'/'+pin.sourcePath.slice(prefix.length):project+'/'+pin.sourcePath;
  if(hash(file)!==pin.sha256||fs.statSync(file).size!==pin.bytes)throw Error('Frozen bytes changed: '+pin.sourcePath);checked++;
}
const harness=JSON.parse(fs.readFileSync(here+'/harness-manifest.json'));
for(const pin of harness.files)if(hash(here+'/'+pin.path)!==pin.sha256)throw Error('Runtime source changed');
console.log(JSON.stringify({status:'passed',frozenPins:checked,runtimeFiles:harness.files.length,runtimeExecuted:false}));
