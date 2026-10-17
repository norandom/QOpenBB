import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {cases,fixture,fixtureHash,planHash,hash,canonical,limits} from './contract.mjs';
import {coordinate} from './collector.mjs';
import {install,geometry,acquire} from './projection.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),checks=[];
function check(name,condition){checks.push({name,passed:!!condition});if(!condition)throw Error(name);}
const f=fixture();check('fixture hash',hash(canonical(f))===fixtureHash);
check('five rows',f.rows.length===5);check('explicit null',Object.hasOwn(f.rows[2],'revenue')&&f.rows[2].revenue===null);
check('absent revenue',!Object.hasOwn(f.rows[3],'revenue'));check('series source order',f.seriesOrder.join(',')==='cashFlow,operatingIncome,revenue');
check('duplicate category unequal values',f.rows[0].period===f.rows[1].period&&f.rows[0].revenue!==f.rows[1].revenue);
check('tie',f.rows[4].revenue===f.rows[4].operatingIncome);check('eight fixed cases',cases.map(c=>c.id).join(',')==='T01,T02,T03,T04,T05,T06,T07,T08');
check('case actions arithmetic',7*limits.caseActions+limits.keyboardActions+limits.setupActions===limits.totalActions);
const pointerProbes=cases.reduce((n,c)=>n+(c.probes?.length??0),0);
check('24 fixed pointer probes',pointerProbes===24);check('48 planned maximum screenshots',pointerProbes+3+3*7===limits.screenshots);
check('approved caps',JSON.stringify(limits)===JSON.stringify({cases:8,setupActions:24,caseActions:36,keyboardActions:120,totalActions:396,
  caseMs:60000,keyboardMs:120000,startupMs:180000,casesMs:600000,cleanupMs:60000,outerMs:900000,inputStopMs:840000,
  selectorMs:4000,settlementMs:6000,updateMs:4000,geometrySamples:8,geometryIntervalMs:250,
  tooltipSamples:20,tooltipIntervalMs:100,tooltipMs:2000,screenshots:48,probes:96,
  caseBytes:131072,jsonBytes:2097152,pngBytes:2097152,runBytes:104857600,htmlBytes:8192}));
const projection=fs.readFileSync(here+'/projection.mjs','utf8'),journey=fs.readFileSync(here+'/journey.mjs','utf8');
const shell=fs.readFileSync(here+'/run.sh','utf8'),io=fs.readFileSync(here+'/io.mjs','utf8'),cleanup=fs.readFileSync(here+'/cleanup.mjs','utf8'),collector=fs.readFileSync(here+'/collector.mjs','utf8');
check('no engine mutation/picking/focus',!/(?:\.focus\(|dispatchEvent|pickNodes|getTooltipContent|updateChart|setChart|setOptions|transformPoint|localToCanvas)/.test(projection+journey));
check('finite ancestry',projection.includes('depth<18')&&projection.includes('root.parentNode===null')&&projection.includes('managed.parentNode===sr'));
check('only named node point leaves',projection.includes("p.pick(n.point,['x','y'])"));
check('no broad page dump',!/(document\.body\.(?:innerHTML|textContent)|accessibility\.snapshot|storageState|localStorage|sessionStorage)/.test(projection+journey));
check('credentials omitted from setup ledger',journey.includes("argument:phase==='setup'?null"));
check('admission retained before assertion',journey.indexOf("status:'admission-observed'")<journey.indexOf("assert(delivered>0"));
check('whole-table or explicit range',journey.includes('start===null&&end===null||start===0&&end===4'));
check('five table rows and amount validation',journey.includes('tableRows.length===5')&&journey.includes('Table amount mismatch'));
check('prospective started action receipt',journey.includes('current.ledger.push(entry);persist();'));
check('final action receipt',journey.includes('entry.elapsedMs=Date.now()-started;persist();'));
check('affected probe closes case',journey.includes("record.reason=String(e.message).split('\\n')[0];throw e;"));
check('single-process timer watchdog',shell.includes('setTimeout(')&&!shell.includes('sleep 840'));
check('bounded active/watchdog waits',shell.includes('3s tail --pid=')&&shell.includes('50s node'));
check('owned browser process identity',cleanup.includes('browserIdentityMatched')&&cleanup.includes('owned.startTicks'));
check('cleanup before diagnostics',journey.indexOf('context.close()')<journey.indexOf("[['diagnostics',diagnostics]"));
check('cleanup nested finally',journey.includes('finally{try{if(browser)')&&journey.includes('finally{if(browserServer)'));
check('reserved failure/cleanup bytes',io.includes('32768')&&io.includes('limits.jsonBytes-reserved'));
check('inactive identical pair',collector.includes('prior?.animationActive===false')&&collector.includes('JSON.stringify(sample)===JSON.stringify(prior)'));
check('nonstable tooltip closes probe',journey.includes("if(record.status!=='stable')throw Error(record.status)"));
check('nonstable tooltip closes keyboard',journey.includes("if(state.status!=='stable'){k.terminalImage=")&&journey.includes("if(after.status!=='stable')throw Error(after.status)"));
check('keyboard images with explicit before-state reuse',journey.includes('beforeImageReuse:')&&journey.includes('initialOrTerminalImage'));
check('dependent versus budget remaining outcomes',journey.includes("'not-run-budget':'not-run-dependent'"));
check('options/effective field validation',journey.includes("[['options',admitted.options.data],['effective',data]]"));
for(const name of fs.readdirSync(here).filter(n=>n.endsWith('.mjs'))){execFileSync(process.execPath,['--check',here+'/'+name]);check('syntax '+name,true);}
execFileSync('bash',['-n',here+'/run.sh']);check('shell syntax',true);
const field=value=>({kind:'value',value}),absent={kind:'absent',own:false};
const transform=(x,y)=>({translationX:field(x),translationY:field(y),rotation:absent,scalingX:absent,scalingY:absent});
const plain={translationX:absent,translationY:absent,rotation:absent,scalingX:absent,scalingY:absent};
const g={dpr:1,animationActive:false,seriesRect:{x:10,y:20,width:200,height:200},scene:{width:400,height:400},canvas:{x:100,y:100,width:400,height:400},area:{x:100,y:100,width:400,height:400},
  series:[{id:'s',yKey:'cashFlow',chainValid:true,transforms:[transform(0,0),plain,transform(10,20),plain],nodes:[{fields:{datumIndex:field(0),x:field(20),y:field(30),width:field(10),height:field(20)},xValue:{id:field('wrapper-0')},point:{x:field(25),y:field(40)}}]}]};
check('bar coordinate uses translations once',JSON.stringify(coordinate(g,0,'cashFlow','groupedColumn').point)===JSON.stringify({x:135,y:160}));
check('line point coordinate',JSON.stringify(coordinate(g,0,'cashFlow','line').point)===JSON.stringify({x:135,y:160}));
const sourceRoot={parentNode:undefined},sourceSeriesRoot={parentNode:sourceRoot,translationX:10,translationY:20},managed={parentNode:sourceSeriesRoot},content={parentNode:managed,translationX:0,translationY:0};
const fakeElement={getClientRects:()=>[{}],getBoundingClientRect:()=>({x:100,y:100,width:400,height:400})};
globalThis.window={};globalThis.document={querySelectorAll:()=>[fakeElement]};globalThis.getComputedStyle=()=>({visibility:'visible',opacity:'1'});globalThis.devicePixelRatio=1;
install();window.__tooltipProxy={chart:{seriesRect:{x:10,y:20,width:200,height:200},seriesRoot:sourceSeriesRoot,
  ctx:{root:sourceRoot,scene:{width:400,height:400},animationManager:{isActive:()=>false}},series:[{id:'s',type:'bar',properties:{yKey:'cashFlow'},contentGroup:content,
    getNodeData:()=>[{datumIndex:0,x:20,y:30,width:10,height:20,xValue:{id:'wrapper-0',value:'2024-Q1'},point:{x:25,y:40}}]}]}};
const undefinedRoot=geometry({ordinal:0,key:'cashFlow'});
check('actual geometry accepts source undefined root terminal',undefinedRoot.series[0].chainValid&&undefinedRoot.series[0].rootTerminal.own&&undefinedRoot.series[0].rootTerminal.in&&undefinedRoot.series[0].rootTerminal.type==='undefined'&&undefinedRoot.series[0].rootTerminal.value.kind==='undefined');
check('undefined root coordinate',coordinate(undefinedRoot,0,'cashFlow','groupedColumn').point.x===135);
sourceRoot.parentNode=null;const nullRoot=geometry({ordinal:0,key:'cashFlow'});
check('actual geometry accepts null root terminal',nullRoot.series[0].chainValid&&nullRoot.series[0].rootTerminal.type==='object'&&nullRoot.series[0].rootTerminal.value===null);
sourceRoot.parentNode={};check('actual geometry rejects extra ancestor',geometry({ordinal:0,key:'cashFlow'}).series[0].chainValid===false);
delete globalThis.window;delete globalThis.document;delete globalThis.getComputedStyle;delete globalThis.devicePixelRatio;
function acquisitionCase(build){globalThis.window={};install();const root={};globalThis.document={querySelectorAll:()=>[root]};
  const proxy={getOptions(){},waitForUpdate(){},chart:{chartOptions:{processedOptions:{}}}};
  let calls=0;const api={getChartModels:()=>[{chartId:'only-chart',chartType:'groupedColumn',chartThemeName:'ag-default-dark'}],getChartRef:id=>{calls++;if(id!=='only-chart')throw Error('Wrong model key');return {chart:proxy};}};
  const fiber={memoizedProps:{value:{gridRef:{current:{api}}}},return:null};root.__reactFiber_test=fiber;build({root,fiber,api,proxy});const result=acquire();
  delete globalThis.window;delete globalThis.document;return {result,calls};}
let a=acquisitionCase(()=>{});check('model keyed finite acquisition',a.result.ok&&a.calls===1&&a.result.modelIdentity.chartId.value==='only-chart');
a=acquisitionCase(({fiber,api})=>{fiber.memoizedProps={};fiber.child={stateNode:{api}};});check('approved direct child seam',a.result.ok&&a.calls===1);
a=acquisitionCase(({fiber})=>{fiber.memoizedProps={};});check('absence stage retained',a.result.stage==='grid-api-unavailable'&&!a.result.ok&&a.calls===0);
a=acquisitionCase(({fiber})=>{fiber.child={stateNode:{api:{getChartModels(){}}}};});check('distinct APIs rejected',a.result.stage==='grid-api-ambiguous'&&a.result.ambiguous&&a.calls===0);
a=acquisitionCase(({api})=>{api.getChartModels=()=>[];});check('zero model stage retained',a.result.stage==='model-count'&&a.result.modelCount===0&&a.calls===0);
a=acquisitionCase(({api})=>{api.getChartModels=()=>[{chartId:'a'},{chartId:'b'}];});check('multiple models rejected',a.result.stage==='model-count'&&a.result.modelCount===2&&a.calls===0);
a=acquisitionCase(({proxy})=>{proxy.chart=null;});check('missing proxy stage retains model identity',a.result.stage==='chart-proxy-unavailable'&&a.result.modelIdentity.chartId.value==='only-chart'&&a.calls===1);
a=acquisitionCase(({root,api})=>{let far={memoizedProps:{value:{gridRef:{current:{api}}}},return:null};for(let i=0;i<18;i++)far={memoizedProps:{},return:far};root.__reactFiber_test=far;});
check('eighteen ancestor ceiling',a.result.stage==='grid-api-unavailable'&&a.result.ancestry.length===18&&a.calls===0);
check('acquisition receipt before dependent assertion',journey.indexOf("status:'acquisition-observed'")<journey.indexOf("assert(acquired.ok"));
for(const [name,mutate] of [['broken chain',x=>x.series[0].chainValid=false],['zero bar',x=>x.series[0].nodes[0].fields.height=field(0)],
  ['unexpected plain translation',x=>x.series[0].transforms[1].translationX=field(0)],['DPR mismatch',x=>x.dpr=2],['scene mismatch',x=>x.scene.width=401],['active animation',x=>x.animationActive=true]]){
  const copy=structuredClone(g);mutate(copy);let rejected=false;try{coordinate(copy,0,'cashFlow','groupedColumn');}catch{rejected=true;}check('reject '+name,rejected);}
const plan=path.resolve(here,'../../plan.md');check('frozen source plan',hash(fs.readFileSync(plan))===planHash);
const files=fs.readdirSync(here).filter(n=>fs.statSync(here+'/'+n).isFile()).map(name=>({name,bytes:fs.statSync(here+'/'+name).size,sha256:hash(fs.readFileSync(here+'/'+name))}));
const result={scope:'offline collector preparation only',runtimeExecuted:false,checks,files,limits};
fs.writeFileSync(path.resolve(here,'../static-verification.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify({checks:checks.length,passed:checks.every(x=>x.passed),runtimeExecuted:false,files:files.length}));
