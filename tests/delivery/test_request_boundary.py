"""Execute the owned Workspace authentication boundary against real JS URL/Headers."""

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_request_boundary_behavior():
    result = subprocess.run(
        ["node", "--test", str(ROOT / "vendor/workspace/terminalpro/tests/unit/backendOrigin.test.mjs")],
        cwd=ROOT, capture_output=True, text=True, timeout=30, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "pass 24" in result.stdout
