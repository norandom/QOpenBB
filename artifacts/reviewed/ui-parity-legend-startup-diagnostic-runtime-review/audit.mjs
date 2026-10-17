import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
const root='artifacts/ui-parity-legend-startup-diagnostic';
const attempt=root+'/attempt-20261017T1615437-672fb2a3';
const analysis=root+'/analysis-attempt-20261017T1615437-672fb2a3';
const own='artifacts/ui-parity-legend-startup-diagnostic-runtime-review';
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(p));
const checks=[];function check(name,fn){fn();checks.push(name);}
const allowlist=read(analysis+'/publication-allowlist.json');
check('dispatch allowlist pin',()=>assert.equal(hash(analysis+'/publication-allowlist.json'),'7c846fea4bc194c8ad83ae32829ee85022af7d3b25beaee2795744b3a2fbb0b1'));
const manifest=read(attempt+'/source-manifest.json');
check('accepted source pins',()=>{
  assert.equal(hash(attempt+'/source-manifest.json'),'29096d4612637299972e068e4b4d76dbe1331051e1dce7f885258cb3bc79fe3b');
  assert.equal(hash(root+'/harness-manifest.json'),hash(attempt+'/source-manifest.json'));
  assert.equal(hash(root+'/source-hashes.json'),'95128fc21fd7f16d230e5e7488ee32972822c00134cd045b689ff9e4ba1a4a7b');
  for(const f of read(root+'/source-hashes.json').sourceFiles){assert.equal(hash(root+'/'+f.path),f.sha256);assert.equal(fs.statSync(root+'/'+f.path).size,f.bytes);}
});
check('seven exact executed runtime copies',()=>{assert.equal(manifest.files.length,7);for(const f of manifest.files){assert.equal(hash(attempt+'/'+f.path),f.sha256);assert.equal(fs.statSync(attempt+'/'+f.path).size,f.bytes);}});
const frozen=allowlist.map(e=>({...e}));
check('27 unique safe selected entries',()=>{
  assert.equal(allowlist.length,27);assert.equal(new Set(allowlist.map(e=>e.sourcePath)).size,27);
  for(const f of allowlist){assert(f.sourcePath.startsWith(attempt+'/')||f.sourcePath.startsWith(analysis+'/'));assert(!f.sourcePath.includes('..'));assert(!/-private\.json$|\.log$|\/state-/.test(f.sourcePath));assert(!fs.lstatSync(f.sourcePath).isSymbolicLink());assert.equal(hash(f.sourcePath),f.sha256);assert.equal(fs.statSync(f.sourcePath).size,f.bytes);}
});
const samples=read(attempt+'/samples.json'),runtime=read(attempt+'/runtime-private.json');
const result=read(attempt+'/probe-result.json'),observations=read(analysis+'/observations.json');
check('three finite same-instance selected observations',()=>{
  assert.equal(samples.length,3);assert.deepEqual(samples.map(s=>s.context.plannedOffsetMs),[0,1000,3000]);
  for(const [i,s] of samples.entries()){
    assert.equal(s.context.sample,i+1);assert.equal(s.context.containerId,runtime.container);assert.equal(s.context.networkId,runtime.networkId);
    assert(s.context.readStartedMs<=s.context.readEndedMs);assert(s.context.elapsedSinceRunReturnMs>=s.context.plannedOffsetMs);assert(s.context.elapsedSinceRunReturnMs<90000);
    if(i)assert(s.context.readStartedMs>samples[i-1].context.readEndedMs);
    assert.deepEqual(s.runtime.target,{own:true,in:true,kind:'null',type:'object',value:null});
    assert.equal(s.configured.target.arrayLength,1);assert.equal(s.configured.target.own,true);assert.equal(s.configured.target.in,true);
    assert.equal(s.configured.target.entries[0].HostIp.value,'127.0.0.1');assert.equal(s.configured.target.entries[0].HostPort.value,'');
    assert.deepEqual(s.errors,[]);assert.equal(s.security.attachedNetworkCount,1);for(const k of ['containerIdMatched','labelMatched','exactNetwork'])assert.equal(s.security[k],true);assert(Object.values(s.security.network).every(v=>v===true));
    for(const [k,v] of Object.entries({Status:'running',Running:true,Restarting:false,Dead:false,ExitCode:0,OOMKilled:false}))assert.equal(s.state[k].value,v);
    assert.equal(s.state.StartedAt.value,samples[0].state.StartedAt.value);assert.equal(s.state.FinishedAt.value,'0001-01-01T00:00:00Z');
    assert.equal(observations.samples[i].actualReadEndAfterRunMs,s.context.elapsedSinceRunReturnMs);assert.deepEqual(observations.samples[i].runtimeTarget,s.runtime.target);assert.deepEqual(observations.samples[i].configuredTarget,s.configured.target);
    for(const [k,v] of Object.entries(observations.samples[i].state))assert.equal(s.state[k].value,v);
  }
});
check('unresolved result retains nonzero status and zero-health source gate',()=>{
  assert.equal(result.outcome,'publication-not-observed-within-window');assert.equal(result.samples,3);assert(!('health' in result));assert.equal(result.browserCreated,false);assert.equal(result.noRetry,true);
  assert.equal(result.image,manifest.image);assert.equal(result.originalSource,manifest.originalSource);assert.deepEqual(observations.rawResult,result);
  const status=read(attempt+'/run-status.json');assert.equal(status.status,'diagnostic-closed');assert.equal(status.exitCode,1);assert.equal(status.outcome,result.outcome);assert.deepEqual(status,observations.rawStatus);assert.equal(read(attempt+'/watchdog-status.json').exitCode,1);
  assert.equal(observations.counters.healthRequests,0);assert.equal(observations.counters.browserProcesses,0);
});
const cleanup=read(attempt+'/cleanup-report.json'),absence=read(analysis+'/owned-absence.json'),launcher=read(analysis+'/launcher-absence.json'),launch=read(attempt+'/launch.json');
check('retained exact cleanup and later absence proofs; current filesystem absence',()=>{
  assert.equal(cleanup.status,'cleaned');assert.equal(cleanup.failure,null);
  for(const k of ['containerAbsent','networkAbsent','stateAbsent','credentialAbsent']){assert.equal(cleanup[k],true);assert.equal(absence[k],true);}
  assert.equal(absence.passed,true);assert.equal(absence.readOnly,true);assert.equal(absence.browserCreated,false);assert.equal(launcher.absent,true);assert.equal(launcher.windowsLauncherPid,launch.windowsLauncherPid);assert.equal(launch.hidden,true);
  assert(Date.parse(absence.checkedAt)>Date.parse(launch.startedAtUtc));assert(Date.parse(launcher.checkedAtUtc)>Date.parse(launch.startedAtUtc));
  assert(!fs.existsSync(attempt+'/credential-private.json'));assert(!fs.readdirSync(attempt).some(n=>n.startsWith('state-')));
});
const files=[];function scan(directory){for(const e of fs.readdirSync(directory,{withFileTypes:true})){const p=path.join(directory,e.name);assert(!e.isSymbolicLink());if(e.isDirectory())scan(p);else files.push({path:path.relative(attempt,p).replaceAll('\\','/'),bytes:fs.statSync(p).size});}}scan(attempt);
const bytes=files.reduce((n,f)=>n+f.bytes,0),publicJson=files.filter(f=>f.path.endsWith('.json')&&!f.path.endsWith('-private.json')).reduce((n,f)=>n+f.bytes,0);
check('actual retained inventory and public bounds',()=>{
  const completed=read(analysis+'/completed-output-inventory.json');assert.equal(files.length,25);assert.equal(bytes,33226);assert.equal(completed.files,files.length);assert.equal(completed.bytes,bytes);assert(files.length<=32&&bytes<=2097152&&publicJson<=524288);
  for(const f of files.filter(f=>f.path.endsWith('.json')))assert(f.bytes<=65536);
  const final=read(attempt+'/final-output-inventory.json');assert.equal(final.totals.files+1,files.length);assert.equal(final.totals.bytes+fs.statSync(attempt+'/final-output-inventory.json').size,bytes);
  for(const f of final.entries)assert.equal(files.find(x=>x.path===f.path)?.bytes,f.bytes);
  for(const f of completed.omitted){assert.equal(files.find(x=>x.path===f.path)?.bytes,f.bytes);assert(!allowlist.some(e=>e.sourcePath===attempt+'/'+f.path));}
  assert.equal(completed.selected.length,18);assert.equal(completed.omitted.length,7);
});
check('no generated private values or common credential patterns selected',()=>{
  for(const f of allowlist){const text=fs.readFileSync(f.sourcePath,'utf8');assert(!text.includes(runtime.ownership));assert(!/legend-probe-[a-f0-9]{12}@example\.com|Aa1![a-f0-9]{48}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:ghp_|github_pat_)[A-Za-z0-9_]{25,}/.test(text));}
});
const supplied=spawnSync(process.execPath,[analysis+'/verify-evidence.mjs'],{encoding:'utf8',windowsHide:true});
check('supplied read-only evidence verifier',()=>assert.equal(supplied.status,0,supplied.stderr));
check('selected frozen bytes preserved',()=>{for(const f of frozen){assert.equal(hash(f.sourcePath),f.sha256);assert.equal(fs.statSync(f.sourcePath).size,f.bytes);}});
const receipt={status:'passed',scope:'Independent existing evidence/source/filesystem review only; no Docker, runtime, network, process probe, retry, build, install or frozen writes',node:process.version,checks,allowlistSha256:hash(analysis+'/publication-allowlist.json'),runtimeCopies:7,selectedFiles:27,physicalAttemptFiles:files.length,physicalAttemptBytes:bytes,publicJsonBytes:publicJson,readEndAfterRunMs:samples.map(s=>s.context.elapsedSinceRunReturnMs),outcome:result.outcome,exitCode:1,cleanup:'cleaned',absenceEvidence:{ownedCheckedAt:absence.checkedAt,launcherCheckedAt:launcher.checkedAtUtc,reviewerReranLiveChecks:false},suppliedVerifier:{exitCode:supplied.status,output:JSON.parse(supplied.stdout)},frozenPreserved:true,conclusion:'Configured loopback/dynamic binding was present; runtime allocation was null on three running same-instance observations. No root-cause or future-readiness conclusion.'};
fs.writeFileSync(own+'/verification.json',JSON.stringify(receipt,null,2)+'\n');
fs.copyFileSync(analysis+'/publication-allowlist.json',own+'/reviewed-evidence-publication-allowlist.json');
console.log(JSON.stringify({status:'passed',checks:checks.length,selectedFiles:27,physicalAttemptFiles:files.length,physicalAttemptBytes:bytes,publicJsonBytes:publicJson,frozenPreserved:true}));
