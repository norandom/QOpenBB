// Context routes include popups; every specialized callback rechecks origin itself.
export async function registerRoutes({context,runtime,fixture,rows,diagnostic}){
  async function allowed(route){
    let url;try{url=new URL(route.request().url());}catch{diagnostic('externalDenied',{invalidURL:true});await route.abort();return false;}
    if(url.origin===runtime.origin)return true;
    diagnostic('externalDenied',{scheme:url.protocol});await route.abort();return false;
  }
  await context.route('**/*',async route=>{if(await allowed(route))return route.continue();});
  await context.route('**/api/pro/dash/{sync,validate-and-sync}',async route=>{
    if(!await allowed(route))return;
    if(route.request().method()!=='GET')return route.continue();
    const response=await route.fetch({maxRedirects:0,timeout:4000});
    if(new URL(response.url()).origin!==runtime.origin||response.status()>=300&&response.status()<400){await route.abort();throw Error('traffic-unresolved: sync redirect');}
    const actual=await response.json();
    return route.fulfill({json:{...actual,owned:Object.fromEntries(Object.entries(fixture).map(([key,content])=>[key,{content,is_shared:false,created_by:'Synthetic Parity',created_date:'2026-10-17T00:00:00Z',updated_date:'2026-10-17T00:00:00Z'}])),shared:{},entity_shared:{}}});
  });
  await context.route('**/synthetic_financials',async route=>{if(await allowed(route))return route.fulfill({json:rows});});
}
