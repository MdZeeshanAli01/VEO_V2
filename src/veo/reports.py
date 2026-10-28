import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np


def write_result(path: Path, payload: dict, config=None, inputs: dict[str, Path] | None = None) -> Path:
    """Write an experiment result with a provenance block so every number can be traced."""
    from .provenance import provenance

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({**payload, "provenance": provenance(config, inputs)}, indent=2, default=str), encoding="utf-8")
    return path


def write_manifest(pairs, path: Path, split: str) -> None:
    payload = [{"sample_id": p.sample_id, "rgb_path": str(p.rgb_path), "depth_path": str(p.depth_path), "split": split} for p in pairs]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _failure_extent(records: list[dict]) -> dict:
    """How much of the evaluated image area fails, and how much of it each hypothesis covers.

    Shares are of all valid pixels across the split, so models with different region counts compare fairly.
    """
    if not records or "valid_pixels" not in records[0]:
        return {}
    valid = sum(record["valid_pixels"] for record in records)
    regions = [region for record in records for region in record["regions"]]
    label_pixels = Counter()
    top_pixels = Counter()
    for region in regions:
        top_pixels[region["top_cause"]] += region["area"]
        for label in region.get("labels", []):
            label_pixels[label] += region["area"]
    return {
        "valid_pixels": valid,
        "mean_failure_pixel_fraction": float(np.mean([record["failure_pixel_fraction"] for record in records])),
        "region_pixel_fraction": sum(region["area"] for region in regions) / valid,
        "top_cause_pixel_fraction": {label: count / valid for label, count in top_pixels.items()},
        "label_pixel_fraction": {label: count / valid for label, count in label_pixels.items()},
        "label_counts": dict(Counter(label for region in regions for label in region.get("labels", []))),
        "multi_label_regions": sum(len(region.get("labels", [])) > 1 for region in regions),
    }


def write_summary(records: list[dict], output_dir: Path) -> None:
    causes = Counter(region["top_cause"] for record in records for region in record["regions"])
    metric_names = ("mae", "rmse", "abs_rel", "sq_rel", "delta1", "delta2", "delta3", "spearman")
    metrics = {
        name: float(np.mean([record["metrics"][name] for record in records if name in record["metrics"]]))
        for name in metric_names
        if records and all(name in record["metrics"] for record in records)
    }
    summary = {
        "num_samples": len(records),
        "num_regions": sum(record["num_regions"] for record in records),
        "mean_metrics": metrics,
        "cause_counts": dict(causes),
        **_failure_extent(records),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    with (output_dir / "regions.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["sample_id", "region_id", "mean_error", "area", "top_cause", "confidence"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in records:
            for region in record["regions"]:
                writer.writerow({"sample_id": record["sample_id"], **{field: region[field] for field in fields[1:]}})


def write_correlations(records: list[dict], output_path: Path) -> None:
    from scipy.stats import pearsonr

    regions = [region for record in records for region in record["regions"]]
    signals = sorted(regions[0]["features"].keys()) if regions else []
    errors = np.asarray([region["mean_error"] for region in regions], dtype=float)
    rows = []
    for signal in signals:
        values = np.asarray([region["features"][signal] for region in regions], dtype=float)
        if len(values) < 2 or np.std(values) == 0 or np.std(errors) == 0:
            correlation, p_value = float("nan"), float("nan")
        else:
            correlation, p_value = pearsonr(values, errors)
        rows.append({"signal": signal, "pearson_r": correlation, "p_value": p_value, "significant": bool(p_value < 0.05) if np.isfinite(p_value) else False})
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["signal", "pearson_r", "p_value", "significant"])
        writer.writeheader()
        writer.writerows(rows)