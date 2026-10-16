import { defineConfig } from '@playwright/test';
if (process.argv.some(value => /^(--workers(=|$)|-j)/.test(value)) || process.env.PW_TEST_WORKERS || process.env.PWDEBUG) {
  throw new Error('worker override forbidden; browser ceiling is one');
}
export default defineConfig({ testDir: '../tests/e2e', workers: 1, retries: 0,
  reporter: [['line']], outputDir: '../artifacts/task-1.7/test-results',
  use: { headless: true, trace: 'off', screenshot: 'off', video: 'off' } });
