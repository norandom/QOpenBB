"""Exercise the packaged internal ASGI entry point over an Ubuntu loopback socket."""

import json
import os
import socket
import subprocess
import sys
from contextlib import contextmanager
from time import monotonic, sleep
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from test_model_identity import ENV, assertion
from test_orchestration import OWNER, request
from test_orchestration import inputs as snapshot_fixture
from test_orchestration import service as evaluation_fixture

snapshot = snapshot_fixture
evaluations = evaluation_fixture


def exchange(url, token=None, headers=None, *, payload=None):
    headers = dict(headers or {})
    if token:
        headers["Authorization"] = "Bearer " + token
    if payload is not None:
        headers["Content-Type"] = "application/json"
    try:
        response = urlopen(Request(url, headers=headers, data=payload), timeout=3)
    except HTTPError as error:
        response = error
    with response:
        return response.status, json.load(response)


@contextmanager
def internal_listener(run_dir):
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        origin = f"http://127.0.0.1:{listener.getsockname()[1]}"
        command = [
            sys.executable, "-m", "uvicorn", "--factory",
            "qopenbb_data.modeling.service.bootstrap:create_app",
            "--fd", str(listener.fileno()), "--no-access-log",
        ]
        with subprocess.Popen(
            command, pass_fds=(listener.fileno(),),
            env={**os.environ, **ENV, "QOPENBB_MODEL_RUN_DIR": str(run_dir)},
        ) as server:
            try:
                deadline = monotonic() + 10
                while server.poll() is None:
                    try:
                        exchange(origin + "/modeling/v1/models")
                        break
                    except (URLError, TimeoutError):
                        if monotonic() >= deadline:
                            raise
                        sleep(0.05)
                assert server.poll() is None
                yield origin
            finally:
                server.terminate()
                server.wait(timeout=5)


def test_internal_listener_authenticates_and_reopens_saved_run(evaluations, snapshot, tmp_path):
    run = evaluations().evaluate(request(inputs=snapshot), OWNER)
    with internal_listener(tmp_path / "runs") as origin:
        prefix = origin + "/modeling/v1"
        signed = assertion(claims={"sub": OWNER.subject})
        assert exchange(prefix + "/models", headers={"X-User-Id": OWNER.subject})[0] == 401
        status, catalog = exchange(prefix + "/models", signed)
        assert status == 200
        assert ("issuer_fcf_yield", "1") in {
            (model["model_id"], model["method_version"]) for model in catalog["models"]
        }
        payload = request(inputs=snapshot).model_dump_json().encode()
        assert exchange(prefix + "/evaluations", payload=payload)[0] == 401
        status, failure = exchange(prefix + "/evaluations", signed, payload=payload)
        assert status == 422 and failure["code"] == "unsupported_method"
        status, saved = exchange(prefix + "/runs/" + run.run_id, signed)
        assert status == 200 and saved == run.model_dump(mode="json")
        assert exchange(prefix + "/runs/" + run.run_id, assertion(claims={"sub": "other"}))[0] == 404
        status, output = exchange(prefix + "/runs/" + run.run_id + "/outputs/value", signed)
        assert status == 200 and output["results"][0]["status"] == "verified"
        assert exchange(origin + "/docs")[0] == 404
