import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {randomBytes} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {root,output} from './io.mjs';
import {diagnose,ownerLabel,networkProjection,networkValid} from './projection.mjs';
export function safeFailure(error,stage){return {outcome:'probe-unresolved',stage,reason:error?.probeReason??'unexpected-probe-error',exitCode:Number.isInteger(error?.status)?error.status:null};}
export function fail(reason){const error=Error(reason);error.probeReason=reason;throw error;}
export function command(docker,stage,args,timeout){try{return docker(args,timeout);}catch(error){const safe=Error('docker-command-failed');safe.probeReason='docker-command-failed';safe.status=Number.isInteger(error?.status)?error.status:null;safe.stage=stage;throw safe;}}
export async function healthOnce(port,{request=fetch,remaining=()=>2000}={}){
  if(!/^\d+$/.test(port)||Number(port)<1||Number(port)>65535)return {outcome:'health-unresolved',reason:'invalid-loopback-port'};
  const timeout=Math.min(2000,remaining());if(timeout<=0)return {outcome:'health-unresolved',reason:'input-deadline'};
  try{const response=await request('http://127.0.0.1:'+port+'/api/health',{method:'GET',redirect:'manual',signal:AbortSignal.timeout(Math.max(1,Math.floor(timeout)))});
    const status=response.status,redirect=status>=300&&status<400||response.headers.has('location');await response.body?.cancel();
    return redirect?{outcome:'health-unresolved',reason:'redirect-rejected',status}:{outcome:status===200?'loopback-healthy':'health-unresolved',status};
  }catch{return {outcome:'health-unresolved',reason:'health-transport-or-timeout'};}
}
export async function main(){
  let stage='attempt-admission';const io=output(),samples=[];
  const startedAt=Number(process.env.ATTEMPT_STARTED_MS),remaining=()=>90000-(Date.now()-startedAt);
  const docker=(args,timeout)=>execFileSync('docker',args,{encoding:'utf8',timeout,maxBuffer:262144,stdio:['ignore','pipe','pipe'],windowsHide:true});
  const run=(label,...args)=>{stage=label;const timeout=Math.min(5000,remaining());if(timeout<=0)fail('input-deadline');return command(docker,label,args,Math.max(1,Math.floor(timeout)));};
  const parse=text=>{try{return JSON.parse(text);}catch{fail('inspect-json-unresolved');}};
  try{
    if(!Number.isFinite(startedAt)||remaining()<=0||path.resolve(root)!==fs.realpathSync(root)||path.basename(path.dirname(root))!=='ui-parity-legend-startup-diagnostic'||!/^attempt-[\w-]+$/.test(path.basename(root)))fail('owned-attempt-unresolved');
    const image='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f',source='38dffc33389aca0e4a87e0e88d42f7067aa220df';
    if(parse(run('image-id','image','inspect',image,'--format','{{json .Id}}'))!==image||run('image-source','image','inspect',image,'--format','{{index .Config.Labels "org.qopenbb.source.workspace"}}').trim()!==source)fail('image-identity-unresolved');
    if(fs.existsSync(root+'/runtime-private.json'))fail('existing-runtime-receipt');
    const name='qopenbb-legend-probe-'+randomBytes(5).toString('hex'),statePath=path.join(root,'state-'+randomBytes(6).toString('hex'));
    const credential={email:'legend-probe-'+randomBytes(6).toString('hex')+'@example.com',password:'Aa1!'+randomBytes(24).toString('hex')};
    const runtime={name,networkName:name+'-net',ownership:randomBytes(12).toString('hex'),networkId:null,container:null,statePath,image,source,browserCreated:false,startedAt};
    io.json('runtime-private',runtime,{privateFile:true});io.json('credential-private',credential,{privateFile:true});fs.mkdirSync(statePath);
    const save=()=>io.json('runtime-private',runtime,{privateFile:true});
    runtime.networkId=run('network-create','network','create','--driver','bridge','--internal','--label',ownerLabel+'='+runtime.ownership,runtime.networkName).trim();if(!/^[a-f0-9]{64}$/.test(runtime.networkId))fail('network-id-unresolved');save();
    const network=networkProjection(parse(run('network-inspect','network','inspect',runtime.networkId))[0],runtime);io.json('network-admission',network);if(!networkValid(network))fail('network-isolation-unresolved');
    runtime.container=run('container-create','run','-d','--name',name,'--network',runtime.networkName,'--dns','127.0.0.1','--label',ownerLabel+'='+runtime.ownership,'--mount',`type=bind,src=${statePath},dst=/data`,
      '-e','HTTP_PROXY=','-e','HTTPS_PROXY=','-e','ALL_PROXY=','-e','http_proxy=','-e','https_proxy=','-e','all_proxy=',
      '-p','127.0.0.1::3000','-e',`OPENBB_ADMIN_PASSWORD=${credential.password}`,'-e','PUBLIC_URL=http://localhost','-e',`OPENBB_ADMIN_EMAIL=${credential.email}`,image).trim();if(!/^[a-f0-9]{64}$/.test(runtime.container))fail('container-id-unresolved');save();
    const runReturnedAt=performance.now(),deadline=runReturnedAt+Math.max(0,remaining());
    const result=await diagnose({runReturnedAt,deadline,inspect:async()=>({container:parse(run('container-inspect','inspect',runtime.container))[0],network:parse(run('network-inspect','network','inspect',runtime.networkId))[0],expected:runtime}),
      persist:async receipt=>{samples.push(receipt);io.json('samples',samples);},health:port=>healthOnce(port,{remaining})});
    io.json('probe-result',{...result,originalSource:source,image,browserCreated:false,noRetry:true});
    if(result.health?.outcome!=='loopback-healthy')process.exitCode=1;
  }catch(error){io.json('probe-result',{...safeFailure(error,stage),samples:samples.length,browserCreated:false,noRetry:true});process.exitCode=1;}
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))await main();
