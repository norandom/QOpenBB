# Exact retention ACL correction review

## Review Verdict
- VERDICT: APPROVED for the single fixed-leaf ACL-only action; application and post-correction content verification remain controller/reviewer follow-up.

Independently recomputed helper SHA256d74742f25192da73fe3cd9df262e1cc86be8539d163b8f6b27d26bb60fa99ca7 and inspected complete helper/plan. Fixed target is runtime-capture-check/session/research-retention.json; explicit apply/hash, isolated cwd and unused private receipt directory are mandatory. No alternate path argument or recursive mutation exists.

The strict owner-only session root pins ancestors. The leaf is opened exclusively with READ_CONTROL|WRITE_DAC, without data-read or data-write rights; identity checks reject reparse/directory/multiple-link objects. Eligibility requires current owner,8578bytes and the reviewed three-explicit-ACE pattern. The private before receipt is created and flushed before mutation. SetSecurityInfo receives only protected-DACL information, on the same handle, using the existing current-owner-only Protection descriptor; owner/SACL/payload are not rewritten. Strict post-policy and same file identity/size/mtime/attributes/owner are verified before private after/success receipts. Failure cannot claim success or restore broader access.

Independently ran all5 mock-only tests: PASS, exit0. Tests exercise metadata/ACL refusals, receipt-before-mutation order, strict after verification and unchanged identity/mtime, and absence of payload I/O rights/calls. No checkpoint access or real permission mutation occurred in those tests or this review. Whole-helper metrics134physical/101logical/maxfunction23 satisfy caps.

The action is an evidence-security correction, not retroactive proof that the original DACL was private. Preserve original ACL metadata and historical exposure qualification. After controller application, use the unchanged strict reader to validate checkpoint scope/state and record its hash. A successful same-handle ACL-only correction plus content agreement does not require repeating provider work. Future direct-write prevention remains a separate scoped change; this helper does not weaken readers or alter frozen runtime inputs.

## Applied correction and secure content review

- VERDICT: APPROVED for closure of the checkpoint permission and content-review gate.

Independently read before.json, after.json and result.json with the unchanged strict private reader. The file identity,8578-byte size, modification time, attributes, link count and owner agree exactly before/after. The former unprotected three-ACE DACL became a protected single explicit current-owner full-access ACE. The reviewed helper had no payload-read/write rights; success receipt reports no payload read or rewrite. The checkpoint is now accepted by the original strict reader without substitution or relaxed policy.

Checkpoint SHA256:461b310e8437a82a8a309502e77c07b7ed88780a2517a42c109001066a4a1557. Secure content checks passed for initial-complete stage, both exact accepted image digests, runtime name, nonempty original Workspace container distinct from the reopened Workspace container, six unique widgets and matching layout identities, five current-source AAPL selections, profile acquisition matching selected evidence, shared symbol/statement-period groups, quarter/limit3, Jan03–Jan30 price dates, ungrouped native peer widget, and ordered ORCL/MSFT rationales. The already-passed retained browser phase asserts exact full state equality to this checkpoint as well as current data. API process/handoff container IDs are a different service and must not be equated to the checkpoint's Workspace container ID.

Private receipt SHA256s: before233ca6ec29307106c72a4a41faef2a78b6f8007d691fad1aec8a76463c428e54; afteref5675bc837fdbfc6c280e82fff58f427fdd78029f50b595ac0f040110758bf3; resulteb361419e96c678a814ac86cfbcc28fbed42d6fd01fdf8e0f315edc4837126af.

The original additional-principal read/execute grant remains a historical exposure qualification. No pre-correction payload hash was obtained because that would have bypassed the rejected privacy policy; non-rewrite evidence is the reviewed rights-limited same-handle action and preserved metadata, not a claimed before/after byte-hash comparison. No provider or financial rerun was needed or performed. Future writer prevention and final publication review remain separate.

Binding limit: accepted-initial records image digests and session identity; the handoff/process container is the API service. No independent preserved initial Workspace inventory snapshot was established. Initial Workspace identity provenance therefore rests on the executed browser's runtime-context-to-checkpoint write and successful reopen inequality assertion, corroborated by the current reopened descriptor; it is not an independent initial container inventory receipt.
