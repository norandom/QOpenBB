"""Publish a completed prototype build and promote verified development aliases."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

from qopenbb_ci import publication

SERVICES = ("workspace", "data-api")


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--build-output", type=Path, required=True)
    result.add_argument("--registry-namespace", required=True)
    result.add_argument("--manifest", type=Path, required=True)
    return result


def inputs(directory: Path, namespace: str) -> tuple[str, dict]:
    summary = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
    version = summary["release_version"]
    if not isinstance(version, str) or not version.startswith("alpha-"):
        raise ValueError("unique alpha release version required")
    if summary.get("schema_version") != 1 or set(summary["images"]) != set(SERVICES):
        raise ValueError("completed two-service build summary required")
    reports = {}
    sources = None
    for service in SERVICES:
        publication.target_reference(namespace + "/qopenbb-" + service, version)
        entry = summary["images"][service]
        # Standard build outputs remain relocatable when retained as CI artifacts.
        report = json.loads((directory / service / "load.json").read_text(encoding="utf-8"))
        archive = directory / service / "image.tar"
        identity = publication.inspect_archive(archive)
        if any(report.get(key) != value for key, value in identity.items()):
            raise ValueError("load report differs from archive")
        if (report.get("loaded_image_id") != entry["image"]
                or not re.fullmatch(publication.DIGEST, entry["image"])
                or identity["labels"].get("org.qopenbb.service") != service):
            raise ValueError("build service identity differs from summary")
        observed_sources = publication.verify_sources(identity)
        if sources is not None and sources != observed_sources:
            raise ValueError("service source revisions differ")
        sources = observed_sources
        reports[service] = (archive, report)
    return version, reports


def promote(published: dict, repository: str) -> dict:
    latest = repository + ":latest"
    publication.docker("image", "tag", published["loaded_image_id"], latest)
    output = publication.docker("image", "push", latest)
    matches = re.findall(r"\bdigest: (" + publication.DIGEST + r")\b", output)
    expected = published["remote"]
    if matches != [expected["manifest_digest"]]:
        raise ValueError("latest push differs from immutable image")
    if publication.remote_identity(latest) != expected:
        raise ValueError("latest remote differs from immutable image")
    return {"latest_reference": latest, "latest_remote": expected}


def publish_build(directory: Path, namespace: str) -> dict:
    version, reports = inputs(directory, namespace)
    images = {}
    for service in SERVICES:
        archive, report = reports[service]
        images[service] = publication.publish(archive, report, namespace + "/qopenbb-" + service, version)
    # Both immutable images must be verified before either mutable alias moves.
    for service in SERVICES:
        images[service].update(promote(images[service], namespace + "/qopenbb-" + service))
    # Recheck the pair after promotion to catch alias races during this run.
    for published in images.values():
        if publication.remote_identity(published["latest_reference"]) != published["remote"]:
            raise ValueError("latest alias changed during pair promotion")
    return {"schema_version": 1, "valid": True, "channel": "alpha",
            "release_version": version, "sources": images["workspace"]["sources"],
            "images": images}


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.manifest.exists():
            raise ValueError("release manifest already exists")
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        result = publish_build(args.build_output, args.registry_namespace)
        with args.manifest.open("x", encoding="utf-8") as stream:
            stream.write(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(json.dumps({"valid": False, "error": type(error).__name__}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

