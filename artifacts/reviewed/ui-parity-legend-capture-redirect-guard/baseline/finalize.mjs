import fs from 'node:fs';
import {json,budget,reconcile,root,limits} from './io.mjs';
import {assessFinal} from './final-status.mjs';
const incoming=Number(process.argv[2]);if(!Number.isInteger(incoming))throw Error('Final status required');
const read=name=>fs.existsSync(root+'/'+name+'.json')?JSON.parse(fs.readFileSync(root+'/'+name+'.json')):null;
const result=assessFinal({incoming,cleanup:read('cleanup-report'),browser:read('browser-cleanup'),eventDrain:read('final-event-drain'),eventOverflow:read('event-overflow'),lateEvents:read('late-events'),failure:read('failure')});
const inventory=budget();for(const entry of inventory.entries){if(entry.path.endsWith('.json')&&entry.bytes>limits.json)throw Error('Final JSON bound');if(entry.path.endsWith('.png')&&entry.bytes>limits.png)throw Error('Final PNG bound');}
json('final-output-inventory',{scope:'Retained public outputs; excludes this receipt and subsequent status',inventory});
json('run-status',result);reconcile();
console.log(JSON.stringify({status:result.status,retained:budget()}));if(result.status!=='observed')process.exitCode=1;
