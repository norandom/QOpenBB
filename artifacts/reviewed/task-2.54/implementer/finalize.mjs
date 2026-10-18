import fs from 'node:fs';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
const root='/mnt/d/Source/QOpenBB/';const dir=root+'artifacts/task-2.54/implementer/';
const paths=['vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/background/ChartBackgroundPanel.tsx','vendor/workspace/terminalpro/src/components/ds/organisms/ChartBackgroundPanel.stories.tsx','vendor/workspace/terminalpro/tests/unit/chartBackgroundPanel.test.tsx'];
const hashes=paths.map(path=>{const text=fs.readFileSync(root+path,'utf8').replace(/\r\n?/g,'\n');fs.writeFileSync(root+path,text);return {path,sha256:crypto.createHash('sha256').update(text).digest('hex'),physical:text.trimEnd().split('\n').length};});
fs.writeFileSync(dir+'source-hashes.json',JSON.stringify(hashes,null,2));
const result=spawnSync(process.execPath,[root+'tools/quality/syntax_units.ts'],{cwd:root,input:JSON.stringify(paths.filter(p=>p.endsWith('.tsx'))),encoding:'utf8'});fs.writeFileSync(dir+'size.json',result.stdout);if(result.status)throw Error(result.stderr);
