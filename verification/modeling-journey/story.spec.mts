import { constants } from "node:fs";
import { access, writeFile } from "node:fs/promises";
import { join } from "node:path";
import type { Response } from "../node_modules/@playwright/test/index.js";
import { expect, test } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/toolchain";
import { observeApplication } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/diagnostics";
import { connectDataSource, signIn } from "./workspace.mts";

const title = "Commodities versus Technology";
const evaluations = "/modeling/v1/evaluations";
const observationDate = "2026-11-13";

async function modeling(action: "stop" | "start") {
  const directory = process.env.JOURNEY_SERVICE_CONTROL;
  if (!directory) throw new Error("Use the packaged story runner for modeling lifecycle control");
  await writeFile(join(directory, action), "", { flag: "wx", mode: 0o600 });
  await expect.poll(() => access(join(directory, action + ".done"), constants.F_OK)
    .then(() => true, () => false), { timeout: 75_000 }).toBe(true);
}

function comparison(response: Response) {
  const request = response.request();
  return new URL(response.url()).pathname === evaluations && request.method() === "POST" &&
    request.postDataJSON()?.acquisition?.dataset_id === "story.etf_pair";
}

test("packaged research story opens from Apps and retries in the same dashboard after modeling restarts", async ({ page }, info) => {
  await signIn(page);
  await connectDataSource(page, "Journey provider data");
  const catalog = await page.request.get("/data/apps.json");
  expect(catalog.ok()).toBe(true);
  const apps = (await catalog.json()).filter((entry: { name: string }) => entry.name === title);
  expect(apps).toHaveLength(1);
  const layout = apps[0].tabs.Research.layout;
  expect(layout).toHaveLength(1);
  expect(layout[0]).toMatchObject({
    i: "research_story",
    state: { storage: { researchStory: { selection: {
      commodity_symbol: "DBC", technology_symbol: "XLK", observation_date: observationDate,
    } } } },
  });
  await page.getByRole("link", { name: "Apps", exact: true }).click();
  const app = page.getByRole("button").filter({ has: page.getByText(title, { exact: true }) });
  await expect(app).toHaveCount(1);
  await modeling("stop");
  const diagnostics = await observeApplication(page);
  const rejected = page.waitForResponse(comparison);
  await app.click();
  const shell = page.locator("#workarea [data-widget-id]");
  await expect(shell).toHaveCount(1);
  await shell.scrollIntoViewIfNeeded();
  const story = shell.locator(".widget-research_story");
  await expect(story.getByRole("combobox", { name: "Commodity proxy", exact: true })).toContainText("DBC");
  await expect(story.getByRole("combobox", { name: "Technology proxy", exact: true })).toContainText("XLK");
  await expect(story.getByLabel("Observation date", { exact: true })).toHaveValue(observationDate);
  expect((await rejected).status()).toBe(503);
  const returns = story.getByRole("region", { name: "Price returns from FMP", exact: true });
  await expect(returns.getByRole("alert")).toHaveText("The evaluation outcome is unknown.");
  await expect(story.getByRole("button", { name: "Retry real yields", exact: true })).toBeVisible();
  const dashboard = page.url();
  expect(new URL(dashboard).pathname).toMatch(/^\/app\/[\da-f-]{36}$/);

  await modeling("start");
  const recovered = page.waitForResponse(comparison, { timeout: 75_000 });
  await returns.getByRole("button", { name: "Retry proxy comparison", exact: true }).click();
  const response = await recovered;
  expect(response.status()).toBe(200);
  const run = await response.json();
  const spread = run.outputs.find((output: { output_id: string }) => output.output_id === "momentum_spread");
  expect(spread).toMatchObject({ status: "verified", unit: "percentage_points" });
  const verdict = story.getByRole("region", { name: "Verdict", exact: true });
  const exactSpread = `${Number(spread.value) > 0 && !spread.value.startsWith("+") ? "+" : ""}${spread.value} pp`;
  await expect(verdict.getByRole("status")).toContainText("Realized price-return spread");
  await expect(verdict.getByRole("status")).toContainText(exactSpread);
  await expect(returns.getByRole("alert")).toHaveCount(0);
  await expect(page).toHaveURL(dashboard);

  expect(diagnostics.errors).toEqual([]);
  expect(diagnostics.requestFailures).toEqual([]);
  expect(diagnostics.failures).toEqual([
    { path: evaluations, status: 503 }, { path: evaluations, status: 503 },
  ]);
  expect(diagnostics.consoleErrors.filter(({ path, message }) =>
    !(path === evaluations && /503/.test(message)))).toEqual([]);
  await info.attach("story-lifecycle", { contentType: "application/json", body: JSON.stringify({
    dashboard: new URL(dashboard).pathname, observationDate, runId: run.run_id,
    outageStatus: 503, recoveredStatus: response.status(),
  }) });
});
