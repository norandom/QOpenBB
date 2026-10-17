export function installProjection() {
  const omitted=[];
  let paths=0;
  const scalar=value=>value===null||['string','boolean'].includes(typeof value)||typeof value==='number'&&Number.isFinite(value);
  function project(value,path,depth=0){
    if(paths>=2048){omitted.push({path,reason:'path-limit'});return undefined;}
    if(scalar(value)){paths++;if(typeof value==='string'&&value.length>1024){omitted.push({path,reason:'string-limit'});return undefined;}return value;}
    if(value===undefined)return undefined;
    if(depth>=10){omitted.push({path,reason:'depth-limit'});return undefined;}
    if(Array.isArray(value)){
      if(value.length>64){omitted.push({path,reason:'array-limit',count:value.length});return undefined;}
      return value.map((item,index)=>project(item,path+'.'+index,depth+1));
    }
    if(typeof value!=='object'||![Object.prototype,null].includes(Object.getPrototypeOf(value))){
      omitted.push({path,reason:'non-plain-'+typeof value});return undefined;
    }
    const keys=Object.keys(value);
    if(keys.length>128){omitted.push({path,reason:'object-key-limit',count:keys.length});return undefined;}
    return Object.fromEntries(keys.map(key=>[key,project(value[key],path+'.'+key,depth+1)]));
  }
  const nodes=new WeakMap();let sequence=0;
  const nodeId=node=>node?(nodes.has(node)?nodes.get(node):(nodes.set(node,++sequence),sequence)):null;
  const visible=node=>!!node&&node.getClientRects().length>0&&getComputedStyle(node).visibility!=='hidden';
  const label=node=>(node?.getAttribute('aria-label')||node?.getAttribute('aria-labelledby')?.split(' ')
    .map(id=>document.getElementById(id)?.textContent).join(' ')||node?.closest('.ag-slider,.ag-field')
    ?.querySelector('label')?.textContent||node?.textContent||'').trim().slice(0,1024);
  const element=node=>node?{tag:node.tagName,id:node.id||null,role:node.getAttribute('role'),label:label(node),
    type:node.type||null,value:node.value?.slice?.(0,1024),checked:node.checked,disabled:node.disabled,
    node:nodeId(node),visible:visible(node)}:null;
  const rectangle=node=>{if(!node)return null;const r=node.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height};};
  const focus=[],chartEvents=[];let focusOverflow=0,chartEventOverflow=0;
  for(const type of ['focusin','focusout'])document.addEventListener(type,event=>{
    if(focus.length<512)focus.push({type,time:Math.round(performance.now()),element:element(event.target)});
    else focusOverflow++;
  },true);
  window.__navigation={
    project,element,rectangle,visible,nodeId,focus,chartEvents,observedGrids:new WeakSet(),
    chartEvent(event){if(chartEvents.length>=2048){chartEventOverflow++;return;}
      chartEvents.push({type:event.type,chartId:event.chartId,chartType:event.chartType,chartThemeName:event.chartThemeName});},
    begin(){paths=0;omitted.length=0;},
    budget(){return {paths,omitted:[...omitted].slice(0,64),omittedCount:omitted.length,focusOverflow,chartEventOverflow};},
  };
}

export function acquireReferences(){
  let api=null,readWidget=null;
  const roots=[...document.querySelectorAll('.ag-root-wrapper')];
  if(roots.length!==1)throw Error('Expected one synthetic grid root; got '+roots.length);
  let fiber=roots[0][Object.keys(roots[0]).find(key=>key.startsWith('__reactFiber'))];
  for(let depth=0;fiber&&depth<18;depth++,fiber=fiber.return){
    const value=fiber.memoizedProps?.value;
    const candidate=value?.gridRef?.current?.api||fiber.child?.stateNode?.api;
    if(typeof candidate?.getChartModels==='function')api=candidate;
    if(typeof value?.getWidget==='function'){
      const widget=value.getWidget();
      if(widget?.id==='synthetic_financials'||widget?.widgetId==='synthetic_financials')readWidget=value.getWidget;
    }
  }
  if(!readWidget){
    const widgetElement=document.getElementById('synthetic_financials');
    if(!widgetElement)throw Error('Source-named synthetic widget element unavailable');
    let widgetFiber=widgetElement[Object.keys(widgetElement).find(key=>key.startsWith('__reactFiber'))];
    for(let depth=0;widgetFiber&&depth<18;depth++,widgetFiber=widgetFiber.return){
      const value=widgetFiber.memoizedProps?.value;
      if(typeof value?.getWidget!=='function'||!value.widgetRef)continue;
      const widget=value.getWidget();
      if(widget?.id==='synthetic_financials'||widget?.widgetId==='synthetic_financials')readWidget=value.getWidget;
    }
  }
  if(!api)throw Error('Named original GridApi unavailable');
  if(!readWidget)throw Error('Named synthetic getWidget getter unavailable');
  window.__navigationGrid=api;window.__navigationReadWidget=readWidget;
  if(!window.__navigation.observedGrids.has(api)){
    window.__navigation.observedGrids.add(api);
    for(const type of ['chartCreated','chartOptionsChanged','chartRangeSelectionChanged','chartDestroyed'])
      api.addEventListener(type,event=>window.__navigation.chartEvent(event));
  }
  const models=api.getChartModels();
  if(models.length>1)throw Error('More than one original chart model');
  const model=models[0];
  const proxy=model?api.getChartRef(model.chartId)?.chart:null;
  window.__navigationProxy=proxy;
  return {chart:!!model,chartType:model?.chartType,chartId:model?.chartId};
}

export function readState(){
  const p=window.__navigation,g=window.__navigationGrid;
  p.begin();
  const widget=window.__navigationReadWidget();
  if(widget?.id!=='synthetic_financials'&&widget?.widgetId!=='synthetic_financials')throw Error('Unexpected widget');
  const storage=widget.storage||{},models=g.getChartModels(),model=models[0];
  const options=value=>value?Object.fromEntries(['common','bar','line'].filter(key=>Object.hasOwn(value,key))
    .map(key=>[key,p.project(value[key],'options.'+key)])):undefined;
  const chartModel=raw=>raw?{chartId:raw.chartId,chartType:raw.chartType,chartThemeName:raw.chartThemeName,
    cellRange:p.project(raw.cellRange,'model.cellRange'),chartOptions:options(raw.chartOptions),
    switchCategorySeries:raw.switchCategorySeries,aggFunc:typeof raw.aggFunc==='function'?'[function]':raw.aggFunc,
    suppressChartRanges:raw.suppressChartRanges}:null;
  const partitions=Object.entries(storage).filter(([key,value])=>!['chartModel','chartOptions'].includes(key)
    &&value&&typeof value==='object'&&Object.hasOwn(value,'chartModel'));
  if(partitions.length>2)throw Error('Storage partition limit');
  const rootStorage=Object.fromEntries(['chartSettingsOpen','chartType','totalSeries','isPivotMode','chartView']
    .map(key=>[key,{own:Object.hasOwn(storage,key),value:p.project(storage[key],'storage.'+key)}]));
  rootStorage.chartOptions={own:Object.hasOwn(storage,'chartOptions'),value:options(storage.chartOptions)};
  rootStorage.chartModel=chartModel(storage.chartModel);
  rootStorage.partitions=partitions.map(([key,value])=>({key,chartModel:chartModel(value.chartModel),
    ranges:Object.fromEntries(['groupedColumn','line'].filter(family=>value[family]?.cellRange)
      .map(family=>[family,p.project(value[family].cellRange,'partition.'+family)]))}));
  const rows=[];g.forEachNode(node=>{if(rows.length>=4)throw Error('Source row limit');
    rows.push({id:node.id,period:node.data?.period,revenue:node.data?.revenue,operatingIncome:node.data?.operatingIncome});});
  const columns=g.getColumnState();if(columns.length>3)throw Error('Column limit');
  const ranges=g.getCellRanges()||[];if(ranges.length>8)throw Error('Cell range limit');
  const proxy=window.__navigationProxy,processed=proxy?.chart?.chartOptions?.processedOptions;
  const rawOptions=proxy?.getOptions();
  const chart=processed?{model:chartModel(model),
    raw:{data:p.project(rawOptions.data,'raw.data'),series:p.project(rawOptions.series,'raw.series'),
      theme:{baseTheme:typeof rawOptions.theme?.baseTheme==='string'?rawOptions.theme.baseTheme:'[nested-theme]'}},
    effective:{data:p.project(processed.data,'effective.data'),axes:p.project(processed.axes,'effective.axes'),
      series:p.project(processed.series,'effective.series'),title:p.project(processed.title,'effective.title'),
      legend:p.project(processed.legend,'effective.legend')},animationActive:proxy.chart.ctx.animationManager.isActive()}:null;
  const panel=document.querySelector('.ag-chart-docked-container');
  const panelElements=panel?[...panel.querySelectorAll('*')]:[];
  if(panelElements.length>3000)throw Error('Panel DOM node limit');
  const controls=panel?[...panel.querySelectorAll('input,[role=combobox],button,[role=tab]')].filter(p.visible):[];
  if(controls.length>256)throw Error('Control limit');
  const headings=panel?[...panel.querySelectorAll('.ag-charts-format-top-level-group-title-bar')]:[];
  if(headings.length>32)throw Error('Heading limit');
  const scrollOwners=[panel,...panelElements].filter(node=>node&&node.scrollHeight>node.clientHeight+1
    &&['auto','scroll'].includes(getComputedStyle(node).overflowY));
  if(scrollOwners.length>8)throw Error('Scroll owner limit');
  const active=document.activeElement,ancestors=[];let ancestor=active?.parentElement;
  for(let depth=0;ancestor&&depth<8;depth++,ancestor=ancestor.parentElement)ancestors.push(p.element(ancestor));
  const gridState=g.getState?.();
  return {sourceRows:rows,columnState:columns.map(col=>({colId:col.colId,width:col.width,hide:col.hide,pinned:col.pinned,sort:col.sort})),
    rootStorage,chart,chartEvents:[...p.chartEvents],table:{focusedCell:(()=>{const cell=g.getFocusedCell();return cell?
      {rowIndex:cell.rowIndex,rowPinned:cell.rowPinned,colId:cell.column?.getColId()}:null;})(),
      ranges:ranges.map(range=>({startRow:p.project(range.startRow,'range.start'),endRow:p.project(range.endRow,'range.end'),
        columns:range.columns.map(col=>col.getColId())})),
      state:{scroll:p.project(gridState?.scroll,'table.scroll'),cellSelection:p.project(gridState?.cellSelection,'table.selection'),
        focusedCell:p.project(gridState?.focusedCell,'table.focus')},
      cells:[...document.querySelectorAll('.ag-row[row-index] .ag-cell[col-id]')].filter(p.visible).slice(0,12)
        .map(node=>({row:node.closest('.ag-row').getAttribute('row-index'),column:node.getAttribute('col-id'),text:node.textContent,rect:p.rectangle(node)}))},
    dom:{dark:document.documentElement.classList.contains('dark'),htmlClass:document.documentElement.className,
      panel:p.element(panel),panelRect:p.rectangle(panel),menuVisible:!!document.querySelector('.ag-chart-menu-visible'),
      chartNode:p.nodeId(document.querySelector('.ag-charts-canvas')),chartRect:p.rectangle(document.querySelector('.ag-charts-canvas')),
      tabs:panel?[...panel.querySelectorAll('[role=tab]')].map(node=>({...p.element(node),selected:node.getAttribute('aria-selected')})):[],
      headings:headings.map(node=>({...p.element(node),class:node.className,expanded:node.getAttribute('aria-expanded'),
        parentClass:node.parentElement?.className})),controls:controls.map(p.element),
      scroll:scrollOwners.map(node=>({node:p.nodeId(node),class:node.className,scrollTop:node.scrollTop,
        clientHeight:node.clientHeight,scrollHeight:node.scrollHeight,rect:p.rectangle(node)})),
      active:p.element(active),activeAncestors:ancestors,focusEvents:[...p.focus]},
    budget:p.budget()};
}
