import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import assert from 'node:assert/strict';

const base=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(base,'../..');
const folder=path.join(root,'artifacts/ui-parity-legend-fixed-relay');
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const read=file=>fs.readFileSync(file);
const json=file=>JSON.parse(read(file));
const expected={
  'harness-manifest.json':'2f8caf154955b8bd429f01d9507c8248a35d40a607ac11d8e5a0171dd88a0864',
  'source-hashes.json':'dc254dd794854bf8ad122f66cfb982998fe1ec1f48887f24af9a1c4aea4190d3',
  'publication-allowlist.json':'e78baa39c45fe4fadeda5ab97dd7b06420618c8ffa0c48ef93d2f547f02a066b'};
function entry(file,expectedHash,bytes){
  const data=read(file);
  assert.equal(hash(data),expectedHash,file);
  if(bytes!==undefined)assert.equal(data.length,bytes,file);
}
function frozen(){
  for(const [file,digest] of Object.entries(expected))entry(path.join(folder,file),digest);
  const manifest=json(path.join(folder,'source-hashes.json'));
  assert.equal(manifest.sourceFiles.length,17);
  for(const file of manifest.sourceFiles)entry(path.join(folder,file.path),file.sha256,file.bytes);
  assert.equal(manifest.sourceInputs.length,11);
  for(const file of manifest.sourceInputs)entry(path.join(root,file.sourcePath),file.sha256,file.bytes);
  const selection=json(path.join(folder,'publication-allowlist.json'));
  assert.equal(selection.length,18);
  assert.equal(new Set(selection.map(file=>file.sourcePath)).size,18);
  for(const file of selection){
    assert(file.sourcePath.startsWith('artifacts/ui-parity-legend-fixed-relay/'));
    assert(!file.sourcePath.includes('..'));
    assert(!fs.lstatSync(path.join(root,file.sourcePath)).isSymbolicLink());
    entry(path.join(root,file.sourcePath),file.sha256,file.bytes);
  }
  return manifest;
}
const manifest=frozen();
for(const file of manifest.gitSources){
  assert.equal(file.repository,'vendor/workspace');
  assert.equal(file.revision,'38dffc33389aca0e4a87e0e88d42f7067aa220df');
  assert(['lite/Dockerfile','lite/supervisord.conf'].includes(file.path));
  const bytes=execFileSync('git',['-C',path.join(root,file.repository),'show',file.revision+':'+file.path],{windowsHide:true,maxBuffer:262144});
  assert.equal(hash(bytes),file.sha256);assert.equal(bytes.length,file.bytes);
}
const commands=[];
function run(program,args){
  const output=execFileSync(program,args,{cwd:root,encoding:'utf8',windowsHide:true,maxBuffer:262144});
  commands.push({program,args,exitCode:0,stdout:output.trim()});
  return output.trim();
}
const offline=JSON.parse(run(process.execPath,[path.join(folder,'verify-offline.mjs')]));
assert.deepEqual(offline,{status:'passed',javascriptTests:20,pythonTests:9,syntaxFiles:8,runtimeExecuted:false});
for(const file of ['harness/run.sh','supervise.sh'])run('wsl',['-d','Debian','-u','mc','--','bash','-n','/mnt/d/Source/QOpenBB/artifacts/ui-parity-legend-fixed-relay/'+file]);
const transport=JSON.parse(run('py',['-3','-B',path.join(base,'counterexample.py')]));
assert(transport.reproduced&&transport.falseEof&&transport.unreadClientBytes===1);
assert(Object.values(transport.violations).every(value=>value===0));
const control=JSON.parse(run(process.execPath,[path.join(base,'counterexamples.mjs')]));
assert(control.cleanup.returnedComplete&&control.cleanup.recordedLiveIdsUnchecked===2);
assert(control.preassert.falseAndAbsentInternalProduceIdenticalReceipt);
frozen();
assert(read(path.join(base,'reviewed-source-publication-allowlist.json')).equals(read(path.join(folder,'publication-allowlist.json'))));
const selected=json(path.join(folder,'publication-allowlist.json'));
for(const file of selected){
  const text=read(path.join(root,file.sourcePath)).toString('utf8');
  assert(!/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/.test(text));
  assert(!/\b(?:gh[pousr]_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{32,}|AKIA[A-Z0-9]{16})\b/.test(text));
}
const receipt={reviewVerdict:'REJECTED',auditStatus:'passed-exact-input-and-counterexample-checks',
  runtimeExecuted:false,networkOpened:false,freezeOrPreparationExecuted:false,
  inputHashes:expected,sourceFileCount:17,publicationFileCount:18,localInputCount:11,gitBlobCount:2,
  commands,transport,control,sourceInputsPreserved:true,
  scanScope:'18 selected public source/evidence files; bounded common-token/private-key markers and manual review',
  productionCaps:'Research exclusion; future maintained 400 physical/file, 300 logical/file, 50/function with inventory/checker'};
if(process.argv.includes('--record'))fs.writeFileSync(path.join(base,'verification.json'),JSON.stringify(receipt,null,2)+'\n');
else assert.deepEqual(json(path.join(base,'verification.json')),receipt);
console.log(JSON.stringify({reviewVerdict:receipt.reviewVerdict,auditStatus:receipt.auditStatus,sourceInputsPreserved:true,commands:commands.length,runtimeExecuted:false}));
