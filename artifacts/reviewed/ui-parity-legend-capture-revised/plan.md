# Review four bounded collector corrections before any runtime

This revision addresses B01-B04 in the [independent collector review](../ui-parity-legend-collector-review/review.md). The accepted [eight-case Legend plan](../ui-parity-legend-plan-revised/plan.md), SHA256 `5a33a0237eb351df5a7a6060da2aff5c83379f89999c4a4ca82faa40c92e29ef`, remains the contract. The initial collector and its review remain frozen. Only this new artifact folder is writable. No application/browser/container, build, install or network-topology test is authorized by this source revision.

## B01: deny external traffic at both owned boundaries

Every context route callback checks the request origin itself before continue, fetch or fulfill. Sync fetches use zero redirects and reject a foreign response identity or any redirect response. Routing covers the owned browser context, including any new page, and service workers are blocked.

Before creating the original container, startup creates one randomly named, ownership-labeled internal bridge. It inspects the exact ID/name/label, bridge driver, Internal=true and IPv6=false. The container receives only that network, loopback DNS and empty HTTP/HTTPS/ALL proxy variables. Before health admission, its inspect record must show exactly that one attached network and exactly one port-3000 publication on 127.0.0.1. The only startup HTTP probe targets the recorded loopback origin with redirects rejected. A missing or inaccessible publication stops admission within the existing startup deadline; there is no topology retry, fallback network or alternate origin.

Docker documents that internal networks have no default route and firewall rules drop traffic crossing to other networks; host gateway access remains possible. Its bridge driver supports published ports, and a publication bound to 127.0.0.1 is host-local. These documented mechanisms support this source proposal; they do not prove compatibility with the installed daemon. See [internal networks](https://docs.docker.com/reference/cli/docker/network/create/#network-internal-mode---internal), [bridge driver](https://docs.docker.com/engine/network/drivers/bridge/) and [port publication](https://docs.docker.com/engine/network/port-publishing/). The future same-origin health admission is the bounded port-viability check. No host relay/provider endpoint is configured, and no general claim that internal networking makes every host service unreachable is made.

The raw receipt records network identity before creation and its actual ID immediately afterward, permitting cleanup after partial startup. Cleanup verifies exact owned network name/ID/label, removes the original owned container first, refuses to remove a network with remaining attachments, then removes and verifies absence of only that network. Wrong isolation configuration fails admission but does not prevent removal of an otherwise proven owned empty network. No daemon-wide firewall or network setting is changed.

## B02: retain invalid getter brackets

Settlement retains the latest invalid sample's index/time and its exact fourteen before/after operand records, including when later equal samples succeed or a later active/missing/deadline sample fails. It records the invalid count and how many earlier invalid samples were omitted by this bounded rule. No extra getter, sample, node or deadline is added. Observation and total byte ceilings still fail closed.

## B03: prove owned browser-process absence

The browser launches through Playwright BrowserServer and records its returned child PID and Linux /proc start ticks before connecting. This reuses the reviewed tooltip helper pattern identified in provenance.json. Parsing handles command names containing spaces. Transport closure remains a separate supporting receipt.

After normal close, the journey checks the recorded process identity's absence. Cleanup independently rereads the same private identity and uses bounded TERM then KILL only while PID/start ticks still match. PID reuse refuses termination. A missing identity, surviving process or failed check remains cleanup-unverified. Final status requires the independent process-absence receipt and owned network absence. The existing 120-second cleanup reserve and 2,220-second hard limit remain unchanged.

## B04: drain events and overflow together

The page's synchronous drain removes the original listener when final, then returns one bounded copy of the ordered events plus overflow and listener-removal state. The host persists the event prefix before checking overflow; overflow gets a bounded receipt and fails the attempt. Successful summary creation occurs after the final drain. Finalization also rejects overflow, late-event, failed-drain or failure receipts even if an incoming process status is zero.

Each settled observation's sequence must equal its subsequent drain. The action ledger ends its event interval at the after-observation's sequence and records the actual drained count separately. An event arriving during raster capture produces late-events-unresolved and stops new input; it is never linked to older settled pixels. This correction takes no additional settling poll and extends no deadline.

## Fixed scope and verification

The four-quarter/two-series fixture bytes, original controls, L01-L08, seven BBox calls, fourteen operands, fourteen scene identities, all numerical/output/time limits and original UX remain unchanged. There is no extra scene traversal, fixture, provider call or candidate execution. Research scripts/tests/frozen baseline are excluded from production size caps; future production retains the inventory/checker foundation, 400 physical lines/file, 300 logical units/file and 50/function.

Source checks:

```powershell
node artifacts/ui-parity-legend-capture-revised/offline-tests.mjs
node artifacts/ui-parity-legend-capture-revised/static-check.mjs
node artifacts/ui-parity-legend-capture-revised/freeze.mjs
```

The canonical future command requires independent approval and a separate controller grant. It has not run:

```bash
node artifacts/ui-parity-legend-capture-revised/prepare-run.mjs
LEGEND_HEAVY_GRANTED=controller-granted bash artifacts/ui-parity-legend-capture-revised/supervise.sh /mnt/d/Source/QOpenBB/artifacts/ui-parity-legend-capture-revised/attempt-<printed-id>
```

Use the exact printed attempt path with a hidden WSL helper. No automatic retry follows a failed admission, case, budget or cleanup.
