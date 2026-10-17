export async function expandAxis(group,role,one,step){
  if(await group.count()!==1)throw Error('Axis group cardinality');
  const heading=group.locator(':scope > .ag-charts-format-top-level-group-title-bar');await one(heading);
  const state=await heading.getAttribute('aria-expanded');
  if(!['true','false'].includes(state))throw Error('Expansion aria state missing');
  if(state==='false')await step('Expand '+role,heading,'click');
}
