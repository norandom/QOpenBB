import assert from 'node:assert/strict';
import path from 'node:path';
import * as oldCleanup from '../ui-parity-legend-fixed-relay/harness/cleanup.mjs';
import * as newCleanup from '../ui-parity-legend-fixed-relay-revised/harness/cleanup.mjs';
import * as oldAdmission from '../ui-parity-legend-fixed-relay/harness/admission.mjs';
import * as newAdmission from '../ui-parity-legend-fixed-relay-revised/harness/admission.mjs';

const directory=path.resolve('artifacts/ui-parity-legend-fixed-relay-revision-review');
const runtime={name:'qopenbb-legend-relay-aaaaaaaaaa',ownership:'b'.repeat(24),
  internalNetworkId:'1'.repeat(64),ingressNetworkId:'2'.repeat(64),appId:'3'.repeat(64),relayId:'4'.repeat(64),
  statePath:path.join(directory,'state-cccccccccccc'),relaySourcePath:path.join(directory,'harness','relay.py'),
  configPath:path.join(directory,'relay-config.json'),statsPath:path.join(directory,'relay-stats.json')};
const kinds=['relay','app','ingress','internal'];
const resourceId=kind=>runtime[kind+(kind==='relay'||kind==='app'?'Id':'NetworkId')];
async function cleanupCase(implementation,scenario,partial=false){
  const live=new Set(kinds),renamed=new Set(scenario==='renamed-before'?['relay']:[]),calls=[];
  let removals=0;
  const docker=(...args)=>{
    calls.push(args);
    const listing=args[0]==='ps'||args[0]==='network'&&args[1]==='ls';
    if(listing){
      const filter=args[args.indexOf('--filter')+1],byId=filter.startsWith('id=');
      const kind=kinds.find(key=>filter==='id='+resourceId(key)||filter.includes(runtime.name+'-'+key));
      assert(kind);
      if(!live.has(kind)||!byId&&renamed.has(kind))return '';
      return args[0]==='ps'||byId?resourceId(kind):resourceId(kind)+' '+runtime.name+'-'+kind;
    }
    const kind=kinds.find(key=>args.includes(resourceId(key)));
    assert(kind);
    if(args[0]==='inspect'||args[0]==='network'&&args[1]==='inspect'){
      const actual={Id:resourceId(kind),Name:renamed.has(kind)?'/renamed-owned-resource':runtime.name+'-'+kind,
        Config:{Labels:{[newAdmission.ownerLabel]:runtime.ownership}},Labels:{[newAdmission.ownerLabel]:runtime.ownership},
        State:{Running:true},Containers:{}};
      return JSON.stringify([actual]);
    }
    if(args[0]==='stop')return '';
    if(args[0]==='rm'||args[0]==='network'&&args[1]==='rm'){
      removals++;
      if(scenario==='survivor-'+kind)renamed.add(kind);else live.delete(kind);
      return '';
    }
    throw Error('Unexpected injected command');
  };
  const value=partial?{...runtime,relayId:null,appId:null,internalNetworkId:null,ingressNetworkId:null}:runtime;
  try{
    const proof=await implementation.cleanupOwned(value,{directory,docker,remove:()=>{},exists:()=>false});
    return {completed:implementation.absenceComplete(proof),proof,remaining:[...live],removals,idQueries:calls.filter(args=>args.some(arg=>arg.startsWith('id='))).length};
  }catch(error){return {completed:false,reason:error.probeReason,proof:error.cleanupProof,remaining:[...live],removals,idQueries:calls.filter(args=>args.some(arg=>arg.startsWith('id='))).length};}
}
const cleanup=[];
for(const scenario of ['renamed-before','survivor-relay','survivor-ingress']){
  const baseline=await cleanupCase(oldCleanup,scenario),revised=await cleanupCase(newCleanup,scenario);
  assert(baseline.completed&&baseline.remaining.length===1&&baseline.idQueries===0);
  assert(!revised.completed&&revised.idQueries>0);
  assert.equal(revised.reason,scenario==='renamed-before'?'cleanup-resource-identity-unresolved':'cleanup-recorded-resource-survived');
  assert(!newCleanup.absenceComplete(revised.proof));
  if(scenario==='renamed-before')assert.equal(revised.removals,0);
  cleanup.push({scenario,baseline,revised});
}
const partial=await cleanupCase(newCleanup,'clean',true);
assert(partial.completed&&partial.remaining.length===0&&partial.idQueries===4);
for(const kind of kinds)assert.equal(partial.proof.identities[kind].basis,'recovered');

const network={Id:runtime.internalNetworkId,Name:runtime.name+'-internal',Labels:{[newAdmission.ownerLabel]:runtime.ownership},Driver:'bridge',EnableIPv6:false};
assert.deepEqual(oldAdmission.networkProjection(network,runtime,'internal'),oldAdmission.networkProjection({...network,Internal:false},runtime,'internal'));
const absent=newAdmission.networkProjection(network,runtime,'internal'),explicitFalse=newAdmission.networkProjection({...network,Internal:false},runtime,'internal');
assert.notDeepEqual(absent,explicitFalse);
assert.equal(absent.selected.Internal.kind,'absent');assert.equal(explicitFalse.selected.Internal.value,false);
assert(!newAdmission.networkValid(absent)&&!newAdmission.networkValid(explicitFalse));
const raw={Config:{Labels:{[newAdmission.ownerLabel]:'PRIVATE_LABEL_SENTINEL'},Env:['PRIVATE_ENV_SENTINEL'],User:'65534:65534',Healthcheck:{Test:['CMD']},Entrypoint:['/opt/.venv/bin/python'],Cmd:['-B','-I','-S','-u','/relay/relay.py','/relay/config.json']},
  HostConfig:{CapDrop:['NET_ADMIN'],SecurityOpt:['no-new-privileges'],Sysctls:{'net.ipv4.ip_forward':'1','net.ipv6.conf.all.forwarding':'0'},Tmpfs:{'/data':'rw,nosuid,nodev,size=1048576'}},
  Mounts:[{Destination:'/relay/relay.py',Source:'PRIVATE_SOURCE_SENTINEL',Type:'bind',RW:true}],State:{Error:'PRIVATE_STATE_SENTINEL'}};
const saved=[];
const observed=newAdmission.observeContainer(raw,runtime,'relay',value=>saved.push(structuredClone(value)));
assert.equal(observed.decision.kind,'security-unresolved');assert.equal(saved.length,1);
const operands=saved[0].selected;
assert.equal(operands.ReadonlyRootfs.kind,'absent');
assert.equal(operands.CapDrop.entries[0].value,'NET_ADMIN');
assert.equal(operands.Sysctls.ipv4Forwarding.value,'1');
assert.equal(operands.Healthcheck.Test.entries[0].value,'CMD');
assert.equal(operands.Mounts.entries[0].RW.value,true);
for(const sentinel of ['PRIVATE_LABEL_SENTINEL','PRIVATE_ENV_SENTINEL','PRIVATE_SOURCE_SENTINEL','PRIVATE_STATE_SENTINEL'])assert(!JSON.stringify(saved).includes(sentinel));
raw.HostConfig.ReadonlyRootfs=false;
assert.equal(newAdmission.projectContainer(raw,runtime,'relay').selected.ReadonlyRootfs.value,false);
raw.HostConfig.CapDrop=['x'.repeat(129)];raw.Mounts=Array(9).fill({Source:'PRIVATE_SOURCE_SENTINEL'});
const bounded=newAdmission.projectContainer(raw,runtime,'relay');
assert.equal(bounded.selected.CapDrop.entries[0].length,129);
assert(!bounded.selected.Mounts.entries);assert.equal(bounded.selected.Mounts.length,9);
assert(!JSON.stringify(bounded).includes('x'.repeat(129)));
assert(Buffer.byteLength(JSON.stringify(bounded))<65536);
console.log(JSON.stringify({scope:'F2/F3 source-only regression checks',cleanup,partialRecovery:partial,
  operands:{baselineCollapse:true,revisedDistinct:true,savedBeforeRejection:true,selectedFlagsRetained:true,privateSentinelsExcluded:true,boundsRetained:true},runtimeExecuted:false,realMutations:false}));
