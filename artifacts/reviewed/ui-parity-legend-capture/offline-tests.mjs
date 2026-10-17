import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {install,acquire} from './harness/projection.mjs';
import {geometryTools} from './harness/geometry.mjs';
import {settle} from './harness/settlement.mjs';
import {createWriter,increment} from './harness/io.mjs';
import {createEventStore} from './harness/events.mjs';
import {assertFixture} from './harness/guards.mjs';
import {limits,rows} from './harness/limits.mjs';
import {executeCases} from './harness/cases.mjs';
const results=[],test=async(name,fn)=>{await fn();results.push({name,status:'passed'});};
function fixture(){
  const calls=[];class Group{static className='Group';}class Item{static className='MarkerLabel';}
  const base=(x=0,y=0)=>({visible:true,opacity:1,translationX:x,translationY:y});
  const node=(kind,x,y,w,h)=>Object.assign(new kind(),base(),{getBBox(){calls.push(this.name);return {x,y,width:w,height:h};}});
  const root=Object.assign(new Group(),{visible:true,opacity:1}),group=node(Group,10,20,200,20);group.name='group';group.translationX=10;group.translationY=20;group.parentNode=root;
  const names=['Revenue (USD millions)','Operating Income (USD millions)'];
  const items=names.map((text,i)=>{const item=node(Item,i*100,0,90,20);item.name='item'+i;item.translationX=i*100;item.parentNode=group;item.pageIndex=0;item.spacing=5;item.length=11;
    item.symbolsGroup=Object.assign(new Group(),{visible:true,opacity:1,parentNode:item});
    item.label=Object.assign(node(Group,16,-5,70,10),{name:'label'+i,parentNode:item,text,fontFamily:'Verdana, sans-serif',fontSize:11,fontWeight:400,fontStyle:'normal',fill:'white',x:16,y:0});
    item.marker=Object.assign(node(Group,-5,-5,11,11),{name:'marker'+i,parentNode:item.symbolsGroup,x:0,y:0,size:11,strokeWidth:1,stroke:'blue',fill:'blue',shape:'square'});
    item.line=Object.assign(new Group(),{parentNode:item.symbolsGroup,visible:false,strokeWidth:0});
    item.datum={id:'item-'+i,seriesId:'series-'+i,itemId:['revenue','operatingIncome'][i],enabled:true,label:{text}};
    item.proxyButton={getElement:()=>element('BUTTON',{textContent:text})};return item;});
  const legend={enabled:true,visible:true,position:'top',spacing:20,maxHeight:50,item:{paddingX:32,paddingY:8,marker:{size:11,strokeWidth:1,padding:5,shape:'square'},label:{fontFamily:'Verdana, sans-serif',fontSize:11,fontWeight:400,fontStyle:'normal',color:'white'}},
    group,itemSelection:{each(fn){items.forEach(n=>fn(n,n.datum));}},pagination:{visible:false,currentPage:0,totalPages:1}};
  const data=rows.map((r,i)=>({...r,period:{id:i,value:r.period}})),source={data,theme:{overrides:{}},series:names.map((yName,i)=>({id:'series-'+i,type:'bar',xKey:'period',yKey:['revenue','operatingIncome'][i],yName}))};
  const chart={legend,padding:{top:20,right:20,bottom:20,left:20},seriesRect:{x:20,y:80,width:600,height:300},ctx:{scene:{root,width:700,height:500},animationManager:{isActive:()=>false}},
    series:source.series.map(s=>({id:s.id,type:'bar',visible:true,properties:{xKey:s.xKey,yKey:s.yKey,visible:true,strokeWidth:0,stroke:'blue'},contentGroup:Object.assign(new Group(),{visible:true,opacity:1})})),
    chartOptions:{processedOptions:{legend,data,series:source.series}}};
  const model={chartId:'chart-1',chartType:'groupedColumn',chartThemeName:'custom',switchCategorySeries:false,aggFunc:undefined,chartOptions:{},cellRange:{rowStartIndex:null,rowEndIndex:null,columns:['period','revenue','operatingIncome']}};
  const grid={getChartModels:()=>[model],getChartRef:id=>id===model.chartId?{chart:proxy}:null,addEventListener(){},removeEventListener(){}};
  const proxy={chart,getOptions:()=>source,waitForUpdate:async()=>{}};
  const canvas=element('CANVAS',{width:700,height:500,box:{x:10,y:10,width:700,height:500}}),toolbar=element('DIV',{contains:()=>true});
  const gridRoot={__reactFiber:{memoizedProps:{value:{gridRef:{current:{api:grid}}}},return:null}};
  globalThis.window={};globalThis.devicePixelRatio=1;globalThis.getComputedStyle=()=>({display:'block',visibility:'visible',opacity:'1'});
  globalThis.document={fonts:{check:()=>true},activeElement:null,getElementById:()=>null,querySelector:()=>null,
    querySelectorAll:selector=>selector==='.ag-root-wrapper'?[gridRoot]:selector==='.ag-charts-canvas canvas'?[canvas]:selector==='.ag-charts-proxy-legend-toolbar'?[toolbar]:[]};
  install();const acquired=acquire();return {calls,items,chart,group,root,grid,model,source,acquired,store:window.__legend};
}
function element(tagName,extra={}){const box=extra.box??{x:10,y:10,width:100,height:20};return {tagName,textContent:'',isConnected:true,getBoundingClientRect:()=>box,getClientRects:()=>[box],getAttribute:()=>null,...extra};}
await test('seven direct BBox calls and fourteen before/after operands',()=>{const f=fixture(),s=f.store.snapshot();assert.equal(s.valid,true);assert.deepEqual(f.calls,['group','item0','label0','marker0','item1','label1','marker1']);assert.equal(s.operands.before.length,14);assert.deepEqual(s.operands.before,s.operands.after);assert.equal(s.live.scene.nodeCount,14);assertFixture(s);});
await test('parent-space conversion does not double-add marker translation or seriesRect',()=>{const f=fixture(),s=f.store.snapshot(),g=geometryTools().convert(s.live.scene);assert.equal(g.legend.x,10);assert.equal(g.items[1].item.x,110);assert.equal(g.items[1].marker.x,105);assert.equal(g.items[1].label.x,126);assert.equal(g.items[1].markerLabelGap,10);assert.equal(geometryTools().gap({x:0,y:20,width:10,height:30},{x:0,y:45,width:10,height:10},'top'),-5);});
await test('lazy BBox operand mutation invalidates complete sample without extra calls',()=>{const f=fixture(),old=f.items[0].getBBox;f.items[0].getBBox=function(){this.marker.x=9;return old.call(this);};const s=f.store.snapshot();assert.equal(s.valid,false);assert.equal(s.reason,'bbox-getter-operands-changed');assert.equal(f.calls.length,7);assert.equal(s.operands.after.length,14);});
await test('wrong marker parent fails before any getter',()=>{const f=fixture();f.items[1].marker.parentNode=f.root;assert.throws(()=>f.store.snapshot(),/scene-unresolved: marker -> symbols/);assert.equal(f.calls.length,0);});
await test('source-ordered second-series identity/visibility mismatches fail closed',()=>{let f=fixture();f.chart.series[1].id='wrong';assert.throws(()=>f.store.snapshot(),/series-identity-mismatch/);f=fixture();f.chart.series[1].visible=false;assert.throws(()=>f.store.snapshot(),/series-visibility-mismatch/);f=fixture();f.chart.series[1].contentGroup.visible=false;assert.throws(()=>f.store.snapshot(),/series-visibility-mismatch/);});
await test('actual visibility and property visibility disagreement remains visible',()=>{const f=fixture();f.chart.series[1].properties.visible=false;const s=f.store.snapshot();assert.equal(s.live.scene.items[1].series.visible.value,true);assert.equal(s.live.scene.items[1].series.properties.visible.value,false);});
await test('raw absent undefined null value stay distinct and no defaults inserted',()=>{const f=fixture();f.model.chartOptions={common:undefined,bar:{legend:{enabled:null,spacing:0}}};const s=f.store.snapshot();assert.equal(s.model.chartOptions.common.namespace.kind,'undefined');assert.equal(s.model.chartOptions.line.namespace.kind,'absent');assert.equal(s.model.chartOptions.bar.legend.enabled.kind,'null');assert.equal(s.model.chartOptions.bar.legend.spacing.value,0);assert.equal(s.model.chartOptions.bar.legend.item.paddingX.kind,'absent');});
await test('ambiguous API candidates and root cardinality stop acquisition',()=>{const f=fixture();document.querySelectorAll=()=>[{__reactFiber:{memoizedProps:{value:{gridRef:{current:{api:f.grid}}}},child:{stateNode:{api:{getChartModels(){}}}}}}];assert.throws(acquire,/ambiguous API/);document.querySelectorAll=()=>[];assert.throws(acquire,/exact grid root/);});
await test('nonfinite transforms and wrong role reject conversion',()=>{let f=fixture(),s=f.store.snapshot();s.live.scene.group.fields.translationX.value=NaN;assert.throws(()=>geometryTools().convert(s.live.scene),/finite translationX/);f=fixture();s=f.store.snapshot();s.live.scene.items[1].symbols.className='Unknown';assert.throws(()=>geometryTools().convert(s.live.scene),/plain Group roles/);});
await test('two inactive equal samples at least 100ms apart',async()=>{const f=fixture(),s=f.store.snapshot();let t=0;const r=await settle({waitForUpdate:async()=>{},sample:async()=>s,now:()=>t,pause:async n=>{t+=n;}});assert.equal(r.settled.count,2);assert(r.settled.pair[1].at-r.settled.pair[0].at>=100);});
await test('invalid getter sample only recovers within existing ten polls',async()=>{const f=fixture(),valid=f.store.snapshot();let t=0,count=0;const r=await settle({waitForUpdate:async()=>{},sample:async()=>++count===1?{valid:false,reason:'bbox-getter-operands-changed',operands:valid.operands}:valid,now:()=>t,pause:async n=>{t+=n;}});assert.equal(r.settled.count,3);assert.equal(r.settled.invalidCount,1);});
await test('changing/active/missing and deadline outcomes never become success',async()=>{let t=0,count=0;await assert.rejects(settle({waitForUpdate:async()=>{},sample:async()=>({valid:true,animationActive:++count%2===0,live:{count}}),now:()=>t,pause:async n=>{t+=n;}}),/settlement-unresolved/);assert.equal(count,10);await assert.rejects(settle({waitForUpdate:async()=>{throw Error('method missing');},sample:async()=>{throw Error('unreachable');}}),/method missing/);t=0;await assert.rejects(settle({waitForUpdate:async()=>{},sample:async()=>{t=6001;return {valid:true,animationActive:false};},now:()=>t,pause:async()=>{}}),/settlement-unresolved/);});
await test('incremental I/O rejects prospective count/byte/JSON/path and reconciles drift',()=>{const directory=fs.mkdtempSync(path.join(os.tmpdir(),'legend-offline-'));
  try{const caps={...limits,json:64,jsonTotal:80,total:120,files:3,png:64},writer=createWriter(directory,{caps});writer.json('one',{a:'x'.repeat(30)});assert.throws(()=>writer.json('two',{b:'x'.repeat(40)}),/Prospective/);assert(!fs.existsSync(path.join(directory,'two.json')));assert.throws(()=>writer.json('huge',{x:'x'.repeat(100)}),/JSON byte/);assert.throws(()=>writer.writeBytes('../escape',Buffer.from('x')),/Unowned/);writer.png('image',Buffer.alloc(60));assert.throws(()=>writer.reservePNG('next',50),/Prospective/);assert.equal(writer.stats().initialScans,1);writer.reconcile();fs.writeFileSync(path.join(directory,'untracked'),Buffer.from('x'));assert.throws(()=>writer.reconcile(),/Untracked/);
  }finally{fs.rmSync(directory,{recursive:true,force:true});}});
await test('event prefix survives bounded persistence and rejects regression',()=>{const saved=[],store=createEventStore((name,value)=>saved.push({name,value}));const values=Array.from({length:17},(_,i)=>({sequence:i+1,action:'c1'}));store.save(values);const writes=saved.length;store.save(values);assert.equal(saved.length,writes);assert.equal(store.last().length,17);assert.throws(()=>store.save(values.slice(1)),/regression/);assert.throws(()=>store.save([{sequence:2}]),/regression/);assert.equal(increment(159,160,'actions'),160);assert.throws(()=>increment(160,160,'actions'),/cap/);});
await test('event action/case/run bounds preserve finite original-order prefixes',()=>{const f=fixture();for(let i=0;i<9;i++)f.store.listener({type:'chartOptionsChanged',chartId:'chart-1',chartOptions:{bar:{legend:{spacing:i}}}});assert.equal(f.store.events.length,8);assert.equal(f.store.events[7].chartOptions.bar.legend.spacing.value,7);assert.match(f.store.overflow.reason,/event bound/);assert.equal(f.store.events[1].deltas.find(d=>d.path==='bar.legend.spacing').before.value,0);});
await test('eight named case actions restore recorded values within counters',async()=>{
  const values={'Font':'Verdana, sans-serif','Size':'11','Position':'Top','Spacing':'20','Marker Size':'11','Marker Stroke':'1','Item Spacing':'5','Horizontal Spacing':'32','Vertical Spacing':'8','Enabled':true},initial=structuredClone(values),ids=[];
  let actions=0,changes=0,observation=0;const control=(name,type)=>({name,type,inputValue:async()=>String(values[name]),textContent:async()=>String(values[name]),isChecked:async()=>values[name]});
  const checkpoint=async()=>({id:'o'+(++observation),snapshot:{effective:structuredClone(values)}});
  const step=async(label,target,method,arg)=>{actions++;const previous=values[target.name];if(method==='press'&&arg==='Space')values[target.name]=!previous;if(method==='press'&&arg==='ArrowRight')values[target.name]=String(Number(previous)+1);if(method==='click'&&target.type==='range')values[target.name]=String(Number(previous)+1);if(previous!==values[target.name])changes++;};
  await executeCases({controls:{inventory:async()=>{},combo:async name=>control(name),numeric:async(name,type)=>control(name,type),enabled:async()=>control('Enabled')},step,
    menu:async(name,value)=>{actions+=2;if(values[name]!==value)changes++;values[name]=value;},number:async(label,value,name=label)=>{actions+=2;if(values[name]!==String(value))changes++;values[name]=String(value);},
    checkpoint,runCase:async(id,fn)=>{ids.push(id);await fn();},record(){},arranged:()=>false});
  assert.deepEqual(ids,['L01','L02','L03','L04','L05','L06','L07','L08']);assert.deepEqual(values,initial);assert(actions<=160);assert(changes<=56);assert(observation<20);
});
const report={scope:'Offline source collector verification only; no browser/container/runtime',status:'passed',tests:results.length,results,node:process.version,fixtureSha256:createHash('sha256').update(fs.readFileSync(new URL('./harness/fixture.json',import.meta.url))).digest('hex')};
fs.writeFileSync(new URL('./offline-verification.json',import.meta.url),JSON.stringify(report,null,2));console.log(JSON.stringify(report));
