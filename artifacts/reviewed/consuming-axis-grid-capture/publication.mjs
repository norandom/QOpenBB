import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';

const root=path.dirname(new URL(import.meta.url).pathname);
const read=name=>JSON.parse(fs.readFileSync(root+'/'+name+'.json'));
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
if(process.argv.includes('--check')){
  const manifest=read('publication-allowlist');
  for(const entry of manifest.files){
    assert(!/(credential|runtime-private|state-|\.log$|diagnostics\.json$)/.test(entry.path));
    assert.equal(hash(fs.readFileSync(root+'/'+entry.path)),entry.sha256,entry.path);
  }
  console.log(JSON.stringify({allowlistFiles:manifest.files.length,hashesMatch:true}));
  process.exit(0);
}
const names=['baseline','ui-axis-thickness-3','ui-grid-thickness-4','ui-grid-dash-5',
  'synthetic-width-3-style-1','synthetic-width-1-style-4','synthetic-opacity-quarter','synthetic-opacity-one'];
const fields=['stroke','width','strokeWidth','strokeOpacity','opacity','visible','enabled','lineDash'];
const pick=object=>Object.fromEntries(fields.filter(key=>object[key]!==undefined).map(key=>[key,object[key]]));
const measurements=names.map(name=>{
  const snapshot=read(name),axis=snapshot.state.effective.axes.find(value=>value.position==='left');
  const live=snapshot.state.live.find(value=>value.position==='left');
  return {name,kind:snapshot.kind,input:snapshot.input,effectiveLine:pick(axis.line),
    effectiveGrid:{width:axis.gridLine.width,style:axis.gridLine.style.map(pick)},liveLine:pick(live.lineNode),
    liveGrid:live.gridNodes.map(value=>pick(value.node)),optionsEvents:snapshot.state.events.length};
});
fs.writeFileSync(root+'/measurements.json',JSON.stringify({derivedFrom:names.map(name=>name+'.json'),
  scope:'Original dark groupedColumn, left number axis',measurements},null,2));
const diagnostics=read('diagnostics');
const summary={source:{path:'diagnostics.json',sha256:hash(fs.readFileSync(root+'/diagnostics.json'))},
  cdp:diagnostics.cdp,pageErrors:diagnostics.errors.filter(value=>value.kind==='pageerror'),
  cdpExceptions:diagnostics.errors.filter(value=>value.kind==='cdp-exception'),
  networkLoadingFailures:diagnostics.errors.filter(value=>value.kind==='cdp-network-failed'),
  chartWarnings:diagnostics.errors.filter(value=>value.kind==='console'&&value.type==='warning'&&
    (value.text.startsWith('AG Charts')||value.text.startsWith('AG Grid'))),
  httpFailures:diagnostics.requests.filter(value=>value.status>=400),
  blockedExternalRequests:diagnostics.requests.filter(value=>'blocked' in value).length,
  sanitization:'Raw authentication routes, successful HTTP inventory and stack traces omitted. Owned origin replaced.'};
fs.writeFileSync(root+'/diagnostic-summary.json',JSON.stringify(summary,null,2));
const selected=['report.md','fixture.json','start.mjs','journey.mjs','cleanup.mjs','run.sh','manifest.mjs',
  'verify.mjs','publication.mjs','source-manifest.json','source-excerpts.json','ag-charts-MIT-LICENSE.txt','runtime-identity.json',
  'summary.json','measurements.json','action-ledger.json','diagnostic-summary.json','verification.json',
  'start-status.json','journey-status.json','run-status.json','cleanup-status.json','cleanup-report.json',
  'browser-cleanup.json','verification-status.json','attempt1/journey.mjs','attempt1/start.mjs',
  'attempt1/run.sh','attempt1/failure.json','attempt1/start-status.json','attempt1/journey-status.json',
  'attempt1/run-status.json','attempt1/cleanup-status.json','attempt1/cleanup-report.json',
  'attempt1/browser-cleanup.json',...names.flatMap(name=>[name+'.json',name+'.png'])];
const entries=selected.map(name=>({path:name,sourcePath:'artifacts/consuming-axis-grid-capture/'+name,
  sha256:hash(fs.readFileSync(root+'/'+name)),sanitization:name==='diagnostic-summary.json'?
    'Finite derivative; original bytes/hash recorded inside file':'None; original reviewed synthetic bytes'}));
for(const entry of entries){
  const bytes=fs.readFileSync(root+'/'+entry.path);
  if(!entry.path.endsWith('.png')){
    const text=bytes.toString('utf8');
    assert(!/Aa1![0-9a-f]{48}/.test(text),'Generated credential in '+entry.path);
    assert(!/"(?:access_token|refresh_token|id_token)"\s*:/.test(text),'Authentication token in '+entry.path);
  }
}
fs.writeFileSync(root+'/publication-allowlist.json',JSON.stringify({status:'Prepared for independent review; not published',
  originalRoot:'artifacts/consuming-axis-grid-capture',files:entries,
  excluded:['credential-private.json (removed)','state-* (removed)','runtime-private.json','attempt1/runtime-private.json',
    'diagnostics.json','attempt1/diagnostics.json','*.log','browser profiles and dependency caches'],
  historicalFailure:'Attempt1 failed on original onboarding tier400; exact scripts and failure/cleanup receipts retained.'},null,2));
console.log(JSON.stringify({allowlistFiles:entries.length,prepared:true}));
