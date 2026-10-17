"""Reproduce and verify the real-grid teardown using an isolated source closure."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path("/mnt/d/Source/QOpenBB")
OUT = ROOT / "artifacts/appearance-grid-teardown"
BASE = Path("/home/mc/qopenbb-work/task241-20261017135547/terminalpro")
WORK = Path("/home/mc/qopenbb-work/appearance-grid-teardown/terminalpro")
DEPS = Path("/home/mc/qopenbb-work/appearance-deps/terminalpro/node_modules")
NODE = ROOT / "artifacts/task-1.2/node-v24.22.0-linux-x64/bin/node"
TEST = Path("tests/unit/chart-application/gridCapture.grid.test.ts")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(name, args):
    command = [str(NODE), "node_modules/vitest/vitest.mjs", "run", "--config",
               "tests/unit/chart-application/vitest.config.mjs", *args]
    start = time.monotonic()
    result = subprocess.run(command, cwd=WORK, capture_output=True, text=True)
    (OUT / f"{name}.log").write_text(result.stdout + result.stderr)
    record = {"command": command, "cwd": str(WORK),
              "exit_code": result.returncode,
              "duration_seconds": time.monotonic() - start,
              "test_sha256": digest(WORK / TEST)}
    (OUT / f"{name}.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record), flush=True)


OUT.mkdir(parents=True, exist_ok=True)
if not WORK.exists():
    shutil.copytree(BASE, WORK, ignore=shutil.ignore_patterns("node_modules"))
    (WORK / "node_modules").symlink_to(DEPS, target_is_directory=True)
for relative in ["src/components/General/Table/Chart", "tests/unit/chart-application"]:
    shutil.copytree(ROOT / "vendor/workspace/terminalpro" / relative,
                    WORK / relative, dirs_exist_ok=True)

patched = (WORK / TEST).read_text()
original = patched.replace("  vi.useFakeTimers();\n", "", 1)
start = original.index("afterEach(async () => {")
end = original.index("async function grid", start)
original = (original[:start] + "afterEach(() => {\n  api?.destroy();\n"
            "  host.remove();\n  vi.unstubAllGlobals();\n});\n" + original[end:])
if "--probe-only" not in sys.argv:
    (WORK / TEST).write_text(original)
    run("original-focused", [str(TEST)])
    (WORK / TEST).write_text(patched)
    run("fixed-focused", [str(TEST)])
    run("fixed-application", [])

# Observe the locked dependency's real callback chain without changing the fix.
probe = patched.replace("  vi.useFakeTimers();", '''  vi.useFakeTimers();
  const schedule = window.setTimeout;
  vi.spyOn(window, "setTimeout").mockImplementation((handler, delay, ...args) => {
    const origin = new Error().stack ?? "";
    return schedule(() => {
      if (api?.isDestroyed()) console.log("TEARDOWN_PROBE", JSON.stringify({
        delay, windowAlive: typeof window !== "undefined", destroyed: api.isDestroyed(),
        origin,
      }));
      if (typeof handler === "function") handler(...args);
    }, delay);
  });''', 1)
probe = probe.replace("    api?.destroy();", '''    console.log("TEARDOWN_PENDING_BEFORE", vi.getTimerCount());
    api?.destroy();
    console.log("TEARDOWN_PENDING_DESTROYED", vi.getTimerCount());''', 1)
probe = probe.replace("    expect(vi.getTimerCount()).toBe(0);", '''    console.log("TEARDOWN_PENDING_DRAINED", vi.getTimerCount());
    expect(vi.getTimerCount()).toBe(0);''', 1)
probe = probe.replace("    vi.useRealTimers();", "    vi.restoreAllMocks();\n    vi.useRealTimers();", 1)
(OUT / "probe.test.ts").write_text(probe)
(WORK / TEST).write_text(probe)
run("callback-lifecycle-probe", [str(TEST)])
(WORK / TEST).write_text(patched)

for name in ["application.log", "application.json"]:
    shutil.copyfile(ROOT / "artifacts/task-2.44/review" / name,
                    OUT / ("original-review-" + name))
