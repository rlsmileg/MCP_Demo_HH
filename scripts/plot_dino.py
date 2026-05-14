"""Render the dino dataset as a scatterplot PNG."""

import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "api" / "datasets" / "dino.json"
OUT = ROOT / "dino.png"

points = json.loads(DATA.read_text())["points"]
xs = [p["x"] for p in points]
ys = [p["y"] for p in points]

fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(xs, ys, s=30, color="#0b645f", edgecolor="white", linewidth=0.5)
ax.set_title(f"Datasaurus: dino ({len(points)} points)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(OUT, dpi=150)
print(f"wrote {OUT.relative_to(ROOT)}")
