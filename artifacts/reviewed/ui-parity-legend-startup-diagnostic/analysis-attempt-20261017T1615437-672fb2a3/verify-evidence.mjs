import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {classify} from '../attempt-20261017T1615437-672fb2a3/harness/projection.mjs';
const base=path.dirname(fileURLToPath(import.meta.url)),parent=path.dirname(base),project=path.resolve(parent,'../..'),attempt=parent+'/attempt-20261017T1615437-672fb2a3';
const sha=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex'),read=file=>JSON.parse(fs.readFileSync(file));
assert.equal(sha(parent+'/harness-manifest.json'),'29096d4612637299972e068e4b4d76dbe1331051e1dce7f885258cb3bc79fe3b');
assert.equal(sha(parent+'/source-hashes.json'),'95128fc21fd7f16d230e5e7488ee32972822c00134cd045b689ff9e4ba1a4a7b');
assert.equal(sha(project+'/artifacts/ui-parity-legend-startup-diagnostic-review/review.md'),'3905af98f1418ddcb52ca95b3e757726da7ca7b21bb6abf9a8160185abf10ff7');
for(const f of read(parent+'/source-hashes.json').sourceFiles){assert.equal(sha(parent+'/'+f.path),f.sha256);assert.equal(fs.statSync(parent+'/'+f.path).size,f.bytes);}
assert.equal(sha(attempt+'/source-manifest.json'),sha(parent+'/harness-manifest.json'));
for(const f of read(attempt+'/source-manifest.json').files){assert.equal(sha(attempt+'/'+f.path),f.sha256);assert.equal(fs.statSync(attempt+'/'+f.path).size,f.bytes);}
const samples=read(attempt+'/samples.json');assert.equal(samples.length,3);assert.deepEqual(samples.map(x=>x.context.plannedOffsetMs),[0,1000,3000]);
assert.equal(new Set(samples.map(x=>x.context.containerId)).size,1);assert.equal(new Set(samples.map(x=>x.context.networkId)).size,1);
for(const sample of samples){assert.equal(classify(sample).kind,'allocation-pending');assert.equal(sample.runtime.target.kind,'null');assert.equal(sample.runtime.target.value,null);assert.equal(sample.runtime.target.own,true);assert.equal(sample.runtime.target.in,true);assert.equal(sample.configured.target.entries[0].HostIp.value,'127.0.0.1');assert.equal(sample.configured.target.entries[0].HostPort.value,'');assert.equal(sample.state.Status.value,'running');assert.equal(sample.state.Running.value,true);assert.equal(sample.state.Dead.value,false);assert.equal(sample.state.Restarting.value,false);assert.equal(sample.errors.length,0);}
const result=read(attempt+'/probe-result.json');assert.equal(result.outcome,'publication-not-observed-within-window');assert(!('health' in result));assert.equal(result.browserCreated,false);assert.equal(result.noRetry,true);
assert.equal(read(attempt+'/cleanup-report.json').status,'cleaned');assert.equal(read(attempt+'/run-status.json').exitCode,1);assert.equal(read(attempt+'/run-status.json').status,'diagnostic-closed');
assert.equal(read(base+'/owned-absence.json').passed,true);assert.equal(read(base+'/launcher-absence.json').absent,true);assert(!fs.existsSync(attempt+'/credential-private.json'));
const inventory=read(base+'/completed-output-inventory.json');assert(inventory.files<=32);assert(inventory.bytes<=2097152);
const allowed=read(base+'/publication-allowlist.json');for(const f of allowed){assert(!/-private\.json$|\.log$|\/(?:state-|\.env)|\.(?:zip|tar|gz)$/i.test(f.sourcePath));const file=path.resolve(project,f.sourcePath);assert.equal(sha(file),f.sha256);assert.equal(fs.statSync(file).size,f.bytes);}
console.log(JSON.stringify({status:'verified-one-diagnostic-evidence',readOnly:true,sourceCopies:7,selectedSnapshots:3,healthRequests:0,browserCreated:false,cleanup:'cleaned',freshOwnedAbsence:true,allowlistFiles:allowed.length,noRetry:true,conclusion:'Publication not observed within this finite window; root cause unresolved'}));
