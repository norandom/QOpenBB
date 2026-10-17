import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const root=path.dirname(new URL(import.meta.url).pathname);
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8',stdio:['ignore','pipe','pipe']});
const receipt=root+'/runtime-private.json';
const runtime=fs.existsSync(receipt)?JSON.parse(fs.readFileSync(receipt)):null;
let containerAbsent=true,stateAbsent=true;
if(runtime){
  if(!/^qopenbb-axis-grid-20261017-[a-f0-9]{10}$/.test(runtime.name))throw Error('Unsafe container name');
  const state=path.resolve(runtime.statePath);
  if(path.dirname(state)!==root||!/^state-[a-f0-9]{12}$/.test(path.basename(state)))throw Error('Unsafe state path');
  const found=docker('ps','-a','--filter','name=^/'+runtime.name+'$','--format','{{.ID}}').trim();
  if(found)docker('rm','-f',runtime.container||runtime.name);
  fs.rmSync(state,{recursive:true,force:true});
  stateAbsent=!fs.existsSync(state);
  containerAbsent=!docker('ps','-a','--filter','name=^/'+runtime.name+'$','--format','{{.Names}}').trim();
}
fs.rmSync(root+'/credential-private.json',{force:true});
const credentialAbsent=!fs.existsSync(root+'/credential-private.json');
const remainingOwnedState=fs.readdirSync(root).filter(x=>/^state-[a-f0-9]{12}$/.test(x));
const report={containerAbsent,stateAbsent,credentialAbsent,remainingOwnedState};
fs.writeFileSync(root+'/cleanup-report.json',JSON.stringify(report,null,2));
if(!containerAbsent||!stateAbsent||!credentialAbsent||remainingOwnedState.length)throw Error('Owned resource cleanup incomplete');
console.log('Owned container, state and credential absent');
