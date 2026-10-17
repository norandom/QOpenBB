import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const root='/mnt/d/Source/QOpenBB';
const source='artifacts/ui-parity-tooltip-plan';
const review='artifacts/ui-parity-tooltip-review';
const manifest=JSON.parse(fs.readFileSync(root+'/'+source+'/source-hashes.json'));
const sha=b=>createHash('sha256').update(b).digest('hex');
const checks=[];
const check=(name,passed)=>checks.push({name,passed:!!passed});
for(const item of [...manifest.inputs,...manifest.outputs]){
  let bytes;
  if(item.kind==='pinned-original-source')bytes=execFileSync('git',['-C',root+'/'+item.repository,'show',item.revision+':'+item.path],{maxBuffer:4*1024*1024});
  else if(item.kind==='local-installed-public-dependency-source-clue')bytes=fs.readFileSync('/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/'+item.package+'/'+item.path);
  else bytes=fs.readFileSync(root+'/'+item.path);
  check('hash:'+item.path,sha(bytes)===item.sha256);
  if(item.bytes!==undefined)check('bytes:'+item.path,bytes.length===item.bytes);
}
const sorted=value=>Array.isArray(value)?value.map(sorted):value&&typeof value==='object'?Object.fromEntries(Object.keys(value).sort().map(k=>[k,sorted(value[k])])):value;
const fixture=JSON.stringify(sorted(manifest.fixture));
check('fixture-canonical-hash',sha(Buffer.from(fixture))===manifest.fixtureCanonicalSha256);
check('fixture-canonical-bytes',Buffer.byteLength(fixture)===manifest.fixtureCanonicalBytes);
check('null-versus-absent',Object.hasOwn(manifest.fixture.rows[2],'revenue')&&manifest.fixture.rows[2].revenue===null&&!Object.hasOwn(manifest.fixture.rows[3],'revenue'));
check('duplicate-period-identity',manifest.fixture.rows[0].period===manifest.fixture.rows[1].period&&manifest.fixture.rows[0].observationId!==manifest.fixture.rows[1].observationId);
check('source-only',manifest.sourceOnly===true&&manifest.candidateExecuted===false);
const plan=fs.readFileSync(root+'/'+source+'/plan.md','utf8');
check('eight-cases',(plan.match(/^\| T0[1-8] /gm)||[]).length===8);
const links=[];
for(const m of plan.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){
  const target=m[1];if(/^(https?:|#)/.test(target))continue;
  const destination=path.posix.normalize('artifacts/reviewed/ui-parity-tooltip-plan/'+target.split('#')[0]);
  const local=destination.replace('artifacts/reviewed/','artifacts/');
  const exists=fs.existsSync(root+'/'+destination)||fs.existsSync(root+'/'+local);
  links.push({target,destination,exists});check('link:'+target,exists);
}
const result={scope:'Independent tooltip source plan preflight; no runtime',planSha256:sha(Buffer.from(plan)),checkCount:checks.length,failed:checks.filter(x=>!x.passed),links,checks};
fs.writeFileSync(root+'/'+review+'/verification.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({checks:checks.length,failed:result.failed,links:links.length}));
if(result.failed.length)process.exitCode=1;
