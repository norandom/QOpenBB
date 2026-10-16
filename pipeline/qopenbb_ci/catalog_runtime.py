"""Read-only generation against an explicitly identified local image and fork."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time
import uuid

from qopenbb_ci.catalog import canonical

UTILS = "openbb_platform/extensions/platform_api/openbb_platform_api/utils"
ASSET = "openbb_platform/providers/fred/openbb_fred/assets/apps.json"


def docker(*args: str, **kwargs) -> str:
    return subprocess.run(["docker", *args], check=True, text=True, capture_output=True,
                          timeout=120, **kwargs).stdout


def cleanup(container: str) -> None:
    subprocess.run(["docker", "rm", "-f", container], text=True, capture_output=True, timeout=30)


def verified_sources(source: Path, revision: str) -> dict:
    paths = [f"{UTILS}/widgets.py", f"{UTILS}/openapi.py", ASSET]
    hashes = {}
    for relative in paths:
        try:
            expected = subprocess.run(["git", "-C", str(source), "show", f"{revision}:{relative}"],
                                      check=True, capture_output=True, timeout=30).stdout
            actual = (source / relative).read_bytes()
        except (OSError, subprocess.SubprocessError) as exc:
            raise ValueError("unavailable accepted generator source") from exc
        if actual != expected:
            raise ValueError("generator source differs from accepted revision: " + relative)
        hashes[relative] = hashlib.sha256(actual).hexdigest()
    return {"revision": revision, "files_sha256": hashes,
            "generator": f"{UTILS}/widgets.py:build_json", "asset": ASSET}


def image_identity(image: str) -> dict:
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", image):
        raise ValueError("use exact local image ID, never a mutable tag")
    identity = json.loads(docker("image", "inspect", image))[0]
    if identity["Id"] != image:
        raise ValueError("image ID mismatch")
    return identity


def capture_schema(image: str) -> tuple[dict, dict]:
    identity = image_identity(image)
    container = "qopenbb-schema-" + uuid.uuid4().hex
    code = ("import urllib.request; "
            "print(urllib.request.urlopen('http://127.0.0.1:6900/openapi.json',timeout=3).read().decode())")
    try:
        docker("run", "-d", "--name", container, "--network", "none", image)
        for _ in range(60):
            try:
                return json.loads(docker("exec", container, "python", "-c", code)), identity
            except (subprocess.CalledProcessError, json.JSONDecodeError):
                time.sleep(1)
        raise ValueError("owned data image failed to serve schema within 60 seconds")
    finally:
        cleanup(container)


def upstream_widgets(image: str, source: Path, schema: dict, inventory: dict, work: Path) -> dict:
    subset = deepcopy(schema)
    subset["paths"] = {item["path"]: deepcopy(schema["paths"][item["path"]])
                       for item in inventory["datasets"]}
    with tempfile.TemporaryDirectory(prefix="catalog-", dir=work) as directory:
        inputs = Path(directory)
        inputs.chmod(0o755)
        (inputs / "schema.json").write_bytes(canonical(subset))
        script = Path(__file__).with_name("catalog_upstream.py")
        mounts = [(source / UTILS, "/generator"), (script, "/bridge.py"), (inputs, "/input")]
        container = "qopenbb-generator-" + uuid.uuid4().hex
        args = ["run", "--rm", "--name", container, "--network", "none", "--entrypoint", "python"]
        for local, target in mounts:
            args.extend(["--mount", f"type=bind,source={local.resolve()},target={target},readonly"])
        try:
            output = docker(*args, image, "/bridge.py")
        finally:
            cleanup(container)
    lines = [line.removeprefix("QOPENBB_CATALOG=") for line in output.splitlines()
             if line.startswith("QOPENBB_CATALOG=")]
    if len(lines) != 1:
        raise ValueError("upstream generator produced no unique catalog")
    return json.loads(lines[0])
