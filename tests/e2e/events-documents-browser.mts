import { readFileSync, renameSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { expect } from '../../verification/node_modules/@playwright/test/index.mjs';
import type { Locator, Page } from '../../verification/node_modules/@playwright/test/index.mjs';

export type Slot = 'calendar' | 'filings' | 'transcript' | 'news';
export const plan = JSON.parse(readFileSync(new URL('./events-documents-plan.json', import.meta.url), 'utf8')) as {
  slots: Record<Slot, [string, string]>;
  initial: Record<Slot, Record<string, string | number>>;
  edits: Record<Slot, Record<string, string | number>>;
  groups: Record<string, Slot[]>;
};

export const titles = { calendar: 'Calendar window', filings: 'Filing bounds', transcript: 'Transcript period', news: 'News bounds' };
export const fields = { eps_actual: 'Actual EPS', eps_consensus: 'Estimated EPS',
  revenue_actual: 'Actual revenue', revenue_consensus: 'Estimated revenue' };

export function query(stage: string, slot: Slot) {
  const choices = stage === slot || stage === 'reopen' ? plan.edits : plan.initial;
  return slot === 'calendar' ? choices.calendar : { symbol: stage === 'launch' ? 'AAPL' : 'MSFT', ...choices[slot] };
}

export async function arm(stage: string) {
  const directory = process.env.EVENTS_STAGE_DIR!;
  writeFileSync(join(directory, 'pending'), stage, { mode: 0o644 });
  renameSync(join(directory, 'pending'), join(directory, 'current'));
  await expect.poll(() => readFileSync(join(directory, 'applied'), 'utf8')).toBe(stage);
}

export async function login(page: Page, origin: string, credentials: { email: string; password: string }) {
  let entityReady: Promise<null | Error> | undefined;
  page.on('response', response => {
    if (new URL(response.url()).pathname === '/api/pro/user-has-entity') entityReady = response.finished();
  });
  await page.goto(origin + '/login');
  await page.getByLabel('Email', { exact: true }).fill(credentials.email);
  await page.getByLabel('Password', { exact: true }).fill(credentials.password);
  await page.getByRole('button', { name: 'Login', exact: true }).click();
  await page.waitForURL(url => /^\/(app|onboarding)(?:\/|$)/.test(url.pathname));
  if (new URL(page.url()).pathname === '/onboarding') {
    await expect.poll(() => Boolean(entityReady)).toBe(true);
    await entityReady;
    await page.evaluate(() => new Promise<void>(resolve => requestAnimationFrame(() => requestAnimationFrame(() => resolve()))));
    await page.getByPlaceholder('Enter your first name').fill('Browser');
    await page.getByPlaceholder('Enter your last name').fill('Verification');
    await page.getByRole('button', { name: 'Continue', exact: true }).click();
  }
  await expect(page).toHaveURL(url => /^\/app(?:\/|$)/.test(url.pathname));
  await expect(page.locator('#tabs')).toBeVisible();
}

export async function connect(page: Page, origin: string) {
  await page.goto(origin + '/app/connections');
  const changelog = page.getByRole('dialog').filter({ has: page.getByRole('heading', { name: 'Changelog', exact: true }) });
  await page.addLocatorHandler(changelog, () => changelog.getByRole('button', { name: 'Close', exact: true }).click());
  await page.getByRole('button', { name: 'Connect Backend', exact: true }).first().click();
  const dialog = page.getByRole('dialog').filter({ has: page.getByPlaceholder('OpenBB App') });
  await dialog.getByPlaceholder('OpenBB App').fill('Events candidate');
  await dialog.getByPlaceholder('http://127.0.0.1:5056').fill(origin + '/data');
  await dialog.getByRole('button', { name: 'Test', exact: true }).click();
  await expect(dialog.getByText('Test successful', { exact: true })).toBeVisible();
  await dialog.getByRole('button', { name: /^add$/i }).click();
  await expect(dialog).not.toBeVisible();
  await page.getByRole('link', { name: 'Apps', exact: true }).click();
}

const fieldLabels = { start_date: 'Start date', end_date: 'End date', page: 'Page', limit: 'Limit', year: 'Year', quarter: 'Quarter' };

export async function edit(story: Locator, slot: Slot) {
  const group = story.getByRole('group', { name: titles[slot], exact: true });
  for (const [field, value] of Object.entries(plan.edits[slot])) {
    await group.getByLabel(fieldLabels[field as keyof typeof fieldLabels], { exact: true }).fill(String(value));
  }
  await group.getByRole('button', { name: 'Apply ' + titles[slot].toLowerCase(), exact: true }).click();
}

export async function restoredChoices(story: Locator) {
  await expect(story.getByRole('button', { name: 'Microsoft (MSFT)', exact: true })).toHaveAttribute('aria-pressed', 'true');
  for (const slot of Object.keys(plan.edits) as Slot[]) {
    const group = story.getByRole('group', { name: titles[slot], exact: true });
    for (const [field, value] of Object.entries(plan.edits[slot])) {
      await expect(group.getByLabel(fieldLabels[field as keyof typeof fieldLabels], { exact: true })).toHaveValue(String(value));
    }
  }
  await expect(story.getByLabel('EPS chart display')).toHaveValue('point');
  await expect(story.getByLabel('Revenue chart display')).toHaveValue('bar');
}

export async function downloadTemplate(page: Page, id: string) {
  await page.locator(`#tab-${id}`).click({ button: 'right' });
  await page.getByRole('menuitem', { name: 'Export apps.json', exact: true }).click();
  const dialog = page.getByRole('dialog').filter({ has: page.getByRole('heading', { name: 'Export App', exact: true }) });
  await dialog.getByPlaceholder('Enter app name...').fill('Events review');
  await dialog.getByPlaceholder('Describe what this app does and when to use it...').fill('Bounded events and documents');
  const downloading = page.waitForEvent('download');
  await dialog.getByRole('button', { name: 'Download App', exact: true }).click();
  const path = await (await downloading).path();
  if (!path) throw new Error('Missing template download');
  return JSON.parse(readFileSync(path, 'utf8'));
}

export const finalChoices = { version: 1, symbol: 'MSFT', ...plan.edits, charts: { eps: 'point', revenue: 'bar' } };
