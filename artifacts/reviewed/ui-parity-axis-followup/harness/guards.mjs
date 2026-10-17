function requireValue(condition,message){if(!condition)throw Error(message);}
export function assertFinancialData(data,fixture,fixtures){
  requireValue(data.value?.length===4,'Exact four finite fixture rows required');
  for(const [i,row] of data.value.entries()){
    const period=row.period.value,actual=period.type==='category-wrapper'?period.fields.value.value:period.value;
    requireValue(actual===fixture.periods[i]&&row.amounts.revenue.value===fixtures.revenue[i]&&row.amounts.operatingIncome.value===fixtures.operatingIncome[i],'Exact synthetic reporting period and USD-million amounts required');
  }
}
export function assertBaseline(snapshot){
  requireValue(snapshot.live.axes.length===2,'Two baseline axes required');
  for(const [direction,type,position,auto] of [['x','category','bottom',true],['y','number','left',false]]){
    const axes=snapshot.live.axes.filter(a=>a.identity.direction.value===direction);requireValue(axes.length===1,'Unique physical baseline role');
    const a=axes[0],label=a.style.label.value;
    requireValue(a.identity.type.value===type&&a.identity.position.value===position&&a.style.tick.value.enabled.value===false,'Conflicting baseline axis role/type/position/ticks');
    requireValue(label.fontFamily.value==='Verdana, sans-serif'&&label.fontSize.value===11&&label.spacing.value===11&&label.autoRotate.value===auto,'Conflicting baseline typography/spacing/Auto Rotate');
  }
}
export function assertLabelUI(actual,expected){
  for(const key of ['family','size','spacing','auto'])requireValue(actual[key]===expected[key],'Label restoration mismatch '+key);
  if(!actual.auto)requireValue(Number(actual.rotation)===Number(expected.rotation),'Label restoration mismatch manual rotation');
}
