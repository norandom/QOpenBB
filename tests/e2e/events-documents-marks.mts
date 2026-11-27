import { expect } from '../../verification/node_modules/@playwright/test/index.mjs';
import type { BrowserContext, Locator } from '../../verification/node_modules/@playwright/test/index.mjs';

type TextDraw = { text: string; x: number; y: number };
type DrawLog = WeakMap<HTMLCanvasElement, TextDraw[]>;
const colors = {
  actual: ['23,103,169', '134,185,252'],
  estimate: ['168,91,36', '246,167,108'],
};

export async function observeChartCanvas(context: BrowserContext) {
  await context.addInitScript(() => {
    const prototype = CanvasRenderingContext2D.prototype;
    const draw = prototype.fillText;
    const log = new WeakMap<HTMLCanvasElement, TextDraw[]>();
    Object.defineProperty(window, '__eventsChartDrawLog', { value: log, configurable: false });
    prototype.fillText = function (text, x, y, maxWidth) {
      const point = this.getTransform().transformPoint({ x, y });
      const current = log.get(this.canvas) ?? [];
      if (!log.has(this.canvas)) log.set(this.canvas, current);
      if (current.length >= 4096) current.splice(0, 2048);
      current.push({ text, x: point.x, y: point.y });
      if (maxWidth === undefined) return draw.call(this, text, x, y);
      return draw.call(this, text, x, y, maxWidth);
    };
  });
}

async function renderedGeometry(canvas: Locator) {
  return canvas.evaluate((element, palette) => {
    const image = element as HTMLCanvasElement;
    const { width, height } = image;
    const context = image.getContext('2d');
    if (!context) throw new Error('Calendar chart canvas unavailable');
    const data = context.getImageData(0, 0, width, height).data;
    const log = (window as unknown as { __eventsChartDrawLog: DrawLog }).__eventsChartDrawLog;
    const text = log.get(image) ?? [];
    const categories = Object.fromEntries(
      ['Actual', 'Estimate'].map(name => [name.toLowerCase(), text.findLast(label => label.text === name)?.x]),
    );
    const ticks = Array.from(new Map(text.filter(label => /^-?\d[\d,.]*(?:e[+-]?\d+)?$/i.test(label.text))
      .filter(label => label.x < Math.min(categories.actual ?? 0, categories.estimate ?? 0))
      .map(label => [label.text, label])).values(), label => ({
      value: label.text.replaceAll(',', ''), y: label.y,
    }));
    const marks: { category: string; left: number; right: number; top: number; bottom: number }[] = [];
    const classes = new Uint8Array(width * height);
    const [actual, estimated] = [palette.actual, palette.estimate].map(group =>
      group.map(color => color.split(',').map(Number)));
    for (let pixel = 0; pixel < classes.length; pixel++) {
      const offset = pixel * 4;
      // Scatter marks are 80% opaque. Canvas readback can round premultiplied RGB.
      if (data[offset + 3] < 170) continue;
      const matches = (color: number[]) => color.every((channel, index) => Math.abs(data[offset + index] - channel) <= 2);
      if (actual.some(matches)) classes[pixel] = 1;
      else if (estimated.some(matches)) classes[pixel] = 2;
    }
    for (let pixel = 0; pixel < classes.length; pixel++) {
      const category = classes[pixel];
      if (!category) continue;
      const x = pixel % width;
      const y = Math.floor(pixel / width);
      const bounds = { category: category === 1 ? 'actual' : 'estimate', left: x, right: x, top: y, bottom: y };
      const pending = [pixel];
      classes[pixel] = 0;
      for (let next = pending.pop(); next !== undefined; next = pending.pop()) {
        const column = next % width;
        const line = Math.floor(next / width);
        bounds.left = Math.min(bounds.left, column);
        bounds.right = Math.max(bounds.right, column);
        bounds.top = Math.min(bounds.top, line);
        bounds.bottom = Math.max(bounds.bottom, line);
        // The horizontal axis can paint through a zero point, splitting it by one pixel.
        const neighbors = [next - 2 * width, next - width, next + width, next + 2 * width,
          column > 0 ? next - 1 : -1, column + 1 < width ? next + 1 : -1];
        for (const neighbor of neighbors) if (classes[neighbor] === category) {
          classes[neighbor] = 0;
          pending.push(neighbor);
        }
      }
      marks.push(bounds);
    }
    const axisTitles = [...new Set(text.filter(label => ['EPS per share', 'Revenue (monetary amount)'].includes(label.text))
      .map(label => label.text))];
    return { width, height, ticks, categories, marks, axisTitles };
  }, colors);
}

async function tooltip(canvas: Locator, x: number, y: number) {
  const box = await canvas.boundingBox();
  if (!box) throw new Error('Calendar mark is outside the displayed canvas');
  await canvas.evaluate(element => (window as unknown as { __eventsChartDrawLog: DrawLog }).__eventsChartDrawLog
    .set(element as HTMLCanvasElement, []));
  await canvas.page().mouse.move(box.x + box.width * x, box.y + box.height * y);
  let text: string[] = [];
  await expect.poll(async () => {
    text = await canvas.evaluate(element => {
      const log = (window as unknown as { __eventsChartDrawLog: DrawLog }).__eventsChartDrawLog;
      return (log.get(element as HTMLCanvasElement) ?? []).map(draw => draw.text);
    });
    return text.some(line => /^Receipt \d+ · ordinal \d+ · \w+$/.test(line));
  }, { message: 'Canvas mark must show its own source identity' }).toBe(true);
  const identity = text.find(line => /^Receipt \d+ · ordinal \d+ · \w+$/.test(line))!;
  const detail = text.find(line => /^(Actual|Estimated) (EPS|revenue):/.test(line));
  const title = text.find(line => /^Report date \d{4}-\d{2}-\d{2} · market row \d+$/.test(line));
  const units = text.find(line => /^(Currency per share|Monetary amount|Unknown) · Currency/.test(line));
  if (!detail || !title || !units) throw new Error('Calendar canvas tooltip is missing source values');
  return { identity, detail, title, units };
}

export async function readCalendarChart(figure: Locator, measure: string, display: string) {
  const canvas = figure.locator('canvas');
  if (!(await canvas.count())) return null;
  await canvas.scrollIntoViewIfNeeded();
  let geometry!: Awaited<ReturnType<typeof renderedGeometry>>;
  await expect.poll(async () => {
    geometry = await renderedGeometry(canvas);
    return geometry.ticks.length >= 2 && geometry.categories.actual !== undefined && geometry.categories.estimate !== undefined;
  }, { message: 'Calendar renderer must expose its painted axes' }).toBe(true);
  const marks = [];
  for (const mark of geometry.marks) {
    const x = (mark.left + mark.right + 1) / (2 * geometry.width);
    const y = (mark.top + mark.bottom + 1) / (2 * geometry.height);
    marks.push({ ...mark, ...await tooltip(canvas, x, y) });
  }
  await figure.page().mouse.move(0, 0);
  const { ticks, categories, axisTitles } = geometry;
  return { measure, display, ticks, categories, axisTitles, marks };
}
