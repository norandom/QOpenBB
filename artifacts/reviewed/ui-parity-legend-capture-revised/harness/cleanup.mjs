import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {root,json} from './io.mjs';
import {ownerLabel,networkOwnership,ownedNetworkIds} from './network.mjs';
import {cleanupBrowser} from './browser-process.mjs';
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8',timeout:10000,stdio:['ignore','pipe','pipe'],windowsHide:true});
const runtime=fs.existsSync(root+'/runtime-private.json')?JSON.parse(fs.readFileSync(root+'/runtime-private.json')):null;
let containerAbsent=true,stateAbsent=true,networkAbsent=false,browserProof={identityRecorded:false,browserProcessAbsent:false},browserError=null;
const browserFile=root+'/owned-browser-private.json';
try{if(!fs.existsSync(browserFile))throw Error('browser-identity-unresolved: missing receipt');browserProof=await cleanupBrowser(JSON.parse(fs.readFileSync(browserFile)));}
catch(error){browserError=String(error.message).slice(0,512);}
if(runtime){
  if(!/^qopenbb-legend-20261017-[a-f0-9]{10}$/.test(runtime.name))throw Error('Unsafe container name');
  const state=path.resolve(runtime.statePath);
  if(path.dirname(state)!==path.resolve(root)||!/^state-[a-f0-9]{12}$/.test(path.basename(state)))throw Error('Unsafe state path');
  const found=docker('ps','-a','--no-trunc','--filter','name=^/'+runtime.name+'$','--format','{{.ID}}').trim();
  if(found){if(runtime.container&&found!==runtime.container)throw Error('Container ID mismatch');
    const actual=JSON.parse(docker('inspect',found))[0];if(actual?.Config?.Labels?.[ownerLabel]!==runtime.ownership)throw Error('Container ownership label mismatch');docker('rm','-f',found);}
  fs.rmSync(state,{recursive:true,force:true});stateAbsent=!fs.existsSync(state);
  containerAbsent=!docker('ps','-a','--filter','name=^/'+runtime.name+'$','--format','{{.Names}}').trim();
  if(runtime.networkName!==runtime.name+'-net'||!/^qopenbb-legend-20261017-[a-f0-9]{10}-net$/.test(runtime.networkName))throw Error('Unsafe network name');
  const ids=ownedNetworkIds(docker,runtime);
  if(ids.length){const network=JSON.parse(docker('network','inspect',ids[0]))[0];
    if(runtime.networkId&&runtime.networkId!==ids[0])throw Error('Network ID mismatch');
    networkOwnership({...runtime,networkId:ids[0]},network);
    if(Object.keys(network.Containers??{}).length)throw Error('Owned network still has attached containers');docker('network','rm',ids[0]);}
  networkAbsent=ownedNetworkIds(docker,runtime).length===0;
}
fs.rmSync(root+'/credential-private.json',{force:true});
const credentialAbsent=!fs.existsSync(root+'/credential-private.json');
const remainingOwnedState=fs.readdirSync(root).filter(name=>/^state-[a-f0-9]{12}$/.test(name));
json('cleanup-report',{status:containerAbsent&&stateAbsent&&networkAbsent&&browserProof.browserProcessAbsent&&credentialAbsent&&!remainingOwnedState.length&&!browserError?'cleaned':'cleanup-unverified',containerAbsent,stateAbsent,networkAbsent,credentialAbsent,remainingOwnedState,browser:browserProof,browserError});
if(!containerAbsent||!stateAbsent||!networkAbsent||!browserProof.browserProcessAbsent||browserError||!credentialAbsent||remainingOwnedState.length)throw Error('Cleanup incomplete');
