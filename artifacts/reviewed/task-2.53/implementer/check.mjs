import fs from 'node:fs';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
const root='/mnt/d/Source/QOpenBB/';const cwd=root+'vendor/workspace/terminalpro';const dir=root+'artifacts/task-2.53/implementer/';
const story='src/components/ds/organisms/ChartEditorControls.stories.tsx';
const flags=['--noEmit','--skipLibCheck','--strict','--target','esnext','--module','esnext','--moduleResolution','bundler','--jsx','react-jsx','--allowSyntheticDefaultImports'];
const results={};
for(const [name,args] of Object.entries({lint:['node_modules/@biomejs/biome/bin/biome','lint',story],typecheck:['node_modules/typescript/bin/tsc',...flags,story],baseline:['node_modules/typescript/bin/tsc',...flags,'src/components/ds/atoms/Switch.tsx']})) {
 const r=spawnSync(process.execPath,args,{cwd,encoding:'utf8'});results[name]=r.status;fs.writeFileSync(dir+name+'.log',r.stdout+r.stderr);
}
fs.writeFileSync(dir+'check-exits.json',JSON.stringify(results,null,2));
const paths=[story,'src/components/General/Table/Chart/editor/ChartEditorDock.tsx',...['setup','titles','legend','padding'].flatMap(part=>fs.readdirSync(cwd+'/src/components/General/Table/Chart/editor/'+part).filter(p=>/\.(tsx|css)$/.test(p)).map(p=>'src/components/General/Table/Chart/editor/'+part+'/'+p))];
fs.writeFileSync(dir+'source-hashes.json',JSON.stringify(paths.map(path=>({path:'vendor/workspace/terminalpro/'+path,sha256:crypto.createHash('sha256').update(fs.readFileSync(cwd+'/'+path)).digest('hex')})),null,2));
