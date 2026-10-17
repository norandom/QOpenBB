import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const here=path.dirname(fileURLToPath(import.meta.url));
const repo=path.resolve(here,'../..');
const base=path.join(repo,'artifacts/ui-parity-tooltip-followup');
const capture=path.join(base,'capture');
const attempt=path.join(capture,'attempt-20261017-tooltip-followup-a1');
const sha=b=>createHash('sha256').update(b).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(p));
const checks=[];
function check(name,result){checks.push({name,passed:!!result});if(!result)throw Error(name);}
const allow=read(path.join(capture,'publication-allowlist.json'));
check('frozen report',sha(fs.readFileSync(path.join(capture,'report.md')))==='3a65389817de160b24557808dedd198a39a6b294870c198d51b46e70283555b6');
check('frozen allowlist',sha(fs.readFileSync(path.join(capture,'publication-allowlist.json')))==='99f7299909520b0c2fa35ac99da4c33dbf1d89d878620fc1e38584678d3e2871');
const scanned=[];
for(const f of allow.files){
  const b=fs.readFileSync(path.join(repo,f.path));
  check('selected byte identity '+f.path,b.length===f.bytes&&sha(b)===f.sha256);
  if(!f.path.endsWith('.png')){
    const s=b.toString('utf8');
    check('no concrete token/private-key pattern '+f.path,!/(?:sk-(?:proj-|ant-)?[A-Za-z0-9_-]{24,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|Bearer [A-Za-z0-9_.-]{24,})/.test(s));
    scanned.push(f.path);
  }
}
const cases=Array.from({length:8},(_,i)=>read(path.join(attempt,'T0'+(i+1)+'.json')));
const pointers=cases.flatMap(c=>c.probes);
const p=id=>pointers.find(x=>x.id===id);
const tip=x=>x.observation.pair.at(-1).tooltip;
const rows=id=>tip(p(id)).rows.map(r=>r.label+'='+r.value);
const labels=['Cash <&> flow (USD millions)','Operating Income (USD millions)','Revenue (USD millions)'];
const expected={
  'T01.p1':[[0,'-4.125']],'T01.p2':[[1,'27.625']],'T01.p3':[[2,'12.375']],
  'T02.p4':[[2,'27.625']],'T02.p5':[[1,'12.375']],'T02.p6':[[2,'12.375']],
  'T03.p7':[[0,'-7.125'],[1,'0']],'T03.p8':[[0,'0'],[1,'-3.375']],
  'T04.p9':[[0,'2.125'],[1,'7.125']],'T04.p10':[[0,'2.125'],[1,'7.125']],
  'T04.p11':[[0,'-4.125'],[1,'27.625'],[2,'12.375']],
  'T04.p12':[[0,'8.125'],[1,'12.375'],[2,'27.625']],
  'T05.p13':[[0,'-4.125']],'T05.p14':[[1,'27.625']],'T05.p15':[[2,'12.375']],
  'T05.p16':[[2,'27.625']],'T05.p17':[[2,'27.625']],
  'T07.p46':[[2,'7.125']],'T07.p47':[[0,'-4.125']],
  'T07.p48':[[0,'-7.125'],[1,'0']],'T07.p49':[[0,'0'],[1,'-3.375']],
  'T08.p50':[[0,'-4.125'],[1,'27.625'],[2,'12.375']],
  'T08.p51':[[0,'2.125'],[1,'7.125'],[2,'7.125']],'T08.p52':[[2,'27.625']]
};
for(const [id,values] of Object.entries(expected))check('actual rendered rows '+id,JSON.stringify(rows(id))===JSON.stringify(values.map(([i,v])=>labels[i]+'='+v)));
check('T03 prescribed fallback',p('T03.p7').key==='operatingIncome'&&p('T03.p7').target.yKey==='cashFlow'&&p('T03.p7').fallbackReason.startsWith('no-hittable-node'));
check('duplicate labels have distinct intended wrappers',p('T02.p4').target.wrapperId!==p('T02.p6').target.wrapperId);
check('T05 target differs from displayed amount',p('T05.p17').target.geometry.fields.yValue.value===7.125);
check('T08 target differs from displayed series and amount',p('T08.p52').target.yKey==='operatingIncome'&&p('T08.p52').target.geometry.fields.yValue.value===12.375);
for(const x of pointers){
  check('hover DOM pair equality '+x.id,x.observation.status==='stable'&&JSON.stringify(x.observation.pair[0])===JSON.stringify(x.observation.pair[1]));
  check('leave DOM pair equality and hidden '+x.id,x.leave.status==='stable'&&JSON.stringify(x.leave.pair[0])===JSON.stringify(x.leave.pair[1])&&x.leave.pair.at(-1).tooltip?.visible===false);
}
const keyboard=cases[5];
check('Single 24 actual settled Tabs outside series',keyboard.keyboard[0].tabs.length===24&&keyboard.keyboard[0].tabs.every(t=>t.state.status==='stable'&&!t.state.pair.at(-1).active.inSeriesArea));
check('Multiple partial 3 Tabs and Compact absent',keyboard.keyboard[1].tabs.length===3&&keyboard.keyboard[1].status==='seeking'&&keyboard.remainingModes[0].mode==='Compact'&&keyboard.remainingModes[0].status==='not-run-budget');
check('no arrow sequence',keyboard.keyboard.every(k=>k.keys.length===0));
check('27 emitted Tab ledger entries',keyboard.ledger.filter(e=>e.method==='key'&&e.argument==='Tab').length===27);
check('T06 final bytes and guard threshold',fs.statSync(path.join(attempt,'T06.json')).size===119493&&119493>131072-16000);
const preflight=read(path.join(attempt,'identity-fixture-preflight.json'));
for(const stage of ['options','effective']){
  check(stage+' explicit null preserved',preflight.admitted[stage].data[2].values.revenue.value===null);
  check(stage+' absent becomes own undefined',preflight.admitted[stage].data[3].values.revenue.own===true&&preflight.admitted[stage].data[3].values.revenue.kind==='undefined');
}
const ledger=cases.flatMap(c=>c.ledger);
const summary=read(path.join(attempt,'summary.json'));
check('128 actual inputs including nine setup',ledger.length+summary.setupActions===128&&summary.setupActions===9&&ledger.every(e=>e.status==='observed'));
check('24 pointer records',pointers.length===24);
check('exact two narrow column thumbnails',cases[7].thumbnails.length===2&&cases[7].thumbnails.map(t=>t.name).join('|')==='Grouped Column|Stacked Column');
const screenshots=allow.files.filter(f=>f.path.endsWith('.png'));
check('all 25 images selected',screenshots.length===25);
const result={date:'2026-10-17',scope:'Independent source/artifact review, no browser or build',passed:true,checks,selectedFiles:allow.files.length,textFilesScanned:scanned.length,screenshotsReviewed:screenshots.map(f=>({sourcePath:f.path,sha256:f.sha256,bytes:f.bytes})),visualReview:'All 25 original full images inspected individually; synthetic chart shell, no visible credentials/private account or provider data; rendered values agree with the case records.',upstreamVerifier:{exitCode:0,checks:506,sideEffect:'Rewrites capture/evidence-verification.json; does not launch runtime. Selected bytes unchanged.'}};
fs.writeFileSync(path.join(here,'verification.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({passed:true,checks:checks.length,selectedFiles:allow.files.length,textFilesScanned:scanned.length,screenshotsReviewed:screenshots.length}));
