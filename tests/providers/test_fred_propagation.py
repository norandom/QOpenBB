"""Original acquisition time survives transport cache paths."""
import asyncio
from datetime import datetime, timezone

import pytest
from openbb_fred.utils import cache, rate_limiter as limiter
from openbb_fred.utils.acquisition import FredAcquisition

URL = "https://api.stlouisfed.org/fred/series?series_id=GDP&api_key=fixture"
PAYLOAD = {"seriess": [{"id": "GDP"}]}
STAMP = datetime(2020, 1, 1, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    limiter.cache_clear()
    monkeypatch.setenv("OPENBB_FRED_DISK_CACHE", "0")
    monkeypatch.setenv("OPENBB_FRED_DISK_CACHE_DIR", str(tmp_path))
    cache.close()
    yield
    limiter.cache_clear()
    cache.close()


def test_network_memory_default(monkeypatch):
    calls = []
    async def fetch(*args, **kwargs):
        calls.append(kwargs)
        return {"value": [1]}
    monkeypatch.setattr(limiter, "_fetch", fetch)
    async def run():
        before = datetime.now(timezone.utc)
        first = await limiter.fred_get(URL, with_provenance=True)
        assert before <= first.retrieved_at <= datetime.now(timezone.utc)
        assert first.cache_state == "network"
        first.payload["value"].append(2)
        second = await limiter.fred_get(URL, with_provenance=True)
        assert second == FredAcquisition({"value": [1]}, first.retrieved_at, "memory")
        assert await limiter.fred_get(URL) == {"value": [1]}
    asyncio.run(run())
    assert len(calls) == 1


def test_disk_promoted_without_refresh(monkeypatch):
    monkeypatch.setenv("OPENBB_FRED_DISK_CACHE", "1")
    async def run():
        await cache.disk_set(URL, FredAcquisition(PAYLOAD, STAMP, "network"))
        assert await limiter.fred_get(URL, with_provenance=True) == FredAcquisition(PAYLOAD, STAMP, "disk")
        assert await limiter.fred_get(URL, with_provenance=True) == FredAcquisition(PAYLOAD, STAMP, "memory")
    asyncio.run(run())


def test_coalesced_mixed_callers_and_cancelled_waiter(monkeypatch):
    calls = []
    async def run():
        started, release = asyncio.Event(), asyncio.Event()
        async def fetch(*args, **kwargs):
            calls.append(1)
            started.set()
            await release.wait()
            return PAYLOAD
        monkeypatch.setattr(limiter, "_fetch", fetch)
        owner = asyncio.create_task(limiter.fred_get(URL))
        await started.wait()
        waiter = asyncio.create_task(limiter.fred_get(URL, with_provenance=True))
        cancelled = asyncio.create_task(limiter.fred_get(URL))
        await asyncio.sleep(0)
        cancelled.cancel()
        with pytest.raises(asyncio.CancelledError):
            await cancelled
        release.set()
        raw, result = await asyncio.gather(owner, waiter)
        assert raw == result.payload
        assert result.cache_state == "coalesced"
        memory = await limiter.fred_get(URL, with_provenance=True)
        assert memory.retrieved_at == result.retrieved_at
    asyncio.run(run())
    assert len(calls) == 1


def test_bypass(monkeypatch):
    async def forbidden(*args, **kwargs):
        pytest.fail("cache accessed")
    monkeypatch.setattr(cache, "disk_get", forbidden)
    monkeypatch.setattr(cache, "disk_set", forbidden)
    calls = []
    async def fetch(*args, **kwargs):
        calls.append(kwargs)
        await asyncio.sleep(0)
        return PAYLOAD
    monkeypatch.setattr(limiter, "_fetch", fetch)
    async def run():
        values = await asyncio.gather(*(limiter.fred_get(URL, with_provenance=True, use_cache=False, timeout=7) for _ in range(2)))
        assert all(v.cache_state == "network" for v in values)
        assert not limiter._cache
    asyncio.run(run())
    assert len(calls) == 2
    assert all(c["timeout"] == 7 and "with_provenance" not in c for c in calls)


@pytest.mark.parametrize("headers,expected", [({"Retry-After": "3"}, [3, 3]), ({}, [2, 4])])
def test_retry_after_finite_and_timeout(monkeypatch, headers, expected):
    from openbb_core.provider.utils import helpers
    calls, sleeps = [], []
    async def acquire():
        pass
    async def sleep(seconds):
        sleeps.append(seconds)
    class Response:
        status = 429
    Response.headers = headers
    async def request(url, response_callback, **kwargs):
        calls.append(kwargs)
        return await response_callback(Response(), None)
    monkeypatch.setattr(limiter, "acquire", acquire)
    monkeypatch.setattr(limiter.asyncio, "sleep", sleep)
    monkeypatch.setattr(helpers, "amake_request", request)
    with pytest.raises(Exception, match="rate limit"):
        asyncio.run(limiter.fred_get(URL, max_retries=2, use_cache=False, timeout=7))
    assert len(calls) == 3
    assert sleeps == expected
    assert all(c["timeout"] == 7 for c in calls)


def test_versioned_memory_key():
    assert limiter._cache_key(URL).startswith("fred-acquisition:1:")
    assert "fixture" not in limiter._cache_key(URL)


def test_legacy_memory_and_disk_are_misses(monkeypatch):
    monkeypatch.setenv("OPENBB_FRED_DISK_CACHE", "1")
    limiter._cache[cache.redact(URL)] = (limiter.time.monotonic(), PAYLOAD)
    cache.get_disk_cache().set(cache.redact(URL), PAYLOAD)
    calls = []
    async def fetch(*args, **kwargs):
        calls.append(1)
        return PAYLOAD
    monkeypatch.setattr(limiter, "_fetch", fetch)
    async def run():
        acquired = await limiter.fred_get(URL, with_provenance=True)
        limiter.cache_clear()
        disk = await limiter.fred_get(URL, with_provenance=True)
        assert disk == FredAcquisition(PAYLOAD, acquired.retrieved_at, "disk")
        assert cache.get_disk_cache().get(cache.redact(URL)) == PAYLOAD
    asyncio.run(run())
    assert len(calls) == 1


def test_failed_owner_releases_waiters_and_allows_retry(monkeypatch):
    async def run():
        started, release = asyncio.Event(), asyncio.Event()
        async def fetch(*args, **kwargs):
            started.set()
            await release.wait()
            raise ValueError("fixture failure")
        monkeypatch.setattr(limiter, "_fetch", fetch)
        owner = asyncio.create_task(limiter.fred_get(URL))
        await started.wait()
        waiter = asyncio.create_task(limiter.fred_get(URL, with_provenance=True))
        await asyncio.sleep(0)
        release.set()
        results = await asyncio.gather(owner, waiter, return_exceptions=True)
        assert all(isinstance(r, ValueError) for r in results)
        assert not limiter._inflight
        assert not limiter._cache
        async def success(*args, **kwargs):
            return PAYLOAD
        monkeypatch.setattr(limiter, "_fetch", success)
        assert await limiter.fred_get(URL) == PAYLOAD
    asyncio.run(run())
