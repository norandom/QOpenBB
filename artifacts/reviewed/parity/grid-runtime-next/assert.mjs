import fs from 'node:fs';
import assert from 'node:assert/strict';
const root='/mnt/d/Source/QOpenBB/artifacts/parity/grid-runtime-next';
const read=n=>JSON.parse(fs.readFileSync(root+'/'+n+'.json'));
const results=[];
function check(name,fn){try{fn();results.push({name,passed:true});}catch(e){results.push({name,passed:false,message:e.message});}}
const baseline=read('ordinary'),bounded=read('filtered-sorted-bounds');
check('ordinary observations preserve zero negative fractional null',()=>{assert.deepEqual(baseline.chart.effective.data.map(r=>[r.revenue,r.operatingIncome]),[[100,20],[0,0],[-5.5,-2],[75.25,null],[140,30],[160,40]]);});
check('ordinary resolved category and ordered numeric series',()=>{assert.deepEqual(baseline.chart.effective.series.map(s=>[s.xKey,s.yKey]),[['period','revenue'],['period','operatingIncome']]);});
check('duplicate categories retain separate wrapper IDs',()=>{const d=baseline.chart.effective.data;assert.equal(d[0].period.value,d[1].period.value);assert.notEqual(d[0].period.id,d[1].period.id);assert.notEqual(baseline.table.rows[0].id,baseline.table.rows[1].id);});
check('filtered displayed order independently specified',()=>{assert.deepEqual(bounded.table.rows.map(r=>r.raw.rowKey),['obs-F','obs-E','obs-A','obs-D','obs-B']);});
check('inclusive displayed bounds and selected numeric order',()=>{assert.equal(bounded.chart.model.cellRange.rowStartIndex,1);assert.equal(bounded.chart.model.cellRange.rowEndIndex,3);assert.deepEqual(bounded.chart.effective.data.map(r=>[r.revenue,r.operatingIncome]),[[140,30],[100,20],[75.25,null]]);assert.deepEqual(bounded.chart.effective.series.map(s=>s.yKey),['operatingIncome','revenue']);});
for(const name of ['numeric-only','multiple-category','formatted-margin','hidden-selected','synthetic-value-getter']){const value=read(name);check(name+' has finite rendered series and six observations',()=>{assert.ok(value.chart.effective.series.length>0);assert.equal(value.chart.effective.data.length,6);});}
const numeric=read('numeric-only'),multiple=read('multiple-category'),hidden=read('hidden-selected');
check('numeric-only generates ordinal category and retains numeric identities',()=>{assert.deepEqual(numeric.chart.effective.series.map(s=>[s.xKey,s.yKey]),[['AG-GRID-DEFAULT-CATEGORY','revenue'],['AG-GRID-DEFAULT-CATEGORY','operatingIncome']]);assert.deepEqual(numeric.chart.effective.data.map(r=>r['AG-GRID-DEFAULT-CATEGORY'].value),[1,2,3,4,5,6]);});
check('two visible categories resolve to period for this fixture',()=>{assert.ok(multiple.table.columns.find(c=>c.id==='region').visible);assert.ok(multiple.table.columns.find(c=>c.id==='period').visible);assert.deepEqual(multiple.chart.model.cellRange.columns,['period','revenue','operatingIncome']);assert.deepEqual(multiple.chart.effective.series.map(s=>s.xKey),['period','period']);});
check('dynamically hidden selected series is absent from chart',()=>{assert.equal(hidden.table.columns.find(c=>c.id==='operatingIncome').visible,false);assert.deepEqual(hidden.chart.model.cellRange.columns,['period','revenue']);assert.deepEqual(hidden.chart.effective.series.map(s=>s.yKey),['revenue']);});
const formatted=read('formatted-margin');
check('normalizedPercent presentation does not scale chart observations',()=>{assert.equal(formatted.table.rows[0].raw.margin,0.2);assert.equal(formatted.chart.effective.data[0].margin,0.2);assert.ok(formatted.table.domRows.some(r=>r.cells.some(c=>c.columnId==='margin'&&c.text.includes('20'))));});
const getter=read('synthetic-value-getter');
check('synthetic getter uses grid value rather than raw provider value',()=>{assert.equal(getter.table.rows[0].raw.revenue,100);assert.equal(getter.table.rows[0].grid.revenue,200);assert.deepEqual(getter.chart.effective.data.map(r=>r.revenue),[200,0,-11,150.5,280,320]);});
fs.writeFileSync(root+'/assertions.json',JSON.stringify({passed:results.every(x=>x.passed),results},null,2));
console.log(JSON.stringify({checks:results.length,failed:results.filter(x=>!x.passed)}));
if(results.some(x=>!x.passed))process.exitCode=1;
