import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const base=path.dirname(fileURLToPath(import.meta.url)),parent=path.dirname(base),project=path.resolve(parent,'../..'),attempt=parent+'/attempt-20261017T1615437-672fb2a3';
const sha=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex'),read=name=>JSON.parse(fs.readFileSync(attempt+'/'+name+'.json'));
const entry=file=>({sourcePath:path.relative(project,file).replaceAll('\\','/'),sha256:sha(file),bytes:fs.statSync(file).size});
const write=(name,value)=>fs.writeFileSync(base+'/'+name+'.json',JSON.stringify(value,null,2));
const samples=read('samples'),result=read('probe-result'),runtime=read('runtime-private'),run=read('run-status');
write('observations',{attempt:path.basename(attempt),outcome:result.outcome,rawResult:result,rawStatus:run,
  sourceManifest:entry(attempt+'/source-manifest.json'),selectedReceipt:entry(attempt+'/samples.json'),derived:true,
  samples:samples.map(sample=>({sample:sample.context.sample,plannedOffsetMs:sample.context.plannedOffsetMs,actualReadEndAfterRunMs:sample.context.elapsedSinceRunReturnMs,
    runtimeTarget:sample.runtime.target,configuredTarget:sample.configured.target,state:Object.fromEntries(['Status','Running','Restarting','Dead','ExitCode','OOMKilled','StartedAt','FinishedAt'].map(key=>[key,sample.state[key].value])),allOwnershipAndNetworkChecksTrue:sample.errors.length===0&&sample.security.containerIdMatched&&sample.security.labelMatched&&sample.security.exactNetwork&&sample.security.attachedNetworkCount===1&&Object.values(sample.security.network).every(Boolean)})),
  counters:{snapshots:samples.length,healthRequests:0,browserProcesses:0,containerInstances:1,ownedNetworks:1,restarts:0,recreations:0,basis:'Selected receipt classifications and exact executed source; no allocated port, so health call was unreachable'},
  conclusion:'Publication was not observed for this one running owned instance within the finite selected window. No unsupported-topology or root-cause claim.',noRetry:true,
  elapsedToCompletedWatchdogMs:Math.max(0,Math.round(fs.statSync(attempt+'/watchdog-status.json').mtimeMs-runtime.startedAt))});
const files=[];function scan(directory){for(const item of fs.readdirSync(directory,{withFileTypes:true})){const file=path.join(directory,item.name);if(item.isSymbolicLink())throw Error('Unexpected symlink');if(item.isDirectory())scan(file);else files.push(file);}}scan(attempt);
const selected=[],omitted=[];for(const file of files){if(file.endsWith('-private.json')||file.endsWith('.log'))omitted.push({path:path.relative(attempt,file).replaceAll('\\','/'),bytes:fs.statSync(file).size,reason:'Private runtime metadata or raw log; no contents selected'});else selected.push(entry(file));}
write('completed-output-inventory',{scope:'Fresh actual completed attempt scan after watchdog, including omitted file bytes',files:files.length,bytes:files.reduce((n,file)=>n+fs.statSync(file).size,0),selected,omitted});
write('publication-notes',{sanitization:'None for selected source/receipts: whitelist projection only. No raw private receipt or log is selected.',generatedCredentialsPublished:false,
  omitted,metadata:'The allowlist excludes itself; sourcePath/SHA256/bytes refer to exact original selected bytes',runtimeScope:'One no-browser diagnostic; no UI acceptance or grant extension'});
for(const name of ['observations.json','completed-output-inventory.json','publication-notes.json','owned-absence.json','launcher-absence.json','report.md','verify-owned-absence.mjs','verify-evidence.mjs','package-evidence.mjs'])selected.push(entry(base+'/'+name));
for(const f of selected){const text=fs.readFileSync(project+'/'+f.sourcePath,'utf8');if(text.includes(runtime.ownership)||/legend-probe-[a-f0-9]{12}@example\.com|Aa1![a-f0-9]{48}/.test(text))throw Error('Generated private value in publication selection');}
write('publication-allowlist',selected);
console.log(JSON.stringify({status:'diagnostic-evidence-frozen',selectedFiles:selected.length,physicalAttemptFiles:files.length,physicalAttemptBytes:files.reduce((n,file)=>n+fs.statSync(file).size,0),allowlistSha256:sha(base+'/publication-allowlist.json')}));
