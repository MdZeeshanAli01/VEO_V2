> **Errata (phase 0 revision):** some v1 claims were overstated or incorrect. See [ERRATA_V1.md](../docs/ERRATA_V1.md) for the corrections.

# Scripts

Analysis lives in `src/veo` and the per-result experiments live in [`experiments/`](../experiments/). This folder holds presentation tooling only.

| Script | Output | Notes |
|---|---|---|
| `generate_figures.py` | `web_app/assets/fig1..fig3*.png` | Figure 2(a) plots measured per-scene scales from `outputs/alignment_ablation_full/test/alignment_ablation.json` when present, otherwise only the reported sign counts. |
| `site/export_data.py` | `web_app/data/app_data_v2.js` | Needs local NYU data, predictions and the metric checkpoint. |
| `site/build_index.py` | `web_app/index.html` | Static explorer page. |
| `site/build_model_lab.py` | `web_app/model_lab.html` | 3D teaching lab page. |
| `site/generate_video.py` | `web_app/veo_explainer.mp4` | Slide video rendered with OpenCV/PIL. |
| `site/check_server.py` | — | Manual smoke check of `web_app/serve.py` on port 8000 (the automated version is `tests/test_web_server.py`). |
| `run_smoke.ps1` | — | Windows shortcut for `pytest` plus `veo smoke`. |

Run every script from the repository root, for example `uv run python scripts/generate_figures.py`.
