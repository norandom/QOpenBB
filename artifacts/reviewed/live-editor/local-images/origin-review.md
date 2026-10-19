# Static asset origin repair review

APPROVED for task 2.94. Missing `/assets/` requests now return an explicit 404 instead of executing the SPA document as JavaScript. The controller may commit the repair and rebuild the identified image; task 2.91 still requires a passing packaged browser check.

- Independently inspected the frozen changes in `vendor/workspace/lite/nginx.conf.template` and `tests/delivery/test_origin_routing.py`. The production diff adds only the dedicated static asset location and its rationale comment. Existing SPA fallback, API, external route include and proxy configuration are unchanged.
- Independent command on 2026-10-19: `wsl -d Debian -u mc -- bash -lc 'cd /mnt/d/Source/QOpenBB && /home/mc/qopenbb-work/sqlite-runtime/venv/bin/python -m pytest tests/delivery/test_origin_routing.py -q'` exited 0: **7 passed in 9.18s**. Tests execute real pinned nginx, not a string-only configuration check.
- Regression assertions verify the actual missing datafeed path returns 404 without SPA bytes, an existing asset returns its exact contents with 200, and a deep application route still returns the SPA. Existing API prefix handling, data routing, redirect, unavailable-agent and available-agent streaming assertions remain active.
- RED evidence verified in `origin-routing-red.txt`: both parameterized nginx cases failed because the missing asset returned 200. Worker GREEN records seven passing checks. Scoped whitespace checks pass in both repositories. The production template is **64 physical lines**, within the 400-line cap; logical/function caps do not apply to nginx configuration.
- Boundary audit: clean. No diagnostic allowlist, feature flag, application script, PWA, dependency or Dagger change. No new placeholder or concrete credential in the diff. No blocking findings or mandatory remediation.

Rebuild and verify the ordinary packaged frontend before claiming its JavaScript exception is resolved. This review approves the routing repair only, with no release, live-provider, Anthropic, Excel or deployment acceptance.
