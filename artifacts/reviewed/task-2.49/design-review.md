# Controls design review

PASS for the bounded implementation of tasks 2.49 and 2.50. No blocking contract defect found. This is design/task review, not implementation acceptance, visual parity, persistence or full Customize acceptance.

Reviewed on 2026-10-17: .kiro/specs/openbb-self-service/chart-editor-controls-design.md, SHA256 `1375E25FFF48C78765495979546E57C45E3AC9EA0D4CE54D93A14EAE6BD878C7`; tasks 2.49/2.50 in .kiro/specs/openbb-self-service/tasks.md; existing chart-caption-padding-findings.md and chart-color-shadow-findings.md in that spec directory. No new reference capture or research was performed.

The two production directories and focused tests/stories have disjoint owners. Both depend on accepted 2.48; the controller owns dock composition and shared metadata. Task 2.50's composition completion bullet is satisfied at that controller-owned join, not by granting the Titles worker ownership of the dock.

Set Up retains the observed category/aggregation controls, series chips and switch. Exact IDs, caller-controlled ordering/removal, retained hidden aggregation method and unknown menu values give implementers an executable UI contract without inventing storage or financial transformations. Pointer and keyboard reorder evidence remains required.

Titles keeps four independent caption states and the combined Weight menu. Opaque weight keys defer the observed ordered weight/style writes and absence distinctions to the future adapter. Caller choices preserve Verdana and unknown values. Alpha-capable color editing, invalid drafts, linked numeric controls and focus restoration are feasible with the specified existing dependencies; picker opening must not infer caption normalization from axis captures. These are implementation obligations, not tested results here.

The development preview must identify Customize as Titles only. No permission for renderer activation, flags, storage writes, provider calls or additional Customize groups follows from this pass. New or changed production files require the existing inventory and whole-file 400 physical / 300 logical / 50-function checks, focused verification and independent implementation review. The unchanged scoped DS TS2578 diagnostic may remain a documented baseline limitation; new diagnostics may not be attributed to it.

Applicable complexity, delegation, documentation, testing and CI steering was read. The default product.md, tech.md and structure.md steering files do not exist in this checkout; no policy was invented for them. No implementation tests were run for this document-only review.
