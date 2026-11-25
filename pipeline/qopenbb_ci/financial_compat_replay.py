"""Replay the provider export from its source commit in a disposable directory."""

import os
import subprocess
import sys
import tarfile
from pathlib import Path
from tempfile import TemporaryDirectory

from .financial_compat_inputs import CONSUMER, ROOT, require


def verify_source_export(revision: str, bundle: Path, consumer: Path) -> None:
    env = os.environ | {"GIT_NO_LAZY_FETCH": "1", "GIT_NO_REPLACE_OBJECTS": "1"}
    # The caller has already checked that revision is a full hexadecimal commit ID.
    resolved = subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{revision}^{{commit}}"],
        cwd=ROOT,
        env=env,
        text=True,
        stderr=subprocess.PIPE,
    ).strip()
    require(resolved == revision, "candidate provider commit unavailable")
    consumer_path = _consumer_path(revision, consumer.read_bytes(), env)
    with TemporaryDirectory() as replay:
        source = Path(replay) / "source"
        with (Path(replay) / "source.tar").open("w+b") as archive:
            subprocess.run(
                [
                    "git",
                    "archive",
                    revision,
                    "pipeline/qopenbb_ci",
                    "services/data-api/qopenbb_data",
                    str(consumer_path),
                ],
                cwd=ROOT,
                env=env,
                stdout=archive,
                check=True,
                stderr=subprocess.PIPE,
            )
            archive.seek(0)
            with tarfile.open(fileobj=archive) as files:
                files.extractall(source, filter="data")
        packages = (source / "pipeline", source / "services/data-api")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "qopenbb_ci.modeling_bundle",
                "check",
                "--revision",
                revision,
                "--output",
                str(bundle.resolve()),
                "--consumer",
                str(source / consumer_path),
            ],
            cwd=source,
            env=env | {"PYTHONPATH": os.pathsep.join(map(str, packages))},
            capture_output=True,
            check=False,
        )
        require(
            result.returncode == 0,
            "bundle does not reproduce from its provider and consumer revision",
        )


def _consumer_path(revision: str, payload: bytes, env: dict[str, str]) -> Path:
    oid = subprocess.check_output(
        ["git", "hash-object", "--stdin"], input=payload, cwd=ROOT, env=env
    ).strip()
    tree = subprocess.check_output(
        ["git", "ls-tree", "-r", "-z", revision, "--", str(CONSUMER.parent)],
        cwd=ROOT,
        env=env,
    )
    for entry in tree.split(b"\0")[:-1]:
        header, name = entry.split(b"\t", 1)
        mode, kind, sha = header.split()
        if kind == b"blob" and mode in (b"100644", b"100755") and sha == oid:
            return Path(os.fsdecode(name))
    raise ValueError("consumer bytes absent from the declared consumer source revision")
