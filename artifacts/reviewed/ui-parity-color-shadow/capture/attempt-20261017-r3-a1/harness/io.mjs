import fs from 'node:fs';
export const root=process.env.CAPTURE_ROOT;
if(!root)throw Error('CAPTURE_ROOT required');
export const retained=new Map();
export function json(name,value,{snapshot=false}={}){
  const text=JSON.stringify(value),bytes=Buffer.byteLength(text);
  if(snapshot&&bytes>256*1024)throw Error('Checkpoint exceeds 256KiB');
  if(['action-ledger','events'].includes(name)&&bytes>2*1024*1024)throw Error('Ledger exceeds 2MiB');
  fs.writeFileSync(root+'/'+name+'.json',text);retained.set(name+'.json',bytes);
}
export function budget(){return {retainedJsonBytes:[...retained.values()].reduce((a,b)=>a+b,0),
  files:Object.fromEntries(retained),checkpointByteCap:262144,eventLedgerByteCap:2097152};}
