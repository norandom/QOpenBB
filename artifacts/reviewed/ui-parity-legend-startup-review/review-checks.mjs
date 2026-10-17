import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
const own=path.dirname(fileURLToPath(import.meta.url)),repo=path.resolve(own,'../..');
const parent=path.join(repo,'artifacts/ui-parity-legend-capture-redirect-guard'),id='attempt-20261017T1549043-3a567782',attempt=parent+'/'+id,analysis=parent+'/analysis-'+id;
const read=p=>JSON.parse(fs.readFileSync(p)),sha=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const entry=p=>({sourcePath:path.relative(repo,p).replaceAll('\\','/'),sha256:sha(p),bytes:fs.statSync(p).size});
const allowed=read(analysis+'/publication-allowlist.json'),before=allowed.map(f=>entry(path.join(repo,f.sourcePath)));
assert.equal(sha(attempt+'/source-manifest.json'),'9ba3ebf7976b2fc8f0a027fd2823c93365cba5e297de5d988311da7c405f4531');
assert.equal(sha(parent+'/source-hashes.json'),'5b0674b7aae4e0a7c9e26fb26b7009def4e42fb73ed67865a31d71b34c502704');
const manifest=read(attempt+'/source-manifest.json');assert.equal(manifest.files.length,21);
for(const f of manifest.files){assert.equal(sha(attempt+'/'+f.path),f.sha256);assert.equal(fs.statSync(attempt+'/'+f.path).size,f.bytes);assert.equal(sha(attempt+'/'+f.path),sha(parent+'/'+f.path));}
for(const f of allowed){assert.equal(sha(path.join(repo,f.sourcePath)),f.sha256);assert.equal(fs.statSync(path.join(repo,f.sourcePath)).size,f.bytes);assert(!/-private\.json$|\.log$|\/(?:state-|\.env)|\.(?:zip|tar|gz)$/i.test(f.sourcePath));}
const execution=read(analysis+'/execution-receipt.json'),cleanup=read(attempt+'/cleanup-report.json'),run=read(attempt+'/run-status.json'),absence=read(analysis+'/owned-absence.json');
for(const [key,name] of [['start','start-status'],['cleanup','cleanup-status'],['run','run-status'],['watchdog','watchdog-status']])assert.deepEqual(execution.rawStatuses[key],read(attempt+'/'+name+'.json'));
assert.equal(run.status,'cleanup-unverified');assert.equal(run.cleanupVerified,false);assert.equal(run.eventAccountingVerified,false);
assert.equal(cleanup.browser.identityRecorded,false);assert.equal(cleanup.browser.browserProcessAbsent,false);assert.equal(cleanup.browserError,'browser-identity-unresolved: missing receipt');
for(const key of ['containerAbsent','networkAbsent','stateAbsent','credentialAbsent'])assert.equal(cleanup[key],true);
for(const key of ['containerAbsent','networkAbsent','stateAbsent','credentialAbsent','startupProcessAbsent','browserIdentityReceiptAbsent','journeyStatusAbsent','journeyLogAbsent','ownedInfrastructureAbsenceVerified'])assert.equal(absence[key],true);
const runtime=read(attempt+'/runtime-private.json');
assert(/^[a-f0-9]{64}$/.test(runtime.container));assert(/^[a-f0-9]{64}$/.test(runtime.networkId));assert.equal(runtime.origin,null);assert.equal(runtime.health,null);
assert.equal(runtime.source,execution.originalSource);assert.equal(runtime.image,execution.image);
assert(!fs.existsSync(attempt+'/'+path.basename(runtime.statePath)));assert(!fs.existsSync(attempt+'/credential-private.json'));
const shell=fs.readFileSync(attempt+'/harness/run.sh','utf8');
const startupGate='if [ "$status" != 0 ]; then exit "$status"; fi';assert(shell.includes(startupGate));assert(shell.indexOf(startupGate)<shell.indexOf('node "$harness/journey.mjs"'));
for(const name of ['journey-status.json','journey.log','owned-browser-private.json','browser-cleanup.json','summary.json','counters.json'])assert(!fs.existsSync(attempt+'/'+name),name);
assert.equal(execution.browserJourneyLaunched,false);assert.equal(execution.originalContainerCreated,true);assert.equal(execution.noRetry,true);
assert.equal(execution.loopbackShape.networkSettingsPorts3000Tcp.status,'unobserved');assert.equal(execution.loopbackShape.hostConfigPortBindings3000Tcp.status,'unobserved');
const cases=read(analysis+'/cases.json');assert.deepEqual(cases.map(c=>c.id),Array.from({length:8},(_,i)=>'L0'+(i+1)));assert(cases.every(c=>c.status==='not-run-admission'&&c.evidenceKind.includes('Offline derivation')));
for(const key of ['chartActions','fieldMutations','events','observations','pngs'])assert.equal(execution.counters[key],0);
const inventory=read(analysis+'/completed-output-inventory.json'),physical=[];
function walk(dir){for(const item of fs.readdirSync(dir,{withFileTypes:true})){assert(!item.isSymbolicLink());const p=path.join(dir,item.name);if(item.isDirectory())walk(p);else physical.push(p);}}walk(attempt);
assert.equal(physical.length,inventory.files);assert.equal(physical.reduce((n,p)=>n+fs.statSync(p).size,0),inventory.bytes);
assert.equal(inventory.publicEligible.length+inventory.omitted.length,physical.length);
for(const f of inventory.publicEligible){const p=path.join(repo,f.sourcePath);assert.equal(sha(p),f.sha256);assert.equal(fs.statSync(p).size,f.bytes);}
for(const f of inventory.omitted)assert.equal(fs.statSync(attempt+'/'+f.path).size,f.bytes);
for(const d of read(analysis+'/sanitization.json').derivatives){
  const raw=path.join(repo,d.source.sourcePath),published=path.join(repo,d.published.sourcePath);assert.equal(sha(raw),d.source.sha256);assert.equal(sha(published),d.published.sha256);assert.notEqual(d.source.sha256,d.published.sha256);assert.equal(d.originalHashClaimedForDerivative,false);
  const sanitized=fs.readFileSync(raw,'utf8').replaceAll(attempt,'[owned-attempt]').replaceAll('/mnt/d/Source/QOpenBB','[workspace]').replaceAll('D:\\Source\\QOpenBB','[workspace]');assert.equal(sanitized,fs.readFileSync(published,'utf8'));
}
assert(fs.readFileSync(analysis+'/start-failure.txt','utf8').includes('network-isolation-unresolved: loopback publication'));
const independent=spawnSync(process.execPath,[analysis+'/verify-evidence.mjs'],{encoding:'utf8',windowsHide:true});assert.equal(independent.status,0,independent.stderr);
assert.deepEqual(allowed.map(f=>entry(path.join(repo,f.sourcePath))),before);
const report={date:'2026-10-17',command:'node artifacts/ui-parity-legend-startup-review/review-checks.mjs',node:process.version,exitCode:0,scope:'Read-only filesystem/source review of completed failed attempt; no runtime, Docker, process or network probe',attempt:id,sourceManifest:entry(attempt+'/source-manifest.json'),analysisAllowlist:entry(analysis+'/publication-allowlist.json'),sourceCopiesMatched:21,selectedFilesVerified:allowed.length,selectedBytes:allowed.reduce((n,f)=>n+f.bytes,0),actualAttemptInventory:{files:physical.length,bytes:inventory.bytes,includesOmittedPhysicalBytes:true},rawStatusesPreserved:execution.rawStatuses,browserNonLaunch:{sourceGateVerified:true,journeyEvidenceAbsent:true,claim:'Supported by exact supervisor source, nonzero start receipt and absent journey outputs; no universal process-absence claim'},casesNotRun:cases.map(c=>c.id),zeroCountersDerivedNotRaw:true,portBindingValues:'Both NetworkSettings.Ports and HostConfig.PortBindings unobserved; root cause unresolved',ownedAbsenceReceipt:{...entry(analysis+'/owned-absence.json'),checkedAt:absence.checkedAt,interpretation:'Reviewed stored exact-resource absence observation; no independent live Docker/process probe performed in this review'},sanitizedDerivativesReproduced:true,providedOfflineVerifier:{exitCode:independent.status,result:JSON.parse(independent.stdout.trim())},frozenSelectedFilesUnchanged:true,publicationVerdict:'Approved exact selected failure evidence; no success/cleanup upgrade, retry or runtime grant',selected:allowed};
fs.writeFileSync(own+'/verification.json',JSON.stringify(report,null,2)+'\n');fs.writeFileSync(own+'/reviewed-evidence-publication-allowlist.json',fs.readFileSync(analysis+'/publication-allowlist.json'));
console.log(JSON.stringify({sourceCopies:21,selectedFiles:allowed.length,physicalAttemptFiles:physical.length,physicalAttemptBytes:inventory.bytes,casesNotRun:8,rawStatus:'cleanup-unverified',safePublication:true,noRuntimeOrRetry:true}));
