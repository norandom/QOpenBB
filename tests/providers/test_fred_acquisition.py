"""Acquisition freshness survives disk storage without changing raw callers."""

import asyncio
from datetime import datetime, timedelta, timezone

import pytest
from openbb_fred.utils import cache
from openbb_fred.utils.acquisition import FredAcquisition

URL = "https://api.stlouisfed.org/fred/series?series_id=GDP&api_key=fixture"
STAMP = datetime(2024, 1, 2, 3, 4, 5, 123456, tzinfo=timezone.utc)
PAYLOAD = {"observations": [{"value": "-2.5"}, {"value": "."}]}


@pytest.fixture
def disk(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENBB_FRED_DISK_CACHE", "1")
    monkeypatch.setenv("OPENBB_FRED_DISK_CACHE_DIR", str(tmp_path))
    cache.close()
    yield cache.get_disk_cache()
    cache.close()


def test_disk_roundtrip_retains_acquisition_time_and_raw_payload(disk):
    acquisition = FredAcquisition(PAYLOAD, STAMP, "network")
    asyncio.run(cache.disk_set(URL, acquisition))
    cache.close()
    restored = asyncio.run(cache.disk_get(URL, with_provenance=True))
    assert restored == FredAcquisition(PAYLOAD, STAMP, "disk")
    assert asyncio.run(cache.disk_get(URL)) == PAYLOAD


def test_legacy_payload_is_a_miss_without_deleting_unrelated_data(disk):
    disk.set(cache.redact(URL), PAYLOAD)
    disk.set("unrelated", "retain")
    assert asyncio.run(cache.disk_get(URL)) is None
    assert asyncio.run(cache.disk_get(URL, with_provenance=True)) is None
    assert disk.get(cache.redact(URL)) == PAYLOAD
    assert disk.get("unrelated") == "retain"


def test_raw_writer_never_fabricates_timestamp(disk):
    asyncio.run(cache.disk_set(URL, PAYLOAD))
    assert asyncio.run(cache.disk_get(URL)) == PAYLOAD
    assert asyncio.run(cache.disk_get(URL, with_provenance=True)) is None


@pytest.mark.parametrize("record", [
    {"version": 2, "payload": PAYLOAD, "retrieved_at": STAMP.isoformat()},
    {"version": 1, "payload": PAYLOAD, "retrieved_at": "not-a-time"},
    {"version": 1, "payload": PAYLOAD, "retrieved_at": "2024-01-01T00:00:00"},
    {"version": 1, "retrieved_at": STAMP.isoformat()},
    PAYLOAD,
])
def test_unknown_or_invalid_record_is_a_provenance_miss(disk, record):
    disk.set(("fred-acquisition", 1, cache.redact(URL)), record)
    assert asyncio.run(cache.disk_get(URL, with_provenance=True)) is None


def test_versioned_cache_key_omits_credentials_and_retains_endpoint_ttl(disk):
    asyncio.run(cache.disk_set(URL, FredAcquisition(PAYLOAD, STAMP, "network")))
    key, = disk.iterkeys()
    assert "fixture" not in str(key)
    assert "__redacted__" in str(key)
    _, expires = disk.get(key, expire_time=True)
    import time
    assert 0 < expires - time.time() <= cache.ttl_for(URL)


def test_disk_disabled_does_not_open_or_write_cache(monkeypatch):
    monkeypatch.setenv("OPENBB_FRED_DISK_CACHE", "0")
    monkeypatch.setattr(cache, "cache_directory", lambda: pytest.fail("disk opened"))
    asyncio.run(cache.disk_set(URL, FredAcquisition(PAYLOAD, STAMP, "network")))
    assert asyncio.run(cache.disk_get(URL, with_provenance=True)) is None
    assert asyncio.run(cache.disk_get(URL)) is None


@pytest.mark.parametrize("state", ["network", "memory", "disk", "coalesced"])
def test_acquisition_normalizes_aware_timestamps_without_changing_instant(state):
    other_zone = STAMP.astimezone(timezone(timedelta(hours=2)))
    result = FredAcquisition(PAYLOAD, other_zone, state)
    assert result.retrieved_at == STAMP
    assert result.retrieved_at.tzinfo is timezone.utc


@pytest.mark.parametrize("stamp,state", [(STAMP.replace(tzinfo=None), "network"), (STAMP, "unknown")])
def test_acquisition_rejects_unknown_time_or_state(stamp, state):
    with pytest.raises(ValueError):
        FredAcquisition(PAYLOAD, stamp, state)
