import config from "../../vendor/workspace/terminalpro/tests/e2e/live-chart/playwright.config";
import { browserEnvironment, checkedOutput } from "../evidence.ts";

browserEnvironment();
checkedOutput(process.env.WORKSPACE_EVIDENCE_ROOT ?? "");
if (process.env.FMP_API_KEY || process.env.FRED_API_KEY || process.env.JOURNEY_SIGNER)
  throw new Error("Modeling browser process received service-only credentials");
export default { ...config, testDir: ".", testMatch: "analyst.spec.mts", timeout: 180_000 };
