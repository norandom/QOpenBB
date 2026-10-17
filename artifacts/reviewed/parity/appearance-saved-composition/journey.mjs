import {chromium} from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
const dir=process.env.CAPTURE_OUT||'/mnt/d/Source/QOpenBB/artifacts/parity/appearance-saved-composition';
const input='/mnt/d/Source/QOpenBB/artifacts/parity/appearance-saved-composition';
const runtime=JSON.parse(fs.readFileSync(input+'/runtime.json'));
const credential=JSON.parse(fs.readFileSync(input+'/credential-private.json'));const secrets={OPENBB_ADMIN_EMAIL:credential.email,OPENBB_ADMIN_PASSWORD:credential.password};
const env={...process.env};delete env.WAYLAND_DISPLAY;
const browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
const context=await browser.newContext({viewport:{width:1440,height:1000}});const page=await context.newPage();const errors=[],requests=[];page.on('console',m=>{if(m.type()==='error')errors.push({type:'console',text:m.text()});});
const cdp=await context.newCDPSession(page);await cdp.send('Runtime.enable');await cdp.send('Network.enable');
cdp.on('Runtime.exceptionThrown',e=>errors.push({type:'exception',message:e.exceptionDetails.text,details:e.exceptionDetails.exception?.description,stack:e.exceptionDetails.stackTrace,url:e.exceptionDetails.url,line:e.exceptionDetails.lineNumber,scriptId:e.exceptionDetails.scriptId}));
cdp.on('Network.loadingFailed',e=>errors.push({type:'network',...e}));
page.on('pageerror',e=>errors.push({type:'pageerror',message:e.message}));
await page.route('**/*',async route=>{const url=new URL(route.request().url());if(url.origin!==runtime.origin){requests.push({blocked:url.origin+url.pathname});await route.abort();}else await route.continue();});
page.on('response',r=>{if(new URL(r.url()).origin===runtime.origin)requests.push({url:r.url(),status:r.status(),contentType:r.headers()["content-type"]});});
const cases=JSON.parse(fs.readFileSync(dir+'/case-inputs.json'));let active=cases[0];const writes=[];let stage='baseline';page.on('request',r=>{if(r.url().includes('/api/pro/dash/')&&r.method()==='POST'){try{const b=r.postDataJSON();if(b.items){const items=Object.fromEntries(Object.entries(b.items).filter(([k])=>k==='11111111-1111-4111-8111-111111111111'));writes.push({stage,items});fs.writeFileSync(dir+'/widget-writes.json',JSON.stringify(writes,null,2));}}catch{}}});
async function settle(label){stage=label;console.log('waiting '+label);await page.keyboard.press('Control+Shift+s');await page.waitForTimeout(10000);if(!writes.some(x=>x.stage===label)){console.log('timer fallback '+label);await page.waitForTimeout(12000);}fs.writeFileSync(dir+'/widget-writes.json',JSON.stringify(writes,null,2));console.log('settled '+label+' writes='+writes.filter(x=>x.stage===label).length);}
try{
await page.route('**/api/pro/dash/{sync,validate-and-sync}',async route=>{if(route.request().method()!=='GET')return route.continue();const upstream=await route.fetch();const actual=await upstream.json();const fixture=JSON.parse(fs.readFileSync(input+'/fixture.json').toString().replaceAll('http://127.0.0.1:32773',runtime.origin));fixture['11111111-1111-4111-8111-111111111111'].data.widgets[0].storage={chartView:{enabled:false},default:{chartModel:{chartType:active.family,chartThemeName:'openbb-dark',cellRange:{columns:['period','revenue','operatingIncome']},chartOptions:active.saved}}};await route.fulfill({json:{...actual,owned:Object.fromEntries(Object.entries(fixture).map(([id,content])=>[id,{content,is_shared:false,created_by:'Synthetic Parity',created_date:'2026-10-16T00:00:00Z',updated_date:'2026-10-16T00:00:00Z'}])),shared:{},entity_shared:{}}});}); await page.route('**/synthetic_financials',route=>route.fulfill({json:[{period:'2024-Q1',revenue:100,operatingIncome:20},{period:'2024-Q2',revenue:null,operatingIncome:null},{period:'2024-Q3',revenue:140,operatingIncome:30},{period:'2024-Q4',revenue:160,operatingIncome:40}]})); await page.goto(runtime.origin,{waitUntil:'networkidle'}); await page.getByLabel('Email',{exact:true}).fill(secrets.OPENBB_ADMIN_EMAIL); await page.getByLabel('Password',{exact:true}).fill(secrets.OPENBB_ADMIN_PASSWORD); await page.getByRole('button',{name:'Login',exact:true}).click(); await page.waitForTimeout(5000);if(page.url().endsWith('/onboarding')){await page.getByLabel('First Name',{exact:true}).fill('Synthetic');await page.getByLabel('Last Name',{exact:true}).fill('Capture');await page.getByRole('button',{name:'Continue',exact:true}).click();await page.waitForTimeout(3000);} await page.goto(runtime.origin+'/app/11111111-1111-4111-8111-111111111111',{waitUntil:'networkidle'}); await page.waitForTimeout(6000); await page.screenshot({path:dir+'/table-dark.png'});
for(const v of ['2024-Q1','2024-Q2','2024-Q3','2024-Q4','100','140','160'])if(!await page.getByText(v,{exact:true}).count())throw Error('Missing displayed '+v);
async function acquire(){return page.evaluate(()=>{
 const roots=[...document.querySelectorAll('.ag-root-wrapper')];
 for(const root of roots){let f=root[Object.keys(root).find(k=>k.startsWith('__reactFiber'))];
  for(let level=0;f&&level<18;level++,f=f.return){
   const value=f.memoizedProps?.value;
   const g=value?.gridRef?.current?.api||f.child?.stateNode?.api;
   if(typeof g?.getChartModels==='function')window.__referenceGrid=g;
   const p=value?.chartRef?.current?.chart;
   if(typeof p?.getOptions==='function')window.__referenceProxy=p;
  }
 }
 const g=window.__referenceGrid;if(!g)throw Error('No finite grid reference');
 const model=g.getChartModels()[0];const p=g.getChartRef(model.chartId).chart;window.__referenceProxy=p;
 return {grid:true,proxy:typeof p.getOptions==='function',processed:!!p.chart?.chartOptions?.processedOptions};
});}
const outputs=[];
for(const c of cases){active=c;stage=c.id;await page.goto(runtime.origin+'/app/11111111-1111-4111-8111-111111111111',{waitUntil:'networkidle'});await page.waitForTimeout(2200);if(await page.locator('#chart-view-button').isVisible())await page.locator('#chart-view-button').click();await page.waitForTimeout(1800);await acquire();
const result=await page.evaluate(async ({id,saved,family})=>{
 const g=window.__referenceGrid,p=window.__referenceProxy;await p.waitForUpdate();const model=g.getChartModels()[0],o=p.chart.chartOptions.processedOptions;
 const pick=(x,keys)=>Object.fromEntries(keys.map(k=>[k,{presence:!Object.hasOwn(x??{},k)?'absent':x[k]===undefined?'undefined':x[k]===null?'null':'value',...(x?.[k]!==undefined?{value:x[k]}:{})}]));
 const title=x=>pick(x,['enabled','text','color','fontSize']);const series=x=>({...pick(x,['fill','stroke','strokeWidth','connectMissingData']),marker:pick(x?.marker,['enabled','fill','stroke','strokeWidth','shape','size'])});
 const branch=x=>({title:title(x?.title),legend:pick(x?.legend,['enabled','position']),series:series(x?.series),axes:x?.axes?Object.fromEntries(Object.entries(x.axes).map(([k,a])=>[k,{label:pick(a.label,['color']),left:{label:pick(a.left?.label,['color'])}}])):null});
 const project=x=>Object.fromEntries(['common','bar','line'].filter(k=>x?.[k]).map(k=>[k,branch(x[k])]));
 const combined=g.getGridOption('chartThemeOverrides');
 return {actionId:id,syntheticSavedFixture:saved,requestedFamily:family,model:{chartType:model.chartType,chartThemeName:model.chartThemeName,chartOptions:project(model.chartOptions)},hookCombined:project(combined),effective:{title:title(o.title),legend:pick(o.legend,['enabled','position']),axes:o.axes.map(a=>({type:a.type,position:a.position,label:pick(a.label,['color'])})),series:o.series.map(a=>({type:a.type,yKey:a.yKey,...series(a)}))}};
},c);if(result.model.chartType!==c.family)throw Error('Requested family mismatch '+c.id);if(!Object.keys(result.hookCombined).length)throw Error('Missing hook-combined projection '+c.id);outputs.push(result);fs.writeFileSync(dir+'/cases.json',JSON.stringify(outputs,null,2));await page.screenshot({path:dir+'/'+c.id+'.png'});console.log('CASE '+c.id);}
}catch(e){fs.writeFileSync(dir+'/failure.json',JSON.stringify({error:e.message,stack:e.stack}));throw e;}finally{fs.writeFileSync(dir+'/diagnostics.json',JSON.stringify({errors,requests},null,2));await browser.close();}
