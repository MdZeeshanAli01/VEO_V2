"""Objective-label evaluation and calibration of VEO's failure hypotheses (Phase 3).

For each split, region masks are recomputed from the cached predictions (results files store only
bounding boxes), checked against the stored regions, and given silver labels from NYU's semantic
and instance annotations. Models are fitted on the train split and scored on the test split.
"""

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np

from veo.calibration import evaluate, fit, public_models
from veo.checkpoint import JsonlLog, resumed
from veo.config import config_from_dict
from veo.data import RGBDepthPair
from veo.pipeline import compute_regions
from veo.provenance import config_hash
from veo.reports import write_result
from veo.runner import load_sample
from veo.silver import SILVER_CATEGORIES, class_ids, region_silver, silver_maps


def build_rows(results_path: Path, checkpoint: Path | None = None) -> tuple[list[dict], dict]:
    """Silver-labelled rows for every region; with ``checkpoint``, finished images are logged and skipped on resume."""
    payload = json.loads(results_path.read_text(encoding="utf-8"))
    config = config_from_dict(payload["config"])
    split_dir = config.dataset.depth_dir.parent
    prediction_dir = results_path.parent / "predictions"
    groups = class_ids(json.loads((split_dir / "label_names.json").read_text(encoding="utf-8")))
    scenes = {record["sample_id"]: record["scene"] for record in json.loads((split_dir / "metadata.json").read_text(encoding="utf-8"))}
    log = JsonlLog(checkpoint, config_hash({"results": str(results_path), "config": payload["config"]})) if checkpoint else None
    finished = log.load() if log else {}
    rows = [row for sample_rows in finished.values() for row in sample_rows]
    records = {record["sample_id"]: record for record in payload["records"]}
    for sample_id in resumed(list(records), set(finished)):
        record = records[sample_id]
        sample_rows = []
        pair = RGBDepthPair(sample_id, split_dir / "rgb" / f"{sample_id}.png", split_dir / "depth" / f"{sample_id}.npy")
        _, target, dense, valid = load_sample(pair, config)
        computed = compute_regions(target, np.load(prediction_dir / f"{sample_id}.npy"), valid, config.experiment)
        stored = {region["region_id"]: region for region in record["regions"]}
        recomputed = {region["region_id"]: region for region in computed["regions"]}
        if stored.keys() != recomputed.keys():
            raise RuntimeError(f"{sample_id}: recomputed regions differ from the stored results")
        instances_path = split_dir / "instances" / f"{sample_id}.npy"
        maps = silver_maps(
            np.load(split_dir / "labels" / f"{sample_id}.npy"),
            np.load(instances_path) if instances_path.exists() else None,
            dense,
            groups,
        )
        for region_id, region in stored.items():
            sample_rows.append({
                "sample_id": sample_id,
                "scene": scenes.get(sample_id, sample_id),
                "region_id": region_id,
                "area": region["area"],
                "features": region["features"],
                "top_cause": region["top_cause"],
                "labels": region["labels"],
                "silver": region_silver(maps, recomputed[region_id]["mask"]),
            })
        rows.extend(sample_rows)
        if log:
            log.append(sample_id, sample_rows)
    return rows, payload["config"]["experiment"]


def top_label_precision(rows: list[dict]) -> dict:
    """How often VEO's top label is confirmed by the silver labels, for categories that have them."""
    report = {}
    for category in SILVER_CATEGORIES:
        chosen = [row for row in rows if row["top_cause"] == category]
        confirmed = sum(category in row["silver"]["labels"] for row in chosen)
        report[category] = {"predicted": len(chosen), "confirmed": confirmed, "precision": confirmed / len(chosen) if chosen else None}
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--train-results", type=Path, required=True)
    parser.add_argument("--test-results", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    train_rows, settings = build_rows(args.train_results, args.output.with_name(args.output.stem + "_train.checkpoint.jsonl"))
    test_rows, _ = build_rows(args.test_results, args.output.with_name(args.output.stem + "_test.checkpoint.jsonl"))
    models = fit(train_rows)
    payload = {
        "train": {"regions": len(train_rows), "silver_counts": dict(Counter(label for row in train_rows for label in row["silver"]["labels"]))},
        "test": {
            "regions": len(test_rows),
            "silver_counts": dict(Counter(label for row in test_rows for label in row["silver"]["labels"])),
            "mean_annotated_share": float(np.mean([row["silver"]["annotated_share"] for row in test_rows])) if test_rows else None,
            "top_label_precision": top_label_precision(test_rows),
            "evaluation": evaluate(models, test_rows, settings),
        },
        "models": public_models(models),
    }
    write_result(args.output, payload, inputs={"train_results": args.train_results, "test_results": args.test_results})
    for category, entry in payload["test"]["evaluation"]["categories"].items():
        parts = [f"{name} AUROC {entry[name]['auroc']:.3f}" for name in ("hand_set", "calibrated", "learned") if name in entry and entry[name]["auroc"] is not None]
        print(f"{category:<16} positives {entry['positives']:>5}  " + "  ".join(parts))
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
