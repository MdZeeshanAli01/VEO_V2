import csv
import json
from collections import Counter
from pathlib import Path

import numpy as np


def write_manifest(pairs, path: Path, split: str) -> None:
    payload = [{"sample_id": p.sample_id, "rgb_path": str(p.rgb_path), "depth_path": str(p.depth_path), "split": split} for p in pairs]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_summary(records: list[dict], output_dir: Path) -> None:
    causes = Counter(region["top_cause"] for record in records for region in record["regions"])
    metrics = {name: float(np.mean([record["metrics"][name] for record in records])) for name in ("abs_rel", "rmse", "delta1")} if records else {}
    summary = {
        "num_samples": len(records),
        "num_regions": sum(record["num_regions"] for record in records),
        "mean_metrics": metrics,
        "cause_counts": dict(causes),
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