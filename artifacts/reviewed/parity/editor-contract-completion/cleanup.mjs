import fs from 'node:fs';import path from 'node:path';import {execFileSync} from 'node:child_process';
const root='/mnt/d/Source/QOpenBB/artifacts/parity/editor-contract-completion';
const name='qopenbb-editor-contract-completion-20261017-stock';
const result=execFileSync('docker',['rm','-f',name],{encoding:'utf8'}).trim();
const removed=[];for(const name of ['state-a56487df5c45','credential-private.json']){const target=path.resolve(root,name);if(!target.startsWith(root+'/'))throw Error('Outside owned path');fs.rmSync(target,{recursive:true,force:true});removed.push(name);}
const remaining=execFileSync('docker',['ps','-a','--filter','name=^/qopenbb-editor-contract-completion-20261017-stock$','--format','{{.Names}}'],{encoding:'utf8'}).trim();if(remaining)throw Error('Owned container remains');
fs.writeFileSync(root+'/cleanup-report.json',JSON.stringify({containerRemoved:result,containerAbsent:true,removed,remainingPrivatePaths:fs.readdirSync(root).filter(x=>x.startsWith('state-')||x.includes('credential'))},null,2));console.log('Owned container and private state removed');