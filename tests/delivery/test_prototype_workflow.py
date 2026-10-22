"""Release events build tagged sources and enrich the existing prerelease."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import textwrap
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = (ROOT / ".github/workflows/prototype.yml").read_text()


def job_text(name):
    return WORKFLOW.split("  " + name + ":\n", 1)[1].split("\n  publish-alpha:", 1)[0]


def step(name):
    return WORKFLOW.split("      - name: " + name + "\n", 1)[1].split("\n      - ", 1)[0]


def expression(line, context):
    source = line.strip().removeprefix("${{").removesuffix("}}").strip()
    return eval(source.replace("&&", " and ").replace("||", " or "),
                {"__builtins__": {}}, context)


@pytest.mark.parametrize("event,ref,build,prerelease,checks,publishes", [
    ("pull_request", "refs/pull/1/merge", False, False, True, False),
    ("push", "refs/heads/main", False, False, True, False),
    ("workflow_dispatch", "refs/heads/main", False, False, True, False),
    ("workflow_dispatch", "refs/heads/main", True, False, True, True),
    ("workflow_dispatch", "refs/heads/topic", True, False, True, False),
    ("release", "refs/tags/v0.2.0-preview", False, True, True, True),
    ("release", "refs/tags/v0.2.0", False, False, False, False),
])
def test_event_policy(event, ref, build, prerelease, checks, publishes):
    context = {"github": SimpleNamespace(event_name=event, ref=ref,
               event=SimpleNamespace(release=SimpleNamespace(prerelease=prerelease))),
               "inputs": SimpleNamespace(build_images=build)}
    candidate = job_text("candidate")
    check_condition = re.search(r"^    if: (.+)$", candidate, re.M)[1]
    build_condition = re.search(r"^      BUILD_IMAGES: (.+)$", candidate, re.M)[1]
    publish_condition = re.search(r"^    if: (.+)$", job_text("publish-alpha"), re.M)[1]
    assert bool(expression(check_condition, context)) is checks
    assert bool(expression(build_condition, context)) is publishes
    assert bool(expression(publish_condition, context)) is publishes
    for name in ("Install pinned Dagger CLI", "Build candidate images through Dagger",
                 "Retain built image archives"):
        assert "env.BUILD_IMAGES == 'true'" in step(name)


def test_release_trigger_checkout_and_unique_build_identity():
    assert "  release:\n    types: [published]\n" in WORKFLOW
    assert WORKFLOW.count("ref: ${{ github.sha }}") == 2
    assert "github.event.release.target_commitish" not in WORKFLOW
    assert "--release-version alpha-${{ github.run_id }}-${{ github.run_attempt }}" in WORKFLOW
    assert "    concurrency:\n      group: prototype-alpha-publication\n      cancel-in-progress: false" in job_text("publish-alpha")
    assert "github.event_name == 'workflow_dispatch'" in step("Create tagged alpha prerelease")
    assert "github.event_name == 'release'" in step("Attach images to published prerelease")
    assert "tests/delivery/test_prototype_workflow.py" in (ROOT / "pipeline/ci.sh").read_text()


def run_block(name, directory, environment):
    block = textwrap.dedent(step(name).split("run: |\n", 1)[1])
    assert "${{" not in block
    subprocess.run(["bash", "-euo", "pipefail", "-c", block], cwd=directory,
                   env={**os.environ, **environment}, check=True)


@pytest.mark.skipif(os.name != "posix", reason="Release plumbing runs on a Linux runner")
def test_existing_release_upload_keeps_notes_and_attaches_exact_source(tmp_path):
    output = tmp_path / "artifacts/alpha-release"
    output.mkdir(parents=True)
    manifest = {"release_version": "alpha-123-2", "images": {"workspace": {}, "data-api": {}}}
    (output / "manifest.json").write_text(json.dumps(manifest))
    (tmp_path / "compose.yaml").write_text("services: {}\n")
    (tmp_path / ".env.sample").write_text("PUBLIC_SETTING=sample\n")
    (tmp_path / "release-notes.md").write_text("Owner release notes stay intact.\n")
    binary = tmp_path / "pipeline/.venv/bin/python"
    binary.parent.mkdir(parents=True)
    binary.symlink_to(sys.executable)
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    gh = fake_bin / "gh"
    gh.write_text("#!" + sys.executable + "\n" + textwrap.dedent('''\
        import json
        from pathlib import Path
        import sys
        Path("gh-args.json").write_text(json.dumps(sys.argv[1:]))
        '''))
    gh.chmod(0o700)
    tag = 'preview-$(touch injected)'
    environment = {"PATH": str(fake_bin) + os.pathsep + os.environ["PATH"],
                   "RELEASE_TAG": tag, "SOURCE_SHA": "a" * 40,
                   "REPOSITORY": "norandom/QOpenBB"}
    run_block("Record release source identity", tmp_path, environment)
    run_block("Attach images to published prerelease", tmp_path, environment)
    attached = json.loads((output / "manifest.json").read_text())
    assert attached == {**manifest, "release": {"tag": tag, "repository": "norandom/QOpenBB",
                                               "source_revision": "a" * 40}}
    assert json.loads((tmp_path / "gh-args.json").read_text()) == [
        "release", "upload", "--clobber", "--", tag,
        "artifacts/alpha-release/manifest.json", "artifacts/alpha-release/compose.yaml",
        "artifacts/alpha-release/.env.sample"]
    assert (tmp_path / "release-notes.md").read_text() == "Owner release notes stay intact.\n"
    assert (output / "compose.yaml").read_bytes() == (tmp_path / "compose.yaml").read_bytes()
    assert (output / ".env.sample").read_bytes() == (tmp_path / ".env.sample").read_bytes()
    assert not (tmp_path / "injected").exists()
