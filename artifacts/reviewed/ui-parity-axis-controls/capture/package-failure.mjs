import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const repo='/mnt/d/Source/QOpenBB',base=repo+'/artifacts/ui-parity-axis-controls/capture';
const hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const files=[];const add=relative=>{const source=base+'/'+relative;files.push({source:path.relative(repo,source),destination:'ui-parity-axis-controls/capture/'+relative,sha256:hash(source),bytes:fs.statSync(source).size});};
for(const attempt of ['attempt-20261017T1409125-18fed9af','attempt-20261017T1413358-2f46bb8c','attempt-20261017T1416524-c93ff5a0','attempt-20261017T1422580-7c412f5c']){
const dir=base+'/'+attempt,read=n=>JSON.parse(fs.readFileSync(dir+'/'+n+'.json'));
if(read('run-status').exitCode!==1||!read('cleanup-report').containerAbsent||!read('browser-cleanup').browserClosed)throw Error('Failure outputs not closed');
const ledger=read('action-ledger');
fs.writeFileSync(dir+'/action-ledger-public.json',JSON.stringify({kind:'setup counts/status only; chart action values and finite DOM retained; setup values and DOM omitted',actions:ledger.map(a=>({id:a.id,case:a.case,label:a.label,method:a.method,change:a.change,completed:a.completed,
  ...(a.case!=='entry'?{intendedValue:a.intendedValue,before:a.before,after:a.after}:{}),...(a.beforeEvidence?{beforeEvidence:a.beforeEvidence,afterEvidence:a.afterEvidence??null}:{})}))}));
const diagnostics=read('diagnostics');fs.writeFileSync(dir+'/diagnostic-summary.json',JSON.stringify({records:diagnostics.records,overflow:diagnostics.overflow,limitation:'CDP loadingFailed retains text/type only; no complete failed-asset attribution'}));
for(const name of fs.readdirSync(dir+'/harness'))add(attempt+'/harness/'+name);
for(const name of ['source-manifest.json','preparation.json','failure.json','counters.json','runtime-identity.json','start-status.json','journey-status.json','run-status.json','cleanup-status.json','cleanup-report.json','browser-cleanup.json','watchdog-status.json','onboarding-A.json','event-index.json','action-ledger-public.json','diagnostic-summary.json'])add(attempt+'/'+name);
for(const name of fs.readdirSync(dir).filter(n=>/^\d{3}-.*\.(json|png)$|^observations-.*\.json$|^identity-.*\.json$|^entry-data-.*\.json$|^events-p\d{2}\.json$|^(cases|menus|screenshots|transactions|recovered-event-index|transaction-findings|event-deltas|partial-verification)\.json$/.test(n)))add(attempt+'/'+name);
}
for(const name of fs.readdirSync(base+'/harness'))add('harness/'+name);
for(const name of ['harness-manifest.json','static-verification.json','report.md','attempt-notes.md','prepare-run.mjs','verify.mjs','supervise.sh','package-failure.mjs','analyze.mjs','recover-events.mjs','verify-partial.mjs','profile-io.mjs','io-profile-cd8e6adb3119.json'])add(name);
const manifest={schemaVersion:1,status:'A01-A04 supported in attempt4; A05 partial; A06-A09 unrun; four failed attempts preserved',files,metadataPolicy:'allowlist hashes itself only in controller sync manifest',
  excluded:['runtime-private.json','credential-private.json','state-*','raw action-ledger.json','raw diagnostics.json','logs','profiles','auth records','environment files','dependencies','images'],
  derivatives:[{source:'each attempt/action-ledger.json',published:'each attempt/action-ledger-public.json',change:'Setup values and DOM omitted; counts/status and chart-entry evidence refs retained'},
    {source:'each attempt/diagnostics.json',published:'each attempt/diagnostic-summary.json',change:'Safe original synthetic diagnostics only; attribution limitation added'}]};
fs.writeFileSync(base+'/publication-allowlist.json',JSON.stringify(manifest,null,2));
console.log(JSON.stringify({files:files.length,bytes:files.reduce((a,f)=>a+f.bytes,0),reportSha256:hash(base+'/report.md'),allowlistSha256:hash(base+'/publication-allowlist.json')}));
