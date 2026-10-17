import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
const base=path.dirname(fileURLToPath(import.meta.url)),parent=path.dirname(base),project=path.resolve(parent,'../..'),attempt=parent+'/attempt-20261017T1549043-3a567782';
const sha=file=>createHash('sha256').update(fs.readFileSync(file)).digest('hex'),read=file=>JSON.parse(fs.readFileSync(file));
assert.equal(sha(parent+'/harness-manifest.json'),'9ba3ebf7976b2fc8f0a027fd2823c93365cba5e297de5d988311da7c405f4531');
assert.equal(sha(parent+'/source-hashes.json'),'5b0674b7aae4e0a7c9e26fb26b7009def4e42fb73ed67865a31d71b34c502704');
for(const f of read(parent+'/source-hashes.json').sourceFiles){assert.equal(sha(parent+'/'+f.path),f.sha256);assert.equal(fs.statSync(parent+'/'+f.path).size,f.bytes);}
assert.equal(sha(attempt+'/source-manifest.json'),sha(parent+'/harness-manifest.json'));
for(const f of read(attempt+'/source-manifest.json').files){assert.equal(sha(attempt+'/'+f.path),f.sha256);assert.equal(fs.statSync(attempt+'/'+f.path).size,f.bytes);}
const execution=read(base+'/execution-receipt.json'),absence=read(base+'/owned-absence.json'),cases=read(base+'/cases.json');
assert.equal(execution.outcome,'startup-admission-unresolved');assert.equal(execution.browserJourneyLaunched,false);assert.equal(execution.noRetry,true);
assert.equal(read(attempt+'/run-status.json').status,'cleanup-unverified');assert.equal(read(attempt+'/start-status.json').exitCode,1);
assert.equal(execution.loopbackShape.networkSettingsPorts3000Tcp.status,'unobserved');assert.equal(execution.loopbackShape.hostConfigPortBindings3000Tcp.status,'unobserved');
assert.equal(absence.ownedInfrastructureAbsenceVerified,true);assert.equal(cases.length,8);assert(cases.every(c=>c.status==='not-run-admission'));
for(const key of ['chartActions','fieldMutations','events','observations','pngs'])assert.equal(execution.counters[key],0);
assert(!fs.existsSync(attempt+'/journey.log'));assert(!fs.existsSync(attempt+'/credential-private.json'));assert(!fs.existsSync(attempt+'/owned-browser-private.json'));
const allowed=read(base+'/publication-allowlist.json');for(const f of allowed){assert(!/-private\.json$|\.log$|\/(?:state-|\.env)|\.(?:zip|tar|gz)$/i.test(f.sourcePath));const file=path.resolve(project,f.sourcePath);assert.equal(sha(file),f.sha256);assert.equal(fs.statSync(file).size,f.bytes);}
for(const derivative of read(base+'/sanitization.json').derivatives){assert.notEqual(derivative.source.sha256,derivative.published.sha256);assert.equal(derivative.originalHashClaimedForDerivative,false);}
console.log(JSON.stringify({status:'verified-failed-startup-evidence',readOnly:true,sourceCopies:read(attempt+'/source-manifest.json').files.length,allowlistFiles:allowed.length,casesNotRun:8,rawStatusPreserved:'cleanup-unverified',browserRun:false,topologyRetried:false}));
