import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const base=path.dirname(fileURLToPath(import.meta.url)),attempt='attempt-20261017T1449392-91e1b733',output=path.join(base,'analysis-'+attempt),hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const plan=fs.readFileSync(path.join(base,'plan.md'),'utf8');
if(hash(path.join(base,'plan.md'))!==hash(path.join(base,attempt,'plan.md')))throw Error('Copied plan bytes differ');
const links=[...plan.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)].map(m=>m[1]).filter(h=>!h.startsWith('http')&&!h.startsWith('#')).map(href=>{
  const target=path.resolve(base,href.split('#')[0]);if(!fs.existsSync(target))throw Error('Missing canonical target '+href);
  return {href,resolveRelativeTo:'artifacts/ui-parity-axis-followup/',canonicalTarget:path.relative(path.resolve(base,'../..'),target).split(path.sep).join('/')};
});
const receipt={scope:'Frozen historical copied plan retains canonical-source relative link base',copiedPlan:attempt+'/plan.md',canonicalSource:'artifacts/ui-parity-axis-followup/plan.md',identicalSha256:hash(path.join(base,'plan.md')),publicCanonicalSource:'artifacts/reviewed/ui-parity-axis-followup/plan.md',links};
fs.writeFileSync(path.join(output,'copied-plan-link-map.json'),JSON.stringify(receipt,null,2));console.log(JSON.stringify({links:links.length,canonicalTargetsExist:true,immutableCopiedPlan:true}));
