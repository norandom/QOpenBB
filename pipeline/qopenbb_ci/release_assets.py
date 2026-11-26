"""Assemble or check the Modeling contract ZIP and release manifest offline.

--images is the service-keyed map of publication reports (service, reference,
remote and labels). --pulled is the packaged journey's before/after image
report. --evidence takes reviewed repository paths at the release revision.
"""

import argparse
import json
import os
import re
import stat
import subprocess
import sys
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_STORED, ZipFile, ZipInfo

import tomllib

from .build_model_image import MODELING_FILES
from .financial_compat_inputs import (
    BUNDLE,
    CONSUMER,
    _contracts,
    decode,
    digest,
    require,
)
from .modeling_bundle import REPOSITORY, _json_bytes
from .publication import DIGEST, target_reference

SERVICES = {"workspace": "workspace", "data-api": "data_api", "modeling": "modeling"}
MANIFEST = "manifest.json"
ARCHIVE = "modeling-contracts-v1.zip"
PROVIDER = CONSUMER.with_name("provider.lock.json")
POLICY = CONSUMER.with_name("compatibility.v1.lock.json")
CASES = CONSUMER.with_name("saved-output.cases.v1.json")
FCF = CONSUMER.with_name("issuer-fcf-yield.v1.json")
PRIOR_RELEASE = "artifacts/reviewed/fmp-expansion-b/publication-verification.json"


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "--no-replace-objects", "--literal-pathspecs", "-C", str(root), *args],
        env=os.environ | {"GIT_NO_LAZY_FETCH": "1"},
        capture_output=True,
        check=False,
    )
    require(result.returncode == 0, "pinned Git input unavailable")
    return result.stdout


def commit(root: Path, revision: str) -> None:
    require(bool(re.fullmatch(r"[0-9a-f]{40}", revision)), "full Git commit SHA required")
    require(git(root, "cat-file", "-t", revision) == b"commit\n", "Git commit required")


def blob(root: Path, revision: str, path: Path) -> bytes:
    entry = git(root, "ls-tree", "--full-tree", "-z", revision, "--", path.as_posix())
    require(
        entry.startswith((b"100644 blob ", b"100755 blob ")),
        f"regular Git file required: {path}",
    )
    return git(root, "cat-file", "blob", entry.split(b" ", 2)[2].split(b"\t", 1)[0].decode())


def contract_files(root: Path, revision: str) -> tuple[dict, dict]:
    consumers = {name: blob(root, revision, name) for name in (CONSUMER, PROVIDER, POLICY, CASES, FCF)}
    lock = decode(consumers[PROVIDER])
    policy = decode(consumers[POLICY])
    adoption = policy["adoption_revision"]
    commit(root, adoption)
    require(
        git(root, "merge-base", adoption, revision).strip().decode() == adoption,
        "consumer adoption must be an ancestor of the release",
    )
    for path in (PROVIDER, CASES, CONSUMER):
        require(
            consumers[path] == blob(root, adoption, path),
            f"adopted consumer input differs: {path}",
        )
    require(
        policy["expectations_sha256"] == digest(consumers[CASES]),
        "consumer cases hash mismatch",
    )

    provider = lock["source_revision"]
    commit(root, provider)
    manifest_path = BUNDLE / MANIFEST
    manifest = blob(root, revision, manifest_path)
    require(
        manifest == blob(root, adoption, manifest_path),
        "adopted provider manifest differs",
    )
    require(
        lock
        == {
            "contract_version": 1,
            "repository": "norandom/QOpenBB",
            "source_revision": provider,
            "bundle": BUNDLE.as_posix(),
            "manifest_sha256": digest(manifest),
        },
        "provider lock mismatch",
    )

    entries = git(root, "ls-tree", "--full-tree", "-r", "-z", revision, "--", BUNDLE.as_posix())
    payloads = {}
    for entry in entries.rstrip(b"\0").split(b"\0"):
        header, name = entry.split(b"\t", 1)
        mode, kind, oid = header.split()
        path = Path(name.decode())
        filename = path.relative_to(BUNDLE).as_posix()
        require(
            mode in {b"100644", b"100755"}
            and kind == b"blob"
            and re.fullmatch(r"[a-z][a-z0-9.-]*\.json", filename) is not None,
            "unexpected provider bundle entry",
        )
        if path != manifest_path:
            payloads[filename] = git(root, "cat-file", "blob", oid.decode())
    accepted = _contracts(manifest, consumers[CONSUMER], payloads)
    require(
        accepted.revision == provider and accepted.consumer["contract_version"] == 1,
        "provider and saved-output identities differ",
    )
    require(
        consumers[CONSUMER] == blob(root, provider, CONSUMER),
        "provider consumer pin differs",
    )
    payloads[MANIFEST] = manifest
    return consumers | {BUNDLE / name: data for name, data in payloads.items()}, {
        "provider": lock,
        "compatibility": policy,
    }


def source_pins(root: Path, revision: str) -> dict:
    lock = decode(blob(root, revision, Path("sources.lock.json")))
    sources = {"modeling": {"repository": REPOSITORY, "revision": revision}}
    for name in ("workspace", "data_api"):
        pin = lock[name]
        sources[name] = {"repository": pin["repository"], "revision": pin["revision"]}
        require(
            bool(re.fullmatch(r"[0-9a-f]{40}", pin["revision"])),
            f"invalid source pin: {name}",
        )
    return sources


def modeling_fingerprints(root: Path, revision: str) -> dict:
    hashes = {name: digest(blob(root, revision, Path(name))) for name in sorted(MODELING_FILES)}
    return {
        "runtime-inputs": digest((json.dumps(hashes, sort_keys=True) + "\n").encode()),
        "runtime-lock": hashes["services/modeling/uv.lock"],
    }


def publication_images(raw: dict, pins: dict, fingerprints: dict, args: argparse.Namespace) -> dict:
    require(set(raw) == SERVICES.keys(), "all three publication reports required")
    result = {}
    for service, source in SERVICES.items():
        report = raw[service]
        remote = report["remote"]
        labels = report["labels"]
        reference = report["reference"]
        repository, separator, immutable = reference.partition("@")
        target_reference(repository, "release-check")
        require(
            separator
            and re.fullmatch(DIGEST, immutable)
            and remote["manifest_digest"] == immutable
            and re.fullmatch(DIGEST, remote["config_digest"])
            and remote["os"] == "linux"
            and remote["architecture"] == "amd64",
            f"invalid published image identity: {service}",
        )
        require(
            type(report["schema_version"]) is int
            and report["schema_version"] == 1
            and report["valid"] is True
            and report["service"] == service
            and labels["org.qopenbb.service"] == service,
            f"image service differs: {service}",
        )
        if service != "data-api":
            expected_repo = f"{args.registry_namespace}/qopenbb-{service}"
            require(repository == expected_repo, f"published repository differs: {service}")
            require(
                report["tag_reference"] == target_reference(expected_repo, args.tag),
                f"published tag differs: {service}",
            )
        if service == "modeling":
            for name, expected in fingerprints.items():
                require(
                    labels[f"org.qopenbb.{name}.sha256"] == expected,
                    f"Modeling {name} differs",
                )
        else:
            pin = pins[source]
            require(
                labels[f"org.qopenbb.source.{source}"] == pin["revision"]
                and labels[f"org.qopenbb.repository.{source}"] == pin["repository"],
                f"published counterpart differs from source pin: {service}",
            )
        result[service] = {
            "reference": reference,
            "manifest_digest": immutable,
            "config_digest": remote["config_digest"],
            "os": "linux",
            "architecture": "amd64",
        }
        if service != "data-api":
            result[service]["tag_reference"] = report["tag_reference"]
    return result


def verify_reused_image(prior: dict, image: dict, pin: dict) -> None:
    previous = prior["images"]["data-api"]
    require(
        prior["status"] == "VERIFIED"
        and prior["sources"]["data_api"] == pin["revision"]
        and previous["reference"] == image["reference"]
        and previous["manifest_digest"] == image["manifest_digest"]
        and previous["config_digest"] == image["config_digest"]
        and previous["platform"] == "linux/amd64",
        "reused Data API differs from prior verified release",
    )


def verify_pull(raw: dict, images: dict) -> dict:
    for phase in ("before", "after"):
        require(set(raw[phase]) == SERVICES.keys(), f"incomplete pull report: {phase}")
        for service, expected in images.items():
            observed = raw[phase][service]
            require(
                observed["reference"] == expected["reference"]
                and observed["image"] in {expected["manifest_digest"], expected["config_digest"]},
                f"pulled image differs: {phase}/{service}",
            )
    return {
        phase: {service: records["image"] for service, records in raw[phase].items()}
        for phase in ("before", "after")
    }


def reviewed_hashes(root: Path, revision: str, names: list[str]) -> dict:
    require(len(set(names)) == len(names), "duplicate evidence path")
    sync = decode(blob(root, revision, Path("artifacts/reviewed/sync-manifest.json")))
    expected = {}
    for entry in sync["entries"]:
        name = entry["publishedpath"]
        if name in names:
            require(name not in expected, f"duplicate reviewed manifest entry: {name}")
            expected[name] = entry["publishedSHA256"]
    result = {}
    for name in names:
        require(
            re.fullmatch(
                r"artifacts/reviewed/(?:[A-Za-z0-9_-]+/)+[A-Za-z0-9_.-]+\.(?:md|json)",
                name,
            )
            is not None,
            "evidence must be a reviewed Markdown or JSON repository path",
        )
        data = blob(root, revision, Path(name))
        require(bool(data.strip()), f"empty evidence: {name}")
        actual = digest(data)
        require(expected.get(name) == actual, f"reviewed evidence hash differs: {name}")
        result[name] = actual
    return result


def contract_zip(files: dict) -> bytes:
    buffer = BytesIO()
    with ZipFile(buffer, "w", compression=ZIP_STORED) as archive:
        for name, data in sorted((path.as_posix(), data) for path, data in files.items()):
            entry = ZipInfo(name)
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(entry, data)
    return buffer.getvalue()


def assets(args: argparse.Namespace) -> dict[str, bytes]:
    commit(args.root, args.revision)
    project = tomllib.loads(blob(args.root, args.revision, Path("services/modeling/pyproject.toml")).decode())
    version = project["project"]["version"]
    require(
        re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version) and args.tag == f"modeling-v{version}",
        "release tag must match the Modeling package version",
    )
    files, contracts = contract_files(args.root, args.revision)
    pins = source_pins(args.root, args.revision)
    fingerprints = modeling_fingerprints(args.root, args.revision)
    images = publication_images(decode(args.images.read_bytes()), pins, fingerprints, args)
    pull_data = args.pulled.read_bytes()
    pulled = verify_pull(decode(pull_data), images)
    evidence_paths = list(args.evidence)
    if args.prior_release not in evidence_paths:
        evidence_paths.append(args.prior_release)
    evidence = reviewed_hashes(args.root, args.revision, evidence_paths)
    prior_hash = evidence[args.prior_release]
    evidence = {name: evidence[name] for name in args.evidence}
    prior = decode(blob(args.root, args.revision, Path(args.prior_release)))
    verify_reused_image(prior, images["data-api"], pins["data_api"])
    archive = contract_zip(files)
    manifest = {
        "schema_version": 1,
        "release": {
            "tag": args.tag,
            "version": version,
            "repository": REPOSITORY,
            "revision": args.revision,
        },
        "sources": pins,
        "images": images,
        "modeling_build": fingerprints,
        "contracts": contracts
        | {
            "archive": {"path": ARCHIVE, "sha256": digest(archive)},
            "files": {path.as_posix(): digest(data) for path, data in files.items()},
        },
        "evidence": {
            "reviewed_source_files": evidence,
            "reused_data_api_release": {
                "tag": prior["release"],
                "path": args.prior_release,
                "sha256": prior_hash,
            },
            "published_pull": {"report_sha256": digest(pull_data), "image_ids": pulled},
        },
    }
    return {ARCHIVE: archive, MANIFEST: _json_bytes(manifest)}


def bundle(action: str, output: Path, expected: dict[str, bytes]) -> None:
    if action == "write":
        output.mkdir(parents=True, exist_ok=False)
        # Write the manifest last so a partial write can never advertise a complete bundle.
        for name, data in expected.items():
            with (output / name).open("xb") as stream:
                stream.write(data)
    require(
        not output.is_symlink() and not output.is_junction(),
        "bundle must be a regular directory",
    )
    require(
        {path.name for path in output.iterdir()} == expected.keys(),
        "unexpected release asset set",
    )
    for name, data in expected.items():
        path = output / name
        require(
            stat.S_ISREG(path.lstat().st_mode) and path.read_bytes() == data,
            f"release asset differs: {name}",
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("write", "check"))
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository with pinned Git objects",
    )
    parser.add_argument("--revision", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--registry-namespace", required=True)
    parser.add_argument("--images", type=Path, required=True)
    parser.add_argument("--pulled", type=Path, required=True, help="Published before/after image report")
    parser.add_argument(
        "--evidence",
        action="append",
        required=True,
        help="Reviewed path at the release revision",
    )
    parser.add_argument(
        "--prior-release",
        default=PRIOR_RELEASE,
        help="Reviewed Data API publication record",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        bundle(args.action, args.output, assets(args))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        print(f"release assets: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
