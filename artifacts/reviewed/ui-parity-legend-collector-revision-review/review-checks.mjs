import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {registerRoutes} from '../ui-parity-legend-capture-revised/harness/routes.mjs';
import {cleanupBrowser} from '../ui-parity-legend-capture-revised/harness/browser-process.mjs';

const own=path.dirname(fileURLToPath(import.meta.url)),repo=path.resolve(own,'../..'),base=path.resolve(own,'../ui-parity-legend-capture-revised');
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const entry=p=>({sourcePath:path.relative(repo,p).replaceAll('\\','/'),sha256:hash(p),bytes:fs.statSync(p).size});
assert.equal(hash(base+'/harness-manifest.json'),'a26c8d2ff6fc1274f2a8e2ec660e42ab33b5e2730e2245039a349e524fbb786c');
assert.equal(hash(base+'/source-hashes.json'),'943b08f97dc22eb2a11bebf0d3a36cf840467e1d1899eac6e468161f4f59811a');
const manifest=JSON.parse(fs.readFileSync(base+'/source-hashes.json'));
const files=manifest.sourceFiles.map(f=>{const p=path.join(base,f.path);assert.equal(hash(p),f.sha256,f.path);assert.equal(fs.statSync(p).size,f.bytes,f.path);return entry(p);});
files.push(entry(base+'/source-hashes.json'));
const provenance=JSON.parse(fs.readFileSync(base+'/provenance.json'));
for(const f of provenance.localInputs){const p=path.join(repo,f.path);assert.equal(hash(p),f.sha256);assert.equal(fs.statSync(p).size,f.bytes);}
const oldBase=path.resolve(base,'../ui-parity-legend-capture');
assert.equal(hash(oldBase+'/source-hashes.json'),'f8c4ba54c233a97fbb3a7ab5ffc5331873ff1e49532735a1e403a9b76b2e2bf6');
for(const f of JSON.parse(fs.readFileSync(oldBase+'/source-hashes.json')).sourceFiles){assert.equal(hash(oldBase+'/'+f.path),f.sha256);assert.equal(fs.statSync(oldBase+'/'+f.path).size,f.bytes);}
const baseline=JSON.parse(fs.readFileSync(base+'/baseline-source-manifest.json'));
for(const f of baseline.files)assert.equal(hash(base+'/baseline/'+path.basename(f.path)),f.sha256);

let replay=fs.readFileSync(base+'/offline-tests.mjs','utf8');
replay=replay.replace(/from '(\.\/[^']+)'/g,(_m,p)=>'from '+JSON.stringify(pathToFileURL(path.resolve(base,p)).href));
replay=replay.replace("new URL('./harness/fixture.json',import.meta.url)",JSON.stringify(path.join(base,'harness/fixture.json')));
replay=replay.replace("fs.writeFileSync(new URL('./offline-verification.json',import.meta.url),JSON.stringify(report,null,2));console.log(JSON.stringify(report));",'globalThis.__revisionReplay=report;');
await import('data:text/javascript;base64,'+Buffer.from(replay).toString('base64'));
assert.equal(globalThis.__revisionReplay.tests,25);
const syntax=[];
for(const folder of ['harness','baseline'])for(const name of fs.readdirSync(path.join(base,folder)))if(name.endsWith('.mjs'))syntax.push(folder+'/'+name);
for(const name of fs.readdirSync(base))if(name.endsWith('.mjs'))syntax.push(name);
for(const name of syntax){const result=spawnSync(process.execPath,['--check',path.join(base,name)],{encoding:'utf8',windowsHide:true});assert.equal(result.status,0,name+result.stderr);}
const stable=['cases.mjs','controls.mjs','events.mjs','fixture.json','geometry.mjs','guards.mjs','io.mjs','limits.mjs','run.sh','status.mjs'];
for(const name of stable)assert.equal(hash(base+'/harness/'+name),hash(oldBase+'/harness/'+name),name);
assert.deepEqual(fs.readFileSync(base+'/harness/fixture.json'),fs.readFileSync(path.resolve(base,'../ui-parity-captions/capture/runs/attempt-20261017T134459Z-3656a1b9/harness/fixture.json')));

const routes=[],calls=[];
await registerRoutes({context:{route:async(pattern,callback)=>routes.push({pattern,callback})},runtime:{origin:'http://127.0.0.1:12345'},fixture:{},rows:[],diagnostic(){}});
function fake(method,url){return {request:()=>({url:()=>url,method:()=>method}),continue:async()=>calls.push({method,url,decision:'unrestricted-continue'}),fetch:async()=>assert.fail('Unexpected fetch'),abort:async()=>assert.fail('Unexpected abort')};}
await routes[0].callback(fake('GET','http://127.0.0.1:12345/login'));
await routes[1].callback(fake('POST','http://127.0.0.1:12345/api/pro/dash/sync'));
assert.equal(calls.length,2);
const corePath=path.join(repo,'verification/node_modules/.pnpm/playwright-core@1.64.0/node_modules/playwright-core/lib/coreBundle.js');
const core=fs.readFileSync(corePath,'utf8');
const needle='if (redirectedFrom || !this._userRequestInterceptionEnabled && this._protocolRequestInterceptionEnabled)';
const offset=core.indexOf(needle);assert(offset>=0);
const fragment=core.slice(offset,core.indexOf('const isNavigationRequest',offset));
assert(fragment.includes('Fetch.continueRequest'));assert(fragment.includes('} else {\n            route2 = new RouteImpl'));
const line=core.slice(0,offset).split('\n').length;
const owned={pid:12345,startTicks:'123'},signals=[];let reads=0;
await assert.rejects(cleanupBrowser(owned,{read:()=>++reads===1?owned:{...owned,startTicks:'999'},kill:(pid,signal)=>signals.push({pid,signal}),pause:async()=>{}}),/PID reused/);
assert.deepEqual(signals,[{pid:12345,signal:'SIGTERM'}]);

for(const f of files){assert.equal(hash(path.join(repo,f.sourcePath)),f.sha256);assert.equal(fs.statSync(path.join(repo,f.sourcePath)).size,f.bytes);}
const report={date:'2026-10-17',scope:'Independent B01-B04 source/offline rereview; no runtime',command:'node artifacts/ui-parity-legend-collector-revision-review/review-checks.mjs',node:process.version,exitCode:0,frozenUnchanged:true,sourceFiles:files,provenanceVerified:true,initialFrozenVerified:true,baselineVerified:true,unchangedHarnessFiles:stable,fixtureBytesEqual:true,offlineReplay:{tests:globalThis.__revisionReplay.tests,results:globalThis.__revisionReplay.results,adaptation:'Relative imports/fixture read resolve to original frozen files; final test report redirected to memory.'},syntax:{count:syntax.length,files:syntax.sort(),status:'passed'},additionalChecks:[{id:'B01-redirect-incomplete',calls,observation:'Both paths continue the allowed first URL without response/redirect validation.',installedSource:{...entry(corePath),line,behavior:'Chromium redirectedFrom branch sends Fetch.continueRequest without a RouteImpl; shared page/context path.'},runtimeCounterexampleExecuted:false},{id:'B03-PID-reuse-during-fallback',signals,observation:'A changed start-tick identity after TERM raises before another signal.'}],verdict:{B01:'partial; generic and non-GET redirects remain blocked for approval',B02:'closed for source review',B03:'closed for recorded parent-process scope',B04:'closed for source review',runtimeEligible:false},sources:[{url:'https://playwright.dev/docs/api/class-page#page-route',claim:'Routing handler applies only to first URL in an HTTP redirect chain.'},{url:'https://raw.githubusercontent.com/microsoft/playwright/main/packages/playwright-core/src/server/chromium/crNetworkManager.ts',claim:'Redirected Chromium request path continues without creating a route.'},{url:'https://docs.docker.com/reference/cli/docker/network/create/#network-internal-mode---internal',claim:'Internal networks block other-network traffic; host gateway communication remains possible.'}],runtimeExecuted:false};
fs.writeFileSync(own+'/verification.json',JSON.stringify(report,null,2)+'\n');
fs.writeFileSync(own+'/reviewed-collector-publication-allowlist.json',JSON.stringify(files,null,2)+'\n');
console.log(JSON.stringify({offlineTests:25,syntaxFiles:syntax.length,frozenUnchanged:true,remainingBlocker:'B01 generic/non-GET redirect bypass',sourcePublicationFiles:files.length}));
