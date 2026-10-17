import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,path.basename(path.dirname(here))==='reviewed'?'../../..':'../..');
const prefix='artifacts/ui-parity-legend-ui-relay-capacity-review/';
const source='artifacts/ui-parity-legend-ui-relay-capacity/';
const read=p=>fs.readFileSync(path.join(root,p));
const sha=b=>createHash('sha256').update(b).digest('hex');
const json=p=>JSON.parse(read(p));
const write=(name,value)=>fs.writeFileSync(path.join(here,name),JSON.stringify(value,null,2)+'\n');
const checks=[];
function check(name,value){assert.ok(value,name);checks.push({name,passed:true});}
check('requested proposal pin',sha(read(source+'proposal.md'))==='6cbc7954d4f60a75eb9c682c368bf6fcf57f0674868a8d98cf75b02c0c93d733');
check('requested allowlist pin',sha(read(source+'publication-allowlist.json'))==='91514cf9098958482e4ac1ea08c8b34348ec483f188c0e9dda59de08972e12af');
const selection=json(source+'publication-allowlist.json');
check('six proposal files',selection.length===6);
for(const pin of [...selection,...json(source+'source-hashes.json').sourceInputs]){
  const bytes=read(pin.sourcePath);check('pin '+pin.sourcePath,bytes.length===pin.bytes&&sha(bytes)===pin.sha256);
}
for(const pin of selection)check('bounded scan '+pin.sourcePath,!/\b(?:TODO|TBD|FIXME|HACK|XXX)\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{30,}/.test(read(pin.sourcePath).toString()));
const c=json(source+'capacity-contract.json'),m=json(source+'measurements.json');
check('envelope arithmetic',m.sizing.envelopeBytes===31997430+320*5+25473168);
check('pair arithmetic',2*m.sizing.envelopeBytes+16777216===131721612&&c.relay.maximumBytesPerPairBothDirections===134217728);
check('total arithmetic',4*m.sizing.envelopeBytes+33554432===263443224&&c.relay.maximumTotalBytesBothDirections===268435456);
check('pair count arithmetic',4*(320+133)+2100===3912&&c.relay.maximumAcceptedPairs===4096);
check('socket and queue caps',c.relay.maximumConcurrentPairs===16&&c.relay.maximumTcpSocketsIncludingListener===33&&c.relay.maximumQueuedPayloadBytes===2097152&&c.relay.bufferBytesPerDirection===65536);
assert.deepEqual(c.lifecycleMs,{startup:180000,journey:1920000,stopInput:2100000,cleanup:120000,hard:2220000});check('lifecycle exact',true);
const limits=await import(pathToFileURL(path.join(root,'artifacts/ui-parity-legend-capture-redirect-guard/harness/limits.mjs')).href);
for(const [field,key] of Object.entries({chartActions:'actions',fieldMutations:'changes',events:'events',pngs:'pngs',totalBytes:'total',retainedFiles:'files',jsonBytes:'jsonTotal',observations:'observations',selectedNodesPerObservation:'nodes',admissionActions:'admission'}))check('unchanged '+field,c.unchangedEvidence[field]===limits.limits[key]);
check('no execution claim',c.runtimeExecuted===false&&c.implementationPrepared===false&&m.exactImageTransferMeasured===false);
const freeze=process.argv.includes('--freeze');
if(freeze)fs.writeFileSync(path.join(here,'reviewed-proposal-publication-allowlist.json'),read(source+'publication-allowlist.json'));
check('copied selection identical',read(source+'publication-allowlist.json').equals(fs.readFileSync(path.join(here,'reviewed-proposal-publication-allowlist.json'))));
for(const match of fs.readFileSync(path.join(here,'review.md'),'utf8').matchAll(/\]\(([^)]+)\)/g)){
  if(freeze&&['verification.json','publication-allowlist.json'].includes(match[1]))continue;
  check('link '+match[1],fs.existsSync(path.resolve(here,match[1])));
}
if(freeze){
  write('verification.json',{date:'2026-10-17',command:'node '+prefix+'audit.mjs',exitCode:0,proposalVerification:{command:'node '+source+'verify.mjs',exitCode:0,groupedChecks:8},scope:'Proposal source and capacity review only',checks});
  write('publication-allowlist.json',['review.md','audit.mjs','reviewed-proposal-publication-allowlist.json','verification.json'].map(name=>{const bytes=fs.readFileSync(path.join(here,name));return {sourcePath:prefix+name,sha256:sha(bytes),bytes:bytes.length};}));
}else for(const pin of JSON.parse(fs.readFileSync(path.join(here,'publication-allowlist.json')))){
  const bytes=fs.readFileSync(path.join(here,pin.sourcePath.slice(prefix.length)));check('review publication '+pin.sourcePath,bytes.length===pin.bytes&&sha(bytes)===pin.sha256);
}
console.log(JSON.stringify({passed:checks.length,scope:'Source proposal only; no implementation or runtime acceptance'}));
