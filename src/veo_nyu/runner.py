import json
from dataclasses import asdict
from pathlib import Path

from .config import Config
from .data import discover_pairs, load_depth, load_rgb, make_valid_mask, validate_pairs
from .inference import PrecomputedPredictor
from .metrics import compute_error_map
from .pipeline import analyze_sample
from .reports import write_correlations, write_summary
from .visualization import save_panel


def run_precomputed(config: Config, prediction_dir: Path) -> list[dict]:
    pairs = discover_pairs(config.dataset.rgb_dir, config.dataset.depth_dir)
    validate_pairs(pairs)
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