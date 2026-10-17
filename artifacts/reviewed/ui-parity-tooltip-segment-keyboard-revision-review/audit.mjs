import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {observe} from '../ui-parity-tooltip-segment-keyboard-revised/harness/collector.mjs';
import {observe as rejected} from '../ui-parity-tooltip-segment-keyboard-revised/baseline/collector.mjs';
import {limits} from '../ui-parity-tooltip-segment-keyboard-revised/harness/contract.mjs';
import {sample,settlement} from '../ui-parity-tooltip-segment-keyboard-revised/harness/keyboard-retention.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../..'),proposal=path.join(root,'artifacts/ui-parity-tooltip-segment-keyboard-revised');
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),read=p=>JSON.parse(fs.readFileSync(p));
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b),checks=[];
function check(name,value){checks.push({name,passed:!!value});if(!value)throw Error(name);}
const pins={'plan.md':'2cbf5814b0faed0c7c060ad85ba980ac8abf581c14470926ea00fe3e389c149c','source-hashes.json':'bc04326902f1f8f249b075ee1b2411ec14c85f9879bbd9b1ef9af7eb6c7aa172','publication-allowlist.json':'b9fa990c55d9521fe31fb82557d18165f33b49cd013d804a632c660840130324','collector.diff':'344ee487276ef57ff669e53cc9d21b0632cf7f3de0bd28476b2c79eedbaf72dd'};
for(const [file,hash] of Object.entries(pins))check('dispatch pin '+file,sha(proposal+'/'+file)===hash);
const manifest=read(proposal+'/source-hashes.json'),list=read(proposal+'/publication-allowlist.json');
for(const item of [...manifest.inputs,...manifest.outputs,...list.files])check('source bytes '+item.sourcePath,sha(root+'/'+item.sourcePath)===item.sha256&&fs.statSync(root+'/'+item.sourcePath).size===item.bytes);
check('45 unique content files',list.files.length===45&&new Set(list.files.map(x=>x.sourcePath)).size===45);
for(const item of list.files){check('safe proposal text '+item.sourcePath,item.sourcePath.startsWith('artifacts/ui-parity-tooltip-segment-keyboard-revised/')&&!item.sourcePath.includes('..')&&/\.(mjs|md|json|diff|sh)$/.test(item.sourcePath));
  check('no concrete private key or token '+item.sourcePath,!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_-]{20,}/.test(fs.readFileSync(root+'/'+item.sourcePath,'utf8')));}
const priorRoot=root+'/artifacts/ui-parity-tooltip-segment-keyboard';
for(const item of read(priorRoot+'/publication-allowlist.json').files)check('original immutable '+item.sourcePath,sha(root+'/'+item.sourcePath)===item.sha256);
for(const item of read(root+'/artifacts/ui-parity-tooltip-segment-keyboard-review/publication-allowlist.json').files)check('original review immutable '+item.sourcePath,sha(root+'/'+item.sourcePath)===item.sha256);
for(const name of fs.readdirSync(proposal+'/baseline'))check('rejected baseline identity '+name,sha(proposal+'/baseline/'+name)===sha(priorRoot+'/harness/'+name));
const changed=fs.readdirSync(proposal+'/harness').filter(n=>sha(proposal+'/harness/'+n)!==sha(proposal+'/baseline/'+n));check('collector is sole source change',equal(changed,['collector.mjs']));
const before=fs.readFileSync(proposal+'/baseline/collector.mjs','utf8'),after=fs.readFileSync(proposal+'/harness/collector.mjs','utf8');
const reconstructed=before.replace('let prior=null,count=0,last=null;','let prior=null,previous=null,count=0,last=null;').replace('prior=last;if(count<limits.tooltipSamples)','previous=prior;prior=last;if(count<limits.tooltipSamples)').replace('pair:prior?[prior,last]:[]','pair:previous?[previous,last]:last?[last]:[]');
check('exact three substitutions reconstruct collector',reconstructed===after);
const raw=read(root+'/artifacts/ui-parity-tooltip-followup/capture/attempt-20261017-tooltip-followup-a1/T06.json').keyboard[0].tabs[0].state.pair[0];
const a=structuredClone(raw);a.tooltip={visible:false,sanitizedInnerHTML:'alpha'};
const b=structuredClone(a);b.tooltip.sanitizedInnerHTML='beta';check('counterexample raw differs but compact equal',!equal(a,b)&&equal(sample(a),sample(b)));
async function run(fn,{sequence,readTime=0,delayTime=0,zero=false,inspectFailure=false}={}){
  let clock=0,dateCalls=0;const inputs=[],order=[];
  const context={limits,dom:function dom(){},Date:{now:()=>zero&&dateCalls++>0?limits.tooltipMs:clock},delay:async()=>{clock+=delayTime;order.push('delay');}};
  vm.createContext(context);vm.runInContext('this.run='+fn.toString(),context);
  const result=await context.run({evaluate:async()=>{order.push('read');clock+=readTime;const value=structuredClone(sequence?sequence[Math.min(inputs.length,sequence.length-1)]:(inputs.length%2?b:a));inputs.push(value);return value;}},()=>order.push('guard'),()=>{order.push('inspect');if(inspectFailure)throw Error('injected inspector failure');});
  return {result,inputs,order,clock};
}
const sampleCap=await run(observe),old=await run(rejected);
check('baseline R01 reproduces',old.result.pair[0]===old.result.pair[1]&&!equal(old.inputs.at(-2),old.inputs.at(-1)));
check('sample cap unchanged',sampleCap.inputs.length===20&&sampleCap.result.sampleCount===20);
check('actual distinct final two preserved',sampleCap.result.pair[0]===sampleCap.inputs.at(-2)&&sampleCap.result.pair[1]===sampleCap.inputs.at(-1)&&!equal(...sampleCap.result.pair));
check('raw unresolved status truthful',sampleCap.result.status==='tooltip-observation-unresolved');
const compact=settlement(sampleCap.result);check('projected unresolved equal members stay unresolved',compact.status==='tooltip-observation-unresolved'&&compact.pair.length===2&&equal(...compact.pair));
const deadline=await run(observe,{readTime:700,delayTime:100});check('deadline retains exact final two',deadline.inputs.length===3&&deadline.result.sampleCount===3&&deadline.result.pair[0]===deadline.inputs[1]&&deadline.result.pair[1]===deadline.inputs[2]);
const single=await run(observe,{readTime:2001,delayTime:100});check('single has exactly one actual sample',single.result.sampleCount===1&&single.result.pair.length===1&&single.result.pair[0]===single.inputs[0]&&settlement(single.result).pair.length===1);
const zero=await run(observe,{zero:true});check('zero samples invent no evidence',zero.inputs.length===0&&zero.result.sampleCount===0&&zero.result.pair.length===0);
const stable=await run(observe,{sequence:[a,b,b]}),stableOld=await run(rejected,{sequence:[a,b,b]});
check('stable full DOM semantics unchanged',equal(stable.result,stableOld.result)&&stable.result.status==='stable'&&stable.result.sampleCount===3&&stable.result.pair[0]===stable.inputs[1]&&stable.result.pair[1]===stable.inputs[2]);
check('stable inspector/read ordering unchanged',equal(stable.order,stableOld.order)&&stable.order.join(',')==='guard,read,inspect,delay,guard,read,inspect,delay,guard,read,inspect');
for(const [name,item] of [['sample',sampleCap],['deadline',deadline],['single',single]])check(name+' every read inspected',item.order.filter(x=>x==='read').length===item.order.filter(x=>x==='inspect').length&&item.inputs.length===item.result.sampleCount);
let failure;try{await run(observe,{inspectFailure:true});}catch(e){failure=e.message;}check('inspector failure still propagates',failure==='injected inspector failure');
const links=[];for(const m of fs.readFileSync(proposal+'/plan.md','utf8').matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){const target=m[1].split('#')[0];check('plan link '+target,fs.existsSync(path.resolve(proposal,target)));links.push(target);}
const result={date:'2026-10-17',verdict:'APPROVED',scope:'R01 closure and source publication only; runtime blocked',runtimeExecuted:false,pins,command:'node artifacts/ui-parity-tooltip-segment-keyboard-revision-review/audit.mjs',exitCode:0,checks:checks.length,
  suppliedVerifier:{exitCode:0,checks:177,receipt:'exact byte equality then write suppressed; IO redirected into review ownership'},freezeChecker:{exitCode:0,checks:151},
  independentCases:{sampleExhaustion:sampleCap.result.sampleCount,deadlineExhaustion:deadline.result.sampleCount,single:single.result.sampleCount,zero:zero.result.sampleCount,stable:stable.result.sampleCount,baselineDefectReproduced:true},
  publication:{contentFiles:45,metadataFiles:1,sourceLinks:links,destinationAudit:'required after synchronization'},
  open:['B01 traffic denial','Inherited lifecycle proof and exact-source controller grant','Complete keyboard coverage: unchanged 70-Tab mock stops 91 bytes above reservation guard'],results:checks};
fs.writeFileSync(here+'/verification.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,results:undefined,publication:undefined}));
