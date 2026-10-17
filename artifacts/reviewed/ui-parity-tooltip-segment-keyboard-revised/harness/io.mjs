import fs from 'node:fs';
import {limits} from './contract.mjs';
import {casePrewrite} from './keyboard-retention.mjs';
export const root=process.env.CAPTURE_ROOT;
if(!root)throw Error('CAPTURE_ROOT required');
export const retained=new Map();
function inventory(){let json=0,total=0;for(const n of fs.readdirSync(root)){const p=root+'/'+n;if(!fs.statSync(p).isFile())continue;
  const b=fs.statSync(p).size;total+=b;if(n.endsWith('.json'))json+=b;}return {json,total};}
export function json(name,value){if(name==='T06')casePrewrite(value);const bytes=Buffer.from(JSON.stringify(value));
  if(/^T0[1-8]$/.test(name)&&bytes.length>limits.caseBytes)throw Error('Case JSON bound');
  const file=root+'/'+name+'.json',old=fs.existsSync(file)?fs.statSync(file).size:0,now=inventory();
  const reserved=/cleanup|failure|byte-budget|diagnostics/.test(name)?0:32768;
  if(now.json-old+bytes.length>limits.jsonBytes-reserved||now.total-old+bytes.length>limits.runBytes-reserved)throw Error('Retained byte bound');
  fs.writeFileSync(file,bytes);retained.set(name+'.json',bytes.length);}
export function budget(){const now=inventory();return {retainedJsonBytes:now.json,retainedTotalBytes:now.total,limits};}
export function png(name,bytes){if(bytes.length>limits.pngBytes)throw Error('PNG bound');
  if(inventory().total+bytes.length>limits.runBytes)throw Error('Run byte bound');fs.writeFileSync(root+'/'+name+'.png',bytes);}
