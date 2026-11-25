"""Write or verify a reproducible financial-modeling contract bundle.

Format 1 uses sorted compact UTF-8 JSON with a trailing LF. The manifest
records the QOpenBB repository and source revision, SHA-256 hex digests by
payload path, and the consumer ID, contract version, source revision and
SHA-256 of the original consumer file. Both revisions name the same commit.
"""

import argparse
import hashlib
import json
import ntpath
import os
import re
import stat
import subprocess
import sys
import tempfile
from importlib.util import find_spec
from pathlib import Path, PurePosixPath

REPOSITORY = "https://github.com/norandom/QOpenBB.git"
MANIFEST = "manifest.json"
EXPORTER = "pipeline/qopenbb_ci"
DATA_API = "services/data-api/qopenbb_data"
SOURCE_INPUTS = {
    ".python-version",
    f"{EXPORTER}/__init__.py",
    f"{EXPORTER}/modeling_bundle.py",
    f"{EXPORTER}/modeling_documents.py",
    f"{DATA_API}/__init__.py",
    "pipeline/pyproject.toml",
    "pipeline/uv.lock",
    "services/data-api/pyproject.toml",
    "services/data-api/uv.lock",
}


def _json_bytes(value: dict | list) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _payloads() -> dict[str, bytes]:
    from .modeling_documents import documents

    payloads = {}
    for name, document in documents().items():
        path = PurePosixPath(name)
        if (
            not path.parts
            or path.is_absolute()
            or path.as_posix() != name
            or ".." in path.parts
            or ntpath.isreserved(name)
            or ntpath.splitdrive(name)[0]
            or "\\" in name
            or path.parts[0].casefold() == MANIFEST
        ):
            raise ValueError(f"invalid bundle payload path {name!r}")
        if not isinstance(document, (dict, list)):
            raise TypeError(f"bundle payload {name!r} must be a JSON object or array")
        try:
            payloads[name] = _json_bytes(document)
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"cannot serialize bundle payload {name!r}: {error}"
            ) from error
    return dict(sorted(payloads.items()))


def _git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "--no-replace-objects", "--literal-pathspecs", "-C", str(root), *args],
        env=os.environ | {"GIT_NO_LAZY_FETCH": "1"},
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(
            f"Git source verification failed: {result.stderr.decode(errors='replace').strip()}"
        )
    return result.stdout


def _is_producer(name: str) -> bool:
    return name.endswith(".py") and (
        name.startswith((f"{DATA_API}/", f"{EXPORTER}/modeling_"))
    )


def _verify_source(
    revision: str, consumer: Path, consumer_bytes: bytes, *, root: Path | None = None
) -> None:
    if root is None:
        root = Path(__file__).resolve().parents[2]
        data_api = find_spec("qopenbb_data")
        if (
            data_api is None
            or data_api.origin is None
            or (Path(data_api.origin).resolve() != root / DATA_API / "__init__.py")
        ):
            raise ValueError("write requires the Data API package from this checkout")
    if _git(root, "cat-file", "-t", revision) != b"commit\n":
        raise ValueError("--revision must identify a local Git commit")
    try:
        consumer_name = Path(os.path.abspath(consumer)).relative_to(root).as_posix()
    except ValueError as error:
        raise ValueError(
            "write requires a consumer manifest inside this checkout"
        ) from error
    required = SOURCE_INPUTS | {consumer_name}
    listing = _git(
        root,
        "ls-tree",
        "-r",
        "-z",
        "--full-tree",
        revision,
        "--",
        *sorted(required | {EXPORTER, DATA_API}),
    )
    pinned = {}
    for record in listing.split(b"\0")[:-1]:
        header, path = record.split(b"\t", 1)
        name = os.fsdecode(path)
        if name in required or _is_producer(name):
            mode, _, oid = header.split()
            if mode not in {b"100644", b"100755"}:
                raise ValueError(f"source input must be a regular Git file: {name}")
            pinned[name] = oid

    current = required | {
        path.relative_to(root).as_posix()
        for path in (
            *root.joinpath(EXPORTER).glob("modeling_*.py"),
            *root.joinpath(DATA_API).rglob("*"),
        )
        if path.suffix == ".py" or path.is_symlink() or path.is_junction()
    }
    algorithm = "sha1" if len(revision) == 40 else "sha256"
    for name in sorted(current | pinned.keys()):
        path = root / name
        if name not in pinned or not path.is_file() or path.resolve() != path:
            raise ValueError(f"source input differs from revision: {name}")
        content = consumer_bytes if name == consumer_name else path.read_bytes()
        blob = hashlib.new(algorithm, f"blob {len(content)}\0".encode())
        blob.update(content)
        if blob.hexdigest().encode() != pinned[name]:
            raise ValueError(f"source input differs from revision: {name}")


def _invalid_json_constant(value: str) -> None:
    raise ValueError(f"invalid JSON constant {value}")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _consumer_identity(data: bytes) -> tuple[str, int]:
    try:
        consumer = json.loads(
            data,
            parse_constant=_invalid_json_constant,
            object_pairs_hook=_unique_object,
        )
    except (UnicodeError, ValueError) as error:
        raise ValueError("consumer manifest must contain valid JSON") from error
    if not isinstance(consumer, dict):
        raise TypeError("consumer manifest must be a JSON object")
    identifier = consumer.get("consumer_id")
    version = consumer.get("contract_version")
    if not isinstance(identifier, str) or not identifier.strip():
        raise ValueError("consumer manifest requires a nonempty consumer_id")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        raise ValueError(
            "consumer manifest requires a positive integer contract_version"
        )
    return identifier, version


def _expected(action: str, revision: str, consumer: Path) -> dict[str, bytes]:
    if re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", revision) is None:
        raise ValueError("--revision must be a full lowercase Git commit SHA")
    consumer_bytes = consumer.read_bytes()
    consumer_id, consumer_version = _consumer_identity(consumer_bytes)
    if action == "write":
        _verify_source(revision, consumer, consumer_bytes)
    payloads = _payloads()
    payloads[MANIFEST] = _json_bytes(
        {
            "format_version": 1,
            "hash_algorithm": "sha256",
            "repository": REPOSITORY,
            "source_revision": revision,
            "files": {
                name: hashlib.sha256(data).hexdigest()
                for name, data in payloads.items()
            },
            "consumer_id": consumer_id,
            "consumer_contract_version": consumer_version,
            "consumer_source_revision": revision,
            "consumer_manifest_sha256": hashlib.sha256(consumer_bytes).hexdigest(),
        }
    )
    return payloads


def _directories(expected: dict[str, bytes]) -> set[str]:
    directories = {
        str(parent) for name in expected for parent in PurePosixPath(name).parents
    }
    files = {name.casefold() for name in expected}
    if len(files) != len(expected) or len(
        {name.casefold() for name in directories}
    ) != len(directories):
        raise ValueError(
            "bundle paths must be distinct on case-insensitive filesystems"
        )
    for directory in sorted(directories):
        if directory.casefold() in files:
            raise ValueError(f"bundle payload path {directory!r} is also a directory")
    return directories


def _inspect(output: Path, expected: dict[str, bytes]) -> set[str]:
    directories = _directories(expected)
    if output.is_symlink() or output.is_junction():
        raise ValueError(f"bundle output must be a directory, got link {output}")
    if not output.exists():
        return set()
    if not output.is_dir():
        raise ValueError(f"bundle output must be a directory: {output}")

    found = set()
    pending = [output]
    while pending:
        for entry in sorted(pending.pop().iterdir()):
            name = entry.relative_to(output).as_posix()
            mode = entry.lstat().st_mode
            if name in directories and stat.S_ISDIR(mode) and not entry.is_junction():
                pending.append(entry)
            elif name in expected and stat.S_ISREG(mode):
                found.add(name)
            else:
                raise ValueError(f"unexpected bundle entry: {name}")
    for name, data in expected.items():
        if name in found and (output / name).read_bytes() != data:
            raise ValueError(f"bundle file differs: {name}")
    return found


def _bundle(action: str, output: Path, expected: dict[str, bytes]) -> None:
    output = output.absolute()
    present = _inspect(output, expected)
    missing = [name for name in expected if name not in present]
    if action == "check" and missing:
        raise ValueError(f"missing bundle files: {', '.join(missing)}")
    if missing:
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix=".modeling-bundle-", dir=output.parent
        ) as temp:
            staged = Path(temp) / "payload"
            for name in missing:
                path = output / name
                path.parent.mkdir(parents=True, exist_ok=True)
                staged.write_bytes(expected[name])
                # Linking publishes completed bytes without replacing a concurrent writer's file.
                os.link(staged, path)
                staged.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("write", "check"))
    parser.add_argument(
        "--revision", required=True, help="Full lowercase Git commit SHA"
    )
    parser.add_argument("--output", required=True, type=Path, help="Bundle directory")
    parser.add_argument(
        "--consumer", required=True, type=Path, help="Consumer manifest file"
    )
    args = parser.parse_args(argv)
    try:
        _bundle(
            args.action,
            args.output,
            _expected(args.action, args.revision, args.consumer),
        )
    except (ImportError, OSError, TypeError, ValueError) as error:
        print(f"modeling bundle: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
