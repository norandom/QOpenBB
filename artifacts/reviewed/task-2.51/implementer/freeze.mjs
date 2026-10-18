import fs from 'node:fs';
import crypto from 'node:crypto';
const root='/mnt/d/Source/QOpenBB/';
const paths=[
  'vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/legend/ChartLegendPanel.tsx',
  'vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/legend/LegendInputs.tsx',
  'vendor/workspace/terminalpro/src/components/General/Table/Chart/editor/legend/chartLegendPanel.css',
  'vendor/workspace/terminalpro/src/components/ds/organisms/ChartLegendPanel.stories.tsx',
  'vendor/workspace/terminalpro/tests/unit/chartLegendPanel.test.tsx',
];
const files=paths.map(path=>{
  const text=fs.readFileSync(root+path,'utf8').replace(/\r\n?/g,'\n');
  fs.writeFileSync(root+path,text);
  const bytes=fs.readFileSync(root+path);
  return {path,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),bytes:bytes.length,physical:text.replace(/\n$/,'').split('\n').length,lf:true};
});
fs.writeFileSync(root+'artifacts/task-2.51/implementer/source-hashes.json',JSON.stringify({files},null,2)+'\n');
