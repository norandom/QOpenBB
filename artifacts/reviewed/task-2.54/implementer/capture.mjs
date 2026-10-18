import { chromium, expect } from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
const dir='/mnt/d/Source/QOpenBB/artifacts/task-2.54/implementer';
const env={...process.env};delete env.WAYLAND_DISPLAY;
const browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
try {
 const context=await browser.newContext({viewport:{width:700,height:600}});
 const page=await context.newPage();const errors=[];const networkFailures=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('requestfailed',r=>networkFailures.push(r.url()));
 const cdp=await context.newCDPSession(page);await cdp.send('Runtime.enable');await cdp.send('Network.enable');
 await page.goto('http://127.0.0.1:6026/',{waitUntil:'networkidle',timeout:20000});
 await page.screenshot({path:dir+'/background-light-dark.png',fullPage:true});
 for(const theme of ['light','dark']) {
  const scope=page.locator(`[data-theme="${theme}"]`);const output=scope.locator('output');
  const toggle=scope.getByRole('switch',{name:'Background'});const input=scope.getByRole('textbox',{name:'Color',exact:true});
  await expect(output).toHaveText('null');await expect(input).toHaveCSS('height','32px');
  await input.fill('rgba(10, 20, 30, 0.35)');await expect(output).toHaveText('{"field":"fill","value":"rgba(10, 20, 30, 0.35)"}');
  for(const draft of ['', 'oops','#12']) {await input.fill(draft);await expect(input).toHaveAttribute('aria-invalid','true');await expect(output).toHaveText('{"field":"fill","value":"rgba(10, 20, 30, 0.35)"}');}
  await input.fill('#12345678');await toggle.click();await expect(input).toHaveCount(0);await expect(output).toHaveText('{"field":"visible","value":false}');
  await toggle.focus();await page.keyboard.press('Space');await expect(input).toHaveValue('#12345678');
  const opener=scope.getByRole('button',{name:'Choose color'});await opener.click();const picker=scope.getByLabel('Picker color');await expect(picker).toHaveValue('#12345678');
  await picker.fill('rgba(50, 60, 70, 0.2)');await expect(input).toHaveValue('rgba(50, 60, 70, 0.2)');
  await picker.press('Escape');await expect(opener).toBeFocused();await opener.press('Enter');await expect(picker).toBeVisible();await picker.press('Enter');await expect(opener).toBeFocused();
 }
 fs.writeFileSync(dir+'/browser-results.json',JSON.stringify({isolated:true,workers:1,cdp:['Runtime','Network'],checks:['light/dark real subsection','no mount edits','raw alpha edits','invalid drafts recover','pointer toggle and keyboard restore retain fill','picker keyboard open/close and focus'],errors,networkFailures},null,2));
 if(errors.length||networkFailures.length)throw Error('Browser diagnostics failed');await context.close();
} finally {await browser.close();}
