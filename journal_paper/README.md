# VEO Journal Manuscript Package (Single-Column)

> **Manuscript Title:** Vision Error Observatory (VEO): A Model-Agnostic Diagnostic and Attribution Framework for Local Failure Modes in Monocular Depth Estimation  
> **Target Publishers:** Springer Nature / Elsevier (ScienceDirect)  
> **Format:** Journal-Neutral Single-Column LaTeX Package  

---

## 1. Directory Structure

```
journal_paper/
├── main.tex                    # Complete single-column LaTeX manuscript source
├── references.bib              # Verified BibTeX bibliography (55 authentic entries)
├── main.pdf                    # Compiled PDF manuscript
├── claims_and_evidence.md       # Audit mapping all paper claims to empirical evidence
├── submission_checklist.md     # Pre-submission readiness checklist for Springer/Elsevier
├── figures/                    # Publication-grade figures (300 DPI PNG + vector PDF)
│   ├── fig1_veo_architecture.pdf / .png
│   ├── fig2_polarity_and_fingerprints.pdf / .png
│   ├── fig3_intervention_and_downstream.pdf / .png
│   ├── fig4_signal_sensitivity_ablation.pdf / .png
│   └── fig5_human_validation_matrix.pdf / .png
├── results/                    # Authentic JSON & CSV experimental outputs
│   ├── nyu_final_summary.json
│   ├── dpt_hybrid_summary.json
│   ├── human_validation_results.json
│   ├── signal_ablation.json
│   ├── intervention_faithfulness.json
│   ├── downstream_improvement.json
│   ├── hypersim_metric_results.json
│   └── correlations.csv
└── scripts/                    # Figure generation & compilation scripts
    ├── generate_journal_figures.py
    ├── generate_bib.py
    └── build_latex_manuscript.py
```

---

## 2. Compilation Instructions

### Option A: Compiling on Overleaf (Recommended)
1. Zip the contents of the `journal_paper/` folder:
   - Include `main.tex`, `references.bib`, and the `figures/` directory.
2. Log in to [Overleaf](https://www.overleaf.com) and click **New Project** $\rightarrow$ **Upload Project**.
3. Select the zip file.
4. Set compiler to **pdfLaTeX** or **XeLaTeX** in Project Settings.
5. Click **Recompile**.

### Option B: Compiling Locally with TeX Live or MiKTeX
Run the standard four-pass compilation in terminal:

```bash
cd journal_paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## 3. Re-Generating Figures & Data

All figures are programmatically generated from the authentic experimental data stored in `journal_paper/results/`:

```bash
# Generate all 5 publication-grade figures (PNG + vector PDF)
python journal_paper/scripts/generate_journal_figures.py
```

---

## 4. Adapting to Specific Publisher Templates

### To adapt to Springer Nature (`sn-jnl.cls`):
1. Download the official `sn-jnl` template package from Springer Nature.
2. In `main.tex`, change `\documentclass[11pt,a4paper]{article}` to:
   ```latex
   \documentclass[pdflatex,sn-basic]{sn-jnl}
   ```
   (or `sn-mathphys` for numbered citations).
3. Place `sn-jnl.cls` in the root folder alongside `main.tex`.

### To adapt to Elsevier (`elsarticle.cls`):
1. Download `elsarticle.cls` from Elsevier.
2. Change the document class to:
   ```latex
   \documentclass[preprint,12pt,1p]{elsarticle}
   ```
