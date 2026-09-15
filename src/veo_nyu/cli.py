import argparse
from pathlib import Path

import numpy as np

from .config import Config, DatasetConfig, ExperimentConfig, OutputConfig, load_config
from .data import discover_pairs, validate_pairs
from .pipeline import analyze_sample
from .reports import write_manifest
from .runner import run_model, run_precomputed


def run_smoke() -> None:
    height, width = 48, 64
    rng = np.random.default_rng(42)
    rgb = rng.integers(0, 256, size=(height, width, 3), dtype=np.uint8)
    target = np.full((height, width), 2.0, dtype=np.float32)
    target[:, width // 2:] = 4.0
    prediction = target + rng.normal(0, 0.15, size=target.shape).astype(np.float32)
    prediction[18:30, 28:40] += 1.5
    valid_mask = np.ones_like(target, dtype=bool)
    result = analyze_sample(rgb, target, prediction, valid_mask, ExperimentConfig(min_region_area=5))
    print(f"Smoke test passed: AbsRel={result['metrics']['abs_rel']:.4f}, regions={result['num_regions']}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="veo-nyu")
    parser.add_argument("command", choices=["smoke", "manifest", "run-precomputed", "run-model"])
    parser.add_argument("--config", type=Path, default=Path("configs/nyu.yaml"))
    parser.add_argument("--rgb-dir", type=Path, default=Path("data/nyu/rgb"))
    parser.add_argument("--depth-dir", type=Path, default=Path("data/nyu/depth"))
    parser.add_argument("--prediction-dir", type=Path, default=Path("data/nyu/predictions"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--model-id", default="depth-anything/Depth-Anything-V2-Small-hf")
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    args = parser.parse_args()
    if args.command == "smoke":
        run_smoke()
    elif args.command == "manifest":
        config = load_config(args.config)
        dataset = DatasetConfig(
            name=config.dataset.name,
            rgb_dir=args.rgb_dir,
            depth_dir=args.depth_dir,
            depth_scale=config.dataset.depth_scale,
            max_depth_m=config.dataset.max_depth_m,
            split=config.dataset.split,
        )
        config = Config(dataset=dataset, experiment=config.experiment, outputs=OutputConfig(directory=args.output_dir))
        pairs = discover_pairs(config.dataset.rgb_dir, config.dataset.depth_dir)
        validate_pairs(pairs, config.dataset.rgb_dir, config.dataset.depth_dir)
        manifest_path = config.outputs.directory / f"{config.dataset.split}_manifest.json"
        write_manifest(pairs, manifest_path, config.dataset.split)
        print(f"Manifest created for {len(pairs)} samples: {manifest_path}")
    elif args.command == "run-precomputed":
        config = load_config(args.config)
        config = Config(
            dataset=DatasetConfig(rgb_dir=args.rgb_dir, depth_dir=args.depth_dir, depth_scale=config.dataset.depth_scale, max_depth_m=config.dataset.max_depth_m, split=config.dataset.split),
            experiment=config.experiment,
            outputs=OutputConfig(directory=args.output_dir),
        )
        records = run_precomputed(config, args.prediction_dir)
        print(f"Processed {len(records)} NYU samples. Results: {args.output_dir / 'precomputed_results.json'}")
    elif args.command == "run-model":
        config = load_config(args.config)
        config = Config(
            dataset=DatasetConfig(rgb_dir=args.rgb_dir, depth_dir=args.depth_dir, depth_scale=config.dataset.depth_scale, max_depth_m=config.dataset.max_depth_m, split=config.dataset.split),
            experiment=config.experiment,
            outputs=OutputConfig(directory=args.output_dir),
        )
        records = run_model(config, args.model_id, args.device)
        print(f"Processed {len(records)} NYU samples. Results: {args.output_dir / 'model_results.json'}")


if __name__ == "__main__":
    main()
