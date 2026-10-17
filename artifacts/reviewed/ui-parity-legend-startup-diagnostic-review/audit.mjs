import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';

const source='artifacts/ui-parity-legend-startup-diagnostic';
const own='artifacts/ui-parity-legend-startup-diagnostic-review';
const hash=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const entry=sourcePath=>({sourcePath,sha256:hash(sourcePath),bytes:fs.statSync(sourcePath).size});
const pins={
  'harness-manifest.json':'29096d4612637299972e068e4b4d76dbe1331051e1dce7f885258cb3bc79fe3b',
  'source-hashes.json':'95128fc21fd7f16d230e5e7488ee32972822c00134cd045b689ff9e4ba1a4a7b',
  'publication-allowlist.json':'524d43265b94dd6e5f95fffbe96aa319b2dab2e52e100bcf67254bf1527ce298'
};
for(const [name,pin] of Object.entries(pins))assert.equal(hash(source+'/'+name),pin);
const manifest=JSON.parse(fs.readFileSync(source+'/harness-manifest.json'));
const hashes=JSON.parse(fs.readFileSync(source+'/source-hashes.json'));
const allowlist=JSON.parse(fs.readFileSync(source+'/publication-allowlist.json'));
const before=[...allowlist,entry(source+'/publication-allowlist.json'),...hashes.sourceInputs];
function verify(entries){for(const e of entries){assert.equal(hash(e.sourcePath),e.sha256,e.sourcePath);assert.equal(fs.statSync(e.sourcePath).size,e.bytes,e.sourcePath);}}
verify(before);
verify(hashes.sourceFiles.map(f=>({...f,sourcePath:source+'/'+f.path})));
verify(manifest.files.map(f=>({...f,sourcePath:source+'/'+f.path})));
assert.equal(manifest.files.length,7);
assert.equal(new Set(allowlist.map(e=>e.sourcePath)).size,15);
for(const f of allowlist){
  assert(f.sourcePath.startsWith(source+'/')&&!f.sourcePath.includes('..'));
  assert(!fs.lstatSync(f.sourcePath).isSymbolicLink());
  const text=fs.readFileSync(f.sourcePath,'utf8');
  assert(!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:ghp_|github_pat_)[A-Za-z0-9_]{25,}|AKIA[A-Z0-9]{16}/.test(text));
  if(f.sourcePath.endsWith('.md'))for(const m of text.matchAll(/\]\(([^)]+)\)/g))assert(fs.existsSync(path.resolve(path.dirname(f.sourcePath),m[1].split('#')[0])));
}

// Run the original test assertions with only their output destinations relocated.
// The guarded main functions are imported, never invoked; all Docker/HTTP adapters are fake.
let testSource=fs.readFileSync(source+'/verify-offline.mjs','utf8');
for(const file of ['projection','probe','cleanup','io'])testSource=testSource.replace("'./harness/"+file+".mjs'",JSON.stringify(pathToFileURL(path.resolve(source+'/harness/'+file+'.mjs')).href));
testSource=testSource.replace('path.dirname(fileURLToPath(import.meta.url))',JSON.stringify(path.resolve(source)));
testSource=testSource.replace('os.tmpdir()',JSON.stringify(path.resolve(own)));
testSource=testSource.replace("fs.writeFileSync(base+'/offline-verification.json',JSON.stringify(report,null,2));console.log(JSON.stringify({status:'passed',tests:results.length,syntaxFiles:syntax.length}));",'globalThis.__diagnosticReviewOffline=report;');
assert(!testSource.includes("fs.writeFileSync(base+'/offline-verification.json'"));
await import('data:text/javascript;base64,'+Buffer.from(testSource).toString('base64'));
const offline=globalThis.__diagnosticReviewOffline;
assert.equal(offline.tests,21);assert.equal(offline.syntax.length,8);

const {diagnose,ownerLabel,projectContainer,classify}=await import(pathToFileURL(path.resolve(source+'/harness/projection.mjs')));
const {healthOnce}=await import(pathToFileURL(path.resolve(source+'/harness/probe.mjs')));
const {cleanupOwned}=await import(pathToFileURL(path.resolve(source+'/harness/cleanup.mjs')));
const independent=[];
function fixture(){
  const expected={name:'qopenbb-legend-probe-0123456789',networkName:'qopenbb-legend-probe-0123456789-net',ownership:'a'.repeat(24),container:'b'.repeat(64),networkId:'c'.repeat(64),statePath:path.resolve(own,'state-0123456789ab')};
  return {expected,network:{Id:expected.networkId,Name:expected.networkName,Labels:{[ownerLabel]:expected.ownership},Driver:'bridge',Internal:true,EnableIPv6:false},container:{Id:expected.container,Config:{Labels:{[ownerLabel]:expected.ownership}},NetworkSettings:{Ports:{'3000/tcp':[{HostIp:'127.0.0.1',HostPort:'12345'}]},Networks:{[expected.networkName]:{NetworkID:expected.networkId}}},HostConfig:{PortBindings:{'3000/tcp':[{HostIp:'127.0.0.1',HostPort:''}]}},State:{Status:'running',Running:true,Restarting:false,Dead:false,ExitCode:0,OOMKilled:false,StartedAt:'2026-10-17T00:00:00Z',FinishedAt:''}}};
}
for(let status=300;status<400;status++){
  let calls=0;
  const r=await healthOnce('12345',{request:async()=>{calls++;return {status,headers:{has:()=>false},body:{cancel:async()=>{}}};}});
  assert.equal(calls,1);assert.equal(r.reason,'redirect-rejected');
}
independent.push({name:'Every HTTP 3xx rejects with one fake request',cases:100,status:'passed'});
for(const status of [200,204,400,500]){
  const r=await healthOnce('12345',{request:async()=>({status,headers:{has:()=>true},body:{cancel:async()=>{}}})});assert.equal(r.reason,'redirect-rejected');
}
independent.push({name:'Location rejects success and error statuses',cases:4,status:'passed'});
let calls=0;assert.equal((await healthOnce('12345',{remaining:()=>0,request:async()=>{calls++;}})).reason,'input-deadline');assert.equal(calls,0);
assert.equal((await healthOnce('12345',{request:async()=>{calls++;throw Error('PRIVATE-SENTINEL');}})).reason,'health-transport-or-timeout');assert.equal(calls,1);
independent.push({name:'Expired health makes no request; transport failure makes one',cases:2,status:'passed'});
for(const mode of ['wrong-instance','wrong-owner','broad-binding','malformed-target']){
  const first=fixture();first.container.NetworkSettings.Ports['3000/tcp']=null;const second=fixture();
  if(mode==='wrong-instance')second.container.Id='foreign';
  if(mode==='wrong-owner')second.network.Labels[ownerLabel]='foreign';
  if(mode==='broad-binding')second.container.NetworkSettings.Ports['3000/tcp'][0].HostIp='0.0.0.0';
  if(mode==='malformed-target')second.container.NetworkSettings.Ports['3000/tcp']={private:'PRIVATE-SENTINEL'};
  let time=0,reads=0,health=0;const saved=[];
  const r=await diagnose({inspect:async()=>[first,second][reads++],persist:async x=>saved.push(x),health:async()=>{health++;},now:()=>time,pause:async ms=>{time+=ms;},runReturnedAt:0,deadline:90000});
  assert.equal(reads,2);assert.equal(saved.length,2);assert.equal(health,0);assert.equal(r.outcome,mode==='malformed-target'?'projection-unresolved':'security-unresolved');assert(!JSON.stringify(saved).includes('PRIVATE-SENTINEL'));
}
independent.push({name:'Later security/shape failure persists operands and stops before health or third sample',cases:4,status:'passed'});
const f=fixture();f.expected.container=null;f.expected.networkId=null;let container=true,network=true;const mutations=[];
const proof=await cleanupOwned(f.expected,{directory:own,docker:(...args)=>{
  if(args[0]==='ps')return container?'b'.repeat(64):'';
  if(args[0]==='inspect')return JSON.stringify([{Id:'b'.repeat(64),Name:'/'+f.expected.name,Config:{Labels:{[ownerLabel]:f.expected.ownership}}}]);
  if(args[0]==='rm'){container=false;mutations.push('container');return '';}
  if(args[1]==='ls')return network?'c'.repeat(64)+' '+f.expected.networkName:'';
  if(args[1]==='inspect')return JSON.stringify([{Id:'c'.repeat(64),Name:f.expected.networkName,Labels:{[ownerLabel]:f.expected.ownership},Containers:{}}]);
  if(args[1]==='rm'){network=false;mutations.push('network');return '';}
  throw Error('unexpected fake command');
},remove:()=>{},exists:()=>false});
assert.deepEqual(mutations,['container','network']);assert.equal(proof.containerAbsent&&proof.networkAbsent&&proof.stateAbsent&&proof.credentialAbsent,true);
independent.push({name:'Interrupted creation ID-save uses exact random name/ownership and inspected ID cleanup',cases:1,status:'passed'});
for(const name of ['supervise.sh','harness/run.sh'])assert(!fs.readFileSync(source+'/'+name).includes(13));
verify(before);
const receipt={status:'passed',scope:'Independent source/offline review only; no Docker, network, browser, container, build, install, preparation or frozen write',node:process.version,pins,sourceEntries:allowlist.length,inputEntries:hashes.sourceInputs.length,runtimeFiles:manifest.files.length,offline,independent,frozenPreserved:true,shellLineEndings:'LF',sourcePublication:'15 selected files approved; allowlist metadata separately',productionCaps:'Research excluded; future production 400 physical/file, 300 logical/file, 50/function'};
fs.writeFileSync(own+'/verification.json',JSON.stringify(receipt,null,2)+'\n');
fs.copyFileSync(source+'/publication-allowlist.json',own+'/reviewed-source-publication-allowlist.json');
console.log(JSON.stringify({status:'passed',offlineTests:offline.tests,syntax:offline.syntax.length,independentCases:independent.reduce((n,x)=>n+x.cases,0),frozenPreserved:true}));
