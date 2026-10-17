import {isIPv4} from 'node:net';
export const ownerLabel='org.qopenbb.capture.owner';
export const image='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f';
export const source='38dffc33389aca0e4a87e0e88d42f7067aa220df';
export function fail(reason){const error=Error(reason);error.probeReason=reason;throw error;}
export function safeFailure(error,stage){return {outcome:'probe-unresolved',stage,reason:error?.probeReason??'unexpected-probe-error',exitCode:Number.isInteger(error?.status)?error.status:null};}
export function command(docker,stage,args,timeout){try{return docker(args,timeout);}catch(error){const safe=Error('docker-command-failed');safe.probeReason='docker-command-failed';safe.status=Number.isInteger(error?.status)?error.status:null;safe.stage=stage;throw safe;}}
const own=(object,key)=>object!=null&&Object.hasOwn(object,key);
function scalar(value){return typeof value==='boolean'||typeof value==='number'&&Number.isFinite(value)||typeof value==='string'&&value.length<=128?value:null;}
function ports(value,target){const entries=value?.[target];return {parentSupported:value!==null&&typeof value==='object'&&!Array.isArray(value),own:own(value,target),kind:entries===undefined?'absent':entries===null?'null':Array.isArray(entries)?'array':'unsupported',
  count:Array.isArray(entries)?entries.length:null,entries:Array.isArray(entries)&&entries.length<=4?entries.map(entry=>({HostIp:scalar(entry?.HostIp),HostPort:scalar(entry?.HostPort)})):[],
  otherPublication:Object.entries(value??{}).some(([key,list])=>key!==target&&list!==null&&(!Array.isArray(list)||list.length!==0)),parentKeys:Object.keys(value??{}).length};}
export function networkProjection(raw,runtime,kind){return {idMatched:raw?.Id===runtime[kind+'NetworkId'],nameMatched:raw?.Name===runtime.name+'-'+kind,
  labelMatched:raw?.Labels?.[ownerLabel]===runtime.ownership,driverBridge:raw?.Driver==='bridge',internalMatched:raw?.Internal===(kind==='internal'),ipv6Disabled:raw?.EnableIPv6===false};}
export const allTrue=record=>Object.values(record).every(value=>value===true);
export function projectContainer(raw,runtime,kind){
  const settings=raw?.NetworkSettings,networks=settings?.Networks??{},host=raw?.HostConfig??{},expected=kind==='app'?['internal']:['internal','ingress'];
  const internal=networks[runtime.name+'-internal'],target=kind==='app'?'3000/tcp':'3100/tcp';
  const attachments=Object.keys(networks),state=raw?.State??{},relay=kind==='relay';
  const security={idMatched:raw?.Id===runtime[kind+'Id'],nameMatched:raw?.Name==='/'+runtime.name+'-'+kind,labelMatched:raw?.Config?.Labels?.[ownerLabel]===runtime.ownership,
    exactNetworks:attachments.length===expected.length&&expected.every(key=>networks[runtime.name+'-'+key]?.NetworkID===runtime[key+'NetworkId']),
    restartDisabled:host.RestartPolicy?.Name==='no',imageMatched:raw?.Image===image,unprivileged:host.Privileged===false,publishAllDisabled:host.PublishAllPorts===false,
    exactPrimaryNetwork:host.NetworkMode===runtime.name+'-'+(relay?'ingress':'internal')};
  if(relay)Object.assign(security,{readOnlyRootfs:host.ReadonlyRootfs===true,nonRoot:raw?.Config?.User==='65534:65534',capDropAll:host.CapDrop?.length===1&&host.CapDrop[0]==='ALL',
    noNewPrivileges:host.SecurityOpt?.length===1&&host.SecurityOpt[0]==='no-new-privileges',forwardingDisabled:Object.keys(host.Sysctls??{}).length===2&&host.Sysctls?.['net.ipv4.ip_forward']==='0'&&host.Sysctls?.['net.ipv6.conf.all.forwarding']==='0',
    healthDisabled:raw?.Config?.Healthcheck?.Test?.length===1&&raw.Config.Healthcheck.Test[0]==='NONE',
    pythonEntrypoint:raw?.Config?.Entrypoint?.length===1&&raw.Config.Entrypoint[0]==='/opt/.venv/bin/python',
    exactCommand:JSON.stringify(raw?.Config?.Cmd)===JSON.stringify(['-B','-I','-S','-u','/relay/relay.py','/relay/config.json']),
    exactMounts:Array.isArray(raw?.Mounts)&&raw.Mounts.length===4&&[
      ['/relay/relay.py',runtime.relaySourcePath,false,'bind'],['/relay/config.json',runtime.configPath,false,'bind'],['/evidence/relay-stats.json',runtime.statsPath,true,'bind'],['/data',null,true,'tmpfs']
    ].every(([destination,sourcePath,rw,type])=>raw.Mounts.some(mount=>mount.Destination===destination&&mount.Type===type&&mount.RW===rw&&(sourcePath===null||mount.Source===sourcePath))),
    boundedTmpfs:host.Tmpfs?.['/data']==='rw,nosuid,nodev,size=1048576'});
  return {kind,security,configured:ports(host.PortBindings,target),runtime:ports(settings?.Ports,target),
    noConfiguredPublications:host.PortBindings!=null&&typeof host.PortBindings==='object'&&!Array.isArray(host.PortBindings)&&Object.keys(host.PortBindings).length<=8&&Object.values(host.PortBindings).every(list=>Array.isArray(list)&&list.length===0),
    noRuntimePublications:settings?.Ports!=null&&typeof settings.Ports==='object'&&!Array.isArray(settings.Ports)&&Object.keys(settings.Ports).length<=8&&Object.values(settings.Ports).every(list=>list===null||Array.isArray(list)&&list.length===0),
    internalIPv4:typeof internal?.IPAddress==='string'&&internal.IPAddress.length<=15?internal.IPAddress:null,
    state:Object.fromEntries(['Status','Running','Restarting','Dead','ExitCode','OOMKilled'].map(key=>[key,scalar(state[key])]))};
}
export function admitContainer(receipt){
  if(!allTrue(receipt.security))return {kind:'security-unresolved'};
  const s=receipt.state;if(s.Status!=='running'||s.Running!==true||s.Restarting!==false||s.Dead!==false||s.OOMKilled!==false||s.ExitCode!==0)return {kind:'container-not-running'};
  if(!isIPv4(receipt.internalIPv4??'')||/^(0|127|22[4-9]|23\d)\./.test(receipt.internalIPv4))return {kind:'internal-address-unresolved'};
  if(receipt.kind==='app')return receipt.noConfiguredPublications&&receipt.noRuntimePublications?{kind:'app-admitted',address:receipt.internalIPv4}:{kind:'app-publication-unresolved'};
  const cfg=receipt.configured,actual=receipt.runtime;
  for(const item of [cfg,actual])if(!item.parentSupported||item.parentKeys>8||item.otherPublication||item.kind!=='array'||item.count!==1||item.entries[0]?.HostIp!=='127.0.0.1')return {kind:'loopback-binding-unresolved'};
  if(!(cfg.entries[0].HostPort===''||/^\d+$/.test(cfg.entries[0].HostPort??'')))return {kind:'configured-port-unresolved'};
  const port=actual.entries[0].HostPort;if(typeof port!=='string'||!/^\d+$/.test(port)||Number(port)<1||Number(port)>65535)return {kind:'runtime-port-unresolved'};
  return {kind:'relay-admitted',port};
}
export function observeContainer(raw,runtime,kind,persist){const receipt=projectContainer(raw,runtime,kind);persist(receipt);return {receipt,decision:admitContainer(receipt)};}
export function statsDecision(stats){
  const limits={acceptedPairs:16,activePairs:4,peakPairs:4,peakSockets:9,receivedBytes:33554432,forwardedBytes:33554432,peakBufferedBytes:524288,maximumPairBytes:4194304,refusedConnections:16,peerClosures:16};
  if(!stats||stats.phase!=='closed'||stats.cleanStop!==true||stats.activePairs!==0)return {ok:false,reason:'relay-stop-unobserved'};
  if(Object.entries(limits).some(([key,max])=>!Number.isSafeInteger(stats[key])||stats[key]<0||stats[key]>max)||stats.forwardedBytes>stats.receivedBytes)return {ok:false,reason:'relay-counter-unresolved'};
  const reasons=['accepted-pairs','pair-bytes','total-bytes','connect-timeout','transport-truncated','socket-error','config-error','stats-error'];
  if(!stats.violations||Object.keys(stats.violations).length!==reasons.length||reasons.some(key=>!Number.isSafeInteger(stats.violations[key])||stats.violations[key]<0))return {ok:false,reason:'relay-violations-unresolved'};
  return Object.values(stats.violations).some(Boolean)?{ok:false,reason:'relay-bound-or-transport-breach'}:{ok:true,reason:'relay-counters-admitted'};
}
export async function healthOnce(port,{request=fetch,remaining=()=>2000}={}){
  if(typeof port!=='string'||!/^\d+$/.test(port)||Number(port)<1||Number(port)>65535)return {outcome:'health-unresolved',reason:'invalid-loopback-port'};
  const timeout=Math.min(2000,remaining());if(timeout<=0)return {outcome:'health-unresolved',reason:'input-deadline'};
  try{const response=await request('http://127.0.0.1:'+port+'/api/health',{method:'GET',headers:{Connection:'close'},redirect:'manual',signal:AbortSignal.timeout(Math.max(1,Math.floor(timeout)))});
    const status=response.status,redirect=status>=300&&status<400||response.headers.has('location');
    if(redirect){await response.body?.cancel();return {outcome:'health-unresolved',reason:'redirect-rejected',status};}
    let bytes=0;if(response.body)for await(const chunk of response.body){bytes+=chunk.length;if(bytes>4194304)return {outcome:'health-unresolved',reason:'health-body-bound',status};}
    return {outcome:status===200?'loopback-healthy':'health-unresolved',status};
  }catch{return {outcome:'health-unresolved',reason:'health-transport-or-timeout'};}
}
export async function readiness({port,remaining,request,now=()=>performance.now(),publicationAt,pause=ms=>new Promise(resolve=>setTimeout(resolve,ms)),persist=async()=>{}}){
  const start=publicationAt??now(),attempts=[];let last=-Infinity;
  for(let index=0;index<10;index++){
    const wait=Math.max(0,last+3000-now());if(now()+wait+2000>start+30000||remaining()<wait+2000)break;if(wait)await pause(wait);
    last=now();const result=await healthOnce(port,{request,remaining:()=>Math.min(remaining(),start+30000-now())});attempts.push({index:index+1,startedMs:Math.round(last-start),...result});await persist(attempts);
    if(result.outcome==='loopback-healthy')return {outcome:'readiness-observed',attempts:attempts.length};
    if(result.reason==='redirect-rejected'||result.reason==='health-body-bound')return {outcome:'probe-unresolved',reason:result.reason,attempts:attempts.length};
  }
  return {outcome:'probe-unresolved',reason:'readiness-not-observed-within-fixed-budget',attempts:attempts.length};
}
