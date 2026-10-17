import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import * as r from '../ui-parity-tooltip-segment-keyboard-revised/harness/keyboard-retention.mjs';
import {cases,limits} from '../ui-parity-tooltip-segment-keyboard-revised/harness/contract.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../..'),source=root+'/artifacts/ui-parity-tooltip-reservation-analysis';
const read=p=>JSON.parse(fs.readFileSync(p)),sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),checks=[];
function check(name,value){checks.push({name,passed:!!value});if(!value)throw Error(name);}
function throws(name,fn,pattern){let e;try{fn();}catch(error){e=error;}check(name,e&&pattern.test(e.message));return e;}
const pins={'report.md':'9a8ac973294208f21857a272047cd35a05e980b5ca47917124912a0ddea9b629','source-hashes.json':'a7a10f1cea7d9734dc99f9c830855f52c5e7d41e7b340e076c90421c88afe5a6','publication-allowlist.json':'dcd1178172292a48a2a75089db750cba6eb3d28e6bb8b5e68ef612c85f97f32d'};
for(const [name,hash] of Object.entries(pins))check('frozen pin '+name,sha(source+'/'+name)===hash);
const manifest=read(source+'/source-hashes.json'),list=read(source+'/publication-allowlist.json');
for(const item of [...manifest.inputs,...manifest.outputs,...list.files])check('input/output bytes '+item.sourcePath,sha(root+'/'+item.sourcePath)===item.sha256&&fs.statSync(root+'/'+item.sourcePath).size===item.bytes);
check('five unique content files',list.files.length===5&&new Set(list.files.map(x=>x.sourcePath)).size===5);
for(const item of list.files){check('safe analysis-owned text '+item.sourcePath,item.sourcePath.startsWith('artifacts/ui-parity-tooltip-reservation-analysis/')&&!item.sourcePath.includes('..')&&/\.(mjs|md|json)$/.test(item.sourcePath));
  check('no private key or common token '+item.sourcePath,!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_-]{20,}/.test(fs.readFileSync(root+'/'+item.sourcePath,'utf8')));}
const journey=fs.readFileSync(root+'/artifacts/ui-parity-tooltip-segment-keyboard-revised/harness/journey.mjs','utf8');
const start=journey.indexOf("}catch(e){current.status=e.message==='not-run-budget'");
const caseCode=journey.slice(start+1,journey.indexOf('    const events=',start));
const outerStart=journey.indexOf('}catch(e){process.exitCode=1;const reason=');
const outerCode=journey.slice(outerStart+1,journey.indexOf('finally{clearTimeout(timer)',outerStart));
function applyCase(current,error){const context={current,item:cases[5],injected:error};vm.createContext(context);vm.runInContext('try{throw injected;}'+caseCode,context);return current;}
function applyOuter(current,error,persist){const context={current,injected:error,process:{exitCode:0},credential:{email:'synthetic@example.invalid',password:'unmatched-synthetic-password'},persist,phase:'T06',results:[],json:()=>{}};vm.createContext(context);vm.runInContext('try{throw injected;}'+outerCode,context);return context.process.exitCode;}
const candidate=14336+6144+2048+2*1024+2048;check('candidate arithmetic',candidate===26624&&r.retention.inputReserve-candidate===6144);
check('separate tail arithmetic',limits.caseBytes-r.retention.caseGuard===16000);
const record=read(source+'/verification.json');
check('mock72 arithmetic only',record.mockOnly.experimental.caseBytes+candidate===111325&&r.retention.caseGuard-111325===3747&&record.mockOnly.experimental.globalProbes===96);
check('late completed in-memory arithmetic',record.counterexamples.lateObservation.afterCatchBytes-record.counterexamples.lateObservation.beforeCatchBytes===40087&&122850+16000-1===138849&&138849>limits.caseBytes);
const tiny={id:'T06',actions:0,ledger:[],probes:[],keyboard:[],status:'started'};
const boundary=structuredClone(tiny);boundary.padding='';boundary.padding='x'.repeat(r.retention.caseGuard-candidate-r.bytes(boundary));
check('boundary exactly88448',r.bytes(boundary)===88448);
const before=r.bytes(boundary);applyCase(boundary,Error('x'.repeat(27624)));const afterReason=r.bytes(boundary);
check('independent actual catch grows27823',afterReason-before===27823&&afterReason===116271&&boundary.reason.length===27624);
const tail={events:[''],elapsedMs:1};tail.events[0]='x'.repeat(16000-r.bytes(tail));r.finalTail(tail.events,tail.elapsedMs);
check('API-admissible exact tail',r.bytes(tail)===16000);const merged={...boundary,...tail};
check('disjoint object merge adds15999',r.bytes(merged)-afterReason===15999&&r.bytes(merged)===132270);
throws('hard case prewrite rejects completed construction',()=>r.casePrewrite(merged),/Case JSON bound/);
const escaped=structuredClone(tiny);applyCase(escaped,Error('\u0000'.repeat(7000)));
check('case reason UTF8JSON growth exceeds current reserve',escaped.reason.length===7000&&r.bytes(escaped)-r.bytes(tiny)>32768);
const outer=structuredClone(tiny);let outerPersisted;applyOuter(outer,Error('x'.repeat(40000)),()=>{outerPersisted=structuredClone(outer);});
check('outer actual catch retains uncapped40000 reason',outerPersisted.reason.length===40000&&r.bytes(outerPersisted)-r.bytes(tiny)>32768);
const input=journey.slice(journey.indexOf('async function input('),journey.indexOf('const ui='));
const current=structuredClone(tiny);let sent=0;const snapshots=[];
const c={current,actions:0,setupActions:0,phase:'T06',limits,ledger:[],guard:()=>{},reserveInput:r.reserveInput,ready:false,credential:{email:'synthetic@example.invalid',password:'unmatched-synthetic-password'},boundedEntry:r.entry,persist:()=>{r.casePrewrite(current);snapshots.push(structuredClone(current));},page:{keyboard:{press:async()=>{sent++;throw Error('x'.repeat(6000));}}}};
vm.createContext(c);vm.runInContext(input,c);let inputError;try{await c.input('Tab traversal',null,'key','Tab');}catch(e){inputError=e;}
check('actual input emitted once before failure',sent===1&&c.actions===1&&current.actions===1&&snapshots[0].ledger[0].status==='started');
check('input ledger bounded6000 reason persists',current.ledger[0].reason.length===6000&&r.bytes(current.ledger[0])<=6144&&snapshots.at(-1).ledger[0].status==='failed');
applyCase(current,inputError);check('case duplicates input error outside bounded entry',current.reason===current.ledger[0].reason&&r.bytes(current.reason)>2048);
const ioDir=here+'/temporary-io';fs.mkdirSync(ioDir,{recursive:true});process.env.CAPTURE_ROOT=ioDir;
let physical={};
try{const io=await import('../ui-parity-tooltip-segment-keyboard-revised/harness/io.mjs');
  const prefix=structuredClone(tiny);prefix.padding='';prefix.padding='x'.repeat(88448-r.bytes(prefix));io.json('T06',prefix);const prior=fs.readFileSync(ioDir+'/T06.json');
  const error=throws('actual writer rejects overlimit merged record',()=>io.json('T06',merged),/Case JSON bound/);
  check('physical preceding file is unchanged at rejected write',fs.readFileSync(ioDir+'/T06.json').equals(prior));
  applyOuter(merged,error,()=>io.json('T06',merged));const final=read(ioDir+'/T06.json');
  check('outer catch can subsequently replace prefix with bounded failure',final.status==='unresolved'&&final.reason==='Case JSON bound'&&final.events[0]===tail.events[0]&&r.bytes(final)<limits.caseBytes);
  physical={beforeRejectedWrite:prior.length,rejectedCompletedBytes:132270,afterOuterCatchBytes:r.bytes(final),outerReason:final.reason,limit:'Synthetic padded case and API-admissible tail; no browser reachability claim'};
}finally{fs.unlinkSync(ioDir+'/T06.json');fs.rmdirSync(ioDir);}
const report=fs.readFileSync(source+'/report.md','utf8');for(const match of report.matchAll(/\[[^\]]*\]\(([^)]+)\)/g))check('report link '+match[1],fs.existsSync(path.resolve(source,match[1].split('#')[0])));
for(const item of [...manifest.inputs,...manifest.outputs,...list.files])check('original remains frozen '+item.sourcePath,sha(root+'/'+item.sourcePath)===item.sha256);
const result={date:'2026-10-17',verdict:'APPROVED',scope:'Analysis and exact publication only; no smaller reserve selected or implementation/runtime approved',pins,command:'node artifacts/ui-parity-tooltip-reservation-review/audit.mjs',exitCode:0,checks:checks.length,runtimeExecuted:false,
  calculator:{exitCode:0,checks:27,receiptWrite:'suppressed only after exact-byte equality'},freezeChecker:{exitCode:0,checks:38},
  independent:{candidate,guard:115072,hardCeiling:131072,boundaryBytes:before,afterReasonBytes:afterReason,afterTailBytes:132270,physical},
  smallestPrerequisite:'One enforced serialized failure-metadata policy covering both case and outer catch, followed by exact finite interval/scaffold derivation with terminal-write counterexamples; no reserve change yet',
  publication:{contentFiles:5,metadataFiles:1,destinationHashLinkAudit:'required after copy'},results:checks};
fs.writeFileSync(here+'/verification.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,results:undefined}));
