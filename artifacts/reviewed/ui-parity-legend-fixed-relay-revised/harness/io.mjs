import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
export const root=process.env.CAPTURE_ROOT;
export function verifySource(directory){
  const hash=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex'),manifestFile=path.join(directory,'source-manifest.json');
  const proof=JSON.parse(fs.readFileSync(path.join(directory,'preparation.json'))),manifest=JSON.parse(fs.readFileSync(manifestFile));
  if(proof.manifestSha256!==hash(manifestFile)||proof.exactCopies!==true||manifest.files.length!==8)throw Error('source-manifest-unresolved');
  for(const f of manifest.files){if(!/^(harness\/[\w.-]+|supervise\.sh)$/.test(f.path)||hash(path.join(directory,f.path))!==f.sha256||fs.statSync(path.join(directory,f.path)).size!==f.bytes)throw Error('attempt-source-mismatch');}
}
export function createWriter(directory,{disk=fs,caps={files:32,total:2097152,json:65536,publicJson:524288}}={}){
  const base=path.resolve(directory);
  function inventory(){const files=[];function walk(dir){for(const item of disk.readdirSync(dir,{withFileTypes:true})){const file=path.join(dir,item.name);if(item.isSymbolicLink())throw Error('output-symlink');if(item.isDirectory()&&/^state-[a-f0-9]{12}$/.test(item.name))continue;if(item.isDirectory())walk(file);else files.push({path:path.relative(base,file),bytes:disk.statSync(file).size});}}walk(base);return files;}
  function totals(files){return {files:files.length,bytes:files.reduce((sum,f)=>sum+f.bytes,0),publicJson:files.filter(f=>f.path.endsWith('.json')&&!f.path.endsWith('-private.json')).reduce((sum,f)=>sum+f.bytes,0)};}
  function check(files){const t=totals(files);if(t.files>caps.files||t.bytes>caps.total||t.publicJson>caps.publicJson)throw Error('retained-output-bound');return t;}
  function json(name,value,{privateFile=false,fixedBytes=null}={}){
    if(!/^[\w-]+$/.test(name)||privateFile!==name.endsWith('-private'))throw Error('output-name-unresolved');
    let bytes=Buffer.from(JSON.stringify(value));if(bytes.length>caps.json)throw Error('json-output-bound');
    if(fixedBytes!==null){if(fixedBytes!==4096||bytes.length>fixedBytes)throw Error('json-reservation-bound');bytes=Buffer.concat([bytes,Buffer.alloc(fixedBytes-bytes.length,32)]);}
    const filename=name+'.json',file=path.join(base,filename);if(disk.existsSync(file)&&disk.lstatSync(file).isSymbolicLink())throw Error('output-symlink');
    const prospective=inventory().filter(entry=>entry.path!==filename);prospective.push({path:filename,bytes:bytes.length});check(prospective);
    disk.writeFileSync(file,bytes,{mode:privateFile?0o600:0o644});
  }
  check(inventory());return {json,reserveJson:(name,value,size)=>json(name,value,{fixedBytes:size}),inventory,check:()=>check(inventory())};
}
let writer;export function output(){if(!root)throw Error('attempt-root-required');return writer??=createWriter(root);}
// Drain helper output without letting a failed helper exhaust retained evidence.
if(process.argv[2]==='--bounded-log'){
  const name=process.argv[3];if(!['probe.log','cleanup.log','supervisor.log','finalize.log'].includes(name)||!root)throw Error('log-target-unresolved');
  const file=path.join(root,name),limit=8192,marker=Buffer.from('\nOUTPUT_LIMIT_REACHED\n');
  if(!fs.existsSync(file)||fs.lstatSync(file).isSymbolicLink()||fs.statSync(file).size>limit)throw Error('log-reservation-unresolved');
  const fd=fs.openSync(file,'w');let retained=0,overflow=false;
  for await(const chunk of process.stdin){const part=chunk.subarray(0,Math.max(0,limit-retained));if(part.length){fs.writeSync(fd,part);retained+=part.length;}if(part.length<chunk.length)overflow=true;}
  if(overflow)fs.writeSync(fd,marker,0,marker.length,limit-marker.length);fs.closeSync(fd);
}
