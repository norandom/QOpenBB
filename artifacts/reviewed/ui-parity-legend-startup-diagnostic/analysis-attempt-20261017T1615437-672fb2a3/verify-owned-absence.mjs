import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
const base=path.dirname(fileURLToPath(import.meta.url)),attempt=path.resolve(base,'../attempt-20261017T1615437-672fb2a3');
const runtime=JSON.parse(fs.readFileSync(attempt+'/runtime-private.json'));
if(!/^qopenbb-legend-probe-[a-f0-9]{10}$/.test(runtime.name)||runtime.networkName!==runtime.name+'-net'||! /^[a-f0-9]{64}$/.test(runtime.container)||! /^[a-f0-9]{64}$/.test(runtime.networkId))throw Error('Owned identities required');
const state=path.resolve(runtime.statePath);if(path.dirname(state)!==attempt||!/^state-[a-f0-9]{12}$/.test(path.basename(state)))throw Error('Owned state path required');
const docker=(...args)=>execFileSync('docker',args,{encoding:'utf8',timeout:5000,windowsHide:true});
const proof={checkedAt:new Date().toISOString(),readOnly:true,containerAbsent:docker('ps','-a','--no-trunc','--filter','id='+runtime.container,'--format','{{.ID}}').trim()==='',
  networkAbsent:docker('network','ls','--no-trunc','--filter','id='+runtime.networkId,'--format','{{.ID}}').trim()==='',stateAbsent:!fs.existsSync(state),credentialAbsent:!fs.existsSync(attempt+'/credential-private.json'),browserCreated:runtime.browserCreated,
  scope:'Exact recorded container/network IDs and owned state/credential; no browser PID or universal process claim'};
proof.passed=proof.containerAbsent&&proof.networkAbsent&&proof.stateAbsent&&proof.credentialAbsent&&proof.browserCreated===false;
fs.writeFileSync(base+'/owned-absence.json',JSON.stringify(proof,null,2));console.log(JSON.stringify(proof));if(!proof.passed)process.exitCode=1;
