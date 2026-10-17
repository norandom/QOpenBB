import {geometry,dom} from './projection.mjs';
import {limits} from './contract.mjs';
const delay=ms=>new Promise(r=>setTimeout(r,ms));
const v=f=>f?.value;
const finite=x=>typeof x==='number'&&Number.isFinite(x);
export function coordinate(g,ordinal,key,family){
  if(g.dpr!==1||g.animationActive!==false)throw Error('coordinate-unresolved: DPR/animation');
  const s=g.series.find(s=>s.yKey===key);
  if(!s||!s.chainValid||s.terminalValid!==true||
    !['contentGroup','managedParent','seriesRoot','sceneRoot'].every(k=>s.nodePresence?.[k]===true)||
    !['contentGroup','managedParent','seriesRoot','sceneRoot'].every(k=>s.nodeKinds?.[k]==='object')||
    !['contentToManaged','managedToSeriesRoot','seriesRootToSceneRoot'].every(k=>s.links?.[k]===true))throw Error('coordinate-unresolved: exact parent chain');
  const n=s.nodes.find(n=>v(n.fields.datumIndex)===ordinal);
  if(!n)throw Error('no-hittable-node: missing datum ordinal');
  for(let i=0;i<4;i++){const t=s.transforms[i],plain=i===1||i===3;
    for(const k of ['rotation','scalingX','scalingY'])if(t[k].kind!=='absent'&&v(t[k])!==(k==='rotation'?0:1))throw Error('coordinate-unresolved: nonidentity transform');
    for(const k of ['translationX','translationY'])if(plain?t[k].kind!=='absent':!finite(v(t[k])))throw Error('coordinate-unresolved: translation');}
  if(Math.abs(v(s.transforms[2].translationX)-Math.floor(g.seriesRect.x))>1||Math.abs(v(s.transforms[2].translationY)-Math.floor(g.seriesRect.y))>1)throw Error('coordinate-unresolved: seriesRect translation');
  if(Math.abs(g.scene.width-g.canvas.width)>.5||Math.abs(g.scene.height-g.canvas.height)>.5)throw Error('coordinate-unresolved: CSS scene');
  const line=family==='line',width=v(n.fields.width),height=v(n.fields.height);
  if(!line&&(!(width>0)||!(height>0)))throw Error('no-hittable-node: zero bar');
  const stacked=family==='stackedColumn';
  if(stacked&&(!finite(v(n.midPoint?.x))||!finite(v(n.midPoint?.y))))throw Error('coordinate-unresolved: finite stacked midpoint required');
  const local={x:line?v(n.point.x):stacked?v(n.midPoint.x):v(n.fields.x)+width/2,
    y:line?v(n.point.y):stacked?v(n.midPoint.y):v(n.fields.y)+height/2};
  const point={x:g.canvas.x+local.x+v(s.transforms[0].translationX)+v(s.transforms[2].translationX),
    y:g.canvas.y+local.y+v(s.transforms[0].translationY)+v(s.transforms[2].translationY)};
  for(const b of [g.canvas,g.area])if(!finite(point.x)||!finite(point.y)||point.x<b.x||point.y<b.y||point.x>b.x+b.width||point.y>b.y+b.height)throw Error('coordinate-unresolved: outside chart');
  return {observationOrdinal:ordinal,wrapperId:n.xValue.id?.value??null,yKey:key,seriesId:s.id,geometry:n,local,point,operands:{canvas:g.canvas,seriesRect:g.seriesRect,scene:g.scene,area:g.area,transforms:s.transforms},valid:true};
}
export async function settle(page,request,guard){
  const began=Date.now(),deadline=began+limits.settlementMs;
  guard();await Promise.race([page.evaluate(()=>window.__tooltipProxy.waitForUpdate()),delay(limits.updateMs).then(()=>{throw Error('settlement-unresolved: update timeout');})]);
  let prior=null,count=0;
  while(count<limits.geometrySamples&&Date.now()<deadline){guard();const sample=await page.evaluate(geometry,request);count++;
    if(sample.animationActive===false&&prior?.animationActive===false&&JSON.stringify(sample)===JSON.stringify(prior))return {pair:[prior,sample],sampleCount:count,elapsedMs:Date.now()-began};
    prior=sample;if(count<limits.geometrySamples&&Date.now()+limits.geometryIntervalMs<deadline)await delay(limits.geometryIntervalMs);else break;}
  throw Error('settlement-unresolved: no equal inactive pair');
}
export async function observe(page,guard,inspect=()=>{}){
  const began=Date.now();let prior=null,previous=null,count=0,last=null;
  while(count<limits.tooltipSamples&&Date.now()-began<limits.tooltipMs){guard();last=await page.evaluate(dom);inspect(last);count++;
    if(prior&&JSON.stringify(last)===JSON.stringify(prior))return {status:'stable',pair:[prior,last],sampleCount:count,elapsedMs:Date.now()-began};
    previous=prior;prior=last;if(count<limits.tooltipSamples)await delay(limits.tooltipIntervalMs);}
  return {status:'tooltip-observation-unresolved',pair:previous?[previous,last]:last?[last]:[],sampleCount:count,elapsedMs:Date.now()-began};
}
