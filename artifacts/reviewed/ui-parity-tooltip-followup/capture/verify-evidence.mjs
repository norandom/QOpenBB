import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const here=path.dirname(fileURLToPath(import.meta.url)),base=path.resolve(here,'..'),repo=path.resolve(base,'../..');
const attempt=here+'/attempt-20261017-tooltip-followup-a1',checks=[];
const sha=b=>createHash('sha256').update(b).digest('hex');
const check=(name,passed)=>{checks.push({name,passed:!!passed});if(!passed)throw Error(name);};
const read=n=>JSON.parse(fs.readFileSync(attempt+'/'+n+'.json'));
const allow=JSON.parse(fs.readFileSync(here+'/publication-allowlist.json'));
for(const f of allow.files){const resolved=path.resolve(repo,f.path);check('owned selection '+f.path,resolved.startsWith(base+'/'));
  const bytes=fs.readFileSync(resolved);check('selected bytes '+f.path,bytes.length===f.bytes&&sha(bytes)===f.sha256);
  check('selected path excludes private/logs '+f.path,!/private|credential|\.log$|fresh-verification\.json$/.test(f.path));}
const source=JSON.parse(fs.readFileSync(base+'/source-hashes.json'));
check('reviewed source unchanged',sha(fs.readFileSync(base+'/source-hashes.json'))==='3c8820b49ec8f694e2e46c212d2d3ebc217be4700c7c44288310a0e7b0ae87c7');
check('reviewed plan unchanged',sha(fs.readFileSync(base+'/plan.md'))==='95c7f4384c6c25ea48e99859126e03713c14f09645ed75adbba0e657abf2dbdd');
const manifestBytes=fs.readFileSync(attempt+'/static-verification.json'),manifest=JSON.parse(manifestBytes),proof=read('executed-source-verification');
check('executed frozen manifest',sha(manifestBytes)==='31c23562ec901872025a66c7a0bc275e722b938e3e1a715305a830f868628530'&&proof.passed&&proof.files.length===12);
for(const f of manifest.files)check('executed source '+f.name,sha(fs.readFileSync(attempt+'/harness/'+f.name))===f.sha256&&proof.files.some(p=>p.name===f.name&&p.sha256===f.sha256&&p.expectedSha256===f.sha256));
for(const f of proof.support)check('copied support '+f.name,sha(fs.readFileSync(attempt+'/verification-support/'+f.name))===f.sha256&&source.support.some(p=>p.path.endsWith('/'+f.name)&&p.sha256===f.sha256));
check('copied static import support',sha(fs.readFileSync(attempt+'/followup-static.mjs'))===proof.support.find(f=>f.name==='followup-static.mjs').sha256);
const summary=read('summary'),fixture=JSON.parse(fs.readFileSync(attempt+'/harness/fixture.json'));
check('original only',summary.source===source.original&&summary.image===source.image&&summary.candidateExecuted===false);
check('fixture identity',summary.fixtureHash===source.fixtureCanonicalSha256&&fixture.rows.length===5);
let hover=0,leave=0,pointers=0,tabs=0,total=0;const rows=[];
for(let i=1;i<=8;i++){const c=read('T0'+i);check('case cap '+c.id,fs.statSync(attempt+'/'+c.id+'.json').size<=131072&&c.actions<=(i===6?120:36));
  check('case ledger '+c.id,c.ledger.length===c.actions);total+=c.actions;
  for(const e of c.ledger){if(e.method==='move'){if(e.label.startsWith('Hover '))hover++;if(e.label==='Leave canvas')leave++;}if(e.label==='Tab traversal')tabs++;}
  for(const p of c.probes){pointers++;check('stable samples '+p.id,p.status==='stable'&&p.settlement.pair.length===2&&JSON.stringify(p.settlement.pair[0])===JSON.stringify(p.settlement.pair[1]));
    const g=p.settlement.pair[1];check('all required node/link kinds '+p.id,g.animationActive===false&&g.series.every(s=>s.chainValid&&s.terminalValid&&Object.values(s.nodePresence).every(Boolean)&&Object.values(s.nodeKinds).every(k=>k==='object')&&Object.values(s.links).every(Boolean)));
    const t=p.observation.pair.at(-1).tooltip;rows.push({case:c.id,id:p.id,ordinal:p.ordinal,requested:p.key,target:p.target.yKey,wrapper:p.target.wrapperId,
      targetYValue:p.target.geometry.fields.yValue?.value,point:p.target.point,status:p.status,rows:t?.rows,heading:t?.heading,pagination:t?.pagination,image:p.image,
      leaveVisible:p.leave?.pair.at(-1)?.tooltip?.visible??null,settledPair:p.settlement?.pair.length===2});}}
check('24 actual hover and leave moves',hover===24&&leave===24&&pointers===24);check('27 actual Tabs',tabs===27);
check('total input accounting',total+summary.setupActions===summary.actions&&summary.actions===128&&summary.probes===52&&summary.probes<=96);
check('derived observations exact',JSON.stringify(rows)===JSON.stringify(JSON.parse(fs.readFileSync(here+'/observations.json')).observations));
const keyboard=read('T06');check('keyboard limits retained',keyboard.status==='not-run-budget'&&keyboard.keyboard[0].tabs.length===24&&keyboard.keyboard[0].status==='keyboard-unreachable-within-bound'&&keyboard.keyboard[1].tabs.length===3&&keyboard.remainingModes[0].mode==='Compact');
const compact=rows.find(p=>p.id==='T05.p17'),stacked=rows.find(p=>p.id==='T08.p52');
check('grouped Compact discrepancy retained',compact.target==='revenue'&&compact.targetYValue===7.125&&compact.rows[0].label==='Revenue (USD millions)'&&compact.rows[0].value==='27.625');
check('stacked Compact discrepancy retained',stacked.target==='operatingIncome'&&stacked.targetYValue===12.375&&stacked.rows[0].label==='Revenue (USD millions)'&&stacked.rows[0].value==='27.625');
const pngs=fs.readdirSync(attempt).filter(n=>n.endsWith('.png'));check('25 PNG count',pngs.length===25&&summary.shots===25);
for(const n of pngs){const b=fs.readFileSync(attempt+'/'+n);check('PNG dimensions/cap '+n,b.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10]))&&b.readUInt32BE(16)===1440&&b.readUInt32BE(20)===1000&&b.length<=2097152);}
const flat=fs.readdirSync(attempt).filter(n=>fs.statSync(attempt+'/'+n).isFile());
const sum=names=>names.reduce((n,f)=>n+fs.statSync(attempt+'/'+f).size,0);
check('all root JSON within cap',sum(flat.filter(f=>f.endsWith('.json')))<=2097152);check('root output within cap',sum(flat)<=104857600);
const absence=read('owned-absence-verification'),cleanup=read('cleanup-report'),browser=read('browser-cleanup');
check('fresh recorded owned absence',absence.passed&&absence.containerAbsent&&absence.stateAbsent&&absence.credentialAbsent&&absence.browserProcessAbsent&&absence.supervisorProcessAbsent);
check('recorded nested cleanup',browser.contextClosed&&browser.closed&&browser.serverClosed&&cleanup.remainingOwnedState.length===0&&cleanup.browserAbsent);
check('wrapper/frozen verifier exits',read('run-status').exitCode===0&&read('fresh-verification-public').failures.length===0);
for(const doc of ['plan.md','capture/report.md'])for(const [,target] of fs.readFileSync(base+'/'+doc,'utf8').matchAll(/\[[^\]]+\]\(([^)]+)\)/g)){
  const current=path.resolve(base,path.dirname(doc),target),final=path.resolve(repo,'artifacts/reviewed/ui-parity-tooltip-followup',path.dirname(doc),target);
  const proposed=path.resolve(repo,'artifacts/reviewed/ui-parity-tooltip-followup');
  check('local link '+doc+' '+target,fs.existsSync(current));check('publication-depth link '+doc+' '+target,fs.existsSync(final.startsWith(proposed+'/')?current:final));}
const result={scope:'Fresh selected-byte and finite runtime evidence audit; not invocation or parity acceptance',checks,passed:true,selectedFiles:allow.files.length,
  actualHoverInputs:hover,actualLeaveInputs:leave,actualTabs:tabs,pointerRecords:pointers,pngs:pngs.length,
  allowlistSha256:sha(fs.readFileSync(here+'/publication-allowlist.json'))};
fs.writeFileSync(here+'/evidence-verification.json',JSON.stringify(result,null,2));
console.log(JSON.stringify({checks:checks.length,passed:true,selectedFiles:allow.files.length,actualHoverInputs:hover,pngs:pngs.length,allowlistSha256:result.allowlistSha256}));
