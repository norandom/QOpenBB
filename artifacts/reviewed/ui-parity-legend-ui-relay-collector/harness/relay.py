"""Bounded test transport. The only upstream comes from the sealed config file."""
import errno
import hashlib
import ipaddress
import json
import selectors
import signal
import socket
import sys
import time

PAIR_LIMIT = 16
ACCEPT_LIMIT = 4096
BUFFER_LIMIT = 65536
PAIR_BYTES = 134217728
TOTAL_BYTES = 268435456
CONNECT_SECONDS = 2
STATS_PATH = "/evidence/relay-stats.json"


def config_target(value):
    if not isinstance(value, dict) or set(value) != {"upstreamIPv4", "upstreamPort"}:
        raise ValueError("config-shape")
    address = ipaddress.IPv4Address(value["upstreamIPv4"])
    if str(address) != value["upstreamIPv4"] or address.is_unspecified or address.is_loopback or address.is_multicast:
        raise ValueError("config-address")
    if type(value["upstreamPort"]) is not int or value["upstreamPort"] != 3000:
        raise ValueError("config-port")
    return str(address), 3000


def new_stats():
    return {"phase": "initializing", "cleanStop": False,
            "snapshotSequence": 0, "checkpointSequence": 0, "uptimeMs": 0, "acceptedPairs": 0,
            "activePairs": 0, "peakPairs": 0, "peakSockets": 0,
            "receivedBytes": 0, "forwardedBytes": 0, "peakBufferedBytes": 0,
            "maximumPairBytes": 0, "refusedConnections": 0, "peerClosures": 0,
            "violations": {key: 0 for key in ("accepted-pairs", "pair-bytes", "total-bytes",
                "connect-timeout", "transport-truncated", "socket-error", "config-error", "stats-error")}}


def save_stats(stats, filename=STATS_PATH):
    snapshot, checkpoint = stats.get("snapshotSequence"), stats.get("checkpointSequence")
    if type(snapshot) is not int or type(checkpoint) is not int or not 0 <= checkpoint <= 4 or snapshot < checkpoint:
        raise ValueError("stats-sequence")
    if type(stats.get("uptimeMs")) is not int or stats["uptimeMs"] < 0:
        raise ValueError("stats-uptime")
    payload = json.dumps(stats, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    envelope = {"version": 1, "snapshotSequence": snapshot, "checkpointSequence": checkpoint,
                "payloadJson": payload, "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest()}
    encoded = json.dumps(envelope, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    if len(encoded) > 4096:
        raise ValueError("stats-bound")
    # The controller reserves this one writable file before the read-only relay starts.
    with open(filename, "r+b", buffering=0) as stream:
        stream.seek(0)
        frame = encoded + b" " * (4096 - len(encoded))
        if stream.write(frame) != 4096:
            raise OSError("stats-short-write")
        stream.truncate(4096)


class Relay:
    def __init__(self, target, selector=None, clock=time.monotonic, factory=socket.socket):
        self.target, self.selector, self.clock, self.factory = target, selector or selectors.DefaultSelector(), clock, factory
        self.stats, self.pairs, self.listener, self.stopping = new_stats(), [], None, False
        self.started_at, self.checkpoint_pending = self.clock(), False

    def request_checkpoint(self):
        self.checkpoint_pending = True

    def write_snapshot(self, persist):
        self.stats["snapshotSequence"] += 1
        self.stats["uptimeMs"] = max(self.stats["uptimeMs"], int((self.clock() - self.started_at) * 1000))
        persist(self.stats)

    def breach(self, reason):
        self.stats["violations"][reason] += 1
        self.stopping = True

    def close_pair(self, pair):
        if pair not in self.pairs:
            return
        for endpoint in pair["ends"]:
            try:
                self.selector.unregister(endpoint)
            except (KeyError, ValueError):
                pass
            endpoint.close()
        self.pairs.remove(pair)
        self.stats["activePairs"] = len(self.pairs)

    def set_events(self, endpoint, mask, data):
        try:
            self.selector.unregister(endpoint)
        except (KeyError, ValueError):
            pass
        if mask:
            self.selector.register(endpoint, mask, data)

    def refresh(self, pair):
        for side, endpoint in enumerate(pair["ends"]):
            other = 1 - side
            if pair["eof"][other] and not pair["buffers"][side] and not pair["shutdown"][side] and (side == 0 or not pair["connecting"]):
                endpoint.shutdown(socket.SHUT_WR)
                pair["shutdown"][side] = True
            mask = 0
            if side == 1 and pair["connecting"]:
                mask = selectors.EVENT_WRITE
            else:
                if not pair["eof"][side] and len(pair["buffers"][other]) < BUFFER_LIMIT:
                    mask |= selectors.EVENT_READ
                if pair["buffers"][side]:
                    mask |= selectors.EVENT_WRITE
            self.set_events(endpoint, mask, (pair, side))
        if all(pair["eof"]) and not any(pair["buffers"]):
            self.close_pair(pair)

    def accept_pair(self):
        client, _ = self.listener.accept()  # Peer addresses are deliberately discarded.
        client.setblocking(False)
        self.stats["acceptedPairs"] += 1
        upstream = None
        try:
            upstream = self.factory(socket.AF_INET, socket.SOCK_STREAM)
            upstream.setblocking(False)
            result = upstream.connect_ex(self.target)
            if result not in (0, errno.EINPROGRESS, errno.EWOULDBLOCK, errno.EALREADY):
                if result == errno.ECONNREFUSED:
                    self.stats["refusedConnections"] += 1
                else:
                    self.breach("socket-error")
                client.close()
                upstream.close()
                return
            pair = {"ends": [client, upstream], "buffers": [bytearray(), bytearray()],
                    "eof": [False, False], "shutdown": [False, False], "bytes": 0,
                    "connecting": result != 0, "connectBy": self.clock() + CONNECT_SECONDS}
            self.pairs.append(pair)
            self.stats["activePairs"] = len(self.pairs)
            self.stats["peakPairs"] = max(self.stats["peakPairs"], len(self.pairs))
            self.stats["peakSockets"] = max(self.stats["peakSockets"], 1 + 2 * len(self.pairs))
            self.refresh(pair)
        except OSError:
            client.close()
            if upstream is not None:
                upstream.close()
            self.breach("socket-error")

    def read(self, pair, side):
        buffer = pair["buffers"][1 - side]
        capacity = BUFFER_LIMIT - len(buffer)
        if capacity <= 0:
            return
        payload = pair["ends"][side].recv(capacity)
        if not payload:
            pair["eof"][side] = True
            return
        # Received bytes reserve forwarding capacity before any payload is queued.
        if pair["bytes"] + len(payload) > PAIR_BYTES:
            self.breach("pair-bytes")
            return
        if self.stats["receivedBytes"] + len(payload) > TOTAL_BYTES:
            self.breach("total-bytes")
            return
        pair["bytes"] += len(payload)
        self.stats["receivedBytes"] += len(payload)
        self.stats["maximumPairBytes"] = max(self.stats["maximumPairBytes"], pair["bytes"])
        buffer.extend(payload)
        buffered = sum(sum(len(buf) for buf in current["buffers"]) for current in self.pairs)
        self.stats["peakBufferedBytes"] = max(self.stats["peakBufferedBytes"], buffered)

    def transfer(self, pair, side, mask):
        endpoint = pair["ends"][side]
        try:
            try:
                if side == 1 and pair["connecting"]:
                    error = endpoint.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                    if error:
                        if error == errno.ECONNREFUSED:
                            self.stats["refusedConnections"] += 1
                        else:
                            self.breach("socket-error")
                        self.close_pair(pair)
                        return
                    pair["connecting"] = False
                else:
                    if mask & selectors.EVENT_READ:
                        self.read(pair, side)
                    if mask & selectors.EVENT_WRITE and pair["buffers"][side] and not self.stopping:
                        count = endpoint.send(pair["buffers"][side])
                        del pair["buffers"][side][:count]
                        self.stats["forwardedBytes"] += count
            except (BlockingIOError, InterruptedError):
                # A preceding read may have filled the opposite buffer.
                pass
            if not self.stopping:
                self.refresh(pair)
        except (BlockingIOError, InterruptedError):
            pass
        except (ConnectionResetError, BrokenPipeError):
            self.stats["peerClosures"] += 1
            # A reset with unforwarded bytes is a truncated transport, never a pass.
            if any(pair["buffers"]):
                self.breach("socket-error")
            self.close_pair(pair)
        except OSError:
            self.breach("socket-error")
            self.close_pair(pair)

    def tick(self):
        for pair in self.pairs[:]:
            if pair["connecting"] and self.clock() >= pair["connectBy"]:
                self.breach("connect-timeout")
        accepting = len(self.pairs) < PAIR_LIMIT and self.stats["acceptedPairs"] < ACCEPT_LIMIT
        self.set_events(self.listener, selectors.EVENT_READ if accepting else 0, None)
        if self.stats["acceptedPairs"] >= ACCEPT_LIMIT:
            self.breach("accepted-pairs")

    def run(self, persist=save_stats):
        try:
            self.listener = self.factory(socket.AF_INET, socket.SOCK_STREAM)
            self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listener.bind(("0.0.0.0", 3100))
            self.listener.listen(PAIR_LIMIT)
            self.listener.setblocking(False)
            self.stats["phase"], self.stats["peakSockets"] = "listening", 1
            self.write_snapshot(persist)
            while not self.stopping:
                if self.checkpoint_pending:
                    self.checkpoint_pending = False
                    if self.stats["checkpointSequence"] >= 4:
                        self.breach("stats-error")
                        break
                    self.stats["checkpointSequence"] += 1
                    self.write_snapshot(persist)
                self.tick()
                if self.stopping:
                    break
                for key, mask in self.selector.select(0.05):
                    if self.stopping:
                        break
                    if key.data is None:
                        self.accept_pair()
                    elif key.data[0] in self.pairs:
                        self.transfer(*key.data, mask)
                    if self.stopping:
                        break
        except (OSError, ValueError):
            self.breach("socket-error")
        finally:
            if self.pairs:
                self.breach("transport-truncated")
            for pair in self.pairs[:]:
                self.close_pair(pair)
            if self.listener is not None:
                self.listener.close()
            self.selector.close()
            self.stats["phase"], self.stats["cleanStop"] = "closed", True
            self.write_snapshot(persist)


def main():
    relay = None
    try:
        if len(sys.argv) != 2 or sys.argv[1] != "/relay/config.json":
            raise ValueError("config-path")
        with open(sys.argv[1], encoding="ascii") as stream:
            target = config_target(json.loads(stream.read(257)))
        relay = Relay(target)
        signal.signal(signal.SIGTERM, lambda *_: setattr(relay, "stopping", True))
        signal.signal(signal.SIGINT, lambda *_: setattr(relay, "stopping", True))
        signal.signal(signal.SIGUSR1, lambda *_: relay.request_checkpoint())
        relay.run()
        return int(any(relay.stats["violations"].values()))
    except Exception:
        stats = relay.stats if relay is not None else new_stats()
        stats["phase"] = "failed"
        stats["violations"]["config-error" if relay is None else "stats-error"] += 1
        try:
            if relay is not None:
                relay.write_snapshot(save_stats)
            else:
                stats["snapshotSequence"] = 1
                save_stats(stats)
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    sys.exit(main())
