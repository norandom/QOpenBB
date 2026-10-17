import {install,geometry} from './harness/projection.mjs';
import {coordinate} from './harness/collector.mjs';
import {controls,expandSeries} from './harness/controls.mjs';

export async function followupChecks(check){
  const element={getClientRects:()=>[{}],getBoundingClientRect:()=>({x:100,y:100,width:400,height:400})};
  function sample(change=()=>{}){
    const root={parentNode:undefined},sr={parentNode:root,translationX:10,translationY:20};
    const managed={parentNode:sr},content={parentNode:managed,translationX:0,translationY:0};
    const s={id:'s',type:'bar',properties:{yKey:'cashFlow'},contentGroup:content,
      getNodeData:()=>[{datumIndex:0,x:20,y:30,width:10,height:20,xValue:{id:'wrapper-0',value:'2024-Q1'},point:{x:25,y:40}}]};
    const c={seriesRect:{x:10,y:20,width:200,height:200},seriesRoot:sr,
      ctx:{scene:{root,width:400,height:400},animationManager:{isActive:()=>false}},series:[s]};
    globalThis.window={};globalThis.document={querySelectorAll:()=>[element]};
    globalThis.getComputedStyle=()=>({visibility:'visible',opacity:'1'});globalThis.devicePixelRatio=1;
    install();window.__tooltipProxy={chart:c};change({root,sr,managed,content,c,s});
    const result=geometry({ordinal:0,key:'cashFlow'});
    check('source representative ctx has no root',!Object.hasOwn(c.ctx,'root'));
    delete globalThis.window;delete globalThis.document;delete globalThis.getComputedStyle;delete globalThis.devicePixelRatio;
    return result;
  }
  const valid=sample(),s=valid.series[0];
  check('scene root accepted with undefined terminal',s.chainValid&&s.nodePresence.sceneRoot&&s.nodeKinds.sceneRoot==='object'&&s.rootTerminal.value.kind==='undefined');
  check('all three links retained',Object.keys(s.links).length===3&&Object.values(s.links).every(Boolean));
  check('all four node presence flags retained',Object.keys(s.nodePresence).length===4&&Object.values(s.nodePresence).every(Boolean));
  check('scene root produces reviewed coordinate',coordinate(valid,0,'cashFlow','groupedColumn').point.x===135);
  const rejection=(name,g)=>{let rejected=false;try{coordinate(g,0,'cashFlow','groupedColumn');}catch{rejected=true;}check(name,rejected);};
  for(const [name,change] of [
    ['contentToManaged',({content})=>content.parentNode=content],
    ['managedToSeriesRoot',({managed})=>managed.parentNode={}],
    ['seriesRootToSceneRoot',({sr})=>sr.parentNode={}],
  ]){const bad=sample(change);check('individual failed link receipt '+name,bad.series[0].links[name]===false&&!bad.series[0].chainValid);
    rejection('individual link stops coordinate '+name,bad);}
  for(const rootValue of [null,undefined]){const bad=sample(({c})=>c.ctx.scene.root=rootValue),node=bad.series[0];
    check('missing scene root typed '+String(rootValue),!node.nodePresence.sceneRoot&&node.nodeKinds.sceneRoot===(rootValue===null?'null':'undefined')&&!node.links.seriesRootToSceneRoot&&!node.terminalValid);
    rejection('missing scene root stops coordinate '+String(rootValue),bad);}
  const terminal=sample(({root})=>root.parentNode={});check('extra root parent receipt',!terminal.series[0].terminalValid&&terminal.series[0].rootTerminal.value.kind==='nonterminal-object');
  rejection('extra root parent stops coordinate',terminal);
  for(const primitive of [0,false,'root']){const bad=sample(({c,sr})=>{c.ctx.scene.root=primitive;sr.parentNode=primitive;});
    check('primitive scene root typed '+String(primitive),bad.series[0].nodePresence.sceneRoot&&bad.series[0].nodeKinds.sceneRoot===typeof primitive&&!bad.series[0].chainValid);
    rejection('primitive scene root stops coordinate '+String(primitive),bad);}
  for(const key of Object.keys(s.links)){const bad=structuredClone(valid);bad.series[0].links[key]=false;
    rejection('coordinate checks individual link despite aggregate true '+key,bad);}
  for(const key of Object.keys(s.nodePresence)){const bad=structuredClone(valid);bad.series[0].nodePresence[key]=false;
    rejection('coordinate checks individual presence despite aggregate true '+key,bad);}
  for(const key of Object.keys(s.nodeKinds)){const bad=structuredClone(valid);bad.series[0].nodeKinds[key]='number';
    rejection('coordinate checks individual node kind despite aggregate true '+key,bad);}
  for(const initial of ['true','false',null,'expanded']){
    let state=initial,clicks=0;const receipts=[];
    const heading={getAttribute:async name=>{if(name!=='aria-expanded')throw Error('Wrong expansion source');return state;}};
    let failed=false;try{await expandSeries(heading,async()=>{clicks++;state='true';},r=>receipts.push(r));}catch{failed=true;}
    check('aria expansion state '+String(initial),['true','false'].includes(initial)?!failed&&clicks===(initial==='false'?1:0)&&receipts.at(-1).after==='true':failed&&clicks===0&&receipts.length===1);
    check('aria expansion before retained '+String(initial),receipts[0].before===initial);
  }
  const stuck=[];let failure=false;try{await expandSeries({getAttribute:async()=> 'false'},async()=>{},r=>stuck.push(r));}catch{failure=true;}
  check('failed expansion retained and stopped',failure&&stuck.at(-1).after==='false');
  for(const [label,names,expected] of [
    ['unique',['Grouped Column. Selected','Stacked Column','Line','Other'],true],
    ['selected suffix',['Grouped Column','Stacked Column. Selected','Line'],true],
    ['absent',['Grouped Column','Line'],false],
    ['ambiguous',['Stacked Column','Stacked Column. Selected'],false],
    ['nearby wrong name',['Grouped Column','100% Stacked Column','Stacked Column chart'],false],
  ]){
    const result=await familyCase(names);check('thumbnail '+label,result.clicked===expected&&result.failed===!expected);
    check('thumbnail inventory narrow '+label,result.inventory.every(x=>/^(Grouped Column|Stacked Column)(\. Selected)?$/.test(x.name)));
    check('thumbnail inventory retained before resolution '+label,result.receipts.length===2&&result.receipts[0].kind==='column-thumbnail-count');
  }
  const overflow=await familyCase(Array(33).fill('Stacked Column'));
  check('thumbnail prospective cap stops mapping',overflow.failed&&!overflow.clicked&&overflow.mapped===0&&overflow.receipts.length===1&&overflow.receipts[0].count===33);
}

async function familyCase(names){
  const receipts=[],clicks=[];let mapped=0;
  const select=(role,options)=>{
    const matches=role==='button'?names.filter(n=>typeof options.name==='string'?n===options.name:options.name.test(n)):[options.name];
    return {waitFor:async()=>{if(matches.length!==1)throw Error('Unique target');},count:async()=>matches.length,
      evaluateAll:async fn=>{mapped++;return fn(matches.map(name=>({getClientRects:()=>[{}],getAttribute:k=>k==='aria-label'?name:null,textContent:name})));},matches};
  };
  const panel={isVisible:async()=>true,getByRole:select};
  const page={locator:selector=>{if(selector!=='.ag-chart-docked-container')throw Error('Unexpected selector');return panel;}};
  let failed=false;try{await controls(page,async(label,locator)=>clicks.push({label,matches:locator.matches}),r=>receipts.push(r)).family('stackedColumn');}catch{failed=true;}
  return {failed,mapped,clicked:clicks.some(x=>x.label==='Family stackedColumn'),receipts,inventory:receipts.find(r=>r.kind==='column-thumbnails')?.thumbnails??[]};
}
