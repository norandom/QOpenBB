import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {root,json} from './io.mjs';
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8',timeout:10000,stdio:['ignore','pipe','pipe'],windowsHide:true});
const runtime=fs.existsSync(root+'/runtime-private.json')?JSON.parse(fs.readFileSync(root+'/runtime-private.json')):null;
let containerAbsent=true,stateAbsent=true;
if(runtime){
  if(!/^qopenbb-axis-controls-20261017-[a-f0-9]{10}$/.test(runtime.name))throw Error('Unsafe container name');
  const state=path.resolve(runtime.statePath);
  if(path.dirname(state)!==path.resolve(root)||!/^state-[a-f0-9]{12}$/.test(path.basename(state)))throw Error('Unsafe state path');
  const found=docker('ps','-a','--no-trunc','--filter','name=^/'+runtime.name+'$','--format','{{.ID}}').trim();
  if(found){if(runtime.container&&found!==runtime.container)throw Error('Container ID mismatch');docker('rm','-f',found);}
  fs.rmSync(state,{recursive:true,force:true});stateAbsent=!fs.existsSync(state);
  containerAbsent=!docker('ps','-a','--filter','name=^/'+runtime.name+'$','--format','{{.Names}}').trim();
}
fs.rmSync(root+'/credential-private.json',{force:true});
const credentialAbsent=!fs.existsSync(root+'/credential-private.json');
const remainingOwnedState=fs.readdirSync(root).filter(name=>/^state-[a-f0-9]{12}$/.test(name));
json('cleanup-report',{containerAbsent,stateAbsent,credentialAbsent,remainingOwnedState});
if(!containerAbsent||!stateAbsent||!credentialAbsent||remainingOwnedState.length)throw Error('Cleanup incomplete');
