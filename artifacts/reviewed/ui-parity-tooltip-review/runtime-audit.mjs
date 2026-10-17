import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const base='artifacts/ui-parity-tooltip-plan/capture',review='artifacts/ui-parity-tooltip-review';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,''));
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const checks=[];const check=(name,passed)=>checks.push({name,passed:!!passed});
const allow=read(base+'/publication-allowlist.json');
const selected=new Set(allow.files.map(f=>f.path));
for(const f of allow.files){
  check('hash '+f.path,hash(f.path)===f.sha256);
  check('bytes '+f.path,fs.statSync(f.path).size===f.bytes);
  check('safe path '+f.path,f.path.startsWith(base+'/')&&!/private|\.log$|\/state-|node_modules|\.env(?:\.|$)/i.test(f.path));
  if(f.path.endsWith('.json'))check('no credential material '+f.path,!/Bearer\s+[A-Za-z0-9._-]{12,}|eyJ[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\./.test(fs.readFileSync(f.path,'utf8')));
}
check('78 exact files',allow.files.length===78&&selected.size===78);
let links=0;
for(const m of fs.readFileSync(base+'/report.md','utf8').matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){
  if(/^(https?:|#)/.test(m[1]))continue;links++;
  check('report link '+m[1],selected.has(path.posix.normalize(base+'/'+m[1].split('#')[0])));
}
for(const [id,pin] of [['a1','53487962b319998a928a18fb4a323a41106f47a88a6ab6792f2b54a3f9de041a'],['a2','c098553db7a38c72eafec8ab0fc3a7e06c41ce74396f9062e44c794b8f6cb123']]){
  const root=base+'/attempt-20261017-r4-'+id;
  check(id+' executed manifest',hash(root+'/static-verification.json')===pin);
  for(const f of read(root+'/static-verification.json').files)check(id+' executed '+f.name,hash(root+'/harness/'+f.name)===f.sha256);
  const absence=read(root+'/owned-absence-verification.json');
  check(id+' owned absence',absence.passed&&['containerAbsent','stateAbsent','credentialAbsent','browserProcessAbsent','supervisorProcessAbsent'].every(k=>absence[k]===true));
}
const root=base+'/attempt-20261017-r4-a2',summary=read(root+'/summary.json'),admission=read(root+'/identity-fixture-preflight.json');
check('eight unresolved',summary.results.length===8&&summary.results.every(c=>c.status==='unresolved'));
check('bounded accounting',summary.actions===64&&summary.setupActions===9&&summary.probes===28&&summary.shots===1&&summary.candidateExecuted===false);
check('ready bounded acquisition',admission.acquired.ok&&admission.acquired.stage==='ready'&&admission.acquired.ancestry.length===18&&admission.acquired.candidateCount===1&&!admission.acquired.ambiguous&&admission.acquired.modelCount===1);
const expected=[[-4.125,27.625,12.375],[8.125,12.375,27.625],[-7.125,0,null],[0,-3.375,undefined],[2.125,7.125,7.125]];
const periods=['2024-Q1','2024-Q1','2024-Q2','2024-Q3','2024-Q4'];
for(const stage of ['options','effective']){
  const rows=admission.admitted[stage].data;check(stage+' five rows',rows.length===5);
  for(let i=0;i<5;i++){
    check(stage+' wrapper '+i,rows[i].period.id.value===i&&rows[i].period.value.value===periods[i]);
    for(const [j,key] of ['cashFlow','operatingIncome','revenue'].entries())check(stage+' value '+i+' '+key,rows[i].values[key].value===expected[i][j]);
  }
  check(stage+' missing remains undefined',rows[3].values.revenue.own&&rows[3].values.revenue.kind==='undefined');
  check(stage+' explicit null remains null',rows[2].values.revenue.kind==='null');
}
let pointerInputs=0,caseActions=0;
for(let i=1;i<=8;i++){
  const id='T0'+i,c=read(root+'/'+id+'.json');caseActions+=c.ledger.length;
  pointerInputs+=c.ledger.filter(a=>/hover|pointer|mouse/i.test(a.label??'')).length;
  check(id+' unresolved',c.status==='unresolved');
  check(id+' finite case',fs.statSync(root+'/'+id+'.json').size<=131072&&c.actions<=c.actionCap&&c.elapsedMs<=c.timeCap);
  if([1,2,4,7].includes(i)){
    const p=c.probes[0],pair=p.settlement.pair;
    check(id+' no coordinate emitted',p.status==='coordinate-unresolved'&&!('coordinate'in p));
    check(id+' inactive equal pair',pair.length===2&&!pair[0].animationActive&&!pair[1].animationActive&&JSON.stringify(pair[0])===JSON.stringify(pair[1]));
    check(id+' nonvacuous false chain',pair.every(s=>s.series.length===3&&s.series.every(r=>r.chainValid===false)));
  }
  if([3,5].includes(i))check(id+' stopped before mode click',c.ledger.map(a=>a.label).join('|')==='Customize|Expand Series');
}
check('no pointer input',pointerInputs===0);
check('all 64 actions accounted',caseActions+summary.setupActions===summary.actions);
const keyboard=read(root+'/T06.json').keyboard[0];
check('Single only keyboard',keyboard.mode==='Single'&&keyboard.status==='keyboard-unreachable-within-bound'&&keyboard.tabs.length===24&&keyboard.keys.length===0);
check('24 settled outside series area',keyboard.tabs.every(t=>t.state.status==='stable'&&t.state.pair.length===2&&t.state.pair.every(s=>s.active?.inSeriesArea===false)));
check('T08 stopped before selection',read(root+'/T08.json').reason==='Thumbnail bound 32'&&read(root+'/T08.json').ledger.length===1);
const result={scope:'Unresolved tooltip research and safe publication; no invocation acceptance',checkCount:checks.length,links,selectedFiles:allow.files.length,failed:checks.filter(c=>!c.passed),checks};
fs.writeFileSync(review+'/runtime-verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({checkCount:checks.length,links,selectedFiles:allow.files.length,failed:result.failed}));
if(result.failed.length)process.exitCode=1;
