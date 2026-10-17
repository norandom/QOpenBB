export const ownerLabel='org.qopenbb.capture.owner';
const own=(object,key)=>object!=null&&Object.hasOwn(object,key);
export function presence(object,key){const found=object!=null&&key in Object(object),value=found?object[key]:undefined;return {own:own(object,key),in:found,kind:!found?'absent':value===undefined?'undefined':value===null?'null':'value',type:found?typeof value:'absent',...(value===null?{value:null}:{})};}
export function field(object,key,errors){const record=presence(object,key),value=object?.[key];if(record.kind!=='value')return record;
  if(typeof value==='boolean'||typeof value==='number'&&Number.isFinite(value)||typeof value==='string'&&value.length<=128)return {...record,value};
  errors.push('unsupported-selected-scalar');return {...record,unsupported:true,...(typeof value==='string'?{length:value.length}:{})};}
function target(parent,key,errors){const value=parent?.[key],record=presence(parent,key);if(record.kind!=='value')return record;
  if(!Array.isArray(value)){errors.push('target-array-type');return {...record,unsupported:true};}
  if(value.length>4){errors.push('target-array-bound');return {...record,arrayLength:value.length,unsupported:true};}
  return {...record,arrayLength:value.length,entries:value.map(entry=>({HostIp:field(entry,'HostIp',errors),HostPort:field(entry,'HostPort',errors)}))};}
function parentRecord(object,key,errors){const record=presence(object,key),value=object?.[key];if(record.kind==='value'&&(typeof value!=='object'||Array.isArray(value)))errors.push('selected-parent-type');return record;}
export function networkProjection(raw,expected){return {idMatched:raw?.Id===expected.networkId,nameMatched:raw?.Name===expected.networkName,labelMatched:raw?.Labels?.[ownerLabel]===expected.ownership,driverBridge:raw?.Driver==='bridge',internal:raw?.Internal===true,ipv6Disabled:raw?.EnableIPv6===false};}
export function networkValid(record){return Object.values(record).every(value=>value===true);}
export function projectContainer(raw,network,expected,context){
  const errors=[],networks=raw?.NetworkSettings?.Networks,networkKeys=Object.keys(networks??{});
  const ports=raw?.NetworkSettings?.Ports,bindings=raw?.HostConfig?.PortBindings;
  return {context:{...context,containerId:expected.container,networkId:expected.networkId},errors,
    security:{containerIdMatched:raw?.Id===expected.container,labelMatched:raw?.Config?.Labels?.[ownerLabel]===expected.ownership,attachedNetworkCount:networkKeys.length,
      exactNetwork:networkKeys.length===1&&networkKeys[0]===expected.networkName&&networks[networkKeys[0]]?.NetworkID===expected.networkId,network:networkProjection(network,expected)},
    runtime:{NetworkSettings:parentRecord(raw,'NetworkSettings',errors),Ports:parentRecord(raw?.NetworkSettings,'Ports',errors),target:target(ports,'3000/tcp',errors)},
    configured:{HostConfig:parentRecord(raw,'HostConfig',errors),PortBindings:parentRecord(raw?.HostConfig,'PortBindings',errors),target:target(bindings,'3000/tcp',errors)},
    state:{presence:presence(raw,'State'),...Object.fromEntries(['Status','Running','Restarting','Dead','ExitCode','OOMKilled','StartedAt','FinishedAt'].map(key=>[key,field(raw?.State,key,errors)]))}};
}
const missing=record=>record.kind!=='value'||record.arrayLength===0;
const value=(record,key)=>record.entries?.[0]?.[key]?.value;
const port=value=>typeof value==='string'&&/^\d+$/.test(value)&&Number(value)>=1&&Number(value)<=65535;
export function classify(receipt){
  const s=receipt.security,state=receipt.state,cfg=receipt.configured.target,actual=receipt.runtime.target;
  if(receipt.errors.length)return {kind:'projection-unresolved'};
  if(!s.containerIdMatched||!s.labelMatched||s.attachedNetworkCount!==1||!s.exactNetwork||!networkValid(s.network))return {kind:'security-unresolved'};
  for(const record of [cfg,actual])if(!missing(record)&&record.entries?.some(entry=>entry.HostIp.value!=='127.0.0.1'))return {kind:'security-unresolved'};
  for(const [key,type] of [['Status','string'],['Running','boolean'],['Restarting','boolean'],['Dead','boolean'],['ExitCode','number'],['OOMKilled','boolean'],['StartedAt','string'],['FinishedAt','string']])if(state[key].kind!=='value'||state[key].type!==type)return {kind:'state-unresolved'};
  if(state.Status.value!=='running'||state.Running.value!==true||state.Restarting.value!==false||state.Dead.value!==false)return {kind:'container-not-running'};
  if(missing(cfg))return {kind:'configured-binding-missing'};
  if(cfg.arrayLength!==1||typeof value(cfg,'HostPort')!=='string'||!(value(cfg,'HostPort')===''||/^\d+$/.test(value(cfg,'HostPort'))&&Number(value(cfg,'HostPort'))<=65535))return {kind:'configured-binding-unresolved'};
  if(missing(actual))return {kind:'allocation-pending'};
  if(actual.arrayLength!==1||!port(value(actual,'HostPort')))return {kind:'publication-shape-unresolved'};
  return {kind:'publication-observed',port:value(actual,'HostPort')};
}
export async function diagnose({inspect,persist,health,now=()=>performance.now(),pause=ms=>new Promise(resolve=>setTimeout(resolve,ms)),runReturnedAt,deadline}){
  let priorMissing=false;
  for(const [index,offset] of [0,1000,3000].entries()){
    if(now()>=deadline)return {outcome:'deadline-unresolved',samples:index};
    const wait=runReturnedAt+offset-now();if(wait>0){if(now()+wait>=deadline)return {outcome:'deadline-unresolved',samples:index};await pause(wait);}
    const readStartedMs=now(),{container,network,expected}=await inspect();
    const receipt=projectContainer(container,network,expected,{sample:index+1,plannedOffsetMs:offset,readStartedMs,readEndedMs:now(),elapsedSinceRunReturnMs:now()-runReturnedAt});
    await persist(receipt); // A stopping assertion must not discard its operands.
    if(now()>=deadline)return {outcome:'deadline-unresolved',samples:index+1};
    const decision=classify(receipt);
    if(decision.kind==='publication-observed')return {outcome:priorMissing?'delayed-publication-observed':'publication-observed',samples:index+1,health:await health(decision.port)};
    if(decision.kind!=='allocation-pending')return {outcome:decision.kind,samples:index+1};priorMissing=true;
  }
  return {outcome:'publication-not-observed-within-window',samples:3};
}
