# VEO NYU

A clean, reproducible implementation of the Vision Error Observatory for the NYU Depth V2 dataset.

VEO NYU diagnoses *where* a monocular depth model fails and records measurable evidence for possible causes. It does not train a new depth model.

## Pipeline

1. Discover aligned NYU RGB/depth pairs.
2. Load dense depth in meters and construct an invalid-depth mask.
3. Accept a model prediction, optionally align it to ground truth, and compute masked metrics.
4. Localize high-error pixels and connected failure regions.
5. Extract region evidence from RGB and depth.
6. Assign interpretable rule-based cause scores and confidence.
7. Save run metadata, metrics, regions, and validation-ready records.

## Project layout

- `veo_nyu/`: reusable pipeline code
- `scripts/`: command-line entry points
- `configs/`: experiment configuration
- `tests/`: unit and smoke tests
- `data/`: local dataset mount point, excluded from git
- `outputs/`: generated results, excluded from git
- `notebooks/`: optional inspection notebooks only

## Setup on Windows PowerShell

```powershell
uv sync --extra dev
```

The repository-level `.venv` is the preferred interpreter for this workspace. Create it first if it does not exist:

```powershell
uv venv
```

## Smoke test

```powershell
uv run pytest -q
uv run veo-nyu smoke
```

## Run on precomputed NYU predictions

Place aligned files using the same sample ID in each directory:

```text
data/nyu/rgb/scene_0001.png
data/nyu/depth/scene_0001.png
data/nyu/predictions/scene_0001.npy
```

Then run:

```powershell
uv run veo-nyu run-precomputed
```

The command validates dimensions, evaluates only valid NYU depth pixels, extracts failure regions, classifies them, and writes `outputs/precomputed_results.json`. Custom directories can be supplied with `--rgb-dir`, `--depth-dir`, `--prediction-dir`, and `--output-dir`.

The optional model adapter is available through `TransformersDepthPredictor`. Install it with `pip install -e ".[model]"`; model inference remains separate from diagnosis so experiments can compare multiple predictors consistently.

To run Depth Anything V2 directly after installing the model extra:

```powershell
uv sync --extra dev --extra model
uv run veo-nyu run-model --model-id depth-anything/Depth-Anything-V2-Small-hf
```

This downloads the model from Hugging Face on first use, saves predictions under `outputs/predictions/`, and writes `outputs/model_results.json`.

## NYU data contract

The pipeline expects a directory containing matching files such as:

```text
data/nyu/rgb/scene_0001.png
data/nyu/depth/scene_0001.png
```

Depth PNG values are interpreted as `raw_value / depth_scale` meters. The default scale is 1000 for millimetre-encoded depth. `.npy` depth arrays are treated as metres by default. Use `configs/nyu.yaml` to set the exact split, scale, maximum depth, and experiment thresholds.

Do not use KITTI sparse-depth assumptions in this project. NYU evaluation is dense but still requires an explicit invalid-depth policy and a documented maximum evaluation depth.

## Official training-aligned profile

The official Depth Anything V2 repository distinguishes relative depth models from metric-depth models. The official indoor metric checkpoint used by this project is:

```text
Depth-Anything-V2-Metric-Hypersim-Small
```

It is fine-tuned on the synthetic Hypersim dataset, uses a 20 metre maximum depth, and produces metric depth in metres. NYU Depth V2 is not the training dataset for this checkpoint; NYU is an external indoor evaluation option.

The official source repository is cloned locally at `official/Depth-Anything-V2` and the checkpoint is stored locally at `checkpoints/`. Both are ignored by Git because they are external source/large binary assets.

After downloading the original Hypersim release and creating an official two-column manifest (`RGB_PATH DEPTH_HDF5_PATH` per line), run:

```powershell
uv run veo-nyu run-official-metric `
	--config configs/hypersim.yaml `
	--manifest data/hypersim/manifest.txt `
	--checkpoint checkpoints/depth_anything_v2_metric_hypersim_vits.pth `
	--official-repo official/Depth-Anything-V2 `
	--encoder vits `
	--max-depth 20 `
	--device cpu
```

The official Hypersim depth files are HDF5 distance maps. VEO applies the same official distance-to-depth conversion used by Depth Anything V2 before evaluating regions.

## Current status

The initial implementation validates the data contract, masked metrics, region extraction, evidence scoring, manifests, visual panels, aggregate summaries, and correlation exports. Human labels can be added to `outputs/regions.csv` for agreement analysis in the next research stage.
