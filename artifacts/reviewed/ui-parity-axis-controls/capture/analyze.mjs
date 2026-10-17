import fs from 'node:fs';
import path from 'node:path';
const root=path.resolve(process.argv[2]),load=name=>JSON.parse(fs.readFileSync(root+'/'+name));
if(!fs.existsSync(root+'/run-status.json')||!load('cleanup-report.json').containerAbsent)throw Error('Analyze only a closed attempt');
const difference=(a,b,prefix='')=>{
  if(JSON.stringify(a)===JSON.stringify(b))return [];
  if(a===null||b===null||typeof a!=='object'||typeof b!=='object')return [{path:prefix,before:a??null,after:b??null}];
  const keys=new Set([...Object.keys(a),...Object.keys(b)]);return [...keys].flatMap(k=>difference(a[k],b[k],prefix?prefix+'.'+k:k));
};
const value=f=>f?.value;
function axes(snapshot){return snapshot.live.axes.map(a=>{
  const nodes=new Map(snapshot.live.nodes.map(n=>[n.identity,n])),parents=new Map(snapshot.live.ancestors.map(p=>[p.identity,p]));
  const visible=n=>{const chain=[n,...n.parents.map(id=>parents.get(id))];
    if(!n.parents.length||chain.some(x=>!x||!x.fields.visible.in||typeof x.fields.visible.value!=='boolean'))return 'unresolved';
    return chain.every(x=>x.fields.visible.value&&x.fields.opacity.value!==0);};
  const labels=a.labels.map(id=>{const n=nodes.get(id);return {text:value(n.fields.text),fontFamily:value(n.fields.fontFamily),fontSize:value(n.fields.fontSize),
    rotation:value(n.fields.rotation),translationX:value(n.fields.translationX),translationY:value(n.fields.translationY),bbox:n.bbox,visible:visible(n)};});
  const ticks=a.ticks.map(id=>{const n=nodes.get(id);return {width:value(n.fields.strokeWidth),x1:value(n.fields.x1),x2:value(n.fields.x2),y1:value(n.fields.y1),y2:value(n.fields.y2),visible:visible(n)};});
  return {direction:value(a.identity.direction),type:value(a.identity.type),position:value(a.identity.position),style:a.style,labels,ticks};
});}
const transactions=fs.existsSync(root+'/transactions.json')?load('transactions.json'):[];
const amountValues=s=>s.explicit.data.value?.map(r=>[value(r.amounts.revenue),value(r.amounts.operatingIncome)]);
const periodValues=s=>s.explicit.data.value?.map(r=>{const p=r.period.value;return p.type==='category-wrapper'?value(p.fields.value):p.type==='Date'?p.milliseconds:p.value;});
const findings=transactions.map(t=>{const before=load(t.before),after=load(t.after);
  return {...t,modelChanges:difference(before.model.chartOptions,after.model.chartOptions),explicitAxisChanges:difference(before.explicit.axes,after.explicit.axes),
    effectiveAxisChanges:difference(before.effective.axes,after.effective.axes),geometryChanges:difference(before.geometry,after.geometry),
    rawDataRepresentationUnchanged:JSON.stringify(before.explicit.data)===JSON.stringify(after.explicit.data),
    financialAmountsUnchanged:amountValues(before)?.length===4&&JSON.stringify(amountValues(before))===JSON.stringify(amountValues(after)),
    reportingPeriodValuesUnchanged:periodValues(before)?.length===4&&JSON.stringify(periodValues(before))===JSON.stringify(periodValues(after)),afterAxes:axes(after)};});
const indexName=fs.existsSync(root+'/recovered-event-index.json')?'recovered-event-index.json':'event-index.json';
const index=load(indexName),events=index.files.flatMap(load);let previous=null;
const eventDeltas=events.map(e=>{const delta={sequence:e.sequence,fixture:e.fixture,action:e.action,identity:e.identity,
  accumulatedModelChangedLeaves:previous&&previous.fixture===e.fixture?difference(previous.chartOptions,e.chartOptions):null};previous=e;return delta;});
const output={status:fs.existsSync(root+'/failure.json')?'incomplete':'observed',cases:fs.existsSync(root+'/cases.json')?load('cases.json'):[],transactions:findings,
  eventSource:indexName,eventSequenceCompleteForRun:!fs.existsSync(root+'/failure.json'),
  limitation:'Coordinates are local/parent scene coordinates, with no guessed canvas transform. Effective visibility includes typed actual parentNode ancestry. Internal editor scroll offsets were not retained.'};
const write=(name,data)=>{const bytes=Buffer.from(JSON.stringify(data));if(bytes.length>2097152)throw Error('Analysis JSON cap');fs.writeFileSync(root+'/'+name,bytes);};
write('transaction-findings.json',output);write('event-deltas.json',eventDeltas);
console.log(JSON.stringify({status:output.status,transactions:findings.length,events:events.length,financialAmountsUnchanged:findings.every(f=>f.financialAmountsUnchanged),
  reportingPeriodValuesUnchanged:findings.every(f=>f.reportingPeriodValuesUnchanged)}));
