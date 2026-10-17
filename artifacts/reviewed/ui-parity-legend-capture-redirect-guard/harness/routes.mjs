// Context routes include popups; every specialized callback rechecks origin itself.
export async function registerRoutes({context,runtime,fixture,rows,diagnostic}){
  async function allowed(route){
    let url;try{url=new URL(route.request().url());}catch{diagnostic('externalDenied',{invalidURL:true});await route.abort();return false;}
    if(!['http:','https:'].includes(url.protocol)){diagnostic('externalDenied',{reason:'unsupported-protocol',scheme:url.protocol.slice(0,32)});await route.abort();return false;}
    if(url.origin===runtime.origin)return true;
    diagnostic('externalDenied',{reason:'unapproved-origin',scheme:url.protocol});await route.abort();return false;
  }
  async function reject(route,reason){diagnostic('externalDenied',{reason});await route.abort();throw Error('traffic-unresolved: '+reason);}
  async function noFollow(route){
    // Omitting method/postData overrides preserves this intercepted request's method/body.
    let response;try{response=await route.fetch({maxRedirects:0,maxRetries:0,timeout:4000});}catch{return reject(route,'request-fetch-failed');}
    let url;try{url=new URL(response.url());}catch{return reject(route,'invalid-response-identity');}
    if(!['http:','https:'].includes(url.protocol)||url.origin!==runtime.origin)return reject(route,'foreign-response-identity');
    const status=response.status(),headers=response.headers();
    if(status>=300&&status<400)return reject(route,'redirect-response-'+status);
    if(Object.keys(headers).some(key=>key.toLowerCase()==='location'))return reject(route,'location-transition');
    return response;
  }
  await context.route('**/*',async route=>{if(!await allowed(route))return;return route.fulfill({response:await noFollow(route)});});
  await context.route('**/api/pro/dash/{sync,validate-and-sync}',async route=>{
    if(!await allowed(route))return;
    const response=await noFollow(route);
    if(route.request().method()!=='GET')return route.fulfill({response});
    const actual=await response.json();
    return route.fulfill({response,json:{...actual,owned:Object.fromEntries(Object.entries(fixture).map(([key,content])=>[key,{content,is_shared:false,created_by:'Synthetic Parity',created_date:'2026-10-17T00:00:00Z',updated_date:'2026-10-17T00:00:00Z'}])),shared:{},entity_shared:{}}});
  });
  await context.route('**/synthetic_financials',async route=>{if(await allowed(route))return route.fulfill({json:rows});});
}
