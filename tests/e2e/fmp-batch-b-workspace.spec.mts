import { readFileSync, writeFileSync }  from 'node:fs';
import { randomUUID } from 'node:crypto';
import type { Page } from 'playwright-core';
import { test, expect, loginDisposableWorkspace } from '../../vendor/workspace/terminalpro/tests/e2e/live-chart/fixtures.ts';
import { observeApplication } from '../../vendor/workspace/terminalpro/tests/e2e/live-chart/diagnostics.ts';
import { readRuntimeDescriptor } from '../../verification/runtime-descriptor.ts';
import { control, renameAndSave, cell, numberMatches, documentProof, licensedStrings, leakedPaths } from './fmp-batch-b-helpers.mts';

const root = new URL('../../', import.meta.url);
const catalog = JSON.parse(readFileSync(new URL('contracts/widgets.json', root), 'utf8'));
const gallery = JSON.parse(readFileSync(new URL('contracts/gallery/catalog.json', root), 'utf8')).widgets;
const matrix = JSON.parse(readFileSync(process.env.QOPENBB_BATCH_B_MATRIX!, 'utf8'));
const offlineReceipts = process.env.QOPENBB_BATCH_B_OFFLINE_RECEIPTS ? JSON.parse(readFileSync(process.env.QOPENBB_BATCH_B_OFFLINE_RECEIPTS, 'utf8')).receipts : null;
const cases = matrix.browser.filter((c: any) => c.id.endsWith('-initial'));

test('Batch B five actual widgets save export and isolated reopen', async ({ page, browser }, info) => {
  const progress = (stage: string) => writeFileSync(info.outputPath('progress.json'), JSON.stringify({ stage, at: new Date().toISOString() }));
  page.setDefaultTimeout(60000);
  progress('runtime');
  const runtime = await readRuntimeDescriptor(process.env.WORKSPACE_RUNTIME_PRIVATE!);
  const initial = await control();
  expect(initial.fmp_count).toBeGreaterThanOrEqual(0);
  // Negative control: the leak scan must find a multiline, quoted body after a JSON round trip,
  // which a search of serialized text cannot do.
  const probe = 'First line of a long licensed body\nSecond line with "quoted" words';
  expect(JSON.stringify({ note: probe }).includes(probe)).toBe(false);
  expect(leakedPaths(JSON.parse(JSON.stringify({ data: { note: `saved ${probe}` } })), licensedStrings([{ content: probe }]))).toEqual(['$.data.note']);
  const diagnostics: any[] = [], requests: any[] = [], receipts: any[] = [], observations: any[] = [], stored: any[] = [];
  const reads: Promise<void>[] = [], missingReceipts: string[] = [];
  // The app does not reliably issue validate-and-sync after login; address the native endpoint directly.
  const syncUrl = `${runtime.origin}/api/pro/dash/validate-and-sync`;
  let authorization = '', phase = 'setup';
  const watch = async (target: Page) => {
    diagnostics.push(await observeApplication(target));
    target.on('request', request => {
      const url = new URL(request.url());
      if (url.pathname.startsWith('/data/api/v1/')) requests.push({ phase, path: url.pathname, query: Object.fromEntries(url.searchParams) });
    });
    target.on('response', response => {
      const url = new URL(response.url());
      if (!url.pathname.startsWith('/data/api/v1/')) return;
      const pending = response.json().then(payload => { receipts.push({ phase, path: url.pathname, status: response.status(), payload }); });
      reads.push(pending); void pending.catch(() => undefined);
    });
    if (offlineReceipts) await target.route('**/data/api/v1/**', async route => {
      const pathname = new URL(route.request().url()).pathname;
      const receipt = offlineReceipts.find((entry: any) => entry.path === pathname && entry.status === 200);
      // Abort rather than continue: an unarmed request reaching the guarded API is a recorded denial.
      if (!receipt) { missingReceipts.push(pathname); return route.abort(); }
      await route.fulfill({ status: 200, json: receipt.payload });
    });
    // Real widget discovery; suppress starter application fanout only.
    await target.route('**/data/apps.json', route => route.fulfill({ json: [] }));
  };
  const loginWithNativeBearer = async (target: Page) => {
    const pending = target.waitForResponse(response => {
      const url = new URL(response.url());
      return url.origin === runtime.origin && url.pathname === '/api/pro/login' &&
        response.request().method() === 'POST' && response.status() === 200;
    });
    await loginDisposableWorkspace(target);
    const token: unknown = (await (await pending).json()).access_token;
    if (typeof token !== 'string' || !token || /[\r\n\s]/.test(token))
      throw Error('Successful native login must provide a usable bearer token');
    authorization = `Bearer ${token}`;
  };
  const headers = (): Record<string, string> => {
    if (!authorization) throw Error('Authenticated native login required before protected control API access');
    return { authorization };
  };
  const serverRead = async (target: Page, id: string) => {
    const response = await target.request.get(syncUrl, { headers: headers(), maxRedirects: 0 });
    expect(response.status()).toBe(200); return (await response.json()).owned[id].content;
  };
  await watch(page);
  try {
    await page.waitForTimeout(65000);
    progress('login'); await loginWithNativeBearer(page); progress('connect backend');
    await page.goto('/app/connections');
    await page.getByRole('button', { name: 'Connect Backend', exact: true }).first().click();
    const dialog = page.getByRole('dialog').filter({ has: page.getByRole('heading', { name: 'Connect backend', exact: true }) });
    await dialog.getByPlaceholder('OpenBB App').fill('Batch B reviewed candidate');
    await dialog.getByPlaceholder('http://127.0.0.1:5056').fill(`${runtime.origin}/data`);
    let sourceId = "";
    const testBackend = dialog.getByRole("button", { name: "Test", exact: true });
    const duplicate = dialog.getByText('"Batch B reviewed candidate" is already using this URL', { exact: true });
    await expect.poll(async () => (await testBackend.isEnabled()) || (await duplicate.isVisible())).toBe(true);
    if (await duplicate.isVisible()) {
      const discovered = await page.request.get(`${runtime.origin}/data/widgets.json`);
      expect(discovered.status()).toBe(200); expect(await discovered.json()).toEqual({ ...catalog, ...gallery });
      const listed = await page.request.get(syncUrl.replace(/dash\/validate-and-sync$/, "data-connectors/api-source"), { headers: headers(), maxRedirects: 0 });
      expect(listed.status()).toBe(200);
      const sources = (await listed.json()).filter((source: any) => source.name === "Batch B reviewed candidate" && source.url === `${runtime.origin}/data`);
      expect(sources).toHaveLength(1); sourceId = sources[0].id;
      await dialog.getByRole("button", { name: "Close", exact: true }).click();
    } else {
      const discovered = page.waitForResponse(r => new URL(r.url()).pathname === "/data/widgets.json");
      await testBackend.click(); expect(await (await discovered).json()).toEqual({ ...catalog, ...gallery });
      await expect(dialog.getByText("Test successful", { exact: true })).toBeVisible();
      const posted = page.waitForRequest(r => r.method() === "POST" && new URL(r.url()).pathname.includes("/pro/data-connectors/api-source/"));
      await dialog.getByRole("button", { name: /^add$/i }).click();
      sourceId = new URL((await posted).url()).pathname.split("/").at(-1)!;
    }
    await expect(dialog).not.toBeVisible();
    const existing = await page.request.get(syncUrl, { headers: headers(), maxRedirects: 0 });
    expect(existing.status()).toBe(200);
    const knownIds = new Set(Object.keys((await existing.json()).owned));
    await page.locator('#tabs').getByRole('button').first().click();
    await page.getByRole('button', { name: /New Dashboard/ }).click();
    // The route briefly keeps the previously visited dashboard; wait for an id the server did not own.
    const createdId = () => new URL(page.url()).pathname.split('/').at(-1)!;
    await expect.poll(() => /^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(createdId()) && !knownIds.has(createdId())).toBe(true);
    const blankId = createdId();
    await expect(page.locator(`#tab-${blankId}`)).toBeVisible();
    await expect(page.getByRole('main').getByRole('button', { name: 'Add widgets', exact: true })).toBeVisible();
    progress('save blank');
    const blank = await renameAndSave(page, blankId, 'Batch B empty landing');
    expect(blank.data.widgets).toHaveLength(0); expect(syncUrl).toBeTruthy();
    const items: Record<string, any> = {};
    for (const call of cases) {
      const definition = structuredClone(catalog[call.widget_id]);
      const params = { provider: 'fmp', ...call.params };
      const id = randomUUID(), instance = randomUUID();
      const widget = { ...definition, id: instance, widgetId: call.widget_id, innerTab: '', groupId: '',
        external: true, sourceId, sourceName: 'Batch B reviewed candidate', connectionType: 'advanced-backend',
        endpointHeaders: [], endpoint: { url: `${runtime.origin}/data${definition.endpoint}`, method: 'GET' },
        refetchInterval: false, storage: { params },
        params: definition.params.map((p: any) => ({ ...p, label: p.label ?? p.paramName, type: p.type ?? 'text', options: p.options ?? [] })) };
      const content = structuredClone(blank); content.index = id;
      content.data = { ...content.data, name: `Batch B ${definition.name}`, type: 'custom', widgets: [widget], groups: [],
        gridLayout: { '': [{ i: instance, x: 0, y: 0, w: 40, h: 24 }] }, currentTab: '' };
      items[id] = content; stored.push({ id, instance, call, params });
    }
    const treeResponse = await page.request.get(syncUrl, { headers: headers(), maxRedirects: 0 });
    expect(treeResponse.status()).toBe(200);
    const owned: Record<string, { content: any }> = (await treeResponse.json()).owned;
    const roots = Object.entries(owned).filter(([, entry]) => entry.content?.isRoot === true);
    expect(roots).toHaveLength(1);
    const [rootId, rootEntry] = roots[0];
    const rootContent = structuredClone(rootEntry.content);
    expect(rootContent.index).toBe(rootId); expect(rootContent.children).toContain(blankId);
    for (const item of stored) {
      expect(owned).not.toHaveProperty(item.id);
      items[item.id].parentId = rootId;
    }
    // Native normalization retains only items reachable from the owned root tree.
    items[rootId] = { ...rootContent, children: [...rootContent.children, ...stored.map(item => item.id)] };
    progress('import dashboards');
    const imported = await page.request.post(syncUrl.replace(/validate-and-sync$/, 'sync'), { headers: headers(), data: { items }, maxRedirects: 0 });
    expect(imported.ok()).toBe(true);
    for (const item of stored) expect((await serverRead(page, item.id)).parentId).toBe(rootId);
    const visit = async (target: Page, item: any, pass: 'initial' | 'save-reopen') => {
      phase = pass; progress(`${item.call.model}-${pass}`);
      const definition = catalog[item.call.widget_id], pathname = `/data${definition.endpoint}`;
      const before = await control(offlineReceipts ? 'proof' : 'arm', `${item.call.model}-${pass}`);
      const acquired = target.waitForResponse(r => new URL(r.url()).pathname === pathname, { timeout: 180000 });
      await target.goto(`/app/${item.id}`);
      const response = await acquired;
      expect(response.status(), 'Provider denial blocks acceptance; no automatic rerun').toBe(200);
      const payload = await response.json(), metadata = payload.extra.results_metadata.__qopenbb_financial__;
      expect(payload.results.length).toBeGreaterThan(0);
      expect(metadata.provider).toBe('fmp'); expect(metadata.effective_query).toMatchObject(item.call.params);
      expect(metadata.dataset).toBe(definition.endpoint.replace('/api/v1/', ''));
      expect(Number.isFinite(Date.parse(metadata.retrieved_at))).toBe(true);
      const widget = target.locator(`#workarea .widget-${item.call.widget_id}`);
      await expect(widget).toBeVisible(); const row = payload.results[0];
      const displayed: Record<string, string> = {};
      if (definition.type === 'company_documents') {
        displayed.document = await documentProof(widget, row, item.call.model);
        for (const parameter of definition.params.filter((p: any) => p.show !== false && p.paramName !== 'provider')) {
          const input = widget.getByLabel(parameter.label ?? parameter.paramName, { exact: true });
          await expect(input).toHaveValue(String(item.params[parameter.paramName] ?? parameter.value ?? ''));
          await input.focus(); await expect(input).toBeFocused();
          displayed[`control:${parameter.paramName}`] = await input.inputValue();
        }
        // Editing a query choice must not acquire until the explicit Apply query submission.
        const symbol = widget.getByLabel('Symbol', { exact: true });
        const original = await symbol.inputValue(), issued = requests.length;
        await symbol.fill('MSFT'); await expect(symbol).toHaveValue('MSFT');
        await target.waitForTimeout(1500); expect(requests).toHaveLength(issued);
        await symbol.fill(original); await expect(symbol).toHaveValue(original);
      }
      else {
        if (row.symbol) { await expect(await cell(widget, 'symbol')).toHaveText(row.symbol); displayed.symbol = row.symbol; }
        // Amount and adjusted amount stay distinct; yield is a fraction displayed in percent.
        const fields = item.call.model === 'HistoricalDividends' ? ['amount', 'adjusted_amount', 'dividend_yield'] : ['eps_actual', 'eps_consensus'];
        for (const field of fields) {
          const shown = await cell(widget, field);
          if (row[field] == null) expect((await shown.innerText()).trim()).not.toMatch(/^0(?:\.0+)?$/);
          else await expect.poll(async () => numberMatches(await shown.innerText(), row[field])).toBe(true);
          displayed[field] = (await shown.innerText()).trim();
        }
        const dateFields = item.call.model === 'HistoricalDividends' ? ['ex_dividend_date', 'declaration_date', 'record_date', 'payment_date'] : ['report_date'];
        for (const field of dateFields) {
          const text = (await (await cell(widget, field)).innerText()).trim();
          if (row[field] == null) expect(text).toMatch(/^-?$/);
          else expect(text).toBe(row[field]);
          displayed[field] = text;
        }
        writeFileSync(info.outputPath(`${pass}-${item.call.model}.aria.yml`), await widget.ariaSnapshot());
        // Header query controls show the saved choices; the market-wide calendar has no company control.
        const shortDate = (iso: string) => new Date(`${iso}T12:00:00`).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        if (item.call.model === 'HistoricalDividends') {
          const symbolControl = widget.getByRole('textbox', { name: 'Symbol', exact: true });
          await expect(symbolControl).toHaveValue(item.params.symbol);
          await expect(widget.getByRole('spinbutton', { name: 'Limit', exact: true })).toHaveValue(String(item.params.limit));
          await expect(widget.getByRole('button', { name: 'Pick a date', exact: true })).toHaveCount(2);
          await symbolControl.focus(); await expect(symbolControl).toBeFocused();
          displayed['control:symbol'] = await symbolControl.inputValue();
        } else {
          await expect(widget.getByRole('textbox', { name: 'Symbol', exact: true })).toHaveCount(0);
          await expect(widget.getByRole('combobox', { name: 'Symbol', exact: true })).toHaveCount(0);
          for (const key of ['start_date', 'end_date']) {
            const control = widget.getByRole('button', { name: shortDate(item.params[key]), exact: true });
            await expect(control).toBeVisible(); displayed[`control:${key}`] = shortDate(item.params[key]);
          }
        }
      }
      if (pass === 'initial') {
        item.savedName = `Batch B verified ${definition.name}`;
        await renameAndSave(target, item.id, item.savedName);
        await target.locator(`#tab-${item.id}`).click({ button: 'right' });
        await target.getByRole('menuitem', { name: 'Export apps.json', exact: true }).click();
        const exportDialog = target.getByRole('dialog').filter({ has: target.getByRole('heading', { name: 'Export App', exact: true }) });
        await exportDialog.getByPlaceholder('Enter app name...').fill(item.savedName);
        await exportDialog.getByPlaceholder('Describe what this app does and when to use it...').fill('Bounded saved query choices');
        const downloading = target.waitForEvent('download');
        await exportDialog.getByRole('button', { name: 'Download App', exact: true }).click();
        const download = await downloading; expect(await download.failure()).toBeNull();
        const destination = info.outputPath(`${item.call.model}-safe-template.json`); await download.saveAs(destination);
        const exported = readFileSync(destination, 'utf8');
        expect(leakedPaths(JSON.parse(exported), licensedStrings(payload.results)), 'Export must not carry response text').toEqual([]);
        const template = JSON.parse(exported);
        const layouts: any[] = Object.values(template.tabs).flatMap((tab: any) => tab.layout);
        const exportedWidget = layouts.find((entry: any) => entry.i === item.call.widget_id);
        expect(exportedWidget).toBeTruthy();
        if (definition.type === 'company_documents') expect(exportedWidget.state).toEqual({ params: item.params });
      }
      const saved = await serverRead(target, item.id);
      expect(saved.data.name).toBe(item.savedName);
      expect(saved.data.widgets[0]).toMatchObject({ widgetId: item.call.widget_id, refetchInterval: false, storage: { params: item.params } });
      expect(saved.data.widgets[0].storage).toEqual({ params: item.params });
      expect(leakedPaths(saved, licensedStrings(payload.results)), 'Saved dashboard must not carry response text').toEqual([]);
      const after = await control(); expect(after.fmp_count).toBe(before.fmp_count + (offlineReceipts ? 0 : 1));
      observations.push({ pass, model: item.call.model, row, displayed, metadata, before, after });
      await widget.screenshot({ path: info.outputPath(`${pass}-${item.call.model}.png`) });
    };
    for (const item of stored) await visit(page, item, 'initial');
    // Zero-send failure and recovery: the browser itself fulfils the typed API error envelope and then
    // the body this run already received, so no request reaches the guarded API in either mode.
    await Promise.all(reads); phase = 'failure-recovery';
    const failureCases = [
      { model: 'CompanyNews', code: 'timeout', status: 400, retryable: true, detail: 'Provider request timed out. Try again later.' },
      { model: 'HistoricalDividends', code: 'entitlement', status: 502, retryable: false, detail: 'Provider subscription access is required.' },
    ];
    for (const failure of failureCases) {
      const item = stored.find(entry => entry.call.model === failure.model);
      const definition = catalog[item.call.widget_id], pathname = `/data${definition.endpoint}`;
      const recovered = receipts.find(entry => entry.phase === 'initial' && entry.path === pathname && entry.status === 200).payload;
      let failing = true, fulfilled = 0;
      const matcher = (url: URL) => url.pathname === pathname;
      const handler = (route: any) => { fulfilled++; return failing
        ? route.fulfill({ status: failure.status, json: { detail: failure.detail, code: failure.code, provider: 'fmp', retryable: failure.retryable } })
        : route.fulfill({ status: 200, json: recovered }); };
      const before = await control(); progress(`${failure.model}-failure-recovery`);
      await page.route(matcher, handler);
      try {
        await page.goto(`/app/${item.id}`);
        const widget = page.locator(`#workarea .widget-${item.call.widget_id}`);
        if (definition.type === 'company_documents') {
          await expect(widget.getByRole('alert')).toHaveText('Document acquisition failed. Retry to recover.');
          await expect(widget.getByRole('list', { name: 'Company documents' })).toHaveCount(0);
          failing = false; await widget.getByRole('button', { name: 'Refresh documents', exact: true }).click();
          await expect(widget.getByRole('alert')).toHaveCount(0);
          await expect(widget.getByRole('list', { name: 'Company documents' }).getByRole('button').first()).toBeVisible();
        } else {
          await expect(widget.getByText(failure.detail, { exact: true })).toBeVisible();
          await page.waitForTimeout(1500); expect(fulfilled).toBe(1); // one attempt; no automatic retry
          failing = false; await page.reload();
          await expect.poll(async () => numberMatches(await (await cell(widget, 'amount')).innerText(), recovered.results[0].amount)).toBe(true);
        }
        await widget.screenshot({ path: info.outputPath(`failure-recovery-${failure.model}.png`) });
      } finally { await page.unroute(matcher, handler); }
      const after = await control(); expect(after.fmp_count).toBe(before.fmp_count);
      expect(fulfilled).toBeGreaterThanOrEqual(2);
      observations.push({ pass: 'failure-recovery', model: failure.model, injected: { status: failure.status, code: failure.code }, fulfilled, before, after });
    }
    const landing = `/app/${blankId}`;
    const parked = requests.length;
    await page.goto(landing);
    await expect(page).toHaveURL(`${runtime.origin}${landing}`);
    await expect(page.getByRole('main').getByRole('button', { name: 'Add widgets', exact: true })).toBeVisible();
    // The app does not reliably post lastVisitedPage on navigation; persist only that field natively.
    const userUrl = `${runtime.origin}/api/pro/user`;
    const userBefore = await page.request.get(userUrl, { headers: headers(), maxRedirects: 0 });
    expect(userBefore.status()).toBe(200);
    const nextSettings = { ...(await userBefore.json()).pro_display_settings, lastVisitedPage: landing };
    const settingsSaved = await page.request.post(`${runtime.origin}/api/pro/display-settings`, { headers: headers(), data: nextSettings, maxRedirects: 0 });
    expect(settingsSaved.status()).toBe(200);
    const userAfter = await page.request.get(userUrl, { headers: headers(), maxRedirects: 0 });
    expect((await userAfter.json()).pro_display_settings).toEqual(nextSettings);
    expect((await serverRead(page, blankId)).data.widgets).toHaveLength(0); expect(requests).toHaveLength(parked);
    await page.close();
    await new Promise(resolve => setTimeout(resolve, 65000));
    const context = await browser.newContext({ baseURL: runtime.origin, serviceWorkers: 'block', viewport: { width: 1600, height: 1000 } });
    try {
      const reopened = await context.newPage(); await watch(reopened); await loginWithNativeBearer(reopened);
      await expect(reopened).toHaveURL(`${runtime.origin}${landing}`); expect(requests).toHaveLength(parked);
      for (const item of stored) await visit(reopened, item, 'save-reopen');
    } finally { await context.close(); }
    await Promise.all(reads);
    const final = await control(); expect(final).toMatchObject({ api_container: initial.api_container, fmp_count: initial.fmp_count + (offlineReceipts ? 0 : 10), cumulative_fmp_count: initial.cumulative_fmp_count + (offlineReceipts ? 0 : 10) });
    const acquisitions = requests.filter(request => request.phase !== 'failure-recovery');
    expect(acquisitions).toHaveLength(10);
    for (const [index, request] of acquisitions.entries()) {
      const item = stored[index % 5];
      expect(request.path).toBe(`/data${catalog[item.call.widget_id].endpoint}`);
      expect(request.query).toEqual(Object.fromEntries(Object.entries(item.params).map(([key, value]) => [key, String(value)])));
    }
    const injectedPaths = failureCases.map(failure => `/data${catalog[stored.find(entry => entry.call.model === failure.model).call.widget_id].endpoint}`);
    expect(requests.filter(request => request.phase === 'failure-recovery').every(request => injectedPaths.includes(request.path))).toBe(true);
    expect(missingReceipts).toEqual([]);
    // Only the deliberately injected typed errors may appear in the browser diagnostics.
    // Exact {path, status} pairs are excused on the first page only; the reopened context has none.
    const expectedFailures = failureCases.map((failure, index) => ({ path: injectedPaths[index], status: failure.status }));
    const byPath = (a: any, b: any) => a.path.localeCompare(b.path);
    for (const [index, diagnostic] of diagnostics.entries()) {
      expect(diagnostic.errors).toEqual([]); expect(diagnostic.requestFailures).toEqual([]);
      const allowed = index === 0 ? expectedFailures : [];
      expect([...diagnostic.failures].sort(byPath)).toEqual([...allowed].sort(byPath));
      expect(diagnostic.consoleErrors.filter((entry: any) => !(allowed.some(pair => pair.path === entry.path)
        && new RegExp(`Failed to load resource.*${allowed.find(pair => pair.path === entry.path)!.status}`).test(entry.message)))).toEqual([]);
    }
  } finally {
    await control('disarm'); await Promise.allSettled(reads);
    const record = { mode: offlineReceipts ? 'offline-rehearsal' : 'live', initial, requests, receipts, observations, diagnostics,
      limitations: ['Authenticated dashboard import used; app-template reimport not covered.',
        'Superseded-response races are covered by mounted Workspace tests, not by this browser journey.',
        'HistoricalSplits, CalendarDividend and CalendarSplits have API acceptance only; no browser sample.'] };
    writeFileSync(info.outputPath('private-receipts.json'), JSON.stringify(record));
    await info.attach('batch-b-private-receipts', { contentType: 'application/json', body: JSON.stringify(record) });
  }
});
