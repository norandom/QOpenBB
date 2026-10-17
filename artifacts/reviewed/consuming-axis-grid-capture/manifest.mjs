import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';

const root=path.dirname(new URL(import.meta.url).pathname);
const repo='/mnt/d/Source/QOpenBB';
const original='38dffc33389aca0e4a87e0e88d42f7067aa220df';
const digest=bytes=>createHash('sha256').update(bytes).digest('hex');
const file=name=>({path:name,sha256:digest(fs.readFileSync(name))});
const owned=['terminalpro/package.json','terminalpro/src/components/General/Table/Chart/themes.tsx',
  'terminalpro/src/components/General/Table/Chart/hooks/useChartOptions.tsx',
  'terminalpro/src/routes/developer_onboarding/DeveloperOnboardingHomepage.tsx','terminalpro/src/api/auth.api.ts'];
const dependency='/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/ag-charts-community';
const scripts=['start.mjs','journey.mjs','cleanup.mjs','run.sh','manifest.mjs','verify.mjs','publication.mjs','fixture.json'];
const reused=['start.mjs','focused.mjs','cleanup.mjs','fixture.json'];
const result={recordedAt:new Date().toISOString(),original,
  image:'sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f',
  candidateSource:execFileSync('git',['-C',repo+'/vendor/workspace','rev-parse','HEAD'],{encoding:'utf8'}).trim(),
  candidateExecuted:false,command:'wsl -d Debian -u mc -- bash /mnt/d/Source/QOpenBB/artifacts/consuming-axis-grid-capture/run.sh',
  node:{version:process.version,executable:process.execPath},
  scripts:scripts.map(name=>file(root+'/'+name)),
  reused:reused.map(name=>file(repo+'/artifacts/reviewed/parity/editor-runtime-next/'+name)),
  source:owned.map(name=>({repository:'vendor/workspace',revision:original,path:name,
    sha256:digest(execFileSync('git',['-C',repo+'/vendor/workspace','show',original+':'+name]))})),
  installedDependency:{name:'ag-charts-community',version:JSON.parse(fs.readFileSync(dependency+'/package.json')).version,
    files:['package.json','LICENSE.txt','dist/package/main.cjs.js'].map(name=>file(dependency+'/'+name))}};
fs.writeFileSync(root+'/source-manifest.json',JSON.stringify(result,null,2));
const bundle=fs.readFileSync(dependency+'/dist/package/main.cjs.js','utf8').split(/\r?\n/);
const excerpts=[[17114,17138],[17290,17306],[20093,20101],[20123,20130],[20165,20166],
  [20410,20421],[26227,26242],[26341,26372],[26892,26902]].map(([first,last])=>({
    first,last,lines:bundle.slice(first-1,last)}));
fs.writeFileSync(root+'/source-excerpts.json',JSON.stringify({kind:'installed-MIT-source-evidence-not-runtime',
  source:result.installedDependency.files.at(-1),excerpts},null,2));
fs.copyFileSync(dependency+'/LICENSE.txt',root+'/ag-charts-MIT-LICENSE.txt');
console.log('Recorded original source, dependency, fixture and script hashes');
