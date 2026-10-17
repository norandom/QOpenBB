import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const repo='/mnt/d/Source/QOpenBB';
const root=repo+'/artifacts/ui-parity-navigation';
const out=repo+'/artifacts/ui-parity-navigation-review';
const read=p=>JSON.parse(fs.readFileSync(p));
const sha=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const checks=[];
const check=(name,value)=>checks.push({name,passed:!!value});
const manifest=read(root+'/source-manifest.json');
const allowlist=read(root+'/publication-allowlist.json');
for(const file of allowlist.files){
  const resolved=path.resolve(root,file.path);
  check('safe-path:'+file.path,resolved.startsWith(root+'/')&&!/private|\.log$|\.env$|\/state-/.test(file.path));
  check('publication-hash:'+file.path,sha(resolved)===file.sha256);
}
for(const source of manifest.source){
  const bytes=execFileSync('git',['-C',repo+'/'+source.repository,'show',source.revision+':'+source.path],{maxBuffer:4*1024*1024});
  check('source-hash:'+source.path,createHash('sha256').update(bytes).digest('hex')===source.sha256);
}
check('identities',manifest.original==='38dffc33389aca0e4a87e0e88d42f7067aa220df'&&manifest.image==='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f'&&manifest.candidateSource==='ea02ec15956dee8d2c8a06825387a570757db12d'&&manifest.candidateExecuted===false);
for(let n=1;n<=4;n++){
  const dir=root+'/run-20261017-r1-a'+n;
  const cleanup=read(dir+'/cleanup-report.json');
  check('cleanup:'+n,cleanup.containerAbsent&&cleanup.stateAbsent&&cleanup.credentialAbsent&&cleanup.remainingOwnedState.length===0&&read(dir+'/browser-cleanup.json').browserClosed===true&&read(dir+'/cleanup-status.json').exitCode===0);
  check('attempt-exit:'+n,read(dir+'/run-status.json').exitCode===(n===4?0:1));
  if(n<4)check('failure-retained:'+n,typeof read(dir+'/failure.json').error==='string');
}
const run=root+'/run-20261017-r1-a4';
const state=n=>read(run+'/'+n+'.json');
const checkpoints=read(run+'/checkpoints.json');
const cases=read(run+'/cases.json');
check('12-ordered-cases',cases.length===12&&cases.every((c,i)=>c.id==='N'+String(i+1).padStart(2,'0')&&c.status==='observed'&&c.elapsedMs<3000));
check('36-checkpoints',checkpoints.length===36);
const expected=JSON.stringify([['2024-Q1',100,20],['2024-Q2',120,25],['2024-Q3',140,30],['2024-Q4',160,40]]);
for(const c of checkpoints){
  const s=state(c.name),b=s.budget;
  check('source-values:'+c.name,JSON.stringify(s.sourceRows.map(r=>[r.period,r.revenue,r.operatingIncome]))===expected);
  check('budget-complete:'+c.name,b.omittedCount===b.omitted.length&&b.omittedCount<=46&&b.paths<=429&&b.focusOverflow===0&&b.chartEventOverflow===0&&b.omitted.every(o=>['non-plain-function','non-plain-object'].includes(o.reason)));
  check('tabs-honestly-absent:'+c.name,s.dom.tabs.every(t=>t.selected===null));
  if(s.chart)check('actual-full-resolved-data:'+c.name,JSON.stringify(s.chart.effective.data.map(r=>[r.period?.value??r.period,r.revenue,r.operatingIncome]))===expected);
}
const before=state('N01-table-pre-entry'),after=state('N11-table-stable');
check('selection-discriminator',state('N01-click-selection-observed').table.ranges.length===0&&JSON.stringify(before.table.ranges)==='[{"startRow":{"rowIndex":1,"rowPinned":null},"endRow":{"rowIndex":2,"rowPinned":null},"columns":["revenue","operatingIncome"]}]');
check('width-scroll-restoration',JSON.stringify(before.columnState)===JSON.stringify(after.columnState)&&JSON.stringify(before.table.state.scroll)===JSON.stringify(after.table.state.scroll)&&after.table.state.scroll.left===65&&after.table.ranges.length===0);
const closePre=state('N03-pre-close'),reopened=state('N04-reopened');
check('dock-scroll-and-focus',closePre.dom.scroll[0].scrollTop===547&&reopened.dom.scroll[0].scrollTop===547&&closePre.dom.panel.node===reopened.dom.panel.node&&reopened.dom.active.label==='Customize');
check('direct-theme-observed',state('N07-dark-pre').dom.active.tag==='INPUT'&&state('N07-light').chart.model.chartThemeName==='openbb-light'&&state('N07-light').dom.active.tag==='BODY'&&state('N08-dark').chart.model.chartThemeName==='openbb-dark');
check('new-chart-reentry',state('N12-chart-untouched').chart.model.chartId!==state('N01-chart-entered').chart.model.chartId&&state('N12-chart-untouched').dom.active.label==='Chart');
const result={scope:'Independent offline audit; no runtime replay or candidate acceptance',checkCount:checks.length,failed:checks.filter(c=>!c.passed),checks};
fs.writeFileSync(out+'/verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({checks:checks.length,failed:result.failed}));
if(result.failed.length)process.exitCode=1;
