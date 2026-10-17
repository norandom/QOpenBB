import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
const base=path.dirname(fileURLToPath(import.meta.url)),entries=[],results=[];
for(const folder of ['harness','baseline'])for(const name of fs.readdirSync(path.join(base,folder)).sort())entries.push(folder+'/'+name);
for(const name of fs.readdirSync(base).filter(n=>n.endsWith('.mjs')))entries.push(name);
for(const entry of entries.filter(n=>n.endsWith('.mjs'))){const result=spawnSync(process.execPath,['--check',path.join(base,entry)],{encoding:'utf8',windowsHide:true});assert.equal(result.status,0,entry+' '+result.stderr);results.push({path:entry,syntax:'passed'});}
const projection=fs.readFileSync(base+'/harness/projection.mjs','utf8'),journey=fs.readFileSync(base+'/harness/journey.mjs','utf8');
for(const forbidden of ['.children','.nodes()','.select(','getTextMeasureBBox','computeBBox(','computeCSSBounds(','toCanvas(','ctx.chartRef','ctx.root','getComputedTransform','setOptions(','updateDelta(','updateOptions('])assert(!projection.includes(forbidden),'Forbidden projection '+forbidden);
assert.equal((projection.match(/\.getBBox\(/g)||[]).length,1,'Only named bbox helper dispatch');
assert(projection.includes('bbox(lg.group)')&&projection.includes('item:bbox(n),label:bbox(n.label),marker:bbox(n.marker)'));
assert(projection.includes('const before=operands()')&&projection.includes('const after=operands()'));
assert(journey.indexOf('if(before&&(wantRaster||potentialMutation))')<journey.indexOf('target[method](arg)'),'Prospective actual before raster');
assert(journey.includes("serviceWorkers:'block'")&&journey.includes('registerRoutes({context,'),'Context-wide routing and service-worker denial');
assert(journey.includes('chromium.launchServer(')&&journey.includes('browserServer.process().pid')&&journey.includes("owned-browser-private.json"),'Owned BrowserServer identity');
const startup=fs.readFileSync(base+'/harness/start.mjs','utf8'),routing=fs.readFileSync(base+'/harness/routes.mjs','utf8');
assert(startup.indexOf("docker('network','create'")<startup.indexOf("docker('run'"),'Network exists before original container');
assert(startup.includes("'--internal'")&&startup.includes('networkGuard(runtime,')&&startup.includes('containerNetworkGuard(runtime,'),'Internal network and exclusive attachment guards');
assert.equal((routing.match(/await allowed\(route\)/g)||[]).length,3,'Independent guard in all three callbacks');
assert(routing.includes('maxRedirects:0'),'Sync fetch cannot follow an external redirect');
assert(!routing.includes('route.continue('),'No unrestricted HTTP continuation escape');
assert(routing.includes('maxRetries:0')&&routing.includes("key.toLowerCase()==='location'"),'No retry or Location transition');
const unchangedRuntime=[];
for(const name of fs.readdirSync(base+'/harness'))if(name!=='routes.mjs'){
  const current=fs.readFileSync(base+'/harness/'+name,'utf8'),old=fs.readFileSync(base+'/baseline/'+name,'utf8');
  assert.equal(current.replaceAll('ui-parity-legend-capture-redirect-guard','ui-parity-legend-capture-revised'),old,'Unchanged runtime '+name);unchangedRuntime.push(name);
}
assert(projection.includes('p.drain=final=>')&&projection.includes('overflow:p.overflow?{...p.overflow}:null'),'Atomic events plus overflow envelope');
const fixture=fs.readFileSync(base+'/harness/fixture.json'),original=fs.readFileSync(path.resolve(base,'../ui-parity-captions/capture/runs/attempt-20261017T134459Z-3656a1b9/harness/fixture.json'));assert.deepEqual(fixture,original);
const files=entries.map(name=>({path:name,bytes:fs.statSync(base+'/'+name).size,physicalLines:fs.readFileSync(base+'/'+name,'utf8').replace(/\r\n?|\n/g,'\n').replace(/\n$/,'').split('\n').length}));
const report={status:'passed',scope:'Source-only syntax, bounded seam scan, fixture equality and unchanged-runtime comparison; no runtime import',results,files,unchangedRuntime,
  productionCaps:'Research harness/test/baseline exclusions; no production complexity pass claimed',excluded:'Frozen baseline is the previous revised Legend collector; never copied into redirect-guard runtime harness'};
fs.writeFileSync(base+'/static-verification.json',JSON.stringify(report,null,2));console.log(JSON.stringify({status:'passed',syntaxFiles:results.length,fixtureBytesEqual:true}));
