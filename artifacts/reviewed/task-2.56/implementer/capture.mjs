import { chromium, expect } from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
const dir='/mnt/d/Source/QOpenBB/artifacts/task-2.56/implementer';
const env={...process.env};delete env.WAYLAND_DISPLAY;
const browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
try {
 const context=await browser.newContext({viewport:{width:900,height:900}});const page=await context.newPage();page.setDefaultTimeout(3000);const errors=[];const failures=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('requestfailed',r=>failures.push(r.url()));
 const cdp=await context.newCDPSession(page);await cdp.send('Runtime.enable');await cdp.send('Network.enable');
 await page.goto('http://127.0.0.1:6017/',{waitUntil:'networkidle'});
 for(const theme of ['light','dark']) {
  const panel=page.locator(`[data-theme="${theme}"]`);
  await panel.getByRole('tab',{name:'Customize',exact:true}).click();
  await expect(panel.getByRole('button',{name:'Series',exact:true})).toHaveAttribute('aria-expanded','false');
  await expect(panel.getByRole('switch',{name:'Tooltips',exact:true})).toHaveCount(0);
  await panel.getByRole('button',{name:'Chart Style',exact:true}).click();
  const padding=panel.getByRole('group',{name:'Padding',exact:true});const background=panel.getByRole('group',{name:'Background',exact:true});
  await expect(background).toBeVisible();
  const order=await panel.locator('fieldset').evaluateAll(nodes=>nodes.map(node=>node.getAttribute('aria-label')));expect(order.indexOf('Background')).toBeGreaterThan(order.indexOf('Padding'));
  await padding.getByLabel('Left value',{exact:true}).fill('67.5');
  const color=background.getByRole('textbox',{name:'Color',exact:true});await color.fill('#12345680');await color.press('Tab');
  await background.getByRole('switch',{name:'Background',exact:true}).click();await expect(color).toHaveCount(0);
  await background.getByRole('switch',{name:'Background',exact:true}).focus();await page.keyboard.press('Space');await expect(color).toHaveValue('#12345680');
  await panel.getByRole('button',{name:'Collapse chart editor'}).click();await panel.getByRole('button',{name:'Chart settings',exact:true}).click();
  await expect(color).toHaveValue('#12345680');await expect(padding.getByLabel('Left value',{exact:true})).toHaveValue('67.5');
 }
 await page.screenshot({path:dir+'/dock-background-light-dark.png'});
 for(const theme of ['light','dark']) {
  const panel=page.locator(`[data-theme="${theme}"]`);await panel.getByRole('button',{name:'Chart Style',exact:true}).click();
  const series=panel.getByRole('button',{name:'Series',exact:true});await series.click();const mode=panel.getByRole('combobox',{name:'Tooltip Mode',exact:true});const toggle=panel.getByRole('switch',{name:'Tooltips',exact:true});
  await expect(mode).toHaveValue('shared');await expect(mode.locator('option')).toHaveText(['Single','Multiple','Compact']);
  for(const value of ['single','shared','compact']){await mode.selectOption(value);await expect(mode).toHaveValue(value);}
  await toggle.click();await expect(mode).toHaveCount(0);await toggle.focus();await page.keyboard.press('Space');await expect(mode).toHaveValue('compact');
  await panel.getByRole('button',{name:'Collapse chart editor'}).click();await panel.getByRole('button',{name:'Chart settings',exact:true}).click();await expect(mode).toHaveValue('compact');
  await panel.getByRole('tab',{name:'Set Up',exact:true}).click();await expect(panel.getByLabel('Category',{exact:true})).toHaveValue('period');
  await panel.getByRole('tab',{name:'Chart',exact:true}).click();await expect(panel.getByRole('button',{name:/Grouped Column/})).toBeVisible();
  await panel.getByRole('tab',{name:'Customize',exact:true}).click();await expect(series).toHaveAttribute('aria-expanded','false');
  await panel.getByRole('button',{name:'Chart Style',exact:true}).click();await expect(panel.getByRole('group',{name:'Background',exact:true}).getByRole('textbox',{name:'Color',exact:true})).toHaveValue('#12345680');await expect(panel.getByLabel('Left value',{exact:true})).toHaveValue('67.5');
  await panel.getByRole('button',{name:'Chart Style',exact:true}).click();await series.click();await expect(mode).toHaveValue('compact');
  await expect(panel.getByRole('button',{name:'Titles',exact:true})).toBeVisible();await expect(panel.getByRole('button',{name:'Legend',exact:true})).toBeVisible();
 }
 await page.screenshot({path:dir+'/dock-tooltips-light-dark.png'});
 expect(errors).toEqual([]);expect(failures).toEqual([]);
 fs.writeFileSync(dir+'/browser-results.json',JSON.stringify({status:'passed',isolated:true,workers:1,checks:['actual combined story in both themes','Background after Padding within Chart Style','Tooltips within initially collapsed Series','exact three mode values','independent alpha background and padding edits','toggle hidden fill/mode retention','dock close/reopen retains values','tab remount retains values and resets Series expansion','Set Up, gallery, Titles, Legend remain available'],errors,networkFailures:failures,cdp:['Runtime.enable','Network.enable']},null,2)+'\n');
}finally{await browser.close();}

