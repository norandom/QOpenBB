import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {runRoot,write} from './io.mjs';
import {roles,rows,limits} from './limits.mjs';
const read=name=>JSON.parse(fs.readFileSync(path.join(runRoot,name)));
const value=field=>field?.value;
const values=fields=>Object.fromEntries(Object.entries(fields||{}).map(([key,field])=>[key,value(field)]));
const names=fs.readdirSync(runRoot).filter(name=>/^\d{3}-.*\.json$/.test(name)).sort();
const snapshots=names.map(name=>({name,...read(name)}));
const ledger=read('action-ledger.json'),summary=read('summary.json'),cases=read('cases.json');
const baseline=snapshots[0].state;
const axis=(snapshot,role)=>snapshot.effective.axes.find(item=>value(item.identity.type)===role.type&&
  value(item.identity.position)===role.position);
const roleSource=(snapshot,role)=>role.key?snapshot.effective[role.key]:axis(snapshot,role).title;
function roleScene(snapshot,role){
  if(role.key)return snapshot.scene[role.key].node;
  return snapshot.scene.axes.find(item=>value(item.identity.type)===role.type&&
    value(item.identity.position)===role.position).titleCaption.node;
}
const roleState=(snapshot,role)=>({label:role.label,effective:values(roleSource(snapshot,role)),
  node:values(roleScene(snapshot,role).fields),bbox:values(roleScene(snapshot,role).bbox),
  ancestors:roleScene(snapshot,role).ancestors?.map(parent=>({className:parent.className,fields:values(parent.fields)})),
  coordinateSpace:roleScene(snapshot,role).coordinateSpace});
const geometry=snapshot=>({padding:values(snapshot.effective.padding),livePadding:values(snapshot.scene.padding),
  seriesRect:values(snapshot.scene.seriesRect),captions:roles.map(role=>roleState(snapshot,role)),
  legendBounds:snapshot.scene.legend.bounds,canvas:snapshot.geometry.canvas,editor:snapshot.geometry.editor,
  dpr:snapshot.geometry.dpr});
function leaves(object,prefix='',result={}){
  if(object&&typeof object==='object'&&Object.hasOwn(object,'own')&&Object.hasOwn(object,'kind')){
    result[prefix]=object;return result;
  }
  if(object&&typeof object==='object')for(const[key,item]of Object.entries(object))leaves(item,prefix?prefix+'.'+key:key,result);
  return result;
}
const canonical=key=>key.replaceAll('.positions.','.').replaceAll('.legendLabel.','.legend.item.label.')
  .replaceAll('.seriesLabel.','.series.label.');
function differences(before,after){
  const left=leaves(before),right=leaves(after);
  return Object.keys(right).filter(key=>JSON.stringify(left[key])!==JSON.stringify(right[key]))
    .map(key=>({path:canonical(key),before:left[key],after:right[key]}));
}
const deltas=ledger.map(item=>{
  const before=read(item.before).state,after=read(item.after).state;
  let previous=before.model.chartOptions;
  const events=after.events.map((event,index)=>{
    const changed=differences(previous,event.chartOptions);previous=event.chartOptions;
    return {index,identity:event.identity,changed};
  });
  const b=values(before.scene.seriesRect),a=values(after.scene.seriesRect);
  return {name:item.name,case:item.case,before:item.before,after:item.after,input:item.input,
    rawModelDelta:differences(before.model.chartOptions,after.model.chartOptions),events,
    beforeGeometry:geometry(before),afterGeometry:geometry(after),
    seriesRectDelta:Object.fromEntries(['x','y','width','height'].map(key=>[key,a[key]-b[key]]))};
});
const allOn=read('019-all-on.json').state,final=read('100-final-all-on.json').state;
const checks=[];
function check(label,operation){operation();checks.push({label,passed:true});}
check('all nine cases completed',()=>assert.equal(cases.length,9));
check('all four runtime command exits zero',()=>{for(const name of ['start','journey','cleanup','run'])
  assert.equal(read(name+'-status.json').exitCode,0);});
check('owned cleanup complete',()=>{const cleanup=read('cleanup-report.json');
  assert.equal(cleanup.containerAbsent&&cleanup.stateAbsent&&cleanup.credentialAbsent,true);
  assert.equal(cleanup.remainingOwnedState.length,0);assert.equal(read('browser-cleanup.json').closed,true);});
check('counter and case deadlines bounded',()=>{
  assert(summary.interactions<=limits.interactions&&summary.edits<=limits.edits&&summary.durationMs<=limits.journey);
  for(const entry of cases)assert(entry.durationMs<=(entry.name.startsWith('07-')?limits.weightCase:
    entry.name.startsWith('08-')?limits.paddingCase:limits.case));
});
check('every snapshot stable/inactive and retains four-row data/key order',()=>{
  for(const snapshot of snapshots){assert.equal(snapshot.state.settled.animationActive,false);
    assert.equal(snapshot.state.settled.stableSamples,2);assert.deepEqual(snapshot.state.data,baseline.data);
    assert.deepEqual(snapshot.state.effective.series.map(series=>series.identity),baseline.effective.series.map(series=>series.identity));}
  for(const [index,row]of baseline.data.effective.entries()){
    assert.equal(row.values.revenue.value,rows[index].revenue);
    assert.equal(row.values.operatingIncome.value,rows[index].operatingIncome);
    assert.equal(row.period.wrapper.value.value,rows[index].period);
  }
});
check('all-on roles have distinct expected text and visible scene nodes',()=>{
  for(const role of roles){const scene=roleScene(allOn,role);assert.equal(value(roleSource(allOn,role).text),role.text);
    assert.equal(value(scene.fields.text),role.text);assert.equal(value(scene.fields.visible),true);
    assert.equal(scene.parentLink?.field,'parentNode');assert.equal(scene.parentLink?.present,true);
    assert(scene.ancestors.length>0);
    assert(scene.ancestors.every(parent=>value(parent.fields.visible)!==false&&value(parent.fields.opacity)!==0));}
});
check('each off case hides only selected caption and retains source text',()=>{
  const offNames=['021-disable-chart-title-after.json','025-disable-subtitle-after.json',
    '029-disable-horizontal-axis-title-after.json','033-disable-vertical-axis-title-after.json'];
  for(const[index,name]of offNames.entries())for(const[roleIndex,role]of roles.entries()){
    const snapshot=read(name).state,scene=roleScene(snapshot,role),off=index===roleIndex;
    assert.equal(value(roleSource(snapshot,role).enabled),!off);assert.equal(value(roleSource(snapshot,role).text),role.text);
    if(off)assert(value(scene.fields.visible)===false||value(scene.fields.text)==='');
    else assert.equal(value(scene.fields.text),role.text);
  }
});
check('final captions retain text and effective Weight pairs',()=>{
  const beforeRetained=read('083-padding-restore-left-after.json').state;
  for(const role of roles){assert.equal(value(roleSource(final,role).text),role.text);
    for(const key of ['fontWeight','fontStyle'])assert.deepEqual(roleSource(final,role)[key],roleSource(beforeRetained,role)[key]);}
});
check('per-action ordered events and case/journey ceilings respected',()=>{
  assert(ledger.every(item=>item.eventCount<=limits.actionEvents));
  assert(final.eventCounters.total<=limits.events);
  assert(snapshots.every(item=>item.state.eventCounters.case<=limits.caseEvents));
});
check('every synthetic PNG has fixed viewport dimensions',()=>{
  for(const name of fs.readdirSync(runRoot).filter(name=>name.endsWith('.png'))){const bytes=fs.readFileSync(path.join(runRoot,name));
    assert.equal(bytes.readUInt32BE(16),1440);assert.equal(bytes.readUInt32BE(20),1000);}
});
check('snapshot and retained JSON bytes remain bounded',()=>{
  for(const name of names)assert(fs.statSync(path.join(runRoot,name)).size<=limits.snapshotBytes);
  const total=fs.readdirSync(runRoot).filter(name=>name.endsWith('.json'))
    .reduce((sum,name)=>sum+fs.statSync(path.join(runRoot,name)).size,0);assert(total<=limits.jsonBytes);
});
const weight=deltas.filter(item=>item.name.startsWith('weight-')).map(item=>({name:item.name,
  before:item.before,after:item.after,delta:item.rawModelDelta,events:item.events,
  effective:item.afterGeometry.captions.map(role=>({label:role.label,fontWeight:role.effective.fontWeight,fontStyle:role.effective.fontStyle}))}));
const diagnostics=read('diagnostics.json');
write('measurements',{scope:'Original dark groupedColumn only; finite parent-space bounds plus reviewed screenshot pixels',
  snapshotCount:snapshots.length,ledgerCount:ledger.length,baseline:geometry(baseline),allOn:geometry(allOn),final:geometry(final),
  captionCases:deltas.filter(item=>/^(disable|restore)-/.test(item.name)),
  paddingCases:deltas.filter(item=>item.name.startsWith('padding-')),weight,
  rawInitialWeightAndStyle:Object.fromEntries(roles.map(role=>[role.label,{effective:roleSource(baseline,role),
    sourceModel:role.key?baseline.model.chartOptions.bar[role.key]:baseline.model.chartOptions.bar.axes[role.type].positions[role.position].title}]))});
write('event-model-deltas',{sourcePredictions:'plan.md; observed paths below can disprove the prediction',actions:deltas.map(item=>({
  name:item.name,before:item.before,after:item.after,input:item.input,rawModelDelta:item.rawModelDelta,events:item.events}))});
write('verification',{status:'passed offline assertions; independent runtime/publication review pending',checks,
  diagnostics:{count:diagnostics.diagnostics.length,overflow:diagnostics.overflow,
    kinds:diagnostics.diagnostics.reduce((result,item)=>(result[item.kind]=(result[item.kind]||0)+1,result),{})},
  snapshots:snapshots.length,actions:ledger.length,events:final.eventCounters.total,
  scope:'Does not certify light, other families, persistence, consuming implementation or frozen type repair.'});
console.log(JSON.stringify({checks:checks.length,snapshots:snapshots.length,actions:ledger.length,events:final.eventCounters.total,
  diagnostics:diagnostics.diagnostics.length}));
