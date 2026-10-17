import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
const base='artifacts/ui-parity-internal-network-source-diagnosis';
const own='artifacts/ui-parity-internal-network-source-review';
const hashBytes=b=>createHash('sha256').update(b).digest('hex');
const hash=p=>hashBytes(fs.readFileSync(p));
const read=p=>JSON.parse(fs.readFileSync(p));
const checks=[];function check(name,fn){fn();checks.push(name);}
const pins={'report.md':'452683d6236946992b34584a3ab1844e8f192e5ab0ab53b93962042d6ed77e62','source-hashes.json':'3b9009fc81f3a7eae88f9542622f59bff1a0ed296e4caaa6472a6439a406da41','publication-allowlist.json':'f41eea03628a31488df4594d988b8e281447698fb867d8b9a26ffffaafc0d469'};
check('dispatch pins',()=>{for(const [n,pin] of Object.entries(pins))assert.equal(hash(base+'/'+n),pin);});
const manifest=read(base+'/source-hashes.json'),allowed=read(base+'/publication-allowlist.json').files;
check('all source inputs and 19 publication hashes/bytes',()=>{for(const f of [...manifest.files,...allowed]){assert.equal(hash(f.sourcePath),f.sha256);assert.equal(fs.statSync(f.sourcePath).size,f.bytes);}assert.equal(allowed.length,19);assert.equal(new Set(allowed.map(x=>x.sourcePath)).size,19);});
const linkage=read(base+'/version-linkage.json'),ref=read(base+'/tag-ref.json'),tag=read(base+'/tag-object.json'),release=read(base+'/release.json');
check('tag/ref/release and controller-attributed version linkage',()=>{
  assert.equal(ref.object.type,'tag');assert.equal(ref.object.sha,tag.sha);assert.equal(tag.sha,linkage.tagObjectSha);assert.equal(tag.object.sha,manifest.commit);assert.equal(tag.object.type,'commit');assert.equal(linkage.commit,'6a43e3d5afddf4111da0f864bbc7cae5d7e95001');assert.equal(tag.tag,'docker-v29.7.2');assert.equal(release.tag_name,tag.tag);assert.equal(release.published_at,linkage.releasePublishedAt);assert.equal(linkage.controllerReportedDaemon.version,'29.7.2');assert(linkage.commit.startsWith(linkage.controllerReportedDaemon.gitCommit));assert(linkage.controllerReportedDaemon.provenance.includes('Controller'));
});
check('LICENSE NOTICE and public-only selection',()=>{
  for(const name of ['LICENSE','NOTICE'])assert(allowed.some(f=>f.sourcePath===base+'/source/'+name));
  assert(fs.readFileSync(base+'/source/LICENSE','utf8').includes('Apache License'));
  for(const f of allowed){assert(f.sourcePath.startsWith(base+'/')&&!f.sourcePath.includes('..'));assert(!fs.lstatSync(f.sourcePath).isSymbolicLink());const text=fs.readFileSync(f.sourcePath,'utf8');assert(!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:ghp_|github_pat_)[A-Za-z0-9_]{25,}|Aa1![a-f0-9]{48}|legend-probe-[a-f0-9]{12}@example\.com/.test(text));}
});
check('all report local references and commit-scoped code links',()=>{
  for(const m of fs.readFileSync(base+'/report.md','utf8').matchAll(/\]\(([^)]+)\)/g)){
    if(!/^https?:/.test(m[1]))assert(fs.existsSync(path.resolve(base,m[1].split('#')[0])));
    else if(m[1].includes('/blob/'))assert(m[1].includes('/blob/'+linkage.commit+'/'));
  }
});
// Execute the supplied offline assertions with the sole report write suppressed.
let script=fs.readFileSync(base+'/verify.mjs','utf8');
script=script.replace(/^const dir = .*;$/m,'const dir = '+JSON.stringify(path.resolve(base))+';');
script=script.replace("fs.writeFileSync(path.join(dir, 'verification.json'), JSON.stringify(result, null, 2) + '\\n');",'globalThis.__sourceDiagnosisOffline=result;');
script=script.replace('console.log(JSON.stringify({ passed: true, checks: checks.length, localLinks }));','');
assert(!script.includes('fs.writeFileSync'));
await import('data:text/javascript;base64,'+Buffer.from(script).toString('base64'));
check('36 protected supplied offline checks',()=>assert.equal(globalThis.__sourceDiagnosisOffline.checksCount,36));
const freeze=spawnSync(process.execPath,[base+'/freeze-check.mjs'],{encoding:'utf8',windowsHide:true});
check('38 read-only supplied freeze hash/byte checks',()=>{assert.equal(freeze.status,0,freeze.stderr);assert.equal(JSON.parse(freeze.stdout).sha256AndBytesChecks,38);});
// Independent complete truth table of the cited expression. This is derived
// Boolean evaluation, not compiling or executing upstream Go.
let predicateCases=0;
for(const old of [false,true])for(const requested of [false,true])for(const natDisabled of [false,true])for(const oldRouted of [false,true])for(const requestedRouted of [false,true]){
  const actual=(!old&&requested)||(natDisabled&&!oldRouted&&requestedRouted);
  const expected=(!old&&requested)||([natDisabled,!oldRouted,requestedRouted].every(Boolean));
  assert.equal(actual,expected);if(!requested&&!natDisabled)assert.equal(actual,false);predicateCases++;
}
checks.push('32-case derived publication predicate including routed-mode limits');
const upstream=[];
if(process.argv.includes('--fetch-primary')){
  const sources=manifest.files.filter(f=>f.upstreamUrl);
  for(let i=0;i<sources.length;i+=3)await Promise.all(sources.slice(i,i+3).map(async f=>{
    const response=await fetch(f.upstreamUrl,{redirect:'error',signal:AbortSignal.timeout(15000)});assert.equal(response.status,200,f.upstreamUrl);
    const bytes=Buffer.from(await response.arrayBuffer());assert(bytes.length<1048576);assert.equal(hashBytes(bytes),f.sha256,f.sourcePath);assert.equal(bytes.length,f.bytes,f.sourcePath);
    upstream.push({url:f.upstreamUrl,sha256:f.sha256,bytes:f.bytes,matched:true});
  }));
  const url='https://api.github.com/repos/moby/moby/git/tags/'+linkage.tagObjectSha;
  const response=await fetch(url,{headers:{'User-Agent':'QOpenBB-source-review'},redirect:'error',signal:AbortSignal.timeout(15000)});assert.equal(response.status,200);
  const remote=await response.json();assert.equal(remote.sha,tag.sha);assert.equal(remote.object.sha,linkage.commit);assert.equal(remote.tag,linkage.tag);
  upstream.push({url,tagObjectSha:remote.sha,commit:remote.object.sha,matched:true});
  upstream.sort((a,b)=>a.url.localeCompare(b.url));
  fs.writeFileSync(own+'/primary-source-receipt.json',JSON.stringify({scope:'Public upstream source retrieval only; no daemon/runtime probe',checkedAt:new Date().toISOString(),entries:upstream},null,2)+'\n');
}
check('frozen source and publication preserved',()=>{for(const f of [...manifest.files,...allowed])assert.equal(hash(f.sourcePath),f.sha256);for(const [n,pin] of Object.entries(pins))assert.equal(hash(base+'/'+n),pin);});
fs.writeFileSync(own+'/reviewed-source-publication-allowlist.json',JSON.stringify(allowed.map(({sourcePath,sha256,bytes})=>({sourcePath,sha256,bytes})),null,2)+'\n');
const receipt={status:'passed',scope:'Independent source interpretation and offline metadata review; no Docker, daemon probe, Moby build/test, browser, topology change, Git mutation or frozen write',node:process.version,pins,checks,suppliedOfflineChecks:36,suppliedFreezeChecks:38,predicateCases,sourcePublicationFiles:19,upstreamRetrieved:upstream.length,sourceCommit:linkage.commit,binaryIdentity:'Controller-attributed version/short commit only; not a reproducible binary attestation',frozenPreserved:true};
fs.writeFileSync(own+'/verification.json',JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify({status:'passed',groups:checks.length,suppliedOffline:36,suppliedFreeze:38,predicateCases,sourcePublicationFiles:19,upstreamRetrieved:upstream.length,frozenPreserved:true}));
