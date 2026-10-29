# Benchmark v1.2 Design Review — Resolution Report

**Repository:** `farmer-benefit-ml`  
**Review date:** 2026-10-28  
**Reviewer:** Methodological design review (read-only; no implementation changes)  
**Document under review:** `research/dataset_research/benchmark_v1.2_design_proposal.md`  
**Resolution document:** `reports/benchmark_v1.2_design_readiness_checklist.md`  
**Reference documents:** `reports/benchmark_v1.1_model_selection_decision.md`, `reports/benchmark_v1.1_feature_ablation.md`, `reports/benchmark_v1.1_ml_methodology_audit.md`, `research/dataset_research/evaluation_preregistration.md`, `src/eligibility/engine.py`

---

## Review Resolution Summary

| # | Issue | Original Status | Resolution Status | Resolution Location |
|---|-------|-----------------|-------------------|---------------------|
| 1 | Feature policy | REVISE | **RESOLVED** (documented; approval pending) | Readiness checklist Item 1; Design proposal Section 6 |
| 2 | Scenario construction | REVISE | **RESOLVED** (documented; approval pending) | Readiness checklist Item 2; Design proposal Section 3.2 |
| 3 | Scenario diversity | REVISE | **RESOLVED** (documented; approval pending) | Readiness checklist Item 3; Design proposal Section 3.3 |
| 4 | Ground-truth protocol | REVISE | **RESOLVED** (documented; approval pending) | Readiness checklist Item 4; Design proposal Section 4 |
| 5 | Evaluation design | REVISE | **RESOLVED** (documented; approval pending) | Readiness checklist Item 5; Design proposal Section 5; Separate preregistration |
| 6 | Data provenance | REVISE | **RESOLVED** (documented; approval pending) | Readiness checklist Item 6; Design proposal Sections 3.2/9 |

---

## Release Gate

**Verdict: NO-GO**

All 10 checklist items have been documented with proposed resolutions in `reports/benchmark_v1.2_design_readiness_checklist.md`. However, the release gate criteria require that "all mandatory design decisions have been resolved, their evidence is documented, **and required approval has actually been recorded**."

Two items require external research-team approval that has **not yet been recorded**:

1. **Item 4:** Single-annotator deviation authorization (if two independent reviewers cannot be secured)
2. **Item 5:** v1.2-specific acceptance criteria preregistration

**Blocker:** Research-team approval for v1.2 acceptance criteria and single-annotator deviation process is outstanding. No approval has been documented.

**Path to GO:** Obtain documented research-team approval for:
1. The v1.2 pre-registration document (`research/dataset_research/benchmark_v1.2_evaluation_preregistration.md`), including acceptance criteria
2. The single-annotator deviation process (if two independent reviewers cannot be secured)

Once both approvals are recorded, the design readiness checklist moves to GO and v1.2 scenario generation may proceed.

---

## Preservation Statement

All v1.1 artifacts preserved unchanged:
- `src/models/benchmark_v1_1/ranker.py` — ML model code
- `scripts/train_exploratory_ranker_v1_1.py` — v1.1.0 training script
- `scripts/ablate_ml_ranker_v1_1.py` — v1.1.1 ablation script
- `data/benchmarks/v1.1/ml_experiment/` — all v1.1.0 and v1.1.1 outputs
- `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` — annotation file
- `src/eligibility/engine.py` — frozen eligibility engine (unchanged)
- `research/dataset_research/evaluation_preregistration.md` — preregistered gates (unchanged)
- `reports/benchmark_v1.1_ml_experiment.md`, `reports/benchmark_v1.1_feature_ablation.md`, `reports/benchmark_v1.1_ml_methodology_audit.md`, `reports/benchmark_v1.1_annotation_readiness_audit.md`, `reports/benchmark_v1.1_model_selection_decision.md` — all preserved

No scenarios generated, no eligibility engine changes, no model retraining, no label alterations, no commits, no pushes.
