# Benchmark v1.1 ML Exploratory Ranking Experiment

**Benchmark Version:** `v1.1` (S071–S130, N=60 scenarios)
**Experiment Type:** Exploratory ML ranking (NOT formal pre-registered evaluation)
**Model:** BenchmarkV11Ranker (HistGradientBoostingRegressor pipeline)
**Baseline:** Heuristic baseline (need-to-scheme mapping)
**Labels Source:** `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` (single annotator)

## Important Limitations

### Provenance Limitation
All 269 relevance scores in the annotation file match an earlier AI practice file row-for-row (269/269 identical scores). The quality-control report records this without assuming authorship. These labels are treated as exploratory training targets only and MUST NOT be described as verified independent human gold labels. Any model trained on these labels inherits this provenance limitation.

### Single-Annotator Dataset
The annotation file has a single rater_id (`human reviewer`). No inter-rater reliability (Cohen's kappa, Krippendorff's alpha) is available or computed.

### Small Dataset
Only 60 scenarios and 269 candidate pairs are available. This is too small for robust ML generalization estimates. Results should be treated as a prototype, not evidence of production readiness.

### No Formal Acceptance Gates Evaluated
The preregistered acceptance criteria (ΔNDCG@3 ≥ +0.050, paired permutation test p < 0.050, zone-level non-regression) are NOT evaluated here. Those gates require two independent systems and resolved annotation provenance.

## Feature Engineering

Features are derived from scenario context (`scenario_matrix.json`) and scheme metadata (`scheme_master.json`) only. No label information (relevance scores, rationales, complementarity notes) is used as input. The heuristic score itself is NOT included as a feature to prevent leakage.

### Scenario Features
- Numeric: land_size_acres, annual_family_income_lakh, secondary_constraint_count
- Categorical: zone_id, district, crop_primary, crop_secondary, land_type, social_category, farmer_category, operational_water_source, borewell_electric_status, immediate_need, archetype_id
- Boolean: is_pure_tenant_without_land_title, land_ownership_cutoff_pre_feb_2019, paid_income_tax_last_assessment_year, pensioner_is_mts_exempt, registered_professional_is_none

### Scheme Features
- Numeric: min_land_acres, max_land_acres
- Categorical: scheme_id, government_level, benefit_type, target_crops, irrigation_requirements, record_type, parent_scheme_id

### Interaction Features
- land_size_within_scheme_range
- water_source_compatible
- immediate_need_matches_heuristic_primary

## Cross-Validation Strategy

- Primary: GroupKFold (n_splits=5) grouped by scenario_id. All candidates from one scenario stay in the same fold to prevent leakage.
- Secondary: Leave-one-archetype-out (6 archetypes, 10 scenarios each). Stricter test of generalization across farmer need profiles.

## Results

### Global Metrics
- ML Model Mean NDCG@3: **0.9974**
- ML Model Mean MRR: **1.0000**
- Heuristic Baseline Mean NDCG@3: **0.7760**
- Heuristic Baseline Mean MRR: **0.7833**
- Delta NDCG@3 (ML - Heuristic): **+0.2214**
- Delta MRR (ML - Heuristic): **+0.2167**

### Zone-Level Summary

| Zone | Zone Name | Scenarios | ML NDCG@3 | Heuristic NDCG@3 | Delta |
|------|-----------|-----------|-----------|------------------|-------|
| Z1 | North Eastern Transition Zone | 6 | 1.0000 | 0.7934 | +0.2066 |
| Z2 | North Eastern Dry Zone | 6 | 1.0000 | 0.7934 | +0.2066 |
| Z3 | Northern Dry Zone | 6 | 1.0000 | 0.8007 | +0.1993 |
| Z4 | Central Dry Zone | 6 | 1.0000 | 0.7934 | +0.2066 |
| Z5 | Eastern Dry Zone | 6 | 1.0000 | 0.7539 | +0.2461 |
| Z6 | Southern Dry Zone | 6 | 1.0000 | 0.8146 | +0.1854 |
| Z7 | Southern Transition Zone | 6 | 0.9738 | 0.6818 | +0.2920 |
| Z8 | Northern Transition Zone | 6 | 1.0000 | 0.7934 | +0.2066 |
| Z9 | Hilly Zone | 6 | 1.0000 | 0.7752 | +0.2248 |
| Z10 | Coastal Zone | 6 | 1.0000 | 0.7598 | +0.2402 |

### Leave-One-Archetype-Out NDCG@3

| Archetype | ML NDCG@3 | Heuristic NDCG@3 | Delta |
|-----------|-----------|------------------|-------|
| ARCH_1 | 0.9468 | 0.8036 | +0.1432 |
| ARCH_2 | 0.6291 | 0.6291 | +0.0000 |
| ARCH_3 | 0.5424 | 0.7509 | -0.2084 |
| ARCH_4 | 1.0000 | 1.0000 | +0.0000 |
| ARCH_5 | 0.9855 | 0.6598 | +0.3258 |
| ARCH_6 | 0.8425 | 0.8124 | +0.0300 |

### Per-Scenario Results

| Scenario | Zone | District | ML NDCG@3 | Heuristic NDCG@3 | Delta |
|----------|------|----------|-----------|------------------|-------|
| S071 | Z1 | Kalaburagi | 1.0000 | 0.7660 | +0.2340 |
| S072 | Z1 | Bidar | 1.0000 | 0.6291 | +0.3709 |
| S073 | Z1 | Kalaburagi | 1.0000 | 0.6871 | +0.3129 |
| S074 | Z1 | Bidar | 1.0000 | 1.0000 | +0.0000 |
| S075 | Z1 | Kalaburagi | 1.0000 | 0.8657 | +0.1343 |
| S076 | Z1 | Bidar | 1.0000 | 0.8124 | +0.1876 |
| S077 | Z2 | Raichur | 1.0000 | 0.7660 | +0.2340 |
| S078 | Z2 | Kalaburagi | 1.0000 | 0.6291 | +0.3709 |
| S079 | Z2 | Yadgir | 1.0000 | 0.6871 | +0.3129 |
| S080 | Z2 | Raichur | 1.0000 | 1.0000 | +0.0000 |
| S081 | Z2 | Kalaburagi | 1.0000 | 0.8657 | +0.1343 |
| S082 | Z2 | Yadgir | 1.0000 | 0.8124 | +0.1876 |
| S083 | Z3 | Koppal | 1.0000 | 0.7660 | +0.2340 |
| S084 | Z3 | Vijayapura | 1.0000 | 0.6291 | +0.3709 |
| S085 | Z3 | Bagalkot | 1.0000 | 0.8146 | +0.1854 |
| S086 | Z3 | Gadag | 1.0000 | 1.0000 | +0.0000 |
| S087 | Z3 | Koppal | 1.0000 | 0.7824 | +0.2176 |
| S088 | Z3 | Vijayapura | 1.0000 | 0.8124 | +0.1876 |
| S089 | Z4 | Davanagere | 1.0000 | 0.7660 | +0.2340 |
| S090 | Z4 | Tumakuru | 1.0000 | 0.6291 | +0.3709 |
| S091 | Z4 | Chitradurga | 1.0000 | 0.6871 | +0.3129 |
| S092 | Z4 | Davanagere | 1.0000 | 1.0000 | +0.0000 |
| S093 | Z4 | Tumakuru | 1.0000 | 0.8657 | +0.1343 |
| S094 | Z4 | Chitradurga | 1.0000 | 0.8124 | +0.1876 |
| S095 | Z5 | Chikkaballapura | 1.0000 | 1.0000 | +0.0000 |
| S096 | Z5 | Bengaluru Rural | 1.0000 | 0.6291 | +0.3709 |
| S097 | Z5 | Ramanagara | 1.0000 | 0.6871 | +0.3129 |
| S098 | Z5 | Kolar | 1.0000 | 1.0000 | +0.0000 |
| S099 | Z5 | Chikkaballapura | 1.0000 | 0.3948 | +0.6052 |
| S100 | Z5 | Bengaluru Rural | 1.0000 | 0.8124 | +0.1876 |
| S101 | Z6 | Mandya | 1.0000 | 0.7660 | +0.2340 |
| S102 | Z6 | Mysuru | 1.0000 | 0.6291 | +0.3709 |
| S103 | Z6 | Chamarajanagar | 1.0000 | 0.8146 | +0.1854 |
| S104 | Z6 | Mandya | 1.0000 | 1.0000 | +0.0000 |
| S105 | Z6 | Mysuru | 1.0000 | 0.8657 | +0.1343 |
| S106 | Z6 | Chamarajanagar | 1.0000 | 0.8124 | +0.1876 |
| S107 | Z7 | Shivamogga | 0.8428 | 0.4398 | +0.4030 |
| S108 | Z7 | Chikkamagaluru | 1.0000 | 0.6291 | +0.3709 |
| S109 | Z7 | Hassan | 1.0000 | 0.8146 | +0.1854 |
| S110 | Z7 | Shivamogga | 1.0000 | 1.0000 | +0.0000 |
| S111 | Z7 | Chikkamagaluru | 1.0000 | 0.3948 | +0.6052 |
| S112 | Z7 | Hassan | 1.0000 | 0.8124 | +0.1876 |
| S113 | Z8 | Haveri | 1.0000 | 0.7660 | +0.2340 |
| S114 | Z8 | Dharwad | 1.0000 | 0.6291 | +0.3709 |
| S115 | Z8 | Belagavi | 1.0000 | 0.6871 | +0.3129 |
| S116 | Z8 | Haveri | 1.0000 | 1.0000 | +0.0000 |
| S117 | Z8 | Dharwad | 1.0000 | 0.8657 | +0.1343 |
| S118 | Z8 | Belagavi | 1.0000 | 0.8124 | +0.1876 |
| S119 | Z9 | Kodagu | 1.0000 | 1.0000 | +0.0000 |
| S120 | Z9 | Chikkamagaluru | 1.0000 | 0.6291 | +0.3709 |
| S121 | Z9 | Uttara Kannada | 1.0000 | 0.8146 | +0.1854 |
| S122 | Z9 | Kodagu | 1.0000 | 1.0000 | +0.0000 |
| S123 | Z9 | Chikkamagaluru | 1.0000 | 0.3948 | +0.6052 |
| S124 | Z9 | Uttara Kannada | 1.0000 | 0.8124 | +0.1876 |
| S125 | Z10 | Udupi | 1.0000 | 1.0000 | +0.0000 |
| S126 | Z10 | Uttara Kannada | 1.0000 | 0.6291 | +0.3709 |
| S127 | Z10 | Dakshina Kannada | 1.0000 | 0.8146 | +0.1854 |
| S128 | Z10 | Udupi | 1.0000 | 1.0000 | +0.0000 |
| S129 | Z10 | Uttara Kannada | 1.0000 | 0.3024 | +0.6976 |
| S130 | Z10 | Dakshina Kannada | 1.0000 | 0.8124 | +0.1876 |

## Interpretation

- These are **exploratory** results on single-annotator labels with a documented provenance limitation.
- The ML model uses GroupKFold out-of-fold predictions, so each scenario is ranked by a model that did not train on that scenario's candidates.
- No statistical significance testing is performed (requires proper train/test separation and more data).
- The heuristic baseline is a deterministic need-to-scheme mapping with no learning.
- Delta NDCG@3 close to 0 suggests the ML model does not clearly outperform the heuristic on this small exploratory dataset.

## Outputs

- Model metadata: `C:\Users\User\Desktop\subsidy\farmer-benefit-ml\data\benchmarks\v1.1\ml_experiment\model_metadata_v1.1.0.json`
- OOF predictions: `C:\Users\User\Desktop\subsidy\farmer-benefit-ml\data\benchmarks\v1.1\ml_experiment\oof_predictions_v1.1.0.json`
- Metrics: `C:\Users\User\Desktop\subsidy\farmer-benefit-ml\data\benchmarks\v1.1\ml_experiment\metrics_v1.1.0.json`
- Report: `C:\Users\User\Desktop\subsidy\farmer-benefit-ml\reports\benchmark_v1.1_ml_experiment.md`

## Reproducibility

- Random seed: 42
- scikit-learn version: 1.8.0
- All data loaded from repository sources (no external downloads)

---
*Generated by train_exploratory_ranker_v1_1.py. Exploratory only — not a formal pre-registered evaluation.*