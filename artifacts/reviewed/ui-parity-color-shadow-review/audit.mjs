import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const repo='/mnt/d/Source/QOpenBB';
const manifest=JSON.parse(fs.readFileSync(repo+'/artifacts/ui-parity-color-shadow/source-hashes.json'));
const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
const checks=[];
const check=(name,value)=>checks.push({name,passed:!!value});
for(const item of [...manifest.inputs,{...manifest.output,path:manifest.output.localPath},...manifest.installedDependencies.flatMap(d=>d.files)]){
  check('file:'+item.path,hash(fs.readFileSync(item.path.startsWith('/')?item.path:repo+'/'+item.path))===item.sha256);
}
for(const item of manifest.gitBlobs){
  check('blob:'+item.path,hash(execFileSync('git',['-C',repo+'/'+item.repository,'show',item.revision+':'+item.path],{maxBuffer:4*1024*1024}))===item.sha256);
}
const plan=fs.readFileSync(repo+'/'+manifest.output.localPath,'utf8');
check('nine-cases',(plan.match(/^\| C0[1-9] /gm)||[]).length===9);
check('alpha-left',/Left.*alpha|alpha.*Left/.test(plan));
check('no-candidate-runtime',manifest.candidateExecuted===false&&manifest.runtimeExecuted===false);
const result={scope:'Independent source-only preflight audit; no runtime',checkCount:checks.length,failed:checks.filter(c=>!c.passed),checks};
fs.writeFileSync(repo+'/artifacts/ui-parity-color-shadow-review/verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({checks:checks.length,failed:result.failed}));
if(result.failed.length)process.exitCode=1;
