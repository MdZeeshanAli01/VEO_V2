import csv
import json
from pathlib import Path
from veo_nyu.validation import ablation_change

def main():
    results_path = Path("outputs/nyu_final/test/model_results.json")
    output_dir = Path("outputs/nyu_final/test")
    
    print("Loading test results from:", results_path)
    data = json.load(results_path.open("r", encoding="utf-8"))
    records = data["records"]
    total_regions = sum(len(r["regions"]) for r in records)
    print(f"Total test failure regions: {total_regions}")

    signals = [
        "texture_var",
        "contrast",
        "brightness",
        "edge_density",
        "highlight_ratio",
        "aspect_ratio",
        "depth_discontinuity",
    ]

    neutral_defaults = {
        "texture_var": "500.0 (High Texture)",
        "contrast": "60.0 (Normal Contrast)",
        "brightness": "128.0 (Mid-Gray)",
        "edge_density": "0.0 (Zero Edges)",
        "highlight_ratio": "0.0 (Zero Highlights)",
        "aspect_ratio": "1.0 (Square BBox)",
        "depth_discontinuity": "0.0 (Flat Depth)",
    }

    rows = []
    print("\n" + "=" * 70)
    print(f"{'Feature Signal':<22} {'Neutral Value':<24} {'Changed':<10} {'Sensitivity (%)':<15}")
    print("=" * 70)

    for signal in signals:
        res = ablation_change(records, signal, include_reflection=True)
        changed = res["changed_regions"]
        total = res["total_regions"]
        pct = (changed / total * 100) if total > 0 else 0.0
        neutral_str = neutral_defaults.get(signal, "-")
        rows.append({
            "signal": signal,
            "neutral_replacement": neutral_str,
            "changed_regions": changed,
            "total_regions": total,
            "sensitivity_percentage": round(pct, 2),
        })
        print(f"{signal:<22} {neutral_str:<24} {changed:<10} {pct:<15.2f}")

    print("=" * 70)

    csv_path = output_dir / "signal_ablation.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["signal", "neutral_replacement", "changed_regions", "total_regions", "sensitivity_percentage"])
        writer.writeheader()
        writer.writerows(rows)

    json_path = output_dir / "signal_ablation.json"
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"\n[OK] Ablation study saved to: {csv_path} and {json_path}\n")

if __name__ == "__main__":
    main()

