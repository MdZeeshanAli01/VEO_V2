"""Agreement between VEO labels and blinded human raters.

Two input modes:
  * rater CSVs (rating_id, human_label) plus the VEO results file the rating set was drawn from;
  * a stored confusion matrix (rows = rater 1, columns = VEO), e.g. results/v1/human_validation_results.json,
    which is all that survives of the v1 study in the repository.
"""

import argparse
import csv
import json
from pathlib import Path

import numpy as np

from veo.reports import write_result
from veo.validation import agreement_report, cohens_kappa, labels_from_confusion


def veo_labels_for_rating_set(results_path: Path, count: int, seed: int) -> dict[str, str]:
    """Rebuild rating_id -> VEO label using the same selection as veo.validation.export_rating_set."""
    payload = json.loads(results_path.read_text(encoding="utf-8"))
    regions = [region for record in payload["records"] for region in record["regions"]]
    regions.sort(key=lambda region: region["mean_error"])
    indices = np.linspace(0, len(regions) - 1, min(count, len(regions)), dtype=int)
    selected = [regions[index] for index in indices]
    np.random.default_rng(seed).shuffle(selected)
    return {f"rating_{i:04d}": region["top_cause"] for i, region in enumerate(selected, start=1)}


def load_rater_csv(path: Path) -> dict[str, str]:
    with path.open(encoding="utf-8") as handle:
        return {row["rating_id"]: row["human_label"].strip().lower() for row in csv.DictReader(handle)}


def from_csvs(args) -> tuple[dict, dict[str, Path]]:
    veo = veo_labels_for_rating_set(args.results_path, args.count, args.seed)
    ids = sorted(veo)
    predicted = [veo[i] for i in ids]
    rater1 = load_rater_csv(args.rater1)
    payload = {"source": "rater_csvs", "veo_vs_rater1": agreement_report([rater1[i] for i in ids], predicted)}
    inputs = {"veo_results": args.results_path, "rater1": args.rater1}
    if args.rater2:
        rater2 = load_rater_csv(args.rater2)
        payload["veo_vs_rater2"] = agreement_report([rater2[i] for i in ids], predicted)
        payload["inter_rater_kappa"] = cohens_kappa([rater1[i] for i in ids], [rater2[i] for i in ids])
        inputs["rater2"] = args.rater2
    return payload, inputs


def from_confusion(path: Path) -> tuple[dict, dict[str, Path]]:
    stored = json.loads(path.read_text(encoding="utf-8"))
    reference, predicted = labels_from_confusion(stored["confusion_matrix"])
    payload = {
        "source": "stored_confusion_matrix",
        "veo_vs_rater1": agreement_report(reference, predicted),
        # Rater 2 is only available as summary statistics in the stored file
        "veo_vs_rater2_kappa": stored.get("cohens_kappa_r2_veo"),
        "inter_rater_kappa": stored.get("cohens_kappa_inter"),
    }
    return payload, {"confusion_matrix": path}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from-confusion", type=Path, help="Stored results JSON with a confusion_matrix")
    parser.add_argument("--rater1", type=Path)
    parser.add_argument("--rater2", type=Path)
    parser.add_argument("--results-path", type=Path, default=Path("outputs/nyu_final/test/model_results.json"))
    parser.add_argument("--count", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, default=Path("results/v1/human_agreement.json"))
    args = parser.parse_args()
    if args.from_confusion:
        payload, inputs = from_confusion(args.from_confusion)
    elif args.rater1:
        payload, inputs = from_csvs(args)
    else:
        parser.error("pass --from-confusion or --rater1")
    write_result(args.output, payload, inputs=inputs)
    report = payload["veo_vs_rater1"]
    print(f"VEO vs rater 1 (all {report['n']}): accuracy {report['accuracy']:.3f}, kappa {report['kappa']:.3f}, macro-F1 {report['macro_f1']:.3f}")
    selective = report["selective"]
    if selective:
        print(
            f"Committed {selective['n']}/{report['n']} (coverage {report['coverage']:.2f}): accuracy {selective['accuracy']:.3f}, "
            f"kappa {selective['kappa']:.3f}; majority baseline {selective['majority_baseline_accuracy']:.3f}"
        )
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
