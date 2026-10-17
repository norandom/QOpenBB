import assert from 'node:assert/strict';
import path from 'node:path';
import {cleanupOwned, absenceComplete} from '../ui-parity-legend-fixed-relay/harness/cleanup.mjs';
import {networkProjection, ownerLabel} from '../ui-parity-legend-fixed-relay/harness/admission.mjs';

const directory = path.resolve('artifacts/ui-parity-legend-fixed-relay-review');
const runtime = {name:'qopenbb-legend-relay-aaaaaaaaaa', ownership:'b'.repeat(24),
  internalNetworkId:'1'.repeat(64), ingressNetworkId:'2'.repeat(64), appId:'3'.repeat(64), relayId:'4'.repeat(64),
  statePath:path.join(directory,'state-cccccccccccc'), relaySourcePath:path.join(directory,'harness','relay.py'),
  configPath:path.join(directory,'relay-config.json'), statsPath:path.join(directory,'relay-stats.json')};
// Renamed containers are detached from the owned networks; both IDs still exist.
const calls = [], liveIds = new Set([runtime.relayId, runtime.appId]);
const networks = new Set(['internal','ingress']);
const proof = await cleanupOwned(runtime, {directory, remove:()=>{}, exists:()=>false, docker:(...args)=>{
  calls.push(args);
  if(args[0]==='ps')return '';
  if(args[0]==='inspect'&&liveIds.has(args[1]))return JSON.stringify([{Id:args[1],Name:'/renamed-owned-container',Config:{Labels:{[ownerLabel]:runtime.ownership}}}]);
  if(args[0]==='network'){
    if(args[1]==='ls'){
      const kind=['internal','ingress'].find(key=>args.includes('name='+runtime.name+'-'+key));
      return networks.has(kind)?runtime[kind+'NetworkId']+' '+runtime.name+'-'+kind:'';
    }
    const kind=['internal','ingress'].find(key=>args[2]===runtime[key+'NetworkId']);
    if(args[1]==='inspect')return JSON.stringify([{Id:runtime[kind+'NetworkId'],Name:runtime.name+'-'+kind,Labels:{[ownerLabel]:runtime.ownership},Containers:{}}]);
    if(args[1]==='rm'){networks.delete(kind);return '';}
  }
  throw Error('Unexpected command: source never queries recorded IDs when name lookup is empty');
}});
assert(absenceComplete(proof));
assert.equal(liveIds.size,2);
assert(!calls.some(args=>args.includes(runtime.relayId)||args.includes(runtime.appId)));
const raw = {Id:runtime.internalNetworkId, Name:runtime.name+'-internal', Labels:{[ownerLabel]:runtime.ownership}, Driver:'bridge', EnableIPv6:false};
const first = networkProjection({...raw,Internal:false},runtime,'internal');
const second = networkProjection(raw,runtime,'internal');
assert.deepEqual(first,second);
console.log(JSON.stringify({cleanup:{reproduced:true, returnedComplete:absenceComplete(proof), recordedLiveIdsUnchecked:liveIds.size, commandCount:calls.length, mutationsExecuted:false}, preassert:{reproduced:true, falseAndAbsentInternalProduceIdenticalReceipt:true}, runtimeExecuted:false}));
