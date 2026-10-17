import {chromium} from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
import {root,json,budget} from './io.mjs';
import {install,acquire,read} from './projection.mjs';
const runtime=JSON.parse(fs.readFileSync(root+'/runtime-private.json')),credential=JSON.parse(fs.readFileSync(root+'/credential-private.json'));
const clean=value=>String(value).replaceAll(runtime.origin,'[owned-origin]').replaceAll(credential.email,'[synthetic-account]').replaceAll(credential.password,'[redacted]').slice(0,1024);
const safeUrl=value=>{try{const u=new URL(value);return (u.origin===runtime.origin?'[owned-origin]':'[blocked-origin]')+u.pathname.slice(0,256);}catch{return '[invalid-url]';}};
const diagnostics=[],statuses=new Map(),ledger=[],cases=[],shots=[];let overflow=false,ready=false,phase='setup',actions=0,changes=0,sequence=0,cancelled=false;
const record=v=>{if(diagnostics.length>=128){overflow=true;return;}diagnostics.push(v);};
const assert=(v,message)=>{if(!v)throw Error(message);};
const env={...process.env};delete env.WAYLAND_DISPLAY;
let browser,context,page,timer;
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function one(locator){await locator.waitFor({state:'visible',timeout:4000});const count=await locator.count();assert(count===1,'Unique target required; got '+count);return locator;}
async function state(){await page.evaluate(acquire);return page.evaluate(read);}
async function settled(){await page.evaluate(acquire);
  await Promise.race([page.evaluate(()=>window.__colorProxy.waitForUpdate()),delay(10000).then(()=>{throw Error('Update deadline');})]);
  await page.waitForFunction(()=>window.__colorProxy.chart.ctx.animationManager.isActive()===false,null,{timeout:10000,polling:50});}
async function saveState(name,{image=false}={}){
  await settled();const value=await state();json(name,value,{snapshot:true});
  if(image){assert(shots.length<24,'Screenshot checkpoint cap');await page.screenshot({path:root+'/'+name+'.png'});shots.push(name);json('screenshots',shots);}
  return value;
}
async function action(label,locator,method,arg,{change=false,image=false,keyboard=false}={}){
  assert(!cancelled&&!overflow,'Cancelled/diagnostic overflow');assert(++actions<=80,'Action cap');if(change)assert(++changes<=20,'Mutation cap');
  const id=phase+'.s'+String(++sequence).padStart(2,'0'),target=locator?await one(locator):null;
  const before=ready?await saveState(id+'-before'):null,start=Date.now();
  if(ready)await page.evaluate(id=>{window.__color.action=id;},id);
  const focused=ready?await page.evaluate(()=>window.__color.el(document.activeElement)):null;
  if(keyboard)await page.keyboard.press(arg);else if(target)await target[method](arg);else await page[method](arg);
  const after=ready?await saveState(id+'-after',{image}):null;
  const entry={id,label,method,intendedValue:arg==null?null:clean(arg),uniqueLocatorCount:target?1:null,focusedBefore:focused,
    focusedAfter:after?.dom.active??null,before:before?id+'-before.json':null,after:after?id+'-after.json':null,
    eventSequence:{from:before?.eventSequence??0,to:after?.eventSequence??0},elapsedMs:Date.now()-start,image:image?id+'-after.png':null,outcome:'observed'};
  ledger.push(entry);json('action-ledger',ledger);if(ready)json('events',await page.evaluate(()=>window.__color.events));return after;
}
const group=label=>page.locator('.ag-charts-format-top-level-group').filter({has:page.locator('.ag-charts-format-top-level-group-title-bar').filter({hasText:new RegExp('^\\s*'+label+'\\s*$')})});
async function expand(label){const h=group(label).locator('.ag-charts-format-top-level-group-title-bar');await one(h);
  const expanded=await h.evaluate(n=>n.closest('.ag-charts-format-top-level-group').className.includes('expanded'));
  if(!expanded)await action('Expand '+label,h,'click');}
const picker=(label,ref)=>group(label).locator('[data-ref='+ref+'] .ag-picker-field-wrapper');
const popup=()=>page.locator('.ag-color-panel');
const colorText=()=>popup().locator('input[type=text]');
async function press(label,key,{change=false,image=false,target=null}={}){return action(label,target,'press',key,{change,image,keyboard:!target});}
async function openColor(label,target,key='Enter',image=true){await action(label+' focus',target,'focus');await press(label+' open',key,{target,image});await one(popup());}
async function number(label,value){const target=group('Series').locator('[data-ref=shadowGroup] .ag-slider').filter({has:page.locator('label').filter({hasText:new RegExp('^'+label+'$')})}).locator('input[type=number]');
  await action(label+' fill',target,'fill',String(value),{change:true,image:true});await press(label+' commit','Tab',{target,image:true});}
async function runCase(id,fn){phase=id;sequence=0;const began=Date.now();await fn();cases.push({id,status:'observed',elapsedMs:Date.now()-began});json('cases',cases);}
try{
  browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
  timer=setTimeout(()=>{cancelled=true;page?.close().catch(()=>{});},240000);
  context=await browser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1});page=await context.newPage();
  page.setDefaultTimeout(6000);page.setDefaultNavigationTimeout(20000);const cdp=await context.newCDPSession(page);
  await cdp.send('Runtime.enable');await cdp.send('Network.enable');
  page.on('console',m=>{if(['error','warning'].includes(m.type()))record({kind:'console',type:m.type(),text:clean(m.text())});});
  page.on('pageerror',e=>record({kind:'pageerror',text:clean(e.message)}));
  cdp.on('Runtime.exceptionThrown',e=>record({kind:'cdp-exception',text:clean(e.exceptionDetails.text),description:clean(e.exceptionDetails.exception?.description||'')}));
  cdp.on('Network.loadingFailed',e=>record({kind:'cdp-loading-failed',text:clean(e.errorText),canceled:e.canceled,type:e.type}));
  page.on('response',r=>{const key=safeUrl(r.url())+' '+r.status();if(!statuses.has(key)&&statuses.size>=256){overflow=true;return;}statuses.set(key,(statuses.get(key)||0)+1);});
  await page.route('**/*',route=>{if(new URL(route.request().url()).origin!==runtime.origin){record({kind:'blocked-origin',url:safeUrl(route.request().url())});return route.abort();}return route.continue();});
  await page.route('**/api/pro/dash/{sync,validate-and-sync}',async route=>{
    if(route.request().method()!=='GET')return route.continue();const upstream=await route.fetch(),actual=await upstream.json();
    const fixture=JSON.parse(fs.readFileSync(new URL('./fixture.json',import.meta.url),'utf8').replaceAll('http://127.0.0.1:32773',runtime.origin));
    return route.fulfill({json:{...actual,owned:Object.fromEntries(Object.entries(fixture).map(([id,content])=>[id,{content,is_shared:false,
      created_by:'Synthetic Parity',created_date:'2026-10-17T00:00:00Z',updated_date:'2026-10-17T00:00:00Z'}])),shared:{},entity_shared:{}}});});
  await page.route('**/synthetic_financials',route=>route.fulfill({json:[{period:'2024-Q1',revenue:100,operatingIncome:20},
    {period:'2024-Q2',revenue:120,operatingIncome:25},{period:'2024-Q3',revenue:140,operatingIncome:30},{period:'2024-Q4',revenue:160,operatingIncome:40}]}));
  await action('Login navigation',null,'goto',runtime.origin);await action('Email',page.getByLabel('Email',{exact:true}),'fill',credential.email);
  await action('Password',page.getByLabel('Password',{exact:true}),'fill',credential.password);await action('Login',page.getByRole('button',{name:'Login',exact:true}),'click');
  await page.waitForURL(url=>!['/','/login'].includes(url.pathname),{timeout:20000});
  if(new URL(page.url()).pathname==='/onboarding'){
    await action('First name',page.getByLabel('First Name',{exact:true}),'fill','Synthetic');await action('Last name',page.getByLabel('Last Name',{exact:true}),'fill','Color Shadow');
    const updated=page.waitForResponse(r=>new URL(r.url()).pathname==='/api/user'&&r.request().method()==='PUT',{timeout:6000});
    await action('Continue',page.getByRole('button',{name:'Continue',exact:true}),'click');assert((await updated).status()===200,'Profile PUT failed');
    await page.waitForFunction(()=>location.pathname.startsWith('/app')||[...document.querySelectorAll('button')].some(b=>b.textContent.trim()==='Continue'&&!b.disabled),null,{timeout:6000});
    json('onboarding-receipt',{profilePutStatus:200,appNavigationOrContinueEnabled:true});
  }
  await action('Synthetic dashboard',null,'goto',runtime.origin+'/app/11111111-1111-4111-8111-111111111111');
  for(const value of ['2024-Q1','2024-Q2','2024-Q3','2024-Q4','100','140','160'])await page.getByText(value,{exact:true}).first().waitFor({state:'visible',timeout:6000});
  await action('Chart entry',page.locator('#chart-view-button'),'click');await page.locator('.ag-charts-canvas canvas').first().waitFor({state:'visible',timeout:6000});
  await page.evaluate(install);const identity=await page.evaluate(acquire);assert(identity.chartType==='groupedColumn','Baseline family');
  assert(await page.evaluate(()=>document.documentElement.classList.contains('dark')),'Baseline dark theme');ready=true;
  await action('Widget menu',page.locator('button').filter({has:page.locator('svg#list-unordered')}),'click');
  await action('Chart settings',page.getByRole('menuitem',{name:'Chart settings',exact:true}),'click');
  await action('Customize',page.getByRole('tab',{name:'Customize',exact:true}),'click');
  await runCase('C01',async()=>{await expand('Horizontal Axis');await saveState('C01-axis-baseline');await expand('Vertical Axis');
    await saveState('C01-grid-baseline');await expand('Series');await saveState('C01-baseline',{image:true});});
  await runCase('C02',async()=>{await expand('Horizontal Axis');const target=picker('Horizontal Axis','axisColorInput');await openColor('Axis Color',target);
    const spectrum=popup().locator('.ag-spectrum-color');await one(spectrum);assert(await spectrum.evaluate(n=>n===document.activeElement),'Spectrum initial focus');
    await press('Spectrum Right','ArrowRight',{change:true,image:true});await press('Tab hue','Tab');
    assert(await popup().locator('[data-ref=spectrumHueSlider]').evaluate(n=>n===document.activeElement),'Hue focus');
    await press('Hue Right','ArrowRight',{change:true,image:true});await press('Tab alpha','Tab');
    assert(await popup().locator('[data-ref=spectrumAlphaSlider]').evaluate(n=>n===document.activeElement),'Alpha focus');
    await press('Alpha Left','ArrowLeft',{change:true,image:true});await press('Tab text','Tab');
    await action('Axis hex6',colorText(),'fill','#E34B55',{change:true,image:true});await press('Axis Enter','Enter',{target:colorText(),image:true});
    await openColor('Axis reopen',target,'Enter',false);await press('Axis Escape','Escape',{image:true});});
  await runCase('C03',async()=>{await expand('Vertical Axis');await openColor('Grid Color',picker('Vertical Axis','gridLineColorPicker'),'Space');
    const before=await state();await action('Invalid grid token',colorText(),'fill','not-a-color',{change:true,image:true});
    const invalid=await state();json('C03-invalid-check',{eventsUnchanged:before.eventSequence===invalid.eventSequence,
      input:invalid.dom.popup.records.find(r=>r.tag==='INPUT')});assert(before.eventSequence===invalid.eventSequence,'Invalid color emitted event');
    await action('Grid hex8',colorText(),'fill','#27C6A080',{change:true,image:true});await press('Grid Enter','Enter',{target:colorText(),image:true});});
  const toggle=()=>group('Series').getByRole('checkbox',{name:'Shadow',exact:true});
  await runCase('C04',async()=>{await expand('Series');assert(!(await (await one(toggle())).isChecked()),'Shadow baseline off');
    await action('Focus Shadow',toggle(),'focus');await press('Enable Shadow','Space',{target:toggle(),change:true,image:true});});
  await runCase('C05',async()=>{await openColor('Shadow Color',picker('Series','shadowColorPicker'));
    await action('Shadow rgba',colorText(),'fill','rgba(249, 195, 61, 0.6)',{change:true,image:true});await press('Shadow Enter','Enter',{target:colorText(),image:true});});
  await runCase('C06',()=>number('Blur',12));await runCase('C07',()=>number('X Offset',-7));await runCase('C08',()=>number('Y Offset',9));
  await runCase('C09',async()=>{await action('Focus Shadow retention',toggle(),'focus');await press('Disable Shadow','Space',{target:toggle(),change:true,image:true});
    await press('Restore Shadow','Space',{target:toggle(),change:true,image:true});});
  json('summary',{status:'observed',cases,actions,potentiallyChangingActions:changes,screenshots:shots.length,browserVersion:browser.version(),candidateExecuted:false});
}catch(error){json('failure',{phase,error:clean(error.message),stack:clean(error.stack),completedCases:cases.map(c=>c.id)});
  if(ready&&!page?.isClosed())try{await saveState('failure-state');}catch(e){json('failure-capture',{error:clean(e.message)});}process.exitCode=1;
}finally{
  clearTimeout(timer);cancelled=true;
  let listenerRemoved=!ready;
  if(ready&&!page?.isClosed())try{listenerRemoved=await page.evaluate(()=>{if(window.__color.listener){window.__colorGrid.removeEventListener('chartOptionsChanged',window.__color.listener);window.__color.listener=null;}return window.__color.listener===null;});}catch{}
  json('diagnostics',{records:diagnostics,ownedStatuses:[...statuses].map(([pathStatus,count])=>({pathStatus,count})),overflow});
  try{await context?.close();}finally{await browser?.close();}
  json('browser-cleanup',{browserClosed:!browser?.isConnected(),listenerRemoved,listenerDisposedWithPage:ready&&!!page?.isClosed()&&!listenerRemoved});
  if(browser?.isConnected())process.exitCode=1;json('byte-budget',budget());
}
