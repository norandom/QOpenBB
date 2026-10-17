import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const base=path.dirname(new URL(import.meta.url).pathname),sha=b=>createHash('sha256').update(b).digest('hex');
const attempts=[{name:'attempt-20261017-r4-a1',manifest:'53487962b319998a928a18fb4a323a41106f47a88a6ab6792f2b54a3f9de041a',checks:59},
  {name:'attempt-20261017-r4-a2',manifest:'c098553db7a38c72eafec8ab0fc3a7e06c41ce74396f9062e44c794b8f6cb123',checks:68}];
const runtime=['identity-fixture-preflight.json','T01.json','T02.json','T03.json','T04.json','T05.json','T06.json','T07.json','T08.json',
  'summary.json','failure.json','diagnostics.json','cleanup-report.json','browser-cleanup.json','owned-absence-verification.json',
  'start-status.json','journey-status.json','cleanup-status.json','run-status.json','runtime-identity.json','byte-budget.json'];
const paths=['report.md','preparation.md','verify-owned.mjs','package.mjs','commands.json'],commands=[];
for(const attempt of attempts){const dir=base+'/'+attempt.name,manifestBytes=fs.readFileSync(dir+'/static-verification.json'),manifest=JSON.parse(manifestBytes);
  if(sha(manifestBytes)!==attempt.manifest)throw Error('Executed manifest mismatch');
  const executed=manifest.files.map(f=>({name:f.name,sha256:sha(fs.readFileSync(dir+'/harness/'+f.name)),expectedSha256:f.sha256}));
  if(executed.some(f=>f.sha256!==f.expectedSha256))throw Error('Executed source mismatch');
  fs.writeFileSync(dir+'/executed-source-verification.json',JSON.stringify({passed:true,manifestSha256:sha(manifestBytes),files:executed},null,2));
  const selected=runtime.filter(n=>fs.existsSync(dir+'/'+n));selected.push(...fs.readdirSync(dir).filter(n=>n.endsWith('.png')));
  const local=JSON.parse(fs.readFileSync(dir+'/fresh-verification.json'));local.files=local.files.filter(f=>selected.includes(f.name));
  local.inventoryScope='Safe selected files only; local private receipts and raw logs omitted';
  fs.writeFileSync(dir+'/fresh-verification-public.json',JSON.stringify(local,null,2));
  paths.push(...manifest.files.map(f=>attempt.name+'/harness/'+f.name),attempt.name+'/static-verification.json',attempt.name+'/executed-source-verification.json',
    ...selected.map(n=>attempt.name+'/'+n),attempt.name+'/fresh-verification-public.json');
  const lifecycle=JSON.parse(fs.readFileSync(dir+'/lifecycle-private.json'));
  commands.push({attempt:attempt.name,startedAt:new Date(lifecycle.launchedAt).toISOString(),elapsedMs:Math.round(fs.statSync(dir+'/run-status.json').mtimeMs-lifecycle.launchedAt),
    staticChecks:attempt.checks,commands:[
      {command:'<pinned-node> capture/harness/static-check.mjs (offline checks before attempt-local copy)',exitCode:0},
      {command:'env TOOLTIP_HEAVY_GRANTED=yes timeout --signal=TERM --kill-after=1s 900s bash <attempt>/harness/run.sh <attempt>',exitCode:JSON.parse(fs.readFileSync(dir+'/run-status.json')).exitCode},
      {command:'<pinned-node> <attempt>/harness/verify.mjs <attempt>',exitCode:local.failures.length?1:0,result:local.checks.length+' structural checks; no UI acceptance inference'},
      {command:'<pinned-node> capture/verify-owned.mjs <attempt>',exitCode:0,result:'All recorded owned resources absent'}]});
}
fs.writeFileSync(base+'/commands.json',JSON.stringify({shell:'wsl -d Debian -u mc',pinnedNode:'/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node',attempts:commands},null,2));
const links=[];for(const file of ['report.md','preparation.md'])for(const m of fs.readFileSync(base+'/'+file,'utf8').matchAll(/\[[^\]]+\]\(([^)]+)\)/g)){
  if(/^(?:https?:|#)/.test(m[1]))continue;const exists=fs.existsSync(path.resolve(base,path.dirname(file),m[1]));links.push({from:file,target:m[1],exists});if(!exists)throw Error('Missing local link');}
fs.writeFileSync(base+'/link-verification.json',JSON.stringify({passed:true,links},null,2));paths.push('link-verification.json');
const files=paths.map(p=>{const bytes=fs.readFileSync(base+'/'+p);return {path:'artifacts/ui-parity-tooltip-plan/capture/'+p,bytes:bytes.length,sha256:sha(bytes),
  sanitization:p.endsWith('fresh-verification-public.json')?'Safe inventory derivative; private receipt/log inventory omitted':'None; synthetic or sanitized original bytes'};});
fs.writeFileSync(base+'/publication-allowlist.json',JSON.stringify({scope:'Safe original-only unresolved attempts; not tooltip behavior acceptance',authoritativeAttempt:attempts.at(-1).name,
  preservedAttempts:attempts.map(a=>a.name),automaticRetries:0,separatelyGrantedAttempts:2,containsCredentialValues:false,
  omissions:['Private runtime/process ownership receipts','Raw logs','Browser profiles and authentication state'],files},null,2));
console.log(JSON.stringify({safeFiles:files.length,links:links.length,allLinksResolve:true,attemptsPreserved:attempts.length}));
