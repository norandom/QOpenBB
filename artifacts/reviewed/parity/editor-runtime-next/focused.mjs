import {chromium} from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
const dir=process.env.CAPTURE_OUT||'/mnt/d/Source/QOpenBB/artifacts/parity/editor-runtime-next';
const input='/mnt/d/Source/QOpenBB/artifacts/parity/editor-runtime-next';
const runtime=JSON.parse(fs.readFileSync(input+'/runtime.json'));
const credential=JSON.parse(fs.readFileSync(input+'/credential-private.json'));const secrets={OPENBB_ADMIN_EMAIL:credential.email,OPENBB_ADMIN_PASSWORD:credential.password};
const env={...process.env};delete env.WAYLAND_DISPLAY;
const browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
const context=await browser.newContext({viewport:{width:1440,height:1000}});const page=await context.newPage();const errors=[],requests=[];page.on('console',m=>{if(m.type()==='error')errors.push({type:'console',text:m.text()});});
page.setDefaultTimeout(4000);const cdp=await context.newCDPSession(page);await cdp.send('Runtime.enable');await cdp.send('Network.enable');
cdp.on('Runtime.exceptionThrown',e=>errors.push({type:'exception',message:e.exceptionDetails.text,details:e.exceptionDetails.exception?.description,stack:e.exceptionDetails.stackTrace,url:e.exceptionDetails.url,line:e.exceptionDetails.lineNumber,scriptId:e.exceptionDetails.scriptId}));
cdp.on('Network.loadingFailed',e=>errors.push({type:'network',...e}));
page.on('pageerror',e=>errors.push({type:'pageerror',message:e.message}));
await page.route('**/*',async route=>{const url=new URL(route.request().url());if(url.origin!==runtime.origin){requests.push({blocked:url.origin+url.pathname});await route.abort();}else await route.continue();});
page.on('response',r=>{if(new URL(r.url()).origin===runtime.origin)requests.push({url:r.url(),status:r.status(),contentType:r.headers()["content-type"]});});
const writes=[];let stage='baseline';page.on('request',r=>{if(r.url().includes('/api/pro/dash/')&&r.method()==='POST'){try{const b=r.postDataJSON();if(b.items){const items=Object.fromEntries(Object.entries(b.items).filter(([k])=>k==='11111111-1111-4111-8111-111111111111'));writes.push({stage,items});fs.writeFileSync(dir+'/widget-writes.json',JSON.stringify(writes,null,2));}}catch{}}});
async function settle(label){stage=label;console.log('waiting '+label);await page.keyboard.press('Control+Shift+s');await page.waitForTimeout(10000);if(!writes.some(x=>x.stage===label)){console.log('timer fallback '+label);await page.waitForTimeout(12000);}fs.writeFileSync(dir+'/widget-writes.json',JSON.stringify(writes,null,2));console.log('settled '+label+' writes='+writes.filter(x=>x.stage===label).length);}
try{
await page.route('**/api/pro/dash/{sync,validate-and-sync}',async route=>{if(route.request().method()!=='GET')return route.continue();const upstream=await route.fetch();const actual=await upstream.json();const fixture=JSON.parse(fs.readFileSync(input+'/fixture.json').toString().replaceAll('http://127.0.0.1:32773',runtime.origin));await route.fulfill({json:{...actual,owned:Object.fromEntries(Object.entries(fixture).map(([id,content])=>[id,{content,is_shared:false,created_by:'Synthetic Parity',created_date:'2026-10-16T00:00:00Z',updated_date:'2026-10-16T00:00:00Z'}])),shared:{},entity_shared:{}}});}); await page.route('**/synthetic_financials',route=>route.fulfill({json:[{period:'2024-Q1',revenue:100,operatingIncome:20},{period:'2024-Q1',revenue:120,operatingIncome:25},{period:'2024-Q3',revenue:140,operatingIncome:30},{period:'2024-Q4',revenue:160,operatingIncome:40}]})); await page.goto(runtime.origin,{waitUntil:'networkidle'}); await page.getByLabel('Email',{exact:true}).fill(secrets.OPENBB_ADMIN_EMAIL); await page.getByLabel('Password',{exact:true}).fill(secrets.OPENBB_ADMIN_PASSWORD); await page.getByRole('button',{name:'Login',exact:true}).click(); await page.waitForTimeout(5000);if(page.url().endsWith('/onboarding')){await page.getByLabel('First Name',{exact:true}).fill('Synthetic');await page.getByLabel('Last Name',{exact:true}).fill('Capture');await page.getByRole('button',{name:'Continue',exact:true}).click();await page.waitForTimeout(3000);} await page.goto(runtime.origin+'/app/11111111-1111-4111-8111-111111111111',{waitUntil:'networkidle'}); await page.waitForTimeout(6000); await page.screenshot({path:dir+'/table-dark.png'});

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
});}await page.locator('#chart-view-button').click();await page.waitForTimeout(1800);await acquire();
await page.locator('button').filter({has:page.locator('svg#list-unordered')}).click();await page.getByRole('menuitem',{name:'Chart settings',exact:true}).click();
const panel=page.locator('.ag-chart-docked-container');const ledger=[];const failures=[];
const heading=label=>page.locator('.ag-charts-format-top-level-group-title-bar').filter({hasText:new RegExp('^\\s*'+label+'\\s*$')});
async function state(){await acquire();return page.evaluate(async()=>{
const p=window.__referenceProxy,g=window.__referenceGrid;await p.waitForUpdate();
const scalar=(v,path)=>{if(v===null||['string','boolean'].includes(typeof v)||typeof v==='number'&&Number.isFinite(v))return v;throw Error('Unexpected value '+path+' '+typeof v+' keys='+Object.keys(v??{}).join(',')+' leaves='+Object.entries(v??{}).filter(([k,x])=>x===null||['string','boolean','number'].includes(typeof x)).map(([k,x])=>k+':'+String(x)).join('|'))};
const pick=(x,ks,path)=>Object.fromEntries(ks.filter(k=>x?.[k]!==undefined).map(k=>[k,scalar(x[k],path+'.'+k)]));
const text=(x,path)=>pick(x,['enabled','text','fontFamily','fontSize','fontWeight','fontStyle','color','spacing','padding','rotation','autoRotate','avoidCollisions','placement','minSpacing'],path);
const data=(x,path)=>x?.map((v,i)=>{const r=pick(v,['revenue','operatingIncome'],path+i);if(v.period!==undefined){if(v.period!==null&&typeof v.period==='object'){const keys=Object.keys(v.period);if(keys.some(k=>!['id','value','toString'].includes(k))||typeof v.period.toString!=='function')throw Error('Unknown category wrapper '+path+i);r.period=pick(v.period,['id','value'],path+i+'.period');}else r.period=scalar(v.period,path+i+'.period');}return r;});
const arr=(x,type,path)=>x?.map((v,i)=>{if(typeof v!==type)throw Error('Unexpected '+path+i);return scalar(v,path+i)});
const series=(x,path)=>({...pick(x,['type','xKey','yKey','yName','fill','stroke','strokeWidth','strokeOpacity','fillOpacity','connectMissingData'],path),data:data(x?.data,path+'.data'),lineDash:arr(x?.lineDash,'number',path+'.dash'),label:text(x?.label,path+'.label'),tooltip:pick(x?.tooltip,['enabled','mode','range'],path+'.tooltip'),marker:pick(x?.marker,['enabled','shape','size','fill','stroke','strokeWidth'],path+'.marker'),shadow:pick(x?.shadow,['enabled','color','xOffset','yOffset','blur'],path+'.shadow')});
const axisBase=(x,path)=>({...pick(x,['type','position','min','max'],path),keys:arr(x?.keys,'string',path+'.keys'),title:text(x?.title,path+'.title'),label:text(x?.label,path+'.label'),line:pick(x?.line,['enabled','color','width'],path+'.line'),tick:pick(x?.tick,['enabled','color','width','size'],path+'.tick'),gridLine:{...pick(x?.gridLine,['enabled','stroke','width'],path+'.gridLine'),style:x?.gridLine?.style?.map((v,i)=>({...pick(v,['stroke','strokeWidth'],path+'.style'+i),lineDash:arr(v.lineDash,'number',path+'.dash')}))}});
const axis=(x,path)=>({...axisBase(x,path),...Object.fromEntries(['top','bottom','left','right'].filter(k=>x?.[k]).map(k=>[k,axisBase(x[k],path+'.'+k)]))});
const legend=(x,path)=>({...pick(x,['enabled','position','spacing'],path),item:{...pick(x?.item,['paddingX','paddingY'],path+'.item'),label:text(x?.item?.label,path+'.label'),marker:pick(x?.item?.marker,['size','strokeWidth','padding','shape'],path+'.marker')}});
const branch=(x,path)=>({title:text(x?.title,path+'.title'),subtitle:text(x?.subtitle,path+'.subtitle'),legend:legend(x?.legend,path+'.legend'),series:series(x?.series,path+'.series'),axes:x?.axes?Object.fromEntries(Object.entries(x.axes).map(([k,v])=>[k,axis(v,path+'.axes.'+k)])):undefined});
window.__projectBranch=branch;const raw=g.getChartModels()[0],o=p.chart.chartOptions.processedOptions;
return {events:window.__referenceEvents||[],model:{...pick(raw,['chartId','chartType','chartThemeName','switchCategorySeries','suppressChartRanges','unlinkChart','aggFunc'],'model'),cellRange:{...pick(raw.cellRange,['rowStartIndex','rowEndIndex','rowStartPinned','rowEndPinned'],'range'),columns:arr(raw.cellRange?.columns,'string','columns')},chartOptions:Object.fromEntries(['common','bar','line'].filter(k=>raw.chartOptions?.[k]).map(k=>[k,branch(raw.chartOptions[k],'patch.'+k)]))},options:{data:data(p.getOptions().data,'options.data')},effective:{data:data(o.data,'processed.data'),title:text(o.title,'title'),subtitle:text(o.subtitle,'subtitle'),legend:legend(o.legend,'legend'),axes:o.axes?.map((x,i)=>axis(x,'axis'+i)),series:o.series?.map((x,i)=>series(x,'series'+i))}};
});}
function json(name,v){fs.writeFileSync(dir+'/'+name+'.json',JSON.stringify(v,null,2));}
async function inventory(){return panel.locator('input,[role=combobox]').evaluateAll(xs=>xs.filter(x=>x.getClientRects().length&&getComputedStyle(x).visibility!=='hidden').map(x=>{const label=x.getAttribute('aria-label')||x.getAttribute('aria-labelledby')?.split(' ').map(id=>document.getElementById(id)?.textContent).join(' ')||x.closest('.ag-slider,.ag-field')?.querySelector('label')?.textContent||'';return {id:x.id||null,tag:x.tagName,type:x.type,role:x.getAttribute('role'),label:label.trim(),value:x.value??x.textContent.trim(),checked:x.checked,disabled:x.disabled,min:x.min,max:x.max,step:x.step,html:x.outerHTML};}));}
async function snap(name){json(name,{text:await panel.innerText(),controls:await inventory(),state:await state()});await page.screenshot({path:dir+'/'+name+'.png'});}
async function save(label){stage=label;await page.keyboard.press('Control+Shift+s');await page.waitForTimeout(1800);json('widget-writes',writes);}
async function edit(label,fn){const before=await state();try{await fn();await page.waitForTimeout(180);ledger.push({label,before,after:await state()});json('event-ledger',ledger);}catch(e){failures.push({label,error:e.message});json('unresolved-actions',failures);await page.keyboard.press('Escape');}}
async function group(label,family){await heading(label).click();await snap(family+'-'+label.replaceAll(' ','-')+'-default');
 // Enable existing nested switches through their visible public inputs; never mutate state.
 const toggles=await inventory();for(const c of toggles.filter(x=>x.type==='checkbox'&&!x.checked&&!x.disabled&&x.id))await edit(family+'/'+label+'/enable/'+c.label,async()=>{await page.locator('[id="'+c.id+'"]').check();});
 await snap(family+'-'+label.replaceAll(' ','-')+'-expanded');
 // Dropdown inventories are captured before one real selection; choose a distinct finite option.
 const combos=panel.getByRole('combobox').filter({visible:true});const count=await combos.count();for(let i=0;i<count;i++){const combo=combos.nth(i);if(!await combo.isVisible())continue;const name=await combo.getAttribute('aria-labelledby');await edit(family+'/'+label+'/select/'+i,async()=>{await combo.click();const opts=await page.getByRole('option').allTextContents();json(family+'-'+label.replaceAll(' ','-')+'-options-'+i,{name,options:opts});if(opts.length>1){await page.getByRole('option').nth(Math.min(1,opts.length-1)).click();}else await page.keyboard.press('Escape');});}
 const nums=(await inventory()).filter(x=>x.type==='number'&&!x.disabled&&x.id);for(const c of nums)await edit(family+'/'+label+'/number/'+c.label+'/'+c.id,async()=>{const v=Number(c.value),max=c.max===''?999:Number(c.max);const next=Math.min(max,v+(v<1?0.2:1));const loc=page.locator('[id="'+c.id+'"]');await loc.fill(String(next));await loc.press('Tab');});
 const texts=(await inventory()).filter(x=>x.type==='text'&&!x.disabled&&x.id);for(const c of texts)await edit(family+'/'+label+'/text/'+c.label,async()=>{const loc=page.locator('[id="'+c.id+'"]');await loc.fill('Synthetic '+label+' '+family);await loc.press('Tab');});
 await snap(family+'-'+label.replaceAll(' ','-')+'-edited');await save(family+'-'+label);await heading(label).click();}
await snap('initial-chart');const initial=JSON.parse(fs.readFileSync(dir+'/initial-chart.json'));if(initial.state.effective.data.length!==4)throw Error('Initial finite projection row count');json('initial-projection-assertion',{passed:true,rows:4});
await page.evaluate(()=>{window.__referenceEvents=[];for(const type of ['chartOptionsChanged','chartRangeSelectionChanged','chartCreated'])window.__referenceGrid.addEventListener(type,e=>{const entry={type:e.type,chartId:e.chartId,chartType:e.chartType,chartThemeName:e.chartThemeName};if(e.chartOptions)entry.chartOptions=Object.fromEntries(['common','bar','line'].filter(k=>e.chartOptions[k]).map(k=>[k,window.__projectBranch(e.chartOptions[k],'event.'+k)]));window.__referenceEvents.push(entry);});});
await page.getByRole('tab',{name:'Customize',exact:true}).click();await page.waitForTimeout(500);
async function numberField(label,value){const loc=panel.locator('.ag-slider').filter({has:page.locator('label').filter({hasText:new RegExp('^'+label+'$')})}).locator('input[type=number]:visible').first();await loc.fill(String(value));await loc.press('Tab');}
async function options(label,choose){const combo=panel.getByRole('combobox',{name:label,exact:true});await combo.click();json('domain-'+stage+'-'+label.replaceAll(' ','-'),{label,options:await page.getByRole('option').allTextContents()});if(choose)await page.getByRole('option',{name:choose,exact:true}).click();else await page.keyboard.press('Escape');}
for(const name of ['Horizontal Axis','Vertical Axis','Series','Legend']){
 stage=name.replaceAll(' ','-');await heading(name).click();await snap(stage+'-default');
 if(name==='Horizontal Axis'){
  await edit('horizontal-label-padding-9',()=>numberField('Padding',9));
  await edit('horizontal-label-auto-rotate-off',()=>panel.getByRole('checkbox',{name:'Auto Rotate',exact:true}).uncheck());
  await snap('Horizontal-Axis-auto-rotate-off');
 }
 if(name==='Vertical Axis'){await edit('vertical-thickness-3',()=>numberField('Thickness',3));await edit('vertical-label-size-14',()=>options('Size','14'));}
 if(name==='Series'){
  await edit('series-tooltip-single',()=>options('Tooltip Mode','Single'));
  await edit('series-labels-on',()=>panel.getByRole('checkbox',{name:'Labels',exact:true}).check());await snap('Series-labels-enabled');
  
  await edit('series-stroke-width-3',()=>numberField('Stroke Width',3));
 }
 if(name==='Legend'){
  await edit('legend-weight-bold',()=>options('Weight','Bold'));
  await edit('legend-size-14',()=>options('Size','14'));
  await edit('legend-marker-size-15',()=>numberField('Marker Size',15));
  await edit('legend-horizontal-spacing-40',()=>numberField('Horizontal Spacing',40));
 }
 await snap(stage+'-edited');await heading(name).click();
}
await page.getByRole('tab',{name:'Set Up',exact:true}).click();await snap('setup-default');
for(const name of ['Aggregate','Switch Category / Series']){await edit('setup/'+name+'/on',async()=>await panel.getByRole('checkbox',{name,exact:true}).check());await snap('setup-'+name.replaceAll(' / ','-').replaceAll(' ','-')+'-on');await edit('setup/'+name+'/off',async()=>await panel.getByRole('checkbox',{name,exact:true}).uncheck());await snap('setup-'+name.replaceAll(' / ','-').replaceAll(' ','-')+'-off');}
await page.getByRole('tab',{name:'Chart',exact:true}).click();await page.getByRole('button',{name:'Line',exact:true}).click();await page.getByRole('tab',{name:'Customize',exact:true}).click();await heading('Series').click();await snap('line-Series-default');
await edit('line-markers-on',()=>panel.getByRole('checkbox',{name:'Markers',exact:true}).check());await snap('line-markers-on');
await edit('line-marker-shape',()=>options('Shape','Diamond'));await edit('line-marker-size-9',()=>numberField('Size',9));await snap('line-Series-edited');
await save('final');json('summary',{actions:ledger.length,failures});
}catch(e){await page.screenshot({path:dir+'/failure.png'});fs.writeFileSync(dir+'/failure-ui.txt',await page.locator('body').innerText());throw e;}finally{fs.writeFileSync(dir+'/diagnostics.json',JSON.stringify({errors,requests},null,2));await browser.close();}


