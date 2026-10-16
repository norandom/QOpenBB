# Component notices and release constraints

The acquired sources are available for review, but QOpenBB is not ready for release. Resolve the essential component rights in [the constraint inventory](../sources/constraints.json) before accepting a distributable image. This inventory records evidence and missing decisions; it does not decide legal entitlement.

## Retained upstream evidence

The [notice inventory](../sources/notices.json) maps every retained license/notice to its exact source revision, original path and SHA256. Files under [sources/notices](../sources/notices/) preserve the original bytes, including upstream wording. The owned checkouts retain the complete source trees. Repository licenses do not establish rights to every dependency or proprietary asset.

| Component | Observed source license evidence | Scope |
| --- | --- | --- |
| Workspace | Root Apache-2.0 LICENSE and NOTICE | Full frontend/application packaging at the acquired revision |
| Excel add-in | Its own MIT LICENSE, alongside Workspace root notices | Source inventory only; implementation waits for Anthropic acceptance |
| Data API | Root Apache-2.0 LICENSE at both acquired and candidate revisions | Required own-source runtime packages; exact package metadata in [packages.json](../sources/packages.json) |
| FMP 1.6.1 | Published package metadata declares AGPL-3.0-only | The wheel and source archive omit a standalone license file. Retained historical upstream root AGPL text has separate provenance; the v5 Apache license does not relicense the old extension |

FMP source archive SHA256 is `5f6f27af6283075912df42f373c45ed37bc6970097342ed73110fb6101be5517`. This is provenance for later restoration into the owned data fork, not evidence that FMP works with core 2.

## Rights decisions before release

AG Grid Enterprise 34.1.1, AG Charts Enterprise 12.1.1 and Highcharts 11.4.8 appear in the frozen frontend inputs and are imported by actual renderers. Their applicable rights remain unresolved for QOpenBB. Establish rights for the intended use/distribution or review and test their replacement/removal before accepting the Full image. An upstream embedded key supplies no entitlement evidence and its value must not be copied into reports. Review the vendors' [AG Grid/Charts terms](https://www.ag-grid.com/license-pricing/) and [Highcharts licensing](https://shop.highcharts.com/license) against the selected artifacts and intended use.

TradingView Advanced Charts is absent, as the retained Workspace NOTICE states. Keep that optional renderer disabled and report it unavailable. Enabling it requires separately supplied assets, applicable rights and a new verification gate; see [TradingView's library page](https://www.tradingview.com/advanced-charts/). Its absence does not change the selected Full build variant.

The later Excel lock references `@openbb/ui` 0.3.0 at a public npm URL. Its complete dependency/notice audit and clean installation remain pending after Anthropic acceptance. Public availability alone proves neither entitlement nor compatibility. A complete transitive license inventory belongs to the locked build inputs, which do not yet exist.

## Reproduce the evidence

On 2026-10-16 acquisition inspected the owned revisions in [sources.lock.json](../sources.lock.json), the official [API release](https://github.com/openbq-org/OpenBB/releases/tag/openbb-v5.0.0) and [FMP package metadata](https://pypi.org/pypi/openbb-fmp/1.6.1/json). Hash retained files as bytes, then compare with `sources/notices.json`; compare Git-backed files with `git show <revision>:<path>` without newline conversion. Each inventory entry identifies its source, so a changed revision or hash invalidates that evidence.

No image build, dependency installation or runtime/license acceptance was performed here. [Compatibility status](compatibility.md) identifies the follow-up engineering gates.
