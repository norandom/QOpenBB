import {root,json,budget,reconcile,limits} from './io.mjs';
const [incoming]=process.argv.slice(2);if(!/^\d+$/.test(incoming))throw Error('Final incoming status required');
const before=budget();
for(const entry of before.entries){
  if(entry.path.endsWith('.json')&&entry.bytes>limits.json)throw Error('Final JSON bound '+entry.path);
  if(entry.path.endsWith('.png')&&entry.bytes>limits.png)throw Error('Final PNG bound '+entry.path);
}
json('final-output-inventory',{scope:'Retained public outputs; excludes this newly written receipt from entries',beforeReceipt:before});
reconcile();json('run-status',{exitCode:Number(incoming)});const after=reconcile();
console.log(JSON.stringify({root,files:after.files,bytes:after.bytes,reconciled:true}));
