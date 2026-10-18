import fs from 'node:fs';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
const root='/mnt/d/Source/QOpenBB', out=root+'/artifacts/task-2.55/review', cwd=root+'/vendor/workspace/terminalpro';
const files=['src/components/General/Table/Chart/editor/tooltips/ChartTooltipsPanel.tsx','src/components/ds/organisms/ChartTooltipsPanel.stories.tsx','tests/unit/chartTooltipsPanel.test.tsx'];
const flags=['--noEmit','--skipLibCheck','--strict','--target','esnext','--module','esnext','--moduleResolution','bundler','--jsx','react-jsx','--allowSyntheticDefaultImports'];
const commands={unit:['node_modules/vitest/vitest.mjs','run','--config',root+'/artifacts/task-2.55/implementer/unit.config.mjs'],lint:['node_modules/@biomejs/biome/bin/biome','lint',...files],types:['node_modules/typescript/bin/tsc',...flags,...files.slice(0,2)],baseline:['node_modules/typescript/bin/tsc',...flags,'src/components/ds/atoms/Switch.tsx']};
const results={};
for(const [key,args] of Object.entries(commands)){const p=spawnSync(process.execPath,args,{cwd,encoding:'utf8'});fs.writeFileSync(out+'/'+key+'.log',p.stdout+p.stderr);results[key]={command:[process.execPath,...args],exit:p.status};}
const source=files.map(p=>{const bytes=fs.readFileSync(cwd+'/'+p);return {path:'vendor/workspace/terminalpro/'+p,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),physical:bytes.toString().replace(/\r\n?/g,'\n').replace(/\n$/,'').split('\n').length};});
const expected=JSON.parse(fs.readFileSync(root+'/artifacts/task-2.55/implementer/source-hashes.json'));results.hashesMatch=source.every((p,i)=>p.sha256===expected[i].sha256);results.sources=source;
const size=spawnSync(process.execPath,['tools/quality/syntax_units.ts'],{cwd:root,input:JSON.stringify(source.map(p=>p.path)),encoding:'utf8'});fs.writeFileSync(out+'/size.json',size.stdout);results.sizeExit=size.status;
const candidates=fs.readdirSync(root+'/artifacts/task-2.55/implementer',{withFileTypes:true}).filter(p=>p.isFile()&&!['vite.log','capture.log'].includes(p.name)).map(p=>{const bytes=fs.readFileSync(root+'/artifacts/task-2.55/implementer/'+p.name);return {path:'artifacts/task-2.55/implementer/'+p.name,sha256:crypto.createHash('sha256').update(bytes).digest('hex')};});
fs.writeFileSync(out+'/publication-candidates.json',JSON.stringify(candidates,null,2));fs.writeFileSync(out+'/results.json',JSON.stringify(results,null,2));console.log(JSON.stringify(results));
