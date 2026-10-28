"""Feature sensitivity ablation: how many region labels change when one feature is set to a neutral value."""

import argparse
import json
from pathlib import Path

from veo.reports import write_result
from veo.validation import NEUTRAL_VALUES, ablation_change


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-path", type=Path, default=Path("outputs/nyu_final/test/model_results.json"))
    parser.add_argument("--output", type=Path, default=Path("results/nyu_test/signal_ablation.json"))
    args = parser.parse_args()

    records = json.loads(args.results_path.read_text(encoding="utf-8"))["records"]
    rows = []
    for signal, neutral in NEUTRAL_VALUES.items():
        counts = ablation_change(records, signal, include_reflection=True)
        total = counts["total_regions"]
        rows.append({
            "signal": signal,
            "neutral_value": neutral,
            **counts,
            "changed_fraction": counts["changed_regions"] / total if total else 0.0,
        })
        print(f"{signal:<22} -> {neutral:<6} changed {counts['changed_regions']:>5}/{total} ({rows[-1]['changed_fraction']:.2%})")
    write_result(args.output, {"rows": rows}, inputs={"veo_results": args.results_path})
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
