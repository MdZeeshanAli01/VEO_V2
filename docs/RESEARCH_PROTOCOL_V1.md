# VEO Research Protocol v1

**Status:** Frozen before full-scale evaluation  
**Scope:** Ground-truth-assisted, post-hoc diagnosis of monocular depth-estimation errors

## 1. Central Claim

VEO is a model-agnostic framework that localizes high-error depth regions and generates interpretable hypotheses about visual and geometric conditions associated with those errors.

VEO does not claim to recover the model's internal reasoning or prove causal failure mechanisms without controlled interventions.

## 2. Research Questions

- **RQ1:** Does region-level error localization reveal failure structure hidden by global depth metrics?
- **RQ2:** Do measurable visual and geometric signals predict human-assigned failure hypotheses?
- **RQ3:** Are VEO explanations faithful under controlled image interventions?
- **RQ4:** Do failure patterns transfer across depth models and indoor datasets?
- **RQ5:** Can VEO diagnosis guide targeted data or augmentation changes that improve regional performance?

## 3. Claim Boundaries

### Allowed claims

- error-associated evidence
- failure hypothesis
- region-level diagnostic category
- ground-truth-assisted offline analysis
- post-hoc explanation

### Disallowed without additional experiments

- true cause of failure
- causal explanation
- explanation of internal model parameters
- deployment-time RGB-only diagnosis
- generalization from a single dataset or ten-image sample

## 4. Failure Taxonomy

The frozen categories are:

1. `textureless`: low local visual texture or weak discriminative appearance
2. `boundary_mixing`: error concentrated near visible object boundaries
3. `occlusion`: error associated with a depth discontinuity at a region boundary
4. `thin_object`: elongated structure with insufficient visual support
5. `poor_lighting`: extreme illumination combined with low local contrast
6. `reflection`: specular/highlight evidence associated with error
7. `ambiguous`: insufficient evidence or competing hypotheses

`ambiguous` is a valid result, not a discarded sample.

A region may have multiple evidence scores, but the primary label is selected only after applying the frozen ambiguity rule.

## 5. Dataset Roles

- **NYU Depth V2:** primary real indoor evaluation dataset. It is not treated as training data for the relative Depth Anything V2 checkpoint.
- **Hypersim:** training-aligned synthetic indoor dataset for evaluating the official metric-Hypersim checkpoint and studying synthetic-to-real transfer.
- **Additional dataset:** required for a cross-domain claim; otherwise claims remain limited to indoor NYU evaluation.

Raw data is never committed to Git.

## 6. Data Splits

Splits must be scene-level, never random frame-level splits.

- **Development:** feature implementation and debugging only.
- **Validation:** threshold calibration and classifier selection.
- **Test:** frozen final evaluation, used once for headline results.

No threshold, category rule, or model-selection decision may use test labels or test results.

## 7. Model Protocol

Every model report must record:

- model and checkpoint identifier
- relative or metric depth output type
- preprocessing and input size
- device and software versions
- maximum evaluation depth
- validity mask policy
- alignment policy

Relative-depth models use scale-shift alignment for metric evaluation. Metric-depth models are evaluated without fitted alignment unless a separate ablation explicitly studies alignment.

## 8. Error Localization Protocol

The primary baseline uses valid-pixel relative error and the 85th percentile per image, followed by connected components and a minimum area of 25 pixels.

Sensitivity analysis must report 75th, 85th, 90th, and 95th percentiles. Failure-region conclusions are conditional on this selection process and must not be presented as unbiased whole-image feature correlations.

## 9. Classifier Protocol

Rules are calibrated only on development/validation data. The final test classifier is frozen before test evaluation.

The classifier reports:

- all evidence scores
- primary hypothesis
- score margin
- confidence
- ambiguity status

Hand-tuned parameters are baseline parameters until validated against independent human labels.

## 10. Required Validation

Before publication claims:

- at least two independent human raters
- at least 200 blinded regions
- human-human agreement
- VEO-human agreement
- per-category precision, recall, and macro-F1
- confusion matrix
- threshold sensitivity
- signal ablation
- scene-level confidence intervals
- controlled interventions for faithfulness

Cohen's kappa is not reported as evidence of validation until human labels exist.

## 11. Reproducibility Requirements

Each experiment must save:

- protocol version
- dataset split or manifest
- model checkpoint identifier
- configuration
- package lockfile
- random seed
- predictions
- metrics
- region records
- classifier scores
- code commit

## 12. Publication Gate

The project is not publication-ready for a top-tier venue until it demonstrates:

1. held-out scene-level evaluation;
2. multiple-model comparison;
3. human validation;
4. explanation-faithfulness interventions; and
5. at least one diagnosis-guided improvement experiment.
