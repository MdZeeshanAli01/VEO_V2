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
from .metrics import compute_error_map
from .pipeline import analyze_sample
from .reports import write_correlations, write_summary
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


def run_model(config: Config, model_id: str, device: str = "auto") -> list[dict]:
    pairs = _pairs(config)
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