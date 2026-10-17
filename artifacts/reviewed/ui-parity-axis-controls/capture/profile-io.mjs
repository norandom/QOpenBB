import fs from 'node:fs';
import path from 'node:path';
import {createHash,randomBytes} from 'node:crypto';
const base=path.resolve(new URL('.',import.meta.url).pathname),temp=base+'/bench-'+randomBytes(5).toString('hex');
const source=process.argv[2]||base+'/attempt-20261017T1422580-7c412f5c/harness/io.mjs';
const hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');
fs.mkdirSync(temp);const samples=[];
try{
  for(let i=0;i<100;i++)fs.writeFileSync(temp+'/sample-'+i+'.json','{}');process.env.CAPTURE_ROOT=temp;
  const io=await import(source),payload={synthetic:'x'.repeat(315000)};
  for(let i=0;i<8;i++){const start=performance.now();io.json('rewrite',payload);samples.push(performance.now()-start);}
  const receipt={scope:'Offline synthetic retained-file I/O only; no application/browser execution',source:path.relative(base,source),sourceSha256:hash(source),
    files:100,payloadBytes:315016,rewrites:samples.length,elapsedMs:samples,meanMs:samples.reduce((a,b)=>a+b,0)/samples.length,
    retained:io.budget().bytes,rootDeleted:false};
  if(path.dirname(path.resolve(temp))!==base||!/^bench-[a-f0-9]{10}$/.test(path.basename(temp)))throw Error('Unsafe benchmark cleanup');
  fs.rmSync(temp,{recursive:true});receipt.rootDeleted=!fs.existsSync(temp);
  fs.writeFileSync(base+'/io-profile-'+hash(source).slice(0,12)+'.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt));
}finally{if(fs.existsSync(temp)&&path.dirname(path.resolve(temp))===base&&/^bench-[a-f0-9]{10}$/.test(path.basename(temp)))fs.rmSync(temp,{recursive:true});}
