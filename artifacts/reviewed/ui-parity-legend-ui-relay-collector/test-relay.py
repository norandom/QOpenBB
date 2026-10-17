"""Offline relay faults: injected sockets/selectors only; no network is opened."""
import errno
import hashlib
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
        self.recv_counts = []

    def setblocking(self, value):
        self.blocking = value

    def connect_ex(self, target):
        self.connected.append(target)
        return self.connect_result

    def recv(self, count):
        self.recv_counts.append(count)
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

    def test_combined_read_write_backpressure_keeps_unread_byte(self):
        for would_block in (BlockingIOError(), InterruptedError()):
            with self.subTest(error=type(would_block).__name__):
                payload = b"A" * 65536
                client = FakeSocket([payload, b"Z", b""], sends=[would_block])
                upstream = FakeSocket([b"response", b""])
                instance, pair, _, _ = self.make(client, upstream)
                instance.transfer(pair, 1, selectors.EVENT_READ)
                instance.transfer(pair, 0, selectors.EVENT_READ | selectors.EVENT_WRITE)
                self.assertEqual(len(pair["buffers"][1]), 65536)
                self.assertFalse(instance.selector.entries[client][0] & selectors.EVENT_READ)
                self.assertFalse(any(pair["eof"]))
                self.assertEqual(client.reads, [b"Z", b""])
                self.assertEqual(client.shut + upstream.shut, [])
                # A stale event must not turn a full buffer into peer EOF.
                before = list(client.recv_counts)
                instance.transfer(pair, 0, selectors.EVENT_READ)
                self.assertEqual(client.recv_counts, before)
                self.assertFalse(pair["eof"][0])
                instance.transfer(pair, 1, selectors.EVENT_WRITE)
                self.assertTrue(instance.selector.entries[client][0] & selectors.EVENT_READ)
                instance.transfer(pair, 0, selectors.EVENT_READ)
                instance.transfer(pair, 1, selectors.EVENT_WRITE)
                instance.transfer(pair, 0, selectors.EVENT_WRITE)
                self.assertEqual(bytes(upstream.sent), payload + b"Z")
                self.assertEqual(bytes(client.sent), b"response")
                self.assertEqual(client.shut + upstream.shut, [])
                instance.transfer(pair, 0, selectors.EVENT_READ)
                self.assertEqual(upstream.shut, [socket.SHUT_WR])
                instance.transfer(pair, 1, selectors.EVENT_READ)
                self.assertEqual(client.shut, [socket.SHUT_WR])
                self.assertEqual(instance.pairs, [])
                self.assertEqual(client.reads, [])
                self.assertNotIn(0, client.recv_counts + upstream.recv_counts)
                self.assertEqual(instance.stats["receivedBytes"], 65545)
                self.assertEqual(instance.stats["forwardedBytes"], 65545)
                self.assertFalse(any(instance.stats["violations"].values()))

    def test_concurrent_and_accepted_caps(self):
        instance = relay.Relay(("172.30.0.10", 3000), selector=FakeSelector(), factory=lambda *_: FakeSocket())
        instance.listener = FakeSocket()
        for _ in range(16):
            instance.listener.accepted.append(FakeSocket())
            instance.accept_pair()
        instance.tick()
        self.assertEqual(instance.stats["peakSockets"], 33)
        self.assertEqual(instance.stats["peakPairs"], 16)
        self.assertNotIn(instance.listener, instance.selector.entries)
        instance.close_pair(instance.pairs[0])
        instance.tick()
        self.assertEqual(instance.selector.entries[instance.listener][0], selectors.EVENT_READ)
        for pair in instance.pairs[:]:
            instance.close_pair(pair)
        for _ in range(4080):
            instance.listener.accepted.append(FakeSocket())
            instance.accept_pair()
            instance.close_pair(instance.pairs[0])
        instance.tick()
        self.assertEqual(instance.stats["acceptedPairs"], 4096)
        self.assertEqual(instance.stats["violations"]["accepted-pairs"], 1)
        self.assertTrue(instance.stopping)
        self.assertNotIn(instance.listener, instance.selector.entries)

    def test_pair_and_global_byte_limits(self):
        for field, limit, reason in (("pair", 134217728, "pair-bytes"), ("total", 268435456, "total-bytes")):
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
            self.assertEqual(target.stat().st_size, 4096)
            envelope = json.loads(target.read_bytes())
            self.assertEqual(json.loads(envelope["payloadJson"]), instance.stats)
            before = target.read_bytes()
            with self.assertRaises(ValueError):
                relay.save_stats(dict(instance.stats, oversized="x" * 4096), target)
            self.assertEqual(target.read_bytes(), before)

    def test_exact_ui_profile(self):
        self.assertEqual((relay.PAIR_LIMIT, relay.ACCEPT_LIMIT, relay.BUFFER_LIMIT,
                          relay.PAIR_BYTES, relay.TOTAL_BYTES, relay.CONNECT_SECONDS),
                         (16, 4096, 65536, 134217728, 268435456, 2))

    def test_fixed_frame_payload_hash_and_sequences(self):
        stats = dict(relay.new_stats(), snapshotSequence=2, checkpointSequence=1, uptimeMs=250)
        with tempfile.TemporaryDirectory(prefix="qopenbb-relay-frame-") as directory:
            target = Path(directory) / "stats.json"
            target.write_bytes(b" " * 4096)
            relay.save_stats(stats, target)
            raw = target.read_bytes()
            self.assertEqual(len(raw), 4096)
            frame = json.loads(raw)
            self.assertEqual(set(frame), {"version", "snapshotSequence", "checkpointSequence", "payloadJson", "sha256"})
            self.assertEqual(frame["version"], 1)
            self.assertEqual(frame["snapshotSequence"], 2)
            self.assertEqual(frame["checkpointSequence"], 1)
            self.assertEqual(frame["sha256"], hashlib.sha256(frame["payloadJson"].encode("utf-8")).hexdigest())
            self.assertEqual(json.loads(frame["payloadJson"]), stats)
            self.assertTrue(raw.endswith(b" "))
            before = raw
            for change in ({"snapshotSequence": True}, {"checkpointSequence": -1},
                           {"checkpointSequence": 5}, {"uptimeMs": float("nan")},
                           {"extra": "漢" * 4096}):
                with self.subTest(change=next(iter(change))), self.assertRaises(ValueError):
                    relay.save_stats(dict(stats, **change), target)
                self.assertEqual(target.read_bytes(), before)

    def checkpoint_run(self, count, fifth=False):
        now, saved = [0.0], []
        selector = FakeSelector()
        instance = relay.Relay(("172.30.0.10", 3000), selector=selector,
                               clock=lambda: now[0], factory=lambda *_: FakeSocket())
        def next_event():
            now[0] += 0.25
            if instance.stats["checkpointSequence"] < count or fifth:
                instance.request_checkpoint()
                instance.request_checkpoint()  # Coalesced while exactly one request is outstanding.
            else:
                instance.stopping = True
            return []
        selector.on_select = next_event
        instance.run(persist=lambda stats: saved.append(json.loads(json.dumps(stats))))
        return instance, saved

    def test_fresh_bounded_checkpoint_sequence_and_final_snapshot(self):
        instance, saved = self.checkpoint_run(4)
        self.assertEqual([v["snapshotSequence"] for v in saved], [1, 2, 3, 4, 5, 6])
        self.assertEqual([v["checkpointSequence"] for v in saved], [0, 1, 2, 3, 4, 4])
        self.assertEqual([v["uptimeMs"] for v in saved], [0, 250, 500, 750, 1000, 1250])
        self.assertEqual(saved[0]["phase"], "listening")
        self.assertEqual(saved[-1]["phase"], "closed")
        self.assertEqual(saved[-1]["activePairs"], 0)
        self.assertFalse(any(instance.stats["violations"].values()))

    def test_partial_journey_allows_fewer_checkpoints_and_final_close(self):
        for count in (0, 2):
            with self.subTest(checkpoints=count):
                instance, saved = self.checkpoint_run(count)
                self.assertEqual(len(saved), count + 2)
                self.assertEqual(saved[-1]["checkpointSequence"], count)
                self.assertEqual(saved[-1]["phase"], "closed")
                self.assertGreater(saved[-1]["snapshotSequence"], saved[-2]["snapshotSequence"])
                self.assertFalse(any(instance.stats["violations"].values()))

    def test_fifth_checkpoint_request_is_unresolved_not_an_extra_ack(self):
        instance, saved = self.checkpoint_run(4, fifth=True)
        self.assertEqual(saved[-1]["checkpointSequence"], 4)
        self.assertEqual(len(saved), 6)
        self.assertEqual(saved[-1]["violations"]["stats-error"], 1)
        self.assertTrue(instance.stopping)

    def test_refused_connection_counters_do_not_claim_zero_loss(self):
        instance, pair, client, upstream = self.make(FakeSocket([b"pending"]), FakeSocket(connect=errno.EINPROGRESS))
        instance.transfer(pair, 0, selectors.EVENT_READ)
        upstream.error = errno.ECONNREFUSED
        instance.transfer(pair, 1, selectors.EVENT_WRITE)
        self.assertEqual(instance.stats["receivedBytes"], 7)
        self.assertEqual(instance.stats["forwardedBytes"], 0)
        self.assertEqual(instance.stats["refusedConnections"], 1)
        self.assertFalse(any(instance.stats["violations"].values()))
        self.assertEqual(instance.pairs, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
