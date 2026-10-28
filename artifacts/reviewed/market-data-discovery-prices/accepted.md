# FMP discovery and daily-price acceptance

Tasks 2.5 and 2.6 source-accepted 2026-10-28 after independent financial review. Discovery source commit39f504c0c452903e684122699497eb79606c108e; daily price source commit1907741737d7d2d71f4fa3534610857da56674f7.

Independent focused verification: 68 passed in 13.29 seconds, exit0 (37 discovery/peer tests and 31 daily tests). Owning FMP Ruff passes allfour production files. Combined Node 24.22.1 scope/size gate: 78 files, no errors or violations. final-source.json records frozen hashes and whole-file measurements; each meets 400/300/50 caps.

Name and symbol searches preserve alternative listings, exchange/currency and supplied issuer/security attributes without inferring issuer equivalence. Provider peers remain suggestions, not an analyst-approved peer universe. Search and peer bounds default 20 and allow strict integer 1..100. Metadata preserves receipt timestamps, observed clipping and unknown completeness.

Daily history requires explicit ordered dates within five calendar years, daily interval and the supported split-adjusted endpoint convention. It preserves zero/null values, source payloads and stable duplicate order, rejects unsupported adjustment/intraday modes, and discloses the 5000-row cap. Percent conversion to fraction is an explicit local transformation; price fields use currency/share. Missing dates are not filled, and unavailable currency/corporate-action details remain explicit.

Actual preimplementation missing-module RED was captured in both lanes. Earlier shell wrappers printed failed pytest output but returned 0; the reports identify that limitation rather than claim a pass. Frozen GREEN output and independent verification establish current behavior. A transient Windows launcher failure was retried with an owned hidden process; it was not a pytest failure or WSL outage.

No live provider account, subscription, installed-route/widget, image build or publication acceptance is claimed. Registration remains its own later task. This batch supplies data adapters; the separate house-modeling layer remains queued.
