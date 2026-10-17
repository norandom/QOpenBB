import {json} from './io.mjs';
const [name,code]=process.argv.slice(2);
if(!['cleanup-status','run-status','start-status','journey-status'].includes(name)||!/^\d+$/.test(code))throw Error('Status arguments');
json(name,{exitCode:Number(code)});
