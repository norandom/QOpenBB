import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import type { Page } from "../node_modules/@playwright/test/index.js";
import { expect, test } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/toolchain";
import { observeApplication } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/diagnostics";
import { saveDashboard } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/editor";
import { addWidget, newDashboard, signIn } from "./workspace.mts";

const phase = process.env.JOURNEY_PHASE;
const checkpoint = process.env.JOURNEY_CHECKPOINT!;
const fixtures = resolve(import.meta.dirname, "../financial-real-inputs");
const load = (file: string) => JSON.parse(readFileSync(resolve(fixtures, file), "utf8"));
const registry = load("journey-inputs.json");
const selected = registry.cases[registry.default_case];
const positive = load(selected.request);
const negative = load(registry.cases["aapl-historical-strict"].request);
const oracle = load(selected.expected)[selected.expected_key];
const evaluator = (page: Page) => page.locator("#workarea .widget-qopenbb_issuer_fcf_yield");
const reader = (page: Page) => page.locator("#workarea .widget-qopenbb_saved_model_output");
const result = (page: Page) => evaluator(page).getByRole("region", { name: "Saved modeling result" });

async function submit(page: Page, request: typeof positive) {
  await page.getByLabel("Input snapshot JSON").fill(JSON.stringify(request.inputs));
  await page.getByLabel("Effective date").fill(request.assumptions.effective_date);
  await page.getByLabel("Assumption version").fill(request.assumptions.version);
  const sign = page.getByRole("combobox").filter({hasText: /CapEx sign convention|Cash outflow is negative|Spending is positive/i});
  if (!(await sign.textContent())?.includes("Cash outflow is negative")) {
    await sign.click();
    await page.getByRole("option", { name: "Cash outflow is negative" }).click();
  }
  const response = page.waitForResponse(r => r.url().endsWith("/modeling/v1/evaluations") && r.request().method() === "POST");
  await page.getByRole("button", { name: "Evaluate FCF yield" }).click();
  const saved = await response;
  expect(saved.status()).toBe(200);
  const run = await saved.json();
  await expect(result(page).getByText(run.run_id, { exact: true })).toBeVisible();
  return run.run_id as string;
}

async function confirmYield(page: Page, id: string) {
  const view = result(page);
  await expect(view.getByText(id, { exact: true })).toBeVisible();
  await expect(view.getByText(oracle.value, { exact: true })).toBeVisible();
  await expect(view.getByText("verified", { exact: true })).toBeVisible();
  await expect(view.getByText(/capex_sign = cash_outflow_negative/)).toBeVisible();
  await view.getByText("Checks and verification", { exact: true }).click();
  await expect(view.getByText(/Independent verification · match/)).toBeVisible();
  await view.getByText("Trace", { exact: true }).click();
  await expect(view.getByText(`fcf_yield v1 · ${oracle.trace.expression}`, { exact: true })).toBeVisible();
  await expect(view.getByText("Source records " + oracle.trace.source_record_ids.join(", "), {exact: true})).toBeVisible();
}

async function verifyProviderView(page: Page) {
  await page.goto("/app/connections");
  await page.getByRole("button", {name: "Connect Backend", exact: true}).first().click();
  const dialog = page.getByRole("dialog").filter({has: page.getByPlaceholder("OpenBB App")});
  await dialog.getByPlaceholder("OpenBB App").fill("Journey provider data");
  await dialog.getByPlaceholder("http://127.0.0.1:5056").fill(process.env.WORKSPACE_FRONTEND_ORIGIN + "/data");
  const testBackend = dialog.getByRole("button", {name: "Test", exact: true});
  const duplicate = dialog.getByText('"Journey provider data" is already using this URL', {exact: true});
  await expect.poll(async () => await testBackend.isEnabled() || await duplicate.isVisible()).toBe(true);
  if (await duplicate.isVisible()) {
    await dialog.getByRole("button", {name: "Close", exact: true}).click();
  } else {
    await testBackend.click();
    await expect(dialog.getByText("Test successful", {exact: true})).toBeVisible();
    await dialog.getByRole("button", {name: /^add$/i}).click();
  }
  await expect(dialog).not.toBeVisible();
  const providerDashboard = await newDashboard(page);
  await addWidget(page, "Profile");
  await saveDashboard(page);
  await page.goto(providerDashboard);
  const profile = page.locator("#workarea .widget-equity_profile_fmp_obb");
  const field = profile.getByPlaceholder("Symbol", {exact: true});
  const read = page.waitForResponse(r => {
    const url = new URL(r.url());
    return url.pathname === "/data/api/v1/equity/profile" && url.searchParams.get("symbol") === "AAPL";
  });
  await profile.getByRole("combobox", {name: "Company name", exact: true}).fill("Apple");
  await page.getByRole("listbox").getByRole("option").filter({hasText: "Apple Inc. (AAPL)"}).click();
  await expect(field).toHaveValue("AAPL");
  const response = await read;
  expect(response.status()).toBe(200);
  const payload = await response.json();
  const row = payload.results[0];
  expect(row).toMatchObject({symbol: "AAPL", currency: "USD"});
  await expect(profile.getByRole("status")).toContainText(row.name);
  await expect(profile.getByRole("gridcell", {name: row.symbol, exact: true})).toBeVisible();
  await expect(profile.getByRole("gridcell", {name: row.currency, exact: true})).toBeVisible();
}

test("analyst evaluates, saves and reopens the FCF yield dashboard", async ({page}, info) => {
  await signIn(page);
  const diagnostics = await observeApplication(page);
  const posts: string[] = [];
  page.on("request", request => {
    if (request.method() === "POST" && request.url().endsWith("/modeling/v1/evaluations")) posts.push("evaluate");
  });
  if (phase === "evaluate") {
    const dashboard = await newDashboard(page);
    await addWidget(page, "Issuer FCF yield");
    const withheld = await submit(page, negative);
    await expect(result(page).getByText("withheld", {exact: true})).toBeVisible();
    await expect(result(page).getByText("—", {exact: true})).toBeVisible();
    const id = await submit(page, positive);
    expect(id).not.toBe(withheld);
    await confirmYield(page, id);
    await page.getByLabel("Assumption version").fill("changed");
    await expect(page.getByText("Showing a stale saved result.")).toBeVisible();
    const final = await submit(page, positive);
    await addWidget(page, "Saved model output");
    await reader(page).getByLabel("Run ID", {exact: true}).fill(final);
    await reader(page).getByLabel("Output ID", {exact: true}).fill("fcf_yield");
    await expect(reader(page).getByText(oracle.value, {exact: true})).toBeVisible();
    const sync = await saveDashboard(page);
    const widgets = sync.items[dashboard.split("/").at(-1)!].data.widgets;
    expect(widgets.some((w: {storage?: {params?: {run_id?: string}}}) => w.storage?.params?.run_id === final)).toBe(true);
    writeFileSync(checkpoint, JSON.stringify({dashboard, id: final}), {mode: 0o600});
    expect(posts).toHaveLength(3);
  } else {
    const {dashboard, id} = JSON.parse(readFileSync(checkpoint, "utf8"));
    await page.goto(dashboard);
    await expect(page.getByLabel("Input snapshot JSON")).toHaveValue(JSON.stringify(positive.inputs));
    if (phase === "reopen") {
      await confirmYield(page, id);
      await expect(reader(page).getByText(oracle.value, {exact: true})).toBeVisible();
      const read = page.waitForResponse(r => r.url().includes("/modeling/v1/widget-results") && r.status() === 200);
      await reader(page).getByRole("button", {name: "Refresh saved result"}).click();
      await read;
      await expect(result(page).getByText(id, {exact: true})).toBeVisible();
    } else {
      expect(phase).toBe("unavailable");
      await expect(evaluator(page).getByRole("alert").filter({hasText: /Modeling request failed|service unavailable/i})).toBeVisible();
      await verifyProviderView(page);
    }
    expect(posts).toHaveLength(0);
  }
  expect(diagnostics.errors).toEqual([]);
  const outageRead = (path?: string) => phase === "unavailable" &&
    !!path && /^\/modeling\/v1\/(runs\/[0-9a-f]{32}|widget-results)$/.test(path);
  if (phase === "unavailable") expect(diagnostics.failures.length).toBeGreaterThan(0);
  expect(diagnostics.failures.filter(item => !(outageRead(item.path) && item.status === 503))).toEqual([]);
  expect(diagnostics.consoleErrors.filter(item => !(outageRead(item.path) && /503/.test(item.message)))).toEqual([]);
  expect(diagnostics.requestFailures).toEqual([]);
  await info.attach("modeling-journey", {contentType: "application/json", body: JSON.stringify({
    phase, evaluationPosts: posts.length, errors: diagnostics.errors.length, failures: diagnostics.failures,
    consoleErrorCount: diagnostics.consoleErrors.length, requestFailures: diagnostics.requestFailures,
  })});
});
