import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .data import load_depth, load_rgb
from .metrics import compute_error_map
from .scoring import classify


def cohens_kappa(first: list[str], second: list[str]) -> float:
    if len(first) != len(second) or not first:
        raise ValueError("Both label lists must be non-empty and have equal length")
    total = len(first)
    categories = set(first) | set(second)
    observed = sum(left == right for left, right in zip(first, second)) / total
    first_counts = Counter(first)
    second_counts = Counter(second)
    expected = sum((first_counts[label] / total) * (second_counts[label] / total) for label in categories)
    if expected == 1.0:
        return 1.0
    return float((observed - expected) / (1.0 - expected))


def ablation_change(records: list[dict], dropped_signal: str, include_reflection: bool = True) -> dict[str, int]:
    changed = 0
    total = 0
    for record in records:
        for region in record["regions"]:
            features = dict(region["features"])
            if dropped_signal not in features:
                continue
            if dropped_signal == "texture_var":
                features["texture_var"] = 500.0
            elif dropped_signal == "edge_density":
                features["edge_density"] = 0.0
            elif dropped_signal == "brightness":
                features["brightness"] = 128.0
                features["contrast"] = 60.0
            elif dropped_signal == "contrast":
                features["contrast"] = 60.0
            elif dropped_signal == "highlight_ratio":
                features["highlight_ratio"] = 0.0
            elif dropped_signal == "aspect_ratio":
                features["aspect_ratio"] = 1.0
            elif dropped_signal == "depth_discontinuity":
                features["depth_discontinuity"] = 0.0
            else:
                raise ValueError(f"Unsupported ablation signal: {dropped_signal}")
            new_label = classify(features, include_reflection)["top_cause"]
            changed += new_label != region["top_cause"]
            total += 1
    return {"changed_regions": changed, "total_regions": total}


def export_rating_set(results_path: Path, rgb_dir: Path, depth_dir: Path, prediction_dir: Path, output_dir: Path, count: int = 200, seed: int = 42) -> int:
    payload = json.loads(results_path.read_text(encoding="utf-8"))
    regions = [(record["sample_id"], region) for record in payload["records"] for region in record["regions"]]
    if not regions:
        raise ValueError("Results file contains no regions")
    regions.sort(key=lambda item: item[1]["mean_error"])
    indices = np.linspace(0, len(regions) - 1, min(count, len(regions)), dtype=int)
    selected = [regions[index] for index in indices]
    rng = np.random.default_rng(seed)
    rng.shuffle(selected)
    panel_dir = output_dir / "panels"
    panel_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for rating_index, (sample_id, region) in enumerate(selected, start=1):
        rgb = load_rgb(rgb_dir / f"{sample_id}.png")
        depth = load_depth(depth_dir / f"{sample_id}.npy")
        prediction = np.asarray(np.load(prediction_dir / f"{sample_id}.npy"), dtype=np.float32)
        error = compute_error_map(prediction, depth, np.isfinite(depth) & (depth > 0))
        x, y, width, height = region["bbox"]
        slices = (slice(y, y + height), slice(x, x + width))
        figure, axes = plt.subplots(1, 4, figsize=(12, 3))
        axes[0].imshow(rgb[slices]); axes[0].set_title("RGB")
        axes[1].imshow(depth[slices], cmap="magma"); axes[1].set_title("Ground truth")
        axes[2].imshow(prediction[slices], cmap="magma"); axes[2].set_title("Prediction")
        axes[3].imshow(error[slices], cmap="inferno"); axes[3].set_title("Error")
        for axis in axes:
            axis.axis("off")
        panel_path = panel_dir / f"rating_{rating_index:04d}.png"
        figure.tight_layout()
        figure.savefig(panel_path, dpi=120)
        plt.close(figure)
        rows.append({"rating_id": f"rating_{rating_index:04d}", "panel_path": str(panel_path), "sample_id": sample_id, "human_label": "", "human_confidence": "", "notes": ""})
    with (output_dir / "rating_template.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "rater_instructions.md").write_text(
        "# VEO Blind Region Rating\n\nAssign one primary label to each panel without inspecting VEO predictions or scores.\n\n"
        "Allowed labels: `textureless`, `boundary_mixing`, `occlusion`, `thin_object`, `poor_lighting`, `reflection`, `ambiguous`.\n\n"
        "Use `ambiguous` when evidence is insufficient or multiple labels are equally plausible. Record confidence as `high`, `medium`, or `low`. Do not infer the label from the filename.\n",
        encoding="utf-8",
    )
    return len(rows)
