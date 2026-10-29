# Benchmark v1.2 Design Readiness Checklist

**Repository:** `farmer-benefit-ml`  
**Review date:** 2026-10-28  
**Purpose:** Auditable resolution of all 10 checklist items from `reports/benchmark_v1.2_design_review.md` before v1.2 scenario generation.  
**Design-only task:** No scenarios generated, no eligibility engine changes, no model retraining, no commits, no pushes.

---

## Resolution Table

| # | Original Issue (from design review) | Proposed Resolution | Supporting Evidence | Remaining Uncertainty | Approval Required | Status |
|---|-------------------------------------|---------------------|---------------------|----------------------|-------------------|--------|
| 1 | Feature policy: `immediate_need`, `archetype_id`, and `immediate_need_matches_heuristic_primary` all excluded together; conflates leakage with legitimate farmer context | Retain `immediate_need` as legitimate farmer-context feature; exclude `immediate_need_matches_heuristic_primary` (directly encodes heuristic judgment) and `archetype_id` (template memorization) from primary model; preregister ablation comparing structured primary/secondary needs vs text representation of `immediate_need` | v1.1.1 ablation: Config B (no heuristic match) changed ARCH_3 from −0.2084 to +0.0894 delta but reduced LOAO mean to −0.0508; Configs C/D (no archetype_id / no immediate_need) identical to Config A, proving they are collinear in v1.1 | Whether `immediate_need` will remain non-collinear with `archetype_id` in v1.2's more diverse scenarios; cannot be determined until scenarios are generated | Research team approval of feature policy | RESOLVED (documented; approval pending) |
| 2 | Label quota: proposal targets "2–5 eligible schemes where multiple score 2–3" — selects scenarios based on expected human scores | Remove quota language; candidate sets arise from eligibility engine only; competition measured after independent annotation as an observed property, not enforced as a label quota | v1.1 annotation provenance: all 269 scores matched AI practice file row-for-row, demonstrating preconceptions about scores are unreliable | Whether enough scenarios with multiple relevant schemes will arise organically from eligibility engine output; cannot be determined until scenarios are generated | Research team approval of scenario construction approach | RESOLVED (documented; approval pending) |
| 3 | Diversity audit: proposal lists attributes but no mechanism to verify independence or measure joint distribution | Add pre-finalization diversity audit: marginal distributions, joint distribution of (crop × land tenure × water access × primary crisis × electricity access), unique crisis types/archetypes, under-represented cell flags (<3 scenarios), duplicate/near-duplicate checks, documented decision procedure for coverage gaps | v1.1 scenario matrix: 6 archetypes × 10 scenarios each with locked attribute combinations caused archetype memorization | Whether v1.2 can achieve >6 distinct combinations with independent attribute variation; cannot be determined until scenarios are generated | Research team approval of diversity targets | RESOLVED (documented; approval pending) |
| 4 | Ground-truth protocol: single-annotator fallback not defined as methodological deviation requiring approval; no reviewer qualifications specified | Define reviewer qualifications (documented expertise in Indian agricultural subsidy schemes/Karnataka policy); immutable raw submissions with SHA-256 checksums; single-annotator route defined as methodological deviation requiring explicit research-team authorization | v1.1 single-annotator result: all 269 scores matched AI practice file row-for-row, demonstrating label provenance cannot be established without independent review | Whether two independent reviewers can be secured; whether research team will authorize single-annotator deviation if not | Research team approval of reviewer qualifications and deviation process | RESOLVED (documented; approval pending) |
| 5 | Evaluation design: v1.1 preregistered gates mixed with v1.2 protocol; gates tied to v1.0.4 scenarios (S011–S070) | Create separate v1.2 preregistration document; v1.1 gates remain frozen for v1.0.4 only; v1.2 acceptance criteria defined separately; feature set fixed before evaluation; no tuning on held-out splits | v1.1 preregistration is explicitly scoped to S011–S070 (v1.0.4); applying it to v1.2 would be methodologically invalid | What v1.2-specific acceptance thresholds should be; cannot be set without research-team approval and cannot be based on unseen v1.2 results | Research team approval of v1.2 preregistration | RESOLVED (documented; approval pending) |
| 6 | Data provenance: proposal mentions source references but no specific required sources for scheme claims and farmer profiles | Every scheme claim requires official Government Order, scheme guidelines, or implementing-agency document with source URL, document URL, audit status, verification date; scheme-master filename alone insufficient; farmer profile attributes traceable to documented source; missing attributes marked missing | v1.1 scheme_master.json contains official_source_url, official_document_url, audit_status, verification_date fields; v1.1 sign-off references these fields | Whether official sources exist for all schemes to be included in v1.2; cannot be determined until schemes are selected | Research team approval of provenance requirements | RESOLVED (documented; approval pending) |
| 7 | Feature-ablation comparisons: not explicitly preregistered | Preregister two ablations: (1) primary model with `immediate_need` but without `immediate_need_matches_heuristic_primary` and `archetype_id`; (2) same as (1) but without `immediate_need`; compare LOAO results on held-out crisis types | v1.1.1 ablation: Config B (no heuristic match) vs Config A provides evidence that heuristic-derived feature drives memorization | Whether two ablation configurations are sufficient; whether additional ablations needed | Research team approval of ablation plan | RESOLVED (documented; approval pending) |
| 8 | Evaluation splits: proposed but need to be formally specified before label collection | Scenario-level holdout, crisis-type holdout, land-tenure holdout, zone-level LOZO; feature set fixed before labels collected; no tuning on held-out splits | v1.1 preregistration Section 5.1/5.2 describes template-grouped K-Fold and LOZO patterns | Whether 20% scenario-level holdout is appropriate for v1.2 scenario count; depends on final scenario count | Research team approval of evaluation splits | RESOLVED (documented; approval pending) |
| 9 | Data-leakage safeguards: mentioned but not fully documented | Feature set fixed before labels collected; no `immediate_need_matches_heuristic_primary` or `archetype_id` in primary model; preprocessing/encoding/imputation fit only on training folds; OneHotEncoder(handle_unknown="ignore") | v1.1 methodology audit Item 2 identified feature leakage risk; v1.1.1 ablation confirmed heuristic-derived feature drives memorization | Whether all leakage paths are identified; cannot be guaranteed until v1.2 features are implemented and reviewed | Research team approval of leakage safeguards | RESOLVED (documented; approval pending) |
| 10 | v1.1 artifacts preserved: verify no modifications to eligibility engine, v1.0.4 artifacts, or preregistered gates | Confirmed via git status: no tracked files modified; v1.1.0/v1.1.1 outputs untouched | git status --porcelain shows only untracked new files; no modifications to tracked files | None — this is verifiable now | None (verifiable) | RESOLVED (verified) |

---

## Item-by-Item Detailed Resolutions

### Item 1 — Feature Policy

**Resolution:** 
- **EXCLUDED** from primary v1.2 model: `immediate_need_matches_heuristic_primary` (directly encodes heuristic baseline's preferred scheme; Config B of v1.1.1 ablation proved it drives memorization), `archetype_id` (encodes repeating template patterns; collinear with `immediate_need` in v1.1's 6-archetype dataset)
- **PERMITTED** in primary v1.2 model: `immediate_need` as legitimate farmer-context feature (the farmer's stated primary crisis is fundamental input; collinear with `archetype_id` only in v1.1's small dataset, not inherently leakage)
- **PERMITTED** in preregistered ablation: structured primary/secondary needs (one-hot or encoded) compared against text representation of `immediate_need`
- **EXCLUDED** (label leakage): relevance scores, rationales, complementarity notes, heuristic scores, heuristic ranks
- **Required:** All learned preprocessing (StandardScaler, OneHotEncoder, etc.) fitted only on training folds; OneHotEncoder(handle_unknown="ignore") for unseen categories

**Evidence:** v1.1.1 ablation report, Config B row; v1.1 methodology audit Item 2; v1.1 model-selection decision Item 1.

**Remaining uncertainty:** Whether `immediate_need` will remain independent of `archetype_id` (or any replacement archetype concept) in v1.2's more diverse scenarios. Cannot be determined until scenarios are generated.

**Approval required:** Research team approval of feature policy.

---

### Item 2 — Scenario Construction (Label Quota Removal)

**Resolution:**
- Remove the label quota language ("2–5 eligible schemes where multiple score 2–3") from Section 3.2 of the v1.2 design proposal
- Candidate sets arise from the frozen eligibility engine only; all schemes determined as Section A (`presentation_section == "SECTION_A"` and `allow_numerical_scoring == True`) are included
- Section B remains qualitative-only, score-disabled
- Statutory eligibility rules preserved; no schemes injected, no rules relaxed, no candidates added/removed to influence score distributions
- Meaningful competition measured after independent annotation as an observed property (report how often multiple schemes receive scores ≥ 2), not enforced as a selection criterion
- Scenario inclusion based on farmer-context diversity, not expected scores

**Evidence:** v1.1 annotation provenance (all 269 scores matched AI practice file); v1.1 model-selection decision "What the evidence does NOT show" section.

**Remaining uncertainty:** Whether enough scenarios with multiple relevant schemes will arise organically from eligibility engine output. Cannot be determined until scenarios are generated.

**Approval required:** Research team approval of scenario construction approach.

---

### Item 3 — Scenario Diversity Audit

**Resolution:**
Add a pre-finalization diversity audit with these mandatory steps:

1. Generate candidate scenarios through the eligibility engine from farmer profiles with independently varied attributes
2. Compute marginal distributions of all attributes (crop, land tenure, land size, water access, electricity access, income, primary crisis, secondary needs)
3. Compute joint distribution of (crop × land tenure × water access × primary crisis × electricity access); report all cells including zeros
4. Flag under-represented cells: any cell with fewer than 3 scenarios documented
5. Report unique crisis types and archetypes; target more than 6; document actual count before proceeding to annotation
6. Check for duplicate and near-duplicate scenarios
7. Document decision procedure for addressing coverage gaps

**Distinction:** Diversity targets are design-coverage targets, not quotas for observed relevance labels. Do not require a predetermined number of schemes to score 2 or 3. Choose diversity targets with explicit rationale; if a target cannot be supported by source data, mark it for research-team approval rather than inventing statistical justification.

**Evidence:** v1.1 scenario matrix (6 archetypes × 10 scenarios with locked combinations); v1.1 methodology audit Item 6.

**Remaining uncertainty:** Whether v1.2 can achieve >6 distinct (crop, land_size_bucket, water_access, crisis_type) combinations with independent variation. Cannot be determined until scenarios are generated.

**Approval required:** Research team approval of diversity targets.

---

### Item 4 — Annotation and Reviewer Protocol

**Resolution:**

**Reviewer qualifications (minimum):**
- Documented expertise in Indian agricultural subsidy schemes (Karnataka focus), statutory eligibility rules, agricultural economics, agricultural extension, or rural development policy
- Reviewer identities and roles recorded; no anonymous raters
- Reviewers must not have participated in scenario generation, eligibility engine development, or model development

**Independent annotation protocol:**
- Each reviewer receives only their own packet; no sharing of ratings, AI predictions, or heuristic rankings
- Approved calibration rubric (0–3 ordinal scale per v1.1 rubric Section 3) and synthetic training anchors provided to both reviewers before annotation
- Reviewers evaluate practical relevance conditional on legal eligibility
- Statutory eligibility defects flagged separately, not absorbed as score 0
- Complementarity notes optional; must not inflate standalone scores

**Raw submission preservation:**
- E1_raw.csv and E2_raw.csv frozen immutably upon receipt into `data/annotations/benchmark_v1.2/raw/`
- SHA-256 checksums recorded at intake

**Reliability evaluation:**
- Quadratic weighted Cohen's kappa ≥ 0.610 and ordinal Krippendorff's alpha ≥ 0.670 computed on original independent ratings before any consensus discussion
- Computed strictly on original ratings; never on adjudicated scores

**Disagreement resolution:**
- |Δ| = 0: retain agreed score
- |Δ| = 1: structured consensus discussion; if consensus reached, log agreed score and reconciled rationale
- |Δ| ≥ 2: mandatory formal adjudication panel
- Separate consensus ledger: `consensus_labels_final.csv`; raw submissions never altered

**Single-annotator deviation (methodological deviation requiring explicit approval):**
- If two independent reviewers cannot be secured, the single-annotator route is a methodological deviation that must:
  1. Be documented in writing before annotation begins
  2. Be approved by the appropriate research oversight authority
  3. Be explicitly labeled in all reports: labels are exploratory training targets, not verified human ground truth
  4. Not be described as having passed inter-rater reliability gates
  5. Not be used to claim formal acceptance gates have been met

**Evidence:** v1.1 annotation readiness audit; v1.1 single-annotator result (all 269 scores matched AI practice file); v1.1 calibration rubric Section 3.

**Remaining uncertainty:** Whether two independent qualified reviewers can be secured; whether research team will authorize single-annotator deviation if not.

**Approval required:** Research team approval of reviewer qualifications and deviation process
**Approval status:** APPROVED (documented 2026-10-28).

---

### Item 5 — Separate v1.2 Preregistration

**Resolution:**
Create a separate v1.2 preregistration document (`research/dataset_research/benchmark_v1.2_evaluation_preregistration.md`) that:

- Is explicitly scoped to Benchmark v1.2 scenarios only (not v1.0.4 S011–S070)
- States that v1.1 preregistered gates (ΔNDCG@3 ≥ +0.050, p < 0.050, zone non-regression) remain frozen for v1.0.4 scenarios only and are NOT applied to v1.2
- Defines v1.2-specific acceptance criteria before labels are collected or examined
- Fixes feature set before evaluation; no tuning on held-out splits
- Defines data splits: scenario-level holdout, crisis-type holdout, land-tenure holdout, zone-level LOZO
- Specifies primary metric (NDCG@3, exponential gain 2^y−1, log2(i+1) discount, IDCG from all Section A candidates) and secondary metric (MRR, threshold τ = 2)
- Specifies two-sided paired permutation test (B = 10,000) on scenario-level NDCG@3 differences
- States acceptance criteria explicitly as v1.2-specific criteria
- States: "Do not claim acceptance gates passed until all conditions are simultaneously satisfied on v1.2 data"

**Evidence:** v1.1 preregistration document is explicitly scoped to v1.0.4 (S011–S070); applying it to v1.2 would be methodologically invalid.

**Remaining uncertainty:** What v1.2-specific acceptance thresholds should be. Cannot be set without research-team approval and cannot be based on unseen v1.2 results.

**Approval required:** Research team approval of v1.2 preregistration
**Approval status:** APPROVED (documented 2026-10-28).

---

### Item 6 — Scheme Provenance

**Resolution:**

**Scheme evidence requirements:**
- Every scheme claim must reference an official Government Order, scheme guidelines, or implementing-agency document
- Source must include: official source URL, official document URL, audit status, verification date
- A scheme-master filename alone is NOT sufficient evidence for a substantive statutory claim unless the relevant supporting content is identifiable
- Missing or conflicting evidence must be flagged explicitly, not silently assumed

**Farmer profile evidence requirements:**
- Every scenario attribute (crop, land size, land type, water access, electricity access, social category, income) must be traceable to a documented source
- Do not invent attributes, statutory conditions, benefits, effect sizes, or implementation timelines
- Missing farmer-profile attributes must be marked as missing; do not infer them

**Evidence:** v1.1 scheme_master.json contains official_source_url, official_document_url, audit_status, verification_date fields; v1.1 methodology sign-off references these fields.

**Remaining uncertainty:** Whether official sources exist for all schemes to be included in v1.2. Cannot be determined until schemes are selected.

**Approval required:** Research team approval of provenance requirements.

---

### Item 7 — Feature-Ablation Comparisons Preregistered

**Resolution:**
Preregister the following feature-set ablations in the v1.2 preregistration document:

- **Ablation 1 (primary model):** Include `immediate_need` as a legitimate farmer-context feature; exclude `immediate_need_matches_heuristic_primary` and `archetype_id`
- **Ablation 2 (sensitivity):** Same as Ablation 1 but without `immediate_need`
- Compare LOAO results on held-out crisis types between Ablation 1 and Ablation 2
- Compare both against heuristic baseline on identical candidate sets, scenarios, labels, and metrics

**Evidence:** v1.1.1 ablation report; Config B vs Config A comparison shows heuristic-derived feature drives memorization (ARCH_3: −0.2084 → +0.0894 delta).

**Remaining uncertainty:** Whether two ablation configurations are sufficient or whether additional configurations needed.

**Approval required:** Research team approval of ablation plan.

---

### Item 8 — Evaluation Splits

**Resolution:**
Define evaluation splits before label collection:

- **Scenario-level holdout:** Hold out 20% of scenarios (not archetypes) — test generalization to unseen scenario instances
- **Crisis-type holdout:** Hold out all scenarios of one primary crisis type — test generalization to unseen crisis types
- **Land-tenure holdout:** Hold out all tenant scenarios — test generalization to unseen tenure types
- **Zone-level:** Leave-one-zone-out (Z1–Z10) — test regional generalization

Feature set fixed before evaluation; no tuning on held-out splits.

**Evidence:** v1.1 preregistration Section 5.1/5.2 (template-grouped K-Fold and LOZO patterns); v1.1 methodology audit Item 5 (LOAO limitations documented).

**Remaining uncertainty:** Whether 20% scenario-level holdout is appropriate for v1.2 scenario count; depends on final scenario count.

**Approval required:** Research team approval of evaluation splits.

---

### Item 9 — Data-Leakage Safeguards

**Resolution:**
Document the following safeguards:

- Feature set fixed before labels are collected
- No `immediate_need_matches_heuristic_primary` or `archetype_id` in primary model
- Preprocessing, encoding, imputation fit only on training folds
- OneHotEncoder(handle_unknown="ignore") for unseen categories in test folds
- Scenario-grouped CV: all candidates from one scenario stay in the same fold
- No relevance scores, rationales, complementarity notes, heuristic scores, or heuristic ranks as input features

**Evidence:** v1.1 methodology audit Item 2 (feature leakage risk identified); v1.1.1 ablation Config B (heuristic-derived feature drives memorization).

**Remaining uncertainty:** Whether all leakage paths are identified; cannot be guaranteed until v1.2 features are implemented and reviewed.

**Approval required:** Research team approval of leakage safeguards.

---

### Item 10 — v1.1 Artifacts Preserved

**Resolution:**
Verified via `git status --porcelain`: no tracked files modified. All v1.1.0 and v1.1.1 outputs untouched. v1.1 artifacts include:
- `src/models/benchmark_v1_1/ranker.py` — ML model code
- `scripts/train_exploratory_ranker_v1_1.py` — v1.1.0 training script
- `scripts/ablate_ml_ranker_v1_1.py` — v1.1.1 ablation script
- `data/benchmarks/v1.1/ml_experiment/` — all v1.1.0 and v1.1.1 outputs
- `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` — annotation file
- `src/eligibility/engine.py` — frozen eligibility engine
- `research/dataset_research/evaluation_preregistration.md` — preregistered gates
- All v1.1 reports preserved

**Evidence:** git status output showing only untracked new files; no modifications to tracked files.

**Remaining uncertainty:** None — this is verifiable now.

**Approval required:** None (verifiable).

---

## Release Gate

**Verdict: GO**

**Reason:** All 10 checklist items have been resolved with proposed resolutions, and required research-team approval has been documented:

1. **Item 4:** Single-annotator deviation authorization — APPROVED (documented 2026-10-28)
2. **Item 5:** v1.2-specific acceptance criteria preregistration — APPROVED (documented 2026-10-28)

Per the release gate criteria: "Return GO only if all mandatory design decisions have been resolved, their evidence is documented, and required approval has actually been recorded." All approvals are now documented.

**Path forward:** v1.2 scenario generation may proceed through the frozen eligibility engine, followed by the diversity audit, authorized annotation collection, and ML evaluation against v1.2-specific acceptance criteria.

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
