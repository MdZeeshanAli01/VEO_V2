# VISION ERROR OBSERVATORY (VEO)
## Capstone Project Status Report — Project Management Review

**Academic Program:** B.Tech Computer Engineering (Final Year Capstone Project)  
**Institution:** NMIMS — Department of Computer Engineering  
**Project Title:** Vision Error Observatory: Interpretable Diagnostics & Attribution for Monocular Depth Estimation  
**Repository:** `MdZeeshanAli01/VEO_V2`  
**Report Date:** October 27, 2026 | **Reporting Period:** Sprint Cycle 5–6 (Phase: Execution & Pre-Closure)  
**Project Methodology:** Agile-Stage Gate Hybrid (2-Week Iterative Sprints with Milestone Stage Reviews)  

---

## 1. Executive Summary & Triple Constraint Health (RAG Status)

| Constraint / Pillar | RAG Status | Trend | Executive Assessment |
|---|:---:|:---:|---|
| **Overall Project Status** | 🟢 **GREEN** | ↗ Improving | Core pipeline, benchmarking, academic paper, and interactive visual interface delivered. |
| **Scope Baseline** | 🟢 **GREEN** | → Stable | Scope strictly locked to indoor RGB-D evaluation (NYU Depth V2, Hypersim); outdoor sparse data (KITTI) formally excluded to avoid scope creep. |
| **Schedule (Time)** | 🟢 **GREEN** | ↗ Ahead | Sprints 1–5 completed 4 days ahead of scheduled critical path; exhibition web app operational. |
| **Cost & Resources** | 🟢 **GREEN** | → Controlled | Budget variance = 0. Zero external cloud debt. 100% open-source local inference and offline WebGL visualization. |
| **Quality & Assurance (QA)** | 🟢 **GREEN** | → Stable | 100% unit and integration test pass rate; zero regression defects; mathematically verified metric formulas. |

> **Summary Statement:** The VEO Capstone Project is tracking on-time, within budget, and fully compliant with project scope. All core deliverables (diagnostic engine, multi-model evaluation on 1,449 NYU scenes, IEEE-format research paper, and 3D WebGL interactive observatory) have achieved operational readiness.

---

## 2. Project Charter & Scope Management

### 2.1 Project Objectives
1. **Primary Technical Objective:** Bridge the explainability gap in monocular depth estimation by diagnosing *where* and *why* models fail rather than relying on aggregate global metrics (RMSE/AbsRel).
2. **Project Management Objective:** Deliver a reproducible, verified, model-agnostic software artifact and academic research paper within the academic semester timeline.

### 2.2 Scope Traceability (In-Scope vs. Out-of-Scope)
* **In-Scope (Delivered):**
  - Full dataset ingestion & mm-to-meter calibration for **NYU Depth V2** (1,449 labeled images: 1,009 train, 196 val, 244 test).
  - Pretrained model integration: **Depth Anything V2** (ViT-Small) and comparative model **Intel DPT-Hybrid** (MiDaS).
  - Automated 5×5 and arbitrary-scale error region extraction via percentile adaptive thresholding.
  - Multi-hypothesis causal failure taxonomy (Textureless, Specular Reflection, Depth Discontinuity / Boundary Mixing, Optical Vignetting / Lighting).
  - Standalone, zero-CORS interactive 3D WebGL Observatory for non-specialist and faculty evaluation.
* **Out-of-Scope (Change Control Exclusions):**
  - **KITTI Dataset:** Excluded via formal change control due to sparse LiDAR sensor artifacts violating indoor dense-depth assumptions.
  - **Training New Foundational Models:** Excluded from the scope baseline; VEO is designed as a post-hoc diagnostic tool, not an architecture training loop.

---

## 3. Work Breakdown Structure (WBS) & Deliverables Tracker

```
WBS 1.0 Data Ingestion & Calibration
 ├── 1.1 NYU Depth V2 Preprocessing & Mask Extraction [Completed]
 ├── 1.2 Metric Alignment Engine (Least Squares & Median) [Completed]
 └── 1.3 Ground-Truth Sanity Suite & uint16 Validation [Completed]

WBS 2.0 Core Diagnostic & Attribution Engine
 ├── 2.1 Pixel-Level Residual & Relative Error Mapping [Completed]
 ├── 2.2 Connected-Component Failure Region Extraction [Completed]
 ├── 2.3 Image & Depth Feature Extraction (Texture, Edges, Lighting) [Completed]
 └── 2.4 Multi-Class Rule-Based & Heuristic Taxonomy Classifier [Completed]

WBS 3.0 Quantitative Benchmarking & Ablation
 ├── 3.1 1,449-Sample NYU Depth V2 Benchmark Run [Completed]
 ├── 3.2 Second-Model Comparative Evaluation (DPT-Hybrid) [Completed]
 ├── 3.3 Threshold Sensitivity & Alignment Ablation (75th–95th percentile) [Completed]
 └── 3.4 Downstream Error-Mitigation Simulation (Guided bilateral refinement) [Completed]

WBS 4.0 Interactive Web Observatory (Visual UI)
 ├── 4.1 Zero-Dependency Lightweight HTTP Server with Byte-Range Streaming [Completed]
 ├── 4.2 Three.js WebGL 3D Surface Lattice & Error Vector Simulation [Completed]
 ├── 4.3 Synchronized 2D Viewport Tracking & 5×5 Pixel Inspection [Completed]
 └── 4.4 8-Scene Educational Guided Narrative Flow [Completed]

WBS 5.0 Governance, Validation & Final Defense
 ├── 5.1 Blinded Human-in-the-Loop Validation Package & Cohen's Kappa [In Progress - 80%]
 ├── 5.2 Research Paper & Publication Manuscript [Completed - 100%]
 └── 5.3 Final Capstone Defense Presentation & Faculty Demonstration [Planned]
```

### Deliverable Status Table
| WBS Code | Deliverable Name | Planned Date | Actual Date | Status | Verification Evidence |
|:---:|---|:---:|:---:|:---:|---|
| **1.3** | Ground-Truth Depth Calibrator | Week 3 | Week 3 | 100% | `scripts/test_uint16_depth.py` |
| **2.4** | Failure Taxonomy Classifier | Week 5 | Week 5 | 100% | `outputs/nyu_final/test/summary.json` |
| **3.1** | NYU Benchmark Dataset Run | Week 7 | Week 6 | 100% | 1,449 samples processed; official tables |
| **3.3** | Sensitivity & Ablation Reports | Week 8 | Week 8 | 100% | `outputs/alignment_ablation_full/` |
| **4.4** | 3D Interactive Exhibition Web App | Week 9 | Week 9 | 100% | `http://localhost:8000/index.html` |
| **5.1** | Human-in-the-Loop Agreement | Week 10 | Week 10 | 80% | Rating CSVs & `compute_human_agreement.py` |
| **5.2** | Conference Paper Manuscript | Week 10 | Week 9 | 100% | `VEO_conference_paper_final.pdf` (IEEE Format) |

---

## 4. Schedule & Critical Path Analysis

### 4.1 Milestone Progression
* **Milestone M1 (Week 2): Scope & Pipeline Architecture Baselined** — Completed ✅
* **Milestone M2 (Week 4): Core Diagnostic & Attribution Algorithm Validated** — Completed ✅
* **Milestone M3 (Week 6): Full Dataset Benchmarking & Model Comparison Executed** — Completed ✅
* **Milestone M4 (Week 8): Interactive Visual Observatory System Deployed** — Completed ✅
* **Milestone M5 (Week 10): Academic Manuscript & Capstone Defense Readiness** — Active (90% Ready) ⏳

### 4.2 Critical Path (Zero-Float Activities)
$$\text{Data Ingestion} \rightarrow \text{Region Extraction} \rightarrow \text{Taxonomy Scoring} \rightarrow \text{Ablation Benchmarking} \rightarrow \text{Manuscript Approval}$$
* **Schedule Variance (SV):** $+4\text{ days}$ (Project is slightly ahead of schedule).
* **Schedule Performance Index (SPI):** $1.04$ ($> 1.0$ indicates ahead of schedule).

---

## 5. RAID Log (Risks, Assumptions, Issues, Dependencies)

### 5.1 Risk Register
| Risk ID | Category | Description | Severity | Probability | Mitigation Strategy | Contingency Plan | Status |
|:---:|:---:|---|:---:|:---:|---|---|:---:|
| **R-01** | Technical | Evaluator confusion regarding complex mathematical depth concepts. | High | High | Developed an 8-scene 3D guided interactive web exhibition to visually show 25-pixel errors. | Provide live WebGL demo during oral viva. | **Mitigated** |
| **R-02** | Validation | Subjectivity in human rater labeling of failure regions. | Medium | Medium | Implemented a blinded rater protocol with structured taxonomy guidelines and Cohen's Kappa. | Report inter-rater agreement threshold ($\kappa > 0.65$). | **Controlled** |
| **R-03** | Technical | Live deep learning GPU inference failure during faculty evaluation. | High | Low | Pre-computed lightweight 9.2 MB offline data payload (`app_data_v2.js`) for zero-latency, 100% reliable execution. | Fallback to pre-generated static high-resolution figures. | **Closed** |

### 5.2 Assumptions & Dependencies Log
* **Assumption A-01:** Ground truth depth provided by calibrated Microsoft Kinect sensors represents reliable physical reality ($0.8\text{m} - 4.5\text{m}$).
* **Dependency D-01:** PyTorch, Torchvision, and Hugging Face Transformers libraries for baseline model weight extraction.
* **Dependency D-02:** Three.js (r128) WebGL graphics engine running locally without external CDN connectivity.

### 5.3 Issue Log (Resolved Issues)
* **Issue I-01:** Browser styling rendering conflict on local execution.  
  *Resolution:* Implemented a self-contained, zero-dependency inline CSS design system with strict scene visibility isolation (`display: none !important`), eliminating external CDN dependencies.

---

## 6. Quality Assurance (QA) & Project Performance Metrics (KPIs)

| Quality Metric / KPI | Target Metric | Achieved Metric | Status |
|---|:---:|:---:|:---:|
| **Unit & Integration Test Pass Rate** | $100\%$ | $100\%$ ($11/11$ endpoints, $100\%$ test suite) | 🟢 Met |
| **NYU Benchmark Error (Depth Anything V2)** | AbsRel $< 0.10$ | $\text{AbsRel} = 0.086$ (State-of-the-art) | 🟢 Met |
| **Diagnostic Processing Speed** | $< 1.0\text{ sec/image}$ | $0.28\text{ sec/image}$ (Batch optimized) | 🟢 Exceeded |
| **Web Interface Rendering Latency** | $< 100\text{ ms}$ | $16\text{ ms}$ (60 FPS WebGL rendering) | 🟢 Exceeded |
| **Code Modularity & Reproducibility** | Zero dead code | Clean modular structure (`scripts/`, `web_app/`, `docs/`) | 🟢 Met |

---

## 7. Resource & Budget Utilization

* **Financial Budget:** Allocated: ₹0.00 | Expended: ₹0.00 | Variance: ₹0.00 (Self-contained, open research stack).
* **Compute Resources:** Local NVIDIA RTX GPU and standard x86 workstation. All models leveraged existing open-source checkpoints (`Depth-Anything-V2-Small`, `Intel/dpt-hybrid-midas`).
* **Storage Allocation:** Repository footprint minimized (<15 MB code & web payload; large datasets isolated in gitignore).

---

## 8. Next Steps & Capstone Closure Plan (Next 2 Weeks)

1. **Sprint 7 Goal (Week 11):** Consolidate double-blind human agreement results from independent raters and incorporate Kappa coefficients into Section 5 of the thesis document.
2. **Sprint 8 Goal (Week 12):** Rehearse Capstone Oral Defense with project advisor using the interactive web observatory. Complete repository sign-off and final PDF submission.

