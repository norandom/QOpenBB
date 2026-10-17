import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const base=path.dirname(fileURLToPath(import.meta.url)),repo=path.resolve(base,'../..'),attempt=path.resolve(process.argv[2]),derived=path.resolve(process.argv[3]);
if(path.dirname(attempt)!==base||path.dirname(derived)!==base||!path.basename(attempt).startsWith('attempt-')||!path.basename(derived).startsWith('analysis-attempt-'))throw Error('Owned evidence paths required');
const read=n=>JSON.parse(fs.readFileSync(path.join(attempt,n))),hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');
if(!read('cleanup-report.json').containerAbsent||!read('browser-cleanup.json').browserClosed||!fs.existsSync(path.join(attempt,'watchdog-status.json')))throw Error('Only closed evidence may be packaged');
const write=(name,value)=>{const bytes=Buffer.from(JSON.stringify(value));if(bytes.length>2097152)throw Error('Derived JSON cap');fs.writeFileSync(path.join(derived,name),bytes);};
const actions=read('action-ledger.json').map(a=>({id:a.id,case:a.case,label:a.label,method:a.method,change:a.change,completed:a.completed,
  ...(a.case!=='entry'?{intendedValue:a.intendedValue,before:a.before,after:a.after}:{}),...(a.beforeEvidence?{beforeEvidence:a.beforeEvidence,afterEvidence:a.afterEvidence??null}:{})}));
write('action-ledger-public.json',{policy:'Setup values/DOM omitted; setup action counts/status and chart evidence references retained',actions});
const diagnostics=read('diagnostics.json');write('diagnostic-summary.json',{...diagnostics,limitation:'CDP loadingFailed retains text/type only; complete failed-asset attribution and internal editor scroll offsets unmeasured'});
const files=[],added=new Set(),slash=p=>p.split(path.sep).join('/');
function add(file){
  const relative=slash(path.relative(base,file));if(added.has(relative))return;added.add(relative);
  files.push({source:slash(path.relative(repo,file)),destination:'ui-parity-axis-followup/'+relative,bytes:fs.statSync(file).size,sha256:hash(file)});
}
for(const name of ['plan.md','source-hashes.json','harness-manifest.json','offline-verification.json','static-verification.json','verify-offline.mjs','verify-runtime.mjs','verify-owned-absence.mjs','map-copied-plan.mjs','analyze.mjs','prepare-run.mjs','supervise.sh','package-evidence.mjs','report.md'])add(path.join(base,name));
for(const dir of ['harness','frozen/harness'])for(const name of fs.readdirSync(path.join(base,dir)))add(path.join(base,dir,name));
add(path.join(base,'frozen/executed-source-manifest.json'));
const exact=new Set(['grant-proof.json','plan.md','source-hashes.json','source-manifest.json','preparation.json','runtime-identity.json','start-status.json','journey-status.json','run-status.json','cleanup-status.json','cleanup-report.json','browser-cleanup.json','watchdog-status.json','counters.json','cases.json','menus.json','screenshots.json','transactions.json','event-index.json','summary.json','failure.json','retained-bytes.json','final-output-inventory.json']);
for(const name of fs.readdirSync(attempt))if(exact.has(name)||/^\d{3}-.*\.(json|png)$|^(observations|identity|entry-data|baseline|restoration|onboarding)-.*\.json$|^events-p\d{2}\.json$/.test(name))add(path.join(attempt,name));
for(const name of fs.readdirSync(path.join(attempt,'harness')))add(path.join(attempt,'harness',name));
for(const name of fs.readdirSync(derived))if(name.endsWith('.json'))add(path.join(derived,name));
const verification=JSON.parse(fs.readFileSync(path.join(derived,'runtime-verification.json')));
const derivatives=[['action-ledger.json','action-ledger-public.json','Setup values and DOM removed; counts/status/finite chart-action observations retained'],['diagnostics.json','diagnostic-summary.json','Safe finite diagnostics plus attribution limitations']].map(([source,destination,change])=>({source:slash(path.relative(repo,path.join(attempt,source))),sourceSha256:hash(path.join(attempt,source)),destination:slash(path.relative(repo,path.join(derived,destination))),publishedSha256:hash(path.join(derived,destination)),change}));
const manifest={schemaVersion:1,status:verification.status,scope:verification.scope,files,derivatives,excluded:['credential-private.json','runtime-private.json','state-*','raw action-ledger.json','raw diagnostics.json','logs','profiles','authentication traces','environment files','dependency caches','image archives'],selfHashPolicy:'Controller sync manifest hashes this allowlist; no self hash'};
fs.writeFileSync(path.join(base,'publication-allowlist.json'),JSON.stringify(manifest,null,2));
console.log(JSON.stringify({files:files.length,bytes:files.reduce((s,f)=>s+f.bytes,0),sha256:hash(path.join(base,'publication-allowlist.json'))}));
