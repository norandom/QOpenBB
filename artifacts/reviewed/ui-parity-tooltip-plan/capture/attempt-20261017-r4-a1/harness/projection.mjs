export function install(){
  const cap=(a,n,label)=>{if(!Array.isArray(a)||a.length>n)throw Error(label+' bound');return a;};
  const scalar=v=>v===null||['string','boolean'].includes(typeof v)||typeof v==='number'&&Number.isFinite(v);
  const field=(o,k)=>{const own=Object.hasOwn(o??{},k),v=o?.[k];if(v!==undefined&&!scalar(v))throw Error('Non-scalar '+k);
    return {own,kind:!(k in Object(o??{}))?'absent':v===undefined?'undefined':v===null?'null':'value',...(v!==undefined?{value:v}:{})};};
  const pick=(o,ks)=>Object.fromEntries(ks.map(k=>[k,field(o,k)]));
  const rect=n=>{if(!n)return null;const r=n.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height};};
  const box=o=>{if(!o)return null;return {x:o.x,y:o.y,width:o.width,height:o.height};};
  const category=v=>v!==null&&typeof v==='object'?pick(v,['id','value']):{scalar:v};
  const data=rows=>{if(!Array.isArray(rows)||rows.length>5)throw Error('At most five data rows');
    return rows.map(r=>({period:category(r.period),values:pick(r,['cashFlow','operatingIncome','revenue'])}));};
  const series=o=>pick(o,['type','xKey','yKey','yName']);
  const tooltip=o=>pick(o,['enabled','mode','range']);
  const model=m=>({identity:pick(m,['chartId','chartType','chartThemeName','switchCategorySeries','aggFunc']),
    cellRange:{...pick(m.cellRange,['rowStartIndex','rowEndIndex']),columns:cap(m.cellRange?.columns,4,'Columns')},
    modes:{bar:tooltip(m.chartOptions?.bar?.tooltip),line:tooltip(m.chartOptions?.line?.tooltip)}});
  const visible=n=>!!n&&!!n.getClientRects().length&&getComputedStyle(n).visibility!=='hidden'&&getComputedStyle(n).opacity!=='0';
  const text=(v,max=512)=>{const s=v==null?'':String(v);if(s.length>max)throw Error('Text bound');return s;};
  const active=n=>n?{tag:n.tagName,role:n.getAttribute('role'),name:text(n.getAttribute('aria-label')||n.getAttribute('aria-labelledby')?.split(' ').map(id=>document.getElementById(id)?.textContent).join(' ')),
    tabindex:n.getAttribute('tabindex'),id:n.id||null,focusVisible:n.matches(':focus-visible'),rect:rect(n),inSeriesArea:!!n.closest('.ag-charts-series-area')}:null;
  window.__tooltip={cap,pick,rect,box,category,data,series,tooltip,model,visible,text,active,events:[],overflow:false};
}
export function acquire(){
  const roots=document.querySelectorAll('.ag-root-wrapper');if(roots.length!==1)throw Error('One grid required');
  let fiber=roots[0][Object.keys(roots[0]).find(k=>k.startsWith('__reactFiber'))],api=null,proxy=null;
  for(let depth=0;fiber&&depth<18;depth++,fiber=fiber.return){const v=fiber.memoizedProps?.value;
    if(v?.gridRef?.current?.api)api=v.gridRef.current.api;if(v?.chartRef?.current?.chart)proxy=v.chartRef.current.chart;}
  if(!api||!proxy?.chart?.chartOptions?.processedOptions)throw Error('Named grid/chart context unavailable');
  if(api.getChartModels().length!==1)throw Error('One chart required');window.__tooltipGrid=api;window.__tooltipProxy=proxy;
  const p=window.__tooltip;
  if(!p.listener){p.listener=e=>{if(p.events.length>=96){p.overflow=true;return;}
    p.events.push({action:p.action??'setup',sequence:p.events.length+1,type:e.type,chartId:e.chartId,chartType:e.chartType,chartThemeName:e.chartThemeName,
      modes:{bar:p.tooltip(e.chartOptions?.bar?.tooltip),line:p.tooltip(e.chartOptions?.line?.tooltip)}});};
    api.addEventListener('chartOptionsChanged',p.listener);api.addEventListener('chartRangeSelectionChanged',p.listener);}
  return {model:p.model(api.getChartModels()[0])};
}
export function admission(){const p=window.__tooltip,proxy=window.__tooltipProxy,o=proxy.getOptions(),effective=proxy.chart.chartOptions.processedOptions;
  const table=[...document.querySelectorAll('.ag-center-cols-container [role=row]')];if(table.length>5)throw Error('At most five table rows');
  return {model:p.model(window.__tooltipGrid.getChartModels()[0]),options:{tooltip:p.tooltip(o.tooltip),data:p.data(o.data),series:p.cap(o.series,3,'Series').map(p.series)},
    effective:{tooltip:p.tooltip(effective.tooltip),data:p.data(effective.data),series:p.cap(effective.series,3,'Series').map(p.series)},
    table:table.map(r=>({rowIndex:r.getAttribute('row-index'),cells:[...r.querySelectorAll('[role=gridcell]')].slice(0,5).map(c=>({column:c.getAttribute('col-id'),text:p.text(c.textContent)}))})),
    generatedCombined:{available:false,reason:'No reviewed generated/combined finite seam'}};
}
export function geometry(request){
  const p=window.__tooltip,c=window.__tooltipProxy.chart;
  const canvas=[...document.querySelectorAll('.ag-charts-canvas canvas')].filter(p.visible);if(canvas.length!==1)throw Error('One visible chart canvas required');
  const areas=[...document.querySelectorAll('.ag-charts-series-area')].filter(p.visible);if(areas.length!==1)throw Error('One series area required');
  const series=p.cap(c.series,3,'Live series').map(s=>{const group=s.contentGroup,managed=group?.parentNode,root=c.ctx.root,sr=c.seriesRoot;
    const chainValid=!!group&&!!managed&&!!sr&&!!root&&group!==managed&&managed!==sr&&sr!==root&&
      group.parentNode===managed&&managed.parentNode===sr&&sr.parentNode===root&&(root.parentNode===null||root.parentNode===undefined);
    const rootTerminal={own:Object.hasOwn(root??{},'parentNode'),in:'parentNode' in Object(root??{}),type:typeof root?.parentNode,
      value:root?.parentNode===undefined?{kind:'undefined'}:root.parentNode===null?null:{kind:'nonterminal-object'}};
    const transforms=[group,managed,sr,root].map(n=>p.pick(n,['translationX','translationY','rotation','scalingX','scalingY']));
    const nodes=p.cap(s.getNodeData(),5,'Nodes').filter(n=>n.datumIndex===request.ordinal).map(n=>({fields:p.pick(n,['datumIndex','yValue','x','y','width','height']),
      xValue:p.category(n.xValue),point:p.pick(n.point,['x','y']),midPoint:p.pick(n.midPoint,['x','y'])}));
    return {id:s.id,type:s.type,yKey:s.properties.yKey,chainValid,rootTerminal,transforms,nodes};});
  if(typeof c.ctx.animationManager.isActive!=='function')throw Error('Animation query unavailable');
  return {seriesRect:p.box(c.seriesRect),scene:{width:c.ctx.scene.width,height:c.ctx.scene.height},canvas:p.rect(canvas[0]),area:p.rect(areas[0]),
    dpr:devicePixelRatio,animationActive:c.ctx.animationManager.isActive(),series,request};
}
export function dom(){
  const p=window.__tooltip,all=[...document.querySelectorAll('.ag-charts-tooltip')];p.cap(all,1,'Tooltip');
  const t=all[0],head=t?[...t.querySelectorAll('.ag-charts-tooltip-heading')]:[],rows=t?[...t.querySelectorAll('.ag-charts-tooltip-row')]:[];
  p.cap(head,1,'Heading');p.cap(rows,3,'Tooltip rows');
  let html=t?.innerHTML||'';if(new TextEncoder().encode(html).length>8192)throw Error('Tooltip HTML bound');
  if(t){const clone=t.cloneNode(true);for(const e of clone.querySelectorAll('*'))for(const a of [...e.attributes])
    if(!['class','role','aria-label'].includes(a.name))e.removeAttribute(a.name);html=clone.innerHTML;}
  const area=document.querySelector('.ag-charts-series-area'),imgs=area?[...area.querySelectorAll('[role=img]')]:[];p.cap(imgs,2,'Swapchain');
  const statuses=[...document.querySelectorAll('.ag-charts-announcer,[role=status]')].filter(n=>n.closest('.ag-charts-wrapper,.ag-chart-wrapper'));p.cap(statuses,1,'Live status');
  return {tooltip:t?{visible:p.visible(t),bounds:p.rect(t),heading:head.map(n=>p.text(n.textContent)),
    rows:rows.map(n=>({label:p.text(n.querySelector('.ag-charts-tooltip-label')?.textContent),value:p.text(n.querySelector('.ag-charts-tooltip-value')?.textContent)})),
    compact:[...t.children].slice(0,4).map(n=>p.text(n.textContent)),sanitizedInnerHTML:html,pagination:!!t.querySelector('.ag-charts-tooltip-pagination')}:null,
    active:p.active(document.activeElement),area:p.active(area),swapchain:imgs.map(p.active),liveStatus:p.text(statuses[0]?.textContent,2048)};
}
