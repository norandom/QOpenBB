# Keep the reserve until failure metadata has a finite proof

No smaller reservation is selected. The proposed 26,624-byte sum is arithmetically correct for its declared components, and it closes the synthetic 72-Tab mock. It is not a finite bound for every append path in the accepted source: case-level and outer exception handlers retain uncapped error text outside the capped input ledger. The nominal 2,048-byte scaffold is an assumption, not enforcement. Keep the source's 32,768-byte reservation unchanged pending a separately scoped proof and independent review.

This source-only analysis is dated 2026-10-17. The [R01 correction](../ui-parity-tooltip-segment-keyboard-revised/plan.md) and its [independent acceptance](../ui-parity-tooltip-segment-keyboard-revision-review/review.md) remain separate and unchanged. This is no new tooltip diagnosis, collector edit, runtime grant or UI-parity acceptance. Only `artifacts/ui-parity-tooltip-reservation-analysis/` is written. The accepted fixture, eight cases, 396 actions, 96 probes, 48 PNGs, all time/serialization caps, 115,072-byte guard and 131,072-byte case ceiling remain unchanged.

## What the arithmetic does and does not cover

The declared candidate is `14336 invocation + 6144 ledger entry + 2048 baseline + 2*1024 control receipts + 2048 scaffold = 26624` serialized UTF-8 JSON bytes. It is 6,144 bytes below the accepted 32,768-byte reservation. Examining that arithmetic is not an increase to any retained-byte or input budget. The calculator substitutes the candidate only in an isolated VM's reservation callback; it does not change, copy over or run the collector.

The actual reservation is checked before T06 action counters/started receipts/input, and before keyboard probe counters. A full finite interval proof must cover all additions until the next check or case close, including paths that throw instead of completing an invocation. This inventory is exhaustive by the source's T06 state writers; its final columns distinguish checked component bounds from unfinished interval bounds.

| Append or mutation path | Existing enforcement | Consequence for the candidate proof |
| --- | --- | --- |
| New case constants, `actions`, ledger arrays and keyboard arrays | Fixed contract/case schema; action cap 120 | Initial case bytes are measured at reservation. Later counter digits, new array commas and property punctuation still need an explicit interval derivation. |
| Started input entry, then status/time/event counters and `after` or `reason` mutations | `casePrewrite` checks ledger entries; `boundedEntry` checks completed entry at 6,144 bytes | Completed entries are bounded including failed receipts and JSON escaping. A larger in-memory failed entry can be rejected, leaving a previously persisted started prefix. This is a stop, not proof that every failure receipt fits. |
| Ledger `after` active/visible tooltip/live status | Projection 4,096 bytes and field/array/finite caps; entry cap also applies | Character maxima alone are insufficient. Actual serialization includes multibyte text, control-character escapes, keys, quotes and punctuation before the byte cap accepts it. |
| Series control receipts before/after an optional expansion input | Each receipt checked at 1,024 bytes before push | Two full receipt objects are budgeted; their array commas and first property key belong in the interval scaffold. Each setup input rechecks the reserve. |
| New mode object, its baseline and status/image names | Baseline checked at 2,048 bytes; exact source strings/modes bounded; baseline changes stop | The baseline object is bounded before assignment. The wrapper key, new mode object, array comma, status replacement and terminal/initial image fields need their own finite overhead derivation. A sample failure can occur after a new baseline was assigned. |
| Tab/arrow invocation push | Whole invocation checked at 14,336 bytes before push | Includes before sample, both actual settled members, counts/times, key/image fields. The enclosing array comma remains outside the cap. R01's actual final failure pair is unchanged. |
| Mode end, screenshots, later mode creation before another input | Fixed mode/status/image naming; screenshot count cap | These changes occur after a prior input's reserve. They are finite on successful source paths, but no executable 2,048-byte combined scaffold cap exists. Screenshot errors flow to the uncapped case reason. |
| Case catch `status`, `reason`, `remainingProbes`, `remainingModes` | Fixed statuses/mode list; **no `reason` cap** | `String(e.message).split('\n')[0]` can exceed either reserve. T06 `remainingProbes` is empty; remaining modes are finite. Bounded ledger error text does not bound an observation/locator/screenshot/transport exception caught here. |
| Outer catch overwriting `current.reason` and attempting persist | Credential replacement but **no length/byte cap** | It can also retain unbounded sanitized text. It does not provide a finite replacement for the failed interval proof. |
| Final `{events,elapsedMs}` tail | Whole object checked at 16,000 bytes before assignment | This has a separate reserve: `131072-115072=16000`. For disjoint keys in a nonempty JSON object, merge growth is `tailBytes-1`, so a legal tail fits if all preceding growth really remained within the case guard. A tail accepted by this retention API is not proof that the synthetic event sequence can be emitted by the browser. |
| Final `json()` persistence and aggregate accounting | Hard case, ledger/invocation/baseline checks; aggregate JSON/run-byte checks with overwrite accounting | These reject excessive output and preserve the previous file on checked failure. They do not prove that the missing final record or failure metadata fits the prospective allowance. Filesystem crash atomicity is outside this arithmetic. |

All object serialization uses the actual `Buffer.byteLength(JSON.stringify(value))` rule. Keys, quotes, array separators, Unicode bytes and JSON escapes are included in component caps. Finite projection numbers are also checked. Unbounded exception text remains unbounded after UTF-8/JSON encoding; more generous average text assumptions cannot close that path. Case and outer reasons are not part of the 16,000-byte final-tail object. Global JSON/run-byte reserve is a separate writer contract and is not available as extra case headroom.

## Actual extracted mock, with unchanged caps

The calculator reuses the actual extracted `input()` and `keyboard()` functions and actual R01-corrected `observe()` source with a controlled clock. It supplies one retained DOM sample, synthetic Mode/Escape and Escape popup actions, and mock screenshots/persistence. It omits real browser controls and does not reproduce full case setup. The failure catch tests supply the ordinary empty `probes` array required by the actual case schema; the historical traversal mock omits that field to reproduce its prior byte count exactly.

| Allowance examined in VM only | Tabs by mode | Actions / probes | Current case bytes | Case plus allowance | Result |
| --- | --- | --- | --- | --- | --- |
| Accepted 32,768 | 24 / 24 / 22 | 76 / 94 | 82,395 | 115,163 | Stops `not-run-budget`, 91 bytes above guard; Compact still seeking. |
| Hypothetical 26,624 | 24 / 24 / 24 | 78 / 96 | 84,701 | 111,325 | Completes this fixed mock, with 3,747 bytes below guard. |

No real 72-Tab coverage follows. Larger names, visible tooltip values, events, full setup actions, failures and other permitted states differ from this mock. Conditional arrows remain inside the same shared probe/image caps. The accepted source still stops at 70 in the historical mock because its reserve is unchanged.

## Counterexamples to the total append claim

The [offline receipt](verification.json) records 27 passing assertions, including successful reproductions of these limitations. Passing those assertions does not approve the smaller reserve.

1. **Failed input metadata repeats outside the ledger.** The actual extracted input function emits one action and retains a 6,132-byte failed entry for a synthetic 6,000-character error. The actual case catch then also stores the 6,000-character message in `current.reason`, outside that bounded entry. This refutes the proposed 2,048-byte scaffold as a universal metadata allowance. It does not alone prove that the full 26,624 sum is exceeded, because a failed input may omit other components.
2. **A post-input observation exception has no finite component cap.** The actual extracted T06 path receives an injected 40,000-character exception after a counted input. Its case catch grows by more than either proposed or accepted reserve. This is a synthetic fault input to actual source; it does not claim that a particular browser/Playwright version emits such a message.
3. **Late error plus a tail accepted by the retention API exceeds the hard ceiling.** Under the hypothetical callback, 70 Tabs are retained and the 71st Tab is emitted before its observation throws. There are 77 actions and 95 global probes. The case is 82,763 bytes before the catch and 122,850 after it. A separately accepted 16,000-byte tail brings it to 138,849, and the unchanged hard case prewrite rejects it. The source's rejection is correct; the candidate did not reserve the claimed complete closing record. The tail is an admissible API-shape fixture, not a claim of runtime event reachability.
4. **A pure byte-boundary construction isolates the arithmetic.** A synthetic case with padding is exactly `115072-26624=88448` bytes. The actual catch adds 27,823 bytes for a 27,624-character message plus metadata, reaching 116,271 before the tail and 132,270 after a legal 16,000-byte tail. This constructed padded state is not a reachable browser-case assertion; it shows why guard arithmetic plus the current writer contract cannot prove the universal bound.

The same unbounded-error issue can exceed 32,768 as well. This report does not claim that the accepted larger reserve already guarantees complete retention of arbitrary failures, or that R01 introduced this gap. R01 closed the independently reviewed pair-retention defect. The present question is whether a smaller finite allowance has a sufficient proof; it does not.

## Conditions for a later proposal

Before choosing a smaller reserve, define and enforce a finite policy for case-level and outer failure text, including errors outside `input()`. Specify whether excessive text causes a bounded unresolved record, a separately bounded diagnostic, or rejection preserving a truthful started prefix. Do not silently truncate identity or financial tooltip content. Derive key/comma/counter/mode/status/image/remaining-mode overhead from the exact source, across successful, after-input-failed, baseline-failed and finalization paths. Replace the nominal scaffold assumption with that derivation or an explicit bound. Keep the final 16,000-byte tail and global writer checks separate.

A disproof condition for any later candidate is an accepted source state whose additions before the next reservation/close exceed the proposed finite amount, or a permitted terminal record that cannot fit the unchanged hard ceiling despite all declared component caps. Review must challenge every append path and distinguish API-admissible synthetic states from demonstrated runtime-reachable states. This package supplies a refutation of the current proof, not an implementation of those future policies.

Independent review is required before any arithmetic is adopted in collector code. Runtime traffic-denial/lifecycle prerequisites, full keyboard reachability, T05, T04, actual picked identity and UI parity remain open. No lifecycle/network rewrite, private picked-state inspection, fixture change, production/root-document change, Git action or automatic run is authorized by this analysis.

## Reproduction and publication

From the repository root:

```powershell
node artifacts/ui-parity-tooltip-reservation-analysis/calculate.mjs
node artifacts/ui-parity-tooltip-reservation-analysis/freeze-check.mjs
```

The [calculator](calculate.mjs) reads frozen named source/data inputs and writes only this package's deterministic verification receipt. It launches no application, browser, container, subprocess build, dependency installation or network request. [Source hashes](source-hashes.json) pin the accepted source, independent R01 review and inspected inputs. The [publication allowlist](publication-allowlist.json) uses sourcePath/hash/bytes and includes only this bounded text analysis, calculator, freeze checker, manifest and receipt. It excludes credentials, private state, runtime traces/logs, dependency contents and images. Its metadata is copied separately without a self-hash. Publication is pending independent review and does not approve a collector change; verify destination hashes and links after any approved copy.

The owning specification language is English. Previously read testing, delegation, documentation and complexity steering applies. `kiro-verify-completion` limits the claim to fresh source/offline arithmetic and successful counterexample reproduction. The research package is excluded from production caps; future maintained adoption retains the executable inventory/checker foundation, 400 physical lines/file, 300 logical units/file, 50 logical units/function and final shared-module audit. No source reserve was reduced.
