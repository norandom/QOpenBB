import fs from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {scriptRoot,runRoot,write} from './io.mjs';
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const plan=fs.readFileSync(path.join(scriptRoot,'..','plan.md'));
if(sha(plan)!=='a5194d24b08c5e222a4a4ed2d51acd637eae41c8a7689427a5610cff5da86ace')
  throw Error('Reviewed plan bytes changed');
const files=['limits.mjs','io.mjs','start.mjs','cleanup.mjs','projection.mjs','journey.mjs',
  'manifest.mjs','offline-check.mjs','publication.mjs','run.sh','fixture.json'];
fs.mkdirSync(path.join(runRoot,'harness'));
const scripts=files.map(name=>{
  const bytes=fs.readFileSync(path.join(scriptRoot,name));
  fs.writeFileSync(path.join(runRoot,'harness',name),bytes);
  return {path:'harness/'+name,sourcePath:'artifacts/ui-parity-captions/capture/'+name,sha256:sha(bytes)};
});
const fixture=scripts.find(file=>file.path==='harness/fixture.json');
if(fixture.sha256!=='2de20cebe2674659947f11fecb7497dc5d67fdd740f1c1443f0f746db8ceea30')
  throw Error('Reviewed four-row fixture bytes changed');
write('source-manifest',{kind:'original-runtime-capture',plan:{path:'artifacts/ui-parity-captions/plan.md',sha256:sha(plan)},
  image:'sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f',
  source:'38dffc33389aca0e4a87e0e88d42f7067aa220df',candidate:{revision:'ea02ec15956dee8d2c8a06825387a570757db12d',executed:false},
  scripts,command:'QOPENBB_CAPTIONS_HEAVY_GRANT=controller-granted bash artifacts/ui-parity-captions/capture/run.sh',
  dependencyReuse:{node:'artifacts/task-1.2/node-v24.22.0-linux-x64/bin',
    playwright:'verification/node_modules',browserCache:'artifacts/playwright-browsers'},
  productionCaps:'Evidence-only scripts excluded; any future production work retains 400 physical/file, 300 logical/file, 50/function.'});
