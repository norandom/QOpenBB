import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8').replace(/^\uFEFF/,''));
const digest=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const capture='artifacts/ui-parity-axis-controls/capture';
const review='artifacts/ui-parity-axis-controls-review';
const selected=read(capture+'/publication-allowlist.json').files;
const checks=[];const check=(name,passed)=>checks.push({name,passed:!!passed});
check('worker manifest identity',digest(capture+'/publication-allowlist.json')==='542d3c441e40a13b71b737f016c0044018ec5722359dc58cbb377ee6ddbdb3ae');
check('worker report identity',digest(capture+'/report.md')==='ba135d830c33107d8265cb34c21579aa59b528ffe20d8143d8fcd46fd292084d');
const destinations=new Set(selected.map(f=>f.destination));
for(const f of selected){
  check('hash '+f.destination,digest(f.source)===f.sha256);
  check('size '+f.destination,fs.statSync(f.source).size===f.bytes);
  check('safe path '+f.destination,!/(?:private|\.log$|\/state-|\/profiles?\/|node_modules|\.env(?:\.|$)|\/action-ledger\.json$|\/diagnostics\.json$)/i.test(f.source));
  check('contained path '+f.destination,f.source.startsWith(capture+'/')&&f.destination===f.source.slice('artifacts/'.length)&&!f.source.includes('..'));
  if(f.source.endsWith('.json')){
    const raw=fs.readFileSync(f.source,'utf8');read(f.source);
    check('no credential material '+f.destination,!/Bearer\s+[A-Za-z0-9._-]{12,}|eyJ[A-Za-z0-9_-]{16,}\.[A-Za-z0-9_-]{16,}\./.test(raw));
    if(f.source.endsWith('/action-ledger-public.json'))check('setup values omitted '+f.destination,read(f.source).actions.filter(a=>a.case==='entry').every(a=>!('intendedValue'in a)&&!('before'in a)&&!('after'in a)));
  }
}
check('240 unique worker paths',selected.length===240&&destinations.size===240);
const report=fs.readFileSync(capture+'/report.md','utf8');let linkCount=0;
for(const m of report.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){
  if(/^(https?:|#)/.test(m[1]))continue;linkCount++;
  const target=path.posix.normalize('ui-parity-axis-controls/capture/'+m[1].split('#')[0]);
  check('published report link '+m[1],destinations.has(target));
}
const recovery=read(capture+'/attempt-20261017T1422580-7c412f5c/recovered-event-index.json');
const attempt=capture+'/attempt-20261017T1422580-7c412f5c/';
for(const f of [recovery.originalIndex,...recovery.chunks])check('recovery hash '+f.path,digest(attempt+f.path)===f.sha256);
check('recovery explicitly incomplete',recovery.count===31&&recovery.isCompleteRun===false);
const result={scope:'Exact safe selected bytes, report links and recovery provenance',checkCount:checks.length,linkCount,selectedFiles:selected.length,failed:checks.filter(c=>!c.passed),checks};
fs.writeFileSync(review+'/publication-verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({checkCount:checks.length,linkCount,selectedFiles:selected.length,failed:result.failed}));
if(result.failed.length)process.exitCode=1;
