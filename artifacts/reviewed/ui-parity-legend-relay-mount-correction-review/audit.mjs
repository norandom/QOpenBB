import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,path.basename(path.dirname(here))==='reviewed'?'../../..':'../..');
const prefix='artifacts/ui-parity-legend-relay-mount-correction-review/';
const proposal='artifacts/ui-parity-legend-relay-mount-correction/';
const read=p=>fs.readFileSync(path.join(root,p));
const hash=b=>createHash('sha256').update(b).digest('hex');
const pin=p=>({sourcePath:p,sha256:hash(read(p)),bytes:read(p).length});
const write=(name,value)=>fs.writeFileSync(path.join(here,name),JSON.stringify(value,null,2)+'\n');
const freeze=process.argv.includes('--freeze');
if(freeze){
  const paths=[...JSON.parse(read(proposal+'source-hashes.json')).inputs.map(x=>x.sourcePath),...['proposal.md','audit.mjs','source-hashes.json','verification.json','publication-allowlist.json'].map(x=>proposal+x)];
  write('source-hashes.json',{date:'2026-10-17',inputs:[...new Set(paths)].map(pin)});
  fs.writeFileSync(path.join(here,'reviewed-proposal-publication-allowlist.json'),read(proposal+'publication-allowlist.json'));
}
const checks=[];
const check=(name,ok)=>{assert.ok(ok,name);checks.push({name,passed:true});};
for(const item of JSON.parse(fs.readFileSync(path.join(here,'source-hashes.json'))).inputs){
  const bytes=read(item.sourcePath);check('pinned '+item.sourcePath,hash(bytes)===item.sha256&&bytes.length===item.bytes);
}
check('reviewed proposal allowlist identical',read(proposal+'publication-allowlist.json').equals(fs.readFileSync(path.join(here,'reviewed-proposal-publication-allowlist.json'))));
const text=read(proposal+'proposal.md').toString();
for(const phrase of ['exactly three entries','exactly one own enumerable key','rw,nosuid,nodev,size=1048576','unexpectedKeyCount','planned disproof tests, not completed candidate tests','No future probe grant follows'])check('contract '+phrase,text.includes(phrase));
for(const item of JSON.parse(read(proposal+'publication-allowlist.json'))){
  const bytes=read(item.sourcePath);check('selected proposal '+item.sourcePath,hash(bytes)===item.sha256&&bytes.length===item.bytes);
  check('bounded placeholder/secret scan '+item.sourcePath,!/\b(?:TODO|TBD|FIXME|HACK|XXX)\b|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{30,}/.test(bytes.toString()));
}
for(const name of ['review.md'])for(const match of fs.readFileSync(path.join(here,name),'utf8').matchAll(/\]\(([^)]+)\)/g)){
  if(freeze&&['verification.json','publication-allowlist.json'].includes(match[1]))continue;
  check('review link '+match[1],fs.existsSync(path.resolve(here,match[1])));
}
if(!freeze)for(const item of JSON.parse(fs.readFileSync(path.join(here,'publication-allowlist.json')))){
  const bytes=fs.readFileSync(path.join(here,item.sourcePath.slice(prefix.length)));check('review publication '+item.sourcePath,hash(bytes)===item.sha256&&bytes.length===item.bytes);
}
if(freeze){
  write('verification.json',{date:'2026-10-17',command:'node '+prefix+'audit.mjs',exitCode:0,scope:'Read-only proposal/source review; no candidate predicate or runtime test',checks});
  write('publication-allowlist.json',['review.md','audit.mjs','source-hashes.json','reviewed-proposal-publication-allowlist.json','verification.json'].map(name=>pin(prefix+name)));
}
console.log(JSON.stringify({passed:checks.length,scope:'Proposal review only; no runtime or implementation acceptance'}));
