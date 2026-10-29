# Benchmark v1.1 Exploratory Ranking Evaluation Report

**Benchmark Version:** `v1.1` (S071–S130, N=60 scenarios)
**Evaluation Type:** Exploratory (NOT formal pre-registered evaluation)
**Model Evaluated:** Heuristic Baseline (need-to-scheme mapping)
**Labels Source:** `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` (single annotator)
**Metric Definitions:** Reused from `research/dataset_research/evaluation_preregistration.md`

## Blockers and Limitations

### Blocker 1: No ML Recommender Exists
The repository contains only a deterministic heuristic baseline (`src/models/heuristic_baseline.py`). No ML recommender, neural network, or learned ranker is implemented. The notebooks directories (`notebooks/05_baseline/`, `notebooks/06_ml_models/`) contain only `.gitkeep` files. Therefore, only heuristic baseline rankings are generated; there is no learned model to compare against.

### Blocker 2: Evaluation Infrastructure Frozen for v1.0.4 (S011–S070)
The pre-registered evaluation infrastructure is locked to Benchmark v1.0.4 scenarios (S011–S070):
- `src/evaluation/benchmark_candidates.py::FROZEN_BENCHMARK_SECTION_A_CANDIDATES` covers only S011–S070.
- `src/evaluation/metrics.py::evaluate_standalone_ranking_system()` strictly enforces S011–S070 scenario keys.
- `src/evaluation/metrics.py::FROZEN_BENCHMARK_ZONE_MAP` covers only S011–S070.
The annotation file covers v1.1 scenarios (S071–S130). The strict key enforcement in `evaluate_standalone_ranking_system` prevents its direct use for v1.1. Instead, the underlying metric functions (`compute_ndcg_at_k`, `compute_mrr`) are reused directly with v1.1 data.

### Blocker 3: No Separate Baseline for Comparison
Only one ranking model (heuristic baseline) is available. There is no separate recommender or baseline to compare against. The preregistered acceptance criteria (ΔNDCG@3 ≥ +0.050, paired permutation test p < 0.050, zone non-regression) require two systems and cannot be applied.

### Provenance Limitation: AI Practice File Match
All 269 relevance scores in `human_reviewer_annotations.csv` match an earlier AI practice file row-for-row. The quality-control report records this without assuming authorship. These scores are treated as a single-annotator dataset for exploratory purposes only and must NOT be presented as validated human ground truth or independent expert judgments.

### Single-Annotator Dataset
The annotation file has a single rater_id (`human reviewer`). No inter-rater reliability (Cohen's kappa, Krippendorff's alpha) is computed, as required for two independent human reviews.

## Validation Results

- Total annotation rows: 269
- Unique scenarios: 60 (S071–S130)
- Unique schemes: 7 (SCH001, SCH003, SCH004, SCH005, SCH008_CENTRAL, SCH009, SCH010_AMBEDKAR)
- Rater IDs: human reviewer
- Score values: 0, 1, 2, 3
- Duplicate (scenario_id, scheme_id) pairs: 0
- Missing relevance_score: 0
- Missing relevance_rationale: 0
- Validation errors: 0

## Ranking Validity Results

- Scenarios ranked: 60
- Scenarios not evaluated: 0
- Invalid scheme IDs in rankings: 0
- Duplicate rankings: 0
- Missing schemes from rankings: 0

## Exploratory Metric Results

- Global Mean NDCG@3: **0.7760**
- Global Mean MRR: **0.7833**
- Scenarios evaluated: 60

## Zone-Level Summary

| Zone | Zone Name | Scenarios | Mean NDCG@3 | Mean MRR |
|------|-----------|-----------|-------------|----------|
| Z1 | North Eastern Transition Zone | 6 | 0.7934 | 0.8333 |
| Z2 | North Eastern Dry Zone | 6 | 0.7934 | 0.8333 |
| Z3 | Northern Dry Zone | 6 | 0.8007 | 0.8333 |
| Z4 | Central Dry Zone | 6 | 0.7934 | 0.8333 |
| Z5 | Eastern Dry Zone | 6 | 0.7539 | 0.7083 |
| Z6 | Southern Dry Zone | 6 | 0.8146 | 0.8333 |
| Z7 | Southern Transition Zone | 6 | 0.6818 | 0.7083 |
| Z8 | Northern Transition Zone | 6 | 0.7934 | 0.8333 |
| Z9 | Hilly Zone | 6 | 0.7752 | 0.7083 |
| Z10 | Coastal Zone | 6 | 0.7598 | 0.7083 |

## Per-Scenario Results

| Scenario | Zone | District | Immediate Need | NDCG@3 | MRR |
|----------|------|----------|----------------|--------|-----|
| S071 | Z1 | Kalaburagi | SOLAR_PUMP_INSTALLATION | 0.7660 | 1.0000 |
| S072 | Z1 | Bidar | CROP_INSURANCE | 0.6291 | 0.5000 |
| S073 | Z1 | Kalaburagi | PROTECTED_HORTICULTURE | 0.6871 | 0.5000 |
| S074 | Z1 | Bidar | FARM_MECHANIZATION | 1.0000 | 1.0000 |
| S075 | Z1 | Kalaburagi | RAINWATER_HARVESTING | 0.8657 | 1.0000 |
| S076 | Z1 | Bidar | SOIL_HEALTH_AND_FERTILIZER | 0.8124 | 1.0000 |
| S077 | Z2 | Raichur | SOLAR_PUMP_INSTALLATION | 0.7660 | 1.0000 |
| S078 | Z2 | Kalaburagi | CROP_INSURANCE | 0.6291 | 0.5000 |
| S079 | Z2 | Yadgir | PROTECTED_HORTICULTURE | 0.6871 | 0.5000 |
| S080 | Z2 | Raichur | FARM_MECHANIZATION | 1.0000 | 1.0000 |
| S081 | Z2 | Kalaburagi | RAINWATER_HARVESTING | 0.8657 | 1.0000 |
| S082 | Z2 | Yadgir | SOIL_HEALTH_AND_FERTILIZER | 0.8124 | 1.0000 |
| S083 | Z3 | Koppal | SOLAR_PUMP_INSTALLATION | 0.7660 | 1.0000 |
| S084 | Z3 | Vijayapura | CROP_INSURANCE | 0.6291 | 0.5000 |
| S085 | Z3 | Bagalkot | PROTECTED_HORTICULTURE | 0.8146 | 0.5000 |
| S086 | Z3 | Gadag | FARM_MECHANIZATION | 1.0000 | 1.0000 |
| S087 | Z3 | Koppal | RAINWATER_HARVESTING | 0.7824 | 1.0000 |
| S088 | Z3 | Vijayapura | SOIL_HEALTH_AND_FERTILIZER | 0.8124 | 1.0000 |
| S089 | Z4 | Davanagere | SOLAR_PUMP_INSTALLATION | 0.7660 | 1.0000 |
| S090 | Z4 | Tumakuru | CROP_INSURANCE | 0.6291 | 0.5000 |
| S091 | Z4 | Chitradurga | PROTECTED_HORTICULTURE | 0.6871 | 0.5000 |
| S092 | Z4 | Davanagere | FARM_MECHANIZATION | 1.0000 | 1.0000 |
| S093 | Z4 | Tumakuru | RAINWATER_HARVESTING | 0.8657 | 1.0000 |
| S094 | Z4 | Chitradurga | SOIL_HEALTH_AND_FERTILIZER | 0.8124 | 1.0000 |
| S095 | Z5 | Chikkaballapura | SOLAR_PUMP_INSTALLATION | 1.0000 | 1.0000 |
| S096 | Z5 | Bengaluru Rural | CROP_INSURANCE | 0.6291 | 0.5000 |
| S097 | Z5 | Ramanagara | PROTECTED_HORTICULTURE | 0.6871 | 0.5000 |
| S098 | Z5 | Kolar | FARM_MECHANIZATION | 1.0000 | 1.0000 |
| S099 | Z5 | Chikkaballapura | RAINWATER_HARVESTING | 0.3948 | 0.2500 |
| S100 | Z5 | Bengaluru Rural | SOIL_HEALTH_AND_FERTILIZER | 0.8124 | 1.0000 |
| S101 | Z6 | Mandya | SOLAR_PUMP_INSTALLATION | 0.7660 | 1.0000 |
| S102 | Z6 | Mysuru | CROP_INSURANCE | 0.6291 | 0.5000 |
| S103 | Z6 | Chamarajanagar | PROTECTED_HORTICULTURE | 0.8146 | 0.5000 |
| S104 | Z6 | Mandya | FARM_MECHANIZATION | 1.0000 | 1.0000 |
| S105 | Z6 | Mysuru | RAINWATER_HARVESTING | 0.8657 | 1.0000 |
| S106 | Z6 | Chamarajanagar | SOIL_HEALTH_AND_FERTILIZER | 0.8124 | 1.0000 |
| S107 | Z7 | Shivamogga | SOLAR_PUMP_INSTALLATION | 0.4398 | 1.0000 |
| S108 | Z7 | Chikkamagaluru | CROP_INSURANCE | 0.6291 | 0.5000 |
| S109 | Z7 | Hassan | PROTECTED_HORTICULTURE | 0.8146 | 0.5000 |
| S110 | Z7 | Shivamogga | FARM_MECHANIZATION | 1.0000 | 1.0000 |
| S111 | Z7 | Chikkamagaluru | RAINWATER_HARVESTING | 0.3948 | 0.2500 |
| S112 | Z7 | Hassan | SOIL_HEALTH_AND_FERTILIZER | 0.8124 | 1.0000 |
| S113 | Z8 | Haveri | SOLAR_PUMP_INSTALLATION | 0.7660 | 1.0000 |
| S114 | Z8 | Dharwad | CROP_INSURANCE | 0.6291 | 0.5000 |
| S115 | Z8 | Belagavi | PROTECTED_HORTICULTURE | 0.6871 | 0.5000 |
| S116 | Z8 | Haveri | FARM_MECHANIZATION | 1.0000 | 1.0000 |
| S117 | Z8 | Dharwad | RAINWATER_HARVESTING | 0.8657 | 1.0000 |
| S118 | Z8 | Belagavi | SOIL_HEALTH_AND_FERTILIZER | 0.8124 | 1.0000 |
| S119 | Z9 | Kodagu | SOLAR_PUMP_INSTALLATION | 1.0000 | 1.0000 |
| S120 | Z9 | Chikkamagaluru | CROP_INSURANCE | 0.6291 | 0.5000 |
| S121 | Z9 | Uttara Kannada | PROTECTED_HORTICULTURE | 0.8146 | 0.5000 |
| S122 | Z9 | Kodagu | FARM_MECHANIZATION | 1.0000 | 1.0000 |
| S123 | Z9 | Chikkamagaluru | RAINWATER_HARVESTING | 0.3948 | 0.2500 |
| S124 | Z9 | Uttara Kannada | SOIL_HEALTH_AND_FERTILIZER | 0.8124 | 1.0000 |
| S125 | Z10 | Udupi | SOLAR_PUMP_INSTALLATION | 1.0000 | 1.0000 |
| S126 | Z10 | Uttara Kannada | CROP_INSURANCE | 0.6291 | 0.5000 |
| S127 | Z10 | Dakshina Kannada | PROTECTED_HORTICULTURE | 0.8146 | 0.5000 |
| S128 | Z10 | Udupi | FARM_MECHANIZATION | 1.0000 | 1.0000 |
| S129 | Z10 | Uttara Kannada | RAINWATER_HARVESTING | 0.3024 | 0.2500 |
| S130 | Z10 | Dakshina Kannada | SOIL_HEALTH_AND_FERTILIZER | 0.8124 | 1.0000 |

## Interpretation

- These are **exploratory** results on a single-annotator dataset.
- The heuristic baseline ranks schemes by need-to-scheme mapping with deterministic tie-breaking.
- NDCG@3 measures ranking quality at the top-3 cutoff using exponential relevance gain.
- MRR measures the reciprocal rank of the first scheme scored ≥ 2 (Relevant or Highly Relevant).
- No statistical significance testing is performed (requires two systems for comparison).
- The preregistered acceptance gates (ΔNDCG@3 ≥ +0.050, p < 0.050, zone non-regression) are NOT evaluated.

## Provenance and Reproducibility

- Annotation file: `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` (preserved unchanged)
- Predictions: `data/benchmarks/v1.1/exploratory_predictions_v1.1.0.json`
- Metrics: `data/benchmarks/v1.1/exploratory_metrics_v1.1.0.json`
- All scores match an earlier AI practice file (269/269). This limitation is disclosed and the results are treated as exploratory only.

---
*Generated by exploratory evaluation script. Not a formal pre-registered benchmark evaluation.*