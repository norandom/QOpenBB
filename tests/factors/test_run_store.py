import json
import os
import re
import stat
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

import pytest
from qopenbb_data.modeling.contracts import ModelRun
from qopenbb_data.modeling.service import run_store
from qopenbb_data.modeling.service.ports import Principal
from qopenbb_data.modeling.service.run_store import (
    FileRunStore,
    RunNotFound,
    RunPublishedError,
    RunStoreError,
)
from test_model_run_evidence import verify_price

pytest_plugins = ("test_model_run_evidence",)


@pytest.fixture
def run(run_fields, owner):
    run_fields["owner_id"] = owner.subject
    verify_price(run_fields)
    return ModelRun.model_validate(run_fields)


@pytest.fixture
def owner():
    return Principal(subject="Test/Analyst")


def test_full_round_trip_with_relative_private_bind(tmp_path, monkeypatch, run, owner):
    monkeypatch.chdir(tmp_path)
    store = FileRunStore()
    run_id = store.save(run, owner)
    assert re.fullmatch(r"[0-9a-f]{32}", run_id)
    assert run_id != run.run_id
    directory = tmp_path / "data/modeling"
    path = directory / f"{run_id}.json"
    assert stat.S_IMODE(directory.stat().st_mode) == 0o700
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    record = json.loads(path.read_bytes())
    assert record["run"]["outputs"][0]["value"] == "10"
    assert record["run"]["created_at"].endswith("Z")
    assert record["run"]["inputs"]["tables"][0]["rows"][0]["observation_date"] == "2024-01-02"
    reopened = FileRunStore().get(run_id, owner)
    assert reopened == run.model_copy(update={"run_id": run_id})
    assert record["fingerprints"] == {
        "inputs": run.inputs.fingerprint(),
        "assumptions": run.assumptions.fingerprint(),
        "descriptor": run.descriptor.fingerprint(),
        "run": reopened.fingerprint(),
    }


def test_wrong_owner_missing_invalid_and_symlink_lookups_are_indistinguishable(tmp_path, run, owner):
    store = FileRunStore(tmp_path)
    run_id = store.save(run, owner)
    symlink_id = "f" * 32
    (tmp_path / f"{symlink_id}.json").symlink_to(f"{run_id}.json")
    for candidate, principal in [
        (run_id, Principal(subject=owner.subject.lower())),
        (run_id, Principal(subject=owner.subject + " ")),
        ("0" * 32, owner),
        (f"../{run_id}", owner),
        (str(tmp_path / run_id), owner),
        (run_id + "\n", owner),
        (symlink_id, owner),
        (run_id, None),
    ]:
        with pytest.raises(RunNotFound, match="^model run not found$"):
            store.get(candidate, principal)


def test_revalidates_run_before_writing(tmp_path, run, owner):
    bad_output = run.outputs[0].model_copy(update={"value": "NaN"})
    invalid = run.model_copy(update={"outputs": (bad_output, *run.outputs[1:])})
    with pytest.raises(RunStoreError, match="^invalid model run$"):
        FileRunStore(tmp_path).save(invalid, owner)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("subject", ["test/analyst", None])
def test_save_requires_the_exact_authenticated_owner(tmp_path, run, subject):
    principal = Principal(subject=subject) if subject is not None else None
    with pytest.raises(RunNotFound, match="^model run not found$"):
        FileRunStore(tmp_path).save(run, principal)
    assert not list(tmp_path.iterdir())


def test_detects_changed_saved_evidence_without_disclosing_contents(tmp_path, run, owner):
    store = FileRunStore(tmp_path)
    run_id = store.save(run, owner)
    path = tmp_path / f"{run_id}.json"
    record = json.loads(path.read_bytes())
    record["run"]["outputs"][-1]["value"] = "11"
    path.write_text(json.dumps(record))
    with pytest.raises(RunStoreError, match="^invalid saved model run$"):
        store.get(run_id, owner)


def test_concurrent_saves_retry_id_collision_without_overwriting(tmp_path, run, owner, monkeypatch):
    store = FileRunStore(tmp_path)
    existing_id = store.save(run, owner)
    existing_path = tmp_path / f"{existing_id}.json"
    original = existing_path.read_bytes()
    candidates = iter([existing_id, existing_id, "a" * 32, "b" * 32])
    monkeypatch.setattr(run_store, "_new_run_id", lambda: next(candidates))
    barrier = Barrier(2)

    def save(value):
        output = run.outputs[-1].model_copy(update={"value": value})
        changed = run.model_copy(update={"outputs": (*run.outputs[:-1], output)})
        barrier.wait(timeout=5)
        return store.save(changed, owner), value

    with ThreadPoolExecutor(max_workers=2) as pool:
        saved = dict(pool.map(save, ("11", "12")))
    assert set(saved) == {"a" * 32, "b" * 32}
    assert existing_path.read_bytes() == original
    for run_id, value in saved.items():
        assert str(store.get(run_id, owner).outputs[-1].value) == value
    assert len(list(tmp_path.iterdir())) == 3


def test_interrupted_file_sync_never_publishes_run(tmp_path, run, owner, monkeypatch):
    store = FileRunStore(tmp_path)
    run_id = "a" * 32
    monkeypatch.setattr(run_store, "_new_run_id", lambda: run_id)

    def interrupt(_fd):
        with pytest.raises(RunNotFound):
            store.get(run_id, owner)
        assert list(tmp_path.glob("*.json")) == []
        raise KeyboardInterrupt

    with monkeypatch.context() as patch:
        patch.setattr(os, "fsync", interrupt)
        with pytest.raises(KeyboardInterrupt):
            store.save(run, owner)
    assert list(tmp_path.iterdir()) == []
    assert store.save(run, owner) == run_id
    assert store.get(run_id, owner).owner_id == owner.subject


def test_rejects_a_bind_writable_by_other_local_users(tmp_path, run, owner):
    tmp_path.chmod(0o770)
    with pytest.raises(RunStoreError, match="^model run storage unavailable$"):
        FileRunStore(tmp_path).save(run, owner)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("failure", ["unlink", "directory_fsync", "file_fsync"])
def test_post_publication_failure_preserves_recoverable_id(tmp_path, run, owner, monkeypatch, failure):
    store = FileRunStore(tmp_path)
    published_id = "a" * 32
    retry_id = "b" * 32
    candidates = iter([published_id, published_id, retry_id])
    monkeypatch.setattr(run_store, "_new_run_id", lambda: next(candidates))
    original_fsync = os.fsync

    def fail_staging_unlink(_name, *, dir_fd):
        raise OSError("staging cleanup failed")

    def fail_directory_sync(fd):
        is_directory = stat.S_ISDIR(os.fstat(fd).st_mode)
        if is_directory == (failure == "directory_fsync"):
            raise OSError("sync failed")
        original_fsync(fd)

    with monkeypatch.context() as patch:
        if failure == "unlink":
            patch.setattr(os, "unlink", fail_staging_unlink)
        else:
            patch.setattr(os, "fsync", fail_directory_sync)
        with pytest.raises(RunStoreError) as error:
            store.save(run, owner)

    if failure == "file_fsync":
        assert type(error.value) is RunStoreError
        with pytest.raises(RunNotFound):
            store.get(published_id, owner)
        assert store.save(run, owner) == published_id
        return

    assert isinstance(error.value, RunPublishedError)
    assert error.value.run_id == published_id
    committed = store.get(error.value.run_id, owner)
    assert committed == run.model_copy(update={"run_id": published_id})
    existing_path = tmp_path / f"{published_id}.json"
    original = existing_path.read_bytes()
    assert store.save(run, owner) == retry_id
    assert existing_path.read_bytes() == original
    assert store.get(retry_id, owner) == run.model_copy(update={"run_id": retry_id})
