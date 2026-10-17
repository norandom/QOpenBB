import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {randomBytes} from 'node:crypto';
import assert from 'node:assert/strict';
const root=path.dirname(fileURLToPath(import.meta.url));
const temporary=path.join(root,'runs','attempt-19700101T000000Z-'+randomBytes(4).toString('hex'));
fs.mkdirSync(temporary,{recursive:true});
process.env.CAPTURE_RUN=temporary;
try{
  const {write}=await import('./io.mjs');
  const repeated={text:'x'.repeat(600000)};
  for(let index=0;index<60;index++)write('rewritten',repeated);
  assert.equal(fs.readFileSync(path.join(temporary,'rewritten.json'),'utf8'),JSON.stringify(repeated));
  write('action-ledger',{text:'x'.repeat(1200000)});
  write('001-snapshot',{keep:true});
  const valid=fs.readFileSync(path.join(temporary,'001-snapshot.json'),'utf8');
  assert.throws(()=>write('001-snapshot',{text:'x'.repeat(1100000)}),/bound/);
  assert.equal(fs.readFileSync(path.join(temporary,'001-snapshot.json'),'utf8'),valid);
  for(let index=0;index<7;index++)write('payload-'+index,{text:'x'.repeat(4000000)});
  assert.throws(()=>write('payload-new',{text:'x'.repeat(4000000)}),/bound/);
  assert.equal(fs.existsSync(path.join(temporary,'payload-new.json')),false);
  assert.equal(fs.readFileSync(path.join(temporary,'001-snapshot.json'),'utf8'),valid);
  const result={passed:true,checks:['60 overwrites retain one file size','aggregate ledger may exceed snapshot cap',
    'individual snapshot overflow rejected','new file exceeding retained total rejected','rejected writes preserve previous valid bytes'],
    runtimeEvidence:false};
  fs.writeFileSync(path.join(root,'offline-output-check.json'),JSON.stringify(result,null,2));
  console.log('Offline retained-output checks passed.');
}finally{
  if(path.dirname(temporary)!==path.join(root,'runs')||!/^attempt-19700101T000000Z-[a-f0-9]{8}$/.test(path.basename(temporary)))
    throw Error('Unsafe synthetic check cleanup');
  fs.rmSync(temporary,{recursive:true,force:true});
}
