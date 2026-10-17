import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const base=path.dirname(fileURLToPath(import.meta.url)),parent=path.dirname(base),attempt=parent+'/attempt-20261017T1549043-3a567782';
const project=path.resolve(parent,'../..'),sha=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const relative=file=>path.relative(project,file).replaceAll('\\','/');
const entry=file=>({sourcePath:relative(file),sha256:sha(file),bytes:fs.statSync(file).size});
const write=(name,value)=>fs.writeFileSync(base+'/'+name,JSON.stringify(value,null,2));
const read=name=>JSON.parse(fs.readFileSync(attempt+'/'+name+'.json'));
const runtime=read('runtime-private'),start=read('start-status'),run=read('run-status'),cleanup=read('cleanup-report'),watchdog=read('watchdog-status'),launch=read('launch');
const manifest=read('source-manifest');
for(const f of manifest.files)if(sha(attempt+'/'+f.path)!==f.sha256||fs.statSync(attempt+'/'+f.path).size!==f.bytes)throw Error('Executed copy changed '+f.path);
if(start.exitCode!==1||run.status!=='cleanup-unverified'||runtime.origin!==null||fs.existsSync(attempt+'/journey.log'))throw Error('Unexpected execution prefix');
const cases=Array.from({length:8},(_,i)=>({id:'L0'+(i+1),status:'not-run-admission',reason:'Startup stopped at loopback publication guard before journey launch',evidenceKind:'Offline derivation from supervisor source/start status; not a raw case observation'}));
write('cases.json',cases);
write('execution-receipt.json',{attempt:path.basename(attempt),outcome:'startup-admission-unresolved',reason:'network-isolation-unresolved: loopback publication',
  originalSource:runtime.source,image:runtime.image,candidateExecuted:false,providerChecksExecuted:false,browserJourneyLaunched:false,originalContainerCreated:true,
  rawStatuses:{start,cleanup:read('cleanup-status'),run,watchdog},
  counters:{chartActions:0,fieldMutations:0,events:0,observations:0,pngs:0,basis:'Derived from the source startup exit gate; no journey counter receipt exists'},
  sourceManifest:entry(attempt+'/source-manifest.json'),preparedSourceProof:entry(attempt+'/prepared-source-verification.json'),
  loopbackShape:{networkSettingsPorts3000Tcp:{status:'unobserved'},hostConfigPortBindings3000Tcp:{status:'unobserved'},reason:'The guard threw before inspect values were retained; container was removed. No recreation or probe performed.'},
  admittedOriginalOrigin:runtime.origin,health:runtime.health,
  cleanupInterpretation:'Raw status remains cleanup-unverified because no browser PID identity was recorded before startup failed. Fresh read-only evidence separately verifies absence of created container/network/state/credential/startup process.',
  launch:{hidden:launch.hidden,distro:launch.distro,user:launch.user,command:launch.command,windowsLauncherPid:launch.windowsLauncherPid},
  elapsedToWatchdogReceiptMs:Math.max(0,Math.round(fs.statSync(attempt+'/watchdog-status.json').mtimeMs-runtime.startedAt)),noRetry:true});
const derivatives=[];
for(const [raw,name] of [['start.log','start-failure.txt'],['cleanup.log','cleanup-failure.txt']]){
  const source=fs.readFileSync(attempt+'/'+raw,'utf8');
  if(source.length>8192)throw Error('Unexpected diagnostic length');
  const sanitized=source.replaceAll(attempt,'[owned-attempt]').replaceAll('/mnt/d/Source/QOpenBB','[workspace]').replaceAll('D:\\Source\\QOpenBB','[workspace]');
  fs.writeFileSync(base+'/'+name,sanitized);derivatives.push({source:entry(attempt+'/'+raw),published:entry(base+'/'+name),sanitization:'Owned absolute workspace/attempt paths replaced; diagnostic text otherwise retained',originalHashClaimedForDerivative:false});
}
write('sanitization.json',{derivatives,omitted:['runtime-private.json','all raw .log files','any state/credential/profile/environment/archive/cache data'],generatedCredentialsPublished:false});
const files=[];function scan(directory){for(const item of fs.readdirSync(directory,{withFileTypes:true})){const file=path.join(directory,item.name);if(item.isSymbolicLink())throw Error('Unexpected symlink');if(item.isDirectory())scan(file);else files.push(file);}}scan(attempt);
const omitted=[],eligible=[];for(const file of files){const name=path.relative(attempt,file).replaceAll('\\','/');
  if(name.endsWith('-private.json')||name.endsWith('.log'))omitted.push({path:name,bytes:fs.statSync(file).size,reason:'Raw private receipt or log; no contents selected'});else eligible.push(entry(file));}
write('completed-output-inventory.json',{scope:'Fresh scan of completed actual attempt after watchdog receipt; includes physical bytes of omitted files',files:files.length,bytes:files.reduce((n,file)=>n+fs.statSync(file).size,0),publicEligible:eligible,omitted});
const selected=[...eligible,...['report.md','cases.json','execution-receipt.json','sanitization.json','completed-output-inventory.json','owned-absence.json','start-failure.txt','cleanup-failure.txt','verify-owned-absence.mjs','verify-evidence.mjs','package-evidence.mjs'].map(name=>entry(base+'/'+name))];
write('publication-allowlist.json',selected);
console.log(JSON.stringify({status:'completed-failed-attempt-packaged',selectedFiles:selected.length,physicalAttemptFiles:files.length,physicalAttemptBytes:files.reduce((n,file)=>n+fs.statSync(file).size,0),allowlistSha256:sha(base+'/publication-allowlist.json')}));
