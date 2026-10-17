import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const root=path.dirname(new URL(import.meta.url).pathname);
const read=name=>JSON.parse(fs.readFileSync(root+'/'+name));
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const checks=[];
function check(name,value){checks.push({name,passed:!!value});}
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const run='run-20261017-r1-a4';
const state=name=>read(run+'/'+name+'.json');
const manifest=read('source-manifest.json');
for(const file of manifest.files)check('file-hash:'+file.path,sha(fs.readFileSync(root+'/'+file.path))===file.sha256);
for(const source of manifest.source)check('original-source:'+source.path,sha(execFileSync('git',[
  '-C','/mnt/d/Source/QOpenBB/vendor/workspace','show',source.revision+':'+source.path],{maxBuffer:4*1024*1024}))===source.sha256);
check('original-identity',manifest.original==='38dffc33389aca0e4a87e0e88d42f7067aa220df'&&
  manifest.image==='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f'&&!manifest.candidateExecuted);
for(let number=1;number<=4;number++){
  const dir='run-20261017-r1-a'+number;
  for(const name of ['containerAbsent','stateAbsent','credentialAbsent'])check(dir+':'+name,read(dir+'/cleanup-report.json')[name]===true);
  check(dir+':no-owned-state',read(dir+'/cleanup-report.json').remainingOwnedState.length===0);
  check(dir+':browser-closed',read(dir+'/browser-cleanup.json').browserClosed===true);
  check(dir+':runtime-exit',read(dir+'/run-status.json').exitCode===(number===4?0:1));
  check(dir+':cleanup-exit',read(dir+'/cleanup-status.json').exitCode===0);
  check(dir+':fixture-identical',sha(fs.readFileSync(root+'/'+dir+'/fixture.json'))==='2de20cebe2674659947f11fecb7497dc5d67fdd740f1c1443f0f746db8ceea30');
}
const cases=read(run+'/cases.json');
check('exact-twelve-cases',same(cases.map(item=>item.id),Array.from({length:12},(_,index)=>'N'+String(index+1).padStart(2,'0'))));
check('case-deadlines',cases.every(item=>item.status==='observed'&&item.elapsedMs<30000));
const checkpoints=read(run+'/checkpoints.json');
check('36-checkpoints',checkpoints.length===36);
const expected=[['2024-Q1',100,20],['2024-Q2',120,25],['2024-Q3',140,30],['2024-Q4',160,40]];
const rootFields=['chartSettingsOpen','chartType','totalSeries','isPivotMode','chartView','chartOptions','chartModel','partitions'];
for(const checkpoint of checkpoints){
  const s=state(checkpoint.name),name=checkpoint.name;
  check(name+':source-values',same(s.sourceRows.map(row=>[row.period,row.revenue,row.operatingIncome]),expected));
  check(name+':root-field-allowlist',same(Object.keys(s.rootStorage),rootFields));
  check(name+':projection-no-budget-overflow',s.budget.paths<=2048&&s.budget.focusOverflow===0&&s.budget.chartEventOverflow===0&&
    s.budget.omittedCount===s.budget.omitted.length&&s.budget.omitted.every(item=>['non-plain-function','non-plain-object'].includes(item.reason)));
  check(name+':bounded-focus-log',s.dom.focusEvents.length<=512);
  if(s.chart){
    check(name+':chart-resolved-range',same(s.chart.model.cellRange.columns,['period','revenue','operatingIncome'])&&
      s.chart.model.cellRange.rowStartIndex===null&&s.chart.model.cellRange.rowEndIndex===null);
    check(name+':resolved-chart-values',same(s.chart.effective.data.map(row=>[row.period?.value??row.period,row.revenue,row.operatingIncome]),expected));
    check(name+':ordered-financial-bindings',same(s.chart.effective.series.map(series=>[series.xKey,series.yKey]),
      [['period','revenue'],['period','operatingIncome']]));
    check(name+':settled-chart',s.chart.animationActive===false);
  }
  const png=fs.readFileSync(root+'/'+run+'/'+name+'.png');
  check(name+':png-signature',png.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])));
  check(name+':png-viewport',png.readUInt32BE(16)===1440&&png.readUInt32BE(20)===1000);
}
const expanded=(s,label)=>s.dom.headings.find(item=>item.label===label)?.expanded;
const scrolled=s=>s.dom.scroll.find(item=>item.scrollTop>0);
const entered=state('N01-chart-entered'),prepared=state('N03-pre-close'),closed=state('N03-closed'),reopened=state('N04-reopened');
check('click-shift-click-original-clears',state('N01-click-selection-observed').table.ranges.length===0);
check('real-drag-selection-created',state('N01-table-pre-entry').table.ranges.length===1&&read(run+'/selection-discriminator.json').resolved);
check('selection-rows-columns',same(state('N01-table-pre-entry').table.ranges[0],{startRow:{rowIndex:1,rowPinned:null},
  endRow:{rowIndex:2,rowPinned:null},columns:['revenue','operatingIncome']}));
check('resize-281-to-347',state('N01-table-initial').columnState[1].width===281&&state('N01-table-pre-entry').columnState[1].width===347);
check('grid-lines-control-preserved',prepared.dom.controls.filter(item=>item.label==='Grid Lines').every(item=>item.checked===true));
check('customize-prepared-expanded-scrolled',expanded(prepared,'Vertical Axis')==='true'&&scrolled(prepared)?.scrollTop===547&&prepared.dom.active.label==='Thickness');
check('dock-close-flag-and-menu',prepared.rootStorage.chartSettingsOpen.value===true&&closed.rootStorage.chartSettingsOpen.value===false&&!closed.dom.menuVisible);
check('dock-close-focus-body',closed.dom.active.tag==='BODY');
check('reopen-same-panel-chart',prepared.dom.panel.node===reopened.dom.panel.node&&prepared.dom.chartNode===reopened.dom.chartNode);
check('reopen-group-scroll-retained',expanded(reopened,'Vertical Axis')==='true'&&scrolled(reopened)?.scrollTop===547&&scrolled(prepared).node===scrolled(reopened).node);
check('reopen-focus-customize-tab',reopened.dom.active.role==='tab'&&reopened.dom.active.label==='Customize');
check('setup-focus-no-transform',state('N05-pre-close').dom.active.label==='Aggregate'&&
  state('N05-pre-close').dom.active.checked===false&&state('N05-reopened').dom.active.label==='Set Up');
check('chart-thumbnail-focus-then-tab',state('N06-pre-close').dom.active.label==='Grouped Column. Selected'&&state('N06-reopened').dom.active.label==='Chart');
const beforeLight=state('N07-dark-pre'),light=state('N07-light'),dark=state('N08-dark');
check('dark-light-dark-theme',beforeLight.dom.dark&&!light.dom.dark&&dark.dom.dark&&
  light.chart.model.chartThemeName==='openbb-light'&&dark.chart.model.chartThemeName==='openbb-dark');
check('theme-preserves-chart-panel-owner',beforeLight.dom.panel.node===light.dom.panel.node&&beforeLight.dom.chartNode===light.dom.chartNode&&
  beforeLight.chart.model.chartId===light.chart.model.chartId);
check('theme-resets-customize-groups',expanded(beforeLight,'Vertical Axis')==='true'&&light.dom.headings.every(item=>item.expanded==='false')&&
  dark.dom.headings.every(item=>item.expanded==='false'));
check('theme-rebuilds-fields-removes-overflow-focus',beforeLight.dom.active.tag==='INPUT'&&light.dom.active.tag==='BODY'&&light.dom.scroll.length===0&&
  beforeLight.dom.headings.at(-1).node!==light.dom.headings.at(-1).node);
check('theme-read-model-vs-stored-model',light.chart.model.chartThemeName==='openbb-light'&&
  light.rootStorage.partitions[0].chartModel.chartThemeName==='openbb-dark');
check('no-root-chartOptions-write',checkpoints.every(checkpoint=>state(checkpoint.name).rootStorage.chartOptions.own===false));
const line=state('N09-line-Customize'),column=state('N10-column-Customize');
check('family-column-line-column',entered.chart.model.chartType==='groupedColumn'&&line.chart.model.chartType==='line'&&column.chart.model.chartType==='groupedColumn');
check('family-preserves-chart-owner',entered.chart.model.chartId===line.chart.model.chartId&&entered.dom.chartNode===line.dom.chartNode&&line.dom.panel.node===column.dom.panel.node);
check('family-resets-customize-groups',line.dom.headings.every(item=>item.expanded==='false')&&column.dom.headings.every(item=>item.expanded==='false'));
const table=state('N11-table-stable'),reentry=state('N12-chart-untouched');
check('table-widths-restored',read(run+'/table-width-comparison.json').equal===true&&same(table.columnState,state('N01-table-pre-entry').columnState));
check('table-horizontal-scroll65-retained',same(table.table.state.scroll,{top:0,left:65})&&
  same(table.table.state.scroll,state('N01-table-pre-entry').table.state.scroll)&&!state('N01-table-initial').table.state.scroll);
check('table-selection-cleared-chart-destroyed',table.table.ranges.length===0&&table.chart===null&&table.dom.chartNode===null);
check('table-stored-settings-remain-open',table.rootStorage.chartSettingsOpen.value===true&&table.rootStorage.chartView.value.enabled===false);
check('reentry-new-chart-panel',reentry.chart.model.chartId!==entered.chart.model.chartId&&reentry.dom.panel.node!==prepared.dom.panel.node&&
  reentry.dom.chartNode!==entered.dom.chartNode);
check('reentry-auto-open-default-chart-focus',reentry.dom.menuVisible&&reentry.rootStorage.chartSettingsOpen.value===true&&reentry.dom.active.label==='Chart'&&
  reentry.dom.scroll.length===1&&reentry.dom.scroll[0].scrollTop===0);
const actions=read(run+'/action-ledger.json');
check('real-ui-ledger',actions.every(item=>item.kind==='original-application-real-ui'));
check('exact-two-family-two-theme-ui-actions',actions.filter(item=>item.label.startsWith('family-')).length===2&&actions.filter(item=>item.label.startsWith('theme-')).length===2);
check('no-transform-or-grid-lines-activation',!actions.some(item=>/toggle|check|fill|transform/i.test(item.label)));
const diagnostics=read(run+'/diagnostics.json');
check('diagnostics-bounded',diagnostics.overflow===0&&diagnostics.events.length<=2048);
check('no-blocked-external-or-network-failure',!diagnostics.events.some(item=>['blocked-external','cdp-network-failed'].includes(item.kind)));
check('known-datafeed-exceptions-retained',diagnostics.events.filter(item=>item.kind==='pageerror').length===2&&
  diagnostics.events.filter(item=>item.kind==='cdp-exception').length===2);
check('known-light-theme-warning-retained',diagnostics.events.some(item=>item.kind==='console'&&item.text.includes('openbb-light')&&item.text.includes('error #139')));
const allowlist=read('publication-allowlist.json');
check('publication-no-private-paths',allowlist.files.every(file=>!/runtime-private|credential-private|\.log$|\.env$|\/state-/.test(file.path)));
const failed=checks.filter(item=>!item.passed);
const result={recordedAt:new Date().toISOString(),status:failed.length?'FAIL':'PASS',checkCount:checks.length,failedCount:failed.length,
  scope:'Recorded original navigation evidence only; no candidate/persistence/export/release acceptance',checks};
fs.writeFileSync(root+'/verification.json',JSON.stringify(result,null,2));
allowlist.files=allowlist.files.filter(file=>file.path!=='verification.json');
allowlist.files.push({path:'verification.json',sha256:sha(fs.readFileSync(root+'/verification.json')),sanitization:'None; offline verification result'});
fs.writeFileSync(root+'/publication-allowlist.json',JSON.stringify(allowlist,null,2));
console.log(JSON.stringify({status:result.status,checkCount:checks.length,failed}));
if(failed.length)process.exitCode=1;
