"""Scoped F1 review: frozen Python sources and injected sockets only."""
import ast
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import selectors
import socket
import sys
import unittest

sys.dont_write_bytecode = True
BASE = Path(__file__).parent
ARTIFACTS = BASE.parent
FILES = {
    "ui-parity-legend-fixed-relay-revised/harness/relay.py": "ab893aa22478d28c0ae0fd596543086a3d0b757da469cd5c08fcfb2a63a408cf",
    "ui-parity-legend-fixed-relay-revised/test-relay.py": "e05cbfce89628773dc853fd0f5634079cad5fecf2db66a5d9a18fbee6c2c7144",
    "ui-parity-legend-fixed-relay/harness/relay.py": "273a5c95ab976024ee6bd0c004a7cf8c9a3684cfddc437d2333f1e3823f44f0b",
}


def verify_inputs():
    for relative, expected in FILES.items():
        assert hashlib.sha256((ARTIFACTS / relative).read_bytes()).hexdigest() == expected


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ARTIFACTS / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def deny_socket(*_args, **_kwargs):
    raise AssertionError("A real socket is outside this review")


def run_suite(suite):
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    return {"tests": result.testsRun, "failures": len(result.failures),
            "errors": len(result.errors), "successful": result.wasSuccessful()}, stream.getvalue()


verify_inputs()
socket.socket = deny_socket
fixtures = load("f1_fixtures", "ui-parity-legend-fixed-relay-revised/test-relay.py")
revised = fixtures.relay
baseline = load("f1_baseline", "ui-parity-legend-fixed-relay/harness/relay.py")
all_tests, _ = run_suite(unittest.defaultTestLoader.loadTestsFromTestCase(fixtures.RelayTests))
assert all_tests == {"tests": 10, "failures": 0, "errors": 0, "successful": True}
focused = "test_combined_read_write_backpressure_keeps_unread_byte"
fixtures.relay = baseline
red, red_output = run_suite(unittest.TestSuite([fixtures.RelayTests(focused)]))
assert red == {"tests": 1, "failures": 2, "errors": 0, "successful": False}
assert "AssertionError: 1 is not false" in red_output
fixtures.relay = revised
green, _ = run_suite(unittest.TestSuite([fixtures.RelayTests(focused)]))
assert green == {"tests": 1, "failures": 0, "errors": 0, "successful": True}

cases = []
for side in (0, 1):
    for error_type in (BlockingIOError, InterruptedError):
        endpoints = [fixtures.FakeSocket(), fixtures.FakeSocket()]
        endpoints[side].reads = [b"A" * 65536, b"Z", b""]
        endpoints[side].sends = [error_type()]
        endpoints[1-side].reads = [b"response", b""]
        instance, pair, client, upstream = fixtures.RelayTests().make(*endpoints)
        instance.transfer(pair, 1-side, selectors.EVENT_READ)
        instance.transfer(pair, side, selectors.EVENT_READ | selectors.EVENT_WRITE)
        assert not instance.selector.entries[endpoints[side]][0] & selectors.EVENT_READ
        before = list(endpoints[side].recv_counts)
        instance.transfer(pair, side, selectors.EVENT_READ)
        assert endpoints[side].recv_counts == before and not any(pair["eof"])
        instance.transfer(pair, 1-side, selectors.EVENT_WRITE)
        instance.transfer(pair, side, selectors.EVENT_READ)
        instance.transfer(pair, 1-side, selectors.EVENT_WRITE)
        instance.transfer(pair, side, selectors.EVENT_WRITE)
        assert endpoints[1-side].sent == b"A" * 65536 + b"Z"
        assert endpoints[side].sent == b"response"
        assert not client.shut and not upstream.shut
        instance.transfer(pair, side, selectors.EVENT_READ)
        instance.transfer(pair, 1-side, selectors.EVENT_READ)
        assert not instance.pairs and not endpoints[side].reads
        assert client.shut == [socket.SHUT_WR] and upstream.shut == [socket.SHUT_WR]
        assert 0 not in client.recv_counts + upstream.recv_counts
        assert instance.stats["receivedBytes"] == instance.stats["forwardedBytes"] == 65545
        assert not any(instance.stats["violations"].values())
        cases.append({"side": side, "injected": error_type.__name__, "forwardedBytes": 65545,
                      "zeroCapacityReceive": False, "prematureHalfClose": False})

def without_fix(source):
    tree = ast.parse(source)
    relay_class = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Relay")
    relay_class.body = [node for node in relay_class.body if not isinstance(node, ast.FunctionDef) or node.name not in ("read", "transfer")]
    return ast.dump(tree, include_attributes=False)

assert without_fix((ARTIFACTS / "ui-parity-legend-fixed-relay/harness/relay.py").read_text()) == without_fix((ARTIFACTS / "ui-parity-legend-fixed-relay-revised/harness/relay.py").read_text())
limits = {key: getattr(revised, key) for key in ("PAIR_LIMIT", "ACCEPT_LIMIT", "BUFFER_LIMIT", "PAIR_BYTES", "TOTAL_BYTES", "CONNECT_SECONDS")}
assert limits == {"PAIR_LIMIT": 4, "ACCEPT_LIMIT": 16, "BUFFER_LIMIT": 65536, "PAIR_BYTES": 4194304, "TOTAL_BYTES": 33554432, "CONNECT_SECONDS": 2}
verify_inputs()
receipt = {"scope": "F1 only; no joined JavaScript or runtime approval", "status": "F1-closed-source-only",
           "inputHashes": FILES, "fullPythonSuite": all_tests, "baselineFocusedRegression": red,
           "revisedFocusedRegression": green, "independentBidirectionalCases": cases,
           "unchangedOutsideReadAndTransferAst": True, "limits": limits,
           "realSocketFactoryDenied": True, "runtimeExecuted": False, "frozenInputsPreserved": True}
if "--record" in sys.argv:
    (BASE / "f1-verification.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
else:
    assert json.loads((BASE / "f1-verification.json").read_text()) == receipt
print(json.dumps(receipt))
