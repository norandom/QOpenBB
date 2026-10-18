import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
const cwd='/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro';
const dir='/mnt/d/Source/QOpenBB/artifacts/task-2.52/implementer';
const node=process.execPath;
const files=['src/components/General/Table/Chart/editor/padding/ChartPaddingPanel.tsx','src/components/ds/organisms/ChartPaddingPanel.stories.tsx','tests/unit/chartPaddingPanel.test.tsx'];
const results={};
for (const [name,args] of Object.entries({lint:['node_modules/@biomejs/biome/bin/biome','lint',...files],typecheck:['node_modules/typescript/bin/tsc','--noEmit','--skipLibCheck','--strict','--target','esnext','--module','esnext','--moduleResolution','bundler','--jsx','react-jsx','--allowSyntheticDefaultImports',...files.slice(0,2)]})) {
 const result=spawnSync(node,args,{cwd,encoding:'utf8'});
 fs.writeFileSync(dir+'/'+name+'.log',result.stdout+result.stderr); results[name]=result.status;
}
fs.writeFileSync(dir+'/check-exits.json',JSON.stringify(results,null,2));
