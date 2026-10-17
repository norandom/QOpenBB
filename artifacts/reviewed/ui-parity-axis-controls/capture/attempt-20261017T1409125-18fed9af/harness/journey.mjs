import {chromium} from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {root,json,png,limits,check,increment} from './io.mjs';
import {install,acquire} from './projection.mjs';
const runtime=JSON.parse(fs.readFileSync(root+'/runtime-private.json')),credential=JSON.parse(fs.readFileSync(root+'/credential-private.json'));
const fixtures=JSON.parse(fs.readFileSync(new URL('./fixtures.json',import.meta.url)));
const cases=[],ledger=[],menus=[],screenshots=[],diagnostics=[],events=[];
const observations=new Map(),states=new Map();let observationSequence=0;
let browser,context,page,timer,caseTimer,ready=false,phase='entry',fixtureId=null,actions=0,changes=0,checkpoints=0,cached=null,caseStart=0,totalEventCount=0,overflow=null;
const assert=(v,m)=>{if(!v)throw Error(m);};
const clean=v=>{const s=String(v).replaceAll(runtime.origin,'[owned-origin]').replaceAll(credential.email,'[synthetic-account]').replaceAll(credential.password,'[redacted]');
  if(s.length>2048)throw Error('Diagnostic text bound');return s;};
const record=r=>{if(diagnostics.length>=64){overflow='Diagnostic bound';return;}diagnostics.push(r);};
const pause=ms=>new Promise(r=>setTimeout(r,ms));
async function one(l){await l.waitFor({state:'visible',timeout:4000});assert(await l.count()===1,'Unique original control required');return l;}
const axis=role=>page.locator('.ag-chart-docked-container').locator('[data-ref="axisGroup"]').filter({has:page.locator('.ag-charts-format-top-level-group-title').filter({hasText:new RegExp('^'+role+' Axis$')})});
const labels=role=>axis(role).locator('.ag-font-panel');
const combo=(role,ref)=>axis(role).locator('[data-ref="'+ref+'"] [role="combobox"]');
const font=(role,ref)=>labels(role).locator('[data-ref="'+ref+'"] [role="combobox"]');
const toggle=(role,name)=>name==='Ticks'?axis(role).locator('[data-ref="axisTicksGroup"]').getByRole('checkbox',{name,exact:true}):labels(role).getByRole('checkbox',{name,exact:true});
const tickNumber=(role,ref)=>axis(role).locator('[data-ref="'+ref+'"] input[type="number"]:visible');
const padding=role=>labels(role).locator('.ag-slider').filter({has:page.locator('label[data-ref="eLabel"]').filter({hasText:/^Padding$/})}).locator('input[type="number"]:visible');
const rotation=role=>labels(role).locator('.ag-angle-select').filter({has:page.locator('[data-ref="eLabel"]').filter({hasText:/^Rotation °$/})}).locator('[data-ref="eAngleValue"] input[type="number"]:visible');
function saveEvents(values){const files=[];for(let offset=0;offset<values.length;offset+=16){const name='events-p'+String(offset/16).padStart(2,'0');
    json(name,values.slice(offset,offset+16));files.push(name+'.json');}json('event-index',{count:values.length,files,chunkSize:16});}
async function collectEvents(){if(!ready)return;const values=await page.evaluate(()=>window.__axis.events);assert(totalEventCount+values.length<=256,'Run event bound');saveEvents([...events,...values.map(e=>({...e,fixture:fixtureId,sequence:totalEventCount+e.sequence}))]);}
async function step(label,l,method,arg,{change=false,authentication=false}={}){
  assert(!overflow,'Diagnostic overflow');const target=l?await one(l):null;
  actions=increment(actions,limits.actions,'UI interaction');if(change)changes=increment(changes,limits.changes,'Field edit');
  const id=fixtureId+'.'+phase+'.u'+actions;
  if(ready)await page.evaluate(id=>{window.__axis.action=id;window.__axis.actionEvents=0;},id);
  const settledBefore=ready?await checkpoint('before-'+actions):null;
  const before=target?await target.evaluate(n=>({tag:n.tagName,type:n.type,value:n.type==='password'?null:n.value,checked:n.checked??null,controls:n.getAttribute('aria-controls')})):null;
  cached=null;const entry={id,case:phase,label,method,intendedValue:authentication?'[authentication omitted]':arg??null,change,before,beforeEvidence:settledBefore?.observationId??null,completed:false};ledger.push(entry);json('action-ledger',ledger);
  if(target)await target[method](arg);else await page[method](arg);
  entry.completed=true;entry.after=target&&await target.count()===1?await target.evaluate(n=>({tag:n.tagName,type:n.type,value:n.type==='password'?null:n.value,checked:n.checked??null,controls:n.getAttribute('aria-controls')})):null;
  if(authentication){entry.before=null;entry.after=null;}json('action-ledger',ledger);await collectEvents();
  if(ready){const after=await checkpoint('after-'+actions);entry.afterEvidence=after.observationId;json('action-ledger',ledger);}
}
async function checkpoint(label,image=false){
  const deadline=Date.now()+12000;
  await Promise.race([page.evaluate(()=>window.__axisProxy.waitForUpdate()),pause(12000).then(()=>{throw Error('waitForUpdate deadline');})]);
  const times=[];let previous=null,snapshot=null;
  while(Date.now()<deadline){await page.waitForFunction(()=>!window.__axisProxy.chart.ctx.animationManager.isActive(),null,{timeout:Math.max(1,deadline-Date.now()),polling:50});
    snapshot=await page.evaluate(()=>window.__axis.snapshot());const signature=JSON.stringify({live:snapshot.live,geometry:snapshot.geometry});times.push(Date.now());
    if(previous===signature&&times.length>=2)break;previous=signature;await pause(110);
  }
  assert(times.length>=2&&times.at(-1)-times.at(-2)>=100&&Date.now()<=deadline,'Stable geometry deadline');
  snapshot.settled={...snapshot.settled,sampleTimes:times,identicalFiniteSamples:true};snapshot.fixture=fixtureId;snapshot.case=phase;
  const {dom,settled,...chartState}=snapshot;delete chartState.case;
  const signature=createHash('sha256').update(JSON.stringify(chartState)).digest('hex');let name=states.get(signature);
  if(!name){checkpoints=increment(checkpoints,limits.checkpoints,'Checkpoint');name=String(checkpoints).padStart(3,'0')+'-'+fixtureId+'-'+phase+'-'+label;states.set(signature,name);json(name,snapshot);}
  const observationId='o'+(++observationSequence),observation={id:observationId,fixture:fixtureId,case:phase,label,uiSerial:actions,
    checkpoint:name+'.json',chartSha256:signature,dom,settled,eventSequence:snapshot.eventSequence};
  const key=fixtureId+'-'+phase+'-p'+Math.floor(observationSequence/16);if(!observations.has(key))observations.set(key,[]);observations.get(key).push(observation);json('observations-'+key,observations.get(key));
  cached={name,snapshot,uiSerial:actions,observationId};
  if(image){assert(screenshots.length<limits.pngs,'Screenshot count');const imageName=name+'-view'+screenshots.length;
    png(imageName,await page.screenshot());screenshots.push(imageName+'.png');observation.screenshot=imageName+'.png';json('screenshots',screenshots);json('observations-'+key,observations.get(key));}
  await collectEvents();return cached;
}
async function before(label){if(cached&&cached.uiSerial===actions)return cached;return checkpoint(label+'-before');}
async function transaction(label,fn,image=true){const b=await before(label),first=actions+1;await fn();const a=await checkpoint(label+'-after',image);
  transactions.push({fixture:fixtureId,case:phase,label,before:b.name+'.json',after:a.name+'.json',beforeObservation:b.observationId,afterObservation:a.observationId,uiActions:{first,last:actions}});json('transactions',transactions);return a.snapshot;}
const transactions=[];
async function popup(l){const id=await (await one(l)).getAttribute('aria-controls');assert(id&&/^[\w:-]+$/.test(id),'Unique controlled popup ID required');
  const p=page.locator('[id="'+id+'"]');await one(p);return p;}
async function menu(l,selected=null,label='menu'){
  await step(label+' open',l,'click');const p=await popup(l),items=p.locator('[role="option"]:visible');
  const count=await items.count();assert(count>0&&count<=24,'Popup option cap');
  const options=await items.evaluateAll(ns=>ns.map(n=>({text:n.textContent.trim(),role:n.getAttribute('role'),selected:n.getAttribute('aria-selected')})));
  for(const item of options)assert(item.text.length<=512,'Menu string cap');menus.push({fixture:fixtureId,case:phase,label,options});json('menus',menus);
  if(selected!==null){assert(options.filter(o=>o.text===selected).length===1,'Requested menu value absent/ambiguous '+selected);
    await step(label+' choose '+selected,p.getByRole('option',{name:selected,exact:true}),'click',undefined,{change:true});
  }else await step(label+' close',l,'press','Escape');
}
async function select(label,l,value){return transaction(label,()=>menu(l,value,label));}
async function number(label,l,value){return transaction(label,async()=>{await step(label+' fill',l,'fill',String(value),{change:true});await step(label+' commit',l,'press','Tab');});}
async function checked(label,l,value){const t=await one(l);if(await t.isChecked()===value)return;return transaction(label,()=>step(label,l,'setChecked',value,{change:true}));}
async function expand(role){const g=axis(role);assert(await g.count()===1,'Axis group cardinality');const h=g.locator(':scope > .ag-charts-format-top-level-group-title-bar');await one(h);
  const state=await h.getAttribute('aria-expanded');assert(['true','false'].includes(state),'Expansion aria state missing');if(state==='false')await step('Expand '+role,h,'click');}
async function inventory(role,typography=false){
  await expand(role);for(const [ref,label] of [['axisTypeSelect','Axis Type'],['axisPositionSelect','Position']]){
    const l=combo(role,ref);if(await l.count()&&await l.isVisible())await menu(l,null,role+' '+label);
  }
  if(typography){await menu(font(role,'familySelect'),null,role+' Font');await menu(font(role,'sizeSelect'),null,role+' Size');}
  await checkpoint(role+'-inventory',true);
}
async function tickCase(role,width,length){await expand(role);const t=toggle(role,'Ticks');const initial=await (await one(t)).isChecked();
  await checked(role+'-ticks-on',t,true);const w=tickNumber(role,'axisTicksWidthSlider'),s=tickNumber(role,'axisTicksSizeSlider');
  const oldW=await (await one(w)).inputValue(),oldS=await (await one(s)).inputValue();
  await number(role+'-tick-width',w,width);await number(role+'-tick-length',s,length);await checked(role+'-ticks-off',t,false);await checked(role+'-ticks-retained',t,true);
  await number(role+'-tick-width-restore',w,oldW);await number(role+'-tick-length-restore',s,oldS);await checked(role+'-ticks-baseline',t,initial);
}
async function labelCase(role,family,size,spacing,angles){
  await inventory(role,true);const f=font(role,'familySelect'),s=font(role,'sizeSelect'),p=padding(role),a=toggle(role,'Auto Rotate');
  const old={family:(await f.textContent()).trim(),size:(await s.textContent()).trim(),spacing:await (await one(p)).inputValue(),auto:await (await one(a)).isChecked()};
  await select(role+'-font',f,family);await select(role+'-size',s,String(size));await number(role+'-spacing',p,spacing);
  await checked(role+'-manual',a,false);const r=rotation(role),oldRotation=await (await one(r)).inputValue();
  for(const angle of angles)await number(role+'-rotation-'+angle,r,angle);
  await checked(role+'-automatic',a,true);await checked(role+'-manual-retained',a,false);
  await select(role+'-font-restore',f,old.family);await select(role+'-size-restore',s,old.size);await number(role+'-spacing-restore',p,old.spacing);
  await number(role+'-rotation-restore',r,oldRotation);await checked(role+'-auto-restore',a,old.auto);
}
async function runCase(id,seconds,fn){phase=id;caseStart=Date.now();await page.evaluate(()=>{window.__axis.caseEvents=0;});
  caseTimer=setTimeout(()=>page.close().catch(()=>{}),seconds*1000);try{await fn();cases.push({id,fixture:fixtureId,status:'observed',elapsedMs:Date.now()-caseStart});json('cases',cases);}finally{clearTimeout(caseTimer);}}
async function closeContext(){if(ready&&!page.isClosed()){
    const e=await page.evaluate(()=>{const p=window.__axis;window.__axisGrid.removeEventListener('chartOptionsChanged',p.listener);p.listener=null;return p.events;});
    events.push(...e.map(v=>({...v,fixture:fixtureId,sequence:totalEventCount+v.sequence})));totalEventCount+=e.length;
  }ready=false;cached=null;await context?.close();saveEvents(events);}
async function entry(id){
  fixtureId=id;phase='entry';cached=null;context=await browser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1});page=await context.newPage();
  page.setDefaultTimeout(4000);page.setDefaultNavigationTimeout(20000);const cdp=await context.newCDPSession(page);await cdp.send('Runtime.enable');await cdp.send('Network.enable');
  page.on('console',m=>{if(['error','warning'].includes(m.type()))record({fixture:id,kind:'console',type:m.type(),text:clean(m.text())});});
  page.on('pageerror',e=>record({fixture:id,kind:'pageerror',text:clean(e.message)}));
  cdp.on('Runtime.exceptionThrown',e=>record({fixture:id,kind:'cdp-exception',text:clean(e.exceptionDetails.text)}));
  cdp.on('Network.loadingFailed',e=>record({fixture:id,kind:'cdp-loading-failed',text:clean(e.errorText),type:e.type,canceled:e.canceled}));
  await page.route('**/*',route=>new URL(route.request().url()).origin===runtime.origin?route.continue():route.abort());
  await page.route('**/api/pro/dash/{sync,validate-and-sync}',async route=>{if(route.request().method()!=='GET')return route.continue();
    const response=await route.fetch(),actual=await response.json(),dashboard=JSON.parse(fs.readFileSync(new URL('./dashboard.json',import.meta.url),'utf8').replaceAll('http://127.0.0.1:32773',runtime.origin));
    dashboard['11111111-1111-4111-8111-111111111111'].data.widgets[0].data.table.columnsDefs[0].cellDataType=fixtures[id].cellDataType;
    return route.fulfill({json:{...actual,owned:Object.fromEntries(Object.entries(dashboard).map(([key,content])=>[key,{content,is_shared:false,created_by:'Synthetic Parity',created_date:'2026-10-17T00:00:00Z',updated_date:'2026-10-17T00:00:00Z'}])),shared:{},entity_shared:{}}});});
  await page.route('**/synthetic_financials',route=>route.fulfill({json:fixtures[id].periods.map((period,i)=>({period,revenue:fixtures.revenue[i],operatingIncome:fixtures.operatingIncome[i]}))}));
  await step('Login navigation',null,'goto',runtime.origin);await step('Email',page.getByLabel('Email',{exact:true}),'fill',credential.email,{authentication:true,change:true});
  await step('Password',page.getByLabel('Password',{exact:true}),'fill',credential.password,{authentication:true,change:true});await step('Login',page.getByRole('button',{name:'Login',exact:true}),'click');
  await page.waitForURL(u=>!['/','/login'].includes(u.pathname),{timeout:20000});
  if(new URL(page.url()).pathname==='/onboarding'){
    await step('First name',page.getByLabel('First Name',{exact:true}),'fill','Synthetic',{change:true});await step('Last name',page.getByLabel('Last Name',{exact:true}),'fill','Axis Controls',{change:true});
    const updated=page.waitForResponse(r=>new URL(r.url()).pathname==='/api/user'&&r.request().method()==='PUT',{timeout:4000});
    await step('Continue',page.getByRole('button',{name:'Continue',exact:true}),'click');assert((await updated).status()===200,'Successful profile PUT required');
    await page.waitForFunction(()=>location.pathname.startsWith('/app')||[...document.querySelectorAll('button')].some(b=>b.textContent.trim()==='Continue'&&!b.disabled),null,{timeout:4000});
    json('onboarding-'+id,{profilePutStatus:200,appNavigationOrContinueEnabled:true});
  }
  await step('Synthetic dashboard',null,'goto',runtime.origin+'/app/11111111-1111-4111-8111-111111111111');
  for(const value of ['100','140','160'])await page.getByText(value,{exact:true}).first().waitFor({state:'visible',timeout:4000});
  await step('Chart entry',page.locator('#chart-view-button'),'click');await page.locator('.ag-charts-canvas canvas').first().waitFor({state:'visible',timeout:4000});
  await page.evaluate(install);const identity=await page.evaluate(acquire);assert(identity.chartType.value==='groupedColumn','Original groupedColumn required');
  assert(identity.cellRange.columns.value?.join()==='period,revenue,operatingIncome','Exact three financial keys required');
  assert(identity.cellRange.rowStartIndex.value===0&&identity.cellRange.rowEndIndex.value===3,'Four-row chart range required');
  assert(await page.evaluate(()=>document.documentElement.classList.contains('dark')),'Original dark theme required');ready=true;json('identity-'+id,identity);
  await step('Widget menu',page.locator('button').filter({has:page.locator('svg#list-unordered')}),'click');
  await step('Chart settings',page.getByRole('menuitem',{name:'Chart settings',exact:true}),'click');await step('Customize',page.getByRole('tab',{name:'Customize',exact:true}),'click');
}
try{
  const env={...process.env};delete env.WAYLAND_DISPLAY;
  browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
  timer=setTimeout(()=>page?.close().catch(()=>{}),900000);
  await entry('A');
  await runCase('A01',60,async()=>{await inventory('Horizontal');await inventory('Vertical');});
  await runCase('A02',60,async()=>{for(const [r,values] of [['Horizontal',['Top','Bottom']],['Vertical',['Right','Left']]])for(const v of values)await select(r+'-position-'+v,combo(r,'axisPositionSelect'),v);});
  await runCase('A03',90,()=>tickCase('Horizontal',3,11));await runCase('A04',90,()=>tickCase('Vertical',2,7));
  await runCase('A05',120,()=>labelCase('Horizontal','Arial, sans-serif',14,17,[315,45]));
  await runCase('A06',120,()=>labelCase('Vertical','Courier New, monospace',16,23,[330]));await closeContext();
  await entry('B');await runCase('A07',90,async()=>{await inventory('Horizontal');await inventory('Vertical');await number('B-spacing',padding('Horizontal'),19);
    await checked('B-ticks-on',toggle('Horizontal','Ticks'),true);await number('B-tick-width',tickNumber('Horizontal','axisTicksWidthSlider'),3);
    await select('B-number',combo('Horizontal','axisTypeSelect'),'Number');await select('B-time',combo('Horizontal','axisTypeSelect'),'Time');});
  await runCase('A08',90,async()=>{await menu(combo('Horizontal','axisTimeFormatSelect'),null,'Time Format');await checkpoint('Time-format-inventory');
    await select('B-ISO',combo('Horizontal','axisTimeFormatSelect'),'YYYY-MM-DD');await select('B-European',combo('Horizontal','axisTimeFormatSelect'),'DD/MM/YYYY');
    await select('B-category',combo('Horizontal','axisTypeSelect'),'Category');});await closeContext();
  await entry('C');await runCase('A09',60,async()=>{await inventory('Horizontal');await inventory('Vertical');});await closeContext();
  json('summary',{status:'observed',cases,actions,changes,checkpoints,screenshots:screenshots.length,events:totalEventCount,browserVersion:browser.version(),candidateExecuted:false,retained:check()});
}catch(error){json('failure',{fixture:fixtureId,case:phase,error:clean(error.message),completedCases:cases.map(c=>c.id),actions,changes,checkpoints,overflow});process.exitCode=1;
}finally{
  clearTimeout(timer);clearTimeout(caseTimer);let closeError=null;
  try{await closeContext();}catch(e){closeError=clean(e.message);await context?.close();}
  await browser?.close();json('diagnostics',{records:diagnostics,overflow});json('browser-cleanup',{browserClosed:!browser?.isConnected(),contextClosed:!page||page.isClosed(),listenerRemovedOrDisposed:!page||page.isClosed(),closeError});
  json('counters',{actions,changes,checkpoints,screenshots:screenshots.length,events:totalEventCount});json('retained-bytes',check());
}
