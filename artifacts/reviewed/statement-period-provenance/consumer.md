# Statement consumer contract accepted

Task 4 accepted on 2026-11-10. The existing financial OpenAPI projection supports the typed statement extension without production changes. Controlled fixtures establish Python/native HTTP metadata equivalence, duplicate attribution, zero/null preservation, safe malformed-evidence rejection and complete schema references. FRED and unrelated Enterprise responses omit the absent member.

Independent review ran both affected consumer test files after the FMP package refresh: **81 passed**, exit 0. Earlier worker runs passed 33 and 27 selected checks. An initial fixture expected explicit null revenue to disappear; the expectation was corrected to preserve existing Income behavior. This was not a production RED failure.

This accepts consumer compatibility against controlled fixtures, not the task-5 source/live matrix or published images. The strict-client migration draft remains bound to the final joined core/provider revision at task 5. Old strict validators reject the new member; no backward-compatibility claim is made for them. Tests/docs changed only; production size caps are not applicable. See [independent review](consumer-review.md).
