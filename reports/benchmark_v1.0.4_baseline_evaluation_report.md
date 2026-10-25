# Benchmark v1.0.4 Deterministic Heuristic Baseline Reference Evaluation Report

**Benchmark Version:** `v1.0.4`  
**Evaluation Standard:** Exponential NDCG@3 ($2^y - 1$), MRR (Threshold $\tau \ge 2$), Section A Candidates  
**Consensus Ground Truth:** `data/annotations/benchmark_v1.0.4/consensus_labels_final.csv`  
**Observation Unit:** 60 Scenarios ($N=60$), S011–S070 across 10 Agro-Climatic Zones  

---

## 1. Global Benchmark Performance Summary

| Metric | Reference Value | Description |
| :--- | :---: | :--- |
| **Global Mean NDCG@3** | **`0.9818`** | Ranking quality over top-3 positions (Ideal DCG normalized) |
| **Global Mean MRR** | **`0.6958`** | Mean Reciprocal Rank at first relevant hit ($y \ge 2$) |
| **Total Evaluated Scenarios** | `60` | Complete S011–S070 coverage |
| **Total Candidates Evaluated** | `283` | All Section A schemes evaluated |

---

## 2. Agro-Climatic Zone Breakdown (Z1–Z10)

| Zone ID | Agro-Climatic Zone Name | Scenarios | Mean NDCG@3 | Mean MRR |
| :---: | :--- | :---: | :---: | :---: |
| **Z1** | North Eastern Transition Zone | 6 | `0.9898` | `1.0000` |
| **Z2** | North Eastern Dry Zone | 6 | `1.0000` | `0.6667` |
| **Z3** | Northern Dry Zone | 6 | `1.0000` | `0.6667` |
| **Z4** | Central Dry Zone | 6 | `0.8939` | `0.7083` |
| **Z5** | Eastern Dry Zone | 6 | `1.0000` | `1.0000` |
| **Z6** | Southern Dry Zone | 6 | `1.0000` | `0.5000` |
| **Z7** | Southern Transition Zone | 6 | `1.0000` | `0.6667` |
| **Z8** | Northern Transition Zone | 6 | `0.9500` | `0.9167` |
| **Z9** | Hilly Zone | 6 | `1.0000` | `0.5000` |
| **Z10** | Coastal Zone | 6 | `0.9840` | `0.3333` |

---

## 3. Pre-Registered Model Acceptance Implications

Under the pre-registered evaluation standards (`research/dataset_research/evaluation_preregistration.md`):

1. **Substantive Gain Criterion:** A trained ML model must achieve $\Delta \overline{\text{NDCG@3}} \ge +0.050$.

   - Since Baseline Mean NDCG@3 = `0.9818`, achieving a +0.050 gain requires an NDCG@3 of **`1.0318`**, which exceeds the theoretical upper limit of 1.0000.
   - This mathematically demonstrates that the deterministic rule-based baseline is near-optimal on the frozen Section A candidate sets.
2. **Zone Non-Regression:** Any candidate model must not regress in any zone ($\Delta \text{NDCG@3}_z \ge 0.000$).
3. **Conclusion:** The deterministic baseline provides an exceptionally rigorous reference standard for the subsidy recommendation engine.
