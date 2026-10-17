import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {limits} from './limits.mjs';
export const scriptRoot=path.dirname(fileURLToPath(import.meta.url));
export const runRoot=path.resolve(process.env.CAPTURE_RUN||'');
if(path.dirname(runRoot)!==path.join(scriptRoot,'runs')||
  !/^attempt-[0-9]{8}T[0-9]{6}Z-[a-f0-9]{8}$/.test(path.basename(runRoot)))
  throw Error('Explicit owned CAPTURE_RUN required');
let total=0;
export function write(name,value){
  if(!/^[a-z0-9-]+$/.test(name))throw Error('Unsafe output name');
  const data=JSON.stringify(value,null,2),bytes=Buffer.byteLength(data);
  if(bytes>limits.snapshotBytes||total+bytes>limits.jsonBytes){
    fs.writeFileSync(path.join(runRoot,'overflow.json'),JSON.stringify({kind:'output-bound',name,bytes,total}));
    throw Error('JSON output bound exceeded '+name);
  }
  total+=bytes;
  fs.writeFileSync(path.join(runRoot,name+'.json'),data);
}
