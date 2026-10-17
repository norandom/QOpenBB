import { chromium, expect } from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
const dir='/mnt/d/Source/QOpenBB/artifacts/task-2.49/controller/combined';
const env={...process.env}; delete env.WAYLAND_DISPLAY;
const browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
try {
 const context=await browser.newContext({viewport:{width:900,height:850}});
 const page=await context.newPage(); const errors=[]; const failures=[];
 page.on('pageerror',e=>errors.push(e.message)); page.on('console',m=>{if(m.type()==='error')errors.push(m.text());}); page.on('requestfailed',r=>failures.push(r.url()));
 const cdp=await context.newCDPSession(page); await cdp.send('Runtime.enable'); await cdp.send('Network.enable');
 await page.goto('http://127.0.0.1:6017/',{waitUntil:'networkidle'});
 await page.screenshot({path:dir+'/dock-setup-light-dark.png'});
 for(const theme of ['light','dark']) {
  const panel=page.locator(`[data-theme="${theme}"]`);
  await panel.getByLabel('Category',{exact:true}).selectOption('region');
  await panel.getByRole('switch',{name:'Aggregate',exact:true}).click();
  await panel.getByLabel('Aggregation method').selectOption('average');
  await panel.getByRole('switch',{name:'Switch Category / Series',exact:true}).click();
  await panel.getByRole('button',{name:'Collapse chart editor'}).click();
  await panel.getByRole('button',{name:'Chart settings',exact:true}).click();
  await expect(panel.getByLabel('Category',{exact:true})).toHaveValue('region');
  await expect(panel.getByLabel('Aggregation method')).toHaveValue('average');
  await expect(panel.getByRole('switch',{name:'Switch Category / Series',exact:true})).toBeChecked();
  await panel.getByRole('tab',{name:'Customize',exact:true}).click();
  await panel.getByRole('button',{name:'Titles',exact:true}).click();
  await panel.getByRole('switch',{name:'Chart Title',exact:true}).click();
  await panel.getByRole('group',{name:'Chart Title',exact:true}).getByLabel('Title',{exact:true}).fill('Retained synthetic title');
  await panel.getByRole('button',{name:'Collapse chart editor'}).click();
  await panel.getByRole('button',{name:'Chart settings',exact:true}).click();
  await expect(panel.getByRole('group',{name:'Chart Title',exact:true}).getByLabel('Title',{exact:true})).toHaveValue('Retained synthetic title');
  await panel.getByRole('tab',{name:'Set Up',exact:true}).click();
  await expect(panel.getByLabel('Category',{exact:true})).toHaveValue('region');
  await expect(panel.getByLabel('Aggregation method')).toHaveValue('average');
  await panel.getByRole('tab',{name:'Customize',exact:true}).click();
  await expect(panel.getByRole('button',{name:'Titles',exact:true})).toHaveAttribute('aria-expanded','false');
  await panel.getByRole('button',{name:'Titles',exact:true}).click();
  await expect(panel.getByRole('switch',{name:'Chart Title',exact:true})).toBeChecked();
  await expect(panel.getByRole('group',{name:'Chart Title',exact:true}).getByLabel('Title',{exact:true})).toHaveValue('Retained synthetic title');
 }
 await page.screenshot({path:dir+'/dock-titles-light-dark.png'});
 expect(errors).toEqual([]); expect(failures).toEqual([]);
 fs.writeFileSync(dir+'/browser-results.json',JSON.stringify({status:'passed',checks:['real dock/setup/titles composition','light/dark','controlled category/method/switch retention through close/reopen and tabs','title enabled/text retention through close/reopen and tabs','Titles transient expansion resets after tab departure'],errors,networkFailures:failures,cdp:['Runtime.enable','Network.enable']},null,2));
} finally {await browser.close();}
