import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {root,json} from './io.mjs';
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8',timeout:10000,stdio:['ignore','pipe','pipe'],windowsHide:true});
const runtime=fs.existsSync(root+'/runtime-private.json')?JSON.parse(fs.readFileSync(root+'/runtime-private.json')):null;
if(!/^attempt-[a-zA-Z0-9-]+$/.test(path.basename(root))||path.basename(path.dirname(root))!=='capture'||fs.realpathSync(root)!==path.resolve(root))throw Error('Unsafe attempt root');
let containerAbsent=true,stateAbsent=true;
let browserAbsent=true,browserIdentityMatched=null;
const browserFile=root+'/owned-browser-private.json';
if(fs.existsSync(browserFile)){const owned=JSON.parse(fs.readFileSync(browserFile));
  if(!Number.isSafeInteger(owned.pid)||owned.pid<=1)throw Error('Unsafe browser PID');
  const present=()=>fs.existsSync('/proc/'+owned.pid+'/stat');
  if(present()){browserIdentityMatched=fs.readFileSync('/proc/'+owned.pid+'/stat','utf8').split(' ')[21]===owned.startTicks;
    if(!browserIdentityMatched)throw Error('Browser process identity changed');
    process.kill(owned.pid,'SIGTERM');const deadline=Date.now()+5000;
    while(present()&&Date.now()<deadline)await new Promise(r=>setTimeout(r,100));
    if(present()){process.kill(owned.pid,'SIGKILL');await new Promise(r=>setTimeout(r,250));}}
  browserAbsent=!present();}
if(runtime){
  if(!/^qopenbb-tooltip-20261017-[a-f0-9]{10}$/.test(runtime.name))throw Error('Unsafe container name');
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
json('cleanup-report',{containerAbsent,stateAbsent,credentialAbsent,remainingOwnedState,browserAbsent,browserIdentityMatched});
if(!containerAbsent||!stateAbsent||!credentialAbsent||remainingOwnedState.length||!browserAbsent)throw Error('Cleanup incomplete');
