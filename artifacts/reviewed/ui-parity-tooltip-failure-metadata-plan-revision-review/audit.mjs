import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../..'),base=root+'/artifacts/ui-parity-tooltip-failure-metadata-plan-revised';
const read=p=>JSON.parse(fs.readFileSync(p)),sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),checks=[];
function check(name,value){checks.push({name,passed:!!value});if(!value)throw Error(name);}
const pins={'plan.md':'248354c82919366fec8c440b3a2f298f715a069bb6de7b96434a948baf527257','source-hashes.json':'e4e0f5dc1babce58dcc3b2d3ac92ed5550f295612b7a10514951d459787c4f9d','publication-allowlist.json':'7a7c512988059bbee6e2a1c4a1a9184bc5dcfc7645c4aae87936a605c35e9ba2'};
for(const [name,hash] of Object.entries(pins))check('frozen dispatch pin '+name,sha(base+'/'+name)===hash);
const manifest=read(base+'/source-hashes.json'),list=read(base+'/publication-allowlist.json');
for(const item of [...manifest.inputs,...list])check('hash and bytes '+item.sourcePath,sha(root+'/'+item.sourcePath)===item.sha256&&fs.statSync(root+'/'+item.sourcePath).size===item.bytes);
check('exact13inputs4contentfiles',manifest.inputs.length===13&&list.length===4&&new Set(list.map(x=>x.sourcePath)).size===4);
const plan=fs.readFileSync(base+'/plan.md','utf8'),original=fs.readFileSync(root+'/artifacts/ui-parity-tooltip-failure-metadata-plan/plan.md','utf8');
const formatter=text=>text.slice(text.indexOf('## Smallest policy'),text.indexOf('## Retain the first'));
check('formatter512policy unchanged',formatter(plan)===formatter(original));
check('F01 all4outcomes explicit',['`succeeded`','`rejected-prior-prefix`','`not-attempted`','`write-unverified`'].every(x=>plan.includes(x)));
check('F01 unknown stage conservatively unverified',plan.includes('If the current catch cannot prove the stage, choose `write-unverified`')&&plan.includes('exception text alone does not establish that'));
check('F01 prewrite guarantee is stage-specific',plan.includes('before `fs.writeFileSync` was invoked')&&plan.includes('no prefix-preservation claim is allowed'));
check('F02 existing firstCaseFailure copied when applicable',plan.includes('include exactly one `firstCaseFailure` object containing those existing four bounded fields')&&plan.includes('without re-extracting the exception or copying ledger/tooltip data'));
check('F02 wrapper accounted separate from1024objectbytes',plan.includes('not a 1,024-byte total receipt')&&plan.includes('its property key, braces/comma and the whole receipt'));
check('F02 durable claims require successful containing write',plan.includes('The first failure is only claimed persisted if a containing write succeeds')&&plan.includes('A standalone receipt can itself be rejected or partially written'));
check('source/runtime/reserve boundary unchanged',plan.includes('32,768-byte input reservation')&&plan.includes('115,072-byte guard')&&plan.includes('16,000-byte final tail')&&plan.includes('131,072-byte case ceiling')&&plan.includes('no scaffold proof is claimed complete')&&plan.includes('no collector edit or runtime is authorized here'));
const links=[];for(const match of plan.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){check('link '+match[1],fs.existsSync(path.resolve(base,match[1].split('#')[0])));links.push(match[1]);}
for(const item of list){check('safe owned text '+item.sourcePath,item.sourcePath.startsWith('artifacts/ui-parity-tooltip-failure-metadata-plan-revised/')&&!item.sourcePath.includes('..')&&/\.(md|json)$/.test(item.sourcePath));
  check('no concrete secret or placeholder '+item.sourcePath,!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_-]{20,}|\b(?:TBD|TODO|FIXME|HACK|XXX)\b/.test(fs.readFileSync(root+'/'+item.sourcePath,'utf8')));}
const result={date:'2026-10-17',verdict:'APPROVED',scope:'Targeted F01/F02 plan closure and exact publication only; no implementation or runtime grant',pins,command:'node artifacts/ui-parity-tooltip-failure-metadata-plan-revision-review/audit.mjs',exitCode:0,checks:checks.length,runtimeExecuted:false,implementationExecuted:false,findingsClosed:['F01','F02'],scaffoldProofCompleted:false,reservationReduced:false,publication:{contentFiles:4,metadataFiles:1,links,destinationAudit:'required after synchronization'},results:checks};
fs.writeFileSync(here+'/verification.json',JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({...result,results:undefined}));
