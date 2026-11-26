import { writeFile } from "node:fs/promises";
import type { Locator, Page } from "../../vendor/workspace/terminalpro/node_modules/@playwright/test/index";
import { expect, test } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/toolchain";
import { expectApplicationDiagnostics, observeApplication } from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/diagnostics";
import { inspectMacro, inspectPrices, runsFor } from "./story-selection-evidence.mts";
import { connectDataSource, openStory, signIn } from "./workspace.mts";

test.use({ locale: "en-US" });

const eligible = "2026-11-13";
const shortHistory = "2026-01-13";

async function selectProxy(control: Locator, symbol: string) {
  const page = control.page();
  await control.press("Space");
  await expect(page.getByRole("option", { selected: true })).toBeFocused();
  await page.keyboard.press("ArrowDown");
  const choice = page.getByRole("option", { name: new RegExp("^" + symbol + " ·") });
  await expect(choice).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(control).toContainText(symbol);
  await expect(control).toBeFocused();
}

async function changeMonth(input: Locator, month: string, expected: string) {
  // Chromium exposes month, day and year as keyboard-editable segments in en-US.
  await input.focus();
  await input.press("ArrowLeft");
  await input.press("ArrowLeft");
  for (const digit of month) await input.page().keyboard.press(digit);
  await expect(input).toHaveValue(expected);
  await expect(input).toBeFocused();
}

async function theme(page: Page, dark: boolean) {
  const html = page.locator("html");
  if ((await html.getAttribute("class"))?.split(" ").includes("dark") !== dark) {
    const saved = page.waitForResponse(response => response.request().method() === "POST" &&
      new URL(response.url()).pathname === "/api/pro/display-settings");
    await page.keyboard.press("Control+m");
    expect((await saved).ok()).toBe(true);
  }
  await expect.poll(async () => (await html.getAttribute("class"))?.split(" ").includes("dark") === dark).toBe(true);
}

async function checkShortHistory(story: Locator, date: Locator, verdict: Locator) {
  const missing = runsFor(story.page(), shortHistory);
  await changeMonth(date, "01", shortHistory);
  const insufficient = await missing;
  await expect(date).toBeFocused();
  expect(insufficient.price.outputs.find(output => output.output_id === "momentum_spread"))
    .toMatchObject({ status: "withheld", value: null });
  await expect(verdict).toContainText("Insufficient data.");
  await expect(verdict).toContainText(shortHistory);
  await expect(verdict).toContainText("GLD and VGT");
  const schedule = insufficient.price.inputs.tables.find(table => table.table_id === "sessions")!;
  expect(schedule.rows).toHaveLength(8);
  expect(schedule.rows.at(-1)?.observation_date).toBe(shortHistory);
  await expect(verdict).toContainText("requires 64 scheduled sessions, found 8");
  await expect(story.getByRole("figure")).toHaveCount(0);
  return { theme: "dark", observationDate: shortHistory, runId: insufficient.price.run_id,
    macroRunId: insufficient.macro.run_id, verdict: "insufficient_data",
    scheduledSessionCount: schedule.rows.length };
}

test("packaged research story selection, saved financial evidence and keyboard recovery", async ({ page }, info) => {
  await signIn(page);
  await connectDataSource(page, "Journey provider data");
  await theme(page, false);
  const diagnostics = await observeApplication(page);
  const initial = runsFor(page, eligible);
  const story = await openStory(page);
  const commodity = story.getByRole("combobox", { name: "Commodity proxy" });
  const technology = story.getByRole("combobox", { name: "Technology proxy" });
  const date = story.getByLabel("Observation date", { exact: true });
  const verdict = story.getByRole("region", { name: "Verdict", exact: true }).getByRole("status");
  const evidence = [];

  await expect(commodity).toContainText("DBC");
  await expect(technology).toContainText("XLK");
  await expect(date).toHaveValue(eligible);
  const baseline = await initial;
  evidence.push({ theme: "light", ...await inspectPrices(story, baseline.price, ["DBC", "XLK"]),
    macro: await inspectMacro(story, baseline.macro, baseline.price) });
  await story.getByRole("figure", { name: "Price returns input chart", exact: true })
    .screenshot({ path: info.outputPath("story-fmp-price-light.png") });

  const left = runsFor(page, eligible);
  await selectProxy(commodity, "GLD");
  await expect(verdict).toContainText("Pending verified price-return spread");
  await expect(story.getByRole("figure", { name: "Price returns input chart", exact: true })).toHaveCount(0);
  const changedLeft = await left;
  await expect(commodity).toBeFocused();
  evidence.push({ theme: "light", ...await inspectPrices(story, changedLeft.price, ["GLD", "XLK"]),
    macro: await inspectMacro(story, changedLeft.macro, changedLeft.price) });

  await theme(page, true);
  const right = runsFor(page, eligible);
  await selectProxy(technology, "VGT");
  const changedRight = await right;
  await expect(technology).toBeFocused();
  evidence.push({ theme: "dark", ...await inspectPrices(story, changedRight.price, ["GLD", "VGT"]),
    macro: await inspectMacro(story, changedRight.macro, changedRight.price) });
  await story.getByRole("figure", { name: "Realized volatility input chart", exact: true })
    .screenshot({ path: info.outputPath("story-fmp-risk-dark.png") });

  evidence.push(await checkShortHistory(story, date, verdict));

  const recovery = runsFor(page, eligible);
  await changeMonth(date, "11", eligible);
  const recovered = await recovery;
  await expect(date).toBeFocused();
  await expect(verdict).toContainText("Realized price-return spread");
  evidence.push({ theme: "dark", ...await inspectPrices(story, recovered.price, ["GLD", "VGT"]),
    macro: await inspectMacro(story, recovered.macro, recovered.price) });
  expect(new Set(evidence.map(item => item.runId)).size).toBe(evidence.length);
  for (const item of evidence) {
    if ("macro" in item) expect(item.macro).toMatchObject({
      status: "withheld", unavailableEndpointDates: expect.arrayContaining([eligible]),
    });
  }
  await page.keyboard.press("End");
  await expect(verdict).toBeInViewport();
  expectApplicationDiagnostics(diagnostics);
  const summary = { observationDate: eligible, evidence, browserDiagnostics: "clean" };
  await writeFile(info.outputPath("story-selection.json"), JSON.stringify(summary, null, 2) + "\n", { mode: 0o600 });
});
