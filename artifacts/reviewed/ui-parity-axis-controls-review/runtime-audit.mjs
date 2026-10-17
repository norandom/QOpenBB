import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const repo=process.cwd();
const evidenceRoot=process.argv[2]??'artifacts';
const base=evidenceRoot+'/ui-parity-axis-controls/capture/attempt-20261017T1422580-7c412f5c';
const read=n=>JSON.parse(fs.readFileSync(path.join(repo,base,n),'utf8').replace(/^\uFEFF/,''));
const hash=b=>createHash('sha256').update(b).digest('hex');
const checks=[];const check=(name,passed)=>checks.push({name,passed:!!passed});
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const names=fs.readdirSync(path.join(repo,base));
const observations=names.filter(n=>/^observations-A-/.test(n)).flatMap(read);
const byObservation=new Map(observations.map(o=>[o.id,o]));
const stateNames=names.filter(n=>/^\d{3}-A-.*\.json$/.test(n));
const states=new Map(stateNames.map(n=>[n,read(n)]));
const eventNames=names.filter(n=>/^events-p\d+\.json$/.test(n)).sort();
const events=eventNames.flatMap(read);
const ledger=read('action-ledger-public.json').actions;
const transactions=read('transactions.json');
check('only completed A01-A04',eq(read('cases.json').map(c=>c.id),['A01','A02','A03','A04']));
check('A05 failure preserved',read('failure.json').case==='A05');
check('raw faulty zero index preserved',read('event-index.json').count===0&&read('counters.json').events===0);
check('surviving 31 raw events',events.length===31);
check('event sequence contiguous',events.every((e,i)=>e.sequence===i+1));
check('event action references',events.every(e=>ledger.some(a=>a.id===e.action)));
check('20 events in completed cases',events.filter(e=>/^A\.A0[1-4]\./.test(e.action)).length===20);
check('position events omit theme branches',events.slice(0,4).every(e=>e.chartOptions.common.presence.kind==='absent'&&e.chartOptions.bar.presence.kind==='absent'));
check('33 full states',states.size===33);
check('unique observation IDs',byObservation.size===observations.length);
for(const name of read('screenshots.json')){
  const bytes=fs.readFileSync(path.join(repo,base,name));
  check(name+' bounded PNG identity',bytes.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10]))&&bytes.readUInt32BE(16)===1440&&bytes.readUInt32BE(20)===1000&&bytes.length<=4194304);
}
for(const o of observations){
  const s=states.get(o.checkpoint);check(o.id+' checkpoint exists',!!s);if(!s)continue;
  const {dom,settled,...chart}=s;delete chart.case;
  check(o.id+' chart identity',hash(JSON.stringify(chart))===o.chartSha256);
  check(o.id+' settled pair',o.settled.identicalFiniteSamples===true&&o.settled.sampleTimes.length>=2&&o.settled.sampleTimes.at(-1)-o.settled.sampleTimes.at(-2)>=100);
  check(o.id+' event sequence',o.eventSequence===s.eventSequence&&o.eventSequence<=events.length);
}
for(const t of transactions.filter(t=>['A02','A03','A04'].includes(t.case))){
  const before=byObservation.get(t.beforeObservation),after=byObservation.get(t.afterObservation);
  check(t.label+' linked states',before?.checkpoint===t.before&&after?.checkpoint===t.after);
  const actions=ledger.filter(a=>Number(a.id.split('.u')[1])>=t.uiActions.first&&Number(a.id.split('.u')[1])<=t.uiActions.last);
  check(t.label+' complete actions',actions.length===t.uiActions.last-t.uiActions.first+1&&actions.every(a=>a.completed&&byObservation.has(a.beforeEvidence)&&byObservation.has(a.afterEvidence)));
}
const expected=[[0,'2024-Q1',100,20],[1,'2024-Q2',120,25],[2,'2024-Q3',140,30],[3,'2024-Q4',160,40]];
for(const [name,s] of states){
  for(const channel of ['explicit','effective'])check(name+' '+channel+' data',eq(s[channel].data.value.map(r=>[r.period.value.fields.id.value,r.period.value.fields.value.value,r.amounts.revenue.value,r.amounts.operatingIncome.value]),expected));
  check(name+' axes identity',s.live.axes.length===2&&eq(s.live.axes.map(a=>a.identity.direction.value),['x','y']));
  const parents=new Map(s.live.ancestors.map(p=>[p.identity,p]));
  check(name+' nonempty ancestry',s.live.nodes.length>0&&s.live.nodes.every(n=>n.parents.length>0&&n.parents.every(p=>parents.has(p))));
  check(name+' actual inherited visibility',s.live.ancestors.every(p=>typeof p.fields.visible.value==='boolean'&&Number.isFinite(p.fields.opacity.value)));
}
const after=label=>states.get(transactions.find(t=>t.label===label).after);
for(const [role,direction,position] of [['Horizontal','x','Top'],['Horizontal','x','Bottom'],['Vertical','y','Right'],['Vertical','y','Left']]){
  const s=after(role+'-position-'+position),i=direction==='x'?0:1;
  check(role+' '+position+' explicit/effective/live',s.explicit.axes.value[i].position.value===position.toLowerCase()&&s.effective.axes.value[i].position.value===position.toLowerCase()&&s.live.axes[i].identity.position.value===position.toLowerCase());
}
for(const [role,index,width,size] of [['Horizontal',0,3,11],['Vertical',1,2,7]]){
  const selected=after(role+'-tick-length'),off=after(role+'-ticks-off'),retained=after(role+'-ticks-retained'),baseline=after(role+'-ticks-baseline');
  for(const [label,s,enabled] of [['selected',selected,true],['off',off,false],['retained',retained,true]]){
    const axis=s.live.axes[index],tick=axis.style.tick.value,nodes=axis.ticks.map(id=>s.live.nodes.find(n=>n.identity===id));
    check(role+' '+label+' tuple',tick.enabled.value===enabled&&tick.width.value===width&&tick.size.value===size);
    check(role+' '+label+' nonempty scene ticks',nodes.length>0&&nodes.every(n=>n.fields.strokeWidth.value===width));
    const effectiveVisible=n=>n.fields.visible.value&&n.parents.every(id=>s.live.ancestors.find(p=>p.identity===id).fields.visible.value);
    check(role+' '+label+' inherited visibility',nodes.every(n=>effectiveVisible(n)===enabled));
  }
  const tick=baseline.live.axes[index].style.tick.value;
  check(role+' restored baseline',tick.enabled.value===false&&tick.width.value===1&&tick.size.value===6);
}
for(const attempt of ['attempt-20261017T1409125-18fed9af','attempt-20261017T1413358-2f46bb8c','attempt-20261017T1416524-c93ff5a0','attempt-20261017T1422580-7c412f5c']){
  const r=n=>JSON.parse(fs.readFileSync(path.join(repo,evidenceRoot,'ui-parity-axis-controls/capture',attempt,n),'utf8').replace(/^\uFEFF/,''));
  const cleanup=r('cleanup-report.json'),browser=r('browser-cleanup.json');
  check(attempt+' cleanup',cleanup.containerAbsent&&cleanup.stateAbsent&&cleanup.credentialAbsent&&cleanup.remainingOwnedState.length===0&&browser.browserClosed&&browser.contextClosed&&browser.listenerRemovedOrDisposed);
  for(const f of r('source-manifest.json').files)check(attempt+' source '+f.path,hash(fs.readFileSync(path.join(repo,evidenceRoot,'ui-parity-axis-controls/capture',attempt,f.path)))===f.sha256);
}
const result={scope:'Independent immutable axis partial-run evidence audit; A01-A04 only',attempt:base,checkCount:checks.length,failed:checks.filter(c=>!c.passed),counts:{states:states.size,observations:observations.length,events:events.length,completedCases:4},checks};
fs.writeFileSync(path.join(repo,'artifacts/ui-parity-axis-controls-review/runtime-verification.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({checkCount:checks.length,failed:result.failed,counts:result.counts}));
if(result.failed.length)process.exitCode=1;
