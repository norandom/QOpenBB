# Correct write outcomes and first-failure retention

This revision preserves the original proposal and changes only two failure-evidence contracts. It remains a source-only plan, with no implementation, reservation reduction or runtime grant.

1. `caseWrite` gains `write-unverified`. Only a proven prewrite rejection may claim the prior prefix is preserved. A filesystem write can modify or truncate the target before throwing; the plan makes no atomicity or rollback claim and requires this fault in later offline tests.
2. The standalone failure receipt carries at most one existing bounded `firstCaseFailure` object when available, as well as its bounded outer metadata. This covers a first case reason that exists only in memory when the complete case write rejects. The optional wrapper is counted separately, and persistence is claimed only after a successful containing write.

The proposed 512-byte per-object metadata ceiling, two-object limit, financial/tooltip values, action truth, independent final-tail accounting and existing 32,768/115,072/16,000/131,072-byte constants are unchanged. The revised proof obligations cover partial writes, failed standalone receipt writes and preservation of the first metadata without a recursive fallback chain. No complete scaffold proof is claimed.
