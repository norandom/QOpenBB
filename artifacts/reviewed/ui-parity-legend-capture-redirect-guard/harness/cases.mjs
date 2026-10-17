export async function executeCases(api){
  const {controls:c,step,menu,number,checkpoint,runCase,record}=api;
  const value=async name=>(await c.numeric(name)).inputValue();
  const comboValue=async name=>(await (await c.combo(name)).textContent()).trim();
  async function range(name,required=null){
    const locator=await c.numeric(name,'range');await step(name+' range focus',locator,'click',undefined,{potentialMutation:true,raster:true});
    const actual=await value(name);record('range-focus',{name,actual,required});
    if(required!==null&&actual!==String(required)){record('subprobe',{name,status:'range-click-changed',actual});return;}
    await step(name+' ArrowRight',await c.numeric(name,'range'),'press','ArrowRight',{potentialMutation:true,raster:true});
  }
  async function numericCase(id,name,target,strict=false){await runCase(id,async()=>{await c.inventory();const baseline=await value(name);await checkpoint(id+'-baseline',true);
    await number(name,target);await range(name,strict?target:null);await number(name+' restore',baseline,name);record('restoration',{name,expected:baseline,actual:await value(name),rawByteIdentityClaimed:false});});}
  await runCase('L01',async()=>{await c.inventory();if(await comboValue('Position')!=='Top')throw Error('baseline-unresolved: Position Top');await checkpoint('L01-baseline',true);
    for(const position of ['Right','Bottom','Left','Top'])await menu('Position',position);});
  await numericCase('L02','Spacing',44,true);
  await numericCase('L03','Marker Size',19);
  await numericCase('L04','Marker Stroke',5);
  await numericCase('L05','Item Spacing',13);
  await runCase('L06',async()=>{await c.inventory();const x=await value('Horizontal Spacing'),y=await value('Vertical Spacing');
    const top=await checkpoint('L06-top-baseline',true);record('layout',{orientation:'row',available:api.arranged(top.snapshot,'row'),status:api.arranged(top.snapshot,'row')?'available':'layout-discriminator-unavailable'});
    await number('Horizontal Spacing',7);await range('Horizontal Spacing');await number('Horizontal Spacing restore',x,'Horizontal Spacing');
    await menu('Position','Right');const right=await checkpoint('L06-right-baseline',true);record('layout',{orientation:'column',available:api.arranged(right.snapshot,'column'),status:api.arranged(right.snapshot,'column')?'available':'layout-discriminator-unavailable'});
    await number('Vertical Spacing',21);await range('Vertical Spacing');await number('Vertical Spacing restore',y,'Vertical Spacing');await menu('Position','Top');});
  await runCase('L07',async()=>{await c.inventory();const family=await comboValue('Font'),size=await comboValue('Size');await checkpoint('L07-baseline',true);
    await menu('Font','Courier New, monospace');await menu('Size','18');await menu('Size',size);await menu('Font',family);});
  await runCase('L08',async()=>{await c.inventory();const spacing=await value('Spacing'),size=await comboValue('Size');
    await number('Spacing',44);await menu('Size','18');const retained=await checkpoint('L08-retained',true);record('retained-tuple',{observation:retained.id});
    const enabled=await c.enabled();if(!await enabled.isChecked())throw Error('baseline-unresolved: Enabled');
    await step('Enabled focus',enabled,'focus');await step('Enabled off',await c.enabled(),'press','Space',{potentialMutation:true,raster:true});
    await step('Enabled on',await c.enabled(),'press','Space',{potentialMutation:true,raster:true});
    const on=await checkpoint('L08-on-retained');const same=JSON.stringify(retained.snapshot.effective)===JSON.stringify(on.snapshot.effective);
    record('retained-tuple-comparison',{before:retained.id,after:on.id,same});if(!same)throw Error('legend-retention-mismatch');
    await number('Spacing restore',spacing,'Spacing');await menu('Size',size);});
}
