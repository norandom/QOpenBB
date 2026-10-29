# Authoritative financial schema projection accepted

All 11 financial annotation repair tasks and main task 4.1 are accepted on 2026-10-29. The market-data first batch is now **16/26 tasks accepted**. FMP profile, statements, discovery/peers, daily prices, metrics, ratios and enterprise inputs share class-owned financial declarations with the API projection; FRED declares dynamic quantity semantics resolved at runtime.

The final join verifies actual installed profile/income/FRED route associations and all eleven first-batch fetcher models in an isolated native registry. It also checks real transform-to-OBBject serialization, financial metadata placement, missing declarations, response modes, references, idempotence and preserved native schema components.

Native verification exposed one documentation defect: upstream success schemas use aliases while routes serialize canonical names. The projection now derives its namespaced envelope from the actual route response model. Provider output is unchanged; stale or unsupported typed envelopes fail explicitly. The [debug finding](debug.md) explains the correction.

Independent Astra verification passed 389 affected tests. After test-only lint cleanup, all eight final native cases and Ruff passed again. Production measures 236 physical lines, 151 logical units and 27 units in its largest function. The combined Node 24.22.1 root gate passed 75 maintained files; the separate whole-file audit passed all 27 shared/provider modules. Source locks match both exact fork revisions, and unrelated working changes were preserved.

See the [independent review](review.md), [final source identities](final-source.json) and [shared-module audit](shared-module-audit.json). This accepts the source component. Provider registration, policy/error handler installation, generation/runtime wiring, live-provider acceptance and image publication retain their later main tasks.
