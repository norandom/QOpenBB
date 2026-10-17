import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {runRoot,write} from './io.mjs';
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8',timeout:20000,
  stdio:['ignore','pipe','pipe'],windowsHide:true});
const receipt=path.join(runRoot,'runtime-private.json');
const runtime=fs.existsSync(receipt)?JSON.parse(fs.readFileSync(receipt)):null;
let containerAbsent=true,stateAbsent=true;
if(runtime){
  if(!/^qopenbb-captions-[a-f0-9]{16}$/.test(runtime.name))throw Error('Unsafe container name');
  const state=path.resolve(runtime.statePath);
  if(path.dirname(state)!==runRoot||!/^state-[a-f0-9]{12}$/.test(path.basename(state)))
    throw Error('Unsafe owned state path');
  const found=docker('ps','-a','--filter','name=^/'+runtime.name+'$','--format','{{.Names}}').trim();
  if(found)docker('rm','-f',runtime.name);
  containerAbsent=!docker('ps','-a','--filter','name=^/'+runtime.name+'$','--format','{{.Names}}').trim();
  fs.rmSync(state,{recursive:true,force:true});stateAbsent=!fs.existsSync(state);
}
fs.rmSync(path.join(runRoot,'credential-private.json'),{force:true});
const credentialAbsent=!fs.existsSync(path.join(runRoot,'credential-private.json'));
const remainingOwnedState=fs.readdirSync(runRoot).filter(name=>/^state-[a-f0-9]{12}$/.test(name));
write('cleanup-report',{containerAbsent,stateAbsent,credentialAbsent,remainingOwnedState});
if(!containerAbsent||!stateAbsent||!credentialAbsent||remainingOwnedState.length)
  throw Error('Owned resource cleanup incomplete');
