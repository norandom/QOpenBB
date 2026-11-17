import { readFileSync } from "node:fs";
import { randomUUID } from "node:crypto";
import { execFile } from "node:child_process";
import { isAbsolute } from "node:path";
import type { Page, Locator } from "playwright-core";
import { test, expect, loginDisposableWorkspace } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/fixtures.ts";
import { observeApplication } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/diagnostics.ts";
import { readRuntimeDescriptor } from "../../verification/runtime-descriptor.ts";

const root = new URL("../../", import.meta.url);
const startCountText = process.env.QOPENBB_FMP_BROWSER_START_COUNT ?? "";
if (!/^(0|[1-9][0-9]*)$/.test(startCountText) || Number(startCountText) > 40)
  throw Error("Explicit initial FMP count must leave eight acquisitions within the approved 48-call cap");
const startCount = Number(startCountText);
const sourceRevision = process.env.QOPENBB_BROWSER_SOURCE_REVISION ?? "";
if (!/^[a-f0-9]{40}$/.test(sourceRevision)) throw Error("Exact runtime source revision receipt required");
const catalog = JSON.parse(readFileSync(new URL("contracts/widgets.json", root), "utf8"));
const galleryWidgets = JSON.parse(readFileSync(new URL("contracts/gallery/catalog.json", root), "utf8")).widgets;
if (Object.keys(galleryWidgets).some(id => Object.hasOwn(catalog, id))) throw Error("Canonical/gallery widget identity collision");
const installedCatalog = { ...catalog, ...galleryWidgets };
const starter = JSON.parse(readFileSync(new URL("contracts/apps.json", root), "utf8"))[0];
const cases = [
  ["equity_estimates_historical_fmp_obb", "estimated_revenue_avg"],
  ["equity_fundamental_revenue_per_geography_fmp_obb", "revenue"],
  ["equity_fundamental_income_growth_fmp_obb", "growth_revenue"],
  ["equity_price_quote_fmp_obb", "last_price"],
] as const;

async function proof() {
  const argv: string[] = JSON.parse(process.env.QOPENBB_BROWSER_PROOF_CMD ?? "null");
  if (!Array.isArray(argv) || argv.length < 2) throw Error("Reviewed identity/ledger proof helper required");
  const proofHome = process.env.QOPENBB_BROWSER_PROOF_HOME ?? (process.platform === "win32" ? process.env.USERPROFILE : process.env.HOME);
  if (!proofHome || !isAbsolute(proofHome)) throw Error("Native host absolute proof HOME required");
  const text = await new Promise<string>((resolve, reject) => execFile(argv[0], argv.slice(1),
    { windowsHide: true, timeout: 60000, maxBuffer: 1048576, encoding: "utf8", env: { ...process.env, HOME: proofHome } },
    (error, stdout) => error ? reject(Error("API identity/ledger proof failed")) : resolve(stdout)));
  const result = JSON.parse(text);
  expect(result.api_container).toMatch(/^[a-f0-9]{64}$/);
  expect(result.api_pid).toBeTruthy();
  expect(Number.isInteger(result.fmp_count)).toBe(true);
  return result;
}

async function cell(widget: Locator, field: string) {
  const target = widget.locator(`.ag-row[row-index="0"] [col-id="${field}"]`).first();
  for (let index = 0; index < 35 && !(await target.count()); index++) {
    await widget.locator(".ag-body-horizontal-scroll-viewport").evaluate((el, x) => { el.scrollLeft = x; }, index * 450);
    await widget.page().waitForTimeout(40);
  }
  await expect(target).toBeVisible();
  await target.scrollIntoViewIfNeeded();
  return target;
}

function numberMatches(text: string, expected: number) {
  const match = /^(-?\d+(?:\.(\d+))?)([KMBT])?(%)?$/.exec(text.replace(/[,\s$]/g, "").toUpperCase());
  if (!match) return false;
  const scale = ({ K: 1e3, M: 1e6, B: 1e9, T: 1e12 } as Record<string, number>)[match[3]] ?? 1;
  // Growth is a native ratio. Only an actually rendered percent sign changes display units.
  const divisor = match[4] ? 100 : 1;
  const quantum = scale / divisor * 10 ** -(match[2]?.length ?? 0);
  return Math.abs(Number(match[1]) * scale / divisor - expected) <= quantum / 2 + Math.abs(expected) * Number.EPSILON;
}

function csvRecords(text: string) {
  const rows: string[][] = []; let row: string[] = []; let field = ""; let quoted = false;
  const source = text.replace(/^\uFEFF/, "").replace(/^sep=,\r?\n/, "");
  for (let i = 0; i < source.length; i++) {
    const char = source[i];
    if (char === '"') {
      if (quoted && source[i + 1] === '"') { field += '"'; i++; }
      else quoted = !quoted;
    } else if (char === "," && !quoted) { row.push(field); field = ""; }
    else if ((char === "\r" || char === "\n") && !quoted) {
      if (char === "\r" && source[i + 1] === "\n") i++;
      row.push(field); if (row.some(value => value !== "")) rows.push(row); row = []; field = "";
    } else field += char;
  }
  expect(quoted, "CSV must close quoted fields").toBe(false);
  if (field || row.length) { row.push(field); rows.push(row); }
  return rows;
}

async function renameAndSave(page: Page, id: string, name: string) {
  // Arm before mutating so an ordinary autosave cannot race the explicit save shortcut.
  const posted = page.waitForResponse(r => r.request().method() === "POST" &&
    new URL(r.url()).pathname.endsWith("/pro/dash/sync") && r.request().postDataJSON()?.items?.[id]?.data?.name === name);
  await page.locator(`#tab-${id}`).click({ button: "right" });
  await page.getByRole("menuitem", { name: "Rename", exact: true }).click();
  const dialog = page.getByRole("dialog").filter({ has: page.getByRole("heading", { name: "Rename dashboard", exact: true }) });
  await dialog.getByRole("textbox").fill(name); await dialog.getByRole("textbox").press("Enter");
  await page.keyboard.press("Control+Shift+S");
  const response = await posted; expect(response.ok()).toBe(true);
  return response.request().postDataJSON().items[id];
}

async function csvExport(page: Page, widget: Locator, field: string, row: any, info: any, label: string) {
  await widget.locator("button:has(svg#list-unordered)").click();
  await page.getByRole("menuitem", { name: "Export", exact: true }).click();
  const dialog = page.getByRole("dialog").filter({ has: page.getByRole("heading", { name: "Export widget", exact: true }) });
  await dialog.getByRole("radio", { name: "CSV", exact: true }).click();
  await dialog.locator("#save-as").fill(label);
  const pending = page.waitForEvent("download");
  await dialog.getByRole("button", { name: "Export", exact: true }).click();
  const download = await pending;
  expect(await download.failure()).toBeNull();
  const path = info.outputPath(`${label}.csv`);
  await download.saveAs(path);
  const csv = readFileSync(path, "utf8");
  const [headers, ...records] = csvRecords(csv);
  const columns = catalog[label].data.table.columnsDefs;
  const column = (key: string) => {
    const heading = columns.find((c: any) => c.field === key)?.headerName;
    expect(heading).toBeTruthy(); expect(headers.filter(h => h === heading)).toHaveLength(1);
    return headers.indexOf(heading);
  };
  const identity = ["symbol", "region", "date", "period_ending"].filter(key => row[key] !== undefined && row[key] !== null);
  expect(identity.length).toBeGreaterThan(0);
  const indices = Object.fromEntries(identity.map(key => [key, column(key)]));
  const matches = records.filter(record => identity.every(key => {
    const actual = record[indices[key]];
    if (["date", "period_ending"].includes(key)) return Number.isFinite(Date.parse(actual)) &&
      new Date(actual).toISOString().slice(0, 10) === String(row[key]).slice(0, 10);
    return actual === String(row[key]);
  }));
  expect(matches, "CSV identity must select exactly the acquired row").toHaveLength(1);
  const exported = matches[0][column(field)];
  expect(numberMatches(exported, row[field]), "CSV intended column must preserve value at exported decimal precision").toBe(true);
  return { file: path, field, header: headers[column(field)], identity: Object.fromEntries(identity.map(key => [key, row[key]])),
    exported, responseValue: row[field], precision: "exported decimal quantum", bytes: Buffer.byteLength(csv) };
}

test("Batch A bounded native display save export recovery and fresh reopen", async ({ page, browser }, info) => {
  const runtime = await readRuntimeDescriptor(process.env.WORKSPACE_RUNTIME_PRIVATE!);
  const initialProof = await proof();
  expect(initialProof.fmp_count).toBe(startCount);
  const diagnostics: any[] = [];
  const requests: any[] = [];
  const responses: any[] = [];
  const reads: Promise<void>[] = [];
  const observations: any[] = [];
  const stored: any[] = [];
  const syncUrl = `${runtime.origin}/api/pro/dash/validate-and-sync`;
  let authorization = "";
  const loginReceipts: { path: string; status: number }[] = [];
  let sourceId = "";
  let phase = "setup";
  const watch = async (target: Page) => {
    diagnostics.push(await observeApplication(target));
    target.on("request", request => {
      const url = new URL(request.url());
      if (url.pathname.startsWith("/data/api/v1/")) requests.push({ phase, path: url.pathname, query: Object.fromEntries(url.searchParams) });
    });
    target.on("response", response => {
      const url = new URL(response.url());
      if (!url.pathname.startsWith("/data/api/v1/")) return;
      const read = response.json().then(payload => { responses.push({ phase, path: url.pathname,
        query: Object.fromEntries(url.searchParams), status: response.status(), payload }); });
      reads.push(read); void read.catch(() => undefined);
    });
    // Catalog discovery remains real. Only the app list is empty to prevent starter fanout.
    await target.route("**/data/apps.json", route => route.fulfill({ json: [] }));
  };
  const loginWithNativeBearer = async (target: Page) => {
    const pending = target.waitForResponse(response => {
      const url = new URL(response.url());
      return url.origin === runtime.origin && url.pathname === "/api/pro/login" &&
        response.request().method() === "POST" && response.status() === 200;
    });
    await loginDisposableWorkspace(target);
    const response = await pending;
    const token: unknown = (await response.json()).access_token;
    if (typeof token !== "string" || !token || /[\r\n\s]/.test(token))
      throw Error("Successful native login must provide a usable bearer token");
    authorization = `Bearer ${token}`;
    loginReceipts.push({ path: "/api/pro/login", status: response.status() });
  };
  const headers = (): Record<string, string> => {
    if (!authorization) throw Error("Authenticated native login required before protected control API access");
    return { authorization };
  };
  const serverRead = async (target: Page, id: string) => {
    const response = await target.request.get(syncUrl, { headers: headers(), maxRedirects: 0 });
    expect(response.status()).toBe(200);
    return (await response.json()).owned[id].content;
  };
  await watch(page);
  try {
    // Startup uses one login. A full 65-second cooldown precedes each browser login.
    await page.waitForTimeout(65000);
    await loginWithNativeBearer(page);
    await page.goto("/app/connections");
    await page.getByRole("button", { name: "Connect Backend", exact: true }).first().click();
    const dialog = page.getByRole("dialog").filter({ has: page.getByRole("heading", { name: "Connect backend", exact: true }) });
    await dialog.getByPlaceholder("OpenBB App").fill("Batch A bounded candidate");
    await dialog.getByPlaceholder("http://127.0.0.1:5056").fill(`${runtime.origin}/data`);
    const testBackend = dialog.getByRole("button", { name: "Test", exact: true });
    const duplicate = dialog.getByText('"Batch A bounded candidate" is already using this URL', { exact: true });
    await expect.poll(async () => (await testBackend.isEnabled()) || (await duplicate.isVisible())).toBe(true);
    if (await duplicate.isVisible()) {
      const discovered = await page.request.get(`${runtime.origin}/data/widgets.json`);
      expect(discovered.status()).toBe(200); expect(await discovered.json()).toEqual(installedCatalog);
      const listed = await page.request.get(syncUrl.replace(/dash\/validate-and-sync$/, "data-connectors/api-source"), { headers: headers(), maxRedirects: 0 });
      expect(listed.status()).toBe(200);
      const sources = (await listed.json()).filter((source: any) => source.name === "Batch A bounded candidate" && source.url === `${runtime.origin}/data`);
      expect(sources).toHaveLength(1); sourceId = sources[0].id;
      await dialog.getByRole("button", { name: "Close", exact: true }).click();
    } else {
      const discovered = page.waitForResponse(r => new URL(r.url()).pathname === "/data/widgets.json");
      await testBackend.click(); expect(await (await discovered).json()).toEqual(installedCatalog);
      await expect(dialog.getByText("Test successful", { exact: true })).toBeVisible();
      const posted = page.waitForRequest(r => r.method() === "POST" && new URL(r.url()).pathname.includes("/pro/data-connectors/api-source/"));
      await dialog.getByRole("button", { name: /^add$/i }).click();
      sourceId = new URL((await posted).url()).pathname.split("/").at(-1)!;
    }
    await expect(dialog).not.toBeVisible();
    await page.locator("#tabs").getByRole("button").first().click();
    await page.getByRole("button", { name: /New Dashboard/ }).click();
    await expect(page).toHaveURL(url => url.origin === runtime.origin && /^\/app\/[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/.test(url.pathname));
    const blankId = new URL(page.url()).pathname.split("/").at(-1)!;
    await expect(page.locator(`#tab-${blankId}`)).toBeVisible();
    await expect(page.getByRole("main").getByRole("button", { name: "Add widgets", exact: true })).toBeVisible();
    const blank = await renameAndSave(page, blankId, "Batch A empty safe landing");
    expect(blank.data.widgets).toHaveLength(0);
    expect(syncUrl).toBeTruthy();
    const items: Record<string, any> = {};
    for (const [widgetId] of cases) {
      const template = starter.tabs.Data.layout.find((item: any) => item.i === widgetId);
      const params = structuredClone(template.state.params);
      const initialParams = { ...params, ...(widgetId === cases[0][0] ? { symbol: "" } : {}) };
      const definition = structuredClone(catalog[widgetId]);
      const id = randomUUID(); const widgetInstance = randomUUID();
      const widget = { ...definition, id: widgetInstance, widgetId, innerTab: "", groupId: "",
        external: true, sourceId, sourceName: "Batch A bounded candidate", connectionType: "advanced-backend",
        endpointHeaders: [], endpoint: { url: `${runtime.origin}/data${definition.endpoint}`, method: "GET" },
        refetchInterval: false, storage: { params: initialParams },
        params: definition.params.map((p: any) => ({ ...p, label: p.label ?? p.paramName, type: p.type ?? "text", options: p.options ?? [] })) };
      const content = structuredClone(blank);
      content.index = id;
      content.data = { ...content.data, name: `Batch A ${definition.name}`, type: "custom", widgets: [widget], groups: [],
        gridLayout: { "": [{ i: widgetInstance, x: 0, y: 0, w: 40, h: 24 }] }, currentTab: "" };
      items[id] = content; stored.push({ id, widgetId, params, initialParams, widgetInstance });
    }
    const treeResponse = await page.request.get(syncUrl, { headers: headers(), maxRedirects: 0 });
    expect(treeResponse.status()).toBe(200);
    const owned: Record<string, { content: any }> = (await treeResponse.json()).owned;
    const roots = Object.entries(owned).filter(([, entry]) => entry.content?.isRoot === true);
    expect(roots).toHaveLength(1);
    const [rootId, rootEntry] = roots[0];
    const rootContent = structuredClone(rootEntry.content);
    expect(rootContent.index).toBe(rootId); expect(rootContent.children).toContain(blankId);
    for (const item of stored) {
      expect(owned).not.toHaveProperty(item.id);
      items[item.id].parentId = rootId;
    }
    // Native normalization retains only items reachable from the owned root tree.
    items[rootId] = { ...rootContent, children: [...rootContent.children, ...stored.map(item => item.id)] };
    const imported = await page.request.post(syncUrl.replace(/validate-and-sync$/, "sync"), { headers: headers(), data: { items }, maxRedirects: 0 });
    expect(imported.ok()).toBe(true);
    observations.push({ pass: "native-rooted-import", path: "/api/pro/dash/sync", status: imported.status(),
      rootId, newDashboardIds: stored.map(item => item.id), priorChildren: rootContent.children.length });
    const persistedRoot = await serverRead(page, rootId);
    expect(persistedRoot.children.slice(0, rootContent.children.length)).toEqual(rootContent.children);
    for (const item of stored) expect(persistedRoot.children.filter((id: string) => id === item.id)).toHaveLength(1);
    for (const item of stored) {
      const content = await serverRead(page, item.id);
      expect(content.parentId).toBe(rootId);
      expect(content.data.widgets[0].refetchInterval).toBe(false);
      expect(content.data.widgets[0].storage.params).toEqual(item.initialParams);
    }
    const visit = async (target: Page, item: any, pass: string) => {
      phase = pass;
      const definition = catalog[item.widgetId];
      const pathname = `/data${definition.endpoint}`;
      const acquisition = target.waitForResponse(r => new URL(r.url()).pathname === pathname && new URL(r.url()).searchParams.get("symbol") === "MSFT", { timeout: 120000 });
      await target.goto(`/app/${item.id}`);
      if (pass === "initial" && item.widgetId === cases[0][0]) {
        const widget = target.locator(`#workarea .widget-${item.widgetId}`);
        const error = widget.getByText("Invalid financial query parameters.", { exact: true });
        await expect(error).toBeVisible();
        // Existing native retry is allowed only for pre-I/O validation; never for an acquisition.
        await target.waitForTimeout(1500);
        await expect(error).toBeVisible();
        const rejected = requests.filter(x => x.path === pathname && !x.query.symbol);
        expect(rejected.length).toBeGreaterThanOrEqual(1); expect(rejected.length).toBeLessThanOrEqual(2);
        const beforeRecovery = await proof(); expect(beforeRecovery.fmp_count).toBe(startCount);
        await info.attach("pre-io-validation-error", { body: await widget.screenshot(), contentType: "image/png" });
        const input = widget.getByRole("textbox", { name: "Symbol", exact: true });
        await expect(target.locator(`#tab-${item.id}`)).toBeVisible();
        await input.fill("MSFT"); await input.press("Tab");
        await expect(error).not.toBeVisible();
        observations.push({ pass: "recovery", widgetId: item.widgetId, expectedStatus: 422,
          preIoRejectedRequests: rejected.length, beforeRecovery });
      }
      const response = await acquisition;
      expect(response.status(), "Entitlement/consumer failure is blocked acceptance; never auto-rerun").toBe(200);
      const payload = await response.json();
      expect(payload.results.length).toBeGreaterThan(0);
      const metadata = payload.extra.results_metadata.__qopenbb_financial__;
      expect(metadata.provider).toBe("fmp");
      expect(metadata.effective_query).toMatchObject(Object.fromEntries(Object.entries(item.params).filter(([name]) => name !== "provider")));
      expect(metadata.dataset).toBe(definition.endpoint.replace("/api/v1/", ""));
      expect(Number.isFinite(Date.parse(metadata.retrieved_at))).toBe(true);
      const widget = target.locator(`#workarea .widget-${item.widgetId}`);
      await expect(widget).toBeVisible();
      const row = payload.results[0];
      const field = cases.find(([id]) => id === item.widgetId)![1];
      expect(metadata.fields[field]).toMatchObject({ scale: 1, unit: field === "growth_revenue" ? "ratio" : field === "last_price" ? "currency/share" : "currency" });
      expect(Number.isFinite(row[field])).toBe(true);
      const valueCell = await cell(widget, field);
      await expect.poll(async () => numberMatches(await valueCell.innerText(), row[field])).toBe(true);
      if (row.symbol) await expect(await cell(widget, "symbol")).toHaveText(row.symbol);
      if (row.region) await expect(await cell(widget, "region")).toHaveText(row.region);
      if (row.reported_currency) await expect(await cell(widget, "reported_currency")).toHaveText(row.reported_currency);
      const exported = pass === "initial" ? await csvExport(target, widget, field, row, info, item.widgetId) : null;
      if (pass === "initial") {
        item.savedName = `Batch A verified ${definition.name}`;
        await renameAndSave(target, item.id, item.savedName);
      }
      const saved = await serverRead(target, item.id);
      expect(saved.data.name).toBe(item.savedName);
      expect(saved.data.widgets).toHaveLength(1);
      expect(saved.data.widgets[0]).toMatchObject({ widgetId: item.widgetId, refetchInterval: false, storage: { params: item.params } });
      observations.push({ pass, widgetId: item.widgetId, field, displayed: await valueCell.innerText(), row, metadata, exported });
      await widget.screenshot({ path: info.outputPath(`${pass}-${item.widgetId}.png`) });
    };
    for (const item of stored) await visit(page, item, "initial");
    const midpoint = await proof();
    expect(midpoint).toMatchObject({ api_container: initialProof.api_container, api_pid: initialProof.api_pid, fmp_count: startCount + 4 });
    const landingPath = `/app/${blankId}`;
    const parkedRequests = requests.length;
    await page.goto(landingPath);
    await expect(page).toHaveURL(`${runtime.origin}${landingPath}`);
    await expect(page.getByRole("main").getByRole("button", { name: "Add widgets", exact: true })).toBeVisible();
    await expect(page.locator("#workarea [data-widget-id]")).toHaveCount(0);
    const userUrl = `${runtime.origin}/api/pro/user`;
    const userBefore = await page.request.get(userUrl, { headers: headers(), maxRedirects: 0 });
    expect(userBefore.status()).toBe(200);
    const previousSettings = (await userBefore.json()).pro_display_settings;
    const nextSettings = { ...previousSettings, lastVisitedPage: landingPath };
    const settingsSaved = await page.request.post(`${runtime.origin}/api/pro/display-settings`, {
      headers: headers(), data: nextSettings, maxRedirects: 0 });
    expect(settingsSaved.status()).toBe(200);
    expect((await serverRead(page, blankId)).data.widgets).toHaveLength(0);
    const userResponse = await page.request.get(userUrl, { headers: headers(), maxRedirects: 0 });
    expect(userResponse.status()).toBe(200);
    expect((await userResponse.json()).pro_display_settings).toEqual(nextSettings);
    expect(requests).toHaveLength(parkedRequests);
    observations.push({ pass: "native-empty-landing-setting", landingPath,
      allOtherSettingsPreserved: true, financialRequests: parkedRequests });
    await page.close();
    await new Promise(resolve => setTimeout(resolve, 65000));
    const context = await browser.newContext({ baseURL: runtime.origin, serviceWorkers: "block", viewport: { width: 1600, height: 1000 } });
    try {
      const reopened = await context.newPage(); await watch(reopened);
      await loginWithNativeBearer(reopened);
      await expect(reopened).toHaveURL(`${runtime.origin}${landingPath}`);
      await expect(reopened.locator("#workarea [data-widget-id]")).toHaveCount(0);
      expect(requests).toHaveLength(parkedRequests);
      for (const item of stored) await visit(reopened, item, "reopen");
    } finally { await context.close(); }
    await Promise.all(reads);
    const finalProof = await proof();
    expect(finalProof).toMatchObject({ api_container: initialProof.api_container, api_pid: initialProof.api_pid, fmp_count: startCount + 8 });
    const invalidRequests = requests.filter(x => !x.query.symbol);
    expect(invalidRequests.length).toBeGreaterThanOrEqual(1); expect(invalidRequests.length).toBeLessThanOrEqual(2);
    expect(responses.filter(x => x.status === 422)).toHaveLength(invalidRequests.length);
    const valid = requests.filter(x => x.query.symbol === "MSFT");
    expect(valid).toHaveLength(8); expect(requests).toHaveLength(8 + invalidRequests.length);
    expect(valid.map(x => x.path)).toEqual([...cases, ...cases].map(([id]) => `/data${catalog[id].endpoint}`));
    for (const [index, request] of valid.entries()) expect(request.query).toEqual(Object.fromEntries(
      Object.entries(stored[index % 4].params).map(([key, value]) => [key, String(value)])));
    for (const diagnostic of diagnostics) {
      const invalidPath = `/data${catalog[cases[0][0]].endpoint}`;
      expect(diagnostic.consoleErrors.filter((x: any) => !(x.path === invalidPath && /Failed to load resource.*422/.test(x.message)))).toEqual([]);
      expect(diagnostic.errors).toEqual([]);
      expect(diagnostic.failures.filter((x: any) => !(x.path === invalidPath && x.status === 422))).toEqual([]);
      expect(diagnostic.requestFailures).toEqual([]);
    }
  } finally {
    await Promise.allSettled(reads);
    await info.attach("batch-a-own-response-receipts", { contentType: "application/json", body: JSON.stringify({
      images: runtime.images, runtimeSourceRevision: sourceRevision, initialProof, requests, responses, observations, diagnostics, loginReceipts,
      limitations: ["Native authenticated dashboard API import; no app-template import coverage.",
        "Recovery uses real pre-I/O invalid-symbol rejection then the first of eight provider acquisitions; native validation retry capped at two requests.",
        "Eight browser acquisitions follow the explicitly supplied cumulative initial count; local image bytes only, CI/release acceptance separate."] }) });
  }
});
