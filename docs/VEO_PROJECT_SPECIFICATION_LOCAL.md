# VEO PROJECT — COMPLETE RESEARCH DOCUMENTATION
## Vision Error Observatory: A Validated, Evidence-Based Framework for Region-Level Failure Diagnosis in Monocular Depth Estimation

**Document Version:** 2.0 (Local Development Edition)  
**Date:** September 2026  
**Status:** Active Development (Weeks 8-12)  
**Institution:** SVKM's NMIMS University, MPSTME, Hyderabad  
**Team:** Member 1 (Depth Estimation) | Member 2 (Error Analysis) | Member 3 (Evidence Engine)

---

# TABLE OF CONTENTS

1. [PROJECT OVERVIEW](#1-project-overview)
2. [RESEARCH PROBLEM & MOTIVATION](#2-research-problem--motivation)
3. [LITERATURE REVIEW & GAP](#3-literature-review--gap)
4. [METHODOLOGY & ARCHITECTURE](#4-methodology--architecture)
5. [TECHNICAL SPECIFICATIONS](#5-technical-specifications)
6. [DATA SPECIFICATIONS](#6-data-specifications)
7. [CODE STRUCTURE & ORGANIZATION](#7-code-structure--organization)
8. [CURRENT STATUS & DECISIONS](#8-current-status--decisions)
9. [LOCAL DEVELOPMENT SETUP (VS CODE)](#9-local-development-setup-vs-code)
10. [STEP-BY-STEP EXECUTION GUIDE](#10-step-by-step-execution-guide)
11. [EXPECTED OUTPUTS & MILESTONES](#11-expected-outputs--milestones)
12. [VALIDATION PROTOCOL](#12-validation-protocol)
13. [PAPER WRITING INTEGRATION](#13-paper-writing-integration)
14. [GITHUB WORKFLOW & VERSION CONTROL](#14-github-workflow--version-control)
15. [TESTING & QUALITY ASSURANCE](#15-testing--quality-assurance)

---

# 1. PROJECT OVERVIEW

## 1.1 Project Title
**Vision Error Observatory (VEO): A Validated, Evidence-Based Framework for Region-Level Failure Diagnosis in Monocular Depth Estimation**

## 1.2 Research Objective
To systematically identify, localize, classify, and validate failure modes in monocular depth estimation (MDE) models using a rule-based evidence scoring framework combined with human expert validation.

## 1.3 Core Innovation
**NOT** a new depth estimation model. Instead:
- Model-agnostic failure analysis (works with any pretrained MDE model)
- Pixel-level error localization (where failures occur)
- Visual evidence extraction (why failures occur)
- Rule-based classification (interpretable cause assignment)
- Human validation (proof that explanations are trustworthy)

## 1.4 Scope (MVP Phase)
| Component | Status | Models | Datasets |
|-----------|--------|--------|----------|
| Depth Prediction | ✓ Complete | Depth Anything V2, ZoeDepth | KITTI (50 images) |
| Error Analysis | ✓ Complete | - | KITTI (50 images) |
| Failure Discovery | In Progress | Both models | Both datasets |
| Evidence Engine | In Progress | Both models | Both datasets |
| Validation Protocol | Planned | - | Manual labels (100-150 regions) |
| Dashboard | Planned | - | - |
| Paper Writing | Planned | - | - |

## 1.5 Research Questions (RQ1-RQ5)
1. **RQ1:** Can we systematically localize high-error regions beyond global metrics?
   - **Answer:** Yes, via pixel-wise error thresholding (85th percentile)

2. **RQ2:** Do visual/geometric features consistently indicate failure causes?
   - **Answer:** Depends on correlation testing (CELL 5 results)

3. **RQ3:** Are rule-based classifications interpretable and defensible?
   - **Answer:** Validated via human expert agreement (Cohen's kappa)

4. **RQ4:** Do failure patterns differ across models?
   - **Answer:** Yes, Depth Anything V2 vs. ZoeDepth comparison shows different distributions

5. **RQ5:** Can validation be systematic and reproducible?
   - **Answer:** Yes, via correlation tests + human agreement + ablation studies

---

# 2. RESEARCH PROBLEM & MOTIVATION

## 2.1 The Problem
Monocular depth estimation (MDE) has achieved strong global metrics:
- **AbsRel (relative error):** ~0.16 on KITTI
- **RMSE (absolute error):** ~4m on KITTI
- **Delta1 (25% threshold accuracy):** ~0.80

**BUT:** These aggregate metrics hide crucial diagnostic information:
- WHERE do failures occur? (spatial localization)
- WHY do they occur? (visual/geometric causes)
- HOW can we improve? (actionable insights)

## 2.2 Existing Limitations
| Existing Approach | Limitation | VEO Answer |
|---|---|---|
| RMSE, AbsRel, δ1 | Aggregate only; no spatial info | Pixel-level error maps |
| DEDN (Chawla 2021) | Detects error but doesn't classify cause | Rule-based cause classification |
| Uncertainty models | Quantify confidence, not causes | Evidence extraction |
| Explainable AI (Grad-CAM, LIME) | Model-centric, not depth-centric | Visual feature measurement |

## 2.3 VEO Contribution
**End-to-end pipeline** that:
1. Localizes failures (error map → connected components)
2. Classifies causes (6 evidence signals → rule-based scores)
3. Validates explanations (human agreement → Cohen's kappa)
4. Enables model debugging (systematic root-cause analysis)

---

# 3. LITERATURE REVIEW & GAP

## 3.1 Research Clusters & Key Works
| Cluster | Representative Works | Key Limitation |
|---------|---|---|
| **Evolution of MDE** | Eigen 2014 → Depth Anything V2 2024 | No localized failure analysis |
| **Depth Datasets** | KITTI, NYU, MegaDepth | Benchmarks only, no failure annotation |
| **Evaluation Frameworks** | FastDepth, UBD | Performance varies but no root-cause |
| **Uncertainty & Confidence** | Aleatoric/Epistemic uncertainty | Quantify confidence, not causes |
| **Error & Failure Analysis** | DEDN (2021), RoboDepth | Localize or induce, not validate |
| **Transformer & Foundation Models** | Depth Anything, ZoeDepth, Marigold | Optimized for accuracy, not interpretability |
| **Explainable AI for CV** | Grad-CAM, LIME, Integrated Gradients | Influential regions ≠ failure causes |
| **Model Debugging** | Manifold, iNNspector | General ML, not depth-specific |

## 3.2 Identified Gap
No unified framework that:
1. Localizes high-error regions in MDE
2. Classifies failures into interpretable causes
3. Validates explanations against ground truth
4. Works across multiple models

## 3.3 VEO Fills the Gap
**Depth Prediction → Error Localization → Feature Extraction → Evidence-Based Classification → Human Validation**

---

# 4. METHODOLOGY & ARCHITECTURE

## 4.1 System Architecture (VEO Pipeline)

```
INPUT
  RGB Image (480×640×3)
  + Ground Truth Depth Map (480×640)
    ↓
PHASE 1: DEPTH PREDICTION
  Depth Anything V2 (pretrained, ViT-Small)
  → Relative depth prediction
    ↓
PHASE 2: GROUND TRUTH ALIGNMENT
  Scale-shift transformation
  depth_aligned = scale * depth_pred + shift
  (Least-squares fit to GT)
    ↓
PHASE 3: ERROR ANALYSIS
  AbsRel = mean(|pred - GT| / GT)
  RMSE = sqrt(mean((pred - GT)²))
  Delta1 = mean(max(pred/GT, GT/pred) < 1.25)
  Error map: pixel-wise |pred - GT| / GT
    ↓
PHASE 4: FAILURE LOCALIZATION
  Threshold: error > 85th percentile
  Connected components → failure regions
  Min area filter: ≥50 pixels
    ↓
PHASE 5: FEATURE EXTRACTION (per region)
  6 evidence signals:
    1. texture_var (textureless surfaces)
    2. edge_density (object boundaries)
    3. brightness (poor illumination)
    4. contrast (low-contrast areas)
    5. highlight_ratio (specular reflections)
    6. depth_discontinuity (occlusions)
    ↓
PHASE 6: RULE-BASED SCORING
  For each signal → category score (0-1)
  Top score determines cause
  Confidence: High (>0.6), Medium (0.4-0.6), Low (<0.4)
    ↓
PHASE 7: VALIDATION PROTOCOL
  Evidence-error correlation test
  Human expert agreement (Cohen's kappa)
  Ablation study (remove each signal)
    ↓
OUTPUT
  Classified failure regions
  Cause labels + confidence
  Evidence visualization
  Metrics & statistics
```

## 4.2 Failure Categories (MVP = 6)

| Category | Definition | Primary Signal | Threshold |
|----------|---|---|---|
| **Occlusion** | Depth discontinuity at boundaries | depth_discontinuity | > 2.0m (TBD: may adjust to 3.0-4.0) |
| **Boundary Mixing** | Object edge ambiguity | edge_density | > 0.1 (threshold = 3.0x) |
| **Textureless** | Low texture/ambiguity | texture_var | < 500 variance |
| **Poor Lighting** | Extreme shadows/overexposure | brightness + contrast | brightness < 60 or > 200 |
| **Thin Objects** | High aspect ratio structures | aspect_ratio | > 3.0 |
| **Reflection** | Specular reflections (EXTENDED scope, data-driven) | highlight_ratio | > 0.02 |

**Note:** Category resolution is PENDING final decision (see Section 8)

## 4.3 Evidence Signals & Formulas

### Signal 1: Texture Variance
```
texture_var = variance of grayscale patch
score = clip(1 - texture_var/500, 0, 1)
Interpretation: Low variance → textureless surface
```

### Signal 2: Edge Density
```
edge_density = canny_edge_pixels / total_pixels
score = clip(edge_density * 3, 0, 1)
Interpretation: High edges → object boundary
```

### Signal 3: Brightness & Contrast
```
brightness = mean(grayscale patch)
contrast = std(grayscale patch)
score = clip(1 - contrast/60, 0, 1)
      if (brightness < 60 or brightness > 200) else 0
Interpretation: Extreme brightness/low contrast → poor lighting
```

### Signal 4: Saturation & Highlights
```
hsv = cv2.cvtColor(patch, cv2.COLOR_RGB2HSV)
highlight_mask = (V > 200) & (S < 40)
highlight_ratio = highlight_mask.sum() / total_pixels
score = clip(highlight_ratio * 5, 0, 1)
Interpretation: High saturation + high value → reflection
```

### Signal 5: Region Shape (Aspect Ratio)
```
bbox = [x, y, w, h]
aspect_ratio = max(w, h) / max(min(w, h), 1)
score = clip((aspect_ratio - 3) / 5, 0, 1)
Interpretation: High aspect ratio → thin object
```

### Signal 6: Depth Discontinuity
```
gy, gx = gradient(GT_depth_patch)
grad_mag = sqrt(gx² + gy²)
discontinuity = mean(grad_mag at region boundary)
score = clip(discontinuity / 2.0, 0, 1)
Interpretation: High discontinuity → occlusion
```

**Note:** Threshold 2.0 is TBD; may be adjusted to 3.0+ based on correlation testing

## 4.4 Confidence Assignment

```
confidence = function(top_score, cluster_agreement)

if top_score > 0.6:
    confidence = "High" (if cluster_agrees) else "Medium"
elif top_score > 0.4:
    confidence = "Medium"
else:
    confidence = "Low"

Interpretation:
  High: Strong evidence, clear classification
  Medium: Moderate evidence, some uncertainty
  Low: Weak evidence, consider alternative explanations
```

---

# 5. TECHNICAL SPECIFICATIONS

## 5.1 Software Stack

| Layer | Technology | Version | Purpose |
|-------|---|---|---|
| **Language** | Python | 3.9+ | Primary development |
| **DL Framework** | PyTorch | 2.0+ | Model loading & inference |
| **Model Hub** | HuggingFace Transformers | 4.30+ | Depth Anything V2, ZoeDepth |
| **Image Processing** | OpenCV | 4.8+ | Region extraction, morphology |
| **Scientific Computing** | NumPy, SciPy | Latest | Statistics, correlation tests |
| **Data Processing** | Pandas | 2.0+ | Results organization |
| **Visualization** | Matplotlib, Seaborn | Latest | Plots & figures |
| **Metrics** | scikit-learn | 1.3+ | Cohen's kappa, confusion matrix |
| **Version Control** | Git/GitHub | - | Code repository |
| **IDE** | VS Code | Latest | Local development |
| **Environment** | Python venv / Conda | - | Dependency isolation |

## 5.2 Hardware Requirements

| Component | Requirement | Rationale |
|-----------|---|---|
| **GPU** | NVIDIA (8GB+ VRAM) | Depth model inference (batch processing) |
| **CPU** | 4+ cores | Parallel region processing |
| **RAM** | 16GB+ | Loading KITTI dataset (50 images + predictions) |
| **Storage** | 100GB+ | Raw images, predictions, outputs, intermediate files |
| **Network** | 100Mbps | Downloading models from HuggingFace (one-time) |

## 5.3 Dependencies (Complete List)

```
# Core
torch>=2.0.0
torchvision>=0.15.0
transformers>=4.30.0
opencv-python>=4.8.0
numpy>=1.24.0
scipy>=1.11.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0

# GPU acceleration
cuda-python>=12.0 (if using NVIDIA GPU)

# Utilities
tqdm>=4.66.0 (progress bars)
pillow>=10.0.0 (image I/O)
pyyaml>=6.0 (configuration files)
```

## 5.4 Directory Structure (Local)

```
VEO_Project/
│
├── data/
│   ├── raw_kitti/
│   │   ├── image/              # 50 RGB images
│   │   └── depth/              # 50 GT depth maps
│   └── README.md               # Data documentation
│
├── outputs/
│   ├── predictions/            # Depth Anything V2 predictions
│   ├── error_maps/             # Pixel-wise error maps
│   ├── regions/                # Failure regions (JSON)
│   ├── evidence/               # Evidence features
│   ├── visualizations/         # 4-panel images
│   ├── results/                # Summary statistics
│   └── correlations/           # Correlation test results
│
├── src/
│   ├── __init__.py
│   ├── config.py               # Configuration (paths, hyperparams)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── depth_inference.py  # Depth model loading & inference
│   │   └── model_loader.py     # Model download & caching
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── alignment.py        # Scale-shift alignment
│   │   ├── error_analysis.py   # Error metrics & maps
│   │   └── region_extraction.py # Failure region detection
│   ├── features/
│   │   ├── __init__.py
│   │   ├── evidence_signals.py # 6 evidence signal computation
│   │   ├── scoring.py          # Rule-based classification
│   │   └── validation.py       # Correlation & ablation tests
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── io.py               # File I/O (JSON, CSV, images)
│   │   ├── visualization.py    # Plot generation
│   │   └── logging.py          # Logging utilities
│   └── main.py                 # Entry point
│
├── notebooks/
│   ├── 01_data_exploration.ipynb    # Initial data analysis
│   ├── 02_error_analysis.ipynb      # Error visualization
│   ├── 03_feature_extraction.ipynb  # Feature exploration
│   ├── 04_correlation_analysis.ipynb # Correlation testing
│   └── 05_cross_model_comparison.ipynb
│
├── tests/
│   ├── __init__.py
│   ├── test_alignment.py       # Unit tests for alignment
│   ├── test_scoring.py         # Unit tests for scoring
│   └── test_validation.py      # Integration tests
│
├── scripts/
│   ├── run_pipeline.py         # Complete end-to-end pipeline
│   ├── run_validation.py       # Validation protocol
│   ├── run_cross_model.py      # ZoeDepth analysis
│   └── generate_paper_tables.py # Extract results for paper
│
├── paper/
│   ├── veo_research_paper.md   # Paper (markdown)
│   ├── figures/                # All paper figures
│   ├── tables/                 # All paper tables
│   └── references.bib          # BibTeX citations
│
├── docs/
│   ├── ARCHITECTURE.md         # System design
│   ├── API_REFERENCE.md        # Function documentation
│   ├── DECISIONS.md            # Design decisions log
│   └── RESEARCH_LOG.md         # Week-by-week progress
│
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions (testing on push)
│
├── .gitignore
├── requirements.txt
├── setup.py
├── README.md                   # Project readme
└── PROJECT_SPECIFICATION.md    # This document

```

---

# 6. DATA SPECIFICATIONS

## 6.1 Input Data (KITTI Dataset)

### Images
- **Source:** KITTI driving dataset (http://www.cvlibs.net/datasets/kitti/)
- **Count:** 50 RGB images (subset for MVP testing)
- **Format:** PNG
- **Resolution:** 1226 × 370 pixels
- **Color Space:** RGB (3 channels)
- **Normalization:** [0, 255] → [0, 1] (divide by 255)

### Ground Truth Depth
- **Source:** KITTI sparse LiDAR projections
- **Format:** PNG (16-bit unsigned)
- **Encoding:** depth(m) = pixel_value / 256.0
- **Invalid pixels:** pixel_value = 0 (no LiDAR return)
- **Validity mask:** sparse_mask = depth > 0
- **Sparsity:** ~5-10% valid pixels (LiDAR-only coverage)

### Preprocessing Required
```
1. Load RGB image
   rgb = np.array(Image.open(path))  # shape: (370, 1226, 3)

2. Load GT depth
   gt_raw = np.array(Image.open(path))  # shape: (370, 1226)
   depth = gt_raw.astype(np.float32) / 256.0
   valid_mask = depth > 0

3. Size consistency check
   assert rgb.shape[:2] == depth.shape
```

## 6.2 Intermediate Data (Processing Outputs)

### Predicted Depth Maps
- **Source:** Depth Anything V2 inference
- **Format:** NumPy (.npy) and PNG
- **Range:** [0, max_depth] (varies per image)
- **Type:** float32
- **Size:** Same as input RGB (1226 × 370)
- **Storage:** `outputs/predictions/depth_anything_v2/{image_id}.npy`

### Aligned Depth (Scale-Shift)
```python
# Alignment formula
valid = valid_mask
A = np.stack([pred[valid], np.ones_like(pred[valid])], axis=1)
scale, shift = np.linalg.lstsq(A, gt[valid], rcond=None)[0]
pred_aligned = pred * scale + shift
```

### Error Maps
- **Definition:** AbsRel per pixel = |pred - gt| / gt
- **Mask:** Only valid pixels (where GT exists)
- **Range:** [0, ∞) but clipped for visualization
- **Storage:** `outputs/error_maps/{image_id}_error.npy`

### Failure Regions
- **Definition:** Connected components where error > 85th percentile
- **Min area:** 50 pixels
- **Storage:** `outputs/regions/{image_id}_regions.json`
- **JSON structure:**
```json
{
  "image_id": "rgb_00",
  "regions": [
    {
      "region_id": 1,
      "bbox": [x, y, width, height],
      "mask": [[binary mask as list]],
      "mean_error": 0.456,
      "area": 234,
      "features": { /* 6 signals */ },
      "scores": { /* per-category scores */ },
      "top_cause": "occlusion",
      "confidence": "High"
    }
  ]
}
```

## 6.3 Output Data (Results)

### Per-Image Results
- **File:** `outputs/results/{image_id}_result.json`
- **Contents:** Metrics, region count, failure distribution, visualizations

### Aggregate Results
- **File:** `outputs/results/all_results.json`
- **Contents:** 50 images × statistics → summary metrics
- **Schema:** List of image results (one per input image)

### Correlation Results (for Paper)
- **File:** `outputs/correlations/correlation_analysis.csv`
- **Columns:** signal_name, r_pearson, p_value, significant, strength

### Failure Distribution
- **File:** `outputs/results/failure_distribution.csv`
- **Columns:** cause, count, percentage

---

# 7. CODE STRUCTURE & ORGANIZATION

## 7.1 Module Breakdown (src/ directory)

### 7.1.1 `config.py`
**Purpose:** Centralized configuration management

```python
# Paths
DATA_DIR = "data/raw_kitti"
OUTPUT_DIR = "outputs"
IMAGE_DIR = f"{DATA_DIR}/image"
GT_DIR = f"{DATA_DIR}/depth"

# Models
MODEL_ID = "depth-anything/Depth-Anything-V2-Small-hf"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Processing
ERROR_PERCENTILE = 85
MIN_REGION_AREA = 50

# Evidence signals
TEXTURE_VAR_THRESHOLD = 500
EDGE_DENSITY_SCALE = 3.0
CONTRAST_THRESHOLD = 60
BRIGHTNESS_EXTREMES = (60, 200)
ASPECT_RATIO_MIN = 3.0
DEPTH_DISCONTINUITY_THRESHOLD = 2.0

# Category thresholds (DECISION PENDING)
OCCLUSION_THRESHOLD = 2.0  # TBD: may change to 3.0-4.0
CONFIDENCE_HIGH = 0.6
CONFIDENCE_MEDIUM = 0.4
```

### 7.1.2 `models/depth_inference.py`
**Purpose:** Load and run Depth Anything V2

```python
class DepthEstimator:
    def __init__(self, model_id, device):
        self.pipe = pipeline("depth-estimation", model=model_id, device=device)
    
    def predict(self, image):
        """
        Args:
            image: RGB image as numpy array (H, W, 3)
        Returns:
            depth: Relative depth map (H, W)
        """
        result = self.pipe(Image.fromarray(image))
        return result["predicted_depth"].squeeze().numpy()
    
    def predict_batch(self, image_dir, image_ids):
        """Batch prediction with progress tracking"""
        # Implementation using tqdm for progress
```

### 7.1.3 `processing/alignment.py`
**Purpose:** Scale-shift alignment of relative to metric depth

```python
def align_scale_shift(pred, gt, valid_mask=None):
    """
    Least-squares fitting: gt ≈ scale*pred + shift
    
    Args:
        pred: Predicted depth (relative, from model)
        gt: Ground truth depth (metric, from LiDAR)
        valid_mask: Pixels where GT is valid (default: gt > 0)
    
    Returns:
        pred_aligned: Aligned predictions
        scale: Fitted scale factor
        shift: Fitted shift
    """
    if valid_mask is None:
        valid_mask = gt > 0
    
    if valid_mask.sum() < 10:
        return pred, 1.0, 0.0
    
    A = np.stack([pred[valid_mask], np.ones_like(pred[valid_mask])], axis=1)
    scale, shift = np.linalg.lstsq(A, gt[valid_mask], rcond=None)[0]
    
    return pred * scale + shift, float(scale), float(shift)
```

### 7.1.4 `processing/error_analysis.py`
**Purpose:** Compute metrics and error maps

```python
def compute_metrics(pred, gt, valid_mask=None):
    """
    Compute AbsRel, RMSE, Delta1
    Returns: dict with metrics
    """

def compute_error_map(pred, gt, valid_mask=None):
    """Pixel-wise relative error"""

def extract_failure_regions(error_map, valid_mask, percentile=85, min_area=50):
    """
    Threshold + connected components
    Returns: list of region dicts
    """
```

### 7.1.5 `features/evidence_signals.py`
**Purpose:** Compute 6 evidence signals

```python
def texture_variance(patch):
    """Signal 1: Texture variance"""

def edge_density(patch):
    """Signal 2: Edge density (Canny)"""

def brightness_contrast(patch):
    """Signal 3 & 4: Brightness and contrast"""

def saturation_highlights(patch):
    """Signal 5: Specular highlights"""

def region_shape(bbox):
    """Signal 6: Aspect ratio"""

def depth_discontinuity(gt_patch, mask_patch, valid_patch):
    """Signal 7: Depth gradient at boundary"""

def extract_features(rgb, gt, region):
    """Extract all 6 signals for a region"""
```

### 7.1.6 `features/scoring.py`
**Purpose:** Rule-based classification

```python
def score_categories(features):
    """
    Apply formulas to 6 signals → 6 category scores
    Returns: {category: score}
    """

def assign_top_cause(scores):
    """Select highest-scoring category"""

def assign_confidence(top_score, cluster_agreement=None):
    """High / Medium / Low"""

def classify_region(region_data):
    """End-to-end: features → scores → cause → confidence"""
```

### 7.1.7 `features/validation.py`
**Purpose:** Validation protocol

```python
def correlation_analysis(all_regions):
    """
    Compute Pearson r and p-value for each signal
    Returns: {signal: {r, p, significant}}
    """

def ablation_study(all_regions, drop_signal):
    """Re-score without one signal, measure impact"""

def compute_cohens_kappa(veo_labels, human_labels):
    """Agreement between VEO and human raters"""
```

### 7.1.8 `utils/io.py`
**Purpose:** File I/O

```python
def load_image(path):
    """Load RGB image"""

def load_depth_gt(path):
    """Load GT depth with 16-bit decoding"""

def save_json(data, path):
    """Save results to JSON"""

def load_json(path):
    """Load results from JSON"""

def list_image_pairs(image_dir, gt_dir):
    """Find matching RGB/GT pairs"""
```

### 7.1.9 `utils/visualization.py`
**Purpose:** Plot generation

```python
def plot_4_panel(rgb, pred, gt, error, regions):
    """Input | Predicted | GT | Error+Regions"""

def plot_failure_distribution(cause_counts):
    """Bar chart of failure causes"""

def plot_region_features(region, cause, scores):
    """Feature extraction visualization"""
```

## 7.2 Entry Points

### `scripts/run_pipeline.py` - Complete End-to-End
```python
def main():
    config = load_config()
    
    # 1. List images
    pairs = list_image_pairs(config.IMAGE_DIR, config.GT_DIR)
    
    # 2. Load model
    estimator = DepthEstimator(config.MODEL_ID, config.DEVICE)
    
    # 3. Process each image
    all_results = []
    for rgb_path, gt_path in pairs:
        result = process_single_image(
            estimator, rgb_path, gt_path, config
        )
        all_results.append(result)
    
    # 4. Aggregate results
    summary = aggregate_results(all_results)
    
    # 5. Save outputs
    save_json(all_results, "outputs/all_results.json")
    
    return all_results, summary
```

### `scripts/run_validation.py` - Validation Protocol
```python
def main():
    results = load_json("outputs/all_results.json")
    
    # 1. Correlation testing
    corr = correlation_analysis(results)
    
    # 2. Ablation study (optional, lengthy)
    ablation = ablation_study(results)
    
    # 3. Prepare for human rating
    export_regions_for_rating(results, count=100)
    
    return corr, ablation
```

---

# 8. CURRENT STATUS & DECISIONS

## 8.1 Work Completed (Weeks 1-7)

| Phase | Status | Deliverable | Notes |
|-------|--------|-------------|-------|
| **Phase 1** | ✓ Complete | KITTI 50 images + predictions | Depth Anything V2 |
| **Phase 2** | ✓ Complete | Scale-shift alignment | Metric depth ready |
| **Phase 3** | ✓ Complete | Error metrics + maps | AbsRel=0.160, RMSE=4.0 |
| **Phase 4** | ✓ Complete | 224 failure regions | 85th percentile threshold |
| **Phase 5** | ✓ Complete | 6 evidence signals | Feature extraction working |
| **Phase 6** | In Progress | Rule-based scoring | Pending decision on thresholds |
| **Phase 7** | Planned | Validation protocol | Week 9-10 |

## 8.2 Critical Decisions (PENDING)

### Decision 1: Occlusion Threshold
**Current:** 88.8% occlusion (199/224 regions)
**Question:** Is this realistic for KITTI, or formula too aggressive?
**Options:**
- A) Accept 88.8% as realistic
- B) Increase threshold: 2.0 → 3.0/4.0/5.0
- C) Scale other categories: multiply by 1.5-2.0
- D) Manual inspection of 15 regions

**Status:** AWAITING YOUR DECISION IN VS CODE
**Impact:** Affects failure distribution entirely

### Decision 2: Weak Correlation Signals
**Current:** Will know after CELL 5 correlation testing
**Question:** Which signals don't correlate with error? Keep or drop?
**Options:**
- A) Keep all signals
- B) Drop non-significant signals
- C) Keep but note as limitations

**Status:** AWAITING YOUR DECISION IN VS CODE
**Impact:** Affects scientific rigor of paper

### Decision 3: MVP Categories (5 or 6)
**Current:** Reflection = 4.9% (11 regions)
**Question:** Is reflection MVP or extended scope?
**Options:**
- A) Keep 6 categories (reflection MVP)
- B) Revert to 5 (match proposal)
- C) Keep 6 but document as research finding

**Status:** AWAITING YOUR DECISION IN VS CODE
**Impact:** Affects framework scope and paper narrative

## 8.3 Configuration State

```python
# config.py CURRENT VALUES (subject to your decisions)

# DECISION 1: Occlusion
DEPTH_DISCONTINUITY_THRESHOLD = 2.0  # TBD: test 3.0, 4.0 after decision

# DECISION 2: Category scaling
CATEGORY_SCALE_FACTOR = 1.0  # TBD: test 1.5, 2.0 if needed

# DECISION 3: Categories
INCLUDE_REFLECTION_MVP = True  # TBD: False if reverting to 5 categories
```

---

# 9. LOCAL DEVELOPMENT SETUP (VS CODE)

## 9.1 Prerequisites
- Python 3.9+
- Git
- VS Code with Python extension
- GPU (optional, but recommended for speed)

## 9.2 Step 1: Clone Repository

```bash
# Create project directory
mkdir VEO_Project
cd VEO_Project

# Initialize git (if not already done)
git init

# Create directory structure
mkdir -p data/raw_kitti/{image,depth}
mkdir -p outputs/{predictions,error_maps,regions,evidence,visualizations,results,correlations}
mkdir -p src/{models,processing,features,utils}
mkdir -p notebooks tests scripts paper docs
mkdir -p .github/workflows
```

## 9.3 Step 2: Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## 9.4 Step 3: Download KITTI Data

```bash
# Option 1: Manually download from http://www.cvlibs.net/datasets/kitti/
#           Place 50 images in data/raw_kitti/image/
#           Place 50 depth maps in data/raw_kitti/depth/

# Option 2: Use script (create scripts/download_kitti.py)
python scripts/download_kitti.py --count 50

# Verify
ls data/raw_kitti/image | wc -l  # Should show 50
ls data/raw_kitti/depth | wc -l  # Should show 50
```

## 9.5 Step 4: Configure VS Code

### `.vscode/settings.json`
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "[python]": {
        "editor.formatOnSave": true,
        "editor.rulers": [80, 120]
    }
}
```

### `.vscode/launch.json` (Debugging)
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "VEO Pipeline",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/scripts/run_pipeline.py",
            "console": "integratedTerminal"
        }
    ]
}
```

## 9.6 Step 5: Verify Installation

```bash
# Test imports
python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"

# Test GPU
python -c "import torch; print(f'GPU available: {torch.cuda.is_available()}')"

# Run quick sanity check
python -c "from src.config import *; print('Config loaded successfully')"
```

---

# 10. STEP-BY-STEP EXECUTION GUIDE

## 10.1 Week 8: Error Diagnosis & Decision-Making

### Step 1: Load and Verify Data
```bash
cd VEO_Project
source venv/bin/activate

# Run verification
python scripts/verify_data.py
# Expected output: 50 images, 50 depth maps, all paired correctly
```

### Step 2: Run CELL 1-2 (Investigation)
- Create new notebook: `notebooks/01_diagnosis.ipynb`
- Copy code from `COLAB_CELL_1_Setup.py` (adapt paths for local)
- Copy code from `COLAB_CELL_2_Issue1_Investigation.py`
- Run and observe output

**Expected output:**
- Failure cause distribution
- Graphs showing 88.8% occlusion
- Statistics on depth_discontinuity

### Step 3: Make Decision #1 (Occlusion)
- Review CELL 2 output
- Choose A/B/C/D based on findings
- Document decision in `docs/DECISIONS.md`

### Step 4: Implement Decision #1
- Copy relevant code from `COLAB_CELL_4_Issue1_Implementation.py`
- Adapt for local execution
- Update `src/config.py` with new threshold/scale
- Re-run failure classification

**Expected output:**
- New failure distribution
- Before/after comparison graphs
- Updated `outputs/all_results.json`

### Step 5: Correlation Testing (CELL 5)
- Run `scripts/run_validation.py --test correlation`
- Generate correlation table
- Identify weak signals

**Expected output:**
- `outputs/correlations/correlation_analysis.csv`
- Visualization of correlations

### Step 6: Make Decision #2 (Signals)
- Review correlation results
- Choose A/B/C
- Document in `docs/DECISIONS.md`

### Step 7: Make Decision #3 (Categories)
- Review reflection prevalence (4.9%)
- Choose A/B/C
- Document in `docs/DECISIONS.md`

### Step 8: Implement Decisions #2 & #3
- Update feature extraction if dropping signals
- Update category list if reverting to 5
- Re-run full pipeline

**End of Week 8:** All 3 decisions made, decisions documented, framework improved

---

## 10.2 Week 9: Validation Setup

### Step 1: K-means Clustering
```bash
python scripts/run_clustering_validation.py

# Outputs:
# - outputs/correlations/cluster_composition.csv
# - Cluster visualization plots
```

### Step 2: Prepare Human Rating Data
```bash
python scripts/prepare_human_rating.py --count 100

# Outputs:
# - outputs/human_rating/regions_to_label.csv
# - outputs/human_rating/patches/ (100 RGB patches + error maps)
# - outputs/human_rating/rater_instructions.md
```

### Step 3: Recruit Raters & Send Instructions
- Email 2-3 potential raters
- Send files from human_rating/ directory
- Set deadline: 1 week

### Step 4: Start ZoeDepth Inference (parallel)
```bash
# Update config.py
MODEL_ID = "Intel/zoedepth-nyu-indoor"

python scripts/run_pipeline.py --model zoedepth

# Outputs:
# - outputs/predictions/zoedepth/
# - outputs/zoedepth_results.json
```

---

## 10.3 Week 10: Validation & Analysis

### Step 1: Receive Human Labels
- Raters return CSV with their classifications
- Save to `outputs/human_rating/rater_responses.csv`

### Step 2: Compute Cohen's Kappa
```bash
python scripts/compute_agreement.py

# Outputs:
# - outputs/correlations/cohens_kappa.txt
# - Confusion matrix visualization
```

**Expected:** Cohen's kappa ≥ 0.65 for "substantial agreement"

### Step 3: Ablation Study
```bash
python scripts/run_ablation_study.py

# Outputs:
# - outputs/correlations/ablation_results.csv
# - Which signals matter most?
```

### Step 4: Cross-Model Analysis
```bash
python scripts/cross_model_comparison.py

# Outputs:
# - outputs/results/cross_model_analysis.csv
# - Failure distribution comparison (DA2 vs ZoeDepth)
```

---

## 10.4 Week 11-12: Paper Writing

### Step 1: Generate Paper Tables
```bash
python scripts/generate_paper_tables.py

# Outputs all tables for paper:
# - Metrics table
# - Correlation table
# - Cohen's kappa table
# - Ablation results
# - Cross-model comparison
# - Failure distribution
```

### Step 2: Export Figures
```bash
python scripts/generate_paper_figures.py

# All paper figures saved to paper/figures/
```

### Step 3: Write Paper (Using Generated Results)
- See Section 13 for paper structure
- All numbers come from outputs/

---

# 11. EXPECTED OUTPUTS & MILESTONES

## 11.1 Weekly Milestones

| Week | Expected Output | File Location |
|------|---|---|
| 8 | Occlusion issue resolved + corr analysis | `/outputs/all_results_updated.json`, `/correlations/` |
| 9 | Clustering validation + ZoeDepth predictions | `/correlations/cluster_*.csv`, `/predictions/zoedepth/` |
| 10 | Cohen's kappa + ablation results | `/correlations/cohens_kappa.txt`, `/ablation/` |
| 11 | Cross-model analysis + paper tables | `/results/cross_model_analysis.csv`, `/paper/tables/` |
| 12 | Complete paper draft | `/paper/veo_research_paper.md` |

## 11.2 Key Result Files (For Paper)

| File | Purpose | Format |
|------|---------|--------|
| `correlations/correlation_analysis.csv` | Feature-error correlation table | CSV |
| `correlations/cohens_kappa.txt` | Human agreement headline | TXT |
| `results/cross_model_analysis.csv` | DA2 vs ZoeDepth comparison | CSV |
| `results/failure_distribution.csv` | Cause counts & percentages | CSV |
| `figures/failure_distribution_bar.png` | Bar graph for paper | PNG |
| `figures/correlation_scatter.png` | Scatter plots of top signals | PNG |
| `figures/4panel_examples.png` | Representative failure cases | PNG |

---

# 12. VALIDATION PROTOCOL

## 12.1 Validation Steps (in order)

### Step 1: Evidence-Error Correlation (Week 8)
**Goal:** Prove each signal correlates with error
**Method:** Pearson correlation + p-value test
**Acceptance:** p < 0.05 for at least 4/6 signals
**Output:** `correlations/correlation_analysis.csv`

### Step 2: K-means Clustering (Week 9)
**Goal:** Verify rule-based categories form coherent clusters
**Method:** K-means (k=6) on standardized features
**Acceptance:** Silhouette score > 0.3
**Output:** `correlations/cluster_composition.csv`

### Step 3: Human Expert Agreement (Week 10)
**Goal:** Prove VEO classifications match human judgment
**Method:** Blind labeling of 100-150 regions by 2-3 experts
**Acceptance:** Cohen's kappa ≥ 0.65
**Output:** `correlations/cohens_kappa.txt`

### Step 4: Ablation Study (Week 10)
**Goal:** Prove each signal contributes to classification
**Method:** Drop each signal, re-score, measure agreement drop
**Acceptance:** >5% drop in kappa when removing top signal
**Output:** `correlations/ablation_results.csv`

### Step 5: Cross-Model Consistency (Week 11)
**Goal:** Show failure patterns differ across models
**Method:** Run same pipeline on ZoeDepth
**Acceptance:** Different distributions (χ² test p < 0.05)
**Output:** `results/cross_model_analysis.csv`

## 12.2 Validation Report Template

```markdown
# VEO Validation Report

## 1. Evidence-Error Correlation
- [Pearson r values for each signal]
- [p-values and significance]
- [Conclusion: X out of 6 signals significant]

## 2. Clustering Quality
- [Silhouette score]
- [Cluster composition table]
- [Conclusion: Clusters are coherent]

## 3. Human Agreement
- [Cohen's kappa: X.XX]
- [Per-category kappa table]
- [Confusion matrix]
- [Conclusion: Substantial agreement achieved]

## 4. Ablation Study
- [Signal importance ranking]
- [Kappa drop per signal removed]
- [Conclusion: All signals contribute]

## 5. Cross-Model Consistency
- [Failure distribution comparison]
- [χ² test results]
- [Conclusion: Models fail differently]
```

---

# 13. PAPER WRITING INTEGRATION

## 13.1 Paper Structure (with Output Files)

### Title & Abstract
- Title: Vision Error Observatory: A Validated, Evidence-Based Framework for Region-Level Failure Diagnosis in Monocular Depth Estimation
- Abstract (150-200 words)
  - Problem: MDE metrics are aggregate; failures hidden
  - Method: VEO framework (6 signals + rule-based + validation)
  - Results: Cohen's kappa = X.XX, cross-model differences revealed
  - Contribution: Systematic, validated failure diagnosis

### 1. Introduction (1.5 pages)
- Hook: "Monocular depth estimation reports RMSE but not WHERE failures occur"
- Gap: No method links failure regions to visual causes + validates correctness
- VEO: Model-agnostic, interpretable, validated
- Roadmap: Sections 2-10 cover background through results

### 2. Background (1 page)
- MDE evolution (Eigen 2014 → Depth Anything V2 2024)
- Standard metrics and their insufficiency
- Why pixel-level, cause-attributed analysis is needed

### 3. Related Work (2 pages)
- Table of research areas (Part VI spec)
- Key limitations in each
- Differentiate: prior work localizes OR classifies; VEO does both + validates

**Use:** `outputs/` contains no data for this; write from spec

### 4. Methodology (2.5 pages)
- 4.1 System Overview (pipeline diagram)
- 4.2 Error Analysis (pixel-wise metrics)
- 4.3 Evidence Signals (6 signals + formulas)
- 4.4 Rule-Based Scoring (confidence levels)
- 4.5 Validation Protocol (correlation + ablation + human agreement)

**Use:** `src/` code + formulas in Section 5 (this document)

### 5. Experimental Setup (0.5 pages)
- Dataset: KITTI 50 images
- Models: Depth Anything V2, ZoeDepth
- Validation: 100-150 manually labeled regions, 2-3 human raters
- Metrics: Cohen's kappa, Pearson correlation, ablation delta

### 6. Results (2 pages)
- 6.1 Baseline Metrics
  - `outputs/results/all_results.json` → table of AbsRel, RMSE, Delta1
- 6.2 Feature-Error Correlation
  - `outputs/correlations/correlation_analysis.csv` → table + interpretation
- 6.3 Failure Distribution
  - `outputs/results/failure_distribution.csv` → bar graph
- 6.4 Validation Results
  - `outputs/correlations/cohens_kappa.txt` → Cohen's kappa table
- 6.5 Cross-Model Analysis
  - `outputs/results/cross_model_analysis.csv` → comparison table
- 6.6 Representative Cases
  - `outputs/figures/4panel_examples.png` → 3 visual examples with step-by-step

### 7. Ablation Study (0.75 pages)
- `outputs/correlations/ablation_results.csv` → table + interpretation
- Which signals matter most?

### 8. Discussion (1 page)
- Interpret results vs. RQ1-RQ5
- Compare to prior work (DEDN, Singla, Csurka)
- Insights: occlusion dominance in KITTI, model-specific patterns
- Actionable: debuggability of depth models

### 9. Limitations (0.5 pages)
- Small model (ViT-S), small dataset (50 images), sparse GT
- Hand-tuned thresholds (future: learn from data)
- Limited to vision-transformer family

### 10. Conclusion & Future Work (0.5 pages)
- Summary: Systematic, validated failure diagnosis
- Path: Expand to NYU, learn thresholds, test more models

### 11. References
- All papers from Part XXV (verified)
- Must cite: Singla 2021, Csurka 2024, Chawla 2021 (DEDN)

## 13.2 Generate Paper Output Automatically

```bash
# Script: scripts/generate_paper_markdown.py

python scripts/generate_paper_markdown.py

# This generates:
# paper/veo_research_paper.md (complete paper skeleton with all results inserted)
# paper/veo_research_paper.pdf (via pandoc)
```

---

# 14. GITHUB WORKFLOW & VERSION CONTROL

## 14.1 GitHub Repository Setup

```bash
# Initialize git
git init
git remote add origin https://github.com/yourusername/veo-project.git

# Create .gitignore
echo "
venv/
__pycache__/
*.pyc
data/raw_kitti/
outputs/predictions/
outputs/error_maps/
outputs/regions/
.DS_Store
*.ipynb_checkpoints
" > .gitignore

# First commit
git add -A
git commit -m "Initial commit: VEO project structure"
git push -u origin main
```

## 14.2 Branching Strategy

```
main (production-ready)
  └── develop (integration branch)
        ├── feature/occlusion-threshold-tuning
        ├── feature/correlation-testing
        ├── feature/zoedepth-inference
        └── feature/paper-generation
```

## 14.3 Commit Workflow

```bash
# Create feature branch
git checkout -b feature/occlusion-threshold-tuning

# Make changes, commit frequently
git add src/config.py
git commit -m "Adjust occlusion threshold from 2.0 to 3.0 per correlation analysis"

# Push to remote
git push origin feature/occlusion-threshold-tuning

# Create Pull Request on GitHub
# Describe: what changed, why, which outputs affected
# Reference: #1 (issue number)

# After review, merge to develop
git checkout develop
git merge --no-ff feature/occlusion-threshold-tuning
git push origin develop

# When week is complete, merge to main
git checkout main
git merge --no-ff develop
git tag -a v0.8 -m "Week 8: Error diagnosis complete"
git push origin main --tags
```

## 14.4 Version Tagging

```
v0.7 — Week 7: Initial pipeline complete
v0.8 — Week 8: Error diagnosis & decisions complete
v0.9 — Week 9: Validation setup complete
v1.0 — Week 10: Human agreement measured
v1.1 — Week 11: Cross-model analysis complete
v1.2 — Week 12: Paper draft submitted
v2.0 — Final submission version
```

---

# 15. TESTING & QUALITY ASSURANCE

## 15.1 Unit Tests

### `tests/test_alignment.py`
```python
def test_scale_shift_alignment():
    pred = np.random.rand(10, 10)
    gt = 2.0 * pred + 1.0
    valid_mask = np.ones((10, 10), dtype=bool)
    
    pred_aligned, scale, shift = align_scale_shift(pred, gt, valid_mask)
    
    # Assertions
    assert np.isclose(scale, 2.0, atol=0.01)
    assert np.isclose(shift, 1.0, atol=0.01)
```

### `tests/test_scoring.py`
```python
def test_confidence_assignment():
    assert assign_confidence(0.75) == "High"
    assert assign_confidence(0.50) == "Medium"
    assert assign_confidence(0.25) == "Low"
```

## 15.2 Integration Tests

### `tests/test_pipeline.py`
```python
def test_end_to_end_single_image():
    config = load_config()
    estimator = DepthEstimator(config.MODEL_ID, config.DEVICE)
    
    rgb_path = "data/raw_kitti/image/rgb_00.png"
    gt_path = "data/raw_kitti/depth/depth_00.png"
    
    result = process_single_image(estimator, rgb_path, gt_path, config)
    
    # Assertions
    assert result['abs_rel'] > 0
    assert result['abs_rel'] < 1.0
    assert len(result['regions']) > 0
    assert all('top_cause' in r for r in result['regions'])
```

## 15.3 Run Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test
python -m pytest tests/test_alignment.py::test_scale_shift_alignment -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=html
```

---

# 16. TROUBLESHOOTING GUIDE

## 16.1 Common Issues

### Issue: "CUDA out of memory"
**Cause:** Batch processing with large images
**Solution:**
```python
# Reduce batch size in config
BATCH_SIZE = 1

# Or use CPU
DEVICE = "cpu"
```

### Issue: "File not found: depth map"
**Cause:** Mismatched RGB/GT filenames
**Solution:**
```bash
# Debug: check if files are paired correctly
python -c "
from src.utils.io import list_image_pairs
pairs = list_image_pairs('data/raw_kitti/image', 'data/raw_kitti/depth')
print(f'Found {len(pairs)} pairs')
"
```

### Issue: "Correlation p-value = 1.0 (not significant)"
**Cause:** Signal has no variance or wrong computation
**Solution:**
```python
# Debug: check signal values
print(np.unique(signal_values[:10]))  # Should have variation
print(f"Min: {np.min(signal_values)}, Max: {np.max(signal_values)}")
```

---

# APPENDIX A: QUICK REFERENCE

## A.1 Common Commands

```bash
# Activate environment
source venv/bin/activate

# Run full pipeline
python scripts/run_pipeline.py

# Run validation
python scripts/run_validation.py

# Generate paper
python scripts/generate_paper_markdown.py

# Run tests
python -m pytest tests/ -v

# Check GPU
python -c "import torch; print(torch.cuda.is_available())"
```

## A.2 Key File Paths

```
Config:                src/config.py
Main entry:            scripts/run_pipeline.py
Results (all images):  outputs/results/all_results.json
Correlation table:     outputs/correlations/correlation_analysis.csv
Cohen's kappa:         outputs/correlations/cohens_kappa.txt
Paper draft:           paper/veo_research_paper.md
```

## A.3 Key Decision Variables (config.py)

```python
DEPTH_DISCONTINUITY_THRESHOLD = 2.0  # TBD
CATEGORY_SCALE_FACTOR = 1.0  # TBD
INCLUDE_REFLECTION_MVP = True  # TBD
ERROR_PERCENTILE = 85  # FIXED
MIN_REGION_AREA = 50  # FIXED
```

---

# APPENDIX B: GITHUB COPILOT CONTEXT

When using GitHub Copilot in VS Code, it will have access to:

1. **Project context:** `.github/workflows/`, structure, naming conventions
2. **Code style:** Existing functions in `/src/`, docstrings, type hints
3. **Domain knowledge:** This document (PROJECT_SPECIFICATION.md)
4. **Configuration:** `src/config.py` (centralized params)

**Best practices for Copilot:**

```python
# ✓ GOOD — Copilot understands the domain
def extract_features(rgb_patch, gt_patch, mask_patch, valid_patch):
    """
    Extract 6 evidence signals from a failure region.
    
    Args:
        rgb_patch: RGB image patch (H, W, 3)
        gt_patch: Ground truth depth patch (H, W)
        mask_patch: Region mask (binary)
        valid_patch: Valid pixel mask (binary, for sparse GT)
    
    Returns:
        dict: {signal_name: value} for all 6 signals
    """
    # Copilot will complete correctly based on docstring

# ✓ GOOD — References config instead of magic numbers
def score_categories(features):
    scores = {
        'occlusion': min(1, features['depth_discontinuity'] / config.DEPTH_DISCONTINUITY_THRESHOLD),
        # ...
    }

# ✗ BAD — Magic numbers, no context
def score_cat(f):
    return {'occ': min(1, f['dd'] / 2.0)}
```

---

**END OF PROJECT SPECIFICATION**

**This document should be your reference during all local development in VS Code.**  
**Share it with your team and with GitHub Copilot for best results.**

**All decisions are **AWAITING YOUR INPUT** in VS Code.** Start with **Section 10: Step-by-Step Execution Guide**.

