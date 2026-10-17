import fs from 'node:fs';
const out='/mnt/d/Source/QOpenBB/artifacts/parity/grid-runtime-next';
const fixture=JSON.parse(fs.readFileSync('/mnt/d/Source/QOpenBB/artifacts/parity/editor-contract-retry/fixture.json'));
const widget=fixture['11111111-1111-4111-8111-111111111111'].data.widgets[0];
widget.name='Synthetic Grid Observations';
widget.endpoint.url='__ORIGIN__/synthetic_financials';
widget.data.table.columnsDefs=[
 {field:'period',headerName:'Period',cellDataType:'text',chartDataType:'category'},
 {field:'revenue',headerName:'Revenue (USD millions)',cellDataType:'number',chartDataType:'series'},
 {field:'operatingIncome',headerName:'Operating Income (USD millions)',cellDataType:'number',chartDataType:'series'},
 {field:'region',headerName:'Region',cellDataType:'text',chartDataType:'category',hide:true},
 {field:'margin',headerName:'Margin',cellDataType:'number',chartDataType:'series',formatterFn:'normalizedPercent',hide:true},
 {field:'rowKey',headerName:'Synthetic observation ID',cellDataType:'text',chartDataType:'category',hide:true}
];
widget.storage={chartModel:{chartType:'groupedColumn',cellRange:{columns:['period','revenue','operatingIncome']}}};
fs.writeFileSync(out+'/fixture.json',JSON.stringify(fixture,null,2));
fs.writeFileSync(out+'/rows.json',JSON.stringify([
 {rowKey:'obs-A',period:'2024-Q1',region:'North',revenue:100,operatingIncome:20,margin:0.2},
 {rowKey:'obs-B',period:'2024-Q1',region:'South',revenue:0,operatingIncome:0,margin:0},
 {rowKey:'obs-C',period:'2024-Q2',region:'North',revenue:-5.5,operatingIncome:-2,margin:-0.1},
 {rowKey:'obs-D',period:'2024-Q3',region:'South',revenue:75.25,operatingIncome:null,margin:0.125},
 {rowKey:'obs-E',period:'2024-Q4',region:'North',revenue:140,operatingIncome:30,margin:0.2142857143},
 {rowKey:'obs-F',period:'2025-Q1',region:'South',revenue:160,operatingIncome:40,margin:0.25}
],null,2));
