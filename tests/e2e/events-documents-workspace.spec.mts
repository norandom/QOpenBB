import { lstatSync, readFileSync, realpathSync, writeFileSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';
import { test, expect } from '../../verification/node_modules/@playwright/test/index.mjs';
import type { BrowserContext, Locator, Page } from '../../verification/node_modules/@playwright/test/index.mjs';
import { leakedPaths, licensedStrings, renameAndSave } from './fmp-batch-b-helpers.mts';
import { arm, connect, downloadTemplate, edit, fields, finalChoices, login, plan, query, restoredChoices } from './events-documents-browser.mts';
import type { Slot } from './events-documents-browser.mts';
import { observeChartCanvas, readCalendarChart } from './events-documents-marks.mts';

const documentTitles = { filings: 'SEC filings', transcript: 'Earnings-call transcript', news: 'Company news' };

function synthetic(slot: Slot, parameters: Record<string, string | number>) {
  const report_date = String(parameters.end_date);
  const results = slot === 'calendar' ? [
    { symbol: 'AAPL', report_date, eps_actual: 8 },
    { symbol: 'MSFT', report_date, eps_actual: 0, eps_consensus: null, revenue_actual: '__EXACT_INTEGER__' },
    { symbol: 'MSFT', report_date, eps_actual: 2.75, eps_consensus: 2.125, revenue_actual: 59, revenue_consensus: 55 },
  ] : [];
  const [dataset, endpoint] = plan.slots[slot];
  const limit = slot === 'calendar' ? 250 : parameters.limit ?? 1;
  return JSON.stringify({ results, extra: { results_metadata: { __qopenbb_financial__: {
    schema_version: 1, provider: 'fmp', dataset, source: { endpoint }, effective_query: parameters,
    retrieved_at: '2026-11-27T10:00:00Z', bounds: { requested_limit: limit, effective_limit: limit,
      returned_count: results.length, truncated: null, completeness: 'unknown' },
    fields: slot === 'calendar' ? {
      eps_actual: { definition: 'Actual EPS', unit: 'currency_per_share' },
      revenue_actual: { definition: 'Actual revenue', unit: 'currency', currency: 'JPY', scale: 1000 },
    } : {},
  } } } }).replace('"__EXACT_INTEGER__"', '9007199254740993');
}

type Acquisition = {
  index: number; stage: string; slot: Slot; query: Record<string, string | number>;
  status?: number; receipt?: number; documentCount?: number; rows?: any[]; done?: boolean;
};

async function calendarProof(story: Locator, acquisition: Acquisition, symbol: string) {
  const region = story.getByRole('region', { name: 'FMP earnings calendar' });
  const articles = region.getByRole('article');
  const expected = acquisition.rows?.filter(row => row.symbol === symbol).length ?? 0;
  await expect(articles).toHaveCount(expected);
  const observed = { index: acquisition.index, symbol, marketCount: 0, clipped: false, retrievedAt: '', rows: [] as object[] };
  if (acquisition.status === 200) {
    observed.marketCount = Number(await region.getByText('Market rows returned', { exact: true }).locator('xpath=following-sibling::dd[1]').textContent());
    observed.clipped = await region.getByText('Clipping observed', { exact: true }).count() === 1;
    observed.retrievedAt = (await region.getByText('Provider retrieval time', { exact: true }).locator('xpath=following-sibling::dd[1]').textContent()) ?? '';
  }
  for (const article of await articles.all()) {
    const title = (await article.getByRole('heading', { level: 3 }).textContent()) ?? '';
    const identity = /^Report date (\d{4}-\d{2}-\d{2}) · market row (\d+)$/.exec(title);
    if (!identity) throw new Error('Invalid market row label');
    const values: Record<string, string> = {};
    const updated = await article.getByText('Last updated', { exact: true }).locator('xpath=following-sibling::dd[1]').textContent();
    const fieldUnits: Record<string, string | null> = {};
    let generation = '';
    for (const [field, label] of Object.entries(fields)) {
      const button = article.getByRole('button', { name: new RegExp('^' + label + ' .*inspect source$') });
      const text = (await button.textContent()) ?? '';
      await button.press('Enter');
      const detail = article.getByRole('region', { name: new RegExp('^' + label + ' source') });
      await expect(detail).toBeFocused();
      for (const [term, value] of Object.entries({
        'Source': 'FMP · earnings-calendar', 'Listing': symbol, 'Report date': identity[1],
        'Source row ordinal': String(Number(identity[2]) - 1), 'Source field': field, 'Exact source value': text,
        'Provider retrieval time': observed.retrievedAt,
        'Effective market window': `${acquisition.query.start_date} to ${acquisition.query.end_date} inclusive`,
      })) {
        if (await detail.getByText(term, { exact: true }).locator('xpath=following-sibling::dd[1]').textContent() !== value)
          throw new Error('Calendar source detail mismatch: ' + term);
      }
      const currentGeneration = await detail.getByText('Receipt generation', { exact: true }).locator('xpath=following-sibling::dd[1]').textContent();
      if (!currentGeneration || (generation && generation !== currentGeneration)) throw new Error('Calendar source generation mismatch');
      generation = currentGeneration;
      const units = await detail.getByText('Units', { exact: true }).locator('xpath=following-sibling::dd[1]').textContent();
      fieldUnits[field] = units;
      if (!units?.startsWith(field.startsWith('eps') ? 'Currency per share' : 'Monetary amount')) throw new Error('Calendar units mismatch');
      await detail.press('Escape');
      await expect(button).toBeFocused();
      values[field] = text;
    }
    const charts = [];
    for (const [measure, label, unit] of [['eps', 'EPS', 'EPS per share'], ['revenue', 'Revenue', 'Revenue (monetary amount)']]) {
      const figure = article.getByRole('figure', { name: unit + ' chart · ' + title, exact: true });
      const hasData = Object.entries(values).some(([field, value]) => field.startsWith(measure) && value !== 'Missing');
      await expect(figure).toHaveCount(hasData ? 1 : 0);
      if (hasData) {
        const display = await story.getByLabel(label + ' chart display').inputValue();
        charts.push(await readCalendarChart(figure, measure, display));
      }
    }
    observed.rows.push({ ordinal: Number(identity[2]) - 1, date: identity[1], fields: values, updated, fieldUnits, generation, charts });
  }
  return observed;
}

async function availableDocument(story: Locator, acquisition: Acquisition) {
  const slot = acquisition.slot as keyof typeof documentTitles;
  const section = story.getByRole('region', { name: documentTitles[slot] + ' · FMP', exact: true });
  const buttons = section.getByRole('list', { name: 'Company documents' }).getByRole('button');
  const rows = acquisition.rows ?? [];
  await expect(buttons).toHaveCount(rows.length);
  acquisition.documentCount = await buttons.count();
  if (!rows.length) return;
  const value = async (locator: Locator, label: string) =>
    locator.getByText(label, { exact: true }).locator('xpath=following-sibling::dd[1]').textContent();
  for (const [index, row] of rows.entries()) {
    const invoker = buttons.nth(index);
    await invoker.press('Enter');
    const detail = section.getByRole('region', { name: 'Document detail' });
    await expect(detail).toBeFocused();
    const expected: Record<string, string> = { Company: row.symbol, Provider: 'FMP', 'Query symbol': String(acquisition.query.symbol) };
    if (slot === 'filings') Object.assign(expected, {
      'Filing date': row.filing_date, Form: row.report_type, CIK: row.cik ?? 'CIK unknown',
      Accepted: row.accepted_date ?? 'Acceptance date unknown',
    });
    if (slot === 'news') Object.assign(expected, {
      Published: row.date, Site: row.source ?? 'Source unknown', Publisher: row.publisher ?? 'Publisher unknown',
    });
    if (slot === 'transcript') {
      Object.assign(expected, { 'Transcript date': row.date, 'Fiscal period': `${row.quarter} ${row.year}` });
      if (row.event_datetime) expected['Event timestamp'] = row.event_datetime;
    }
    for (const [label, expectedValue] of Object.entries(expected)) {
      if (expectedValue && await value(detail, label) !== expectedValue) throw new Error('Document metadata mismatch: ' + slot + '/' + label);
    }
    await expect(detail.getByText(`Source row ${index + 1}`, { exact: true })).toBeVisible();
    const body = slot === 'news' ? row.excerpt : slot === 'transcript' ? row.content : null;
    if (body?.trim() && await detail.getByTestId('document-text').textContent() !== body)
      throw new Error('Document text mismatch: ' + slot);
    const links = slot === 'filings' ? { 'Report document': row.report_url, 'Filing index': row.filing_url }
      : slot === 'news' ? { Article: row.url } : {};
    for (const [title, href] of Object.entries(links)) {
      const link = detail.getByRole('link', { name: title, exact: true });
      if (!href) await expect(link).toHaveCount(0);
      else if (await link.getAttribute('href') !== href) throw new Error('Document link mismatch: ' + slot);
    }
    const headline = slot === 'news' ? `${row.symbol} · ${row.title} · ${row.date}` : null;
    if (headline && await detail.getByRole('heading', { level: 3 }).textContent() !== headline)
      throw new Error('Document headline mismatch');
    await expect(detail.locator('img, iframe, video, audio')).toHaveCount(0);
    await detail.press('Escape');
    await expect(detail).toHaveCount(0);
    await expect(invoker).toBeFocused();
  }
}

test('Events and Documents acquires the frozen listing, edits and fresh reopen', async ({ browser }, info) => {
  const mode = process.env.EVENTS_VERIFICATION_MODE;
  if (mode !== 'controlled' && mode !== 'live') throw new Error('Explicit controlled or live mode required');
  const destination = process.env.WORKSPACE_EVIDENCE_ROOT!;
  const output = lstatSync(destination);
  const child = relative(resolve('artifacts'), destination);
  if (!output.isDirectory() || output.mode % 512 !== 0o700 || realpathSync(destination) !== destination ||
      !/^events-documents-run-[a-z0-9_]+$/.test(child)) throw new Error('Expected private owned run directory');
  const { origin, credentials, phase } = JSON.parse(readFileSync(process.env.WORKSPACE_RUNTIME_PRIVATE!, 'utf8'));
  if (phase !== 'ready' || origin !== process.env.WORKSPACE_FRONTEND_ORIGIN) throw new Error('Expected owned ready session');
  const requests: Acquisition[] = [], calendar: object[] = [], issues: string[] = [];
  const contexts: BrowserContext[] = [];
  let browserRequests = 0;
  let stage = 'disarmed';
  async function advance(next: string) { await arm(next); stage = next; }

  async function contextPage() {
    const context = await browser.newContext({ serviceWorkers: 'block', viewport: { width: 1600, height: 1000 } });
    contexts.push(context);
    await observeChartCanvas(context);
    const page = await context.newPage();
    const cdp = await context.newCDPSession(page);
    await cdp.send('Runtime.enable');
    cdp.on('Runtime.exceptionThrown', () => issues.push('uncaught-browser-exception'));
    await context.route('**/*', async route => {
      const target = new URL(route.request().url());
      if (target.origin !== origin) return route.abort();
      if (!target.pathname.startsWith('/data/api/v1/')) return route.continue();
      browserRequests++;
      const slot = (Object.keys(plan.slots) as Slot[]).find(key => target.pathname === '/data/api/v1/' + plan.slots[key][0]);
      const expected = slot && plan.groups[stage]?.includes(slot) && query(stage, slot);
      const entries = [...target.searchParams].sort();
      const planned = expected && Object.entries({ provider: 'fmp', ...expected }).map(([key, value]) => [key, String(value)]).sort();
      if (!slot || !expected || route.request().method() !== 'GET' || JSON.stringify(entries) !== JSON.stringify(planned)
        || requests.some(entry => entry.stage === stage && entry.slot === slot)) {
        issues.push('unexpected-browser-acquisition');
        return route.abort();
      }
      const entry: Acquisition = { index: requests.length + 1, stage, slot, query: expected };
      requests.push(entry);
      try {
        const controlled = mode === 'controlled' ? synthetic(slot, expected) : null;
        const response = controlled === null ? await route.fetch({ maxRedirects: 0, maxRetries: 0, timeout: 45000 }) : null;
        const body = response ? await response.body() : Buffer.from(controlled!);
        entry.status = response?.status() ?? 200;
        const receipt = response?.headers()['x-qopenbb-events-receipt'];
        if (mode === 'live' && !/^\d+$/.test(receipt ?? '')) issues.push('missing-provider-correlation');
        if (receipt) entry.receipt = Number(receipt);
        writeFileSync(join(destination, entry.index + '.installed'), body, { mode: 0o600, flag: 'wx' });
        // Decode structure and document text only. The oracle owns all financial numeric comparisons.
        if (entry.status === 200) entry.rows = JSON.parse(body.toString('utf8')).results.map((row: any) => slot === 'calendar' ?
          { symbol: row.symbol, hasFigure: Object.keys(fields).some(field => row[field] != null) } : row);
        const headers = response?.headers() ?? { 'content-type': 'application/json' };
        for (const header of ['content-encoding', 'content-length', 'transfer-encoding']) delete headers[header];
        await route.fulfill({ status: entry.status, headers, body });
      } catch {
        issues.push('browser-acquisition-failed');
        await route.abort().catch(() => undefined);
      } finally { entry.done = true; }
    });
    return page;
  }

  let activeCalendar: Acquisition;
  const active = new Map<Slot, Acquisition>();
  async function settled(story: Locator, symbol: string) {
    const current = stage;
    await expect.poll(() => requests.filter(item => item.stage === current && item.done).length).toBe(plan.groups[current].length);
    await expect(story.getByText('Loading FMP earnings calendar.', { exact: true })).toHaveCount(0);
    await expect(story.getByText('Retrieving FMP evidence.', { exact: true })).toHaveCount(0);
    for (const entry of requests.filter(item => item.stage === current)) {
      active.set(entry.slot, entry);
      if (entry.slot === 'calendar') activeCalendar = entry;
      else await availableDocument(story, entry);
    }
    if (current === 'launch' || current === 'listing' || current === 'calendar' || current === 'reopen') {
      const displayed = await calendarProof(story, activeCalendar!, symbol);
      calendar.push(displayed);
      if (mode === 'controlled' && symbol === 'MSFT' &&
          !displayed.rows.some(row => JSON.stringify(row).includes('9007199254740993'))) throw new Error('Exact integer proof missing');
    }
    const usable = [...active.values()].filter(entry => entry.slot === 'calendar'
      ? entry.rows?.some(row => row.symbol === symbol && row.hasFigure) : entry.rows?.length).length;
    await expect(story.getByRole('region', { name: 'Conclusion', exact: true }).getByRole('status'))
      .toContainText(`${usable} of 4 FMP inputs have usable evidence.`);
    await advance('disarmed');
  }

  try {
    const page = await contextPage();
    await login(page, origin, credentials);
    await connect(page, origin);
    const app = page.getByRole('button').filter({ has: page.getByText('Events and Documents', { exact: true }) });
    await expect(app).toHaveCount(1);
    await advance('launch');
    await app.click();
    const story = page.locator('#workarea .widget-events_documents_story');
    await expect(story.getByRole('heading', { name: /What earnings figures does FMP report/ })).toBeVisible();
    await expect(story.getByRole('button', { name: 'Apple (AAPL)', exact: true })).toHaveAttribute('aria-pressed', 'true');
    await settled(story, 'AAPL');

    await advance('listing');
    await story.getByRole('button', { name: 'Microsoft (MSFT)', exact: true }).press('Enter');
    await settled(story, 'MSFT');
    for (const slot of Object.keys(plan.edits) as Slot[]) {
      await advance(slot);
      await edit(story, slot);
      await settled(story, 'MSFT');
    }
    await story.getByLabel('Custom listing symbol').fill('!!');
    await story.getByRole('button', { name: 'Apply symbol', exact: true }).click();
    await expect(story.getByLabel('Custom listing symbol')).toHaveAttribute('aria-invalid', 'true');
    await story.getByLabel('EPS chart display').selectOption('point');
    await story.getByLabel('Revenue chart display').selectOption('bar');
    await restoredChoices(story);
    const id = new URL(page.url()).pathname.split('/').at(-1)!;
    const saved = await renameAndSave(page, id, 'Events verification');
    const storage = saved.data.widgets.find((widget: any) => widget.widgetId === 'events_documents_story').storage;
    expect(storage).toEqual({ eventsDocuments: finalChoices });
    const exported = await downloadTemplate(page, id);
    const layout = Object.values(exported.tabs).flatMap((tab: any) => tab.layout);
    const widget = layout.find((entry: any) => entry.i === 'events_documents_story') as any;
    expect(widget.state).toEqual({ storage: { eventsDocuments: finalChoices } });
    const licensed = licensedStrings(requests.flatMap(entry => entry.slot === 'calendar' ? [] : entry.rows ?? []));
    if (leakedPaths(saved, licensed).length || leakedPaths(exported, licensed).length) throw new Error('Licensed document text persisted');
    await page.context().close();

    await advance('reopen');
    const reopened = await contextPage();
    await login(reopened, origin, credentials);
    if (new URL(reopened.url()).pathname !== '/app/' + id) await reopened.goto(origin + '/app/' + id);
    const fresh = reopened.locator('#workarea .widget-events_documents_story');
    await restoredChoices(fresh);
    await settled(fresh, 'MSFT');
    if (mode === 'live') {
      const chartRow = fresh.getByRole('region', { name: 'FMP earnings calendar' }).getByRole('article').filter({ has: reopened.locator('canvas') }).first();
      if (await chartRow.count()) await chartRow.screenshot({ path: join(destination, 'private-earnings-sample.png') });
    }
    await reopened.locator(`#tab-${id}`).click({ button: 'right' });
    await expect(reopened.getByRole('menuitem', { name: 'Export apps.json', exact: true })).toBeVisible();
    expect(issues).toEqual([]);
  } catch (error) {
    // Browser reports stay private. Publish only the fixed task outcome through the launcher.
    writeFileSync(join(destination, 'browser-failure.txt'), String(error), { mode: 0o600 });
    throw new Error('Events browser journey failed; inspect the private diagnostics');
  } finally {
    await advance('disarmed').catch(() => issues.push('guard-disarm-failed'));
    await Promise.allSettled(contexts.map(context => context.close()));
    writeFileSync(join(destination, 'observations.json'), JSON.stringify({
      mode, browser: browser.version(), browserRequests, calendar, issues,
      requests: requests.map(({ rows: _rows, ...request }) => request),
    }), { mode: 0o600, flag: 'wx' });
  }
});
