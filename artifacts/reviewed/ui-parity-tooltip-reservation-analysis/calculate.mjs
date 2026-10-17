import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import * as r from '../ui-parity-tooltip-segment-keyboard-revised/harness/keyboard-retention.mjs';
import {observe} from '../ui-parity-tooltip-segment-keyboard-revised/harness/collector.mjs';
import {limits,cases} from '../ui-parity-tooltip-segment-keyboard-revised/harness/contract.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,path.basename(path.dirname(here))==='reviewed'?'../../..':'../..');
const source=root+'/artifacts/ui-parity-tooltip-segment-keyboard-revised';
const historical=root+'/artifacts/ui-parity-tooltip-followup/capture/attempt-20261017-tooltip-followup-a1/T06.json';
const raw=JSON.parse(fs.readFileSync(historical)).keyboard[0].tabs[0].state.pair[0];
const clone=v=>structuredClone(v),same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const checks=[];
function check(name,ok){checks.push({name,passed:!!ok});if(!ok)throw Error(name);}
function rejects(name,fn,pattern){let error;try{fn();}catch(e){error=e;}check(name,error&&pattern.test(error.message));}
const journey=fs.readFileSync(source+'/harness/journey.mjs','utf8');
const inputCode=journey.slice(journey.indexOf('async function input('),journey.indexOf('const ui='));
const keyboardCode=journey.slice(journey.indexOf('async function keyboard('),journey.indexOf('function dashboard('));
const catchAt=journey.indexOf("}catch(e){current.status=e.message==='not-run-budget'");
const catchCode=journey.slice(catchAt+1,journey.indexOf('    const events=',catchAt));
const caseCatch=(current,error)=>{current.probes??=[];const c={current,item:cases[5],injected:error};vm.createContext(c);vm.runInContext('try{throw injected;}'+catchCode,c);return c.current;};

function mock(allowance,{failure=null}={}){
  let clock=0,sent=0,images=0,observations=0;const writes=[];
  const c={current:{id:'T06',ledger:[],keyboard:[],actions:0,modes:['Single','Multiple','Compact'],tabCap:24,sequence:cases[5].sequence},phase:'T06',actions:0,setupActions:0,probes:24,
    limits,ledger:[],ready:true,credential:{email:'synthetic@example.invalid',password:'synthetic'},guard:()=>{},sample:r.sample,modeSample:r.modeSample,settlement:r.settlement,
    invocation:r.invocation,boundedEntry:r.entry,dom:function dom(){},Date:{now:()=>clock},Buffer,JSON,
    page:{evaluate:async fn=>fn===c.dom||fn.name==='dom'?clone(raw):sent,keyboard:{press:async()=>{sent++;if(failure==='input')throw Error('x'.repeat(6000));}}},
    persist:()=>{r.casePrewrite(c.current);writes.push(JSON.stringify(c.current));},screenshot:async name=>{images++;return name+'.png';}};
  // Only the analysis VM substitutes this arithmetic; the accepted source reserve remains 32768.
  c.reserveInput=current=>{if(current.id==='T06'&&r.bytes(current)+allowance>r.retention.caseGuard)throw Error('not-run-budget');};
  c.observe=async(page,guard,inspect)=>{
    if(failure==='observation'||failure==='late-observation'&&observations===70)throw Error('x'.repeat(40000));
    const local={limits,dom:c.dom,Date:{now:()=>clock},delay:async ms=>{clock+=ms;}};
    vm.createContext(local);vm.runInContext('this.run='+observe.toString(),local);observations++;
    return local.run({evaluate:async()=>clone(raw)},guard,inspect);
  };
  c.ui=()=>({mode:async()=>c.input('Mode',null,'key','Escape'),close:async()=>{}});
  vm.createContext(c);vm.runInContext(inputCode+'\n'+keyboardCode,c);
  return {c,run:()=>c.keyboard(),stats:()=>({sent,images,observations,writes})};
}
async function traversal(allowance){const m=mock(allowance);let stop=null;try{await m.run();}catch(e){stop=e.message;}
  return {allowance,stop,tabs:m.c.current.keyboard.map(k=>k.tabs.length),modes:m.c.current.keyboard.map(k=>k.status),
    totalTabs:m.c.current.keyboard.reduce((n,k)=>n+k.tabs.length,0),actions:m.c.actions,globalProbes:m.c.probes,emittedInputs:m.stats().sent,
    caseBytes:r.bytes(m.c.current),reservedTotal:r.bytes(m.c.current)+allowance,guard:r.retention.caseGuard};}

check('all accepted reservation and case caps unchanged',same(r.retention,{sampleBytes:4096,baselineBytes:2048,entryBytes:6144,invocationBytes:14336,inputReserve:32768,caseGuard:115072,tailReserve:16000}));
check('all fixed case/input/image/time caps unchanged',cases.length===8&&limits.totalActions===396&&limits.probes===96&&limits.screenshots===48&&limits.outerMs===900000&&limits.caseBytes===131072);
const declared=[14336,6144,2048,2*1024,2048],candidate=declared.reduce((a,b)=>a+b,0);
check('declared arithmetic is 26624',candidate===26624);
check('guard to hard ceiling equals separate tail reserve',limits.caseBytes-r.retention.caseGuard===r.retention.tailReserve);
const original=await traversal(r.retention.inputReserve),proposed=await traversal(candidate);
check('accepted 70-Tab mock reproduced exactly',original.stop==='not-run-budget'&&same(original.tabs,[24,24,22])&&original.caseBytes===82395&&original.reservedTotal-original.guard===91&&original.globalProbes===94&&original.actions===76);
check('experimental 26624 VM closes fixed 72-Tab mock',proposed.stop===null&&same(proposed.tabs,[24,24,24])&&proposed.totalTabs===72&&proposed.globalProbes===96&&proposed.actions===78);
check('experimental 72 mock stays within unchanged guard',proposed.reservedTotal<=proposed.guard&&proposed.caseBytes<=limits.caseBytes);

const entry={id:'T06.a001',label:'Tab traversal',method:'key',argument:'Tab',elapsedMs:0,status:'failed',reason:''};
entry.reason='\u0000'.repeat(900);r.entry(entry);
check('failed entry accounts for escaped JSON bytes',r.bytes(entry)>entry.reason.length&&r.bytes(entry)<=r.retention.entryBytes);
rejects('failed input receipt cap checks serialization',()=>r.entry({...entry,reason:'\u0000'.repeat(1100)}),/entry bytes/);
rejects('multibyte visible state aggregate cap enforced',()=>r.sample({...clone(raw),liveStatus:'\u0000'.repeat(2048)}),/sample bytes/);
const failed=mock(candidate,{failure:'input'});let failedError;try{await failed.c.input('Tab traversal',null,'key','Tab');}catch(e){failedError=e;}
check('actual failed input emits one counted action',failed.stats().sent===1&&failed.c.actions===1&&failed.c.current.actions===1);
check('actual bounded failed receipt preserves failed status',failed.c.current.ledger[0].status==='failed'&&r.bytes(failed.c.current.ledger[0])<=r.retention.entryBytes);
const beforeFailedCatch=r.bytes(failed.c.current);caseCatch(failed.c.current,failedError);
check('case reason repeats bounded input error outside entry',failed.c.current.reason===failedError.message&&r.bytes(failed.c.current)>beforeFailedCatch+failedError.message.length);

const tiny={id:'T06',actions:0,ledger:[],probes:[],keyboard:[],status:'started'};
const atBoundary=clone(tiny);atBoundary.padding='';atBoundary.padding='x'.repeat(r.retention.caseGuard-candidate-r.bytes(atBoundary));
check('candidate boundary constructed exactly',r.bytes(atBoundary)+candidate===r.retention.caseGuard);
const error=Error('x'.repeat(candidate+1000)),beforeReason=r.bytes(atBoundary);
caseCatch(atBoundary,error);const afterReason=r.bytes(atBoundary);
check('actual case catch has uncapped reason larger than candidate',afterReason-beforeReason>candidate&&atBoundary.reason.length===candidate+1000);
check('uncapped reason exceeds nominal scaffold 2048',afterReason-beforeReason>2048);
check('counterexample remains below hard ceiling before tail',afterReason<limits.caseBytes);
const tail={events:[],elapsedMs:1};tail.events.push('');tail.events[0]='x'.repeat(r.retention.tailReserve-r.bytes(tail));
r.finalTail(tail.events,tail.elapsedMs);const beforeTail=r.bytes(atBoundary);Object.assign(atBoundary,tail);
check('valid full tail respects serialized tail cap',r.bytes(tail)===r.retention.tailReserve);
check('JSON object merge accounts for separators',r.bytes(atBoundary)-beforeTail===r.bytes(tail)-1);
rejects('uncapped case reason plus legal tail rejected at hard ceiling',()=>r.casePrewrite(atBoundary),/Case JSON bound/);
const overEntry=clone(tiny);overEntry.ledger=[{reason:'x'.repeat(r.retention.entryBytes)}];
rejects('invalid failed entry remains outside completed retention proof',()=>r.casePrewrite(overEntry),/entry bytes/);

const observedFailure=mock(candidate,{failure:'observation'});let observationError;
try{await observedFailure.run();}catch(e){observationError=e;}
const observationBefore=r.bytes(observedFailure.c.current);caseCatch(observedFailure.c.current,observationError);
check('actual T06 post-input observation error reaches uncapped catch',observationError.message.length===40000&&observedFailure.c.current.reason.length===40000&&r.bytes(observedFailure.c.current)-observationBefore>candidate);
check('observation failure occurs after emitted counted input',observedFailure.c.actions===3&&observedFailure.stats().sent===3&&observedFailure.c.probes===25);
const lateFailure=mock(candidate,{failure:'late-observation'});let lateError;
try{await lateFailure.run();}catch(e){lateError=e;}
const lateBefore=r.bytes(lateFailure.c.current);caseCatch(lateFailure.c.current,lateError);const lateAfter=r.bytes(lateFailure.c.current);
check('late counterexample follows 70 retained Tabs with emitted 71st',lateFailure.c.current.keyboard.reduce((n,k)=>n+k.tabs.length,0)===70&&lateFailure.c.probes===95&&lateFailure.c.actions===77);
check('late non-input error grows beyond examined allowance',lateAfter-lateBefore>candidate&&lateAfter<limits.caseBytes);
Object.assign(lateFailure.c.current,tail);
rejects('late error and legal tail fail hard case prewrite',()=>r.casePrewrite(lateFailure.c.current),/Case JSON bound/);
const sameIssue=clone(tiny);caseCatch(sameIssue,Error('x'.repeat(40000)));
check('gap is not unique to candidate or an R01 regression',r.bytes(sameIssue)-r.bytes(tiny)>r.retention.inputReserve);

const result={scope:'Source-only reservation arithmetic; no collector adoption or runtime',command:'node artifacts/ui-parity-tooltip-reservation-analysis/calculate.mjs',exitCode:0,checks:checks.length,
  verdict:'NO_SMALLER_RESERVE_SELECTED: total append proof incomplete',candidateExamined:candidate,acceptedReserveUnchanged:r.retention.inputReserve,
  declaredComponents:{invocation:14336,ledger:6144,baseline:2048,twoControlReceipts:2048,nominalScaffold:2048,sum:candidate},
  mockOnly:{accepted:original,experimental:proposed,conditions:'Extracted actual input/keyboard/observe source; controlled clock; one retained DOM sample; Mode/Escape and Escape popup only; no browser controls or real runtime'},
  counterexamples:{uncappedReasonBytes:error.message.length,boundaryBytes:beforeReason,afterReasonBytes:afterReason,reasonGrowth:afterReason-beforeReason,
    legalTailBytes:r.bytes(tail),afterTailBytes:r.bytes(atBoundary),hardCeiling:limits.caseBytes,
    observationErrorBytes:observationError.message.length,failedInputEntryBytes:r.bytes(failed.c.current.ledger[0]),failedInputCaseReasonBytes:failed.c.current.reason.length,
    lateObservation:{retainedTabs:70,emittedTabs:71,actions:lateFailure.c.actions,globalProbes:lateFailure.c.probes,beforeCatchBytes:lateBefore,afterCatchBytes:lateAfter,afterTailBytes:r.bytes(lateFailure.c.current)}},
  conditionsForFutureProof:['Finite bound/rejection rule for case-level and outer-catch reason before serialization, including non-input exceptions.',
    'Derive every intervening schema/key/array/counter/image/mode/failure-field byte from exact source instead of assuming a 2048 scaffold.',
    'Retain separate 16000 final-tail proof and all global JSON/run-byte checks; fail-closed partial prefixes remain explicit.',
    'Independent review before any code adoption; runtime network/lifecycle prerequisites and complete keyboard coverage remain open.'],runtimeExecuted:false,results:checks};
fs.writeFileSync(here+'/verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({...result,results:undefined}));
