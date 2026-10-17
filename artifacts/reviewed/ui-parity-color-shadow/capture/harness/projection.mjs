export function install(){
  const limit=(items,max,label)=>{if(items.length>max)throw Error(label+' overflow '+items.length);return items;};
  const scalar=v=>v===null||['string','boolean'].includes(typeof v)||typeof v==='number'&&Number.isFinite(v);
  const text=v=>{if(v==null)return null;v=String(v);if(v.length>256)throw Error('Text overflow');return v;};
  const presence=(o,k)=>{const present=o!=null&&k in Object(o),v=o?.[k];return {own:Object.hasOwn(o??{},k),presence:!present?'absent':v===undefined?'undefined':v===null?'null':'value'};};
  function field(o,k){const present=o!=null&&k in Object(o),v=o?.[k];
    if(present&&v!==undefined&&!scalar(v))throw Error('Nonfinite scalar '+k);
    return {...presence(o,k),...(v!==undefined?{value:v}:{})};}
  const pick=(o,keys)=>Object.fromEntries(keys.map(k=>[k,field(o,k)]));
  const numeric=v=>v==null?null:limit(v,16,'numeric array').map(x=>{if(typeof x!=='number'||!Number.isFinite(x))throw Error('Nonfinite array');return x;});
  const style=o=>({...pick(o,['stroke','strokeWidth','strokeOpacity','opacity']),lineDash:numeric(o?.lineDash),lineDashPresence:o?Object.hasOwn(o,'lineDash'):false});
  const line=o=>pick(o,['enabled','stroke','width']);
  const grid=o=>({...pick(o,['enabled','width']),stylePresence:presence(o,'style'),
    style:o?.style==null?null:limit(o.style,16,'grid styles').map(style)});
  const shadow=o=>pick(o,['enabled','color','blur','xOffset','yOffset']);
  const marker=o=>pick(o,['enabled','fill','stroke','fillOpacity','strokeOpacity','strokeWidth','size','shape']);
  const series=o=>({...pick(o,['type','id','xKey','yKey','fill','stroke','fillOpacity','strokeOpacity','strokeWidth']),marker:marker(o?.marker),shadow:shadow(o?.shadow)});
  const axis=o=>({...pick(o,['type','position']),line:line(o?.line),gridLine:grid(o?.gridLine)});
  const axisOverride=o=>({...axis(o),...Object.fromEntries(['left','right','top','bottom'].map(k=>[k,axis(o?.[k])]))});
  const branch=o=>({axes:Object.fromEntries(['category','number','time','grouped-category'].map(k=>[k,axisOverride(o?.axes?.[k])])),series:series(o?.series)});
  const options=o=>Object.fromEntries(['common','bar','line'].map(k=>[k,{presence:o&&Object.hasOwn(o,k)?'own':'absent',value:branch(o?.[k])}]));
  const model=o=>({...pick(o,['chartType','chartThemeName']),chartOptions:options(o?.chartOptions)});
  const parents=o=>{const result=[];for(let p=o?.parentNode;p;p=p.parentNode){if(result.length>=8)throw Error('Parent overflow');result.push(pick(p,['visible','opacity']));}return result;};
  const node=o=>({...pick(o,['x','y','width','height','x1','x2','y1','y2','translationX','translationY','fill','stroke',
    'strokeWidth','visible','opacity','fillOpacity','strokeOpacity']),lineDash:numeric(o?.lineDash),parents:parents(o),fillShadow:shadow(o?.fillShadow)});
  const visible=n=>!!n&&!!n.getClientRects().length&&getComputedStyle(n).visibility!=='hidden';
  const rect=n=>{if(!n)return null;const r=n.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height};};
  const label=n=>text((n?.getAttribute('aria-label')||n?.getAttribute('aria-labelledby')?.split(' ').map(id=>document.getElementById(id)?.textContent).join(' ')||
    n?.closest('.ag-slider,.ag-field')?.querySelector('label')?.textContent||'').trim());
  const el=n=>n?{tag:n.tagName,type:n.type||null,role:n.getAttribute('role'),label:label(n),id:n.id||null,class:text(n.className),
    dataRef:n.getAttribute('data-ref'),tabindex:n.getAttribute('tabindex'),expanded:n.getAttribute('aria-expanded'),ariaDisabled:n.getAttribute('aria-disabled'),
    ariaInvalid:n.getAttribute('aria-invalid'),labelledby:n.getAttribute('aria-labelledby'),checked:n.checked??null,value:text(n.value),
    min:n.min??null,max:n.max??null,step:n.step??null,readOnly:n.readOnly??null,disabled:n.disabled??null,visible:visible(n),rect:rect(n),
    validity:n.validity?{valid:n.validity.valid,customError:n.validity.customError,validationMessage:text(n.validationMessage)}:null}:null;
  window.__color={limit,pick,axis,series,node,options,model,shadow,visible,rect,el,events:[],action:'setup',overflow:false};
}
export function acquire(){
  const roots=document.querySelectorAll('.ag-root-wrapper');if(roots.length!==1)throw Error('Expected one grid');
  let f=roots[0][Object.keys(roots[0]).find(k=>k.startsWith('__reactFiber'))],api=null;
  for(let depth=0;f&&depth<18;depth++,f=f.return){const v=f.memoizedProps?.value,c=v?.gridRef?.current?.api||f.child?.stateNode?.api;
    if(typeof c?.getChartModels==='function')api=c;}
  if(!api)throw Error('GridApi unavailable');
  const models=api.getChartModels();if(models.length!==1)throw Error('Expected one chart model');
  const proxy=api.getChartRef(models[0].chartId)?.chart;if(!proxy?.chart?.chartOptions?.processedOptions)throw Error('Chart unavailable');
  window.__colorGrid=api;window.__colorProxy=proxy;
  if(!window.__color.listener){const p=window.__color;p.listener=e=>{if(p.events.length>=64){p.overflow=true;return;}
    p.events.push({sequence:p.events.length+1,action:p.action,type:e.type,...p.pick(e,['chartType','chartThemeName']),chartOptions:p.options(e.chartOptions)});};
    api.addEventListener('chartOptionsChanged',p.listener);}
  return {chartType:models[0].chartType,chartThemeName:models[0].chartThemeName};
}
export function read(){
  const p=window.__color,chart=window.__colorProxy.chart,processed=chart.chartOptions.processedOptions;
  if(p.overflow)throw Error('Event overflow');
  const axes=p.limit(chart.axes,2,'axes').map(a=>{const grids=[];a.gridLineGroupSelection.each((n,d)=>grids.push({node:p.node(n),datum:p.pick(d,['stroke','strokeWidth'])}));
    return {...p.axis(a),lineNode:p.node(a.lineNode),gridNodes:p.limit(grids,16,'grid nodes')};});
  let total=0;const series=p.limit(chart.series,2,'series').map(s=>{if(!s.datumSelection?.each)throw Error('Unsupported datumSelection');const nodes=[];
    s.datumSelection.each(n=>nodes.push(p.node(n)));total+=nodes.length;p.limit(nodes,4,'series rects');return {properties:p.series(s.properties),nodes};});
  if(total!==8)throw Error('Expected eight bar rectangles, got '+total);
  const groups=[...document.querySelectorAll('.ag-charts-format-top-level-group')].filter(g=>['Horizontal Axis','Vertical Axis','Series']
    .includes(g.querySelector('.ag-charts-format-top-level-group-title-bar')?.textContent.trim()));p.limit(groups,3,'groups');
  const controls=[];const selectors='[data-ref=axisColorInput] .ag-picker-field-wrapper,[data-ref=gridLineColorPicker] .ag-picker-field-wrapper,'+
    '[data-ref=shadowGroup] input,[data-ref=shadowGroup] .ag-picker-field-wrapper';
  const dom=groups.map(g=>({name:g.querySelector('.ag-charts-format-top-level-group-title-bar').textContent.trim(),visible:p.visible(g),rect:p.rect(g),
    controls:[...g.querySelectorAll(selectors)].map(n=>{const r=p.el(n);controls.push(r);return r;})}));p.limit(controls,48,'controls');
  const popup=document.querySelector('.ag-color-panel'),popupNodes=popup?[...popup.querySelectorAll('.ag-spectrum-color,.ag-spectrum-slider,input,.ag-recent-colors>*')]:[];
  p.limit(popupNodes,16,'popup records');const recent=popup?[...popup.querySelectorAll('.ag-recent-colors>*')]:[];p.limit(recent,8,'swatches');
  const active=p.el(document.activeElement),ancestors=[];for(let n=document.activeElement?.parentElement;n&&ancestors.length<8;n=n.parentElement)ancestors.push(p.el(n));
  return {model:p.model(window.__colorGrid.getChartModels()[0]),effective:{axes:p.limit(processed.axes,2,'processed axes').map(p.axis),
    series:p.limit(processed.series,2,'processed series').map(p.series)},live:{axes,series},generatedCombined:{available:false,reason:'No existing documented finite merge seam'},
    eventSequence:p.events.length,geometry:{chart:p.rect(document.querySelector('.ag-charts-canvas')),panel:p.rect(document.querySelector('.ag-chart-docked-container')),
      plot:chart.seriesRect?{x:chart.seriesRect.x,y:chart.seriesRect.y,width:chart.seriesRect.width,height:chart.seriesRect.height}:null,
      pixelRatio:chart.scene?.canvas?.pixelRatio??window.devicePixelRatio},
    dom:{groups:dom,popup:popup?{rect:p.rect(popup),records:popupNodes.map(p.el),swatches:recent.map(n=>({color:getComputedStyle(n).backgroundColor,rect:p.rect(n)}))}:null,
      active,ancestors},settled:{animationActive:chart.ctx.animationManager.isActive()}};
}
