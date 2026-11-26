# FCF yield on the packaged modeling runtime

On 2026-11-26, native Docker Compose pulled the following Linux amd64 images by digest. Workspace and modeling came from a disposable loopback registry. The data API came from its published release on GHCR.

| Service | Image manifest SHA-256 |
| --- | --- |
| Workspace | `8d3347a55a9cfa48d93e5e8f78e53c51b1301b18b3a3b3576a0e25bda681d0aa` |
| Data API | `79d46d09a913a1b6583ae823961ca87b9e4a6bb112739ca738567b131ca79a73` |
| Modeling | `317f279fac69ddac4fe5d3f3f34656e49817c500ef09f772c6cdb7124bd1b516` |

Dagger 0.21.8 built Workspace from integration revision `aa1a625e5d9478f023226b9ac9acd3bcfb71da4a`. The modeling image used 58 explicitly staged inputs with fingerprint `7f8f876752ccf8a53e371dede8d49edff690c70b7419c090125365302e3a2b00` and dependency lock SHA-256 `ff215e49f121e302af3e7f40493a050bbd898d9cfca5ac229047b09b7b730664`. A sealed rebuild reproduced the running manifest. Runtime probes verified UID/GID 10001, writable private state, unsigned request rejection and six methods available to an authenticated caller. Provider credentials stayed in the data service.

| Playwright phase | Observed result |
| --- | --- |
| Evaluate and save | The historical AAPL case withheld yield. The verified SAP.DE result displayed 3.78554% and saved through the native Workspace flow. |
| Reopen | Docker recreated Workspace and modeling while retaining the data API container. A fresh session reopened the persisted result without submitting another evaluation. |
| Modeling unavailable | After Docker stopped modeling, Workspace continued to serve the Apple company profile through the data API. |

The independent reviewer approved task 12.2 after checking the container identities, input hashes, access controls and all three browser reports. Each phase passed once with zero skips, unexpected outcomes or flaky retries. Raw local reports are under `artifacts/modeling-image-candidate/packaged-amwgvz8c/`. Task 12.3 owns registry publication and verification of the published image set. Owner-server acceptance requires a separate run.

[Packaged verification procedure](../../../docs/modeling-deployment.md)
