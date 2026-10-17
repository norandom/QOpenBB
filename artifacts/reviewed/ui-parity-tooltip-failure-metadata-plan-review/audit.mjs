import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {casePrewrite,retention,bytes} from '../ui-parity-tooltip-segment-keyboard-revised/harness/keyboard-retention.mjs';
import {limits} from '../ui-parity-tooltip-segment-keyboard-revised/harness/contract.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../..'),proposal=root+'/artifacts/ui-parity-tooltip-failure-metadata-plan';
const read=p=>JSON.parse(fs.readFileSync(p)),sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),checks=[];
function check(name,value){checks.push({name,passed:!!value});if(!value)throw Error(name);}
const pins={'plan.md':'b3856296d8b97244f2baf0f15efb844cf4d79a824078682069e3d6cf1da92edd','source-hashes.json':'7310b2f88334df1d06cff18bd390adfedfc4e6ea888a7423629003ad85c36c02','publication-allowlist.json':'5bf17c132b780a4c8119551c03de78226fddb25c608adcaea2748e13dde13976'};
for(const [name,hash] of Object.entries(pins))check('frozen proposal pin '+name,sha(proposal+'/'+name)===hash);
const manifest=read(proposal+'/source-hashes.json'),list=read(proposal+'/publication-allowlist.json'),supplied=read(proposal+'/verification.json');
for(const item of [...manifest.inputs,...list])check('actual hash/bytes '+item.sourcePath,sha(root+'/'+item.sourcePath)===item.sha256&&fs.statSync(root+'/'+item.sourcePath).size===item.bytes);
check('three selected unique files',list.length===3&&new Set(list.map(x=>x.sourcePath)).size===3);
for(const item of list){check('safe owned text '+item.sourcePath,item.sourcePath.startsWith('artifacts/ui-parity-tooltip-failure-metadata-plan/')&&!item.sourcePath.includes('..')&&/\.(md|json)$/.test(item.sourcePath));
  check('no concrete private key/token/placeholder '+item.sourcePath,!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_-]{20,}|\b(?:TBD|TODO|FIXME|HACK|XXX)\b/.test(fs.readFileSync(root+'/'+item.sourcePath,'utf8')));}
check('512metadatacap proposed only',supplied.proposedFailureMetadataBytes===512&&!supplied.implementationExecuted&&!supplied.scaffoldProofCompleted&&!supplied.reservationReduced&&!supplied.runtimeExecuted);
for(const shape of supplied.fixedFallbackShapes)check('fixed fallback fits '+shape.value.failureOrigin+'/'+shape.value.reasonCode,bytes(shape.value)===shape.bytes&&bytes(shape.value)<=512);
for(const origin of ['case','outer']){const metadata={reason:'',reasonCode:'exception',reasonOmitted:false,failureOrigin:origin},emptyBytes=bytes(metadata);
  metadata.reason='x'.repeat(512-emptyBytes);check('complete metadata can equal512 '+origin,bytes(metadata)===512);metadata.reason+='x';check('one ASCII character exceeds cap '+origin,bytes(metadata)===513);
  metadata.reason='\u0000'.repeat(72);check('escapes require serialized-byte cap '+origin,metadata.reason.length<512&&bytes(metadata)>512);}
check('existing reserve and limits unchanged',retention.inputReserve===32768&&retention.caseGuard===115072&&retention.tailReserve===16000&&limits.caseBytes===131072);
const writer=fs.readFileSync(root+'/artifacts/ui-parity-tooltip-segment-keyboard-revised/harness/io.mjs','utf8');
const ioBody=writer.replace(/^import .*;\r?\n/gm,'').replaceAll('export ','').replace('const root=process.env.CAPTURE_ROOT;',"const root='/owned';");
const original=Buffer.from(JSON.stringify({id:'T06',ledger:[],keyboard:[],actions:1,status:'started'}));let stored=Buffer.from(original),writeCalls=0;
const mockFs={readdirSync:()=>['T06.json'],statSync:()=>({size:stored.length,isFile:()=>true}),existsSync:()=>true,
  writeFileSync:(_file,value)=>{writeCalls++;stored=Buffer.from(value).subarray(0,13);throw Error('injected ordinary write failure');}};
const context={fs:mockFs,limits,casePrewrite,Buffer};vm.createContext(context);vm.runInContext(ioBody,context);
let rejection;try{context.json('T06',{id:'T06',ledger:[],keyboard:[],actions:2,status:'unresolved'});}catch(e){rejection=e.message;}
check('F01 actual writer reached writeFileSync before injected failure',writeCalls===1&&rejection==='injected ordinary write failure');
check('F01 preceding bytes no longer established',!stored.equals(original)&&stored.length===13);
check('F01 three proposed outcomes are insufficient',rejection!==undefined&&writeCalls===1&&!stored.equals(original));
const text=fs.readFileSync(proposal+'/plan.md','utf8');
check('F01 proposal explicitly only three outcomes',text.includes('This finite three-value field')&&text.includes('caseWrite: rejected-prior-prefix'));
check('F02 receipt description carries outer only',text.includes('The separate existing failure receipt uses that same bounded outer metadata')&&text.includes('If a case already has case-origin metadata, preserve it'));
const first={reason:'Observation failed',reasonCode:'exception',reasonOmitted:false,failureOrigin:'case'},outer={reason:'Case JSON bound',reasonCode:'exception',reasonOmitted:false,failureOrigin:'outer'};
const attempted={...JSON.parse(original),...first,outerFailure:outer},prior=JSON.parse(original),receipt={phase:'T06',caseId:'T06',...outer,caseWrite:'rejected-prior-prefix',completedCases:[]};
check('F02 rejection outcome leaves first failure in attempted object only',attempted.reason===first.reason&&!Object.hasOwn(prior,'reason')&&!JSON.stringify(receipt).includes(first.reason));
check('F02 two bounded metadata objects are finite without history',bytes(first)<=512&&bytes(outer)<=512);
const links=[];for(const match of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){const target=match[1].split('#')[0];check('plan link '+target,fs.existsSync(path.resolve(proposal,target)));links.push(target);}
for(const item of [...manifest.inputs,...list])check('original preserved '+item.sourcePath,sha(root+'/'+item.sourcePath)===item.sha256);
const result={date:'2026-10-17',verdict:'REJECTED',scope:'Source-plan review; two narrow terminal-evidence corrections required; no implementation/runtime grant',pins,command:'node artifacts/ui-parity-tooltip-failure-metadata-plan-review/audit.mjs',exitCode:0,checks:checks.length,runtimeExecuted:false,
  findings:[{id:'F01',severity:'Important',contract:'Three-value caseWrite omits attempted-write failure with unverified prior prefix',evidence:'Actual unchanged writer executed only in VM with injected filesystem failure after a partial write; no real file damaged'},{id:'F02',severity:'Important',contract:'First case failure survives only in memory if case writes reject; standalone receipt specifies outer metadata only',evidence:'Plan-defined schema counterexample; proposed policy is not implemented'}],
  fixedFallbackBytes:supplied.fixedFallbackShapes.map(x=>x.bytes),publication:{contentFiles:3,metadataFiles:1,links,approvedScope:'Safe publication as rejected source proposal accompanied by this review',destinationAudit:'required after synchronization'},results:checks};
fs.writeFileSync(here+'/verification.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,results:undefined}));
