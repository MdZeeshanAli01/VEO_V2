# Publication Figures

This directory contains high-resolution (300 DPI) figures generated for the VEO conference manuscript.

---

## Figure Index

| Figure | Filename | Description | Method / Source |
| :--- | :--- | :--- | :--- |
| **Fig. 1** | **`fig1_veo_architecture.png`** | **End-to-End Modular Diagnostic Architecture of VEO:** Illustrates the complete pipeline from RGB-D inputs through Module M1 (Scale-Shift Alignment), Module M2 (Dense Error Maps), Module M3 (Region Segmentation), Module M4 (Evidence Extraction), and Module M5 (Rule-Based Attribution & Calibrated Ambiguity Gate), leading to downstream applications. | Rendered via `scripts/generate_paper_figures.py`. *[Note: Architecture diagram generated using AI visualization tools]* |
| **Fig. 2** | **`fig2_polarity_and_fingerprints.png`** | **Empirical Proof of Polarity Reversal & Cross-Model Failure Fingerprinting:**<br>*(a)* Fitted scale slopes across 244 NYU Depth V2 test scenes showing direct depth regression causes $s < 0$ (polarity reversal) in 244/244 scenes vs. strictly positive slopes in inverse-depth alignment ($s > 0$).<br>*(b)* Comparative failure category prevalence (%) between Depth Anything V2 Small (5,236 regions) and DPT-Hybrid-MiDaS (3,689 regions). | Grounded in empirical results from `outputs/alignment_ablation_full/` and `outputs/second_model_dpt_hybrid_midas/`. Rendered via `scripts/generate_paper_figures.py`. |
| **Fig. 3** | **`fig3_intervention_and_downstream.png`** | **Explanation Faithfulness Intervention & Downstream Error Refinement:**<br>*(a)* Controlled synthetic texture injection on `scene_0049` Region 8 showing texture variance rise ($176.82 \to 689.39$) and textureless score collapse ($0.6464 \to 0.0000$).<br>*(b)* Quantitative error reduction inside VEO-segmented boundary failure masks across 207 test scenes. | Grounded in `outputs/nyu_final/test/intervention_faithfulness.json` and `outputs/nyu_final/test/downstream_improvement.json`. Rendered via `scripts/generate_paper_figures.py`. |

---

## Regeneration

To regenerate all figures at 300 DPI:
```bash
uv run python scripts/generate_paper_figures.py
```

