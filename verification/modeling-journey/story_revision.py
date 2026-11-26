"""Acquire a changed closing price through the packaged model's ordinary data API route."""

import json
import os
import subprocess
from decimal import Decimal
from pathlib import Path

from story_preflight import API, Candidate
from story_preflight_evidence import require, timestamp


def docker(*args, **kwargs):
    return subprocess.run(["docker", *args], timeout=90, text=True, check=True, **kwargs)


def exercise_peer(origin, password, checkpoint, fixture):
    peer = Candidate(origin)
    peer.token = peer.exchange("/api/pro/login", {"email": "story-peer@example.com", "password": password})["access_token"]
    peer.exchange(f"{API}/runs/{checkpoint['state']['run_refs']['comparison']}", error_expected=404)
    run = peer.saved_run(fixture["request"])
    require(run["inputs"]["provenance"]["origin"] == "service_acquired", "Expected service-acquired fixture")
    receipts = dict(run["inputs"]["provenance"]["query"])
    tables = {item["table_id"]: item["rows"] for item in run["inputs"]["tables"]}
    for side, symbol in (("left", "DBC"), ("right", "XLK")):
        receipt = side + "_retrieved_at"
        require(timestamp(receipts[receipt]) > timestamp(checkpoint["real"]["financial"]["retrievedAt"][receipt]),
                "Controlled leg receipt must follow the original close receipt")
        actual = [[row["observation_date"], Decimal(row["value"])] for row in tables[f"{side}_closes"]]
        require(actual == [[day, Decimal(close)] for day, close in fixture["histories"][symbol]],
                "Controlled run differs from the revised fixture history")
    spread = next(o for o in run["outputs"] if o["output_id"] == "momentum_spread")
    reference = next(v for v in run["verification"] if v["output_id"] == "momentum_spread")
    require(spread["status"] == "verified" and reference["status"] == "match", "Unverified controlled spread")
    require(Decimal(spread["value"]) != Decimal(checkpoint["real"]["financial"]["spreadPercentagePoints"]),
            "Controlled revision must change the realized spread")
    return {"foreign": run["run_id"], "revision": {"source": "controlled data API history fixture",
            "observationDate": fixture["histories"]["DBC"][-1][0], "table": "left_closes",
            "revisedClose": fixture["histories"]["DBC"][-1][1], "spread": spread["value"],
            "retrievedAt": {side: receipts[side + "_retrieved_at"] for side in ("left", "right")}},
            "ordinaryAccountLogins": ["peer"], "foreignReadStatus": 404, "ownReadStatus": 200}


def controlled_revision(root, compose, env, origin, peer_password):
    checkpoint_path = root / "checkpoint.json"
    saved = json.loads(checkpoint_path.read_text())
    fixture = json.loads((root / "history-fixture.json").read_text())
    last = fixture["histories"]["DBC"][-1]
    require(last[0] == saved["state"]["selection"]["observation_date"], "Expected ending DBC close")
    original = last[1]
    last[1] = str(Decimal(original) + Decimal("1.00"))
    path = root / "controlled-history.json"
    path.write_text(json.dumps(fixture["histories"]))
    path.chmod(0o600)
    project = compose[compose.index("-p") + 1]
    code = Path(__file__).with_name("story_history_fixture.py").read_text()
    subprocess.run([*compose, "stop", "data-api"], env=env, check=True, timeout=90)
    try:
        container = docker("run", "-d", "--rm", "--pull", "never", "--network", project + "_default",
                           "--network-alias", "data-api", "--user", f"{os.getuid()}:{os.getgid()}",
                           "--mount", f"type=bind,src={path},dst=/controlled-history.json,readonly",
                           "--entrypoint", "python", env["DATA_API_IMAGE"], "-c", code, capture_output=True).stdout.strip()
        try:
            docker("exec", container, "python", "-c", """
import socket, time
for attempt in range(50):
    try:
        socket.create_connection(("127.0.0.1", 6900), timeout=1).close()
        break
    except OSError:
        time.sleep(0.1)
else:
    raise RuntimeError("Controlled history fixture failed to listen")
""")
            saved["controlled"] = exercise_peer(origin, peer_password, saved, fixture)
            saved["controlled"]["revision"]["originalClose"] = original
            checkpoint_path.write_text(json.dumps(saved))
        finally:
            docker("rm", "-f", container, capture_output=True)
    finally:
        subprocess.run([*compose, "start", "--wait", "--wait-timeout", "60", "data-api"],
                       env=env, check=True, timeout=90)
