export function install(){
  const scalar=(v,k)=>{if(v===null||typeof v==='boolean'||typeof v==='number'&&Number.isFinite(v)||typeof v==='string'&&v.length<=512)return v;throw Error('nonfinite-scalar: '+k);};
  const field=(o,k)=>{const present=o!=null&&k in Object(o),v=present?o[k]:undefined;
    return {own:o!=null&&Object.hasOwn(o,k),in:present,kind:!present?'absent':v===undefined?'undefined':v===null?'null':'value',type:present?typeof v:'absent',...(v!==undefined?{value:scalar(v,k)}:{})};};
  const pick=(o,ks)=>Object.fromEntries(ks.map(k=>[k,field(o,k)]));
  const shape=o=>{const v=o?.shape;return typeof v==='function'?{...pick(o,[]),type:'function',constructorName:scalar(v.name||v.constructor?.name||'','shape')}:field(o,'shape');};
  const label=o=>pick(o,['fontFamily','fontSize','fontWeight','fontStyle','color','maxLength']);
  const marker=o=>({...pick(o,['size','strokeWidth','padding','enabled']),shape:shape(o)});
  const legend=o=>({...pick(o,['enabled','visible','position','spacing','maxWidth','maxHeight']),item:{...pick(o?.item,['paddingX','paddingY']),marker:marker(o?.item?.marker),label:label(o?.item?.label)}});
  const options=o=>Object.fromEntries(['common','bar','line'].map(k=>[k,{namespace:{own:o!=null&&Object.hasOwn(o,k),in:o!=null&&k in Object(o),kind:o==null||!(k in Object(o))?'absent':o[k]===undefined?'undefined':o[k]===null?'null':'value',type:o==null||!(k in Object(o))?'absent':typeof o[k]},legend:legend(o?.[k]?.legend)}]));
  const data=o=>{if(!Array.isArray(o)||o.length!==4)throw Error('fixture-unresolved: four rows');return o.map(r=>({amounts:pick(r,['revenue','operatingIncome']),period:r.period!==null&&typeof r.period==='object'?{wrapper:pick(r.period,['id','value'])}:field(r,'period')}));};
  const sourceSeries=(o,shared)=>{if(!Array.isArray(o)||o.length!==2)throw Error('fixture-unresolved: two source series');return o.map(s=>({identity:pick(s,['id','type','xKey','yKey','yName']),
    data:{own:Object.hasOwn(s,'data'),in:'data' in s,kind:!('data' in s)?'absent':s.data===undefined?'undefined':s.data===null?'null':'value',type:typeof s.data,...(s.data!==undefined&&s.data!==null?{value:data(s.data)}:{})},
    inputValues:data(s.data??shared).map(r=>({period:r.period,amount:r.amounts[s.yKey]}))}));};
  const columns=o=>{if(!Array.isArray(o)||o.length!==3)throw Error('fixture-unresolved: exact three columns');return o.map(c=>scalar(c,'column'));};
  const model=o=>({...pick(o,['chartId','chartType','chartThemeName','switchCategorySeries','aggFunc']),chartOptions:options(o?.chartOptions),cellRange:{...pick(o?.cellRange,['rowStartIndex','rowEndIndex','rowStartPinned','rowEndPinned']),columns:columns(o?.cellRange?.columns)}});
  const transforms=['visible','opacity','translationX','translationY','rotation','scalingX','scalingY'];
  const rect=n=>n?pick(n.getBoundingClientRect(),['x','y','width','height']):null;
  const text=v=>v==null?null:scalar(String(v),'DOM text');
  const accessible=n=>(n?.getAttribute('aria-label')||n?.getAttribute('aria-labelledby')?.split(/\s+/).map(id=>document.getElementById(id)?.textContent||'').join(' ')||n?.labels?.[0]?.textContent||'').trim();
  const dom=n=>{if(!n)return null;const css=getComputedStyle(n);return {tag:n.tagName,type:n.type??null,label:text(accessible(n)),text:text(n.textContent?.trim()),role:n.getAttribute('role'),ref:n.getAttribute('data-ref'),
    checked:n.checked??null,value:n.value??null,attached:n.isConnected,visible:!!n.getClientRects().length&&css.visibility!=='hidden'&&css.display!=='none',enabled:!n.disabled,
    ariaChecked:n.getAttribute('aria-checked'),hidden:n.getAttribute('aria-hidden'),tabindex:n.getAttribute('tabindex'),controls:n.getAttribute('aria-controls'),
    labelledby:n.getAttribute('aria-labelledby'),min:n.min??null,max:n.max??null,step:n.step??null,css:pick(css,['display','visibility','opacity']),rect:rect(n)};};
  const store={pick,field,legend,options,model,data,sourceSeries,rect,dom,accessible,events:[],action:'admission',caseEvents:0,actionEvents:0,overflow:null};
  store.snapshot=()=>{
    if(store.overflow)throw Error('event-overflow: '+JSON.stringify(store.overflow));
    const chart=window.__legendProxy.chart,processed=chart.chartOptions.processedOptions,lg=chart.legend,root=chart.ctx.scene.root;
    if(typeof lg?.itemSelection?.each!=='function')throw Error('scene-unresolved: selection');
    const selected=[];lg.itemSelection.each((n,d)=>{if(selected.length>=2)throw Error('scene-unresolved: selection bound');selected.push({n,d});});
    if(selected.length!==2||chart.series?.length!==2)throw Error('scene-unresolved: exact two items/series');
    const parents=(n,p,name)=>{if(!n||n.parentNode!==p)throw Error('scene-unresolved: '+name);};
    const node=n=>({className:scalar(n.constructor?.className||n.constructor?.name||'','class'),constructorName:scalar(n.constructor?.name||'','class'),fields:pick(n,transforms)});
    if(!root||!lg.group||root.parentNode!=null)throw Error('scene-unresolved: root termination');
    parents(lg.group,root,'legend -> root');
    const items=selected.map(({n,d},index)=>{
      parents(n,lg.group,'item -> legend');parents(n.label,n,'label -> item');parents(n.symbolsGroup,n,'symbols -> item');parents(n.marker,n.symbolsGroup,'marker -> symbols');parents(n.line,n.symbolsGroup,'line -> symbols');
      const s=chart.series[index];
      if(!s.contentGroup||s.id!==d?.seriesId||s.properties?.xKey!=='period'||s.properties?.yKey!==['revenue','operatingIncome'][index])throw Error('series-identity-mismatch');
      if(s.visible!==true||s.contentGroup.visible!==true)throw Error('series-visibility-mismatch');
      return {...node(n),datum:{...pick(d,['id','seriesId','itemId','enabled']),label:pick(d?.label,['text'])},...pick(n,['spacing','length','pageIndex']),
        symbols:node(n.symbolsGroup),line:pick(n.line,['visible','strokeWidth']),
        label:{...node(n.label),style:pick(n.label,['text','fontFamily','fontSize','fontWeight','fontStyle','fill','x','y'])},
        marker:{...node(n.marker),style:{...pick(n.marker,['size','stroke','strokeWidth','fill','x','y']),shape:shape(n.marker)}},
        proxy:dom(n.proxyButton?.getElement()),series:{identity:pick(s,['id','type']),properties:pick(s.properties,['xKey','yKey','visible','stroke','strokeWidth']),visible:field(s,'visible'),contentGroup:node(s.contentGroup)}};
    });
    const namedNodes=[root,lg.group,...selected.flatMap(({n},index)=>[n,n.symbolsGroup,n.label,n.marker,n.line,chart.series[index].contentGroup])];
    if(new Set(namedNodes).size!==14)throw Error('scene-unresolved: fourteen distinct named identities');
    const operands=()=>[...['translationX','translationY'].map(k=>({owner:'legend.group',key:k,record:field(lg.group,k)})),...selected.flatMap(({n},i)=>[
      ...['translationX','translationY'].map(k=>({owner:'item'+i,key:k,record:field(n,k)})),...['x','y','translationX','translationY'].map(k=>({owner:'marker'+i,key:k,record:field(n.marker,k)}))])];
    const bbox=n=>{if(typeof n?.getBBox!=='function')throw Error('scene-unresolved: getBBox');return pick(n.getBBox(),['x','y','width','height']);};
    const before=operands();
    const boxes={group:bbox(lg.group),items:selected.map(({n})=>({item:bbox(n),label:bbox(n.label),marker:bbox(n.marker)}))};
    const after=operands(),valid=JSON.stringify(before)===JSON.stringify(after);
    if(!valid)return {valid:false,reason:'bbox-getter-operands-changed',operands:{before,after},eventSequence:store.events.length};
    const canvases=[...document.querySelectorAll('.ag-charts-canvas canvas')];if(canvases.length!==1)throw Error('scene-unresolved: exact canvas');
    const canvas=canvases[0],canvasBox=canvas.getBoundingClientRect();
    if(devicePixelRatio!==1||Math.abs(chart.ctx.scene.width-canvasBox.width)>.5||Math.abs(chart.ctx.scene.height-canvasBox.height)>.5)throw Error('scene-unresolved: scene canvas dimensions');
    const toolbar=document.querySelectorAll('.ag-charts-proxy-legend-toolbar');if(toolbar.length!==1)throw Error('scene-unresolved: toolbar');
    for(let i=0;i<2;i++){const button=selected[i].n.proxyButton?.getElement();if(!button||!toolbar[0].contains(button))throw Error('scene-unresolved: exact proxy button');}
    const editor=document.querySelectorAll('.ag-chart-docked-container');if(editor.length>1)throw Error('selector-unresolved: editor cardinality');
    const heads=editor[0]?[...editor[0].querySelectorAll('.ag-charts-format-top-level-group-title-bar')].filter(n=>n.textContent.trim()==='Legend'):[];
    if(heads.length>1)throw Error('selector-unresolved: Legend title');const panel=heads[0]?.parentElement;
    const controls=panel?[...panel.querySelectorAll('input,[role="combobox"]')]:[];if(controls.length>32)throw Error('selector-unresolved: controls bound');
    const color=panel?[...panel.querySelectorAll('.ag-font-panel .ag-color-picker')]:[];if(color.length>1)throw Error('selector-unresolved: Color wrapper');
    const paginationDOM=[...document.querySelectorAll('.ag-charts-proxy-legend-pagination')];if(paginationDOM.length>1)throw Error('scene-unresolved: pagination');
    const paginationButtons=paginationDOM[0]?[...paginationDOM[0].querySelectorAll('button')]:[];if(paginationButtons.length>2)throw Error('scene-unresolved: pagination buttons');
    const source=window.__legendProxy.getOptions(),models=window.__legendGrid.getChartModels();if(models.length!==1)throw Error('identity-unresolved: model cardinality');
    const fonts=items.map(i=>{const f=i.label.style;const css=`${f.fontStyle.value||'normal'} ${f.fontWeight.value||'normal'} ${f.fontSize.value}px ${f.fontFamily.value}`;return {css,available:document.fonts.check(css)};});
    return {valid:true,model:model(models[0]),internalOverrides:options(source.theme?.overrides),effective:legend(processed.legend),data:data(processed.data),sourceSeries:sourceSeries(source.series,source.data),
      live:{legend:legend(lg),pagination:pick(lg.pagination,['visible','currentPage','totalPages']),
        scene:{root:{...node(root),parentNode:{own:Object.hasOwn(root,'parentNode'),in:'parentNode' in root,type:typeof root.parentNode,value:root.parentNode??null}},group:node(lg.group),items,boxes,chainValid:true,nodeCount:14}},
      geometry:{padding:pick(chart.padding,['top','right','bottom','left']),seriesRect:pick(chart.seriesRect,['x','y','width','height']),scene:pick(chart.ctx.scene,['width','height']),canvas:{css:rect(canvas),backing:pick(canvas,['width','height'])},seriesArea:rect(document.querySelector('.ag-charts-series-area')),dpr:devicePixelRatio},
      dom:{toolbar:dom(toolbar[0]),pagination:dom(paginationDOM[0]),paginationButtons:paginationButtons.map(dom),controls:controls.map(dom),color:color.map(dom),panel:rect(panel),active:{tag:document.activeElement?.tagName,type:document.activeElement?.type??null,label:text(accessible(document.activeElement)),ref:document.activeElement?.getAttribute('data-ref')},
        aggregate:[...document.querySelectorAll('input[type="checkbox"]')].filter(n=>accessible(n)==='Aggregate').map(dom),switchCategorySeries:[...document.querySelectorAll('input[type="checkbox"]')].filter(n=>accessible(n)==='Switch category/series').map(dom)},
      fonts,operands:{before,after,valid},eventSequence:store.events.length,animationActive:chart.ctx.animationManager.isActive()};
  };
  window.__legend=store;
}
export function acquire(){
  const p=window.__legend,receipts=[];p.receipts=receipts;
  const roots=document.querySelectorAll('.ag-root-wrapper');receipts.push({stage:'grid-root',count:roots.length});if(roots.length!==1)throw Error('identity-unresolved: exact grid root');
  let fiber=roots[0][Object.keys(roots[0]).find(k=>k.startsWith('__reactFiber'))],api=null;
  for(let depth=0;fiber&&depth<18;depth++,fiber=fiber.return){
    const candidates=[fiber.memoizedProps?.value?.gridRef?.current?.api,fiber.child?.stateNode?.api];
    for(const candidate of candidates)if(typeof candidate?.getChartModels==='function'){if(api&&api!==candidate)throw Error('identity-unresolved: ambiguous API');api=candidate;}
  }
  receipts.push({stage:'grid-api',present:!!api});if(!api)throw Error('identity-unresolved: API missing');
  const models=api.getChartModels();receipts.push({stage:'models',count:models.length});if(models.length!==1)throw Error('identity-unresolved: exact model');
  const proxy=api.getChartRef(models[0].chartId)?.chart;receipts.push({stage:'chart-proxy',present:!!proxy,chart:!!proxy?.chart,getOptions:typeof proxy?.getOptions,waitForUpdate:typeof proxy?.waitForUpdate});
  if(typeof proxy?.getOptions!=='function'||typeof proxy?.waitForUpdate!=='function'||!proxy.chart)throw Error('identity-unresolved: proxy methods');
  window.__legendGrid=api;window.__legendProxy=proxy;
  p.lastOptions=p.options(models[0].chartOptions);
  p.listener=e=>{try{if(p.events.length>=256||p.caseEvents>=64||p.actionEvents>=8)throw Error('event bound');const projection=p.options(e.chartOptions),previous=p.lastOptions;
    const deltas=[];const walk=(a,b,path)=>{if(a&&typeof a==='object'&&'kind' in a&&'type' in a){if(JSON.stringify(a)!==JSON.stringify(b))deltas.push({path,before:b??{kind:'absent'},after:a});return;}
      for(const key of Object.keys(a??{}))walk(a[key],b?.[key],path?path+'.'+key:key);};walk(projection,previous,'');
    p.events.push({sequence:p.events.length+1,action:p.action,identity:p.pick(e,['type','chartId','chartType','chartThemeName']),chartOptions:projection,deltas});p.lastOptions=projection;p.caseEvents++;p.actionEvents++;
  }catch(error){p.overflow={reason:error.message,action:p.action};}};
  api.addEventListener('chartOptionsChanged',p.listener);return {model:p.model(models[0]),receipts};
}
