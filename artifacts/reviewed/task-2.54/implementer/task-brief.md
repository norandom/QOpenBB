# Background task brief

Implement a controlled Background subsection with the original toggle and Color field. The caller owns `visible` and `fill`; exact discriminated edits report changes without mutating caller values. Hiding Color retains the fill, including alpha. Mounting and opening the picker emit nothing. Invalid color drafts remain correctable through the accepted shared color control.

Requirements 4.8, 4.9, 10.1, 10.4, 10.5 and 10.6 apply to this component scope. The frozen contract is in `chart-background-tooltip-design.md`, Contracts and ownership. Reuse CaptionColorInput, DS Switch and Titles CSS without changes; no opacity field, flags, dependencies, renderer or storage activation.

Focused component tests precede production implementation. Validation uses existing Vitest, Biome, scoped TypeScript and isolated Vite/Playwright/CDP tooling. Report known upstream compiler failures separately. The production module must stay within 400 physical lines, 300 logical units and 50 units per function. Controller owns inventory, breadth, combined dock composition and commits.

The referenced original Chart Style PNG was viewed before implementation. It shows Padding in the visible scrolled viewport; Background is below that viewport. The existing JSON/source references in the design establish the Background contract. Core product.md, tech.md and structure.md steering files are absent; the requested task-specific steering is present and was read.
