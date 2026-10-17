import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const here=path.dirname(fileURLToPath(import.meta.url)),base=path.resolve(here,'..'),repo=path.resolve(base,'../..');
const name='attempt-20261017-tooltip-followup-a1',attempt=here+'/'+name;
const read=n=>JSON.parse(fs.readFileSync(attempt+'/'+n+'.json'));
const sha=b=>createHash('sha256').update(b).digest('hex');
const files=['plan.md','source-hashes.json','capture/static-verification.json','capture/offline-verification.json','capture/source-diff.patch',
  'capture/followup-static.mjs','capture/freeze-source.mjs','capture/verify-offline.mjs','capture/prepare-attempt.mjs','capture/verify-owned.mjs',
  'capture/report.md','capture/package-evidence.mjs','capture/verify-evidence.mjs','capture/commands.json','capture/observations.json'];
const source=JSON.parse(fs.readFileSync(base+'/source-hashes.json'));
for(const f of [...source.baseline,...source.proposed])files.push(path.relative(base,path.join(repo,f.path)));
const runtime=['identity-fixture-preflight.json',...Array.from({length:8},(_,i)=>'T0'+(i+1)+'.json'),
  'summary.json','diagnostics.json','cleanup-report.json','browser-cleanup.json','owned-absence-verification.json',
  'start-status.json','journey-status.json','cleanup-status.json','run-status.json','runtime-identity.json','byte-budget.json',
  'static-verification.json','executed-source-verification.json','reviewed-plan.md','source-hashes.json','followup-static.mjs'];
for(const f of runtime)files.push('capture/'+name+'/'+f);
for(const f of fs.readdirSync(attempt).filter(f=>f.endsWith('.png')))files.push('capture/'+name+'/'+f);
for(const dir of ['harness','verification-support'])for(const f of fs.readdirSync(attempt+'/'+dir))files.push('capture/'+name+'/'+dir+'/'+f);
const observations=[];for(let i=1;i<=8;i++){const c=read('T0'+i);for(const p of c.probes??[]){const t=p.observation?.pair.at(-1)?.tooltip;
  observations.push({case:c.id,id:p.id,ordinal:p.ordinal,requested:p.key,target:p.target?.yKey,wrapper:p.target?.wrapperId,
    targetYValue:p.target?.geometry.fields.yValue?.value,point:p.target?.point,status:p.status,rows:t?.rows,heading:t?.heading,pagination:t?.pagination,image:p.image,
    leaveVisible:p.leave?.pair.at(-1)?.tooltip?.visible??null,settledPair:p.settlement?.pair.length===2});}}
fs.writeFileSync(here+'/observations.json',JSON.stringify({scope:'Derived finite observations; intended target is not proof of actual picked identity',observations},null,2));
const life=read('lifecycle-private'),summary=read('summary');
const commands={shell:'wsl -d Debian -u mc',pinnedNode:'/mnt/d/Source/QOpenBB/artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node',
  attempt:name,startedAt:new Date(life.launchedAt).toISOString(),wrapperElapsedMs:Math.round(fs.statSync(attempt+'/run-status.json').mtimeMs-life.launchedAt),journeyElapsedMs:summary.elapsedMs,
  commands:[{command:'<pinned-node> capture/verify-offline.mjs',exitCode:0,result:'122 offline identity/link checks and 136 static checks'},
    {command:'<pinned-node> capture/prepare-attempt.mjs',exitCode:0,result:'12 frozen collector files and verification support copied before execution'},
    {command:'env TOOLTIP_HEAVY_GRANTED=yes timeout --signal=TERM --kill-after=1s 900s bash <attempt>/harness/run.sh <attempt>',exitCode:read('run-status').exitCode},
    {command:'<pinned-node> <attempt>/harness/verify.mjs <attempt>',exitCode:read('fresh-verification').failures.length?1:0,result:'95 structural checks; no semantic acceptance'},
    {command:'<pinned-node> capture/verify-owned.mjs <attempt>',exitCode:read('owned-absence-verification').passed?0:1,result:'Fresh owned resources absent; heavy lane released'}]};
fs.writeFileSync(here+'/commands.json',JSON.stringify(commands,null,2));
const derivative=read('fresh-verification');
const selectedNames=new Set(runtime.concat(fs.readdirSync(attempt).filter(n=>n.endsWith('.png'))));
derivative.files=derivative.files.filter(f=>selectedNames.has(f.name));
derivative.inventoryScope='Safe selected original files only; local private receipts, raw logs and unselected inventories omitted';
fs.writeFileSync(attempt+'/fresh-verification-public.json',JSON.stringify(derivative,null,2));files.push('capture/'+name+'/fresh-verification-public.json');
const entries=[...new Set(files)].sort().map(p=>{if(/private|\.log$|credential/i.test(p))throw Error('Unsafe selection '+p);
  const bytes=fs.readFileSync(base+'/'+p);return {path:'artifacts/ui-parity-tooltip-followup/'+p,bytes:bytes.length,sha256:sha(bytes),
    sanitization:p.endsWith('fresh-verification-public.json')?'Safe inventory derivative; raw private inventory omitted':p.endsWith('observations.json')?'Finite projection derived from selected case JSON':p.endsWith('commands.json')?'Private lifecycle fields projected to start time and elapsed time only':'None; synthetic/sanitized bytes or source'};});
const allowlist={scope:'Proposed single-attempt tooltip follow-up evidence; independent review required before publication',runtimeExecuted:true,candidateExecuted:false,
  automaticRetries:0,separatelyGrantedAttempts:1,authoritativeAttempt:name,containsCredentialValues:false,
  omissions:['Raw private runtime/process/lifecycle ownership receipts','Raw logs','Raw verifier inventory','Owner environments, credentials, browser profiles and authentication state'],files:entries};
fs.writeFileSync(here+'/publication-allowlist.json',JSON.stringify(allowlist,null,2));
console.log(JSON.stringify({safeFiles:entries.length,observations:observations.length,sha256:sha(fs.readFileSync(here+'/publication-allowlist.json'))}));
