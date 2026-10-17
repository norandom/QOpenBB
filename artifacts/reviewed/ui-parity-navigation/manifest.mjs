import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const root=path.dirname(new URL(import.meta.url).pathname);
const repository='/mnt/d/Source/QOpenBB';
const original='38dffc33389aca0e4a87e0e88d42f7067aa220df';
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const sources=[
  'terminalpro/src/components/Widget.context.tsx',
  'terminalpro/src/components/DraggableCard/DraggableCard.tsx',
  'terminalpro/src/components/General/Table/AgGrid.tsx',
  'terminalpro/src/components/General/Table/utils.tsx',
  'terminalpro/src/components/General/Table/Chart/AgChartView.tsx',
  'terminalpro/src/components/General/Table/Chart/hooks/useChartOptions.tsx',
  'terminalpro/src/components/General/Table/hooks/useTableContext.tsx',
  'terminalpro/src/components/General/Table/hooks/useUpdateColumnState.ts',
  'terminalpro/src/hooks/useAuthKeyPresses.tsx',
  'terminalpro/src/components/Settings/GeneralTab.tsx',
  'terminalpro/src/index.css',
];
const source=sources.map(name=>({repository:'vendor/workspace',revision:original,path:name,
  sha256:sha(execFileSync('git',['-C',repository+'/vendor/workspace','show',original+':'+name],{maxBuffer:4*1024*1024}))}));
const safeRunFile=name=>/^(N\d\d-.*|failure-state)\.(json|png)$/.test(name)||
  /^(start|journey|cleanup|projection)\.mjs$/.test(name)||['run.sh','fixture.json','failure.json','failure-capture.json',
    'cases.json','checkpoints.json','summary.json','browser-cleanup.json','cleanup-report.json','start-status.json',
    'journey-status.json','cleanup-status.json','run-status.json','runtime-identity.json','diagnostics.json',
    'selection-discriminator.json','table-width-comparison.json'].includes(name);
const runs=fs.readdirSync(root).filter(name=>/^run-20261017-r1-a[1-4]$/.test(name)).sort();
const relative=[];
for(const run of runs)for(const name of fs.readdirSync(root+'/'+run).filter(safeRunFile).sort())relative.push(run+'/'+name);
for(const name of ['plan.md','attempt-a1-diagnosis.md','attempt-a2-diagnosis.md','attempt-a3-diagnosis.md',
  'report.md','manifest.mjs','verify.mjs'])if(fs.existsSync(root+'/'+name))relative.push(name);
const files=relative.map(name=>({path:name,sourcePath:'artifacts/ui-parity-navigation/'+name,sha256:sha(fs.readFileSync(root+'/'+name)),bytes:fs.statSync(root+'/'+name).size,
  sanitization:'None; finite synthetic evidence or reviewed harness source'}));
fs.writeFileSync(root+'/source-manifest.json',JSON.stringify({recordedAt:new Date().toISOString(),original,
  image:'sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f',
  candidateSource:'ea02ec15956dee8d2c8a06825387a570757db12d',candidateExecuted:false,
  node:process.version,source,files,commands:runs.map(run=>({run,command:
    'wsl -d Debian -u mc -- timeout --signal=TERM --kill-after=10s 480s bash /mnt/d/Source/QOpenBB/artifacts/ui-parity-navigation/'+run+'/run.sh'}))},null,2));
fs.writeFileSync(root+'/publication-allowlist.json',JSON.stringify({status:'Completed finite evidence pending independent review',
  originalRoot:'artifacts/ui-parity-navigation',destination:'artifacts/reviewed/ui-parity-navigation',
  exclusions:['runtime-private.json','credential-private.json','state-*','*.log','environment files','auth traces',
    'profiles','dependency caches','image archives'],files:[...files,
    {path:'source-manifest.json',sha256:sha(fs.readFileSync(root+'/source-manifest.json')),sanitization:'None'},
    ...['verification.json'].filter(name=>fs.existsSync(root+'/'+name)).map(name=>({path:name,
      sha256:sha(fs.readFileSync(root+'/'+name)),sanitization:'None'}))]},null,2));
console.log('Hashed '+files.length+' finite files and '+source.length+' original source blobs');
