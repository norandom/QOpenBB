# Portable runtime boundary restored

The Linux runtime entry uses explicit Linux storage, container executable and daemon endpoint, while Windows retains its native preflight. Linux inputs reject filesystem roots, links and Windows-mounted cache/storage paths. Checked browser consumers receive absolute reader and Python paths.

Independent Astra review accepted the bounded correction after fixing virtual-environment symlink handling: the selected Python retains its invocation path rather than resolving to a base interpreter without its dependencies. Captured RED demonstrates that defect; final affected Windows checks passed 67 tests with three platform skips. Independent focused checks passed, and the hidden-child-process regression passed separately. Real Linux symlink-venv and checked-reader execution remain pending CI; Windows results do not certify Linux.

The existing portable CI check now includes the affected runtime, storage, reader and offline budget tests, preserving previous checks and excluding live providers. The combined production gate passed after the correction; no size exceptions were added. Raw evidence and review inputs remain under D:/BuildArtifacts/QOpenBB/native-linux. Full task 12 remains open until integration and real Linux acceptance.
