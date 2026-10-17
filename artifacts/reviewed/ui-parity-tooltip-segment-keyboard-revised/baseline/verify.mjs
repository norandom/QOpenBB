import fs from 'node:fs';
import path from 'node:path';
import {limits,source,image,fixtureHash,hash} from './contract.mjs';
const attempt=process.argv[2];if(!attempt)throw Error('Attempt path required');
const checks=[];const check=(name,passed)=>checks.push({name,passed:!!passed});
const read=n=>JSON.parse(fs.readFileSync(path.join(attempt,n+'.json')));
let total=0,jsonBytes=0,pngs=0;const files=[];
for(const name of fs.readdirSync(attempt)){const file=path.join(attempt,name);if(!fs.statSync(file).isFile())continue;
  const bytes=fs.readFileSync(file);total+=bytes.length;if(name.endsWith('.json'))jsonBytes+=bytes.length;
  if(name.endsWith('.png')){pngs++;check('PNG cap '+name,bytes.length<=limits.pngBytes);}
  if(/^T0[1-8]\.json$/.test(name))check('Case cap '+name,bytes.length<=limits.caseBytes);
  files.push({name,bytes:bytes.length,sha256:hash(bytes)});
}
check('JSON retained cap',jsonBytes<=limits.jsonBytes);check('Run retained cap',total<=limits.runBytes);check('PNG count',pngs<=limits.screenshots);
check('No credential file',!fs.existsSync(path.join(attempt,'credential-private.json')));
const preflight=read('identity-fixture-preflight');check('Pinned original',preflight.source===source&&preflight.image===image);check('Fixture',preflight.fixtureHash===fixtureHash);
const summary=read('summary');check('Eight cases',summary.results.map(c=>c.id).join(',')==='T01,T02,T03,T04,T05,T06,T07,T08');
check('Input actions',summary.actions<=limits.totalActions&&summary.setupActions<=limits.setupActions);check('Probes',summary.probes<=limits.probes);check('Screenshots',summary.shots<=limits.screenshots);
for(let i=1;i<=8;i++){const id='T0'+i,c=read(id);check('Case action cap '+id,c.actions<=(i===6?limits.keyboardActions:limits.caseActions));
  check('Case ledger '+id,c.ledger.length===c.actions);check('Case time '+id,c.elapsedMs<=(i===6?limits.keyboardMs:limits.caseMs)+limits.selectorMs);
  for(const p of c.probes){if(p.target)check('Settlement before pointer '+p.id,p.settlement.pair.length===2&&p.settlement.pair.every(s=>s.animationActive===false)&&JSON.stringify(p.settlement.pair[0])===JSON.stringify(p.settlement.pair[1]));}}
const cleanup=read('cleanup-report');check('Owned cleanup',cleanup.containerAbsent&&cleanup.stateAbsent&&cleanup.credentialAbsent&&cleanup.remainingOwnedState.length===0);
check('Browser process absent',cleanup.browserAbsent);const browser=read('browser-cleanup');
check('Browser/context/server close',browser.closed&&browser.contextClosed&&browser.serverClosed);check('Run exit',read('run-status').exitCode===0);
const report={scope:'Fresh bounded original capture verification; unresolved case outcomes remain unresolved',checks,failures:checks.filter(c=>!c.passed),files,totalBytes:total,jsonBytes,pngs};
fs.writeFileSync(path.join(attempt,'fresh-verification.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({checks:checks.length,failures:report.failures}));
if(report.failures.length)process.exitCode=1;
