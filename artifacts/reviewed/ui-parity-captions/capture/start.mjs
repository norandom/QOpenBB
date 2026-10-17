import fs from 'node:fs';
import path from 'node:path';
import {randomBytes} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {runRoot,write} from './io.mjs';
import {limits} from './limits.mjs';
const deadline=Date.now()+limits.startup;
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8',timeout:Math.min(30000,
  Math.max(1,deadline-Date.now())),stdio:['ignore','pipe','pipe'],windowsHide:true});
const image='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f';
const source='38dffc33389aca0e4a87e0e88d42f7067aa220df';
if(JSON.parse(docker('image','inspect',image,'--format','{{json .Id}}'))!==image||
  docker('image','inspect',image,'--format','{{index .Config.Labels "org.qopenbb.source.workspace"}}').trim()!==source)
  throw Error('Original image identity mismatch');
const receipt=path.join(runRoot,'runtime-private.json');
if(fs.existsSync(receipt))throw Error('Runtime receipt already exists; preserve attempt');
const name='qopenbb-captions-'+randomBytes(8).toString('hex');
const statePath=path.join(runRoot,'state-'+randomBytes(6).toString('hex'));
const credential={email:'captions-synthetic@example.com',password:'Aa1!'+randomBytes(24).toString('hex')};
const runtime={name,statePath,image,source,container:null,origin:null,health:null};
fs.mkdirSync(statePath);
fs.writeFileSync(path.join(runRoot,'credential-private.json'),JSON.stringify(credential),{mode:0o600});
const save=()=>fs.writeFileSync(receipt,JSON.stringify(runtime,null,2),{mode:0o600});
save();
runtime.container=docker('run','-d','--name',name,'--mount',`type=bind,src=${statePath},dst=/data`,
  '-p','127.0.0.1::3000','-e',`OPENBB_ADMIN_PASSWORD=${credential.password}`,
  '-e','PUBLIC_URL=http://localhost','-e',`OPENBB_ADMIN_EMAIL=${credential.email}`,image).trim();
save();
while(Date.now()<deadline){
  const ports=JSON.parse(docker('inspect',runtime.name,'--format','{{json .NetworkSettings.Ports}}'));
  const port=ports['3000/tcp']?.[0]?.HostPort;
  if(port){runtime.origin='http://127.0.0.1:'+port;save();try{
    const response=await fetch(runtime.origin+'/api/health',{signal:AbortSignal.timeout(2000)});
    if(response.status===200){runtime.health=200;break;}
  }catch{}}
  await new Promise(resolve=>setTimeout(resolve,500));
}
save();write('runtime-identity',{image,source,health:runtime.health,
  isolation:{disposableState:true,syntheticAccount:true,dynamicLoopbackPort:true}});
if(runtime.health!==200)throw Error('Original image readiness deadline exceeded');
console.log('Original image healthy; fresh disposable caption runtime created');
