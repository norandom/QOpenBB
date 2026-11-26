"""Verify saved-run ownership across the Workspace and Modeling Python environments."""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "vendor/workspace/backend-api/backend"
DATA_API = ROOT / "services/data-api"
SCRIPT = Path(__file__).resolve()
BRIDGE_TIMEOUT = 90


def test_workspace_modeling_saved_run_ownership(tmp_path, monkeypatch):
    default_python = BACKEND / (
        ".venv/Scripts/python.exe" if os.name == "nt" else ".venv/bin/python"
    )
    workspace_python = Path(
        os.environ.get("QOPENBB_WORKSPACE_PYTHON", default_python)
    ).absolute()
    assert workspace_python.is_file(), (
        f"Workspace lock environment required. Set QOPENBB_WORKSPACE_PYTHON ({workspace_python})."
    )
    monkeypatch.syspath_prepend(str(ROOT / "tests/factors"))
    monkeypatch.syspath_prepend(str(DATA_API))
    payload = _evaluation_payload()
    sandbox = tmp_path / "workspace"
    sandbox.mkdir()
    env = {
        "PATH": os.defpath,
        "HOME": str(sandbox),
        "PYTHONPATH": str(BACKEND),
        "QOPENBB_SQLITE_SANDBOX": str(sandbox),
        "DATABASE_TYPE": "sqlite",
        "DB_PATH": str(sandbox / "settings.db"),
        "FOLDER_STORAGE_PATH": str(sandbox / "storage"),
        "STORAGE_PROVIDER": "folder",
        "MODE": "onprem",
        "SELFURL": "http://localhost.invalid/api",
        "PROURL": "http://localhost.invalid",
        "REDIS_PASS": "synthetic-test-password",
        "JOSESECRET": "synthetic-test-jwt-secret",
        "OPENBB_AES_KEY": "0123456789abcdef0123456789abcdef",
    }
    if os.name == "nt":
        env["SYSTEMROOT"] = os.environ["SYSTEMROOT"]
    result = subprocess.run(
        [workspace_python, SCRIPT, "workspace", sys.executable],
        input=payload,
        cwd=sandbox,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


async def _workspace_process(modeling_python, payload):
    # Install the fork's SQLite audit hooks before loading Workspace settings or routers.
    import httpx
    from pytest import MonkeyPatch
    from sqlalchemy.ext.asyncio import async_sessionmaker
    from tests_sqlite import conftest as sqlite
    from tests_sqlite import test_modeling_bridge_support as support
    from main import app

    engine = sqlite.file_engine(Path.cwd() / "bridge.db")
    try:
        metadata, tables = sqlite.dependency_tables()
        async with engine.begin() as connection:
            await connection.run_sync(
                lambda sync: metadata.create_all(sync, tables=tables)
            )
        await support.create_session_table(engine)
        sessions = async_sessionmaker(engine, expire_on_commit=False)

        with MonkeyPatch.context() as patch:
            support.bind_session_store(patch, sessions)
            patch.setenv("QFM_IDENTITY_CURRENT_KID", support.KEY_ID)
            patch.setenv("QFM_IDENTITY_CURRENT_SECRET", support.KEY)
            owner, other = await support.create_users(sessions)

            # A fresh upstream process for each request also proves persistence across restarts.
            async def relay(request):
                assert (
                    str(request.url.copy_with(path="/", query=None)).rstrip("/")
                    == support.UPSTREAM_ORIGIN
                )
                response = await asyncio.to_thread(
                    _upstream_request, modeling_python, request, await request.aread()
                )
                return httpx.Response(**response)

            patch.setitem(
                app.dependency_overrides,
                support.modeling.get_modeling_transport,
                lambda: httpx.MockTransport(relay),
            )
            transport = httpx.ASGITransport(app=app)
            owner_token = await support.issue_session(sessions, owner)
            other_token = await support.issue_session(sessions, other)
            async with httpx.AsyncClient(
                transport=transport, base_url="http://workspace.invalid"
            ) as client:
                await _save_and_reopen(
                    client, support, payload, (owner, owner_token), (other, other_token)
                )
            assert not sqlite.DENIED_READS
    finally:
        await engine.dispose()


async def _save_and_reopen(client, support, payload, owner_session, other_session):
    from decimal import Decimal

    owner, owner_token = owner_session
    other, other_token = other_session
    prefix = support.PREFIX
    owner_headers = {**support.bearer(owner_token), "X-User-Id": str(other)}
    other_headers = {**support.bearer(other_token), "X-User-Id": str(owner)}
    created = await client.post(
        prefix + "/evaluations", content=payload, headers=owner_headers
    )
    assert created.status_code == 200, created.text
    run = created.json()
    assert run["owner_id"] == str(owner)
    assert run["outputs"][0]["output_id"] == "fcf_yield"
    assert run["outputs"][0]["status"] == "verified"
    assert Decimal(run["outputs"][0]["value"]) == Decimal(5)

    other_created = await client.post(
        prefix + "/evaluations", content=payload, headers=other_headers
    )
    assert other_created.status_code == 200, other_created.text
    other_run = other_created.json()
    assert other_run["owner_id"] == str(other)
    assert other_run["run_id"] != run["run_id"]
    other_path = f"{prefix}/runs/{other_run['run_id']}"
    assert (await client.get(other_path, headers=owner_headers)).status_code == 404
    run_path = f"{prefix}/runs/{run['run_id']}"
    output_path = run_path + "/outputs/fcf_yield"
    reopened = await client.get(run_path, headers=owner_headers)
    assert reopened.status_code == 200 and reopened.json() == run
    output = await client.get(output_path, headers=owner_headers)
    assert output.status_code == 200, output.text
    assert output.json()["results"][0]["value"] == run["outputs"][0]["value"]

    widget_path = f"{prefix}/widget-results?run_id={run['run_id']}&output_id=fcf_yield"
    assert (await client.get(widget_path, headers=owner_headers)).status_code == 200
    for path in (run_path, output_path, widget_path):
        denied = await client.get(path, headers=other_headers)
        assert denied.status_code == 404, denied.text
        assert denied.json()["code"] == "not_found"
        assert str(owner) not in denied.text


def _evaluation_payload():
    from fixtures.factor_examples import EXAMPLES, build_run

    example = build_run(EXAMPLES["issuer_fcf_yield"], missing=False)
    return json.dumps(
        {
            "model_id": "issuer_fcf_yield",
            "method_version": "1",
            "inputs": example.inputs.model_dump(mode="json"),
            "assumptions": example.assumptions.model_dump(mode="json"),
        }
    )


def _upstream_request(modeling_python, request, body):
    env = {
        **os.environ,
        "PYTHONPATH": str(DATA_API),
        "QOPENBB_MODEL_RUN_DIR": str(Path.cwd() / "runs"),
    }
    result = subprocess.run(
        [modeling_python, SCRIPT, "modeling"],
        input=json.dumps(
            {
                "method": request.method,
                "path": request.url.path,
                "query": request.url.query.decode("ascii"),
                "headers": request.headers.multi_items(),
                "body": body.decode("utf-8"),
            }
        ),
        env=env,
        capture_output=True,
        text=True,
        timeout=BRIDGE_TIMEOUT,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


async def _modeling_process():
    from qopenbb_data.modeling.service.bootstrap import create_app

    wire = json.load(sys.stdin)
    body = wire["body"].encode()
    response_body = bytearray()
    response = {}

    async def receive():
        nonlocal body
        if body is None:
            await asyncio.Future()
        chunk, body = body, None
        return {"type": "http.request", "body": chunk, "more_body": False}

    async def send(message):
        if message["type"] == "http.response.start":
            response["status_code"] = message["status"]
            response["headers"] = [
                (k.decode("latin-1"), v.decode("latin-1"))
                for k, v in message["headers"]
            ]
        elif message["type"] == "http.response.body":
            response_body.extend(message.get("body", b""))

    path = wire["path"]
    await create_app()(
        {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": wire["method"],
            "scheme": "http",
            "path": path,
            "raw_path": path.encode(),
            "root_path": "",
            "query_string": wire["query"].encode(),
            "headers": [
                (k.encode("latin-1"), v.encode("latin-1")) for k, v in wire["headers"]
            ],
            "client": ("workspace", 1),
            "server": ("modeling", 6901),
        },
        receive,
        send,
    )
    response["content"] = response_body.decode()
    json.dump(response, sys.stdout)


if __name__ == "__main__":
    if sys.argv[1] == "workspace":
        asyncio.run(_workspace_process(sys.argv[2], sys.stdin.read()))
    elif sys.argv[1] == "modeling":
        asyncio.run(_modeling_process())
