import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {failureMetadata} from './harness/failure-metadata.mjs';
import * as r from './harness/keyboard-retention.mjs';
import {limits,cases} from './harness/contract.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const checks=[],measurements=[];
const clone=v=>structuredClone(v),same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const hash=v=>createHash('sha256').update(v).digest('hex');
function check(name,ok){checks.push({name,passed:!!ok});if(!ok)throw Error(name);}
const credential={email:'sample@example.invalid',password:'fixture-password'};
const format=(error,origin='case',creds=credential)=>failureMetadata(error,origin,creds);
const fields=value=>Object.fromEntries(['reason','reasonCode','reasonOmitted','failureOrigin'].map(k=>[k,value[k]]));
const journey=fs.readFileSync(here+'/harness/journey.mjs','utf8');
const caseAt=journey.indexOf('    }catch(e){',journey.indexOf('  for(const item of cases){'));
const caseCode=journey.slice(caseAt+5,journey.indexOf('    const events=',caseAt));
const outerAt=journey.indexOf('}catch(e){process.exitCode=1;');
const outerCode=journey.slice(outerAt+1,journey.indexOf('}finally{clearTimeout',outerAt)+1);
const closingCode=journey.slice(journey.indexOf('    const events=',caseAt),journey.indexOf('\n  }\n  json(\'summary\'',caseAt));
const inputCode=journey.slice(journey.indexOf('async function input('),journey.indexOf('const ui='));
const keyboardCode=journey.slice(journey.indexOf('async function keyboard('),journey.indexOf('function dashboard('));
const ioSource=fs.readFileSync(here+'/harness/io.mjs','utf8').replace(/^import .*;\r?\n/gm,'')
  .replace('export const root=process.env.CAPTURE_ROOT;','').replace("if(!root)throw Error('CAPTURE_ROOT required');",'').replaceAll('export ','');
function writer(directory,write=fs.writeFileSync){
  fs.mkdirSync(directory,{recursive:true});
  const c={fs:{...fs,writeFileSync:write},root:directory,limits,casePrewrite:r.casePrewrite,Buffer,Map};
  vm.createContext(c);vm.runInContext(ioSource+'\nthis.write=json;',c);return c.write;
}
function state(id='T06'){return {id,actions:0,ledger:[],probes:[],keyboard:[],status:'started'};}
function context(current=state(),json=()=>{}){
  const c={current,credential,failureMetadata,process:{exitCode:0},preflight:{status:'setup-pending'},phase:current?.id??'setup',results:[],json,
    item:cases.find(v=>v.id===current?.id)??cases[5],Buffer,JSON};
  c.persist=()=>c.current?c.json(c.current.id,c.current):c.json('identity-fixture-preflight',c.preflight);
  vm.createContext(c);return c;
}
function caseCatch(c,error){c.injected=error;vm.runInContext('try{throw injected;}'+caseCode,c);}
function outerCatch(c,error){c.injected=error;vm.runInContext('try{throw injected;}'+outerCode,c);}
async function close(c,events=[],fault=null){
  c.page={evaluate:async()=>{if(fault)throw fault;return events;}};c.finalTail=r.finalTail;c.Date={now:()=>1};c.current.began??=0;
  await vm.runInContext('(async()=>{'+closingCode+'})()',c);
}

const fixed=format(Error(''));
check('exact four metadata fields',same(Object.keys(fixed),['reason','reasonCode','reasonOmitted','failureOrigin']));
const prefix=r.bytes(format(Error(''))),capacity=512-prefix;
for(const origin of ['case','outer'])for(const omitted of [format({message:7},origin),format(Error('x'.repeat(1000)),origin)]){
  check('fixed fallback satisfies whole object cap '+origin+' '+omitted.reasonCode,r.bytes(omitted)<=512&&omitted.reasonOmitted&&omitted.failureOrigin===origin);
}
for(const delta of [-1,0,1]){
  const message='x'.repeat(capacity+delta),out=format(Error(message));
  check('whole object ASCII boundary '+delta,delta<=0?out.reason===message&&!out.reasonOmitted&&r.bytes(out)===512+delta:out.reasonOmitted&&out.reasonCode==='message-over-byte-cap');
}
for(const unit of ['"','\\','\n','\u0000','漢','😀','\ud800'])for(const delta of [-1,0,1]){
  const base=unit.repeat(Math.floor(capacity/JSON.stringify(unit).slice(1,-1).length/4));
  const room=512-r.bytes(format(Error(base))),message=base+'x'.repeat(room+delta),out=format(Error(message));
  check('serialized special-text boundary '+unit.charCodeAt(0)+' '+delta,delta<=0?out.reason===message&&!out.reasonOmitted&&r.bytes(out)===512+delta:out.reasonOmitted&&out.reasonCode==='message-over-byte-cap');
}
for(const message of ['"\\/\n\u0000'.repeat(14),'€漢😀'.repeat(10),'\ud800','', 'a\nb\nc']){
  const out=format(Error(message));check('complete escaped or multibyte message '+measurements.length,out.reason===message&&!out.reasonOmitted&&r.bytes(out)<=512);
  measurements.push({kind:'serialization',inputCodeUnits:message.length,serializedBytes:r.bytes(out)});
}
for(const message of ['\u0000'.repeat(7000),'漢'.repeat(400),'x'.repeat(27624),'x'.repeat(40000)]){
  const out=format(Error(message));check('oversized full object omitted '+message.length,out.reasonCode==='message-over-byte-cap'&&out.reasonOmitted&&r.bytes(out)<=512);
}
let accesses=0;
const throwing={get message(){accesses++;throw Error('getter');}};
check('throwing getter extracted exactly once',format(throwing).reasonCode==='message-unavailable'&&accesses===1);
let successfulAccesses=0;check('successful getter read once',format({get message(){successfulAccesses++;return 'one read';}}).reason==='one read'&&successfulAccesses===1);
let coerced=0;format({message:{toString(){coerced++;return 'must not convert';}}});check('nonstring message never coerced',coerced===0);
for(const thrown of [null,undefined,{}, {message:7},{message:{toString(){throw Error('must not call');}}}]){
  check('nonstring unavailable '+checks.length,format(thrown).reasonCode==='message-unavailable');
}
const exact=format(Error('not-run-budget'),'case',{email:'not-run-budget',password:''});
check('exact sentinel classified before redaction',exact.reasonCode==='not-run-budget'&&exact.reason==='[redacted]'&&!exact.reasonOmitted);
check('near sentinel stays exception',format(Error('not-run-budget\n')).reasonCode==='exception');
check('nonempty credentials redacted completely',format(Error(credential.email+'\n'+credential.password)).reason==='[redacted]\n[redacted]');
check('empty credentials do not change message',format(Error('abc'),'outer',{email:'',password:''}).reason==='abc');
check('redaction failure unavailable',format(Error('abc'),'case',{get email(){throw Error('redaction');}}).reasonCode==='message-unavailable');

const sensitive={identity:{id:'observation-1'},tooltip:{value:'EUR 123.45',missing:null},financial:{cashFlow:-10,revenue:0}};
for(const item of cases){
  const c=context({...state(item.id),...clone(sensitive)}),before=JSON.stringify(sensitive);c.item=item;
  caseCatch(c,Error('x'.repeat(27624)));
  check('case bounded and data unchanged '+item.id,r.bytes(fields(c.current))<=512&&c.current.reasonOmitted&&JSON.stringify(Object.fromEntries(Object.keys(sensitive).map(k=>[k,c.current[k]])))===before);
  check('fixed remaining reasons and original targets '+item.id,same(c.current.remainingProbes.map(v=>v.target),item.probes??[])&&c.current.remainingProbes.every(v=>v.reason==='Affected case closed; see case reason'));
}
const sentinel=context();caseCatch(sentinel,Error('not-run-budget'));
check('case exact sentinel preserves status',sentinel.current.status==='not-run-budget'&&sentinel.current.remainingModes.length===3);
const getterCatch=context();caseCatch(getterCatch,throwing);
check('case does not reaccess throwing getter',getterCatch.current.reasonCode==='message-unavailable'&&accesses===2);

const temp=here+'/.offline-temp';fs.mkdirSync(temp,{recursive:true});
const evidence=[];
function snapshot(directory,name='T06'){const file=directory+'/'+name+'.json';return fs.existsSync(file)?{bytes:fs.statSync(file).size,sha256:hash(fs.readFileSync(file))}:null;}
function output(directory,name='T06'){return JSON.parse(fs.readFileSync(directory+'/'+name+'.json'));}
function runDirectory(label){const p=temp+'/'+label;fs.mkdirSync(p,{recursive:true});return p;}
try{
  const dir=runDirectory('successful-close'),json=writer(dir),c=context({...state(),...clone(sensitive)},json);
  json('T06',c.current);const prior=snapshot(dir);caseCatch(c,Error('first\ncomplete'));
  const first=fields(c.current);outerCatch(c,Error('x'.repeat(40000)));
  const receipt=output(dir,'failure'),actual=output(dir);
  check('successful case retry preserves first and bounded outer',same(fields(actual),first)&&actual.outerFailure.reasonCode==='message-over-byte-cap'&&same(receipt.firstCaseFailure,first)&&receipt.caseWrite==='succeeded');
  check('successful retry keeps data unchanged',same(actual.identity,sensitive.identity)&&same(actual.tooltip,sensitive.tooltip)&&same(actual.financial,sensitive.financial));
  evidence.push({kind:'normal-return',prior,final:snapshot(dir),failure:snapshot(dir,'failure'),caseWrite:receipt.caseWrite});

  const rejectedDir=runDirectory('prewrite-rejected'),rejectedJson=writer(rejectedDir),rejected=context(state(),rejectedJson);
  rejectedJson('T06',rejected.current);const prefix=snapshot(rejectedDir);
  rejected.current.ledger.push({id:'T06.a001',status:'failed',reason:'\u0000'.repeat(7000)});rejected.current.actions=1;
  caseCatch(rejected,Error('first exists only in memory'));const firstMemory=fields(rejected.current);
  outerCatch(rejected,Error('Case JSON bound'));
  const rejectedReceipt=output(rejectedDir,'failure');
  check('actual invalid ledger prewrite rejects and physical prefix preserved',same(prefix,snapshot(rejectedDir))&&output(rejectedDir).actions===0&&rejected.current.actions===1&&rejected.current.ledger[0].reason.length===7000);
  check('unclassified rejection uses unverified despite bound-like text',rejectedReceipt.caseWrite==='write-unverified');
  check('memory-only first failure retained in standalone receipt',same(rejectedReceipt.firstCaseFailure,firstMemory)&&rejectedReceipt.failureOrigin==='outer'&&rejectedReceipt.reason==='Case JSON bound');
  evidence.push({kind:'observed-prewrite-rejection',prior:prefix,final:snapshot(rejectedDir),failure:snapshot(rejectedDir,'failure'),caseWrite:rejectedReceipt.caseWrite});

  const partialDir=runDirectory('partial-write');let partial=false,attempts=0;
  const partialJson=writer(partialDir,(file,bytes)=>{attempts++;if(partial&&file.endsWith('/T06.json')){fs.writeFileSync(file,bytes.subarray(0,37));throw Error('Case JSON bound');}fs.writeFileSync(file,bytes);});
  const partialCase=context(state(),partialJson);partialJson('T06',partialCase.current);const beforePartial=snapshot(partialDir);
  caseCatch(partialCase,Error('original failure'));partial=true;outerCatch(partialCase,Error('closing failure'));
  check('actual partial write is unverified with changed physical bytes',output(partialDir,'failure').caseWrite==='write-unverified'&&snapshot(partialDir).bytes===37&&snapshot(partialDir).sha256!==beforePartial.sha256);
  check('partial case write attempts one closing write and one receipt',attempts===3);
  evidence.push({kind:'partial-write-then-throw',prior:beforePartial,final:snapshot(partialDir),failure:snapshot(partialDir,'failure'),caseWrite:output(partialDir,'failure').caseWrite});

  const failedDir=runDirectory('receipt-failure');let calls=0;
  const failedJson=writer(failedDir,(file,bytes)=>{calls++;fs.writeFileSync(file,bytes.subarray(0,19));throw Error('filesystem failure');});
  const failedCase=context(state(),failedJson);caseCatch(failedCase,Error('first'));outerCatch(failedCase,Error('outer'));
  check('failed standalone write has no recursive retry',calls===2&&snapshot(failedDir,'failure').bytes===19&&failedCase.process.exitCode===1);
  evidence.push({kind:'receipt-partial-failure',final:snapshot(failedDir),failure:snapshot(failedDir,'failure'),persistenceClaim:false,attempts:calls});

  const setupDir=runDirectory('setup'),setup=context(null,writer(setupDir));outerCatch(setup,throwing);
  const setupReceipt=output(setupDir,'failure');
  check('preflight outer metadata and no case write',setupReceipt.caseWrite==='not-attempted'&&!Object.hasOwn(setupReceipt,'firstCaseFailure')&&setup.preflight.failureOrigin==='outer'&&setupReceipt.reasonCode==='message-unavailable');

  const tailDir=runDirectory('legal-tail'),tailCase=context(state(),writer(tailDir));
  const tail={events:[''],elapsedMs:1};tail.events[0]='x'.repeat(16000-r.bytes(tail));r.finalTail(tail.events,tail.elapsedMs);
  caseCatch(tailCase,Error('x'.repeat(27624)));const beforeTail=r.bytes(tailCase.current);await close(tailCase,tail.events);
  const tailRecord=output(tailDir);
  check('legal exact maximum tail retained in completed case',r.bytes(tail)===16000&&same(tailRecord.events,tail.events)&&tailCase.results.length===1&&tailCase.current===null&&tailRecord.reasonOmitted);
  measurements.push({kind:'legal-tail',tailBytes:r.bytes(tail),preTailBytes:beforeTail,finalBytes:r.bytes(tailRecord)});

  const overDir=runDirectory('oversized-complete'),over=context(state(),writer(overDir));
  over.json('T06',over.current);const overPrior=snapshot(overDir);caseCatch(over,Error('bounded first failure'));
  over.current.padding='';over.current.padding='x'.repeat(115200-r.bytes(over.current));let overError;
  try{await close(over,tail.events);}catch(e){overError=e;outerCatch(over,e);}
  check('actual closing path rejects oversized complete case',overError?.message==='Case JSON bound'&&r.bytes(over.current)>limits.caseBytes&&over.results.length===0&&same(overPrior,snapshot(overDir)));
  check('oversized in-memory case retains legal tail and standalone first failure',same(over.current.events,tail.events)&&output(overDir,'failure').caseWrite==='write-unverified'&&output(overDir,'failure').firstCaseFailure.reason==='bounded first failure');
  evidence.push({kind:'synthetic-padded-complete-rejection',prior:overPrior,final:snapshot(overDir),attemptedBytes:r.bytes(over.current),failure:snapshot(overDir,'failure'),caseWrite:output(overDir,'failure').caseWrite});

  const recoveryDir=runDirectory('final-write-recovery');let failNext=false,intermediate;
  const recoveryJson=writer(recoveryDir,(file,bytes)=>{if(failNext&&file.endsWith('/T06.json')){failNext=false;fs.writeFileSync(file,bytes.subarray(0,41));intermediate=snapshot(recoveryDir);throw Error('final persistence');}fs.writeFileSync(file,bytes);});
  const recovery=context(state(),recoveryJson);recoveryJson('T06',recovery.current);const recoveryPrior=snapshot(recoveryDir);
  caseCatch(recovery,Error('first before final write'));failNext=true;let recoveryError;
  try{await close(recovery,tail.events);}catch(e){recoveryError=e;outerCatch(recovery,e);}
  const recoveryFinal=output(recoveryDir);
  check('actual final persistence partial failure followed by successful closing write',recoveryError?.message==='final persistence'&&intermediate.bytes===41&&output(recoveryDir,'failure').caseWrite==='succeeded'&&recoveryFinal.reason==='first before final write'&&recoveryFinal.outerFailure.reason==='final persistence'&&same(recoveryFinal.events,tail.events)&&recovery.results.length===0);
  check('prior intermediate and final bytes are distinct',recoveryPrior.sha256!==intermediate.sha256&&snapshot(recoveryDir).sha256!==intermediate.sha256&&snapshot(recoveryDir).sha256!==recoveryPrior.sha256);
  evidence.push({kind:'actual-final-write-partial-then-recovery',prior:recoveryPrior,intermediate,final:snapshot(recoveryDir),failure:snapshot(recoveryDir,'failure'),caseWrite:output(recoveryDir,'failure').caseWrite});

  const tailFaultDir=runDirectory('tail-failure'),tailFault=context(state(),writer(tailFaultDir));
  caseCatch(tailFault,Error('earlier'));let tailError;
  try{await close(tailFault,[],Error('tail collection'));}catch(e){tailError=e;outerCatch(tailFault,e);}
  check('actual tail collection failure retains earlier case reason',tailError.message==='tail collection'&&output(tailFaultDir).reason==='earlier'&&output(tailFaultDir).outerFailure.reason==='tail collection'&&tailFault.results.length===0);

  const raw={active:null,tooltip:{visible:false},liveStatus:'',area:null,swapchain:[]};
  function inputs(label,fault){
    const inputDir=runDirectory(label),c=context({...state(),modes:['Single'],tabCap:1,sequence:[]},writer(inputDir));
    let sent=0,domReads=0;
    Object.assign(c,{phase:'T06',actions:0,setupActions:0,probes:0,ledger:[],ready:true,limits,guard:()=>{},reserveInput:r.reserveInput,
      sample:r.sample,modeSample:r.modeSample,settlement:r.settlement,invocation:r.invocation,boundedEntry:r.entry,dom:function dom(){},Date:{now:()=>1}});
    c.page={evaluate:async fn=>fn===c.dom?clone(fault==='baseline'&&++domReads>1?{...raw,liveStatus:'\u0000'.repeat(2048)}:raw):0,
      keyboard:{press:async()=>{sent++;if(fault==='input6000')throw Error('x'.repeat(6000));if(fault==='input7000')throw Error('\u0000'.repeat(7000));}}};
    c.ui=()=>({mode:async()=>{},close:async()=>{}});
    c.observe=async()=>{if(fault==='observation')throw Error('x'.repeat(40000));return {status:'stable',pair:[clone(raw),clone(raw)],sampleCount:2,elapsedMs:1};};
    c.screenshot=async()=>{if(fault==='screenshot')throw Error('screenshot failed');return 'synthetic.png';};
    vm.runInContext(inputCode+'\n'+keyboardCode,c);return {c,dir:inputDir,sent:()=>sent};
  }
  for(const fault of ['input6000','input7000','observation','baseline','screenshot']){
    const m=inputs(fault,fault);let error;try{await m.c.keyboard();}catch(e){error=e;}
    check('actual keyboard injected fault '+fault,!!error);
    const prior=snapshot(m.dir),actions=m.c.actions,probes=m.c.probes,ledger=JSON.stringify(m.c.current.ledger);
    caseCatch(m.c,error);outerCatch(m.c,Error('second closing error'));
    const receipt=output(m.dir,'failure');
    check('counted inputs and ledger preserved '+fault,m.c.actions===actions&&m.c.probes===probes&&JSON.stringify(m.c.current.ledger)===ledger&&m.c.current.actions===m.sent());
    check('actual catch bounded failure '+fault,r.bytes(fields(m.c.current))<=512&&r.bytes(m.c.current.outerFailure)<=512&&same(receipt.firstCaseFailure,fields(m.c.current)));
    if(fault==='input6000')check('6000 input full reason remains counted and failed',m.c.current.ledger[0].status==='failed'&&m.c.current.ledger[0].reason.length===6000&&receipt.caseWrite==='succeeded');
    if(fault==='input7000')check('invalid escaped input remains unresolved without legalizing entry',m.c.current.ledger[0].reason.length===7000&&receipt.caseWrite==='write-unverified'&&same(prior,snapshot(m.dir)));
    if(fault==='baseline')check('baseline assigned before sample failure retained',Object.hasOwn(m.c.current.keyboard[0],'baseline'));
    if(fault==='screenshot')check('screenshot error does not invent image',!Object.hasOwn(m.c.current.keyboard[0],'initialOrTerminalImage')&&m.c.current.keyboard[0].tabs.length===1);
    evidence.push({kind:'actual-keyboard-'+fault,prior,final:snapshot(m.dir),failure:snapshot(m.dir,'failure'),caseWrite:receipt.caseWrite,actions,probes});
  }
}finally{fs.rmSync(temp,{recursive:true,force:true});}

const report={date:'2026-10-17',command:'node artifacts/ui-parity-tooltip-failure-metadata-source/faults.mjs',exitCode:0,
  scope:'Offline actual extracted catches/input/keyboard/closing path and actual IO writer under mocks; no browser/runtime/network',checks,measurements,evidence,
  limits:{metadataBytes:512,inputReserve:r.retention.inputReserve,caseGuard:r.retention.caseGuard,tailReserve:r.retention.tailReserve,caseBytes:limits.caseBytes},
  limitations:['No finite scaffold proof or universal terminal fit','No runtime reachability claim for constructed faults','Input path and probe catch remain unchanged','Unclassified writer failures always write-unverified; physical prefix preservation is independently observed only']};
fs.writeFileSync(here+'/verification.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({passed:checks.length,evidenceCases:evidence.length}));
