import argparse
from pathlib import Path

import numpy as np

from .config import Config, DatasetConfig, ExperimentConfig, OutputConfig, load_config
from .data import discover_manifest, discover_pairs, validate_pairs
from .pipeline import analyze_sample
from .reports import write_manifest
from .runner import run_model, run_official_metric, run_precomputed


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


def configured(args, config: Config, max_depth: float | None = None) -> Config:
    dataset = DatasetConfig(
        name=config.dataset.name,
        rgb_dir=args.rgb_dir or config.dataset.rgb_dir,
        depth_dir=args.depth_dir or config.dataset.depth_dir,
        manifest=args.manifest if args.manifest else config.dataset.manifest,
        depth_scale=config.dataset.depth_scale,
        max_depth_m=max_depth if max_depth is not None else config.dataset.max_depth_m,
        split=config.dataset.split,
    )
    return Config(dataset=dataset, experiment=config.experiment, outputs=OutputConfig(directory=args.output_dir or config.outputs.directory))


def main() -> None:
    parser = argparse.ArgumentParser(prog="veo-nyu")
    parser.add_argument("command", choices=["smoke", "manifest", "run-precomputed", "run-model", "run-official-metric"])
    parser.add_argument("--config", type=Path, default=Path("configs/nyu.yaml"))
    parser.add_argument("--rgb-dir", type=Path)
    parser.add_argument("--depth-dir", type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--prediction-dir", type=Path, default=Path("data/nyu/predictions"))
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--model-id", default="depth-anything/Depth-Anything-V2-Small-hf")
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    parser.add_argument("--official-repo", type=Path, default=Path("official/Depth-Anything-V2"))
    parser.add_argument("--checkpoint", type=Path, default=Path("checkpoints/depth_anything_v2_metric_hypersim_vits.pth"))
    parser.add_argument("--encoder", choices=["vits", "vitb", "vitl"], default="vits")
    parser.add_argument("--max-depth", type=float, default=20.0)
    args = parser.parse_args()
    if args.command == "smoke":
        run_smoke()
    elif args.command == "manifest":
        config = load_config(args.config)
        config = configured(args, config)
        pairs = discover_manifest(config.dataset.manifest) if config.dataset.manifest else discover_pairs(config.dataset.rgb_dir, config.dataset.depth_dir)
        validate_pairs(pairs, config.dataset.rgb_dir, config.dataset.depth_dir)
        manifest_path = config.outputs.directory / f"{config.dataset.split}_manifest.json"
        write_manifest(pairs, manifest_path, config.dataset.split)
        print(f"Manifest created for {len(pairs)} samples: {manifest_path}")
    elif args.command == "run-precomputed":
        config = load_config(args.config)
        config = configured(args, config)
        records = run_precomputed(config, args.prediction_dir)
        print(f"Processed {len(records)} NYU samples. Results: {args.output_dir / 'precomputed_results.json'}")
    elif args.command == "run-model":
        config = load_config(args.config)
        config = configured(args, config)
        records = run_model(config, args.model_id, args.device)
        print(f"Processed {len(records)} NYU samples. Results: {args.output_dir / 'model_results.json'}")
    elif args.command == "run-official-metric":
        config = load_config(args.config)
        config = configured(args, config, args.max_depth)
        config = Config(dataset=config.dataset, experiment=ExperimentConfig(**{**config.experiment.__dict__, "model_name": f"metric_hypersim_{args.encoder}", "align_scale_shift": False}), outputs=config.outputs)
        records = run_official_metric(config, args.official_repo, args.checkpoint, args.encoder, args.max_depth, args.device)
        print(f"Processed {len(records)} samples. Results: {args.output_dir / 'official_metric_results.json'}")


if __name__ == "__main__":
    main()
