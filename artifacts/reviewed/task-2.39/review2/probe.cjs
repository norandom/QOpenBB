const fs = require('node:fs');
const path = require('node:path');
const stage = JSON.parse(fs.readFileSync('/mnt/d/Source/QOpenBB/artifacts/task-2.39/repair1/source-stage-manifest.json')).stage;
const ts = require(path.join(stage, 'node_modules/typescript'));
require.extensions['.ts'] = (module, filename) => module._compile(ts.transpileModule(fs.readFileSync(filename, 'utf8'), {compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText,filename);
const {captureDisplayedChart} = require(path.join(stage,'src/components/General/Table/Chart/application/gridCapture.ts'));
const {proxy,revoke} = Proxy.revocable({}, {}); revoke();
const input = {
 api: {isDestroyed:()=>false,getGridOption:k=>k==='rowData'?[]:undefined,getDisplayedRowCount:()=>1,getDisplayedRowAtIndex:()=>({id:'r'}),getCellValue:()=>{throw proxy;},getColumns:()=>[],getPinnedTopRowCount:()=>0,getPinnedBottomRowCount:()=>0},
 stamp:{address:{widgetId:'w',stateKey:'s',stateAddress:'["w","s"]'},generation:1,dataRevision:1,renderRevision:1},
 range:{columnIds:['category','value'],originalRange:{}},categoryColumnId:'category',
 columns:[{id:'category',label:'Category',role:'category'},{id:'value',label:'Value',role:'number'}],originalModel:{}
};
try { console.log(JSON.stringify(captureDisplayedChart(input))); }
catch(error) { console.error('ESCAPED:', error.stack); process.exitCode=1; }
