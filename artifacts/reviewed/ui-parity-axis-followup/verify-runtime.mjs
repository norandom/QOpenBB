import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {assertFinancialData} from './harness/guards.mjs';
const root=path.resolve(process.argv[2]),output=path.resolve(process.argv[3]),auditOnly=process.argv.includes('--read-only');
if(!fs.existsSync(output)){if(auditOnly)throw Error('Existing analysis input directory required');fs.mkdirSync(output);}
const load=n=>JSON.parse(fs.readFileSync(path.join(root,n))),hash=n=>createHash('sha256').update(fs.readFileSync(path.join(root,n))).digest('hex');
const checks=[];function assert(v,label){if(!v)throw Error(label);checks.push(label);}
const manifest=load('source-manifest.json'),fixtures=JSON.parse(fs.readFileSync(path.join(root,'harness/fixtures.json')));
assert(hash('source-manifest.json')==='ac534d3491e22ddf1873da0fa957a043cb7ee468021c2e0770fa2a887e52e9e4','frozen collector manifest');
assert(hash('plan.md')==='1c5ceae2d8dc8f5f8f955b1d961489df89455efed3384beadff980e0e69f41d5','reviewed plan');
assert(hash('source-hashes.json')==='68e0c0e68fd30e3fb1547b1d313a4ef959d5eef0b28e8a4a29116d4cc56f2fa6','reviewed source manifest');
for(const f of manifest.files)assert(hash(f.path)===f.sha256,'executed source '+f.path);
const cleanup=load('cleanup-report.json'),browser=load('browser-cleanup.json');
assert(cleanup.containerAbsent&&cleanup.stateAbsent&&cleanup.credentialAbsent&&!cleanup.remainingOwnedState.length,'owned runtime cleanup');
assert(browser.browserClosed&&browser.contextClosed&&browser.listenerRemovedOrDisposed&&!browser.closeError,'owned browser cleanup without close error');
const cases=load('cases.json'),expected=['A05','A06','A07','A08','A09'];
assert(cases.every((c,i)=>c.id===expected[i]),'only original remaining cases in order');
const index=load('event-index.json'),events=index.files.flatMap(load),counters=load('counters.json');
assert(index.count===events.length&&events.every((e,i)=>e.sequence===i+1)&&counters.events===events.length,'event index/chunks/counter agree without recovery');
assert(events.length<=256,'run event cap');
const ledger=load('action-ledger.json'),observations=fs.readdirSync(root).filter(n=>/^observations-.*\.json$/.test(n)).flatMap(load),lookup=new Map(observations.map(o=>[o.id,o]));
const offsets=Object.fromEntries(['A','B','C'].map(f=>[f,events.filter(e=>e.fixture<f).length]));
for(const action of ledger.filter(a=>a.beforeEvidence&&a.completed)){
  const before=lookup.get(action.beforeEvidence),after=lookup.get(action.afterEvidence);assert(before&&after,'action evidence '+action.id);
  const own=events.filter(e=>e.action===action.id),offset=offsets[action.id[0]];
  assert(own.length<=8&&own.every(e=>e.sequence>before.eventSequence+offset&&e.sequence<=after.eventSequence+offset),'ordered per-action events '+action.id);
  if(own.length)assert(before.checkpoint!==after.checkpoint,'event-emitting action has distinct settled full state '+action.id);
  for(const obs of [before,after]){
    const state=load(obs.checkpoint),{dom,settled,...chart}=state;delete chart.case;
    assert(createHash('sha256').update(JSON.stringify(chart)).digest('hex')===obs.chartSha256,'fresh chart reference '+obs.id);
    assert(!obs.settled.animationActive&&obs.settled.identicalFiniteSamples&&obs.settled.sampleTimes.at(-1)-obs.settled.sampleTimes.at(-2)>=100,'settlement '+obs.id);
    assertFinancialData(state.explicit.data,fixtures[state.fixture],fixtures);
    assert(state.live.nodes.every(n=>n.parents.length&&n.parentLink.in)&&state.live.ancestors.every(a=>a.fields.visible.in),'actual scene ancestry '+obs.id);
  }
}
assert(counters.actions===ledger.length&&counters.actions<=240&&counters.changes===ledger.filter(a=>a.change).length&&counters.changes<=80,'action/edit counters and caps');
const checkpointFiles=fs.readdirSync(root).filter(n=>/^\d{3}-.*\.json$/.test(n)),pngFiles=fs.readdirSync(root).filter(n=>n.endsWith('.png'));
assert(counters.checkpoints===checkpointFiles.length&&checkpointFiles.length<=96&&counters.screenshots===pngFiles.length&&pngFiles.length<=64,'checkpoint/PNG accounting');
for(const c of cases)assert(events.filter(e=>e.action.split('.')[1]===c.id).length<=64,'case event cap '+c.id);
const findings=JSON.parse(fs.readFileSync(path.join(output,'transaction-findings.json'))),transactions=findings.transactions;
for(const t of transactions){
  const state=load(t.after),nodes=new Map(state.live.nodes.map(n=>[n.identity,n]));
  for(const a of t.afterAxes){
    const raw=state.live.axes.find(x=>x.identity.direction.value===a.direction);
    assert(raw&&raw.identity.type.value===a.type&&JSON.stringify(raw.style)===JSON.stringify(a.style),'derived axis equals immutable finite source '+t.label+' '+a.direction);
    assert(raw.labels.length===a.labels.length&&raw.labels.every((id,i)=>{const n=nodes.get(id);return n.fields.text.value===a.labels[i].text&&n.fields.rotation.value===a.labels[i].rotation&&JSON.stringify(n.bbox)===JSON.stringify(a.labels[i].bbox); }),'derived labels/geometry equal immutable finite source '+t.label+' '+a.direction);
  }
}
assert(transactions.every(t=>t.financialAmountsUnchanged&&t.reportingPeriodValuesUnchanged),'every completed transaction preserves financial values and periods');
for(const role of ['Horizontal','Vertical'])if(fs.existsSync(path.join(root,'restoration-'+role+'.json'))){
  const r=load('restoration-'+role+'.json');assert(r.uiEquivalent&&!r.rawByteIdentityClaimed,'restoration receipt '+role);
}
const complete=cases.length===5&&!fs.existsSync(path.join(root,'failure.json'));
if(complete){
  assert(load('run-status.json').exitCode===0&&load('journey-status.json').exitCode===0&&load('cleanup-status.json').exitCode===0&&load('watchdog-status.json').exitCode===0,'successful lifecycle status');
  const axis=(label,d)=>transactions.find(t=>t.label===label)?.afterAxes.find(a=>a.direction===d),value=f=>f?.value;
  for(const [label,angle] of [['Horizontal-rotation-315',-45],['Horizontal-rotation-45',45],['Vertical-rotation-330',-30]])assert(value(axis(label,label.startsWith('Horizontal')?'x':'y')?.style.label.value.rotation)===angle,'manual wrap '+label);
  assert(axis('B-number','x').type==='number'&&axis('B-time','x').type==='time'&&axis('B-category','x').type==='category','category-role Number/Time/Category transitions');
  for(const [label,format] of [['B-ISO','%Y-%m-%d'],['B-European','%d/%m/%Y']]){
    const t=transactions.find(t=>t.label===label),state=load(t.after),x=state.explicit.axes.value.find(a=>a.position.value==='bottom');assert(x.label.value.format.value===format,'explicit time format '+label);
  }
  for(const [role,direction,type,positions,family,size,spacing] of [['Horizontal','x','category',['top','bottom'],'Arial, sans-serif',14,17],['Vertical','y','number',['left','right'],'Courier New, monospace',16,23]]){
    for(const [suffix,key,wanted] of [['font','fontFamily',family],['size','fontSize',size],['spacing','spacing',spacing]]){
      const t=transactions.find(t=>t.label===role+'-'+suffix),state=load(t.after),live=axis(role+'-'+suffix,direction);
      assert(live.style.label.value[key].value===wanted,'live label binding '+role+' '+key);
      assert(positions.every(p=>state.model.chartOptions.bar.axes[type].value.positions[p].value.label.value[key].value===wanted),'both theme positions '+role+' '+key);
      const before=load(t.before),other=state.live.axes.find(a=>a.identity.direction.value!==direction),oldOther=before.live.axes.find(a=>a.identity.direction.value!==direction);
      assert(JSON.stringify(other.style)===JSON.stringify(oldOther.style),'other label role unchanged '+role+' '+key);
    }
  }
  for(const [label,direction,angle] of [['Horizontal-rotation-315','x',-45],['Horizontal-rotation-45','x',45],['Vertical-rotation-330','y',-30]])assert(axis(label,direction).labels.every(n=>Math.abs(Math.sin(n.rotation)-Math.sin(angle*Math.PI/180))<1e-12&&Math.abs(Math.cos(n.rotation)-Math.cos(angle*Math.PI/180))<1e-12),'scene rotation modulo full turn '+label);
  for(const [role,direction,retained] of [['Horizontal','x',45],['Vertical','y',-30]])assert(axis(role+'-automatic',direction).style.label.value.autoRotate.value===true&&axis(role+'-manual-retained',direction).style.label.value.rotation.value===retained,'Auto Rotate remembers manual rotation '+role);
  const control=(o,role,label)=>o.dom.groups.find(g=>g.name===role+' Axis')?.controls.filter(c=>c.label===label&&c.role==='combobox')??[];
  for(const role of ['Horizontal','Vertical']){
    const o=observations.find(o=>o.fixture==='C'&&o.case==='A09'&&o.label===role+'-inventory');assert(o,'fixture C role-specific expanded observation '+role);
    assert(control(o,role,'Axis Type').length===1&&control(o,role,'Axis Type')[0].visible===false,'nonnumeric Axis Type present but hidden '+role);
    assert(['Position','Font','Size'].every(label=>control(o,role,label).length===1&&control(o,role,label)[0].visible),'nonnumeric Position/Labels still visible '+role);
  }
  const timeUI=label=>lookup.get(transactions.find(t=>t.label===label).afterObservation);
  assert(control(timeUI('B-time'),'Horizontal','Time Format')[0]?.visible===true&&control(timeUI('B-number'),'Horizontal','Time Format')[0]?.visible===false&&control(timeUI('B-category'),'Horizontal','Time Format')[0]?.visible===false,'Time Format visibility follows category-role type');
  const discriminators=['B-number','B-time','B-category'].map(label=>axis(label,'x'));
  assert(discriminators.every(a=>a.style.label.value.spacing.value===11&&a.style.tick.value.enabled.value===false&&a.style.tick.value.width.value===1),'recorded discriminator loss through type transitions');
  const iso=axis('B-ISO','x').labels.map(n=>n.text),european=axis('B-European','x').labels.map(n=>n.text);
  assert(JSON.stringify(iso)===JSON.stringify(european)&&iso.length===2&&iso[0].includes('Jan 01 2023')&&iso[1].includes('Jan 01 2027'),'time-format selection leaves observed scene text unchanged');
  assert(load('restoration-Horizontal.json').uiEquivalent&&load('restoration-Vertical.json').uiEquivalent,'both label-role restoration sequences completed');
}
const excluded=n=>n.startsWith('state-')||n.endsWith('-private.json')||n.endsWith('.log'),entries=[];
function walk(dir){for(const item of fs.readdirSync(dir,{withFileTypes:true})){
  if(excluded(item.name))continue;assert(!item.isSymbolicLink(),'no retained symlink '+item.name);
  const f=path.join(dir,item.name);if(item.isDirectory())walk(f);else{const bytes=fs.statSync(f).size;if(f.endsWith('.json'))assert(bytes<=2097152,'final JSON size '+item.name);if(f.endsWith('.png'))assert(bytes<=4194304,'final PNG size '+item.name);entries.push({path:path.relative(root,f),bytes,sha256:createHash('sha256').update(fs.readFileSync(f)).digest('hex')});}
}}walk(root);
const bytes=entries.reduce((a,e)=>a+e.bytes,0);assert(entries.length<=320&&bytes<=167772160,'final actual-disk file/total caps including outer receipts');
const report={status:complete?'passed':'partial',scope:complete?'Original remaining A05-A09 only':'Completed prefix only; failure remains',checks:checks.length,cases,events:events.length,counters,retained:{files:entries.length,bytes},allFiveCasesVerified:complete,candidateExecuted:false,persistenceVerified:false,internalEditorScrollOffsetsMeasured:false};
if(!auditOnly){fs.writeFileSync(path.join(output,'runtime-verification.json'),JSON.stringify(report,null,2));fs.writeFileSync(path.join(output,'actual-output-inventory.json'),JSON.stringify({entries,bytes,scope:'Actual final retained disk including watchdog receipt; private/log/state excluded'},null,2));}console.log(JSON.stringify({...report,auditOnly}));
