import existing from "../vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config";

import { browserEnvironment, checkedOutput } from "./evidence.ts";

browserEnvironment();
checkedOutput(process.env.WORKSPACE_EVIDENCE_ROOT ?? "");

const suites: Record<string, { filename: string; timeout: number }> = {
  "fmp-expansion-a": { filename: "fmp-expansion-workspace.spec.mts", timeout: 420000 },
  "fmp-expansion-b": { filename: "fmp-batch-b-workspace.spec.mts", timeout: 1800000 },
  "events-documents": { filename: "events-documents-workspace.spec.mts", timeout: 1800000 },
};
const suite = process.env.QOPENBB_FINANCIAL_SUITE;
if (suite !== undefined && !Object.hasOwn(suites, suite)) throw new Error("Unknown financial Workspace suite");
if (suite !== undefined && (process.env.FMP_API_KEY || process.env.FRED_API_KEY))
  throw new Error("Provider secrets must not enter the browser process");
const selected = suite === undefined ? undefined : suites[suite];

export default {
  ...existing,
  testDir: "../tests/e2e",
  testMatch: selected?.filename ?? "financial-workspace.spec.mts",
  ...(selected ? { timeout: selected.timeout, fullyParallel: false } : {}),
  ...(suite === "events-documents" ? { reporter: [["line"]] } : {}),
};
