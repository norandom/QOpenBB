export function controlTools(page,step){
  const fail=m=>{throw Error('selector-unresolved: '+m);};
  async function one(locator,visible=true){if(await locator.count()!==1)fail('unique control');if(visible)await locator.waitFor({state:'visible',timeout:4000});return locator;}
  async function panel(){
    const editor=page.locator('.ag-chart-docked-container');await one(editor);
    const heading=editor.locator('.ag-charts-format-top-level-group-title-bar').filter({hasText:/^Legend$/});await one(heading);
    const state=await heading.getAttribute('aria-expanded');if(!['true','false'].includes(state))fail('Legend aria-expanded');
    if(state==='false')await step('Expand Legend',heading,'click');
    if(await heading.getAttribute('aria-expanded')!=='true')fail('Legend expansion');return heading.locator('..');
  }
  async function combo(name){return one((await panel()).getByRole('combobox',{name,exact:true}));}
  async function enabled(){return one((await panel()).getByLabel('Enabled',{exact:true}).and(page.locator('input[type="checkbox"]')));}
  async function numeric(name,type='number'){
    const scope=await panel(),direct=scope.getByLabel(name,{exact:true}).and(page.locator('input[type="'+type+'"]'));
    if(await direct.count()===1)return one(direct);
    const candidates=scope.locator('input[type="'+type+'"]');
    const ids=await candidates.evaluateAll((ns,label)=>ns.filter(n=>{
      const ids=n.getAttribute('aria-labelledby')?.trim().split(/\s+/);return ids?.length&&ids.map(id=>document.getElementById(id)?.textContent?.trim()||'').join(' ')===label;
    }).map(n=>({labelledby:n.getAttribute('aria-labelledby')})),name);
    if(ids.length!==1)fail(name+' '+type+' exact label');
    const attribute=ids[0].labelledby;if(!/^[\w:\s-]+$/.test(attribute))fail('label identity');
    return one(scope.locator('input[type="'+type+'"][aria-labelledby="'+attribute+'"]'));
  }
  async function inventory(){
    const scope=await panel();for(const name of ['Font','Weight','Size','Position'])await combo(name);
    await enabled();for(const name of ['Spacing','Marker Size','Marker Stroke','Item Spacing','Horizontal Spacing','Vertical Spacing']){await numeric(name);await numeric(name,'range');}
    if(await scope.locator('input,[role="combobox"]').count()!==17)fail('exact seventeen named controls');
    const colors=scope.locator('.ag-font-panel .ag-color-picker');if(await colors.count()!==1)fail('Font Color wrapper');
    return scope;
  }
  return {one,panel,combo,enabled,numeric,inventory};
}
