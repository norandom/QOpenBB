import {chromium} from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
import {root,json,png,budget} from './io.mjs';
import {fixture,fixtureHash,cases,limits,source,image} from './contract.mjs';
import {install,acquire,attach,admission,dom} from './projection.mjs';
import {settle,observe,coordinate} from './collector.mjs';
import {controls} from './controls.mjs';
import {failureMetadata} from './failure-metadata.mjs';
import {sample,modeSample,settlement,invocation,entry as boundedEntry,reserveInput,finalTail,controlReceipt} from './keyboard-retention.mjs';
const runtime=JSON.parse(fs.readFileSync(root+'/runtime-private.json'));
const credential=JSON.parse(fs.readFileSync(root+'/credential-private.json'));
const f=fixture(),launch=Date.now(),lifecycle=JSON.parse(fs.readFileSync(root+'/lifecycle-private.json'));
let browser,browserServer,context,page,phase='setup',current=null,actions=0,setupActions=0,probes=0,shots=0,admittedAt=null,ready=false,timer,contextClosed=false;
const ledger=[],results=[],diagnostics={consoleErrors:0,pageErrors:0,cdpExceptions:0,blockedOrigins:0,responseFailures:0,failures:[]};
const preflight={source,image,fixtureHash,status:'setup-pending',setup:{actionCount:0,entries:[]}};
function persist(){if(current)json(current.id,current);else{preflight.setup={actionCount:setupActions,entries:ledger.filter(e=>e.id.startsWith('setup.')).map(({id,status})=>({id,status}))};json('identity-fixture-preflight',preflight);}}
const assert=(c,m)=>{if(!c)throw Error(m);};
function guard(){const now=Date.now();if(now-lifecycle.launchedAt>=limits.inputStopMs)throw Error('Outer input stop');
  if(admittedAt&&now-admittedAt>limits.casesMs)throw Error('Case lifecycle bound');
  if(!admittedAt&&now-lifecycle.launchedAt>limits.startupMs)throw Error('Startup bound');
  if(current&&(now-current.began>current.timeCap||current.actions>=current.actionCap||Buffer.byteLength(JSON.stringify(current))>limits.caseBytes-16000))throw Error('not-run-budget');}
async function input(label,target,method,arg){guard();if(current?.id==='T06')reserveInput(current);if(actions>=limits.totalActions||phase==='setup'&&setupActions>=limits.setupActions)throw Error('Action bound');
  const id=phase+'.a'+String((current?.actions??setupActions)+1).padStart(3,'0');actions++;if(current)current.actions++;else setupActions++;
  const started=Date.now(),entry={id,label,method,argument:phase==='setup'?null:arg??null,elapsedMs:0,status:'started'};ledger.push(entry);
  if(current)current.ledger.push(entry);persist();
  if(ready){entry.eventsFrom=await page.evaluate(id=>{window.__tooltip.action=id;return window.__tooltip.events.length;},id);}
  try{if(method==='goto')await page.goto(arg,{waitUntil:'domcontentloaded'});else if(method==='move')await page.mouse.move(arg.x,arg.y);
    else if(method==='key')await page.keyboard.press(arg);else await target[method](...(arg===undefined?[]:[arg]));
    entry.status='observed';if(ready){const observed=await page.evaluate(dom);entry.after=current?.id==='T06'?sample(observed):{active:observed.active,tooltip:observed.tooltip?{visible:observed.tooltip.visible,heading:observed.tooltip.heading,rows:observed.tooltip.rows}:null,liveStatus:observed.liveStatus};entry.eventsTo=await page.evaluate(()=>window.__tooltip.events.length);}else entry.after={setup:true};
  }catch(e){entry.status='failed';entry.reason=String(e.message).split('\n')[0].replaceAll(credential.email,'[redacted]').replaceAll(credential.password,'[redacted]');throw e;}
  finally{entry.elapsedMs=Date.now()-started;if(current?.id==='T06')boundedEntry(entry);persist();}}
const ui=()=>controls(page,input,receipt=>{if(!current)throw Error('Case receipt required');
  if(current.id==='T06')controlReceipt(receipt);(current.controlReceipts??=[]).push(receipt);persist();});
async function screenshot(name){if(shots>=limits.screenshots)throw Error('Screenshot bound');const bytes=await page.screenshot();png(name,bytes);shots++;return name+'.png';}
async function probe(ordinal,key,fallback){
  guard();if(probes>=limits.probes)throw Error('Probe bound');probes++;
  const record={id:current.id+'.p'+probes,ordinal,key,status:'started'};current.probes.push(record);
  try{const settled=await settle(page,{ordinal,key},guard);record.settlement=settled;
    try{record.target=coordinate(settled.pair[1],ordinal,key,current.family);}catch(e){
      if(fallback&&String(e.message).startsWith('no-hittable-node')){record.fallbackReason=e.message;record.target=coordinate(settled.pair[1],ordinal,fallback,current.family);}else throw e;}
    await input('Hover '+ordinal+' '+record.target.yKey,null,'move',record.target.point);record.observation=await observe(page,guard);
    record.status=record.observation.status;if(record.status!=='stable')throw Error(record.status);record.image=await screenshot(record.id);
    record.ownerConclusion=ordinal===4?'owner-unresolved: tied values do not alone identify actual picked series':'rendered content retained separately from intended target';
    await input('Leave canvas',null,'move',{x:settled.pair[1].canvas.x-8,y:settled.pair[1].canvas.y-8});record.leave=await observe(page,guard);if(record.leave.status!=='stable')throw Error(record.leave.status);
  }catch(e){record.status=String(e.message).split(':')[0];record.reason=String(e.message).split('\n')[0];throw e;}}
async function keyboard(){for(const mode of current.modes){guard();await ui().mode(mode);await input('Escape popup',null,'key','Escape');await ui().close();
  const k={mode,status:'seeking',tabs:[],keys:[]};current.keyboard.push(k);let reached=false;
  const beforeSample=async()=>modeSample(k,await page.evaluate(dom));
  const observed=async()=>settlement(await observe(page,guard,raw=>modeSample(k,raw)));
  const reserveProbe=()=>{guard();if(probes>=limits.probes)throw Error('not-run-budget');reserveInput(current);};
  for(let i=0;i<current.tabCap;i++){const before=await beforeSample();reserveProbe();probes++;
    await input('Tab traversal',null,'key','Tab');const state=await observed();k.tabs.push(invocation({before,state}));
    if(state.status!=='stable'){k.terminalImage=await screenshot(current.id+'-'+mode+'-terminal');throw Error(state.status);}
    if(state.pair.at(-1)?.active?.inSeriesArea){reached=true;break;}}
  k.status=reached?'reached':'keyboard-unreachable-within-bound';k.initialOrTerminalImage=await screenshot(current.id+'-'+mode+'-'+(reached?'initial':'terminal'));
  let previousImage=k.initialOrTerminalImage;
  if(reached)for(const key of current.sequence){const before=await beforeSample(),beforeImage=previousImage;reserveProbe();probes++;
    await input('Keyboard '+key,null,'key',key);const after=await observed();
    const afterImage=await screenshot(current.id+'-'+mode+'-key'+(k.keys.length+1));k.keys.push(invocation({key,before,after,beforeImage,afterImage,beforeImageReuse:'Immediately preceding screenshot; no intervening input'}));
    previousImage=afterImage;if(after.status!=='stable')throw Error(after.status);}
}}
function dashboard(){const widget={id:'synthetic_financials',widgetId:'synthetic_financials',name:'Synthetic Financials',type:'table',widgetType:'single',connectionType:'single',external:true,
  storage:f.widgetInput.storage,endpoint:{url:runtime.origin+'/synthetic_financials',method:'GET'},gridData:{i:'synthetic_financials',x:0,y:0,w:30,h:12},
  data:{table:{enableCharts:true,columnsDefs:f.columns}}};
  return {'00000000-0000-4000-8000-000000000000':{name:'root',isRoot:true,isFolder:true,children:['11111111-1111-4111-8111-111111111111'],index:'00000000-0000-4000-8000-000000000000'},
    '11111111-1111-4111-8111-111111111111':{name:'Synthetic Financials',parentId:'00000000-0000-4000-8000-000000000000',index:'11111111-1111-4111-8111-111111111111',
      data:{name:'Synthetic Financials',type:'custom',currentTab:'',widgets:[widget],gridLayout:{'':[widget.gridData]},groups:[]}}};}
try{
  assert(runtime.source===source&&runtime.image===image,'Runtime identity mismatch');
  browserServer=await chromium.launchServer({headless:true,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
  const browserPid=browserServer.process().pid,browserStartTicks=fs.readFileSync('/proc/'+browserPid+'/stat','utf8').split(' ')[21];
  fs.writeFileSync(root+'/owned-browser-private.json',JSON.stringify({pid:browserPid,startTicks:browserStartTicks}),{mode:0o600});
  browser=await chromium.connect(browserServer.wsEndpoint());
  context=await browser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1});page=await context.newPage();page.setDefaultTimeout(limits.selectorMs);page.setDefaultNavigationTimeout(20000);
  context.on('close',()=>{contextClosed=true;});
  timer=setTimeout(()=>page.close().catch(()=>{}),Math.max(1,limits.inputStopMs-(Date.now()-lifecycle.launchedAt)));
  const cdp=await context.newCDPSession(page);await cdp.send('Runtime.enable');await cdp.send('Network.enable');
  cdp.on('Runtime.exceptionThrown',()=>diagnostics.cdpExceptions++);page.on('pageerror',()=>diagnostics.pageErrors++);
  page.on('console',m=>{if(m.type()==='error')diagnostics.consoleErrors++;});
  page.on('response',r=>{const u=new URL(r.url());if(r.status()>=400){diagnostics.responseFailures++;
    if(u.origin===runtime.origin&&!/auth|login|user|token|session/i.test(u.pathname)&&diagnostics.failures.length<20)diagnostics.failures.push({path:u.pathname,status:r.status()});}});
  await page.route('**/*',r=>{if(new URL(r.request().url()).origin!==runtime.origin){diagnostics.blockedOrigins++;return r.abort();}return r.continue();});
  await page.route('**/api/pro/dash/{sync,validate-and-sync}',async r=>{if(r.request().method()!=='GET')return r.continue();const upstream=await r.fetch(),actual=await upstream.json();
    return r.fulfill({json:{...actual,owned:Object.fromEntries(Object.entries(dashboard()).map(([id,content])=>[id,{content,is_shared:false,created_by:'Synthetic Parity',created_date:'2026-10-17T00:00:00Z',updated_date:'2026-10-17T00:00:00Z'}])),shared:{},entity_shared:{}}});});
  let delivered=0;await page.route('**/synthetic_financials',r=>{delivered++;return r.fulfill({json:f.rows});});
  await input('Login navigation',null,'goto',runtime.origin);await input('Email',await ui().one(page.getByLabel('Email',{exact:true})),'fill',credential.email);
  await input('Password',await ui().one(page.getByLabel('Password',{exact:true})),'fill',credential.password);await input('Login',await ui().one(page.getByRole('button',{name:'Login',exact:true})),'click');
  await page.waitForURL(u=>!['/','/login'].includes(u.pathname),{timeout:20000});
  if(new URL(page.url()).pathname==='/onboarding'){await input('First name',await ui().one(page.getByLabel('First Name',{exact:true})),'fill','Synthetic');
    await input('Last name',await ui().one(page.getByLabel('Last Name',{exact:true})),'fill','Tooltip');
    const updated=page.waitForResponse(r=>new URL(r.url()).pathname==='/api/user'&&r.request().method()==='PUT');
    await input('Continue',await ui().one(page.getByRole('button',{name:'Continue',exact:true})),'click');assert((await updated).status()===200,'Profile PUT failed');
    await page.waitForFunction(()=>location.pathname.startsWith('/app')||[...document.querySelectorAll('button')].some(n=>n.textContent.trim()==='Continue'&&!n.disabled),null,{timeout:4000});}
  await input('Synthetic dashboard',null,'goto',runtime.origin+'/app/11111111-1111-4111-8111-111111111111');
  for(const id of f.rows.map(r=>r.observationId))await page.getByText(id,{exact:true}).waitFor({state:'visible'});
  await input('Chart entry',await ui().one(page.locator('#chart-view-button')),'click');await page.locator('.ag-charts-canvas canvas').first().waitFor({state:'visible'});
  await page.evaluate(install);const acquired=await page.evaluate(acquire);Object.assign(preflight,{status:'acquisition-observed',acquired});persist();
  assert(acquired.ok,'Finite acquisition stopped at '+acquired.stage);await page.evaluate(attach);ready=true;
  const admitted=await page.evaluate(admission);Object.assign(preflight,{status:'admission-observed',fixture:f,deliveredEndpointCount:delivered,acquired,admitted,viewport:{width:1440,height:1000,dpr:1}});persist();
  assert(delivered>0,'Fixture endpoint not delivered');
  assert(admitted.model.identity.chartType.value==='groupedColumn'&&admitted.model.identity.switchCategorySeries.value===false,'Initial family/transpose');
  assert(admitted.effective.series.map(s=>s.yKey.value).join(',')===f.seriesOrder.join(','),'Series order mismatch');
  const start=admitted.model.cellRange.rowStartIndex.value,end=admitted.model.cellRange.rowEndIndex.value;
  assert((start===null&&end===null||start===0&&end===4)&&admitted.model.cellRange.columns.join(',')==='period,cashFlow,operatingIncome,revenue','Chart range changed');
  const data=admitted.effective.data;assert(data.length===5&&admitted.options.data.length===5,'Five effective/options rows required');assert(data[0].period.id.value!==data[1].period.id.value,'Duplicate wrapper collapsed');
  assert(data.every((r,i)=>r.period.value.value===f.rows[i].period),'Category/ordinal mismatch');
  const transitions=[];for(const [stage,rows] of [['options',admitted.options.data],['effective',data]]){
  assert(rows.every((r,i)=>r.period.value.value===f.rows[i].period)&&rows[0].period.id.value!==rows[1].period.id.value,'Options/effective category identity mismatch');
  for(let i=0;i<5;i++)for(const key of f.seriesOrder){const actual=rows[i].values[key],own=Object.hasOwn(f.rows[i],key),value=f.rows[i][key];
    if(own&&value!==null)assert(actual.value===value,'Delivered numeric row changed');
    if(actual.own!==own||actual.value!==value)transitions.push({stage,ordinal:i,key,input:{own,...(own?{value}:{})},actual,status:value===null&&actual.value===0?'financial-mismatch-null-to-zero':'unresolved-input-transition'});}}
  const tableRows=admitted.table;assert(tableRows.length===5&&tableRows.every((r,i)=>r.cells.find(c=>c.column==='observationId')?.text===f.rows[i].observationId&&r.cells.find(c=>c.column==='period')?.text===f.rows[i].period),'Table ordinal/ID/Period mismatch');
  for(let i=0;i<5;i++)for(const key of f.seriesOrder)if(typeof f.rows[i][key]==='number'){
    const text=tableRows[i].cells.find(c=>c.column===key)?.text;assert(text!==undefined&&Number(text.replaceAll(',',''))===f.rows[i][key],'Table amount mismatch');}
  Object.assign(preflight,{status:'admitted',transitions,rangeRepresentation:start===null?'whole-table-null':'literal-bounded'});persist();
  admittedAt=Date.now();let family='groupedColumn',mode=null;
  for(const item of cases){phase=item.id;current={...item,began:Date.now(),actions:0,actionCap:item.keyboard?limits.keyboardActions:limits.caseActions,timeCap:item.keyboard?limits.keyboardMs:limits.caseMs,ledger:[],probes:[],keyboard:[],status:'started'};
    try{if(family!==item.family){current.thumbnails=await ui().family(item.family);family=item.family;mode=null;}
      if(item.keyboard)await keyboard();else{if(mode!==item.mode){await ui().mode(item.mode);mode=item.mode;}
        for(const [ordinal,key,third] of item.probes){if(['Single','Multiple','Compact'].includes(third)&&mode!==third){await ui().mode(third);mode=third;}
          await probe(ordinal,key,third==='cashFlow'?third:null);}}
      current.status=current.probes.some(p=>p.status!=='stable')?'unresolved':'observed';
    }catch(e){const failure=failureMetadata(e,'case',credential);current.status=failure.reasonCode==='not-run-budget'?'not-run-budget':'unresolved';Object.assign(current,failure);
      const remainingStatus=current.status==='not-run-budget'?'not-run-budget':'not-run-dependent';
      current.remainingProbes=(item.probes??[]).slice(current.probes.length).map(target=>({target,status:remainingStatus,reason:'Affected case closed; see case reason'}));
      if(item.keyboard)current.remainingModes=item.modes.slice(current.keyboard.length).map(mode=>({mode,status:remainingStatus}));}
    const events=await page.evaluate(()=>{if(window.__tooltip.overflow)throw Error('Event bound');return window.__tooltip.events;});
    const tail={events,elapsedMs:Date.now()-current.began};if(current.id==='T06')finalTail(tail.events,tail.elapsedMs);
    Object.assign(current,tail);json(current.id,current);results.push({id:current.id,status:current.status,actions:current.actions,probes:current.probes.length});current=null;
  }
  json('summary',{status:'bounded-original-capture',source,image,fixtureHash,candidateExecuted:false,results,actions,setupActions,probes,shots,elapsedMs:Date.now()-launch,browserVersion:browser.version(),limits});
}catch(e){process.exitCode=1;const failure=failureMetadata(e,'outer',credential);let caseWrite='not-attempted',firstCaseFailure;
  if(current){current.status='unresolved';
    if(current.failureOrigin==='case'){firstCaseFailure={reason:current.reason,reasonCode:current.reasonCode,reasonOmitted:current.reasonOmitted,failureOrigin:current.failureOrigin};current.outerFailure=failure;}
    else Object.assign(current,failure);
    caseWrite='write-unverified';try{persist();caseWrite='succeeded';}catch{}
  }else{preflight.status='admission-unresolved';Object.assign(preflight,failure);try{persist();}catch{}}
  try{json('failure',{phase,...failure,caseWrite,...(firstCaseFailure?{firstCaseFailure}:{}),completedCases:results});}catch{}
}finally{clearTimeout(timer);const cleanup={contextClosed:false,closed:false,serverClosed:false,listenerRemoved:false};
  const bounded=async fn=>{try{await Promise.race([fn(),new Promise((_,reject)=>setTimeout(()=>reject(Error('Close bound')),5000))]);return true;}catch{return false;}};
  try{if(ready&&!page?.isClosed())cleanup.listenerRemoved=await bounded(()=>page.evaluate(()=>{const p=window.__tooltip;window.__tooltipGrid.removeEventListener('chartOptionsChanged',p.listener);window.__tooltipGrid.removeEventListener('chartRangeSelectionChanged',p.listener);}));}
  finally{try{if(context)await bounded(()=>context.close());cleanup.contextClosed=!context||contextClosed;}
    finally{try{if(browser)await bounded(()=>browser.close());cleanup.closed=!browser?.isConnected();}
      finally{if(browserServer)await bounded(()=>browserServer.close());cleanup.serverClosed=!browserServer||browserServer.process().exitCode!==null||browserServer.process().signalCode!==null;}}}
  for(const item of cases)if(!fs.existsSync(root+'/'+item.id+'.json'))try{json(item.id,{id:item.id,status:admittedAt?'not-run-budget':'not-discriminating',reason:'Lifecycle or admission stopped before this case',actions:0,ledger:[],probes:[],elapsedMs:0});}catch{process.exitCode=1;}
  if(!fs.existsSync(root+'/summary.json'))try{json('summary',{status:'failed-bounded-capture',source,image,fixtureHash,actions,setupActions,probes,shots,candidateExecuted:false,
    results:cases.map(c=>({id:c.id,status:JSON.parse(fs.readFileSync(root+'/'+c.id+'.json')).status})),limits});}catch{process.exitCode=1;}
  for(const [name,value] of [['diagnostics',diagnostics],['browser-cleanup',cleanup],['byte-budget',budget()]])try{json(name,value);}catch{process.exitCode=1;}
  if(!cleanup.closed||!cleanup.contextClosed||!cleanup.serverClosed)process.exitCode=1;}
