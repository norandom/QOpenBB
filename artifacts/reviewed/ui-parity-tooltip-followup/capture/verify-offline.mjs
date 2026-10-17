import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../../..'),checks=[];
const hash=b=>createHash('sha256').update(b).digest('hex');
const read=p=>fs.readFileSync(path.join(root,p));
const check=(name,passed)=>{checks.push({name,passed:!!passed});if(!passed)throw Error(name);};
const sourcePath='artifacts/ui-parity-tooltip-followup/source-hashes.json',source=JSON.parse(read(sourcePath));
check('source-only claim',source.runtimeExecuted===false&&source.proposed.length===12&&source.baseline.length===12);
const markdown=read(source.plan.path).toString('utf8');
for(const [,target] of markdown.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)){
  const current=path.resolve(here,'..',target),final=path.resolve(root,'artifacts/reviewed/ui-parity-tooltip-followup',target);
  check('current plan link '+target,fs.existsSync(current));
  const proposedFinal=path.resolve(root,'artifacts/reviewed/ui-parity-tooltip-followup');
  const selected=final===proposedFinal||final.startsWith(proposedFinal+'/')?current:final;
  check('publication-depth plan link '+target,fs.existsSync(selected));
}
for(const f of [...source.inputs,...source.baseline,...source.proposed,...source.support,source.plan])
  check('source identity '+f.path,read(f.path).length===f.bytes&&hash(read(f.path))===f.sha256);
const old='artifacts/ui-parity-tooltip-plan/capture/attempt-20261017-r4-a2';
const oldBytes=read(old+'/static-verification.json');
check('original executed manifest',hash(oldBytes)==='c098553db7a38c72eafec8ab0fc3a7e06c41ce74396f9062e44c794b8f6cb123');
const original=JSON.parse(oldBytes),allowed=original.files.map(f=>f.name).sort();
for(const f of original.files){check('executed file preserved '+f.name,hash(read(old+'/harness/'+f.name))===f.sha256);
  check('baseline matches executed manifest '+f.name,hash(fs.readFileSync(here+'/baseline/harness/'+f.name))===f.sha256);}
for(const dir of ['harness','baseline/harness'])check('exact file inventory '+dir,JSON.stringify(fs.readdirSync(here+'/'+dir).sort())===JSON.stringify(allowed));
let diff='';for(const name of allowed){
  try{diff+=execFileSync('diff',['-u','--label','baseline/harness/'+name,'--label','harness/'+name,here+'/baseline/harness/'+name,here+'/harness/'+name],{encoding:'utf8'});}
  catch(e){if(e.status!==1)throw e;diff+=e.stdout;}}
check('explicit diff matches bytes',diff===fs.readFileSync(here+'/source-diff.patch','utf8'));
for(const name of ['start.mjs','run.sh','io.mjs','cleanup.mjs','verify.mjs','fixture.json'])
  check('unchanged accepted guard '+name,hash(fs.readFileSync(here+'/harness/'+name))===hash(fs.readFileSync(here+'/baseline/harness/'+name)));
const journey=fs.readFileSync(here+'/harness/journey.mjs','utf8'),baselineJourney=fs.readFileSync(here+'/baseline/harness/journey.mjs','utf8');
check('journey changes only persisted control receipts',journey.replace("const ui=()=>controls(page,input,receipt=>{if(!current)throw Error('Case receipt required');\n  (current.controlReceipts??=[]).push(receipt);persist();});",'const ui=()=>controls(page,input);').replaceAll('\r\n','\n')===baselineJourney.replaceAll('\r\n','\n'));
for(const name of ['verify-offline.mjs','freeze-source.mjs','followup-static.mjs']){execFileSync(process.execPath,['--check',here+'/'+name]);check('offline support syntax '+name,true);}
const started=Date.now();const output=execFileSync(process.execPath,[here+'/harness/static-check.mjs'],{encoding:'utf8',timeout:60000});
check('fresh static command completed',JSON.parse(output.trim()).passed===true);
const result=JSON.parse(fs.readFileSync(here+'/static-verification.json'));
check('fresh static scope',result.runtimeExecuted===false&&result.checks.every(c=>c.passed)&&result.files.length===12);
for(const f of result.files)check('fresh manifest identity '+f.name,source.proposed.some(p=>p.path.endsWith('/'+f.name)&&p.sha256===f.sha256));
const report={scope:'offline source checks only; no tooltip invocation, runtime or acceptance claim',runtimeExecuted:false,
  command:process.execPath+' '+fileURLToPath(import.meta.url),exitCode:0,staticCommand:process.execPath+' '+here+'/harness/static-check.mjs',
  elapsedMs:Date.now()-started,sourceManifestSha256:hash(read(sourcePath)),planSha256:source.plan.sha256,
  staticManifestSha256:hash(fs.readFileSync(here+'/static-verification.json')),checks,staticChecks:result.checks.length,staticOutput:JSON.parse(output.trim())};
fs.writeFileSync(here+'/offline-verification.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({offlineChecks:checks.length,staticChecks:result.checks.length,passed:true,runtimeExecuted:false,sourceManifestSha256:report.sourceManifestSha256,staticManifestSha256:report.staticManifestSha256}));
