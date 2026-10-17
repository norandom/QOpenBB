export async function expandSeries(heading,click,retain){
  const before=await heading.getAttribute('aria-expanded');
  const receipt={kind:'series-expansion',before,after:null,clicked:false,status:'before'};retain({...receipt});
  if(!['true','false'].includes(before))throw Error('Series expanded contract missing');
  if(before==='false'){receipt.clicked=true;await click('Expand Series',heading);}
  receipt.after=await heading.getAttribute('aria-expanded');receipt.status='after';retain({...receipt});
  if(receipt.after!=='true')throw Error('Series expansion unresolved');
}
export const columnNames=/^(Grouped Column|Stacked Column)(\. Selected)?$/;
export function controls(page,input,retain=()=>{}){
  const panel=()=>page.locator('.ag-chart-docked-container');
  async function one(locator){await locator.waitFor({state:'visible',timeout:4000});if(await locator.count()!==1)throw Error('Unique visible control required');return locator;}
  const click=async(label,l)=>input(label,await one(l),'click');
  const group=()=>panel().locator('.ag-charts-format-top-level-group').filter({has:page.locator('.ag-charts-format-top-level-group-title-bar').filter({hasText:/^\s*Series\s*$/})});
  async function open(){if(await panel().isVisible())return;await click('Widget menu',page.locator('button').filter({has:page.locator('svg#list-unordered')}));
    await click('Chart settings',page.getByRole('menuitem',{name:'Chart settings',exact:true}));}
  async function mode(name){await open();await click('Customize',panel().getByRole('tab',{name:'Customize',exact:true}));
    const heading=await one(group().locator(':scope > .ag-charts-format-top-level-group-title-bar'));
    await expandSeries(heading,click,retain);
    await click('Tooltip Mode',group().getByRole('combobox',{name:'Tooltip Mode',exact:true}));
    await click('Mode '+name,page.getByRole('option',{name,exact:true}));}
  async function family(name){await open();await click('Chart',panel().getByRole('tab',{name:'Chart',exact:true}));
    let thumbnails=null;if(name==='stackedColumn'){
      const candidates=panel().getByRole('button',{name:columnNames,exact:true}),count=await candidates.count();
      retain({kind:'column-thumbnail-count',count});if(count>32)throw Error('Thumbnail bound 32');
      thumbnails=await candidates.evaluateAll(xs=>xs.filter(n=>n.getClientRects().length).map(n=>({role:n.getAttribute('role')||'button',name:n.getAttribute('aria-label')||n.textContent.trim(),selected:n.getAttribute('aria-pressed')})));
      retain({kind:'column-thumbnails',thumbnails});}
    const target={groupedColumn:/^Grouped Column(\. Selected)?$/,line:'Line',stackedColumn:/^Stacked Column(\. Selected)?$/}[name];
    const button=panel().getByRole('button',{name:target,exact:true});
    if(name==='stackedColumn'&&await button.count()!==1)throw Error('selector-unresolved: unique Stacked Column required');
    await click('Family '+name,button);return thumbnails;}
  async function close(){const close=page.locator('.ag-tabs-close-button.ag-chart-tabbed-menu-close-button');if(await close.isVisible())await click('Close editor',close);}
  return {one,mode,family,close};
}
