import fs from 'node:fs';import crypto from 'node:crypto';
const dir='/mnt/d/Source/QOpenBB/artifacts/parity/theme-matrix';
const files=fs.readdirSync(dir).filter(f=>/\.(json|png|mjs|sh|log)$/.test(f)&&!f.includes('private')&&!['hashes.json'].includes(f)&&fs.statSync(dir+'/'+f).isFile());
fs.writeFileSync(dir+'/hashes.json',JSON.stringify(Object.fromEntries(files.map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(dir+'/'+f)).digest('hex')])),null,2));
