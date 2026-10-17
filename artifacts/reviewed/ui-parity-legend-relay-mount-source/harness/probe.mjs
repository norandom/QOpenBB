import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {randomBytes,createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {root,output,verifySource} from './io.mjs';
import {fail,safeFailure,command,ownerLabel,image,source,networkProjection,networkValid,observeContainer,readiness} from './admission.mjs';
export function ownedRoot(directory){return path.resolve(directory)===fs.realpathSync(directory)&&path.basename(path.dirname(directory))==='ui-parity-legend-relay-mount-source'&&/^attempt-[\w-]+$/.test(path.basename(directory));}
export function appArgs(runtime,credential){return ['run','-d','--name',runtime.name+'-app','--network',runtime.name+'-internal','--dns','127.0.0.1','--label',ownerLabel+'='+runtime.ownership,
  '--mount',`type=bind,src=${runtime.statePath},dst=/data`,'-e','HTTP_PROXY=','-e','HTTPS_PROXY=','-e','ALL_PROXY=','-e','http_proxy=','-e','https_proxy=','-e','all_proxy=',
  '-e',`OPENBB_ADMIN_PASSWORD=${credential.password}`,'-e','PUBLIC_URL=http://localhost','-e',`OPENBB_ADMIN_EMAIL=${credential.email}`,image];}
export function relayArgs(runtime){return ['create','--name',runtime.name+'-relay','--network',runtime.name+'-ingress','--dns','127.0.0.1','--label',ownerLabel+'='+runtime.ownership,
  '-p','127.0.0.1::3100','--entrypoint','/opt/.venv/bin/python','--read-only','--user','65534:65534','--cap-drop','ALL','--security-opt','no-new-privileges',
  '--sysctl','net.ipv4.ip_forward=0','--sysctl','net.ipv6.conf.all.forwarding=0','--no-healthcheck','--tmpfs','/data:rw,nosuid,nodev,size=1048576',
  '--mount',`type=bind,src=${runtime.relaySourcePath},dst=/relay/relay.py,readonly`,
  '--mount',`type=bind,src=${runtime.configPath},dst=/relay/config.json,readonly`,
  '--mount',`type=bind,src=${runtime.statsPath},dst=/evidence/relay-stats.json`,image,'-B','-I','-S','-u','/relay/relay.py','/relay/config.json'];}
export async function main(){
  let stage='attempt-admission';const io=output(),receipts={networks:{},containers:{}};
  const startedAt=Number(process.env.ATTEMPT_STARTED_MS),remaining=()=>90000-(Date.now()-startedAt);
  const docker=(args,timeout)=>execFileSync('docker',args,{encoding:'utf8',timeout,maxBuffer:262144,stdio:['ignore','pipe','pipe'],windowsHide:true});
  const run=(label,...args)=>{stage=label;const timeout=Math.min(5000,remaining());if(timeout<=0)fail('input-deadline');return command(docker,label,args,Math.max(1,Math.floor(timeout)));};
  const parse=text=>{try{return JSON.parse(text);}catch{fail('inspect-json-unresolved');}};
  const persist=()=>io.json('admission-receipts',receipts);
  try{
    if(!Number.isFinite(startedAt)||remaining()<=0||!ownedRoot(root))fail('owned-attempt-unresolved');
    stage='attempt-source-verification';verifySource(root);
    if(parse(run('image-id','image','inspect',image,'--format','{{json .Id}}'))!==image||run('image-source','image','inspect',image,'--format','{{index .Config.Labels "org.qopenbb.source.workspace"}}').trim()!==source)fail('image-identity-unresolved');
    if(fs.existsSync(root+'/runtime-private.json'))fail('existing-runtime-receipt');
    const name='qopenbb-legend-relay-'+randomBytes(5).toString('hex'),statePath=path.join(root,'state-'+randomBytes(6).toString('hex'));
    const credential={email:'legend-probe-'+randomBytes(6).toString('hex')+'@example.com',password:'Aa1!'+randomBytes(24).toString('hex')};
    const runtime={name,ownership:randomBytes(12).toString('hex'),internalNetworkId:null,ingressNetworkId:null,appId:null,relayId:null,statePath,
      relaySourcePath:path.join(root,'harness','relay.py'),configPath:path.join(root,'relay-config.json'),statsPath:path.join(root,'relay-stats.json'),image,source,browserCreated:false,startedAt};
    io.json('runtime-private',runtime,{privateFile:true});io.json('credential-private',credential,{privateFile:true});fs.mkdirSync(statePath);
    const save=()=>io.json('runtime-private',runtime,{privateFile:true});
    for(const kind of ['internal','ingress']){
      runtime[kind+'NetworkId']=run('network-create-'+kind,'network','create','--driver','bridge',...(kind==='internal'?['--internal']:[]),'--label',ownerLabel+'='+runtime.ownership,name+'-'+kind).trim();
      if(!/^[a-f0-9]{64}$/.test(runtime[kind+'NetworkId']))fail('network-id-unresolved');save();
      receipts.networks[kind]=networkProjection(parse(run('network-inspect-'+kind,'network','inspect',runtime[kind+'NetworkId']))[0],runtime,kind);persist();
      if(!networkValid(receipts.networks[kind]))fail('network-isolation-unresolved');
    }
    runtime.appId=run('app-create',...appArgs(runtime,credential)).trim();if(!/^[a-f0-9]{64}$/.test(runtime.appId))fail('app-id-unresolved');save();
    const observe=(kind,raw)=>observeContainer(raw,runtime,kind,receipt=>{receipts.containers[kind]=receipt;persist();});
    const app=observe('app',parse(run('app-inspect','inspect',runtime.appId))[0]).decision;if(app.kind!=='app-admitted')fail(app.kind);
    io.json('relay-config',{upstreamIPv4:app.address,upstreamPort:3000});
    io.reserveJson('relay-stats',{phase:'not-started'},4096);fs.chmodSync(runtime.statsPath,0o666);
    receipts.config={sha256:createHash('sha256').update(fs.readFileSync(runtime.configPath)).digest('hex'),fixedUpstreamIPv4:app.address,fixedUpstreamPort:3000};persist();
    runtime.relayId=run('relay-create',...relayArgs(runtime)).trim();if(!/^[a-f0-9]{64}$/.test(runtime.relayId))fail('relay-id-unresolved');save();
    run('relay-connect-internal','network','connect',runtime.internalNetworkId,runtime.relayId);
    run('relay-start','start',runtime.relayId);
    const relay=observe('relay',parse(run('relay-inspect','inspect',runtime.relayId))[0]).decision,publicationAt=performance.now();if(relay.kind!=='relay-admitted')fail(relay.kind);
    // Re-admit the same app and both network identities immediately before any health input.
    if(observe('app',parse(run('app-reinspect','inspect',runtime.appId))[0]).decision.address!==app.address)fail('app-address-or-security-drift');
    for(const kind of ['internal','ingress']){receipts.networks[kind]=networkProjection(parse(run('network-reinspect-'+kind,'network','inspect',runtime[kind+'NetworkId']))[0],runtime,kind);persist();if(!networkValid(receipts.networks[kind]))fail('network-security-drift');}
    const result=await readiness({port:relay.port,remaining,publicationAt,persist:async attempts=>io.json('health-attempts',attempts)});
    io.json('probe-result',{...result,originalSource:source,image,browserCreated:false,noRetry:true,relayFinalCountersRequired:true});
    if(result.outcome!=='readiness-observed')process.exitCode=1;
  }catch(error){io.json('probe-result',{...safeFailure(error,stage),browserCreated:false,noRetry:true,relayFinalCountersRequired:true});process.exitCode=1;}
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))await main();
