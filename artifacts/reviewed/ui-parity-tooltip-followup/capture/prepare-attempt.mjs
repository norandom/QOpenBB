import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const here=path.dirname(fileURLToPath(import.meta.url));
const sha=b=>createHash('sha256').update(b).digest('hex');
const read=p=>fs.readFileSync(here+'/'+p);
const expected={plan:'95c7f4384c6c25ea48e99859126e03713c14f09645ed75adbba0e657abf2dbdd',
  sources:'3c8820b49ec8f694e2e46c212d2d3ebc217be4700c7c44288310a0e7b0ae87c7',
  collector:'31c23562ec901872025a66c7a0bc275e722b938e3e1a715305a830f868628530'};
for(const [file,key] of [['../plan.md','plan'],['../source-hashes.json','sources'],['static-verification.json','collector']])
  if(sha(read(file))!==expected[key])throw Error('Reviewed source mismatch '+file);
const name='attempt-20261017-tooltip-followup-a1',attempt=here+'/'+name;
fs.mkdirSync(attempt);fs.mkdirSync(attempt+'/harness');fs.mkdirSync(attempt+'/verification-support');
const manifest=JSON.parse(read('static-verification.json'));
const files=manifest.files.map(f=>{const bytes=read('harness/'+f.name);if(sha(bytes)!==f.sha256)throw Error('Proposed bytes mismatch '+f.name);
  fs.writeFileSync(attempt+'/harness/'+f.name,bytes);return {name:f.name,sha256:sha(bytes),expectedSha256:f.sha256};});
for(const f of ['static-verification.json'])fs.writeFileSync(attempt+'/'+f,read(f));
const supports=['followup-static.mjs','verify-offline.mjs','freeze-source.mjs'];
const support=supports.map(name=>{const bytes=read(name);fs.writeFileSync(attempt+'/verification-support/'+name,bytes);return {name,sha256:sha(bytes)};});
fs.writeFileSync(attempt+'/followup-static.mjs',read('followup-static.mjs'));
fs.writeFileSync(attempt+'/reviewed-plan.md',read('../plan.md'));
fs.writeFileSync(attempt+'/source-hashes.json',read('../source-hashes.json'));
fs.writeFileSync(attempt+'/executed-source-verification.json',JSON.stringify({passed:true,manifestSha256:expected.collector,
  sourceManifestSha256:expected.sources,planSha256:expected.plan,files,support,scope:'Copied frozen bytes verified before the separately granted single execution'},null,2));
console.log(JSON.stringify({attempt:name,files:files.length,allMatch:true,...expected}));
