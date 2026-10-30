import { readFileSync } from "node:fs";
import type { Locator, Page, Response } from "../../verification/node_modules/@playwright/test/index.js";
import { expectApplicationDiagnostics, observeApplication } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/diagnostics";
import { saveDashboard } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/editor";
import { expect, loginDisposableWorkspace, test } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/fixtures";

const widgetId = "equity_fundamental_income_fmp_obb";
const incomePath = "/data/api/v1/equity/fundamental/income";

async function revenueCell(widget: Locator, field: string) {
  const cell = widget.locator(`.ag-row[row-index="0"] [col-id="${field}"]`).first();
  // Column virtualization requires moving the real viewport, not reading grid internals.
  for (let step = 0; step < 25 && !(await cell.count()); step++) {
    await widget
      .locator(".ag-body-horizontal-scroll-viewport")
      .evaluate((element, position) => {
        element.scrollLeft = position;
      }, step * 450);
    await widget.page().waitForTimeout(60);
  }
  await expect(cell).toBeVisible();
  await cell.scrollIntoViewIfNeeded();
  await expect(cell).toBeInViewport();
  return cell;
}

async function connectInstalledCatalog(page: Page, inspect?: (catalog: Record<string, any>) => void) {
  await page.goto("/app/connections");
  await page
    .getByRole("button", { name: "Connect Backend", exact: true })
    .first()
    .click();
  const dialog = page.getByRole("dialog").filter({
    has: page.getByRole("heading", { name: "Connect backend", exact: true }),
  });
  await dialog.getByPlaceholder("OpenBB App").fill("Installed QOpenBB data API");
  await dialog
    .getByPlaceholder("http://127.0.0.1:5056")
    .fill(`${process.env.WORKSPACE_FRONTEND_ORIGIN}/data`);
  const catalog = page.waitForResponse(
    (response) => new URL(response.url()).pathname === "/data/widgets.json",
  );
  await dialog.getByRole("button", { name: "Test", exact: true }).click();
  const response = await catalog;
  expect(response.status()).toBe(200);
  const catalogDefinition = await response.json();
  inspect?.(catalogDefinition);
  const definition = catalogDefinition[widgetId];
  expect(definition.endpoint).toBe("/api/v1/equity/fundamental/income");
  expect(definition.data.dataKey).toBe("results");
  expect(
    definition.params.find(
      (param: { paramName: string }) => param.paramName === "period",
    ).value,
  ).toBe("annual");
  await expect(dialog.getByText("Test successful", { exact: true })).toBeVisible();
  await dialog.getByRole("button", { name: /^add$/i }).click();
  await expect(dialog).not.toBeVisible();
  await page.getByRole("link", { name: "Apps", exact: true }).click();
  const starter = page.getByRole("button").filter({
    has: page.getByText("QOpenBB starter", { exact: true }),
  });
  await expect(starter).toBeVisible();
  return starter;
}

function incomeQuery(response: Response, symbol: string, period: string) {
  const url = new URL(response.url());
  return url.origin === process.env.WORKSPACE_FRONTEND_ORIGIN &&
    url.pathname === incomePath && url.searchParams.get("provider") === "fmp" &&
    (url.searchParams.get("symbol") ?? "") === symbol && url.searchParams.get("period") === period;
}

function incomeMetadata(payload: any, symbol: string, period: string) {
  const metadata = payload.extra.results_metadata.__qopenbb_financial__;
  expect(metadata).toMatchObject({
    dataset: "equity/fundamental/income", provider: "fmp",
    source: { endpoint: "income-statement" }, effective_query: { symbol, period },
    observation_date_field: "period_ending", point_in_time_safe: false,
    vintage_query_supported: null,
    bounds: { returned_count: payload.results.length, completeness: "unknown", truncated: null },
  });
  expect(Number.isFinite(Date.parse(metadata.retrieved_at))).toBe(true);
  expect(Date.parse(metadata.retrieved_at)).toBeLessThanOrEqual(Date.now() + 1000);
  expect(metadata.limitations.length).toBeGreaterThan(0);
  expect(metadata.fields.revenue).toMatchObject({
    unit: "currency", scale: 1, currency_field: "reported_currency",
    period_basis: period === "annual" ? "annual" : "discrete_quarter",
    value_origin: "provider_observation",
  });
  return metadata;
}

async function verifyNativeIncome(widget: Locator, payload: any, symbol: string, period: string) {
  const metadata = incomeMetadata(payload, symbol, period);
  const row = payload.results[0];
  expect(row).toMatchObject({ symbol, reported_currency: "USD" });
  expect(row.fiscal_period).toMatch(period === "annual" ? /^FY$/ : /^Q[1-4]$/);
  expect(row.period_ending).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  expect(Number.isFinite(row.revenue)).toBe(true);
  expect(row.revenue).toBeGreaterThan(0);
  await expect(widget.getByPlaceholder("Symbol", { exact: true })).toHaveValue(symbol);
  await expect(widget.getByRole("button", { name: period, exact: true })).toBeVisible();
  await expect(await revenueCell(widget, "symbol")).toHaveText(symbol);
  await expect(await revenueCell(widget, "reported_currency")).toHaveText(row.reported_currency);
  const date = await revenueCell(widget, "period_ending");
  await expect.poll(async () => new Date(await date.innerText()).toISOString().slice(0, 10)).toBe(row.period_ending);
  const revenue = await revenueCell(widget, "revenue");
  await expect.poll(async () => {
    const text = (await revenue.innerText()).replace(/[,\s$]/g, "").toUpperCase();
    const match = /^(-?\d+(?:\.(\d+))?)([KMBT])?$/.exec(text);
    if (!match) return false;
    const scale = ({ K: 1e3, M: 1e6, B: 1e9, T: 1e12 } as Record<string, number>)[match[3]] ?? 1;
    // Compare the source amount with the displayed decimal quantum, including suffix scale.
    const quantum = scale * 10 ** -(match[2]?.length ?? 0);
    return Math.abs(Number(match[1]) * scale - row.revenue) <= quantum / 2 + Number.EPSILON * row.revenue;
  }).toBe(true);
  return { symbol, period, row: { currency: row.reported_currency, fiscal_period: row.fiscal_period,
    period_ending: row.period_ending, revenue: row.revenue }, metadata };
}

async function setIncomeSymbol(widget: Locator, symbol: string) {
  const input = widget.getByPlaceholder("Symbol", { exact: true });
  await input.fill(symbol);
  await expect(input).toHaveValue(symbol);
  await input.press("Tab");
  await expect(input).toHaveValue(symbol);
}

async function refreshIncome(widget: Locator) {
  await widget.locator("button").filter({
    has: widget.page().locator('svg use[href$="#timer-icon"]'),
  }).click();
}

test("local packaged financial widgets support native company period recovery and saved reopen", async ({ page, browser }, info) => {
  test.setTimeout(240000);
  const runtime = JSON.parse(readFileSync(process.env.WORKSPACE_RUNTIME_PRIVATE!, "utf8"));
  expect(runtime.name).toMatch(/^qopenbb-browser-/);
  expect(runtime.packaged_image_only).toBe(true);
  expect(runtime.source_overlay).toBeNull();
  expect(runtime.release_image_verified).toBe(false);
  for (const name of ["workspace", "data-api"]) expect(runtime.images[name]).toMatch(/^sha256:[a-f0-9]{64}$/);
  const diagnostics = await observeApplication(page);
  let phase = "initial";
  const requestPhases = new Map<object, string>();
  const requests: { symbol: string | null; period: string | null; provider: string | null; limit: string | null; phase: string }[] = [];
  const responses: { symbol: string | null; period: string | null; status: number; phase: string | undefined }[] = [];
  const incomeFailures: { symbol: string | null; status: number; phase: string | undefined }[] = [];
  const trackIncome = (target: Page) => {
    target.on("request", request => {
      const url = new URL(request.url());
      if (url.pathname === incomePath) requests.push({ symbol: url.searchParams.get("symbol"),
        period: url.searchParams.get("period"), provider: url.searchParams.get("provider"), limit: url.searchParams.get("limit"), phase });
      requestPhases.set(request, phase);
    });
    target.on("response", response => {
      const url = new URL(response.url());
      if (url.pathname === incomePath) responses.push({ symbol: url.searchParams.get("symbol"),
        period: url.searchParams.get("period"), status: response.status(), phase: requestPhases.get(response.request()) });
      if (url.pathname === incomePath && response.status() >= 400)
        incomeFailures.push({ symbol: url.searchParams.get("symbol"), status: response.status(), phase: requestPhases.get(response.request()) });
    });
  };
  trackIncome(page);
  try {
    await loginDisposableWorkspace(page);
    await connectInstalledCatalog(page, catalog => {
      const native = Object.fromEntries(Object.entries(catalog).filter(([, definition]) =>
        typeof definition.endpoint === "string" && definition.endpoint.startsWith("/api/v1/"),
      ));
      expect(Object.keys(native).sort()).toEqual([
        "economy_fred_series_fred_obb", "equity_compare_peers_fmp_obb",
        ...["balance", "cash", "enterprise_values", "income", "metrics", "ratios"].map(name => `equity_fundamental_${name}_fmp_obb`),
        "equity_price_historical_fmp_obb", "equity_profile_fmp_obb", "equity_search_fmp_obb",
      ].sort());
      for (const definition of Object.values(native)) {
        expect(definition.type).toBe("table");
        expect(definition.endpoint).toMatch(/^\/api\/v1\//);
        expect(definition.data.dataKey).toBe("results");
        expect(definition.data.table.columnsDefs.length).toBeGreaterThan(0);
        expect(definition.params.some((param: any) => param.paramName === "provider")).toBe(true);
      }
      expect(catalog[widgetId].params.find((param: any) => param.paramName === "period").options)
        .toEqual(expect.arrayContaining([{ label: "annual", value: "annual" }, { label: "quarter", value: "quarter" }]));
    });
    await page.locator("#tabs").getByRole("button").first().click();
    await page.getByRole("button", { name: /New Dashboard/ }).click();
    await expect(page).toHaveURL(/\/app\/[\da-f-]{36}$/);
    const dashboardUrl = page.url();
    await page.getByRole("main").getByRole("button", { name: "Add widgets", exact: true }).click();
    const widgetMenu = page.getByRole("dialog");
    await widgetMenu.getByText("Income", { exact: true }).click();
    await widgetMenu.getByRole("button", { name: "Add widgets", exact: true }).click();
    const widget = page.locator(`#workarea .widget-${widgetId}`).last();
    await expect(widget).toBeVisible();
    // Wait for native initialization and its bounded missing-symbol retry before editing.
    await expect(widget.getByText("Invalid financial query parameters.", { exact: true })).toBeVisible();
    const observations: Awaited<ReturnType<typeof verifyNativeIncome>>[] = [];
    const initial = page.waitForResponse(response => incomeQuery(response, "AAPL", "annual"));
    // A new standalone widget has no issuer default; enter the baseline through its native control.
    phase = "selected";
    await setIncomeSymbol(widget, "AAPL");
    const initialResponse = await initial;
    expect(initialResponse.status()).toBe(200);
    const annual = await initialResponse.json();
    observations.push(await verifyNativeIncome(widget, annual, "AAPL", "annual"));
    const microsoftResponse = page.waitForResponse(response => incomeQuery(response, "MSFT", "annual"));
    await setIncomeSymbol(widget, "MSFT");
    const microsoft = await microsoftResponse;
    expect(microsoft.status()).toBe(200);
    observations.push(await verifyNativeIncome(widget, await microsoft.json(), "MSFT", "annual"));
    await setIncomeSymbol(widget, "AAPL");
    // The existing 15-minute query cache can reuse this exact successful query.
    observations.push(await verifyNativeIncome(widget, annual, "AAPL", "annual"));
    const quarterlyResponse = page.waitForResponse(response => incomeQuery(response, "AAPL", "quarter"));
    await widget.getByRole("button", { name: "annual", exact: true }).click();
    await page.locator(".obb-dropdown-container").getByText("quarter", { exact: true }).click();
    const quarterly = await quarterlyResponse;
    expect(quarterly.status()).toBe(200);
    const quarter = await quarterly.json();
    observations.push(await verifyNativeIncome(widget, quarter, "AAPL", "quarter"));
    await widget.locator("p.font-semibold").filter({ hasText: "Income" }).hover();
    const tooltip = page.locator(".TooltipContent").filter({ visible: true });
    await expect(tooltip.getByText("FMP", { exact: true }).filter({ visible: true })).toBeVisible();
    await expect(tooltip.getByText("Installed QOpenBB data API", { exact: true }).filter({ visible: true })).toBeVisible();
    await page.mouse.move(0, 0);
    const invalidResponse = page.waitForResponse(response => incomeQuery(response, "", "quarter"));
    phase = "invalid";
    await setIncomeSymbol(widget, "");
    const invalid = await invalidResponse;
    expect(invalid.status()).toBe(422);
    const failure = await invalid.json();
    expect(failure.code).toBe("invalid_parameters");
    expect(failure.detail).toMatch(/parameter|query|input/i);
    await expect(widget.getByText(/invalid|parameter|422/i).first()).toBeVisible();
    await expect(widget.locator('.ag-row[row-index="0"]').first()).toBeHidden();
    phase = "selected";
    await setIncomeSymbol(widget, "AAPL");
    observations.push(await verifyNativeIncome(widget, quarter, "AAPL", "quarter"));
    const refreshedResponse = page.waitForResponse(response => incomeQuery(response, "AAPL", "quarter"));
    await refreshIncome(widget);
    const refreshed = await refreshedResponse;
    expect(refreshed.status()).toBe(200);
    const freshQuarter = await refreshed.json();
    observations.push(await verifyNativeIncome(widget, freshQuarter, "AAPL", "quarter"));
    const programmatic = await page.request.get(refreshed.url());
    expect(programmatic.status()).toBe(200);
    const api = await programmatic.json();
    const apiMetadata = incomeMetadata(api, "AAPL", "quarter");
    expect(api.results).toEqual(freshQuarter.results);
    for (const key of ["effective_query", "source", "fields", "bounds"])
      expect(apiMetadata[key]).toEqual(observations.at(-1)!.metadata[key]);
    await widget.screenshot({ path: info.outputPath("packaged-native-quarter-income.png") });
    const saved = (await saveDashboard(page)).items[new URL(dashboardUrl).pathname.split("/").at(-1)!];
    expect(saved.data.widgets.find((item: any) => item.widgetId === widgetId).storage.params)
      .toMatchObject({ symbol: "AAPL", period: "quarter", provider: "fmp" });
    const context = await browser.newContext({ baseURL: process.env.WORKSPACE_FRONTEND_ORIGIN,
      serviceWorkers: "block", viewport: { width: 1600, height: 1000 } });
    try {
      const later = await context.newPage();
      trackIncome(later);
      const laterDiagnostics = await observeApplication(later);
      const reopenedResponse = later.waitForResponse(response => incomeQuery(response, "AAPL", "quarter"));
      await loginDisposableWorkspace(later);
      if (later.url() !== dashboardUrl) await later.goto(dashboardUrl);
      const reopened = await reopenedResponse;
      expect(reopened.status()).toBe(200);
      observations.push(await verifyNativeIncome(later.locator(`#workarea .widget-${widgetId}`).last(),
        await reopened.json(), "AAPL", "quarter"));
      expectApplicationDiagnostics(laterDiagnostics);
      await info.attach("reopened-financial-diagnostics", { contentType: "application/json", body: JSON.stringify(laterDiagnostics) });
    } finally { await context.close(); }
    expect(requests.filter(request => request.phase !== "invalid").length).toBeLessThanOrEqual(7);
    const expectedFailures = diagnostics.failures.filter(item => item.path === incomePath && item.status === 422);
    expect(expectedFailures.length).toBeGreaterThan(0);
    expect(expectedFailures.length).toBe(incomeFailures.length);
    for (const failure of incomeFailures) {
      expect(failure.status).toBe(422);
      if (failure.phase === "initial") expect([null, ""]).toContain(failure.symbol);
      else {
        expect(failure.phase).toBe("invalid");
        expect([null, ""]).toContain(failure.symbol);
      }
    }
    expectApplicationDiagnostics({ ...diagnostics,
      failures: diagnostics.failures.filter(item => !(item.path === incomePath && item.status === 422)),
      consoleErrors: diagnostics.consoleErrors.filter(item => !(item.path === incomePath && /Failed to load resource.*422/.test(item.message))),
    });
    await info.attach("packaged-financial-journey", { contentType: "application/json", body: JSON.stringify({
      images: runtime.images, release_image_verified: false, observations, invalid: { status: invalid.status(), code: failure.code },
      requests, incomeFailures, programmaticQueryCompared: true, diagnostics,
      limitation: "Local image acceptance; visible native currency/date/source plus API metadata, no metadata-pane or published-release claim",
    }) });
  } finally {
    await info.attach("packaged-financial-attempt", { contentType: "application/json", body: JSON.stringify({
      phase, requests, responses, diagnostics,
      limitation: "Allowlisted native income query fields and statuses; no authentication or raw API payloads",
    }) });
  }
});
