# Benchmark v1.2 ML Ranking Evaluation Report

**Benchmark Version:** `v1.2` (S131–S220, N=90 scenarios)  
**Experiment Version:** `v1.2.0`  
**Model:** BenchmarkV12Ranker (HistGradientBoostingRegressor pipeline)  
**Baseline:** Heuristic baseline (need-to-scheme mapping, v1.2 adaptation)  
**Preregistration:** `research/dataset_research/benchmark_v1.2_evaluation_preregistration.md` (approved 2026-10-28)  
**Generated:** 2026-10-29T05:30:52Z

---

## ⚠️ Important Limitations

### Single-Annotator Labels
Labels sourced from `data/annotations/benchmark_v1.2/E2_v1.2_blank.csv` (rater: `human reviewer 2`).  
**No independent inter-rater reliability (IRR) has been computed or is available** — neither Cohen's kappa nor Krippendorff's alpha. This is a preregistered methodological deviation (single-annotator authorization documented 2026-10-28 in `reports/benchmark_v1.2_design_readiness_checklist.md`).  
Labels are treated as exploratory training targets only. Performance on these labels does **not** constitute evidence of generalizable real-world recommendation quality.

### Acceptance-Criteria Gap
The approved v1.2 preregistration **does not specify numeric thresholds** for:
- Gate 1: δ_min (minimum substantive NDCG@3 gain)
- Gate 2: α (significance threshold)

Per the preregistration: _"No numeric thresholds are set in this preregistration. The research team must define δ_min and α before v1.2 label collection."_  
**Formal PASS/FAIL for Gates 1 and 2 is therefore not possible.** Observed values are reported. Only Gate 3 (zone-level non-regression) can be evaluated without numeric thresholds.

### Small Dataset
90 scenarios, 369 candidate pairs, 8 unique Section A schemes. This is insufficient for robust generalization estimates.

---

## 1. Data Validation

| Check | Result |
|---|---|
| Annotation file SHA-256 | `8ab03fba5f4cd4a1c9783a2bac3864f3d8530ed15e112ddd3f3a05f90fdf3d26` ✅ |
| Annotation rows | 369 ✅ |
| Scenarios covered | 90 (S131–S220) ✅ |
| Annotated pairs match Section A candidate sets | All 369 pairs verified ✅ |
| Relevance scores in {0,1,2,3} | All valid ✅ |
| Rater | `human reviewer 2` (single annotator) |
| Independent IRR | Not available |
| Score distribution | `0`: 61  `1`: 157  `2`: 116  `3`: 35 |

---

## 2. Feature Policy & Preregistered Need Representation Comparison

### Ablation 1 — Primary Model: Structured Features (29 features)
Includes `immediate_need` as categorical One-Hot feature (along with `primary_crisis`):
  - `land_size_acres`
  - `annual_family_income_lakh`
  - `secondary_constraint_count`
  - `zone_id`
  - `district`
  - `crop_primary`
  - `crop_secondary`
  - `land_type`
  - `social_category`
  - `farmer_category`
  - `operational_water_source`
  - `borewell_electric_status`
  - `immediate_need`
  - `primary_crisis`
  - `is_pure_tenant_without_land_title`
  - `land_ownership_cutoff_pre_feb_2019`
  - `paid_income_tax_last_assessment_year`
  - `pensioner_is_mts_exempt`
  - `registered_professional_is_none`
  - `min_land_acres`
  - `max_land_acres`
  - `government_level`
  - `benefit_type`
  - `target_crops`
  - `irrigation_requirements`
  - `record_type`
  - `parent_scheme_id`
  - `land_size_within_scheme_range`
  - `water_source_compatible`

**Excluded (preregistration):**
- `immediate_need_matches_heuristic_primary` — heuristic-derived leakage
- `archetype_id` — template-memorisation risk

### Ablation 2 — Sensitivity: No Immediate Need (28 features)
Excludes `immediate_need`:
  - `land_size_acres`
  - `annual_family_income_lakh`
  - `secondary_constraint_count`
  - `zone_id`
  - `district`
  - `crop_primary`
  - `crop_secondary`
  - `land_type`
  - `social_category`
  - `farmer_category`
  - `operational_water_source`
  - `borewell_electric_status`
  - `primary_crisis`
  - `is_pure_tenant_without_land_title`
  - `land_ownership_cutoff_pre_feb_2019`
  - `paid_income_tax_last_assessment_year`
  - `pensioner_is_mts_exempt`
  - `registered_professional_is_none`
  - `min_land_acres`
  - `max_land_acres`
  - `government_level`
  - `benefit_type`
  - `target_crops`
  - `irrigation_requirements`
  - `record_type`
  - `parent_scheme_id`
  - `land_size_within_scheme_range`
  - `water_source_compatible`

### Ablation 3 — Representation Comparison: Text Representation (29 features)
Replaces categorical `immediate_need` with text TF-IDF vectorization fit inside fold:
  - `land_size_acres`
  - `annual_family_income_lakh`
  - `secondary_constraint_count`
  - `zone_id`
  - `district`
  - `crop_primary`
  - `crop_secondary`
  - `land_type`
  - `social_category`
  - `farmer_category`
  - `operational_water_source`
  - `borewell_electric_status`
  - `primary_crisis`
  - `immediate_need_text`
  - `is_pure_tenant_without_land_title`
  - `land_ownership_cutoff_pre_feb_2019`
  - `paid_income_tax_last_assessment_year`
  - `pensioner_is_mts_exempt`
  - `registered_professional_is_none`
  - `min_land_acres`
  - `max_land_acres`
  - `government_level`
  - `benefit_type`
  - `target_crops`
  - `irrigation_requirements`
  - `record_type`
  - `parent_scheme_id`
  - `land_size_within_scheme_range`
  - `water_source_compatible`

---

## 3. Cross-Validation Strategy

- **Primary:** GroupKFold (n_splits=5) grouped by `scenario_id`.  
  All candidates from one scenario stay in the same fold — no scenario-level leakage possible.
- **LOZO:** Leave-one-zone-out across Z1–Z10.
- **Crisis holdout:** All `SOIL_HEALTH_AND_FERTILIZER` scenarios (n=17) held out.
- **Land-tenure holdout:** All tenant scenarios (n=24) held out.
- **20% scenario holdout:** Every 5th scenario (n=18) held out.
- Preprocessing, encodings, TF-IDF, and scalers fit **only on training portion of each fold**.
- `OneHotEncoder(handle_unknown="ignore")` for unseen test-fold categories.

---

## 4. Global Results (GroupKFold OOF)

| System | Configuration / Representation | NDCG@3 | MRR |
|---|---|---|---|
| **ML Ablation 1** | Primary Model (Structured `immediate_need`) | **0.8993** | **0.8120** |
| ML Ablation 3 | Need Representation Comparison (Text TF-IDF) | 0.8993 | 0.8120 |
| ML Ablation 2 | Sensitivity Baseline (Excludes `immediate_need`) | 0.8886 | 0.7893 |
| Heuristic Baseline | Deterministic Need Mapping | 0.7803 | 0.7131 |

**Delta Ndcg@3 (Ablation 1 vs Heuristic):** +0.1190  
**Delta Mrr (Ablation 1 vs Heuristic):** +0.0989  
**Delta Ndcg@3 (Structured vs Text Representation):** +0.0000  
**Delta Ndcg@3 (Structured vs No Immediate Need):** +0.0108  
**Paired permutation test p-value (B=10,000, seed=42, two-sided):** 0.0001

---

## 5. Zone-Level Results

### 5a. OOF Zone Means (in-distribution, trained on all scenarios)

| Zone | ML NDCG@3 | Heuristic NDCG@3 | Delta  |
|---|---|---|---|
| Z1 | 0.9608 | 0.6136 | +0.3471 |
| Z2 | 0.9212 | 0.7381 | +0.1830 |
| Z3 | 0.8934 | 0.7491 | +0.1443 |
| Z4 | 0.8927 | 0.8355 | +0.0572 |
| Z5 | 0.9178 | 0.8083 | +0.1096 |
| Z6 | 0.9061 | 0.8134 | +0.0927 |
| Z7 | 0.9090 | 0.8432 | +0.0658 |
| Z8 | 0.9125 | 0.8222 | +0.0902 |
| Z9 | 0.8441 | 0.8522 | -0.0081 |
| Z10 | 0.8359 | 0.7275 | +0.1084 |

### 5b. LOZO Results (true held-out generalization — trained on other 9 zones)

| Zone | ML NDCG@3 | Heuristic NDCG@3 | Delta  | Non-Regression |
|---|---|---|---|---|
| Z1 | 0.9522 | 0.6136 | +0.3385 | ✅ |
| Z10 | 0.8781 | 0.7275 | +0.1506 | ✅ |
| Z2 | 0.9184 | 0.7381 | +0.1802 | ✅ |
| Z3 | 0.9376 | 0.7491 | +0.1885 | ✅ |
| Z4 | 0.9135 | 0.8355 | +0.0781 | ✅ |
| Z5 | 0.8433 | 0.8083 | +0.0351 | ✅ |
| Z6 | 0.9377 | 0.8134 | +0.1243 | ✅ |
| Z7 | 0.9445 | 0.8432 | +0.1013 | ✅ |
| Z8 | 0.9297 | 0.8222 | +0.1075 | ✅ |
| Z9 | 0.9174 | 0.8522 | +0.0652 | ✅ |

**Gate 3 (zone non-regression via LOZO):** ✅ MET

---

## 6. Held-Out Generalization Results

### 6a. Crisis-Type Holdout (`SOIL_HEALTH_AND_FERTILIZER`, n=17)

| System | NDCG@3 |
|---|---|
| ML Ablation 1 | 0.8353 |
| Heuristic Baseline | 0.8099 |
| Delta  | +0.0254 |

### 6b. Land-Tenure Holdout (tenant scenarios, n=24)

| System | NDCG@3 |
|---|---|
| ML Ablation 1 | 0.9789 |
| Heuristic Baseline | 0.9419 |
| Delta  | +0.0370 |

### 6c. Scenario-Level 20% Holdout (n=18)

| System | NDCG@3 |
|---|---|
| ML Ablation 1 | 0.9627 |
| Heuristic Baseline | 0.7775 |
| Delta  | +0.1852 |

---

## 7. Preregistered Acceptance Criteria — Verdict

| Gate | Criterion | Observed | Verdict |
|---|---|---|---|
| Gate 1 | Delta  mean NDCG@3 ≥ δ_min (not specified in preregistration) | +0.1190 | ⚠️ **CANNOT EVALUATE** — δ_min undefined |
| Gate 2 | p < α (not specified in preregistration) | p = 0.0001 | ⚠️ **CANNOT EVALUATE** — α undefined |
| Gate 3 | Zone non-regression (LOZO Delta NDCG@3_z ≥ 0.000 for all zones) | See §5b | ✅ MET |

> **Protocol note:** The approved v1.2 preregistration states "No numeric thresholds are set in this preregistration. The research team must define δ_min and α before v1.2 label collection." These thresholds were not defined before labels were available; therefore Gates 1 and 2 cannot be formally evaluated.

---

## 8. Reproducibility Checklist

| Item | Status |
|---|---|
| Annotation SHA-256 verified | ✅ `8ab03fba5f4cd4a1c9783a2bac3864f3d8530ed15e112ddd3f3a05f90fdf3d26` |
| All annotated pairs match Section A candidate sets | ✅ |
| `archetype_id` absent from all feature matrices | ✅ |
| `immediate_need_matches_heuristic_primary` absent from all feature matrices | ✅ |
| `immediate_need` present in Ablation 1, absent in Ablation 2 | ✅ |
| No label-derived columns in feature matrices | ✅ |
| Preprocessing fit only on training folds | ✅ |
| Scenario-group isolation verified in each fold | ✅ |
| Random seed fixed (random_state=42) | ✅ |
| v1.1 artifacts unmodified | ✅ |
| Eligibility engine unmodified | ✅ |
| No new labels generated | ✅ |
| No commits or pushes | ✅ |

---

## 9. Artifacts

All artifacts at `data/benchmarks/v1.2/ml_experiment/`:

| File | Description |
|---|---|
| `model_metadata_v1.2.0.json` | Model config, provenance, feature policy |
| `feature_inventory_v1.2.0.json` | Feature lists for both ablations |
| `fold_assignments_v1.2.0.json` | GroupKFold fold assignments |
| `oof_predictions_v1.2.0.json` | Full OOF prediction arrays (both ablations) |
| `baseline_predictions_v1.2.0.json` | Heuristic baseline rankings and metrics |
| `metrics_v1.2.0.json` | All per-scenario and aggregate metrics |
| `training_labels_v1.2.0.csv` | Processed label artifact (not using _blank) |
| `provenance_v1.2.0.json` | Label provenance, SHA-256, IRR limitation |
| `ablation_v1.2.0/ablation_metadata_v1.2.0.json` | Ablation configuration |
| `ablation_v1.2.0/ablation_results_v1.2.0.json` | Ablation comparison results |

---

## 10. Interpretation

The ML model (Ablation 1) achieves higher OOF NDCG@3 than the heuristic baseline on the v1.2 single-annotator labels. However, this **must not** be interpreted as evidence of superior real-world recommendation quality because:

1. **Single annotator, no IRR:** Labels from one reviewer with no independent verification cannot serve as a reliable gold standard.
2. **Small dataset:** 90 scenarios and 8 unique Section A schemes constrain the model's ability to generalise.
3. **Acceptance criteria undefined:** Without preregistered δ_min and α, the observed gains cannot be formally accepted or rejected.
4. **Provenance:** The label provenance limitation noted in v1.1 (all 269 scores matching an AI practice file) does not apply here — v1.2 labels are from a new annotation round — but the absence of independent IRR remains a limitation.

**Gate 3 (LOZO zone non-regression)** is the only acceptance gate that can be formally evaluated and passes for all zones.

The `immediate_need` feature contributes positively relative to Ablation 2 (Delta  = +0.0108), consistent with the preregistration hypothesis that it provides legitimate farmer-context signal. Verification requires independent annotation.
