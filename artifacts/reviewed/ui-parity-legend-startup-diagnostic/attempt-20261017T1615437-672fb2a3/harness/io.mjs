import fs from 'node:fs';
import path from 'node:path';
export const root=process.env.CAPTURE_ROOT;
export function createWriter(directory,{disk=fs,caps={files:32,total:2097152,json:65536,publicJson:524288}}={}){
  const base=path.resolve(directory);
  function inventory(){const files=[];function walk(dir){for(const item of disk.readdirSync(dir,{withFileTypes:true})){const file=path.join(dir,item.name);if(item.isSymbolicLink())throw Error('output-symlink');if(item.isDirectory()&&/^state-[a-f0-9]{12}$/.test(item.name))continue;if(item.isDirectory())walk(file);else files.push({path:path.relative(base,file),bytes:disk.statSync(file).size});}}walk(base);return files;}
  function totals(files){return {files:files.length,bytes:files.reduce((sum,f)=>sum+f.bytes,0),publicJson:files.filter(f=>f.path.endsWith('.json')&&!f.path.endsWith('-private.json')).reduce((sum,f)=>sum+f.bytes,0)};}
  function check(files){const t=totals(files);if(t.files>caps.files||t.bytes>caps.total||t.publicJson>caps.publicJson)throw Error('retained-output-bound');return t;}
  function json(name,value,{privateFile=false}={}){
    if(!/^[\w-]+$/.test(name)||privateFile!==name.endsWith('-private'))throw Error('output-name-unresolved');
    const bytes=Buffer.from(JSON.stringify(value));if(bytes.length>caps.json)throw Error('json-output-bound');
    const filename=name+'.json',file=path.join(base,filename);if(disk.existsSync(file)&&disk.lstatSync(file).isSymbolicLink())throw Error('output-symlink');
    const prospective=inventory().filter(entry=>entry.path!==filename);prospective.push({path:filename,bytes:bytes.length});check(prospective);
    disk.writeFileSync(file,bytes,{mode:privateFile?0o600:0o644});
  }
  check(inventory());return {json,inventory,check:()=>check(inventory())};
}
let writer;export function output(){if(!root)throw Error('attempt-root-required');return writer??=createWriter(root);}
