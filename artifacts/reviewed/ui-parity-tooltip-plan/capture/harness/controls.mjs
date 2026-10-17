export function controls(page,input){
  const panel=()=>page.locator('.ag-chart-docked-container');
  async function one(locator){await locator.waitFor({state:'visible',timeout:4000});if(await locator.count()!==1)throw Error('Unique visible control required');return locator;}
  const click=async(label,l)=>input(label,await one(l),'click');
  const group=()=>panel().locator('.ag-charts-format-top-level-group').filter({has:page.locator('.ag-charts-format-top-level-group-title-bar').filter({hasText:/^\s*Series\s*$/})});
  async function open(){if(await panel().isVisible())return;await click('Widget menu',page.locator('button').filter({has:page.locator('svg#list-unordered')}));
    await click('Chart settings',page.getByRole('menuitem',{name:'Chart settings',exact:true}));}
  async function mode(name){await open();await click('Customize',panel().getByRole('tab',{name:'Customize',exact:true}));
    const heading=await one(group().locator('.ag-charts-format-top-level-group-title-bar'));
    const expanded=await heading.evaluate(n=>n.closest('.ag-charts-format-top-level-group').className.includes('expanded'));
    if(!expanded)await click('Expand Series',heading);
    await click('Tooltip Mode',group().getByRole('combobox',{name:'Tooltip Mode',exact:true}));
    await click('Mode '+name,page.getByRole('option',{name,exact:true}));}
  async function family(name){await open();await click('Chart',panel().getByRole('tab',{name:'Chart',exact:true}));
    let thumbnails=null;if(name==='stackedColumn'){const buttons=await panel().getByRole('button').evaluateAll(xs=>xs.filter(n=>n.getClientRects().length).map(n=>({role:n.getAttribute('role')||'button',name:n.getAttribute('aria-label')||n.textContent.trim(),selected:n.getAttribute('aria-pressed')})));
      if(buttons.length>32)throw Error('Thumbnail bound 32');thumbnails=buttons;}
    await click('Family '+name,panel().getByRole('button',{name:{groupedColumn:'Grouped Column',line:'Line',stackedColumn:'Stacked Column'}[name],exact:true}));return thumbnails;}
  async function close(){const close=page.locator('.ag-tabs-close-button.ag-chart-tabbed-menu-close-button');if(await close.isVisible())await click('Close editor',close);}
  return {one,mode,family,close};
}
