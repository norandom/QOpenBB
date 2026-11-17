import existing from "../vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config";

import { browserEnvironment, checkedOutput } from "./evidence.ts";
browserEnvironment();
checkedOutput(process.env.WORKSPACE_EVIDENCE_ROOT ?? "");
const suite = process.env.QOPENBB_FINANCIAL_SUITE;
if (suite !== undefined && suite !== "fmp-expansion-a") throw new Error("Unknown financial Workspace suite");
if (suite === "fmp-expansion-a" && (process.env.FMP_API_KEY || process.env.FRED_API_KEY))
  throw new Error("Provider secrets must not enter the browser process");

export default {
  ...existing,
  testDir: "../tests/e2e",
  testMatch: suite === "fmp-expansion-a" ? "fmp-expansion-workspace.spec.mts" : "financial-workspace.spec.mts",
  ...(suite === "fmp-expansion-a" ? { timeout: 420000, fullyParallel: false } : {}),
};
