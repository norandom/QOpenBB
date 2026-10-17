import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const repo='/mnt/d/Source/QOpenBB';
const root=repo+'/artifacts/ui-parity-captions/capture';
const accepted='attempt-20261017T134459Z-3656a1b9';
const run=root+'/runs/'+accepted;
const read=p=>JSON.parse(fs.readFileSync(p));
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const checks=[];
const check=(name,value)=>checks.push({name,passed:!!value});
const state=n=>read(run+'/'+n).state;
const v=f=>f?.value;
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const roles=s=>[s.scene.title.node,s.scene.subtitle.node,...s.scene.axes.map(a=>a.titleCaption.node)];
const effective=s=>[s.effective.title,s.effective.subtitle,...s.effective.axes.map(a=>a.title)];
const ancestry=node=>node.parentLink.field==='parentNode'&&node.parentLink.present===true&&node.ancestors.length>0&&node.ancestors.length<=8&&node.ancestors.every(a=>a.fields.visible.kind==='value'&&typeof v(a.fields.visible)==='boolean'&&a.fields.opacity.kind==='value'&&Number.isFinite(v(a.fields.opacity)));
const attempts=['attempt-20261017T133416Z-88ca52a8','attempt-20261017T133623Z-00578185','attempt-20261017T133725Z-f4544eb6','attempt-20261017T133848Z-e6488b85',accepted];
for(const [i,name]of attempts.entries()){
  const dir=root+'/runs/'+name,m=read(dir+'/source-manifest.json');
  check('identity:'+name,m.source==='38dffc33389aca0e4a87e0e88d42f7067aa220df'&&m.image==='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f'&&m.candidate.revision==='ea02ec15956dee8d2c8a06825387a570757db12d'&&m.candidate.executed===false);
  for(const f of m.scripts)check('harness-hash:'+name+'/'+f.path,hash(dir+'/'+f.path)===f.sha256);
  const c=read(dir+'/cleanup-report.json');
  check('cleanup:'+name,c.containerAbsent&&c.stateAbsent&&c.credentialAbsent&&c.remainingOwnedState.length===0&&read(dir+'/browser-cleanup.json').closed&&read(dir+'/cleanup-status.json').exitCode===0);
  check('exit:'+name,read(dir+'/run-status.json').exitCode===(i<3?1:0));
}
check('incomplete-attempt-four-retained',fs.existsSync(root+'/runs/'+attempts[3]+'/verification-correction.json'));
const files=fs.readdirSync(run).filter(n=>/^\d{3}-.*\.json$/.test(n)).sort();
const expected=[['2024-Q1',100,20],['2024-Q2',120,25],['2024-Q3',140,30],['2024-Q4',160,40]];
check('100-snapshots',files.length===100);
for(const name of files){
  const s=state(name);
  check('ancestor-fields:'+name,roles(s).every(ancestry));
  check('stable:'+name,s.settled.animationActive===false&&s.settled.stableSamples===2&&s.settled.sampleSpacingMs>=100);
  check('fixture:'+name,same(s.data.effective.map(r=>[v(r.period.wrapper.value),v(r.values.revenue),v(r.values.operatingIncome)]),expected));
  check('snapshot-size:'+name,fs.statSync(run+'/'+name).size<=1048576);
}
const allOn=state('019-all-on.json');
const texts=['Financial performance','USD millions, 2024 quarters','Reporting quarter','USD millions'];
check('all-on-real-parent-visibility',roles(allOn).every((n,i)=>v(n.fields.text)===texts[i]&&v(n.fields.visible)===true&&n.ancestors.every(a=>v(a.fields.visible)===true&&v(a.fields.opacity)>0)));
const off=['021-disable-chart-title-after.json','025-disable-subtitle-after.json','029-disable-horizontal-axis-title-after.json','033-disable-vertical-axis-title-after.json'];
for(const [i,name]of off.entries()){
  const s=state(name);
  check('independent-off:'+name,effective(s).every((r,j)=>v(r.enabled)===(i!==j)&&v(r.text)===texts[j])&&roles(s).every((n,j)=>j===i?(v(n.fields.visible)===false||v(n.fields.text)===''):(v(n.fields.text)===texts[j]&&v(n.fields.visible)===true&&n.ancestors.every(a=>v(a.fields.visible)===true&&v(a.fields.opacity)>0))));
}
const ledger=read(run+'/action-ledger.json');
const weight=ledger.filter(x=>x.name.startsWith('weight-'));
check('47-actions-12-weight-selections-eight-roles',ledger.length===47&&weight.length===12&&new Set(weight.map(w=>w.input.control)).size===8);
for(const w of weight){
  const s=state(w.after),control=w.input.control,choice=w.input.choice;
  const expected={Normal:['normal','normal'],Bold:['bold','normal'],Italic:['normal','italic'],'Bold Italic':['bold','italic'],Predefined:[400,'normal']}[choice];
  let raw=[],eff=[],nodes=[];
  const caption={'Chart Title Weight':0,'Subtitle Weight':1,'Horizontal Axis Title Weight':2,'Vertical Axis Title Weight':3}[control];
  if(caption!==undefined){eff=[effective(s)[caption]];nodes=[roles(s)[caption]];
    raw=caption<2?[s.model.chartOptions.bar[caption===0?'title':'subtitle']]:Object.values(s.model.chartOptions.bar.axes[caption===2?'category':'number'].positions).filter(a=>a.title.fontWeight.kind==='value').map(a=>a.title);
  }else if(control==='Legend Weight'){raw=[s.model.chartOptions.bar.legendLabel];eff=[s.effective.legendLabel];nodes=s.scene.legend.labels;
  }else if(control==='Series Labels Weight'){raw=[s.model.chartOptions.bar.seriesLabel];eff=s.effective.series.map(a=>a.label);nodes=s.scene.series.flatMap(a=>a.labels);
  }else{const type=control.startsWith('Horizontal')?'category':'number';raw=Object.values(s.model.chartOptions.bar.axes[type].positions).filter(a=>a.label.fontWeight.kind==='value').map(a=>a.label);eff=s.effective.axes.filter(a=>v(a.identity.type)===type).map(a=>a.label);nodes=s.scene.axes.find(a=>v(a.identity.type)===type).labels;}
  check('weight-pair:'+w.name,raw.length>0&&eff.length>0&&nodes.length>0&&[...raw,...eff,...nodes.map(n=>n.fields)].every(f=>same([v(f.fontWeight),v(f.fontStyle)],expected))&&nodes.every(ancestry)&&w.eventCount===2);
}
const a=state('071-padding-left-13-after.json'),b=state('075-padding-left-67-after.json');
check('padding-swap-preserves-width-moves-x54',v(b.scene.seriesRect.width)===v(a.scene.seriesRect.width)&&v(b.scene.seriesRect.x)-v(a.scene.seriesRect.x)===54&&v(a.effective.padding.left)===13&&v(a.effective.padding.right)===67&&v(b.effective.padding.left)===67&&v(b.effective.padding.right)===13);
const end=state('100-final-all-on.json'),before=state('083-padding-restore-left-after.json');
check('retained-details',effective(end).every((r,i)=>v(r.text)===texts[i]&&same(r.fontWeight,effective(before)[i].fontWeight)&&same(r.fontStyle,effective(before)[i].fontStyle)));
check('predefined-explicit-style',v(state('045-weight-chart-title-predefined-after.json').model.chartOptions.bar.title.fontWeight)===400&&v(state('045-weight-chart-title-predefined-after.json').model.chartOptions.bar.title.fontStyle)==='normal'&&allOn.model.chartOptions.bar.title.fontStyle.kind==='absent');
const summary=read(run+'/summary.json');
check('bounded-case-counters',summary.completed&&summary.cases===9&&summary.interactions===164&&summary.edits===51&&summary.durationMs<900000&&read(run+'/cases.json').every(c=>c.completed));
const publication=root+'/publication-allowlist.json';
if(fs.existsSync(publication)){
  const allow=read(publication);
  for(const f of allow.files){const p=f.sourcePath||f.path;const full=p.startsWith('artifacts/')?repo+'/'+p:root+'/'+p;
    check('publication-safe:'+p,!/private|\.log$|\.env$|\/state-/.test(p)&&full.startsWith(root+'/'));
    check('publication-hash:'+p,hash(full)===f.sha256);
  }
  const report=fs.readFileSync(root+'/report.md','utf8');
  const selected=new Set(allow.files.map(f=>path.resolve(repo,f.sourcePath||f.path)));
  for(const match of report.matchAll(/\]\(([^)]+)\)/g)){
    const target=match[1].split('#')[0];if(/^[a-z]+:/.test(target))continue;
    const full=path.resolve(root,target);
    check('report-link-exists:'+target,fs.existsSync(full));
    if(full.startsWith(root+'/')&&full!==publication)check('report-link-published:'+target,selected.has(full));
  }
}
const result={scope:'Independent offline original caption evidence audit; no runtime replay',checkCount:checks.length,failed:checks.filter(c=>!c.passed),checks};
fs.writeFileSync(repo+'/artifacts/ui-parity-captions-review/verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({checks:checks.length,failed:result.failed}));
if(result.failed.length)process.exitCode=1;
