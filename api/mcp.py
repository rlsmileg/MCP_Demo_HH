"""Self-contained Vercel entrypoint: FastMCP DatasauRus server exposed as ASGI.

Inlines the logic from /server.py so the function has no cross-file imports;
reads myDatasauRus.csv from this directory (bundled alongside the function).
"""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastmcp import FastMCP


mcp = FastMCP("DatasauRus")

DATA_PATH = Path(__file__).with_name("myDatasauRus.csv")


def _point(row: dict[str, str]) -> dict[str, float]:
    return {"x": float(row["x"]), "y": float(row["y"])}


def _summary(points: list[dict[str, float]]) -> dict[str, Any]:
    xs = [p["x"] for p in points]
    ys = [p["y"] for p in points]
    return {
        "count": len(points),
        "x": {"min": min(xs), "max": max(xs)},
        "y": {"min": min(ys), "max": max(ys)},
    }


@lru_cache(maxsize=1)
def _load_datasets() -> dict[str, list[dict[str, float]]]:
    datasets: dict[str, list[dict[str, float]]] = {}
    with DATA_PATH.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            datasets.setdefault(row["dataset"], []).append(_point(row))
    return datasets


def _resolve_dataset_name(dataset: str) -> str:
    requested = dataset.strip()
    datasets = _load_datasets()
    if requested in datasets:
        return requested
    lowered = requested.lower()
    for name in datasets:
        if name.lower() == lowered:
            return name
    available = ", ".join(sorted(datasets))
    raise ValueError(f"Unknown dataset '{dataset}'. Available datasets: {available}.")


@mcp.tool
def list_datasets() -> list[dict[str, Any]]:
    """List available DatasauRus dataset names and point counts."""
    return [
        {"name": name, "count": len(points)}
        for name, points in sorted(_load_datasets().items())
    ]


@mcp.tool
def get_dataset_points(dataset: str) -> dict[str, Any]:
    """Return all x and y values for a specific dataset name."""
    name = _resolve_dataset_name(dataset)
    points = _load_datasets()[name]
    return {"dataset": name, "points": points, "summary": _summary(points)}


@mcp.tool
def get_dataset_summary(dataset: str | None = None) -> dict[str, Any]:
    """Return count and x/y ranges for one dataset, or for every dataset."""
    datasets = _load_datasets()
    if dataset:
        name = _resolve_dataset_name(dataset)
        return {"dataset": name, "summary": _summary(datasets[name])}
    return {
        "datasets": [
            {"dataset": name, "summary": _summary(points)}
            for name, points in sorted(datasets.items())
        ]
    }


app = mcp.http_app(path="/")
