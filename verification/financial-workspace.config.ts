import existing from "../vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config";

export default {
  ...existing,
  testDir: "../tests/e2e",
  testMatch: "financial-workspace.spec.mts",
};
