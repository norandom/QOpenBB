export function install(){
  const limit=(a,n,k)=>{if(!Array.isArray(a)||a.length>n)throw Error('Array bound '+k);return a;};
  const scalar=(v,k)=>{if(v===null||typeof v==='boolean'||typeof v==='number'&&Number.isFinite(v)||typeof v==='string'&&v.length<=512)return v;throw Error('Scalar '+k);};
  const presence=(o,k)=>({own:o!=null&&Object.hasOwn(o,k),in:o!=null&&k in Object(o),
    kind:o==null||!(k in Object(o))?'absent':o[k]===undefined?'undefined':o[k]===null?'null':'value',type:o==null||!(k in Object(o))?'absent':typeof o[k]});
  const field=(o,k)=>({...presence(o,k),...(o?.[k]!==undefined?{value:scalar(o[k],k)}:{})});
  const pick=(o,keys)=>Object.fromEntries(keys.map(k=>[k,field(o,k)]));
  const array=(o,k,n,project)=>({...presence(o,k),...(o?.[k]!=null?{value:limit(o[k],n,k).map(project)}:{})});
  const nested=(o,k,project)=>({presence:presence(o,k),value:project(o?.[k])});
  const dash=o=>array(o,'lineDash',8,x=>scalar(x,'dash'));
  const style=o=>({...pick(o,['stroke','strokeWidth','fill','fillOpacity']),lineDash:dash(o)});
  const line=o=>pick(o,['enabled','stroke','width']);
  const tick=o=>pick(o,['enabled','stroke','width','size']);
  const label=o=>({...pick(o,['enabled','fontFamily','fontSize','fontWeight','fontStyle','color','spacing','padding','autoRotate','rotation','format']),
    formatter:{...presence(o,'formatter'),...(typeof o?.formatter==='function'?{name:scalar(o.formatter.name.length<=128?o.formatter.name:undefined,'formatter.name')}:{})}});
  const grid=o=>({...pick(o,['enabled','width']),style:array(o,'style',4,style)});
  const axis=o=>({...pick(o,['type','position']),tick:nested(o,'tick',tick),label:nested(o,'label',label),line:nested(o,'line',line),gridLine:nested(o,'gridLine',grid),keys:array(o,'keys',3,x=>scalar(x,'key'))});
  const axisOverride=o=>({...axis(o),positions:Object.fromEntries(['top','bottom','left','right'].map(k=>[k,nested(o,k,axis)]))});
  const options=o=>Object.fromEntries(['common','bar'].map(k=>[k,{presence:presence(o,k),axes:Object.fromEntries(['category','number','time'].map(t=>[t,nested(o?.[k]?.axes,t,axisOverride)]))}]));
  const dataValue=v=>{if(v instanceof Date)return {type:'Date',milliseconds:v.getTime(),iso:v.toISOString()};
    if(v!==null&&typeof v==='object')return {type:'category-wrapper',fields:pick(v,['id','value'])};return {type:typeof v,value:scalar(v,'period')};};
  const rows=o=>array(o,'data',4,r=>({period:{...presence(r,'period'),...(r.period!==undefined?{value:dataValue(r.period)}:{})},amounts:pick(r,['revenue','operatingIncome'])}));
  const series=o=>({...pick(o,['type','xKey','yKey','yName','id']),data:rows(o)});
  const envelope=o=>({axes:array(o,'axes',2,axis),data:rows(o),series:array(o,'series',2,series),themeOverrides:options(o?.theme?.overrides)});
  const model=o=>({...pick(o,['chartId','chartType','chartThemeName','switchCategorySeries','aggFunc']),chartOptions:options(o?.chartOptions),
    cellRange:{...pick(o?.cellRange,['rowStartIndex','rowEndIndex','rowStartPinned','rowEndPinned']),columns:array(o?.cellRange,'columns',3,x=>scalar(x,'column'))}});
  const nodeKeys=['id','visible','opacity','x','y','x1','y1','x2','y2','stroke','strokeWidth','strokeOpacity','text','fill','fontFamily','fontSize','fontWeight','fontStyle',
    'textAlign','textBaseline','rotation','rotationCenterX','rotationCenterY','translationX','translationY','scalingX','scalingY'];
  const parentKeys=['id','visible','opacity','rotation','rotationCenterX','rotationCenterY','translationX','translationY','scalingX','scalingY'];
  const datumKeys=['tickId','tickLabel','tickLabelFormatted','text','visible','translation','x','y','x1','y1','x2','y2','rotation','rotationCenterX','rotationCenterY','stroke','strokeWidth'];
  const rect=n=>n?pick(n.getBoundingClientRect(),['x','y','width','height','top','right','bottom','left']):null;
  const visible=n=>!!n&&!!n.getClientRects().length&&getComputedStyle(n).visibility!=='hidden';
  const text=v=>v==null?null:scalar(String(v),'DOM text');
  const el=n=>n?{tag:n.tagName,type:n.type??null,role:n.getAttribute('role'),ref:n.getAttribute('data-ref'),
    label:text((n.getAttribute('aria-label')||n.getAttribute('aria-labelledby')?.split(' ').map(id=>document.getElementById(id)?.textContent||'').join(' ')||
      n.closest('.ag-slider,.ag-field')?.querySelector('label')?.textContent||'').trim()),id:n.id,controls:n.getAttribute('aria-controls'),
    checked:n.checked??null,disabled:n.disabled??null,value:text(n.value),selected:text(n.textContent?.trim()),
    min:n.min??null,max:n.max??null,step:n.step??null,visible:visible(n),rect:rect(n),
    inViewport:!!n&&n.getBoundingClientRect().bottom>0&&n.getBoundingClientRect().top<innerHeight&&n.getBoundingClientRect().right>0&&n.getBoundingClientRect().left<innerWidth}:null;
  const store={limit,presence,pick,axis,options,envelope,model,rect,el,events:[],action:'setup',caseEvents:0,actionEvents:0,overflow:null};
  store.snapshot=()=>{
    if(store.overflow)throw Error('Event failure '+JSON.stringify(store.overflow));
    const chart=window.__axisProxy.chart,processed=chart.chartOptions.processedOptions,ancestors=[],ancestorIds=new Map(),nodes=[],nodeIds=new Map();
    const parent=p=>{if(ancestorIds.has(p))return ancestorIds.get(p);if(ancestors.length>=96)throw Error('Ancestor bound');
      const id='p'+ancestors.length;ancestorIds.set(p,id);ancestors.push({identity:id,fields:pick(p,parentKeys),parentLink:presence(p,'parentNode')});return id;};
    const node=(n,d)=>{if(!n)throw Error('Required named scene node missing');if(nodeIds.has(n))return nodeIds.get(n);
      if(nodes.length>=136)throw Error('Node bound');const id='n'+nodes.length;nodeIds.set(n,id);const parents=[];
      let p=n.parentNode;for(let depth=0;p&&depth<8;depth++,p=p.parentNode)parents.push(parent(p));if(p)throw Error('Ancestor depth bound');
      if(!parents.length)throw Error('Vacuous scene ancestry');if(typeof n.getBBox!=='function')throw Error('getBBox unavailable');
      nodes.push({identity:id,fields:pick(n,nodeKeys),lineDash:dash(n),parentLink:presence(n,'parentNode'),parents,
        bbox:pick(n.getBBox(),['x','y','width','height']),coordinateSpace:'getBBox parent space; local scene transforms; no guessed canvas coordinates',datum:pick(d??n.datum,datumKeys)});return id;};
    const selection=s=>{if(typeof s?.each!=='function')throw Error('Required named selection missing');const out=[];
      s.each((n,d)=>{if(out.length>=32)throw Error('Tick selection bound');out.push(node(n,d));});return out;};
    const axes=limit(chart.axes,2,'live axes').map(a=>({identity:pick(a,['type','direction','position','id']),style:axis(a),
      lineNode:node(a.lineNode),tickLineGroup:node(a.tickLineGroup),tickLabelGroup:node(a.tickLabelGroup),
      ticks:selection(a.tickLineGroupSelection),labels:selection(a.tickLabelGroupSelection)}));
    const groups=limit([...document.querySelectorAll('[data-ref="axisGroup"]')],2,'axis groups').map(g=>({
      name:text(g.querySelector('.ag-charts-format-top-level-group-title')?.textContent.trim()),rect:rect(g),visible:visible(g),
      controls:limit([...g.querySelectorAll('input,[role="combobox"]')],48,'axis controls').map(el),
      sliders:limit([...g.querySelectorAll('.ag-slider')],16,'sliders').map(s=>({label:text(s.querySelector('label[data-ref="eLabel"]')?.textContent.trim()),rect:rect(s)})),
      rotationCircle:rect(g.querySelector('.ag-angle-select'))}));
    const canvases=limit([...document.querySelectorAll('.ag-charts-canvas canvas')],8,'canvases');
    const popupNodes=limit([...document.querySelectorAll('[role="listbox"]')].filter(visible),1,'visible popup');
    const popup=popupNodes.map(p=>({id:p.id,rect:rect(p),options:limit([...p.querySelectorAll('[role="option"]')].filter(visible),24,'popup options').map(el)}));
    return {model:model(window.__axisGrid.getChartModels()[0]),explicit:envelope(window.__axisProxy.getOptions()),effective:envelope(processed),
      live:{axes,nodes,ancestors},geometry:{seriesRect:pick(chart.seriesRect,['x','y','width','height']),padding:pick(chart.padding,['top','right','bottom','left']),
        canvas:canvases.map(c=>({css:rect(c),backing:pick(c,['width','height'])})),dpr:devicePixelRatio,editor:rect(document.querySelector('.ag-chart-docked-container'))},
      dom:{groups,popup,active:el(document.activeElement),scrollOwner:{tag:document.scrollingElement?.tagName,top:document.scrollingElement?.scrollTop,left:document.scrollingElement?.scrollLeft}},
      eventSequence:store.events.length,settled:{animationActive:chart.ctx.animationManager.isActive()}};
  };
  window.__axis=store;
}
export function acquire(){
  const roots=document.querySelectorAll('.ag-root-wrapper');if(roots.length<1||roots.length>4)throw Error('Grid root bound');let api=null;
  for(const root of roots){let f=root[Object.keys(root).find(k=>k.startsWith('__reactFiber'))];
    for(let depth=0;f&&depth<18;depth++,f=f.return){const c=f.memoizedProps?.value?.gridRef?.current?.api||f.child?.stateNode?.api;
      if(typeof c?.getChartModels==='function'){if(api&&api!==c)throw Error('Ambiguous grid');api=c;}}}
  if(!api)throw Error('Grid API missing');const models=api.getChartModels();if(models.length!==1)throw Error('Exact one model');
  const proxy=api.getChartRef(models[0].chartId)?.chart;if(typeof proxy?.getOptions!=='function'||typeof proxy?.waitForUpdate!=='function')throw Error('Named getters missing');
  window.__axisGrid=api;window.__axisProxy=proxy;const p=window.__axis;
  if(!p.listener){p.listener=e=>{try{if(p.events.length>=256||p.caseEvents>=64||p.actionEvents>=8)throw Error('Event bound');
    p.events.push({sequence:p.events.length+1,action:p.action,identity:p.pick(e,['type','chartId','chartType','chartThemeName']),chartOptions:p.options(e.chartOptions)});p.caseEvents++;p.actionEvents++;
  }catch(error){p.overflow={message:error.message,action:p.action};}};api.addEventListener('chartOptionsChanged',p.listener);}
  return p.model(models[0]);
}
