import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {root,output} from './io.mjs';
import {ownerLabel} from './projection.mjs';
import {command,fail,safeFailure} from './probe.mjs';
export function ownedPaths(directory,runtime){
  if(!/^qopenbb-legend-probe-[a-f0-9]{10}$/.test(runtime.name)||runtime.networkName!==runtime.name+'-net'||! /^[a-f0-9]{24}$/.test(runtime.ownership))fail('cleanup-ownership-unresolved');
  const state=path.resolve(runtime.statePath);if(path.dirname(state)!==path.resolve(directory)||!/^state-[a-f0-9]{12}$/.test(path.basename(state)))fail('cleanup-state-path-unresolved');return state;
}
export function assertResource(actual,runtime,kind){
  const name=kind==='container'?runtime.name:runtime.networkName,id=kind==='container'?runtime.container:runtime.networkId;
  if((actual.Name??'').replace(/^\//,'')!==name||id&&actual.Id!==id||(kind==='container'?actual.Config?.Labels:actual.Labels)?.[ownerLabel]!==runtime.ownership)fail('cleanup-resource-identity-unresolved');
}
export async function cleanupOwned(runtime,{directory,docker,remove,exists}){
  const state=ownedPaths(directory,runtime),proof={containerAbsent:false,networkAbsent:false,stateAbsent:false,credentialAbsent:false,browserCreated:false};
  const ids=(kind,name)=>{const args=kind==='container'?['ps','-a','--no-trunc','--filter','name=^/'+name+'$','--format','{{.ID}}']:['network','ls','--no-trunc','--filter','name='+name,'--format','{{.ID}} {{.Name}}'];
    const lines=docker(...args).trim().split('\n').filter(Boolean);if(lines.length>4)fail('cleanup-list-bound');const matches=kind==='container'?lines:lines.map(line=>line.trim().split(/\s+/)).filter(([,n])=>n===name).map(([id])=>id);if(matches.length>1)fail('cleanup-ambiguous-resource');if(matches.some(id=>!/^[a-f0-9]{64}$/.test(id)))fail('cleanup-id-unresolved');return matches;};
  let found=ids('container',runtime.name);
  if(found.length){const actual=JSON.parse(docker('inspect',found[0]))[0];assertResource(actual,runtime,'container');docker('rm','-f',found[0]);}
  proof.containerAbsent=ids('container',runtime.name).length===0;if(!proof.containerAbsent)fail('cleanup-container-survived');
  found=ids('network',runtime.networkName);
  if(found.length){const actual=JSON.parse(docker('network','inspect',found[0]))[0];assertResource(actual,runtime,'network');if(Object.keys(actual.Containers??{}).length)fail('cleanup-shared-network');docker('network','rm',found[0]);}
  proof.networkAbsent=ids('network',runtime.networkName).length===0;if(!proof.networkAbsent)fail('cleanup-network-survived');
  remove(state,{recursive:true,force:true});proof.stateAbsent=!exists(state);
  remove(path.join(directory,'credential-private.json'),{force:true});proof.credentialAbsent=!exists(path.join(directory,'credential-private.json'));
  return proof;
}
export async function main(){
  const io=output(),startedAt=Number(process.env.ATTEMPT_STARTED_MS),end=Math.min(Date.now()+59000,startedAt+145000);let stage='cleanup-admission';
  let proof={containerAbsent:false,networkAbsent:false,stateAbsent:false,credentialAbsent:false,browserCreated:false},failure=null;
  try{
    if(!Number.isFinite(startedAt)||path.resolve(root)!==fs.realpathSync(root)||path.basename(path.dirname(root))!=='ui-parity-legend-startup-diagnostic'||!/^attempt-[\w-]+$/.test(path.basename(root)))fail('cleanup-root-unresolved');
    const runtimeFile=root+'/runtime-private.json';
    if(fs.existsSync(runtimeFile)){
      const runtime=JSON.parse(fs.readFileSync(runtimeFile));
      const docker=(...args)=>{stage='cleanup-'+args[0];const left=end-Date.now();if(left<=0)fail('cleanup-deadline');return command((values,timeout)=>execFileSync('docker',values,{encoding:'utf8',timeout,maxBuffer:262144,stdio:['ignore','pipe','pipe'],windowsHide:true}),stage,args,Math.max(1,Math.min(5000,left)));};
      proof=await cleanupOwned(runtime,{directory:root,docker,remove:(...args)=>fs.rmSync(...args),exists:filename=>fs.existsSync(filename)});
    }else{
      // Startup writes ownership before creating any resource.
      proof={containerAbsent:true,networkAbsent:true,stateAbsent:!fs.readdirSync(root).some(name=>/^state-/.test(name)),credentialAbsent:!fs.existsSync(root+'/credential-private.json'),browserCreated:false,ownershipNeverWritten:true};
    }
  }catch(error){failure=safeFailure(error,stage);}
  const cleaned=!failure&&proof.containerAbsent&&proof.networkAbsent&&proof.stateAbsent&&proof.credentialAbsent;
  io.json('cleanup-report',{status:cleaned?'cleaned':'cleanup-unverified',...proof,failure});if(!cleaned)process.exitCode=1;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))await main();
