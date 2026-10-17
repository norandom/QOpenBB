import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {limits} from './limits.mjs';
export const scriptRoot=path.dirname(fileURLToPath(import.meta.url));
export const runRoot=path.resolve(process.env.CAPTURE_RUN||'');
if(path.dirname(runRoot)!==path.join(scriptRoot,'runs')||
  !/^attempt-[0-9]{8}T[0-9]{6}Z-[a-f0-9]{8}$/.test(path.basename(runRoot)))
  throw Error('Explicit owned CAPTURE_RUN required');
const sizes=new Map(fs.readdirSync(runRoot).filter(name=>/^[a-z0-9-]+\.json$/.test(name))
  .map(name=>[name,fs.statSync(path.join(runRoot,name)).size]));
let total=[...sizes.values()].reduce((sum,bytes)=>sum+bytes,0);
export function write(name,value){
  if(!/^[a-z0-9-]+$/.test(name))throw Error('Unsafe output name');
  const data=JSON.stringify(value),bytes=Buffer.byteLength(data),filename=name+'.json';
  const nextTotal=total-(sizes.get(filename)||0)+bytes;
  if(/^\d{3}-/.test(name)&&bytes>limits.snapshotBytes||nextTotal>limits.jsonBytes){
    fs.writeFileSync(path.join(runRoot,'overflow.json'),JSON.stringify({kind:'output-bound',name,bytes,total,nextTotal}));
    throw Error('JSON output bound exceeded '+name);
  }
  total=nextTotal;sizes.set(filename,bytes);
  fs.writeFileSync(path.join(runRoot,filename),data);
}
