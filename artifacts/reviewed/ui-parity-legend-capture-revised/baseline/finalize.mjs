import fs from 'node:fs';
import {json,budget,reconcile,root,limits} from './io.mjs';
const incoming=Number(process.argv[2]);if(!Number.isInteger(incoming))throw Error('Final status required');
const read=name=>fs.existsSync(root+'/'+name+'.json')?JSON.parse(fs.readFileSync(root+'/'+name+'.json')):null;
const cleanup=read('cleanup-report'),browser=read('browser-cleanup');
const cleaned=cleanup?.status==='cleaned'&&browser?.browserClosed===true&&browser?.contextClosed===true&&!browser?.closeError;
const status=cleaned?(incoming===0?'observed':'capture-failed'):'cleanup-unverified';
const inventory=budget();for(const entry of inventory.entries){if(entry.path.endsWith('.json')&&entry.bytes>limits.json)throw Error('Final JSON bound');if(entry.path.endsWith('.png')&&entry.bytes>limits.png)throw Error('Final PNG bound');}
json('final-output-inventory',{scope:'Retained public outputs; excludes this receipt and subsequent status',inventory});
json('run-status',{exitCode:incoming,status,cleanupVerified:cleaned,candidateExecuted:false});reconcile();
console.log(JSON.stringify({status,retained:budget()}));if(!cleaned||incoming!==0)process.exitCode=1;
