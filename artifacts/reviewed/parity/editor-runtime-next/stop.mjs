import fs from 'node:fs';
const expected='node\0artifacts/parity/editor-runtime-next/journey.mjs\0';
const stopped=[];for(const item of fs.readdirSync('/proc'))if(/^\d+$/.test(item)){try{if(fs.readFileSync('/proc/'+item+'/cmdline','utf8')===expected){process.kill(Number(item),'SIGTERM');stopped.push(Number(item));}}catch{}}
fs.writeFileSync('/mnt/d/Source/QOpenBB/artifacts/parity/editor-runtime-next/bounded-stop.json',JSON.stringify({reason:'Initial action selectors exposed hidden duplicates and incorrect field types; preserve partial run and replay observed controls with 4 second deadlines.',stopped}));
