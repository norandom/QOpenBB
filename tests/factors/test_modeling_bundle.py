import hashlib
import json
import sys
from types import ModuleType

import pytest

REVISION = "a" * 40
PAYLOAD = "schemas/example.json"


@pytest.fixture
def bundle(tmp_path, monkeypatch):
    from qopenbb_ci import modeling_bundle

    documents = {PAYLOAD: {"z": "café", "a": True}, "methods.json": [{"id": "example"}]}
    module = ModuleType("qopenbb_ci.modeling_documents")
    module.documents = lambda: documents
    monkeypatch.setitem(sys.modules, module.__name__, module)
    consumer = tmp_path / "consumer.json"
    consumer.write_bytes(
        b'{ "consumer_id": "workspace.saved", "contract_version": 1 }\r\n'
    )
    monkeypatch.setattr(
        modeling_bundle, "_verify_source", lambda *args: None, raising=False
    )
    output = tmp_path / "bundle"

    def run(action, revision=REVISION, destination=output):
        return modeling_bundle.main(
            [
                action,
                "--revision",
                revision,
                "--output",
                str(destination),
                "--consumer",
                str(consumer),
            ]
        )

    return run, output, consumer, documents


def test_bundle_reproduces_canonical_bytes_and_hashes(bundle, tmp_path):
    run, output, consumer, documents = bundle
    assert run("write") == 0
    assert run("check") == 0
    assert (output / PAYLOAD).read_bytes() == '{"a":true,"z":"café"}\n'.encode()
    assert (output / "methods.json").read_bytes() == b'[{"id":"example"}]\n'
    manifest = (output / "manifest.json").read_bytes()
    assert json.loads(manifest) == {
        "format_version": 1,
        "hash_algorithm": "sha256",
        "consumer_id": "workspace.saved",
        "consumer_contract_version": 1,
        "consumer_source_revision": REVISION,
        "repository": "https://github.com/norandom/QOpenBB.git",
        "source_revision": REVISION,
        "consumer_manifest_sha256": hashlib.sha256(consumer.read_bytes()).hexdigest(),
        "files": {
            path: hashlib.sha256((output / path).read_bytes()).hexdigest()
            for path in documents
        },
    }
    documents[PAYLOAD] = {"a": True, "z": "café"}
    second = tmp_path / "second"
    assert run("write", destination=second) == 0
    assert (second / "manifest.json").read_bytes() == manifest
    assert run("write") == 0


@pytest.mark.parametrize(
    "drift", ["payload", "manifest", "consumer", "extra", "missing"]
)
def test_check_reports_exact_drift(bundle, capsys, drift):
    run, output, consumer, _ = bundle
    assert run("write") == 0
    if drift == "consumer":
        consumer.write_bytes(consumer.read_bytes().strip())
        expected = "manifest.json"
    elif drift == "extra":
        (output / "extra.json").touch()
        expected = "extra.json"
    elif drift == "missing":
        (output / PAYLOAD).unlink()
        expected = PAYLOAD
    else:
        expected = PAYLOAD if drift == "payload" else "manifest.json"
        path = output / expected
        path.write_bytes(path.read_bytes() + b" ")
    assert run("check") != 0
    assert expected in capsys.readouterr().err


@pytest.mark.parametrize("revision", ["HEAD", "v1.0", "a" * 39, "g" * 40])
def test_rejects_mutable_or_invalid_revision(bundle, revision):
    run, output, _, _ = bundle
    assert run("write", revision) != 0
    assert not output.exists()


@pytest.mark.parametrize("entry", [PAYLOAD, "unrelated.txt"])
def test_write_preserves_existing_files(bundle, entry):
    run, output, _, _ = bundle
    existing = output / entry
    existing.parent.mkdir(parents=True)
    existing.write_bytes(b"owned elsewhere")
    assert run("write") != 0
    assert existing.read_bytes() == b"owned elsewhere"
    assert not (output / "manifest.json").exists()


@pytest.mark.parametrize(
    "unsafe",
    [
        "../escape.json",
        "/absolute.json",
        "manifest.json",
        "schemas",
        "schemas//alias.json",
        "C:/drive.json",
    ],
)
def test_unsafe_document_paths_fail_before_writing(bundle, unsafe, capsys):
    run, output, _, documents = bundle
    documents[unsafe] = {}
    assert run("write") != 0
    assert unsafe in capsys.readouterr().err
    assert not output.exists()


def test_refuses_symlinked_payload_directory(bundle, tmp_path):
    run, output, _, _ = bundle
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    output.mkdir()
    (output / "schemas").symlink_to(elsewhere, target_is_directory=True)
    assert run("write") != 0
    assert run("check") != 0
    assert list(elsewhere.iterdir()) == []


def test_check_regenerates_against_current_documents_and_revision(bundle, capsys):
    run, _, _, documents = bundle
    assert run("write") == 0
    assert run("check", "b" * 40) != 0
    assert "manifest.json" in capsys.readouterr().err
    documents[PAYLOAD] = {"updated": True}
    assert run("check") != 0
    assert PAYLOAD in capsys.readouterr().err


@pytest.mark.parametrize(
    "invalid",
    [
        b"junk",
        b"[]",
        b'{"consumer_id":"widget","contract_version":1,"extra":NaN}',
        b'{"consumer_id":"widget","consumer_id":"other","contract_version":1}',
        b'{"consumer_id":" ","contract_version":1}',
        b'{"consumer_id":"widget","contract_version":true}',
        b'{"consumer_id":"widget","contract_version":0}',
    ],
)
def test_requires_consumer_json_identity(bundle, invalid, capsys):
    run, output, consumer, _ = bundle
    consumer.write_bytes(invalid)
    assert run("write") != 0
    assert "consumer manifest" in capsys.readouterr().err
    assert not output.exists()


def test_write_can_resume_after_interrupted_publication(bundle, monkeypatch):
    from qopenbb_ci import modeling_bundle

    run, output, _, _ = bundle
    link = modeling_bundle.os.link

    def fail_second(source, target):
        if target.name == "example.json":
            raise OSError("interrupted")
        link(source, target)

    with monkeypatch.context() as interrupted:
        interrupted.setattr(modeling_bundle.os, "link", fail_second)
        assert run("write") != 0
    assert (output / "methods.json").read_bytes() == b'[{"id":"example"}]\n'
    assert not (output / PAYLOAD).exists()
    assert not (output / "manifest.json").exists()
    assert run("write") == 0
    assert run("check") == 0


@pytest.fixture
def source_repo(tmp_path):
    import subprocess

    from qopenbb_ci import modeling_bundle

    def git(*args):
        return (
            subprocess.check_output(["git", "-C", str(tmp_path), *args])
            .decode()
            .strip()
        )

    git("init", "-q")
    consumer = tmp_path / "consumer.json"
    consumer.write_bytes(b'{"consumer_id":"widget","contract_version":1}')
    for name in modeling_bundle.SOURCE_INPUTS:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("original\n", encoding="utf-8")
    git("add", ".")
    git(
        "-c",
        "user.name=Bundle Test",
        "-c",
        "user.email=bundle@example.test",
        "commit",
        "-qm",
        "source",
    )
    return modeling_bundle, git("rev-parse", "HEAD"), consumer, tmp_path


@pytest.mark.parametrize(
    "change", ["clean", "absent_sha", "dirty", "missing", "untracked", "consumer"]
)
def test_write_source_guard_checks_local_commit_and_worktree(source_repo, change):
    module, revision, consumer, root = source_repo
    exporter = root / module.EXPORTER / "modeling_documents.py"
    if change == "clean":
        module._verify_source(revision, consumer, consumer.read_bytes(), root=root)
        return
    if change == "absent_sha":
        revision = "a" * 40
    elif change == "missing":
        exporter.unlink()
    elif change == "untracked":
        (root / module.DATA_API / "untracked.py").touch()
    elif change == "consumer":
        consumer.write_bytes(consumer.read_bytes() + b"\n")
    else:
        exporter.write_text("changed\n", encoding="utf-8")
    with pytest.raises(
        ValueError, match="Git source verification|source input differs"
    ):
        module._verify_source(revision, consumer, consumer.read_bytes(), root=root)


def test_check_does_not_consult_git(bundle, monkeypatch):
    from qopenbb_ci import modeling_bundle

    run, _, _, _ = bundle
    assert run("write") == 0

    def unexpected_git(*args):
        pytest.fail("check must work without local Git objects")

    monkeypatch.setattr(modeling_bundle, "_git", unexpected_git)
    assert run("check") == 0
