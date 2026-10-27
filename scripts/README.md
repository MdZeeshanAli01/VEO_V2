# Reproduction & Validation Scripts

This directory contains standalone, reproducible Python scripts that generate all empirical tables, ablation results, validation metrics, and publication figures presented in the VEO research paper.

---

## Script Inventory

| Script | Outputs Produced | Target Paper Table / Figure | Description |
| :--- | :--- | :---: | :--- |
| **`generate_paper_figures.py`** | `figures/fig1_veo_architecture.png`<br>`figures/fig2_polarity_and_fingerprints.png`<br>`figures/fig3_intervention_and_downstream.png` | **Fig. 1**<br>**Fig. 2**<br>**Fig. 3** | Renders 300-DPI high-resolution publication figures: Modular architecture diagram, scale polarity reversal & failure fingerprints, and faithfulness intervention & downstream refinement plots. |
| **`build_final_word_paper.py`** | `paper/VEO_conference_paper.docx`<br>`VEO_conference_paper.docx`<br>`VEO_conference_paper_final.docx` | **Full Manuscript** (Tables I–IX, Figs 1–3) | Compiles the complete 10-section IEEE conference paper into `.docx` format with custom OpenXML bookmarks (`ref_1`–`ref_51`), clickable in-text citations, padded booktabs tables, and embedded 300-DPI figures. |
| **`compute_human_agreement.py`** | `outputs/rating_set_test_50/human_validation_results.json` | **Table VII** | Ingests independent expert Excel annotations (`rating_1.csv.xlsx`, `rating_2.csv.xlsx`), parses multi-rater ratings across 50 failure regions, and computes inter-annotator & model-annotator Cohen's $\kappa$, raw percentage agreement, and per-class precision/recall/F1 metrics. |
| **`run_signal_ablation.py`** | `outputs/nyu_final/test/signal_ablation.csv`<br>`outputs/nyu_final/test/signal_ablation.json` | **Table VIII** | Performs full feature-signal sensitivity ablation across all 5,236 held-out test failure regions by replacing each signal with neutral reference values and quantifying classification flip rates. |
| **`run_faithfulness_intervention.py`** | `outputs/nyu_final/test/intervention_faithfulness.json` | **Section VI-C, Fig. 3a** | Executes controlled image-level counterfactual perturbations (synthetic high-frequency texture noise injection into `scene_0049` Region 8) to prove explanation faithfulness. |
| **`run_downstream_improvement.py`** | `outputs/nyu_final/test/downstream_improvement.json`<br>`outputs/nyu_final/test/downstream_improvement_samples.csv` | **Table IX, Fig. 3b** | Applies VEO mask-guided edge-preserving bilateral filtering to 207 boundary failure test scenes, measuring regional RMSE/AbsRel error reductions against global ground truth. |
| **`generate_explainer_video.py`** | `web_app/veo_explainer.mp4`<br>`outputs/veo_explainer_video.mp4` | **Executive Presentation Video** | Generates high-definition 720p HD MP4 video with smooth transitions explaining the Pain Point, Observability Gaps, Polarity Reversal, and VEO 5 Modules. |
| **`export_web_app_data.py`** | `web_app/data/app_data.json` | **Interactive Web App Asset** | Extracts real test scenes (`scene_0049`, `scene_0051`, `scene_0052`), aligns depth maps, generates relative error maps, and formats region features and formulas into JSON. |
| **`build_web_app.py`** | `web_app/index.html` | **Interactive Diagnostic Platform** | Compiles the standalone interactive web dashboard with embedded data, 4-view multi-modal grid, live mathematical formula calculations, ambiguity gate checker, and intervention sandbox. |
| **`run_smoke.ps1`** | Terminal test logs | Smoke verification | PowerShell smoke test utility to verify inference and evaluation pipelines on minimal test subsets. |

---

## Execution Guide

All scripts are configured to run within the project's isolated `uv` virtual environment:

```bash
# 1. Generate all 300-DPI publication figures
uv run python scripts/generate_paper_figures.py

# 2. Generate executive 720p explainer video
uv run python scripts/generate_explainer_video.py

# 3. Export web application data and compile index.html
uv run python scripts/export_web_app_data.py
uv run python scripts/build_web_app.py

# 4. Run signal sensitivity ablation across all 5,236 test regions
uv run python scripts/run_signal_ablation.py

# 5. Verify explanation faithfulness via controlled image intervention
uv run python scripts/run_faithfulness_intervention.py

# 6. Evaluate downstream boundary refinement on 207 test scenes
uv run python scripts/run_downstream_improvement.py

# 7. Compute blinded multi-rater human agreement
uv run python scripts/compute_human_agreement.py

# 8. Compile the final IEEE Word conference paper
uv run python scripts/build_final_word_paper.py
```

