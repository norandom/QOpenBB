import { lstatSync, readFileSync, realpathSync, writeFileSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';
import { test, expect } from '../../verification/node_modules/@playwright/test/index.mjs';
import type { BrowserContext, Locator, Page } from '../../verification/node_modules/@playwright/test/index.mjs';
import { leakedPaths, licensedStrings, renameAndSave } from './fmp-batch-b-helpers.mts';
import { arm, connect, downloadTemplate, edit, fields, finalChoices, fourInputs, login, plan, query, restoredChoices, supplemental, symbols } from './events-documents-browser.mts';
import type { Slot } from './events-documents-browser.mts';
import { controlledDiagnostics } from './events-documents-diagnostics.mts';
import { observeChartCanvas, readCalendarChart } from './events-documents-marks.mts';

import { apply, conclusion, controlledGroups, controlledQuery, earnings, fixtureHost,
  keyboardConclusion, news, outcome, retrievalTime, setTheme, synthetic } from './events-documents-controlled.mts';

const replayListings = ['0151.HK', 'GMGMF'];
const documentTitles = { filings: 'SEC filings', transcript: 'Earnings-call transcript', news: 'Company news' };

type Acquisition = {
  index: number; stage: string; slot: Slot; query: Record<string, string | number>;
  status?: number; receipt?: number; retrievedAt?: string; documentCount?: number; rows?: any[]; done?: boolean; cancelled?: boolean;
};

async function calendarProof(story: Locator, acquisition: Acquisition, symbol: string) {
  const region = story.getByRole('region', { name: 'FMP earnings calendar' });
  const articles = region.getByRole('article');
  const expected = acquisition.rows?.filter(row => row.symbol === symbol).length ?? 0;
  await expect(articles).toHaveCount(expected);
  const observed = { index: acquisition.index, symbol, marketCount: 0, clipped: false, retrievedAt: '', rows: [] as object[] };
  if (process.env.EVENTS_VERIFICATION_MODE === 'live') {
    const value = (label: string) =>
      region.getByText(label, { exact: true }).locator('xpath=following-sibling::dd[1]');
    await expect(value('Listing filter')).toHaveText(symbol);
    await expect(value('Effective market window')).toHaveText(`${acquisition.query.start_date} to ${acquisition.query.end_date} inclusive`);
    const condition = acquisition.status === 204 || (acquisition.status === 200 && !acquisition.rows?.length)
      ? 'Empty market calendar for this window.' : acquisition.status !== 200 ? null
      : expected === 0 ? `No returned market rows match ${symbol}.`
      : acquisition.rows?.some(row => row.symbol === symbol && row.hasFigure)
        ? 'Current FMP earnings calendar.' : 'Matching rows have no reported figures.';
    if (condition) await expect(region.getByRole('status')).toHaveText(condition);
  }
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
  const controlled = process.env.EVENTS_VERIFICATION_MODE === 'controlled';
  const invalid = controlled && acquisition.stage === 'listing' && slot === 'transcript';
  const rows = invalid ? [] : acquisition.rows ?? [];
  await expect(buttons).toHaveCount(rows.length);
  acquisition.documentCount = await buttons.count();
  const value = async (locator: Locator, label: string) =>
    locator.getByText(label, { exact: true }).locator('xpath=following-sibling::dd[1]').textContent();
  if (!controlled && acquisition.status === 204) {
    const label = slot === 'transcript' ? `Transcript for Q${acquisition.query.quarter} ${acquisition.query.year} is unavailable.`
      : 'FMP returned no items for this query.';
    await expect(section.getByRole('status')).toHaveText(label);
  }
  if (!controlled && acquisition.status !== undefined && acquisition.status >= 400) {
    await expect(section.getByRole('alert')).toContainText(`HTTP ${acquisition.status}.`);
    await expect(section.getByText('Provider retrieval time unavailable.', { exact: true })).toBeVisible();
  }
  if (!rows.length) return;
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
    {
      const { year, quarter, page, limit, start_date, end_date } = acquisition.query;
      const scope = { Freshness: 'Current result', 'Retrieval time': controlled ? retrievalTime : acquisition.retrievedAt,
        'Source query': '/data/api/v1/' + plan.slots[slot][0] };
      Object.assign(scope, slot === 'transcript' ? { 'Selected period': `Q${quarter} ${year}` } : {
        Pagination: `Page ${page}, limit ${limit}`,
        'Date bounds': start_date ? `${start_date} through ${end_date} (inclusive)` : 'No date filter',
      });
      for (const [label, expectedValue] of Object.entries(scope))
        await expect.poll(() => value(detail, label)).toBe(expectedValue);
      const content = slot === 'transcript' ? 'Completeness unknown' : body ?
        'Partial excerpt; full article is not supplied inline.' : 'Metadata only; document text is not supplied inline.';
      await expect(detail.getByText(content, { exact: true })).toBeVisible();
      if (body) await expect(detail.getByTestId('document-text')).toHaveCSS('white-space', 'pre-wrap');
      else await expect(detail.getByTestId('document-text')).toHaveCount(0);
    }
    const links = slot === 'filings' ? { 'Report document': row.report_url, 'Filing index': row.filing_url }
      : slot === 'news' ? { Article: row.url } : {};
    for (const [title, href] of Object.entries(links)) {
      const link = detail.getByRole('link', { name: title, exact: true });
      if (!href || controlled && index === 1) await expect(link).toHaveCount(0);
      else {
        await expect(link).toHaveAttribute('href', href);
        if (controlled) {
          await expect(link).toHaveAttribute('rel', 'noopener noreferrer');
          await expect(link).toHaveAttribute('target', '_blank');
        }
      }
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

test('Events and Documents acquires the frozen listing, edits and fresh reopen', async ({ browser }) => {
  const mode = process.env.EVENTS_VERIFICATION_MODE;
  if (mode !== 'controlled' && mode !== 'live') throw new Error('Explicit controlled or live mode required');
  const destination = process.env.WORKSPACE_EVIDENCE_ROOT!;
  const output = lstatSync(destination);
  const child = relative(resolve('artifacts'), destination);
  if (!output.isDirectory() || output.mode % 512 !== 0o700 || realpathSync(destination) !== destination ||
      !/^events-documents-run-[a-z0-9_]+$/.test(child)) throw new Error('Expected private owned run directory');
  const { origin, credentials, phase } = JSON.parse(readFileSync(process.env.WORKSPACE_RUNTIME_PRIVATE!, 'utf8'));
  if (phase !== 'ready' || origin !== process.env.WORKSPACE_FRONTEND_ORIGIN) throw new Error('Expected owned ready session');
  const replay = process.env.EVENTS_REPLAY_CALENDAR === '1';
  const seedPreflight = process.env.EVENTS_SEED_PREFLIGHT === '1';
  if (replay && mode !== 'controlled') throw new Error('Replay requires the offline provider guard');
  const requests: Acquisition[] = [], calendar: object[] = [], issues: string[] = [];
  const contexts: BrowserContext[] = [];
  let browserRequests = 0;
  let seedAborts = 0;
  let stage = 'disarmed';
  const seedLaunchSlots = new Set<Slot>();
  const groups = mode === 'controlled' ? { ...plan.groups, ...controlledGroups } : plan.groups;
  if (replay) for (const symbol of replayListings) groups['replay-' + symbol] = plan.groups.listing;
  const scenarios: string[] = [];
  const conclusions: Record<string, number> = {};
  const release = new Map<string, () => void>();
  const held = new Map<string, Promise<void>>();
  const diagnostics = controlledDiagnostics(origin, fixtureHost, mode === 'live');
  const network = diagnostics.result;
  const liveChecks: { passed: string[]; failed: string[] } = { passed: [], failed: [] };
  async function verify(label: string, assertion: () => Promise<void>) {
    if (mode === 'controlled' && !replay) return assertion();
    try {
      await assertion();
      liveChecks.passed.push(label);
    } catch (error) {
      liveChecks.failed.push(label);
      writeFileSync(join(destination, 'failure-' + label.replaceAll('/', '-') + '.txt'),
        String(error), { mode: 0o600, flag: 'wx' });
    }
  }
  async function advance(next: string) {
    if (!Object.hasOwn(controlledGroups, next) && !next.startsWith('replay-')) await arm(next);
    stage = next;
  }

  async function contextPage(seeding = false, verifySeedLaunch = false) {
    const context = await browser.newContext({ serviceWorkers: 'block', viewport: { width: 1600, height: 1000 } });
    contexts.push(context);
    await observeChartCanvas(context);
    const page = await context.newPage();
    const cdp = await context.newCDPSession(page);
    await cdp.send('Runtime.enable');
    if (mode === 'live' && !seeding) {
      await cdp.send('Network.enable');
      cdp.on('Network.loadingFailed', event => {
        if (!event.canceled && !event.blockedReason) diagnostics.recordTransportFailure();
      });
    }
    cdp.on('Runtime.exceptionThrown', () => issues.push('uncaught-browser-exception'));
    if (!seeding) diagnostics.observe(page);
    await context.route('**/*', async route => {
      const target = new URL(route.request().url());
      if (target.origin !== origin) {
        diagnostics?.blockExternal(target);
        return route.abort();
      }
      if (!target.pathname.startsWith('/data/api/v1/')) return route.continue();
      if (seeding) {
        seedAborts++;
        if (verifySeedLaunch) {
          const slot = (Object.keys(plan.slots) as Slot[]).find(key => target.pathname === '/data/api/v1/' + plan.slots[key][0]);
          const actual = [...target.searchParams].sort();
          const expected = slot && Object.entries({ provider: 'fmp', ...query('launch', slot) })
            .map(([key, value]) => [key, String(value)]).sort();
          if (!slot || seedLaunchSlots.has(slot) || route.request().method() !== 'GET'
            || JSON.stringify(actual) !== JSON.stringify(expected)) issues.push('invalid-saved-seed-launch');
          else seedLaunchSlots.add(slot);
        }
        return route.abort();
      }
      browserRequests++;
      const slot = (Object.keys(plan.slots) as Slot[]).find(key => target.pathname === '/data/api/v1/' + plan.slots[key][0]);
      let expected = slot && groups[stage]?.includes(slot) &&
        (Object.hasOwn(controlledGroups, stage) ? controlledQuery(stage, slot) : query(stage, slot));
      if (expected && replay && stage.startsWith('replay-')) expected = { ...expected, symbol: stage.slice(7) };
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
        const controlled = mode === 'controlled' ? synthetic(slot, expected, entry.stage) : null;
        const response = controlled === null ? await route.fetch({ maxRedirects: 0, maxRetries: 0, timeout: 45000 }) : null;
        const replayLaunch = replay && entry.stage === 'launch' && entry.slot === 'calendar';
        const replayDocument = replay && entry.slot !== 'calendar';
        const body = replayLaunch ? readFileSync(join(destination, 'replay-calendar.installed'))
          : replayDocument ? Buffer.alloc(0) : response ? await response.body() : Buffer.from(controlled!.body);
        entry.status = replayLaunch ? 200 : replayDocument ? 204 : response?.status() ?? controlled!.status;
        const receipt = response?.headers()['x-qopenbb-events-receipt'];
        if (mode === 'live' && !/^\d+$/.test(receipt ?? '')) issues.push('missing-provider-correlation');
        if (receipt) entry.receipt = Number(receipt);
        writeFileSync(join(destination, entry.index + '.installed'), body, { mode: 0o600, flag: 'wx' });
        // Decode structure and document text only. The oracle owns all financial numeric comparisons.
        if (entry.status === 200) {
          const decoded = JSON.parse(body.toString('utf8'));
          entry.retrievedAt = decoded.extra?.results_metadata?.__qopenbb_financial__?.retrieved_at;
          entry.rows = decoded.results.map((row: any) => slot === 'calendar' ?
            { symbol: row.symbol, hasFigure: Object.keys(fields).some(field => row[field] != null) } : row);
        }
        const headers = response?.headers() ?? { 'content-type': 'application/json' };
        for (const header of ['content-encoding', 'content-length', 'transfer-encoding']) delete headers[header];
        diagnostics?.register(route.request(), entry, entry.status);
        await held.get(entry.stage);
        await route.fulfill({ status: entry.status, headers, body });
      } catch {
        if (mode === 'controlled' && entry.stage.endsWith('-away')) entry.cancelled = true;
        else issues.push('browser-acquisition-failed');
        await route.abort().catch(() => undefined);
      } finally { entry.done = true; }
    });
    return page;
  }

  let activeCalendar: Acquisition;
  const active = new Map<Slot, Acquisition>();
  async function settled(story: Locator, symbol: string) {
    const current = stage;
    await expect.poll(() => requests.filter(item => item.stage === current && item.done).length).toBe(groups[current].length);
    await expect(story.getByText('Loading FMP earnings calendar.', { exact: true })).toHaveCount(0);
    await expect(story.getByText('Retrieving FMP evidence.', { exact: true })).toHaveCount(0);
    await advance('disarmed');
    for (const entry of requests.filter(item => item.stage === current)) {
      active.set(entry.slot, entry);
      if (entry.slot === 'calendar') activeCalendar = entry;
      else await verify(current + '/' + entry.slot, () => availableDocument(story, entry));
    }
    if (['launch', 'listing', 'calendar', 'reopen', 'restore-calendar'].includes(current)) {
      await verify(current + '/calendar', async () => {
        const displayed = await calendarProof(story, activeCalendar!, symbol);
        calendar.push(displayed);
        if (mode === 'controlled' && symbol === 'MSFT' &&
            !displayed.rows.some(row => JSON.stringify(row).includes('9007199254740993'))) throw new Error('Exact integer proof missing');
      });
    }
    const usable = [...active.values()].filter(entry => entry.slot === 'calendar'
      ? entry.rows?.some(row => row.symbol === symbol && row.hasFigure) : entry.documentCount).length;
    await verify(current + '/conclusion', async () => {
      const status = story.getByRole('region', { name: 'Conclusion', exact: true }).getByRole('status');
      await expect(status).toContainText(`${usable} of 4 FMP inputs have usable evidence.`);
      const title = usable === 4 ? 'Evidence available' : usable === 0 ? 'Insufficient evidence' : 'Partial evidence';
      await expect(status).toContainText(title);
      conclusions[current] = usable;
    });
  }

  async function controlledRecovery(page: Page, story: Locator) {
    const section = earnings(story);
    const invoker = section.getByRole('button', { name: /^Actual EPS 0 .*inspect source$/ });
    await invoker.press('Enter');
    const detail = section.getByRole('region', { name: /^Actual EPS source/ });
    await expect(detail).toBeFocused();
    await advance('empty-calendar');
    await apply(story, 'calendar', 'Start date', '2025-07-29', true);
    await settled(story, 'MSFT');
    await expect(detail).toHaveCount(0);
    await expect(section.getByRole('heading', { name: 'FMP earnings calendar' })).toBeFocused();
    await expect(section.getByText('Empty market calendar for this window.', { exact: true })).toBeVisible();
    await expect(section.getByRole('article')).toHaveCount(0);
    await outcome(story, 'Partial evidence', 3);
    scenarios.push('empty-market-calendar', 'disappearing-calendar-invoker');

    await advance('restore-calendar');
    await apply(story, 'calendar', 'Start date', '2025-07-30');
    await settled(story, 'MSFT');
    const stable = conclusion(story).getByRole('heading', { name: /^(Earnings calendar|SEC filings|Earnings-call transcript) · FMP$/ })
      .locator('xpath=..');
    const untouched = await stable.allTextContents();
    const invalid = await apply(story, 'news', 'Limit', '51');
    await expect(invalid).toHaveAttribute('aria-invalid', 'true');
    expect(await stable.allTextContents()).toEqual(untouched);
    await invalid.fill('10');
    scenarios.push('invalid-bounds-no-request');

    await advance('timeout-news');
    await apply(story, 'news', 'Page', '1');
    await settled(story, 'MSFT');
    await expect(news(story).getByRole('alert')).toHaveText('FMP request timeout. HTTP 400.');
    await outcome(story, 'Partial evidence', 3);
    expect(await stable.allTextContents()).toEqual(untouched);
    await advance('retry-news');
    await news(story).getByRole('button', { name: 'Retry Company news' }).press('Enter');
    await settled(story, 'MSFT');
    await expect(news(story).getByText(/Synthetic article retry-news/)).toBeVisible();
    await outcome(story, 'Evidence available', 4);
    expect(await stable.allTextContents()).toEqual(untouched);
    scenarios.push('typed-timeout-same-query-retry', 'stable-neighbors');

    for (const theme of ['light', 'dark'] as const) {
      await setTheme(page, theme);
      await supersede(story, theme);
      calendar.push(await calendarProof(story, activeCalendar, 'MSFT'));
      await keyboardConclusion(story);
      scenarios.push(theme + '-keyboard-focus-and-supersession');
    }

    held.set('no-issuer', new Promise<void>(resolve => release.set('no-issuer', resolve)));
    await advance('no-issuer');
    await story.getByLabel('Custom listing symbol').fill('NONE');
    await story.getByRole('button', { name: 'Apply symbol', exact: true }).press('Enter');
    await expect.poll(() => requests.filter(item => item.stage === 'no-issuer').length).toBe(3);
    await expect(section.getByText('No returned market rows match NONE.', { exact: true })).toBeVisible();
    await expect(section.getByText('Wider market coverage unknown', { exact: true })).toBeVisible();
    await outcome(story, 'Pending', 0);
    release.get('no-issuer')!();
    await settled(story, 'NONE');
    await outcome(story, 'Insufficient evidence', 0);
    scenarios.push('empty-issuer-filter', 'pending-and-insufficient-conclusions');

  }

  async function supersede(story: Locator, theme: 'light' | 'dark') {
    const subsection = news(story);
    const invoker = subsection.getByRole('list', { name: 'Company documents' }).getByRole('button').first();
    const detail = subsection.getByRole('region', { name: 'Document detail' });
    await invoker.press('Enter');
    await expect(detail).toBeFocused();
    await detail.press('Escape');
    await expect(invoker).toBeFocused();
    await invoker.press('Enter');
    await expect(detail).toBeFocused();

    const away = theme + '-away';
    held.set(away, new Promise<void>(resolve => release.set(away, resolve)));
    await advance(away);
    await story.getByRole('button', { name: 'Apple (AAPL)', exact: true }).dispatchEvent('click');
    await expect.poll(() => requests.filter(item => item.stage === away).length).toBe(3);
    await expect(subsection.getByRole('heading', { name: 'Company news · FMP' })).toBeFocused();
    await expect(detail).toHaveCount(0);
    await expect(subsection.getByRole('list', { name: 'Company documents' })).toHaveCount(0);
    await expect(subsection.getByText('Retrieving FMP evidence.', { exact: true })).toBeVisible();
    await outcome(story, 'Partial evidence', 1);
    await advance(theme + '-back');
    await story.getByRole('button', { name: 'Microsoft (MSFT)', exact: true }).press('Enter');
    await settled(story, 'MSFT');
    await outcome(story, 'Evidence available', 4);
    release.get(away)!();
    await expect.poll(() => requests.filter(item => item.stage === away && item.done).length).toBe(3);
    await expect(subsection.getByText(new RegExp('Synthetic article ' + theme + '-back'))).toBeVisible();
    await expect(subsection.getByText(new RegExp('Synthetic article ' + away))).toHaveCount(0);
    await expect(subsection.getByRole('alert')).toHaveCount(0);
    await outcome(story, 'Evidence available', 4);
  }

  const storyWidget = (page: Page) => page.locator('#workarea .widget-events_documents_story');
  const appButton = (page: Page) => page.getByRole('button').filter({
    has: page.getByText('Events and Documents', { exact: true }),
  });
  async function applySymbol(story: Locator, symbol: string) {
    await story.getByLabel('Custom listing symbol').fill(symbol);
    await story.getByRole('button', { name: 'Apply symbol', exact: true }).press('Enter');
  }
  async function prepareSupplement() {
    const seed = await contextPage(true);
    await login(seed, origin, credentials);
    await connect(seed, origin);
    const app = appButton(seed);
    await expect(app).toHaveCount(1);
    await app.click();
    const story = storyWidget(seed);
    await applySymbol(story, symbols.launch);
    for (const slot of Object.keys(plan.initial) as Slot[]) await edit(story, slot, plan.initial);
    const choices = { ...finalChoices, ...plan.initial, symbol: symbols.launch, charts: { eps: 'bar', revenue: 'point' } };
    await restoredChoices(story, choices);
    const id = new URL(seed.url()).pathname.split('/').at(-1)!;
    const saved = await renameAndSave(seed, id, 'Events verification seed');
    expect(saved.data.widgets.find((widget: any) => widget.widgetId === 'events_documents_story').storage)
      .toEqual({ eventsDocuments: choices });
    await seed.context().close();
    scenarios.push('native-catalog-seeded-through-workspace-controls');
    return { id, choices };
  }

  try {
    const start = supplemental ? await prepareSupplement() : undefined;
    if (seedPreflight && start) {
      const checked = await contextPage(true, true);
      await login(checked, origin, credentials);
      if (new URL(checked.url()).pathname !== '/app/' + start.id) await checked.goto(origin + '/app/' + start.id);
      await restoredChoices(storyWidget(checked), start.choices);
      await expect.poll(() => seedLaunchSlots.size).toBe(4);
      expect(issues).toEqual([]);
      scenarios.push('seed-restored-planned-native-queries-without-sends');
      return;
    }
    const page = await contextPage();
    if (start) await advance('launch');
    await login(page, origin, credentials);
    if (start) {
      if (new URL(page.url()).pathname !== '/app/' + start.id) await page.goto(origin + '/app/' + start.id);
      await restoredChoices(storyWidget(page), start.choices);
    } else {
      await connect(page, origin);
      const app = appButton(page);
      await expect(app).toHaveCount(1);
      await advance('launch');
      await app.click();
      await expect(storyWidget(page).getByRole('button', { name: 'Apple (AAPL)', exact: true })).toHaveAttribute('aria-pressed', 'true');
    }
    const story = storyWidget(page);
    await expect(story.getByRole('heading', { name: /What earnings figures does FMP report/ })).toBeVisible();
    if (replay) {
      const connectionToast = page.locator('[data-sonner-toast]').filter({ hasText: 'Backend added successfully' });
      if (await connectionToast.isVisible()) await connectionToast.getByRole('button', { name: 'Close toast' }).click();
      await expect(connectionToast).toBeHidden();
      await settled(story, 'AAPL');
      for (const symbol of replayListings) {
        await advance('replay-' + symbol);
        await story.getByLabel('Custom listing symbol').fill(symbol);
        await story.getByRole('button', { name: 'Apply symbol', exact: true }).press('Enter');
        await settled(story, symbol);
        await story.getByLabel('EPS chart display').selectOption('bar');
        await story.getByLabel('Revenue chart display').selectOption('bar');
        await verify(symbol + '/bar', async () => {
          const bars = await calendarProof(story, activeCalendar!, symbol);
          expect(bars.rows.length).toBeGreaterThan(0);
          calendar.push(bars);
        });
        await story.getByLabel('EPS chart display').selectOption('point');
        await story.getByLabel('Revenue chart display').selectOption('point');
        if (symbol === replayListings[0]) {
          const chartRow = earnings(story).getByRole('article').first();
          await expect(chartRow.locator('canvas')).toHaveCount(2);
          await chartRow.screenshot({ path: join(destination, 'private-replayed-earnings-sample.png') });
        }
        await verify(symbol + '/point', async () => {
          calendar.push(await calendarProof(story, activeCalendar!, symbol));
        });
      }
      expect(issues).toEqual([]);
      expect(network.errors).toEqual({});
      expect(liveChecks.failed).toEqual([]);
      return;
    }
    await settled(story, symbols.launch);
    if (fourInputs) {
      const chartRow = earnings(story).getByRole('article').filter({ has: page.locator('canvas') }).first();
      if (await chartRow.count()) await chartRow.screenshot({ path: join(destination, 'private-earnings-sample.png') });
      await outcome(story, 'Evidence available', 4);
      expect(issues).toEqual([]);
      expect(network.errors).toEqual({});
      expect(liveChecks.failed).toEqual([]);
      return;
    }
    if (mode === 'controlled') {
      await expect(story.getByText('Transcript for Q1 2025 is unavailable.', { exact: true })).toBeVisible();
      await outcome(story, 'Partial evidence', 3);
      scenarios.push('empty-transcript', 'partial-conclusion');
    }

    await advance('listing');
    if (supplemental) await applySymbol(story, symbols.later);
    else await story.getByRole('button', { name: 'Microsoft (MSFT)', exact: true }).press('Enter');
    await settled(story, symbols.later);
    if (mode === 'controlled') {
      await expect(story.getByText('FMP evidence failed validation for this query. HTTP 200.', { exact: true })).toBeVisible();
      await expect(news(story).getByRole('alert')).toHaveText('Workspace access to this source or session is unavailable. HTTP 403.');
      await expect(news(story).getByRole('button', { name: 'Retry Company news' })).toHaveCount(0);
      await outcome(story, 'Partial evidence', 2);
      scenarios.push('denied-input', 'mismatched-transcript');
    }
    for (const slot of Object.keys(plan.edits) as Slot[]) {
      await advance(slot);
      await edit(story, slot);
      await settled(story, symbols.later);
    }
    if (mode === 'controlled') {
      await expect(earnings(story).getByText('Clipping observed', { exact: true })).toBeVisible();
      await expect(earnings(story).getByText('250 rows', { exact: true })).toBeVisible();
      await expect(earnings(story).getByRole('article')).toHaveCount(2);
      await outcome(story, 'Evidence available', 4);
      scenarios.push('clipped-calendar', 'duplicate-report-dates', 'zero-and-missing-marks', 'literal-and-safe-document-details');
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
    if (mode === 'live') scenarios.push('save-and-export-choices');
    await page.context().close();
    await advance('reopen');
    const reopened = await contextPage();
    await login(reopened, origin, credentials);
    if (new URL(reopened.url()).pathname !== '/app/' + id) await reopened.goto(origin + '/app/' + id);
    const fresh = reopened.locator('#workarea .widget-events_documents_story');
    await restoredChoices(fresh);
    if (mode === 'live') scenarios.push('fresh-authenticated-reopen-choices');
    await settled(fresh, symbols.later);
    if (mode === 'live') {
      const chartRow = fresh.getByRole('region', { name: 'FMP earnings calendar' }).getByRole('article').filter({ has: reopened.locator('canvas') }).first();
      if (await chartRow.count()) await chartRow.screenshot({ path: join(destination, 'private-earnings-sample.png') });
    }
    await reopened.locator(`#tab-${id}`).click({ button: 'right' });
    await expect(reopened.getByRole('menuitem', { name: 'Export apps.json', exact: true })).toBeVisible();
    if (mode === 'controlled') {
      await reopened.keyboard.press('Escape');
      scenarios.push('save-fresh-authenticated-reopen-safe-export');
      await controlledRecovery(reopened, fresh);
      await expect.poll(() => network!.abortedData).toBe(6);
      expect(network!.fixtureExternal).toBe(0);
      expect(network!.httpErrors).toEqual({ 'listing/news/403': 1, 'timeout-news/news/400': 1 });
      expect(network!.errors).toEqual({});
      await expect(fresh.getByText('private_fixture_error', { exact: false })).toHaveCount(0);
    }
    expect(issues).toEqual([]);
    expect(liveChecks.failed).toEqual([]);
    if (mode === 'live') expect(network.errors).toEqual({});
  } catch (error) {
    // Browser reports stay private. Publish only the fixed task outcome through the launcher.
    writeFileSync(join(destination, 'browser-failure.txt'), String(error), { mode: 0o600 });
    throw new Error('Events browser journey failed; inspect the private diagnostics');
  } finally {
    for (const unblock of release.values()) unblock();
    await advance('disarmed').catch(() => issues.push('guard-disarm-failed'));
    await Promise.allSettled(contexts.map(context => context.close()));
    writeFileSync(join(destination, 'observations.json'), JSON.stringify({
      mode, replay, browser: browser.version(), browserRequests, seedAborts, calendar, issues, scenarios, network, liveChecks, conclusions,
      requests: requests.map(({ rows: _rows, ...request }) => request),
    }), { mode: 0o600, flag: 'wx' });
  }
});
