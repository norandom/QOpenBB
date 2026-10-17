"""Read-only offline review; --record writes only this review's receipt."""
import ast
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import socket
import sys
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = "artifacts/ui-parity-legend-ui-relay-collector/"
PINS = {
    SOURCE + "harness/relay.py": "b4274ed8bad51791ed7d6126cdd3cd6f6ccceeafc57a7313b4c7df2c387b028c",
    SOURCE + "test-relay.py": "b0ab59b0ffacce9aa104abc38113ed01bd068f9029391ce4864ffd59ef32feda",
    "artifacts/ui-parity-legend-relay-mount-source/harness/relay.py": "ab893aa22478d28c0ae0fd596543086a3d0b757da469cd5c08fcfb2a63a408cf",
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def deny_socket(*args, **kwargs):
    raise AssertionError("real socket forbidden in offline review")


def definitions(path):
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            values[node.name] = ast.dump(node)
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    values[node.name + "." + item.name] = ast.dump(item)
    return values


def run_suite(suite):
    result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    return {"run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors)}


def focused(fixtures):
    relay = fixtures.relay
    results = []
    # A signal during persistence only sets a flag; it never reenters serialization.
    selector = fixtures.FakeSelector()
    instance = relay.Relay(("172.30.0.10", 3000), selector=selector,
                           factory=lambda *_: fixtures.FakeSocket(), clock=lambda: 0)
    saved = []
    def persist(stats):
        saved.append(json.loads(json.dumps(stats)))
        if stats["checkpointSequence"] < 4:
            for _ in range(100):
                instance.request_checkpoint()
    def event():
        if instance.stats["checkpointSequence"] == 4:
            instance.stopping = True
        return []
    selector.on_select = event
    instance.run(persist=persist)
    assert [s["snapshotSequence"] for s in saved] == [1, 2, 3, 4, 5, 6]
    assert [s["checkpointSequence"] for s in saved] == [0, 1, 2, 3, 4, 4]
    assert saved[-1]["phase"] == "closed" and not any(saved[-1]["violations"].values())
    results.append("400 requests during snapshot writes coalesce to four acknowledgements and one fresh closure")

    for failed_write in (1, 2, 3):
        selector, listener, calls = fixtures.FakeSelector(), fixtures.FakeSocket(), []
        instance = relay.Relay(("172.30.0.10", 3000), selector=selector,
                               factory=lambda *_: listener, clock=lambda: 0)
        def event():
            if instance.stats["checkpointSequence"] == 0:
                instance.request_checkpoint()
            else:
                instance.stopping = True
            return []
        def persist(stats):
            calls.append(json.loads(json.dumps(stats)))
            if len(calls) == failed_write:
                raise OSError("injected-persist-failure")
        selector.on_select = event
        escaped = False
        try:
            instance.run(persist=persist)
        except OSError:
            escaped = True
        assert len(calls) == (2 if failed_write == 1 else 3)
        assert escaped == (failed_write == 3)
        assert listener.closed and selector.closed and calls[-1]["phase"] == "closed"
        if not escaped:
            assert calls[-1]["violations"]["socket-error"] == 1
    results.append("startup/checkpoint/final persistence failures terminate with bounded writes and closed endpoints")

    class ShortWriter:
        def __init__(self):
            self.writes, self.truncates = [], []
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def seek(self, offset):
            assert offset == 0
        def write(self, data):
            self.writes.append(data)
            return 2048
        def truncate(self, size):
            self.truncates.append(size)
    stream = ShortWriter()
    with patch.object(relay, "open", create=True, return_value=stream) as opened:
        try:
            relay.save_stats(dict(relay.new_stats(), snapshotSequence=1))
            raise AssertionError("short write accepted")
        except OSError as exc:
            assert str(exc) == "stats-short-write"
        opened.assert_called_once_with("/evidence/relay-stats.json", "r+b", buffering=0)
    assert len(stream.writes) == 1 and len(stream.writes[0]) == 4096 and stream.truncates == []
    frame = json.loads(stream.writes[0])
    assert frame["sha256"] == hashlib.sha256(frame["payloadJson"].encode()).hexdigest()
    results.append("short write fails after one fixed 4096-byte attempt without truncate or extra file")
    return results


def audit():
    for path, sha in PINS.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path
    baseline_path = list(PINS)[2]
    current, baseline = definitions(SOURCE + "harness/relay.py"), definitions(baseline_path)
    preserved = ["config_target"] + ["Relay." + name for name in
        ("breach", "close_pair", "set_events", "refresh", "accept_pair", "read", "transfer", "tick")]
    for name in preserved:
        assert current[name] == baseline[name], name
    with patch.object(socket, "socket", deny_socket):
        fixtures = load("review_fixtures", SOURCE + "test-relay.py")
        green = run_suite(unittest.defaultTestLoader.loadTestsFromTestCase(fixtures.RelayTests))
        assert green == {"run": 16, "failures": 0, "errors": 0}, green
        checks = focused(fixtures)
        fixtures.relay = load("review_baseline", baseline_path)
        negative = run_suite(unittest.TestSuite(fixtures.RelayTests(name) for name in
            ("test_exact_ui_profile", "test_fixed_frame_payload_hash_and_sequences")))
        assert negative == {"run": 2, "failures": 2, "errors": 0}, negative
    return {"verdict": "APPROVED_PYTHON_ONLY", "pins": PINS, "canonicalTests": green,
            "baselineRed": negative, "unchangedDefinitions": preserved, "focusedChecks": checks,
            "runtimeExecuted": False, "mutableJavaScriptInspected": False}


if __name__ == "__main__":
    result = audit()
    target = HERE / "verification.json"
    if sys.argv[1:] == ["--record"]:
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    else:
        assert sys.argv[1:] == []
        assert json.loads(target.read_text(encoding="utf-8")) == result
    print(json.dumps(result, indent=2))
