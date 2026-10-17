"""Copy only the two owned lane files between the workspace and frozen stage."""
from pathlib import Path
import shutil
import sys

working = Path("/mnt/d/Source/QOpenBB/vendor/workspace/terminalpro")
stage = Path("/home/mc/qopenbb-work/task243-colors-20261017/terminalpro")
source, target = (working, stage) if sys.argv[1] == "stage" else (stage, working)
for name in ["src/components/General/Table/Chart/application/appearanceColors.ts",
             "tests/unit/chart-application/appearanceColors.test.ts"]:
    shutil.copy2(source / name, target / name)
