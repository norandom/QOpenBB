# FMP statement provenance integration accepted

Task 3 accepted on 2026-11-10 at API commit `e78d87b2000`, following core `b373da3f8d7`. Annual/quarter Income, Balance and Cash now carry source facts and original ordinals through their existing ordering and clipping. Unsupported flow duration remains unknown. Balance/closing cash retain instant dates; beginning cash remains undated. Other Income query selectors retain baseline behavior.

RED: nine failed/six passed because the sidecar was absent. GREEN and independent review: **102 passed**, exit 0. Seven changed FMP files and both frozen core files match installed packages. Actual source facts, alias precedence/conflicts, null versus absence, duplicate ordinals, unfamiliar labels, normalized dates and safe errors are covered. No live requests or image acceptance is claimed here.

The combined clean inventory gate passed **110 files**, zero errors/violations. Initial gate identified a missing include-pattern entry for the new helper; the clean proposal now registers the exact helper path in both ownership selection and maintained files. No size limit or exception was relaxed. Largest modified data model is 363 physical lines; all modified production files pass 400/300/50.

[Independent review](provider-review.md) records one non-blocking internal-call observation: deliberately constructing an invalid acquisition can cause TypeError before validation, but actual routes reject non-dictionary rows in their acquisition helper. No broader malformed-input guarantee is claimed. Source/live integration, packaged widgets and publication remain tasks 5-7; IA-B remains open.
