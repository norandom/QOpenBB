import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const root=path.resolve(process.argv[2]),hash=file=>createHash('sha256').update(fs.readFileSync(root+'/'+file)).digest('hex');
if(!fs.existsSync(root+'/run-status.json')||!JSON.parse(fs.readFileSync(root+'/cleanup-report.json')).containerAbsent)throw Error('Closed attempt required');
const names=fs.readdirSync(root).filter(n=>/^events-p\d{2}\.json$/.test(n)).sort(),chunks=[],events=[];
for(const name of names){const data=JSON.parse(fs.readFileSync(root+'/'+name));if(!Array.isArray(data)||data.length>16)throw Error('Chunk bound');
  chunks.push({path:name,sha256:hash(name),bytes:fs.statSync(root+'/'+name).size,count:data.length});events.push(...data);}
if(events.length>256||events.some((e,i)=>e.sequence!==i+1))throw Error('Noncontiguous retained event sequence');
const receipt={schemaVersion:1,kind:'Derived recovery index; immutable event chunks unchanged',originalIndex:{path:'event-index.json',sha256:hash('event-index.json')},
  count:events.length,files:names,chunks,lastObservedAction:events.at(-1)?.action??null,isCompleteRun:false,
  boundary:'Page closed at case deadline; finalization replaced original index/counter with zero. These chunks prove only their retained ordered events; later unobserved events remain unresolved.'};
fs.writeFileSync(root+'/recovered-event-index.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify({count:events.length,chunks:chunks.length,lastObservedAction:receipt.lastObservedAction,isCompleteRun:false}));
