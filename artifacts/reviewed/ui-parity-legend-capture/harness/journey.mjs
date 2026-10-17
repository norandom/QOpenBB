import {chromium} from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {root,json,png,check,reconcile,increment} from './io.mjs';
import {limits,rows} from './limits.mjs';
import {createEventStore} from './events.mjs';
import {install,acquire} from './projection.mjs';
import {geometryTools} from './geometry.mjs';
import {settle} from './settlement.mjs';
import {controlTools} from './controls.mjs';
import {assertFixture,arranged} from './guards.mjs';
import {executeCases} from './cases.mjs';
const runtime=JSON.parse(fs.readFileSync(root+'/runtime-private.json')),credential=JSON.parse(fs.readFileSync(root+'/credential-private.json'));
const cases=[],ledger=[],menus=[],raster=[],diagnostics=[],records=[],caseIds=Array.from({length:8},(_,i)=>'L0'+(i+1));
const eventStore=createEventStore(json),pictures=new Map(),geometry=geometryTools();
let browser,context,page,ready=false,phase='admission',actions=0,admission=0,changes=0,observations=0,baseline=null,fixedPlot=null,fixedLegend=null,caseDeadline=Infinity,journeyDeadline=Infinity,caseTimer,journeyTimer;
const counts={console:0,pageerror:0,network:0,externalDenied:0,cdp:0};
const clean=value=>String(value).replaceAll(runtime.origin,'[owned-origin]').replaceAll(credential.email,'[synthetic-account]').replaceAll(credential.password,'[redacted]').slice(0,512);
const record=(kind,value)=>{if(records.length>=256)throw Error('record-bound');records.push({case:phase,kind,...value});json('case-records',records);};
function diagnostic(kind,value){counts[kind]=(counts[kind]??0)+1;if(diagnostics.length<20)diagnostics.push({kind,...value});}
const assert=(condition,message)=>{if(!condition)throw Error(message);};
function guardTime(){if(Date.now()>=caseDeadline)throw Error('not-run-budget: case deadline');if(Date.now()>=journeyDeadline)throw Error('not-run-budget: journey deadline');}
async function collectEvents(){if(ready&&!page.isClosed()){const events=await page.evaluate(()=>window.__legend.events);eventStore.save(events);}}
function counters(){json('counters',{phase,admission,actions,changes,observations,pngs:raster.length,events:eventStore.count(),remainingMs:Math.max(0,journeyDeadline-Date.now()),retained:check()});}
function saveActions(){
  const files=[];for(let i=0;i<ledger.length;i+=16)files.push('actions-p'+String(i/16).padStart(2,'0')+'.json');
  if(ledger.length){const offset=Math.floor((ledger.length-1)/16)*16;json(files.at(-1).slice(0,-5),ledger.slice(offset));}
  json('action-index',{count:ledger.length,files,chunkSize:16});
}
async function screenshot(state){
  const snapshot=state.snapshot,scene=snapshot.live.scene;
  const signature=createHash('sha256').update(JSON.stringify({live:snapshot.live,geometry:snapshot.geometry})).digest('hex');
  if(pictures.has(signature)){state.raster=pictures.get(signature);return;}
  const canvas=geometry.box(snapshot.geometry.canvas.css),plot=geometry.box(snapshot.geometry.seriesRect),boxes=snapshot.canvasGeometry;
  const identity=scene.items.map(i=>({id:i.series.identity.id.value,yKey:i.series.properties.yKey.value}));
  const clip=box=>{const x=Math.max(canvas.x,canvas.x+box.x),y=Math.max(canvas.y,canvas.y+box.y),right=Math.min(canvas.x+canvas.width,canvas.x+box.x+box.width),bottom=Math.min(canvas.y+canvas.height,canvas.y+box.y+box.height);
    assert(right>x&&bottom>y,'raster-unresolved: empty crop');return {x,y,width:right-x,height:bottom-y};};
  fixedPlot??=plot;fixedLegend??=boxes.legend;
  const legend=boxes.legend.width>0&&boxes.legend.height>0?boxes.legend:fixedLegend;
  const regions=[['plot',fixedPlot],['legend',legend]];
  const receipt={signature,observation:state.id,series:identity,seriesRect:plot,crops:[]};
  for(const [role,box] of regions){assert(raster.length<limits.pngs,'PNG count cap');const name='raster-'+String(raster.length+1).padStart(3,'0')+'-'+role;
    const region=clip(box);png(name,await page.screenshot({clip:region,timeout:4000}));raster.push({path:name+'.png',role,observation:state.id,clip:region,series:identity});receipt.crops.push(raster.at(-1));}
  pictures.set(signature,receipt);state.raster=receipt;json('raster-index',raster);
}
async function checkpoint(label,image=false){
  guardTime();assert(observations<limits.observations,'observation cap');
  let result;
  try{result=await settle({waitForUpdate:()=>page.evaluate(()=>window.__legendProxy.waitForUpdate()),sample:()=>page.evaluate(()=>window.__legend.snapshot()),deadlineMs:Math.min(limits.settlement,caseDeadline-Date.now(),journeyDeadline-Date.now())});}
  catch(error){if(error.diagnostic)json('settlement-failure',{case:phase,label,...error.diagnostic});throw error;}
  const snapshot=result.snapshot;assertFixture(snapshot,baseline);snapshot.canvasGeometry=geometry.convert(snapshot.live.scene);
  snapshot.canvasGeometry.gap=geometry.gap(snapshot.canvasGeometry.legend,geometry.box(snapshot.geometry.seriesRect),snapshot.effective.position.value);
  const id='o'+String(++observations).padStart(3,'0'),state={id,case:phase,label,actions,eventSequence:snapshot.eventSequence,snapshot,settled:result.settled};
  if(image)await screenshot(state);json('observation-'+id,state);await collectEvents();return state;
}
const targetState=async target=>target&&await target.count()===1?target.evaluate(n=>({tag:n.tagName,type:n.type??null,value:n.type==='password'?null:n.value??null,checked:n.checked??null,text:n.type==='password'?null:n.textContent?.trim().slice(0,512),controls:n.getAttribute('aria-controls')})):null;
async function step(label,target,method,arg,{authentication=false,potentialMutation=false,raster:wantRaster=false}={}){
  guardTime();if(ready){assert(changes<limits.changes,'field mutation cap');actions=increment(actions,limits.actions,'chart action');}else admission=increment(admission,limits.admission,'admission action');
  const id=(ready?'c':'a')+(ready?actions:admission),before=ready?await checkpoint(label+' before'):null;
  const entry={id,case:phase,label,method,arg:authentication?'[omitted]':arg??null,completed:false,before:authentication?null:await targetState(target),beforeObservation:before?.id??null,eventFirst:eventStore.count()+1};
  if(before&&(wantRaster||potentialMutation)){await screenshot(before);json('observation-'+before.id,before);}
  ledger.push(entry);saveActions();if(ready)await page.evaluate(id=>{window.__legend.action=id;window.__legend.actionEvents=0;},id);
  try{if(target)await target[method](arg);else await page[method](arg);entry.completed=true;entry.after=authentication?null:await targetState(target);
    if(ready){const after=await checkpoint(label+' after');entry.afterObservation=after.id;
      const changed=JSON.stringify(before.snapshot.model.chartOptions)!==JSON.stringify(after.snapshot.model.chartOptions);entry.actualFieldMutation=changed;
      if(changed){changes=increment(changes,limits.changes,'field mutation');if(!potentialMutation)entry.unexpectedMutation=true;}
      if(wantRaster||changed){assert(before.raster,'raster-unresolved: missing prospective before capture');await screenshot(after);json('observation-'+after.id,after);entry.raster={before:before.raster,after:after.raster};}
    }
  }catch(error){entry.error=clean(error.message);throw error;}
  finally{try{await collectEvents();}finally{entry.eventLast=eventStore.count();saveActions();counters();}}
}
let controls;
async function menu(name,selection){
  const combo=await controls.combo(name);await step(name+' open',combo,'click');
  const id=await combo.getAttribute('aria-controls');assert(id&&/^[\w:-]+$/.test(id),'selector-unresolved: popup ownership');
  const popup=page.locator('[id="'+id+'"]');await controls.one(popup);
  const options=popup.getByRole('option'),count=await options.count();assert(count>0&&count<=limits.options,'selector-unresolved: options cap');
  const values=await options.evaluateAll(ns=>ns.map(n=>({name:n.textContent.trim(),role:n.getAttribute('role'),selected:n.getAttribute('aria-selected')})));
  assert(values.every(v=>v.name.length<=512),'option string cap');
  if(!menus.some(m=>m.name===name)){assert(['Font','Size','Position'].includes(name)&&menus.length<3,'menu inventory bound');menus.push({name,options:values});json('menus',menus);}
  if(selection===null){await step(name+' Escape',combo,'press','Escape');return;}
  assert(values.filter(v=>v.name===selection).length===1,'selector-unresolved: option '+selection);
  await step(name+' choose '+selection,popup.getByRole('option',{name:selection,exact:true}),'click',undefined,{potentialMutation:true,raster:true});
  assert((await (await controls.combo(name)).textContent()).trim()===selection,'control-value-unresolved: '+name);
}
async function number(label,value,name=label){const target=await controls.numeric(name);const n=Number(value),min=Number(await target.getAttribute('min')),max=Number(await target.getAttribute('max'));
  assert(Number.isInteger(n)&&n>=min&&n<=max,'control-domain-unresolved: '+name);await step(label+' fill',target,'fill',String(value),{potentialMutation:true,raster:true});await step(label+' Tab',await controls.numeric(name),'press','Tab',{potentialMutation:true,raster:true});
  assert(Number(await (await controls.numeric(name)).inputValue())===n,'control-value-unresolved: '+name);}
async function runCase(id,fn){phase=id;caseDeadline=Math.min(Date.now()+limits.case,journeyDeadline);const started=Date.now();await page.evaluate(()=>{window.__legend.caseEvents=0;});
  caseTimer=setTimeout(()=>page.close().catch(()=>{}),Math.max(1,caseDeadline-Date.now()));const item={id,status:'running',startedAt:started};cases.push(item);json('case-'+id,item);
  try{await checkpoint(id+' start');await fn();await checkpoint(id+' boundary');item.status='observed';}
  catch(error){item.status=error.message.startsWith('not-run-budget')?'not-run-budget':error.message.split(':')[0];item.reason=clean(error.message);throw error;}
  finally{clearTimeout(caseTimer);item.elapsedMs=Date.now()-started;json('case-'+id,item);if(['L01','L04','L08'].includes(id))counters();}}
async function admissionJourney(){
  await page.route('**/*',route=>{const url=new URL(route.request().url());if(url.origin===runtime.origin)return route.continue();diagnostic('externalDenied',{scheme:url.protocol});return route.abort();});
  await page.route('**/api/pro/dash/{sync,validate-and-sync}',async route=>{if(route.request().method()!=='GET')return route.continue();const response=await route.fetch(),actual=await response.json();
    const fixture=JSON.parse(fs.readFileSync(new URL('./fixture.json',import.meta.url),'utf8').replaceAll('http://127.0.0.1:32773',runtime.origin));
    return route.fulfill({json:{...actual,owned:Object.fromEntries(Object.entries(fixture).map(([key,content])=>[key,{content,is_shared:false,created_by:'Synthetic Parity',created_date:'2026-10-17T00:00:00Z',updated_date:'2026-10-17T00:00:00Z'}])),shared:{},entity_shared:{}}});});
  await page.route('**/synthetic_financials',route=>route.fulfill({json:rows}));
  await step('Login navigation',null,'goto',runtime.origin);await step('Email',page.getByLabel('Email',{exact:true}),'fill',credential.email,{authentication:true});
  await step('Password',page.getByLabel('Password',{exact:true}),'fill',credential.password,{authentication:true});await step('Login',page.getByRole('button',{name:'Login',exact:true}),'click');
  await page.waitForURL(u=>!['/','/login'].includes(u.pathname),{timeout:4000});
  if(new URL(page.url()).pathname==='/onboarding'){
    await step('First name',page.getByLabel('First Name',{exact:true}),'fill','Synthetic');await step('Last name',page.getByLabel('Last Name',{exact:true}),'fill','Legend Controls');
    const updated=page.waitForResponse(r=>new URL(r.url()).pathname==='/api/user'&&r.request().method()==='PUT',{timeout:4000});await step('Continue',page.getByRole('button',{name:'Continue',exact:true}),'click');assert((await updated).status()===200,'admission-unresolved: profile');
  }
  await step('Synthetic dashboard',null,'goto',runtime.origin+'/app/11111111-1111-4111-8111-111111111111');
  await page.getByText('160',{exact:true}).first().waitFor({state:'visible',timeout:4000});await step('Chart entry',page.locator('#chart-view-button'),'click');
  await page.locator('.ag-charts-canvas canvas').waitFor({state:'visible',timeout:4000});await page.evaluate(install);
  let identity;try{identity=await page.evaluate(acquire);}finally{json('acquisition-stages',await page.evaluate(()=>window.__legend?.receipts??[]));}
  assert(await page.evaluate(()=>document.documentElement.classList.contains('dark')),'admission-unresolved: dark');
  assert(identity.model.chartType.value==='groupedColumn','admission-unresolved: groupedColumn');
  ready=true;phase='admission-controls';await step('Widget menu',page.locator('button').filter({has:page.locator('svg#list-unordered')}),'click');
  await step('Chart settings',page.getByRole('menuitem',{name:'Chart settings',exact:true}),'click');
  const editor=page.locator('.ag-chart-docked-container');await controls.one(editor);await step('Customize',editor.getByRole('tab',{name:'Customize',exact:true}),'click');
  await controls.inventory();const b=await checkpoint('admission-baseline',true);baseline=b.snapshot;
  assert(baseline.effective.position.value==='top'&&baseline.effective.enabled.value===true,'baseline-unresolved: Legend enabled top');
  json('identity-fixture',{identity,rows,columns:['period','revenue','operatingIncome'],units:'USD millions',viewport:{width:1440,height:1000,dpr:1},image:runtime.image,source:runtime.source,baseline:b.id});counters();
}
try{
  const env={...process.env};delete env.WAYLAND_DISPLAY;
  browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
  context=await browser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1});page=await context.newPage();page.setDefaultTimeout(4000);page.setDefaultNavigationTimeout(4000);controls=controlTools(page,step);
  const cdp=await context.newCDPSession(page);await cdp.send('Runtime.enable');await cdp.send('Network.enable');
  page.on('console',m=>{if(['error','warning'].includes(m.type()))diagnostic('console',{type:m.type()});});page.on('pageerror',()=>diagnostic('pageerror',{}));
  page.on('response',r=>{if(r.status()>=400){const u=new URL(r.url());if(u.origin===runtime.origin)diagnostic('network',{path:clean(u.pathname),status:r.status()});}});
  cdp.on('Runtime.exceptionThrown',()=>diagnostic('cdp',{exception:true}));cdp.on('Network.loadingFailed',e=>diagnostic('cdp',{loadingFailed:true,canceled:e.canceled??false}));
  const admissionTimer=setTimeout(()=>page.close().catch(()=>{}),Math.max(1,runtime.startedAt+limits.startup-Date.now()));
  try{await admissionJourney();}finally{clearTimeout(admissionTimer);}
  phase='L01';journeyDeadline=Math.min(Date.now()+limits.journey,runtime.startedAt+limits.inputStop);journeyTimer=setTimeout(()=>page.close().catch(()=>{}),Math.max(1,journeyDeadline-Date.now()));
  await executeCases({controls,step,menu,number,checkpoint,runCase,record,arranged});json('summary',{status:'observed',candidateExecuted:false,cases,actions,changes,observations});
}catch(error){json('failure',{case:phase,reason:clean(error.message),actions,changes,observations});process.exitCode=1;
}finally{
  clearTimeout(caseTimer);clearTimeout(journeyTimer);let closeError=null;
  try{await collectEvents();if(ready&&!page.isClosed())await page.evaluate(()=>window.__legendGrid.removeEventListener('chartOptionsChanged',window.__legend.listener));}catch(e){closeError=clean(e.message);}
  ready=false;await context?.close().catch(e=>{closeError??=clean(e.message);});await browser?.close().catch(e=>{closeError??=clean(e.message);});
  for(const id of caseIds)if(!cases.some(c=>c.id===id))json('case-'+id,{id,status:'not-run-budget',dependency:phase});
  json('diagnostics',{counts,records:diagnostics});json('browser-cleanup',{browserClosed:!browser?.isConnected(),contextClosed:!page||page.isClosed(),listenerRemovedOrDisposed:!page||page.isClosed(),closeError});counters();reconcile();
}
