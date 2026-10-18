import { chromium, expect } from '/mnt/d/Source/QOpenBB/verification/node_modules/@playwright/test/index.mjs';
import fs from 'node:fs';
const dir='/mnt/d/Source/QOpenBB/artifacts/task-2.52/implementer';
const env={...process.env};delete env.WAYLAND_DISPLAY;
const browser=await chromium.launch({headless:true,env,args:['--ozone-platform=headless','--use-gl=angle','--use-angle=swiftshader-webgl','--enable-unsafe-swiftshader']});
try {
 const context=await browser.newContext({viewport:{width:700,height:600}});
 const page=await context.newPage();const errors=[];const networkFailures=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});page.on('requestfailed',r=>networkFailures.push(r.url()));
 const cdp=await context.newCDPSession(page);await cdp.send('Runtime.enable');await cdp.send('Network.enable');
 await page.goto('http://127.0.0.1:6022/',{waitUntil:'networkidle',timeout:20000});
 await page.screenshot({path:dir+'/padding-light-dark.png',fullPage:true});
 const dark=page.locator('[data-theme="dark"]');const top=dark.getByRole('slider',{name:'Top',exact:true});const number=dark.getByLabel('Top value');
 await expect(dark.locator('output')).toHaveText('null');
 await expect(number).toHaveCSS('height','32px');
 await number.fill('250.25');await expect(dark.locator('output')).toHaveText('{"side":"top","value":250.25}');await expect(top).toHaveAttribute('max','250.25');
 await dark.getByLabel('Right value').fill('22.5');await expect(number).toHaveValue('250.25');await expect(dark.getByLabel('Right value')).toHaveValue('22.5');
 for(const draft of ['', '-1','NaN','Infinity','oops']) {await number.fill(draft);await expect(number).toHaveAttribute('aria-invalid','true');await expect(dark.locator('output')).toHaveText('{"side":"right","value":22.5}');}
 await number.fill('30');await expect(top).toHaveValue('30');await top.focus();await page.keyboard.press('ArrowRight');await expect(number).toHaveValue('31');
 const left=dark.getByRole('slider',{name:'Left',exact:true});await left.click({position:{x:80,y:8}});await expect(dark.locator('output')).toContainText('"side":"left"');
 await page.keyboard.press('Tab');await expect(dark.getByLabel('Left value')).toBeFocused();
 await expect(page.locator('[data-theme="light"]').getByLabel('Top value')).toHaveValue('20');
 fs.writeFileSync(dir+'/browser-results.json',JSON.stringify({isolated:true,workers:1,cdp:['Runtime','Network'],checks:['light/dark real subsection','no mount edits','independent side edits','decimal above maximum expands slider','invalid drafts emit nothing and recover','range pointer and keyboard','Tab focus','light state isolated'],errors,networkFailures},null,2));
 if(errors.length||networkFailures.length)throw Error('Browser diagnostics failed');await context.close();
} finally {await browser.close();}
