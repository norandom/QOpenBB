import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {registerRoutes} from '../ui-parity-legend-capture-redirect-guard/harness/routes.mjs';
const own=path.dirname(fileURLToPath(import.meta.url)),repo=path.resolve(own,'../..'),base=path.resolve(own,'../ui-parity-legend-capture-redirect-guard');
const sha=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const entry=p=>({sourcePath:path.relative(repo,p).replaceAll('\\','/'),sha256:sha(p),bytes:fs.statSync(p).size});
const expected={'harness-manifest.json':'9ba3ebf7976b2fc8f0a027fd2823c93365cba5e297de5d988311da7c405f4531','source-hashes.json':'5b0674b7aae4e0a7c9e26fb26b7009def4e42fb73ed67865a31d71b34c502704','publication-allowlist.json':'5eca0931671e3543291e42a66b4000a5a0786414169c4747e69a6c61b1874841'};
for(const [name,hash] of Object.entries(expected))assert.equal(sha(base+'/'+name),hash);
const source=JSON.parse(fs.readFileSync(base+'/source-hashes.json'));
for(const f of source.sourceFiles){assert.equal(sha(base+'/'+f.path),f.sha256,f.path);assert.equal(fs.statSync(base+'/'+f.path).size,f.bytes,f.path);}
const publication=JSON.parse(fs.readFileSync(base+'/publication-allowlist.json'));
assert.equal(publication.length,57);
for(const f of publication){const p=path.join(repo,f.sourcePath);assert.equal(sha(p),f.sha256);assert.equal(fs.statSync(p).size,f.bytes);assert(!/-private\.json$|\.log$|(?:^|\/)attempt-|(?:^|\/)state-/.test(f.sourcePath));}
for(const f of JSON.parse(fs.readFileSync(base+'/provenance.json')).localInputs){const p=path.join(repo,f.path);assert.equal(sha(p),f.sha256);assert.equal(fs.statSync(p).size,f.bytes);}
const prior=path.resolve(base,'../ui-parity-legend-capture-revised'),unchanged=[];
for(const name of fs.readdirSync(base+'/harness')){
  assert.equal(sha(base+'/baseline/'+name),sha(prior+'/harness/'+name),'baseline '+name);
  if(name==='routes.mjs')continue;
  assert.equal(fs.readFileSync(base+'/harness/'+name,'utf8').replaceAll('ui-parity-legend-capture-redirect-guard','ui-parity-legend-capture-revised'),fs.readFileSync(prior+'/harness/'+name,'utf8'),name);unchanged.push(name);
}
for(const folder of ['ui-parity-legend-capture','ui-parity-legend-capture-revised']){const old=path.resolve(base,'../'+folder);for(const f of JSON.parse(fs.readFileSync(old+'/source-hashes.json')).sourceFiles){assert.equal(sha(old+'/'+f.path),f.sha256);assert.equal(fs.statSync(old+'/'+f.path).size,f.bytes);}}
let replay=fs.readFileSync(base+'/offline-tests.mjs','utf8');
replay=replay.replace(/from '(\.\/[^']+)'/g,(_m,p)=>'from '+JSON.stringify(pathToFileURL(path.resolve(base,p)).href));
replay=replay.replace("new URL('./harness/fixture.json',import.meta.url)",JSON.stringify(path.join(base,'harness/fixture.json')));
replay=replay.replace("fs.writeFileSync(new URL('./offline-verification.json',import.meta.url),JSON.stringify(report,null,2));console.log(JSON.stringify(report));",'globalThis.__finalReplay=report;');
await import('data:text/javascript;base64,'+Buffer.from(replay).toString('base64'));
assert.equal(globalThis.__finalReplay.tests,30);
const syntax=[];for(const folder of ['harness','baseline'])for(const name of fs.readdirSync(base+'/'+folder))if(name.endsWith('.mjs'))syntax.push(folder+'/'+name);
for(const name of fs.readdirSync(base))if(name.endsWith('.mjs'))syntax.push(name);
for(const name of syntax){const r=spawnSync(process.execPath,['--check',base+'/'+name],{encoding:'utf8',windowsHide:true});assert.equal(r.status,0,name+r.stderr);}
assert.deepEqual(fs.readFileSync(base+'/harness/fixture.json'),fs.readFileSync(path.resolve(base,'../ui-parity-captions/capture/runs/attempt-20261017T134459Z-3656a1b9/harness/fixture.json')));
const routes=[],diagnostics=[];await registerRoutes({context:{route:async(pattern,callback)=>routes.push({pattern,callback})},runtime:{origin:'http://127.0.0.1:12345'},fixture:{},rows:[],diagnostic:(kind,value)=>diagnostics.push({kind,...value})});
let rejected=0;
for(const [index,method] of [[0,'GET'],[0,'POST'],[1,'PUT']])for(let status=300;status<400;status++){
  let fetches=0,aborts=0;const route={request:()=>({url:()=> 'http://127.0.0.1:12345/resource',method:()=>method}),fetch:async options=>{assert.deepEqual(options,{maxRedirects:0,maxRetries:0,timeout:4000});fetches++;return {url:()=> 'http://127.0.0.1:12345/resource',status:()=>status,headers:()=>({})};},abort:async()=>{aborts++;},fulfill:async()=>assert.fail('Redirect fulfillment'),continue:async()=>assert.fail('Unrestricted continue')};
  await assert.rejects(routes[index].callback(route),/traffic-unresolved/);assert.equal(fetches,1);assert.equal(aborts,1);rejected++;
}
let aborts=0;await assert.rejects(routes[0].callback({request:()=>({url:()=> 'http://127.0.0.1:12345/resource'}),fetch:async()=>{throw Error('sensitive-query-sentinel');},abort:async()=>{aborts++;},fulfill:async()=>assert.fail('Fetch failure fulfillment')}),/request-fetch-failed/);
assert.equal(aborts,1);assert(!JSON.stringify(diagnostics).includes('sensitive-query-sentinel'));
assert(!fs.readFileSync(base+'/harness/routes.mjs','utf8').includes('route.continue('));
for(const [name,hash] of Object.entries(expected))assert.equal(sha(base+'/'+name),hash);
for(const f of publication)assert.equal(sha(path.join(repo,f.sourcePath)),f.sha256);
const report={date:'2026-10-17',command:'node artifacts/ui-parity-legend-redirect-review/review-checks.mjs',node:process.version,exitCode:0,scope:'Independent final B01 source/offline review only',frozenUnchanged:true,manifests:Object.keys(expected).map(n=>entry(base+'/'+n)),provenanceVerified:true,priorInventoriesVerified:true,unchangedRuntime:unchanged,fixtureBytesEqual:true,offlineReplay:{tests:30,results:globalThis.__finalReplay.results,adaptation:'Imports/fixture point to frozen originals; final report redirected to memory, without rewriting original files.'},syntax:{count:syntax.length,files:syntax.sort(),status:'passed'},additionalChecks:{all3xxStatusesRejectedAcrossGenericGETPOSTAndSyncPUT:rejected,fetchFailureAbortedWithSanitizedFixedReason:true,unrestrictedContinueAbsent:true},publication:{verifiedEntries:57,bytes:publication.reduce((n,f)=>n+f.bytes,0),selected:publication,noPrivateStateOrGeneratedCredentials:true,verdict:'Safe exact source-only publication; controller owns mirroring.'},verdict:{B01:'closed for the reviewed HTTP(S) routing boundary',B02:'unchanged; source closure retained',B03:'unchanged; recorded parent-process identity closure retained',B04:'unchanged; source closure retained',eligibleForOneSeparatelyGrantedAttempt:true,runtimeGranted:false},runtimeExecuted:false};
fs.writeFileSync(own+'/verification.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({tests:30,syntaxFiles:syntax.length,additionalRedirectCases:rejected,publicationEntries:57,frozenUnchanged:true,eligibleForOneSeparatelyGrantedAttempt:true}));
