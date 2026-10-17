"""Offline relay faults: injected sockets/selectors only; no network is opened."""
import errno
import importlib.util
import json
from pathlib import Path
import selectors
import socket
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
SOURCE = Path(__file__).parent / "harness" / "relay.py"
SPEC = importlib.util.spec_from_file_location("offline_relay", SOURCE)
relay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(relay)


class FakeSocket:
    def __init__(self, reads=(), connect=0, sends=()):
        self.reads, self.sends = list(reads), list(sends)
        self.connect_result, self.connected = connect, []
        self.sent, self.shut = bytearray(), []
        self.closed, self.blocking, self.accepted = False, None, []
        self.error, self.bound, self.backlog = 0, None, None

    def setblocking(self, value):
        self.blocking = value

    def connect_ex(self, target):
        self.connected.append(target)
        return self.connect_result

    def recv(self, count):
        if not self.reads:
            raise BlockingIOError()
        value = self.reads.pop(0)
        if isinstance(value, BaseException):
            raise value
        if len(value) > count:
            self.reads.insert(0, value[count:])
        return value[:count]

    def send(self, data):
        count = self.sends.pop(0) if self.sends else len(data)
        if isinstance(count, BaseException):
            raise count
        count = min(count, len(data))
        self.sent.extend(data[:count])
        return count

    def shutdown(self, how):
        self.shut.append(how)

    def getsockopt(self, *_):
        return self.error

    def close(self):
        self.closed = True

    def accept(self):
        return self.accepted.pop(0), ("discarded-peer", 1)

    def setsockopt(self, *_):
        pass

    def bind(self, target):
        self.bound = target

    def listen(self, backlog):
        self.backlog = backlog


class FakeSelector:
    def __init__(self):
        self.entries, self.closed, self.on_select = {}, False, None

    def unregister(self, endpoint):
        return self.entries.pop(endpoint)

    def register(self, endpoint, mask, data):
        self.entries[endpoint] = (mask, data)

    def select(self, timeout):
        if self.on_select:
            return self.on_select()
        raise AssertionError("unexpected selector loop")

    def close(self):
        self.closed = True


class RelayTests(unittest.TestCase):
    def make(self, client=None, upstream=None, clock=lambda: 0):
        client, upstream = client or FakeSocket(), upstream or FakeSocket()
        instance = relay.Relay(("172.30.0.10", 3000), selector=FakeSelector(),
                               clock=clock, factory=lambda *_: upstream)
        instance.listener = FakeSocket()
        instance.listener.accepted = [client]
        instance.accept_pair()
        return instance, instance.pairs[0], client, upstream

    def test_fixed_target_config(self):
        good = {"upstreamIPv4": "172.30.0.10", "upstreamPort": 3000}
        self.assertEqual(relay.config_target(good), ("172.30.0.10", 3000))
        bad = [dict(good, upstreamIPv4=value) for value in
               ("example.invalid", "http://172.30.0.10:3000", "127.0.0.1", "0.0.0.0", "224.0.0.1", "172.030.0.10")]
        bad += [dict(good, upstreamPort=value) for value in (80, "3000", True, 3000.0)]
        bad += [dict(good, host="ignored"), {}, [], None]
        for value in bad:
            with self.subTest(value=value), self.assertRaises((ValueError, TypeError)):
                relay.config_target(value)

    def test_byte_passthrough_and_fixed_connect(self):
        payload = b"GET /ws HTTP/1.1\r\nUpgrade: websocket\r\n\r\n\x81\x85\x00\xff\x00"
        response = b"HTTP/1.1 101 Switching Protocols\r\n\r\n\x82\x03\xff\x00\x01"
        instance, pair, client, upstream = self.make(FakeSocket([payload]), FakeSocket([response]))
        self.assertEqual(upstream.connected, [("172.30.0.10", 3000)])
        instance.transfer(pair, 0, selectors.EVENT_READ)
        instance.transfer(pair, 1, selectors.EVENT_WRITE)
        instance.transfer(pair, 1, selectors.EVENT_READ)
        instance.transfer(pair, 0, selectors.EVENT_WRITE)
        self.assertEqual(bytes(upstream.sent), payload)
        self.assertEqual(bytes(client.sent), response)
        self.assertEqual(instance.stats["receivedBytes"], len(payload) + len(response))
        self.assertEqual(instance.stats["forwardedBytes"], instance.stats["receivedBytes"])

    def test_partial_send_backpressure_and_retry(self):
        payload = bytes(range(256)) * 257
        instance, pair, client, upstream = self.make(FakeSocket([payload]), FakeSocket(sends=[BlockingIOError(), 7]))
        instance.transfer(pair, 0, selectors.EVENT_READ)
        self.assertEqual(len(pair["buffers"][1]), 65536)
        self.assertNotIn(client, instance.selector.entries)
        instance.transfer(pair, 1, selectors.EVENT_WRITE)
        self.assertEqual(len(pair["buffers"][1]), 65536)
        instance.transfer(pair, 1, selectors.EVENT_WRITE)
        self.assertEqual(len(pair["buffers"][1]), 65529)
        self.assertTrue(instance.selector.entries[client][0] & selectors.EVENT_READ)
        instance.transfer(pair, 1, selectors.EVENT_WRITE)
        instance.transfer(pair, 0, selectors.EVENT_READ)
        instance.transfer(pair, 1, selectors.EVENT_WRITE)
        self.assertEqual(bytes(upstream.sent), payload)
        self.assertLessEqual(instance.stats["peakBufferedBytes"], 65536)

    def test_half_close_waits_for_buffer_drain(self):
        instance, pair, client, upstream = self.make(FakeSocket([b"abc", b""]), FakeSocket(sends=[1]))
        instance.transfer(pair, 0, selectors.EVENT_READ)
        instance.transfer(pair, 0, selectors.EVENT_READ)
        self.assertEqual(upstream.shut, [])
        instance.transfer(pair, 1, selectors.EVENT_WRITE)
        self.assertEqual(upstream.shut, [])
        instance.transfer(pair, 1, selectors.EVENT_WRITE)
        self.assertEqual(bytes(upstream.sent), b"abc")
        self.assertEqual(upstream.shut, [socket.SHUT_WR])
        upstream.reads = [b""]
        instance.transfer(pair, 1, selectors.EVENT_READ)
        self.assertEqual(client.shut, [socket.SHUT_WR])
        self.assertEqual(instance.pairs, [])

    def test_concurrent_and_accepted_caps(self):
        instance = relay.Relay(("172.30.0.10", 3000), selector=FakeSelector(), factory=lambda *_: FakeSocket())
        instance.listener = FakeSocket()
        for _ in range(4):
            instance.listener.accepted.append(FakeSocket())
            instance.accept_pair()
        instance.tick()
        self.assertEqual(instance.stats["peakSockets"], 9)
        self.assertEqual(instance.stats["peakPairs"], 4)
        self.assertNotIn(instance.listener, instance.selector.entries)
        instance.close_pair(instance.pairs[0])
        instance.tick()
        self.assertEqual(instance.selector.entries[instance.listener][0], selectors.EVENT_READ)
        for pair in instance.pairs[:]:
            instance.close_pair(pair)
        for _ in range(12):
            instance.listener.accepted.append(FakeSocket())
            instance.accept_pair()
            instance.close_pair(instance.pairs[0])
        instance.tick()
        self.assertEqual(instance.stats["acceptedPairs"], 16)
        self.assertEqual(instance.stats["violations"]["accepted-pairs"], 1)
        self.assertTrue(instance.stopping)
        self.assertNotIn(instance.listener, instance.selector.entries)

    def test_pair_and_global_byte_limits(self):
        for field, limit, reason in (("pair", 4194304, "pair-bytes"), ("total", 33554432, "total-bytes")):
            with self.subTest(field=field):
                instance, pair, _, _ = self.make(FakeSocket([b"a", b"b"]))
                if field == "pair":
                    pair["bytes"] = limit - 1
                else:
                    instance.stats["receivedBytes"] = limit - 1
                instance.transfer(pair, 0, selectors.EVENT_READ)
                accepted = (pair["bytes"], instance.stats["receivedBytes"], bytes(pair["buffers"][1]))
                instance.transfer(pair, 0, selectors.EVENT_READ)
                self.assertEqual((pair["bytes"], instance.stats["receivedBytes"], bytes(pair["buffers"][1])), accepted)
                self.assertEqual(instance.stats["violations"][reason], 1)
                self.assertTrue(instance.stopping)

    def test_connect_timeout_and_connection_completion(self):
        now = [0]
        instance, pair, _, upstream = self.make(upstream=FakeSocket(connect=errno.EINPROGRESS), clock=lambda: now[0])
        self.assertTrue(pair["connecting"])
        now[0] = 1.999
        instance.tick()
        self.assertFalse(instance.stopping)
        now[0] = 2
        instance.tick()
        self.assertEqual(instance.stats["violations"]["connect-timeout"], 1)
        instance, pair, _, _ = self.make(upstream=FakeSocket(connect=errno.EINPROGRESS))
        instance.transfer(pair, 1, selectors.EVENT_WRITE)
        self.assertFalse(pair["connecting"])

    def test_reset_with_pending_bytes_is_unresolved(self):
        instance, pair, client, upstream = self.make(FakeSocket([b"pending"]), FakeSocket(sends=[ConnectionResetError()]))
        instance.transfer(pair, 0, selectors.EVENT_READ)
        instance.transfer(pair, 1, selectors.EVENT_WRITE)
        self.assertTrue(instance.stopping)
        self.assertGreater(sum(instance.stats["violations"].values()), 0)
        self.assertEqual(instance.stats["forwardedBytes"], 0)
        self.assertTrue(client.closed and upstream.closed)
        self.assertEqual(instance.pairs, [])

    def test_stop_with_active_pair_and_bounded_stats(self):
        listener, upstream, client = FakeSocket(), FakeSocket(), FakeSocket()
        listener.accepted = [client]
        endpoints = iter([listener, upstream])
        selector = FakeSelector()
        instance = relay.Relay(("172.30.0.10", 3000), selector=selector, factory=lambda *_: next(endpoints))
        def stop_after_pair():
            instance.accept_pair()
            instance.stopping = True
            return []
        selector.on_select = stop_after_pair
        receipts = []
        instance.run(persist=lambda stats: receipts.append(json.loads(json.dumps(stats))))
        self.assertEqual(listener.bound, ("0.0.0.0", 3100))
        self.assertEqual(instance.stats["violations"]["transport-truncated"], 1)
        self.assertEqual(instance.stats["activePairs"], 0)
        self.assertEqual(instance.stats["phase"], "closed")
        self.assertTrue(selector.closed and listener.closed and client.closed and upstream.closed)
        self.assertEqual(len(receipts), 2)
        self.assertFalse(any("discarded-peer" in json.dumps(value) for value in receipts))
        with tempfile.TemporaryDirectory(prefix="qopenbb-relay-offline-") as directory:
            target = Path(directory) / "stats.json"
            target.write_bytes(b" " * 4096)
            relay.save_stats(instance.stats, target)
            self.assertLessEqual(target.stat().st_size, 4096)
            self.assertEqual(json.loads(target.read_bytes()), instance.stats)
            before = target.read_bytes()
            with self.assertRaises(ValueError):
                relay.save_stats({"oversized": "x" * 4096}, target)
            self.assertEqual(target.read_bytes(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
