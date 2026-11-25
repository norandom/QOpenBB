"""Store and verify one evaluation in a killable child."""

import errno
import json
import os
import sys
from functools import partial
from pathlib import Path
from typing import BinaryIO

from ..contracts import ModelRun
from .execution_transport import MAX_RESULT_BYTES
from .ports import Principal
from .run_store import FileRunStore
from .run_store import _publish as _publish_named

_UNSUPPORTED_OPEN = {
    errno.EACCES,
    errno.EINVAL,
    errno.EISDIR,
    errno.ENOENT,
    errno.ENOSYS,
    errno.EOPNOTSUPP,
    errno.EPERM,
}
_UNSUPPORTED_LINK = {
    errno.EACCES,
    errno.EINVAL,
    errno.ELOOP,
    errno.ENOENT,
    errno.ENOSYS,
    errno.EOPNOTSUPP,
    errno.EPERM,
    errno.EXDEV,
}


class _AnonymousStagingUnavailable(Exception):
    """The worker can retry with a private named staging file."""


def _mark_commit(response: BinaryIO, state: bytes) -> None:
    response.write(state)
    response.flush()


def _publish(response: BinaryIO, directory: int, run_id: str, payload: bytes) -> bool:
    try:
        return _publish_anonymous(response, directory, run_id, payload)
    except _AnonymousStagingUnavailable:
        return _publish_named(
            directory,
            run_id,
            payload,
            before_link=partial(_mark_commit, response, b"1"),
            on_collision=partial(_mark_commit, response, b"0"),
        )


def _publish_anonymous(
    response: BinaryIO, directory: int, run_id: str, payload: bytes
) -> bool:
    # An anonymous inode is reclaimed after cancellation before the link.
    if not hasattr(os, "O_TMPFILE"):
        raise _AnonymousStagingUnavailable
    try:
        fd = os.open(".", os.O_TMPFILE | os.O_RDWR, 0o600, dir_fd=directory)
    except OSError as error:
        if error.errno in _UNSUPPORTED_OPEN:
            raise _AnonymousStagingUnavailable from None
        raise
    with os.fdopen(fd, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
        # A killed link can have taken effect. Report the ID from this point on.
        _mark_commit(response, b"1")
        try:
            os.link(
                f"/proc/self/fd/{fd}",
                f"{run_id}.json",
                src_dir_fd=directory,
                dst_dir_fd=directory,
                follow_symlinks=True,
            )
        except FileExistsError:
            _mark_commit(response, b"0")
            return False
        except OSError as error:
            # These failures definitively rejected the link. An I/O error
            # instead leaves the commit marker set for recovery.
            if error.errno in _UNSUPPORTED_LINK:
                _mark_commit(response, b"0")
                raise _AnonymousStagingUnavailable from None
            raise
        os.fsync(directory)
    return True


def main() -> None:
    request = sys.stdin.buffer
    root, subject, run_id, size = json.loads(request.readline(64 * 1024))
    if not 0 < size <= MAX_RESULT_BYTES:
        raise ValueError("invalid publication frame size")
    wire = request.read(size)
    if len(wire) != size:
        raise ValueError("incomplete publication frame")
    run = ModelRun.model_validate_json(wire)
    principal = Principal(subject=subject)
    store = FileRunStore(Path(root))
    store._save(run, principal, (run_id,), partial(_publish, sys.stdout.buffer))
    saved = store.get(run_id, principal)
    if saved != run.model_copy(update={"run_id": run_id}):
        raise ValueError("publication readback differs from evaluated run")


if __name__ == "__main__":
    main()
