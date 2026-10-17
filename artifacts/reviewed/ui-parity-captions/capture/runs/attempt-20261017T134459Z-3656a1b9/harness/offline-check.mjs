import assert from 'node:assert/strict';
import {installProjection} from './projection.mjs';
const events={},rows=Array.from({length:4},(_,index)=>({period:'2024-Q'+(index+1),revenue:100+20*index,
  operatingIncome:[20,25,30,40][index]}));
const selection={each(){}};
const axes=[{type:'category',position:'bottom',tickLabelGroupSelection:selection},
  {type:'number',position:'left',tickLabelGroupSelection:selection}];
const series=[{xKey:'period',yKey:'revenue',labelSelection:selection},
  {xKey:'period',yKey:'operatingIncome',labelSelection:selection}];
const raw={chartId:'offline-only',chartType:'groupedColumn',chartThemeName:'dark',
  cellRange:{columns:['period','revenue','operatingIncome']},
  chartOptions:{bar:{title:{fontWeight:400},subtitle:{fontStyle:undefined}}}};
const processed={data:rows,axes,series,title:{fontWeight:400,fontStyle:'normal'}};
const parentPrototype={visible:true,opacity:0.5};
const parentNode=Object.assign(Object.create(parentPrototype),{id:'offline-parent',translationX:7,parentNode:undefined});
const captionNode={id:'offline-caption',text:'Offline',visible:true,parentNode,
  getBBox:()=>({x:0,y:0,width:1,height:1})};
globalThis.window={__referenceGrid:{getChartModels:()=>[raw],addEventListener:(name,callback)=>{events[name]=callback;}},
  __referenceProxy:{getOptions:()=>({data:rows}),chart:{axes,series,chartOptions:{processedOptions:processed},
    title:{node:captionNode},ctx:{animationManager:{isActive:()=>false}}}}};
globalThis.document={querySelectorAll:()=>[],querySelector:()=>({getBoundingClientRect:()=>({x:0,y:0,width:1,height:1})})};
globalThis.devicePixelRatio=1;
installProjection();
const state=window.__captions.snapshot();
assert.deepEqual(state.model.chartOptions.bar.title.fontWeight,{own:true,in:true,kind:'value',type:'number',value:400});
assert.equal(state.model.chartOptions.bar.title.fontStyle.kind,'absent');
assert.equal(state.model.chartOptions.bar.subtitle.fontStyle.kind,'undefined');
assert.equal(state.model.chartOptions.bar.subtitle.fontStyle.own,true);
assert.equal(state.effective.title.fontStyle.value,'normal');
assert.equal(state.scene.title.node.parentLink.field,'parentNode');
assert.equal(state.scene.title.node.ancestors.length,1);
assert.equal(state.scene.title.node.ancestors[0].fields.visible.own,false);
assert.equal(state.scene.title.node.ancestors[0].fields.opacity.value,0.5);
assert.equal(state.scene.title.node.ancestors[0].fields.translationX.value,7);
for(let index=0;index<8;index++)events.chartOptionsChanged({chartOptions:raw.chartOptions});
assert.equal(window.__captions.events.length,8);
events.chartOptionsChanged({chartOptions:raw.chartOptions});
assert.equal(window.__captions.overflow.kind,'event-bound');
assert.throws(()=>window.__captions.snapshot(),/event-bound/);
installProjection();processed.title.fontWeight=Infinity;
assert.throws(()=>window.__captions.snapshot(),/nonfinite/);
processed.title.fontWeight=400;
let deepParent=captionNode;
for(let index=0;index<9;index++){deepParent.parentNode={visible:true};deepParent=deepParent.parentNode;}
assert.throws(()=>window.__captions.snapshot(),/ancestor bound/);
console.log('Offline projection checks passed: numeric400, absent/undefined, processed separation, event overflow, nonfinite rejection, parentNode inherited visibility/transform and eight-ancestor cap.');
