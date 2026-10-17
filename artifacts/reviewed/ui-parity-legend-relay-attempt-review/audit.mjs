import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {admitContainer,networkValid,statsDecision} from '../ui-parity-legend-fixed-relay-revised/harness/admission.mjs';
import {absenceComplete} from '../ui-parity-legend-fixed-relay-revised/harness/cleanup.mjs';

const base=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(base,'../..');
const source=path.join(root,'artifacts/ui-parity-legend-fixed-relay-revised');
const name='attempt-20261017T1700437-e5d5e603',attempt=path.join(source,name),analysis=path.join(source,'analysis-'+name);
const bytes=file=>fs.readFileSync(file),json=file=>JSON.parse(bytes(file)),hash=file=>createHash('sha256').update(bytes(file)).digest('hex');
const checks=[];
function check(title,body){body();checks.push(title);}
function verify(entry){const file=path.join(root,entry.sourcePath);assert(!entry.sourcePath.includes('..'));assert(!fs.lstatSync(file).isSymbolicLink());assert.equal(hash(file),entry.sha256,entry.sourcePath);assert.equal(bytes(file).length,entry.bytes,entry.sourcePath);}
const selection=json(path.join(analysis,'publication-allowlist.json'));
const allowlistSha256='a0c8a3224ce04bdda3efb58c955166db805a3993f0d1191b99a75e5e58de7aa2';
function frozen(){
  assert.equal(hash(path.join(analysis,'publication-allowlist.json')),allowlistSha256);
  assert.equal(selection.length,26);assert.equal(new Set(selection.map(item=>item.sourcePath)).size,26);
  selection.forEach(verify);
  assert.equal(hash(path.join(source,'source-hashes.json')),'7d1dbfc86d2cef42d8b8e73eacf63c85dd0c3676938c95d10210976cd5d263fb');
  for(const item of json(path.join(source,'source-hashes.json')).sourceFiles)verify({sourcePath:'artifacts/ui-parity-legend-fixed-relay-revised/'+item.path,...item});
  assert.equal(hash(path.join(root,'artifacts/ui-parity-legend-fixed-relay-revision-review/review.md')),'edcc27905f2db4dc5a8f2477776e07e96a4921eeb90626d514246afa276c6bd7');
}
check('Exact 26-file publication and accepted source/review identities',frozen);
const admission=json(path.join(attempt,'admission-receipts.json')),app=admission.containers.app,relay=admission.containers.relay;
const result=json(path.join(attempt,'probe-result.json')),status=json(path.join(attempt,'run-status.json'));
const cleanup=json(path.join(attempt,'cleanup-report.json')),stats=json(path.join(attempt,'relay-stats.json'));
const runtime=json(path.join(attempt,'runtime-private.json')),watchdog=json(path.join(attempt,'watchdog-status.json'));
const observed=json(path.join(analysis,'observations.json')),helper=json(path.join(attempt,'helper-launch.json'));
const owned=json(path.join(analysis,'fresh-owned-absence.json')),helperAbsent=json(path.join(analysis,'fresh-helper-absence.json'));
check('Eight exact executed copies and recorded preparation',()=>{
  const manifest=json(path.join(attempt,'source-manifest.json')),preparation=json(path.join(attempt,'preparation.json'));
  assert.equal(manifest.files.length,8);assert.equal(hash(path.join(attempt,'source-manifest.json')),'dcb25a5a5bcadf2d5628b0f2ebd2077586c7bde325a063b4eb5bf72f266b8700');
  for(const item of manifest.files){assert.equal(hash(path.join(attempt,item.path)),item.sha256);assert.equal(bytes(path.join(attempt,item.path)).length,item.bytes);}
  assert.equal(preparation.attempt,name);assert.equal(preparation.exactCopies,true);assert.equal(preparation.runtimeStarted,false);assert.equal(preparation.manifestSha256,hash(path.join(attempt,'source-manifest.json')));
});
check('Actual classifier and selected state/attachment/publication evidence',()=>{
  assert(Object.values(admission.networks).every(networkValid));
  assert.equal(admitContainer(app).kind,'app-admitted');assert.equal(admitContainer(relay).kind,'security-unresolved');
  assert.deepEqual(Object.entries(relay.security).filter(([,value])=>value!==true),[['exactMounts',false]]);
  for(const container of [app,relay])assert.deepEqual(container.state,{Status:'running',Running:true,Restarting:false,Dead:false,ExitCode:0,OOMKilled:false});
  assert(app.noConfiguredPublications&&app.noRuntimePublications);
  assert.deepEqual(relay.runtime.entries,[{HostIp:'127.0.0.1',HostPort:'32807'}]);
});
check('Three selected bind mounts versus separate configured tmpfs',()=>{
  const rows=relay.selected.Mounts.entries.map(item=>({destination:item.Destination.value,type:item.Type.value,readWrite:item.RW.value,sourceIdentityMatched:item.Source.ownedPathMatched}));
  assert.deepEqual(rows,[{destination:'/relay/relay.py',type:'bind',readWrite:false,sourceIdentityMatched:true},{destination:'/relay/config.json',type:'bind',readWrite:false,sourceIdentityMatched:true},{destination:'/evidence/relay-stats.json',type:'bind',readWrite:true,sourceIdentityMatched:true}]);
  assert.equal(relay.selected.Mounts.length,3);assert.equal(relay.selected.Tmpfs.data.value,'rw,nosuid,nodev,size=1048576');assert.equal(relay.security.boundedTmpfs,true);
  assert.deepEqual(observed.mounts,rows);assert.deepEqual(observed.configuredTmpfs,relay.selected.Tmpfs.data);
  assert(fs.readFileSync(path.join(attempt,'harness/admission.mjs'),'utf8').includes('raw.Mounts.length===4'));
  assert.equal(hash(path.join(attempt,'relay-config.json')),admission.config.sha256);
  assert.deepEqual(json(path.join(attempt,'relay-config.json')),{upstreamIPv4:app.internalIPv4,upstreamPort:3000});
});
check('Stopped prefix implies no harness readiness GET; no browser path',()=>{
  assert.equal(result.stage,'relay-inspect');assert.equal(result.reason,'security-unresolved');assert.equal(result.outcome,'probe-unresolved');
  assert.equal(result.noRetry,true);assert.equal(result.browserCreated,false);assert(!fs.existsSync(path.join(attempt,'health-attempts.json')));
  assert.equal(stats.phase,'closed');assert.equal(stats.cleanStop,true);assert.equal(stats.peakSockets,1);
  for(const key of ['acceptedPairs','activePairs','peakPairs','receivedBytes','forwardedBytes','peakBufferedBytes','maximumPairBytes','refusedConnections','peerClosures'])assert.equal(stats[key],0);
  assert(Object.values(stats.violations).every(value=>value===0));assert(statsDecision(stats).ok);
  assert.equal(status.outcome,'probe-unresolved');assert.equal(status.status,'diagnostic-closed');assert.equal(status.exitCode,1);
  assert.equal(observed.healthGets,0);assert.equal(observed.browsers,0);assert.equal(observed.legendCases,0);
  const code=fs.readFileSync(path.join(attempt,'harness/probe.mjs'),'utf8');
  assert(code.indexOf("if(relay.kind!=='relay-admitted')fail(relay.kind)")<code.indexOf('await readiness('));
});
check('Recorded-ID/name cleanup and saved independent absence scope',()=>{
  assert.equal(cleanup.status,'cleaned');assert.equal(cleanup.failure,null);assert(absenceComplete(cleanup));assert.equal(cleanup.relayStopCompleted,true);
  for(const kind of ['relay','app','ingress','internal']){
    assert.deepEqual(cleanup.identities[kind],{basis:'recorded',recordedIdPresent:true,expectedNamePresent:true,idAbsent:true,nameAbsent:true});
    const key=kind+(kind==='relay'||kind==='app'?'Id':'NetworkId');assert(/^[a-f0-9]{64}$/.test(runtime[key]));
  }
  assert.equal(owned.status,'absence-verified');assert.equal(owned.readOnly,true);assert.equal(owned.commands,8);assert.equal(owned.failure,null);
  assert.deepEqual(owned.checks.map(item=>item.resource),['relay','app','ingress','internal']);
  assert(owned.checks.every(item=>item.recordedIdChecked&&item.expectedNameChecked&&item.idAbsent&&item.nameAbsent));
  assert(owned.stateAbsent&&owned.credentialAbsent);
  const stateName=runtime.statePath.split('/').at(-1);assert(/^state-[a-f0-9]{12}$/.test(stateName));
  assert(runtime.statePath.endsWith('/'+name+'/'+stateName));assert(!fs.existsSync(path.join(attempt,stateName)));assert(!fs.existsSync(path.join(attempt,'credential-private.json')));
});
const absenceUpperBoundMs=Date.parse(owned.checkedAtUtc)-Date.parse(helper.startTimeUtc);
check('Exact helper identity, exit and conservative lifecycle bound',()=>{
  assert.equal(helper.attempt,name);assert.equal(helper.processId,41536);assert.equal(helper.executable,'wsl.exe');assert(helper.hidden&&helper.helperAbsent);assert.equal(helper.exitCode,1);
  assert.equal(helperAbsent.processId,helper.processId);assert.equal(helperAbsent.expectedStartTimeTicks,helper.startTimeTicks);assert(helperAbsent.helperAbsent&&!helperAbsent.sameIdentityPresent&&helperAbsent.readOnly);
  assert.equal(watchdog.exitCode,1);assert.equal(watchdog.hardSeconds,150);assert.equal(absenceUpperBoundMs,69458);assert(absenceUpperBoundMs<150000);
  assert.equal(observed.resourceAbsenceUpperBoundMs,absenceUpperBoundMs);
});
const entries=[];
function inventory(directory){for(const item of fs.readdirSync(directory,{withFileTypes:true})){assert(!item.isSymbolicLink());const file=path.join(directory,item.name);if(item.isDirectory())inventory(file);else entries.push({path:path.relative(attempt,file).replaceAll('\\','/'),bytes:fs.statSync(file).size});}}
inventory(attempt);entries.sort((a,b)=>a.path.localeCompare(b.path));
const publicJson=entries.filter(item=>item.path.endsWith('.json')&&!item.path.endsWith('-private.json'));
const totals={files:entries.length,bytes:entries.reduce((sum,item)=>sum+item.bytes,0),publicJsonBytes:publicJson.reduce((sum,item)=>sum+item.bytes,0)};
check('Final inventory and raw inventory reconciliation within caps',()=>{
  assert.deepEqual(totals,{files:24,bytes:58083,publicJsonBytes:13236});
  const final=json(path.join(analysis,'attempt-inventory.json'));assert.deepEqual(final.entries,entries);assert.deepEqual(final.totals,totals);
  const raw=json(path.join(attempt,'final-output-inventory.json'));assert.equal(raw.totals.files+1,totals.files);
  assert.equal(raw.totals.bytes+bytes(path.join(attempt,'final-output-inventory.json')).length-4,totals.bytes);
  assert.equal(raw.entries.find(item=>item.path==='helper-launch.json').bytes,225);assert.equal(bytes(path.join(attempt,'helper-launch.json')).length,221);
  for(const item of raw.entries)if(item.path!=='helper-launch.json')assert.equal(item.bytes,entries.find(value=>value.path===item.path).bytes);
  assert(totals.files<=32&&totals.bytes<=2097152&&totals.publicJsonBytes<=524288);assert(publicJson.every(item=>item.bytes<=65536));
});
check('Public selection excludes private state/logs and concrete secret markers',()=>{
  for(const item of selection){
    assert(!item.sourcePath.endsWith('-private.json')&&!item.sourcePath.endsWith('.log'));
    const content=fs.readFileSync(path.join(root,item.sourcePath),'utf8');assert(!content.includes(runtime.ownership));
    assert(!/legend-probe-[a-f0-9]{12}@example\.com|Aa1![a-f0-9]{48}/.test(content));
    assert(!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}|AKIA[A-Z0-9]{16})\b/.test(content));
  }
  assert(bytes(path.join(base,'reviewed-evidence-publication-allowlist.json')).equals(bytes(path.join(analysis,'publication-allowlist.json'))));
});
let supplied;
check('Supplied verifier read-only pass and preserved frozen inputs',()=>{
  supplied=JSON.parse(execFileSync(process.execPath,[path.join(analysis,'verify-evidence.mjs')],{cwd:root,encoding:'utf8',windowsHide:true,maxBuffer:65536}));
  assert.equal(supplied.status,'passed');assert.equal(supplied.runtimeCalls,0);assert.equal(supplied.allowlistSha256,allowlistSha256);frozen();
});
const receipt={verdict:'APPROVED',scope:'Failed-attempt interpretation and exact publication selection; no topology or UI success',checks,groupedChecks:checks.length,
  allowlistSha256,executedFiles:8,selectedFiles:26,totals,resourceAbsenceUpperBoundMs:absenceUpperBoundMs,suppliedVerifier:supplied,
  liveDockerOrHelperQueriesRepeated:false,currentStateAndCredentialAbsenceChecked:true,runtimeExecuted:false,networkOpened:false,frozenInputsPreserved:true,
  secretScan:'Exact private ownership value, generated credential patterns and bounded common-token/private-key markers; not exhaustive for every secret format',
  command:'node artifacts/ui-parity-legend-relay-attempt-review/audit.mjs',exitCode:0};
if(process.argv.includes('--record'))fs.writeFileSync(path.join(base,'verification.json'),JSON.stringify(receipt,null,2)+'\n');
else assert.deepEqual(json(path.join(base,'verification.json')),receipt);
console.log(JSON.stringify({verdict:receipt.verdict,groupedChecks:checks.length,selectedFiles:26,runtimeExecuted:false}));
