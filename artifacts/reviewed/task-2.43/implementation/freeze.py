"""Freeze exact owned bytes and safe evidence for the parent review/publication gate."""
import hashlib
import json
from pathlib import Path
import subprocess

root = Path("/mnt/d/Source/QOpenBB")
evidence = root / "artifacts/task-2.43/implementation"
stage = Path("/home/mc/qopenbb-work/task243-colors-20261017/terminalpro")
working = root / "vendor/workspace/terminalpro"
production = "src/components/General/Table/Chart/application/appearanceColors.ts"
test = "tests/unit/chart-application/appearanceColors.test.ts"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for name in [production, test]:
    if digest(stage / name) != digest(working / name):
        raise SystemExit(f"Stage/workspace mismatch: {name}")
prerequisites = [
    ("bc42d60", "src/components/General/Table/Chart/application/appearanceContracts.ts"),
    ("bc42d60", "tests/unit/chart-application/appearanceContracts.types.ts"),
    ("bc42d60", "tests/unit/chart-application/appearanceFixtures.json"),
    ("0a4b2ea", "src/components/General/Table/Chart/application/appearanceComposition.ts"),
    ("0a4b2ea", "tests/unit/chart-application/appearanceComposition.test.ts"),
]
verified = []
for revision, name in prerequisites:
    accepted = subprocess.check_output([
        "git", "-C", str(root / "vendor/workspace"), "show",
        f"{revision}:terminalpro/{name}",
    ])
    if (stage / name).read_bytes() != accepted:
        raise SystemExit(f"Frozen prerequisite mismatch: {name}")
    verified.append({"revision": revision, "path": name, "sha256": digest(stage / name)})
files = [{"path": str(path.relative_to(stage)), "sha256": digest(path)}
         for path in sorted(stage.rglob("*"))
         if path.is_file() and "node_modules" not in path.parts]
(evidence / "source-manifest.json").write_text(json.dumps({
    "stage": str(stage), "verified_prerequisites": verified, "files": files,
}, indent=2) + "\n")
paths = [working / production, working / test]
paths.extend(path for path in sorted(evidence.iterdir())
             if path.is_file() and path.name != "publication-allowlist.json")
allowlist = {"scope": "Frozen task 2.43 safe review set; controller owns publication",
             "files": [{"path": str(path.relative_to(root)), "sha256": digest(path)}
                       for path in paths]}
(evidence / "publication-allowlist.json").write_text(json.dumps(allowlist, indent=2) + "\n")
print(json.dumps({"source_files": len(files), "allowlisted_files": len(paths),
                  "production_sha256": digest(working / production),
                  "test_sha256": digest(working / test)}))
