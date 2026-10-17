import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,path.basename(path.dirname(here))==='reviewed'?'../../..':'../..');
const diagnosis=path.join(root,'artifacts/ui-parity-tooltip-geometry-diagnosis');
const base=path.join(root,'artifacts/reviewed/ui-parity-tooltip-followup/capture/attempt-20261017-tooltip-followup-a1');
const read=file=>JSON.parse(fs.readFileSync(file,'utf8'));
const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const size=value=>Buffer.byteLength(JSON.stringify(value));
const value=field=>field?.value;
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
let checks=0;
function assert(ok,label){checks++;if(!ok)throw Error(label);}
function close(a,b,label){assert(Math.abs(a-b)<1e-8,label);}
const files=['report.md','offline-calculations.json','source-hashes.json','verify.mjs','verification.json','publication-allowlist.json'];
const frozen=files.map(name=>({sourcePath:'artifacts/ui-parity-tooltip-geometry-diagnosis/'+name,sha256:hash(path.join(diagnosis,name)),bytes:fs.statSync(path.join(diagnosis,name)).size}));
const manifest=read(path.join(diagnosis,'source-hashes.json'));
for(const item of [...manifest.inputs,...manifest.outputs]){
  const file=path.join(root,item.path);
  assert(hash(file)===item.sha256&&fs.statSync(file).size===item.bytes,'manifest '+item.path);
}
const allowlist=read(path.join(diagnosis,'publication-allowlist.json'));
assert(allowlist.files.length===5,'five explicitly selected content files');
for(const item of allowlist.files){
  const file=path.join(root,item.sourcePath);
  assert(hash(file)===item.sha256&&fs.statSync(file).size===item.bytes,'publication '+item.sourcePath);
}
const cases=Array.from({length:8},(_,i)=>read(path.join(base,'T0'+(i+1)+'.json')));
const deltas=[];
for(const c of cases)for(const p of c.probes){
  const geometry=p.settlement.pair[0];
  assert(same(geometry,p.settlement.pair[1]),p.id+' full geometry equality');
  const intended=geometry.series.filter(s=>s.id===p.target.seriesId&&s.yKey===p.target.yKey);
  assert(intended.length===1,p.id+' intended series uniqueness');
  const s=intended[0],nodes=s.nodes.filter(n=>value(n.fields.datumIndex)===p.ordinal);
  assert(nodes.length===1,p.id+' intended node uniqueness');
  const n=nodes[0],f=n.fields;
  assert(value(n.xValue.id)===p.target.wrapperId,p.id+' wrapper');
  const local=c.family==='line'?{x:value(n.point.x),y:value(n.point.y)}:{x:value(f.x)+value(f.width)/2,y:value(f.y)+value(f.height)/2};
  if(c.family!=='line')assert(value(f.width)>0&&value(f.height)>0,p.id+' positive envelope');
  const midpoint={x:value(n.midPoint.x),y:value(n.midPoint.y)};
  for(const axis of ['x','y']){
    const suffix=axis.toUpperCase();
    const offset=geometry.canvas[axis]+value(s.transforms[0]['translation'+suffix])+value(s.transforms[2]['translation'+suffix]);
    close(offset,geometry.area[axis],p.id+' area origin '+axis);
    close(local[axis]+offset,p.target.point[axis],p.id+' reconstructed input '+axis);
  }
  deltas.push({id:p.id,family:c.family,dx:midpoint.x-local.x,dy:midpoint.y-local.y});
}
assert(deltas.length===24,'24 retained pointers');
assert(deltas.filter(d=>d.family==='groupedColumn').length===17,'17 grouped');
assert(deltas.filter(d=>d.family==='groupedColumn').every(d=>Math.abs(d.dx)+Math.abs(d.dy)<1e-8),'all grouped unchanged');
const t05=deltas.find(d=>d.id==='T05.p17'),t08=deltas.find(d=>d.id==='T08.p52');
close(t05.dy,0,'T05 zero midpoint delta');close(t08.dy,28.275,'T08 CSS delta');
const stacked=cases[7].probes.find(p=>p.id==='T08.p52').settlement.pair[0].series;
const n=stacked[0].nodes[0],bottom=value(n.fields.y)+value(n.fields.height);
const raw=stacked.map(s=>value(s.nodes[0].fields.yValue));
const scale=value(n.fields.height)/raw.reduce((sum,v)=>sum+v,0);
close(scale,2.9,'affine scale');
const intervals=stacked.map((s,i)=>{
  const consumed=raw.slice(0,i).reduce((sum,v)=>sum+v,0);
  const interval={key:s.yKey,top:bottom-scale*(consumed+raw[i]),bottom:bottom-scale*consumed};
  close((interval.top+interval.bottom)/2,value(s.nodes[0].midPoint.y),'source segment midpoint '+s.yKey);
  return interval;
});
const inside=(y,key)=>intervals.some(v=>v.key===key&&y>v.top&&y<v.bottom);
assert(inside(104.21875,'revenue')&&inside(132.49375,'operatingIncome'),'distinct inferred interval membership');
const old=cases[5],projected=structuredClone(old);
const retain=state=>({active:state.active,tooltip:state.tooltip===null?null:state.tooltip.visible?Object.fromEntries(['visible','heading','rows','compact','pagination'].map(k=>[k,state.tooltip[k]])):{visible:false},liveStatus:state.liveStatus});
const tabSizes=[],baselineSizes=[];
for(const mode of projected.keyboard){
  const baseline={area:mode.tabs[0].before.area,swapchain:mode.tabs[0].before.swapchain};
  assert(baseline.swapchain.length<=2,'bounded baseline '+mode.mode);
  mode.modeBaseline=baseline;baselineSizes.push(size(baseline));
  for(const tab of mode.tabs){
    assert(tab.state.status==='stable'&&tab.state.pair.length===2&&same(...tab.state.pair),'full source DOM pair '+mode.mode);
    for(const sample of [tab.before,...tab.state.pair])assert(same({area:sample.area,swapchain:sample.swapchain},baseline),'baseline unchanged '+mode.mode);
    tab.before=retain(tab.before);tab.state.pair=tab.state.pair.map(retain);tabSizes.push(size(tab));
  }
}
assert(same(projected.ledger,old.ledger),'ledger unchanged');
const maxima={tab:Math.max(...tabSizes),tabLedger:Math.max(...old.ledger.filter(e=>e.label==='Tab traversal').map(size)),otherLedger:Math.max(...old.ledger.filter(e=>e.label!=='Tab traversal').map(size)),baseline:Math.max(...baselineSizes)};
const estimate=size(projected)+45*(maxima.tab+maxima.tabLedger+2)+6*(maxima.otherLedger+1)+maxima.baseline+2048;
assert(tabSizes.length===27&&size(old)===119493&&size(projected)===41350,'projection size');
assert(same(maxima,{tab:745,tabLedger:440,otherLedger:452,baseline:562})&&estimate===100093,'observed maxima arithmetic');
assert(24+3*24===96&&72+18<=120&&estimate<131072-16000,'conditional budget arithmetic');
const sourceFile=path.join(root,'artifacts/task-2.1/frontend/terminalpro/node_modules/ag-charts-community/dist/package/main.esm.mjs');
const source=fs.readFileSync(sourceFile,'utf8');
assert(source.includes('midPoint: { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 }')&&source.includes('x: barRect.x'),'separate segment/envelope source');
assert(read(path.join(path.dirname(sourceFile),'../../package.json')).version==='12.1.1','installed package version');
const report=fs.readFileSync(path.join(diagnosis,'report.md'),'utf8');
const links=[...report.matchAll(/\]\(([^)]+)\)/g)].map(m=>m[1]);
assert(links.length===7,'seven report links');
for(const link of links){
  const resolved=link.startsWith('../ui-parity-')?path.resolve(root,'artifacts/reviewed',link.slice(3)):path.resolve(diagnosis,link);
  assert(fs.existsSync(resolved),'publication source target '+link);
}
const patterns=[/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/,/\b(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_-]{20,}/,/\bAKIA[A-Z0-9]{16}\b/];
for(const entry of frozen){
  const text=fs.readFileSync(path.join(root,entry.sourcePath),'utf8');
  assert(!patterns.some(p=>p.test(text)),'concrete secret scan '+entry.sourcePath);
  assert(!/\b(?:TODO|TBD|FIXME|HACK|XXX)\b/.test(text),'placeholder scan '+entry.sourcePath);
  assert(hash(path.join(root,entry.sourcePath))===entry.sha256,'frozen preservation '+entry.sourcePath);
}
const result={date:'2026-10-17',verdict:'APPROVED for source proposal and publication only',checks,reportVerifier:{command:'node artifacts/ui-parity-tooltip-geometry-diagnosis/verify.mjs',exitCode:0,checks:1255,readOnlyPreload:'read-only-verifier.mjs',identicalReceiptWriteSuppressed:true},pointerRecords:deltas.length,t05,t08,intervals,retainedTabs:tabSizes.length,projectedCaseBytes:size(projected),maxima,conditional72TabEstimate:estimate,reportLinks:links,reviewedFrozenFiles:frozen,runtimeExecuted:false,collectorApproved:false,actualPickedIdentityAccepted:false,keyboardAccepted:false,publicationCopyAudit:'Controller must verify copied bytes and all links, including separately copied allowlist metadata, after synchronization.'};
fs.writeFileSync(path.join(here,'verification.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({checks,pointerRecords:deltas.length,retainedTabs:tabSizes.length,projectedCaseBytes:size(projected),conditional72TabEstimate:estimate}));
