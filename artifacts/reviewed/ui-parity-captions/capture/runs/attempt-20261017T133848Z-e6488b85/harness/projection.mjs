// This function runs inside the original page; it never mutates chart options.
export function installProjection(){
  const textFields=['enabled','text','fontFamily','fontSize','fontWeight','fontStyle','color','spacing','padding'];
  const nodeFields=['id','visible','opacity','text','fontFamily','fontSize','fontWeight','fontStyle','fill',
    'x','y','rotation','rotationCenterX','rotationCenterY','translationX','translationY','scalingX','scalingY',
    'textAlign','textBaseline'];
  const boxFields=['x','y','width','height'];
  const scalar=(value,key)=>{
    if(value===null||typeof value==='boolean'||typeof value==='number'&&Number.isFinite(value))return value;
    if(typeof value==='string'&&value.length<=512)return value;
    throw Error('Unsupported or nonfinite scalar '+key);
  };
  const fields=(object,names)=>{
    if(names.length>64)throw Error('Scalar field bound');
    return Object.fromEntries(names.map(key=>{
      const present=object!=null&&key in Object(object),value=object?.[key];
      return [key,{own:object!=null&&Object.hasOwn(object,key),in:present,
        kind:!present?'absent':value===undefined?'undefined':value===null?'null':'value',
        type:!present?'absent':typeof value,...(present&&value!==undefined?{value:scalar(value,key)}:{})}];
    }));
  };
  const text=object=>fields(object,textFields);
  const padding=object=>fields(object,['top','right','bottom','left']);
  const axisBase=object=>({identity:fields(object,['type','position']),title:text(object?.title),label:text(object?.label)});
  const axis=object=>({...axisBase(object),positions:Object.fromEntries(['top','bottom','left','right']
    .map(key=>[key,axisBase(object?.[key])]))});
  const branch=object=>({title:text(object?.title),subtitle:text(object?.subtitle),padding:padding(object?.padding),
    legendLabel:text(object?.legend?.item?.label),seriesLabel:text(object?.series?.label),
    axes:Object.fromEntries(['category','number'].map(key=>[key,axis(object?.axes?.[key])]))});
  const options=object=>Object.fromEntries(['common','bar','line'].map(key=>[key,branch(object?.[key])]));
  const columns=value=>{
    if(!Array.isArray(value)||value.length!==3)throw Error('Exact three stable column keys required');
    return value.map(item=>scalar(item,'column'));
  };
  const model=object=>({identity:fields(object,['chartId','chartType','chartThemeName','switchCategorySeries',
    'suppressChartRanges','unlinkChart','aggFunc']),chartOptions:options(object.chartOptions),
    cellRange:{...fields(object.cellRange,['rowStartIndex','rowEndIndex','rowStartPinned','rowEndPinned']),
      columns:columns(object.cellRange?.columns)}});
  const data=rows=>{
    if(rows===undefined)return {kind:'undefined'};
    if(!Array.isArray(rows)||rows.length!==4)throw Error('Exact four data rows required');
    return rows.map(row=>({values:fields(row,['revenue','operatingIncome']),period:
      row.period!==null&&typeof row.period==='object'?{wrapper:fields(row.period,['id','value'])}:
        fields(row,['period'])}));
  };
  let nodeCount=0;
  const node=object=>{
    if(!object)return {unresolved:'Named scene node unavailable'};
    if(++nodeCount>160)throw Error('Scene node bound 160');
    const ancestors=[];let parent=object.parent;
    for(let depth=0;parent&&depth<8;depth++,parent=parent.parent)
      ancestors.push({className:parent.constructor?.name,fields:fields(parent,nodeFields.filter(key=>
        !['text','fontFamily','fontSize','fontWeight','fontStyle','fill','textAlign','textBaseline'].includes(key)))});
    if(parent)throw Error('Scene ancestor bound eight');
    const bbox=typeof object.getBBox==='function'?fields(object.getBBox(),boxFields):
      {unresolved:'getBBox unavailable'};
    return {className:object.constructor?.name,fields:fields(object,nodeFields),bbox,
      coordinateSpace:'node getBBox parent coordinate space; no canvas transform applied',ancestors,
      datum:fields(object.datum,['visible','text','x','y','rotation','rotationCenterX','rotationCenterY','textBaseline'])};
  };
  const selection=(value,maximum,select=value=>value)=>{
    if(typeof value?.each!=='function')return {unresolved:'Named scene selection unavailable'};
    const result=[];value.each(item=>{if(result.length>=maximum)throw Error('Scene selection bound '+maximum);
      result.push(node(select(item)));});return result;
  };
  const liveCaption=caption=>({source:text(caption),node:node(caption?.node)});
  window.__captions={events:[],caseEventCount:0,totalEvents:0,overflow:null,options,model};
  window.__referenceGrid.addEventListener('chartOptionsChanged',event=>{
    const store=window.__captions;
    if(store.events.length>=8||store.caseEventCount>=96||store.totalEvents>=512){
      store.overflow={kind:'event-bound',action:store.events.length,case:store.caseEventCount,total:store.totalEvents};return;
    }
    try{store.events.push({identity:fields(event,['type','chartId','chartType','chartThemeName']),
      chartOptions:options(event.chartOptions)});store.caseEventCount++;store.totalEvents++;}
    catch(error){store.overflow={kind:'event-projection',message:error.message};}
  });
  window.__captions.snapshot=()=>{
    const proxy=window.__referenceProxy,chart=proxy.chart,processed=chart.chartOptions.processedOptions;
    if(window.__captions.overflow)throw Error(JSON.stringify(window.__captions.overflow));
    if(chart.axes.length!==2||chart.series.length!==2||processed.axes.length!==2||processed.series.length!==2)
      throw Error('Exact two axes/two series required');
    nodeCount=0;
    const canvases=[...document.querySelectorAll('.ag-charts-canvas canvas')];
    if(canvases.length>16)throw Error('Canvas count bound');
    const rect=element=>fields(element.getBoundingClientRect(),['x','y','width','height','top','right','bottom','left']);
    return {model:model(window.__referenceGrid.getChartModels()[0]),
      internalEnvelope:{themeOverrides:options(proxy.getOptions()?.theme?.overrides)},
      data:{options:data(proxy.getOptions().data),effective:data(processed.data)},
      effective:{title:text(processed.title),subtitle:text(processed.subtitle),padding:padding(processed.padding),
        axes:processed.axes.map(axisBase),legendLabel:text(processed.legend?.item?.label),
        series:processed.series.map(series=>({identity:fields(series,['type','xKey','yKey','yName']),label:text(series.label)}))},
      scene:{title:liveCaption(chart.title),subtitle:liveCaption(chart.subtitle),padding:padding(chart.padding),
        seriesRect:fields(chart.seriesRect,boxFields),
        axes:chart.axes.map(value=>({identity:fields(value,['type','position']),titleSource:text(value.title),
          titleCaption:liveCaption(value.title?.caption),labels:selection(value.tickLabelGroupSelection,64)})),
        legend:{bounds:chart.legend?.group&&typeof chart.legend.group.getBBox==='function'?
          fields(chart.legend.group.getBBox(),boxFields):{unresolved:'Named legend group bounds unavailable'},
          labels:selection(chart.legend?.itemSelection,2,item=>item.label)},
        series:chart.series.map(series=>({identity:fields(series,['id','type','xKey','yKey']),
          labels:selection(series.labelSelection,8)}))},
      geometry:{dpr:devicePixelRatio,canvas:canvases.map(canvas=>({css:rect(canvas),
        backing:fields(canvas,['width','height'])})),editor:rect(document.querySelector('.ag-chart-docked-container'))},
      settled:{animationActive:chart.ctx.animationManager.isActive()},events:window.__captions.events,
      eventCounters:{case:window.__captions.caseEventCount,total:window.__captions.totalEvents}};
  };
}
