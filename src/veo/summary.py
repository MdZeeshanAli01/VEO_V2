"""Render a run's result files into SUMMARY.md, so reported numbers are never typed by hand."""

import json
from pathlib import Path


def _load(path: Path) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _pct(value: float) -> str:
    return f"{100 * value:.1f}%"


def _human(result: dict) -> list[str]:
    report = result["veo_vs_rater1"]
    lines = [
        "## Human agreement",
        "",
        f"- All {report['n']} regions vs rater 1: accuracy {_pct(report['accuracy'])}, κ = {report['kappa']:.3f}, macro-F1 = {report['macro_f1']:.3f}",
    ]
    rater2 = result.get("veo_vs_rater2")
    rater2_kappa = rater2["kappa"] if rater2 else result.get("veo_vs_rater2_kappa")
    if rater2_kappa is not None:
        lines.append(f"- VEO vs rater 2: κ = {rater2_kappa:.3f}")
    if result.get("inter_rater_kappa") is not None:
        lines.append(f"- Inter-rater: κ = {result['inter_rater_kappa']:.3f}")
    selective = report["selective"]
    if selective:
        lines.append(
            f"- Committed {selective['n']}/{report['n']} (abstained {report['abstained']}): accuracy {_pct(selective['accuracy'])}, "
            f"κ = {selective['kappa']:.3f}; majority-class baseline {_pct(selective['majority_baseline_accuracy'])}"
        )
    lines += ["", "| Label | VEO correct / predicted | Rater support |", "|---|---|---|"]
    for label, row in report["per_class"].items():
        lines.append(f"| `{label}` | {row['correct']}/{row['predicted']} | {row['support']} |")
    return lines + [""]


def _model(name: str, summary: dict) -> list[str]:
    total = summary["num_regions"]
    metrics = summary.get("mean_metrics", {})
    lines = [f"## Model: {name}", "", f"- Samples: {summary['num_samples']}, regions: {total:,}"]
    if metrics:
        lines.append(f"- AbsRel {metrics['abs_rel']:.4f}, RMSE {metrics['rmse']:.4f} m, δ1 {metrics['delta1']:.4f}")
    if "mean_failure_pixel_fraction" in summary:
        lines.append(
            f"- Failing pixels: {_pct(summary['mean_failure_pixel_fraction'])} per image on average; "
            f"{_pct(summary['region_pixel_fraction'])} of valid pixels lie in regions; "
            f"{summary['multi_label_regions']:,} regions have more than one label"
        )
    pixel_share = summary.get("top_cause_pixel_fraction", {})
    label_share = summary.get("label_pixel_fraction", {})
    label_counts = summary.get("label_counts", {})
    lines += ["", "| Label | Regions (top label) | Share | Valid pixels (top label) | Regions with label | Valid pixels with label |", "|---|---|---|---|---|---|"]
    labels = set(summary["cause_counts"]) | set(label_counts)
    for label in sorted(labels, key=lambda name: (-summary["cause_counts"].get(name, 0), -label_counts.get(name, 0), name)):
        count = summary["cause_counts"].get(label, 0)
        share = _pct(count / total) if total else "-"
        lines.append(
            f"| `{label}` | {count:,} | {share} | {_pct(pixel_share[label]) if label in pixel_share else '-'} | "
            f"{label_counts.get(label, '-')} | {_pct(label_share[label]) if label in label_share else '-'} |"
        )
    return lines + [""]


def _geometry_agreement(result: dict) -> list[str]:
    lines = [
        "## Ground-truth-free labels (geometry from the aligned prediction)",
        "",
        f"- Same top label as the ground-truth audit on {_pct(result['top_cause_agreement'])} of {result['regions']:,} regions "
        f"(κ = {result['top_cause_kappa']:.3f})",
        "",
        "| Label | Regions (audit) | Regions (prediction only) | Both |",
        "|---|---|---|---|",
    ]
    for label, row in result["per_label"].items():
        lines.append(f"| `{label}` | {row['audit']:,} | {row['prediction_only']:,} | {row['both']:,} |")
    return lines + [""]


def _failure_rules(result: dict) -> list[str]:
    lines = ["## Failure-rule sensitivity", "", "| Rule | Regions | Failing px / image | Top labels (share of regions) |", "|---|---|---|---|"]
    for name, row in result["rules"].items():
        total = row["num_regions"] or 0
        top = ", ".join(f"{label} {_pct(count / total)}" for label, count in sorted(row["cause_counts"].items(), key=lambda item: -item[1])[:3]) if total else "-"
        failing = _pct(row["mean_failure_pixel_fraction"]) if row.get("mean_failure_pixel_fraction") is not None else "-"
        lines.append(f"| {name} | {total:,} | {failing} | {top} |")
    return lines + [""]


def _alignment(result: dict) -> list[str]:
    lines = ["## Alignment protocols", "", "| Protocol | AbsRel | δ1 | s > 0 | s < 0 | mean s ± sd |", "|---|---|---|---|---|---|"]
    for protocol, row in result["summary"].items():
        signs = row["scale_sign_counts"]
        scale = f"{row['mean_scale']:.3f} ± {row['std_scale']:.3f}" if row.get("std_scale") is not None else "-"
        metrics = row["mean_metrics"]
        lines.append(f"| {protocol} | {metrics['abs_rel']:.4f} | {metrics['delta1']:.4f} | {signs['positive']} | {signs['negative']} | {scale} |")
    return lines + [""]


def _ablation(result: dict) -> list[str]:
    lines = ["## Signal ablation", "", "| Signal | Neutral value | Labels changed |", "|---|---|---|"]
    for row in result["rows"]:
        lines.append(f"| `{row['signal']}` | {row['neutral_value']:g} | {row['changed_regions']}/{row['total_regions']} ({_pct(row['changed_fraction'])}) |")
    return lines + [""]


def _sanity(result: dict) -> list[str]:
    if "before" not in result:
        return ["## Scoring sanity check", "", f"- {result.get('skipped', 'not run')}", ""]
    return [
        "## Scoring sanity check (formula only; model not re-run)",
        "",
        f"- {result['sample_id']} region {result['region_id']}: textureless score "
        f"{result['before']['textureless_score']:.3f} → {result['after']['textureless_score']:.3f}",
        "",
    ]


def _oracle(result: dict) -> list[str]:
    mean = result["mean"]
    if not mean:
        return ["## Oracle boundary filter (ground-truth masks)", "", "- No eligible scenes", ""]
    def change(key: str) -> str:
        before, after = mean[f"{key}_before"], mean[f"{key}_after"]
        return f"{before:.4f} → {after:.4f} ({100 * (after - before) / before:+.2f}%)"
    return [
        "## Oracle boundary filter (ground-truth masks; not deployable)",
        "",
        f"- Scenes: {result['evaluated_scenes']}",
        f"- Regional AbsRel {change('region_absrel')}",
        f"- Regional RMSE {change('region_rmse')}",
        f"- Global RMSE {change('global_rmse')}",
        "",
    ]


def write_summary_markdown(results_dir: Path) -> Path:
    """Per-model folders (summary.json, alignment_ablation.json) first, then run-level experiments."""
    lines = [f"# Results: {results_dir.name}", "", "Generated by `veo.summary` from the JSON files in this folder.", ""]
    for model_dir in sorted(path for path in results_dir.iterdir() if path.is_dir()):
        summary = _load(model_dir / "summary.json")
        if summary:
            lines += _model(model_dir.name, summary)
        alignment = _load(model_dir / "alignment_ablation.json")
        if alignment:
            lines += _alignment(alignment)
        rules = _load(model_dir / "failure_rules.json")
        if rules:
            lines += _failure_rules(rules)
        agreement = _load(model_dir / "geometry_agreement.json")
        if agreement and agreement.get("regions"):
            lines += _geometry_agreement(agreement)
    sections = [
        ("human_agreement.json", _human),
        ("signal_ablation.json", _ablation),
        ("scoring_sanity_check.json", _sanity),
        ("oracle_boundary_filter.json", _oracle),
    ]
    for filename, render in sections:
        result = _load(results_dir / filename)
        if result:
            lines += render(result)
    path = results_dir / "SUMMARY.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
