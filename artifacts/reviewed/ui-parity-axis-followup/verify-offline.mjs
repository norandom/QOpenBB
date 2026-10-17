import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {spawnSync} from 'node:child_process';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash,randomBytes} from 'node:crypto';
import {createWriter,limits,increment} from './harness/io.mjs';
import {createEventStore} from './harness/events.mjs';
import {assertFinancialData,assertBaseline,assertLabelUI} from './harness/guards.mjs';
const base=path.dirname(fileURLToPath(import.meta.url)),temp=path.join(base,'offline-'+randomBytes(5).toString('hex'));
fs.mkdirSync(temp);const checks=[],benchmarks=[];
const pass=(name,fn)=>{fn();checks.push(name);};
const sub=name=>{const p=path.join(temp,name);fs.mkdirSync(p);return p;};
const digest=bytes=>createHash('sha256').update(bytes).digest('hex');
const sourceHash=f=>digest(fs.readFileSync(path.join(base,f)));
let cleanup=false;
try{
  const root=sub('equivalence');fs.mkdirSync(path.join(root,'dir'));fs.writeFileSync(path.join(root,'dir','existing.json'),'{}');
  fs.writeFileSync(path.join(root,'z.json'),'[]');fs.writeFileSync(path.join(root,'ignored-private.json'),'private');
  process.env.CAPTURE_ROOT=root;
  const old=await import(pathToFileURL(path.join(base,'frozen/harness/io.mjs')));
  const next=createWriter(root),payload={tag:'synthetic',number:315,undef:undefined,null:null,unicode:'£',values:[1,false,'x']};
  old.json('legacy',payload);const expected=fs.readFileSync(path.join(root,'legacy.json'));
  // New initial inventory deliberately occurs before the legacy write: unrelated writes must be detected.
  pass('extraneous additions fail final reconciliation',()=>assert.throws(()=>next.reconcile(),/Untracked/));
  const writer=createWriter(root);writer.json('legacy',payload);
  pass('JSON bytes unchanged and initial existing files counted',()=>{assert.deepEqual(fs.readFileSync(path.join(root,'legacy.json')),expected);assert.deepEqual(writer.budget(),old.budget());});
  writer.json('legacy',{x:1});writer.png('picture',Buffer.from([137,80,78,71]));writer.json('a',{x:2});
  pass('overwrite shrink and PNG bytes counted with original ordering',()=>assert.deepEqual(writer.reconcile(),old.budget()));
  pass('only one initial scan despite owned writes',()=>assert.equal(writer.stats().initialScans,1));
  pass('unchanged hard caps and counter boundaries',()=>{assert.deepEqual(limits,old.limits);assert.equal(increment(239,240,'a'),240);assert.throws(()=>increment(240,240,'a'),/cap/);});
  const capRoot=sub('caps'),cap=createWriter(capRoot,{caps:{...limits,files:2,total:8,json:8,png:4}});
  cap.writeBytes('a',Buffer.alloc(4));cap.writeBytes('b',Buffer.alloc(4));
  pass('prospective file/total bounds stop before disk mutation',()=>{assert.throws(()=>cap.writeBytes('c',Buffer.alloc(0)),/cap/);assert.throws(()=>cap.writeBytes('a',Buffer.alloc(5)),/cap/);assert.equal(fs.statSync(path.join(capRoot,'a')).size,4);});
  pass('individual JSON/PNG bounds retained',()=>{assert.throws(()=>cap.json('a','1234567'),/JSON byte/);assert.throws(()=>cap.png('x',Buffer.alloc(5)),/PNG byte/);});
  pass('path escape, exclusions and symlink writes rejected',()=>{
    for(const n of ['../escape','..','state-x/file','file-private.json','bad.log'])assert.throws(()=>writer.writeBytes(n,Buffer.alloc(1)),/Unowned/);
    fs.symlinkSync(path.join(root,'legacy.json'),path.join(root,'alias'));assert.throws(()=>writer.writeBytes('alias',Buffer.alloc(1)),/Symlink/);fs.unlinkSync(path.join(root,'alias'));
  });
  const failRoot=sub('failed'),disk=Object.create(fs);let mode='before';
  disk.writeFileSync=(file,bytes)=>{if(mode==='partial')fs.writeFileSync(file,bytes.subarray(0,2));if(mode)throw Error('injected write');fs.writeFileSync(file,bytes);};
  const failed=createWriter(failRoot,{disk});
  pass('failed new write creates no phantom inventory',()=>{assert.throws(()=>failed.json('x',{x:1}),/injected/);assert.equal(failed.reconcile().files,0);});
  mode=null;failed.writeBytes('x',Buffer.alloc(5));mode='partial';
  pass('partial failed overwrite refreshes actual retained bytes',()=>{assert.throws(()=>failed.writeBytes('x',Buffer.alloc(6)),/injected/);assert.equal(failed.reconcile().bytes,2);});
  const extRoot=sub('external'),external=createWriter(extRoot,{caps:{...limits,total:8,files:2,png:8}}),reservation=external.reservePNG('external',6);
  pass('external PNG reservations consume prospective budget',()=>{assert.throws(()=>external.writeBytes('other',Buffer.alloc(3)),/cap/);assert.throws(()=>external.reconcile(),/Unfinished/);});
  fs.writeFileSync(reservation.path,Buffer.alloc(5));reservation.finish();
  const missing=external.reservePNG('missing',3);missing.finish();
  pass('external PNG success and failed-before-write finalize safely',()=>{assert.equal(external.reconcile().bytes,5);assert.equal(external.stats().pending,0);});
  fs.writeFileSync(path.join(extRoot,'external.png'),Buffer.alloc(3));
  pass('extraneous overwrite fails reconciliation',()=>assert.throws(()=>external.reconcile(),/Untracked/));
  const excludedRoot=sub('exclusions');fs.mkdirSync(path.join(excludedRoot,'state-owned'));fs.writeFileSync(path.join(excludedRoot,'state-owned','x'),'x');fs.writeFileSync(path.join(excludedRoot,'auth-private.json'),'x');fs.writeFileSync(path.join(excludedRoot,'stdout.log'),'x');
  pass('legacy excluded paths stay excluded; no new writer exclusion bypass',()=>assert.equal(createWriter(excludedRoot).reconcile().files,0));
  const evRoot=sub('events'),evWriter=createWriter(evRoot),calls=[];
  const store=createEventStore((name,value)=>{calls.push(name);evWriter.json(name,value);});
  const events=Array.from({length:31},(_,i)=>({sequence:i+1,action:'synthetic-'+i,value:i}));
  store.save(events.slice(0,16));const stable=fs.readFileSync(path.join(evRoot,'events-p00.json'));
  calls.length=0;store.save(events.slice(0,20));store.save(events.slice(0,20));
  pass('append persists only changed event chunk and index',()=>assert.deepEqual(calls,['events-p01','event-index']));
  store.save(events);store.save(store.last());
  pass('closed-page finalization preserves captured event sequence and bytes',()=>{assert.equal(store.count(),31);assert.equal(JSON.parse(fs.readFileSync(path.join(evRoot,'event-index.json'))).count,31);assert.deepEqual(fs.readFileSync(path.join(evRoot,'events-p00.json')),stable);});
  const journey=fs.readFileSync(path.join(base,'harness/journey.mjs'),'utf8');
  const closeSource=journey.slice(journey.indexOf('async function closeContext()'),journey.indexOf('async function entry(id)'));
  const closed={ready:true,page:{isClosed:()=>true},events:[],totalEventCount:0,eventStore:store,fixtureId:'A',cached:{},context:{close:async()=>{}},saveEvents:values=>store.save(values)};
  vm.createContext(closed);await vm.runInContext(closeSource+';closeContext()',closed);
  pass('actual journey closed-page finalizer retains captured events and counter',()=>{assert.equal(closed.totalEventCount,31);assert.equal(closed.events.length,31);assert.equal(closed.ready,false);assert.equal(store.count(),31);});
  let raceContextClosed=false;
  const racing={...closed,ready:true,page:{isClosed:()=>false,evaluate:async()=>{throw Error('closed during evaluate');}},events:[],totalEventCount:0,context:{close:async()=>{raceContextClosed=true;}}};
  vm.createContext(racing);await assert.rejects(vm.runInContext(closeSource+';closeContext()',racing),/closed during evaluate/);
  pass('actual cleanup evaluation race preserves prefix/counter and reports read failure',()=>{assert.equal(racing.totalEventCount,31);assert.equal(racing.events.length,31);assert.equal(raceContextClosed,true);});
  const capturedStore=createEventStore(()=>{}),capturedEvents=events.map(e=>({...e,fixture:'A'}));capturedStore.save(capturedEvents);
  let lateClosed=false;const finalRead=[...events,{sequence:32,action:'late',value:32}];
  const afterRead={ready:true,page:{isClosed:()=>lateClosed,evaluate:async()=>{lateClosed=true;return finalRead;}},events:[],totalEventCount:0,eventStore:capturedStore,fixtureId:'A',cached:{},context:{close:async()=>{}},saveEvents:values=>capturedStore.save(values)};
  vm.createContext(afterRead);await vm.runInContext(closeSource+';closeContext()',afterRead);
  pass('successful last read remains authoritative if page closes immediately afterward',()=>{assert.equal(afterRead.totalEventCount,32);assert.equal(capturedStore.count(),32);});
  const baseline={live:{axes:[['x','category','bottom',true],['y','number','left',false]].map(([direction,type,position,auto])=>{
    const label={fontFamily:{value:'Verdana, sans-serif'},fontSize:{value:11},spacing:{value:11},autoRotate:{value:auto}};
    return {identity:{direction:{value:direction},type:{value:type},position:{value:position}},style:{tick:{value:{enabled:{value:false}}},label:{value:label}}};
  })}};
  pass('baseline guards reject wrong role/position/typography instead of resetting UI',()=>{assertBaseline(baseline);const wrong=structuredClone(baseline);wrong.live.axes[0].style.label.value.spacing.value=17;assert.throws(()=>assertBaseline(wrong),/Conflicting baseline/);});
  pass('label restore guard rejects incomplete rotation or spacing restoration',()=>{const ui={family:'Verdana, sans-serif',size:'11',spacing:'11',auto:false,rotation:'0'};assertLabelUI(ui,ui);assert.throws(()=>assertLabelUI({...ui,spacing:'17'},ui),/spacing/);assert.throws(()=>assertLabelUI({...ui,rotation:'45'},ui),/rotation/);});
  const fixtures=JSON.parse(fs.readFileSync(path.join(base,'harness/fixtures.json'))),data={value:fixtures.A.periods.map((p,i)=>({period:{value:{type:'string',value:p}},amounts:{revenue:{value:fixtures.revenue[i]},operatingIncome:{value:fixtures.operatingIncome[i]}}}))};
  pass('case-boundary guard rejects amount or period drift',()=>{assertFinancialData(data,fixtures.A,fixtures);const wrong=structuredClone(data);wrong.value[0].amounts.revenue.value=999;assert.throws(()=>assertFinancialData(wrong,fixtures.A,fixtures),/USD-million/);});
  const index=JSON.parse(fs.readFileSync(path.join(evRoot,'event-index.json'))),retained=index.files.flatMap(n=>JSON.parse(fs.readFileSync(path.join(evRoot,n))));
  pass('all ordered events retained with unchanged serialized chunks',()=>{assert.deepEqual(retained,events);assert.equal(fs.readFileSync(path.join(evRoot,'events-p01.json'),'utf8'),JSON.stringify(events.slice(16)));assert.deepEqual(index,{count:31,files:['events-p00.json','events-p01.json'],chunkSize:16});});
  pass('event loss, changed prefix and sequence gap rejected',()=>{assert.throws(()=>store.save(events.slice(0,20)),/regression/);const changed=structuredClone(events);changed[0].value=99;assert.throws(()=>store.save(changed),/mutation/);assert.throws(()=>store.save([...events,{sequence:33}]),/discontinuity/);});
  let failEvent=true;const retryRoot=sub('event-retry'),retryWriter=createWriter(retryRoot),retry=createEventStore((name,value)=>{if(name==='event-index'&&failEvent)throw Error('event failure');retryWriter.json(name,value);});
  pass('failed event write retries without loss',()=>{assert.throws(()=>retry.save(events),/event failure/);failEvent=false;retry.save(events);assert.equal(retry.count(),31);retryWriter.reconcile();});
  for(const kind of ['pass','oversize','file-overflow']){
    const finalRoot=sub('final-'+kind);fs.writeFileSync(path.join(finalRoot,'run-status.json'),JSON.stringify({exitCode:1}));
    if(kind==='oversize')fs.writeFileSync(path.join(finalRoot,'oversize.png'),Buffer.alloc(limits.png+1));
    if(kind==='file-overflow')for(let i=0;i<limits.files;i++)fs.writeFileSync(path.join(finalRoot,'extra-'+i+'.json'),'{}');
    const result=spawnSync(process.execPath,[path.join(base,'harness/finalize.mjs'),'0'],{env:{...process.env,CAPTURE_ROOT:finalRoot},encoding:'utf8',windowsHide:true});
    pass('actual finalizer '+kind+' leaves truthful final status',()=>{assert.equal(result.status,kind==='pass'?0:1);assert.equal(JSON.parse(fs.readFileSync(path.join(finalRoot,'run-status.json'))).exitCode,kind==='pass'?0:1);});
  }
  for(const implementation of ['frozen','inventory']){
    const p=sub('bench-'+implementation);for(let i=0;i<100;i++)fs.writeFileSync(path.join(p,'sample-'+i+'.json'),'{}');
    let io;
    if(implementation==='frozen'){
      process.env.CAPTURE_ROOT=p;fs.copyFileSync(path.join(base,'frozen/harness/io.mjs'),path.join(p,'io.mjs'));io=await import(pathToFileURL(path.join(p,'io.mjs')));
    }else{fs.copyFileSync(path.join(base,'frozen/harness/io.mjs'),path.join(p,'io.mjs'));io=createWriter(p);}
    const sample={synthetic:'x'.repeat(315000)},elapsed=[];
    for(let i=0;i<8;i++){const start=performance.now();io.json('rewrite',sample);elapsed.push(performance.now()-start);}
    const actual=fs.readFileSync(path.join(p,'rewrite.json'));
    benchmarks.push({implementation,payloadBytes:actual.length,payloadSha256:digest(actual),retainedFiles:io.budget().files,retainedBytes:io.budget().bytes,rewrites:8,elapsedMs:elapsed,meanMs:elapsed.reduce((a,b)=>a+b,0)/8});
    if(io.reconcile)io.reconcile();
  }
  pass('benchmark implementations produce identical serialized output and retention',()=>{assert.equal(benchmarks[0].payloadSha256,benchmarks[1].payloadSha256);assert.equal(benchmarks[0].retainedBytes,benchmarks[1].retainedBytes);});
}finally{
  if(path.dirname(path.resolve(temp))!==base||!/^offline-[a-f0-9]{10}$/.test(path.basename(temp)))throw Error('Unsafe offline cleanup');
  fs.rmSync(temp,{recursive:true});cleanup=!fs.existsSync(temp);
}
const receipt={scope:'Offline synthetic I/O and event persistence only; no application/browser run',status:'passed',checks,benchmarks,cleanup:{rootConfined:true,rootDeleted:cleanup},sources:{io:sourceHash('harness/io.mjs'),events:sourceHash('harness/events.mjs'),frozenIO:sourceHash('frozen/harness/io.mjs')}};
const output=process.argv[2]?path.resolve(process.argv[2]):path.join(base,'offline-verification.json');fs.writeFileSync(output,JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt));
