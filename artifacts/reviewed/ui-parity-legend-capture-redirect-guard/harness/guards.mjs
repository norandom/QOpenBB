import {rows} from './limits.mjs';
export function assertFixture(s,baseline=null){
  const require=(v,m)=>{if(!v)throw Error('fixture-unresolved: '+m);};
  require(s.model.chartType.value==='groupedColumn','groupedColumn');
  require(JSON.stringify(s.model.cellRange.columns)==='["period","revenue","operatingIncome"]','column order');
  const first=s.model.cellRange.rowStartIndex.value,last=s.model.cellRange.rowEndIndex.value;
  require(first===null&&last===null||first===0&&last===3,'whole-table or four rows');
  require(s.model.switchCategorySeries.value===false,'Switch category/series false');
  require(s.model.aggFunc.kind!=='value'||s.model.aggFunc.value==null,'Aggregate off');
  for(let i=0;i<4;i++){const r=s.data[i],period=r.period.wrapper?.value?.value??r.period.value;
    require(period===rows[i].period&&r.amounts.revenue.value===rows[i].revenue&&r.amounts.operatingIncome.value===rows[i].operatingIncome,'quarter/value order');}
  const names=['Revenue (USD millions)','Operating Income (USD millions)'];
  require(s.sourceSeries.length===2&&s.live.scene.items.length===2,'two series');
  for(let i=0;i<2;i++){const source=s.sourceSeries[i].identity,item=s.live.scene.items[i],live=item.series;
    require(source.xKey.value==='period'&&source.yKey.value===['revenue','operatingIncome'][i]&&source.yName.value===names[i],'source series keys/names');
    for(let j=0;j<4;j++)require(s.sourceSeries[i].inputValues[j].amount.value===rows[j][source.yKey.value],'source input series values');
    require(item.datum.seriesId.value===live.identity.id.value&&item.datum.label.text.value===names[i],'legend datum mapping');
    if(source.id.kind==='value')require(source.id.value===live.identity.id.value,'source/live series id');
    require(live.visible.value===true&&live.contentGroup.fields.visible.value===true,'both series visible');
    if(baseline)require(live.identity.id.value===baseline.live.scene.items[i].series.identity.id.value&&item.datum.itemId.value===baseline.live.scene.items[i].datum.itemId.value,'stable generated identities');
  }
  if(s.dom.aggregate.length)require(s.dom.aggregate.length===1&&s.dom.aggregate[0].checked===false,'Aggregate checkbox');
  if(s.dom.switchCategorySeries.length)require(s.dom.switchCategorySeries.length===1&&s.dom.switchCategorySeries[0].checked===false,'Switch checkbox');
}
export function arranged(s,orientation){
  const items=s.live.scene.items.map(i=>i.proxy?.rect);if(items.some(i=>!i))return false;
  const a=items[0],b=items[1],v=(r,k)=>r[k]?.value;
  return orientation==='row'?Math.abs(v(a,'y')-v(b,'y'))<=1&&v(b,'x')>v(a,'x'):
    Math.abs(v(a,'x')-v(b,'x'))<=1&&v(b,'y')>v(a,'y');
}
