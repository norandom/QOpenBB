# Explicit financial provider policy accepted

Main task 4.2 is source-accepted on 2026-10-29. The pure ASGI guard derives exact paths, methods and provider choices from generated financial descriptors. It rejects missing, blank, repeated or unsupported provider selections before forwarding, preserves accepted query bytes and never retries or substitutes providers.

Profile, income and FRED defaults remain intact. Mounted guard/handler tests prove zero execution on omission, one execution on explicit selection and safe typed failures with bounded retry advice. Independent Astra verification passed the 126-test closing join, including both components, the core error contract and projection. Ruff passed; guard counts are 62 physical lines, 40 logical units and 19 per function. The shared Node 24.22.1 size gate passed 77 files.

See [review](review.md) and [source identities](final-source.json). Both HTTP components are ready for task 5.2 installation; no deployed enforcement or image publication is claimed. Main source progress is 18/26.
