import fs from 'node:fs';
import path from 'node:path';
import {randomBytes} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {root,json} from './io.mjs';
import {ownerLabel,networkGuard,containerNetworkGuard} from './network.mjs';
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8',timeout:10000,stdio:['ignore','pipe','pipe'],windowsHide:true});
const image='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f';
const source='38dffc33389aca0e4a87e0e88d42f7067aa220df';
if(path.resolve(root)!==fs.realpathSync(root)||!/^attempt-[A-Za-z0-9-]+$/.test(path.basename(root))||path.basename(path.dirname(root))!=='ui-parity-legend-capture-redirect-guard')throw Error('Canonical owned attempt required');
if(JSON.parse(docker('image','inspect',image,'--format','{{json .Id}}'))!==image||
  docker('image','inspect',image,'--format','{{index .Config.Labels "org.qopenbb.source.workspace"}}').trim()!==source)throw Error('Image mismatch');
if(fs.existsSync(root+'/runtime-private.json'))throw Error('Previous runtime receipt exists');
const startedAt=Number(process.env.ATTEMPT_STARTED_MS);if(!Number.isFinite(startedAt)||Date.now()-startedAt>180000)throw Error('Startup deadline');
const name='qopenbb-legend-20261017-'+randomBytes(5).toString('hex');
const networkName=name+'-net',ownership=randomBytes(12).toString('hex');
const statePath=root+'/state-'+randomBytes(6).toString('hex');
const credential={email:'legend-controls-'+randomBytes(6).toString('hex')+'@example.com',password:'Aa1!'+randomBytes(24).toString('hex')};
fs.mkdirSync(statePath);fs.writeFileSync(root+'/credential-private.json',JSON.stringify(credential),{mode:0o600});
const runtime={name,statePath,image,source,startedAt,ownedProcessId:process.pid,ownership,networkName,networkId:null,container:null,origin:null,health:null};
const save=()=>fs.writeFileSync(root+'/runtime-private.json',JSON.stringify(runtime),{mode:0o600});save();
runtime.networkId=docker('network','create','--driver','bridge','--internal','--label',ownerLabel+'='+ownership,networkName).trim();save();
const networkReceipt=networkGuard(runtime,JSON.parse(docker('network','inspect',runtime.networkId))[0]);
runtime.container=docker('run','-d','--name',name,'--network',networkName,'--dns','127.0.0.1','--label',ownerLabel+'='+ownership,'--mount',`type=bind,src=${statePath},dst=/data`,
  '-e','HTTP_PROXY=','-e','HTTPS_PROXY=','-e','ALL_PROXY=','-e','http_proxy=','-e','https_proxy=','-e','all_proxy=',
  '-p','127.0.0.1::3000','-e',`OPENBB_ADMIN_PASSWORD=${credential.password}`,'-e','PUBLIC_URL=http://localhost',
  '-e',`OPENBB_ADMIN_EMAIL=${credential.email}`,image).trim();save();
const deadline=Math.min(Date.now()+90000,startedAt+180000);
let publication=null;
while(Date.now()<deadline){
  networkGuard(runtime,JSON.parse(docker('network','inspect',runtime.networkId))[0]);
  publication=containerNetworkGuard(runtime,JSON.parse(docker('inspect',runtime.container))[0]);
  const port=publication.port;
  if(port){runtime.origin='http://127.0.0.1:'+port;try{
    if((await fetch(runtime.origin+'/api/health',{redirect:'error',signal:AbortSignal.timeout(2000)})).status===200){runtime.health=200;break;}
  }catch{}}
  await new Promise(resolve=>setTimeout(resolve,500));
}
save();json('runtime-identity',{image,source,health:runtime.health,isolation:{freshRandomAccount:true,disposableState:true,dynamicLoopback:true,network:networkReceipt,publication,loopbackHealthProbed:runtime.health===200}});
if(runtime.health!==200)throw Error('Readiness deadline exceeded');
