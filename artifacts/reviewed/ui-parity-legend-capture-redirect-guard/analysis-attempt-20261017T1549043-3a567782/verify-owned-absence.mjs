import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const output=path.dirname(fileURLToPath(import.meta.url)),attempt=path.resolve(output,'../attempt-20261017T1549043-3a567782');
const runtime=JSON.parse(fs.readFileSync(attempt+'/runtime-private.json'));
if(!/^qopenbb-legend-20261017-[a-f0-9]{10}$/.test(runtime.name)||runtime.networkName!==runtime.name+'-net'||!/^\w{64}$/.test(runtime.container)||!/^\w{64}$/.test(runtime.networkId))throw Error('Owned resource identity required');
const state=path.resolve(runtime.statePath);if(path.dirname(state)!==attempt||!/^state-[a-f0-9]{12}$/.test(path.basename(state)))throw Error('Owned disposable path required');
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8',timeout:10000,windowsHide:true});
const container=docker('ps','-a','--no-trunc','--filter','id='+runtime.container,'--format','{{.ID}}').trim();
const network=docker('network','ls','--no-trunc','--filter','id='+runtime.networkId,'--format','{{.ID}}').trim();
const start=JSON.parse(fs.readFileSync(attempt+'/start-status.json')),run=JSON.parse(fs.readFileSync(attempt+'/run-status.json'));
const proof={checkedAt:new Date().toISOString(),readOnly:true,containerAbsent:container==='',networkAbsent:network==='',stateAbsent:!fs.existsSync(state),credentialAbsent:!fs.existsSync(attempt+'/credential-private.json'),
  startupProcessAbsent:!fs.existsSync('/proc/'+runtime.ownedProcessId+'/stat'),browserIdentityReceiptAbsent:!fs.existsSync(attempt+'/owned-browser-private.json'),journeyStatusAbsent:!fs.existsSync(attempt+'/journey-status.json'),journeyLogAbsent:!fs.existsSync(attempt+'/journey.log'),
  startExitCode:start.exitCode,retainedRunStatus:run.status,browserScope:'No browser identity exists because source exits before journey on startup failure; no universal process-absence claim',attempt:'attempt-20261017T1549043-3a567782'};
proof.ownedInfrastructureAbsenceVerified=proof.containerAbsent&&proof.networkAbsent&&proof.stateAbsent&&proof.credentialAbsent&&proof.startupProcessAbsent;
fs.writeFileSync(output+'/owned-absence.json',JSON.stringify(proof,null,2));console.log(JSON.stringify(proof));if(!proof.ownedInfrastructureAbsenceVerified)process.exitCode=1;
