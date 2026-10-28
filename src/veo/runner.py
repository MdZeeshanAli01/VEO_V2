import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from .config import Config
from .data import (
    discover_manifest,
    discover_pairs,
    load_depth,
    load_rgb,
    make_valid_mask,
    validate_pairs,
)


def _pairs(config: Config):
    pairs = discover_manifest(config.dataset.manifest) if config.dataset.manifest else discover_pairs(config.dataset.rgb_dir, config.dataset.depth_dir)
    validate_pairs(pairs, config.dataset.rgb_dir, config.dataset.depth_dir)
    return pairs
from .inference import (
    OfficialMetricDepthPredictor,
    PrecomputedPredictor,
    TransformersDepthPredictor,
)
from .metrics import align_scale_only, align_scale_shift, compute_error_map, compute_metrics
from .pipeline import analyze_sample
from .reports import write_correlations, write_summary
from .regions import extract_failure_regions
from .visualization import save_panel


def run_precomputed(config: Config, prediction_dir: Path) -> list[dict]:
    pairs = _pairs(config)
    predictor = PrecomputedPredictor(prediction_dir)
    records = []
    for pair in pairs:
        rgb = load_rgb(pair.rgb_path)
        target = load_depth(pair.depth_path, config.dataset.depth_scale)
        if target.shape != rgb.shape[:2]:
            raise ValueError(f"RGB/depth shape mismatch for {pair.sample_id}: {rgb.shape[:2]} vs {target.shape}")
        valid_mask = make_valid_mask(target, config.dataset.max_depth_m)
        prediction = predictor.predict_for_sample(pair.sample_id, target.shape)
        result = analyze_sample(rgb, target, prediction, valid_mask, config.experiment)
        records.append({"sample_id": pair.sample_id, **result})
        error_map = compute_error_map(prediction, target, valid_mask)
        save_panel(rgb, target, prediction, error_map, config.outputs.directory / "panels" / f"{pair.sample_id}.png", pair.sample_id)
    output_dir = config.outputs.directory
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "precomputed_results.json"
    output_path.write_text(json.dumps({"config": asdict(config), "records": records}, default=str, indent=2), encoding="utf-8")
    write_summary(records, output_dir)
    write_correlations(records, output_dir / "correlations.csv")
    return records


def run_model(config: Config, model_id: str, device: str = "auto", limit: int | None = None) -> list[dict]:
    pairs = _pairs(config)
    if limit is not None:
        pairs = pairs[:limit]
    predictor = TransformersDepthPredictor(model_id, device)
    output_dir = config.outputs.directory
    prediction_dir = output_dir / "predictions"
    prediction_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for pair in pairs:
        rgb = load_rgb(pair.rgb_path)
        target = load_depth(pair.depth_path, config.dataset.depth_scale)
        if target.shape != rgb.shape[:2]:
            raise ValueError(f"RGB/depth shape mismatch for {pair.sample_id}: {rgb.shape[:2]} vs {target.shape}")
        valid_mask = make_valid_mask(target, config.dataset.max_depth_m)
        prediction = predictor.predict(rgb)
        np.save(prediction_dir / f"{pair.sample_id}.npy", prediction)
        result = analyze_sample(rgb, target, prediction, valid_mask, config.experiment)
        records.append({"sample_id": pair.sample_id, **result})
        error_map = compute_error_map(prediction, target, valid_mask)
        save_panel(rgb, target, prediction, error_map, output_dir / "panels" / f"{pair.sample_id}.png", pair.sample_id)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "model_results.json"
    output_path.write_text(json.dumps({"model_id": model_id, "config": asdict(config), "records": records}, default=str, indent=2), encoding="utf-8")
    write_summary(records, output_dir)
    write_correlations(records, output_dir / "correlations.csv")
    return records


def run_official_metric(config: Config, official_repo: Path, checkpoint: Path, encoder: str, max_depth: float, device: str = "auto") -> list[dict]:
    pairs = _pairs(config)
    predictor = OfficialMetricDepthPredictor(official_repo, checkpoint, encoder, max_depth, device)
    output_dir = config.outputs.directory
    prediction_dir = output_dir / "predictions"
    prediction_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for pair in pairs:
        rgb = load_rgb(pair.rgb_path)
        target = load_depth(pair.depth_path, config.dataset.depth_scale)
        if target.shape != rgb.shape[:2]:
            raise ValueError(f"RGB/depth shape mismatch for {pair.sample_id}: {rgb.shape[:2]} vs {target.shape}")
        valid_mask = make_valid_mask(target, max_depth)
        prediction = predictor.predict(rgb)
        np.save(prediction_dir / f"{pair.sample_id}.npy", prediction)
        result = analyze_sample(rgb, target, prediction, valid_mask, config.experiment)
        records.append({"sample_id": pair.sample_id, **result})
        save_panel(rgb, target, prediction, compute_error_map(prediction, target, valid_mask), output_dir / "panels" / f"{pair.sample_id}.png", pair.sample_id)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "official_metric_results.json").write_text(json.dumps({"model": f"metric_hypersim_{encoder}", "config": asdict(config), "records": records}, default=str, indent=2), encoding="utf-8")
    write_summary(records, output_dir)
    write_correlations(records, output_dir / "correlations.csv")
    return records


def _scale_sign(scale: float | None) -> str:
    if scale is None:
        return "not_fitted"
    if scale > 0:
        return "positive"
    if scale < 0:
        return "negative"
    return "zero"


def _evaluate_alignment_protocol(
    prediction: np.ndarray,
    target: np.ndarray,
    valid_mask: np.ndarray,
    protocol: str,
) -> dict:
    evaluated, scale, shift, space = _aligned_prediction(prediction, target, valid_mask, protocol)
    return {
        "protocol": protocol,
        "metrics": compute_metrics(evaluated, target, valid_mask),
        "alignment": {
            "scale": scale,
            "shift": shift,
            "scale_sign": _scale_sign(scale),
            "prediction_space": space,
        },
    }


def _aligned_prediction(
    prediction: np.ndarray,
    target: np.ndarray,
    valid_mask: np.ndarray,
    protocol: str,
) -> tuple[np.ndarray, float | None, float | None, str]:
    if protocol == "none":
        evaluated = prediction.astype(np.float32)
        scale, shift, space = None, None, "raw_inverse_depth"
    elif protocol == "direct_depth_scale_shift":
        evaluated, scale, shift = align_scale_shift(prediction, target, valid_mask, "depth")
        space = "depth"
    elif protocol == "inverse_depth_scale_shift":
        evaluated, scale, shift = align_scale_shift(prediction, target, valid_mask, "inverse_depth")
        space = "inverse_depth"
    elif protocol == "inverse_depth_scale_only":
        evaluated, scale = align_scale_only(prediction, target, valid_mask, "inverse_depth")
        shift, space = 0.0, "inverse_depth"
    else:
        raise ValueError(f"Unknown alignment protocol: {protocol}")
    return evaluated, scale, shift, space


def _scene_lookup(config: Config) -> dict[str, str]:
    metadata_path = config.dataset.depth_dir.parent / "metadata.json"
    if not metadata_path.exists():
        return {}
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    return {record["sample_id"]: record["scene"] for record in metadata}


def _bootstrap_mean_ci(records: list[dict], metric: str, scene_lookup: dict[str, str], seed: int, replicates: int = 1000) -> dict[str, float]:
    grouped: dict[str, list[float]] = {}
    for record in records:
        grouped.setdefault(scene_lookup.get(record["sample_id"], record["sample_id"]), []).append(record[metric])
    scenes = sorted(grouped)
    if not scenes:
        return {"lower": float("nan"), "upper": float("nan")}
    scene_means = np.asarray([np.mean(grouped[scene]) for scene in scenes], dtype=float)
    generator = np.random.default_rng(seed)
    samples = generator.integers(0, len(scene_means), size=(replicates, len(scene_means)))
    bootstrap_means = scene_means[samples].mean(axis=1)
    return {"lower": float(np.percentile(bootstrap_means, 2.5)), "upper": float(np.percentile(bootstrap_means, 97.5))}


def _region_sensitivity(
    prediction: np.ndarray,
    target: np.ndarray,
    valid_mask: np.ndarray,
    protocol: str,
    percentiles: tuple[float, ...],
    min_area: int,
) -> dict[str, dict[str, float]]:
    evaluated, _, _, _ = _aligned_prediction(prediction, target, valid_mask, protocol)
    error_map = compute_error_map(evaluated, target, valid_mask)
    result = {}
    for percentile in percentiles:
        regions = extract_failure_regions(error_map, valid_mask, percentile, min_area)
        region_pixels = sum(region["area"] for region in regions)
        result[str(int(percentile))] = {
            "num_regions": float(len(regions)),
            "region_pixels": float(region_pixels),
            "mean_region_area": float(region_pixels / len(regions)) if regions else 0.0,
        }
    return result


def run_alignment_ablation(
    config: Config,
    model_id: str,
    device: str = "auto",
    limit: int | None = None,
    start: int = 0,
) -> dict:
    pairs = _pairs(config)
    if start < 0:
        raise ValueError("start must be non-negative")
    pairs = pairs[start:]
    if limit is not None:
        pairs = pairs[:limit]
    predictor = TransformersDepthPredictor(model_id, device)
    protocols = (
        "none",
        "direct_depth_scale_shift",
        "inverse_depth_scale_shift",
        "inverse_depth_scale_only",
    )
    if config.experiment.primary_protocol not in protocols:
        raise ValueError(f"Unsupported primary protocol: {config.experiment.primary_protocol}")
    sensitivity_percentiles = (75.0, 85.0, 90.0, 95.0)
    scene_lookup = _scene_lookup(config)
    records = []
    prediction_dir = config.outputs.directory / "predictions"
    prediction_dir.mkdir(parents=True, exist_ok=True)

    def append_record(pair, rgb, target, prediction):
        valid_mask = make_valid_mask(target, config.dataset.max_depth_m)
        protocol_results = {
            protocol: _evaluate_alignment_protocol(prediction, target, valid_mask, protocol)
            for protocol in protocols
        }
        records.append({
            "sample_id": pair.sample_id,
            "scene": scene_lookup.get(pair.sample_id, pair.sample_id),
            "protocols": protocol_results,
            "region_sensitivity": {
                "direct_depth_scale_shift": _region_sensitivity(
                    prediction, target, valid_mask, "direct_depth_scale_shift", sensitivity_percentiles, config.experiment.min_region_area
                ),
                "inverse_depth_scale_shift": _region_sensitivity(
                    prediction, target, valid_mask, "inverse_depth_scale_shift", sensitivity_percentiles, config.experiment.min_region_area
                ),
            },
        })

    pending = []
    for pair in pairs:
        rgb = load_rgb(pair.rgb_path)
        target = load_depth(pair.depth_path, config.dataset.depth_scale)
        if target.shape != rgb.shape[:2]:
            raise ValueError(f"RGB/depth shape mismatch for {pair.sample_id}: {rgb.shape[:2]} vs {target.shape}")
        cached_path = prediction_dir / f"{pair.sample_id}.npy"
        if cached_path.exists():
            prediction = np.asarray(np.load(cached_path), dtype=np.float32)
            if prediction.shape != target.shape:
                raise ValueError(f"Cached prediction {cached_path} has shape {prediction.shape}; expected {target.shape}")
            append_record(pair, rgb, target, prediction)
        else:
            pending.append((pair, rgb, target))

    for start in range(0, len(pending), 4):
        batch = pending[start:start + 4]
        rgb_batch = [item[1] for item in batch]
        if hasattr(predictor, "predict_batch"):
            predictions = predictor.predict_batch(rgb_batch, batch_size=4)
        else:
            predictions = [predictor.predict(rgb) for rgb in rgb_batch]
        for (pair, rgb, target), prediction in zip(batch, predictions):
            np.save(prediction_dir / f"{pair.sample_id}.npy", prediction)
            append_record(pair, rgb, target, prediction)
    summary = {}
    for protocol in protocols:
        protocol_records = [record["protocols"][protocol] for record in records]
        summary[protocol] = {
            "num_samples": len(protocol_records),
            "mean_metrics": {
                name: float(np.mean([record["metrics"][name] for record in protocol_records]))
                for name in ("mae", "rmse", "abs_rel", "sq_rel", "delta1", "delta2", "delta3", "spearman")
            } if protocol_records else {},
            "scale_sign_counts": {
                sign: sum(record["alignment"]["scale_sign"] == sign for record in protocol_records)
                for sign in ("positive", "negative", "zero", "not_fitted")
            },
            "mean_scale": float(np.mean([
                record["alignment"]["scale"]
                for record in protocol_records
                if record["alignment"]["scale"] is not None
            ])) if any(record["alignment"]["scale"] is not None for record in protocol_records) else None,
            "bootstrap_ci95": {
                name: _bootstrap_mean_ci(
                    [{"sample_id": item["sample_id"], name: item["protocols"][protocol]["metrics"][name]} for item in records],
                    name,
                    scene_lookup,
                    config.experiment.random_seed,
                )
                for name in ("mae", "rmse", "abs_rel", "sq_rel", "delta1", "delta2", "delta3", "spearman")
            },
        }
    paired_differences = []
    for record in records:
        sample_differences = {"sample_id": record["sample_id"], "scene": record["scene"], "metrics": {}}
        for left_index, left in enumerate(protocols):
            for right in protocols[left_index + 1:]:
                key = f"{left}_minus_{right}"
                sample_differences["metrics"][key] = {
                    name: record["protocols"][left]["metrics"][name] - record["protocols"][right]["metrics"][name]
                    for name in ("mae", "rmse", "abs_rel", "sq_rel", "delta1", "delta2", "delta3", "spearman")
                }
        paired_differences.append(sample_differences)
    region_comparison = {}
    for percentile in sensitivity_percentiles:
        key = str(int(percentile))
        direct = [record["region_sensitivity"]["direct_depth_scale_shift"][key] for record in records]
        inverse = [record["region_sensitivity"]["inverse_depth_scale_shift"][key] for record in records]
        region_comparison[key] = {
            "mean_direct_regions": float(np.mean([item["num_regions"] for item in direct])) if direct else 0.0,
            "mean_inverse_regions": float(np.mean([item["num_regions"] for item in inverse])) if inverse else 0.0,
            "mean_direct_region_area": float(np.mean([item["mean_region_area"] for item in direct])) if direct else 0.0,
            "mean_inverse_region_area": float(np.mean([item["mean_region_area"] for item in inverse])) if inverse else 0.0,
        }
    output_dir = config.outputs.directory
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "model_id": model_id,
        "config": asdict(config),
        "primary_protocol": config.experiment.primary_protocol,
        "protocols": protocols,
        "records": records,
        "summary": summary,
        "paired_differences": paired_differences,
        "region_comparison": region_comparison,
        "causal_claims": False,
    }
    (output_dir / "alignment_ablation.json").write_text(json.dumps(payload, default=str, indent=2), encoding="utf-8")
    return payload