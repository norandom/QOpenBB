import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
const dir='/mnt/d/Source/QOpenBB/artifacts/task-2.56/implementer';
const stage=process.argv[2];if(!['red','green'].includes(stage))throw Error('stage required');
const result=spawnSync(process.execPath,[dir+'/capture.mjs'],{env:{...process.env,PLAYWRIGHT_BROWSERS_PATH:'/mnt/d/Source/QOpenBB/artifacts/playwright-browsers'},encoding:'utf8'});
fs.writeFileSync(dir+'/'+stage+'.log',result.stdout+result.stderr);fs.writeFileSync(dir+'/'+stage+'.exit',String(result.status)+'\n');console.log(stage+': '+result.status);process.exitCode=result.status;
