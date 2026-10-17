import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,path.basename(path.dirname(here))==='reviewed'?'../../..':'../..');
const prefix='artifacts/ui-parity-tooltip-failure-metadata-source/';
const manifest=JSON.parse(fs.readFileSync(here+'/source-hashes.json'));
const allowlist=JSON.parse(fs.readFileSync(here+'/publication-allowlist.json'));
const hash=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
let checked=0;
for(const item of [...manifest.inputs,...manifest.outputs,...allowlist]){
  const file=item.sourcePath.startsWith(prefix)?here+'/'+item.sourcePath.slice(prefix.length):root+'/'+item.sourcePath;
  if(fs.statSync(file).size!==item.bytes||hash(file)!==item.sha256)throw Error('Frozen bytes changed: '+item.sourcePath);checked++;
}
for(const item of manifest.fromBase){
  const base=here+'/base/'+item.name,harness=here+'/harness/'+item.name;
  if(hash(base)!==item.baseSha256||hash(harness)!==item.sha256)throw Error('From-base pin mismatch: '+item.name);
}
const changed=manifest.fromBase.filter(v=>v.changed).map(v=>v.name);
if(JSON.stringify(changed)!=='["journey.mjs"]')throw Error('Unexpected existing harness edits');
if(manifest.added.join(',')!=='failure-metadata.mjs')throw Error('Unexpected harness addition');
console.log(JSON.stringify({scope:'Frozen source/publication byte audit only',checked,passed:true}));
