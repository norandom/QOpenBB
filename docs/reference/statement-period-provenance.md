# Upgrade strict statement consumers together

The published alpha adds row-level period evidence to existing FMP Income, Balance and Cash responses. It preserves financial row fields and widget inputs. Deploy matching core and FMP packages together; update strict Python validators before consuming the new optional `statement_provenance` member.

Published in [alpha-42878062405-1](https://github.com/norandom/QOpenBB/releases/tag/alpha-42878062405-1) from QOpenBB `e09024aa965757d23937ed0472ccce05d9666aea` and API `a965f70c164fe477ce9c99654b9be48e2f1bc9fd`, including the [native optional-limit repair](../../artifacts/reviewed/statement-period-provenance/native-defaults.md). Package version strings (`openbb-core` 2.0.1 and `openbb-fmp` 1.6.1+qopenbb.1) alone do not identify the change. [Publication acceptance](../../artifacts/reviewed/statement-period-provenance/publication.md) verifies the image pair separately from the accepted local browser journey.

## Consumer compatibility

| Consumer | Required action |
| --- | --- |
| Widget reading `results` | Retain existing columns, parameters and `dataKey`. |
| New strict financial validator | Reads both older envelopes and the optional statement member. |
| Older strict financial validator | Upgrade before reading the extended envelope; unknown fields are rejected. |
| FRED or unrelated provider consumer | No statement member is emitted when absent. |

The outer `schema_version` remains 1. It does not make an older strict model compatible with an added member. There is no alternate response format or hidden compatibility switch.

## Financial interpretation

Use `row_index` to associate provenance with each returned row. `source_ordinal` identifies its position in the acquired response; selection and sorting can leave gaps. Duplicate period ends remain separate observations. Supplied null facts differ from absent facts, and zero remains a financial value.

An annual or quarterly request does not prove the duration covered by a reported flow. Without supporting evidence, flow coverage, start date, duration and restatement status remain unknown. Closing stock values retain their reported dates; beginning cash has no inferred date. Filing, acceptance and retrieval timestamps do not establish point-in-time availability.

## Verification boundary

The corrected native run checked annual and quarterly Income, Balance and Cash for MSFT, ORCL and ADBE: 18 cases, each requesting two rows. Source values and raw period facts were compared with the HTTP response. The same captured rows were replayed through the installed Python provider transformation to check provenance agreement without another fetch. This is not a second public Python-command acquisition.

An earlier 18-request run returned HTTP 200 but failed the acceptance comparator because source timestamps used a space and HTTP timestamps used `T`. The comparator was repaired and independently reviewed; the original failures remain recorded. Total provider traffic was 36 FMP requests and zero FRED requests. No financial calculation or coverage inference was added.

The canonical image-backed catalog regenerates all 11 existing widgets. Its six canonical outputs match the published API image byte-for-byte. All seven [implementation tasks](../../.kiro/specs/market-data-integrations/statement-period-provenance-tasks.md) are accepted. Deployment on the owner server and broader analytical compatibility remain separate gates.
