# Benchmark v1.1 — Single-Annotator Submission QC Report

**Input file:** `human_reviewer_annotations.csv`  
**Audit date:** 2026-10-28  
**Purpose:** Structural and traceability checks before downstream evaluation. This report does not certify authorship or methodological approval.

## 1. Structural validation

| Check | Result |
|---|---|
| Data rows | 269 |
| Unique scenario–scheme pairs | 269 |
| Duplicate scenario–scheme pairs | 0 |
| Distinct scenarios | 60 (S071–S130) |
| Scenario IDs within the expected range | all IDs in S071–S130 |
| Scores restricted to integer values 0–3 | True |
| Blank relevance rationales | 0 |
| Rater ID values | `human reviewer` on all 269 rows |

**Structural verdict: PASS** for the checks above.

## 2. Score distribution

| Score | Rows | Share |
|---:|---:|---:|
| 0 | 52 | 19.3% |
| 1 | 107 | 39.8% |
| 2 | 83 | 30.9% |
| 3 | 27 | 10.0% |

## 3. Comparison to the previously supplied AI practice file

A row-key join on `(scenario_id, scheme_id)` was performed against `AI_PRACTICE_v1.1_completed_NOT_HUMAN.csv`.

| Comparison | Result |
|---|---:|
| Candidate-pair sets match | True |
| Identical scores | 269 of 269 |
| Exactly identical rationales | 100 of 269 |
| Rationale pairs with text similarity >= 0.90 | 171 of 269 |
| Mean rationale text similarity | 91.3% |
| Exactly identical complementarity notes | 178 of 269 |

**Interpretation:** All submitted scores match the scores in the AI practice file. Many rationales and complementarity notes also match exactly or closely. This file comparison cannot establish who personally made each judgment, but it is a material provenance/independence signal that must be disclosed in the research record. The file should not be used to claim *independent human* labels or inter-rater reliability solely on the basis of its `rater_id` field. The user's account is that they performed the review themselves; authorship cannot be independently determined from these CSVs alone.

## 4. What can and cannot be concluded

- **Can conclude:** the file is structurally complete for a 269-pair, single-annotator dataset under the checks above.
- **Cannot conclude:** that the annotations are independent of the AI practice file; that two independent human reviewers agree; or that the preregistered kappa/alpha gates have passed.
- With one annotator, quadratic weighted Cohen's kappa and ordinal Krippendorff's alpha for *inter-rater* agreement between two human reviewers cannot be calculated.

## 5. Recommended next step

Treat this as a **single-annotator dataset with a documented provenance caveat**. Before computing ranking metrics, reconcile the file's provenance with the research protocol and obtain any required supervisor approval for the single-annotator deviation. Keep the AI practice file separate. Do not alter historical files or describe single-annotator evaluation as having passed the two-reviewer reliability gates.

## 6. File identity (SHA-256)

- `human_reviewer_annotations.csv`: `38e237fec447e8b760bc59631ab12a4646c87c495c4bff4a63c55ffa280468a1`
- `AI_PRACTICE_v1.1_completed_NOT_HUMAN.csv`: `7c046ce053fde12f06c6344941856fcb4510ee32ca7f3ccb585da6dbab15f93c`
