"""Freeze task 2.43 against accepted source prerequisites, excluding sibling edits."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

root = Path("/mnt/d/Source/QOpenBB")
evidence = root / "artifacts/task-2.43/implementation"
stage = Path("/home/mc/qopenbb-work/task243-colors-20261017/terminalpro")
baseline = Path("/home/mc/qopenbb-work/task241-20261017135547/terminalpro")
if stage.exists():
    raise SystemExit("Stage already exists; preserve its evidence")
shutil.copytree(baseline, stage, symlinks=True)
chart = "src/components/General/Table/Chart/application/"
tests = "tests/unit/chart-application/"
accepted = "0a4b2ea256816111702b2de1d2a284bade9a30ec"
for name in [chart + "appearanceComposition.ts", tests + "appearanceComposition.test.ts"]:
    content = subprocess.check_output([
        "git", "-C", str(root / "vendor/workspace"), "show",
        f"{accepted}:terminalpro/{name}",
    ])
    (stage / name).write_bytes(content)
test = tests + "appearanceColors.test.ts"
shutil.copy2(root / "vendor/workspace/terminalpro" / test, stage / test)
entries = []
for path in sorted(stage.rglob("*")):
    if path.is_file() and "node_modules" not in path.parts:
        entries.append({"path": str(path.relative_to(stage)),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
manifest = {"stage": str(stage), "frozen_prerequisite": str(baseline),
            "accepted_composition_commit": accepted,
            "frozen_contract_commit": "bc42d60", "files": entries}
(evidence / "red-stage-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"stage": str(stage), "files": len(entries)}))
