import { defineConfig } from '@playwright/test';
import { join } from 'node:path';
import { browserEnvironment, outputRoot } from './evidence.ts';
browserEnvironment();
if (process.argv.some(value => /^(--workers(=|$)|-j)/.test(value)) || process.env.PW_TEST_WORKERS || process.env.PWDEBUG) {
  throw new Error('worker override forbidden; browser ceiling is one');
}
export default defineConfig({ testDir: '../tests/e2e', testMatch: 'infrastructure.spec.mts', workers: 1, retries: 0,
  reporter: [['line']], outputDir: join(outputRoot(), 'test-results'),
  use: { headless: true, trace: 'off', screenshot: 'off', video: 'off' } });
