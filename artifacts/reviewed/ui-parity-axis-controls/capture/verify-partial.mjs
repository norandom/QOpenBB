import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const root=path.resolve(process.argv[2]),load=n=>JSON.parse(fs.readFileSync(root+'/'+n)),hash=n=>createHash('sha256').update(fs.readFileSync(root+'/'+n)).digest('hex');
const checks=[];const assert=(v,label)=>{if(!v)throw Error(label);checks.push(label);};
const manifest=load('source-manifest.json');for(const f of manifest.files)assert(hash(f.path)===f.sha256,'executed source '+f.path);
assert(manifest.plan.sha256==='fba60d3b02bbaba092be3ec7a93cfe6a82e4608cd5b5836702da0e6223aa7f6a','executed reviewed plan');
assert(load('run-status.json').exitCode===1&&load('failure.json').case==='A05','failure remains recorded at A05');
const completed=['A01','A02','A03','A04'];assert(load('cases.json').map(c=>c.id).join()===completed.join(),'only four completed cases');
const cleanup=load('cleanup-report.json'),browser=load('browser-cleanup.json');
assert(cleanup.containerAbsent&&cleanup.stateAbsent&&cleanup.credentialAbsent&&!cleanup.remainingOwnedState.length,'owned runtime cleanup');
assert(browser.browserClosed&&browser.contextClosed&&browser.listenerRemovedOrDisposed,'owned browser cleanup');
assert(load('event-index.json').count===0&&load('counters.json').events===0,'raw finalization defect preserved');
const recovery=load('recovered-event-index.json');assert(hash('event-index.json')===recovery.originalIndex.sha256&&!recovery.isCompleteRun,'recovery provenance and incomplete boundary');
for(const c of recovery.chunks)assert(hash(c.path)===c.sha256&&fs.statSync(root+'/'+c.path).size===c.bytes,'immutable event chunk '+c.path);
const events=recovery.files.flatMap(load);assert(events.length===31&&events.every((e,i)=>e.sequence===i+1),'31 retained ordered events');
const observations=fs.readdirSync(root).filter(n=>/^observations-.*\.json$/.test(n)).flatMap(load),lookup=new Map(observations.map(o=>[o.id,o]));
const publicLedger=fs.existsSync(root+'/action-ledger-public.json')?load('action-ledger-public.json').actions:load('action-ledger.json');
const actions=publicLedger.filter(a=>completed.includes(a.case));
for(const a of actions){const before=lookup.get(a.beforeEvidence),after=lookup.get(a.afterEvidence);
  assert(a.completed&&before&&after,'completed action references '+a.id);
  const own=events.filter(e=>e.action===a.id);assert(own.every(e=>e.sequence>before.eventSequence&&e.sequence<=after.eventSequence),'ordered action events '+a.id);
  for(const o of [before,after]){const state=load(o.checkpoint),{dom,settled,...chart}=state;delete chart.case;
    assert(createHash('sha256').update(JSON.stringify(chart)).digest('hex')===o.chartSha256,'fresh state reference '+o.id);
    assert(!o.settled.animationActive&&o.settled.identicalFiniteSamples&&o.settled.sampleTimes.at(-1)-o.settled.sampleTimes.at(-2)>=100,'settlement '+o.id);
    assert(state.live.nodes.every(n=>n.parents.length&&n.parentLink.in)&&state.live.ancestors.every(p=>p.fields.visible.in),'nonvacuous inherited scene visibility '+o.id);
  }
}
const completedIds=new Set(actions.map(a=>a.id)),completedEvents=events.filter(e=>completedIds.has(e.action));
assert(completedEvents.length===20&&completedEvents.every((e,i)=>e.sequence===i+1),'complete 20-event prefix for A01-A04');
const findings=load('transaction-findings.json').transactions,transactions=findings.filter(t=>completed.includes(t.case));
assert(transactions.length===20&&transactions.every(t=>t.financialAmountsUnchanged&&t.reportingPeriodValuesUnchanged),'20 completed control transactions keep financial values');
const find=label=>transactions.find(t=>t.label===label),axis=(t,d)=>t.afterAxes.find(a=>a.direction===d);
for(const [label,direction,position] of [['Horizontal-position-Top','x','top'],['Horizontal-position-Bottom','x','bottom'],['Vertical-position-Right','y','right'],['Vertical-position-Left','y','left']]){
  const t=find(label);assert(t.modelChanges.length===0&&t.explicitAxisChanges.length>0&&axis(t,direction).position===position,'explicit position separate from model '+label);
}
for(const [role,direction,width,length,count] of [['Horizontal','x',3,11,4],['Vertical','y',2,7,5]]){
  const changed=axis(find(role+'-tick-length'),direction),off=axis(find(role+'-ticks-off'),direction),on=axis(find(role+'-ticks-retained'),direction);
  assert(changed.style.tick.value.width.value===width&&changed.style.tick.value.size.value===length,'tick settings '+role);
  const source=load(find(role+'-tick-length').after).model.chartOptions.bar.axes[direction==='x'?'category':'number'].value.positions;
  assert((direction==='x'?['top','bottom']:['left','right']).every(p=>source[p].value.tick.value.width.value===width&&source[p].value.tick.value.size.value===length),'both positional theme branches '+role);
  assert(changed.ticks.length===count&&changed.ticks.every(t=>t.visible===true&&t.width===width&&Math.abs(t.x2-t.x1)+Math.abs(t.y2-t.y1)===length),'finite tick geometry '+role);
  assert(off.ticks.length===count&&off.ticks.every(t=>t.visible===false)&&on.ticks.every(t=>t.visible===true),'retained hidden/reopened ticks '+role);
  assert(transactions.filter(t=>t.case===(role==='Horizontal'?'A03':'A04')).every(t=>t.modelChanges.every(c=>!c.path.includes('gridLine'))),'grid discriminators unchanged '+role);
}
const report={status:'passed',scope:'A01-A04 only; A05 partial and A06-A09 unrun',checks:checks.length,completedEvents:20,retainedEvents:31,
  recoveredFinalizationDefect:true,internalEditorScrollOffsetsMeasured:false,allNineCasesVerified:false};
fs.writeFileSync(root+'/partial-verification.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));
