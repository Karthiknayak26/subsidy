# Benchmark v1.1 Feature-Ablation Experiment (v1.1.1)

**Benchmark Version:** `v1.1` (S071–S130, N=60 scenarios)
**Experiment Type:** Exploratory feature-ablation (NOT formal pre-registered evaluation)
**Model:** BenchmarkV11Ranker (HistGradientBoostingRegressor pipeline)
**Baseline:** Heuristic baseline (need-to-scheme mapping)
**Labels Source:** `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` (single annotator)
**Reference:** v1.1.0 full experiment preserved unchanged

## Important Limitations

### Provenance Limitation
All 269 relevance scores in the annotation file match an earlier AI practice file row-for-row (269/269 identical scores). These labels are treated as exploratory training targets only and MUST NOT be described as verified independent human gold labels. Any model trained on these labels inherits this provenance limitation.

### Single-Annotator Dataset
The annotation file has a single rater_id (`human reviewer`). No inter-rater reliability is computed.

### Small Dataset
Only 60 scenarios and 269 candidate pairs. Six archetypes with 10 scenarios each. Results are exploratory and should not be treated as definitive.

### Model-Selection Bias
The six archetypes are also used for diagnostic comparisons. Choosing a feature set based on these ablation results would constitute model-selection bias and overfit to this diagnostic comparison.

### No Formal Acceptance Gates
The preregistered acceptance criteria (ΔNDCG@3 ≥ +0.050, paired permutation test p < 0.050, zone-level non-regression) are NOT evaluated here.

## Ablation Configurations

| Config | Name | Features | Excluded Columns |
|--------|------|----------|------------------|
| A | full_feature_set | 30 | (none) |
| B | no_heuristic_match | 29 | immediate_need_matches_heuristic_primary |
| C | no_archetype_id | 29 | archetype_id |
| D | no_immediate_need | 29 | immediate_need |
| E | combined_ablation | 27 | immediate_need_matches_heuristic_primary, archetype_id, immediate_need |

## Global Results (Out-of-Fold, GroupKFold by scenario)

| Config | ML NDCG@3 | ML MRR | Heuristic NDCG@3 | Heuristic MRR | Δ NDCG@3 | Δ MRR |
|--------|-----------|--------|------------------|---------------|----------|-------|
| A | 0.9974 | 1.0000 | 0.7760 | 0.7833 | +0.2214 | +0.2167 |
| B | 0.9935 | 1.0000 | 0.7760 | 0.7833 | +0.2175 | +0.2167 |
| C | 0.9974 | 1.0000 | 0.7760 | 0.7833 | +0.2214 | +0.2167 |
| D | 0.9974 | 1.0000 | 0.7760 | 0.7833 | +0.2214 | +0.2167 |
| E | 0.9974 | 1.0000 | 0.7760 | 0.7833 | +0.2214 | +0.2167 |

## Leave-One-Archetype-Out Results (NDCG@3)

| Config | ARCH_1 | ARCH_2 | ARCH_3 | ARCH_4 | ARCH_5 | ARCH_6 | Mean ML | Mean Heuristic | Δ |
|--------|--------|--------|--------|--------|--------|--------|---------|----------------|---|
| A | 0.9468 | 0.6291 | 0.5424 | 1.0000 | 0.9855 | 0.8425 | 0.8244 | 0.7760 | +0.0484 |
| B | 0.7713 | 1.0000 | 0.8402 | 0.7098 | 0.5226 | 0.5070 | 0.7251 | 0.7760 | -0.0508 |
| C | 0.9468 | 0.6291 | 0.5424 | 1.0000 | 0.9855 | 0.8425 | 0.8244 | 0.7760 | +0.0484 |
| D | 0.9468 | 0.6291 | 0.5424 | 1.0000 | 0.9855 | 0.8425 | 0.8244 | 0.7760 | +0.0484 |
| E | 0.8088 | 1.0000 | 0.7831 | 0.6738 | 0.5226 | 0.5070 | 0.7159 | 0.7760 | -0.0601 |

## ARCH_3 Detail (the regression case)

| Config | ML NDCG@3 | Heuristic NDCG@3 | Δ |
|--------|-----------|------------------|---|
| A | 0.5424 | 0.7509 | -0.2084 |
| B | 0.8402 | 0.7509 | +0.0894 |
| C | 0.5424 | 0.7509 | -0.2084 |
| D | 0.5424 | 0.7509 | -0.2084 |
| E | 0.7831 | 0.7509 | +0.0322 |

## Feature-Level Diagnosis

### Config A (Full, 30 features) — Reference
- Global ML NDCG@3: 0.9974
- LOAO ML mean NDCG@3: 0.8244
- LOAO ARCH_3: 0.5424 (heuristic: 0.7509, delta: -0.2084)

### Config B (No heuristic_match, 29 features)
- Global ML NDCG@3: 0.9935
- LOAO ML mean NDCG@3: 0.7251
- LOAO ARCH_3: 0.8402

### Config C (No archetype_id, 29 features)
- Global ML NDCG@3: 0.9974
- LOAO ML mean NDCG@3: 0.8244
- LOAO ARCH_3: 0.5424

### Config D (No immediate_need, 29 features)
- Global ML NDCG@3: 0.9974
- LOAO ML mean NDCG@3: 0.8244
- LOAO ARCH_3: 0.5424

### Config E (Combined, 27 features)
- Global ML NDCG@3: 0.9974
- LOAO ML mean NDCG@3: 0.7159
- LOAO ARCH_3: 0.7831

## Interpretation

- These are **exploratory** ablation results on single-annotator labels.
- All configurations use identical GroupKFold folds and LOAO partitions.
- No hyperparameter tuning was performed.
- The `immediate_need_matches_heuristic_primary` feature directly encodes whether a scheme matches the heuristic's primary scheme for that immediate need; removing it tests whether the model is simply replicating heuristic judgments.
- The `archetype_id` feature identifies which of six repeating scenario patterns a scenario belongs to; removing it tests archetype memorization.
- The `immediate_need` feature is the text label of the scenario's primary need; removing it tests whether the model learns need-specific scheme preferences.
- A config that performs worse than Config A on ARCH_3 LOAO suggests the removed features were important for that archetype's generalization.
- A config that performs better suggests the removed features were causing overfitting to archetype patterns.

## Outputs

- Ablation metadata: `C:\Users\User\Desktop\subsidy\farmer-benefit-ml\data\benchmarks\v1.1\ml_experiment\ablation_v1.1.1\ablation_metadata_v1.1.1.json`
- Ablation results: `C:\Users\User\Desktop\subsidy\farmer-benefit-ml\data\benchmarks\v1.1\ml_experiment\ablation_v1.1.1\ablation_results_v1.1.1.json`
- Report: `C:\Users\User\Desktop\subsidy\farmer-benefit-ml\reports\benchmark_v1.1_feature_ablation.md`

## Reproducibility

- Random seed: 42
- scikit-learn version: 1.8.0
- All data loaded from repository sources (no external downloads)
- v1.1.0 outputs preserved unchanged under data/benchmarks/v1.1/ml_experiment/

---
*Generated by ablate_ml_ranker_v1_1.py. Exploratory only — not a formal pre-registered evaluation.*