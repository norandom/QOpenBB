import fs from 'node:fs';
import path from 'node:path';
import {randomBytes} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {root,json} from './io.mjs';
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8',timeout:10000,stdio:['ignore','pipe','pipe'],windowsHide:true});
const image='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f';
const source='38dffc33389aca0e4a87e0e88d42f7067aa220df';
if(process.env.TOOLTIP_HEAVY_GRANTED!=='yes')throw Error('Explicit root heavy grant required');
if(!/^attempt-[a-zA-Z0-9-]+$/.test(path.basename(root))||path.basename(path.dirname(root))!=='capture'||fs.realpathSync(root)!==path.resolve(root))throw Error('Unsafe attempt root');
if(JSON.parse(docker('image','inspect',image,'--format','{{json .Id}}'))!==image||
  docker('image','inspect',image,'--format','{{index .Config.Labels "org.qopenbb.source.workspace"}}').trim()!==source)throw Error('Image mismatch');
if(fs.existsSync(root+'/runtime-private.json'))throw Error('Previous runtime receipt exists');
const name='qopenbb-tooltip-20261017-'+randomBytes(5).toString('hex');
const statePath=root+'/state-'+randomBytes(6).toString('hex');
const credential={email:'tooltip-'+randomBytes(6).toString('hex')+'@example.com',password:'Aa1!'+randomBytes(24).toString('hex')};
fs.mkdirSync(statePath);fs.writeFileSync(root+'/credential-private.json',JSON.stringify(credential),{mode:0o600});
const runtime={name,statePath,image,source,container:null,origin:null,health:null};
const save=()=>fs.writeFileSync(root+'/runtime-private.json',JSON.stringify(runtime),{mode:0o600});save();
runtime.container=docker('run','-d','--name',name,'--mount',`type=bind,src=${statePath},dst=/data`,
  '-p','127.0.0.1::3000','-e',`OPENBB_ADMIN_PASSWORD=${credential.password}`,'-e','PUBLIC_URL=http://localhost',
  '-e',`OPENBB_ADMIN_EMAIL=${credential.email}`,image).trim();save();
const deadline=Date.now()+90000;
while(Date.now()<deadline){
  const ports=JSON.parse(docker('inspect',runtime.container,'--format','{{json .NetworkSettings.Ports}}'));
  const port=ports['3000/tcp']?.[0]?.HostPort;
  if(port){runtime.origin='http://127.0.0.1:'+port;try{
    if((await fetch(runtime.origin+'/api/health',{signal:AbortSignal.timeout(2000)})).status===200){runtime.health=200;break;}
  }catch{}}
  await new Promise(resolve=>setTimeout(resolve,500));
}
save();json('runtime-identity',{image,source,health:runtime.health,isolation:{freshRandomAccount:true,disposableState:true,dynamicLoopback:true}});
if(runtime.health!==200)throw Error('Readiness deadline exceeded');
