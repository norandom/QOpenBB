"""Alpha publication preserves immutable identity before moving development tags."""
import io
import json
from pathlib import Path
import shutil
import subprocess
import tarfile

import pytest

from qopenbb_ci import alpha_cli
from qopenbb_ci.images import inspect_archive


@pytest.fixture
def candidate(tmp_path, monkeypatch):
    root = tmp_path / "candidate"
    summary = {"schema_version": 1, "release_version": "alpha-123-1", "images": {}}
    state = {"commands": [], "tags": {}, "remotes": {}, "fail": None, "mismatch": None}
    configs = {}
    for index, service in enumerate(alpha_cli.SERVICES):
        folder = root / service
        folder.mkdir(parents=True)
        labels = {"org.qopenbb.service": service, "org.qopenbb.provenance.sha256": "b" * 64}
        for source in ("workspace", "data_api"):
            labels["org.qopenbb.source." + source] = "c" * 40
            labels["org.qopenbb.repository." + source] = "https://github.com/norandom/" + source
        config = json.dumps({"architecture": "amd64", "os": "linux", "config": {"Labels": labels}}).encode()
        archive = folder / "image.tar"
        with tarfile.open(archive, "w") as bundle:
            entries = {"manifest.json": json.dumps([{"Config": "config.json", "Layers": []}]).encode(),
                       "config.json": config}
            for name, content in entries.items():
                member = tarfile.TarInfo(name)
                member.size = len(content)
                bundle.addfile(member, io.BytesIO(content))
        identity = inspect_archive(archive)
        image = identity["image_config_digest"]
        configs[image] = (archive, labels, "sha256:" + str(index + 1) * 64)
        (folder / "load.json").write_text(json.dumps({**identity, "loaded_image_id": image}))
        summary["images"][service] = {"image": image, "report": "/original/absolute/load.json"}
    (root / "summary.json").write_text(json.dumps(summary))

    def execute(command, **kwargs):
        state["commands"].append(command)
        args = command[1:]
        output = ""
        if args[:2] == ["image", "load"]:
            output = "Loaded image ID: " + inspect_archive(Path(args[3]))["image_config_digest"] + "\n"
        elif args[:2] == ["image", "inspect"]:
            output = json.dumps([{"Id": args[2], "Architecture": "amd64", "Os": "linux",
                                  "Config": {"Labels": configs[args[2]][1]}}])
        elif args[:2] == ["image", "save"]:
            shutil.copyfile(configs[args[4]][0], args[3])
        elif args[:2] == ["image", "tag"]:
            state["tags"][args[3]] = args[2]
        elif args[:2] == ["image", "push"]:
            if state["fail"] and state["fail"] in args[2]:
                raise subprocess.CalledProcessError(1, command, output="private diagnostics")
            image = state["tags"][args[2]]
            digest = configs[image][2]
            state["remotes"][args[2]] = (digest, image)
            state["remotes"][args[2].rsplit(":", 1)[0] + "@" + digest] = (digest, image)
            output = "digest: " + digest + " size: 123\n"
        elif args[:3] == ["manifest", "inspect", "--verbose"]:
            digest, image = state["remotes"][args[3]]
            if state["mismatch"] == "config" and args[3].endswith(":latest"):
                image = "sha256:" + "f" * 64
            if state["mismatch"] == "digest" and args[3].endswith(":latest"):
                digest = "sha256:" + "f" * 64
            output = json.dumps({"Descriptor": {"digest": digest, "platform": {
                "architecture": "amd64", "os": "linux"}}, "SchemaV2Manifest": {
                "schemaVersion": 2, "config": {"digest": image}}})
        else:
            raise AssertionError(command)
        return subprocess.CompletedProcess(command, 0, stdout=output)

    monkeypatch.setattr(subprocess, "run", execute)
    monkeypatch.setattr(subprocess, "check_output", lambda command, **kw: execute(command, **kw).stdout)
    return root, state


def run(candidate, tmp_path):
    root, _ = candidate
    output = tmp_path / "release/manifest.json"
    code = alpha_cli.main(["--build-output", str(root), "--registry-namespace",
                           "registry.example/owner", "--manifest", str(output)])
    return code, output


def test_pair_published_before_latest_with_relocatable_reports(candidate, tmp_path):
    code, output = run(candidate, tmp_path)
    assert code == 0
    manifest = json.loads(output.read_text())
    assert manifest["release_version"] == "alpha-123-1"
    pushes = [command[3] for command in candidate[1]["commands"] if command[1:3] == ["image", "push"]]
    assert pushes == ["registry.example/owner/qopenbb-" + service + ":" + tag
                      for tag in ("alpha-123-1", "latest") for service in alpha_cli.SERVICES]
    for service, image in manifest["images"].items():
        assert image["reference"].startswith("registry.example/owner/qopenbb-" + service + "@sha256:")
        assert image["latest_remote"] == image["remote"]
        assert image["sources"] == manifest["sources"]


@pytest.mark.parametrize("failure", ["qopenbb-workspace:alpha", "qopenbb-data-api:alpha",
                                   "qopenbb-workspace:latest", "qopenbb-data-api:latest"])
def test_partial_failure_has_no_manifest(candidate, tmp_path, failure, capsys):
    candidate[1]["fail"] = failure
    code, output = run(candidate, tmp_path)
    assert code == 2
    assert not output.exists()
    if ":alpha" in failure:
        assert not any(command[-1].endswith(":latest") for command in candidate[1]["commands"])
    assert "private" not in str(capsys.readouterr())


@pytest.mark.parametrize("mismatch", ["config", "digest"])
def test_latest_identity_mismatch_has_no_manifest(candidate, tmp_path, mismatch):
    candidate[1]["mismatch"] = mismatch
    code, output = run(candidate, tmp_path)
    assert code == 2
    assert not output.exists()


@pytest.mark.parametrize("mutation", ["summary-id", "report", "service", "version", "source"])
def test_invalid_pair_fails_before_registry_mutation(candidate, tmp_path, mutation):
    root, state = candidate
    summary = json.loads((root / "summary.json").read_text())
    report_path = root / "data-api/load.json"
    report = json.loads(report_path.read_text())
    if mutation == "summary-id":
        summary["images"]["data-api"]["image"] = "sha256:" + "f" * 64
    elif mutation == "version":
        summary["release_version"] = "latest"
    elif mutation == "service":
        report["labels"]["org.qopenbb.service"] = "workspace"
    elif mutation == "source":
        report["labels"]["org.qopenbb.source.workspace"] = "d" * 40
    else:
        report["archive_sha256"] = "f" * 64
    report_path.write_text(json.dumps(report))
    (root / "summary.json").write_text(json.dumps(summary))
    code, output = run(candidate, tmp_path)
    assert code == 2
    assert not output.exists()
    assert not state["commands"]


def test_differing_valid_source_sets_fail_before_publication(candidate, tmp_path, monkeypatch):
    verify = alpha_cli.publication.verify_sources

    def sources(identity):
        result = verify(identity)
        if identity["labels"]["org.qopenbb.service"] == "data-api":
            result["workspace"]["revision"] = "d" * 40
        return result

    monkeypatch.setattr(alpha_cli.publication, "verify_sources", sources)
    code, output = run(candidate, tmp_path)
    assert code == 2
    assert not output.exists()
    assert not candidate[1]["commands"]


def test_existing_manifest_is_preserved_before_any_commands(candidate, tmp_path):
    output = tmp_path / "release/manifest.json"
    output.parent.mkdir()
    output.write_text("previous release")
    assert run(candidate, tmp_path)[0] == 2
    assert output.read_text() == "previous release"
    assert not candidate[1]["commands"]


def test_post_promotion_alias_race_fails_without_manifest(candidate, tmp_path, monkeypatch):
    observe = alpha_cli.publication.remote_identity
    counts = {}

    def raced(reference):
        remote = observe(reference)
        counts[reference] = counts.get(reference, 0) + 1
        if reference.endswith("workspace:latest") and counts[reference] == 2:
            return {**remote, "config_digest": "sha256:" + "f" * 64}
        return remote

    monkeypatch.setattr(alpha_cli.publication, "remote_identity", raced)
    code, output = run(candidate, tmp_path)
    assert code == 2
    assert not output.exists()
