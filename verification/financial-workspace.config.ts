import existing from "../vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config";

import { browserEnvironment, checkedOutput } from "./evidence.ts";
browserEnvironment();
checkedOutput(process.env.WORKSPACE_EVIDENCE_ROOT ?? "");

export default {
  ...existing,
  testDir: "../tests/e2e",
  testMatch: "financial-workspace.spec.mts",
};
