import fs from 'node:fs';
import {createHash} from 'node:crypto';
export const source='38dffc33389aca0e4a87e0e88d42f7067aa220df';
export const image='sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f';
export const planHash='95c7f4384c6c25ea48e99859126e03713c14f09645ed75adbba0e657abf2dbdd';
export const fixtureHash='bda68b15aee2192684d67086c4a599f852943a3079882d4aeb744e6efab262ad';
export const limits=Object.freeze({cases:8,setupActions:24,caseActions:36,keyboardActions:120,totalActions:396,
  caseMs:60000,keyboardMs:120000,startupMs:180000,casesMs:600000,cleanupMs:60000,outerMs:900000,inputStopMs:840000,
  selectorMs:4000,settlementMs:6000,updateMs:4000,geometrySamples:8,geometryIntervalMs:250,
  tooltipSamples:20,tooltipIntervalMs:100,tooltipMs:2000,screenshots:48,probes:96,
  caseBytes:131072,jsonBytes:2097152,pngBytes:2097152,runBytes:104857600,htmlBytes:8192});
export const keys=['cashFlow','operatingIncome','revenue'];
export const cases=[
  {id:'T01',family:'groupedColumn',mode:'Single',probes:[[0,'cashFlow'],[0,'operatingIncome'],[0,'revenue']]},
  {id:'T02',family:'groupedColumn',mode:'Single',probes:[[1,'revenue'],[1,'operatingIncome'],[0,'revenue']]},
  {id:'T03',family:'groupedColumn',mode:'Multiple',probes:[[2,'operatingIncome','cashFlow'],[3,'operatingIncome']]},
  {id:'T04',family:'groupedColumn',mode:'Multiple',probes:[[4,'revenue'],[4,'operatingIncome'],[0,'cashFlow'],[1,'cashFlow']]},
  {id:'T05',family:'groupedColumn',mode:'Compact',probes:[[0,'cashFlow'],[0,'operatingIncome'],[0,'revenue'],[1,'revenue'],[4,'revenue']]},
  {id:'T06',family:'groupedColumn',keyboard:true,modes:['Single','Multiple','Compact'],tabCap:24,
    sequence:['ArrowRight','ArrowRight','ArrowDown','ArrowUp','ArrowLeft','Escape','Tab']},
  {id:'T07',family:'line',mode:'Single',probes:[[4,'revenue'],[0,'cashFlow'],[2,'cashFlow','Multiple'],[3,'operatingIncome','Multiple']]},
  {id:'T08',family:'stackedColumn',mode:'Multiple',probes:[[0,'cashFlow'],[4,'revenue'],[1,'operatingIncome','Compact']]},
];
export const hash=bytes=>createHash('sha256').update(bytes).digest('hex');
export const canonical=v=>Array.isArray(v)?'['+v.map(canonical).join(',')+']':v&&typeof v==='object'?
  '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}':JSON.stringify(v);
export function fixture(){const value=JSON.parse(fs.readFileSync(new URL('./fixture.json',import.meta.url)));
  if(hash(canonical(value))!==fixtureHash)throw Error('Frozen fixture mismatch');return value;}
