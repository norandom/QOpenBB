import fs from 'node:fs';
import path from 'node:path';
export const limits={actions:240,changes:80,checkpoints:96,pngs:64,files:320,json:2097152,png:4194304,total:167772160};
export function increment(value,cap,label){if(value>=cap)throw Error(label+' cap');return value+1;}
const excluded=name=>name.startsWith('state-')||name.endsWith('-private.json')||name.endsWith('.log');
export function createWriter(directory,{disk=fs,caps=limits}={}){
  const base=path.resolve(directory),entries=new Map(),pending=new Map();
  let total=0,initialScans=0,writes=0;
  function target(name){
    const file=path.resolve(base,name),relative=path.relative(base,file);
    if(!relative||relative==='..'||relative.startsWith('..'+path.sep)||path.isAbsolute(relative)||relative.split(path.sep).some(excluded))throw Error('Unowned output path');
    let current=base;
    for(const part of relative.split(path.sep)){
      current=path.join(current,part);
      if(disk.existsSync(current)&&disk.lstatSync(current).isSymbolicLink())throw Error('Symlink output path');
    }
    return {file,name:relative};
  }
  function scan(){
    const found=new Map();
    function walk(dir){for(const item of disk.readdirSync(dir,{withFileTypes:true})){
      if(excluded(item.name))continue;
      const file=path.join(dir,item.name);
      if(item.isSymbolicLink())throw Error('Symlink retained output');
      if(item.isDirectory())walk(file);else found.set(path.relative(base,file),disk.statSync(file).size);
    }}
    walk(base);return found;
  }
  function update(name,size){total-=entries.get(name)??0;if(size===null)entries.delete(name);else{entries.set(name,size);total+=size;}}
  for(const [name,size] of scan())update(name,size);initialScans++;
  function budget(){
    const ordered=[...entries].sort((a,b)=>{
      const aa=a[0].split(path.sep),bb=b[0].split(path.sep);
      for(let i=0;i<Math.min(aa.length,bb.length);i++)if(aa[i]!==bb[i])return aa[i]<bb[i]?-1:1;
      return aa.length-bb.length;
    });
    return {files:entries.size,bytes:total,entries:ordered.map(([name,bytes])=>({path:name,bytes}))};
  }
  function check(){const b=budget();if(b.files>caps.files||b.bytes>caps.total)throw Error('Retained output budget overflow');return b;}
  function prospective(name,size){
    if(pending.has(name))throw Error('Pending external output');
    let bytes=total-(entries.get(name)??0)+size,files=entries.size+(entries.has(name)?0:1);
    for(const [other,p] of pending){bytes+=p.max-(entries.get(other)??0);if(!entries.has(other))files++;}
    if(files>caps.files||bytes>caps.total)throw Error('Prospective retained output cap');
  }
  function refresh(name,file){update(name,disk.existsSync(file)?disk.statSync(file).size:null);}
  function writeBytes(name,bytes){
    const t=target(name);prospective(t.name,bytes.length);
    try{disk.writeFileSync(t.file,bytes);update(t.name,bytes.length);writes++;}
    catch(error){refresh(t.name,t.file);throw error;}
  }
  function json(name,value){const bytes=Buffer.from(JSON.stringify(value));if(bytes.length>caps.json)throw Error('JSON byte bound '+name);writeBytes(name+'.json',bytes);}
  function png(name,bytes){if(bytes.length>caps.png)throw Error('PNG byte bound');writeBytes(name+'.png',bytes);}
  function reservePNG(name,max=caps.png){
    if(!Number.isInteger(max)||max<0||max>caps.png)throw Error('PNG byte bound');
    const t=target(name+'.png');prospective(t.name,max);pending.set(t.name,{max});
    let done=false;
    return {path:t.file,finish(){
      if(done)throw Error('External write already finished');done=true;
      const reserved=pending.get(t.name);pending.delete(t.name);refresh(t.name,t.file);
      if((entries.get(t.name)??0)>reserved.max)throw Error('External PNG exceeded reservation');return check();
    }};
  }
  function reconcile(){
    if(pending.size)throw Error('Unfinished external writes');
    const actual=scan(),drift=[];
    for(const name of new Set([...entries.keys(),...actual.keys()]))if(entries.get(name)!==actual.get(name))drift.push(name);
    if(drift.length)throw Error('Untracked retained output changes: '+drift.join(','));
    return check();
  }
  check();return {json,png,writeBytes,budget,check,reservePNG,reconcile,stats:()=>({initialScans,writes,pending:pending.size})};
}
export const root=process.env.CAPTURE_ROOT;
let singleton;
function writer(){if(!root)throw Error('CAPTURE_ROOT required');return singleton??=createWriter(root);}
export const json=(...args)=>writer().json(...args),png=(...args)=>writer().png(...args),writeBytes=(...args)=>writer().writeBytes(...args);
export const budget=()=>writer().budget(),check=()=>writer().check(),reconcile=()=>writer().reconcile();
