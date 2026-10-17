"""Freeze only the explicitly selected independent review outputs for publication."""
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
NAMES = [
    "research-review.md", "grid-design-review.md", "appearance-inspection.md",
    "verify_appearance.py", "verify_runtime.py", "replay_grid.py", "freeze_review.py",
    "appearance-verification.json", "runtime-verification.json", "grid-replay.json",
]
entries = []
for name in NAMES:
    raw = (BASE / name).read_bytes()
    entries.append({"path": name, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
manifest = {"status": "frozen", "source": "artifacts/runtime-contract-next/review",
            "excluded": ["appearance-reproduction/**", "grid-reproduction/**"],
            "reason": "Reproduction copies duplicate already reviewed public inputs/results; scripts and fresh verification records are retained.",
            "files": entries}
(BASE / "publication-allowlist.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps({"frozen": len(entries)}))
