# VEO Project Information and Evaluator-Feedback Response

**Project:** Vision Error Observatory (VEO)  
**Repository:** `MdZeeshanAli01/VEO_V2`  
**Document status:** Current implementation audit and execution plan  
**Prepared:** October 2026

## 1. Purpose of this document

This document answers three questions:

1. What has already been implemented in the repository?
2. Which evaluator requests are complete, partially complete, or still open?
3. What should two team members implement next, and how will completion be verified?

The status below is based on the code, configuration, tests, documentation, and generated output files currently present in the repository. A feature being implemented in code is not treated as a completed research result until the required experiment has been run and its evidence has been reported.

## 2. Project summary

VEO is a ground-truth-assisted, post-hoc diagnostic pipeline for monocular depth-estimation models. It does not train a new depth model. Its purpose is to identify *where* a model produces large depth errors and record measurable visual or geometric evidence associated with possible failure hypotheses.

The current pipeline is:

1. Discover aligned RGB/depth samples.
2. Load depth in metres and create a valid-depth mask.
3. Obtain a prediction from a pretrained model or a precomputed prediction file.
4. Optionally align relative/inverse-depth output to metric ground truth.
5. Compute global depth metrics and a pixel-level relative-error map.
6. Threshold the error map and extract connected failure regions.
7. Extract region-level RGB/depth features.
8. Score interpretable failure hypotheses.
9. Save per-image records, region records, summaries, correlations, and visual panels.

The current scientific scope is indoor evaluation using **NYU Depth V2** and the official metric-depth **Hypersim** profile. The repository explicitly avoids treating the current small runs as final publication results.

## 3. Evaluator feedback: implementation audit

### Status legend

- **Implemented and evidenced:** the code exists and a relevant experiment/output is present.
- **Implemented, but evidence incomplete:** the mechanism exists, but the evaluator-required full experiment, validation, or written result is missing.
- **Not implemented:** no reliable repository evidence was found.
- **Scope mismatch:** the request names a dataset/model or claim that is not part of the current verified scope.

| Evaluator request | Current status | What is already present | What is still required |
|---|---|---|---|
| 1. Quantitative evaluation on KITTI and NYU, including depth metrics and region-level detection | **Partially implemented; KITTI scope mismatch** | Metrics, error maps, connected regions, summaries, and NYU scene splits are implemented. Full NYU split artifacts exist for 1,009 development, 196 validation, and 244 test samples in the alignment-ablation run. | Run and report the complete approved NYU benchmark as a final table. Add KITTI only if the team chooses to expand scope and can define sparse-depth validity rules. The current project explicitly says not to use KITTI sparse-depth assumptions. |
| 2. Validate cause assignments against human experts with classification/agreement metrics | **Preparation implemented; validation not complete** | `cohens_kappa`, ablation support, blinded rating-package export, rater instructions, and a CSV template exist. The classifier also supports `ambiguous`. | Obtain labels from at least two independent raters for at least 200 blinded regions, then calculate human-human agreement, VEO-human agreement, per-class precision/recall/F1, macro-F1, and a confusion matrix. |
| 3. Explain threshold selection and evaluate sensitivity | **Implemented in code; results require reporting** | The baseline is per-image 85th-percentile valid-pixel relative error with minimum region area 25. The alignment-ablation runner computes 75th, 85th, 90th, and 95th percentile region summaries. | Add a clear written threshold rationale and publish the sensitivity table/plots. Use validation for calibration and keep test settings frozen. |
| 4. Demonstrate model-agnostic behavior with another pretrained model such as ZoeDepth | **Infrastructure is model-agnostic; ZoeDepth comparison not evidenced** | The pipeline accepts precomputed predictions and has a Transformers adapter, so the diagnosis stage is separated from model inference. | Run the same frozen protocol on ZoeDepth or another documented second model, record checkpoint/preprocessing/output-space details, and compare global metrics, region counts, cause distributions, and failure examples. |
| 5. Strengthen related work and identify the contribution beyond error maps | **Partially addressed in project documentation; paper-ready comparison still required** | The project specification discusses the motivation, error analysis, uncertainty, explainability, and model-debugging gap. The research protocol defines VEO as region-level, evidence-based post-hoc diagnosis rather than causal explanation. | Rewrite the paper’s related-work section with verified citations and a comparison table. Clearly state that VEO adds region localization, measurable evidence features, interpretable hypotheses, uncertainty/ambiguity handling, and human-validation protocol beyond a plain error map. |

## 4. What has already been implemented

### 4.1 Reproducible data and experiment configuration

Implemented in:

- [configs/nyu.yaml](../configs/nyu.yaml)
- [configs/hypersim.yaml](../configs/hypersim.yaml)
- [src/veo_nyu/config.py](../src/veo_nyu/config.py)
- [src/veo_nyu/data.py](../src/veo_nyu/data.py)
- [src/veo_nyu/nyu_dataset.py](../src/veo_nyu/nyu_dataset.py)

The configuration records the dataset, depth scale, maximum evaluation depth, split, model type, prediction space, alignment protocol, error percentile, minimum region area, feature scales, ambiguity margin, and random seed.

The NYU preparation code creates scene-level development/validation/test partitions with seed `42`. This prevents frames from the same scene leaking across splits. The repository contains split metadata and manifests, and the full alignment-ablation artifacts contain 1,009 development, 196 validation, and 244 test records.

**Why this was implemented:** random frame-level splitting can make evaluation overly optimistic because nearby frames from one scene are visually related. Scene-level splits make the final evaluation more defensible.

### 4.2 Depth metrics and prediction-space handling

Implemented in [src/veo_nyu/metrics.py](../src/veo_nyu/metrics.py):

- MAE
- RMSE
- AbsRel
- SqRel
- delta1, delta2, delta3
- Spearman correlation
- valid-pixel and finite-value masking
- direct depth scale-shift alignment
- inverse-depth scale-shift alignment
- scale-only alignment

The NYU profile treats the Hugging Face Depth Anything V2 checkpoint as inverse-depth-like and evaluates the reconstructed metric depth. The Hypersim metric checkpoint is evaluated directly in metres without fitted alignment.

**Why this was implemented:** relative-depth models do not have a fixed metric scale. Fitting in the correct inverse-depth space avoids polarity and geometry errors. Recording multiple alignment protocols also makes the choice auditable rather than hidden.

### 4.3 Error localization and region formation

Implemented in:

- [src/veo_nyu/regions.py](../src/veo_nyu/regions.py)
- [src/veo_nyu/pipeline.py](../src/veo_nyu/pipeline.py)

The baseline computes valid-pixel relative error, selects the per-image 85th percentile as the high-error threshold, creates a binary mask, extracts connected components, and removes regions smaller than 25 pixels. Each retained region includes a bounding box, area, mean error, features, scores, cause, confidence, and score margin.

**Why this was implemented:** global metrics say how much error exists but not where it occurs. Connected regions convert a dense error map into inspectable, countable units for diagnosis.

### 4.4 Evidence features and interpretable classification

Implemented in:

- [src/veo_nyu/features.py](../src/veo_nyu/features.py)
- [src/veo_nyu/scoring.py](../src/veo_nyu/scoring.py)

The current evidence signals include:

- texture variance
- edge density
- brightness
- contrast
- highlight ratio
- aspect ratio
- depth discontinuity
- mean depth

The classifier scores:

- `textureless`
- `boundary_mixing`
- `poor_lighting`
- `thin_object`
- `occlusion`
- `reflection`
- `ambiguous`

The `ambiguous` result is produced when the leading score is weak or too close to the next score. It is not silently converted into a forced cause.

**Why this was implemented:** the goal is an interpretable diagnostic hypothesis, not an unsupported claim that VEO has recovered the model’s true internal cause. The ambiguity class makes uncertainty explicit.

### 4.5 Reports and visual inspection outputs

Implemented in:

- [src/veo_nyu/reports.py](../src/veo_nyu/reports.py)
- [src/veo_nyu/visualization.py](../src/veo_nyu/visualization.py)
- [src/veo_nyu/runner.py](../src/veo_nyu/runner.py)

Runs save JSON records, `summary.json`, `regions.csv`, `correlations.csv`, prediction arrays, and RGB/ground-truth/prediction/error panels.

One completed Hypersim artifact is available at [outputs/hypersim/official_metric_results.json](../outputs/hypersim/official_metric_results.json). It contains one sample, 45 detected regions, AbsRel `0.025896`, RMSE `0.102643`, and delta1 `0.998374`. This is useful engineering evidence, but it is **not** a dataset-level result.

The 10-image NYU artifacts contain 151 regions. The tuned classifier output contains 68 ambiguous, 23 reflection, 21 textureless, 19 boundary-mixing, 12 poor-lighting, and 8 thin-object regions. This demonstrates the classifier behavior, but it is explicitly not human validation.

### 4.6 Threshold and alignment sensitivity infrastructure

Implemented in [src/veo_nyu/runner.py](../src/veo_nyu/runner.py), with results under [outputs/alignment_ablation_full/](../outputs/alignment_ablation_full/).

The runner evaluates:

- no alignment
- direct-depth scale-shift
- inverse-depth scale-shift
- inverse-depth scale-only

It also computes region summaries at the 75th, 85th, 90th, and 95th percentiles and bootstrap confidence intervals grouped by scene.

For example, on the 244-sample NYU test split, inverse-depth scale-shift reports AbsRel `0.103975`, RMSE `0.466396`, and delta1 `0.896472`. These are existing generated results, but they should be checked against the final frozen model/configuration before being used as headline paper numbers.

**Why this was implemented:** alignment and threshold choices can change both metric performance and detected region structure. Sensitivity analysis prevents presenting one arbitrary setting as universally valid.

### 4.7 Human-rating preparation

Implemented in [src/veo_nyu/validation.py](../src/veo_nyu/validation.py) and exposed through the `prepare-rating` CLI command.

The export creates:

- blinded visual panels
- `rating_template.csv`
- `rater_instructions.md`

The template does not expose VEO’s predicted label or score to the rater.

**Why this was implemented:** human validation must be blinded; otherwise raters can reproduce the system’s output instead of independently judging the region.

### 4.8 Tests and research guardrails

Implemented in [tests/test_core.py](../tests/test_core.py) and [docs/RESEARCH_PROTOCOL_V1.md](RESEARCH_PROTOCOL_V1.md).

The tests cover alignment, masking, metrics, region extraction, classifier ambiguity, pair discovery, report export, NYU extraction/split disjointness, feature edge cases, and perfect Cohen’s kappa.

The frozen protocol explicitly limits claims to evidence-associated hypotheses and disallows causal claims, RGB-only deployment claims, and generalization claims from a single dataset or ten-image sample.

## 5. Important findings and limitations

### 5.1 KITTI is not currently completed

The evaluator requested KITTI and NYU. The current repository is organized around NYU and Hypersim. The README explicitly states that KITTI sparse-depth assumptions must not be used in this project. Therefore, KITTI should not be claimed as completed.

If KITTI is added, it needs a separate documented data contract covering sparse ground-truth validity, crop policy, minimum valid pixels, depth cap, scene split policy, and comparison with the NYU dense-depth protocol. Do not simply point the NYU loader at KITTI files.

### 5.2 Human validation is prepared, not performed

Having a `cohens_kappa` function and a rating template is not evidence of agreement. The project still needs real independent labels and the full classification report.

### 5.3 The current Hypersim result is only one sample

The Hypersim output demonstrates that the official metric model can be connected to VEO and that the pipeline emits metrics and regions. It does not establish performance across Hypersim or support a general model/dataset claim.

### 5.4 ZoeDepth is not currently demonstrated

The architecture can accept another model’s predictions, but no verified ZoeDepth result is present in the current evidence inventory. “Model-agnostic” is currently an architectural property, not yet a completed comparative experiment.

### 5.5 A causal interpretation is not justified

The classifier generates evidence-based hypotheses. It does not prove that texturelessness, occlusion, lighting, or another feature caused the model error. Controlled image interventions would be required for a causal/faithfulness claim.

## 6. Two-member implementation plan

The plan below divides the remaining work into two tracks. Both members should use the same frozen protocol, model checkpoint records, random seed, and output naming conventions.

### Member 1 — Benchmarking, sensitivity, and second-model evaluation

**Objective:** complete the quantitative evidence requested in evaluator points 1, 3, and 4.

#### Step 1: Freeze the experiment manifest

Record:

- exact commit hash
- dataset split manifests
- model/checkpoint identifiers
- device and package versions
- configuration files
- maximum depth and validity policy
- primary alignment protocol

Do not tune the test split after inspecting its results.

#### Step 2: Complete the NYU benchmark

Run the full development, validation, and test evaluation using the documented scene-level splits. Produce one table containing, for each split:

- number of samples
- number of valid pixels or valid-pixel policy
- MAE
- RMSE
- AbsRel
- SqRel
- delta1, delta2, delta3
- Spearman correlation
- number of high-error regions
- mean regions per image
- cause distribution

Use the existing `evaluate-splits` command and preserve the generated JSON/CSV outputs.

#### Step 3: Report threshold sensitivity

Use the existing alignment-ablation runner to report 75th, 85th, 90th, and 95th percentile behavior. Include:

- region count
- region pixels
- mean region area
- change in region ranking or cause distribution where applicable

Explain why 85th percentile and minimum area 25 remain the baseline. Calibration decisions belong to development/validation; the test setting must remain frozen.

#### Step 4: Evaluate a second model

Run the same diagnosis pipeline on ZoeDepth if the dependency/checkpoint is reproducible. If ZoeDepth cannot be made reproducible in the current environment, select another documented pretrained model and state the substitution explicitly.

For both models, compare:

- model and output space
- preprocessing
- global depth metrics
- number and size of failure regions
- failure-cause distribution
- representative region panels

The error-localization, feature, and scoring configuration must remain unchanged between models.

#### Step 5: Optional KITTI decision

Before implementing KITTI, obtain team approval that expanding the dataset scope is worth the additional protocol work. If approved, implement a dedicated KITTI adapter and report NYU and KITTI separately. If not approved, document KITTI as an explicit out-of-scope limitation rather than implying completion.

**Member 1 acceptance criteria:**

- Reproducible full NYU result files exist for all required splits.
- A final metrics table and threshold-sensitivity table can be generated directly from those files.
- A second-model comparison uses the same frozen VEO diagnosis settings.
- No test-set tuning is introduced.
- Any KITTI result follows a dedicated sparse-depth protocol.

### Member 2 — Human validation, related work, and final research claims

**Objective:** complete evaluator points 2 and 5 and convert implementation evidence into defensible research claims.

#### Step 1: Prepare the blinded rating set

Use the existing `prepare-rating` command on the frozen test results. Select at least 200 regions if the dataset output contains enough regions. Check that the package contains no VEO predicted label, score, or confidence visible to raters.

#### Step 2: Collect independent annotations

Use at least two independent raters. Each rater should assign:

- one primary category from the frozen taxonomy
- confidence (`high`, `medium`, or `low`)
- optional notes

Raters must receive the same instructions and must not discuss individual panels during independent annotation.

#### Step 3: Compute validation metrics

Implement or add a report that calculates:

- human-human Cohen’s kappa
- VEO-human Cohen’s kappa for each rater
- per-category precision
- per-category recall
- per-category F1
- macro-F1
- confusion matrix
- support/count per category

Report `ambiguous` as a real class. Do not remove disagreements or empty categories without documenting the decision.

#### Step 4: Run signal ablation

Use `ablation_change` to remove one evidence signal at a time. Report:

- changed-region count
- total-region count
- percentage changed
- cause-specific changes where sample counts permit

Interpret this as sensitivity of the rule-based classifier, not as proof that a signal is causally responsible.

#### Step 5: Rewrite related work and contribution claims

Create a verified comparison table covering:

- global depth metrics
- error-map methods
- uncertainty/confidence methods
- model-centric explainability methods
- depth-model debugging/failure analysis
- VEO

The VEO contribution should be stated precisely:

> VEO combines region-level error localization with measurable RGB/depth evidence features, interpretable failure hypotheses, explicit ambiguity handling, threshold sensitivity analysis, and a blinded human-validation protocol. It is a ground-truth-assisted offline diagnostic framework, not a causal explanation system.

Every external method and claimed limitation must have a verified citation in the final paper.

#### Step 6: Assemble the final evidence package

Link the final paper/report to:

- protocol version
- configurations
- split manifests
- model/checkpoint IDs
- metrics tables
- region CSVs
- human-validation report
- ablation report
- representative visual panels
- code commit

**Member 2 acceptance criteria:**

- At least 200 regions are independently labeled by two raters, or the shortfall is explicitly documented.
- Agreement and classification metrics are generated from raw annotation files.
- Ablation results are included and correctly interpreted.
- Related work contains a citation-backed comparison table.
- Final claims distinguish implementation, empirical evidence, and future work.

## 7. Coordination and order of work

1. **Member 1 freezes the test configuration and generates the final evaluation package.**
2. **Member 2 uses those frozen test outputs to prepare the blinded rating package.**
3. Both members independently review the final tables and check that no test result was used to retune thresholds.
4. Member 1 supplies second-model and sensitivity results.
5. Member 2 merges human-validation and related-work results into the final report.
6. The team performs a final claim audit against [docs/RESEARCH_PROTOCOL_V1.md](RESEARCH_PROTOCOL_V1.md).

The tracks are mostly parallel after the frozen test package exists, but human validation must not begin from a changing classifier configuration.

## 8. Recommended final claim boundary

Until the open experiments are complete, the project may safely claim:

- VEO implements a reproducible region-level depth-error diagnosis pipeline.
- The pipeline computes standard depth metrics and connected high-error regions.
- The classifier records interpretable evidence scores and can return `ambiguous`.
- The system supports NYU scene-level evaluation and an official metric-Hypersim profile.
- Threshold and alignment sensitivity infrastructure is implemented.
- Human-rating preparation is implemented.

The project should not yet claim:

- completed KITTI evaluation;
- validated human agreement;
- proven causal failure causes;
- completed ZoeDepth/model comparison;
- dataset-level Hypersim performance from the one-sample artifact;
- publication-ready generalization across models and datasets.

## 9. Useful commands

From the repository root in PowerShell:

```powershell
uv run pytest -q
uv run veo-nyu prepare-nyu-splits --mat-path data/nyu/nyu_depth_v2_labeled.mat --output-dir data/nyu/splits
uv run veo-nyu evaluate-splits --config configs/nyu.yaml --split-root data/nyu/splits --output-dir outputs/nyu_evaluation --device cpu
uv run veo-nyu compare-alignment --config configs/nyu.yaml --split-root data/nyu/splits --output-dir outputs/alignment_ablation --device cpu
uv run veo-nyu prepare-rating --results-path outputs/nyu_evaluation/test/model_results.json --rgb-dir data/nyu/splits/test/rgb --depth-dir data/nyu/splits/test/depth --prediction-dir outputs/nyu_evaluation/test/predictions --output-dir outputs/rating_set --limit 200
```

The commands above should be run only after confirming the intended frozen configuration and available hardware. The generated `outputs/` directory is evidence, not a substitute for documenting the protocol and interpreting the results.

## 10. Final conclusion

The evaluator feedback is **partially addressed already**. The core VEO diagnostic implementation is substantially present and tested. The remaining work is primarily research validation and evidence completion rather than rebuilding the pipeline:

- finish and report the full quantitative benchmark;
- publish threshold sensitivity results;
- validate cause assignments with human labels;
- run a controlled second-model comparison;
- strengthen citation-backed related work and contribution claims;
- decide explicitly whether KITTI is added or documented as out of scope.

This distinction is important: the repository has implemented the mechanisms needed for the evaluator requests, but the project is not finished until the corresponding experiments and validation reports are completed.
