import fs from 'node:fs';
// Parse after the closing comm parenthesis; command names can contain spaces.
export function parseStat(text){
  const end=text.lastIndexOf(')'),pid=Number(text.slice(0,text.indexOf(' '))),fields=text.slice(end+2).trim().split(/\s+/);
  if(end<0||!Number.isSafeInteger(pid)||pid<=1||fields.length<20||!/^\d+$/.test(fields[19]))throw Error('browser-identity-unresolved: proc stat');
  return {pid,startTicks:fields[19]};
}
export function readProcess(pid,disk=fs){
  if(!Number.isSafeInteger(pid)||pid<=1)throw Error('browser-identity-unresolved: PID');
  try{return parseStat(disk.readFileSync('/proc/'+pid+'/stat','utf8'));}catch(error){if(error.code==='ENOENT')return null;throw error;}
}
export function ownershipState(owned,current){
  if(!owned||!Number.isSafeInteger(owned.pid)||owned.pid<=1||!/^\d+$/.test(owned.startTicks))throw Error('browser-identity-unresolved: missing owned identity');
  if(!current)return 'absent';
  if(current.pid!==owned.pid||current.startTicks!==owned.startTicks)throw Error('browser-identity-unresolved: PID reused');return 'owned-present';
}
export async function cleanupBrowser(owned,{read=readProcess,kill=(pid,signal)=>process.kill(pid,signal),now=Date.now,pause=ms=>new Promise(r=>setTimeout(r,ms))}={}){
  const state=()=>ownershipState(owned,read(owned.pid));let matched=false,terminated=false;
  if(state()==='owned-present'){
    matched=true;kill(owned.pid,'SIGTERM');terminated=true;const deadline=now()+5000;
    while(state()==='owned-present'&&now()<deadline)await pause(100);
    if(state()==='owned-present'){kill(owned.pid,'SIGKILL');await pause(250);}
  }
  const absent=state()==='absent';return {identityRecorded:true,pid:owned.pid,startTicks:owned.startTicks,identityMatched:matched,terminated,browserProcessAbsent:absent};
}
