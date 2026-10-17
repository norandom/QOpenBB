import fs from 'node:fs';import path from 'node:path';import {execFileSync} from 'node:child_process';
const root='/mnt/d/Source/QOpenBB/artifacts/parity/appearance-saved-composition';const removed=[];
for(const name of fs.readdirSync(root).filter(n=>/^state-[0-9a-f]{12}$/.test(n)||n==='credential-private.json')){const target=path.resolve(root,name);if(!target.startsWith(root+'/'))throw Error('scope');fs.rmSync(target,{recursive:true,force:true});removed.push(name);}
const remaining=execFileSync('docker',['ps','-a','--filter','name=^/qopenbb-appearance-saved-composition-20261017-stock$','--format','{{.Names}}'],{encoding:'utf8'}).trim();if(remaining)throw Error('Owned container remains');
fs.writeFileSync(root+'/cleanup-report.json',JSON.stringify({ownedContainerAbsent:true,removed,remainingOwnedState:fs.readdirSync(root).filter(n=>n.startsWith('state-')||n.includes('credential'))},null,2));
