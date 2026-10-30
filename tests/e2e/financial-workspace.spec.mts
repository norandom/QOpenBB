import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { isAbsolute, relative, resolve } from "node:path";
import type { Locator, Page, Response } from "../../verification/node_modules/@playwright/test/index.js";
import { expectApplicationDiagnostics, observeApplication } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/diagnostics";
import { saveDashboard } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/editor";
import { expect, loginDisposableWorkspace, test } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/fixtures";

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
      requestFailures: diagnostics.requestFailures.filter(item => !(item.path === searchPath && item.reason === "net::ERR_ABORTED")),
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
  const payload = await search.json();
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
  await option.click();
  await expectSelectedCompany(widget, listing);
  return { listing, retrievedAt: metadata.retrieved_at };
}

async function expectSelectedCompany(widget: Locator, listing: any) {
  await widget.scrollIntoViewIfNeeded();
  await expect(widget.getByRole("combobox", { name: "Company name", exact: true })).toHaveValue(listing.name);
  await expect(widget.getByRole("combobox", { name: "Symbol", exact: true })).toHaveValue(listing.symbol);
  await expect(widget.getByRole("status").filter({ hasText: "Current company:" }))
    .toContainText(`Current company: ${listing.name} (${listing.symbol}).`);
}

async function displayedNumber(cell: Locator, amount: number) {
  await expect(cell).toBeInViewport({ ratio: 1 });
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
  return { groups: content.data.groups,
    widgets: content.data.widgets.map((widget: any) => ({ id: widget.id, widgetId: widget.widgetId,
      paramGroups: widget.paramGroups, params: widget.storage.params, selection: widget.storage.companySelection })) };
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
  const suffix = relative(resolve("artifacts/company-selector-implementation"), resolve(checkpoint));
  if (!suffix || suffix.startsWith("..") || isAbsolute(suffix)) throw Error("Use ignored company-selector checkpoint path");
  if (phase === "initial") {
    // Refuse to overwrite a checkpoint from a previously completed journey.
    expect(existsSync(checkpoint)).toBe(false);
  }
  const runtime = JSON.parse(readFileSync(process.env.WORKSPACE_RUNTIME_PRIVATE!, "utf8"));
  expect(runtime.name).toMatch(/^qopenbb-browser-/);
  expect(runtime.packaged_image_only).toBe(true);
  expect(runtime.source_overlay).toBeNull();
  const diagnostics = [await observeApplication(page)];
  const captures: { path: string; symbol: string; payload: any }[] = [];
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
      const read = response.json().then(payload => { captures.push({ path: url.pathname, symbol: url.searchParams.get("symbol") ?? "", payload }); });
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
        if (dark !== (theme === "dark")) await page.keyboard.press("Control+m");
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
      body: JSON.stringify({ phase, images: runtime.images, records, financialRequests, initialFailures, diagnostics,
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
