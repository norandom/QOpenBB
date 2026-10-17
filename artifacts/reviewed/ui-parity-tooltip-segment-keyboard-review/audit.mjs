import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import * as r from '../ui-parity-tooltip-segment-keyboard/harness/keyboard-retention.mjs';
import {observe,coordinate} from '../ui-parity-tooltip-segment-keyboard/harness/collector.mjs';
import {limits,cases} from '../ui-parity-tooltip-segment-keyboard/harness/contract.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../..');
const proposal=path.join(root,'artifacts/ui-parity-tooltip-segment-keyboard');
const historical=path.join(root,'artifacts/ui-parity-tooltip-followup/capture/attempt-20261017-tooltip-followup-a1');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b),clone=v=>structuredClone(v),checks=[];
function check(name,result){checks.push({name,passed:!!result});if(!result)throw Error(name);}
function throws(name,fn,pattern){let error;try{fn();}catch(e){error=e;}check(name,error&&pattern.test(error.message));}
async function fails(name,fn,pattern){let error;try{await fn();}catch(e){error=e;}check(name,error&&pattern.test(error.message));}
const pins={'plan.md':'6e53998013eaf92fd3041143a5ed73d3fdfd55a27ce1840cb1d0146e3d6ba7c7','source-hashes.json':'6ecfd2acdfad61d9860b30cc2c12dade357186fb08cab66cbe97529452fa8dcb','publication-allowlist.json':'54f9a5b383d9fec7131f5fbe3e4134c1fc77b9992295130cbd8d39e4f18ac85d'};
for(const [name,hash] of Object.entries(pins))check('frozen dispatch pin '+name,sha(path.join(proposal,name))===hash);
const manifest=read(proposal+'/source-hashes.json'),allowlist=read(proposal+'/publication-allowlist.json');
for(const item of [...manifest.inputs,...manifest.outputs,...allowlist.files])check('hash and bytes '+item.sourcePath,sha(path.join(root,item.sourcePath))===item.sha256&&fs.statSync(path.join(root,item.sourcePath)).size===item.bytes);
check('exact 31 publication content files',allowlist.files.length===31&&new Set(allowlist.files.map(x=>x.sourcePath)).size===31);
const beforeFrozen=Object.fromEntries([...allowlist.files.map(x=>x.sourcePath),'artifacts/ui-parity-tooltip-segment-keyboard/publication-allowlist.json'].map(p=>[p,sha(path.join(root,p))]));
for(const name of fs.readdirSync(proposal+'/baseline'))check('executed baseline '+name,sha(proposal+'/baseline/'+name)===sha(historical+'/harness/'+name));
const changed=fs.readdirSync(proposal+'/harness').filter(n=>!fs.existsSync(proposal+'/baseline/'+n)||sha(proposal+'/harness/'+n)!==sha(proposal+'/baseline/'+n));
check('four source changes only',equal(changed.sort(),['collector.mjs','io.mjs','journey.mjs','keyboard-retention.mjs']));
const diff=fs.readFileSync(proposal+'/collector.diff','utf8').replaceAll('\r\n','\n');
const sections=diff.split(/(?=^--- )/m).filter(Boolean);check('four exact diff sections',sections.length===4);
for(const section of sections){const lines=section.split('\n'),oldName=lines[0].slice(4),newName=lines[1].slice(4);
  const old=oldName==='/dev/null'?[]:fs.readFileSync(path.join(proposal,oldName),'utf8').replaceAll('\r\n','\n').split('\n').slice(0,-1);
  let cursor=0,out=[];
  for(let i=2;i<lines.length;i++){if(!lines[i].startsWith('@@'))continue;const match=/^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@/.exec(lines[i]);
    const start=Math.max(0,Number(match[1])-1);out.push(...old.slice(cursor,start));cursor=start;
    while(i+1<lines.length&&!lines[i+1].startsWith('@@')){const line=lines[++i];if(line==='')continue;
      if(line[0]===' '||line[0]==='-'){check('diff context '+newName+':'+cursor,old[cursor]===line.slice(1));cursor++;}
      if(line[0]===' '||line[0]==='+')out.push(line.slice(1));}
  }
  out.push(...old.slice(cursor));check('diff reconstructs '+newName,out.join('\n')+'\n'===fs.readFileSync(path.join(proposal,newName),'utf8').replaceAll('\r\n','\n'));
}
const raw=read(historical+'/T06.json').keyboard[0].tabs[0].state.pair[0];
const rawHidden=clone(raw);rawHidden.tooltip={visible:false,sanitizedInnerHTML:'version A'};
const rawOther=clone(rawHidden);rawOther.tooltip.sanitizedInnerHTML='version B';
check('omitted DOM differences project identically',equal(r.sample(rawHidden),r.sample(rawOther)));
let calls=0,inspections=0;
const stable=await observe({evaluate:async()=>clone([rawHidden,rawOther,rawOther][Math.min(calls++,2)])},()=>{},()=>inspections++);
check('full DOM difference delays stable result',calls===3&&inspections===3&&stable.sampleCount===3);
check('stable actual full pair retained',equal(stable.pair,[rawOther,rawOther]));
const unstableInputs=[];
const unstable=await observe({evaluate:async()=>{const value=clone(unstableInputs.length%2?rawOther:rawHidden);unstableInputs.push(value);return value;}},()=>{});
check('exhaustion remains unresolved',unstable.status==='tooltip-observation-unresolved'&&unstableInputs.length>=2);
check('R01 reproduced: unequal final two actual samples',!equal(unstableInputs.at(-2),unstableInputs.at(-1)));
check('R01 reproduced: returned pair duplicates last object',unstable.pair[0]===unstable.pair[1]&&equal(unstable.pair[0],unstableInputs.at(-1)));
const mode={};r.modeSample(mode,raw);const changedArea=clone(raw);changedArea.swapchain[0].name+=' changed';
throws('swapchain baseline change stops',()=>r.modeSample(mode,changedArea),/baseline changed/);
check('previous baseline preserved after rejection',equal(mode.baseline,{area:raw.area,swapchain:raw.swapchain}));
for(const value of [null,NaN,Infinity,'12',undefined]){const g=clone(read(historical+'/T08.json').probes.at(-1).settlement.pair[1]);g.series.find(x=>x.yKey==='operatingIncome').nodes[0].midPoint.x.value=value;
  throws('stacked invalid x '+String(value),()=>coordinate(g,1,'operatingIncome','stackedColumn'),/finite stacked midpoint/);}
for(const field of ['active','liveStatus']){const v=clone(raw);if(field==='active')v.active.name='\u0000'.repeat(512);else v.liveStatus='\u0000'.repeat(2048);
  if(field==='liveStatus')throws('escaped character bytes stop',()=>r.sample(v),/sample bytes/);else check('escaped active string preserved without truncation',r.sample(v).active.name===v.active.name);}
const tiny={id:'T06',ledger:[],keyboard:[],actions:0};
const fit=clone(tiny);fit.padding='';fit.padding='x'.repeat(r.retention.caseGuard-r.retention.inputReserve-r.bytes(fit));
check('exact prospective boundary arithmetic',r.bytes(fit)+r.retention.inputReserve===r.retention.caseGuard);r.reserveInput(fit);
throws('one byte over prospective boundary stops',()=>r.reserveInput({...fit,padding:fit.padding+'x'}),/not-run-budget/);
const journey=fs.readFileSync(proposal+'/harness/journey.mjs','utf8');
const inputCode=journey.slice(journey.indexOf('async function input('),journey.indexOf('const ui='));
const keyboardCode=journey.slice(journey.indexOf('async function keyboard('),journey.indexOf('function dashboard('));
function context(options={}){
  let sent=0,writes=[],images=0,evaluations=0;
  const c={current:{...clone(tiny),modes:['Single','Multiple','Compact'],tabCap:24,sequence:cases[5].sequence},phase:'T06',actions:0,setupActions:0,probes:24,limits,ledger:[],ready:true,
    credential:{email:'synthetic@example.invalid',password:'synthetic-only-placeholder'},guard:()=>{},reserveInput:r.reserveInput,sample:r.sample,modeSample:r.modeSample,settlement:r.settlement,invocation:r.invocation,boundedEntry:r.entry,
    dom:function dom(){},observe,Date,Buffer,JSON,
    page:{evaluate:async fn=>{if(fn===c.dom||fn.name==='dom'){evaluations++;const v=clone(raw);v.active.inSeriesArea=!!options.reached;if(options.oversized&&sent)v.liveStatus='x'.repeat(2049);return v;}return sent;},keyboard:{press:async()=>{sent++;}}},
    persist:()=>{r.casePrewrite(c.current);writes.push(JSON.stringify(c.current));},
    screenshot:async name=>{images++;return name+'.png';},
  };
  c.ui=()=>({mode:async()=>{await c.input('Mode',null,'key','Escape');},close:async()=>{}});
  vm.createContext(c);vm.runInContext(inputCode+'\n'+keyboardCode,c);return {c,stats:()=>({sent,writes,images,evaluations})};
}
const unreachable=context();let traversalStop=null;try{await unreachable.c.keyboard();}catch(e){traversalStop=e.message;}
check('unreachable path stays inside caps or stops at reservation',traversalStop===null||traversalStop==='not-run-budget');
check('unreachable path uses fixed shared 96 probe cap',unreachable.c.probes<=96&&unreachable.c.current.keyboard.every(k=>k.tabs.length<=24&&k.keys.length===0));
check('unreachable branch never marks reached',unreachable.c.current.keyboard.every(k=>k.status!=='reached'));
check('reservation stop emits no extra Tab',unreachable.c.probes-24===unreachable.c.current.keyboard.reduce((n,k)=>n+k.tabs.length,0));
const reached=context({reached:true});await reached.c.keyboard();
check('three conditional arrow branches retain actual invocations',reached.c.current.keyboard.every(k=>k.tabs.length===1&&k.keys.length===7));
check('conditional arrow shared probe accounting',reached.c.probes===48&&reached.stats().images===24);
check('conditional after/entry samples retain equal content',reached.c.current.keyboard.every(k=>k.keys.every(i=>equal(i.after.pair[0],i.after.pair[1]))));
const overflow=context({oversized:true});
await fails('post-input projection overflow stops',()=>overflow.c.input('Tab traversal',null,'key','Tab'),/text cap/);
check('post-input overflow records an emitted action',overflow.stats().sent===1&&overflow.c.actions===1&&overflow.c.current.actions===1);
check('post-input overflow has preserved started prefix',JSON.parse(overflow.stats().writes[0]).ledger[0].status==='started');
check('post-input overflow retains failed receipt when bounded',JSON.parse(overflow.stats().writes.at(-1)).ledger[0].status==='failed');
const noInput=context();noInput.c.current={...fit,padding:fit.padding+'x'};
await fails('actual input at one-byte overflow rejected',()=>noInput.c.input('Tab traversal',null,'key','Tab'),/not-run-budget/);
check('no rejected input counter or receipt advances',noInput.c.actions===0&&noInput.stats().sent===0&&noInput.stats().writes.length===0);
const noProbe=context();noProbe.c.current={...noProbe.c.current,padding:'x'.repeat(r.retention.caseGuard)};noProbe.c.ui=()=>({mode:async()=>{},close:async()=>{}});noProbe.c.input=async()=>{};
await fails('keyboard prospective overflow rejected',()=>noProbe.c.keyboard(),/not-run-budget/);check('rejected keyboard probe does not advance',noProbe.c.probes===24);
const ioDir=path.join(here,'audit-io');fs.mkdirSync(ioDir,{recursive:true});process.env.CAPTURE_ROOT=ioDir;
try{const io=await import('../ui-parity-tooltip-segment-keyboard/harness/io.mjs');io.json('T06',tiny);const priorBytes=fs.readFileSync(ioDir+'/T06.json');
  for(const [name,value,pattern] of [
    ['case',{...tiny,padding:'x'.repeat(limits.caseBytes)},/Case JSON bound/],
    ['invocation',{...tiny,keyboard:[{tabs:[{padding:'x'.repeat(r.retention.invocationBytes)}]}]},/invocation bytes/],
    ['baseline',{...tiny,keyboard:[{baseline:{padding:'x'.repeat(r.retention.baselineBytes)}}]},/baseline bytes/],
    ['ledger',{...tiny,ledger:[{reason:'x'.repeat(r.retention.entryBytes)}]},/entry bytes/]]){
    throws(name+' writer rejects before overwrite',()=>io.json('T06',value),pattern);check(name+' preserves exact persisted prefix',fs.readFileSync(ioDir+'/T06.json').equals(priorBytes));}
}finally{fs.unlinkSync(ioDir+'/T06.json');fs.rmdirSync(ioDir);}
const plan=fs.readFileSync(proposal+'/plan.md','utf8');const links=[];
for(const m of plan.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){const target=m[1].split('#')[0];if(/^https?:/.test(target))continue;check('source plan link '+target,fs.existsSync(path.resolve(proposal,target)));links.push(target);}
for(const item of allowlist.files){check('safe proposal-owned path '+item.sourcePath,item.sourcePath.startsWith('artifacts/ui-parity-tooltip-segment-keyboard/')&&!item.sourcePath.includes('..')&&/\.(mjs|md|json|diff|sh)$/.test(item.sourcePath));
  const text=fs.readFileSync(path.join(root,item.sourcePath),'utf8');
  check('no concrete private key/token '+item.sourcePath,!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_-]{20,}/.test(text));}
for(const [file,hash] of Object.entries(beforeFrozen))check('original package preserved '+file,sha(path.join(root,file))===hash);
const result={scope:'Independent offline review; no runtime grant',date:'2026-10-17',verdict:'REJECTED',runtimeExecuted:false,command:'node artifacts/ui-parity-tooltip-segment-keyboard-review/audit.mjs',exitCode:0,checks:checks.length,
  frozenPins:pins,suppliedVerifier:{checks:108,exitCode:0,receiptWrite:'suppressed after exact-byte equality',temporaryWrites:'redirected to review-owned directory'},freezeCheck:{checks:89,exitCode:0},
  reproduction:{finding:'R01',sampleCount:unstableInputs.length,status:unstable.status,actualFinalTwoEqual:equal(unstableInputs.at(-2),unstableInputs.at(-1)),returnedPairSameObject:unstable.pair[0]===unstable.pair[1],stablePathCorrect:true},
  unreachableSimulation:{stop:traversalStop,actions:unreachable.c.actions,emittedInputs:unreachable.stats().sent,globalProbes:unreachable.c.probes,initialPointerProbes:24,caseBytes:r.bytes(unreachable.c.current),reservedBytes:r.retention.inputReserve,caseGuard:r.retention.caseGuard,modes:unreachable.c.current.keyboard.map(k=>({mode:k.mode,status:k.status,tabs:k.tabs.length,keys:k.keys.length})),setupModel:'Synthetic mode setup emits Mode/Escape and Escape popup only; not full browser controls or a runtime capacity prediction'},
  publication:{contentFiles:31,metadataFiles:1,sourceLinks:links,scope:'Safe for publication as a rejected proposal with this review; not an accepted collector'},
  openRuntimePrerequisites:['B01 traffic-denial boundary','Independent inherited lifecycle review and controller grant'],results:checks};
fs.writeFileSync(here+'/verification.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,results:undefined,publication:undefined}));
