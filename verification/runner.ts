import { chromium } from '@playwright/test';
import type { BrowserContext } from '@playwright/test';
import { join, resolve } from 'node:path';
import { startFixture } from './fixture_server.ts';
import { diagnostics } from './diagnostics.ts';
import { capturePolicy } from './capture.ts';
import { browserEnvironment, runRoot, revision, retain, clearProfile } from './evidence.ts';

export interface RunOptions {
  fail?: boolean; credentialEntry?: boolean; capture?: boolean;
  artifactFailure?: boolean; startupFailure?: boolean;
}

async function observe(context: BrowserContext, url: string, fail: boolean) {
  const page = await context.newPage();
  const diagnostic = await diagnostics(context, page);
  await page.goto(url, { timeout: 10000 });
  const observation = await page.locator('output').innerText();
  await page.evaluate(() => { localStorage.setItem('fixture', 'private'); document.cookie = 'fixture=private'; });
  if (fail) {
    await page.evaluate(async () => {
      console.error('SYNTHETIC_SECRET_DO_NOT_RETAIN', { Authorization: 'Bearer SYNTHETIC_SECRET_DO_NOT_RETAIN' });
      await fetch('/failure?api_key=SYNTHETIC_SECRET_DO_NOT_RETAIN');
    });
    await page.waitForTimeout(100);
  }
  await diagnostic.close();
  return { observation, diagnostics: diagnostic.events };
}

async function checkIsolation(context: BrowserContext, url: string) {
  const page = await context.newPage();
  await page.goto(url);
  return page.evaluate(() => localStorage.length === 0 && document.cookie === '');
}

export async function isolatedRun(options: RunOptions = {}) {
  capturePolicy(options.credentialEntry, options.capture);
  const root = await runRoot();
  const sourceRevision = revision();
  const fixture = await startFixture();
  let browser: Awaited<ReturnType<typeof chromium.launchPersistentContext>> | undefined;
  const record = { status: 'failed', observation: '', isolated: false, cleaned: false, browserClosed: false,
    diagnostics: [] as { kind: string; failed: boolean; status?: number }[],
    revision: sourceRevision, command: 'verification/runner.ts', exit: 1,
    node: process.version, playwright: '1.64.0', browser: '', root,
    scope: 'synthetic infrastructure only', timestamp: new Date().toISOString(), port: fixture.port };
  try {
    if (options.startupFailure) throw new Error('synthetic startup failure');
    browser = await chromium.launchPersistentContext(join(root, 'profile'), {
      headless: true, env: browserEnvironment(), timeout: 20000,
      executablePath: resolve('artifacts/playwright-browsers/chromium-1248/chrome-linux64/chrome'),
    });
    record.browser = browser.browser()!.version();
    const observed = await observe(browser, fixture.url, options.fail ?? false);
    record.observation = observed.observation;
    record.diagnostics = observed.diagnostics;
    const second = await browser.browser()!.newContext();
    try { record.isolated = await checkIsolation(second, fixture.url); }
    finally { await second.close(); }
    record.status = record.diagnostics.length || record.observation !== '123.45 USD' || !record.isolated ? 'failed' : 'passed';
    record.exit = record.status === 'passed' ? 0 : 1;
    if (options.artifactFailure) await retain(join(root, 'missing'), record);
  } catch {
    record.status = 'failed'; record.exit = 1;
  } finally {
    const ownedBrowser = browser?.browser();
    try { await browser?.close(); record.browserClosed = !ownedBrowser?.isConnected(); }
    finally { await fixture.close(); await clearProfile(root); record.cleaned = true; }
    await retain(root, record);
  }
  return record;
}

if (process.argv[1]?.endsWith('/runner.ts')) {
  isolatedRun({ fail: process.argv.includes('--failure') }).then(result => {
    console.log(JSON.stringify({ status: result.status, root: result.root }));
    process.exitCode = result.exit;
  }).catch(() => { console.error('verification startup failed'); process.exitCode = 1; });
}
