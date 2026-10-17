import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import assert from 'node:assert/strict';
import {failureMetadata} from '../ui-parity-tooltip-failure-metadata-source/harness/failure-metadata.mjs';

const here=path.dirname(fileURLToPath(import.meta.url));
const source=path.resolve(here,'../ui-parity-tooltip-failure-metadata-source');
const root=path.resolve(here,path.basename(path.dirname(here))==='reviewed'?'../../..':'../..');
const hash=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const pins={
  'source-hashes.json':'8c423993d9cd5e63999042cd368253167961881f4ada4c4ff355e9b0487c9918',
  'publication-allowlist.json':'ba3a4e6c3d3f0f9ed1130cccc32f6ff0d79b177b1243be813aef67f313aaa6d4',
  'verification.json':'62581a34a42dcce09b74e2670b2cf7d3470ff84d098de3f455071d0a7e719a1a',
  'faults.mjs':'991c22490c084cf248c5cef4c84c9372c1997850f573eb27ecf261f775e78f2c'};
const commands=[];
function run(args){const out=spawnSync(process.execPath,args,{cwd:root,encoding:'utf8',windowsHide:true});commands.push({command:['node',...args.map(v=>v.startsWith('--')?v:path.relative(root,v).replaceAll('\\','/'))].join(' '),exitCode:out.status,stdout:out.stdout,stderr:out.stderr});return out;}
function verifyPins(){for(const [name,pin] of Object.entries(pins))assert.equal(hash(source+'/'+name),pin);}
verifyPins();
assert.equal(run([source+'/freeze-check.mjs']).status,0);
for(const name of ['harness/journey.mjs','harness/failure-metadata.mjs','faults.mjs'])assert.equal(run(['--check',source+'/'+name]).status,0);
let replay=fs.readFileSync(source+'/faults.mjs','utf8');
function replaceOnce(old,next){assert.equal(replay.split(old).length,2,'unique replay path substitution');replay=replay.replace(old,next);}
replay=replay.replaceAll("from './harness/","from '../ui-parity-tooltip-failure-metadata-source/harness/");
replaceOnce('const here=path.dirname(fileURLToPath(import.meta.url));',"const review=path.dirname(fileURLToPath(import.meta.url));const here=path.resolve(review,'../ui-parity-tooltip-failure-metadata-source');");
replaceOnce("const temp=here+'/.offline-temp';","const temp=review+'/.offline-temp';");
replaceOnce("fs.writeFileSync(here+'/verification.json'","fs.writeFileSync(review+'/replay-verification.json'");
replaceOnce("command:'node artifacts/ui-parity-tooltip-failure-metadata-source/faults.mjs'","command:'node artifacts/ui-parity-tooltip-failure-metadata-source-review/audit.mjs (path-isolated replay)' ");
const replayPath=here+'/.replay.mjs',redPath=here+'/.red.mjs';
try{
  fs.writeFileSync(replayPath,replay);assert.equal(run([replayPath]).status,0);
  const old=replay.replace("here+'/harness/journey.mjs'","here+'/base/journey.mjs'");assert.notEqual(old,replay);
  fs.writeFileSync(redPath,old);const red=run([redPath]);assert.notEqual(red.status,0);assert.match(red.stderr,/case bounded and data unchanged T01/);
}finally{for(const file of [replayPath,redPath])if(fs.existsSync(file))fs.unlinkSync(file);}
const result=JSON.parse(fs.readFileSync(here+'/replay-verification.json'));
assert.equal(result.checks.length,103);assert(result.checks.every(v=>v.passed));assert.equal(result.evidence.length,11);
const supplementary=[];
for(const origin of ['case','outer'])for(const unit of ['a','"','\\','\n','\0','漢','😀','\ud800']){
  let kept=0,omitted=0;
  for(let count=0;count<=600;count++){
    const message=unit.repeat(count),out=failureMetadata({message},origin,{email:'',password:''});
    assert(Buffer.byteLength(JSON.stringify(out))<=512);assert.equal(out.failureOrigin,origin);
    if(out.reasonOmitted){omitted++;assert.equal(out.reasonCode,'message-over-byte-cap');}else{kept++;assert.equal(out.reason,message);}
  }
  supplementary.push({origin,unitCodePoint:unit.codePointAt(0),kept,omitted});
}
const selected=JSON.parse(fs.readFileSync(source+'/publication-allowlist.json'));
const prefix='artifacts/ui-parity-tooltip-failure-metadata-source/';
let links=0;
for(const item of selected){
  assert(item.sourcePath.startsWith(prefix));const file=source+'/'+item.sourcePath.slice(prefix.length);
  assert.equal(hash(file),item.sha256);assert.equal(fs.statSync(file).size,item.bytes);
  const content=fs.readFileSync(file,'utf8');
  assert(!/\b(?:TODO|TBD|FIXME|HACK|XXX)\b/.test(content),'placeholder '+item.sourcePath);
  assert(!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{20,}|\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}/.test(content),'concrete secret '+item.sourcePath);
  assert(!/(?:^|\/)(?:credential-private|runtime-private|lifecycle-private|owned-browser-private)\.json$/.test(item.sourcePath));
  if(file.endsWith('.md'))for(const match of content.matchAll(/\]\(([^)]+)\)/g)){const target=match[1].split('#')[0];if(target&&!/^https?:/.test(target)){assert(fs.existsSync(path.resolve(path.dirname(file),target)),'link '+target);links++;}}
}
verifyPins();assert.equal(run([source+'/freeze-check.mjs']).status,0);
const report={date:'2026-10-17',scope:'Independent offline source review; no application runtime, browser, network or container',pins,commands,checks:result.checks.length,fileEvidenceCases:result.evidence.length,supplementaryCases:16*601,supplementary,publication:{entries:selected.length,links,placeholderScan:'clean',concreteSecretPatternScan:'clean'},frozenInputsUnchanged:true};
fs.writeFileSync(here+'/verification.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({passed:true,checks:103,fileEvidenceCases:11,supplementaryCases:16*601,publicationEntries:selected.length,links}));
