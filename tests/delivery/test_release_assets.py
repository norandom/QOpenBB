"""Exercise the release assets against the adopted contract and image report format."""

import json
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile

import pytest
from qopenbb_ci import release_assets

ROOT = Path(__file__).resolve().parents[2]
REVISION = "5407b3f335d9de413f3d988b7a11fbc2a77e7f62"
TAG = "modeling-v0.1.0"
NAMESPACE = "example.test/norandom"
EVIDENCE = "artifacts/reviewed/factor-signals/workspace-modeling-image.md"
PINS = {
    "workspace": "aa1a625e5d9478f023226b9ac9acd3bcfb71da4a",
    "data_api": "5583c958d35282cb59037aae8218cec31d540697",
}


@pytest.fixture
def inputs(tmp_path):
    images = {}
    pulls = {"before": {}, "after": {}}
    for index, (service, source) in enumerate(release_assets.SERVICES.items(), 1):
        repository = f"{NAMESPACE}/qopenbb-{service}"
        manifest, config = (f"sha256:{number:064x}" for number in (index, index + 3))
        reference = f"{repository}@{manifest}"
        if service == "data-api":
            prior = json.loads((ROOT / release_assets.PRIOR_RELEASE).read_bytes())[
                "images"
            ][service]
            reference, manifest, config = (
                prior[key] for key in ("reference", "manifest_digest", "config_digest")
            )
            repository = reference.split("@")[0]
        labels = {"org.qopenbb.service": service}
        if service == "modeling":
            labels.update(
                {
                    "org.qopenbb.runtime-inputs.sha256": "7f8f876752ccf8a53e371dede8d49edff690c70b7419c090125365302e3a2b00",
                    "org.qopenbb.runtime-lock.sha256": "ff215e49f121e302af3e7f40493a050bbd898d9cfca5ac229047b09b7b730664",
                }
            )
        else:
            labels.update(
                {
                    f"org.qopenbb.source.{source}": PINS[source],
                    f"org.qopenbb.repository.{source}": f"https://github.com/norandom/openbb-{service}.git",
                }
            )
        if service == "data-api":
            labels["org.qopenbb.source.workspace"] = "a" * 40
        images[service] = {
            "schema_version": 1,
            "valid": True,
            "service": service,
            "reference": reference,
            "tag_reference": f"{repository}:{'previous-release' if service == 'data-api' else TAG}",
            "remote": {
                "os": "linux",
                "architecture": "amd64",
                "manifest_digest": manifest,
                "config_digest": config,
            },
            "labels": labels,
        }
        pulls["before"][service] = {"reference": reference, "image": config}
        pulls["after"][service] = {"reference": reference, "image": manifest}
    return images, pulls


def run_cli(
    tmp_path, inputs, *, action="write", output="assets", evidence=EVIDENCE, tag=TAG
):
    images = tmp_path / "published.json"
    pulled = tmp_path / "pulled.json"
    images.write_text(json.dumps(inputs[0]))
    pulled.write_text(json.dumps(inputs[1]))
    return release_assets.main(
        [
            action,
            "--root",
            str(ROOT),
            "--revision",
            REVISION,
            "--tag",
            tag,
            "--registry-namespace",
            NAMESPACE,
            "--images",
            str(images),
            "--pulled",
            str(pulled),
            "--evidence",
            evidence,
            "--output",
            str(tmp_path / output),
        ]
    )


def test_cli_reproducible_archive_and_manifest(tmp_path, inputs):
    assert run_cli(tmp_path, inputs) == 0
    assert run_cli(tmp_path, inputs, output="second-build") == 0
    assert run_cli(tmp_path, inputs, action="check") == 0
    output = tmp_path / "assets"
    index = json.loads((output / "manifest.json").read_bytes())
    assert index["release"]["revision"] == REVISION
    assert index["release"]["version"] == "0.1.0"
    assert {name: index["sources"][name]["revision"] for name in PINS} == PINS
    assert (
        index["contracts"]["provider"]["source_revision"]
        == "7f62bf5fd1f9bede9e08030a5db5f20a88eeb4aa"
    )
    assert (
        index["contracts"]["compatibility"]["adoption_revision"]
        == "fe90c945a24a999125cd02434bc967bb8541166d"
    )
    assert index["evidence"]["reviewed_source_files"] == {
        EVIDENCE: "a29d1c02725019c7522d25f19290500fd206d4589b6d6cafcd237df1844c9afc",
    }
    assert (
        index["evidence"]["published_pull"]["report_sha256"]
        == sha256(
            (tmp_path / "pulled.json").read_bytes(),
        ).hexdigest()
    )
    archive = output / "modeling-contracts-v1.zip"
    assert (
        sha256(archive.read_bytes()).hexdigest()
        == index["contracts"]["archive"]["sha256"]
    )
    with ZipFile(archive) as payload:
        assert payload.namelist() == sorted(index["contracts"]["files"])
        assert len(payload.namelist()) == 20
        for filename in payload.namelist():
            assert (
                sha256(payload.read(filename)).hexdigest()
                == index["contracts"]["files"][filename]
            )
    for path in output.iterdir():
        assert path.read_bytes() == (tmp_path / "second-build" / path.name).read_bytes()
    assert run_cli(tmp_path, inputs) == 1
    archive.write_bytes(archive.read_bytes() + b"tampered")
    assert run_cli(tmp_path, inputs, action="check") == 1


@pytest.mark.parametrize(
    ("service", "field", "value", "message"),
    [
        (
            "modeling",
            "org.qopenbb.runtime-inputs.sha256",
            "0" * 64,
            "runtime-inputs differs",
        ),
        (
            "modeling",
            "org.qopenbb.runtime-lock.sha256",
            "0" * 64,
            "runtime-lock differs",
        ),
        ("workspace", "org.qopenbb.source.workspace", "f" * 40, "counterpart differs"),
        ("data-api", "org.qopenbb.source.data_api", "f" * 40, "counterpart differs"),
        (
            "modeling",
            "tag_reference",
            "example.test/norandom/qopenbb-modeling:prior",
            "published tag differs",
        ),
        ("workspace", "architecture", "arm64", "published image identity"),
    ],
)
def test_publication_identity_must_match_pins(
    tmp_path, inputs, capsys, service, field, value, message
):
    image = inputs[0][service]
    record = (
        image["labels"]
        if field.startswith("org.")
        else image["remote"]
        if field == "architecture"
        else image
    )
    record[field] = value
    assert run_cli(tmp_path, inputs) == 1
    assert message in capsys.readouterr().err
    assert not (tmp_path / "assets").exists()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("reference", "localhost:5000/candidate"),
        ("image", "sha256:" + "f" * 64),
    ],
)
def test_pull_report_must_observe_published_images(
    tmp_path, inputs, capsys, field, value
):
    inputs[1]["after"]["modeling"][field] = value
    assert run_cli(tmp_path, inputs) == 1
    assert "pulled image differs: after/modeling" in capsys.readouterr().err


def test_release_tag_matches_version(tmp_path, inputs, capsys):
    assert run_cli(tmp_path, inputs, tag="modeling-v0.2.0") == 1
    assert "must match the Modeling package version" in capsys.readouterr().err


def test_published_namespace_is_required_even_when_pull_matches(
    tmp_path, inputs, capsys
):
    published, pulls = inputs
    image = published["workspace"]
    for key in ("reference", "tag_reference"):
        image[key] = image[key].replace(NAMESPACE, "other.test/norandom")
    for phase in pulls.values():
        phase["workspace"]["reference"] = image["reference"]
    assert run_cli(tmp_path, inputs) == 1
    assert "published repository differs: workspace" in capsys.readouterr().err


def test_reused_data_api_must_match_prior_verified_release(tmp_path, inputs, capsys):
    published, pulls = inputs
    image = published["data-api"]
    digest = "sha256:" + "a" * 64
    image["reference"] = image["reference"].partition("@")[0] + "@" + digest
    image["remote"]["manifest_digest"] = digest
    for phase in pulls.values():
        phase["data-api"].update(reference=image["reference"], image=digest)
    assert run_cli(tmp_path, inputs) == 1
    assert (
        "reused Data API differs from prior verified release" in capsys.readouterr().err
    )


@pytest.mark.parametrize(
    ("path", "message"),
    [
        (release_assets.CASES, "adopted consumer input differs"),
        (release_assets.BUNDLE / "apps.json", "bundle file set or digest mismatch"),
        (Path(EVIDENCE), "reviewed evidence hash differs"),
    ],
)
def test_content_hashes_are_independently_checked(
    monkeypatch, tmp_path, inputs, capsys, path, message
):
    original = release_assets.blob
    original_git = release_assets.git

    def mutated_blob(root, revision, name):
        data = original(root, revision, name)
        return data + b"\n" if revision == REVISION and name == path else data

    def mutated_git(root, *args):
        data = original_git(root, *args)
        return data + b"\n" if args == ("cat-file", "blob", payload_id) else data

    payload_id = original_git(ROOT, "rev-parse", f"{REVISION}:{path}").decode().strip()
    if path == release_assets.BUNDLE / "apps.json":
        monkeypatch.setattr(release_assets, "git", mutated_git)
    else:
        monkeypatch.setattr(release_assets, "blob", mutated_blob)
    assert run_cli(tmp_path, inputs) == 1
    assert message in capsys.readouterr().err
    assert not (tmp_path / "assets").exists()
