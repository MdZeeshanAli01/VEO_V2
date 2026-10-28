"""One command from raw data to a results folder: splits, predictions, analysis, experiments, summary.

``fixture=True`` runs every stage on a small synthetic NYU-format dataset with a synthetic predictor,
so the pipeline can be checked end to end without downloads or a GPU.
"""

import json
import os
import shutil
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

from .config import Config, DatasetConfig, OutputConfig, load_config
from .data import discover_manifest, load_depth
from .fixtures import SyntheticDisparityPredictor, write_fixture_mat
from .nyu_dataset import create_scene_splits, extract_split
from .reports import write_result
from .runner import run_alignment_ablation, run_model, run_pairs
from .summary import write_summary_markdown

REPO_ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS = REPO_ROOT / "experiments"
FIXTURE_MODEL = "synthetic-disparity"


def _slug(model_id: str) -> str:
    return model_id.split("/")[-1].lower()


def prepare_test_split(mat_path: Path, split_root: Path, seed: int) -> Path:
    """Extract the scene-disjoint test split with its manifest and scene metadata."""
    records = create_scene_splits(mat_path, seed)["test"]
    split_dir = split_root / "test"
    extract_split(mat_path, records, split_dir)
    (split_dir / "metadata.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    lines = [f"{split_dir / 'rgb' / record['sample_id']}.png {split_dir / 'depth' / record['sample_id']}.npy" for record in records]
    (split_dir / "manifest.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return split_dir


def _split_config(base: Config, split_dir: Path, output_dir: Path) -> Config:
    dataset = DatasetConfig(
        name=base.dataset.name,
        rgb_dir=split_dir / "rgb",
        depth_dir=split_dir / "depth",
        manifest=split_dir / "manifest.txt",
        depth_scale=base.dataset.depth_scale,
        max_depth_m=base.dataset.max_depth_m,
        split=base.dataset.split,
    )
    return replace(base, dataset=dataset, outputs=OutputConfig(directory=output_dir))


def _run_experiment(script: str, *args: str | Path) -> None:
    env = {**os.environ, "PYTHONPATH": os.pathsep.join(filter(None, [str(REPO_ROOT / "src"), os.environ.get("PYTHONPATH")]))}
    subprocess.run([sys.executable, str(EXPERIMENTS / script), *map(str, args)], check=True, env=env)


def _slim_alignment(payload: dict) -> dict:
    """Keep the summary and per-scene scales; drop per-sample metric dumps."""
    scales = [
        {
            "sample_id": record["sample_id"],
            "direct_depth_scale": record["protocols"]["direct_depth_scale_shift"]["alignment"]["scale"],
            "inverse_depth_scale": record["protocols"]["inverse_depth_scale_shift"]["alignment"]["scale"],
        }
        for record in payload["records"]
    ]
    return {"model_id": payload["model_id"], "summary": payload["summary"], "region_comparison": payload["region_comparison"], "per_scene_scales": scales}


def reproduce(
    workdir: Path,
    config_path: Path,
    fixture: bool = False,
    mat_path: Path | None = None,
    model_ids: tuple[str, ...] = ("depth-anything/Depth-Anything-V2-Small-hf",),
    rater1: Path | None = None,
    rater2: Path | None = None,
    device: str = "auto",
    seed: int = 42,
) -> Path:
    run_name = "fixture" if fixture else "nyu_test"
    outputs = workdir / "outputs" / run_name
    results = workdir / "results" / run_name
    if results.exists():
        shutil.rmtree(results)
    results.mkdir(parents=True)

    if fixture:
        mat_path = write_fixture_mat(outputs / "nyu_fixture.mat", scenes=12)
        model_ids = (FIXTURE_MODEL,)
    elif mat_path is None or not mat_path.exists():
        raise FileNotFoundError(f"NYU labelled .mat not found at {mat_path}. Download it with: veo download-nyu")
    print(f"[1/4] Extracting scene-disjoint test split from {mat_path}")
    split_dir = prepare_test_split(mat_path, outputs / "splits", seed)

    base = load_config(config_path)
    primary_results = None
    for model_id in model_ids:
        slug = _slug(model_id)
        config = _split_config(base, split_dir, outputs / slug)
        print(f"[2/4] Predicting and analyzing with {model_id}")
        if fixture:
            predictor = SyntheticDisparityPredictor(seed)
            pairs = discover_manifest(config.dataset.manifest)
            run_pairs(
                config,
                pairs,
                lambda pair, rgb, shape, predictor=predictor, scale=config.dataset.depth_scale: predictor.predict(rgb, load_depth(pair.depth_path, scale)),
                "model_results.json",
                {"model_id": model_id},
                save_predictions=True,
            )
        else:
            run_model(config, model_id, device)
        alignment = run_alignment_ablation(config, model_id, device)  # reuses the cached predictions
        model_results = results / slug
        model_results.mkdir()
        shutil.copyfile(config.outputs.directory / "summary.json", model_results / "summary.json")
        write_result(model_results / "alignment_ablation.json", _slim_alignment(alignment), config)
        primary_results = primary_results or (config.outputs.directory / "model_results.json")

    print("[3/4] Running experiments on the primary model")
    primary_predictions = primary_results.parent / "predictions"
    _run_experiment("signal_ablation.py", "--results-path", primary_results, "--output", results / "signal_ablation.json")
    _run_experiment(
        "scoring_sanity_check.py", "--results-path", primary_results, "--rgb-dir", split_dir / "rgb",
        "--depth-dir", split_dir / "depth", "--output", results / "scoring_sanity_check.json",
    )
    _run_experiment(
        "oracle_boundary_filter.py", "--results-path", primary_results, "--prediction-dir", primary_predictions,
        "--depth-dir", split_dir / "depth", "--output", results / "oracle_boundary_filter.json",
    )
    if rater1:
        args = ["--rater1", rater1, "--results-path", primary_results, "--output", results / "human_agreement.json"]
        _run_experiment("human_agreement.py", *args, *(["--rater2", rater2] if rater2 else []))

    print("[4/4] Writing summary")
    summary = write_summary_markdown(results)
    print(f"Done: {summary}")
    return summary
