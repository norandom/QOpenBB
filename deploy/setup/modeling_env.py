"""Fill unset modeling defaults in the installer's private dotenv bind mount."""

import fcntl
import io
import os
import re
import secrets
import stat
import sys
import tomllib
from pathlib import Path

from dotenv import dotenv_values


def prepare_model_directory(path: Path) -> None:
    info = path.stat()
    if (info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode)) == (10001, 10001, 0o700):
        return
    if any(path.iterdir()):
        raise SystemExit("Existing data/modeling must be owned by 10001:10001 with mode 0700")
    os.chown(path, 10001, 10001)
    path.chmod(0o700)
    info = path.stat()
    if (info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode)) != (10001, 10001, 0o700):
        raise SystemExit("The modeling directory requires a filesystem that supports Linux ownership and permissions")


def configure(env_path: Path, project_path: Path, existing_bind: bool) -> None:
    with env_path.open("r+b") as env_file:
        fcntl.flock(env_file, fcntl.LOCK_EX)
        content = env_file.read()
        values = dotenv_values(stream=io.StringIO(content.decode("utf-8-sig")), interpolate=False)
        version = tomllib.loads(project_path.read_text())["project"]["version"]
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ValueError("Expected a published modeling release version in pyproject.toml")
        # The Workspace service receives the values after Compose interpolation.
        defaults = {
            "QFM_IDENTITY_CURRENT_KID": "setup-" + secrets.token_hex(8),
            "QFM_IDENTITY_CURRENT_SECRET": secrets.token_urlsafe(48),
        }
        missing = {k: v for k, v in defaults.items() if not os.getenv(k)}
        storage = values.get("QOPENBB_MODELING_STORAGE")
        if existing_bind and storage in (None, "", "./data/modeling"):
            prepare_model_directory(Path("/run/setup-model-state"))
            if not storage:
                missing["QOPENBB_MODELING_STORAGE"] = "./data/modeling"
        elif not existing_bind and not storage:
            missing["QOPENBB_MODELING_STORAGE"] = "model-runs"
        model_image = f"ghcr.io/norandom/qopenbb-modeling:modeling-v{version}"
        if values.get("QOPENBB_SETUP_MODELING_IMAGE") != model_image:
            missing["QOPENBB_SETUP_MODELING_IMAGE"] = model_image
        if missing:
            lines = "".join(f"{key}={value}\n" for key, value in missing.items())
            env_file.write(("\n" + lines).encode())
            env_file.flush()
            os.fsync(env_file.fileno())


if __name__ == "__main__":
    configure(Path("/run/setup.env"), Path("/run/model.toml"), "--existing-model-bind" in sys.argv[1:])
