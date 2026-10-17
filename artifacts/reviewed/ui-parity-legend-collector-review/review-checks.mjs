import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {settle} from '../ui-parity-legend-capture/harness/settlement.mjs';

const own=path.dirname(fileURLToPath(import.meta.url));
const base=path.resolve(own,'../ui-parity-legend-capture');
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const record=p=>({sourcePath:path.relative(path.resolve(own,'../..'),p).replaceAll('\\','/'),sha256:hash(p),bytes:fs.statSync(p).size});
const frozen=JSON.parse(fs.readFileSync(base+'/source-hashes.json'));
const before=frozen.sourceFiles.map(f=>record(path.join(base,f.path)));
assert.equal(hash(base+'/source-hashes.json'),'f8c4ba54c233a97fbb3a7ab5ffc5331873ff1e49532735a1e403a9b76b2e2bf6');
assert.equal(hash(base+'/harness-manifest.json'),'9c6400819ba8d711829ba6abcc1c8b6ace2da1cd554ca01db7ea2627cb9ae1b3');
for(const f of frozen.sourceFiles){assert.equal(hash(path.join(base,f.path)),f.sha256,f.path);assert.equal(fs.statSync(path.join(base,f.path)).size,f.bytes,f.path);}
const manifest=JSON.parse(fs.readFileSync(base+'/harness-manifest.json'));
for(const f of manifest.files){assert.equal(hash(path.join(base,f.path)),f.sha256,f.path);assert.equal(fs.statSync(path.join(base,f.path)).size,f.bytes,f.path);}
assert.equal(hash(path.resolve(base,'../ui-parity-legend-plan-revised/plan.md')),manifest.plan.sha256);
assert.equal(hash(path.resolve(base,'../ui-parity-legend-plan-revision-review/review.md')),manifest.review.sha256);

// Replay the supplied offline tests without allowing their report write in the frozen directory.
let replay=fs.readFileSync(base+'/offline-tests.mjs','utf8');
replay=replay.replace(/from '(\.\/[^']+)'/g,(_m,p)=>'from '+JSON.stringify(pathToFileURL(path.resolve(base,p)).href));
replay=replay.replace("new URL('./harness/fixture.json',import.meta.url)",JSON.stringify(path.join(base,'harness/fixture.json')));
replay=replay.replace("fs.writeFileSync(new URL('./offline-verification.json',import.meta.url),JSON.stringify(report,null,2));console.log(JSON.stringify(report));",'globalThis.__reviewReplay=report;');
await import('data:text/javascript;base64,'+Buffer.from(replay).toString('base64'));
assert.equal(globalThis.__reviewReplay.tests,16);
const syntax=[];
for(const folder of ['harness','baseline'])for(const name of fs.readdirSync(path.join(base,folder)))if(name.endsWith('.mjs'))syntax.push(folder+'/'+name);
for(const name of fs.readdirSync(base))if(name.endsWith('.mjs'))syntax.push(name);
for(const name of syntax){const result=spawnSync(process.execPath,['--check',path.join(base,name)],{encoding:'utf8',windowsHide:true});assert.equal(result.status,0,name+result.stderr);}
assert.deepEqual(fs.readFileSync(base+'/harness/fixture.json'),fs.readFileSync(path.resolve(base,'../ui-parity-captions/capture/runs/attempt-20261017T134459Z-3656a1b9/harness/fixture.json')));

const counterexamples=[];
const operands=Array.from({length:14},(_,i)=>({owner:'named-'+i,key:'x',record:{own:true,in:true,kind:'value',type:'number',value:0}}));
const changed=structuredClone(operands);changed[7].record.value=918273;
const bad={valid:false,reason:'bbox-getter-operands-changed',operands:{before:operands,after:changed}};
const good={valid:true,animationActive:false,live:{},geometry:{},effective:{},fonts:[],operands:{before:operands,after:operands,valid:true}};
let time=0,count=0;
const recovered=await settle({waitForUpdate:async()=>{},sample:async()=>++count===1?bad:good,now:()=>time,pause:async ms=>{time+=ms;}});
assert.equal(recovered.settled.invalidCount,1);assert(!JSON.stringify(recovered).includes('918273'));
counterexamples.push({id:'B02-recovery',observed:'One invalid operand bracket followed by two valid equal samples succeeds, but the changed value and invalid pair are absent from the returned receipt.',samples:count,invalidCount:recovered.settled.invalidCount});
time=0;count=0;
try{await settle({waitForUpdate:async()=>{},sample:async()=>++count===1?bad:{...good,animationActive:true},now:()=>time,pause:async ms=>{time+=ms;}});assert.fail('Expected settlement failure');}
catch(error){assert.equal(error.diagnostic.invalidCount,1);assert(!JSON.stringify(error.diagnostic).includes('918273'));counterexamples.push({id:'B02-failure',observed:'The final active sample also displaces the earlier invalid bracket in a failed settlement.',samples:error.diagnostic.count});}

// Execute only route registration/callbacks with fake page/routes; no Playwright import or network.
const journey=fs.readFileSync(base+'/harness/journey.mjs','utf8');
const routeSource=journey.slice(journey.indexOf("  await page.route('**/*'"),journey.indexOf("  await step('Login navigation'"));
const callbacks=[];
const AsyncFunction=Object.getPrototypeOf(async function(){}).constructor;
await new AsyncFunction('page','runtime','diagnostic','fs','rows',routeSource.replaceAll('import.meta.url',JSON.stringify(pathToFileURL(base+'/harness/journey.mjs').href)))({route:async(pattern,callback)=>callbacks.push({pattern,callback})},{origin:'http://127.0.0.1:12345'},()=>{},fs,[]);
let fetched=0,fulfilled=0,aborted=0;
const fakeRoute=url=>({request:()=>({url:()=>url,method:()=> 'GET'}),fetch:async()=>{fetched++;return {json:async()=>({})};},fulfill:async()=>{fulfilled++;},abort:async()=>{aborted++;},continue:async()=>{}});
await callbacks[1].callback(fakeRoute('https://external.invalid/api/pro/dash/sync'));
await callbacks[2].callback(fakeRoute('https://external.invalid/synthetic_financials'));
assert.equal(fetched,1);assert.equal(fulfilled,2);assert.equal(aborted,0);
counterexamples.push({id:'B01-specialized-routes',observed:'Specialized handlers themselves accept external-origin requests: sync calls route.fetch and synthetic fulfills without an origin check.',mockFetches:fetched,mockFulfillments:fulfilled,mockAborts:aborted,networkExecuted:false});

assert.deepEqual(frozen.sourceFiles.map(f=>record(path.join(base,f.path))),before);
const report={date:'2026-10-17',scope:'Independent source/offline review; no browser, application, container, build, installation or runtime attempt',node:process.version,command:'node artifacts/ui-parity-legend-collector-review/review-checks.mjs',exitCode:0,frozenHashesVerified:true,frozenUnchanged:true,sourceFiles:before,plan:record(path.resolve(base,'../ui-parity-legend-plan-revised/plan.md')),planReview:record(path.resolve(base,'../ui-parity-legend-plan-revision-review/review.md')),offlineReplay:{tests:globalThis.__reviewReplay.tests,results:globalThis.__reviewReplay.results,adaptation:'Only relative imports/fixture path redirected to originals and final report redirected to memory. Original tests did not write frozen reports.'},syntax:{count:syntax.length,files:syntax.sort(),status:'passed'},fixtureBytesEqual:true,counterexamples,runtimeExecuted:false,productionComplexity:'Research exclusion; future maintained code retains 400 physical lines/file, 300 logical units/file, 50/function and inventory/checker foundation.'};
fs.writeFileSync(path.join(own,'verification.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({frozenUnchanged:true,offlineTests:16,syntaxFiles:syntax.length,counterexamples:counterexamples.map(x=>x.id)}));
