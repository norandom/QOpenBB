import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {root,output} from './io.mjs';
import {ownerLabel,command,fail,safeFailure} from './admission.mjs';
import {ownedRoot} from './probe.mjs';
export function ownedPaths(directory,runtime){
  if(!/^qopenbb-legend-relay-[a-f0-9]{10}$/.test(runtime.name)||!/^[a-f0-9]{24}$/.test(runtime.ownership))fail('cleanup-ownership-unresolved');
  const state=path.resolve(runtime.statePath);if(path.dirname(state)!==path.resolve(directory)||!/^state-[a-f0-9]{12}$/.test(path.basename(state)))fail('cleanup-state-path-unresolved');
  for(const [key,relative] of [['relaySourcePath','harness/relay.py'],['configPath','relay-config.json'],['statsPath','relay-stats.json']])if(runtime[key]!==path.join(directory,relative))fail('cleanup-file-path-unresolved');
  return state;
}
export function assertResource(actual,runtime,kind,container){
  const id=runtime[kind+(container?'Id':'NetworkId')],name=runtime.name+'-'+kind;
  if(!/^[a-f0-9]{64}$/.test(actual?.Id??'')||(actual.Name??'').replace(/^\//,'')!==name||id&&actual.Id!==id||(container?actual.Config?.Labels:actual.Labels)?.[ownerLabel]!==runtime.ownership)fail('cleanup-resource-identity-unresolved');
}
export async function cleanupOwned(runtime,{directory,docker,remove,exists}){
  const state=ownedPaths(directory,runtime),proof={relayAbsent:false,appAbsent:false,internalNetworkAbsent:false,ingressNetworkAbsent:false,stateAbsent:false,credentialAbsent:false,browserCreated:false,relayStopCompleted:null,identities:{}};
  const ids=(kind,container,id=null)=>{const name=runtime.name+'-'+kind,filter=id?'id='+id:container?'name=^/'+name+'$':'name='+name,args=container?['ps','-a','--no-trunc','--filter',filter,'--format','{{.ID}}']:['network','ls','--no-trunc','--filter',filter,'--format',id?'{{.ID}}':'{{.ID}} {{.Name}}'];
    const lines=docker(...args).trim().split('\n').filter(Boolean);if(lines.length>4)fail('cleanup-list-bound');const matches=container?lines:lines.map(line=>line.trim().split(/\s+/)).filter(([,n])=>n===name).map(([id])=>id);
    const result=!container&&id?lines:matches;if(result.length>1||result.some(value=>!/^[a-f0-9]{64}$/.test(value)||id&&value!==id))fail('cleanup-ambiguous-resource');return result;};
  const find=(kind,container)=>{
    const recorded=runtime[kind+(container?'Id':'NetworkId')];if(recorded!==null&&!/^[a-f0-9]{64}$/.test(recorded??''))fail('cleanup-recorded-id-unresolved');
    const byId=recorded?ids(kind,container,recorded):[],byName=ids(kind,container);
    proof.identities[kind]={basis:recorded?'recorded':byName.length?'recovered':'no-recorded-or-named-resource',recordedIdPresent:byId.length===1,expectedNamePresent:byName.length===1,idAbsent:false,nameAbsent:false};
    if(recorded&&byName.some(id=>id!==recorded))fail('cleanup-name-id-mismatch');
    return {id:recorded??byName[0]??null,present:(recorded?byId:byName).length===1};
  };
  const absent=(kind,container,id)=>{
    const idAbsent=id?ids(kind,container,id).length===0:true,nameAbsent=ids(kind,container).length===0;
    Object.assign(proof.identities[kind],{idAbsent,nameAbsent});if(!idAbsent||!nameAbsent)fail('cleanup-recorded-resource-survived');
    proof[kind+(container?'Absent':'NetworkAbsent')]=true;
  };
  try{
  for(const kind of ['relay','app']){
    const found=find(kind,true);
    if(found.present){const actual=JSON.parse(docker('inspect',found.id))[0];assertResource(actual,runtime,kind,true);
      if(kind==='relay'&&actual.State?.Running===true){try{docker('stop','--time','2',found.id);proof.relayStopCompleted=true;}catch{proof.relayStopCompleted=false;}}
      docker('rm','-f',found.id);}
    absent(kind,true,found.id);
  }
  for(const kind of ['ingress','internal']){
    const found=find(kind,false);
    if(found.present){const actual=JSON.parse(docker('network','inspect',found.id))[0];assertResource(actual,runtime,kind,false);if(Object.keys(actual.Containers??{}).length)fail('cleanup-shared-network');docker('network','rm',found.id);}
    absent(kind,false,found.id);
  }
  remove(state,{recursive:true,force:true});proof.stateAbsent=!exists(state);
  remove(path.join(directory,'credential-private.json'),{force:true});proof.credentialAbsent=!exists(path.join(directory,'credential-private.json'));
  return proof;
  }catch(error){error.cleanupProof=proof;throw error;}
}
export const absenceComplete=proof=>['relayAbsent','appAbsent','internalNetworkAbsent','ingressNetworkAbsent','stateAbsent','credentialAbsent'].every(key=>proof?.[key]===true)&&(proof.ownershipNeverWritten===true||['relay','app','ingress','internal'].every(kind=>proof.identities?.[kind]?.idAbsent===true&&proof.identities[kind].nameAbsent===true));
export async function main(){
  const io=output(),startedAt=Number(process.env.ATTEMPT_STARTED_MS),end=Math.min(Date.now()+59000,startedAt+145000);let stage='cleanup-admission';
  let proof={browserCreated:false},failure=null;
  try{
    if(!Number.isFinite(startedAt)||!ownedRoot(root))fail('cleanup-root-unresolved');
    if(fs.existsSync(root+'/runtime-private.json')){
      const runtime=JSON.parse(fs.readFileSync(root+'/runtime-private.json'));
      const docker=(...args)=>{stage='cleanup-'+args[0];const left=end-Date.now();if(left<=0)fail('cleanup-deadline');return command((values,timeout)=>execFileSync('docker',values,{encoding:'utf8',timeout,maxBuffer:262144,stdio:['ignore','pipe','pipe'],windowsHide:true}),stage,args,Math.max(1,Math.min(5000,left)));};
      proof=await cleanupOwned(runtime,{directory:root,docker,remove:(...args)=>fs.rmSync(...args),exists:filename=>fs.existsSync(filename)});
    }else proof={relayAbsent:true,appAbsent:true,internalNetworkAbsent:true,ingressNetworkAbsent:true,stateAbsent:!fs.readdirSync(root).some(name=>/^state-/.test(name)),credentialAbsent:!fs.existsSync(root+'/credential-private.json'),browserCreated:false,ownershipNeverWritten:true};
  }catch(error){if(error?.cleanupProof)proof=error.cleanupProof;failure=safeFailure(error,stage);}
  const cleaned=!failure&&absenceComplete(proof);io.json('cleanup-report',{status:cleaned?'cleaned':'cleanup-unverified',...proof,failure});if(!cleaned)process.exitCode=1;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))await main();
