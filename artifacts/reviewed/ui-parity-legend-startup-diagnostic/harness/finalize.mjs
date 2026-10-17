import fs from 'node:fs';
import {root,output} from './io.mjs';
const code=Number(process.argv[2]);if(!Number.isInteger(code))throw Error('watchdog-status-required');
const io=output(),read=name=>fs.existsSync(root+'/'+name+'.json')?JSON.parse(fs.readFileSync(root+'/'+name+'.json')):null;
io.json('watchdog-status',{exitCode:code,inputStopUpperBoundSeconds:90,signalSeconds:85,cleanupMaximumSeconds:60,killSeconds:145,inventoryMaximumSeconds:4,hardSeconds:150});
const cleanup=read('cleanup-report'),result=read('probe-result');
io.json('run-status',{exitCode:code,status:cleanup?.status==='cleaned'?'diagnostic-closed':'cleanup-unverified',outcome:result?.outcome??'missing-probe-result',browserCreated:false,noRetry:true});
io.json('final-output-inventory',{scope:'Completed retained attempt scan including watchdog/status; excludes this new inventory receipt from entries',entries:io.inventory(),totals:io.check()});
io.check();if(code!==0||cleanup?.status!=='cleaned'||!result)process.exitCode=1;
