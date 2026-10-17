import {chromium} from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
import path from 'node:path';

const root=path.dirname(new URL(import.meta.url).pathname);
const runtime=JSON.parse(fs.readFileSync(root+'/runtime-private.json'));
const credential=JSON.parse(fs.readFileSync(root+'/credential-private.json'));
const json=(name,value)=>fs.writeFileSync(root+'/'+name+'.json',JSON.stringify(value,null,2));
const env={...process.env};delete env.WAYLAND_DISPLAY;
const browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless',
  '--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
const context=await browser.newContext({viewport:{width:1440,height:1000}});
const page=await context.newPage();page.setDefaultTimeout(6000);page.setDefaultNavigationTimeout(20000);
const errors=[],requests=[],ledger=[];
const cdp=await context.newCDPSession(page);
await cdp.send('Runtime.enable');await cdp.send('Network.enable');
const safeUrl=url=>{try{const parsed=new URL(url);return parsed.origin===runtime.origin?
  '[owned-origin]'+parsed.pathname:parsed.origin+parsed.pathname;}catch{return '[invalid-url]';}};
page.on('console',message=>{if(['error','warning'].includes(message.type()))errors.push({
  kind:'console',type:message.type(),text:message.text().replaceAll(runtime.origin,'[owned-origin]')});});
page.on('pageerror',error=>errors.push({kind:'pageerror',text:error.message}));
cdp.on('Runtime.exceptionThrown',event=>errors.push({kind:'cdp-exception',text:event.exceptionDetails.text,
  description:event.exceptionDetails.exception?.description?.replaceAll(runtime.origin,'[owned-origin]'),
  url:safeUrl(event.exceptionDetails.url||''),line:event.exceptionDetails.lineNumber}));
cdp.on('Network.loadingFailed',event=>errors.push({kind:'cdp-network-failed',errorText:event.errorText,
  canceled:event.canceled,type:event.type}));
page.on('response',response=>requests.push({url:safeUrl(response.url()),status:response.status()}));
await page.route('**/*',async route=>{
  const url=new URL(route.request().url());
  if(url.origin!==runtime.origin){requests.push({blocked:safeUrl(url.href)});return route.abort();}
  return route.continue();
});

async function acquire(){
  return page.evaluate(()=>{
    for(const root of document.querySelectorAll('.ag-root-wrapper')){
      let fiber=root[Object.keys(root).find(key=>key.startsWith('__reactFiber'))];
      for(let depth=0;fiber&&depth<18;depth++,fiber=fiber.return){
        const value=fiber.memoizedProps?.value;
        const grid=value?.gridRef?.current?.api||fiber.child?.stateNode?.api;
        if(typeof grid?.getChartModels==='function')window.__referenceGrid=grid;
      }
    }
    const grid=window.__referenceGrid,model=grid?.getChartModels()[0];
    if(!model)throw Error('Finite chart reference unavailable');
    const proxy=grid.getChartRef(model.chartId).chart;
    if(!proxy?.chart?.chartOptions?.processedOptions)throw Error('Processed original chart unavailable');
    window.__referenceProxy=proxy;
    return {chartType:model.chartType,chartThemeName:model.chartThemeName};
  });
}

async function settled(){
  await acquire();
  await page.evaluate(()=>window.__referenceProxy.waitForUpdate());
  await page.waitForFunction(()=>window.__referenceProxy.chart.ctx.animationManager.isActive()===false,
    null,{timeout:10000,polling:50});
}

async function installProjection(){
  await page.evaluate(()=>{
    const scalar=value=>value===null||['string','boolean'].includes(typeof value)||
      typeof value==='number'&&Number.isFinite(value);
    const pick=(object,fields)=>Object.fromEntries(fields.filter(key=>object?.[key]!==undefined)
      .map(key=>{if(!scalar(object[key]))throw Error('Unexpected scalar '+key);return [key,object[key]];}));
    const presence=(object,fields)=>Object.fromEntries(fields.map(key=>[key,{
      own:Object.hasOwn(object??{},key),in:key in (object??{}),kind:!(key in (object??{}))?'absent':
        object[key]===undefined?'undefined':object[key]===null?'null':'value'}]));
    const array=value=>value===undefined?undefined:value.map(item=>{
      if(typeof item!=='number'||!Number.isFinite(item))throw Error('Nonfinite numeric array');return item;});
    const lineFields=['enabled','stroke','color','width','strokeWidth','strokeOpacity','opacity','visible'];
    const line=object=>({...pick(object,lineFields),presence:presence(object,lineFields),
      lineDash:array(object?.lineDash)});
    const gridLine=object=>({...pick(object,['enabled','width','strokeOpacity','opacity']),
      presence:presence(object,['enabled','width','strokeOpacity','opacity','style']),
      style:object?.style?.map(style=>({...line(style),...pick(style,['fill','fillOpacity'])}))});
    const axisBase=object=>({...pick(object,['type','position']),line:line(object?.line),
      tick:line(object?.tick),gridLine:gridLine(object?.gridLine)});
    const axis=object=>({...axisBase(object),...Object.fromEntries(['left','right','top','bottom']
      .filter(key=>object?.[key]).map(key=>[key,axisBase(object[key])]))});
    const branch=object=>({axes:object?.axes?Object.fromEntries(Object.entries(object.axes)
      .map(([key,value])=>[key,axis(value)])):undefined});
    const model=raw=>({chartType:raw.chartType,chartThemeName:raw.chartThemeName,
      chartOptions:Object.fromEntries(['common','bar','line'].filter(key=>raw.chartOptions?.[key])
        .map(key=>[key,branch(raw.chartOptions[key])]))});
    const node=object=>{
      const ancestors=[];let parent=object?.parent;
      for(let depth=0;parent&&depth<8;depth++,parent=parent.parent)
        ancestors.push(pick(parent,['visible','opacity']));
      return {...line(object),...pick(object,['x1','y1','x2','y2','translationX','translationY']),ancestors};
    };
    window.__axisProjection={line,gridLine,axis,branch,model,node};
    window.__axisEvents=[];
    window.__referenceGrid.addEventListener('chartOptionsChanged',event=>{
      window.__axisEvents.push({type:event.type,chartType:event.chartType,
        chartThemeName:event.chartThemeName,chartOptions:Object.fromEntries(['common','bar','line']
          .filter(key=>event.chartOptions?.[key]).map(key=>[key,branch(event.chartOptions[key])]))});
    });
  });
}

async function state(){
  await settled();
  return page.evaluate(()=>{
    const proxy=window.__referenceProxy,grid=window.__referenceGrid,project=window.__axisProjection;
    const chart=proxy.chart,processed=chart.chartOptions.processedOptions;
    const live=chart.axes.map(axis=>{
      const nodes=[];
      axis.gridLineGroupSelection.each((node,datum)=>{
        if(nodes.length>=64)throw Error('Grid scene projection exceeded 64 nodes');
        nodes.push({node:project.node(node),datum:project.line(datum)});
      });
      return {type:axis.type,position:axis.position,line:project.line(axis.line),
        lineNode:project.node(axis.lineNode),gridLine:project.gridLine(axis.gridLine),gridNodes:nodes};
    });
    const theme=proxy.getOptions().theme;
    return {model:project.model(grid.getChartModels()[0]),
      effective:{axes:processed.axes.map(axis=>project.axis(axis))},live,
      theme:{baseTheme:theme.baseTheme},events:window.__axisEvents,
      settled:{animationActive:chart.ctx.animationManager.isActive()}};
  });
}

const panel=page.locator('.ag-chart-docked-container');
const heading=label=>page.locator('.ag-charts-format-top-level-group-title-bar')
  .filter({hasText:new RegExp('^\\s*'+label+'\\s*$')});
async function controls(){
  return panel.locator('input,[role=combobox]').evaluateAll(elements=>elements
    .filter(element=>element.getClientRects().length&&getComputedStyle(element).visibility!=='hidden')
    .map(element=>({label:(element.getAttribute('aria-label')||element.getAttribute('aria-labelledby')?.split(' ')
      .map(id=>document.getElementById(id)?.textContent).join(' ')||element.closest('.ag-slider,.ag-field')
      ?.querySelector('label')?.textContent||'').trim(),type:element.type,role:element.getAttribute('role'),
      value:element.value??element.textContent.trim(),checked:element.checked,disabled:element.disabled,
      min:element.min,max:element.max,step:element.step})));
}
async function capture(name,kind,input){
  const measured=await state();
  json(name,{kind,input,ui:{text:await panel.innerText(),controls:await controls()},state:measured});
  await page.screenshot({path:root+'/'+name+'.png'});
  console.log('CAPTURE '+name);
  return measured;
}
async function numberField(label,index,value,expectedCount){
  const locator=panel.locator('.ag-slider').filter({has:page.locator('label')
    .filter({hasText:new RegExp('^'+label+'$')})}).locator('input[type=number]:visible');
  const count=await locator.count();
  if(count!==expectedCount)throw Error(label+' visible count '+count+' expected '+expectedCount);
  await locator.nth(index).fill(String(value));await locator.nth(index).press('Tab');
}
async function uiAction(name,input,action,expected){
  const before=await state();
  await action();
  await page.waitForFunction(expected,null,{timeout:6000,polling:50});
  const after=await capture(name,'original-application-real-ui',input);
  ledger.push({name,kind:'original-application-real-ui',input,before,after});json('action-ledger',ledger);
}

try{
  await page.route('**/api/pro/dash/{sync,validate-and-sync}',async route=>{
    if(route.request().method()!=='GET')return route.continue();
    const upstream=await route.fetch(),actual=await upstream.json();
    const fixture=JSON.parse(fs.readFileSync(root+'/fixture.json','utf8')
      .replaceAll('http://127.0.0.1:32773',runtime.origin));
    return route.fulfill({json:{...actual,owned:Object.fromEntries(Object.entries(fixture)
      .map(([id,content])=>[id,{content,is_shared:false,created_by:'Synthetic Parity',
        created_date:'2026-10-17T00:00:00Z',updated_date:'2026-10-17T00:00:00Z'}])),shared:{},entity_shared:{}}});
  });
  await page.route('**/synthetic_financials',route=>route.fulfill({json:[
    {period:'2024-Q1',revenue:100,operatingIncome:20},{period:'2024-Q2',revenue:120,operatingIncome:25},
    {period:'2024-Q3',revenue:140,operatingIncome:30},{period:'2024-Q4',revenue:160,operatingIncome:40}]}));
  await page.goto(runtime.origin,{waitUntil:'domcontentloaded'});
  await page.getByLabel('Email',{exact:true}).fill(credential.email);
  await page.getByLabel('Password',{exact:true}).fill(credential.password);
  await page.getByRole('button',{name:'Login',exact:true}).click();
  await page.waitForURL(url=>!['/','/login'].includes(url.pathname),{timeout:20000});
  if(new URL(page.url()).pathname==='/onboarding'){
    await page.getByLabel('First Name',{exact:true}).fill('Synthetic');
    await page.getByLabel('Last Name',{exact:true}).fill('Capture');
    const updated=page.waitForResponse(response=>new URL(response.url()).pathname==='/api/user'&&
      response.request().method()==='PUT',{timeout:15000});
    await page.getByRole('button',{name:'Continue',exact:true}).click();
    if((await updated).status()!==200)throw Error('Synthetic profile update failed');
    await page.waitForFunction(()=>[...document.querySelectorAll('button')]
      .some(button=>button.textContent.trim()==='Continue'&&!button.disabled),null,{timeout:15000});
  }
  await page.goto(runtime.origin+'/app/11111111-1111-4111-8111-111111111111',{waitUntil:'domcontentloaded'});
  for(const value of ['2024-Q1','2024-Q2','2024-Q3','2024-Q4','100','140','160'])
    await page.getByText(value,{exact:true}).first().waitFor({state:'visible',timeout:15000});
  await page.locator('#chart-view-button').click();
  await page.locator('.ag-charts-canvas canvas').first().waitFor({state:'visible',timeout:15000});
  await settled();await installProjection();
  await page.locator('button').filter({has:page.locator('svg#list-unordered')}).click();
  await page.getByRole('menuitem',{name:'Chart settings',exact:true}).click();
  await page.getByRole('tab',{name:'Customize',exact:true}).click();
  await heading('Vertical Axis').waitFor({state:'visible'});await heading('Vertical Axis').click();
  await panel.getByRole('combobox',{name:'Position',exact:true}).waitFor({state:'visible'});
  await capture('baseline','original-application-real-ui',{action:'open groupedColumn Customize / Vertical Axis'});
  await uiAction('ui-axis-thickness-3',{control:'Vertical Axis / first Thickness',value:3},
    ()=>numberField('Thickness',0,3,2),()=>window.__referenceProxy.chart.chartOptions.processedOptions.axes
      .some(axis=>axis.position==='left'&&axis.line.enabled===true&&axis.line.width===3));
  await uiAction('ui-grid-thickness-4',{control:'Vertical Axis / Grid Lines / Thickness',value:4},
    ()=>numberField('Thickness',1,4,2),()=>window.__referenceProxy.chart.chartOptions.processedOptions.axes
      .some(axis=>axis.position==='left'&&axis.gridLine.width===4));
  await uiAction('ui-grid-dash-5',{control:'Vertical Axis / Grid Lines / Line Dash',value:5},
    ()=>numberField('Line Dash',0,5,1),()=>window.__referenceProxy.chart.chartOptions.processedOptions.axes
      .some(axis=>axis.position==='left'&&axis.gridLine.style[0].lineDash[0]===5));

  const cases=[
    {name:'synthetic-width-3-style-1',width:3,strokeWidth:1,lineDash:[2,7]},
    {name:'synthetic-width-1-style-4',width:1,strokeWidth:4,lineDash:[2,7]},
    {name:'synthetic-opacity-quarter',width:1,strokeWidth:4,lineDash:[2,7],strokeOpacity:0.25},
    {name:'synthetic-opacity-one',width:1,strokeWidth:4,lineDash:[2,7],strokeOpacity:1}
  ];
  for(const input of cases){
    const outcome=await page.evaluate(async input=>{
      const proxy=window.__referenceProxy;
      const initial=window.__axisSyntheticInitial??(window.__axisSyntheticInitial=proxy.getOptions());
      const theme=initial.theme,overrides=theme.overrides??{},bar=overrides.bar??{},axes=bar.axes??{};
      const number=axes.number??{},left=number.left??{};
      const style={stroke:'#123abc',strokeWidth:input.strokeWidth,lineDash:input.lineDash};
      if(input.strokeOpacity!==undefined)style.strokeOpacity=input.strokeOpacity;
      const gridLine={enabled:true,width:input.width,style:[style]};
      const nextTheme={...theme,overrides:{...overrides,bar:{...bar,axes:{...axes,number:{...number,
        left:{...left,gridLine}}}}}};
      await proxy.update({...initial,theme:nextTheme});await proxy.waitForUpdate();
      return {method:'reference proxy.update; synthetic theme override',gridLine};
    },input);
    const after=await capture(input.name,'synthetic-reference-public-update-no-ui-proof',{...input,outcome});
    ledger.push({name:input.name,kind:'synthetic-reference-public-update-no-ui-proof',input,outcome,after});
    json('action-ledger',ledger);
  }
  json('summary',{completed:true,uiActions:3,baseline:1,syntheticCases:4,
    scope:'Original runtime only. No candidate, persistence, provider or pixel-equivalence claim.'});
}catch(error){
  json('failure',{message:error.message,stack:error.stack?.replaceAll(runtime.origin,'[owned-origin]')});
  if(new URL(page.url()).pathname.startsWith('/app/')){
    await page.screenshot({path:root+'/failure.png'}).catch(()=>{});
    fs.writeFileSync(root+'/failure-ui.txt',await page.locator('body').innerText());
  }
  throw error;
}finally{
  json('diagnostics',{cdp:{runtimeEnabled:true,networkEnabled:true},errors,requests});
  await browser.close();
  json('browser-cleanup',{closed:true});
}
