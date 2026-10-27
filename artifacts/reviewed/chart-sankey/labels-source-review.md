# Sankey label correction and browser preparation

Source correction accepted on 2026-10-27 at Workspace `31fb64c`; browser-test preparation is committed at `e12713d29a9572599c7482d293f37cc040eba12f`. An independent review passed all 18 native-renderer tests and read-only lint, with no blocking findings. The one-line renderer change keeps terminal labels inside the plot; source and intermediate labels retain their placement. Native SVG regressions reproduce the original clipping and verify recovery at 360px and 640px. The combined size gate passes at 275 physical lines, 110 logical units and 26 maximum function units.

The first packaged image (`8ebec7900c95608de692053e5fa14e07f6093a7090fb3349ead910e64f131085`) exposed that clipping. Its second browser run verified the retained FMP values in both themes, mapping recovery, filtered imbalance warnings, filter restoration, refresh and PNG export, with clean browser diagnostic arrays. It then stopped at a test assertion that looked for the saved range inside chartModel instead of the existing Sankey storage partition. That assertion and an earlier warning-text selector are corrected; failed runs remain in local evidence.

The updated image, complete save/fresh-reopen journey and owner appearance are not yet accepted. No updated alpha has been published. The example remains a derived AAPL FY2025 income allocation in USD, not cash flows or provider-supplied links.

Independent source review SHA256: `55f36fb57471995a19411f44576011b72c7570c59ea5d2b2ffafdf8b7ead6371`.
