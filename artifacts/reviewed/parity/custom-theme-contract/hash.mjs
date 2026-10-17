import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
const root='/mnt/d/Source/QOpenBB/artifacts/parity/custom-theme-contract';const files=[];
function walk(dir){for(const ent of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,ent.name);if(ent.isDirectory())walk(p);else if(ent.name!=='hashes.json')files.push(p);}}
walk(root);const hashes=Object.fromEntries(files.sort().map(p=>[path.relative(root,p),crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex')]));fs.writeFileSync(root+'/hashes.json',JSON.stringify(hashes,null,2));console.log(crypto.createHash('sha256').update(fs.readFileSync(root+'/hashes.json')).digest('hex'));
