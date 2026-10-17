# Accept the pinned source explanation within its stated assumptions

VERDICT: APPROVED for source diagnosis and the exact selected publication set. No blocking interpretation or provenance defect was found. The pinned Moby branch supplies a mechanism for the observed null operational binding under the report's ordinary internal-only, default-NAT assumptions. This does not attest the local binary, prove every daemon setting or establish a working relay.

Reviewed on 2026-10-17 against [report.md](../ui-parity-internal-network-source-diagnosis/report.md), SHA-256 `452683d6236946992b34584a3ab1844e8f192e5ab0ab53b93962042d6ed77e62`; [source-hashes.json](../ui-parity-internal-network-source-diagnosis/source-hashes.json), `3b9009fc81f3a7eae88f9542622f59bff1a0ed296e4caaa6472a6439a406da41`; and the original publication wrapper, `f41eea03628a31488df4594d988b8e281447698fb867d8b9a26ffffaafc0d469`. The already reviewed [diagnostic evidence](../ui-parity-legend-startup-diagnostic-runtime-review/review.md) remains an independent finite observation. It was not rerun or retroactively changed into a causal measurement.

## The branch trace is complete for the stated topology

The report does not stop at the internal-network guard in daemon/network.go. That guard omits endpoint-specific port options, while container_operations.go still places configured published/exposed ports into sandbox options. Bridge Join parses those sandbox options. Thus the source explanation preserves the distinction between a configured request and operational allocation instead of incorrectly claiming the request disappeared.

Bridge Join omits gateway assignment for an internal network. needDefaultGW skips internal endpoints, so an internal-only sandbox does not gain a fallback gateway. Gateway selection examines gateway/default-route information, including forced-gateway flags. Under the report's explicit absence of forced gateways, default routes or another non-internal endpoint, both gateway endpoints are nil. epId converts them to empty IDs.

The endpoint's external-connectivity call still runs. In bridge ProgramExternalConnectivity, neither empty gateway ID selects the endpoint, so its IPv4/IPv6 requested flags remain false; the routed flag remains true. getNATDisabled reads routed gateway mode, not the network's Internal flag. With ordinary NAT mode, both NAT-disabled flags are false. The sortAndNormPBs expressions then make add4 and add6 false regardless of existing binding state. Neither address-family append executes, and addPortMappings has no request to allocate. The report's conclusion is therefore conditional on gateway mode and endpoint selection, not a universal claim about every possible internal network configuration.

EndpointOperInfo supplies exposed ports separately from actual mappings. getPortMapInfo initializes exposed entries to nil and appends only operational bindings. Container operations stores that map and inspect returns its copy. This supports the observed configured `127.0.0.1`/empty dynamic HostPort alongside operational `3000/tcp: null`. Waiting alone does not change these source predicates under unchanged assumptions. This source result does not prove that the local daemon has no patch or unobserved configuration difference.

The cited functions and line anchors were read directly in the frozen files, including their surrounding branches. The small Boolean checks are derived arithmetic, not compilation or execution of Moby. No Moby suite was necessary for this source-only interpretation, and no such suite is claimed.

## Provenance and proposed transport limits

The retained official tag ref resolves to annotated tag object `d681cdaead9340bd36c513c7f5413a21bc679cfa`, which resolves to full commit `6a43e3d5afddf4111da0f864bbc7cae5d7e95001`. Independent retrieval of that [official tag object](https://api.github.com/repos/moby/moby/git/tags/d681cdaead9340bd36c513c7f5413a21bc679cfa) confirmed the linkage. Independent raw retrieval also matched all ten upstream file byte counts and SHA-256 values, including LICENSE and NOTICE; results are in the [primary-source receipt](primary-source-receipt.json). This verifies the selected source identity. It does not independently verify the tag's cryptographic signature or demonstrate reproducible correspondence to the running binary.

The local `29.7.2`/`6a43e3d`, linux/amd64 identity is explicitly attributed to the controller's read-only observation. This reviewer ran no Docker command and did not inspect daemon settings. The short-commit match supports selecting the branch for diagnosis, with the report's binary/configuration caveats retained.

The transport comparison remains a proposal. Docker's current documentation supports daemon-host/same-network access, default NAT, loopback publishing and the residual reachability of host services from an ordinary internal bridge. These facts do not establish Windows/WSL client routing or relay isolation. [Official port-publishing documentation](https://docs.docker.com/engine/network/port-publishing/)

A fixed-destination relay would add a dual-network peer and requires its own ownership, forwarding restrictions, cleanup and end-to-end verification. This review accepts the report's comparison and next source-only proposal boundary; it accepts no relay implementation, image availability, topology change, firewall change or runtime grant. The application's single internal endpoint and the existing browser/egress restrictions are not waived.

## Checks and safe publication

The [audit](audit.mjs) passed nine grouped checks under Windows Node v24.20.0. It reran the supplied 36 offline assertions with their sole frozen report write suppressed, ran the supplied read-only 38 hash/byte freeze checks, evaluated 32 combinations of the stated Boolean predicate and verified all frozen input/selected hashes before and after. The [verification receipt](verification.json) records these distinct scopes. Read-only public-source retrieval matched ten raw files and the tag object. No Docker, browser, network topology probe, Moby build/test, dependency installation, Git mutation or frozen write occurred.

```powershell
node artifacts/ui-parity-internal-network-source-review/audit.mjs --fetch-primary
```

The [normalized 19-entry selection](reviewed-source-publication-allowlist.json) is approved and uses the publisher-compatible sourcePath/sha256/bytes array. It preserves every original selected byte/hash while removing only wrapper/entry metadata from this derived selection. Keep the original wrapper separately as publication metadata if desired. All source files are unmodified upstream copies, accompanied by their complete LICENSE and NOTICE. Existing copyright notices and upstream comments remain intact; upstream placeholder comments are not newly introduced QOpenBB implementation placeholders.

The set contains public upstream source, public release/tag metadata, bounded research and offline verification. Public tagger attribution and a public PGP signature are source provenance, not private credentials. A bounded private-key/common-token/generated-test-credential scan found no match. Exploratory API listings and the full commit response are omitted as documented. Existing diagnostic inputs are hash-pinned and already reviewed separately. Local report references resolve; code links use the full immutable commit.

The [review allowlist](publication-allowlist.json) selects this review, audit, receipts and normalized source selection. The controller owns destination hash/link checks, synchronization and commits. These research and upstream snapshot files are excluded from maintained production caps; future production retains the executable inventory/checker foundation and 400 physical lines/file, 300 logical units/file and 50/function. The accepted decision is a bounded source explanation, with no automatic next execution.
