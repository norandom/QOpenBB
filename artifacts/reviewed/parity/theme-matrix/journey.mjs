import {chromium} from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
const dir=process.env.CAPTURE_OUT||'/mnt/d/Source/QOpenBB/artifacts/parity/theme-matrix';
const input='/mnt/d/Source/QOpenBB/artifacts/parity/theme-matrix';
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
const writes=[];let stage='baseline';page.on('request',r=>{if(r.url().includes('/api/pro/dash/')&&r.method()==='POST'){try{const b=r.postDataJSON();if(b.items){const items=Object.fromEntries(Object.entries(b.items).filter(([k])=>k==='11111111-1111-4111-8111-111111111111'));writes.push({stage,items});fs.writeFileSync(dir+'/widget-writes.json',JSON.stringify(writes,null,2));}}catch{}}});
async function settle(label){stage=label;console.log('waiting '+label);await page.keyboard.press('Control+Shift+s');await page.waitForTimeout(10000);if(!writes.some(x=>x.stage===label)){console.log('timer fallback '+label);await page.waitForTimeout(12000);}fs.writeFileSync(dir+'/widget-writes.json',JSON.stringify(writes,null,2));console.log('settled '+label+' writes='+writes.filter(x=>x.stage===label).length);}
try{
await page.route('**/api/pro/dash/{sync,validate-and-sync}',async route=>{if(route.request().method()!=='GET')return route.continue();const upstream=await route.fetch();const actual=await upstream.json();const fixture=JSON.parse(fs.readFileSync(input+'/fixture.json').toString().replaceAll('http://127.0.0.1:32773',runtime.origin));await route.fulfill({json:{...actual,owned:Object.fromEntries(Object.entries(fixture).map(([id,content])=>[id,{content,is_shared:false,created_by:'Synthetic Parity',created_date:'2026-10-16T00:00:00Z',updated_date:'2026-10-16T00:00:00Z'}])),shared:{},entity_shared:{}}});}); await page.route('**/synthetic_financials',route=>route.fulfill({json:[{period:'2024-Q1',revenue:100,operatingIncome:20},{period:'2024-Q2',revenue:null,operatingIncome:null},{period:'2024-Q3',revenue:140,operatingIncome:30},{period:'2024-Q4',revenue:160,operatingIncome:40}]})); await page.goto(runtime.origin,{waitUntil:'networkidle'}); await page.getByLabel('Email',{exact:true}).fill(secrets.OPENBB_ADMIN_EMAIL); await page.getByLabel('Password',{exact:true}).fill(secrets.OPENBB_ADMIN_PASSWORD); await page.getByRole('button',{name:'Login',exact:true}).click(); await page.waitForTimeout(5000);if(page.url().endsWith('/onboarding')){await page.getByLabel('First Name',{exact:true}).fill('Synthetic');await page.getByLabel('Last Name',{exact:true}).fill('Capture');await page.getByRole('button',{name:'Continue',exact:true}).click();await page.waitForTimeout(3000);} await page.goto(runtime.origin+'/app/11111111-1111-4111-8111-111111111111',{waitUntil:'networkidle'}); await page.waitForTimeout(6000); await page.screenshot({path:dir+'/table-dark.png'});
for(const v of ['2024-Q1','2024-Q2','2024-Q3','2024-Q4','100','140','160'])if(!await page.getByText(v,{exact:true}).count())throw Error('Missing displayed '+v);
await page.locator('#chart-view-button').click();await page.waitForTimeout(3000);await page.screenshot({path:dir+'/chart-dark.png'});await settle('baseline');
fs.writeFileSync(dir+'/chart-dom.json',JSON.stringify({text:await page.locator('body').innerText(),html:await page.locator('#chart-view-button').evaluate(x=>x.outerHTML),canvases:await page.locator('canvas').count()},null,2));
async function acquire(){const discovery=await page.evaluate(()=>{const queue=[],seen=new Set(),found=[];for(const el of document.querySelectorAll('*'))for(const k of Object.keys(el))if(k.startsWith('__reactFiber')||k==='__agComponent')queue.push([el[k],k]);let n=0;while(queue.length&&n++<80000){const [o,path]=queue.shift();if(!o||typeof o!=='object'||seen.has(o)||o instanceof Node)continue;seen.add(o);let keys;try{keys=Object.keys(o)}catch{continue}if(keys.includes('chartOptions')||typeof o.getChartModels==='function'||typeof o.waitForUpdate==='function'){found.push({path,keys:keys.slice(0,100),model:typeof o.getChartModels==='function'});if(typeof o.waitForUpdate==='function')window.__referenceProxy=o;if(typeof o.getChartModels==='function')window.__referenceGrid=o;if(o.chartOptions?.processedOptions){window.__referenceChart=o;return {n,found,success:true}}}if(path.split('.').length>24)continue;for(const k of keys){if(['return','child','sibling','memoizedProps','memoizedState','stateNode','current','next','value','gridRef','chartRef','chart','api','context','ref'].includes(k)||path.includes('memoizedState')){try{queue.push([o[k],path+'.'+k])}catch{}}}}return {n,found,success:false}});
 return discovery;}
async function capture(mode,family){
 await acquire();
 const result=await page.evaluate(async({mode,family})=>{
 const p=window.__referenceProxy,g=window.__referenceGrid;await p.waitForUpdate();const model=g.getChartModels()[0];
 if(model?.chartType!==family||model?.chartThemeName!=='openbb-'+mode)throw Error('Model mismatch '+JSON.stringify({type:model?.chartType,theme:model?.chartThemeName}));
 const o=p.chart.chartOptions.processedOptions,u=p.getOptions();
 const pick=(x,ks)=>Object.fromEntries(ks.filter(k=>x?.[k]!==undefined).map(k=>[k,x[k]]));
 const text=x=>pick(x,['enabled','text','fontFamily','fontSize','fontWeight','color','spacing']);
 const row=x=>Object.fromEntries(['period','revenue','operatingIncome'].map(k=>[k,x?.[k]]));const rows=[];g.forEachNode(n=>rows.push(row(n.data)));return {model,gridRows:rows,inputData:u.data?.map(row),inputTheme:u.theme,effective:{mode,family,background:pick(o.background,['visible','fill']),padding:o.padding,title:text(o.title),subtitle:text(o.subtitle),legend:{...pick(o.legend,['enabled','position','spacing','maxHeight']),item:{...pick(o.legend?.item,['paddingX','paddingY']),marker:pick(o.legend?.item?.marker,['shape','size','padding','strokeWidth']),label:text(o.legend?.item?.label)}},axes:o.axes?.map(a=>({...pick(a,['type','position','keys']),title:text(a.title),label:text(a.label),line:pick(a.line,['enabled','color','width']),gridLine:a.gridLine})),series:o.series?.map(t=>({...pick(t,['type','xKey','yKey','yName','fill','stroke','fillOpacity','strokeOpacity','strokeWidth','stacked','grouped','connectMissingData']),marker:pick(t.marker,['enabled','shape','size','fill','stroke','strokeWidth']),label:text(t.label)}))}};
 },{mode,family});
 fs.writeFileSync(dir+'/'+mode+'-'+family+'.json',JSON.stringify(result,(k,v)=>typeof v==='function'?'[callback]':v,2));
 if(await page.getByRole('button',{name:'Confirm',exact:true}).count())await page.getByRole('button',{name:'Confirm',exact:true}).click();await page.waitForTimeout(1500);await page.screenshot({path:dir+'/'+mode+'-'+family+'.png'});await page.waitForTimeout(1500);await page.screenshot({path:dir+'/'+mode+'-'+family+'-stable.png'});console.log('CAPTURED '+mode+' '+family);
}
await capture('dark','groupedColumn');
async function openEditor(){
 const menu=page.locator('button').filter({has:page.locator('svg#list-unordered')});await menu.focus();await menu.press('Enter');await page.getByRole('menuitem',{name:'Chart settings',exact:true}).click();await page.waitForTimeout(600);
}
async function choose(mode,family,label){
 await page.getByRole('tab',{name:'Chart',exact:true}).click();await page.getByRole('button',{name:label,exact:true}).click();await page.waitForTimeout(700);await settle(mode+'-'+family);await capture(mode,family);
}
if(await page.getByRole('button',{name:'Confirm',exact:true}).count())await page.getByRole('button',{name:'Confirm',exact:true}).click();

await page.locator('button').filter({has:page.locator('svg#menu')}).click();await page.getByRole('link',{name:'Settings',exact:true}).click();await page.waitForTimeout(1000);
await page.getByTestId('theme-light').click();await page.waitForTimeout(1000);
await page.goto(runtime.origin+'/app/11111111-1111-4111-8111-111111111111',{waitUntil:'networkidle'});await page.waitForTimeout(3000);await page.locator('#chart-view-button').click();await page.waitForTimeout(1000);await settle('light-groupedColumn');await capture('light','groupedColumn');
if(await page.getByRole('button',{name:'Confirm',exact:true}).count())await page.getByRole('button',{name:'Confirm',exact:true}).click();
await openEditor();await choose('light','stackedColumn','Stacked Column');await choose('light','line','Line');
}catch(e){await page.screenshot({path:dir+'/failure.png'});fs.writeFileSync(dir+'/failure-ui.txt',await page.locator('body').innerText());throw e;}finally{fs.writeFileSync(dir+'/diagnostics.json',JSON.stringify({errors,requests},null,2));await browser.close();}