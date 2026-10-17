# F1 is closed for the two frozen Python files

Preliminary decision: APPROVED for F1 source remediation only. The joined source review, F2/F3 closure, publication gate and runtime grant remain pending. No other revised files were inspected in this staged review.

Reviewed on 2026-10-17: revised relay SHA-256 `ab893aa22478d28c0ae0fd596543086a3d0b757da469cd5c08fcfb2a63a408cf` and test source `e05cbfce89628773dc853fd0f5634079cad5fecf2db66a5d9a18fbee6c2c7144`. The [original finding](../ui-parity-legend-fixed-relay-review/review.md) remains unchanged. Its baseline relay hash is `273a5c95ab976024ee6bd0c004a7cf8c9a3684cfddc437d2333f1e3823f44f0b`.

The revised `read` returns without calling recv when buffer capacity is zero. `transfer` catches a would-block or interrupted operation inside the I/O block and then refreshes selector interests, so a preceding successful read cannot leave the former read mask active. The read/transfer changes preserve the existing limit and error branches. An AST comparison confirms every other module/class member is unchanged, including target admission, pair/socket limits, byte counters, deadline logic and half-close logic.

Fresh verification passed all ten supplied Python unittest methods. Running the added combined READ|WRITE regression against the original relay produces two expected assertion failures, one for BlockingIOError and one for InterruptedError; the revised relay passes both. Four independent cases exercise both directions with both exceptions. Each forwards all 65,545 bytes, makes no zero-capacity receive, delays half-close until genuine EOF, closes the pair and records zero violations. The socket factory is replaced with a rejecting stub during the independent audit; only injected fake sockets are used.

The [audit](f1-audit.py) checks exact input hashes before and after, records baseline failure/revised success, compares unchanged AST members and checks the original caps. The [receipt](f1-verification.json) contains the results. Both this audit and the supplied Python suite exited 0; baseline assertion failures are the intentional negative-control result.

```powershell
py -3 -B artifacts/ui-parity-legend-fixed-relay-revision-review/f1-audit.py
```

No Docker command, image interpreter, real socket, browser, build, install or production modification occurred. This is staged research evidence, excluded from production complexity caps. Future maintained code retains the scope inventory/checker and 400 physical lines/file, 300 logical units/file and 50/function. Final freezing waits for the controller's joined manifest.
