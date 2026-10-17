"""Check lifecycle observations and freeze the reviewable evidence allowlist."""

import hashlib
import json
from pathlib import Path
import re

ROOT = Path("/mnt/d/Source/QOpenBB")
OUT = ROOT / "artifacts/appearance-grid-teardown"
TEST = ROOT / "vendor/workspace/terminalpro/tests/unit/chart-application/gridCapture.grid.test.ts"
DEPENDENCY = Path("/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules/ag-grid-community/dist/package/main.esm.mjs")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


raw = (OUT / "callback-lifecycle-probe.log").read_text()
lines = re.sub(r"\x1b\[[0-9;]*m", "", raw).splitlines()
callbacks = [json.loads(line.split("TEARDOWN_PROBE ", 1)[1])
             for line in lines if line.startswith("TEARDOWN_PROBE ")]
animation = [item for item in callbacks if item.get("delay") == 400
             and "RowRenderer.destroyRowCtrls" in item["origin"]]
nested = [item for item in callbacks if item.get("delay") == 0
          and "RowRenderer.dispatchDisplayedRowsChanged" in item["origin"]
          and "LocalEventService.dispatchAsync" in item["origin"]]
drained = [line for line in lines if line.startswith("TEARDOWN_PENDING_DRAINED ")]
assert animation and nested
assert all(item["windowAlive"] and item["destroyed"] for item in callbacks)
assert len(drained) == 11 and all(line.endswith(" 0") for line in drained)
for name in ["fixed-focused", "fixed-application", "callback-lifecycle-probe"]:
    assert json.loads((OUT / f"{name}.json").read_text())["exit_code"] == 0
assert json.loads((OUT / "fixed-focused.json").read_text())["test_sha256"] == sha(TEST)
assert json.loads((OUT / "fixed-application.json").read_text())["test_sha256"] == sha(TEST)
assert json.loads((OUT / "original-review-application.json").read_text())["exit_code"] == 1

summary = {
    "test_sha256": sha(TEST), "ag_grid_version": "34.1.1",
    "ag_grid_bundle_sha256": sha(DEPENDENCY),
    "animation_callbacks_after_destroy": len(animation),
    "nested_displayed_rows_event_flushes_after_destroy": len(nested),
    "all_observed_callbacks_have_live_window": True,
    "teardowns_asserting_empty_queue": len(drained),
    "original_focused_did_not_reproduce_intermittent_failure": True,
    "original_review_failure_preserved": True,
}
(OUT / "lifecycle-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
source = DEPENDENCY.read_text().splitlines()
sections = [(91, 117), (372, 380), (35920, 35929), (36820, 36856)]
(OUT / "locked-ag-grid-excerpts.txt").write_text(
    "".join(f"{number}: {source[number - 1]}\n"
            for start, end in sections for number in range(start, end + 1)))
allowed = [TEST] + sorted(path for path in OUT.iterdir()
                          if path.is_file() and path.name != "allowlist.json")
manifest = {"files": [{"path": str(path.relative_to(ROOT)), "sha256": sha(path)}
                      for path in allowed],
            "scope": "Test-only lifecycle repair and synthetic local verification evidence",
            "excluded": ["allowlist.json (self)", "dependency cache", "isolated workspace"]}
(OUT / "allowlist.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps(summary, indent=2))
