# N4 independent acceptance review

- VERDICT: APPROVED
- TASK: packaged Nightingale behavior and appearance, 2026-10-24.
- Blocking findings: none. Owner accepted the displayed light comparison with "Keep this appearance", as recorded by the controller. This accepts the tested local candidate, not a published release image or remote deployment.

## Identity and mechanical evidence

Candidate source `596a5234f7dec5c672dd97b09e365bfb90aac755`, image/config `sha256:6edd63b48c0c265a18d8c06315a037691ab98d9fe332bfeac8efc7a850c60604`, loopback port 55564. Reviewed runtime-identity.json and verify_runtime.py bind the reported image/source to the actual container and sole disposable data mount. Original qualification is original-runtime.json: frontend `38dffc33389aca0e4a87e0e88d42f7067aa220df`, image `sha256:f48eb1c9b32e1f84d5199dafc943bc1fc10f3b1745ab29860975d002dc5c8a3f`, port 60307, disclosed backend-only overlay.

Both retained browser-results.json files and exit files pass: original-run-2, 29.6 seconds; candidate-run-4, 69.6 seconds total. Each runs one selected test with one worker, no retry, no skipped/flaky/unexpected test and exit 0. Current test hashes match the executed freeze: spec `32311f1a40ac6da9a589a697c7af92bed679e2192463d2a1b41eb78aaa512b80`; fixture `7007f1bb2c4eacf8ba8339e38307885a150b9a1497aae664a0f32bc03dae3dc5`. Previous scoped static reviews stand; no browser/build rerun was performed for this review.

## Financial and behavioral acceptance

Fresh hashes match retained raw FMP `390dc8cbfc8302720a203bd9782d5e3b1f7363a4f762bdfcef079dbbe4c72f6b`, CSV `2be4fd02d6aa89ae20b95614fa0d21413db18e75a1b75b3458d1ca9d1e7ca7d8`, and provenance `9a416706dfd7e821525d71786a7d09e9a36a3661b8cf2c444962964526c68896`. Four AAPL FY2025 Cost of revenue/Gross profit pairs reconcile exactly to revenue 124300000000, 95359000000, 94036000000 and 102466000000 USD. Revenue is not plotted as a third series. Tests verify fiscal dates/currency and exact CSV amounts before import; native tooltips show the expected rounded magnitude formatting, not full-dollar precision.

Decoded attachments confirm eight observations in light/dark stacked, grouped and normalized modes; four Cost observations after native legend hiding; eight unit counts after aggregation; and eight annular/oriented observations. Independent arithmetic rechecking of attached geometry agrees with the shared affine radius mapping. The count record's generic usd property contains counts, not currency; its mode and plain-number tooltip distinguish this correctly.

Passing assertions establish isolated Thickness crop change, observed Series stroke, nonzero inner-radius geometry and category text rotation. Save checks persist options; refresh verifies returned CSV and rechecks values. The final fresh context verifies backend saved-model equality, nonzero radius and all eight tooltips, then PNG pixel comparisons covering all eight sector bounds. Both candidate diagnostic gates require empty application/network/console failures. Refresh/reopen/export results are evidenced by the completed uncaught assertions and exported PNG; they are not separately attached model/diagnostic dumps.

## Appearance, publication and limits

Inspected all four original/candidate light/dark widget PNGs: financial chart/title only, no credentials, tokens or private account details. These four selected images are suitable for the reviewed mirror with provenance captions and manifest hashes. Raw results, state, descriptors and logs remain private.

Candidate canvas is 619 by 593 CSS pixels; original is 619 by 592, both DPR 1. Disclose the one-pixel height difference and remaining visible spacing differences; do not claim pixel identity. Original native tooltip identities are verified, but source-informed targets are not measured Path2D geometry. Original-run-2 retains one CSV request failure and corresponding console error; it is not clean transport acceptance. Prior failed runs remain diagnostic history. Owner approval resolves further light-view polishing; release publication and image-pull verification remain N5.
