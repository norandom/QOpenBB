import fs from 'node:fs';
import vm from 'node:vm';
import {observe} from './harness/collector.mjs';
import {observe as rejectedObserve} from './baseline/collector.mjs';
import * as r from './harness/keyboard-retention.mjs';
import {limits,cases} from './harness/contract.mjs';

const clone=v=>structuredClone(v),equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function controlled(fn,page,{step=0}={}){
  let clock=0,inspections=0,delays=0,guards=0;
  const context={limits,dom:function dom(){},Date:{now:()=>clock},
    delay:async ms=>{delays++;clock+=step==='interval'?ms:step;}};
  vm.createContext(context);vm.runInContext('this.run='+fn.toString(),context);
  return {run:()=>context.run(page,()=>guards++,()=>inspections++),
    advance:ms=>{clock+=ms;},stats:()=>({clock,inspections,delays,guards})};
}
export async function faults({here,prior,check,sha}){
  const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
  const original=here+'/../ui-parity-tooltip-segment-keyboard';
  check('frozen original source manifest preserved',sha(original+'/source-hashes.json')==='6ecfd2acdfad61d9860b30cc2c12dade357186fb08cab66cbe97529452fa8dcb');
  check('frozen original publication metadata preserved',sha(original+'/publication-allowlist.json')==='54f9a5b383d9fec7131f5fbe3e4134c1fc77b9992295130cbd8d39e4f18ac85d');
  for(const item of read(original+'/publication-allowlist.json').files){
    const file=original+'/'+item.sourcePath.slice('artifacts/ui-parity-tooltip-segment-keyboard/'.length);
    check('original package bytes preserved '+item.sourcePath,sha(file)===item.sha256&&fs.statSync(file).size===item.bytes);
  }
  for(const name of fs.readdirSync(here+'/baseline'))check('rejected proposal baseline '+name,sha(here+'/baseline/'+name)===sha(here+'/../ui-parity-tooltip-segment-keyboard/harness/'+name));
  const changed=fs.readdirSync(here+'/harness').filter(name=>sha(here+'/harness/'+name)!==sha(here+'/baseline/'+name));
  check('R01 only runtime source difference',equal(changed,['collector.mjs']));
  const raw=read(prior+'/T06.json').keyboard[0].tabs[0].state.pair[0];
  const a=clone(raw);a.tooltip={visible:false,sanitizedInnerHTML:'A'};
  const b=clone(a);b.tooltip.sanitizedInnerHTML='B';
  check('different raw HTML has equal compact projection',equal(r.sample(a),r.sample(b))&&!equal(a,b));
  const makeAlternating=()=>{const inputs=[];return {inputs,page:{evaluate:async()=>{const sample=clone(inputs.length%2?b:a);inputs.push(sample);return sample;}}};};
  const sampleCase=makeAlternating(),sampleClock=controlled(observe,sampleCase.page);
  const exhausted=await sampleClock.run();
  check('sample exhaustion reads unchanged cap',sampleCase.inputs.length===limits.tooltipSamples&&exhausted.sampleCount===limits.tooltipSamples);
  check('sample exhaustion remains unresolved',exhausted.status==='tooltip-observation-unresolved');
  check('sample exhaustion actual unequal final two',equal(exhausted.pair,sampleCase.inputs.slice(-2))&&!equal(exhausted.pair[0],exhausted.pair[1]));
  check('sample exhaustion distinct retained objects',exhausted.pair[0]!==exhausted.pair[1]);
  check('sample exhaustion inspection count unchanged',sampleClock.stats().inspections===limits.tooltipSamples&&sampleClock.stats().guards===limits.tooltipSamples);
  const projected=r.settlement(exhausted);
  check('actual T06 unresolved projection retains two samples',projected.status==='tooltip-observation-unresolved'&&projected.pair.length===2&&projected.sampleCount===limits.tooltipSamples);
  check('equal compact failure values never imply stable',equal(projected.pair[0],projected.pair[1])&&projected.status!=='stable');
  const deadlineCase=makeAlternating();let deadlineClock;
  deadlineClock=controlled(observe,{evaluate:async()=>{deadlineClock.advance(700);return deadlineCase.page.evaluate();}},{step:'interval'});
  const deadline=await deadlineClock.run();
  check('deadline exhaustion before sample cap',deadline.sampleCount===3&&deadline.sampleCount<limits.tooltipSamples&&deadlineClock.stats().clock>=limits.tooltipMs);
  check('deadline exhaustion actual final two',deadline.status==='tooltip-observation-unresolved'&&equal(deadline.pair,deadlineCase.inputs.slice(-2))&&!equal(deadline.pair[0],deadline.pair[1]));
  let singleClock;singleClock=controlled(observe,{evaluate:async()=>{singleClock.advance(limits.tooltipMs+1);return clone(a);}},{step:'interval'});
  const single=await singleClock.run(),singleProjected=r.settlement(single);
  check('single sample exhaustion retains one actual sample',single.status==='tooltip-observation-unresolved'&&single.sampleCount===1&&single.pair.length===1&&equal(single.pair[0],a));
  check('single sample actual T06 projection has no invented pair',singleProjected.pair.length===1&&singleProjected.sampleCount===1);
  check('single sample inspection precedes exhaustion',singleClock.stats().inspections===1&&singleClock.stats().guards===1);
  const rejectedCase=makeAlternating(),rejectedClock=controlled(rejectedObserve,rejectedCase.page);
  const rejected=await rejectedClock.run();
  check('baseline reproduces R01 duplicated failure pair',rejected.pair[0]===rejected.pair[1]&&!equal(rejectedCase.inputs.at(-2),rejectedCase.inputs.at(-1)));
  let stableReads=0;const stableInputs=[];
  const stableClock=controlled(observe,{evaluate:async()=>{const sample=clone([a,b,b][stableReads++]);stableInputs.push(sample);return sample;}});
  const stable=await stableClock.run();
  check('stable full DOM equality unchanged',stable.status==='stable'&&stable.sampleCount===3&&stableClock.stats().inspections===3&&equal(stable.pair,stableInputs.slice(-2)));

  const journey=fs.readFileSync(here+'/harness/journey.mjs','utf8');
  const inputCode=journey.slice(journey.indexOf('async function input('),journey.indexOf('const ui='));
  const keyboardCode=journey.slice(journey.indexOf('async function keyboard('),journey.indexOf('function dashboard('));
  function journeyContext({alternating=false}={}){
    let sent=0,images=0,elapsed=0,observation;
    const c={current:{id:'T06',ledger:[],keyboard:[],actions:0,modes:['Single','Multiple','Compact'],tabCap:24,sequence:cases[5].sequence},phase:'T06',actions:0,setupActions:0,probes:24,
      limits,ledger:[],ready:true,credential:{email:'synthetic@example.invalid',password:'synthetic'},guard:()=>{},reserveInput:r.reserveInput,sample:r.sample,modeSample:r.modeSample,
      settlement:r.settlement,invocation:r.invocation,boundedEntry:r.entry,dom:function dom(){},Date:{now:()=>elapsed},Buffer,JSON,
      page:{evaluate:async fn=>fn===c.dom||fn.name==='dom'?clone(alternating?a:raw):sent,keyboard:{press:async()=>{sent++;}}},
      persist:()=>r.casePrewrite(c.current),screenshot:async name=>{images++;return name+'.png';}};
    c.observe=async(page,guard,inspect)=>{
      let count=0;const sampleInputs=[];
      const local={limits,dom:c.dom,Date:{now:()=>elapsed},delay:async ms=>{elapsed+=ms;}};
      vm.createContext(local);vm.runInContext('this.run='+observe.toString(),local);
      observation=await local.run({evaluate:async()=>{const sample=clone(alternating?(count++%2?b:a):raw);sampleInputs.push(sample);return sample;}},guard,inspect);
      observation.inputs=sampleInputs;return observation;
    };
    c.ui=()=>({mode:async()=>c.input('Mode',null,'key','Escape'),close:async()=>{}});
    vm.createContext(c);vm.runInContext(inputCode+'\n'+keyboardCode,c);
    return {c,stats:()=>({sent,images,observation})};
  }
  const actual=journeyContext({alternating:true});let reason;
  try{await actual.c.keyboard();}catch(e){reason=e.message;}
  const actualState=actual.c.current.keyboard[0].tabs[0].state;
  check('actual T06 stops on raw alternating HTML',reason==='tooltip-observation-unresolved'&&actual.c.current.keyboard[0].tabs.length===1);
  check('actual T06 retains unresolved actual projected pair',actualState.status==='tooltip-observation-unresolved'&&actualState.pair.length===2&&equal(actualState.pair,actual.stats().observation.pair.map(r.sample)));
  check('actual T06 no extra input on observation failure',actual.c.probes===25&&actual.c.actions===3&&actual.stats().sent===3);
  const traversal=journeyContext();let stop;
  try{await traversal.c.keyboard();}catch(e){stop=e.message;}
  const modes=traversal.c.current.keyboard.map(k=>k.tabs.length);
  check('unchanged conservative reservation stops at 70 mock Tabs',stop==='not-run-budget'&&equal(modes,[24,24,22]));
  check('70-Tab mock retains shared counters',traversal.c.probes===94&&traversal.c.actions===76&&traversal.stats().sent===76);
  const caseBytes=r.bytes(traversal.c.current),excess=caseBytes+r.retention.inputReserve-r.retention.caseGuard;
  check('70-Tab mock 91 bytes over unchanged guard',caseBytes===82395&&excess===91);
  check('70-Tab mock remains seeking with no arrows',traversal.c.current.keyboard[2].status==='seeking'&&traversal.c.current.keyboard.every(k=>k.keys.length===0));
  return {sampleExhaustion:exhausted.sampleCount,deadlineExhaustion:deadline.sampleCount,singleSample:single.sampleCount,
    actualT06Failure:actualState.status,unreachableMock:{tabs:modes,totalTabs:70,globalProbes:94,actions:76,caseBytes,excessBytes:excess,
      limit:'Synthetic Mode/Escape setup and one retained DOM sample; no runtime capacity or complete 72-Tab coverage'}};
}
