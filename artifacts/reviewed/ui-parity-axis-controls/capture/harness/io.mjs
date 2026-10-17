import fs from 'node:fs';
import path from 'node:path';
export const root=process.env.CAPTURE_ROOT;
if(!root)throw Error('CAPTURE_ROOT required');
export const limits={actions:240,changes:80,checkpoints:96,pngs:64,files:320,json:2097152,png:4194304,total:167772160};
export function increment(value,cap,label){if(value>=cap)throw Error(label+' cap');return value+1;}
export function budget(){
  const files=[];
  const walk=dir=>{for(const item of fs.readdirSync(dir,{withFileTypes:true})){
    if(item.name.startsWith('state-')||item.name.endsWith('-private.json')||item.name.endsWith('.log'))continue;
    const file=path.join(dir,item.name);if(item.isDirectory())walk(file);else files.push({path:path.relative(root,file),bytes:fs.statSync(file).size});
  }};walk(root);
  return {files:files.length,bytes:files.reduce((a,f)=>a+f.bytes,0),entries:files};
}
export function check(){const b=budget();if(b.files>limits.files||b.bytes>limits.total)throw Error('Retained output budget overflow');return b;}
export function json(name,value){
  const bytes=Buffer.from(JSON.stringify(value));if(bytes.length>limits.json)throw Error('JSON byte bound '+name);
  writeBytes(name+'.json',bytes);
}
export function writeBytes(name,bytes){const file=path.join(root,name),existing=fs.existsSync(file)?fs.statSync(file).size:0,b=budget();
  if(b.files+(fs.existsSync(file)?0:1)>limits.files||b.bytes-existing+bytes.length>limits.total)throw Error('Prospective retained output cap');
  fs.writeFileSync(file,bytes);
}
export function png(name,bytes){if(bytes.length>limits.png)throw Error('PNG byte bound');writeBytes(name+'.png',bytes);}
