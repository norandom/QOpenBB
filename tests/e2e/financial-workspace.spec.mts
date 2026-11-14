import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { isAbsolute } from "node:path";
import { pathToFileURL } from "node:url";
import type { RuntimeDescriptor } from "../../verification/runtime-descriptor.ts";
import type { Locator, Page, Response } from "../../verification/node_modules/@playwright/test/index.js";
import { expectApplicationDiagnostics, observeApplication } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/diagnostics";
import { saveDashboard } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/editor";
import { expect, loginDisposableWorkspace, test } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/fixtures";

async function runtimeReader(): Promise<typeof import("../../verification/runtime-descriptor.ts")> {
  const reader = process.env.QOPENBB_RUNTIME_READER;
  if (!reader || !isAbsolute(reader)) throw new Error("Checked runtime reader required");
  return import(pathToFileURL(reader).href);
}

async function readRuntime(): Promise<RuntimeDescriptor> {
  const reader = await runtimeReader();
  return reader.readRuntimeDescriptor(process.env.WORKSPACE_RUNTIME_PRIVATE!);
}

const widgetId = "equity_fundamental_income_fmp_obb";
const incomePath = "/data/api/v1/equity/fundamental/income";

async function revenueCell(widget: Locator, field: string, rowIndex = 0) {
  const cell = widget.locator(`.ag-row[row-index="${rowIndex}"] [col-id="${field}"]`).first();
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

async function connectInstalledCatalog(page: Page, inspect?: (catalog: Record<string, any>) => void, appName = "QOpenBB starter") {
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
  const testBackend = dialog.getByRole("button", { name: "Test", exact: true });
  // The retained account keeps its connector between separate acceptance phases.
  const duplicateUrl = dialog.getByText('"Installed QOpenBB data API" is already using this URL', { exact: true });
  await expect.poll(async () => (await testBackend.isEnabled()) || (await duplicateUrl.isVisible())).toBe(true);
  const reuseConnection = await duplicateUrl.isVisible();
  let response: Pick<Response, "status" | "json">;
  if (reuseConnection) {
    await expect(dialog.getByText('A backend with the name "Installed QOpenBB data API" already exists', { exact: true })).toBeVisible();
    response = await page.request.get(`${process.env.WORKSPACE_FRONTEND_ORIGIN}/data/widgets.json`);
  } else {
    const catalog = page.waitForResponse(item => new URL(item.url()).pathname === "/data/widgets.json");
    await testBackend.click();
    response = await catalog;
  }
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
  if (reuseConnection) await dialog.getByRole("button", { name: "Close", exact: true }).click();
  else {
    await expect(dialog.getByText("Test successful", { exact: true })).toBeVisible();
    await dialog.getByRole("button", { name: /^add$/i }).click();
  }
  await expect(dialog).not.toBeVisible();
  await page.getByRole("link", { name: "Apps", exact: true }).click();
  const starter = page.getByRole("button").filter({
    has: page.getByText(appName, { exact: true }),
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
    period_basis: null,
    value_origin: "provider_observation",
  });
  statementMetadata(payload, period);
  return metadata;
}

function statementMetadata(payload: any, period: string) {
  const metadata = payload.extra.results_metadata.__qopenbb_financial__;
  expect(metadata.point_in_time_safe).toBe(false);
  expect(metadata.statement_provenance.version).toBe(1);
  const provenance = metadata.statement_provenance.rows;
  expect(provenance).toHaveLength(payload.results.length);
  expect(new Set(provenance.map((item: any) => item.source_ordinal)).size).toBe(provenance.length);
  for (const [index, row] of payload.results.entries()) {
    const item = provenance[index];
    expect(item).toMatchObject({ row_index: index, fiscal_year: Number(row.fiscal_year),
      fiscal_period: row.fiscal_period, period_end: row.period_ending, requested_frequency: period,
      flow_coverage: "unknown", period_start: null, duration_days: null,
      restatement_status: "unknown", conventions: [] });
    expect(item.source_ordinal).toBeGreaterThanOrEqual(0);
    expect(["unavailable", "conflicting"]).toContain(item.coverage_status);
    expect(item.facts).toEqual(expect.arrayContaining([
      { semantic_key: "period_end", source_field: "date", value: row.period_ending, presence: "value", evidence_kind: "observation" },
      { semantic_key: "fiscal_period", source_field: "period", value: row.fiscal_period, presence: "value", evidence_kind: "observation" },
    ]));
    for (const fact of item.facts) {
      expect(fact.evidence_kind).toBe("observation");
      expect(fact.presence).toBe(fact.value === null ? "null" : "value");
    }
    for (const [field, details] of Object.entries(metadata.fields) as [string, any][])
      if (details.period_basis === "instant")
        expect(item.instant_dates[field]).toBe(field === "cash_at_beginning_of_period" ? null : row.period_ending);
  }
  return metadata;
}

async function verifyNativeStatement(widget: Locator, payload: any, dataset: string, field: string, period: string) {
  const metadata = statementMetadata(payload, period);
  expect(metadata).toMatchObject({ dataset: `equity/fundamental/${dataset}`, provider: "fmp",
    effective_query: { symbol: "AAPL", period }, source: { endpoint: dataset === "balance" ? "balance-sheet-statement" : "cash-flow-statement" } });
  expect(metadata.fields[field]).toMatchObject({ unit: "currency", scale: 1, currency_field: "reported_currency",
    period_basis: dataset === "balance" ? "instant" : null, value_origin: "provider_observation" });
  const row = payload.results[0];
  expect(row).toMatchObject({ symbol: "AAPL", reported_currency: "USD" });
  expect(Number.isFinite(row[field])).toBe(true);
  await expect(widget.getByPlaceholder("Symbol", { exact: true })).toHaveValue("AAPL");
  await expect(widget.getByRole("button", { name: period, exact: true })).toBeVisible();
  await expect(await revenueCell(widget, "symbol")).toHaveText(row.symbol);
  await expect(await revenueCell(widget, "reported_currency")).toHaveText(row.reported_currency);
  const date = await revenueCell(widget, "period_ending");
  await expect.poll(async () => new Date(await date.innerText()).toISOString().slice(0, 10)).toBe(row.period_ending);
  await displayedNumber(await revenueCell(widget, field), row[field]);
  return { dataset, period, value: row[field], metadata };
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
  const runtime = await readRuntime();
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
  const statementInitialFailures: { path: string; symbol: string | null; status: number }[] = [];
  const statementRequests: { path: string; symbol: string | null; period: string | null }[] = [];
  const incomeFailures: { symbol: string | null; status: number; phase: string | undefined }[] = [];
  const trackIncome = (target: Page) => {
    target.on("request", request => {
      const url = new URL(request.url());
      if (url.pathname === incomePath) requests.push({ symbol: url.searchParams.get("symbol"),
        period: url.searchParams.get("period"), provider: url.searchParams.get("provider"), limit: url.searchParams.get("limit"), phase });
      if (["/data/api/v1/equity/fundamental/balance", "/data/api/v1/equity/fundamental/cash"].includes(url.pathname))
        statementRequests.push({ path: url.pathname, symbol: url.searchParams.get("symbol"), period: url.searchParams.get("period") });
      requestPhases.set(request, phase);
    });
    target.on("response", response => {
      const url = new URL(response.url());
      if (url.pathname === incomePath) responses.push({ symbol: url.searchParams.get("symbol"),
        period: url.searchParams.get("period"), status: response.status(), phase: requestPhases.get(response.request()) });
      if (["/data/api/v1/equity/fundamental/balance", "/data/api/v1/equity/fundamental/cash"].includes(url.pathname) && response.status() >= 400)
        statementInitialFailures.push({ path: url.pathname, symbol: url.searchParams.get("symbol"), status: response.status() });
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
    await widget.screenshot({ path: info.outputPath("packaged-native-quarter-income.png") });
    const statements = [
      { dataset: "balance", name: "Balance", field: "total_assets" },
      { dataset: "cash", name: "Cash", field: "net_cash_from_operating_activities" },
    ];
    const statementObservations: unknown[] = [];
    for (const statement of statements) {
      const id = `equity_fundamental_${statement.dataset}_fmp_obb`;
      const path = `/data/api/v1/equity/fundamental/${statement.dataset}`;
      const query = (response: Response, period: string) => companyQuery(response, path, "AAPL") &&
        new URL(response.url()).searchParams.get("period") === period;
      const panel = await addFinancialWidget(page, statement.name, id);
      await expect(panel.getByText("Invalid financial query parameters.", { exact: true })).toBeVisible();
      const annualResponse = page.waitForResponse(response => query(response, "annual"));
      await setIncomeSymbol(panel, "AAPL");
      const annualResult = await annualResponse;
      expect(annualResult.status()).toBe(200);
      statementObservations.push(await verifyNativeStatement(panel, await annualResult.json(), statement.dataset, statement.field, "annual"));
      const quarterlyResponse = page.waitForResponse(response => query(response, "quarter"));
      await panel.getByRole("button", { name: "annual", exact: true }).click();
      await page.locator(".obb-dropdown-container").getByText("quarter", { exact: true }).click();
      const quarterlyResult = await quarterlyResponse;
      expect(quarterlyResult.status()).toBe(200);
      statementObservations.push(await verifyNativeStatement(panel, await quarterlyResult.json(), statement.dataset, statement.field, "quarter"));
      const refreshResponse = page.waitForResponse(response => query(response, "quarter"));
      await refreshIncome(panel);
      const refreshResult = await refreshResponse;
      expect(refreshResult.status()).toBe(200);
      statementObservations.push(await verifyNativeStatement(panel, await refreshResult.json(), statement.dataset, statement.field, "quarter"));
    }
    const saved = (await saveDashboard(page)).items[new URL(dashboardUrl).pathname.split("/").at(-1)!];
    expect(saved.data.widgets.find((item: any) => item.widgetId === widgetId).storage.params)
      .toMatchObject({ symbol: "AAPL", period: "quarter", provider: "fmp" });
    for (const statement of statements)
      expect(saved.data.widgets.find((item: any) => item.widgetId === `equity_fundamental_${statement.dataset}_fmp_obb`).storage.params)
        .toMatchObject({ symbol: "AAPL", period: "quarter", provider: "fmp" });
    const context = await browser.newContext({ baseURL: process.env.WORKSPACE_FRONTEND_ORIGIN,
      serviceWorkers: "block", viewport: { width: 1600, height: 1000 } });
    try {
      const later = await context.newPage();
      trackIncome(later);
      const laterDiagnostics = await observeApplication(later);
      const reopenedResponse = later.waitForResponse(response => incomeQuery(response, "AAPL", "quarter"));
      const statementResponses = statements.map(statement => later.waitForResponse(response =>
        companyQuery(response, `/data/api/v1/equity/fundamental/${statement.dataset}`, "AAPL") &&
        new URL(response.url()).searchParams.get("period") === "quarter"));
      await loginDisposableWorkspace(later);
      if (later.url() !== dashboardUrl) await later.goto(dashboardUrl);
      const reopened = await reopenedResponse;
      expect(reopened.status()).toBe(200);
      observations.push(await verifyNativeIncome(later.locator(`#workarea .widget-${widgetId}`).last(),
        await reopened.json(), "AAPL", "quarter"));
      for (const [index, statement] of statements.entries()) {
        const panel = later.locator(`#workarea .widget-equity_fundamental_${statement.dataset}_fmp_obb`).last();
        await panel.scrollIntoViewIfNeeded();
        const response = await statementResponses[index];
        expect(response.status()).toBe(200);
        statementObservations.push(await verifyNativeStatement(panel, await response.json(), statement.dataset, statement.field, "quarter"));
      }
      expectApplicationDiagnostics(laterDiagnostics);
      await info.attach("reopened-financial-diagnostics", { contentType: "application/json", body: JSON.stringify(laterDiagnostics) });
    } finally { await context.close(); }
    expect(requests.filter(request => request.phase !== "invalid").length).toBeLessThanOrEqual(7);
    for (const dataset of ["balance", "cash"]) {
      const path = `/data/api/v1/equity/fundamental/${dataset}`;
      expect(statementRequests.filter(item => item.path === path && item.symbol === "AAPL")).toHaveLength(4);
    }
    for (const failure of statementInitialFailures) {
      expect(failure.status).toBe(422);
      expect([null, ""]).toContain(failure.symbol);
    }
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
      requestFailures: diagnostics.requestFailures.filter(item => !(item.path === searchPath && item.reason === "net::ERR_ABORTED")),
      failures: diagnostics.failures.filter(item => !([incomePath, "/data/api/v1/equity/fundamental/balance", "/data/api/v1/equity/fundamental/cash"].includes(item.path) && item.status === 422)),
      consoleErrors: diagnostics.consoleErrors.filter(item => !([incomePath, "/data/api/v1/equity/fundamental/balance", "/data/api/v1/equity/fundamental/cash"].includes(item.path) && /Failed to load resource.*422/.test(item.message))),
    });
    await info.attach("packaged-financial-journey", { contentType: "application/json", body: JSON.stringify({
      images: runtime.images, release_image_verified: false, observations, invalid: { status: invalid.status(), code: failure.code },
      requests, incomeFailures, statementRequests, statementInitialFailures, statementObservations, capturedNativeResponseCompared: true, diagnostics,
      limitation: "Local image acceptance; visible native currency/date/source plus API metadata, no metadata-pane or published-release claim",
    }) });
  } finally {
    await info.attach("packaged-financial-attempt", { contentType: "application/json", body: JSON.stringify({
      phase, requests, responses, statementRequests, statementInitialFailures, diagnostics,
      limitation: "Allowlisted native income query fields and statuses; no authentication or raw API payloads",
    }) });
  }
});

const profileId = "equity_profile_fmp_obb";
const fredId = "economy_fred_series_fred_obb";
const profilePath = "/data/api/v1/equity/profile";
const fredPath = "/data/api/v1/economy/fred_series";
const searchPath = "/data/api/v1/equity/search";

async function newFinancialDashboard(page: Page) {
  await page.locator("#tabs").getByRole("button").first().click();
  await page.getByRole("button", { name: /New Dashboard/ }).click();
  await expect(page).toHaveURL(/\/app\/[\da-f-]{36}$/);
  return page.url();
}

async function addFinancialWidget(page: Page, name: string, id: string) {
  const count = await page.locator(`#workarea .widget-${id}`).count();
  const emptyDashboardAdd = page.getByRole("main").getByRole("button", { name: "Add widgets", exact: true });
  if (await emptyDashboardAdd.isVisible()) await emptyDashboardAdd.click();
  else await page.getByTestId("dashboard-toolbar-add-widget-button").click();
  const dialog = page.getByRole("dialog");
  // Library search removes the duplicate Recently Added section.
  await dialog.getByPlaceholder("Search for widgets", { exact: true }).fill(name);
  const catalogChoice = dialog.getByText(name, { exact: true });
  await expect(catalogChoice).toHaveCount(1);
  await catalogChoice.click();
  await dialog.getByRole("button", { name: "Add widgets", exact: true }).click();
  const widgets = page.locator(`#workarea .widget-${id}`);
  await expect(widgets).toHaveCount(count + 1);
  return widgets.nth(count);
}

async function comparisonTerms(widget: Locator, value: string, label: string) {
  await widget.getByRole("button", { name: label, exact: true }).click();
  const input = widget.page().getByPlaceholder("Add search term", { exact: true });
  await input.fill(value);
  await input.press("Enter");
  await input.press("Escape");
}

async function symbolGroup(widget: Locator, create: boolean, name = "Group 1") {
  // Scope to Symbol: Income also retains independent Period/Limit group triggers.
  const host = widget.locator("[data-company-fields]");
  const trigger = host.locator("button._group-dropdown-trigger");
  if (!(await trigger.isVisible())) await widget.page().keyboard.press("Control+g");
  await trigger.click();
  if (create) await widget.page().getByRole("button", { name: "Create a group", exact: true }).click();
  else {
    const row = widget.page().locator(".group-dropdown").filter({
      has: widget.page().getByText(`${name}:`, { exact: true }),
    }).filter({ has: widget.page().getByTestId("group-row-checkbox") }).last();
    await row.getByTestId("group-row-checkbox").click();
  }
  await widget.page().keyboard.press("Escape");
}

function companyQuery(response: Response, path: string, symbol: string) {
  const url = new URL(response.url());
  return url.origin === process.env.WORKSPACE_FRONTEND_ORIGIN && url.pathname === path &&
    url.searchParams.get("symbol") === symbol && url.searchParams.get("provider") === (path === fredPath ? "fred" : "fmp");
}

async function chooseCompany(widget: Locator, mode: "name" | "symbol", query: string, symbol: string) {
  const page = widget.page();
  const response = page.waitForResponse(item => {
    const url = new URL(item.url());
    return url.pathname === searchPath && url.searchParams.get("query") === query &&
      url.searchParams.get("is_symbol") === String(mode === "symbol");
  });
  await widget.getByRole("combobox", { name: mode === "name" ? "Company name" : "Symbol", exact: true }).fill(query);
  const search = await response;
  expect(search.status()).toBe(200);
  return selectCompanyListing(widget, mode, query, symbol, await search.json());
}

async function selectCompanyListing(widget: Locator, mode: "name" | "symbol", query: string, symbol: string, payload: any, beforeChoose?: () => Promise<void>) {
  const page = widget.page();
  const metadata = payload.extra.results_metadata.__qopenbb_financial__;
  expect(metadata).toMatchObject({ dataset: "equity/search", provider: "fmp",
    source: { endpoint: mode === "name" ? "search-name" : "search-symbol" },
    effective_query: { query, limit: 20 } });
  expect(Number.isFinite(Date.parse(metadata.retrieved_at))).toBe(true);
  const matches = payload.results.filter((row: any) => row.symbol === symbol);
  expect(matches).toHaveLength(1);
  const listing = matches[0];
  expect(typeof listing.name).toBe("string");
  if (mode === "symbol" && query !== symbol) {
    // Read suggestions after the real raw-symbol acknowledgement, rather than racing its timer.
    await expect.poll(async () => (await widget.getByRole("status").allTextContents()).some(text =>
      text.includes(`Current Symbol: ${query}.`) || text.includes(`(${query}).`),
    )).toBe(true);
  }
  const option = page.getByRole("listbox").getByRole("option").filter({
    hasText: `${listing.name} (${symbol})`,
  });
  await expect(option).toHaveCount(1);
  await expect(option).toContainText("fmp");
  for (const field of ["exchange", "exchange_short_name", "currency"])
    if (listing[field]) await expect(option).toContainText(listing[field]);
  await beforeChoose?.();
  await option.click();
  await expectSelectedCompany(widget, listing);
  return { listing, retrievedAt: metadata.retrieved_at };
}

async function expectSelectedCompany(widget: Locator, listing: any) {
  // The loading shell has the same widget selector; wait for the actual table before scrolling.
  await expect(widget.getByRole("grid")).toBeVisible();
  await widget.scrollIntoViewIfNeeded();
  await expect(widget.getByRole("combobox", { name: "Company name", exact: true })).toHaveValue(listing.name);
  await expect(widget.getByRole("combobox", { name: "Symbol", exact: true })).toHaveValue(listing.symbol);
  await expect(widget.getByRole("status").filter({ hasText: "Current company:" }))
    .toContainText(`Current company: ${listing.name} (${listing.symbol}).`);
}

async function displayedNumber(cell: Locator, amount: number) {
  // Allow grid-edge rounding while requiring nearly the entire amount cell on screen.
  await expect(cell).toBeInViewport({ ratio: 0.99 });
  await expect.poll(async () => {
    const text = (await cell.innerText()).replace(/[,\s$]/g, "").toUpperCase();
    const match = /^(-?\d+(?:\.(\d+))?)([KMBT])?$/.exec(text);
    if (!match) return false;
    const scale = ({ K: 1e3, M: 1e6, B: 1e9, T: 1e12 } as Record<string, number>)[match[3]] ?? 1;
    return Math.abs(Number(match[1]) * scale - amount) <= scale * 10 ** -(match[2]?.length ?? 0) / 2 + Number.EPSILON * Math.abs(amount);
  }).toBe(true);
}

async function verifyNativeProfile(widget: Locator, payload: any, symbol: string) {
  const row = payload.results.find((item: any) => item.symbol === symbol);
  expect(row).toBeDefined();
  expect(row.currency).toBe("USD");
  const metadata = payload.extra.results_metadata.__qopenbb_financial__;
  expect(metadata).toMatchObject({ dataset: "equity/profile", provider: "fmp",
    effective_query: { symbol }, point_in_time_safe: false });
  expect(Number.isFinite(Date.parse(metadata.retrieved_at))).toBe(true);
  expect(Number.isFinite(row.last_price)).toBe(true);
  await widget.scrollIntoViewIfNeeded();
  await expect(await revenueCell(widget, "symbol")).toHaveText(symbol);
  await expect(await revenueCell(widget, "name")).toHaveText(row.name);
  await expect(await revenueCell(widget, "currency")).toHaveText(row.currency);
  await displayedNumber(await revenueCell(widget, "last_price"), row.last_price);
  return { row, metadata };
}

async function verifyFredSentinel(widget: Locator, payload: any) {
  await widget.scrollIntoViewIfNeeded();
  const date = await revenueCell(widget, "date");
  const displayedDate = new Date(await date.innerText()).toISOString().slice(0, 10);
  const row = payload.results.find((item: any) => item.date.slice(0, 10) === displayedDate);
  expect(row, "visible FRED date identifies its actual response observation").toBeDefined();
  if (row.GDP === null) await expect(await revenueCell(widget, "GDP")).toHaveText("-");
  // GDP starts with missing 1946 observations; keep those missing and inspect an observed value.
  for (const observationDate of await widget.locator('.ag-row [col-id="date"]').all()) {
    const dateKey = new Date(await observationDate.innerText()).toISOString().slice(0, 10);
    const observation = payload.results.find((item: any) => item.date.slice(0, 10) === dateKey);
    if (!Number.isFinite(observation?.GDP)) continue;
    const index = await observationDate.evaluate(element => element.closest(".ag-row")?.getAttribute("row-index"));
    expect(index).toMatch(/^\d+$/);
    await observationDate.scrollIntoViewIfNeeded();
    await expect(observationDate).toBeInViewport();
    await displayedNumber(await revenueCell(widget, "GDP", Number(index)), observation.GDP);
    return;
  }
  throw new Error("No finite FRED GDP observation was rendered for visible-value verification.");
}

function selectionState(content: any) {
  return { groups: content.data.groups, gridLayout: content.data.gridLayout,
    widgets: content.data.widgets.map((widget: any) => ({ id: widget.id, widgetId: widget.widgetId,
      paramGroups: widget.paramGroups, params: widget.storage.params, selection: widget.storage.companySelection, research: widget.storage.companyResearch })) };
}

async function readFinancialDashboard(page: Page, url: string) {
  const read = page.waitForResponse(response => response.request().method() === "GET" &&
    new URL(response.url()).pathname.endsWith("/pro/dash/validate-and-sync"));
  await page.goto(url);
  const response = await read;
  expect(response.ok()).toBe(true);
  return (await response.json()).owned[new URL(url).pathname.split("/").at(-1)!].content;
}

function allowFinancialInitializationAndCancellation(diagnostics: Awaited<ReturnType<typeof observeApplication>>) {
  const paths = [profilePath, incomePath, fredPath];
  // Empty Symbol requests and cancelled navigation/superseded lookups precede settled value assertions.
  return { ...diagnostics,
    failures: diagnostics.failures.filter(item => !(paths.includes(item.path) && item.status === 422)),
    consoleErrors: diagnostics.consoleErrors.filter(item => !(paths.includes(item.path ?? "") && /Failed to load resource.*422/.test(item.message))),
    requestFailures: diagnostics.requestFailures.filter(item => !([searchPath, ...paths].includes(item.path) && item.reason === "net::ERR_ABORTED")),
  };
}

test("real FMP company name MSFT then symbol AAPL linked research survives fresh login and retained recreation", async ({ page, browser }, info) => {
  test.setTimeout(360000);
  const phase = process.env.QOPENBB_COMPANY_PHASE;
  const checkpoint = process.env.QOPENBB_COMPANY_RETENTION;
  if (!checkpoint || !["initial", "reopen"].includes(phase ?? ""))
    throw Error("Explicit QOPENBB_COMPANY_PHASE initial|reopen and QOPENBB_COMPANY_RETENTION required");
  (await runtimeReader()).checkpointPath(checkpoint);
  if (phase === "initial") {
    // Refuse to overwrite a checkpoint from a previously completed journey.
    expect(existsSync(checkpoint)).toBe(false);
  }
  const runtime = await readRuntime();
  expect(runtime.name).toMatch(/^qopenbb-browser-/);
  expect(runtime.packaged_image_only).toBe(true);
  expect(runtime.source_overlay).toBeNull();
  const diagnostics = [await observeApplication(page)];
  const captures: { path: string; symbol: string; payload: any }[] = [];
  const bodyReadFailures: { path: string; symbol: string; reason: string | null }[] = [];
  const reads: Promise<void>[] = [];
  const financialRequests: { path: string; symbol: string; keys: string[] }[] = [];
  const initialFailures: { path: string; symbol: string | null }[] = [];
  const observeFinancial = (target: Page) => {
    target.on("request", request => {
      const url = new URL(request.url());
      if (![profilePath, incomePath, fredPath].includes(url.pathname)) return;
      financialRequests.push({ path: url.pathname, symbol: url.searchParams.get("symbol") ?? "", keys: [...url.searchParams.keys()] });
    });
    target.on("response", response => {
      const url = new URL(response.url());
      if ([profilePath, incomePath, fredPath].includes(url.pathname) && response.status() === 422)
        initialFailures.push({ path: url.pathname, symbol: url.searchParams.get("symbol") });
      if (![profilePath, incomePath, fredPath].includes(url.pathname) || !response.ok()) return;
      const read = response.json().then(payload => { captures.push({ path: url.pathname, symbol: url.searchParams.get("symbol") ?? "", payload }); }).catch(error => {
        const failure = response.request().failure();
        bodyReadFailures.push({ path: url.pathname, symbol: url.searchParams.get("symbol") ?? "", reason: failure?.errorText ?? null });
        // Superseded requests can lose their bodies; every unconfirmed or non-owned failure still rejects.
        if (url.origin !== process.env.WORKSPACE_FRONTEND_ORIGIN || failure?.errorText !== "net::ERR_ABORTED") throw error;
      });
      reads.push(read);
      void read.catch(() => undefined);
    });
  };
  observeFinancial(page);
  const captured = async (path: string, symbol: string) => {
    await expect.poll(() => captures.some(item => item.path === path && item.symbol === symbol)).toBe(true);
    return captures.findLast(item => item.path === path && item.symbol === symbol)!.payload;
  };
  let dashboardUrl = "";
  let expected: any;
  let selected: any;
  const records: unknown[] = [];
  try {
    await loginDisposableWorkspace(page);
    if (phase === "initial") {
      await connectInstalledCatalog(page);
      dashboardUrl = await newFinancialDashboard(page);
      const profile = await addFinancialWidget(page, "Profile", profileId);
      const income = await addFinancialWidget(page, "Income", widgetId);
      const comparison = await addFinancialWidget(page, "Profile", profileId);
      const fred = await addFinancialWidget(page, "Fred Series", fredId);
      await setIncomeSymbol(profile, "AAPL");
      await setIncomeSymbol(income, "AAPL");
      await setIncomeSymbol(comparison, "AAPL");
      await comparisonTerms(comparison, "MSFT", "AAPL");
      await expect(comparison.getByText("Multiple companies:", { exact: false })).toBeVisible();
      await expect(comparison.getByRole("button", { name: "Symbol (2)", exact: true })).toBeVisible();
      await comparisonTerms(fred, "GDP", "Symbol");
      await expect(await revenueCell(fred, "GDP")).toBeVisible();
      await symbolGroup(profile, true);
      await symbolGroup(income, false);
      await symbolGroup(comparison, true, "Group 2");
      const baseline = (await saveDashboard(page)).items[new URL(dashboardUrl).pathname.split("/").at(-1)!];
      const comparisonStored = baseline.data.widgets.filter((widget: any) => widget.widgetId === profileId)[1];
      const fredStored = baseline.data.widgets.find((widget: any) => widget.widgetId === fredId);
      const sentinelRequests = financialRequests.filter(item => item.path === fredPath || item.path === profilePath && item.symbol.includes(",")).length;
      // AAPL's exact lookup was cached during setup; exercise prefix autocomplete with a fresh query.
      for (const [mode, query, symbol] of [["name", "Microsoft", "MSFT"], ["symbol", "AAP", "AAPL"]] as const) {
        selected = await chooseCompany(profile, mode, query, symbol);
        await expectSelectedCompany(income, selected.listing);
        const profileData = await captured(profilePath, symbol);
        const incomeData = await captured(incomePath, symbol);
        const displayed = await verifyNativeProfile(profile, profileData, symbol);
        const statement = await verifyNativeIncome(income, incomeData, symbol, "annual");
        await displayedNumber(await revenueCell(income, "revenue"), statement.row.revenue);
        await expect(comparison.getByRole("combobox", { name: "Symbol", exact: true })).toHaveValue("AAPL,MSFT");
        await expect(comparison.getByRole("button", { name: "Symbol (2)", exact: true })).toBeVisible();
        const fredPayload = await captured(fredPath, "GDP");
        await verifyFredSentinel(fred, fredPayload);
        const saved = (await saveDashboard(page)).items[new URL(dashboardUrl).pathname.split("/").at(-1)!];
        const pair = saved.data.widgets.filter((widget: any) => widget.id !== comparisonStored.id && [profileId, widgetId].includes(widget.widgetId));
        expect(pair).toHaveLength(2);
        expect(pair[0].paramGroups.symbol).toBe(pair[1].paramGroups.symbol);
        expect(pair[0].paramGroups.symbol).not.toBe(comparisonStored.paramGroups.symbol);
        for (const widget of pair) {
          expect(widget.storage.params.symbol).toBe(symbol);
          expect(widget.storage.params).not.toHaveProperty("companySelection");
          expect(widget.storage.companySelection).toMatchObject({ version: 1, provider: "fmp", symbol,
            name: selected.listing.name, exchange: selected.listing.exchange ?? null,
            exchangeShortName: selected.listing.exchange_short_name ?? null, currency: selected.listing.currency ?? null,
            listingId: selected.listing.listing_id ?? null, issuerId: selected.listing.issuer_id ?? null });
          const [sourceId, prefix] = JSON.parse(widget.storage.companySelection.sourceKey);
          expect(sourceId).toBeTruthy();
          expect(prefix).toBe(`${process.env.WORKSPACE_FRONTEND_ORIGIN}/data`);
        }
        expect(saved.data.widgets.find((widget: any) => widget.id === comparisonStored.id).storage.params).toEqual(comparisonStored.storage.params);
        expect(saved.data.widgets.find((widget: any) => widget.id === fredStored.id).storage.params).toEqual(fredStored.storage.params);
        expect(saved.data.groups.find((group: any) => group.id === comparisonStored.paramGroups.symbol))
          .toEqual(baseline.data.groups.find((group: any) => group.id === comparisonStored.paramGroups.symbol));
        expected = selectionState(saved);
        records.push({ mode, query, symbol, selected, profile: displayed, income: statement });
      }
      expect(financialRequests.filter(item => item.path === fredPath || item.path === profilePath && item.symbol.includes(","))).toHaveLength(sentinelRequests);
      // One settled pair; no extra screenshots of transient search or authentication.
      await profile.scrollIntoViewIfNeeded();
      for (const theme of ["light", "dark"]) {
        const dark = (await page.locator("html").getAttribute("class"))?.split(" ").includes("dark");
        if (dark !== (theme === "dark")) {
          const themeSaved = page.waitForResponse(response => {
            const url = new URL(response.url());
            return url.origin === process.env.WORKSPACE_FRONTEND_ORIGIN &&
              url.pathname === "/api/pro/display-settings" && response.request().method() === "POST" &&
              response.request().postDataJSON()?.theme === theme;
          });
          await page.keyboard.press("Control+m");
          expect((await themeSaved).ok()).toBe(true);
        }
        await expect(page.locator("html")).toHaveClass(theme === "dark" ? /\bdark\b/ : /^(?!.*\bdark\b)/);
        await expectSelectedCompany(profile, selected.listing);
        await profile.screenshot({ path: info.outputPath(`company-selector-${theme}.png`) });
      }
    } else {
      const previous = JSON.parse(readFileSync(checkpoint, "utf8"));
      expect(previous.stage).toBe("initial-complete");
      expect(previous.images).toEqual(runtime.images);
      expect(previous.runtimeName).toBe(runtime.name);
      expect(previous.containerId).not.toBe(runtime.container);
      expect(previous.containerId).toBeTruthy();
      expect(runtime.container).toBeTruthy();
      dashboardUrl = `${process.env.WORKSPACE_FRONTEND_ORIGIN}${previous.dashboardPath}`;
      expected = previous.state;
      selected = previous.selected;
      expect(selectionState(await readFinancialDashboard(page, dashboardUrl))).toEqual(expected);
    }
    await Promise.all(reads);
    captures.length = 0;
    const context = await browser.newContext({ baseURL: process.env.WORKSPACE_FRONTEND_ORIGIN,
      serviceWorkers: "block", viewport: { width: 1600, height: 1000 } });
    try {
      const reopened = await context.newPage();
      diagnostics.push(await observeApplication(reopened));
      observeFinancial(reopened);
      await loginDisposableWorkspace(reopened);
      expect(selectionState(await readFinancialDashboard(reopened, dashboardUrl))).toEqual(expected);
      const profile = reopened.locator(`#workarea .widget-${profileId}`).first();
      const income = reopened.locator(`#workarea .widget-${widgetId}`);
      await expectSelectedCompany(profile, selected.listing);
      await expectSelectedCompany(income, selected.listing);
      await verifyNativeProfile(profile, await captured(profilePath, "AAPL"), "AAPL");
      await verifyNativeIncome(income, await captured(incomePath, "AAPL"), "AAPL", "annual");
      await expect(reopened.locator(`#workarea .widget-${profileId}`).nth(1)
        .getByRole("button", { name: "Symbol (2)", exact: true })).toBeVisible();
      const fred = reopened.locator(`#workarea .widget-${fredId}`);
      const savedFred = expected.widgets.filter((widget: any) => widget.widgetId === fredId);
      expect(savedFred).toHaveLength(1);
      // Offscreen widgets fetch when revealed; the persisted layout item survives table mounting.
      await reopened.locator(`#workarea [data-widget-id="${savedFred[0].id}"]`).scrollIntoViewIfNeeded();
      await expect(fred.getByRole("grid")).toBeVisible();
      await verifyFredSentinel(fred, await captured(fredPath, "GDP"));
      await Promise.all(reads);
      records.push({ stage: phase === "reopen" ? "fresh-login-after-controller-recreation" : "fresh-login-after-save" });
    } finally { await context.close(); }
    await Promise.all(reads);
    for (const request of financialRequests) {
      const allowed = request.path === profilePath ? ["symbol", "provider"] : request.path === incomePath ?
        ["symbol", "provider", "period", "limit"] : ["symbol", "provider", "start_date", "end_date", "limit", "frequency", "aggregation_method", "transform", "use_cache"];
      expect(request.keys.filter(key => !allowed.includes(key)), "selection metadata cannot enter financial query parameters").toEqual([]);
    }
    for (const failure of initialFailures) expect([null, ""]).toContain(failure.symbol);
    for (const diagnostic of diagnostics) expectApplicationDiagnostics(allowFinancialInitializationAndCancellation(diagnostic));
    if (phase === "initial") writeFileSync(checkpoint, `${JSON.stringify({ stage: "initial-complete",
      images: runtime.images, runtimeName: runtime.name, containerId: runtime.container,
      dashboardPath: new URL(dashboardUrl).pathname, selected, state: expected }, null, 2)}\n`, { flag: "wx" });
  } finally {
    await info.attach("company-selector-real-financial-journey", { contentType: "application/json",
      body: JSON.stringify({ phase, images: runtime.images, records, financialRequests, initialFailures, bodyReadFailures, diagnostics,
        limitation: "Actual local packaged FMP/FRED responses required; controller recreates retained bind between phases. Discovery alone is not execution or publication acceptance." }) });
  }
});

test("synthetic company keyboard cancel entitlement failure and stale search cannot relabel committed data", async ({ page }, info) => {
  test.setTimeout(180000);
  const diagnostics = await observeApplication(page);
  const searches: string[] = [];
  const financialSymbols: string[] = [];
  let inTestDashboard = false;
  const listings = {
    AAPL: { symbol: "AAPL", name: "Synthetic Apple", exchange: "NASDAQ", exchange_short_name: "NASDAQ",
      currency: "USD", listing_id: "fmp:AAPL:NASDAQ", issuer_id: null },
    MSFT: { symbol: "MSFT", name: "Synthetic Microsoft", exchange: "NASDAQ", exchange_short_name: "NASDAQ",
      currency: "USD", listing_id: "fmp:MSFT:NASDAQ", issuer_id: null },
  };
  const envelope = (url: URL, results: unknown[]) => ({ results, extra: { results_metadata: {
    __qopenbb_financial__: { dataset: "equity/search", provider: "fmp", retrieved_at: "2026-10-30T10:00:00Z",
      effective_query: { query: url.searchParams.get("query"), limit: 20 },
      source: { endpoint: url.searchParams.get("is_symbol") === "true" ? "search-symbol" : "search-name" } },
  } } });
  let releaseOld!: () => void;
  const oldReleased = new Promise<void>(resolve => { releaseOld = resolve; });
  let oldStarted!: () => void;
  const oldRequest = new Promise<void>(resolve => { oldStarted = resolve; });
  let oldFinished!: () => void;
  const oldCompletion = new Promise<void>(resolve => { oldFinished = resolve; });
  await page.route(`**${incomePath}*`, route => {
    const symbol = new URL(route.request().url()).searchParams.get("symbol") ?? "";
    if (inTestDashboard) financialSymbols.push(symbol);
    return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({
      results: symbol ? [{ symbol, reported_currency: "USD", period_ending: "2025-12-31", fiscal_period: "FY", revenue: symbol === "MSFT" ? 2000000 : 1000000 }] : [],
    }) });
  });
  await page.route(`**${searchPath}*`, async route => {
    const url = new URL(route.request().url());
    const query = url.searchParams.get("query") ?? "";
    if (inTestDashboard) searches.push(query);
    if (query === "Denied") return route.fulfill({ status: 403, contentType: "application/json",
      body: JSON.stringify({ code: "entitlement", detail: "Synthetic source access failure" }) });
    if (query === "Old") {
      oldStarted();
      await oldReleased;
      try { await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(envelope(url, [listings.MSFT])) }); }
      finally { oldFinished(); }
      return;
    }
    const result = query === "Nothing" ? [] : /Apple|AAPL/.test(query) ? [listings.AAPL] : [listings.MSFT];
    return route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(envelope(url, result)) });
  });
  try {
    await loginDisposableWorkspace(page);
    await connectInstalledCatalog(page);
    await newFinancialDashboard(page);
    inTestDashboard = true;
    const widget = await addFinancialWidget(page, "Income", widgetId);
    // The startup fallback is replaced; edit the settled native empty-data control.
    await expect(widget.getByText("No results found", { exact: true })).toBeVisible();
    await setIncomeSymbol(widget, "AAPL");
    await expectSelectedCompany(widget, listings.AAPL);
    const name = widget.getByRole("combobox", { name: "Company name", exact: true });
    await name.fill("Microsoft");
    const option = page.getByRole("option", { name: /Synthetic Microsoft \(MSFT\)/ });
    await expect(option).toBeVisible();
    await expect(name).toHaveAttribute("aria-expanded", "true");
    await name.press("Tab");
    await expect(widget.getByRole("combobox", { name: "Symbol", exact: true })).toHaveValue("AAPL");
    expect(financialSymbols.filter(symbol => symbol === "MSFT")).toEqual([]);
    await name.fill("Microsoft");
    await expect(option).toBeVisible();
    await name.press("ArrowDown");
    await expect(option).toHaveAttribute("aria-selected", "true");
    await expect(name).toHaveAttribute("aria-activedescendant", await option.getAttribute("id") as string);
    await name.press("Escape");
    await expectSelectedCompany(widget, listings.AAPL);
    await name.fill("Microsoft");
    await expect(option).toBeVisible();
    await name.press("ArrowDown");
    await name.press("Enter");
    await expectSelectedCompany(widget, listings.MSFT);
    await expect(await revenueCell(widget, "symbol")).toHaveText("MSFT");
    await displayedNumber(await revenueCell(widget, "revenue"), 2000000);
    await name.fill("Denied");
    await expect(widget.getByRole("status")).toContainText("Company search is unavailable with this source's current access.");
    await expect(widget.getByRole("status")).toContainText("Current company: Synthetic Microsoft (MSFT).");
    await expect(widget.getByRole("combobox", { name: "Symbol", exact: true })).toHaveValue("MSFT");
    await expect(await revenueCell(widget, "symbol")).toHaveText("MSFT");
    await name.press("Escape");
    await expectSelectedCompany(widget, listings.MSFT);
    await name.fill("Nothing");
    await expect(widget.getByRole("status")).toContainText("No matching companies.");
    await expect(page.getByRole("option")).toHaveCount(0);
    await name.fill("Old");
    await oldRequest;
    await name.fill("Apple");
    const apple = page.getByRole("option", { name: /Synthetic Apple \(AAPL\)/ });
    await expect(apple).toBeVisible();
    await name.press("ArrowDown");
    await name.press("Enter");
    await expectSelectedCompany(widget, listings.AAPL);
    releaseOld();
    await oldCompletion;
    await expectSelectedCompany(widget, listings.AAPL);
    await expect(await revenueCell(widget, "symbol")).toHaveText("AAPL");
    await displayedNumber(await revenueCell(widget, "revenue"), 1000000);
    expect(searches.filter(query => query === "Denied")).toHaveLength(1);
    const expectedFailures = diagnostics.failures.filter(item => item.path === searchPath && item.status === 403);
    expect(expectedFailures).toHaveLength(1);
    expectApplicationDiagnostics({ ...diagnostics,
      failures: diagnostics.failures.filter(item => !(item.path === searchPath && item.status === 403)),
      consoleErrors: diagnostics.consoleErrors.filter(item => !(item.path === searchPath && /Failed to load resource.*403/.test(item.message))),
      requestFailures: diagnostics.requestFailures.filter(item => !(item.path === searchPath && item.reason === "net::ERR_ABORTED")),
    });
  } finally {
    releaseOld();
    await info.attach("synthetic-company-keyboard-failure-race", { contentType: "application/json",
      body: JSON.stringify({ source: "Synthetic intercepted search and financial values; no live provider acceptance",
        searches, financialSymbols, diagnostics }) });
  }
});

// Live observations remain private; attachments contain selected financial facts only.
test("Company Research real FMP analyst choices template portability and retained recreation", async ({ page, browser }, info) => {
  test.setTimeout(600000);
  const phase = process.env.QOPENBB_COMPANY_PHASE;
  expect(["initial", "reopen"]).toContain(phase);
  const checkpoint = process.env.QOPENBB_COMPANY_RETENTION!;
  expect(isAbsolute(checkpoint)).toBe(true);
  const runtime = await readRuntime();
  (await runtimeReader()).checkpointPath(checkpoint);
  expect(runtime.packaged_image_only).toBe(true);
  expect(runtime.source_overlay).toBeNull();
  const diagnostics = [await observeApplication(page)];
  const captures: { url: URL; payload: any; requestIndex: number; source: "live" | "deterministic" }[] = [];
  const requestIndices = new WeakMap<object, number>();
  const syntheticRequests = new WeakSet<object>();
  const expected503 = new Set<object>();
  const expectedConsole503 = new Set<object>();
  const reads: Promise<void>[] = [];
  const facts: unknown[] = [];
  const syncReads = new WeakMap<Page, Promise<any>[]>();
  const syncAccess = new WeakMap<Page, { url: string; authorization?: string }>();
  const responseLifecycle: { requestIndex: number; path: string; state: "requested" | "headers" | "finished" | "failed";
    read: "not-started" | "pending" | "resolved" | "not-successful" | "failed"; source: "live" | "deterministic";
    demandedByCaptured: boolean; status?: number; failure?: "aborted" | "transport" }[] = [];
  const captureDemands: { path: string; symbol: string; period: string | null; after: number;
    source: "live" | "deterministic"; matchedRequestIndex: number | null }[] = [];
  const requestEstimate = {
    status: "static normal-path estimate, not measured receipts", cumulativeCeiling: { fmp: 320, fred: 0 },
    initial: { measuredPriorPrefixPlanningAllowance: 20, peerSearchAndInitial: 6, priceEdits: 2, statementQuarter: 3, peerQuarter: 4,
      deterministicRawRefreshes: 0, syntheticFailureUnaffectedLive: 3, recoveryRefresh: 4, exportedImport: 9,
      foreignImportAndReopenPeers: 8, explicitRecovery: 10, freshLoginSingleHydration: 9 },
    retainedReopen: { singleHydration: 9 }, plannedContinuation: 87, priorCumulative: 202, remaining: 118, headroom: 31,
    conditions: "Exact intended-dashboard login landing reuses successful sync; other landing navigates once. Search expiry and legitimate retries consume headroom.",
    loginCounts: { initialTest: 2, retainedReopenTest: 1, excludesControllerReadiness: true },
    accounting: "External cumulative ledger counts actual send reservations including retry=1; exhaustion fails/incompletes acceptance without raising the ceiling.",
  };
  const requests: { path: string; query: Record<string, string> }[] = [];
  const primaryIds = [profileId, widgetId, "equity_fundamental_balance_fmp_obb", "equity_fundamental_cash_fmp_obb", "equity_price_historical_fmp_obb"];
  function observe(target: Page) {
    const successfulSyncs: Promise<any>[] = [];
    syncReads.set(target, successfulSyncs);
    target.on("response", response => {
      if (new URL(response.url()).origin === process.env.WORKSPACE_FRONTEND_ORIGIN &&
        response.request().method() === "GET" && response.ok() &&
        new URL(response.url()).pathname.endsWith("/pro/dash/validate-and-sync")) {
        if (!syncAccess.has(target)) syncAccess.set(target, {
          url: response.url(), authorization: response.request().headers().authorization,
        });
      }
    });
    target.on("request", request => {
      const url = new URL(request.url());
      if (url.origin !== process.env.WORKSPACE_FRONTEND_ORIGIN || !url.pathname.startsWith("/data/api/")) return;
      const query = Object.fromEntries(url.searchParams);
      requestIndices.set(request, requests.length);
      responseLifecycle.push({ requestIndex: requests.length, path: url.pathname, state: "requested", read: "not-started",
        source: "live", demandedByCaptured: false });
      requests.push({ path: url.pathname, query });
      expect(query.provider).toBe("fmp");
      if (url.pathname === searchPath) {
        expect(["Microsoft", "Oracle", "Apple", "AAPL", "MSFT", "ORCL"]).toContain(query.query);
        expect(query.limit).toBe("20");
      } else {
        expect(["AAPL", "MSFT", "ORCL"]).toContain(query.symbol);
        if (url.pathname.includes("/fundamental/")) expect(query.limit).toBe("3");
        if (/metrics|ratios/.test(url.pathname)) expect(query.ttm).toBe("exclude");
        if (url.pathname.endsWith("/price/historical")) {
          // SingleDatePicker applies each endpoint immediately: the middle pair is unavoidable UI state.
          expect(["2025-01-02/2025-01-31", "2025-01-03/2025-01-31", "2025-01-03/2025-01-30"])
            .toContain(`${query.start_date}/${query.end_date}`);
        }
      }
    });
    target.on("response", response => {
      const url = new URL(response.url());
      if (url.origin !== process.env.WORKSPACE_FRONTEND_ORIGIN || !url.pathname.startsWith("/data/api/")) return;
      const state = responseLifecycle[requestIndices.get(response.request())!];
      state.state = "headers";
      state.status = response.status();
      state.source = syntheticRequests.has(response.request()) ? "deterministic" : "live";
      if (response.status() === 503) expect(syntheticRequests.has(response.request()), "unexpected real HTTP 503").toBe(true);
    });
    target.on("requestfailed", request => {
      const index = requestIndices.get(request);
      if (index === undefined) return;
      const state = responseLifecycle[index];
      state.state = "failed";
      state.source = syntheticRequests.has(request) ? "deterministic" : "live";
      state.failure = /ERR_ABORTED|NS_BINDING_ABORTED/.test(request.failure()?.errorText ?? "") ? "aborted" : "transport";
    });
    // Headers may precede cancellation; only a completed transport owns a body read.
    target.on("requestfinished", request => {
      const url = new URL(request.url());
      if (url.origin !== process.env.WORKSPACE_FRONTEND_ORIGIN) return;
      const financial = url.pathname.startsWith("/data/api/");
      const sync = request.method() === "GET" && url.pathname.endsWith("/pro/dash/validate-and-sync");
      if (!financial && !sync) return;
      const index = requestIndices.get(request);
      const state = index === undefined ? undefined : responseLifecycle[index];
      if (state) { state.state = "finished"; state.read = "pending"; }
      const read = request.response().then(async response => {
        expect(response, "Finished request requires response evidence").not.toBeNull();
        if (!response!.ok()) { if (state) state.read = "not-successful"; return undefined; }
        const payload = await response!.json();
        if (financial) {
          expect(index).toBeDefined();
          const source = syntheticRequests.has(request) ? "deterministic" : "live";
          captures.push({ url, payload, requestIndex: index!, source });
          state!.read = "resolved";
          state!.source = source;
        }
        return payload;
      }).catch(() => {
        if (state) state.read = "failed";
        throw new Error(`Completed response body read failed: ${url.pathname}; request ${index ?? "sync"}`);
      });
      if (financial) reads.push(read);
      else successfulSyncs.push(read);
      void read.catch(() => undefined);
    });
  }
  observe(page);
  async function captured(path: string, symbol: string, period?: string, after = 0, source: "live" | "deterministic" = "live") {
    const demand: typeof captureDemands[number] = { path, symbol, period: period ?? null, after, source, matchedRequestIndex: null };
    captureDemands.push(demand);
    const match = (item: typeof captures[number]) => item.requestIndex >= after && item.source === source && item.url.pathname === path && item.url.searchParams.get("symbol") === symbol &&
      (!period || item.url.searchParams.get("period") === period);
    await expect.poll(() => captures.some(match)).toBe(true);
    const selected = captures.findLast(match)!;
    demand.matchedRequestIndex = selected.requestIndex;
    responseLifecycle[selected.requestIndex].demandedByCaptured = true;
    return selected.payload;
  }
  const widget = (target: Page, id: string) => target.locator(`#workarea .widget-${id}`).first();
  async function readResearchDashboard(target: Page, url: string) {
    if (target.url() !== url) return readFinancialDashboard(target, url);
    const id = new URL(url).pathname.split("/").at(-1)!;
    let content: any;
    await expect.poll(async () => {
      const successful = await Promise.all(syncReads.get(target) ?? []);
      content = successful.findLast(item => item?.owned?.[id]?.content)?.owned[id].content;
      return content !== undefined;
    }, { message: "Already-loaded intended dashboard requires successful login sync evidence" }).toBe(true);
    return content;
  }
  async function saved(target: Page, intended: (content: any) => void | Promise<void>) {
    const current = new URL(target.url());
    expect(current.origin).toBe(process.env.WORKSPACE_FRONTEND_ORIGIN);
    const id = current.pathname.split("/").at(-1)!;
    const access = syncAccess.get(target);
    expect(access, "Authenticated same-origin login sync is required").toBeDefined();
    await target.keyboard.press("Control+Shift+S");
    let content: any;
    await expect(async () => {
      const response = await target.request.get(access!.url, {
        headers: access!.authorization ? { authorization: access!.authorization } : {},
        maxRedirects: 0, timeout: 10000,
      }).catch(() => { throw new Error("Authenticated dashboard read failed"); });
      expect(response.status()).toBe(200);
      expect(new URL(response.url()).origin).toBe(current.origin);
      content = (await response.json()).owned?.[id]?.content;
      expect(content, "Server must contain the intended owned dashboard").toBeDefined();
      await intended(content);
    }).toPass({ timeout: 30000, intervals: [250, 500, 1000] });
    return content;
  }
  async function revealResearch(target: Page) {
    const ids = [...primaryIds, "company_research"];
    const shells = target.locator("#workarea [data-widget-id]");
    await expect(shells).toHaveCount(ids.length);
    for (let index = 0; index < ids.length; index++) {
      const shell = shells.nth(index);
      await shell.scrollIntoViewIfNeeded();
      await expect(shell.locator(ids.map(id => `.widget-${id}`).join(","))).toBeVisible();
    }
    for (const id of ids) await expect(target.locator(`#workarea .widget-${id}`)).toHaveCount(1);
  }
  function assertStoredSelection(content: any, id: string, symbol: string, acquisition?: string, selectedAfter?: number) {
    const item = content.data.widgets.find((item: any) => item.widgetId === id);
    expect(item.storage.params.symbol).toBe(symbol);
    expect(item.storage.companySelection).toMatchObject({ version: 1, provider: "fmp", symbol });
    if (acquisition) expect(item.storage.companySelection.retrievedAt).toBe(acquisition);
    if (selectedAfter !== undefined) expect(Date.parse(item.storage.companySelection.selectedAt)).toBeGreaterThanOrEqual(selectedAfter);
  }
  function assertIntended(state: any) {
    const byId = (id: string) => state.widgets.find((item: any) => item.widgetId === id);
    for (const id of primaryIds) {
      expect(byId(id).params.symbol).toBe("AAPL");
      expect(byId(id).selection).toMatchObject({ version: 1, provider: "fmp", symbol: "AAPL" });
    }
    for (const dataset of ["income", "balance", "cash"])
      expect(byId(`equity_fundamental_${dataset}_fmp_obb`).params).toMatchObject({ period: "quarter", limit: 3 });
    expect(byId("equity_price_historical_fmp_obb").params).toMatchObject({ start_date: "2025-01-03", end_date: "2025-01-30" });
    const config = byId("company_research").research;
    expect(config).toMatchObject({ version: 1, period: "quarter", limit: 3 });
    expect(config.peers.map((peer: any) => [peer.identity.symbol, peer.rationale])).toEqual([
      ["ORCL", "ORCL explicit candidate; comparability unverified."], ["MSFT", "MSFT explicit candidate; comparability unverified."],
    ]);
    const symbolGroup = byId(profileId).paramGroups.symbol;
    for (const id of primaryIds) expect(byId(id).paramGroups.symbol).toBe(symbolGroup);
    const periodGroup = byId(widgetId).paramGroups.period;
    for (const dataset of ["income", "balance", "cash"]) expect(byId(`equity_fundamental_${dataset}_fmp_obb`).paramGroups.period).toBe(periodGroup);
    expect(byId("company_research").paramGroups ?? {}).toEqual({});
  }
  function semanticChoices(state: any) {
    return {
      widgets: state.widgets.map((item: any) => ({ widgetId: item.widgetId, params: item.params, research: item.research,
        selection: item.selection ? Object.fromEntries(Object.entries(item.selection).filter(([key]) => !["selectedAt", "retrievedAt"].includes(key))) : undefined,
        groups: Object.entries(item.paramGroups ?? {}).map(([param, id]) => [param, state.groups.find((group: any) => group.id === id)?.name]),
      })),
      layout: Object.entries(state.gridLayout).map(([tab, items]: [string, any]) => [tab, items.map((item: any) => ({ ...item,
        i: state.widgets.find((widget: any) => widget.id === item.i)?.widgetId ?? item.i }))]),
      groups: state.groups.map(({ id, ...group }: any) => group),
    };
  }
  async function settleDashboard(target: Page, after: number) {
    await revealResearch(target);
    for (const dataset of ["income", "balance", "cash"])
      await captured(`/data/api/v1/equity/fundamental/${dataset}`, "AAPL", "quarter", after);
    await captured("/data/api/v1/equity/price/historical", "AAPL", undefined, after);
    const research = widget(target, "company_research");
    for (const symbol of ["ORCL", "MSFT"]) for (const dataset of ["metrics", "ratios"]) {
      const panel = research.getByRole("region", { name: `${symbol} ${dataset}`, exact: true });
      await panel.scrollIntoViewIfNeeded();
      await expect(panel.getByRole("status")).toHaveText("success");
      await captured(`/data/api/v1/equity/fundamental/${dataset}`, symbol, "quarter", after);
    }
    await Promise.all(reads);
  }
  async function openCatalog(target: Page, name: string) {
    await target.goto("/app/connections");
    const refreshedCatalog = target.waitForResponse(response => new URL(response.url()).pathname === "/data/apps.json");
    const sourceRow = target.getByRole("row").filter({ hasText: "Installed QOpenBB data API" });
    await sourceRow.getByRole("button").filter({ has: target.locator("svg[id=refresh-icon-ds]") }).click();
    expect((await refreshedCatalog).ok()).toBe(true);
    await target.getByRole("link", { name: "Apps", exact: true }).click();
    const app = target.getByRole("button").filter({ has: target.getByText(name, { exact: true }) });
    await expect(app).toHaveCount(1);
    await app.click();
    await revealResearch(target);
    await expect(widget(target, "company_research").getByLabel("Peer period", { exact: true })).toBeVisible();
  }
  async function inspector(panel: Locator, payload: any, fields = ["stock_based_compensation", "ebitda", "operating_cash_flow", "free_cash_flow"]) {
    await panel.scrollIntoViewIfNeeded();
    await panel.getByRole("button", { name: "Inspect observations", exact: true }).click();
    const dialog = panel.page().getByRole("dialog", { name: "Observation evidence", exact: true });
    const metadata = payload.extra.results_metadata.__qopenbb_financial__;
    await expect(dialog.getByText(/^(Stale evidence|Refreshing evidence)/)).toHaveCount(0);
    const detail = (label: string) => dialog.locator("dt").filter({ hasText: new RegExp(`^${label}$`) }).locator("xpath=following-sibling::dd[1]");
    await expect(detail("Dataset")).toHaveText(metadata.dataset);
    await expect(detail("Provider")).toHaveText("fmp");
    await expect(detail("Endpoint")).toHaveText(metadata.source.endpoint);
    await expect(detail("Point-in-time safe")).toHaveText("false");
    await expect(detail("Effective query")).toHaveText(JSON.stringify(metadata.effective_query));
    await expect(detail("Acquired at")).toHaveText(metadata.retrieved_at);
    for (const field of fields) {
      const rowIndex = payload.results.findIndex((row: any) => Object.hasOwn(row, field));
      if (rowIndex < 0) { facts.push({ dataset: metadata.dataset, field, status: "not-returned; unverified" }); continue; }
      await dialog.getByRole("combobox", { name: "Original observation", exact: true }).click();
      await panel.page().getByRole("option", { name: new RegExp(`^Original row ${rowIndex}(?: ·|$)`) }).click();
      await dialog.getByRole("combobox", { name: "Field", exact: true }).click();
      await panel.page().getByRole("option", { name: field, exact: true }).click();
      const value = payload.results[rowIndex][field];
      const fieldMetadata = metadata.fields[field];
      const currencyField = fieldMetadata?.currency_field;
      await expect(detail("Currency")).toHaveText(fieldMetadata?.currency ?? (currencyField && payload.results[rowIndex][currencyField] != null ? String(payload.results[rowIndex][currencyField]) : "Unknown"));
      await expect(dialog.getByTestId("observation-value")).toHaveText(value == null ? "Missing (null)" : String(value));
      for (const [label, key] of [["Unit", "unit"], ["Scale", "scale"], ["Period basis", "period_basis"], ["Financial basis", "financial_basis"]])
        await expect(detail(label)).toHaveText(fieldMetadata?.[key] == null ? "Unknown" : typeof fieldMetadata[key] === "object" ? Object.keys(fieldMetadata[key]).length ? JSON.stringify(fieldMetadata[key]) : "Unknown (none supplied)" : String(fieldMetadata[key]));
      const row = payload.results[rowIndex];
      const provenance = metadata.statement_provenance?.rows.find((item: any) => item.row_index === rowIndex);
      const display = (value: any) => value == null || value === "" ? "Unknown" : typeof value === "object" ? Object.keys(value).length ? JSON.stringify(value) : "Unknown (none supplied)" : String(value);
      for (const [label, key] of [["Observation date", "observation_date_field"], ["Valuation date", "valuation_date_field"], ["Publication date", "publication_date_field"]]) {
        const reference = fieldMetadata?.[key] ?? metadata[key];
        await expect(detail(label)).toHaveText(display(reference ? row[reference] : null));
      }
      for (const [label, key] of [["Period end", "period_end"], ["Fiscal year", "fiscal_year"], ["Fiscal period", "fiscal_period"], ["Requested frequency", "requested_frequency"], ["Flow coverage", "flow_coverage"], ["Coverage status", "coverage_status"], ["Period start", "period_start"], ["Duration days", "duration_days"], ["Filing date", "filing_date"], ["Accepted date", "accepted_date"], ["Restatement status", "restatement_status"]])
        await expect(detail(label)).toHaveText(display(provenance?.[key]));
      await expect(detail("Original row index")).toHaveText(String(rowIndex));
      await expect(detail("Source ordinal")).toHaveText(display(provenance?.source_ordinal));
      await expect(detail("Field instant date")).toHaveText(display(provenance?.instant_dates?.[field]));
      facts.push({ dataset: metadata.dataset, field, value, unit: fieldMetadata?.unit, periodBasis: fieldMetadata?.period_basis, rowIndex,
        observationDate: row[fieldMetadata?.observation_date_field ?? metadata.observation_date_field] ?? null, periodEnd: provenance?.period_end ?? null });
    }
    await expect(dialog).toContainText("SBC treatment is unknown");
    await panel.page().keyboard.press("Escape");
  }
  let url = "";
  let expected: any;
  let selected: any;
  let retainedReadAt = 0;
  try {
    if (phase === "reopen") retainedReadAt = requests.length;
    await loginDisposableWorkspace(page);
    if (phase === "initial") {
      expect(existsSync(checkpoint)).toBe(false);
      const app = await connectInstalledCatalog(page, catalog => {
        for (const id of [...primaryIds, "company_research"]) expect(catalog[id]).toBeDefined();
      }, "Company Research");
      const apps = await page.request.get(`${process.env.WORKSPACE_FRONTEND_ORIGIN}/data/apps.json`);
      expect(apps.ok()).toBe(true);
      const generated = (await apps.json()).find((item: any) => item.name === "Company Research");
      expect(generated.tabs.Research.layout.map((item: any) => item.i)).toEqual([...primaryIds, "company_research"]);
      const appOpenedAt = await page.evaluate(() => Date.now());
      await app.click();
      await revealResearch(page);
      await expect(widget(page, "company_research").getByLabel("Peer period", { exact: true })).toBeVisible();
      url = page.url();
      const profile = widget(page, profileId);
      const originalAapl = new Map<string, any>();
      for (const id of primaryIds) {
        const panel = widget(page, id);
        await panel.scrollIntoViewIfNeeded();
        const path = id === profileId ? profilePath : id.includes("price") ? "/data/api/v1/equity/price/historical" : `/data/api/v1/equity/fundamental/${id.split("_")[2]}`;
        originalAapl.set(path, await captured(path, "AAPL", id.includes("fundamental") ? "annual" : undefined));
      }
      await verifyNativeProfile(profile, originalAapl.get(profilePath), "AAPL");
      const initialProfile = (await saved(page, content => {
        assertStoredSelection(content, profileId, "AAPL", undefined, appOpenedAt);
        const selection = content.data.widgets.find((item: any) => item.widgetId === profileId).storage.companySelection;
        expect(captures.some(item => item.source === "live" && item.url.pathname === searchPath &&
          item.url.searchParams.get("query") === "AAPL" && item.url.searchParams.get("is_symbol") === "true" &&
          item.payload.extra.results_metadata.__qopenbb_financial__.retrieved_at === selection.retrievedAt)).toBe(true);
      })).data.widgets.find((item: any) => item.widgetId === profileId);
      const originalSearch = captures.find(item => item.source === "live" && item.url.pathname === searchPath &&
        item.url.searchParams.get("query") === "AAPL" && item.url.searchParams.get("is_symbol") === "true" &&
        item.payload.extra.results_metadata.__qopenbb_financial__.retrieved_at === initialProfile.storage.companySelection.retrievedAt);
      expect(originalSearch).toBeDefined();
      for (const [mode, query, symbol] of [["name", "Microsoft", "MSFT"], ["symbol", "AAPL", "AAPL"]] as const) {
        const changedAt = requests.length;
        if (symbol === "AAPL") {
          let acquisitionsBeforeChoice = new Set<string>([initialProfile.storage.companySelection.retrievedAt]);
          let choiceStartedAt = 0;
          await profile.getByRole("combobox", { name: "Symbol", exact: true }).fill(query);
          selected = await selectCompanyListing(profile, mode, query, symbol, originalSearch!.payload, async () => {
            await Promise.all(reads);
            acquisitionsBeforeChoice = new Set([initialProfile.storage.companySelection.retrievedAt,
              ...captures.filter(item => item.requestIndex >= changedAt && item.source === "live" && item.url.pathname === searchPath &&
                item.url.searchParams.get("query") === query && item.url.searchParams.get("is_symbol") === "true")
                .map(item => item.payload.extra.results_metadata.__qopenbb_financial__.retrieved_at)]);
            choiceStartedAt = await page.evaluate(() => Date.now());
          });
          const returnedProfile = (await saved(page, content => {
            assertStoredSelection(content, profileId, symbol, undefined, choiceStartedAt);
            const choice = content.data.widgets.find((item: any) => item.widgetId === profileId).storage.companySelection;
            expect(acquisitionsBeforeChoice.has(choice.retrievedAt)).toBe(true);
          }))
            .data.widgets.find((item: any) => item.widgetId === profileId);
          await Promise.all(reads);
          const actualAcquisition = returnedProfile.storage.companySelection.retrievedAt;
          const searches = requests.slice(changedAt).filter(item => item.path === searchPath && item.query.query === "AAPL" && item.query.is_symbol === "true");
          const cachedSearch = actualAcquisition === initialProfile.storage.companySelection.retrievedAt;
          if (!cachedSearch) {
            expect(searches.length).toBeGreaterThan(0);
            const fresh = captures.find(item => item.requestIndex >= changedAt && item.source === "live" && item.url.pathname === searchPath &&
              item.url.searchParams.get("query") === query && item.url.searchParams.get("is_symbol") === "true" &&
              item.payload.extra.results_metadata.__qopenbb_financial__.retrieved_at === actualAcquisition);
            expect(fresh).toBeDefined();
            expect(fresh!.payload.extra.results_metadata.__qopenbb_financial__).toMatchObject({ dataset: "equity/search", provider: "fmp",
              source: { endpoint: "search-symbol" }, effective_query: { query, limit: 20 } });
            expect(fresh!.payload.results.filter((row: any) => row.symbol === symbol)).toEqual([selected.listing]);
            selected = { ...selected, retrievedAt: actualAcquisition };
          }
          facts.push({ context: "same mounted profile AAPL search return", outcome: cachedSearch ? "explicit-cache" : "observed-live-after-expiry",
            query: { query, is_symbol: true, limit: 20 }, retrievedAt: actualAcquisition, allWidgetAaplSearches: searches.length,
            evidence: "Profile cache use requires its original acquisition; expiry requires actual matching live response. Other mounted selectors own independent search caches." });
        } else {
          selected = await chooseCompany(profile, mode, query, symbol);
          await saved(page, content => assertStoredSelection(content, profileId, symbol, selected.retrievedAt));
        }
        for (const id of primaryIds.filter(id => !id.includes("price"))) await expectSelectedCompany(widget(page, id), selected.listing);
        // Only this identical-key return intentionally reuses the original live AAPL evidence.
        // The accepted table adapter keeps that query fresh for 15 minutes; selection timestamps do not invalidate it.
        const cachedReturn = symbol === "AAPL";
        const profilePayload = cachedReturn ? originalAapl.get(profilePath) : await captured(profilePath, symbol, undefined, changedAt);
        const incomePayload = cachedReturn ? originalAapl.get(incomePath) : await captured(incomePath, symbol, "annual", changedAt);
        const pricePayload = cachedReturn ? originalAapl.get("/data/api/v1/equity/price/historical") :
          await captured("/data/api/v1/equity/price/historical", symbol, undefined, changedAt);
        await verifyNativeProfile(profile, profilePayload, symbol);
        await verifyNativeIncome(widget(page, widgetId), incomePayload, symbol, "annual");
        if (cachedReturn) {
          await inspector(profile, profilePayload, ["last_price"]);
          await inspector(widget(page, widgetId), incomePayload, ["revenue", "ebitda"]);
          await inspector(widget(page, "equity_price_historical_fmp_obb"), pricePayload, ["close"]);
          expect(requests.slice(changedAt).filter(request => [profilePath, incomePath, "/data/api/v1/equity/price/historical"].includes(request.path))).toEqual([]);
          facts.push({ context: "explicit cached AAPL annual/original-price-window return after MSFT", source: "original successful live response before company changes",
            acquisition: { profile: profilePayload.extra.results_metadata.__qopenbb_financial__.retrieved_at,
              income: incomePayload.extra.results_metadata.__qopenbb_financial__.retrieved_at,
              price: pricePayload.extra.results_metadata.__qopenbb_financial__.retrieved_at },
            evidence: "Current AAPL selectors, visible profile/income/price values and current inspectors match original responses; no fallback for other actions." });
        }
        expect(pricePayload.extra.results_metadata.__qopenbb_financial__.effective_query.symbol).toBe(symbol);
        await expectSelectedCompany(widget(page, "equity_price_historical_fmp_obb"), selected.listing);
        if (pricePayload.results[0]?.close != null) await displayedNumber(await revenueCell(widget(page, "equity_price_historical_fmp_obb"), "close"), pricePayload.results[0].close);
      }
      const research = widget(page, "company_research");
      for (const [query, symbol] of [["Microsoft", "MSFT"], ["Oracle", "ORCL"]]) {
        await research.scrollIntoViewIfNeeded();
        const response = page.waitForResponse(item => new URL(item.url()).pathname === searchPath && new URL(item.url()).searchParams.get("query") === query);
        await research.getByLabel("Find candidate peers", { exact: true }).fill(query);
        const payload = await (await response).json();
        const listing = payload.results.find((row: any) => row.symbol === symbol);
        expect(listing).toBeDefined();
        await research.getByRole("button", { name: `Add ${listing.name} (${symbol})`, exact: true }).click();
        await research.getByLabel(`Rationale for ${symbol}`, { exact: true }).fill(`${symbol} explicit candidate; comparability unverified.`);
      }
      await research.getByRole("button", { name: "Move ORCL up", exact: true }).click();
      await expect(research.getByRole("list", { name: "Selected peers" }).getByRole("listitem").first()).toContainText("ORCL");
      await expect(research.getByRole("region", { name: "Peer observations", exact: true })).toContainText("unverified");
      await expect(research).toContainText("TTM excluded");
      await expect(research).toContainText("Accounting optimization and stock-based compensation");
      const price = widget(page, "equity_price_historical_fmp_obb");
      for (const [oldDate, day] of [["Jan 02, 2025", "3"], ["Jan 31, 2025", "30"]]) {
        const priceAt = requests.length;
        await price.scrollIntoViewIfNeeded();
        await price.getByRole("button", { name: oldDate, exact: true }).click();
        await page.locator(".obb-dropdown-container").getByRole("button", { name: new RegExp(`January ${day}(?:st|nd|rd|th)?, 2025`) }).click();
        await page.keyboard.press("Escape");
        const pricePayload = await captured("/data/api/v1/equity/price/historical", "AAPL", undefined, priceAt);
        expect(pricePayload.extra.results_metadata.__qopenbb_financial__.effective_query).toMatchObject({
          symbol: "AAPL", start_date: "2025-01-03", end_date: day === "3" ? "2025-01-31" : "2025-01-30" });
      }
      const currentStatementPayloads = new Map<string, any>();
      for (const period of ["quarter"]) {
        const changedAt = requests.length;
        const income = widget(page, widgetId);
        await income.scrollIntoViewIfNeeded();
        const current = period === "annual" ? "quarter" : "annual";
        await income.getByRole("button", { name: current, exact: true }).click();
        await page.locator(".obb-dropdown-container").getByText(period, { exact: true }).click();
        await verifyNativeIncome(income, await captured(incomePath, "AAPL", period, changedAt), "AAPL", period);
        for (const dataset of ["income", "balance", "cash"]) {
          const payload = await captured(`/data/api/v1/equity/fundamental/${dataset}`, "AAPL", period, changedAt);
          expect(payload.extra.results_metadata.__qopenbb_financial__.effective_query).toMatchObject({ symbol: "AAPL", period, limit: 3 });
          await expect(widget(page, `equity_fundamental_${dataset}_fmp_obb`).getByRole("button", { name: period, exact: true })).toBeAttached();
          currentStatementPayloads.set(dataset, payload);
        }
        await expect(price.getByRole("button", { name: "Jan 03, 2025", exact: true })).toBeAttached();
        await expect(price.getByRole("button", { name: "Jan 30, 2025", exact: true })).toBeAttached();
      }
      const peerPeriodAt = requests.length;
      await research.getByLabel("Peer period", { exact: true }).selectOption("quarter");
      await expect(research.getByLabel("Peer observation limit", { exact: true })).toHaveValue("3");
      await expect(research.getByRole("button", { name: "Refresh peer observations", exact: true })).toBeEnabled();
      for (const symbol of ["MSFT", "ORCL"]) for (const dataset of ["metrics", "ratios"]) {
        const panel = research.getByRole("region", { name: `${symbol} ${dataset}`, exact: true });
        await panel.scrollIntoViewIfNeeded();
        await expect(panel.getByRole("status")).toHaveText("success");
        await expect(panel).toContainText("unverified");
        const payload = await captured(`/data/api/v1/equity/fundamental/${dataset}`, symbol, "quarter", peerPeriodAt);
        const row = payload.results[0];
        const field = Object.keys(row).find(key => typeof row[key] === "number")!;
        expect(field).toBeTruthy();
        await panel.getByLabel("Original row", { exact: true }).selectOption("0");
        await panel.getByLabel("Field", { exact: true }).selectOption(field);
        await expect(panel.locator("dt").filter({ hasText: /^Original value$/ }).locator("xpath=following-sibling::dd[1]")).toHaveText(String(row[field]));
      }
      const fixturePayload = structuredClone(await captured("/data/api/v1/equity/fundamental/ratios", "ORCL", "quarter"));
      const fixtureField = Object.keys(fixturePayload.results[0]).find(key => typeof fixturePayload.results[0][key] === "number")!;
      expect(fixtureField).toBeTruthy();
      const originalField = fixturePayload.extra.results_metadata.__qopenbb_financial__.fields[fixtureField];
      const originalCurrency = originalField.currency_field ? fixturePayload.results[0][originalField.currency_field] : originalField.currency;
      const originalPanel = research.getByRole("region", { name: "ORCL ratios", exact: true });
      await originalPanel.getByLabel("Field", { exact: true }).selectOption(fixtureField);
      await expect(originalPanel.locator("dt").filter({ hasText: /^Unit \/ scale \/ row currency$/ }).locator("xpath=following-sibling::dd[1]"))
        .toHaveText([originalField.unit, originalField.scale, originalCurrency].map(value => value == null ? "Unknown" : String(value)).join(" / "));
      const fixturePath = (url: URL) => url.origin === process.env.WORKSPACE_FRONTEND_ORIGIN && /^\/data\/api\/v1\/equity\/fundamental\/(metrics|ratios)$/.test(url.pathname);
      const fixtureBaselines = new Map<string, any>();
      for (const symbol of ["MSFT", "ORCL"]) for (const dataset of ["metrics", "ratios"])
        fixtureBaselines.set(`${symbol}/${dataset}`, structuredClone(await captured(`/data/api/v1/equity/fundamental/${dataset}`, symbol, "quarter")));
      let fixtureCase = "missing";
      await page.route(fixturePath, route => {
        syntheticRequests.add(route.request());
        const requestUrl = new URL(route.request().url());
        if (requestUrl.searchParams.get("symbol") !== "ORCL" || !requestUrl.pathname.endsWith("/ratios"))
          return route.fulfill({ json: fixtureBaselines.get(`${requestUrl.searchParams.get("symbol")}/${requestUrl.pathname.split("/").at(-1)}`) });
        const payload = structuredClone(fixturePayload);
        payload.results[0][fixtureField] = fixtureCase === "missing" ? null : fixtureCase === "zero" ? 0 : -1;
        const field = payload.extra.results_metadata.__qopenbb_financial__.fields[fixtureField];
        if (fixtureCase === "incompatible") {
          // This scenario owns synthetic metadata; the original field may have unknown scale.
          field.unit = "shares";
          field.scale = 1;
          field.currency = "EUR";
          delete field.currency_field;
          field.financial_basis = { share_count: "synthetic incompatible diluted basis" };
        }
        return route.fulfill({ json: payload });
      });
      for (fixtureCase of ["missing", "incompatible", "zero", "negative"]) {
        const fixtureAt = requests.length;
        await research.getByRole("button", { name: "Refresh peer observations", exact: true }).click();
        await captured("/data/api/v1/equity/fundamental/ratios", "ORCL", "quarter", fixtureAt, "deterministic");
        const fixturePanel = research.getByRole("region", { name: "ORCL ratios", exact: true });
        await expect(fixturePanel.getByRole("status")).toHaveText("success");
        await fixturePanel.getByLabel("Field", { exact: true }).selectOption(fixtureField);
        await expect(fixturePanel.locator("dt").filter({ hasText: /^Original value$/ }).locator("xpath=following-sibling::dd[1]"))
          .toHaveText(fixtureCase === "missing" ? "Unknown" : fixtureCase === "zero" ? "0" : "-1");
        await expect(fixturePanel).toContainText("unverified");
        if (fixtureCase === "incompatible") {
          await expect(fixturePanel).toContainText("shares / 1 / EUR");
          await expect(fixturePanel).toContainText("synthetic incompatible diluted basis");
        }
        await expect(research.getByRole("button", { name: "Refresh peer observations", exact: true })).toBeEnabled();
        facts.push({ kind: "deterministic owned-route original-evidence fixture", symbol: "ORCL", field: fixtureField, scenario: fixtureCase,
          limitation: "Raw signed value only, not denominator evidence or eligibility; accepted tests/unit/financial-evidence.test.ts owns conditional denominator semantics." });
      }
      await page.unroute(fixturePath);
      // Deterministic failure on the owned application route; no failed provider call is manufactured.
      const failureRoute = `${process.env.WORKSPACE_FRONTEND_ORIGIN}/data/api/v1/equity/fundamental/ratios*`;
      let syntheticFailure = true;
      await page.route(failureRoute, async route => {
        if (new URL(route.request().url()).searchParams.get("symbol") !== "ORCL" || !syntheticFailure) return route.continue();
        syntheticRequests.add(route.request());
        return route.fulfill({ status: 503, json: { detail: "Deterministic browser peer-dataset failure fixture" } });
      });
      const failureDiagnosticStart = { failures: diagnostics[0].failures.length, console: diagnostics[0].consoleErrors.length };
      await research.getByRole("button", { name: "Refresh peer observations", exact: true }).click();
      const failedPeer = research.getByRole("region", { name: "ORCL ratios", exact: true });
      await expect(failedPeer.getByRole("status")).toHaveText("stale");
      await expect(failedPeer.getByRole("alert")).toContainText("Prior evidence retained as stale");
      await expect(research.getByRole("region", { name: "MSFT ratios", exact: true }).getByRole("status")).toHaveText("success");
      await expect(research.getByRole("button", { name: "Refresh peer observations", exact: true })).toBeEnabled();
      for (const item of diagnostics[0].failures.slice(failureDiagnosticStart.failures))
        if (item.path === "/data/api/v1/equity/fundamental/ratios" && item.status === 503) expected503.add(item);
      for (const item of diagnostics[0].consoleErrors.slice(failureDiagnosticStart.console))
        if (item.path === "/data/api/v1/equity/fundamental/ratios" && /Failed to load resource.*503/.test(item.message)) expectedConsole503.add(item);
      expect(expected503.size).toBeGreaterThan(0);
      expect(expected503.size).toBeLessThanOrEqual(2);
      syntheticFailure = false;
      const refreshAt = requests.length;
      await research.getByRole("button", { name: "Refresh peer observations", exact: true }).click();
      for (const symbol of ["MSFT", "ORCL"]) for (const dataset of ["metrics", "ratios"]) {
        const payload = await captured(`/data/api/v1/equity/fundamental/${dataset}`, symbol, "quarter", refreshAt);
        const panel = research.getByRole("region", { name: `${symbol} ${dataset}`, exact: true });
        await expect(panel.locator("dt").filter({ hasText: /^Acquired at$/ }).locator("xpath=following-sibling::dd[1]")).toHaveText(payload.extra.results_metadata.__qopenbb_financial__.retrieved_at);
        const field = Object.keys(payload.results[0]).find(key => typeof payload.results[0][key] === "number")!;
        await panel.getByLabel("Field", { exact: true }).selectOption(field);
        await expect(panel.locator("dt").filter({ hasText: /^Original value$/ }).locator("xpath=following-sibling::dd[1]")).toHaveText(String(payload.results[0][field]));
      }
      await expect(research.getByRole("button", { name: "Refresh peer observations", exact: true })).toBeEnabled();
      await expect(failedPeer.getByRole("status")).toHaveText("success");
      await page.unroute(failureRoute);
      facts.push({ kind: "deterministic owned-route failure/recovery fixture", symbol: "ORCL", dataset: "ratios", status: "stale then success; unaffected MSFT remains success" });
      for (const dataset of ["income", "cash"]) await inspector(widget(page, `equity_fundamental_${dataset}_fmp_obb`), currentStatementPayloads.get(dataset));
      for (const theme of ["light", "dark"]) {
        const dark = (await page.locator("html").getAttribute("class"))?.split(" ").includes("dark");
        if (dark !== (theme === "dark")) await page.keyboard.press("Control+m");
        await expect(page.locator("html")).toHaveClass(theme === "dark" ? /\bdark\b/ : /^(?!.*\bdark\b)/);
        await research.screenshot({ path: info.outputPath(`company-research-${theme}.png`) });
      }
      expected = selectionState(await saved(page, content => assertIntended(selectionState(content))));
      assertIntended(expected);
      const intendedBeforeExport = semanticChoices(expected);
      // Export is the actual dashboard context-menu action; import transport is an owned catalog fixture.
      await page.locator(`[data-rct-item-id="${new URL(url).pathname.split("/").at(-1)}"]`).click({ button: "right" });
      await page.getByText("Export apps.json", { exact: true }).click();
      const exportDialog = page.getByRole("dialog").filter({
        has: page.getByRole("heading", { name: "Export App", exact: true }),
      });
      await expect(exportDialog).toHaveCount(1);
      const exportName = "Company Research exported acceptance";
      const exportDescription = "Company Research acceptance: saved analyst choices and independent peer configuration.";
      await exportDialog.getByPlaceholder("Enter app name...").fill(exportName);
      await exportDialog.getByRole("textbox", { name: "Description", exact: true }).fill(exportDescription);
      await expect(exportDialog.getByPlaceholder("Enter app name...")).toHaveValue(exportName);
      await expect(exportDialog.getByRole("textbox", { name: "Description", exact: true })).toHaveValue(exportDescription);
      const downloadEvent = page.waitForEvent("download");
      await exportDialog.getByRole("button", { name: "Download App", exact: true }).click();
      const download = await downloadEvent;
      const stream = await download.createReadStream();
      expect(stream).toBeTruthy();
      const chunks: Buffer[] = [];
      for await (const chunk of stream!) chunks.push(Buffer.from(chunk));
      const exported = JSON.parse(Buffer.concat(chunks).toString("utf8"));
      expect(exported).toMatchObject({ name: exportName, description: exportDescription });
      const serialized = JSON.stringify(exported);
      expect(serialized).not.toMatch(/providerPayload|access_token|api_key|password|__qopenbb_financial__|results_metadata/);
      expect(exported.tabs.Research.layout).toHaveLength(6);
      let catalogTemplate = exported;
      await page.route(`${process.env.WORKSPACE_FRONTEND_ORIGIN}/data/apps.json`, route => route.fulfill({ json: [catalogTemplate] }));
      await openCatalog(page, exported.name);
      const imported = await saved(page, content => {
        assertIntended(selectionState(content));
        expect(semanticChoices(selectionState(content))).toEqual(intendedBeforeExport);
      });
      const importedState = selectionState(imported);
      expect(importedState.widgets.map((item: any) => item.id)).not.toEqual(expected.widgets.map((item: any) => item.id));
      expect(importedState.widgets.map((item: any) => [item.widgetId, item.params, item.selection, item.research]))
        .toEqual(expected.widgets.map((item: any) => [item.widgetId, item.params, item.selection, item.research]));
      const semanticLayout = (state: any) => Object.entries(state.gridLayout).map(([tab, items]: [string, any]) => [tab,
        items.map((item: any) => ({ ...item, i: state.widgets.find((widget: any) => widget.id === item.i)?.widgetId ?? item.i }))]);
      expect(semanticLayout(importedState)).toEqual(semanticLayout(expected));
      const semanticGroups = (state: any) => state.groups.map(({ id, ...group }: any) => group);
      expect(semanticGroups(importedState)).toEqual(semanticGroups(expected));
      for (const item of importedState.widgets) {
        const original = expected.widgets.find((other: any) => other.widgetId === item.widgetId);
        for (const [param, groupId] of Object.entries(item.paramGroups ?? {})) {
          const importedGroup = importedState.groups.find((group: any) => group.id === groupId);
          const originalGroup = expected.groups.find((group: any) => group.id === original.paramGroups[param]);
          expect(importedGroup.name).toBe(originalGroup.name);
        }
      }
      for (const item of importedState.widgets) for (const groupId of Object.values(item.paramGroups ?? {}))
        expect(importedState.groups.some((group: any) => group.id === groupId)).toBe(true);
      const foreign = structuredClone(exported);
      foreign.name = "Synthetic foreign-source Company Research";
      const foreignKey = JSON.stringify(["synthetic-unknown-source", "https://foreign.invalid/data"]);
      for (const tab of Object.values(foreign.tabs) as any[]) for (const item of tab.layout) {
        if (item.state?.storage?.companySelection) {
          item.state.storage.companySelection.sourceKey = foreignKey;
          if (item.i === profileId) item.state.storage.companySelection.version = 99;
        }
      }
      catalogTemplate = foreign;
      const atUnresolved = requests.length;
      await openCatalog(page, foreign.name);
      const foreignUrl = page.url();
      const assertForeign = (content: any) => {
        const choices = content.data.widgets.filter((item: any) => item.storage?.companySelection);
        expect(choices).toHaveLength(5);
        for (const item of choices) expect(item.storage.companySelection.sourceKey).toBe(foreignKey);
        expect(choices.find((item: any) => item.widgetId === profileId).storage.companySelection.version).toBe(99);
      };
      const foreignSaved = await saved(page, assertForeign);
      const unresolved = foreignSaved.data.widgets.filter((item: any) => item.storage?.companySelection);
      expect(unresolved).toHaveLength(5);
      for (const item of unresolved) expect(item.storage.companySelection.sourceKey).toBe(foreignKey);
      expect(unresolved.find((item: any) => item.widgetId === profileId).storage.companySelection.version).toBe(99);
      await readFinancialDashboard(page, foreignUrl);
      await revealResearch(page);
      await expect(widget(page, profileId).getByRole("status")).toContainText("Select from the current source");
      const reopenedForeign = await saved(page, assertForeign);
      for (const item of reopenedForeign.data.widgets.filter((item: any) => item.storage?.companySelection))
        expect(item.storage.companySelection.sourceKey).toBe(foreignKey);
      expect(reopenedForeign.data.widgets.find((item: any) => item.widgetId === profileId).storage.companySelection.version).toBe(99);
      for (const request of requests.slice(atUnresolved)) {
        expect(["/data/api/v1/equity/fundamental/metrics", "/data/api/v1/equity/fundamental/ratios"]).toContain(request.path);
        expect(["MSFT", "ORCL"]).toContain(request.query.symbol);
      }
      const recoveryAt = requests.length;
      for (const id of primaryIds) {
        const panel = widget(page, id);
        await panel.scrollIntoViewIfNeeded();
        const recovered = await chooseCompany(panel, "name", "Apple", "AAPL");
        if (id === profileId) selected = recovered;
        else expect(recovered.listing).toEqual(selected.listing);
        await expectSelectedCompany(panel, selected.listing);
      }
      await verifyNativeProfile(widget(page, profileId), await captured(profilePath, "AAPL", undefined, recoveryAt), "AAPL");
      for (const dataset of ["income", "balance", "cash"])
        await captured(`/data/api/v1/equity/fundamental/${dataset}`, "AAPL", "quarter", recoveryAt);
      const recoveredPrice = await captured("/data/api/v1/equity/price/historical", "AAPL", undefined, recoveryAt);
      expect(recoveredPrice.extra.results_metadata.__qopenbb_financial__.effective_query).toMatchObject({
        symbol: "AAPL", start_date: "2025-01-03", end_date: "2025-01-30" });
      url = page.url();
      const recoveredState = selectionState(await saved(page, content => {
        assertIntended(selectionState(content));
        expect(semanticChoices(selectionState(content))).toEqual(intendedBeforeExport);
      }));
      assertIntended(recoveredState);
      expect(semanticChoices(recoveredState)).toEqual(intendedBeforeExport);
      expected = recoveredState;
      for (const item of expected.widgets.filter((item: any) => item.selection)) expect(item.selection.sourceKey).not.toBe(foreignKey);
      facts.push({ kind: "deterministic foreign-source catalog configuration", retainedOnReopen: true,
        recovery: "explicit current-source Apple selection in each of five primary widgets", widgets: primaryIds });
      facts.push({ transport: "deterministic owned apps.json catalog fixture; actual exported App imported by Apps UI", provider: "real FMP observations" });
    } else {
      const prior = JSON.parse(readFileSync(checkpoint, "utf8"));
      expect(prior.stage).toBe("initial-complete");
      expect(prior.images).toEqual(runtime.images);
      expect(prior.runtimeName).toBe(runtime.name);
      expect(prior.containerId).not.toBe(runtime.container);
      expect(prior.containerId).toBeTruthy();
      url = `${process.env.WORKSPACE_FRONTEND_ORIGIN}${prior.dashboardPath}`;
      expected = prior.state;
      selected = prior.selected;
      const retainedState = selectionState(await readResearchDashboard(page, url));
      assertIntended(retainedState);
      expect(retainedState).toEqual(expected);
    }
    assertIntended(expected);
    await Promise.all(reads);
    if (phase === "initial") {
    captures.length = 0;
    const context = await browser.newContext({ baseURL: process.env.WORKSPACE_FRONTEND_ORIGIN, serviceWorkers: "block", viewport: { width: 1600, height: 1000 } });
    try {
      const reopened = await context.newPage();
      diagnostics.push(await observeApplication(reopened));
      observe(reopened);
      const reopenedAt = requests.length;
      await loginDisposableWorkspace(reopened);
      const reopenedState = selectionState(await readResearchDashboard(reopened, url));
      assertIntended(reopenedState);
      expect(reopenedState).toEqual(expected);
      await expectSelectedCompany(widget(reopened, profileId), selected.listing);
      await verifyNativeProfile(widget(reopened, profileId), await captured(profilePath, "AAPL", undefined, reopenedAt), "AAPL");
      await settleDashboard(reopened, reopenedAt);
      await expect(widget(reopened, "company_research").getByLabel("Rationale for ORCL", { exact: true })).toHaveValue("ORCL explicit candidate; comparability unverified.");
    } finally { await context.close(); }
    } else {
      // This phase already starts in a fresh authenticated browser context after recreation.
      await expectSelectedCompany(widget(page, profileId), selected.listing);
      await verifyNativeProfile(widget(page, profileId), await captured(profilePath, "AAPL", undefined, retainedReadAt), "AAPL");
      await settleDashboard(page, retainedReadAt);
    }
    await Promise.all(reads);
    for (const diagnostic of diagnostics) expectApplicationDiagnostics({ ...diagnostic,
      failures: diagnostic.failures.filter(item => !expected503.has(item)),
      consoleErrors: diagnostic.consoleErrors.filter(item => !expectedConsole503.has(item)),
      requestFailures: diagnostic.requestFailures,
    });
    if (phase === "initial") await (await runtimeReader()).writeResearchCheckpoint(checkpoint, { stage: "initial-complete", images: runtime.images,
      runtimeName: runtime.name, containerId: runtime.container, dashboardPath: new URL(url).pathname, state: expected, selected });
  } finally {
    await info.attach("company-research-sanitized-financial-facts", { contentType: "application/json",
      body: JSON.stringify({ phase, images: runtime.images, requestEstimate, facts, requests, responseLifecycle, captureDemands,
        limitation: "Retained-data recreation only; no backup/restore or owner-server acceptance. Cumulative provider budget enforced by checked external controller." }) });
  }
});