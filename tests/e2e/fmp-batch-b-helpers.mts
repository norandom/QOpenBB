import { writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { execFile } from 'node:child_process';
import { expect } from '../../vendor/workspace/terminalpro/tests/e2e/live-chart/fixtures.ts';
import type { Page, Locator } from 'playwright-core';

export async function control(action = 'proof', caseId?: string) {
  const argv: string[] = JSON.parse(process.env.QOPENBB_BROWSER_CONTROL_CMD!);
  const controlEnvironment = JSON.parse(process.env.QOPENBB_BROWSER_CONTROL_ENV ?? '{}');
  const nativeDirectories = Object.fromEntries(['HOME', 'USERPROFILE', 'APPDATA', 'LOCALAPPDATA', 'XDG_CONFIG_HOME'].filter(key => typeof controlEnvironment[key] === 'string').map(key => [key, controlEnvironment[key]]));
  const extra = ['--action', action, ...(caseId ? ['--case-id', caseId, '--reason', 'Planned five-widget initial/save-reopen verification'] : [])];
  const output = await new Promise<string>((resolve, reject) => execFile(argv[0], [...argv.slice(1), ...extra],
    { windowsHide: true, timeout: 180000, maxBuffer: 1048576, encoding: 'utf8',
      env: { ...process.env, ...nativeDirectories } },
    (error, stdout, stderr) => { if (error) { writeFileSync(join(process.env.WORKSPACE_EVIDENCE_ROOT!, `control-${action}-${Date.now()}.log`), String(error) + '\n' + stderr); reject(Error('Guarded browser control failed; private diagnostic retained')); } else resolve(stdout); }));
  return JSON.parse(output);
}

export async function renameAndSave(page: Page, id: string, name: string) {
  const posted = page.waitForResponse(r => r.request().method() === 'POST' &&
    new URL(r.url()).pathname.endsWith('/pro/dash/sync') && r.request().postDataJSON()?.items?.[id]?.data?.name === name, { timeout: 60000 });
  await page.locator(`#tab-${id}`).click({ button: 'right' });
  await page.getByRole('menuitem', { name: 'Rename', exact: true }).click();
  const dialog = page.getByRole('dialog').filter({ has: page.getByRole('heading', { name: 'Rename dashboard', exact: true }) });
  await dialog.getByRole('textbox').fill(name); await dialog.getByRole('textbox').press('Enter');
  await page.keyboard.press('Control+Shift+S');
  const response = await posted; expect(response.ok()).toBe(true);
  return response.request().postDataJSON().items[id];
}

export async function cell(widget: Locator, field: string) {
  const target = widget.locator(`.ag-row[row-index="0"] [col-id="${field}"]`).first();
  for (let index = 0; index < 35 && !(await target.count()); index++) {
    await widget.locator('.ag-body-horizontal-scroll-viewport').evaluate((el, x) => { el.scrollLeft = x; }, index * 450);
    await widget.page().waitForTimeout(40);
  }
  await expect(target).toBeVisible(); await target.scrollIntoViewIfNeeded();
  return target;
}

export function numberMatches(text: string, expected: number) {
  const match = /^(-?\d+(?:\.(\d+))?)([KMBT])?(%)?$/.exec(text.replace(/[,\s$]/g, '').toUpperCase());
  if (!match) return false;
  const scale = ({ K: 1e3, M: 1e6, B: 1e9, T: 1e12 } as Record<string, number>)[match[3]] ?? 1;
  const divisor = match[4] ? 100 : 1;
  const quantum = scale / divisor * 10 ** -(match[2]?.length ?? 0);
  return Math.abs(Number(match[1]) * scale / divisor - expected) <= quantum / 2 + Math.abs(expected) * Number.EPSILON;
}

// Response strings long enough to identify licensed or provider text; dates/timestamps excluded.
export function licensedStrings(rows: any[]) {
  const found = new Set<string>();
  const walk = (value: unknown) => {
    if (typeof value === 'string') { if (value.trim().length > 15 && !/^\d{4}-\d{2}-\d{2}/.test(value)) found.add(value.trim()); }
    else if (Array.isArray(value)) value.forEach(walk);
    else if (value && typeof value === 'object') Object.values(value).forEach(walk);
  };
  walk(rows);
  return [...found];
}

// Search parsed string values, never serialized JSON text: serialization escapes newlines and
// quotes, so a multiline transcript body could never match its raw form in a JSON string.
// A leading 120-character fragment also catches truncated copies of long bodies.
export function leakedPaths(document: unknown, strings: string[]) {
  const needles = strings.flatMap(text => text.length > 120 ? [text, text.slice(0, 120)] : [text]);
  const hits: string[] = [];
  const walk = (value: unknown, path: string) => {
    if (typeof value === 'string') { if (needles.some(needle => value.includes(needle))) hits.push(path); }
    else if (Array.isArray(value)) value.forEach((item, index) => walk(item, `${path}[${index}]`));
    else if (value && typeof value === 'object') for (const [key, item] of Object.entries(value)) walk(item, `${path}.${key}`);
  };
  walk(document, '$');
  return hits;
}

export async function documentProof(widget: Locator, row: any, model: string) {
  const selector = widget.getByRole('list', { name: 'Company documents' }).getByRole('button').first();
  await expect(selector).toBeVisible(); const label = (await selector.innerText()).trim();
  await selector.focus(); await selector.press('Enter');
  const detail = widget.getByRole('region', { name: 'Document detail' });
  await expect(detail).toBeVisible(); await expect(detail).toBeFocused();
  await expect(detail.locator('dd').filter({ hasText: /^fmp$/i })).toHaveCount(1);
  for (const value of [row.symbol || row.symbols, row.source, row.publisher, row.event_datetime || row.filing_date || row.date]) {
    if (value) await expect(detail).toContainText(value);
  }
  const body = model === 'CompanyNews' ? row.excerpt : model === 'EarningsCallTranscript' ? row.content : null;
  if (body?.trim()) expect(await detail.getByTestId('document-text').textContent()).toBe(body);
  if (model === 'CompanyNews') {
    await expect(detail).toContainText(row.excerpt?.trim() ? 'Partial excerpt' : 'Metadata only');
    if (row.url) await expect(detail.getByRole('link', { name: 'Article', exact: true })).toHaveAttribute('href', row.url);
  }
  if (model === 'EarningsCallTranscript') {
    await expect(detail).toContainText(`Q${String(row.quarter).replace(/^Q/, '')} ${row.year}`);
    await expect(detail).toContainText('Completeness unknown');
  }
  if (model === 'CompanyFilings') {
    await expect(detail).toContainText('Metadata only'); await expect(detail.getByTestId('document-text')).toHaveCount(0);
    for (const field of ['filing_date', 'accepted_date', 'cik', 'report_type']) if (row[field]) await expect(detail).toContainText(row[field]);
    if (row.filing_url) await expect(detail.getByRole('link', { name: 'Filing index', exact: true })).toHaveAttribute('href', row.filing_url);
    await expect(detail.getByRole('link', { name: 'Report document', exact: true })).toHaveAttribute('href', row.report_url);
  }
  await expect(detail.locator('img')).toHaveCount(0);
  await detail.press('Escape'); await expect(detail).toHaveCount(0); await expect(selector).toBeFocused();
  return label;
}
