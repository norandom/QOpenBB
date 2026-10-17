import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,path.basename(path.dirname(here))==='reviewed'?'../../..':'../..');
const base=path.join(root,'artifacts/reviewed/ui-parity-tooltip-followup/capture/attempt-20261017-tooltip-followup-a1');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const receipt=read(path.join(here,'offline-calculations.json'));
const manifest=read(path.join(here,'source-hashes.json'));
const size=o=>Buffer.byteLength(JSON.stringify(o));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const v=f=>f?.value;
const near=(a,b)=>Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<1e-9;
let checks=0;
function check(ok,label){checks++;if(!ok)throw Error(label);}
function same(a,b,label){check(JSON.stringify(a)===JSON.stringify(b),label);}
for(const item of [...manifest.inputs,...manifest.outputs]){
  const file=item.path.startsWith('artifacts/ui-parity-tooltip-geometry-diagnosis/')?path.join(here,path.basename(item.path)):path.join(root,item.path);
  check(fs.statSync(file).size===item.bytes,item.path+' bytes');
  check(hash(file)===item.sha256,item.path+' hash');
}
let pointerCount=0;
for(let i=1;i<=8;i++){
  const d=read(path.join(base,'T0'+i+'.json'));
  for(const p of d.probes){
    pointerCount++;
    const g=p.settlement.pair[1],s=g.series.find(s=>s.yKey===p.target.yKey);
    const n=s.nodes.find(n=>v(n.fields.datumIndex)===p.ordinal);
    const row=receipt.geometry.find(r=>r.id===p.id);
    same(g,p.settlement.pair[0],p.id+' equal geometry');
    check(g.dpr===1&&g.animationActive===false,p.id+' DPR/animation');
    check(s.chainValid&&s.terminalValid,p.id+' aggregate chain');
    for(const k of ['contentGroup','managedParent','seriesRoot','sceneRoot']){
      check(s.nodePresence[k]===true&&s.nodeKinds[k]==='object',p.id+' '+k);
    }
    for(const k of ['contentToManaged','managedToSeriesRoot','seriesRootToSceneRoot'])check(s.links[k]===true,p.id+' '+k);
    for(let j=0;j<4;j++){
      const t=s.transforms[j];
      for(const k of ['rotation','scalingX','scalingY'])check(t[k].kind==='absent'||v(t[k])===(k==='rotation'?0:1),p.id+' identity '+k);
      for(const k of ['translationX','translationY'])check(j===1||j===3?t[k].kind==='absent':Number.isFinite(v(t[k])),p.id+' translation '+k);
    }
    check(Math.abs(v(s.transforms[2].translationX)-Math.floor(g.seriesRect.x))<=1&&Math.abs(v(s.transforms[2].translationY)-Math.floor(g.seriesRect.y))<=1,p.id+' seriesRect translation');
    check(Math.abs(g.scene.width-g.canvas.width)<=.5&&Math.abs(g.scene.height-g.canvas.height)<=.5,p.id+' CSS scene');
    const center=d.family==='line'?{x:v(n.point.x),y:v(n.point.y)}:{x:v(n.fields.x)+v(n.fields.width)/2,y:v(n.fields.y)+v(n.fields.height)/2};
    const mid={x:v(n.midPoint.x),y:v(n.midPoint.y)};
    const offset={x:g.canvas.x+v(s.transforms[0].translationX)+v(s.transforms[2].translationX),y:g.canvas.y+v(s.transforms[0].translationY)+v(s.transforms[2].translationY)};
    const recorded={x:center.x+offset.x,y:center.y+offset.y};
    const proposed={x:mid.x+offset.x,y:mid.y+offset.y};
    same(center,row.center,p.id+' center');same(mid,row.midpoint,p.id+' midpoint');same(offset,row.offset,p.id+' offset');
    same(recorded,row.recordedCSS,p.id+' original CSS');same(proposed,row.midpointCSS,p.id+' midpoint CSS');
    check(near(recorded.x,p.target.point.x)&&near(recorded.y,p.target.point.y),p.id+' collector result');
    check(n.xValue.id.value===p.target.wrapperId&&p.target.wrapperId===row.wrapperId&&p.target.seriesId===s.id&&row.seriesId===s.id,p.id+' intended identity');
    check(v(n.fields.yValue)===row.rawYValue,p.id+' raw amount');
    same(p.observation.pair[1].tooltip.rows,row.displayedRows,p.id+' displayed content');
    for(const point of [recorded,proposed])for(const box of [g.area,g.canvas])check(point.x>=box.x&&point.x<=box.x+box.width&&point.y>=box.y&&point.y<=box.y+box.height,p.id+' bounds');
  }
}
check(pointerCount===24&&receipt.geometry.length===24,'24 pointer records');
const grouped=receipt.geometry.filter(r=>r.family==='groupedColumn');
check(grouped.length===17&&grouped.every(r=>near(r.center.x,r.midpoint.x)&&near(r.center.y,r.midpoint.y)),'grouped unchanged');
const anomaly=receipt.geometry.find(r=>r.id==='T08.p52');
check(near(anomaly.midpoint.y-anomaly.center.y,28.275),'stacked income delta');
const g=read(path.join(base,'T08.json')).probes.at(-1).settlement.pair[1];
const total=g.series.reduce((n,s)=>n+v(s.nodes[0].fields.yValue),0);
const first=g.series[0].nodes[0],scale=v(first.fields.height)/total;
let bottom=v(first.fields.y)+v(first.fields.height);
for(const s of g.series){
  const n=s.nodes[0],top=bottom-scale*v(n.fields.yValue),midpoint=(top+bottom)/2;
  const expected=receipt.stackedIncomeDerivation.intervals.find(i=>i.key===s.yKey);
  check(near(top,expected.top)&&near(bottom,expected.bottom)&&near(midpoint,expected.midpoint)&&near(midpoint,v(n.midPoint.y)),s.yKey+' segment');
  check(expected.containsOldY===(anomaly.center.y>top&&anomaly.center.y<bottom),s.yKey+' old point membership');
  check(expected.containsProposedY===(anomaly.midpoint.y>top&&anomaly.midpoint.y<bottom),s.yKey+' proposed point membership');
  bottom=top;
}
check(near(scale,2.9)&&near(total,48.125),'stacked affine operands');
const d=read(path.join(base,'T06.json')),projected=structuredClone(d);
const state=o=>({active:o.active,tooltip:o.tooltip?{visible:o.tooltip.visible,...(o.tooltip.visible?{heading:o.tooltip.heading,rows:o.tooltip.rows,compact:o.tooltip.compact,pagination:o.tooltip.pagination}:{})}:null,liveStatus:o.liveStatus});
let maxBaseline=0;
for(const k of projected.keyboard){
  const first=k.tabs[0].before;k.modeBaseline={area:first.area,swapchain:first.swapchain};
  maxBaseline=Math.max(maxBaseline,size(k.modeBaseline));
  for(const t of k.tabs)for(const sample of [t.before,...t.state.pair])same({area:sample.area,swapchain:sample.swapchain},k.modeBaseline,k.mode+' unchanged baseline');
  k.tabs=k.tabs.map(t=>({before:state(t.before),state:{...t.state,pair:t.state.pair.map(state)}}));
}
const tabs=projected.keyboard.flatMap(k=>k.tabs),tabLedger=d.ledger.filter(e=>e.label==='Tab traversal');
const other=d.ledger.filter(e=>e.label!=='Tab traversal');
const maxima={tab:Math.max(...tabs.map(size)),tabLedger:Math.max(...tabLedger.map(size)),otherLedger:Math.max(...other.map(size)),baseline:maxBaseline};
const estimate=size(projected)+45*(maxima.tab+maxima.tabLedger+2)+6*(maxima.otherLedger+1)+maxBaseline+2048;
check(tabs.length===27&&size(d)===119493&&size(projected)===41350,'retained keyboard reprojection');
same(maxima,receipt.keyboard.maxima,'observed maxima');
check(estimate===100093&&estimate===receipt.keyboard.observedMaxima72TabEstimate&&estimate<115072,'conditional72Tab estimate');
const links=[...fs.readFileSync(path.join(here,'report.md'),'utf8').matchAll(/\]\(([^)]+)\)/g)].map(m=>m[1]);
for(const link of links){
  check(!link.includes('node_modules'),'no published dependency-cache link');
  const file=link.startsWith('../ui-parity-')?path.resolve(root,'artifacts/reviewed',link.slice(3)):path.resolve(here,link);
  check(fs.existsSync(file),'publication-depth link '+link);
}
const result={date:'2026-10-17',status:'passed source/artifact/offline checks only',checks,pointerRecords:pointerCount,retainedTabs:tabs.length,projectedCaseBytes:size(projected),observedMaxima72TabEstimate:estimate,sourceInputs:manifest.inputs.length,reportLinks:links.length,runtimeExecuted:false,independentReview:false};
fs.writeFileSync(path.join(here,'verification.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));
