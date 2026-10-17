"""Read-only task-plan checks; writes only this review's result file."""
from pathlib import Path
import difflib
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
PLAN = ROOT / "artifacts/grid-capture-tasks"
SPEC = ROOT / ".kiro/specs/openbb-self-service"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


base = (SPEC / "tasks.md").read_text(encoding="utf-8")
draft = (PLAN / "draft.md").read_text(encoding="utf-8")
merged = (PLAN / "merged-preview.md").read_text(encoding="utf-8")
requirements = (SPEC / "requirements.md").read_text(encoding="utf-8")
blocks = re.split(r"(?=^- \[[ x]\] \d)", merged, flags=re.M)
tasks = {}
for block in blocks:
    match = re.match(r"- \[[ x]\] (\d+(?:\.\d+)?)\b", block)
    if match:
        assert match[1] not in tasks, match[1]
        tasks[match[1]] = block
groups = re.split(r"### Requirement (\d+):", requirements)
required = {
    f"{groups[index]}.{criterion}"
    for index in range(1, len(groups), 2)
    for criterion in re.findall(r"^(\d+)\. ", groups[index + 1], re.M)
}
mapped = {
    value
    for section in re.findall(r"_Requirements: ([^_]+)_", merged)
    for value in re.findall(r"\d+\.\d+", section)
}
assert required == mapped, (sorted(required - mapped), sorted(mapped - required))
edges = {
    identifier: [
        dependency
        for section in re.findall(r"_Depends: ([^_]+)_", block)
        for dependency in re.findall(r"\d+(?:\.\d+)?", section)
    ]
    for identifier, block in tasks.items()
}
visited = set()


def visit(identifier, stack):
    assert identifier in tasks, identifier
    assert identifier not in stack, stack + [identifier]
    if identifier not in visited:
        for dependency in edges[identifier]:
            visit(dependency, stack + [identifier])
        visited.add(identifier)


for identifier in tasks:
    visit(identifier, [])
assert edges["2.38"] == ["1.4", "2.37"]
assert edges["2.39"] == ["2.38"]
assert edges["2.40"] == ["2.39"]
for identifier in ["2.38", "2.39", "2.40"]:
    assert f"- [ ] {identifier} " in draft
    assert "(P)" not in tasks[identifier].splitlines()[0]
    assert "Done when" in tasks[identifier]
    assert "1-3 hours" in tasks[identifier]
    assert "_Boundary:" in tasks[identifier]
assert merged.count(draft.rstrip()) == 1
without_draft = merged.replace(draft.rstrip() + "\n\n", "", 1)
changes = list(difflib.unified_diff(base.splitlines(), without_draft.splitlines()))
publication = ["draft.md", "merged-preview.md", "mechanical.json", "prepare.py"]
for name in publication:
    content = (PLAN / name).read_text(encoding="utf-8")
    assert not re.search(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----", content)
    assert not re.search(r"\b(?:sk-ant-|ghp_|github_pat_)[A-Za-z0-9_-]{15,}", content)
approval = json.loads((SPEC / "spec.json").read_text(encoding="utf-8"))
slice_ = approval["active_amendment"]["application_integration_slice"]["runtime_contract_followup"]
assert slice_["design_approved"] is True
assert slice_["implementation_approved"] is False
assert digest(SPEC / "chart-grid-capture-design.md") == slice_["reviewed_design_sha256"]
result = {
    "scope": "Independent read-only task-graph and small publication-set checks",
    "verdict": "PASS",
    "requirement_count": len(required),
    "task_count": len(tasks),
    "new_tasks": ["2.38", "2.39", "2.40"],
    "missing_requirements": [],
    "unknown_requirements": [],
    "missing_dependencies": [],
    "explicit_dependency_cycles": [],
    "production_tests_run": False,
    "files": {
        str(path.relative_to(ROOT)).replace("\\", "/"): digest(path)
        for path in [SPEC / "tasks.md", SPEC / "spec.json", SPEC / "chart-grid-capture-design.md"]
        + [PLAN / name for name in publication]
    },
    "merge_changes_outside_insert": changes,
}
(PLAN / "review/mechanical.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: value for key, value in result.items() if key not in ["files", "merge_changes_outside_insert"]}))
print("\n".join(changes))
