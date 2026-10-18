import fs from 'node:fs';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
const root='/mnt/d/Source/QOpenBB';const dir=root+'/artifacts/task-2.55/implementer';
const paths=['vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/tooltips/ChartTooltipsPanel.tsx','vendor/workspace/terminalpro/src/components/ds/organisms/ChartTooltipsPanel.stories.tsx','vendor/workspace/terminalpro/tests/unit/chartTooltipsPanel.test.tsx'];
const hashes=paths.map(path=>{const value=fs.readFileSync(root+'/'+path,'utf8').replace(/\r\n?/g,'\n');fs.writeFileSync(root+'/'+path,value);return {path,sha256:crypto.createHash('sha256').update(value).digest('hex'),physical:value.trimEnd().split('\n').length};});
fs.writeFileSync(dir+'/source-hashes.json',JSON.stringify(hashes,null,2));
const measured=spawnSync(process.execPath,['tools/quality/syntax_units.ts'],{cwd:root,input:JSON.stringify(paths),encoding:'utf8'});fs.writeFileSync(dir+'/size.json',measured.stdout);if(measured.status)throw Error(measured.stderr);
const result=spawnSync(process.execPath,['node_modules/vitest/vitest.mjs','run','--config',dir+'/unit.config.mjs'],{cwd:root+'/vendor/workspace/terminalpro',encoding:'utf8'});fs.writeFileSync(dir+'/green.log',result.stdout+result.stderr);fs.writeFileSync(dir+'/green.exit',String(result.status)+'\n');if(result.status)throw Error('unit failure');
