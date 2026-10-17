"""Independently show the IEEE-754 value behind the corrected finite expectation."""
from fractions import Fraction
import json
import math
from pathlib import Path

# For white foreground/black background, normalization produces exactly 1 and 0.
# Therefore only the foreground weight contributes to the source expression.
t = 1.0 - 0.1
weight = 1.0 - t
unrounded = weight * 255.0
result = {"t": t, "foreground_weight": weight,
          "exact_weight": str(Fraction.from_float(weight)),
          "unrounded_channel": unrounded,
          "nearest_byte": math.floor(unrounded + 0.5),
          "expected_light_grid": "#191919"}
Path("/mnt/d/Source/QOpenBB/artifacts/task-2.43/implementation/rounding-oracle.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(json.dumps(result))
