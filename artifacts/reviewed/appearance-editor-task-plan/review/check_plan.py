"""Read-only task-plan coverage and dependency checks; no runtime verification."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SPEC = ROOT / ".kiro/specs/openbb-self-service"
DRAFT = ROOT / "artifacts/appearance-editor-task-plan/draft.md"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


requirements = (SPEC / "requirements.md").read_text(encoding="utf-8-sig")
expected = []
group = None
for line in requirements.splitlines():
    header = re.match(r"### Requirement (\d+):", line)
    if header:
        group = header.group(1)
    criterion = re.match(r"(\d+)\. ", line)
    if criterion and group:
        expected.append(f"{group}.{criterion.group(1)}")

BASE_REVISION = "cff08b347cedbaef95aea064d7fc1d5253d5f300"
canonical_bytes = subprocess.check_output(
    ["git", "show", f"{BASE_REVISION}:.kiro/specs/openbb-self-service/tasks.md"], cwd=ROOT
)
canonical = canonical_bytes.decode("utf-8-sig")
draft = DRAFT.read_text(encoding="utf-8-sig")
task_pattern = re.compile(r"^- \[([ x])\] (\d+(?:\.\d+)?)\.? (.*)$", re.M)
existing = {m.group(2): m.group(1) == "x" for m in task_pattern.finditer(canonical)}
new = list(task_pattern.finditer(draft))
all_ids = set(existing) | {m.group(2) for m in new}
coverage = set()
for mapping in re.findall(r"_Requirements: ([^_]+)_", canonical + "\n" + draft):
    coverage.update(x.strip() for x in mapping.split(","))
tasks = {}
for index, match in enumerate(new):
    body = draft[match.end():new[index + 1].start() if index + 1 < len(new) else len(draft)]
    depends = re.search(r"_Depends: ([^_]+)_", body)
    mapped = re.search(r"_Requirements: ([^_]+)_", body)
    tasks[match.group(2)] = {
        "completed": match.group(1) == "x",
        "parallel": match.group(3).startswith("(P)"),
        "depends": [x.strip() for x in depends.group(1).split(",")] if depends else [],
        "requirements": [x.strip() for x in mapped.group(1).split(",")] if mapped else [],
        "observable_done": "Done:" in body,
        "boundary": bool(re.search(r"_Boundary: [^_]+_", body)),
    }

def cycle(node, visiting):
    if node in visiting:
        return True
    return any(cycle(dep, visiting | {node}) for dep in tasks[node]["depends"] if dep in tasks)

inventory = json.loads((ROOT / ".kiro/complexity-budgets.json").read_text(encoding="utf-8-sig"))
missing_files = [f"{repo['id']}:{file}" for repo in inventory["repositories"]
                 for owner in repo["owners"] for file in owner["files"]
                 if not (ROOT / repo["root"] / file).is_file()]
inputs = [DRAFT, SPEC / "requirements.md", SPEC / "design.md",
          SPEC / "chart-appearance-editor-integration-design.md",
          ROOT / ".kiro/complexity-budgets.json"]
for name in ("chart-application", "chart-compatibility"):
    inputs.extend(ROOT / "vendor/workspace/terminalpro/tests/unit" / name / file
                  for file in ("tsconfig.json", "vitest.config.mjs"))
inputs.append(ROOT / "vendor/workspace/terminalpro/biome.json")
result = {
    "scope": "Static task graph and inventory existence only; no application tests, compiler, lint, browser or size gate executed",
    "input_sha256": {p.relative_to(ROOT).as_posix(): digest(p) for p in inputs},
    "canonical_tasks_baseline": {
        "revision": BASE_REVISION,
        "path": ".kiro/specs/openbb-self-service/tasks.md",
        "git_blob_sha256": hashlib.sha256(canonical_bytes).hexdigest(),
        "source": "git show of pinned baseline, preventing duplicate suffix after publication",
    },
    "expected_criteria_count": len(expected),
    "expected_criteria": expected,
    "combined_covered_criteria_count": len(set(expected) & coverage),
    "missing_criteria": sorted(set(expected) - coverage),
    "unknown_mapped_criteria": sorted(coverage - set(expected)),
    "new_tasks": tasks,
    "duplicate_new_ids": len({m.group(2) for m in new}) != len(new),
    "overlap_existing_ids": sorted(set(tasks) & set(existing)),
    "missing_dependencies": sorted({d for t in tasks.values() for d in t["depends"] if d not in all_ids}),
    "unaccepted_external_prerequisites": sorted({d for t in tasks.values() for d in t["depends"] if d in existing and not existing[d]}),
    "new_graph_cycle": any(cycle(node, set()) for node in tasks),
    "missing_inventory_files": missing_files,
}
result["pass"] = (
    len(expected) == 69 and not result["missing_criteria"]
    and not result["unknown_mapped_criteria"] and not result["duplicate_new_ids"]
    and not result["overlap_existing_ids"] and not result["missing_dependencies"]
    and not result["unaccepted_external_prerequisites"] and not result["new_graph_cycle"]
    and not missing_files and set(tasks) == {f"2.{i}" for i in range(41, 46)}
    and all(not t["completed"] and t["observable_done"] and t["boundary"] for t in tasks.values())
)
(OUT / "mechanical-check.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
raise SystemExit(0 if result["pass"] else 1)
