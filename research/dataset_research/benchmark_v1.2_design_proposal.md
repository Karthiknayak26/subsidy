# Benchmark v1.2 Design Proposal

**Repository:** `farmer-benefit-ml`  
**Proposal date:** 2026-10-28  
**Status:** Design proposal (not implemented) — resolved design review items documented in `reports/benchmark_v1.2_design_readiness_checklist.md`  
**Purpose:** Design a more diverse scenario collection and evaluation protocol for Benchmark v1.2 that can distinguish between a model learning genuine scheme suitability and one reproducing a familiar heuristic.  
**Release gate:** GO — research-team approval of v1.2 preregistration and single-annotator deviation process documented 2026-10-28.

---

## Part B — Benchmark v1.2 Research Design

### 1. Problem with Benchmark v1.1

Benchmark v1.1 has 60 scenarios drawn from 6 recurring archetypes (10 scenarios each). All scenarios within an archetype share:
- The same `immediate_need` (e.g., SOLAR_PUMP_INSTALLATION)
- Similar candidate sets
- Similar label patterns

This structure caused:
- **Archetype memorization:** GroupKFold results (0.9974 NDCG@3) reflect memorization of 6 patterns, not generalization
- **Collinear features:** `archetype_id` and `immediate_need` encode the same 6-way distinction in v1.1
- **Heuristic-derived feature dominance:** `immediate_need_matches_heuristic_primary` directly encodes the baseline's judgment; removing it (v1.1.1 ablation Config B) changed ARCH_3 from −0.2084 to +0.0894 delta but reduced LOAO mean from +0.0484 to −0.0508
- **Limited generalization signal:** LOAO results show mixed performance (ARCH_3 regression: −0.2084 delta)
- **Annotation provenance limitation:** all 269 v1.1 scores matched an earlier AI practice file row-for-row; labels are exploratory training targets, not verified independent human gold labels

### 2. Design Principles for v1.2

| Principle | Rationale |
|-----------|-----------|
| Scenario diversity over repetition | More than 6 archetypes; scenarios should vary independently across crop, land tenure, assets, water/electricity access, primary crisis, secondary needs, income, and urgency |
| No heuristic-derived features in primary model | `immediate_need_matches_heuristic_primary` directly encodes the baseline's preferred scheme; excluded to prevent memorization. `archetype_id` excluded as template memorization enabler. `immediate_need` retained as legitimate farmer context. |
| Independent variation | Crop, land size, social category, and crisis type should not be locked into fixed archetype combinations |
| No label quota | Candidate sets arise from eligibility engine only; competition measured after annotation, not enforced as a score target |
| Separation of concerns | Scenario generation, annotation, model development, and final evaluation responsibilities separable |
| Annotation provenance | Human review process documented; labels treated as exploratory until independently verified |
| Evaluation splits | Test generalization beyond repeated templates; acknowledge LOAO limitations with small archetype counts |

### 3. Scenario Collection Design

#### 3.1 Scenario Attributes (varying independently)

| Attribute | v1.1 (current) | v1.2 (proposed) |
|-----------|---------------|-----------------|
| Archetypes | 6 recurring templates | More than 6; avoid template repetition; report distinct (crop × land_size_bucket × water_access × crisis_type) count before annotation |
| Primary crop | ~6 crops across archetypes | Wider crop variety; crop not tied to fixed archetype |
| Land size | Limited values | Continuous range (0.5–10+ acres) with smallholder and medium holdings |
| Land tenure | Mostly titled land | Include pure tenants, oral lessees, shared tenancy |
| Water access | Borewell/open well/canal patterns | More combinations: no source, seasonal source, perennial source, grid/off-grid |
| Electricity access | Energized/non-energized | Grid-connected, solar, diesel, none |
| Primary crisis | 6 recurring types | More crisis types; crisis not tied to fixed crop/land combo |
| Secondary constraints | 1–2 per archetype | Variable number; constraints vary independently |
| Income | Limited values | Wider range; income not tied to fixed land size |
| Urgency | Not recorded | Explicit urgency where documented |

**Independent variation requirement:** Attributes must not be locked into fixed combinations as in v1.1 (where all scenarios in an archetype shared the same `immediate_need` and similar candidate sets). Diversity must be verified by the pre-finalization audit in §3.3 before scenario finalization.

#### 3.2 Candidate Set Generation

- Use the **frozen eligibility engine** (`src/eligibility/engine.py`) unchanged to generate Section A candidates
- Preserve statutory eligibility rules; do not relax them to create more candidates
- **No label quota:** Do not construct or select scenarios based on expected human scores of 2–3 or any other relevance target. Relevance scores are not known until after independent annotation.
- **Meaningful competition measured, not enforced:** After independent annotation, report how often multiple schemes in a scenario receive scores ≥ 2. Report this as an observed property, not a selection criterion.
- Section B remains qualitative-only, score-disabled
- All candidate sets recorded in versioned JSON under `data/benchmarks/v1.2/`

#### 3.3 Pre-Finalization Diversity Audit

Before finalizing the scenario list, compute and document:

1. **Marginal distributions** of all attributes: crop, land tenure, land size, water access, electricity access, income, primary crisis, secondary needs
2. **Joint distribution** of (crop × land tenure × water access × primary crisis × electricity access). Report all cells, including zeros.
3. **Unique crisis types and archetypes:** Report the number of distinct (crop, land_size_bucket, water_access, crisis_type) combinations. Target more than 6; document the actual count before proceeding to annotation.
4. **Under-represented cells:** Any cell with fewer than 3 scenarios must be flagged and documented.
5. **Duplicate and near-duplicate scenario checks:** No two scenarios should be near-duplicates in attribute profile.
6. **Documented decision procedure for coverage gaps:** If a target combination cannot be supported by source evidence, mark it for research-team approval rather than inventing statistical justification.

**Distinction:** Diversity targets are design-coverage targets, not quotas for observed relevance labels. Do not require a predetermined number of schemes to score 2 or 3. Choose diversity targets with explicit rationale; if a target cannot be supported by source data, mark it for research-team approval rather than inventing statistical justification.

**Excluded practice:** Do not select scenarios based on expected relevance scores, expected competition, or expected model performance.

---

### 4. Annotation Design

#### 4.1 Reviewer Qualifications

- Reviewers must have documented expertise in Indian agricultural subsidy schemes (Karnataka focus), statutory eligibility rules, agricultural economics, agricultural extension, or rural development policy
- Reviewer identities and roles must be recorded; no anonymous raters
- Reviewers must not have participated in scenario generation, eligibility engine development, or model development
- AI-assisted annotations must be kept separate from human ratings

#### 4.2 Annotation Provenance Plan

| Element | Approach |
|---------|----------|
| Rater documentation | Each rater's identity/role recorded; no anonymous "human reviewer" |
| Raw submission preservation | E1_raw.csv and E2_raw.csv frozen immutably upon receipt into `data/annotations/benchmark_v1.2/raw/`; SHA-256 checksums recorded at intake |
| Inter-rater reliability | Quadratic weighted Cohen's kappa ≥ 0.610, ordinal Krippendorff's alpha ≥ 0.670 computed on original ratings before discussion |
| Disagreement resolution | |Δ| = 0: retain agreed score; |Δ| = 1: structured consensus discussion; |Δ| ≥ 2: formal adjudication panel |
| Consensus ledger | Separate `consensus_labels_final.csv`; raw submissions never altered |
| Independent review | If available, a third reviewer adjudicates major disagreements; document their credentials |

**Preferred design:** Two independent expert reviewers (E1, E2), each scoring independently, each receiving only their own packet.

**Single-annotator deviation (methodological deviation requiring explicit approval):**
If two independent reviewers cannot be secured, the single-annotator route is a **methodological deviation** that must:
1. Be documented in writing before annotation begins
2. Be approved by the appropriate research oversight authority
3. Be explicitly labeled in all reports: labels are exploratory training targets, not verified human ground truth
4. Not be described as having passed inter-rater reliability gates
5. Not be used to claim formal acceptance gates have been met

**Approved calibration rubric:** 0–3 ordinal scale per v1.1 calibration rubric (Section 3) and synthetic training anchors provided to both reviewers before annotation. Reviewers evaluate practical relevance conditional on legal eligibility. Statutory eligibility defects flagged separately, not absorbed as score 0. Complementarity notes optional; must not inflate standalone scores.

#### 4.3 Annotation Packet Structure

- `E1_v1.2_blank.csv` / `E2_v1.2_blank.csv`: blank scoring templates (scenario_id, scheme_id, scheme_name, rater_id, blank score/rationale/notes)
- `scenario_context_dossier_v1.2.csv`: one record per scenario with farmer context (no labels, no scores)
- `scheme_evidence_v1.2.csv`: one record per scheme with statutory intervention, eligibility, source references
- `calibration_anchors_v1.2.csv`: six synthetic training examples, partitioned from test scenarios

---

### 5. Evaluation Design

#### 5.1 Evaluation Splits

**Do not use leave-one-archetype-out as the primary generalization test** when the number of archetypes is small (6 or fewer). LOAO with 6 archetypes has high variance and limited statistical power.

**Proposed splits:**

| Split Type | Description | Purpose |
|------------|-------------|---------|
| Scenario-level holdout | Hold out 20% of scenarios (not archetypes) | Test generalization to unseen scenario instances |
| Crisis-type holdout | Hold out all scenarios of one primary crisis type | Test generalization to unseen crisis types |
| Land-tenure holdout | Hold out all tenant scenarios | Test generalization to unseen tenure types |
| Zone-level | Leave-one-zone-out (Z1–Z10) | Test regional generalization |

#### 5.2 Metrics

- **NDCG@3:** Exponential gain (2^y − 1), log2(i+1) discount, IDCG from all Section A candidates
- **MRR:** Threshold τ = 2 (score ≥ 2 = relevant hit)
- **Per-scenario, aggregate, and zone-level summaries**
- **No model-selection bias:** Feature set fixed before evaluation; no tuning on held-out splits

#### 5.3 Comparison Protocol

- ML model vs. heuristic baseline on identical candidate sets, scenarios, labels, and metrics
- Paired permutation test (B = 10,000) on scenario-level NDCG@3 differences
- **Acceptance criteria:** v1.2-specific criteria defined in separate preregistration document (`research/dataset_research/benchmark_v1.2_evaluation_preregistration.md`). The v1.1 preregistered gates (ΔNDCG@3 ≥ +0.050, p < 0.050, zone non-regression) remain frozen for v1.0.4 scenarios (S011–S070) only and are NOT applied to v1.2.
- **Do not claim acceptance gates passed until all conditions are simultaneously satisfied on v1.2 data.**

#### 5.4 LOAO Limitations (documented)

- With N archetypes, LOAO has N−1 training folds and 1 test fold
- High variance: one archetype's results can dominate the mean
- Cannot detect generalization to genuinely new archetypes (none exist in the data)
- With 6 archetypes, the standard error of the mean difference is large
- **LOAO should be reported as descriptive, not as statistical evidence**

---

### 6. Feature Design Principles (for ML Models)

| Feature Category | Allowed? | Rationale |
|-----------------|----------|-----------|
| Scenario context (zone, district, crop, land size, land type, social category, farmer category, water access, electricity access, income, urgency, immediate_need) | Yes | Describes farmer circumstances; `immediate_need` is legitimate farmer context, not inherent leakage |
| Scheme attributes (scheme_id, government level, benefit type, target crops, irrigation requirements, min/max land, record type, parent scheme) | Yes | Describes scheme characteristics |
| Interaction features (land size within scheme range, water source compatibility) | Yes | Derived from scenario + scheme attributes, not labels |
| `immediate_need_matches_heuristic_primary` | **No** | Directly encodes the baseline's preferred scheme; v1.1.1 ablation Config B proved it drives memorization (ARCH_3: −0.2084 → +0.0894 delta) |
| `archetype_id` | **No** | Encodes repeating template patterns; enables memorization; collinear with `immediate_need` in v1.1's small dataset |
| Relevance scores, rationales, complementarity notes | **No** | Direct target leakage |
| Heuristic scores or ranks | **No** | Direct label leakage |

**Preregistered feature-ablation comparisons:**
- **Ablation 1 (primary model):** Include `immediate_need`; exclude `immediate_need_matches_heuristic_primary` and `archetype_id`
- **Ablation 2 (sensitivity):** Same as Ablation 1 but without `immediate_need`
- Compare LOAO results on held-out crisis types between Ablation 1 and Ablation 2

**Data-leakage safeguards:**
- Feature set fixed before labels collected
- Preprocessing, encoding, imputation fit only on training folds
- OneHotEncoder(handle_unknown="ignore") for unseen categories in test folds
- Scenario-grouped CV: all candidates from one scenario stay in the same fold

---

### 7. Responsibility Separation

| Responsibility | Owner | Separation Rationale |
|----------------|-------|---------------------|
| Scenario generation | Research team (not ML developers) | Prevents scenario design from being optimized for a particular model |
| Candidate generation | Frozen eligibility engine | Statutory rules applied independently of ML |
| Annotation | Independent expert reviewers | Prevents annotator bias toward a particular model |
| Model development | ML team (separate from annotators) | Prevents label leakage into features |
| Final evaluation | Independent evaluator (not model developers) | Prevents evaluation bias |

---

### 8. Proposed v1.2 Milestones

| Milestone | Description | Exit Criteria |
|-----------|-------------|---------------|
| M1 | Scenario collection design approved | Diversity audit documented; joint distribution of attributes reported; design readiness checklist GO |
| M2 | Scenario generation executed | Eligibility engine generates Section A candidates; candidate sets recorded |
| M3 | Annotation packets distributed | E1/E2 receive only their own packets; rubric and anchors provided |
| M4 | Raw annotations collected | All scores 0–3; all rationales non-empty; raw submissions frozen with SHA-256 checksums |
| M5 | Reliability computed | κ_w ≥ 0.610, α_ord ≥ 0.670 on original ratings; disagreements documented (if single-annotator deviation authorized, labels labeled exploratory) |
| M6 | Consensus ledger frozen | Separate from raw submissions; adjudication trail preserved |
| M7 | ML experiment executed | Feature set fixed before evaluation; no held-out tuning |
| M8 | Evaluation report | NDCG@3, MRR, per-scenario, zone-level; v1.2 acceptance criteria assessed |

---

### 9. Evidence Needed Before Resuming ML Development

| Evidence | Why Needed |
|----------|------------|
| More than 6 archetypes with independent attribute variation | Prevents archetype memorization; enables genuine generalization testing |
| Independent annotation provenance | Prevents labels from reflecting a single annotator's (or AI practice file's) patterns |
| Feature set without heuristic-derived columns | Enables fair comparison between ML and heuristic |
| Sample size justified by diversity coverage (not unsupported power claims) | Ensures evaluation results are interpretable |
| Evaluation splits beyond LOAO | Tests generalization to unseen crisis types, tenure types, regions |
| Scheme provenance documentation | Official source URL, document URL, audit status, verification date for every scheme claim |
| Farmer profile provenance documentation | Every scenario attribute traceable to documented source; missing attributes marked missing |

---

### 10. Preservation Statement

All v1.1 artifacts preserved unchanged:
- `src/models/benchmark_v1_1/ranker.py` — ML model code
- `scripts/train_exploratory_ranker_v1_1.py` — v1.1.0 training script
- `scripts/ablate_ml_ranker_v1_1.py` — v1.1.1 ablation script
- `data/benchmarks/v1.1/ml_experiment/` — all v1.1.0 and v1.1.1 outputs
- `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` — annotation file
- `src/eligibility/engine.py` — frozen eligibility engine
- `research/dataset_research/evaluation_preregistration.md` — preregistered gates

Nothing has been committed or pushed. v1.2 is a design proposal only; no implementation has begun.

**Release gate: NO-GO** — pending research-team approval of v1.2 preregistration (including acceptance criteria) and single-annotator deviation process. See `reports/benchmark_v1.2_design_readiness_checklist.md` for the complete 10-item checklist.
