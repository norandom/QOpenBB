"""Acceptance transport guard for the packaged aiohttp FMP adapters."""

import contextvars
import hashlib
import json
import os
from pathlib import Path
from threading import Lock
from urllib.parse import parse_qsl, urlsplit

EXPECTED_ENTRYPOINT = ["uvicorn", "qopenbb_data.app:create_app", "--factory", "--host",
                       "0.0.0.0", "--port", "6900", "--no-access-log"]
CURRENT = contextvars.ContextVar("events_receipt", default=None)


class Rejected(RuntimeError):
    """Fixed diagnostic without a URL, query credential, response body or exception chain."""


def schedule(plan):
    translation = {"start_date": "from", "end_date": "to"}
    stages = {}
    symbols = plan.get("symbols", {"launch": "AAPL", "later": "MSFT"})
    for stage, slots in plan["groups"].items():
        stage_wire = stages[stage] = {}
        for slot in slots:
            choice = plan["edits" if stage in (slot, "reopen") else "initial"][slot]
            query = {translation.get(k, k): str(v) for k, v in choice.items()}
            if slot != "calendar":
                query["symbols" if slot == "news" else "symbol"] = symbols["launch" if stage == "launch" else "later"]
            stage_wire[slot] = (plan["slots"][slot][1], query)
    limit = plan["send_limit"]
    if limit < 1 or sum(map(len, stages.values())) != limit:
        raise Rejected("invalid frozen schedule")
    return stages


def wire(request):
    url = urlsplit(str(request.url))
    if (request.method != "GET" or url.scheme != "https" or url.netloc not in
            ("financialmodelingprep.com", "financialmodelingprep.com:443")
            or url.fragment or getattr(request, "proxy", None) or not url.path.startswith("/stable/")):
        raise ValueError
    pairs = parse_qsl(url.query, keep_blank_values=True, strict_parsing=True)
    query = dict(pairs)
    if len(pairs) != len(query) or not query.pop("apikey", None):
        raise ValueError
    return url.path.removeprefix("/stable/"), query


class Guard:
    def __init__(self, directory, phase, stages, live, require_context=False):
        self.directory, self.phase = Path(directory), Path(phase)
        self.directory.mkdir(mode=0o700)
        self.stages, self.live, self.require_context = stages, live, require_context
        self.limit = sum(map(len, stages.values()))
        self.pid, self.lock = os.getpid(), Lock()
        self.entries, self.denials = [], 0
        self.spent, self.poisoned = set(), False
        self.persist()

    @property
    def count(self):
        return len(self.entries)

    def persist(self):
        target = self.directory / "ledger.json"
        temp = target.with_suffix(".pending")
        try:
            fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w") as stream:
                json.dump({"count": self.count, "denials": self.denials, "entries": self.entries}, stream)
                stream.flush()
                os.fsync(stream.fileno())
            temp.replace(target)
            fd = os.open(self.directory, os.O_DIRECTORY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        except OSError:
            self.poisoned = True
            raise Rejected("ledger persistence") from None

    def reserve(self, request):
        with self.lock:
            if self.pid != os.getpid() or self.poisoned:
                raise Rejected("process guard")
            extension = CURRENT.get()
            try:
                stage = self.phase.read_text().strip()
                outgoing = wire(request)
                slot = next(key for key, value in self.stages[stage].items() if value == outgoing)
                if (not self.live or self.count >= self.limit or (stage, slot) in self.spent
                        or (self.require_context and (extension is None or extension["slot"] != slot))):
                    raise ValueError
            except (OSError, AttributeError, KeyError, StopIteration, ValueError):
                self.denials += 1
                self.persist()
                raise Rejected("outbound request outside frozen schedule") from None
            self.spent.add((stage, slot))
            number = self.count + 1
            self.entries.append({"number": number, "stage": stage, "slot": slot, "endpoint": outgoing[0],
                                 "effective_query": outgoing[1], "status": None, "sha256": None})
            self.persist()
            if extension:
                extension["number"] = number
            return number

    async def send(self, original, request, connection):
        number = self.reserve(request)
        response = await original(request, connection)
        response._events_number = number
        return response

    def observe(self, number, status, body=None):
        with self.lock:
            entry = self.entries[number - 1]
            entry["status"] = status
            if body is not None:
                path = self.directory / f"{number}.provider"
                if not path.exists():
                    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                    with os.fdopen(fd, "wb") as stream:
                        stream.write(body)
                entry["sha256"] = hashlib.sha256(body).hexdigest()
            self.persist()


def install_guard(guard):
    import aiohttp
    if aiohttp.__version__ != "3.14.5" or getattr(aiohttp.ClientRequest.send, "_events_guard", False):
        raise Rejected("unverified aiohttp transport")
    original_send = aiohttp.ClientRequest.send
    original_start = aiohttp.ClientResponse.start
    original_read = aiohttp.ClientResponse.read

    async def guarded_send(request, connection):
        return await guard.send(original_send, request, connection)

    async def observe_headers(response, *args, **kwargs):
        result = await original_start(response, *args, **kwargs)
        if number := getattr(response, "_events_number", None):
            guard.observe(number, response.status)
        return result

    async def observe_body(response):
        body = await original_read(response)
        if number := getattr(response, "_events_number", None):
            guard.observe(number, response.status, body)
        return body

    guarded_send._events_guard = True
    aiohttp.ClientRequest.send = guarded_send
    aiohttp.ClientResponse.start = observe_headers
    aiohttp.ClientResponse.read = observe_body


def receipt_middleware(app, plan):
    paths = {f"/api/v1/{dataset}": slot for slot, (dataset, _) in plan["slots"].items()}

    async def wrapped(scope, receive, send):
        record = {"slot": paths.get(scope.get("path"))}
        token = CURRENT.set(record)

        async def respond(message):
            if message["type"] == "http.response.start" and record.get("number"):
                message["headers"].append((b"x-qopenbb-events-receipt", str(record["number"]).encode()))
            await send(message)

        try:
            await app(scope, receive, respond)
        finally:
            CURRENT.reset(token)
    return wrapped


def serve(plan, live):
    if os.environ.get("WEB_CONCURRENCY", "1") != "1" or os.environ.get("UVICORN_WORKERS", "1") != "1":
        raise Rejected("single worker required")
    phase = Path("/tmp/events-stage")
    phase.write_text("disarmed")
    install_guard(Guard("/tmp/events-captures", phase, schedule(plan), live, True))
    from qopenbb_data.app import create_app
    import uvicorn
    uvicorn.run(receipt_middleware(create_app(), plan), host="0.0.0.0", port=6900, workers=1, access_log=False)


def bootstrap(plan, live, entrypoint):
    if entrypoint != EXPECTED_ENTRYPOINT:
        raise Rejected("unverified candidate entrypoint")
    return Path(__file__).read_text() + f"\nserve({plan!r}, {live!r})\n"
