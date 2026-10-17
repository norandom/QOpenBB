import {chromium} from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {runRoot,scriptRoot,write} from './io.mjs';
import {limits,roles,rows} from './limits.mjs';
import {installProjection} from './projection.mjs';

const runtime=JSON.parse(fs.readFileSync(path.join(runRoot,'runtime-private.json')));
const credential=JSON.parse(fs.readFileSync(path.join(runRoot,'credential-private.json')));
if(!/^http:\/\/127\.0\.0\.1:[0-9]+$/.test(runtime.origin))throw Error('Owned origin required');
const started=Date.now(),diagnostics=[],operations=[],ledger=[],menus=[],cases=[];
let interactions=0,edits=0,caseName='setup',stopped=false,caseMarkup=0,browser,page,context;
let currentAction='setup',snapshotIndex=0,lastSnapshot=null,diagnosticOverflow=false;
const journeyTimer=setTimeout(()=>{
  stopped=true;write('deadline',{kind:'journey',limitMs:limits.journey,case:caseName,action:currentAction});
  process.exitCode=1;browser?.close().catch(()=>{});
},limits.journey);
const clean=text=>String(text).replaceAll(credential.email,'[synthetic-email]')
  .replaceAll(credential.password,'[redacted]').replaceAll(runtime.origin,'[owned-origin]');
function diagnostic(entry){
  if(diagnostics.length>=limits.diagnostics){diagnosticOverflow=true;return;}
  for(const value of Object.values(entry))if(typeof value==='string'&&value.length>limits.diagnosticChars){
    diagnosticOverflow=true;return;
  }
  diagnostics.push(entry);
}
function guard(){
  if(stopped)throw Error('Capture already stopped');
  if(Date.now()-started>=limits.journey)throw Error('Dark journey 900s deadline');
  if(diagnosticOverflow)throw Error('Diagnostic projection bound exceeded');
}
async function bounded(label,ms,operation){
  let timer;
  try{return await Promise.race([operation(),new Promise((_,reject)=>{
    timer=setTimeout(()=>{stopped=true;reject(Error(label+' deadline '+ms+'ms'));},ms);
  })]);}finally{clearTimeout(timer);}
}
async function operate(kind,label,operation,fieldEdit=false){
  guard();
  if(interactions>=limits.interactions||fieldEdit&&edits>=limits.edits)throw Error('UI operation budget');
  interactions++;if(fieldEdit)edits++;
  operations.push({case:caseName,action:currentAction,kind,label,interactions,edits});
  write('operations',operations);
  return bounded('UI '+kind,limits.action,operation);
}
async function one(locator,label,visible=true){
  const count=await locator.count();if(count!==1)throw Error(label+' cardinality '+count+' expected one');
  if(visible&&!await locator.isVisible())throw Error(label+' not visible');
  return locator;
}
async function click(locator,label,fieldEdit=false){
  await one(locator,label);
  await operate('scroll',label,()=>locator.scrollIntoViewIfNeeded());
  return operate('click',label,()=>locator.click(),fieldEdit);
}
async function fill(locator,label,value){
  await one(locator,label);await operate('scroll',label,()=>locator.scrollIntoViewIfNeeded());
  await operate('fill',label,()=>locator.fill(value),true);
  await operate('keypress',label+' commit Tab',()=>locator.press('Tab'));
}
async function toggle(locator,label,on){
  await one(locator,label);
  if(await locator.isChecked()===on)throw Error(label+' already in requested toggle state');
  await operate('scroll',label,()=>locator.scrollIntoViewIfNeeded());
  await operate(on?'check':'uncheck',label,()=>on?locator.check():locator.uncheck(),true);
}
const panel=()=>page.locator('.ag-chart-docked-container');
const heading=label=>panel().locator('.ag-charts-format-top-level-group-title-bar')
  .filter({hasText:new RegExp('^\\s*'+label+'\\s*$')});
async function group(label){
  const target=await one(heading(label),label+' heading');
  const expanded=await target.getAttribute('aria-expanded');
  if(!['true','false'].includes(expanded))throw Error(label+' expanded contract missing');
  if(expanded==='false')await click(target,label+' expand');
}
const caption=label=>panel().locator('[data-ref="titleGroup"] .ag-font-panel')
  .filter({has:page.locator('.ag-toggle-button-label').filter({hasText:new RegExp('^'+label+'$')})});
async function captionScope(role){await group('Titles');return one(caption(role.label),role.label+' scope');}
async function acquire(){
  return page.evaluate(()=>{
    for(const root of document.querySelectorAll('.ag-root-wrapper')){
      let fiber=root[Object.keys(root).find(key=>key.startsWith('__reactFiber'))];
      for(let depth=0;fiber&&depth<18;depth++,fiber=fiber.return){
        const value=fiber.memoizedProps?.value,grid=value?.gridRef?.current?.api||fiber.child?.stateNode?.api;
        if(typeof grid?.getChartModels==='function')window.__referenceGrid=grid;
      }
    }
    const grid=window.__referenceGrid,models=grid?.getChartModels();
    if(!models||models.length!==1||models[0].chartType!=='groupedColumn')throw Error('One groupedColumn model required');
    window.__referenceProxy=grid.getChartRef(models[0].chartId).chart;
    if(!window.__referenceProxy?.chart?.chartOptions?.processedOptions)throw Error('Original chart unavailable');
    return {chartId:models[0].chartId,chartType:models[0].chartType,chartThemeName:models[0].chartThemeName};
  });
}
async function state(){
  guard();
  return bounded('settlement',limits.settlement,async()=>{
    await acquire();await page.evaluate(()=>window.__referenceProxy.waitForUpdate());
    await page.waitForFunction(()=>window.__referenceProxy.chart.ctx.animationManager.isActive()===false,
      null,{timeout:limits.settlement,polling:50});
    let previous=null;
    while(true){
      guard();const snapshot=await page.evaluate(()=>window.__captions.snapshot());
      const geometry=JSON.stringify({scene:snapshot.scene,geometry:snapshot.geometry});
      if(geometry===previous){snapshot.settled.stableSamples=2;snapshot.settled.sampleSpacingMs=100;return snapshot;}
      previous=geometry;await new Promise(resolve=>setTimeout(resolve,100));
    }
  });
}
async function controls(){
  return panel().locator('input,[role=combobox]').evaluateAll(elements=>{
    const shown=elements.filter(element=>element.getClientRects().length&&getComputedStyle(element).visibility!=='hidden');
    if(shown.length>128)throw Error('Visible control bound');
    return shown.map(element=>{
      const label=(element.getAttribute('aria-label')||element.getAttribute('aria-labelledby')?.split(' ')
        .map(id=>document.getElementById(id)?.textContent).join(' ')||element.closest('.ag-slider,.ag-field')
        ?.querySelector('label')?.textContent||'').trim();
      const value=element.value??element.textContent.trim();
      if(label.length>512||String(value).length>512)throw Error('Control string bound');
      const box=element.getBoundingClientRect();
      return {label,type:element.type,role:element.getAttribute('role'),value,checked:element.checked,
        disabled:element.disabled,min:element.min,max:element.max,step:element.step,
        rect:{x:box.x,y:box.y,width:box.width,height:box.height},clipped:
          box.top<0||box.left<0||box.bottom>innerHeight||box.right>innerWidth};
    });
  });
}
async function chosen(locator,label){
  await one(locator,label);
  const observation=await locator.evaluate(element=>({tag:element.tagName,id:element.id,
    html:element.closest('.ag-field,.ag-slider,.ag-picker-field,.ag-toggle-button')?.outerHTML||element.outerHTML,
    ancestorClass:element.closest('.ag-font-panel')?.className,
    ancestorLabel:element.closest('.ag-font-panel')?.querySelector('.ag-toggle-button-label')?.textContent}));
  const bytes=Buffer.byteLength(observation.html);
  if(bytes>limits.controlMarkupBytes||caseMarkup+bytes>limits.caseMarkupBytes)throw Error('Chosen control markup bound');
  caseMarkup+=bytes;return {label,cardinality:1,...observation};
}
async function capture(label,screenshot=true){
  const measured=await state(),text=await panel().innerText();
  if(text.length>limits.panelChars)throw Error('Panel text bound');
  const name=String(++snapshotIndex).padStart(3,'0')+'-'+label;
  const captions=await panel().locator('[data-ref="titleGroup"] .ag-font-panel').evaluateAll(elements=>{
    if(elements.length!==4)throw Error('Exact four caption UI scopes required');
    return elements.map(element=>{
      const label=element.querySelector('.ag-toggle-button-label')?.textContent;
      const input=element.querySelector('.ag-toggle-button-input');
      const details=[...element.querySelectorAll('input[type=text],[role=combobox]')].map(control=>({
        role:control.getAttribute('role'),type:control.type,value:control.value??control.textContent,
        visible:!!control.getClientRects().length&&getComputedStyle(control).visibility!=='hidden'}));
      if(details.length>16||details.some(detail=>String(detail.value).length>512))throw Error('Caption UI bound');
      return {label,toggle:input?{checked:input.checked,disabled:input.disabled}:null,details};
    });
  });
  write(name,{case:caseName,action:currentAction,counters:{interactions,edits},
    ui:{text,controls:await controls(),captions},state:measured});
  if(screenshot)await page.screenshot({path:path.join(runRoot,name+'.png')});
  lastSnapshot={name,state:measured};console.log('CAPTURE '+name);return lastSnapshot;
}
async function action(name,input,locator,operation){
  currentAction=name;
  const before=await capture(name+'-before',false),control=await chosen(locator,input.control);
  await page.evaluate(()=>{window.__captions.events=[];});
  await operation();
  const after=await capture(name+'-after');
  ledger.push({case:caseName,name,kind:'original-application-real-ui',input,control,
    before:before.name+'.json',after:after.name+'.json',events:after.state.events,
    counters:{interactions,edits}});write('action-ledger',ledger);return after.state;
}
async function runCase(name,operation,ms=limits.case){
  caseName=name;caseMarkup=0;
  await page.evaluate(()=>{window.__captions.caseEventCount=0;window.__captions.events=[];});
  const begin=Date.now();await bounded('case '+name,ms,operation);
  cases.push({name,completed:true,durationMs:Date.now()-begin,interactions,edits});write('cases',cases);
}
function effectiveRole(snapshot,role){
  return role.key?snapshot.effective[role.key]:snapshot.effective.axes.find(axis=>
    axis.identity.type.value===role.type&&axis.identity.position.value===role.position)?.title;
}
async function captionToggle(role,on,name){
  const scope=await captionScope(role),locator=scope.getByRole('checkbox',{name:role.label,exact:true});
  return action(name,{control:role.label,enabled:on},locator,()=>toggle(locator,role.label,on));
}
async function weight(scope,label,choice){
  const combo=scope.getByRole('combobox',{name:'Weight',exact:true}).filter({visible:true});
  await one(combo,label+' Weight');
  currentAction='menu-'+label.toLowerCase().replaceAll(' ','-');
  await click(combo,label+' Weight open');
  const options=page.getByRole('option').filter({visible:true});
  const domain=await options.allTextContents();
  if(domain.length>limits.options||domain.some(value=>value.length>limits.optionChars))throw Error('Menu domain bound');
  const menu={role:label,choice,selected:await combo.innerText(),domain};menus.push(menu);write('menu-role-matrix',menus);
  if(!domain.includes(choice)){
    await operate('keypress',label+' menu Escape',()=>page.keyboard.press('Escape'));
    if(choice==='Predefined'){menu.notOffered=true;write('menu-role-matrix',menus);return;}
    throw Error(label+' missing Weight '+choice);
  }
  const option=page.getByRole('option',{name:choice,exact:true}).filter({visible:true});
  await action('weight-'+label.toLowerCase().replaceAll(' ','-')+'-'+choice.toLowerCase().replaceAll(' ','-'),
    {control:label+' Weight',choice,domain},option,()=>click(option,label+' Weight '+choice,true));
}
async function paddingField(side,value,name){
  await group('Chart Style');
  const slider=panel().locator('[data-ref="chartPaddingGroup"] [data-ref="padding'+side+'Slider"]');
  await one(slider,side+' padding slider');
  const label=(await slider.locator('label').innerText()).trim();if(label!==side)throw Error('Padding adjacent label mismatch');
  const locator=slider.locator('input[type=number]:visible');await one(locator,side+' padding');
  const attributes=await locator.evaluate(element=>({min:element.min,max:element.max,step:element.step}));
  if(attributes.max!=='200')throw Error('Padding max discriminator mismatch');
  return action(name,{control:'Chart Style Padding '+side,value,attributes},locator,
    ()=>fill(locator,side+' padding',String(value)));
}

async function setup(){
  await page.route('**/*',async route=>{
    const url=new URL(route.request().url());
    if(url.origin!==runtime.origin){diagnostic({kind:'blocked-external',path:clean(url.origin+url.pathname)});return route.abort();}
    return route.continue();
  });
  await page.route('**/api/pro/dash/{sync,validate-and-sync}',async route=>{
    if(route.request().method()!=='GET')return route.continue();
    const upstream=await route.fetch(),actual=await upstream.json();
    const fixture=JSON.parse(fs.readFileSync(path.join(scriptRoot,'fixture.json'),'utf8')
      .replaceAll('http://127.0.0.1:32773',runtime.origin));
    return route.fulfill({json:{...actual,owned:Object.fromEntries(Object.entries(fixture).map(([id,content])=>[id,
      {content,is_shared:false,created_by:'Synthetic Parity',created_date:'2026-10-17T00:00:00Z',
        updated_date:'2026-10-17T00:00:00Z'}])),shared:{},entity_shared:{}}});
  });
  await page.route('**/synthetic_financials',route=>route.fulfill({json:rows}));
  await page.goto(runtime.origin,{waitUntil:'domcontentloaded'});
  await operate('fill','synthetic login email',()=>page.getByLabel('Email',{exact:true}).fill(credential.email),true);
  await operate('fill','synthetic login password',()=>page.getByLabel('Password',{exact:true}).fill(credential.password),true);
  await click(page.getByRole('button',{name:'Login',exact:true}),'Login');
  await page.waitForURL(url=>!['/','/login'].includes(url.pathname),{timeout:limits.navigation});
  if(new URL(page.url()).pathname==='/onboarding'){
    await operate('fill','synthetic first name',()=>page.getByLabel('First Name',{exact:true}).fill('Synthetic'),true);
    await operate('fill','synthetic last name',()=>page.getByLabel('Last Name',{exact:true}).fill('Capture'),true);
    const updated=page.waitForResponse(response=>new URL(response.url()).pathname==='/api/user'&&
      response.request().method()==='PUT',{timeout:15000});
    await click(page.getByRole('button',{name:'Continue',exact:true}),'Onboarding Continue');
    if((await updated).status()!==200)throw Error('Synthetic profile PUT failed');
    await page.waitForFunction(()=>[...document.querySelectorAll('button')].some(button=>
      button.textContent.trim()==='Continue'&&!button.disabled),null,{timeout:15000});
  }
  await page.goto(runtime.origin+'/app/11111111-1111-4111-8111-111111111111',{waitUntil:'domcontentloaded'});
  for(const value of ['2024-Q1','2024-Q2','2024-Q3','2024-Q4','100','140','160'])
    await page.getByText(value,{exact:true}).first().waitFor({state:'visible',timeout:15000});
  await click(page.locator('#chart-view-button'),'Chart view');
  await page.locator('.ag-charts-canvas canvas').first().waitFor({state:'visible',timeout:15000});
  const identity=await acquire();write('chart-identity',identity);
  if(!identity.chartThemeName.toLowerCase().includes('dark'))throw Error('Stock dark fixture required');
  await page.evaluate(installProjection);
  await click(page.locator('button').filter({has:page.locator('svg#list-unordered')}),'Chart actions');
  await click(page.getByRole('menuitem',{name:'Chart settings',exact:true}),'Chart settings');
  await click(page.getByRole('tab',{name:'Customize',exact:true}),'Customize');
}

try{
  const env={...process.env};delete env.WAYLAND_DISPLAY;
  browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle',
    '--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
  context=await browser.newContext({viewport:{width:1440,height:1000}});page=await context.newPage();
  page.setDefaultTimeout(limits.action);page.setDefaultNavigationTimeout(limits.navigation);
  page.on('console',message=>{if(['error','warning'].includes(message.type()))diagnostic({
    kind:'console',type:message.type(),text:clean(message.text())});});
  page.on('pageerror',error=>diagnostic({kind:'pageerror',text:clean(error.message)}));
  page.on('response',response=>{if(response.status()>=400)diagnostic({kind:'http-error',
    path:clean(new URL(response.url()).pathname),status:response.status()});});
  const cdp=await context.newCDPSession(page);await cdp.send('Runtime.enable');await cdp.send('Network.enable');
  cdp.on('Runtime.exceptionThrown',event=>diagnostic({kind:'cdp-exception',text:clean(event.exceptionDetails.text)}));
  cdp.on('Network.loadingFailed',event=>diagnostic({kind:'cdp-network-failed',text:clean(event.errorText),type:event.type}));
  await setup();
  let initialData,initialKeys,originalPadding;
  await runCase('01-stock-baseline',async()=>{
    await group('Chart Style');await capture('stock-padding');await group('Titles');
    for(const role of roles){const scope=await captionScope(role);
      if(await scope.getByRole('checkbox',{name:role.label,exact:true}).isChecked())throw Error(role.label+' baseline unexpectedly on');}
    const baseline=await capture('stock-captions');initialData=JSON.stringify(baseline.state.data);
    initialKeys=JSON.stringify(baseline.state.effective.series.map(series=>series.identity));
  });
  await runCase('02-all-four-captions',async()=>{
    for(const role of roles){
      await captionToggle(role,true,'enable-'+role.label.toLowerCase().replaceAll(' ','-'));
      const scope=await captionScope(role),locator=scope.getByRole('textbox',{name:'Title',exact:true}).filter({visible:true});
      const after=await action('text-'+role.label.toLowerCase().replaceAll(' ','-'),{control:role.label+' Title',text:role.text},
        locator,()=>fill(locator,role.label+' text',role.text));
      if(effectiveRole(after,role)?.text.value!==role.text)throw Error(role.label+' text binding mismatch');
    }
    await capture('all-on');
  });
  for(const [index,role]of roles.entries())await runCase('0'+(index+3)+'-'+role.label.toLowerCase().replaceAll(' ','-')+'-off',async()=>{
    await captionToggle(role,false,'disable-'+role.label.toLowerCase().replaceAll(' ','-'));
    await captionToggle(role,true,'restore-'+role.label.toLowerCase().replaceAll(' ','-'));
  });
  await runCase('07-weight-menu-contract',async()=>{
    const title=await captionScope(roles[0]);
    for(const choice of ['Normal','Bold','Italic','Bold Italic','Predefined'])await weight(title,'Chart Title',choice);
    for(const role of roles.slice(1))await weight(await captionScope(role),role.label,'Bold Italic');
    for(const name of ['Legend','Horizontal Axis','Vertical Axis','Series']){
      await group(name);
      const groupRoot=heading(name).locator('..');
      if(name==='Series'){
        const checkbox=groupRoot.getByRole('checkbox',{name:'Labels',exact:true}).filter({visible:true});
        await action('series-labels-enable',{control:'Series Labels',enabled:true},checkbox,
          ()=>toggle(checkbox,'Series Labels',true));
      }
      await weight(groupRoot,name==='Series'?'Series Labels':name==='Legend'?'Legend':name+' Labels','Bold Italic');
    }
    await capture('weight-matrix-all-on');
  },limits.weightCase);
  await runCase('08-asymmetric-padding',async()=>{
    await group('Chart Style');const start=await capture('padding-start');originalPadding=start.state.effective.padding;
    for(const [side,value]of [['Top',41],['Right',67],['Bottom',29],['Left',13],['Right',13],['Left',67]])
      await paddingField(side,value,'padding-'+side.toLowerCase()+'-'+value);
  },limits.paddingCase);
  await runCase('09-retained-details',async()=>{
    for(const side of ['Top','Right','Bottom','Left']){
      const value=originalPadding[side.toLowerCase()];if(value.kind!=='value')throw Error('Initial padding unavailable');
      await paddingField(side,value.value,'padding-restore-'+side.toLowerCase());
    }
    for(const role of roles){await captionToggle(role,false,'retained-off-'+role.label.toLowerCase().replaceAll(' ','-'));
      await captionToggle(role,true,'retained-on-'+role.label.toLowerCase().replaceAll(' ','-'));}
    const final=await capture('final-all-on');
    if(JSON.stringify(final.state.data)!==initialData||JSON.stringify(final.state.effective.series.map(series=>series.identity))!==initialKeys)
      throw Error('Unchanged data/key ordering assertion failed');
  });
  write('summary',{completed:true,cases:cases.length,interactions,edits,durationMs:Date.now()-started,
    scope:'Original dark groupedColumn only; screenshots require independent visual review.',
    openContract:'Frozen RoleTypography omits fontStyle; capture does not repair or default it.'});
}catch(error){
  stopped=true;write('failure',{case:caseName,action:currentAction,message:clean(error.message),
    counters:{interactions,edits},completedCases:cases.map(entry=>entry.name),lastSnapshot:lastSnapshot?.name});
  process.exitCode=1;
}finally{
  clearTimeout(journeyTimer);
  stopped=true;write('diagnostics',{cdp:{runtimeEnabled:!!page,networkEnabled:!!page},diagnostics,overflow:diagnosticOverflow});
  let closed=false;
  if(browser)try{await bounded('browser cleanup',20000,()=>browser.close());closed=true;}catch{}
  write('browser-cleanup',{closed,unresolved:!closed});if(!closed)process.exitCode=1;
}
