import fs from 'node:fs';import assert from 'node:assert/strict';
const dir=new URL('.',import.meta.url);const read=n=>JSON.parse(fs.readFileSync(new URL(n+'.json',dir)));
const checks=[];const check=(name,fn)=>{fn();checks.push({name,passed:true});};
const ledger=read('event-ledger');
check('seven UI edits completed',()=>assert.equal(ledger.length,7));
for(const mode of ['Single','Multiple','Compact']){
 const row=ledger.find(x=>x.label==='tooltip-'+mode);
 check(mode+' emits options event',()=>assert.ok(row.after.events.length>row.before.events.length));
 check(mode+' root effective mode',()=>assert.equal(row.after.effective.tooltip.mode,{Single:'single',Multiple:'shared',Compact:'compact'}[mode]));
 check(mode+' exact original bar patch',()=>assert.equal(row.after.model.chartOptions.bar.tooltip.mode,{Single:'single',Multiple:'shared',Compact:'compact'}[mode]));
 const hover=read('tooltip-'+mode+'-hover');
 check(mode+' exact rendered content',()=>{const expected={Single:'2024-Q1 Revenue (USD millions) 100',Multiple:'2024-Q1 Revenue (USD millions) 100 Operating Income (USD millions) 20',Compact:'Revenue (USD millions) 100'}[mode];assert.ok(hover.attempts.some(a=>a.visible.some(t=>t.class==='ag-charts-tooltip-content'&&t.text===expected)));});
 check(mode+' rendered numeric tooltip',()=>assert.ok(hover.attempts.some(a=>a.visible.some(t=>t.text.includes('100')))));
}
const on=read('setup-Switch-Category-Series-on').state,off=read('setup-Switch-Category-Series-off').state;
check('transpose model on',()=>assert.equal(on.model.switchCategorySeries,true));
check('transpose complete data',()=>assert.deepEqual(on.effective.data,[{'AG-GRID-DEFAULT-CATEGORY':{id:0,value:'Revenue (USD millions)'},'period:0':100,'period:1':120,'period:2':140,'period:3':160},{'AG-GRID-DEFAULT-CATEGORY':{id:1,value:'Operating Income (USD millions)'},'period:0':20,'period:1':25,'period:2':30,'period:3':40}]));
check('transpose y bindings',()=>assert.deepEqual(on.effective.series.map(s=>s.yKey),['period:0','period:1','period:2','period:3']));
check('transpose restored flag',()=>assert.equal(off.model.switchCategorySeries,false));
check('transpose restored numerical rows',()=>assert.deepEqual(off.effective.data.map(r=>[r.period.value??r.period,r.revenue,r.operatingIncome]),[['2024-Q1',100,20],['2024-Q1',120,25],['2024-Q3',140,30],['2024-Q4',160,40]]));
check('transpose restored series',()=>assert.deepEqual(off.effective.series.map(s=>s.yKey),['revenue','operatingIncome']));
const aggregateOff=read('setup-Aggregate-off').state;
check('sum off removes aggFunc',()=>assert.equal(aggregateOff.model.aggFunc,undefined));
check('sum off restores all rows',()=>assert.deepEqual(aggregateOff.effective.data.map(r=>[r.period.value??r.period,r.revenue,r.operatingIncome]),[['2024-Q1',100,20],['2024-Q1',120,25],['2024-Q3',140,30],['2024-Q4',160,40]]));
const agg=read('setup-Aggregate-on').state,geometry=read('setup-Aggregate-on-geometry');
check('sum model',()=>assert.equal(agg.model.aggFunc,'sum'));
check('sum numeric rows',()=>assert.deepEqual(agg.effective.data.map(r=>[r.period.value??r.period,r.revenue,r.operatingIncome]),[['2024-Q1',220,45],['2024-Q3',140,30],['2024-Q4',160,40]]));
for(const [i,expected] of [[0,[220,140,160]],[1,[45,30,40]]]){
 check('settled series '+i+' numeric geometry',()=>assert.deepEqual(geometry.series[i].data.map(n=>n.yValue),expected));
 check('settled series '+i+' proportional heights',()=>{const ds=geometry.series[i].data;const scale=ds[0].height/ds[0].yValue;assert.ok(scale>0);for(const n of ds)assert.ok(Math.abs(n.height-n.yValue*scale)<0.01);});
}
fs.writeFileSync(new URL('verification.json',dir),JSON.stringify({checks,count:checks.length,exitCode:0},null,2));console.log(JSON.stringify({checks:checks.length,passed:true}));
