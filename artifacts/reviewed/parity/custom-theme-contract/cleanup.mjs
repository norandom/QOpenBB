import fs from 'node:fs';import path from 'node:path';import {execFileSync} from 'node:child_process';
const root='/mnt/d/Source/QOpenBB/artifacts/parity/custom-theme-contract';const removed=[];
for(const name of ['state-e8b0056efcab','state-832c58e07f27','credential-private.json']){const target=path.resolve(root,name);if(!target.startsWith(root+'/'))throw Error('Outside owned scope');fs.rmSync(target,{recursive:true,force:true});removed.push(name);}
const containers=execFileSync('docker',['ps','-a','--filter','name=^/qopenbb-custom-theme-contract-20261017-stock$','--format','{{.Names}}'],{encoding:'utf8'}).trim();if(containers)throw Error('Owned container remains');
fs.writeFileSync(root+'/cleanup-report.json',JSON.stringify({ownedContainerAbsent:true,removed,remainingOwnedState:fs.readdirSync(root).filter(n=>n.startsWith('state-')||n.includes('credential'))},null,2));console.log('Owned cleanup complete');
