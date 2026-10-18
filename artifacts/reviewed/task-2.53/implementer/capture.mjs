import { chromium, expect } from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
const dir='/mnt/d/Source/QOpenBB/artifacts/task-2.53/implementer';
const env={...process.env}; delete env.WAYLAND_DISPLAY;
const browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
try {
 const context=await browser.newContext({viewport:{width:900,height:850}});
 const page=await context.newPage(); page.setDefaultTimeout(3000); const errors=[]; const failures=[];
 page.on('pageerror',e=>errors.push(e.message)); page.on('console',m=>{if(m.type()==='error')errors.push(m.text());}); page.on('requestfailed',r=>failures.push(r.url()));
 const cdp=await context.newCDPSession(page); await cdp.send('Runtime.enable'); await cdp.send('Network.enable');
 await page.goto('http://127.0.0.1:6017/',{waitUntil:'networkidle'});
 for(const theme of ['light','dark']) {
  const panel=page.locator(`[data-theme="${theme}"]`);
  await panel.getByRole('tab',{name:'Customize',exact:true}).click();
  await panel.getByRole('button',{name:'Chart Style',exact:true}).click();
  const padding=panel.getByRole('group',{name:'Padding',exact:true});
  await padding.getByLabel('Left value',{exact:true}).fill('67.5');
  await padding.getByLabel('Right value',{exact:true}).fill('13');
  await expect(padding.getByLabel('Top value',{exact:true})).toHaveValue('20');
  await panel.getByRole('button',{name:'Collapse chart editor'}).click();
  await panel.getByRole('button',{name:'Chart settings',exact:true}).click();
  await expect(padding.getByLabel('Left value',{exact:true})).toHaveValue('67.5');
 }
 await page.screenshot({path:dir+'/dock-padding-light-dark.png'});
 for(const theme of ['light','dark']) {
  const panel=page.locator(`[data-theme="${theme}"]`);
  await panel.getByRole('button',{name:'Chart Style',exact:true}).click();
  await panel.getByRole('button',{name:'Legend',exact:true}).click();
  const legend=panel.getByRole('group',{name:'Legend',exact:true});
  await legend.getByLabel('Position',{exact:true}).selectOption('right');
  await legend.getByLabel('Spacing value',{exact:true}).fill('245.5');
  await legend.getByRole('switch',{name:'Enabled',exact:true}).click();
  await expect(legend.getByLabel('Position',{exact:true})).toHaveCount(0);
  await legend.getByRole('switch',{name:'Enabled',exact:true}).click();
  await expect(legend.getByLabel('Position',{exact:true})).toHaveValue('right');
  await panel.getByRole('tab',{name:'Set Up',exact:true}).click();
  await expect(panel.getByLabel('Category',{exact:true})).toHaveValue('period');
  await panel.getByRole('tab',{name:'Customize',exact:true}).click();
  await expect(panel.getByRole('button',{name:'Legend',exact:true})).toHaveAttribute('aria-expanded','false');
  await panel.getByRole('button',{name:'Chart Style',exact:true}).click();
  await expect(panel.getByLabel('Left value',{exact:true})).toHaveValue('67.5');
  await panel.getByRole('button',{name:'Chart Style',exact:true}).click();
  await panel.getByRole('button',{name:'Legend',exact:true}).click();
  await expect(legend.getByLabel('Position',{exact:true})).toHaveValue('right');
  await expect(legend.getByLabel('Spacing value',{exact:true})).toHaveValue('245.5');
  await expect(legend.getByLabel('Spacing',{exact:true})).toHaveAttribute('max','245.5');
 }
 await page.screenshot({path:dir+'/dock-legend-light-dark.png'});
 expect(errors).toEqual([]); expect(failures).toEqual([]);
 fs.writeFileSync(dir+'/browser-results.json',JSON.stringify({status:'passed',checks:['real dock padding/legend composition','light/dark','independent retained padding edits','legend enabled/details retention','legend position/decimal spacing survives tab remount','expanded maximum retained','Set Up remains available'],errors,networkFailures:failures,cdp:['Runtime.enable','Network.enable']},null,2)+'\n');
} finally {await browser.close();}
