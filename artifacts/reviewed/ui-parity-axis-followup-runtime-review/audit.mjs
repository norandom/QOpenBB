import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const own=path.dirname(fileURLToPath(import.meta.url)),repo=path.resolve(own,'../..');
const base=path.join(repo,'artifacts/ui-parity-axis-followup');
const attempt=path.join(base,'attempt-20261017T1449392-91e1b733');
const derived=path.join(base,'analysis-attempt-20261017T1449392-91e1b733');
const read=f=>JSON.parse(fs.readFileSync(f)),sha=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const checks=[],issues=[];
function check(value,label){checks.push({label,passed:!!value});if(!value)issues.push(label);}
const expected={'report.md':'60615c4ef08d02b568580e46974f6f8c125a35919c535c351163cf686fa8f2d3','publication-allowlist.json':'09bd912e8d207bbdc66aa8db2b1217ae26767f1ad630ac26086f5ce36583ede7','verify-runtime.mjs':'1e40252d0a9643613870afa1b4a7eb752c0a5987a08f0121cdbded1742ad8d81'};
for(const [f,h]of Object.entries(expected))check(sha(path.join(base,f))===h,'frozen identity '+f);
const allow=read(path.join(base,'publication-allowlist.json')),destinations=new Set();
const safetyMatches=[];
for(const f of allow.files){
  const source=path.resolve(repo,f.source),dest=path.resolve(repo,'artifacts/reviewed',f.destination);
  check(source.startsWith(base+path.sep)&&dest.startsWith(path.resolve(repo,'artifacts/reviewed/ui-parity-axis-followup')+path.sep),'contained path '+f.destination);
  check(!fs.lstatSync(source).isSymbolicLink()&&sha(source)===f.sha256&&fs.statSync(source).size===f.bytes,'published bytes '+f.destination);
  check(!destinations.has(f.destination),'unique destination '+f.destination);destinations.add(f.destination);
  check(!/(?:^|\/)(?:runtime-private\.json|credential-private\.json|action-ledger\.json|diagnostics\.json|state-[^/]*|\.env[^/]*|[^/]*\.log)$/.test(f.source),'excluded private/raw filename '+f.destination);
  if(!source.endsWith('.png')){
    const text=fs.readFileSync(source,'utf8');
    for(const pattern of [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/g,/\bBearer\s+[A-Za-z0-9._~-]{20,}/g,/\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g,/\bsk-(?:ant-)?[A-Za-z0-9_-]{25,}/g])if(pattern.test(text))safetyMatches.push({path:f.source,pattern:String(pattern)});
  }
}
check(allow.files.length===199&&allow.files.reduce((s,f)=>s+f.bytes,0)===30641075,'publication count and bytes');
check(safetyMatches.length===0,'no high-confidence embedded credential pattern');
const sources=read(path.join(base,'source-hashes.json'));
for(const f of [...sources.sourceFiles,...sources.evidence,sources.harnessManifest])check(sha(path.join(base,f.path))===f.sha256&&fs.statSync(path.join(base,f.path)).size===f.bytes,'source manifest '+f.path);
const identity=read(path.join(attempt,'runtime-identity.json'));
check(identity.source===sources.originalSource&&identity.source==='38dffc33389aca0e4a87e0e88d42f7067aa220df'&&identity.image===sources.image&&identity.image==='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f','recorded original revision and image identity');
check(fs.readdirSync(base).filter(n=>n.startsWith('attempt-')).length===1,'one attempt directory in this package');
const ledger=read(path.join(attempt,'action-ledger.json')),publicLedger=read(path.join(derived,'action-ledger-public.json')).actions;
check(ledger.length===121&&ledger.filter(a=>a.change).length===41&&ledger.every(a=>a.completed),'121 completed actions and 41 changes');
const projected=ledger.map(a=>({id:a.id,case:a.case,label:a.label,method:a.method,change:a.change,completed:a.completed,...(a.case!=='entry'?{intendedValue:a.intendedValue,before:a.before,after:a.after}:{}),...(a.beforeEvidence?{beforeEvidence:a.beforeEvidence,afterEvidence:a.afterEvidence??null}:{})}));
check(JSON.stringify(projected)===JSON.stringify(publicLedger),'public ledger exactly follows declared projection');
for(const d of allow.derivatives)check(sha(path.join(repo,d.source))===d.sourceSha256&&sha(path.join(repo,d.destination))===d.publishedSha256&&d.sourceSha256!==d.publishedSha256,'distinct derivative provenance '+path.basename(d.destination));
const rawDiagnostics=read(path.join(attempt,'diagnostics.json')),safeDiagnostics=read(path.join(derived,'diagnostic-summary.json'));
check(JSON.stringify(rawDiagnostics.records)===JSON.stringify(safeDiagnostics.records)&&safeDiagnostics.overflow===null,'diagnostic records preserved without overflow');
const events=read(path.join(attempt,'event-index.json')).files.flatMap(f=>read(path.join(attempt,f)));
check(events.length===39&&events.every((e,i)=>e.sequence===i+1&&ledger.some(a=>a.id===e.action)),'39 ordered events resolve to actual action');
const rawStates=fs.readdirSync(attempt).filter(n=>/^\d{3}-.*\.json$/.test(n));
const periods={A:['2024-Q1','2024-Q2','2024-Q3','2024-Q4'],B:[1704067200000,1711929600000,1719792000000,1727740800000],C:['FY24-Q1','FY24-Q2','FY24-Q3','FY24-Q4']};
const geometry=[];
for(const f of rawStates){
  const s=read(path.join(attempt,f));
  const rows=s.explicit.data.value;
  const gotPeriods=rows.map(r=>r.period.value?.type==='category-wrapper'?r.period.value.fields.value.value:r.period.value.value);
  check(JSON.stringify(gotPeriods)===JSON.stringify(periods[s.fixture])&&JSON.stringify(rows.map(r=>[r.amounts.revenue.value,r.amounts.operatingIncome.value]))==='[[100,20],[120,25],[140,30],[160,40]]','independent exact period and financial data '+f);
  geometry.push({file:f,geometry:s.geometry});
}
check(rawStates.length===37,'37 raw full checkpoints');
const transactions=read(path.join(attempt,'transactions.json'));
const stateFor=label=>read(path.join(attempt,transactions.find(t=>t.label===label).after));
const rect=label=>Object.fromEntries(Object.entries(stateFor(label).geometry.seriesRect).map(([k,v])=>[k,v.value]));
check(rect('Horizontal-font').height===251&&rect('Horizontal-size').height===248&&rect('Horizontal-spacing').height===242,'horizontal geometry exact height changes');
check(rect('Vertical-font').x===51&&rect('Vertical-font').width===513&&rect('Vertical-size').x===59&&rect('Vertical-size').width===505&&rect('Vertical-spacing').x===71&&rect('Vertical-spacing').width===493,'vertical geometry exact x and width changes');
const axis=(s,d)=>s.live.axes.find(a=>a.identity.direction.value===d);
for(const [label,d,angle]of [['Horizontal-rotation-315','x',-45],['Horizontal-rotation-45','x',45],['Vertical-rotation-330','y',-30]]){
  const s=stateFor(label),a=axis(s,d),nodes=s.live.nodes.filter(n=>a.labels.includes(n.identity));
  check(a.style.label.value.rotation.value===angle&&nodes.length>0&&nodes.every(n=>Math.abs(Math.atan2(Math.sin(n.fields.rotation.value),Math.cos(n.fields.rotation.value))*180/Math.PI-angle)<1e-9),'raw finite rotation and text geometry '+label);
}
for(const [label,type]of [['B-number','number'],['B-time','time'],['B-category','category']]){
  const s=stateFor(label),a=axis(s,'x');
  check(a.identity.type.value===type&&a.style.label.value.spacing.value===11&&a.style.tick.value.enabled.value===false&&a.style.tick.value.width.value===1&&axis(s,'y').identity.type.value==='number','discriminator loss and separate amount role '+label);
}
const oldStyle=stateFor('B-number').model.chartOptions.bar.axes.category.value.positions.bottom.value;
const exitedStyle=stateFor('B-category').model.chartOptions.bar.axes.category.value.positions.bottom.value;
check(oldStyle.label.value.spacing.value===19&&oldStyle.tick.value.width.value===3&&exitedStyle.label.value.spacing.kind==='absent'&&exitedStyle.tick.value.width.kind==='absent','old category raw style retained at Number but absent on Category exit');
const texts=label=>{const s=stateFor(label);return s.live.nodes.filter(n=>axis(s,'x').labels.includes(n.identity)).map(n=>n.fields.text.value);};
check(JSON.stringify(texts('B-time'))===JSON.stringify(texts('B-ISO'))&&JSON.stringify(texts('B-ISO'))===JSON.stringify(texts('B-European'))&&texts('B-ISO').length===2,'unchanged time strings through both selected formats');
for(const [label,fmt]of [['B-ISO','%Y-%m-%d'],['B-European','%d/%m/%Y']])check(stateFor(label).explicit.axes.value.find(a=>a.position.value==='bottom').label.value.format.value===fmt,'explicit requested time format '+label);
const menus=read(path.join(attempt,'menus.json'));
for(const role of ['Horizontal','Vertical'])check(menus.find(m=>m.label===role+' Font').options.length===20&&menus.find(m=>m.label===role+' Size').options.length===16,'font and size menu counts '+role);
check(menus.find(m=>m.label==='Time Format').options.length===10,'ten time format choices inventoried');
const transactionEvents=label=>{const t=transactions.find(t=>t.label===label);return events.filter(e=>Number(e.action.split('.').at(-1).slice(1))>=t.uiActions.first&&Number(e.action.split('.').at(-1).slice(1))<=t.uiActions.last).map(e=>e.sequence);};
check(JSON.stringify(transactionEvents('B-number'))==='[27,28,29]'&&JSON.stringify(transactionEvents('B-time'))==='[30,31,32,33]'&&JSON.stringify(transactionEvents('B-ISO'))==='[34]'&&JSON.stringify(transactionEvents('B-European'))==='[35]'&&JSON.stringify(transactionEvents('B-category'))==='[36,37,38,39]','reported event sequence groups');
const map=read(path.join(derived,'copied-plan-link-map.json'));
const markdownLinks=text=>[...text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)].map(m=>m[1]).filter(h=>!/^https?:|^#/.test(h));
const planLinks=markdownLinks(fs.readFileSync(path.join(base,'plan.md'),'utf8'));
check(map.links.length===14&&JSON.stringify(planLinks)===JSON.stringify(map.links.map(l=>l.href)),'all 14 frozen-plan relative links mapped');
check(sha(path.join(attempt,'plan.md'))===sha(path.join(base,'plan.md')),'copied plan raw bytes preserved');
const links=[];
for(const item of allow.files.filter(f=>f.source.endsWith('.md'))){
  for(const href of markdownLinks(fs.readFileSync(path.join(repo,item.source),'utf8'))){
    const canonical=item.source.endsWith('/'+map.copiedPlan)?path.resolve(base,href):path.resolve(path.dirname(path.join(repo,item.source)),href);
    const publicTarget=path.relative(path.join(repo,'artifacts'),canonical).replaceAll(path.sep,'/');
    const available=destinations.has(publicTarget)||fs.existsSync(path.join(repo,'artifacts/reviewed',publicTarget));
    check(fs.existsSync(canonical)&&available,'relative publication link '+item.destination+' -> '+href);
    links.push({source:item.destination,href,target:publicTarget,relocated:item.source.endsWith('/'+map.copiedPlan),available});
  }
}
for(const link of map.links)check(path.resolve(base,link.href)===path.resolve(repo,link.canonicalTarget),'relocation target '+link.href);
const result={status:issues.length?'blocked':'passed',scope:'Independent artifact-only A05-A09 publication audit',runtimeStarted:false,frozenInputs:expected,publication:{files:allow.files.length,bytes:allow.files.reduce((s,f)=>s+f.bytes,0)},checks:checks.length,issues,safetyMatches,links,rawGeometry:geometry,results:checks};
fs.writeFileSync(path.join(own,'independent-audit.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,checks:checks.length,issues,safetyMatches,links:links.length}));
