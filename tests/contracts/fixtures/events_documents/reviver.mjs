import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { chromium } from '../../../../verification/node_modules/@playwright/test/index.mjs';

const raw = await readFile(new URL('./receipts.v1.json', import.meta.url), 'utf8');
const browser = await chromium.launch({ headless: true, args: ['--disable-background-networking'] });
try {
  const context = await browser.newContext({ offline: true });
  const page = await context.newPage();
  const cdp = await context.newCDPSession(page);
  const exceptions = [];
  const requests = [];
  cdp.on('Runtime.exceptionThrown', event => exceptions.push(event.exceptionDetails.text));
  cdp.on('Network.requestWillBeSent', event => requests.push(event.request.url));
  await cdp.send('Runtime.enable');
  await cdp.send('Network.enable');
  const result = await page.evaluate(raw => {
    const fields = ['eps_actual', 'eps_consensus', 'revenue_actual', 'revenue_consensus'];
    const tokens = new WeakMap();
    const cases = JSON.parse(raw, function (key, value, context) {
      if (fields.includes(key) && typeof value === 'number') {
        if (!tokens.has(this)) tokens.set(this, {});
        tokens.get(this)[key] = context?.source;
      }
      return value;
    });
    const { body, receipt } = cases['calendar-duplicate'];
    const byOrdinal = Object.fromEntries(body.results.flatMap((row, ordinal) =>
      tokens.has(row) ? [[ordinal, tokens.get(row)]] : []));
    return {
      byOrdinal,
      expected: receipt.tokens,
      rounded: String(body.results[0].revenue_actual),
      missing: body.results[1].eps_consensus,
    };
  }, raw);
  assert.deepEqual(result.byOrdinal, result.expected);
  assert.equal(result.byOrdinal['0'].revenue_actual, '9007199254740993');
  assert.equal(result.rounded, '9007199254740992');
  assert.equal(result.byOrdinal['0'].eps_actual, '0');
  assert.equal(result.missing, null);
  assert.deepEqual(exceptions, []);
  assert.deepEqual(requests, []);
  console.log(`Chromium ${browser.version()} recovered exact numeric tokens in an offline context`);
} finally {
  await browser.close();
}
