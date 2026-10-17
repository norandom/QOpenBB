import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const root='/mnt/d/Source/QOpenBB';
const lane='artifacts/ui-parity-axis-controls-review';
const manifest=JSON.parse(fs.readFileSync(root+'/artifacts/ui-parity-axis-controls/source-hashes.json'));
const hash=b=>createHash('sha256').update(b).digest('hex');
const checks=[];
const check=(name,passed)=>checks.push({name,passed:!!passed});
for(const item of [...manifest.inputs,manifest.plan,manifest.installedChartsSource]) {
  const file=item.path.startsWith('/')?item.path:root+'/'+item.path;
  const bytes=fs.readFileSync(file);
  check('sha256:'+item.path,hash(bytes)===item.sha256);
  if(item.bytes!==undefined)check('bytes:'+item.path,bytes.length===item.bytes);
}
for(const item of manifest.originalSource){
  const bytes=execFileSync('git',['-C',root+'/'+item.repository,'show',item.revision+':'+item.path],{maxBuffer:4*1024*1024});
  check('git-blob:'+item.path,hash(bytes)===item.sha256&&bytes.length===item.bytes);
}
const plan=fs.readFileSync(root+'/'+manifest.plan.path,'utf8');
check('nine-cases',(plan.match(/^\| A0[1-9] /gm)||[]).length===9);
check('fixed-reference',manifest.originalSource.every(x=>x.revision==='38dffc33389aca0e4a87e0e88d42f7067aa220df'));
check('fixed-candidate',manifest.candidate==='ea02ec15956dee8d2c8a06825387a570757db12d');
check('numeric-limits',manifest.limits.contexts===3&&manifest.limits.workers===1&&manifest.limits.fieldEdits===80&&manifest.limits.uiInteractions===240&&manifest.limits.checkpoints===96);
const links=[];
for(const m of plan.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){
  const target=m[1];
  if(/^(https?:|#)/.test(target))continue;
  const published=path.posix.normalize(manifest.publicationBase+'/'+target.split('#')[0]);
  const source=published.replace('artifacts/reviewed/','artifacts/');
  const exists=fs.existsSync(root+'/'+published)||fs.existsSync(root+'/'+source);
  links.push({target,published,exists});
  check('publication-link:'+target,exists);
}
const result={scope:'Independent source-only axis plan preflight; no application runtime',planSha256:hash(Buffer.from(plan)),checkCount:checks.length,failed:checks.filter(x=>!x.passed),links,checks};
fs.writeFileSync(root+'/'+lane+'/verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({checks:checks.length,failed:result.failed,links:links.length}));
if(result.failed.length)process.exitCode=1;
