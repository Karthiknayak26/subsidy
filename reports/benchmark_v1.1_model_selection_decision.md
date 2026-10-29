# Benchmark v1.1 Model-Selection Decision

**Repository:** `farmer-benefit-ml`  
**Decision date:** 2026-10-28  
**Decision scope:** Benchmark v1.1 ML recommender (S071–S130, N=60 scenarios)  
**Status:** Recorded — model remains experimental, not production-ready

---

## Part A — Model-Selection Decision

### Decision

**The Benchmark v1.1 learned ranker (BenchmarkV11Ranker) remains experimental. It is NOT ready for deployment and has NOT met any formal acceptance criteria.** The deterministic heuristic baseline remains the reference system for Benchmark v1.1.

This decision is based on the v1.1.0 exploratory experiment and the v1.1.1 feature-ablation experiment. Both are preserved unchanged for reproducibility.

---

### Observed Evidence (not interpretation)

#### v1.1.0 full experiment (30 features)

| Metric | ML Model | Heuristic Baseline | Delta |
|--------|----------|-------------------|-------|
| Global Mean NDCG@3 | 0.9974 | 0.7760 | +0.2214 |
| Global Mean MRR | 1.0000 | 0.7833 | +0.2167 |

**Leave-One-Archetype-Out (LOAO) NDCG@3:**

| Archetype | ML NDCG@3 | Heuristic NDCG@3 | Delta |
|-----------|-----------|------------------|-------|
| ARCH_1 | 0.9468 | 0.8036 | +0.1432 |
| ARCH_2 | 0.6291 | 0.6291 | +0.0000 |
| ARCH_3 | 0.5424 | 0.7509 | −0.2084 |
| ARCH_4 | 1.0000 | 1.0000 | +0.0000 |
| ARCH_5 | 0.9855 | 0.6598 | +0.3258 |
| ARCH_6 | 0.8425 | 0.8124 | +0.0300 |
| **Mean** | **0.8244** | **0.7760** | **+0.0484** |

- 59/60 scenarios have ML NDCG@3 = 1.0; 60/60 have ML MRR = 1.0
- ARCH_3 (PROTECTED_HORTICULTURE) shows ML underperforming the heuristic by −0.2084

#### v1.1.1 feature-ablation experiment

| Config | Features Excluded | LOAO Mean NDCG@3 | LOAO Mean Delta vs Heuristic | LOAO ARCH_3 NDCG@3 | ARCH_3 Delta vs Heuristic |
|--------|------------------|-------------------|------------------------------|---------------------|--------------------------|
| A — Full (30) | — | 0.8244 | +0.0484 | 0.5424 | −0.2084 |
| B — No heuristic match (29) | `immediate_need_matches_heuristic_primary` | 0.7251 | −0.0508 | 0.8402 | +0.0894 |
| C — No archetype_id (29) | `archetype_id` | 0.8244 | +0.0484 | 0.5424 | −0.2084 |
| D — No immediate_need (29) | `immediate_need` | 0.8244 | +0.0484 | 0.5424 | −0.2084 |
| E — Combined (27) | all three | 0.7159 | −0.0601 | 0.7831 | +0.0322 |

#### Key relationships observed

1. **`archetype_id` and `immediate_need` are collinear** — a 1:1 mapping of six needs to six archetypes. Removing either alone produces identical results to the full feature set (Configs C and D equal Config A).

2. **`immediate_need_matches_heuristic_primary` is the critical feature** — removing it (Config B) changes ARCH_3 from −0.2084 delta to +0.0894 delta, but reduces the LOAO mean from +0.0484 to −0.0508.

3. **Combined removal (Config E)** — ARCH_3 improves to +0.0322 delta, but the LOAO mean drops to −0.0601, below the heuristic baseline.

4. **No configuration improves the LOAO mean above the heuristic baseline** while also improving ARCH_3. The best ARCH_3 result (+0.0894 in Config B) comes with the worst overall LOAO mean (−0.0508).

#### What the evidence does NOT show

- The ablation results do **not** prove the model cannot learn useful farmer–scheme suitability relationships.
- The ablation results do **not** identify which specific non-heuristic features (if any) carry genuine signal.
- The small sample size (60 scenarios, 6 archetypes) prevents definitive conclusions about generalization.

---

### Recorded Limitations

| Limitation | Detail |
|------------|--------|
| Annotation provenance | All 269 annotation scores match an earlier AI practice file row-for-row (269/269). Labels are exploratory training targets, not verified independent human gold labels. |
| Single annotator | One rater_id (`human reviewer`) on all 269 rows. No inter-rater reliability computed. |
| Small dataset | 60 scenarios, 269 candidate pairs, 6 archetypes with 10 scenarios each. |
| Repeated archetypes | All scenarios in an archetype share the same `immediate_need` and similar candidate sets. GroupKFold results reflect memorization of 6 patterns, not generalization. |
| No formal acceptance gates | Preregistered criteria (ΔNDCG@3 ≥ +0.050, p < 0.050, zone non-regression) not evaluated. Requires two independent systems and resolved annotation provenance. |
| Model-selection bias acknowledged | Choosing a feature set based on these ablation results would overfit to this diagnostic comparison. |

---

### Model-Selection Decision

| Question | Decision | Rationale |
|----------|----------|-----------|
| Is the learned ranker ready for deployment? | **No** | Results are exploratory, single-annotator, small sample. No formal gates met. |
| Should the heuristic baseline remain the reference? | **Yes** | Heuristic outperforms or matches all ML configs on LOAO mean when heuristic-derived features are removed. |
| Should v1.1.0 and v1.1.1 outputs be preserved? | **Yes** | All code, predictions, metrics, and reports preserved unchanged for reproducibility. |
| Should ML development continue on v1.1 data? | **No** | The dataset structure (6 repeating archetypes) cannot support reliable generalization assessment. |
| Should v1.2 be planned? | **Yes** | More diverse scenarios and stronger annotation provenance are needed before meaningful ML evaluation. |

---

### Unresolved Questions

1. Does the model learn any genuine farmer–scheme suitability relationships beyond memorizing the heuristic's need-to-scheme mapping? Cannot be determined from 6 archetypes.
2. Which non-heuristic features (if any) carry genuine signal for scheme suitability? Cannot be isolated with collinear `archetype_id`/`immediate_need`.
3. What sample size and scenario diversity would be needed for statistically valid generalization assessment? Requires a formal power/diversity analysis (see v1.2 design proposal).
4. Can annotation provenance be strengthened to support verified human ground truth? Requires independent reviewer collection (see v1.2 design proposal).

---

### Preservation Statement

All v1.1 artifacts are preserved unchanged:
- `src/models/benchmark_v1_1/ranker.py` — ML model code
- `scripts/train_exploratory_ranker_v1_1.py` — v1.1.0 training script
- `scripts/ablate_ml_ranker_v1_1.py` — v1.1.1 ablation script
- `data/benchmarks/v1.1/ml_experiment/` — all v1.1.0 and v1.1.1 outputs
- `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` — annotation file (preserved unchanged)
- `reports/benchmark_v1.1_ml_experiment.md` — v1.1.0 report
- `reports/benchmark_v1.1_feature_ablation.md` — v1.1.1 report
- `reports/benchmark_v1.1_ml_methodology_audit.md` — methodology audit
- `reports/benchmark_v1.1_annotation_readiness_audit.md` — annotation readiness audit
- `src/eligibility/engine.py` — frozen eligibility engine (unchanged)
- `reports/benchmark_v1.0.4_baseline_evaluation_report.md` — v1.0.4 baseline (unchanged)
- `research/dataset_research/evaluation_preregistration.md` — preregistered gates (unchanged)

Nothing has been committed or pushed.
