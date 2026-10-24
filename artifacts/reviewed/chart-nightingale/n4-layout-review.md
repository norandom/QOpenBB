# Nightingale layout refinement review

- VERDICT: APPROVED
- TASK: bounded N4 production layout correction, 2026-10-24. Source review only; rebuilt visual parity remains unverified.
- Frozen files: nightingaleLayout.ts SHA256 `342ac7f4f9fa965ced10b6958b41c627e6e0702d37ba7e11631ef485775fa2dd`; nightingaleMapping.test.ts SHA256 `cd546aba6e017dea6e5b9cff61fd352fe8da244db93023ce8d387ffd4c786794`. Fresh hashes match.

## Mechanical results

- Fresh independent focused Vitest run: exit 0, 11 tests in nightingaleMapping.test.ts and nightingaleEngine.test.ts; pinned Node 24.22.0, existing chart-compatibility config, --maxWorkers=1. No broad suite, browser or build.
- Retained scoped Biome lint: exit 0, two files. Strict TypeScript: four inherited typography/Zod diagnostics retained; no clean compile claimed.
- Complexity evidence: 205 physical lines, 49 logical units, maximum 12/function, within 400/300/50. Parent combined inventory gate remains required.
- Placeholder/credential scan: CLEAN. Boundary and dependency audit: WITHIN the layout owner and focused regression; no alternate state or financial calculation owner.
- RED evidence: prechange original-run-2 and candidate-run-2 light PNGs inspected directly. They show the target defect: candidate numeric labels lie on the diagonal band boundary and extra spokes/circles cross the drawing. This is observed visual defect evidence, not a failing automated RED test.

## Findings

1. No blocking production finding. The new graphic radial labels use the same native min/max/ticks and inner/outer radii as the bars. Signed values map through the complete domain, normalized ticks retain the separate radial formatter, and a degenerate extent avoids division by zero. Raw series values, missing observations, stacking, selection and tooltip owners are unchanged. Focused native tests still cover signed/missing, zero, grouped and one-category behavior.
2. The original screenshot supports an outer category circle, top-ray numerical labels and no internal radial circles/spokes. Retaining the native outer axis preserves its color/thickness control. Category orientation remains independent; label font/color still follow Polar Axis. Center/radius and spacing changes are plausible corrections, but only rebuilt matched captures can establish actual parity. In particular, the old screenshots show different legend spacing; no claim of complete legend appearance parity follows from this source review.
3. Integration requirement for the N4 test owner: the former assertion changed.lines.some(width === 3) is incompatible with intentionally removed straight spokes/radius lines. The surviving axis is a full-circle native outline centered with the sectors at the maximum polar radius. Existing pie-observer Drawing.outlines is Arc[] with x/y/radius/start/end/anticlockwise only; it does not retain stroke width, unlike Drawing.lines and sectors. Do not assert an unavailable outline width or reintroduce spokes to satisfy the old test. A bounded test can isolate Thickness alone, preserve outer-circle geometry and compare a stable public-canvas crop across a clear outer-ring point; a direct stroke-width observation would require an explicit observer scope amendment. Existing SVG engine tests render native output but do not independently assert axis stroke width.

REMEDIATION: None within this production source review. Adapt the affected browser thickness observation before treating rebuilt N4 execution as an acceptance gate; retain the separate parent combined inventory check and rebuilt financial/appearance verification.

Summary: the layout correction is bounded, numerically consistent and supported by fresh focused checks; packaged visual acceptance remains the next gate.
