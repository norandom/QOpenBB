import assert from 'node:assert/strict';

const beans = {};
beans.context = { beans };
const primitive = (value, path) => {
  if (value === null || ['string', 'boolean'].includes(typeof value)) return value;
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  throw new TypeError(`Unexpected capture value at ${path}`);
};
const project = (source, keys) => Object.fromEntries(keys
  .filter(key => source?.[key] !== undefined)
  .map(key => [key, primitive(source[key], key)]));
const row = { period: '2024-Q1', revenue: 0, operatingIncome: null, beans };
const model = { chartId: 'synthetic', chartType: 'line', switchCategorySeries: false, context: beans };
assert.throws(() => JSON.stringify({ model, data: [row] }), /circular/i);
const captured = {
  model: project(model, ['chartId', 'chartType', 'switchCategorySeries']),
  data: [project(row, ['period', 'revenue', 'operatingIncome'])],
  marker: project({ enabled: false, size: 0 }, ['enabled', 'size']),
};
assert.deepEqual(JSON.parse(JSON.stringify(captured)), {
  model: { chartId: 'synthetic', chartType: 'line', switchCategorySeries: false },
  data: [{ period: '2024-Q1', revenue: 0, operatingIncome: null }],
  marker: { enabled: false, size: 0 },
});
assert.throws(() => primitive(Infinity, 'size'), /Unexpected/);
assert.throws(() => primitive(beans, 'size'), /Unexpected/);
console.log('PASS: cycle reproduced; explicit projection preserves zero, false, null and rejects objects/nonfinite numbers.');
