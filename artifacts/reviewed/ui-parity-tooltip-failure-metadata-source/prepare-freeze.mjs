import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../..');
const prefix='artifacts/ui-parity-tooltip-failure-metadata-source/',prior='artifacts/ui-parity-tooltip-segment-keyboard-revised/';
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const pin=sourcePath=>({sourcePath,sha256:hash(root+'/'+sourcePath),bytes:fs.statSync(root+'/'+sourcePath).size});
const save=(name,value)=>fs.writeFileSync(here+'/'+name,JSON.stringify(value,null,2)+'\n');
const names=fs.readdirSync(here+'/base').sort();
const frozen=JSON.parse(fs.readFileSync(root+'/'+prior+'source-hashes.json')).outputs;
for(const name of names){
  const p=prior+'harness/'+name,known=frozen.find(v=>v.sourcePath===p);
  if(!known||hash(root+'/'+p)!==known.sha256||hash(here+'/base/'+name)!==known.sha256)throw Error('Base pin changed '+name);
}
const inputPaths=[...names.map(v=>prior+'harness/'+v),prior+'source-hashes.json',
  'artifacts/ui-parity-tooltip-failure-metadata-plan-revised/plan.md',
  'artifacts/ui-parity-tooltip-failure-metadata-plan-revised/source-hashes.json',
  'artifacts/ui-parity-tooltip-failure-metadata-plan-revision-review/review.md',
  'artifacts/ui-parity-tooltip-reservation-review/review.md',
  'AGENTS.md',...['delegation','testing','documentation','complexity','ci'].map(v=>'.kiro/steering/'+v+'.md')];
const plan=pin(inputPaths[names.length+1]);
if(plan.sha256!=='248354c82919366fec8c440b3a2f298f715a069bb6de7b96434a948baf527257')throw Error('Wrong plan');
const diff=spawnSync('git',['diff','--no-index','--',prefix+'base/journey.mjs',prefix+'harness/journey.mjs'],{cwd:root,encoding:'utf8',windowsHide:true});
if(diff.status!==1)throw Error('Expected journey diff');
const helper=fs.readFileSync(here+'/harness/failure-metadata.mjs','utf8');
fs.writeFileSync(here+'/source.diff',diff.stdout+'\n--- /dev/null\n+++ '+prefix+'harness/failure-metadata.mjs\n@@ -0,0 +1,'+helper.trimEnd().split('\n').length+' @@\n'+helper.trimEnd().split('\n').map(v=>'+'+v).join('\n')+'\n');
const syntax=[];
for(const dir of ['base','harness'])for(const name of fs.readdirSync(here+'/'+dir).filter(v=>v.endsWith('.mjs'))){
  const command=['--check',prefix+dir+'/'+name],run=spawnSync(process.execPath,command,{cwd:root,encoding:'utf8',windowsHide:true});
  syntax.push({command:'node '+command.join(' '),exitCode:run.status});if(run.status!==0)throw Error(run.stderr);
}
save('syntax-verification.json',{date:'2026-10-17',node:process.version,scope:'Syntax only; no imports or collector execution',commands:syntax});
const ownFiles=()=>fs.readdirSync(here,{recursive:true}).filter(v=>fs.statSync(here+'/'+v).isFile()).map(v=>v.replaceAll('\\','/')).sort();
const selected=ownFiles().filter(v=>!['source-hashes.json','publication-allowlist.json'].includes(v));
save('source-hashes.json',{date:'2026-10-17',scope:'Source-only bounded metadata preparation; finite scaffold proof separate',
  inputs:inputPaths.map(pin),outputs:selected.map(v=>pin(prefix+v)),
  fromBase:names.map(name=>({name,baseSourcePath:prior+'harness/'+name,baseSha256:hash(here+'/base/'+name),sha256:hash(here+'/harness/'+name),changed:hash(here+'/base/'+name)!==hash(here+'/harness/'+name)})),
  added:fs.readdirSync(here+'/harness').filter(v=>!names.includes(v)).sort()});
save('publication-allowlist.json',[...selected,'source-hashes.json'].sort().map(v=>pin(prefix+v)));
console.log(JSON.stringify({frozenFiles:selected.length+1,syntaxChecks:syntax.length}));
