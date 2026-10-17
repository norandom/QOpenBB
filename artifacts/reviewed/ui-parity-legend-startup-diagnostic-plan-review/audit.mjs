import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import crypto from 'node:crypto';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../..'),source=root+'/artifacts/ui-parity-legend-startup-diagnostic-plan';
const read=p=>JSON.parse(fs.readFileSync(p)),sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),checks=[];
function check(name,value){checks.push({name,passed:!!value});if(!value)throw Error(name);}
const pins={'plan.md':'efa8a5f3befea5ea6ba5c2494a7370e93f663567c977236521574985f7316eb0','source-hashes.json':'2a25a9384c484712bc40e4629f4de2181c6d8bac2c44ad1656a23cb6084a51f2','publication-allowlist.json':'596b1f22568ba377966ede10786dad01a86a6c3b78b096a6cc35d3143ad500d7'};
for(const [name,hash] of Object.entries(pins))check('dispatch pin '+name,sha(source+'/'+name)===hash);
const manifest=read(source+'/source-hashes.json'),list=read(source+'/publication-allowlist.json'),contract=read(source+'/probe-contract.json');
for(const item of [...manifest.inputs,...manifest.sourceFiles,...list])check('hash and byte length '+item.sourcePath,sha(root+'/'+item.sourcePath)===item.sha256&&fs.statSync(root+'/'+item.sourcePath).size===item.bytes);
check('six unique publication content files',list.length===6&&new Set(list.map(x=>x.sourcePath)).size===6);
for(const item of list){check('safe selected text '+item.sourcePath,item.sourcePath.startsWith('artifacts/ui-parity-legend-startup-diagnostic-plan/')&&!item.sourcePath.includes('..')&&/\.(md|json|mjs)$/.test(item.sourcePath));
  const text=fs.readFileSync(root+'/'+item.sourcePath,'utf8');check('no concrete credentials or placeholders '+item.sourcePath,!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_-]{20,}|\b(?:TBD|TODO|FIXME|HACK|XXX)\b/.test(text));}
const start=fs.readFileSync(root+'/artifacts/ui-parity-legend-capture-redirect-guard/harness/start.mjs','utf8'),network=fs.readFileSync(root+'/artifacts/ui-parity-legend-capture-redirect-guard/harness/network.mjs','utf8');
check('image and original source match actual frozen startup',start.includes("const image='"+contract.image+"'")&&start.includes("const source='"+contract.originalSource+"'"));
check('same dynamic loopback launch and DNS flags',start.includes("'-p','127.0.0.1::3000'")&&start.includes("'--dns','127.0.0.1'"));
check('same internal bridge identity',start.includes("'--driver','bridge','--internal'")&&network.includes("network?.EnableIPv6!==false"));
check('one resource each zero browser/provider/restart',contract.resources.originalContainers===1&&contract.resources.ownedInternalNetworks===1&&contract.resources.browserProcesses===0&&contract.resources.providerRequests===0&&contract.resources.restarts===0&&contract.resources.recreations===0);
check('three fixed same-instance slots',contract.sampling.maximumSnapshots===3&&JSON.stringify(contract.sampling.targetOffsetsMsFromRunReturn)==='[0,1000,3000]'&&contract.sampling.sameOwnedContainerOnly);
check('preassert persistence and early stop',contract.sampling.persistBeforeAssertion&&contract.sampling.stopWhenDiscriminated&&!contract.sampling.readinessPolicy);
check('90+60=150 seconds with finite calls',contract.deadlinesMs.input===90000&&contract.deadlinesMs.cleanup===60000&&contract.deadlinesMs.input+contract.deadlinesMs.cleanup===contract.deadlinesMs.hard&&contract.deadlinesMs.hard===150000&&contract.deadlinesMs.dockerCommand===5000&&contract.deadlinesMs.healthRequest===2000);
check('bounded output ceilings',contract.outputs.retainedFiles===32&&contract.outputs.perPublicJsonBytes===65536&&contract.outputs.publicJsonTotalBytes===524288&&contract.outputs.retainedTotalBytes===2097152&&contract.outputs.portEntriesPerTargetArray===4&&contract.outputs.stringChars===128);
check('exact eight State leaf selection',JSON.stringify(contract.selectedPaths.filter(x=>x.startsWith('State.')))===JSON.stringify(['State.Status','State.Running','State.Restarting','State.Dead','State.ExitCode','State.OOMKilled','State.StartedAt','State.FinishedAt']));
check('one health with no redirect/retry/body retention',contract.sampling.maximumHealthRequests===1&&contract.http.method==='GET'&&contract.http.endpoint==='/api/health'&&contract.http.maxRedirects===0&&contract.http.maxRetries===0&&contract.http.rejectAny3xx&&contract.http.rejectAnyLocation&&contract.http.exactValidatedLoopbackOriginOnly&&contract.forbiddenReceipts.includes('HTTP headers')&&contract.forbiddenReceipts.includes('HTTP bodies'));
check('private inspect fields explicitly excluded', ['Config.Env','Config.Cmd','Config.Entrypoint','full Config.Labels','State.Error','State.Health','full inspect JSON','container logs','credentials'].every(x=>contract.forbiddenReceipts.includes(x)));
check('separate source and runtime gates',contract.gates.includes('independent exact collector-source review')&&contract.gates.includes('separate controller one-probe grant')&&contract.runtimeExecuted===false&&contract.checksExecuted.includes('probe tests are planned'));
const text=fs.readFileSync(source+'/plan.md','utf8'),links=[];
for(const m of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){check('source link '+m[1],fs.existsSync(path.resolve(source,m[1].split('#')[0])));links.push(m[1]);}
check('selected receipt output is bounded before assertions',text.includes('256-KiB command-output bound')&&text.includes('persists it successfully before any publication/state assertion'));
check('same topology stopping rules explicit',text.includes('Only a missing runtime allocation with an otherwise valid configured target and still-running verified instance')&&text.includes('Wrong ownership, a broad host binding or an extra network stops immediately'));
check('exact owned cleanup and conservative missing proof',text.includes('exact name, ID and selected ownership label match')&&text.includes('Refuse cleanup of any mismatched or still-shared resource')&&text.includes('Missing proof never becomes a pass'));
check('plan does not upgrade prior failure',text.includes('that changes no status in the already failed Legend run')&&text.includes('A diagnostic result cannot automatically grant a full UI attempt'));
check('minimal responsibilities no browser framework',text.includes('harness/probe.mjs')&&text.includes('harness/cleanup.mjs')&&text.includes('harness/run.sh')&&text.includes('do not introduce a generic discovery, polling or state framework'));
for(const [name,hash] of Object.entries(pins))check('frozen proposal preserved '+name,sha(source+'/'+name)===hash);
const result={date:'2026-10-17',verdict:'APPROVED',scope:'Narrow source-plan and exact publication review only; no implementation or runtime grant',pins,command:'node artifacts/ui-parity-legend-startup-diagnostic-plan-review/audit.mjs',exitCode:0,checks:checks.length,runtimeExecuted:false,probeTestsExecuted:false,
  suppliedFreeze:{command:'node artifacts/ui-parity-legend-startup-diagnostic-plan/freeze-plan.mjs',exitCode:0,protectedWrites:'three exact-equal frozen writes suppressed'},publication:{contentFiles:6,metadataFiles:1,links,actualDestinationAudit:'required after synchronization'},
  findings:[],downstreamGates:['Exact implemented projection/persistence/fault tests','Finite command/time/output enforcement and exact owned cleanup','Independent exact-source review','Separate controller one-probe grant','Independent interpretation of diagnostic evidence'],results:checks};
fs.writeFileSync(here+'/verification.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,results:undefined}));
