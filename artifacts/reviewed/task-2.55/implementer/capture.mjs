import { chromium, expect } from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
const dir='/mnt/d/Source/QOpenBB/artifacts/task-2.55/implementer';
const env={...process.env};delete env.WAYLAND_DISPLAY;
const browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
try {
 const context=await browser.newContext({viewport:{width:700,height:400}});const page=await context.newPage();const errors=[];const networkFailures=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('requestfailed',r=>networkFailures.push(r.url()));
 const cdp=await context.newCDPSession(page);await cdp.send('Runtime.enable');await cdp.send('Network.enable');
 await page.goto('http://127.0.0.1:6024/',{waitUntil:'networkidle',timeout:20000});
 await page.screenshot({path:dir+'/tooltips-light-dark.png',fullPage:true});
 for(const theme of ['light','dark']) {
  const panel=page.locator(`[data-theme="${theme}"]`);const mode=panel.getByRole('combobox',{name:'Tooltip Mode'});const toggle=panel.getByRole('switch',{name:'Tooltips'});
  await expect(panel.locator('output')).toHaveText('null');await expect(mode).toHaveValue('shared');await expect(mode).toHaveCSS('height','32px');
  await expect(mode.locator('option')).toHaveText(['Single','Multiple','Compact']);
  await mode.focus();await page.keyboard.press('Home');await expect(mode).toHaveValue('single');await expect(panel.locator('output')).toHaveText('{"field":"mode","value":"single"}');
  await page.keyboard.press('End');await expect(mode).toHaveValue('compact');await expect(panel.locator('output')).toHaveText('{"field":"mode","value":"compact"}');
  await toggle.click();await expect(mode).toHaveCount(0);await expect(panel.locator('output')).toHaveText('{"field":"enabled","value":false}');
  await toggle.focus();await page.keyboard.press('Space');await expect(mode).toHaveValue('compact');await expect(panel.locator('output')).toHaveText('{"field":"enabled","value":true}');
  await page.keyboard.press('Tab');await expect(mode).toBeFocused();
  await mode.selectOption('shared');await expect(panel.locator('output')).toHaveText('{"field":"mode","value":"shared"}');
 }
 fs.writeFileSync(dir+'/browser-results.json',JSON.stringify({isolated:true,workers:1,cdp:['Runtime','Network'],checks:['light/dark real subsection','no mount edits','exact mappings','native keyboard Home/End mode edits','pointer toggle hides mode','Space restores retained mode','Tab focus','pointer mode selection'],errors,networkFailures},null,2));
 if(errors.length||networkFailures.length)throw Error('Browser diagnostics failed');await context.close();
} finally {await browser.close();}
