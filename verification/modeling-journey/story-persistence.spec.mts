import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { readFile, writeFile } from "node:fs/promises";
import type { Page } from "../../vendor/workspace/terminalpro/node_modules/@playwright/test/index";
import { expect, test } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/toolchain";
import { expectApplicationDiagnostics, observeApplication } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/diagnostics";
import { saveDashboard } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/editor";
import { inspectMacro, inspectPrices, runsFor } from "./story-selection-evidence.mts";
import { connectDataSource, openStory, signIn } from "./workspace.mts";

const owner = "story-owner@example.com";
const date = "2026-11-13";
const checkpoint = process.env.JOURNEY_CHECKPOINT!;
const evaluations = "/modeling/v1/evaluations";
const runPath = (id: string) => "/modeling/v1/runs/" + id;
const hash = (value: unknown) => createHash("sha256").update(JSON.stringify(value)).digest("hex");
const phase = process.env.JOURNEY_PHASE;
const returnsSeries = { input: ["DBC"], result: ["XLK"] };

async function chartChoices(page: Page, change: boolean) {
  for (const [lane, value] of [["input", "bar"], ["result", "line"]]) {
    const control = page.getByRole("combobox", { name: "Price returns " + lane + " chart type", exact: true });
    const group = page.getByRole("group", { name: "Price returns " + lane + " chart", exact: true });
    const hidden = group.getByRole("checkbox", { name: lane === "input" ? "XLK" : "DBC", exact: true });
    if (change) {
      await control.selectOption(value);
      await hidden.uncheck();
    }
    await expect(hidden).not.toBeChecked();
    await expect(control).toHaveValue(value);
  }
}

async function exportApp(page: Page, dashboard: string, state: unknown) {
  await page.locator("#tab-" + dashboard.split("/").at(-1)).click({ button: "right" });
  const menu = page.getByRole("menuitem", { name: /Export apps.json/ });
  await expect(menu, "Saved story offers dashboard template export").not.toHaveClass(/cursor-not-allowed/, { timeout: 3000 });
  await menu.click();
  const dialog = page.getByRole("dialog").filter({ has: page.getByRole("heading", { name: "Export App", exact: true }) });
  await dialog.getByPlaceholder("Enter app name...").fill("Saved price study");
  await dialog.getByPlaceholder("Describe what this app does and when to use it...").fill("Saved DBC and XLK comparison");
  const download = page.waitForEvent("download");
  await dialog.getByRole("button", { name: "Download App" }).click();
  const app = JSON.parse(await readFile((await (await download).path())!, "utf8"));
  const tab = "Research";
  expect(app).toEqual({
    name: "Saved price study", description: "Saved DBC and XLK comparison", img: "", img_light: "", img_dark: "",
    allowCustomization: true, groups: [], tabs: { [tab]: { id: tab, name: tab, layout: [{
      i: "research_story", x: expect.any(Number), y: expect.any(Number), w: expect.any(Number), h: expect.any(Number),
      groups: [], state: { storage: { researchStory: state } },
    }] } },
  });
  await writeFile(test.info().outputPath("exported-story.json"), JSON.stringify(app, null, 2) + "\n", { mode: 0o600 });
  return hash(app);
}

async function saveStudy(page: Page) {
  await connectDataSource(page, "Journey provider data");
  const contract = new URL("../../contracts/consumers/research-stories/story.v1.json", import.meta.url);
  const config = JSON.parse(await readFile(contract, "utf8")).catalog.default_state;
  const diagnostics = await observeApplication(page);
  const submitted = page.waitForRequest(req => req.method() === "POST" && new URL(req.url()).pathname === evaluations);
  const pending = runsFor(page, date);
  const story = await openStory(page);
  const { price, macro } = await pending;
  await chartChoices(page, true);
  const financial = await inspectPrices(story, price, ["DBC", "XLK"], returnsSeries);
  const context = await inspectMacro(story, macro, price);
  const dashboard = new URL(page.url()).pathname;
  const sync = await saveDashboard(page);
  const widgets = sync.items[dashboard.split("/").at(-1)!].data.widgets;
  expect(widgets).toHaveLength(1);
  const state = widgets[0].storage.researchStory;
  expect(widgets[0].storage).toEqual({ researchStory: state });
  const allowed = ["id", "widgetId", "type", "name", "innerTab", "isMinimized", "originalH", "showTitle",
    "disableRetrievalForCopilot", "params", "storage"];
  expect(Object.keys(widgets[0]).filter(key => !allowed.includes(key))).toEqual([]);
  expect(widgets[0]).toMatchObject({ widgetId: "research_story", type: "research_story", params: [] });
  config.charts.returns.input.chart_type = "bar";
  config.charts.returns.result.chart_type = "line";
  config.charts.returns.input.series = ["left_close"];
  config.charts.returns.result.series = ["right_momentum"];
  expect(new Date(state.cutoff.evaluated_at).toISOString()).toBe(state.cutoff.evaluated_at);
  expect(new Date(price.inputs.cutoff.evaluated_at).toISOString()).toBe(state.cutoff.evaluated_at);
  expect(state).toEqual({ ...config, schedule: { calendar_id: "NYSE_ARCA", schedule_revision: "nyse-arca.2026r1" },
    cutoff: { ...price.inputs.cutoff, evaluated_at: state.cutoff.evaluated_at }, run_refs: { comparison: price.run_id, regime: macro.run_id } });
  const exportDigest = await exportApp(page, dashboard, state);
  const histories = Object.fromEntries(["left", "right"].map((side, index) => {
    const rows = price.inputs.tables.find(table => table.table_id === side + "_closes")!.rows;
    return [["DBC", "XLK"][index], rows.map(row => [row.observation_date, row.value])];
  }));
  const fixture = { histories, request: (await submitted).postDataJSON() };
  await writeFile(join(dirname(checkpoint), "history-fixture.json"), JSON.stringify(fixture), { mode: 0o600 });
  expectApplicationDiagnostics(diagnostics);
  await writeFile(checkpoint, JSON.stringify({ dashboard, state, real: { price: hash(price), macro: hash(macro),
    financial, context, exportDigest } }), { mode: 0o600 });
}

async function reopenStudy(page: Page, unavailable: boolean) {
  const saved = JSON.parse(await readFile(checkpoint, "utf8"));
  const ids = saved.state.run_refs;
  const idsToRead = [unavailable ? saved.controlled.foreign : ids.comparison, ids.regime];
  const reads = idsToRead.map(id => page.waitForResponse(response =>
    new URL(response.url()).pathname === runPath(id) && response.request().method() === "GET"));
  await signIn(page, owner);
  const diagnostics = await observeApplication(page);
  if (new URL(page.url()).pathname !== saved.dashboard) await page.goto(saved.dashboard);
  const responses = await Promise.all(reads);
  expect(responses.map(r => r.status())).toEqual(unavailable ? [404, 404] : [200, 200]);
  const story = page.locator("#workarea .widget-research_story");
  if (unavailable) {
    for (const response of responses) {
      expect(await response.json()).toEqual({
        code: "not_found", retryable: false, correlation_id: expect.stringMatching(/^[a-f0-9]{32}$/),
      });
    }
    await expect(story.getByRole("region", { name: "Price returns from FMP" }).getByRole("alert")).toContainText("unavailable");
    await expect(story.getByRole("region", { name: /DFII10 real yields/ }).getByRole("alert")).toContainText("unavailable");
    const verdict = story.getByRole("region", { name: "Verdict" }).getByRole("status");
    await expect(verdict).toContainText("Insufficient data. DBC and XLK · observation date " + date);
    await expect(verdict).toContainText("Saved run unavailable.");
    await expect(story.getByRole("figure")).toHaveCount(0);
    const missing = new Set(idsToRead.map(runPath));
    expect(diagnostics.errors).toEqual([]);
    expect(diagnostics.requestFailures).toEqual([]);
    expect(diagnostics.failures.filter(failure => !(failure.status === 404 && missing.has(failure.path)))).toEqual([]);
    expect(diagnostics.consoleErrors.filter(error => !(error.path && missing.has(error.path) && /404/.test(error.message)))).toEqual([]);
    return;
  }
  const [price, macro] = await Promise.all(responses.map(response => response.json()));
  expect([hash(price), hash(macro)]).toEqual([saved.real.price, saved.real.macro]);
  await expect(story.getByRole("combobox", { name: "Commodity proxy" })).toContainText("DBC");
  await expect(story.getByRole("combobox", { name: "Technology proxy" })).toContainText("XLK");
  await expect(story.getByLabel("Observation date", { exact: true })).toHaveValue(date);
  await chartChoices(page, false);
  expect(await inspectPrices(story, price, ["DBC", "XLK"], returnsSeries)).toEqual(saved.real.financial);
  expect(await inspectMacro(story, macro, price)).toEqual(saved.real.context);
  expect(await exportApp(page, saved.dashboard, saved.state)).toBe(saved.real.exportDigest);
  const authorization = await responses[0].request().headerValue("authorization");
  if (!authorization) throw new Error("Missing owner session on saved read");
  expectApplicationDiagnostics(diagnostics);
  await seedUnavailableReferences(page, authorization, saved);
}

async function seedUnavailableReferences(page: Page, authorization: string, saved: {
  dashboard: string; state: { run_refs: { regime: string } }; controlled: { foreign: string }
}) {
  // Close the loaded dashboard before replacing its reference through ordinary owner sync.
  const path = "/api/pro/dash/sync";
  const headers = { authorization };
  const api = page.context().request;
  await page.close();
  const response = await api.get(path, { headers });
  expect(response.status()).toBe(200);
  const id = saved.dashboard.split("/").at(-1)!;
  const item = (await response.json()).owned[id].content;
  const original = item.data.widgets[0].storage.researchStory;
  expect(original).toEqual(saved.state);
  original.run_refs.comparison = saved.controlled.foreign;
  const sync = await api.post(path, { headers, data: { items: { [id]: item } } });
  expect(sync.status()).toBe(200);
  const stored = await api.get(path, { headers });
  expect(stored.status()).toBe(200);
  expect((await stored.json()).owned[id].content.data.widgets[0].storage.researchStory.run_refs)
    .toEqual({ comparison: saved.controlled.foreign, regime: saved.state.run_refs.regime });
}

test("packaged saved research story persistence", async ({ page }, info) => {
  const posts: string[] = [];
  const historyRequests: string[] = [];
  page.on("request", req => {
    const path = new URL(req.url()).pathname;
    if (/\/(equity\/price\/historical|economy\/fred_series)$/.test(path)) historyRequests.push(path);
    if (req.method() === "POST" && path === evaluations) posts.push(evaluations);
  });
  if (phase === "save") {
    await signIn(page, owner);
    await saveStudy(page);
  } else await reopenStudy(page, phase === "unavailable");
  expect(historyRequests).toEqual([]);
  expect(posts).toHaveLength(phase === "save" ? 2 : 0);
  await writeFile(info.outputPath("story-persistence.json"), JSON.stringify({
    phase, browserEvaluations: posts.length, directHistoryRequests: historyRequests.length, diagnostics: phase === "unavailable" ?
      "only expected unavailable-reference 404 responses" : "clean",
    ordinaryAccountLogins: ["owner"],
    savedReadStatus: phase === "unavailable" ? { foreignComparison: 404, deletedRegime: 404 } :
      { comparison: 200, regime: 200 }, ...JSON.parse(await readFile(checkpoint, "utf8")),
  }, null, 2), { mode: 0o600 });
});
