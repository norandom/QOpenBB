"""Read the immutable consumer adoption and verify candidate bundle bytes."""

import hashlib
import json
import math
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .modeling_bundle import REPOSITORY, _invalid_json_constant, _unique_object

ROOT = Path(__file__).resolve().parents[2]
BUNDLE = Path("contracts/modeling/v1")
CONSUMER = Path("contracts/consumers/financial-modeling/saved-output.v1.json")
POLICY = ROOT / CONSUMER.parent / "compatibility.v1.lock.json"
EXPECTATIONS = ROOT / CONSUMER.parent / "saved-output.cases.v1.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _finite_number(text: str) -> float:
    value = float(text)
    if not math.isfinite(value):
        raise ValueError("numeric value exceeds the supported JSON range")
    return value


def decode(data: bytes):
    return json.loads(
        data,
        object_pairs_hook=_unique_object,
        parse_constant=_invalid_json_constant,
        parse_float=_finite_number,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


@dataclass
class ContractSet:
    documents: dict
    consumer: dict
    revision: str
    manifest_sha256: str
    consumer_sha256: str


def _contracts(
    manifest: bytes, consumer_bytes: bytes, files: dict[str, bytes]
) -> ContractSet:
    spec = decode(manifest)
    require(
        set(spec)
        == {
            "format_version",
            "hash_algorithm",
            "repository",
            "source_revision",
            "files",
            "consumer_id",
            "consumer_contract_version",
            "consumer_source_revision",
            "consumer_manifest_sha256",
        },
        "unknown or missing provider manifest member",
    )
    consumer = decode(consumer_bytes)
    revision = spec["source_revision"]
    require(
        type(spec["format_version"]) is int
        and spec["format_version"] == 1
        and spec["hash_algorithm"] == "sha256",
        "unsupported bundle format",
    )
    require(spec["repository"] == REPOSITORY, "unexpected provider repository")
    require(bool(re.fullmatch("[0-9a-f]{40}", revision)), "invalid source revision")
    require(
        spec["consumer_source_revision"] == revision,
        "unrecognized consumer revision binding",
    )
    require(
        spec["consumer_manifest_sha256"] == digest(consumer_bytes),
        "consumer digest mismatch",
    )
    require(
        spec["consumer_id"] == consumer["consumer_id"]
        and type(spec["consumer_contract_version"]) is int
        and type(consumer["contract_version"]) is int
        and spec["consumer_contract_version"] == consumer["contract_version"],
        "consumer identity mismatch",
    )
    require(
        spec["files"] == {name: digest(data) for name, data in files.items()},
        "bundle file set or digest mismatch",
    )
    return ContractSet(
        {name: decode(blob) for name, blob in files.items()},
        consumer,
        revision,
        digest(manifest),
        digest(consumer_bytes),
    )


def candidate_contracts(directory: Path, consumer: Path) -> ContractSet:
    require(
        directory.is_dir() and not directory.is_symlink(),
        "invalid candidate bundle directory",
    )
    files = {}
    for entry in directory.rglob("*"):
        require(not entry.is_symlink(), "unexpected link in bundle")
        if entry.is_dir():
            continue
        require(entry.is_file(), "unexpected entry in bundle")
        files[entry.relative_to(directory).as_posix()] = entry.read_bytes()
    return _contracts(files.pop("manifest.json"), consumer.read_bytes(), files)


def _committed(revision: str, path: Path) -> bytes:
    require(bool(re.fullmatch("[0-9a-f]{40}", revision)), "invalid adoption revision")
    result = subprocess.run(
        ["git", "--no-replace-objects", "show", f"{revision}:{path.as_posix()}"],
        cwd=ROOT,
        env=os.environ | {"GIT_NO_LAZY_FETCH": "1"},
        capture_output=True,
        check=False,
    )
    require(
        result.returncode == 0, "adopted contract unavailable at pinned Git revision"
    )
    return result.stdout


def accepted_contracts(policy: dict) -> ContractSet:
    revision = policy["adoption_revision"]
    lock = decode(_committed(revision, CONSUMER.parent / "provider.lock.json"))
    manifest = _committed(revision, BUNDLE / "manifest.json")
    require(
        lock["manifest_sha256"] == digest(manifest),
        "adopted provider manifest digest mismatch",
    )
    data = decode(manifest)
    files = {name: _committed(revision, BUNDLE / name) for name in data["files"]}
    accepted = _contracts(manifest, _committed(revision, CONSUMER), files)
    require(
        accepted.revision == lock["source_revision"],
        "adopted provider revision mismatch",
    )
    return accepted
