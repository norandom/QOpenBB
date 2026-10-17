import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {ownedPaths} from '../attempt-20261017T1717176-4b3330da/harness/cleanup.mjs';
const base=path.dirname(fileURLToPath(import.meta.url)),attempt=path.resolve(base,'../attempt-20261017T1717176-4b3330da');
const runtime=JSON.parse(fs.readFileSync(attempt+'/runtime-private.json')),checks=[],state=ownedPaths(attempt,runtime);
const read=(args)=>execFileSync('docker',args,{encoding:'utf8',timeout:5000,maxBuffer:65536,stdio:['ignore','pipe','pipe'],windowsHide:true}).trim().split('\n').filter(Boolean);
let failure=null;
try{
  for(const kind of ['relay','app','ingress','internal']){
    const container=kind==='relay'||kind==='app',id=runtime[kind+(container?'Id':'NetworkId')],name=runtime.name+'-'+kind;
    if(!/^[a-f0-9]{64}$/.test(id))throw Error('owned-id-unresolved');
    const idLines=read(container?['ps','-a','--no-trunc','--filter','id='+id,'--format','{{.ID}}']:['network','ls','--no-trunc','--filter','id='+id,'--format','{{.ID}}']);
    const nameLines=read(container?['ps','-a','--no-trunc','--filter','name=^/'+name+'$','--format','{{.ID}}']:['network','ls','--no-trunc','--filter','name='+name,'--format','{{.ID}} {{.Name}}']);
    if(idLines.length>4||nameLines.length>4)throw Error('owned-list-bound');
    const exactNames=container?nameLines:nameLines.filter(line=>line.trim().split(/\s+/)[1]===name);
    checks.push({resource:kind,recordedIdChecked:true,expectedNameChecked:true,idAbsent:idLines.length===0,nameAbsent:exactNames.length===0});
  }
}catch{failure='owned-absence-read-unresolved';}
const stateAbsent=!fs.existsSync(state),credentialAbsent=!fs.existsSync(attempt+'/credential-private.json');
const passed=!failure&&checks.length===4&&checks.every(value=>value.idAbsent&&value.nameAbsent)&&stateAbsent&&credentialAbsent;
const receipt={status:passed?'absence-verified':'cleanup-unverified',checkedAtUtc:new Date().toISOString(),readOnly:true,commands:checks.length*2,checks,stateAbsent,credentialAbsent,failure};
fs.writeFileSync(base+'/fresh-owned-absence.json',JSON.stringify(receipt,null,2));console.log(JSON.stringify(receipt));if(!passed)process.exitCode=1;
