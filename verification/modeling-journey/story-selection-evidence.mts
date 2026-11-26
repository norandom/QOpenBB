import { createHash } from "node:crypto";
import type { Locator, Page } from "../../vendor/workspace/terminalpro/node_modules/@playwright/test/index";
import { expect } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/toolchain";

interface Row {
  observation_date: string;
  record_id: string;
  entity_id: string;
  value: string;
  published_at: string | null;
  vintage_at: string | null;
  context: { currency: string; unit: string; basis: string; vintage_coverage: string };
}
interface Output {
  output_id: string;
  trace_ids: string[];
  check_ids: string[];
  unit: string;
  status: string;
  value: string;
}
interface Run {
  run_id: string;
  outputs: Output[];
  verification: { output_id: string; status: string }[];
  checks: { rule_id: string; severity: string; status: string; explanation: string }[];
  trace: {
    trace_id: string;
    source_record_ids: string[];
    intermediate_values: { name: string; period_start: string; period_end: string; value: string; unit: string }[];
  }[];
  inputs: {
    cutoff: { observation_date: string; decision_at: string; session_timezone: string };
    provenance: { source: string; retrieved_at: string; query: [string, string][] };
    tables: { table_id: string; rows: Row[] }[];
  };
}

function fingerprint(value: unknown) {
  return createHash("sha256").update(JSON.stringify(value)).digest("hex");
}

async function savedRun(page: Page, date: string, dataset: string): Promise<Run> {
  const submitted = await page.waitForResponse(response => {
    const request = response.request();
    if (request.method() !== "POST" || new URL(response.url()).pathname !== "/modeling/v1/evaluations") return false;
    const acquisition = request.postDataJSON()?.acquisition;
    return acquisition?.dataset_id === dataset && acquisition.cutoff.observation_date === date;
  }, { timeout: 75_000 });
  expect(submitted.status(), dataset).toBe(200);
  const run = await submitted.json();
  expect(run.run_id).toMatch(/^[a-zA-Z0-9_-]+$/);
  const authorization = await submitted.request().headerValue("authorization");
  if (!authorization) throw new Error("Authenticated story bridge request required");
  const response = await page.request.get("/modeling/v1/runs/" + run.run_id, { headers: { authorization } })
    .catch(() => { throw new Error(dataset + " saved run bridge request failed"); });
  expect(response.status(), dataset + " saved run").toBe(200);
  const saved = await response.json() as Run;
  expect(fingerprint(saved)).toBe(fingerprint(run));
  expect(saved.inputs.cutoff.observation_date).toBe(date);
  return saved;
}

export async function runsFor(page: Page, date: string) {
  const [price, macro] = await Promise.all([
    savedRun(page, date, "story.etf_pair"), savedRun(page, date, "story.dfii10"),
  ]);
  return { price, macro };
}

function rows(run: Run, table: string) {
  return run.inputs.tables.find(item => item.table_id === table)?.rows ?? [];
}

function output(run: Run, id: string) {
  return run.outputs.find(item => item.output_id === id)!;
}

function verified(run: Run, id: string, unit: string) {
  const result = output(run, id);
  expect(result).toMatchObject({ status: "verified", unit });
  expect(run.verification.find(item => item.output_id === id)?.status).toBe("match");
  return result.value;
}

function points(value: string) {
  return (Number(value) > 0 && !value.startsWith("+") ? "+" : "") + value + " pp";
}

async function datedTable(region: Locator, label: string, headers: string[], expected: string[][]) {
  const summary = region.locator("summary").filter({ hasText: new RegExp("^" + label + "$") });
  await summary.press("Enter");
  await expect(summary).toBeFocused();
  const scroll = region.getByRole("region", { name: label, exact: true });
  await summary.press("Tab");
  await expect(scroll).toBeFocused();
  const table = scroll.getByRole("table", { name: label, exact: true });
  await expect(table.getByRole("columnheader")).toHaveText(headers);
  const body = table.locator("tbody tr");
  await expect(body).toHaveCount(expected.length);
  expect(await body.evaluateAll(elements =>
    elements.map(row => Array.from(row.querySelectorAll("th,td"), cell => cell.textContent)))).toEqual(expected);
  await summary.press("Enter");
  await expect(table).toBeHidden();
}

type ChartSeries = { label: string; rows: [string, string, string][] };

async function chart(region: Locator, label: string, source: string, unit: string, expected: ChartSeries[]) {
  const figure = region.getByRole("figure", { name: label, exact: true });
  await expect(figure.locator("figcaption")).toContainText(source);
  if (expected.length > 1) {
    const type = region.getByRole("combobox", { name: label + " type", exact: true });
    await type.press("Tab");
    const controls = region.getByRole("group", { name: label, exact: true });
    await expect(controls.getByRole("checkbox").first()).toBeFocused();
  }
  const canvas = figure.locator("canvas").first();
  await expect(canvas).toBeVisible();
  await expect(figure.getByRole("alert")).toHaveCount(0);
  // Read the options supplied to the mounted renderer. The browser's canvas itself has no data API.
  const projected = await canvas.evaluate(element => {
    type Fiber = { return: Fiber | null; memoizedProps?: { options?: {
      xAxis: { data: string[]; name: string };
      yAxis: { name: string };
      series: { name: string; data: ({ value: number; tooltip: { formatter: string } } | null)[] }[];
    } } };
    const host = element.closest("[_echarts_instance_]") ?? element.parentElement;
    const key = Object.keys(host!).find(name => name.startsWith("__reactFiber$"));
    let fiber = key ? (host as unknown as Record<string, Fiber>)[key] : undefined;
    while (fiber && !fiber.memoizedProps?.options) fiber = fiber.return ?? undefined;
    const options = fiber?.memoizedProps?.options;
    if (!options) throw new Error("Mounted ECharts host has no series projection");
    const { xAxis, yAxis, series } = options;
    const context = (element as HTMLCanvasElement).getContext("2d")!;
    const painted = context.getImageData(0, 0, context.canvas.width, context.canvas.height).data.some((value, index) =>
      index % 4 === 3 && value !== 0);
    return { unit: yAxis.name, painted, series: series.map(item => ({
      name: item.name, rows: item.data.flatMap((point, index) => point ?
        [[xAxis.data[index], point.value, point.tooltip.formatter]] : []),
    })) };
  });
  expect(projected).toEqual({ unit, painted: true, series: expected.map(item => ({
    name: item.label,
    rows: item.rows.map(([date, value, display]) => [date, Number(value), item.label + " · " + date + " · " + display]),
  })) });
}

function decimalPercent(ratio: string) {
  // The reference trace stores ratios. Rescale the decimal without rounding away significant digits.
  const match = /^(-?)(\d+)(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/.exec(ratio)!;
  const [, sign, whole, fraction = "", exponent = "0"] = match;
  const digits = whole + fraction;
  const position = whole.length + Number(exponent) + 2;
  const fixed = position <= 0 ? "0." + "0".repeat(-position) + digits :
    digits.padEnd(position, "0").slice(0, position) + "." + digits.slice(position);
  return (sign + fixed.replace(/^0+(?=\d)/, "").replace(/0+$/, "").replace(/\.$/, "")) + "%";
}

async function checkLeg(run: Run, region: Locator, side: string, symbol: string, days: string[], risk: boolean) {
  const metric = risk ? "volatility" : "momentum";
  const result = output(run, side + "_" + metric);
  const value = verified(run, result.output_id, "percent");
  const trace = run.trace.find(item => item.trace_id === result.trace_ids[0])!;
  const closes = rows(run, side + "_closes").filter(row => trace.source_record_ids.includes(row.record_id));
  expect(closes.map(row => row.observation_date)).toEqual(days);
  expect(closes.every(row => row.entity_id === symbol && row.context.currency === "USD" &&
    row.context.basis === "split_adjusted_dividends_excluded" && row.published_at === null)).toBe(true);
  const receipt = new Map(run.inputs.provenance.query).get(side + "_retrieved_at")!;
  expect(Date.parse(receipt)).toBeGreaterThanOrEqual(Date.parse(days.at(-1)!));
  await expect(region.getByText(new RegExp(symbol + " historical closes as retrieved from FMP at")).locator("time")).toHaveText(receipt);
  const returns = trace.intermediate_values.filter(item => item.name.startsWith("simple_return."));
  if (risk) {
    expect(returns.map(item => [item.period_start, item.period_end, item.unit]))
      .toEqual(days.slice(1).map((day, index) => [days[index], day, "ratio"]));
  }
  const tableLabel = symbol + (risk ? " daily simple returns" : " session closes");
  const expected = risk ? returns.map(item => [item.period_end, decimalPercent(item.value), item.period_start]) :
    closes.map(item => [item.observation_date, item.value]);
  await datedTable(region, tableLabel, risk ? ["Ending session", "Simple return (%)", "Starting session"] :
    ["Session date", "Close (USD)"], expected);
  return {
    input: { label: symbol, rows: expected.map(([date, amount]): [string, string, string] =>
      [date, risk ? amount.slice(0, -1) : amount, risk ? amount : amount + " USD"]) },
    result: { label: symbol, rows: [[symbol, value, value + "%"]] } as ChartSeries,
    digest: fingerprint(expected),
  };
}

async function priceView(story: Locator, run: Run, pair: readonly [string, string], days: string[], risk: boolean) {
  const view = risk ? "Realized volatility" : "Price returns";
  const region = story.getByRole("region", { name: view + " from FMP", exact: true });
  await expect(region).toContainText("Observation date " + days.at(-1));
  await expect(region).toContainText("Window " + days[0] + " to " + days.at(-1));
  await expect(region).toContainText("Calendar NYSE_ARCA, revision nyse-arca.2026r1");
  await expect(region).toContainText("64 trading-session dates in the window");
  await expect(region).toContainText("Historical publication and vintage are unknown");
  await expect(region).toContainText(risk ? "63 daily simple returns" : "Dividends excluded");
  await expect(region.getByText("Verified against the independent reference.", { exact: true }))
    .toHaveCount(risk ? 2 : 3);
  const left = await checkLeg(run, region, "left", pair[0], days, risk);
  const right = await checkLeg(run, region, "right", pair[1], days, risk);
  await chart(region, view + " input chart", pair.join(" and ") + " · FMP", risk ? "%" : "USD", [left.input, right.input]);
  await chart(region, view + " result chart", pair.join(" and ") + " · FMP", "%", [left.result, right.result]);
  return [left.digest, right.digest];
}

export async function inspectPrices(story: Locator, run: Run, pair: readonly [string, string]) {
  expect(run.inputs.provenance.source).toBe("fmp");
  const days = rows(run, "sessions").map(row => row.observation_date);
  expect(days).toHaveLength(64);
  expect(days.at(-1)).toBe(run.inputs.cutoff.observation_date);
  const sessionRows = await priceView(story, run, pair, days, false);
  const dailyReturns = await priceView(story, run, pair, days, true);
  const spread = verified(run, "momentum_spread", "percentage_points");
  const verdict = story.getByRole("region", { name: "Verdict", exact: true }).getByRole("status");
  await expect(verdict).toContainText(days[0] + " to " + days.at(-1));
  await expect(verdict).toContainText(pair.join(" and "));
  await expect(verdict).toContainText(points(spread));
  const returns = story.getByRole("region", { name: "Price returns from FMP", exact: true });
  await expect(returns).toContainText("Spread (commodity minus technology)");
  await expect(returns).toContainText(points(spread));
  const positive = Number(spread) > 0;
  const winner = positive ? pair[0] : pair[1];
  const other = positive ? pair[1] : pair[0];
  await expect(verdict).toContainText(Number(spread) === 0 ? "The proxies tied." : winner + " outperformed " + other);
  const riskDifference = Number(output(run, "left_volatility").value) - Number(output(run, "right_volatility").value);
  if (Number(spread) * riskDifference > 0) await expect(verdict).toContainText(winner + " also had higher realized volatility.");
  return { runId: run.run_id, pair, window: [days[0], days.at(-1)], spreadPercentagePoints: spread,
    closeCountPerLeg: 64, returnCountPerLeg: 63, sessionRows, dailyReturns,
    retrievedAt: Object.fromEntries(run.inputs.provenance.query.filter(([key]) => /^(left|right)_retrieved_at$/.test(key))) };
}

export async function inspectMacro(story: Locator, run: Run, price: Run) {
  expect(run.inputs.cutoff).toEqual(price.inputs.cutoff);
  expect(run.inputs.provenance.source).toBe("fred");
  const region = story.getByRole("region", { name: /DFII10 real yields from the Board of Governors.*via FRED/ });
  await expect(region).toContainText("This product uses the FRED® API but is not endorsed or certified");
  await expect(region.locator("time")).toHaveText([run.inputs.provenance.retrieved_at, run.inputs.cutoff.decision_at]);
  const days = rows(run, "sessions").map(row => row.observation_date);
  const endpoints = [days[0], days.at(-1)!];
  const eligible = rows(run, "dfii10").filter(row => endpoints.includes(row.observation_date) &&
    row.value !== null && row.published_at && row.context.vintage_coverage === "known" &&
    Date.parse(row.published_at) <= Date.parse(run.inputs.cutoff.decision_at) &&
    (!row.vintage_at || Date.parse(row.vintage_at) <= Date.parse(run.inputs.cutoff.decision_at)));
  if (eligible.length) {
    await datedTable(region, "DFII10 endpoint rows", ["Observation date", "Real yield (%)", "Published at", "Vintage at"],
      eligible.map(row => [row.observation_date, row.value + "%", row.published_at!, row.vintage_at ?? "Unavailable"]));
    await chart(region, "Real yields input chart", "Board of Governors of the Federal Reserve System via FRED", "%",
      [{ label: "DFII10", rows: eligible.map(row => [row.observation_date, row.value, row.value + "%"]) }]);
  } else {
    await expect(region.getByRole("figure", { name: "Real yields input chart", exact: true })).toHaveCount(0);
  }
  if (eligible.length === 2) {
    const regime = verified(run, "regime", "classification");
    const change = verified(run, "change", "percentage_points");
    await expect(region).toContainText("DFII10 regime · " + regime);
    await chart(region, "Real yields result chart", "Board of Governors of the Federal Reserve System via FRED", "pp",
      [{ label: "Real yield change", rows: [[endpoints.join(" to "), change, points(change)]] }]);
    return { runId: run.run_id, status: "verified", endpointDates: endpoints };
  }
  const unavailable = endpoints.filter(day => !eligible.some(row => row.observation_date === day));
  for (const id of ["regime", "change"]) {
    const result = output(run, id);
    expect(result.status).toBe("withheld");
    const check = run.checks.find(item => result.check_ids.includes(item.rule_id) &&
      item.status === "fail" && item.severity === "blocking" && item.explanation.includes("DFII10 endpoint"));
    for (const day of unavailable) expect(check?.explanation).toContain(day);
    await expect(region.getByText(check!.explanation).first()).toBeVisible();
  }
  await expect(region.getByRole("figure", { name: "Real yields result chart", exact: true })).toHaveCount(0);
  await expect(story.getByRole("region", { name: "Verdict", exact: true })).toContainText("Realized price-return spread");
  return { runId: run.run_id, status: "withheld", unavailableEndpointDates: unavailable,
    eligibleEndpointCount: eligible.length };
}
