import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {install,acquire} from './projection.mjs';
const base=path.resolve(new URL('..',import.meta.url).pathname),checks=[];
const assert=(condition,label)=>{if(!condition)throw Error(label);checks.push(label);};
const hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');
assert(hash(base+'/../plan.md')==='f4247a1eb9447f5dd2bd8d3faab6013655ddca95039863b565958a7e09952cb8','frozen amended plan');
globalThis.window={};install();const p=window.__axis;
const longContainer={tagName:'DIV',getAttribute:()=>null,get textContent(){throw Error('Container text must never be read');}};
assert(p.active(longContainer).tag==='DIV'&&Object.keys(p.active(longContainer)).join()==='tag,type,ref,label','active container uses only admitted fields');
let longLabel=false;try{p.active({tagName:'DIV',getAttribute:k=>k==='aria-label'?'x'.repeat(513):null});}catch{longLabel=true;}
assert(longLabel,'admitted active label retains strict 512-character bound');
const inherited=Object.create({position:'bottom'});inherited.type=undefined;inherited.tick={enabled:null,width:3};
const a=p.axis(inherited);assert(a.position.own===false&&a.position.value==='bottom','inherited scalar');
const wholeTable=p.model({cellRange:{rowStartIndex:null,rowEndIndex:null,columns:['period','revenue','operatingIncome']}});
assert(wholeTable.cellRange.rowStartIndex.kind==='null'&&wholeTable.cellRange.rowEndIndex.kind==='null','whole-table model bounds remain null');
assert(a.type.kind==='undefined'&&a.label.value.rotation.kind==='absent'&&a.tick.value.enabled.kind==='null','undefined absent null distinct');
assert(p.envelope({axes:[{type:'time',label:{format:'%Y-%m-%d'}}]}).axes.value[0].label.value.format.value==='%Y-%m-%d','explicit axes format projection');
const model={chartId:'synthetic',chartType:'groupedColumn',chartOptions:{},cellRange:{rowStartIndex:0,rowEndIndex:3,columns:['period','revenue','operatingIncome']}};
const proxy={getOptions:()=>({}),waitForUpdate:async()=>{}};
const api={getChartModels:()=>[model],getChartRef:()=>({chart:proxy}),addEventListener:()=>{}};
const root={__reactFiberTest:{memoizedProps:{value:{gridRef:{current:{api}}}}}};
globalThis.document={querySelectorAll:()=>[root]};acquire();
for(let i=0;i<8;i++)p.listener({type:'chartOptionsChanged',chartId:'synthetic',chartOptions:{}});
assert(p.events.length===8&&!p.overflow,'eight ordered options events retained');p.listener({type:'chartOptionsChanged',chartOptions:{}});
assert(p.events.length===8&&!!p.overflow,'ninth event fails closed');
p.overflow=null;
const inheritedParent=Object.create({visible:false,opacity:0.5});inheritedParent.parentNode=null;
const parent={visible:true,opacity:1,parentNode:inheritedParent};
const sceneNode=()=>({visible:true,opacity:1,parentNode:parent,getBBox:()=>({x:0,y:0,width:10,height:1})});
const mockAxis=direction=>({type:direction==='x'?'category':'number',direction,position:direction==='x'?'bottom':'left',
  lineNode:sceneNode(),tickLineGroup:sceneNode(),tickLabelGroup:sceneNode(),
  tickLineGroupSelection:{each:fn=>fn(sceneNode(),{tickId:'0',tickLabel:'Q1'})},tickLabelGroupSelection:{each:fn=>fn(sceneNode(),{tickId:'0',tickLabel:'Q1'})}});
proxy.chart={axes:[mockAxis('x'),mockAxis('y')],chartOptions:{processedOptions:{}},seriesRect:{x:1,y:2,width:3,height:4},padding:{top:1,right:2,bottom:3,left:4},ctx:{animationManager:{isActive:()=>false}}};
globalThis.devicePixelRatio=1;document.querySelectorAll=selector=>selector==='.ag-root-wrapper'?[root]:[];document.querySelector=()=>null;
const scene=p.snapshot();assert(scene.live.nodes.length===10&&scene.live.ancestors.length===2,'bounded node selection and deduplicated ancestry');
assert(scene.live.nodes.every(n=>n.parents.length===2)&&scene.live.ancestors[1].fields.visible.value===false&&scene.live.ancestors[1].fields.opacity.own===false,'nonvacuous parentNode inherited visibility');
proxy.chart.axes[0].lineNode.parentNode=null;let vacuous=false;try{p.snapshot();}catch{vacuous=true;}assert(vacuous,'empty ancestry refused');
const fixtures=JSON.parse(fs.readFileSync(base+'/harness/fixtures.json'));
assert(fixtures.B.periods.every((n,i)=>new Date(n).toISOString()===fixtures.B.utcQuarterStarts[i]),'numeric UTC quarter mapping');
assert(fixtures.revenue.join()==='100,120,140,160'&&fixtures.operatingIncome.join()==='20,25,30,40','finite financial amounts');
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'qopenbb-axis-'));process.env.CAPTURE_ROOT=temp;
try{const io=await import('./io.mjs');io.json('rewrite',{long:'1234567890'});io.json('rewrite',{x:1});
  assert(io.budget().bytes===fs.statSync(temp+'/rewrite.json').size,'retained bytes count overwrites once');
  for(const [label,cap] of [['actions',240],['changes',80],['checkpoints',96]]){assert(io.increment(cap-1,cap,label)===cap,label+' boundary allowed');
    let stopped=false;try{io.increment(cap,cap,label);}catch{stopped=true;}assert(stopped,label+' overflow refused');}
  let refused=false;try{io.json('oversize',{x:'x'.repeat(2097152)});}catch{refused=true;}
  assert(refused&&!fs.existsSync(temp+'/oversize.json'),'JSON overbound refused before write');
}finally{fs.rmSync(temp,{recursive:true,force:true});}
const journey=fs.readFileSync(base+'/harness/journey.mjs','utf8');
assert(journey.includes('delete chartState.case')&&journey.includes('JSON.stringify(chartState)')&&!journey.includes('delete chartState.eventSequence'),'event count forces distinct full checkpoint');
assert(journey.includes("await checkpoint('before-'+actions)")&&journey.includes("await checkpoint('after-'+actions)"),'fresh per raw action chart reads');
const inventory={checkpointFiles:96,pngFiles:64,harnessFiles:12,observationChunks:64,eventChunks:16,otherReceipts:35,totalFiles:287,
  perJsonBytes:2097152,totalBytes:167772160,rawActions:180,fieldEdits:61,observationsPerChunk:16,failClosedAtAllCaps:true};
assert(Object.values(inventory).length>0&&inventory.totalFiles<=320,'bounded output file inventory');
assert(Buffer.byteLength(JSON.stringify(Array.from({length:16},()=>({chartOptions:p.options({})}))))<2097152,'sixteen finite event projections fit one JSON chunk');
const report={status:'passed',checks,inventory,runtimeExecuted:false,originalApplicationStarted:false};
fs.writeFileSync(base+'/static-verification.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));
