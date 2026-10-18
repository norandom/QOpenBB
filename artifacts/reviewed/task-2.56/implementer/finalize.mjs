import fs from 'node:fs';import crypto from 'node:crypto';import {spawnSync} from 'node:child_process';
const root='/mnt/d/Source/QOpenBB';const dir=root+'/artifacts/task-2.56/implementer';
const paths=['vendor/workspace/terminalpro/src/components/ds/organisms/ChartEditorControls.stories.tsx','vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/background/ChartBackgroundPanel.tsx','vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/tooltips/ChartTooltipsPanel.tsx'];
fs.writeFileSync(dir+'/source-hashes.json',JSON.stringify(paths.map(path=>({path,sha256:crypto.createHash('sha256').update(fs.readFileSync(root+'/'+path)).digest('hex')})),null,2)+'\n');
const result=spawnSync(process.execPath,['node_modules/typescript/bin/tsc','--noEmit','--skipLibCheck','--strict','--target','esnext','--module','esnext','--moduleResolution','bundler','--jsx','react-jsx','--allowSyntheticDefaultImports','src/components/ds/organisms/ChartEditorControls.stories.tsx'],{cwd:root+'/vendor/workspace/terminalpro',encoding:'utf8'});
fs.writeFileSync(dir+'/typecheck.log',result.stdout+result.stderr);fs.writeFileSync(dir+'/typecheck.exit',String(result.status)+'\n');
