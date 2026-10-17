import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import assert from 'node:assert/strict';
const dir='/mnt/d/Source/QOpenBB/artifacts/parity/custom-theme-contract';
const writes=JSON.parse(fs.readFileSync(dir+'/theme-writes.json'));
const result=[];
for(const mode of ['dark','light']){
 const record=JSON.parse(fs.readFileSync(dir+'/'+mode+'-groupedColumn.json'));
 const saved=writes.at(-1)[mode].chartTheme;
 assert.equal(record.model.chartThemeName,'custom-'+mode);
 assert.equal(record.effective.background.fill,saved.params.backgroundColor);
 for(let i=0;i<2;i++){assert.equal(record.effective.series[i].fill,saved.palette.fills[i]);assert.equal(record.effective.series[i].stroke,saved.palette.strokes[i]);}
 result.push({mode,theme:record.model.chartThemeName,background:record.effective.background,series:record.effective.series.map(s=>({fill:s.fill,stroke:s.stroke,strokeWidth:s.strokeWidth})),inputTheme:record.inputTheme});
}
fs.writeFileSync(dir+'/assertions.json',JSON.stringify({status:'pass',results:result},null,2));console.log('PASS two saved custom grouped-column modes; palette and background exact');
