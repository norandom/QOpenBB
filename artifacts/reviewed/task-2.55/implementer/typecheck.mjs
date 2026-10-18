import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
const cwd='/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro';
const dir='/mnt/d/Source/QOpenBB/artifacts/task-2.55/implementer';
const flags=['--noEmit','--skipLibCheck','--strict','--target','esnext','--module','esnext','--moduleResolution','bundler','--jsx','react-jsx','--allowSyntheticDefaultImports'];
const files=fs.readdirSync(cwd+'/src/components/General/Table/Chart/editor/tooltips').filter(p=>p.endsWith('.tsx')).map(p=>'src/components/General/Table/Chart/editor/tooltips/'+p);
const result=spawnSync(process.execPath,['node_modules/typescript/bin/tsc',...flags,...files,'src/components/ds/organisms/ChartTooltipsPanel.stories.tsx'],{cwd,encoding:'utf8'});
fs.writeFileSync(dir+'/typecheck.log',result.stdout+result.stderr);
fs.writeFileSync(dir+'/typecheck.exit',String(result.status)+'\n');
const baseline=spawnSync(process.execPath,['node_modules/typescript/bin/tsc',...flags,'src/components/ds/atoms/Switch.tsx'],{cwd,encoding:'utf8'});
fs.writeFileSync(dir+'/typecheck-baseline.log',baseline.stdout+baseline.stderr);
fs.writeFileSync(dir+'/typecheck-baseline.exit',String(baseline.status)+'\n');

