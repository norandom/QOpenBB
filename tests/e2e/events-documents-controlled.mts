import { expect } from '../../verification/node_modules/@playwright/test/index.mjs';
import type { Locator, Page } from '../../verification/node_modules/@playwright/test/index.mjs';
import { plan, query, titles } from './events-documents-browser.mts';
import type { Slot } from './events-documents-browser.mts';

export const fixtureHost = 'events-fixture.invalid';
export const retrievalTime = '2026-11-27T10:00:00Z';

const companySlots: Slot[] = ['filings', 'transcript', 'news'];
export const controlledGroups: Record<string, Slot[]> = {
  'empty-calendar': ['calendar'],
  'restore-calendar': ['calendar'],
  'timeout-news': ['news'],
  'retry-news': ['news'],
  'no-issuer': companySlots,
  'light-away': companySlots,
  'light-back': companySlots,
  'dark-away': companySlots,
  'dark-back': companySlots,
};

export function controlledQuery(stage: string, slot: Slot) {
  if (stage === 'empty-calendar') return { ...plan.edits.calendar, start_date: '2025-07-29' };
  if (stage === 'restore-calendar') return query('reopen', slot);
  return { ...query('reopen', slot), symbol: stage === 'no-issuer' ? 'NONE' : stage.endsWith('-away') ? 'AAPL' : 'MSFT',
    ...(slot === 'news' ? { page: 1 } : {}) };
}

function documentFixtures(slot: Slot, parameters: Record<string, string | number>, stage: string) {
  const symbol = String(parameters.symbol);
  const date = String(parameters.end_date ?? '2026-11-18');
  const literal = '  Synthetic <img src="https://' + fixtureHost + '/embed"> & text\n\n    second line.  ';
  switch (slot) {
    case 'filings': return [
      { symbol, filing_date: date, accepted_date: date + ' 09:10:11.123', report_type: '8-K', cik: '0000000123',
        filing_url: 'https://' + fixtureHost + '/index', report_url: 'https://' + fixtureHost + '/report',
        content_status: 'metadata_only' },
      { symbol, filing_date: date, report_type: '10-Q', filing_url: 'javascript:void(0)',
        report_url: 'https://fixture-user@' + fixtureHost + '/invalid', content_status: 'metadata_only' },
    ];
    case 'transcript': return [
      { symbol, date, event_datetime: date + 'T09:10:11-04:00', year: parameters.year,
        quarter: stage === 'listing' ? 'Q2' : 'Q' + parameters.quarter, content: literal,
        content_status: 'completeness_unknown' },
    ];
    case 'news': return [
      { symbol, date: date + 'T09:10:11Z', title: 'Synthetic article ' + stage, source: 'Fixture site',
        publisher: 'Fixture publisher', excerpt: literal, url: 'https://' + fixtureHost + '/article',
        images: ['https://' + fixtureHost + '/image'], content_status: 'partial' },
      { symbol, date: date + 'T10:10:11Z', title: 'Synthetic headline ' + stage,
        url: 'data:text/plain,fixture', content_status: 'metadata_only' },
    ];
    default: throw new Error('Expected a document slot');
  }
}

export function synthetic(slot: Slot, parameters: Record<string, string | number>, stage: string) {
  if ((slot === 'transcript' && stage === 'launch') || stage === 'empty-calendar' || stage === 'no-issuer') return { status: 204, body: '' };
  if (slot === 'news' && stage === 'listing') return { status: 403, body: JSON.stringify({ detail: 'private_fixture_error' }) };
  if (stage === 'timeout-news' || stage === 'dark-away' && slot === 'news') return { status: 400, body: JSON.stringify({ code: 'timeout', provider: 'fmp', detail: 'private_fixture_error' }) };
  const report_date = String(parameters.end_date);
  const clipped = stage === 'calendar';
  const others = Array.from({ length: clipped ? 247 : 0 }, () => ({ symbol: 'OTHER', report_date }));
  const results = slot === 'calendar' ? [
    { symbol: 'AAPL', report_date, eps_actual: 8 },
    { symbol: 'MSFT', report_date, last_updated: report_date, eps_actual: 0, eps_consensus: null, revenue_actual: '__EXACT_INTEGER__' },
    { symbol: 'MSFT', report_date, eps_actual: 2.75, eps_consensus: 2.125, revenue_actual: 59, revenue_consensus: 55 },
    ...others,
  ] : documentFixtures(slot, parameters, stage);
  const [dataset, endpoint] = plan.slots[slot];
  const limit = slot === 'calendar' ? 250 : parameters.limit ?? null;
  const body = JSON.stringify({ results, extra: { results_metadata: { __qopenbb_financial__: {
    schema_version: 1, provider: 'fmp', dataset, source: { endpoint }, effective_query: parameters,
    retrieved_at: retrievalTime, bounds: { requested_limit: limit, effective_limit: limit,
      returned_count: results.length, truncated: clipped, completeness: clipped ? 'partial' : 'unknown' },
    fields: slot === 'calendar' ? {
      eps_actual: { definition: 'Actual EPS', unit: 'currency_per_share' },
      revenue_actual: { definition: 'Actual revenue', unit: 'currency', scale: 1000 },
    } : {},
  } } } }).replace('"__EXACT_INTEGER__"', '9007199254740993');
  return { status: 200, body };
}

export const conclusion = (story: Locator) => story.getByRole('region', { name: 'Conclusion', exact: true });
export const earnings = (story: Locator) => story.getByRole('region', { name: 'FMP earnings calendar', exact: true });
export const news = (story: Locator) => story.getByRole('region', { name: 'Company news · FMP', exact: true });

export async function outcome(story: Locator, label: string, count: number) {
  await expect(conclusion(story).getByRole('status')).toHaveText(`${label} · ${count} of 4 FMP inputs have usable evidence.`);
}

export async function apply(story: Locator, slot: Slot, label: string, value: string, preserveFocus = false) {
  const group = story.getByRole('group', { name: titles[slot], exact: true });
  const field = group.getByLabel(label, { exact: true });
  const button = group.getByRole('button', { name: /^Apply / });
  if (preserveFocus) {
    const active = await story.page().locator(':focus').elementHandle();
    await field.fill(value);
    await active?.evaluate(element => (element as HTMLElement).focus());
    await button.dispatchEvent('click');
  } else {
    await field.fill(value);
    await button.press('Enter');
  }
  return field;
}

export async function setTheme(page: Page, theme: 'light' | 'dark') {
  const dark = await page.locator('html').evaluate(node => node.classList.contains('dark'));
  if (dark !== (theme === 'dark')) await page.keyboard.press('Control+m');
  await expect(page.locator('html')).toHaveClass(theme === 'dark' ? /\bdark\b/ : /^(?!.*\bdark\b)/);
}

export async function keyboardConclusion(story: Locator) {
  const last = news(story).getByRole('list', { name: 'Company documents' }).getByRole('button').last();
  await last.press('Tab');
  await expect(conclusion(story)).toBeFocused();
}
