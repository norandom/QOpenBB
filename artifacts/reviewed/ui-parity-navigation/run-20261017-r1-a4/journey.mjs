import {chromium} from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {installProjection,acquireReferences,readState} from './projection.mjs';

const root=path.dirname(new URL(import.meta.url).pathname);
const runtime=JSON.parse(fs.readFileSync(root+'/runtime-private.json'));
const credential=JSON.parse(fs.readFileSync(root+'/credential-private.json'));
const json=(name,value)=>fs.writeFileSync(root+'/'+name+'.json',JSON.stringify(value,null,2));
const clean=text=>String(text).replaceAll(runtime.origin,'[owned-origin]').replaceAll(credential.password,'[redacted]')
  .replaceAll(credential.email,'[synthetic-account]').slice(0,1024);
const safeUrl=url=>{try{const parsed=new URL(url);return (parsed.origin===runtime.origin?'[owned-origin]':parsed.origin)+parsed.pathname;}catch{return '[invalid-url]';}};
const diagnostics=[],ledger=[],checkpoints=[],events=[];let phase='setup',appReady=false,cancelled=false,overflow=0;
const record=value=>{if(diagnostics.length<2048)diagnostics.push(value);else overflow++;};
const env={...process.env};delete env.WAYLAND_DISPLAY;
const browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle',
  '--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
const context=await browser.newContext({viewport:{width:1440,height:1000}});
const page=await context.newPage();page.setDefaultTimeout(6000);page.setDefaultNavigationTimeout(20000);
const cdp=await context.newCDPSession(page);await cdp.send('Runtime.enable');await cdp.send('Network.enable');
page.on('console',message=>{if(['error','warning'].includes(message.type()))record({kind:'console',type:message.type(),text:clean(message.text())});});
page.on('pageerror',error=>record({kind:'pageerror',text:clean(error.message)}));
cdp.on('Runtime.exceptionThrown',event=>record({kind:'cdp-exception',text:clean(event.exceptionDetails.text),
  description:clean(event.exceptionDetails.exception?.description||''),url:safeUrl(event.exceptionDetails.url||'')}));
cdp.on('Network.loadingFailed',event=>record({kind:'cdp-network-failed',errorText:event.errorText,canceled:event.canceled,type:event.type}));
page.on('response',response=>record({kind:'response',url:safeUrl(response.url()),status:response.status()}));
await page.route('**/*',async route=>{
  const url=new URL(route.request().url());
  if(url.origin!==runtime.origin){record({kind:'blocked-external',url:safeUrl(url.href)});return route.abort();}
  return route.continue();
});
const assert=(condition,message)=>{if(!condition)throw Error(message);};
const panel=page.locator('.ag-chart-docked-container');
const heading=label=>page.locator('.ag-charts-format-top-level-group-title-bar').filter({hasText:new RegExp('^\\s*'+label+'\\s*$')});
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
let chartBaseline=null,tableBaseline=null;

async function acquire(){return page.evaluate(acquireReferences);}
async function state(){await acquire();return page.evaluate(readState);}
function checkSource(s){
  assert(s.sourceRows.length===4,'Four source rows required');
  const values=s.sourceRows.map(({period,revenue,operatingIncome})=>({period,revenue,operatingIncome}));
  assert(JSON.stringify(values)===JSON.stringify([
    {period:'2024-Q1',revenue:100,operatingIncome:20},{period:'2024-Q2',revenue:120,operatingIncome:25},
    {period:'2024-Q3',revenue:140,operatingIncome:30},{period:'2024-Q4',revenue:160,operatingIncome:40}]),'Source observations changed');
}
async function settled(){
  const found=await acquire();
  if(found.chart){
    await Promise.race([page.evaluate(()=>window.__navigationProxy.waitForUpdate()),delay(10000).then(()=>{throw Error('Original update deadline');})]);
    await page.waitForFunction(()=>!window.__navigationProxy.chart.ctx.animationManager.isActive(),null,{timeout:10000,polling:50});
  }
  let previous=null;const deadline=Date.now()+10000;
  while(Date.now()<deadline){
    const sample=await page.evaluate(()=>{
      const panel=document.querySelector('.ag-chart-docked-container'),canvas=document.querySelector('.ag-charts-canvas');
      const rect=node=>node?{w:node.clientWidth,h:node.clientHeight}:null;
      return JSON.stringify({panel:rect(panel),canvas:rect(canvas),tab:[...document.querySelectorAll('[role=tab][aria-selected=true]')]
        .map(node=>node.textContent),scroll:panel?[...panel.querySelectorAll('*')].filter(node=>node.scrollTop).map(node=>node.scrollTop):[]});
    });
    if(sample===previous)return;previous=sample;await delay(100);
  }
  throw Error('Layout settlement deadline');
}
async function snap(name,{settle=true,image=true}={}){
  if(cancelled)throw Error('Journey cancelled');
  if(settle)await settled();
  const s=await state();checkSource(s);
  json(name,s);if(image)await page.screenshot({path:root+'/'+name+'.png'});
  checkpoints.push({name,phase,chartType:s.chart?.model.chartType||null,selectedTab:s.dom.tabs.find(tab=>tab.selected==='true')?.label,
    omittedCount:s.budget.omittedCount});json('checkpoints',checkpoints);
  return s;
}
async function action(label,run){
  if(cancelled)throw Error('Journey cancelled');
  const before=Date.now();await run();ledger.push({phase,label,kind:'original-application-real-ui',elapsedMs:Date.now()-before});json('action-ledger',ledger);
}
async function runCase(id,run){
  phase=id;console.log('CASE '+id);const began=Date.now();
  let timer;try{await Promise.race([run(),new Promise((_,reject)=>{timer=setTimeout(()=>{cancelled=true;reject(Error(id+' case deadline'));},30000);})]);
    events.push({id,status:'observed',elapsedMs:Date.now()-began});json('cases',events);
  }finally{clearTimeout(timer);}
}
async function openSettings(){
  await action('widget-menu-open',()=>page.locator('button').filter({has:page.locator('svg#list-unordered')}).click());
  await action('external-chart-settings',()=>page.getByRole('menuitem',{name:'Chart settings',exact:true}).click());
  await panel.waitFor({state:'visible'});await delay(350);
}
async function closeSettings(){
  await action('dock-close',()=>page.locator('.ag-tabs-close-button.ag-chart-tabbed-menu-close-button').click());
  await page.waitForFunction(()=>!document.querySelector('.ag-chart-menu-visible'),null,{timeout:6000});
}
async function tab(label){await action('tab-'+label,()=>page.getByRole('tab',{name:label,exact:true}).click());}
async function prepareCustomize(){
  await tab('Customize');
  const h=heading('Vertical Axis');await h.waitFor({state:'visible'});
  const isExpanded=await h.evaluate(node=>node.parentElement.className.includes('ag-charts-format-top-level-group-expanded')||
    node.closest('.ag-charts-format-top-level-group')?.className.includes('expanded'));
  if(!isExpanded){
    const visibleThickness=panel.locator('.ag-slider').filter({has:page.locator('label').filter({hasText:/^Thickness$/})}).locator('input[type=number]:visible');
    if(await visibleThickness.count()===0)await action('expand-vertical-axis',()=>h.click());
  }
  const numbers=panel.locator('.ag-slider').filter({has:page.locator('label').filter({hasText:/^Thickness$/})}).locator('input[type=number]:visible');
  assert(await numbers.count()===2,'Expected axis and existing Grid Lines Thickness controls');
  const checkedBefore=await panel.getByRole('checkbox',{name:'Grid Lines',exact:true}).isChecked();
  await numbers.nth(1).scrollIntoViewIfNeeded();
  const bounds=await panel.boundingBox();await page.mouse.move(bounds.x+bounds.width/2,bounds.y+bounds.height/2);
  await action('panel-wheel',()=>page.mouse.wheel(0,130));
  await action('focus-grid-thickness-no-edit',()=>numbers.nth(1).click());
  assert(await panel.getByRole('checkbox',{name:'Grid Lines',exact:true}).isChecked()===checkedBefore,'Grid Lines changed');
}
async function keyboardFocus(locator,label){
  for(let count=0;count<40;count++){
    if(await locator.evaluate(node=>node===document.activeElement))return;
    await action('focus-traversal-'+label,()=>page.keyboard.press('Tab'));
  }
  throw Error('Bounded focus traversal could not reach '+label);
}

let journeyTimer;
try{
  journeyTimer=setTimeout(()=>{cancelled=true;page.close().catch(()=>{});},360000);
  await page.route('**/api/pro/dash/{sync,validate-and-sync}',async route=>{
    if(route.request().method()!=='GET')return route.continue();
    const upstream=await route.fetch(),actual=await upstream.json();
    const fixture=JSON.parse(fs.readFileSync(root+'/fixture.json','utf8').replaceAll('http://127.0.0.1:32773',runtime.origin));
    return route.fulfill({json:{...actual,owned:Object.fromEntries(Object.entries(fixture).map(([id,content])=>[id,{content,
      is_shared:false,created_by:'Synthetic Parity',created_date:'2026-10-17T00:00:00Z',updated_date:'2026-10-17T00:00:00Z'}])),shared:{},entity_shared:{}}});
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
    await page.getByLabel('First Name',{exact:true}).fill('Synthetic');await page.getByLabel('Last Name',{exact:true}).fill('Navigation');
    const updated=page.waitForResponse(response=>new URL(response.url()).pathname==='/api/user'&&response.request().method()==='PUT',{timeout:15000});
    await page.getByRole('button',{name:'Continue',exact:true}).click();assert((await updated).status()===200,'Profile update failed');
    await page.waitForFunction(()=>[...document.querySelectorAll('button')].some(button=>button.textContent.trim()==='Continue'&&!button.disabled),null,{timeout:15000});
  }
  await page.goto(runtime.origin+'/app/11111111-1111-4111-8111-111111111111',{waitUntil:'domcontentloaded'});
  for(const text of ['2024-Q1','2024-Q2','2024-Q3','2024-Q4','100','140','160'])await page.getByText(text,{exact:true}).first().waitFor({state:'visible',timeout:15000});
  appReady=true;await page.evaluate(installProjection);await acquire();
  await runCase('N01',async()=>{
    await snap('N01-table-initial');
    await action('hover-revenue-header',()=>page.locator('.ag-header-cell[col-id="revenue"]').hover());
    const resize=page.locator('.ag-header-cell[col-id="revenue"] .ag-header-cell-resize');
    const bounds=await resize.boundingBox();assert(bounds,'Revenue resize handle absent');
    await action('resize-revenue',async()=>{await page.mouse.move(bounds.x+bounds.width/2,bounds.y+bounds.height/2);await page.mouse.down();
      await page.mouse.move(bounds.x+70,bounds.y+bounds.height/2,{steps:8});await page.mouse.up();});
    await action('select-q2-revenue',()=>page.locator('.ag-row[row-index="1"] .ag-cell[col-id="revenue"]').click());
    await action('extend-q3-income',()=>page.locator('.ag-row[row-index="2"] .ag-cell[col-id="operatingIncome"]').click({modifiers:['Shift']}));
    await snap('N01-click-selection-observed');
    const start=await page.locator('.ag-row[row-index="1"] .ag-cell[col-id="revenue"]').boundingBox();
    const end=await page.locator('.ag-row[row-index="2"] .ag-cell[col-id="operatingIncome"]').boundingBox();
    await action('drag-finite-cell-range',async()=>{await page.mouse.move(start.x+start.width/2,start.y+start.height/2);await page.mouse.down();
      await page.mouse.move(end.x+Math.min(50,end.width/2),end.y+end.height/2,{steps:12});await page.mouse.up();});
    tableBaseline=await snap('N01-table-pre-entry');json('selection-discriminator',{
      resolved:tableBaseline.table.ranges.length>0,rangeCount:tableBaseline.table.ranges.length,
      policy:'If empty after one real drag, continue independent navigation and retain unresolved selection discriminator'});
    await action('chart-enter',()=>page.locator('#chart-view-button').click());
    await page.locator('.ag-charts-canvas canvas').first().waitFor({state:'visible',timeout:15000});
    chartBaseline=await snap('N01-chart-entered');assert(chartBaseline.chart.model.chartType==='groupedColumn','Initial family');
  });
  await runCase('N02',async()=>{await openSettings();await tab('Chart');await snap('N02-Chart');await tab('Set Up');await snap('N02-Set-Up');
    await prepareCustomize();await snap('N02-Customize-prepared');});
  await runCase('N03',async()=>{await snap('N03-pre-close');await closeSettings();await snap('N03-immediate-closed',{settle:false});
    await snap('N03-closed');});
  await runCase('N04',async()=>{await snap('N04-pre-reopen');await openSettings();await snap('N04-reopened');});
  await runCase('N05',async()=>{await tab('Set Up');const box=panel.getByRole('checkbox',{name:'Aggregate',exact:true});
    const checked=await box.isChecked();await keyboardFocus(box,'Aggregate');assert(await box.isChecked()===checked,'Aggregate changed');
    await snap('N05-pre-close');await closeSettings();await snap('N05-closed');await openSettings();await snap('N05-reopened');});
  await runCase('N06',async()=>{await tab('Chart');const thumb=panel.getByRole('button',{name:'Grouped Column. Selected',exact:true});
    await keyboardFocus(thumb,'Grouped-Column');await snap('N06-pre-close');await closeSettings();await snap('N06-closed');await openSettings();await snap('N06-reopened');});
  await runCase('N07',async()=>{await prepareCustomize();const before=await snap('N07-dark-pre');assert(before.dom.dark,'Expected dark baseline');
    await action('theme-dark-to-light',()=>page.keyboard.press('Control+m'));await page.waitForFunction(()=>!document.documentElement.classList.contains('dark'));
    await snap('N07-light-immediate',{settle:false});await snap('N07-light');});
  await runCase('N08',async()=>{await snap('N08-light-pre');await action('theme-light-to-dark',()=>page.keyboard.press('Control+m'));
    await page.waitForFunction(()=>document.documentElement.classList.contains('dark'));await snap('N08-dark-immediate',{settle:false});await snap('N08-dark');});
  await runCase('N09',async()=>{await prepareCustomize();await snap('N09-column-pre');await tab('Chart');await action('family-line',()=>panel.getByRole('button',{name:'Line',exact:true}).click());
    const result=await snap('N09-line-untouched');assert(result.chart.model.chartType==='line','Line family effect missing');await tab('Customize');await snap('N09-line-Customize');});
  await runCase('N10',async()=>{await snap('N10-line-pre');await tab('Chart');await action('family-groupedColumn',()=>panel.getByRole('button',{name:'Grouped Column',exact:true}).click());
    const result=await snap('N10-column-untouched');assert(result.chart.model.chartType==='groupedColumn','Column family effect missing');await tab('Customize');await snap('N10-column-Customize');});
  await runCase('N11',async()=>{await snap('N11-chart-pre');await action('chart-exit',()=>page.locator('#chart-view-button').click());
    await page.locator('.ag-row[row-index="0"] .ag-cell[col-id="period"]').waitFor({state:'visible'});await snap('N11-table-first',{settle:false});
    await delay(1200);const a=await snap('N11-table-restored');await delay(100);const b=await snap('N11-table-stable');
    assert(JSON.stringify(a.columnState)===JSON.stringify(b.columnState),'Widths did not settle');
    json('table-width-comparison',{before:tableBaseline.columnState,after:b.columnState,
      equal:JSON.stringify(tableBaseline.columnState)===JSON.stringify(b.columnState)});assert(!b.chart,'Chart not destroyed');});
  await runCase('N12',async()=>{await snap('N12-table-pre');await action('chart-reenter',()=>page.locator('#chart-view-button').click());
    await page.locator('.ag-charts-canvas canvas').first().waitFor({state:'visible'});const s=await snap('N12-chart-untouched');
    assert(s.chart.model.chartType==='groupedColumn','Reentry family');if(!s.dom.menuVisible){await openSettings();await snap('N12-manually-reopened');}});
  json('summary',{status:'observed',cases:events,checkpointCount:checkpoints.length,actions:ledger.length,
    initialRange:chartBaseline.chart.model.cellRange,sourceFixtureRows:4,candidateExecuted:false});
}catch(error){
  json('failure',{phase,error:clean(error.message),stack:clean(error.stack),completedCases:events.map(item=>item.id)});
  if(appReady&&!page.isClosed()){try{await snap('failure-state',{settle:false});}catch(captureError){json('failure-capture',{error:clean(captureError.message)});}}
  throw error;
}finally{
  clearTimeout(journeyTimer);cancelled=true;json('diagnostics',{events:diagnostics,overflow});
  await browser.close();json('browser-cleanup',{browserClosed:!browser.isConnected()});
}
