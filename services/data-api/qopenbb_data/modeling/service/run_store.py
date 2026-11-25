"""Append-only model-run storage for the private relative data bind."""

import errno
import json
import os
import re
import stat
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from pathlib import Path
from threading import Event
from uuid import uuid4

from pydantic import ValidationError

from ..contracts import ModelRun
from .ports import Principal

_RUN_ID = re.compile(r"[0-9a-f]{32}")
_ID_ATTEMPTS = 8


class RunNotFound(LookupError):
    """The run is absent or inaccessible to this principal."""

    def __init__(self) -> None:
        super().__init__("model run not found")


class RunStoreError(RuntimeError):
    """A safe validation or storage failure without private run content."""


class RunPublishedError(RunStoreError):
    """Publication may have succeeded and retrying could duplicate the run."""

    def __init__(self, run_id: str) -> None:
        super().__init__("model run published with incomplete storage confirmation")
        self.run_id = run_id


def _new_run_id() -> str:
    return uuid4().hex


def _fingerprints(run: ModelRun) -> dict[str, str]:
    return {
        "inputs": run.inputs.fingerprint(),
        "assumptions": run.assumptions.fingerprint(),
        "descriptor": run.descriptor.fingerprint(),
        "run": run.fingerprint(),
    }


def _subject(principal: Principal) -> str:
    if isinstance(principal, Principal):
        try:
            return Principal.model_validate(principal).subject
        except ValidationError:
            pass
    raise RunNotFound()


def _publish(
    directory: int,
    run_id: str,
    payload: bytes,
    *,
    before_link: Callable[[], None] | None = None,
    on_collision: Callable[[], None] | None = None,
) -> bool:
    staging = f".pending-{uuid4().hex}"
    fd = os.open(staging, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600, dir_fd=directory)
    published = False
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        # A same-directory hard link publishes atomically and refuses to replace an audit run.
        if before_link is not None:
            before_link()
        try:
            os.link(staging, f"{run_id}.json", src_dir_fd=directory, dst_dir_fd=directory)
        except FileExistsError:
            if on_collision is not None:
                on_collision()
            return False
        published = True
    finally:
        try:
            try:
                os.unlink(staging, dir_fd=directory)
            finally:
                # Sync the published entry even if staging cleanup fails.
                if published:
                    os.fsync(directory)
        except OSError:
            if published:
                raise RunPublishedError(run_id) from None
            raise
    return True


def _read(directory: int, filename: str) -> bytes:
    try:
        fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
    except OSError as exc:
        if exc.errno in (errno.ENOENT, errno.ELOOP):
            raise RunNotFound() from None
        raise
    with os.fdopen(fd, "rb") as handle:
        if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
            raise RunNotFound()
        return handle.read()


def _decode(payload: bytes, run_id: str, subject: str) -> ModelRun:
    try:
        record = json.loads(payload)
        if not isinstance(record, dict) or not isinstance(fields := record.get("run"), dict):
            raise TypeError
        if fields.get("owner_id") != subject:
            raise RunNotFound()
        if set(record) != {"run", "fingerprints"} or fields.get("run_id") != run_id:
            raise ValueError
        run = ModelRun.model_validate(fields)
        if record["fingerprints"] != _fingerprints(run):
            raise ValueError
    except (TypeError, ValueError, RecursionError):
        raise RunStoreError("invalid saved model run") from None
    return run


class FileRunStore:
    """Store private JSON files in a service-owned local directory."""

    def __init__(self, root: str | Path = Path("data/modeling")) -> None:
        self._root = Path(root)

    @contextmanager
    def _directory(self) -> Iterator[int]:
        fd = os.open(self._root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            if os.fstat(fd).st_mode & (stat.S_IWGRP | stat.S_IWOTH):
                raise PermissionError("modeling bind must be writable only by its owner")
            yield fd
        finally:
            os.close(fd)

    def save(self, run: ModelRun, principal: Principal) -> str:
        return self._save(run, principal, (_new_run_id() for _ in range(_ID_ATTEMPTS)), _publish)

    def _publish_evaluated(
        self, wire: bytearray, principal: Principal, *, deadline: float, cancel: Event | None
    ) -> str:
        """Save and read back the run within the remaining evaluation budget."""
        from .run_store_transport import publish

        return publish(self._root, wire, principal, deadline, cancel)

    def _save(
        self,
        run: ModelRun,
        principal: Principal,
        run_ids: Iterable[str],
        publish: Callable[[int, str, bytes], bool],
    ) -> str:
        subject = _subject(principal)
        if not isinstance(run, ModelRun):
            raise RunStoreError("invalid model run")
        published = False
        try:
            for run_id in run_ids:
                owned_run = ModelRun.model_validate(run.model_copy(update={"run_id": run_id}))
                if owned_run.owner_id != subject:
                    raise RunNotFound()
                payload = json.dumps(
                    {"run": owned_run.model_dump(mode="json"), "fingerprints": _fingerprints(owned_run)},
                    ensure_ascii=True,
                    allow_nan=False,
                ).encode("utf-8")
                self._root.mkdir(mode=0o700, parents=True, exist_ok=True)
                with self._directory() as directory:
                    published = publish(directory, run_id, payload)
                if published:
                    return run_id
        except ValueError:
            raise RunStoreError("invalid model run") from None
        except OSError:
            if published:
                raise RunPublishedError(run_id) from None
            raise RunStoreError("model run storage unavailable") from None
        raise RunStoreError("could not allocate a model run ID")

    def get(self, run_id: str, principal: Principal) -> ModelRun:
        subject = _subject(principal)
        if not isinstance(run_id, str) or not _RUN_ID.fullmatch(run_id):
            raise RunNotFound()
        try:
            with self._directory() as directory:
                payload = _read(directory, f"{run_id}.json")
        except FileNotFoundError:
            raise RunNotFound() from None
        except OSError:
            raise RunStoreError("model run storage unavailable") from None
        return _decode(payload, run_id, subject)
