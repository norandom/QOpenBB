import { test, expect } from '../../verification/node_modules/@playwright/test/index.js';
import { isolatedRun } from '../../verification/runner.ts';

test('fixture observation and independent browser state', async () => {
  const result = await isolatedRun();
  expect(result.status).toBe('passed');
  expect(result.observation).toBe('123.45 USD');
  expect(result.isolated).toBe(true);
  expect(result.cleaned).toBe(true);
  expect(result.browserClosed).toBe(true);
  expect(await closed(result.port)).toBe(true);
});
import { readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { createConnection } from 'node:net';
import { spawnSync } from 'node:child_process';
import { startFixture } from '../../verification/fixture_server.ts';
import { capturePolicy } from '../../verification/capture.ts';
import { browserEnvironment } from '../../verification/evidence.ts';

async function closed(port: number) {
  return new Promise<boolean>(resolve => {
    const socket = createConnection({ host: '127.0.0.1', port });
    socket.once('error', () => resolve(true));
    socket.once('connect', () => { socket.destroy(); resolve(false); });
  });
}

test('CDP failure evidence excludes secret-bearing payloads and closes resources', async () => {
  const result = await isolatedRun({ fail: true });
  expect(result.status).toBe('failed');
  expect(result.diagnostics.map(event => event.kind)).toEqual(expect.arrayContaining(['console', 'network']));
  expect(result.cleaned).toBe(true);
  expect(result.browserClosed).toBe(true);
  expect(await closed(result.port)).toBe(true);
  expect(await closed(result.port)).toBe(true);
  const files = await readdir(result.root);
  expect(files).toEqual(['evidence.json']);
  expect(await readFile(join(result.root, 'evidence.json'), 'utf8')).not.toContain('SYNTHETIC_SECRET_DO_NOT_RETAIN');
});

for (const fault of ['startupFailure', 'artifactFailure'] as const) {
  test(`${fault} closes owned resources`, async () => {
    const result = await isolatedRun({ [fault]: true });
    expect(result.status).toBe('failed');
    expect(result.cleaned).toBe(true);
  expect(result.browserClosed).toBe(true);
  expect(await closed(result.port)).toBe(true);
    expect(await closed(result.port)).toBe(true);
    expect(await readdir(result.root)).toEqual(['evidence.json']);
  });
}

test('credential capture is refused before creating resources; environment is allowlisted', async () => {
  expect(() => capturePolicy(true, true)).toThrow('capture forbidden');
  expect(capturePolicy(true)).toEqual({ trace: false, screenshot: false, video: false });
  process.env.FMP_API_KEY = 'SYNTHETIC_SECRET_DO_NOT_RETAIN';
  process.env.NODE_OPTIONS = '--inspect';
  try {
    expect(browserEnvironment()).not.toHaveProperty('FMP_API_KEY');
    expect(browserEnvironment()).not.toHaveProperty('NODE_OPTIONS');
  } finally { delete process.env.FMP_API_KEY; delete process.env.NODE_OPTIONS; }
});

test('existing fixture listener is refused', async () => {
  const fixture = await startFixture();
  try { await expect(startFixture(fixture.port)).rejects.toThrow('EADDRINUSE'); }
  finally { await fixture.close(); }
});

test('unexpected diagnostic failure exits nonzero', () => {
  const result = spawnSync(process.execPath, ['verification/runner.ts', '--failure'], {
    encoding: 'utf8', windowsHide: true, timeout: 45000, env: browserEnvironment(),
  });
  expect(result.status).toBe(1);
  expect(result.stdout).toContain('failed');
  expect(result.stdout + result.stderr).not.toContain('SYNTHETIC_SECRET_DO_NOT_RETAIN');
});


test('browser concurrency overrides are refused', () => {
  for (const argument of ['--workers=8', '-j8']) {
    const result = spawnSync(process.execPath, ['verification/node_modules/@playwright/test/cli.js',
      'test', '--config', 'verification/playwright.config.ts', '--list', argument], {
      encoding: 'utf8', windowsHide: true, timeout: 30000, env: browserEnvironment(),
    });
    expect(result.status).not.toBe(0);
    expect(result.stdout + result.stderr).toContain('worker override forbidden');
  }
});
