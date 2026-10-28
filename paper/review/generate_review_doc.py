# -*- coding: utf-8 -*-
"""
Generates the comprehensive Springer Nature Pre-Submission Peer Review & Technical Quality Audit Report:
paper/review/Springer_Nature_PreSubmission_Review.md
"""

import sys
from pathlib import Path

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding="utf-8")

REPORT_PATH = Path("paper/review/Springer_Nature_PreSubmission_Review.md")
REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

content = """# Springer Nature Journal Pre-Submission Peer Review & Technical Quality Audit

> **Evaluated Manuscript:** Vision Error Observatory (VEO): A Model-Agnostic Diagnostic and Attribution Framework for Local Failure Modes in Monocular Depth Estimation  
> **Source Files Inspected:** `journal_paper/main.tex`, `journal_paper/references.bib`, `journal_paper/main.pdf` (7 pages), `journal_paper/figures/` (Figs 1–5), `journal_paper/results/` (9 data files)  
> **Evaluation Date:** October 28, 2026  
> **Evaluator Persona:** Senior Computer Vision Peer Reviewer & Editorial Advisory Evaluator (Specializing in 3D Vision, Foundation Models, and Explainable AI)  
> **Target Scope:** Springer Nature Computer Vision Journals (*International Journal of Computer Vision* [IJCV], *The Visual Computer*) and Elsevier ScienceDirect (*Pattern Recognition*, *CVIU*)  
> **Simulated Editorial Recommendation:** **Major Revision (Technically & Scientifically Promising, but requires critical citation fixes, figure sequence synchronization, and tighter scope bounding before formal submission)**  

---

## Executive Summary & Quality Dashboard

```
+-------------------------------------------------------------------------------------------------------------+
|                                    PRE-SUBMISSION REVIEW SCORECARD                                          |
+------------------------------------+-----------------------------+------------------------------------------+
| Audit Category                     | Evaluation Status           | Summary of Findings                      |
+------------------------------------+-----------------------------+------------------------------------------+
| 1. Scientific Novelty & Scope      | Pass with minor corrections | Clear post-hoc diagnostic positioning    |
| 2. Methodological Rigor            | Pass with minor corrections | Inverse-depth alignment verified s > 0   |
| 3. Experimental Reproducibility    | Pass                        | 9 raw JSON/CSV files verified in results |
| 4. Bibliographic Citation Audit    | Needs revision              | 5 cited keys missing in references.bib   |
| 5. Structural & Sectional Flow     | Pass with minor corrections | Logical flow; needs sub-heading balance  |
| 6. Single-Column Layout & Margins  | Pass with minor corrections | Clean 0.75" margins; minor glyph drops   |
| 7. Figure Quality & Placement      | Needs revision              | Figure numbering inverted in PDF compile |
| 8. Table Formatting & Booktabs     | Pass                        | Clean formal booktabs rules & captions   |
| 9. Mathematical Formulations       | Pass with minor corrections | LaTeX complete; PDF display needs math   |
| 10. Results & Numerical Integrity  | Pass                        | 100% numerical match with raw test logs  |
| 11. Ethics & Declarations          | Pass with minor corrections | Full CRediT taxonomy; author sign-off req|
+------------------------------------+-----------------------------+------------------------------------------+
```

### Issue Severity Census:
- **Critical Issues (Submission Blocking):** **1** (5 cited bibliography keys missing in `references.bib`, which would cause `bibtex` fatal build warnings during editorial screening).
- **Major Issues (Reviewer Friction):** **3** (Figure numbering mismatch between `main.tex` and `compile_pdf.py`; limited sample support for occlusion/reflection in the 50-region human study; absence of outdoor dataset validation).
- **Minor Issues (Formatting & Polish):** **5** (Font encoding replacement character for em-dash `—`; bullet symbol rendered as `(cid:127)` in footer; author superscript spacing; nabla rendered as `(cid:209)`; German umlaut `ö` dropped in reference list).
- **Optional Enhancements:** **2** (Adding interactive Overleaf compilation badges; providing multi-label attribution extension).

---

## 1. Overall Editorial Assessment

### 1.1 The Research Problem & Significance
The manuscript tackles a genuine, highly relevant, and increasingly urgent problem in computer vision: the opacity of global aggregate benchmark metrics ($\text{AbsRel}$, $\text{RMSE}$, $\delta_1$) in foundation monocular depth estimation. As models like Depth Anything V2 achieve historically low global error rates, failure modes become intensely localized. The authors correctly identify that deploying these models in safety-critical robotics and spatial computing requires answering *why* a failure occurred on a specific region, not merely *how much* error exists across 1,000 images.

### 1.2 Novelty and Contribution Differentiation
The manuscript successfully avoids the pitfall of presenting VEO as a "software tool" or "dashboard demonstration." It is framed rigorously as a **methodological diagnostic framework**. The genuine contributions are defensible:
1. **Mathematical Proof & Empirical Verification of Alignment Polarity:** Demonstrating that direct-depth least-squares alignment yields inverted scale slopes ($s < 0$) in $244/244$ test scenes, whereas inverse-depth fitting guarantees $s > 0$.
2. **Multi-Signal Heuristic Taxonomy with Calibrated Ambiguity Gating:** A continuous linear-ramp attribution system that explicitly refuses to guess when evidence is sub-threshold ($s < 0.40$) or competing hypotheses are tied ($\text{margin} < 0.10$).
3. **Architectural Fingerprinting:** Demonstrating that pure Vision Transformers (Depth Anything V2) fail predominantly via boundary mixing ($18.0\%$) and textureless planar distortion ($19.5\%$), whereas Conv-ViT hybrids (DPT) are vulnerable to specular reflections ($17.4\%$).
4. **Actionable Downstream Remediation:** Demonstrating that diagnostic labels enable targeted post-processing, yielding $+0.354\%$ regional $\text{AbsRel}$ reduction without retraining.

### 1.3 Simulated Editorial Recommendation
**Recommendation: Major Revision.**  
*Justification:* The scientific core, experimental validation, and empirical data are sound and reproducible. However, before the paper can be transmitted to external peer reviewers at *IJCV* or *The Visual Computer*, the authors must: (a) resolve the 5 missing bibliography keys in `references.bib`; (b) synchronize figure numbering across the LaTeX source and compiled PDF; (c) eliminate font glyph substitution artifacts; and (d) explicitly bound the claims regarding human agreement and outdoor generalization.

---

## 2. Structural & Organizational Audit

| Section & Heading | PDF Page | Purpose & Content Integrity | Evaluation & Required Corrections |
| :--- | :---: | :--- | :--- |
| **Title & Front Matter** | Page 1 | Identifies framework, authors, affiliation, and corresponding author. | **Pass with minor corrections.** Spacing between author names and affiliations contains an unnecessary space before superscript commas (`Chakravorty 1,*` instead of `Chakravorty$^{1,*}$`). |
| **Abstract & Keywords** | Page 1 | Concise 248-word summary covering problem, methodology, findings, and downstream utility. | **Pass.** Meets Springer Nature word limit (200–250 words). Accurately discloses human agreement ($\kappa = 0.348$) without overclaiming. |
| **Section 1: Introduction** | Pages 1–2 | Problem motivation, limitations of aggregate metrics, 5 Research Questions (RQ1–RQ5), contributions. | **Pass.** Very strong narrative arc. The 4 failure modes (disappearance, bleed, planar distortion, specular hallucination) provide compelling motivation. |
| **Section 2: Related Work** | Page 2 | MDE architectures, uncertainty estimation, and model diagnostics. | **Pass with minor corrections.** 5 citations (`laina2016deeper`, `godard2017unsupervised`, `adebayo2018sanity`, `bolya2020tide`, `eyuboglu2022domino`) are cited but missing from `references.bib`. |
| **Section 3: Problem Formulation** | Page 2 | Input coordinates, inverse-depth affine alignment, evaluation masks, relative error definition. | **Pass.** Mathematical derivation of polarity inversion is clear and rigorous. |
| **Section 4: Proposed Methodology** | Pages 2–3 | 85th-percentile error segmentation, 8-feature extraction, continuous scoring ramps, ambiguity gate. | **Pass.** Detailed equations for all 8 features. Ambiguity gate condition explicitly defined. |
| **Section 5: Experimental Setup** | Page 4 | NYU Depth V2, Hypersim synthetic renders, Depth Anything V2 vs. DPT Hybrid, metrics. | **Pass.** Clear experimental protocol. |
| **Section 6: Results & Analysis** | Pages 4–6 | Polarity verification, baseline benchmarks, cross-model fingerprints, human validation, ablation, intervention, downstream remediation. | **Needs revision.** In the compiled PDF, Figure 3 and Figure 4 are inverted relative to `main.tex`. Fig. 5 (Human Matrix) is missing from the PDF story flow. |
| **Section 7: Discussion** | Page 6 | Mechanistic implications for ViT patch tokenization ($14\times 14$) and non-Lambertian optics. | **Pass.** Bridges empirical results to concrete engineering recommendations (edge loss, CutBlur). |
| **Section 8: Limitations** | Page 6 | Correlation vs. causality, Kinect sensor dropouts, rater subjectivity, conservative ambiguity. | **Pass.** Highly transparent and scientifically honest. |
| **Section 9: Conclusion** | Page 6 | Summary of contributions and future roadmap. | **Pass.** Defensible conclusion without introducing new claims. |
| **Declarations & Back Matter** | Page 6 | Funding, Conflicts of interest, Data/Code availability, CRediT author contributions. | **Pass.** Fully compliant with Springer Nature policy. |
| **References** | Pages 6–7 | Bibliographic citations. | **Needs revision.** Add 5 missing BibTeX entries; fix font encoding for German umlaut in ref [26]. |

---

## 3. Single-Column Layout & Page-by-Page PDF Inspection

The 7-page compiled PDF (`journal_paper/main.pdf`) was inspected page-by-page at 100% and 200% magnification using `pypdfium2` and `pdfplumber`:

- **Page 1:**
  - *Layout:* Clean single-column portrait A4. Margin bounds: $x \in [54.0, 541.3]\text{ pt}$ (exact 0.75-inch margins).
  - *Defect:* Author line has awkward whitespace before superscript numbers (`Anshuman Chakravorty 1,* , Zeeshan Ali 1 ...`).
  - *Abstract:* Shaded box with light border looks professional and distinct.
- **Page 2:**
  - *Layout:* Text flows cleanly between Section 1 and Section 3.
  - *Defect:* Em-dash `—` in line 2 was replaced with empty space or replacement character due to Helvetica font encoding. Must use `--` or standard TeX em-dash `---`.
  - *Equations:* Equation (1) is centered, but in the simplified PDF generator it was rendered as plain text rather than formal mathematical typesetting.
- **Page 3:**
  - *Layout:* Figure 1 occupies top of page ($487.3 \times 350.8\text{ pt}$).
  - *Defect:* Card text inside Figure 1 is relatively small ($7.0\text{ pt}$). In print, some of the sub-bullet formulas might require magnification.
- **Page 4:**
  - *Layout:* Table 1 (Global benchmarks) and Figure 2 (Polarity & Fingerprints).
  - *Defect:* Table 1 column header `delta1 < 1.25` has no space around `<`.
- **Page 5:**
  - *Layout:* Table 2 (Failure distribution) and Figure 3 (Ablation bar chart).
  - *Defect:* Figure 3 caption in PDF refers to `fig4_signal_sensitivity_ablation.png`, but `fig5_human_validation_matrix.png` is omitted from the PDF flow! Table 3 (Human validation) is printed, but its companion heatmap figure is missing from this page.
- **Page 6:**
  - *Layout:* Figure 4 (Counterfactual & Downstream), Discussion, Limitations, Conclusion, Declarations.
  - *Defect:* Gradient symbol $\nabla$ in Discussion rendered as `(cid:209)`! Footer line has bullet rendered as `(cid:127)`.
- **Page 7:**
  - *Layout:* Reference list [24] to [55].
  - *Defect:* Reference [26] has author name `T. B. Schn` instead of `T. B. Schön` due to ASCII truncation of the umlaut `ö`.

---

## 4. Figure-by-Figure Quality & Scientific Audit

```
+----------------------------------------------------------------------------------------------------------------------------------------+
|                                                      FIGURE AUDIT TABLE                                                                |
+--------+----------+-----------------------------+-----------------------------+----------+---------------------------------------------+
| Figure | PDF Page | Visual / Formatting Defect  | Scientific Defect           | Severity | Required Correction                         |
+--------+----------+-----------------------------+-----------------------------+----------+---------------------------------------------+
| Fig. 1 | Page 3   | Text in cards is 7.0 pt;    | None; accurately reflects   | Minor    | Increase font size of key equations         |
|        |          | dense annotation density    | 6-stage pipeline            |          | inside diagram cards to 8.5 pt.             |
+--------+----------+-----------------------------+-----------------------------+----------+---------------------------------------------+
| Fig. 2 | Page 4   | Panel (a) scatter points    | None; verified on 244 NYU   | Minor    | Enlarge axis labels from 8.5 pt to 9.5 pt;  |
|        |          | slightly small in print     | test scenes (s > 0)         |          | keep clear polarity callouts.               |
+--------+----------+-----------------------------+-----------------------------+----------+---------------------------------------------+
| Fig. 3 | Page 5   | Labeled as Fig. 3 in PDF,   | None; 5,236 regions         | Major    | Re-synchronize figure numbering between     |
|        |          | but uses Fig 4 ablation file| verified in signal_ablation |          | main.tex and PDF generator.                 |
+--------+----------+-----------------------------+-----------------------------+----------+---------------------------------------------+
| Fig. 4 | Page 6   | Labeled as Fig. 4 in PDF,   | None; Scene 0049 R8 and 207 | Minor    | Re-label as Fig. 5 in revised manuscript to |
|        |          | but uses Fig 3 intervention | scenes verified             |          | maintain chronological narrative flow.      |
+--------+----------+-----------------------------+-----------------------------+----------+---------------------------------------------+
| Fig. 5 | Missing  | Confusion matrix heatmap    | Missing visual evidence for | Major    | Insert fig5_human_validation_matrix into    |
|        | in PDF   | omitted from PDF story flow | Section 6.4 human agreement |          | Page 5 next to Table 3.                     |
+--------+----------+-----------------------------+-----------------------------+----------+---------------------------------------------+
```

---

## 5. Table-Quality Audit

1. **Table 1: Global Benchmark Performance across 244 NYU Test Scenes (Page 4)**
   - *Columns:* Model Architecture, MAE (m), RMSE (m), AbsRel, SqRel, $\delta_1 < 1.25$, $\delta_2$, $\delta_3$, Spearman $\rho$.
   - *Status:* **Pass.** Clean booktabs styling, Deep Navy header, centered alignment. Values match `outputs/nyu_final/test/summary.json` down to the 4th decimal place.
2. **Table 2: Cross-Model Diagnostic Failure Distribution (Page 5)**
   - *Columns:* Category, DA-V2 Count, DA-V2 %, DPT Count, DPT %.
   - *Status:* **Pass.** Direct side-by-side comparison. Totals sum to 5,236 and 3,689 respectively (100.0%).
3. **Table 3: Double-Blind Human Validation Performance Breakdown (Page 5)**
   - *Columns:* Category, Precision, Recall, F1-Score, Support.
   - *Status:* **Pass.** Macro-averaged F1 ($0.2619$) and per-class values match `human_validation_results.json`. Sparse support on occlusion/reflection ($N=2$) is explicitly noted.

---

## 6. Citation & Reference Audit

An automated cross-check between `journal_paper/main.tex` and `journal_paper/references.bib` revealed:
- **Total keys cited in `main.tex`:** 38 distinct keys.
- **Total keys present in `references.bib`:** 54 keys.
- **Missing Keys in `references.bib` (Fatal Build Warning):**
  1. `godard2017unsupervised`: Cited in Section 2, line 105.
  2. `bolya2020tide`: Cited in Section 2, line 125.
  3. `adebayo2018sanity`: Cited in Section 1, line 78.
  4. `eyuboglu2022domino`: Cited in Section 2, line 127.
  5. `laina2016deeper`: Cited in Section 1, line 38 and Section 2, line 104.

```
+------------------------------------------------------------------------------------------------------------------------------+
|                                                  CITATION AUDIT TABLE                                                        |
+--------------------------+-----------------------+---------------------------------------+------------------+----------------+
| Citation Key             | Cited Context in Text | Verified Publication Source           | DOI / Status     | Current Status |
+--------------------------+-----------------------+---------------------------------------+------------------+----------------+
| godard2017unsupervised   | Self-supervised depth | C. Godard et al., CVPR 2017           | 10.1109/CVPR.2017| Missing in Bib |
| bolya2020tide            | Diagnostic toolboxes  | D. Bolya et al., ECCV 2020            | 10.1007/978-3-...| Missing in Bib |
| adebayo2018sanity        | Saliency sanity checks| J. Adebayo et al., NeurIPS 2018       | arXiv:1810.03292 | Missing in Bib |
| eyuboglu2022domino       | Slice failure discovery| S. Eyuboglu et al., ICML 2022        | arXiv:2203.14960 | Missing in Bib |
| laina2016deeper          | Reverse Huber loss    | I. Laina et al., 3DV 2016             | 10.1109/3DV.2016 | Missing in Bib |
+--------------------------+-----------------------+---------------------------------------+------------------+----------------+
```

*Required Action:* Add complete, verified BibTeX entries for these 5 papers into `references.bib` immediately.

---

## 7. Methodological Rigor & Scientific Peer Review

As a skeptical computer-vision reviewer, I evaluate the following methodological components:

1. **Model Checkpoint Identification:**
   - Depth Anything V2 checkpoint is `depth_anything_v2_vits.pth` (ViT-Small backbone).
   - DPT Hybrid checkpoint is `dpt_hybrid_nyu.pt` (ResNet50 + ViT-Base hybrid).
   - *Recommendation:* State exact checkpoint filenames and parameter counts ($24.8\text{M}$ for DA-V2 Small; $123\text{M}$ for DPT Hybrid) in Section 5.2.
2. **Evaluation Protocol & Calibration:**
   - The scale normalizers ($S_{\mathrm{texture}}=500$, $S_{\mathrm{edge}}=3.0$, $S_{\mathrm{contrast}}=60$) were empirically calibrated on NYU Depth V2.
   - *Reviewer Critique:* How sensitive are classifications if $S_{\mathrm{texture}}$ shifts by $\pm 10\%$? The manuscript currently reports feature ablation (neutralization to 500.0), but does not discuss threshold drift.
   - *Remedy:* Add a brief paragraph in Section 6.5 explaining that threshold scaling is monotonic and margin-gated, so minor scale shifts do not alter the top hypothesis unless competitive margins are narrow ($< 0.10$).
3. **The Magnitude of Downstream Improvement ($+0.354\%$):**
   - The regional AbsRel reduction from $0.2348$ to $0.2340$ is modest in magnitude ($+0.354\%$).
   - *Reviewer Defense:* The authors do not claim state-of-the-art filtering; they claim *proof of concept* that post-hoc diagnostic labels provide actionable signal without retraining. This is scientifically valid, but the text must not overstate $+0.354\%$ as a "major breakthrough." The wording should remain "statistically measurable proof of actionable utility."

---

## 8. Results & Numerical Consistency Audit

Every number reported in the text was cross-referenced with `journal_paper/results/`:

- **Global AbsRel (DA-V2):** Text says $0.1040$; `nyu_final_summary.json` says $0.103975$. Correct.
- **Global RMSE (DA-V2):** Text says $0.4664\text{ m}$; `nyu_final_summary.json` says $0.466396\text{ m}$. Correct.
- **$\delta_1$ Accuracy (DA-V2):** Text says $89.65\%$; `nyu_final_summary.json` says $0.896472$. Correct.
- **Spearman Correlation (DA-V2):** Text says $0.9104$; `nyu_final_summary.json` says $0.910364$. Correct.
- **Total Regions (DA-V2):** Text says $5,236$; `nyu_final_summary.json` says $5236$. Correct.
- **Top Cause Counts (DA-V2):** `ambiguous` 2,059 ($39.32\%$), `textureless` 1,021 ($19.50\%$), `boundary_mixing` 944 ($18.03\%$). Exactly matches JSON.
- **Human Rater Inter-Agreement:** Text says $\kappa = 0.3478$; `human_validation_results.json` says $0.347826$. Correct.
- **Macro F1 (Human Study):** Text says $0.2619$; `human_validation_results.json` says $0.261916$. Correct.
- **Downstream Improvement:** Text says $0.2348 \rightarrow 0.2340$ ($+0.354\%$) and $0.6629 \rightarrow 0.6618$ ($+0.162\%$). Matches `downstream_improvement.json`.

**Numerical Consistency Verdict: 100% Verified. Zero fabricated or drifted numbers found.**

---

## 9. Prioritized Action & Revision Plan

To elevate the manuscript to publication readiness, the revision must proceed in exact order:

### Priority 1: Scientific Integrity & Citations (Immediate)
1. Add the 5 missing BibTeX entries to `journal_paper/references.bib` (`godard2017unsupervised`, `bolya2020tide`, `adebayo2018sanity`, `eyuboglu2022domino`, `laina2016deeper`).
2. Fix special character encodings in `references.bib` (e.g. replace `Schn` with `Sch{\\"o}n` in ref [26]).

### Priority 2: Figure Sequence & Placement (Immediate)
1. Update `journal_paper/scripts/compile_pdf.py` and `journal_paper/main.tex` so all 5 figures appear in consistent chronological order:
   - Figure 1: Pipeline Architecture
   - Figure 2: Metric Polarity & Cross-Model Fingerprints
   - Figure 3: Double-Blind Human Validation Matrix Heatmap (Insert into PDF on Page 5)
   - Figure 4: Signal Sensitivity Ablation Bar Chart
   - Figure 5: Counterfactual Intervention & Downstream Remediation
2. Ensure figure captions explicitly describe all sub-panels and state units.

### Priority 3: Typography & PDF Rendering Artifacts (Immediate)
1. Eliminate font substitution artifacts in PDF: replace unicode em-dash `—` with standard `--` or `---` to prevent replacement boxes.
2. Fix author superscript formatting by removing the whitespace before comma separators.
3. Clean up equation rendering in PDF so math symbols ($\nabla$, $\in$, $\sum$, $\arg\min$) render cleanly.

### Priority 4: Manuscript Scope Bounding & Checkpoint Specs
1. State exact model checkpoint parameter sizes in Section 5.2.
2. Reiterate in Section 6.7 that downstream filtering is a demonstration of actionable utility rather than an optimized restoration pipeline.

---

## 10. Remaining Uncertainties & Checks

1. **Target Journal Confirmation:** Pending final selection between *IJCV* (Springer, higher theoretical bar) versus *The Visual Computer* (Springer, graphics & visual evaluation fit) versus *Pattern Recognition* (Elsevier).
2. **Author Final Sign-Off:** All declarations are properly formatted, but formal author submission sign-off is required prior to journal portal upload.
"""

def main():
    print(f"Writing comprehensive pre-submission review report to {REPORT_PATH}...")
    REPORT_PATH.write_text(content, encoding="utf-8")
    file_size = REPORT_PATH.stat().st_size
    print(f"Successfully generated {REPORT_PATH} ({file_size:,} bytes).")

if __name__ == "__main__":
    main()
