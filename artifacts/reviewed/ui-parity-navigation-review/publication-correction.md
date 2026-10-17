# Add the omitted navigation action ledger

The published report linked `run-20261017-r1-a4/action-ledger.json`, but the frozen 158-file capture allowlist omitted that file. The independent hash audit correctly verified the selected files; it did not prove that every report link was included. The reviewer's subsequent message that the source allowlist included the ledger was incorrect. A fresh published-report check found 37 links with this single missing target.

The original ledger was inspected directly: 46 entries contain only synthetic case IDs, action labels, the real-UI classification and elapsed milliseconds. It contains no credentials, owner data, runtime metadata or account identifiers. Its recorded actions agree with the reviewed harness and navigation checkpoints. Approve this existing file for additive publication through [the supplemental allowlist](supplemental-publication-allowlist.json), together with this correction receipt. The frozen report, raw evidence and original manifests remain unchanged.

This corrects publication completeness only; it does not change the observed navigation conclusions or grant candidate/implementation acceptance. The controller must recheck all published links and the supplemental hashes after copying the files. The supplemental manifest excludes its own hash to avoid recursion.
