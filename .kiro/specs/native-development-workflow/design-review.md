# Native workflow design review

## Summary

APPROVED for owner design review and subsequent task generation. The repaired design maps all approved requirements to bounded components and preserves meaningful financial assertions, isolated browsers, external artifacts and owned cleanup. Native runtime qualification remains implementation work.

Reviewed revision: `D:/BuildArtifacts/QOpenBB/native-validation/design-draft.md`, SHA256 `f6e593b6b70466ef5bc75fe83960acca698d82fd4564deafb9a33a1aa07bc9f7`, on 2026-11-10. Requirements approval is recorded in spec.json; design metadata is intentionally ungenerated during draft review. Core steering files `product.md`, `tech.md` and `structure.md` are absent; applicable CI, testing, complexity, delegation and documentation policies were inspected instead.

## Critical issues

None remain after bounded repair review.

1. Native executable selection is now explicit. The selected real Podman executable and real Compose provider replace profile functions and command wrappers, with argv arrays and preserved provider configuration. Existing image load/catalog/packaging helpers share the adapter. The pinned Dagger executable bypasses the global wrapper and must qualify the selected Podman container transport before export. This resolves requirements 1.1, 1.2 and 4.1 at design level; it does not prove that qualification will pass.
2. Private browser descriptor reads now use one captured-pipe Python bridge with the same handle, ACL and schema validation. Both root financial checks and the owned-fork login fixture consume the checked object without reopening its path. Missing reader configuration fails closed. The exact test-only fork change and controlled source-pin promotion are allocated. This resolves the requirements 5.4/5.5 gap found at `financial-workspace.spec.mts:151,512` and the shared login fixture's direct JSON read.

## Strengths

- Exact immutable image/resource identities, prepared lifecycle state and fail-closed cleanup preserve session ownership. Windows ACL protection, mount translation verification and preserved state do not rely on name prefixes or broad deletion.
- Existing application journeys, financial assertions and login budgets remain authoritative. Native, pinned-build and Linux compatibility claims require real evidence. Historical WSL results and mocks cannot establish acceptance. External storage, Dagger-only builds and the existing 400/300/50 checker remain explicit.

## Final assessment

**APPROVED / GO.** No unresolved design blocker remains. Carry the checked-reader failure cases, actual Compose-provider execution, pinned Dagger transport qualification, native image-load output compatibility and Linux consumer behavior into bounded implementation acceptance. Validate private IPC failures without echoing captured credentials or process-error payloads. The design already requires fail-closed behavior; these are concrete evidence obligations, not further scope.

No runtime execution, installation, provider calls or runtime/spec edits were performed by this reviewer. Only this external report was written. Technical approval does not substitute for owner design approval or implementation approval.
