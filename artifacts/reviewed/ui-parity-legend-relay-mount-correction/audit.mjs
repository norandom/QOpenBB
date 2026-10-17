import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,path.basename(path.dirname(here))==='reviewed'?'../../..':'../..');
const prefix='artifacts/ui-parity-legend-relay-mount-correction/';
const manifest=JSON.parse(fs.readFileSync(here+'/source-hashes.json'));
const allowlist=JSON.parse(fs.readFileSync(here+'/publication-allowlist.json'));
const checks=[];
function check(name,ok){checks.push({name,passed:!!ok});if(!ok)throw Error(name);}
const read=p=>fs.readFileSync(root+'/'+p,'utf8');
const sha=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
for(const pin of [...manifest.inputs,...allowlist]){
  const file=pin.sourcePath.startsWith(prefix)?here+'/'+pin.sourcePath.slice(prefix.length):root+'/'+pin.sourcePath;
  check('frozen bytes '+pin.sourcePath,sha(file)===pin.sha256&&fs.statSync(file).size===pin.bytes);
}
const admission=read('artifacts/ui-parity-legend-fixed-relay-revised/harness/admission.mjs');
const probe=read('artifacts/ui-parity-legend-fixed-relay-revised/harness/probe.mjs');
const proposal=fs.readFileSync(here+'/proposal.md','utf8');
check('source currently requires four runtime mounts',admission.includes('raw.Mounts.length===4')&&admission.includes("['/data',null,true,'tmpfs']"));
check('source separately compares fixed tmpfs string',admission.includes("boundedTmpfs:host.Tmpfs?.['/data']==='rw,nosuid,nodev,size=1048576'"));
const args=probe.slice(probe.indexOf('export function relayArgs('),probe.indexOf('export async function main('));
check('source configures exactly three bind arguments',(args.match(/'--mount'/g)??[]).length===3);
check('source configures exact original tmpfs',args.includes("'--tmpfs','/data:rw,nosuid,nodev,size=1048576'"));
check('proposal preserves exact tmpfs and guard boundary',proposal.includes('rw,nosuid,nodev,size=1048576')&&proposal.includes('every other admission guard')&&proposal.includes('No future probe grant follows'));
check('proposal labels matrix planned rather than executed',proposal.includes('planned disproof tests, not completed candidate tests'));
check('no copied executable or runtime state',fs.readdirSync(here).every(v=>['proposal.md','audit.mjs','source-hashes.json','publication-allowlist.json','verification.json'].includes(v)));
const report={date:'2026-10-17',command:'node artifacts/ui-parity-legend-relay-mount-correction/audit.mjs',exitCode:0,
  scope:'Read-only source/proposal audit; no proposed predicate, Docker command or runtime executed',checks};
if(process.argv.includes('--write'))fs.writeFileSync(here+'/verification.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({passed:checks.length,scope:report.scope}));
