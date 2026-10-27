# Research Documentation & Protocols

This directory contains the foundational design specifications, evaluator audit responses, mathematical formulation notes, and frozen experimental protocols governing the Vision Error Observatory (VEO) project.

---

## Document Index

| Document | Description | Key Focus Area |
| :--- | :--- | :--- |
| **`RESEARCH_PROTOCOL_V1.md`** | Official frozen research protocol for NYU Depth V2 and Hypersim benchmarking. | Fixed scene-disjoint splits (seed 42), metric evaluation bounds ($[0.7\,\text{m}, 10.0\,\text{m}]$), frozen 7-class failure taxonomy, and zero test-set leakage discipline. |
| **`VEO_PROJECT_SPECIFICATION_LOCAL.md`** | Comprehensive software engineering architecture and local CLI execution manual. | Module interfaces (M1–M5), data loader pipelines, configuration schema, and reproducible pipeline contracts. |
| **`VEO_PROJECT_INFO_AND_EVALUATOR_RESPONSE.md`** | Point-by-point audit response addressing faculty reviewer & evaluator feedback. | Verification of publication gate criteria: alignment polarity proof, human agreement study, explanation faithfulness, and downstream refinement. |
| **`notes/MDE Mathematics Notes.pdf`** | Theoretical and mathematical notes on monocular depth estimation. | Inverse-depth scale-shift derivations, closed-form ordinary least squares (OLS) solution, and geometric loss formulations. |

