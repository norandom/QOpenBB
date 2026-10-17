import {limits} from './contract.mjs';

export const bytes=value=>Buffer.byteLength(JSON.stringify(value));
export const retention=Object.freeze({sampleBytes:4096,baselineBytes:2048,entryBytes:6144,
  invocationBytes:14336,inputReserve:32768,caseGuard:115072,tailReserve:16000});
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function fail(reason){throw Error('keyboard-retention-unresolved: '+reason);}
function text(value,max){if(typeof value!=='string'||value.length>max)fail('text cap');return value;}
function finite(value){if(typeof value!=='number'||!Number.isFinite(value)||Math.abs(value)>1e9)fail('finite number cap');return value;}
function nullableText(value,max){return value===null?null:text(value,max);}
function bool(value){if(typeof value!=='boolean')fail('boolean');return value;}
function bounded(value,max,label){if(bytes(value)>max)fail(label+' bytes');return value;}
function rect(value){if(value===null)return null;return Object.fromEntries(['x','y','width','height'].map(k=>[k,finite(value?.[k])]));}
function active(value){if(value===null)return null;return {tag:text(value?.tag,64),role:nullableText(value.role,128),name:text(value.name,512),
  tabindex:nullableText(value.tabindex,32),id:nullableText(value.id,256),focusVisible:bool(value.focusVisible),rect:rect(value.rect),inSeriesArea:bool(value.inSeriesArea)};}
function array(value,max,project){if(!Array.isArray(value)||value.length>max)fail('array cap');return value.map(project);}
function tooltip(value){if(value===null||value?.visible===false)return {visible:false};
  if(value?.visible!==true)fail('tooltip visibility');
  return {visible:true,heading:array(value.heading,1,v=>text(v,512)),
    rows:array(value.rows,3,row=>({label:text(row.label,512),value:text(row.value,512)})),
    compact:array(value.compact,4,v=>text(v,512)),pagination:bool(value.pagination)};}
export function sample(raw){return bounded({active:active(raw.active),tooltip:tooltip(raw.tooltip),liveStatus:text(raw.liveStatus,2048)},retention.sampleBytes,'sample');}
export function modeSample(mode,raw){
  const baseline=bounded({area:active(raw.area),swapchain:array(raw.swapchain,2,active)},retention.baselineBytes,'baseline');
  if(mode.baseline===undefined)mode.baseline=baseline;
  else if(!same(mode.baseline,baseline))fail('area/swapchain baseline changed');
  return sample(raw);
}
export function settlement(raw){
  if(raw.status==='stable'&&(raw.pair?.length!==2||!same(raw.pair[0],raw.pair[1])))fail('full DOM pair unequal');
  return {status:text(raw.status,64),pair:array(raw.pair,2,sample),sampleCount:finite(raw.sampleCount),elapsedMs:finite(raw.elapsedMs)};
}
export function invocation(value){return bounded(value,retention.invocationBytes,'invocation');}
export function entry(value){return bounded(value,retention.entryBytes,'entry');}
export function controlReceipt(value){return bounded(value,1024,'control receipt');}
export function finalTail(events,elapsedMs){return bounded({events,elapsedMs:finite(elapsedMs)},retention.tailReserve,'final tail');}
export function reserveInput(current){
  // Reserve before counters or emitted input; large unseen states stop rather than borrow later capacity.
  if(current.id!=='T06')return;
  if(bytes(current)+retention.inputReserve>retention.caseGuard)throw Error('not-run-budget');
}
export function casePrewrite(current){
  if(current.id!=='T06')return;
  if(limits.caseBytes!==retention.caseGuard+retention.tailReserve)fail('case bound changed');
  if(bytes(current)>limits.caseBytes)throw Error('Case JSON bound');
  for(const item of current.ledger??[])entry(item);
  for(const mode of current.keyboard??[]){
    if(mode.baseline)bounded(mode.baseline,retention.baselineBytes,'baseline');
    for(const item of [...(mode.tabs??[]),...(mode.keys??[])])invocation(item);
  }
}
