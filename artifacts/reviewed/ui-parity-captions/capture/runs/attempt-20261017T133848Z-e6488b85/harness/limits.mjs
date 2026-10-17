export const limits = Object.freeze({interactions:240,edits:96,action:4000,navigation:20000,
  settlement:12000,case:90000,weightCase:240000,paddingCase:120000,journey:900000,
  startup:180000,cleanup:90000,outer:1350000,snapshotBytes:1048576,jsonBytes:33554432,
  actionEvents:8,caseEvents:96,events:512,diagnostics:256,sceneNodes:160,axisLabels:64,
  ancestors:8,options:64,optionChars:128,controls:128,fieldChars:512,panelChars:8192,
  diagnosticChars:2048,controlMarkupBytes:16384,caseMarkupBytes:65536});
export const roles = Object.freeze([
  {label:'Chart Title',text:'Financial performance',key:'title'},
  {label:'Subtitle',text:'USD millions, 2024 quarters',key:'subtitle'},
  {label:'Horizontal Axis Title',text:'Reporting quarter',type:'category',position:'bottom'},
  {label:'Vertical Axis Title',text:'USD millions',type:'number',position:'left'}]);
export const rows = Object.freeze([
  {period:'2024-Q1',revenue:100,operatingIncome:20},
  {period:'2024-Q2',revenue:120,operatingIncome:25},
  {period:'2024-Q3',revenue:140,operatingIncome:30},
  {period:'2024-Q4',revenue:160,operatingIncome:40}]);
