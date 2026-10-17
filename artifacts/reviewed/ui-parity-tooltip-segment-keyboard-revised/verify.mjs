import fs from 'node:fs';
import {faults} from './r01-faults.mjs';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {coordinate,observe} from './harness/collector.mjs';
import {coordinate as originalCoordinate} from './executed-baseline/collector.mjs';
import * as compact from './harness/keyboard-retention.mjs';
import {cases,limits,fixture,fixtureHash} from './harness/contract.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,path.basename(path.dirname(here))==='reviewed'?'../../..':'../..');
const prior=path.join(root,'artifacts/ui-parity-tooltip-followup/capture/attempt-20261017-tooltip-followup-a1');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const clone=value=>structuredClone(value),same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const sha=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const checks=[];
function check(name,ok){checks.push({name,passed:!!ok});if(!ok)throw Error(name);}
function rejects(name,fn,pattern){let error;try{fn();}catch(e){error=e;}check(name,error&&pattern.test(error.message));}
async function rejectsAsync(name,fn,pattern){let error;try{await fn();}catch(e){error=e;}check(name,error&&pattern.test(error.message));}

const baseline=fs.readdirSync(here+'/executed-baseline').sort();
check('exact twelve executed baseline files',baseline.length===12);
for(const name of baseline)check('immutable executed baseline '+name,sha(here+'/executed-baseline/'+name)===sha(prior+'/harness/'+name));
for(const name of fs.readdirSync(here+'/harness'))if(name.endsWith('.mjs')){
  execFileSync(process.execPath,['--check',here+'/harness/'+name],{stdio:'pipe',windowsHide:true});
  check('syntax '+name,true);
}
check('contract byte-identical',sha(here+'/executed-baseline/contract.mjs')===sha(here+'/harness/contract.mjs'));
check('fixture byte-identical',sha(here+'/executed-baseline/fixture.json')===sha(here+'/harness/fixture.json'));
check('fixture frozen semantic identity',fixture().rows.length===5&&fixtureHash==='bda68b15aee2192684d67086c4a599f852943a3079882d4aeb744e6efab262ad');
check('bounds unchanged',cases.length===8&&limits.totalActions===396&&limits.probes===96&&limits.screenshots===48&&limits.outerMs===900000&&limits.caseBytes===131072);
let count=0;
for(let i=1;i<=8;i++)for(const probe of read(prior+'/T0'+i+'.json').probes){
  const geometry=probe.settlement.pair[1],family=cases[i-1].family;
  const next=coordinate(geometry,probe.ordinal,probe.target.yKey,family);
  const old=originalCoordinate(geometry,probe.ordinal,probe.target.yKey,family);count++;
  check(probe.id+' target identity unchanged',next.wrapperId===old.wrapperId&&next.yKey===old.yKey&&next.seriesId===old.seriesId);
  if(family!=='stackedColumn')check(probe.id+' grouped/line unchanged',same(next,old));
  if(probe.id==='T05.p17')check('T05 zero delta, unexplained',same(next.point,old.point));
  if(probe.id==='T08.p52'){
    check('T08 midpoint shift',Math.abs(next.point.y-old.point.y-28.275)<1e-9&&next.point.x===old.point.x);
    for(const invalid of [undefined,NaN,Infinity,'132.49375']){
      const g=clone(geometry),n=g.series.find(s=>s.yKey===probe.target.yKey).nodes[0];
      if(invalid===undefined)delete n.midPoint;else n.midPoint.y.value=invalid;
      rejects('invalid midpoint '+String(invalid),()=>coordinate(g,probe.ordinal,probe.target.yKey,family),/finite stacked midpoint/);
    }
    const g=clone(geometry);g.series.find(s=>s.yKey===probe.target.yKey).nodes[0].midPoint.y.value=1e6;
    rejects('midpoint outside existing bounds',()=>coordinate(g,probe.ordinal,probe.target.yKey,family),/outside chart/);
    const broken=clone(geometry);broken.series.find(s=>s.yKey===probe.target.yKey).links.contentToManaged=false;
    rejects('named chain guard retained',()=>coordinate(broken,probe.ordinal,probe.target.yKey,family),/exact parent chain/);
    const absent=clone(geometry);absent.series.find(s=>s.yKey===probe.target.yKey).nodes=[];
    rejects('missing ordinal stops',()=>coordinate(absent,probe.ordinal,probe.target.yKey,family),/no-hittable-node/);
  }
}
check('all 24 retained pointer probes',count===24);
const historical=read(prior+'/T06.json'),projected=clone(historical);let tabs=0;
for(const mode of projected.keyboard){delete mode.baseline;for(const tab of mode.tabs){
  compact.modeSample(mode,tab.before);
  for(const raw of tab.state.pair)compact.modeSample(mode,raw);
  tab.before=compact.sample(tab.before);tab.state=compact.settlement(tab.state);compact.invocation(tab);tabs++;
}}
check('27 retained Tab states fit finite caps',tabs===27);
const raw=historical.keyboard[0].tabs[0].state.pair[0],mode={};
const p=compact.modeSample(mode,raw);check('baseline retained once',same(mode.baseline,{area:raw.area,swapchain:raw.swapchain}));
check('unchanged baseline accepted',same(p,compact.modeSample(mode,raw)));
const changed=clone(raw);changed.area.name+=' changed';
rejects('baseline change stops',()=>compact.modeSample(mode,changed),/baseline changed/);
const hidden=clone(raw);hidden.tooltip={visible:false,heading:['stale'],rows:[{label:'hidden',value:'secret'}],sanitizedInnerHTML:'<p>stale</p>'};
check('hidden stale tooltip omitted',same(compact.sample(hidden).tooltip,{visible:false}));
const visible=clone(raw);visible.tooltip={visible:true,heading:['Heading'],rows:[{label:'Revenue',value:'27.625'}],compact:['Revenue 27.625'],pagination:true,sanitizedInnerHTML:'html',bounds:{x:1}};
check('full visible content retained',same(compact.sample(visible).tooltip,{visible:true,heading:['Heading'],rows:[{label:'Revenue',value:'27.625'}],compact:['Revenue 27.625'],pagination:true}));
const unequal=clone(raw);unequal.tooltip={...hidden.tooltip,sanitizedInnerHTML:'different hidden HTML'};
rejects('projection equality cannot replace full equality',()=>compact.settlement({status:'stable',pair:[hidden,unequal],sampleCount:2,elapsedMs:1}),/full DOM pair unequal/);
const unseen=clone(raw);unseen.active.name='x'.repeat(513);
rejects('unseen focus text stops',()=>compact.sample(unseen),/text cap/);
const large=clone(visible);large.liveStatus='x'.repeat(2048);large.tooltip.compact=Array(4).fill('x'.repeat(512));
rejects('legal individual strings exceeding sample bytes stop',()=>compact.sample(large),/sample bytes/);
const nonfinite=clone(raw);nonfinite.active.rect.x=NaN;
rejects('nonfinite DOM coordinate stops',()=>compact.sample(nonfinite),/finite number/);
rejects('oversized prospective tail stops',()=>compact.finalTail(['x'.repeat(16000)],1),/final tail bytes/);
rejects('oversized control receipt stops',()=>compact.controlReceipt({before:'x'.repeat(1024)}),/control receipt bytes/);
const extraRow=clone(visible);extraRow.tooltip.rows=Array(4).fill({label:'Revenue',value:'27.625'});
rejects('unseen fourth visible row stops',()=>compact.sample(extraRow),/array cap/);
check('reservation covers bounded next invocation entry baseline receipts scaffolding',compact.retention.invocationBytes+compact.retention.entryBytes+compact.retention.baselineBytes+2*1024+2048<compact.retention.inputReserve);
const tiny={id:'T06',ledger:[],keyboard:[],actions:0};compact.reserveInput(tiny);
const full={...tiny,padding:'x'.repeat(compact.retention.caseGuard)};
rejects('prospective budget stops before write',()=>compact.reserveInput(full),/not-run-budget/);
const journey=fs.readFileSync(here+'/harness/journey.mjs','utf8');
const inputSource=journey.slice(journey.indexOf('async function input('),journey.indexOf('const ui='));
const context={current:full,actions:0,setupActions:0,phase:'T06',limits,guard:()=>{},reserveInput:compact.reserveInput};
vm.createContext(context);vm.runInContext(inputSource,context);
await rejectsAsync('actual input function rejects before action counter',()=>vm.runInContext("input('Tab traversal',null,'key','Tab')",context),/not-run-budget/);
check('input counters and ledger preserved',context.actions===0&&context.current.actions===0&&context.current.ledger.length===0);
const keyboardSource=journey.slice(journey.indexOf('async function keyboard('),journey.indexOf('function dashboard('));
const keyboardContext={current:{...full,modes:['Single'],tabCap:24,keyboard:[]},probes:0,limits,guard:()=>{},reserveInput:compact.reserveInput,modeSample:compact.modeSample,
  ui:()=>({mode:async()=>{},close:async()=>{}}),input:async()=>{},page:{evaluate:async()=>raw},dom:()=>{}};
vm.createContext(keyboardContext);vm.runInContext(keyboardSource,keyboardContext);
await rejectsAsync('actual keyboard rejects before probe counter',()=>vm.runInContext('keyboard()',keyboardContext),/not-run-budget/);
check('probe counter preserved',keyboardContext.probes===0);
let inspections=0,reads=0;
const settled=await observe({evaluate:async()=>{reads++;return clone(raw);}},()=>{},()=>inspections++);
check('inspect every full DOM sample before equality',reads===2&&inspections===2&&same(settled.pair[0],settled.pair[1]));
const temporary=here+'/offline-io';fs.mkdirSync(temporary,{recursive:true});process.env.CAPTURE_ROOT=temporary;
try{
  const io=await import('./harness/io.mjs');io.json('T06',tiny);const before=sha(temporary+'/T06.json');
  rejects('prewrite over hard ceiling rejected',()=>io.json('T06',{...tiny,padding:'x'.repeat(limits.caseBytes)}),/Case JSON bound/);
  check('failed prewrite preserves prior bytes',sha(temporary+'/T06.json')===before);
  rejects('prewrite oversized ledger rejected',()=>io.json('T06',{...tiny,ledger:[{after:'x'.repeat(compact.retention.entryBytes)}]}),/entry bytes/);
  check('ledger bound preserves prior bytes',sha(temporary+'/T06.json')===before);
}finally{if(fs.existsSync(temporary+'/T06.json'))fs.unlinkSync(temporary+'/T06.json');fs.rmdirSync(temporary);}
check('legacy runtime lifecycle unchanged', ['run.sh','start.mjs','cleanup.mjs'].every(n=>sha(here+'/executed-baseline/'+n)===sha(here+'/harness/'+n)));
const r01=await faults({here,prior,check,sha});
const result={r01,scope:'Offline source-only proposal checks; no runtime acceptance',command:'node artifacts/ui-parity-tooltip-segment-keyboard-revised/verify.mjs',exitCode:0,checks:checks.length,
  retainedPointerProbes:count,retainedTabs:tabs,projectedHistoricalBytes:compact.bytes(projected),runtimeExecuted:false,results:checks};
fs.writeFileSync(here+'/verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({...result,results:undefined}));
