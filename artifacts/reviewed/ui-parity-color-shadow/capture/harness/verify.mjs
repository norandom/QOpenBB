import fs from 'node:fs';
import {root,json} from './io.mjs';
const load=name=>JSON.parse(fs.readFileSync(root+'/'+name+'.json'));
const checks=[];const check=(name,passed,detail=null)=>{checks.push({name,passed:!!passed,detail});};
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b),value=o=>Object.fromEntries(Object.entries(o).map(([k,v])=>[k,v.value]));
const summary=load('summary'),ledger=load('action-ledger'),events=load('events'),raster=load('raster-measurements');
check('run-exit0',load('run-status').exitCode===0);check('cleanup-exit0',load('cleanup-status').exitCode===0);
const cleanup=load('cleanup-report'),browser=load('browser-cleanup');
check('exact-owned-cleanup',cleanup.containerAbsent&&cleanup.stateAbsent&&cleanup.credentialAbsent&&cleanup.remainingOwnedState.length===0);
check('browser-listener-cleanup',browser.browserClosed&&browser.listenerRemoved);
check('nine-cases',same(summary.cases.map(c=>c.id),Array.from({length:9},(_,i)=>'C0'+(i+1))));
const opens=ledger.filter(a=>/ open$/.test(a.label));
const conservativeChangingActions=summary.potentiallyChangingActions+opens.length;
check('action-caps',ledger.length===summary.actions&&ledger.length<=80&&conservativeChangingActions<=20,{actions:ledger.length,predeclaredMutations:summary.potentiallyChangingActions,pickerOpens:opens.length,conservativeChangingActions});
check('arrow-directions',same(ledger.filter(a=>a.intendedValue?.startsWith('Arrow')).map(a=>a.intendedValue),['ArrowRight','ArrowRight','ArrowLeft']));
check('picker-open-events-retained',same(opens.map(a=>a.eventSequence.to-a.eventSequence.from),[1,0,1,1]));
check('event-cap',events.length<=64&&fs.statSync(root+'/events.json').size<=2097152,{events:events.length,bytes:fs.statSync(root+'/events.json').size});
const shots=load('screenshots');check('screenshot-cap',shots.length<=24&&shots.length===summary.screenshots,shots.length);
const snapshots=fs.readdirSync(root).filter(n=>/^C\d\d.*\.json$|^setup\.s\d+-(before|after)\.json$/.test(n)&&n!=='C03-invalid-check.json');
check('all-checkpoint-byte-cap',snapshots.every(n=>fs.statSync(root+'/'+n).size<=262144),{count:snapshots.length,max:Math.max(...snapshots.map(n=>fs.statSync(root+'/'+n).size))});
const baseline=load('C01-baseline'),last=load('C09.s03-after'),off=load('C09.s02-after'),beforeOff=load('C09.s02-before');
const channels=s=>s.live.series.map(x=>({fill:x.properties.fill,stroke:x.properties.stroke,marker:x.properties.marker,nodes:x.nodes.map(n=>({fill:n.fill,stroke:n.stroke,fillOpacity:n.fillOpacity,strokeOpacity:n.strokeOpacity}))}));
check('all-series-color-channels-retained',snapshots.every(n=>same(channels(JSON.parse(fs.readFileSync(root+'/'+n))),channels(baseline))));
check('scene-cardinality-and-ancestry',snapshots.every(n=>{const s=JSON.parse(fs.readFileSync(root+'/'+n));return s.live.axes.length===2&&s.live.series.length===2&&s.live.series.every(x=>x.nodes.length===4&&x.nodes.every(d=>d.parents.length>0&&d.parents.length<=8));}));
const axisStroke=s=>s.effective.axes.find(a=>a.position.value==='bottom').line.stroke.value;
const grid=s=>s.effective.axes.find(a=>a.position.value==='left').gridLine;
const axisStepNames=['C02.s03-after','C02.s04-after','C02.s06-after','C02.s08-after','C02.s10-after'];
const colors=axisStepNames.map(n=>axisStroke(load(n)));
check('three-nonboundary-keyboard-effects',colors.slice(1,4).every((c,i)=>c!==colors[i]),colors);
check('axis-hex6-accepted',colors.at(-1)==='rgb(227, 75, 85)');
check('axis-alpha-string',colors[3]==='rgba(187, 189, 194, 0.971)');
const invalid=load('C03-invalid-check');check('invalid-color-no-event-custom-error',invalid.eventsUnchanged&&!invalid.input.validity.valid&&invalid.input.validity.customError);
check('invalid-color-model-effective-scene-unchanged',['model','effective','live'].every(k=>same(load('C03.s04-before')[k],load('C03.s04-after')[k])));
check('popup-tab-path-and-focus-return',same(['C02.s03-after','C02.s05-after','C02.s07-after','C02.s09-after'].map(n=>load(n).dom.active.dataRef),
  ['spectrumColor','spectrumHueSlider','spectrumAlphaSlider','eInput'])&&['C02.s11-after','C02.s14-after'].every(n=>{const s=load(n);return s.dom.popup===null&&s.dom.active.label==='Color'&&s.dom.active.dataRef==='eWrapper';}));
check('grid-hex8-alpha-string',grid(load('C03.s05-after')).style[0].stroke.value==='rgba(39, 198, 160, 0.502)');
check('no-independent-grid-opacity',grid(last).style.every(s=>s.strokeOpacity.presence==='absent'&&s.opacity.presence==='absent'));
check('axis-grid-width-dash-retained',same(baseline.effective.axes.map(a=>({width:a.line.width,gridWidth:a.gridLine.width,dashes:a.gridLine.style.map(s=>s.lineDash)})),
  last.effective.axes.map(a=>({width:a.line.width,gridWidth:a.gridLine.width,dashes:a.gridLine.style.map(s=>s.lineDash)}))));
const tuple={enabled:true,color:'rgba(249, 195, 61, 0.6)',blur:12,xOffset:-7,yOffset:9};
check('all-processed-live-shadow-tuples',last.effective.series.every(s=>same(value(s.shadow),tuple))&&last.live.series.every(s=>same(value(s.properties.shadow),tuple)&&s.nodes.every(n=>same(value(n.fillShadow),tuple))));
check('disabled-shadow-values-retained',off.live.series.every(s=>s.nodes.every(n=>same(value(n.fillShadow),{...tuple,enabled:false})))&&same(beforeOff.model.chartOptions.bar.value.series.shadow,last.model.chartOptions.bar.value.series.shadow));
const nested=off.dom.groups.find(g=>g.name==='Series').controls.filter(c=>['number','range'].includes(c.type)||c.label==='Color');
check('disabled-shadow-controls-hidden-retained',nested.length===7&&nested.every(c=>!c.visible&&c.disabled!==true));
const modelDelta=(a,b,path='',out=[])=>{if(same(a,b))return out;if(a&&b&&typeof a==='object'&&typeof b==='object'&&!Array.isArray(a)&&!Array.isArray(b)){
  for(const k of new Set([...Object.keys(a),...Object.keys(b)]))modelDelta(a[k],b[k],path?path+'.'+k:k,out);
}else out.push({path,before:a,after:b});return out;};
const deltas=ledger.filter(a=>a.before&&a.after).map(a=>({id:a.id,label:a.label,eventSequence:a.eventSequence,
  deltas:modelDelta(load(a.before.replace('.json','')).model,load(a.after.replace('.json','')).model)}));
json('model-deltas',deltas);
check('off-on-enabled-only-model-deltas',deltas.filter(d=>['C09.s02','C09.s03'].includes(d.id)).every(d=>d.deltas.length===1&&d.deltas[0].path.endsWith('.shadow.enabled.value')));
const rasterByName=new Map(raster.records.map(r=>[r.checkpoint,r]));
check('axis-grid-raster-discriminators',rasterByName.get('C02.s10-after').regions[0].previous.changedPixels>0&&
  rasterByName.get('C02.s10-after').regions[1].previous.changedPixels===0&&rasterByName.get('C03.s05-after').regions[1].previous.changedPixels>0);
const haloNames=['C04.s03-after','C05.s03-after','C06.s01-after','C07.s01-after','C08.s01-after','C09.s02-after','C09.s03-after'];
check('each-shadow-step-halo-raster-changes',haloNames.every(n=>rasterByName.get(n).regions[2].previous.changedPixels>0),haloNames.map(n=>({checkpoint:n,changedPixels:rasterByName.get(n).regions[2].previous.changedPixels})));
check('all-bar-interior-regions-unchanged',raster.records.slice(1).every(r=>r.regions[3].previous.changedPixels===0));
const finalImage=fs.readFileSync(root+'/C09.s03-after-region-2.png'),beforeImage=fs.readFileSync(root+'/C08.s02-after-region-2.png');
check('restored-halo-identical-region',finalImage.equals(beforeImage));
const diag=load('diagnostics');check('diagnostic-caps',!diag.overflow&&diag.records.length<=128&&diag.ownedStatuses.length<=256);
json('diagnostic-summary',{cdp:{runtimeEnabled:true,networkEnabled:true},counts:{records:diag.records.length,ownedPathStatusPairs:diag.ownedStatuses.length},
  records:diag.records,expectedExistingFaults:['HTML datafeed script SyntaxError','empty AI URL warning','onboarding-info initial404','unregistered openbb-light custom chart theme warning'],
  verdict:'Not clean diagnostics; no captured color/Shadow-specific warning. Existing faults remain visible.',blockedOrigins:diag.records.filter(r=>r.kind==='blocked-origin').length});
json('action-ledger-public',ledger.filter(a=>a.before&&a.after));
const jsonFiles=fs.readdirSync(root).filter(n=>n.endsWith('.json')&&!n.includes('private')&&n!=='retained-bytes.json');
json('retained-bytes',{basis:'Actual retained bytes at audit; excludes this receipt, private runtime receipt and credential file; no cumulative overwrite accounting',
  totalJsonBytes:jsonFiles.reduce((sum,n)=>sum+fs.statSync(root+'/'+n).size,0),snapshotJsonBytes:snapshots.reduce((sum,n)=>sum+fs.statSync(root+'/'+n).size,0),
  snapshotCount:snapshots.length,files:Object.fromEntries(jsonFiles.map(n=>[n,fs.statSync(root+'/'+n).size]))});
json('verification',{status:checks.every(c=>c.passed)?'passed':'failed',claim:'Nine bounded original color/Shadow observations and cleanup; no candidate parity, persistence, production or frozen-contract acceptance',checks});
console.log(JSON.stringify({checks:checks.length,failed:checks.filter(c=>!c.passed)}));if(checks.some(c=>!c.passed))process.exitCode=1;
