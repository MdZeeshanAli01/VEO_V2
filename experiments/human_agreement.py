import argparse
import csv
import json
from pathlib import Path

import numpy as np

from veo.validation import cohens_kappa


def load_veo_test_labels(results_path: Path, count: int = 50, seed: int = 42) -> dict[str, str]:
    payload = json.loads(results_path.read_text(encoding="utf-8"))
    regions = [(record["sample_id"], region) for record in payload["records"] for region in record["regions"]]
    regions.sort(key=lambda item: item[1]["mean_error"])
    indices = np.linspace(0, len(regions) - 1, min(count, len(regions)), dtype=int)
    selected = [regions[i] for i in indices]
    rng = np.random.default_rng(seed)
    rng.shuffle(selected)
    return {f"rating_{i:04d}": region["top_cause"] for i, (_, region) in enumerate(selected, start=1)}


def load_rater_csv(path: Path) -> dict[str, dict]:
    results = {}
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            results[row["rating_id"]] = {
                "label": row["human_label"].strip().lower(),
                "confidence": row.get("human_confidence", "").strip().lower(),
            }
    return results


def compute_metrics(y_true: list[str], y_pred: list[str], classes: list[str]):
    cm = {c1: {c2: 0 for c2 in classes} for c1 in classes}
    for yt, yp in zip(y_true, y_pred):
        if yt in cm and yp in cm[yt]:
            cm[yt][yp] += 1

    report = {}
    f1_list = []
    for c in classes:
        tp = cm[c][c]
        fp = sum(cm[other][c] for other in classes if other != c)
        fn = sum(cm[c][other] for other in classes if other != c)
        support = sum(cm[c].values())

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        f1_list.append(f1)

        report[c] = {
            "precision": precision,
            "recall": recall,
            "f1-score": f1,
            "support": support,
        }

    macro_f1 = float(np.mean(f1_list)) if f1_list else 0.0
    return report, cm, macro_f1


def main():
    parser = argparse.ArgumentParser(description="Compute human agreement and classification metrics for VEO.")
    parser.add_argument("--rater1", type=Path, required=True, help="Path to rater 1 completed CSV")
    parser.add_argument("--rater2", type=Path, default=None, help="Path to rater 2 completed CSV (optional)")
    parser.add_argument("--results-path", type=Path, default=Path("outputs/nyu_final/test/model_results.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/rating_set_test_50"))
    parser.add_argument("--count", type=int, default=50)
    args = parser.parse_args()

    veo_labels_dict = load_veo_test_labels(args.results_path, count=args.count)
    rater1_data = load_rater_csv(args.rater1)

    rating_ids = sorted(veo_labels_dict.keys())
    y_veo = [veo_labels_dict[rid] for rid in rating_ids]
    y_r1 = [rater1_data[rid]["label"] for rid in rating_ids]

    print("\n" + "=" * 65)
    print("      VEO HUMAN VALIDATION REPORT (OPTION A: 50 REGIONS)")
    print("=" * 65)

    # 1. Rater 1 vs VEO
    kappa_r1_veo = cohens_kappa(y_veo, y_r1)
    print(f"\n[1] VEO vs. Human Rater 1 Agreement:")
    print(f"    Total Evaluated: {len(rating_ids)} regions")
    print(f"    Cohen's Kappa (kappa): {kappa_r1_veo:.4f}")

    # 2. Inter-rater agreement if Rater 2 provided
    kappa_inter = None
    kappa_r2_veo = None
    if args.rater2 and args.rater2.exists():
        rater2_data = load_rater_csv(args.rater2)
        y_r2 = [rater2_data[rid]["label"] for rid in rating_ids]
        kappa_inter = cohens_kappa(y_r1, y_r2)
        kappa_r2_veo = cohens_kappa(y_veo, y_r2)
        print(f"\n[2] Inter-Annotator Agreement (Rater 1 vs. Rater 2):")
        print(f"    Cohen's Kappa (kappa): {kappa_inter:.4f}")
        print(f"\n[3] VEO vs. Human Rater 2 Agreement:")
        print(f"    Cohen's Kappa (kappa): {kappa_r2_veo:.4f}")

    # Classification Metrics (treating Rater 1 as ground truth benchmark)
    classes = sorted(list(set(y_veo) | set(y_r1)))
    report, cm_dict, macro_f1 = compute_metrics(y_r1, y_veo, classes)

    print(f"\n[4] Classification Performance (VEO against Human Rater 1):")
    print(f"    Macro F1-Score: {macro_f1:.4f}")
    print("\nPer-Class Breakdown:")
    print(f"{'Class':<20} {'Precision':<10} {'Recall':<10} {'F1-Score':<10} {'Support':<10}")
    print("-" * 65)
    for c in classes:
        m = report[c]
        print(f"{c:<20} {m['precision']:<10.3f} {m['recall']:<10.3f} {m['f1-score']:<10.3f} {m['support']:<10}")

    print("\nConfusion Matrix (Rows = Human Rater 1, Columns = VEO Prediction):")
    print(f"{'':<18} " + " ".join(f"{c[:6]:>7}" for c in classes))
    for r in classes:
        row_str = " ".join(f"{cm_dict[r][c]:>7}" for c in classes)
        print(f"{r:<18} {row_str}")

    # Save summary report
    summary = {
        "num_regions": len(rating_ids),
        "cohens_kappa_r1_veo": kappa_r1_veo,
        "cohens_kappa_inter": kappa_inter,
        "cohens_kappa_r2_veo": kappa_r2_veo,
        "macro_f1": macro_f1,
        "per_class": report,
        "confusion_matrix": cm_dict,
        "classes": classes,
    }
    output_path = args.output_dir / "human_validation_results.json"
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n[OK] Results saved successfully to: {output_path}")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    main()

