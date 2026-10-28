"""Scoring-function sanity check: adding noise to a textureless region must lower its textureless score.

This checks that the implementation follows its formula (score = 1 - texture_var / 500). It does not
re-run the depth model, so it says nothing about whether VEO's explanation is faithful to the model.
"""

import argparse
import json
from pathlib import Path

import cv2
import numpy as np

from veo.data import load_depth, load_rgb
from veo.features import extract_features
from veo.reports import write_result
from veo.scoring import classify


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--results-path", type=Path, default=Path("outputs/nyu_final/test/model_results.json"))
    parser.add_argument("--rgb-dir", type=Path, default=Path("data/nyu/splits/test/rgb"))
    parser.add_argument("--depth-dir", type=Path, default=Path("data/nyu/splits/test/depth"))
    parser.add_argument("--noise-max", type=int, default=100, help="Uniform noise in [0, noise-max) added to RGB")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("results/nyu_test/scoring_sanity_check.json"))
    args = parser.parse_args()

    records = json.loads(args.results_path.read_text(encoding="utf-8"))["records"]
    candidate = next(
        (
            (record["sample_id"], region)
            for record in records
            for region in record["regions"]
            if region["top_cause"] == "textureless" and region["confidence"] == "High"
        ),
        None,
    )
    if candidate is None:
        write_result(args.output, {"skipped": "no High-confidence textureless region"}, inputs={"veo_results": args.results_path})
        print(f"No eligible region; saved {args.output}")
        return
    sample_id, region = candidate
    rgb = load_rgb(args.rgb_dir / f"{sample_id}.png")
    depth = load_depth(args.depth_dir / f"{sample_id}.npy")
    x, y, w, h = region["bbox"]
    # Result files store the bounding box only, so features are re-extracted over the whole box
    box_region = {"bbox": region["bbox"], "mask": np.zeros_like(depth, dtype=bool)}
    box_region["mask"][y:y + h, x:x + w] = True

    noise = np.random.default_rng(args.seed).integers(0, args.noise_max, size=(h, w, 3), dtype=np.uint8)
    perturbed = rgb.copy()
    perturbed[y:y + h, x:x + w] = cv2.add(perturbed[y:y + h, x:x + w], noise)
    before = classify(extract_features(rgb, depth, box_region))
    after = classify(extract_features(perturbed, depth, box_region))

    payload = {
        "sample_id": sample_id,
        "region_id": region["region_id"],
        "edit": f"uniform integer noise [0, {args.noise_max}) added inside the bounding box",
        "model_rerun": False,
        "before": {"textureless_score": before["scores"]["textureless"], "top_cause": before["top_cause"]},
        "after": {"textureless_score": after["scores"]["textureless"], "top_cause": after["top_cause"]},
        "score_decreased": after["scores"]["textureless"] < before["scores"]["textureless"],
    }
    write_result(args.output, payload, inputs={"veo_results": args.results_path})
    print(f"{sample_id} region {region['region_id']}: textureless {payload['before']['textureless_score']:.3f} -> {payload['after']['textureless_score']:.3f}")
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
