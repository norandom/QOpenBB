"""Reproduce a read/write readiness fault with injected sockets only."""
import importlib.util
import json
from pathlib import Path
import selectors
import sys

sys.dont_write_bytecode = True
source = Path(__file__).parent.parent / "ui-parity-legend-fixed-relay" / "test-relay.py"
spec = importlib.util.spec_from_file_location("relay_test_fixtures", source)
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)

client = fixtures.FakeSocket(reads=[b"A" * 65536, b"Z"], sends=[BlockingIOError()])
upstream = fixtures.FakeSocket(reads=[b"response", b""])
instance, pair, _, _ = fixtures.RelayTests().make(client, upstream)
instance.transfer(pair, 1, selectors.EVENT_READ)
instance.transfer(pair, 0, selectors.EVENT_READ | selectors.EVENT_WRITE)
stale_read = bool(instance.selector.entries[client][0] & selectors.EVENT_READ)
assert len(pair["buffers"][1]) == 65536 and stale_read
instance.transfer(pair, 0, selectors.EVENT_READ)
false_eof = pair["eof"][0] and client.reads == [b"Z"]
assert false_eof
instance.transfer(pair, 1, selectors.EVENT_WRITE)
instance.transfer(pair, 0, selectors.EVENT_WRITE)
instance.transfer(pair, 1, selectors.EVENT_READ)
assert not instance.pairs
assert upstream.sent == b"A" * 65536
assert client.reads == [b"Z"]
assert not any(instance.stats["violations"].values())
print(json.dumps({"reproduced": True, "networkOpened": False,
                  "staleReadRegistration": stale_read, "falseEof": false_eof,
                  "unreadClientBytes": sum(map(len, client.reads)),
                  "forwardedBytes": instance.stats["forwardedBytes"],
                  "receivedBytes": instance.stats["receivedBytes"],
                  "remainingPairs": len(instance.pairs),
                  "violations": instance.stats["violations"]}))
