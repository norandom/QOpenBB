import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {runRoot,write} from './io.mjs';
const names=['source-manifest.json','runtime-identity.json','chart-identity.json','onboarding-gate.json','summary.json','cases.json',
  'operations.json','action-ledger.json','menu-role-matrix.json','diagnostics.json','browser-cleanup.json',
  'cleanup-report.json','start-status.json','journey-status.json','cleanup-status.json','run-status.json',
  'failure.json','overflow.json','deadline.json','measurements.json','event-model-deltas.json','verification.json',
  'verification-correction.json'];
const snapshotNames=fs.readdirSync(runRoot).filter(name=>/^\d{3}-[a-z0-9-]+\.(json|png)$/.test(name));
const harnessNames=['limits.mjs','io.mjs','start.mjs','cleanup.mjs','projection.mjs','journey.mjs',
  'manifest.mjs','offline-check.mjs','offline-output-check.mjs','analyze.mjs','publication.mjs','run.sh','fixture.json']
  .map(name=>'harness/'+name);
const files=[...names,...snapshotNames,...harnessNames].filter(name=>fs.existsSync(path.join(runRoot,name)))
  .map(name=>{const bytes=fs.readFileSync(path.join(runRoot,name));return {path:name,
    sourcePath:'artifacts/ui-parity-captions/capture/runs/'+path.basename(runRoot)+'/'+name,
    bytes:bytes.length,sha256:createHash('sha256').update(bytes).digest('hex'),
    sanitization:'Synthetic finite capture; independent review required before publication'};});
write('publication-allowlist',{status:'Proposed allowlist; not independently reviewed or published',files,
  excluded:['credential-private.json','runtime-private.json','state-*','*.log','profiles','environment files','dependency caches'],
  restrictions:'Publish only completed attempt bytes reviewed by an independent reviewer; preserve failed attempts.'});
