# Benchmark v1.1 ML Experiment — Methodology Audit

**Repository:** `farmer-benefit-ml`  
**Audit date:** 2026-10-28  
**Auditor:** Independent methodological audit (read-only; no model changes, no hyperparameter tuning)  
**Scope:** Exploratory ML ranking experiment (S071–S130, N=60 scenarios)

---

## Audit Summary

| # | Check | Status | Summary |
|---|-------|--------|---------|
| 1 | GroupKFold out-of-fold CV integrity | **PASS** | No scenario appears in both train and test; each scenario is held out exactly once |
| 2 | Feature leakage analysis | **WARN** | No direct target leakage, but 4 features enable memorization of repeating archetype patterns |
| 3 | NDCG@3 / MRR recomputation | **PASS** | All reported figures verified exactly against saved artifacts |
| 4 | ML vs heuristic comparability | **PASS** | Same candidate pairs, scenarios, labels, and metric implementations |
| 5 | Leave-one-archetype-out implementation | **WARN** | Implemented correctly; reveals ARCH_3 regression (−0.2084) |
| 6 | Near-perfect GroupKFold results explained | **WARN** | 59/60 NDCG@3=1.0, 60/60 MRR=1.0 — driven by archetype-memorizing features |
| 7 | Annotation provenance limitation | **PASS** | Documented as exploratory training targets, not verified human gold labels |

**Overall: Results are internally consistent and reproducible, but the near-perfect GroupKFold metrics do not reflect genuine generalization.** The LOAO results (mean 0.8244 vs heuristic 0.7760, delta +0.0484) are more informative but still not statistically validated.

---

## 1. GroupKFold Out-of-Fold CV Integrity — PASS

### What was checked
- `run_out_of_fold_evaluation()` in `src/models/benchmark_v1_1/ranker.py:460`
- `GroupKFold(n_splits=5)` grouped by `scenario_id`
- 269 feature rows across 60 scenarios
- Each scenario appears in exactly one test fold
- No scenario appears in both train and test sets within any fold

### Evidence
- `test_group_kfold_no_scenario_leakage` — PASSES
- `test_group_kfold_covers_all_scenarios` — PASSES (each scenario in test set exactly once)
- `test_oof_evaluation_produces_all_scenarios` — PASSES (no NaN OOF scores)
- All 269 rows have finite OOF predictions

### Preprocessing fit scope
- `ColumnTransformer` with `StandardScaler` and `OneHotEncoder` is fit **only** on each fold's training data (`train_df`)
- `OneHotEncoder(handle_unknown="ignore")` handles unseen categories in test folds
- No target encoding or statistics computed from test data

### Finding
**PASS** — The GroupKFold implementation correctly prevents scenario-level data leakage. Each held-out scenario is ranked by a model that did not train on any of that scenario's candidates.

---

## 2. Feature Leakage Analysis — WARN

### Direct target leakage — NONE FOUND

| Check | Result |
|-------|--------|
| `relevance_score` in features | Not present |
| `relevance_rationale` in features | Not present |
| `complementarity_notes` in features | Not present |
| `heuristic_score` in features | Not present |
| `heuristic_rank` in features | Not present |
| `model_score` / `model_prediction` in features | Not present |
| Any column with "label", "ai_rationale", "consensus" | Not present |

The `validate_no_label_leakage()` function confirms no forbidden columns are present (test `test_no_label_leakage` PASSES).

### Indirect leakage / memorization-enabling features — WARN

The following features do not contain target labels but make the prediction task trivially easy by encoding the same structure that determines the labels:

| Feature | Why it enables memorization |
|---------|---------------------------|
| `immediate_need` | Directly determines which schemes are relevant. All 10 scenarios in an archetype share the same `immediate_need`, and labels follow a consistent pattern per need. |
| `archetype_id` | Same as above — encodes the archetype pattern that drives label assignment. |
| `scheme_id` | Combined with `immediate_need`, allows the model to memorize which scheme is relevant for which need (e.g., SCH009 is score 3 for SOIL_HEALTH_AND_FERTILIZER). |
| `immediate_need_matches_heuristic_primary` | Direct binary encoding of whether a scheme matches the heuristic primary scheme — which is almost always the highest-scored scheme (label 3). |
| `water_source_compatible` | Derived from scenario water source + scheme irrigation requirements. Correlates with eligibility and relevance. |
| `land_size_within_scheme_range` | Derived from land size vs scheme min/max. Correlates with eligibility. |

### Why this matters

The labels were assigned by a single annotator who evaluated schemes against the same `immediate_need` classification that drives the features. With GroupKFold by scenario, when a scenario from ARCH_1 (SOLAR_PUMP_INSTALLATION) is held out, the model still trains on 9 other ARCH_1 scenarios with identical `immediate_need` and very similar candidate sets. The model learns the need-to-scheme mapping rather than generalizing to new patterns.

This explains why 59/60 scenarios achieve NDCG@3 = 1.0 in GroupKFold — the task is effectively memorization of 6 archetype patterns, not generalization.

### Finding
**WARN** — No direct target leakage, but features enable memorization of repeating archetype patterns. GroupKFold results overstate generalization capability.

---

## 3. NDCG@3 / MRR Recomputation — PASS

### What was checked
- Independently recomputed all metrics from saved `oof_predictions_v1.1.0.json` and `metrics_v1.1.0.json`
- Used `compute_ndcg_at_k` and `compute_mrr` from `src/evaluation/metrics.py`
- Compared recomputed values against reported values

### Evidence

| Metric | Recomputed | Reported | Match |
|--------|-----------|----------|-------|
| ML Mean NDCG@3 | 0.997380 | 0.997380 | PASS |
| ML Mean MRR | 1.000000 | 1.000000 | PASS |
| Heuristic Mean NDCG@3 | 0.775959 | 0.775959 | PASS |
| Heuristic Mean MRR | 0.783333 | 0.783333 | PASS |

- 59/60 scenarios have ML NDCG@3 = 1.0
- 60/60 scenarios have ML MRR = 1.0
- All ML rankings use valid Section A candidate sets (no duplicates, no unknown scheme IDs)
- MRR threshold (tau=2.0) is identical for both ML and heuristic

### Finding
**PASS** — All reported figures are exactly reproducible from the saved artifacts.

---

## 4. ML vs Heuristic Comparability — PASS

### What was checked
- Same candidate pairs: ML rankings and heuristic rankings both use Section A candidates from `candidate_generation_results.json`
- Same scenarios: 60 scenarios (S071–S130) for both
- Same relevance labels: Single-annotator `human_reviewer_annotations.csv` used for both
- Same metric implementations: `compute_ndcg_at_k` and `compute_mrr` from `src/evaluation/metrics.py`
- Same MRR threshold: tau=2.0 for both
- No in-sample predictions in OOF metrics: Each scenario's ML ranking comes from a fold where that scenario was held out

### Evidence
- `test_ml_rankings_match_candidate_sets` — PASSES (all 60 scenarios)
- `test_oof_evaluation_grouped_by_scenario` — PASSES (no NaN, all finite)
- `compute_metrics_for_scenario` uses identical `label_map` for both models
- Delta NDCG@3 = +0.2214, Delta MRR = +0.2167 — both computed consistently

### Finding
**PASS** — ML and heuristic results are directly comparable on identical data and metrics.

---

## 5. Leave-One-Archetype-Out Implementation — WARN

### What was checked
- Leave-one-archetype-out evaluation in `scripts/train_exploratory_ranker_v1_1.py:286-351`
- 6 archetypes, 10 scenarios each
- Each archetype held out in turn; model trained on remaining 50 scenarios
- Held-out archetype scenarios excluded from training data

### Evidence

| Archetype | ML NDCG@3 | Heuristic NDCG@3 | Delta |
|-----------|-----------|------------------|-------|
| ARCH_1 | 0.9468 | 0.8036 | +0.1432 |
| ARCH_2 | 0.6291 | 0.6291 | +0.0000 |
| ARCH_3 | 0.5424 | 0.7509 | −0.2084 |
| ARCH_4 | 1.0000 | 1.0000 | +0.0000 |
| ARCH_5 | 0.9855 | 0.6598 | +0.3258 |
| ARCH_6 | 0.8425 | 0.8124 | +0.0300 |

**LOAO mean:** ML = 0.8244, Heuristic = 0.7760, Delta = +0.0484

### Unseen-category handling
- `OneHotEncoder(handle_unknown="ignore")` encodes unseen categories as all zeros
- All archetypes appear in training for 5 of 6 folds, so no truly unseen archetypes in LOAO
- However, within a held-out archetype, all 10 scenarios are unseen, testing generalization to new instances of the same pattern

### ARCH_3 regression warning
ARCH_3 (PROTECTED_HORTICULTURE) shows ML = 0.5424 vs Heuristic = 0.7509, a delta of −0.2084. This is the clearest evidence that the learned model does not generalize better than the heuristic across all pattern types.

### Finding
**WARN** — LOAO implementation is correct but reveals that the ML model underperforms the heuristic on ARCH_3 (−0.2084 delta). The unweighted LOAO mean delta (+0.0484) is a descriptive summary, not a statistical significance result.

---

## 6. Near-Perfect GroupKFold Results Explained — WARN

### Reported results
- ML Mean NDCG@3: 0.9974 (59/60 scenarios at 1.0)
- ML Mean MRR: 1.0000 (60/60 scenarios at 1.0)
- Heuristic Mean NDCG@3: 0.7760
- Delta NDCG@3: +0.2214

### Explanation

The near-perfect GroupKFold results are **not a bug** — they are correctly computed. However, they are **not evidence of strong generalization**. The reasons:

1. **Archetype repetition**: 60 scenarios = 6 archetypes × 10 scenarios each. All scenarios in an archetype share the same `immediate_need` and similar candidate sets.

2. **Feature-label alignment**: The annotator's labels follow the same need-to-scheme logic encoded in features like `immediate_need`, `archetype_id`, and `immediate_need_matches_heuristic_primary`.

3. **GroupKFold limitation**: When a scenario is held out, 9 other scenarios from the same archetype remain in training. The model memorizes the archetype pattern rather than learning generalizable rules.

4. **Histogram Gradient Boosting suitability**: `HistGradientBoostingRegressor` with 269 rows and 30 features can easily fit 6 repeating patterns.

### LOAO as a more realistic estimate
LOAO results (mean 0.8244) are substantially lower than GroupKFold (0.9974), confirming that the GroupKFold results overstate generalization. ARCH_3 shows the model can perform worse than the heuristic on held-out patterns.

### Finding
**WARN** — Reported figures are correct but overstate generalization. LOAO results should be weighted more heavily for assessing real-world performance.

---

## 7. Annotation Provenance Limitation — PASS

### What was checked
- Annotation file: `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv`
- Single rater_id: `human reviewer` on all 269 rows
- QC report: `reports/human_annotation_qc_report.md`
- SHA-256: `38e237fec447e8b760bc59631ab12a4646c87c495c4bff4a63c55ffa280468a1`
- All 269 scores match `AI_PRACTICE_v1.1_completed_NOT_HUMAN.csv` (269/269 identical)

### Documentation
- Model metadata: `provenance_limitation` field explicitly states the limitation
- Experiment report: "Important Limitations" section documents the issue
- Metrics file: `provenance_limitation` field included
- No claim that labels are verified independent human gold labels
- No inter-rater reliability computed (single annotator)

### Finding
**PASS** — The provenance limitation is clearly and repeatedly documented. Labels are treated as exploratory training targets only.

---

## 8. Potential Failure Modes

| Failure Mode | Likelihood | Impact | Mitigation |
|-------------|-----------|--------|------------|
| Archetype memorization inflating GroupKFold metrics | High | High | Rely on LOAO results; add more diverse scenarios |
| Small sample size (60 scenarios) | High | Medium | Results are exploratory; not production-ready |
| Single-annotator labels with AI practice match | High | High | Do not treat as verified ground truth |
| ARCH_3 model regression vs heuristic | Medium | Medium | Investigate feature importance for ARCH_3 |
| No statistical significance testing | Medium | Medium | Paired permutation test not applicable (single model vs baseline on same labels) |

---

## 9. Recommendations

1. **Do not claim formal acceptance gates passed.** The preregistered criteria (ΔNDCG@3 ≥ +0.050, p < 0.050, zone non-regression) require two independent systems and resolved annotation provenance. Neither condition is met.

2. **Use LOAO results, not GroupKFold, for generalization assessment.** LOAO mean delta (+0.0484) is more realistic but still below the +0.050 threshold and lacks statistical validation.

3. **Investigate ARCH_3 regression.** The model underperforms the heuristic on PROTECTED_HORTICULTURE scenarios (−0.2084 delta). This may indicate feature importance issues or insufficient training examples for this archetype.

4. **Consider removing or down-weighting `immediate_need_matches_heuristic_primary`** as it directly encodes the heuristic mapping, making the comparison with the heuristic less meaningful.

5. **Do not tune hyperparameters based on these results.** The dataset is too small for reliable hyperparameter selection.

6. **Preserve all current experiment outputs** for reproducibility. Do not overwrite predictions or metrics.

---

## 10. Reproducibility Commands

```bash
# Re-run the full training and evaluation
python scripts/train_exploratory_ranker_v1_1.py

# Run ML-specific tests
python -m pytest tests/test_ml_ranker_v1_1.py -v

# Run all existing regression tests (should still pass)
python -m pytest tests/ -v

# Independent metric recomputation
python scripts/independent_metric_recompute.py
```

**Expected outputs:**
- ML Global Mean NDCG@3: 0.9974
- ML Global Mean MRR: 1.0000
- Heuristic Global Mean NDCG@3: 0.7760
- Heuristic Global Mean MRR: 0.7833
- LOAO ML mean: 0.8244, LOAO Heuristic mean: 0.7760

---

## Audit Conclusion

The ML experiment is **internally consistent and reproducible**. All reported metrics are verified correct. The GroupKFold CV implementation correctly prevents scenario-level leakage. However, the near-perfect GroupKFold results (0.9974 NDCG@3, 1.0000 MRR) reflect memorization of 6 repeating archetype patterns rather than genuine generalization. The LOAO results (mean 0.8244) are more informative but show mixed performance, with ARCH_3 regression (−0.2084) as a clear warning.

**These are exploratory results on single-annotator labels with a documented AI practice file match. They must not be presented as validated human-ground-truth benchmark results, and the preregistered acceptance criteria have not been met.**
