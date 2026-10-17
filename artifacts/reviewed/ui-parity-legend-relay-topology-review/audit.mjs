import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {admitContainer,networkValid,statsDecision} from '../ui-parity-legend-relay-mount-source/harness/admission.mjs';
import {absenceComplete} from '../ui-parity-legend-relay-mount-source/harness/cleanup.mjs';
const base=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(base,'../..');
const source=path.join(root,'artifacts/ui-parity-legend-relay-mount-source'),name='attempt-20261017T1717176-4b3330da';
const attempt=path.join(source,name),analysis=path.join(source,'analysis-'+name);
const read=file=>fs.readFileSync(file),json=file=>JSON.parse(read(file)),hash=file=>createHash('sha256').update(read(file)).digest('hex');
const selection=json(path.join(analysis,'publication-allowlist.json')),selectionHash='289fa688884eef931aa9e9d2308c74ee2eb9b8c9a41db7c1e2900736f7ba0721';
const checks=[];function check(title,body){body();checks.push(title);}
function verify(file,digest,size){assert.equal(hash(file),digest,file);if(size!==undefined)assert.equal(read(file).length,size,file);}
function frozen(){
  verify(path.join(analysis,'publication-allowlist.json'),selectionHash);
  verify(path.join(analysis,'report.md'),'9e64e9ab0008c37ef629064c33eaf1d0cdc28e94c832338afce92489aa6bd7a5');
  assert.equal(selection.length,27);assert.equal(new Set(selection.map(item=>item.sourcePath)).size,27);
  for(const item of selection){assert(!item.sourcePath.includes('..'));const file=path.join(root,item.sourcePath);assert(!fs.lstatSync(file).isSymbolicLink());verify(file,item.sha256,item.bytes);}
  verify(path.join(source,'source-hashes.json'),'64eecc7260f1c9a269cffe919f73405fda94d645b9667705072402a0ea4019c2');
  for(const item of json(path.join(source,'source-hashes.json')).sourceFiles)verify(path.join(source,item.path),item.sha256,item.bytes);
  verify(path.join(root,'artifacts/ui-parity-legend-relay-mount-source-review/review.md'),'9c4ae8a35203fec6e2c9f3a68d3af76127fe9a37d33f5ebc73f1ac6e59db889f');
}
check('Exact source/review/evidence identities and publication bytes',frozen);
const admission=json(path.join(attempt,'admission-receipts.json')),app=admission.containers.app,relay=admission.containers.relay;
const health=json(path.join(attempt,'health-attempts.json')),stats=json(path.join(attempt,'relay-stats.json'));
const result=json(path.join(attempt,'probe-result.json')),status=json(path.join(attempt,'run-status.json')),cleanup=json(path.join(attempt,'cleanup-report.json'));
const helper=json(path.join(attempt,'helper-launch.json')),helperAbsence=json(path.join(analysis,'fresh-helper-absence.json')),owned=json(path.join(analysis,'fresh-owned-absence.json'));
const runtime=json(path.join(attempt,'runtime-private.json')),observed=json(path.join(analysis,'observations.json'));
check('Eight exact executed files, configuration hash and unchanged finite profile',()=>{
  verify(path.join(attempt,'source-manifest.json'),'b03ba2f0939a637d02937326caa24b1287514d6463efd369fa67361c53e99831');
  const manifest=json(path.join(attempt,'source-manifest.json'));assert.equal(manifest.files.length,8);
  for(const item of manifest.files)verify(path.join(attempt,item.path),item.sha256,item.bytes);
  const prep=json(path.join(attempt,'preparation.json'));assert(prep.exactCopies&&!prep.runtimeStarted);assert.equal(prep.manifestSha256,hash(path.join(attempt,'source-manifest.json')));
  verify(path.join(attempt,'relay-config.json'),admission.config.sha256);assert.deepEqual(json(path.join(attempt,'relay-config.json')),{upstreamIPv4:app.internalIPv4,upstreamPort:3000});
  const contract=json(path.join(source,'probe-contract.json'));assert.deepEqual(contract.deadlinesMs,{input:90000,cleanup:60000,hard:150000});assert.equal(contract.resources.browserProcesses,0);assert.equal(contract.resources.restarts,0);assert.equal(contract.resources.recreations,0);
});
check('Actual admission decisions and selected topology/mount operands',()=>{
  assert(Object.values(admission.networks).every(networkValid));assert.equal(admitContainer(app).kind,'app-admitted');assert.deepEqual(admitContainer(relay),{kind:'relay-admitted',port:'32808'});
  for(const receipt of [app,relay]){assert(Object.values(receipt.security).every(value=>value===true));assert.deepEqual(receipt.state,{Status:'running',Running:true,Restarting:false,Dead:false,ExitCode:0,OOMKilled:false});}
  assert(app.noConfiguredPublications&&app.noRuntimePublications);assert.deepEqual(relay.runtime.entries,[{HostIp:'127.0.0.1',HostPort:'32808'}]);
  const rows=relay.selected.Mounts.entries.map(item=>[item.Destination.value,item.Type.value,item.RW.value,item.Source.ownedPathMatched]);
  assert.deepEqual(rows,[['/relay/relay.py','bind',false,true],['/relay/config.json','bind',false,true],['/evidence/relay-stats.json','bind',true,true]]);
  const tmpfs=relay.selected.Tmpfs;assert(tmpfs.parentSupported&&tmpfs.dataOwn);assert.equal(tmpfs.keyCount,1);assert.equal(tmpfs.unexpectedKeyCount,0);assert.equal(tmpfs.data.value,'rw,nosuid,nodev,size=1048576');assert.deepEqual(observed.configuredTmpfs,tmpfs);
});
check('Ten finite health starts, failed prefix and final 200 only',()=>{
  assert.deepEqual(health.map(item=>item.index),[1,2,3,4,5,6,7,8,9,10]);
  assert.deepEqual(health.map(item=>item.startedMs),[147,3148,6149,9150,12151,15153,18153,21153,24155,27155]);
  for(let index=1;index<health.length;index++)assert(health[index].startedMs-health[index-1].startedMs>=3000);
  assert(health.at(-1).startedMs+2000<30000);
  assert(health.slice(0,5).every(item=>item.outcome==='health-unresolved'&&item.reason==='health-transport-or-timeout'&&!Object.hasOwn(item,'status')));
  assert(health.slice(5,9).every(item=>item.outcome==='health-unresolved'&&item.status===502));assert.equal(health[9].status,200);assert.equal(health[9].outcome,'loopback-healthy');
  assert.deepEqual(observed.health,health);assert.equal(result.outcome,'readiness-observed');assert.equal(result.attempts,10);assert(result.noRetry&&!result.browserCreated);
  const code=fs.readFileSync(path.join(attempt,'harness/admission.mjs'),'utf8');assert(code.includes("redirect:'manual'"));assert(code.includes('AbortSignal.timeout'));assert(code.includes("response.headers.has('location')"));
});
check('Admitted counter/status result with explicit byte-delivery limitation',()=>{
  assert(statsDecision(stats).ok);assert.equal(stats.phase,'closed');assert(stats.cleanStop);assert.equal(stats.acceptedPairs,10);assert.equal(stats.activePairs,0);assert.equal(stats.peakPairs,1);assert.equal(stats.peakSockets,3);assert.equal(stats.refusedConnections,5);
  assert.equal(stats.receivedBytes,2929);assert.equal(stats.forwardedBytes,2404);assert.equal(stats.receivedBytes-stats.forwardedBytes,525);assert(Object.values(stats.violations).every(value=>value===0));
  assert.deepEqual(observed.relayStats,stats);assert.equal(observed.receivedMinusForwardedBytes,525);assert.equal(observed.byteCompletenessClaimed,false);assert.equal(observed.browsers,0);assert.equal(observed.legendCases,0);
  assert.equal(status.outcome,'topology-probe-passed');assert.equal(status.status,'diagnostic-closed');assert.equal(status.exitCode,0);assert.equal(status.logOverflow,false);assert.deepEqual(status.relay,statsDecision(stats));
});
const resourceBound=Date.parse(owned.checkedAtUtc)-Date.parse(helper.startTimeUtc),helperBound=Date.parse(helperAbsence.checkedAtUtc)-Date.parse(helper.startTimeUtc);
check('Saved exact-resource/helper cleanup proof and current local absence',()=>{
  assert(absenceComplete(cleanup));assert.equal(cleanup.status,'cleaned');assert.equal(cleanup.failure,null);assert.equal(cleanup.relayStopCompleted,true);
  for(const kind of ['relay','app','ingress','internal'])assert.deepEqual(cleanup.identities[kind],{basis:'recorded',recordedIdPresent:true,expectedNamePresent:true,idAbsent:true,nameAbsent:true});
  assert.equal(owned.commands,8);assert.equal(owned.status,'absence-verified');assert.equal(owned.failure,null);assert(owned.readOnly&&owned.stateAbsent&&owned.credentialAbsent);
  assert.deepEqual(owned.checks.map(item=>item.resource),['relay','app','ingress','internal']);assert(owned.checks.every(item=>item.recordedIdChecked&&item.expectedNameChecked&&item.idAbsent&&item.nameAbsent));
  assert.equal(helper.processId,5044);assert.equal(helper.exitCode,0);assert(helper.hidden&&helper.helperAbsent);assert.equal(helperAbsence.processId,helper.processId);assert.equal(helperAbsence.expectedStartTimeTicks,helper.startTimeTicks);assert(helperAbsence.helperAbsent&&!helperAbsence.sameIdentityPresent&&helperAbsence.readOnly);
  assert.equal(resourceBound,62469);assert.equal(helperBound,62525);assert(resourceBound<150000&&helperBound<150000);
  const watchdog=json(path.join(attempt,'watchdog-status.json'));assert.equal(watchdog.exitCode,0);assert.equal(watchdog.hardSeconds,150);
  const state=runtime.statePath.split('/').at(-1);assert(/^state-[a-f0-9]{12}$/.test(state));assert(runtime.statePath.endsWith('/'+name+'/'+state));assert(!fs.existsSync(path.join(attempt,state)));assert(!fs.existsSync(path.join(attempt,'credential-private.json')));
});
const entries=[];function inventory(directory){for(const item of fs.readdirSync(directory,{withFileTypes:true})){assert(!item.isSymbolicLink());const file=path.join(directory,item.name);if(item.isDirectory())inventory(file);else entries.push({path:path.relative(attempt,file).replaceAll('\\','/'),bytes:fs.statSync(file).size});}}
inventory(attempt);entries.sort((a,b)=>a.path.localeCompare(b.path));
const publicJson=entries.filter(item=>item.path.endsWith('.json')&&!item.path.endsWith('-private.json')),totals={files:entries.length,bytes:entries.reduce((sum,item)=>sum+item.bytes,0),publicJsonBytes:publicJson.reduce((sum,item)=>sum+item.bytes,0)};
let inventoryAdjustment;
check('Actual finite inventory reconciles earlier inventory and launcher update',()=>{
  assert.equal(totals.files,25);assert.equal(totals.bytes,62626);assert.deepEqual(json(path.join(analysis,'attempt-inventory.json')).entries,entries);assert.deepEqual(json(path.join(analysis,'attempt-inventory.json')).totals,totals);
  assert(totals.files<=32&&totals.bytes<=2097152&&totals.publicJsonBytes<=524288);assert(publicJson.every(item=>item.bytes<=65536));
  const raw=json(path.join(attempt,'final-output-inventory.json')),helperBefore=raw.entries.find(item=>item.path==='helper-launch.json').bytes,helperAfter=read(path.join(attempt,'helper-launch.json')).length,inventoryBytes=read(path.join(attempt,'final-output-inventory.json')).length;
  assert.equal(raw.totals.files+1,totals.files);assert.equal(raw.totals.bytes+inventoryBytes+helperAfter-helperBefore,totals.bytes);
  for(const item of raw.entries)if(item.path!=='helper-launch.json')assert.equal(item.bytes,entries.find(value=>value.path===item.path).bytes);
  inventoryAdjustment={rawBytes:raw.totals.bytes,inventoryBytes,helperBefore,helperAfter};
});
check('Exact safe selection, private exclusion and bounded token scan',()=>{
  for(const item of selection){assert(!item.sourcePath.endsWith('-private.json')&&!item.sourcePath.endsWith('.log'));const value=fs.readFileSync(path.join(root,item.sourcePath),'utf8');assert(!value.includes(runtime.ownership));assert(!/legend-probe-[a-f0-9]{12}@example\.com|Aa1![a-f0-9]{48}/.test(value));assert(!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}|AKIA[A-Z0-9]{16})\b/.test(value));}
  assert(read(path.join(base,'reviewed-evidence-publication-allowlist.json')).equals(read(path.join(analysis,'publication-allowlist.json'))));
});
let supplied;
check('Supplied read-only verification and final frozen preservation',()=>{supplied=JSON.parse(execFileSync(process.execPath,[path.join(analysis,'verify-evidence.mjs')],{cwd:root,encoding:'utf8',windowsHide:true,maxBuffer:65536}));assert.equal(supplied.status,'passed');assert.equal(supplied.checks,13);assert.equal(supplied.runtimeCalls,0);assert.equal(supplied.allowlistSha256,selectionHash);frozen();});
const receipt={verdict:'APPROVED',scope:'Observed final health/topology and recorded cleanup only; no opaque-byte completeness or full UI capacity',selectionHash,checks,groupedChecks:checks.length,totals,inventoryAdjustment,resourceAbsenceUpperBoundMs:resourceBound,helperAbsenceUpperBoundMs:helperBound,byteDifference:525,suppliedVerifier:supplied,
  liveDockerOrHelperQueriesRepeated:false,currentLocalStateAndCredentialAbsenceChecked:true,runtimeExecuted:false,networkOpened:false,frozenInputsPreserved:true,command:'node artifacts/ui-parity-legend-relay-topology-review/audit.mjs',exitCode:0};
if(process.argv.includes('--record'))fs.writeFileSync(path.join(base,'verification.json'),JSON.stringify(receipt,null,2)+'\n');else assert.deepEqual(json(path.join(base,'verification.json')),receipt);
console.log(JSON.stringify({verdict:receipt.verdict,groupedChecks:checks.length,selectedFiles:27,totals,runtimeExecuted:false}));
