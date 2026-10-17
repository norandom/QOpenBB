"""Read-only mechanical review of the scoped appearance/editor amendment."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SPEC = ROOT / ".kiro/specs/openbb-self-service"
DRAFT = SPEC / "chart-appearance-editor-integration-design.md"
text = DRAFT.read_text(encoding="utf-8")
checks = []


def check(name, passed, detail):
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


ids = []
section = None
for line in (SPEC / "requirements.md").read_text(encoding="utf-8").splitlines():
    heading = re.match(r"### Requirement (\d+):", line)
    if heading:
        section = heading[1]
    criterion = re.match(r"(\d+)\. ", line)
    if criterion and section:
        ids.append(f"{section}.{criterion[1]}")
present = set(re.findall(r"\b\d+\.\d+\b", text))
missing = [item for item in ids if item not in present]
base = (SPEC / "design.md").read_text(encoding="utf-8")
base_ids = set(re.findall(r"\b\d+\.\d+\b", base))
check("amendment_scope_traceability", all(x in present for x in ["4.2", "4.7", "4.8", "4.9", "10.5", "10.6"]), {"active_count": len(ids), "present": [x for x in ids if x in present], "not_repeated_in_amendment": missing})
check("unchanged_global_coverage", all(x in base_ids for x in ids), {"owner": ".kiro/specs/openbb-self-service/design.md", "missing": [x for x in ids if x not in base_ids]})
for heading in ["Boundary Commitments", "Out of Boundary", "Allowed Dependencies", "Revalidation Triggers", "File Structure Plan"]:
    start = re.search(r"^(#{2,3}) " + re.escape(heading) + r"\n", text, re.M)
    body = ""
    if start:
        remainder = text[start.end():]
        end = re.search(r"^#{1," + str(len(start[1])) + r"} ", remainder, re.M)
        body = remainder[:end.start()] if end else remainder
    check("populated_" + heading, len(body.strip()) > 40, heading)
plan = text.split("## File Structure Plan\n")[1].split("## Dependency Plan")[0]
check("concrete_paths", "application/appearanceComposition.ts" in plan and "compatibility/editorEvents.ts" in plan, "Explicit create/change and later-join paths")
markers = re.findall(r"\b(?:TBD|TODO|FIXME|HACK|XXX)\b", text)
check("placeholder_scan", not markers, markers)
links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
broken = []
for link in links:
    if "://" not in link and not (DRAFT.parent / link.split("#")[0]).resolve().exists():
        broken.append(link)
check("relative_links_exist", not broken, {"count": len(links), "broken": broken})

source_root = ROOT / "vendor/workspace"
expected = "76edf85a46298f7bc5212ff9944e4b66e9baa4af"
head = subprocess.check_output(["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True).strip()
check("candidate_head", head == expected, head)
manifest = json.loads((ROOT / "artifacts/reviewed/parity/appearance-saved-composition/source-manifest.json").read_text())
source_hashes = []
for entry in manifest["files"]:
    data = subprocess.check_output(["git", "-C", str(source_root), "show", f'{manifest["source"]}:{entry["path"]}'])
    actual = hashlib.sha256(data).hexdigest()
    source_hashes.append({"path": entry["path"], "sha256": actual})
    check("original_blob_" + entry["path"], actual == entry["sha256"], actual)

paths = [
    "application/types.ts", "application/sessionState.ts",
    "compatibility/optionStateTypes.ts", "compatibility/editorEvents.ts",
    "compatibility/optionState.ts", "compatibility/legacyTypes.ts",
    "compatibility/integratedState.ts", "echarts/cartesianStyle.ts",
]
chart = source_root / "terminalpro/src/components/General/Table/Chart"
files = []
for path in paths:
    file = chart / path
    files.append({"path": file.relative_to(ROOT).as_posix(), "sha256": sha(file), "physical_lines": len(file.read_text(encoding="utf-8").splitlines())})
check("inspected_existing_physical_caps", all(x["physical_lines"] <= 400 for x in files), files)
result = {
    "draft": DRAFT.relative_to(ROOT).as_posix(), "draft_sha256": sha(DRAFT),
    "candidate_head": head, "checks": checks, "source_hashes": source_hashes,
    "pass": all(x["passed"] for x in checks),
    "limits": "Read-only design checks, not production tests or complete logical/function complexity measurement. Global coverage remains owned by design.md; direct amendment omissions are reported rather than treated as deleted requirements.",
}
(OUT / "checks.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"pass": result["pass"], "checks": len(checks), "draft_sha256": result["draft_sha256"], "active_requirements": len(ids), "direct_omissions": len(missing)}))
raise SystemExit(0 if result["pass"] else 1)
