"""Disposable Full Workspace service for real-route browser verification.

Reuses the packaging smoke's Docker/HTTP primitives. A source overlay is explicit
development evidence, never evidence that the loaded release image is current.
Run this helper in WSL/Linux against the local Docker daemon.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import socket
import stat
import tempfile
import time
from urllib.error import URLError
from uuid import uuid4

from task25_runtime import docker, request


PREFIX = "qopenbb-browser-"


def source_identity(source):
    files = sorted(path for path in source.rglob("*") if path.is_file()
                   and "__pycache__" not in path.parts and path.suffix != ".pyc")
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(source).as_posix().encode() + b"\0")
        digest.update(path.read_bytes())
    return {"path": str(source), "sha256": digest.hexdigest(), "files": len(files)}


class WorkspaceRuntime:
    """Own one container and disposable state; keep it alive for save/restart tests."""

    def __init__(self, descriptor):
        self.descriptor = descriptor

    @classmethod
    def start(cls, image, source, public_origin):
        if not re.fullmatch(r"http://127\.0\.0\.1:[0-9]+", public_origin or ""):
            raise ValueError("Explicit loopback frontend public origin required")
        if not 0 < int(public_origin.rsplit(":", 1)[1]) < 65536:
            raise ValueError("Invalid frontend port")
        source = Path(source).resolve(strict=True)
        if not (source / "database.py").is_file() or not (source / "__init__.py").is_file():
            raise ValueError("Expected the complete backend api source directory")
        image_id = json.loads(docker("image", "inspect", image))[0]["Id"]
        # An explicit ephemeral port survives Docker restart; an empty binding does not.
        with socket.socket() as reservation:
            reservation.bind(("127.0.0.1", 0))
            backend_port = reservation.getsockname()[1]
        state = Path(tempfile.mkdtemp(prefix=PREFIX)).resolve()
        runtime = cls({"name": PREFIX + uuid4().hex, "state": str(state),
                       "image": image_id, "source_overlay": source_identity(source),
                       "public_origin": public_origin,
                       "release_image_verified": False})
        try:
            runtime.descriptor["container"] = docker(
                "run", "-d", "--name", runtime.descriptor["name"],
                "--mount", f"type=bind,src={state},dst=/data",
                "--mount", f"type=bind,src={source},dst=/opt/code/api,readonly",
                "-p", f"127.0.0.1:{backend_port}:3000", "-e", f"PUBLIC_URL={public_origin}",
                "-e", f"OPENBB_ADMIN_EMAIL=browser-{uuid4().hex}@example.com",
                image_id).strip()
            inspected = json.loads(docker("inspect", runtime.descriptor["name"]))[0]
            binding = inspected["NetworkSettings"]["Ports"]["3000/tcp"][0]
            if binding["HostIp"] != "127.0.0.1" or inspected["Image"] != image_id:
                raise AssertionError("Runtime isolation or image identity mismatch")
            runtime.descriptor["origin"] = "http://127.0.0.1:" + binding["HostPort"]
            runtime.wait_ready()
            _, configuration = request(runtime.origin, "/config.js")
            payload = configuration.decode().strip().removeprefix("window.__APP_CONFIG__ = ").removesuffix(";")
            config = json.loads(re.sub(r'(?m)^(\s*)([A-Za-z][A-Za-z0-9]*):', r'\1"\2":', payload))
            if config["ui"]["isLite"] is not False or config["urls"]["backend"] != "/api":
                raise AssertionError("Disposable service must expose Full same-origin configuration")
            runtime.descriptor["full_config_ready"] = True
            credentials = dict(line.split("=", 1) for line in docker(
                "exec", runtime.descriptor["name"], "cat", "/data/secrets.env").splitlines())
            runtime.descriptor["credentials"] = {
                "email": credentials["OPENBB_ADMIN_EMAIL"],
                "password": credentials["OPENBB_ADMIN_PASSWORD"]}
            status, body = request(runtime.origin, "/api/pro/login", {
                **runtime.descriptor["credentials"], "remember": False})
            if status != 200 or not json.loads(body).get("access_token"):
                raise AssertionError("Disposable account login failed")
            runtime.descriptor["api_login_ready"] = True
            return runtime
        except Exception:
            runtime.close()
            raise

    @property
    def origin(self):
        return self.descriptor["origin"]

    def wait_ready(self):
        for _ in range(90):
            observed = json.loads(docker("inspect", self.descriptor["name"]))[0]["State"]
            if not observed["Running"]:
                raise RuntimeError("Owned backend exited during startup")
            try:
                status, _ = request(self.origin, "/api/health")
                if status == 200 and observed.get("Health", {}).get("Status") == "healthy":
                    return
            except (URLError, TimeoutError, ConnectionError):
                pass
            time.sleep(2)
        raise TimeoutError("Owned backend health timeout")

    def restart(self):
        self.validate_ownership()
        docker("restart", self.descriptor["name"])
        inspected = json.loads(docker("inspect", self.descriptor["name"]))[0]
        binding = inspected["NetworkSettings"]["Ports"]["3000/tcp"][0]
        if self.origin != "http://127.0.0.1:" + binding["HostPort"]:
            raise RuntimeError("Disposable backend port changed; recreate with an explicit binding")
        self.wait_ready()

    def validate_ownership(self):
        state = Path(self.descriptor["state"])
        if (state.is_symlink() or state.resolve() != state
                or state.parent != Path(tempfile.gettempdir()).resolve()
                or not state.name.startswith(PREFIX)
                or not self.descriptor["name"].startswith(PREFIX)):
            raise ValueError("Refusing cleanup outside disposable runtime ownership")
        if self.descriptor.get("container"):
            inspected = json.loads(docker("inspect", self.descriptor["name"]))[0]
            if inspected["Id"] != self.descriptor["container"]:
                raise ValueError("Owned container identity changed")
            mounts = {mount["Destination"]: mount["Source"] for mount in inspected["Mounts"]}
            if mounts.get("/data") != str(state):
                raise ValueError("Owned state mount changed")

    def close(self):
        self.validate_ownership()
        if self.descriptor.get("container"):
            running = json.loads(docker("inspect", self.descriptor["name"]))[0]["State"]["Running"]
            if running:
                docker("exec", "--user", "0", self.descriptor["name"],
                       "chown", "-R", "-h", str(os.getuid()), "/data")
            else:
                docker("run", "--rm", "--network", "none", "--user", "0",
                       "--entrypoint", "chown", "--mount",
                       f"type=bind,src={self.descriptor['state']},dst=/data",
                       self.descriptor["image"], "-R", "-h", str(os.getuid()), "/data")
            docker("rm", "-f", self.descriptor["name"])
        shutil.rmtree(self.descriptor["state"])

    def write_private(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        os.fchmod(fd, 0o600)
        if stat.S_IMODE(os.fstat(fd).st_mode) != 0o600:
            os.close(fd)
            path.unlink()
            raise ValueError("Private descriptor requires a filesystem enforcing mode 0600")
        with os.fdopen(fd, "w") as output:
            json.dump(self.descriptor, output, indent=2)
            output.write("\n")

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "restart", "stop", "status"])
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--image")
    parser.add_argument("--source", type=Path)
    parser.add_argument("--public-origin")
    args = parser.parse_args()
    if args.action == "start":
        if args.private.exists():
            parser.error("Private descriptor already exists; stop its runtime first")
        if not args.image or not args.source or not args.public_origin:
            parser.error("start requires --image, --source and --public-origin")
        runtime = WorkspaceRuntime.start(args.image, args.source, args.public_origin)
        try:
            runtime.write_private(args.private)
        except Exception:
            runtime.close()
            raise
    else:
        runtime = WorkspaceRuntime(json.loads(args.private.read_text()))
        runtime.validate_ownership()
        if args.action == "stop":
            runtime.close()
            args.private.unlink()
            print("Owned runtime removed")
            return
        if args.action == "restart":
            runtime.restart()
        runtime.wait_ready()
    print(json.dumps({key: value for key, value in runtime.descriptor.items()
                      if key not in ("credentials", "state", "container")}))


if __name__ == "__main__":
    main()
