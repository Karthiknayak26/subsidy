# Benchmark v1.2 Evaluation Pre-Registration

**Repository:** `farmer-benefit-ml`  
**Document Version:** `preregistration-v1.2`  
**Status:** Approved (research-team approval documented 2026-10-28)  
**Benchmark Target:** Benchmark v1.2 (S131+, N TBD — diversity-driven, not fixed at 60)  
**Date:** October 2026  
**Relation to v1.1 preregistration:** This document is separate from `preregistration-v1.0`, which remains frozen and applies only to Benchmark v1.0.4 scenarios (S011–S070). The v1.1 gates (ΔNDCG@3 ≥ +0.050, p < 0.050, zone non-regression) are NOT applied to v1.2.

---

## 1. Executive Summary & Purpose

This document formally pre-registers all evaluation metrics, mathematical formulations, edge-case conventions, statistical hypothesis test procedures, and model acceptance criteria for Benchmark v1.2.

All evaluation parameters defined herein are permanently locked prior to the inspection, adjudication, or unblinding of expert relevance labels for v1.2 scenarios. No thresholds, metrics, or acceptance criteria may be altered after v1.2 labels are collected or examined.

---

## 2. Benchmark Scope & Frozen Invariants

### 2.1 Evaluation Set

The benchmark consists of v1.2 scenarios generated through the frozen eligibility engine. The exact scenario count (N) and scenario IDs are not fixed at preregistration time; they will be determined by the diversity audit in Section 3.3 of the v1.2 design proposal. The joint distribution of (crop × land tenure × water access × primary crisis × electricity access) must be reported before scenario finalization.

### 2.2 Section A Numerical Scoring Boundary

Only schemes determined as **Section A** (`presentation_section == "SECTION_A"` and `allow_numerical_scoring == True`) by the frozen eligibility engine are eligible for relevance scoring ($y \in \{0, 1, 2, 3\}$).

### 2.3 Section B Provisional Exclusion

Schemes classified under **Section B** remain strictly score-disabled ($y$ is undefined). They are never scored, ranked, or penalized in numerical evaluation.

---

## 3. Mathematical Metric Formulations & Edge Case Conventions

### 3.1 Normalized Discounted Cumulative Gain at Cutoff 3 (NDCG@3)

The primary ranking metric is **NDCG@3** using standard exponential relevance gain and logarithmic position discounting:

$$\text{DCG}@3 = \sum_{i=1}^{\min(3, K)} \frac{2^{y_{(i)}} - 1}{\log_2(i + 1)}$$

where:
- $K$ is the number of Section A actionable candidate schemes for the scenario.
- $y_{(i)} \in \{0, 1, 2, 3\}$ is the ground truth consensus relevance score of the scheme placed at rank position $i$ by the ranking system under evaluation.
- $\log_2(i + 1)$ is the position discount factor.

The Ideal Discounted Cumulative Gain ($\text{IDCG}@3$) is computed by sorting all candidate scores in descending order:

$$\text{IDCG}@3 = \sum_{i=1}^{\min(3, K)} \frac{2^{y^*_{(i)}} - 1}{\log_2(i + 1)}$$

The scenario NDCG@3 is defined as:

$$\text{NDCG}@3 = \begin{cases} \frac{\text{DCG}@3}{\text{IDCG}@3} & \text{if } \text{IDCG}@3 > 0 \\ 0.0 & \text{if } \text{IDCG}@3 = 0 \end{cases}$$

**Edge Case Conventions:**
- **Edge Case 1 (All Irrelevant):** If every actionable scheme in Section A for a scenario receives score 0, $\text{IDCG}@3 = 0$. By convention, $\text{NDCG}@3 \equiv 0.0$.
- **Edge Case 2 (Short Lists):** If a scenario has fewer than 3 actionable candidates in Section A, DCG and IDCG are summed over all $K$ candidates ($i=1 \dots K$).

### 3.2 Mean Reciprocal Rank (MRR)

**RR** = $\frac{1}{r^*}$ if $\exists i \in \{1 \dots K\}$ such that $y_{(i)} \ge \tau$; otherwise **RR** = 0.0.

where:
- $r^*$ is the minimum rank index ($1 \le r^* \le K$) where the retrieved scheme achieves relevance score $y_{(r^*)} \ge \tau$.
- **Pre-Registered Relevance Threshold ($\tau$):** $\tau \equiv 2$ (a scheme must be rated at least `Relevant / Secondary Priority` ($y=2$) or `Highly Relevant` ($y=3$) to qualify as a successful hit).
- **Edge Case 3 (No Hit):** If no candidate in the top-K ranking reaches $y \ge 2$, $\text{RR} \equiv 0.0$.

---

## 4. Exact Statistical Hypothesis Testing Specification

### 4.1 Observation Unit

The observation unit is the individual farmer scenario query. Individual candidate scheme ratings are **not** independent and must never be treated as degrees of freedom.

### 4.2 Paired Metric Difference

For each scenario $s$, compute the paired difference:

$$d_s = \text{NDCG@3}_{\text{model}}(s) - \text{NDCG@3}_{\text{baseline}}(s)$$

### 4.3 Statistical Test Procedure

A **two-sided paired permutation test** (randomization test) on scenario differences:

- **Null Hypothesis ($H_0$):** The distribution of scenario metric differences $d_s$ is symmetric about zero.
- **Alternative Hypothesis ($H_1$):** The mean scenario metric difference $\bar{d} \ne 0$.
- **Test Statistic:** $T_{\text{obs}} = |\bar{d}| = \left| \frac{1}{N} \sum_{s=1}^N d_s \right|$.
- **Permutation Procedure:** Conduct $B = 10,000$ Monte Carlo resamplings where each paired difference $d_s$ is independently multiplied by a Rademacher sign variable $c_s \in \{-1, +1\}$ with equal probability ($P(c_s = 1) = 0.5$).
- **Permutation p-value:** $p = \frac{1 + \sum_{b=1}^B \mathbb{I}\left( |T^{(b)}| \ge T_{\text{obs}} \right)}{B + 1}$
- **Significance Threshold:** Two-sided $\alpha = 0.05$. The gain is statistically significant if $p < 0.05$.

---

## 5. Grouping Strategy & Data Leakage Controls

### 5.1 Evaluation Splits

The following splits are pre-registered for v1.2:

| Split Type | Description | Purpose |
|------------|-------------|---------|
| Scenario-level holdout | Hold out 20% of scenarios (not archetypes) | Test generalization to unseen scenario instances |
| Crisis-type holdout | Hold out all scenarios of one primary crisis type | Test generalization to unseen crisis types |
| Land-tenure holdout | Hold out all tenant scenarios | Test generalization to unseen tenure types |
| Zone-level | Leave-one-zone-out (Z1–Z10) | Test regional generalization |

### 5.2 Data-Leakage Safeguards

- **Feature set fixed before labels collected:** No feature may be added, removed, or modified after v1.2 annotation labels are available.
- **No heuristic-derived features:** `immediate_need_matches_heuristic_primary` and `archetype_id` are excluded from the primary model.
- **Permitted farmer-context features:** `immediate_need` (text or structured) is permitted as legitimate farmer context.
- **Preprocessing fit scope:** Preprocessing, categorical encodings, and scaling parameters must be fitted strictly on training folds.
- **Unseen categories:** OneHotEncoder(handle_unknown="ignore") for unseen categories in test folds.
- **Scenario-grouped CV:** All candidates from one scenario stay in the same fold.

---

## 6. Pre-Registered Model Acceptance Criteria

**These criteria are v1.2-specific and are distinct from the v1.1 preregistered gates (which apply only to v1.0.4 scenarios S011–S070).**

A machine learning ranking model will be considered superior to the deterministic heuristic baseline for Benchmark v1.2 **if and only if** it satisfies all of the following conditions simultaneously:

1. **Substantive Global Gain:** $\Delta \overline{\text{NDCG@3}} = \overline{\text{NDCG@3}}_{\text{model}} - \overline{\text{NDCG@3}}_{\text{baseline}} \ge \delta_{\text{min}}$, where $\delta_{\text{min}}$ is a v1.2-specific threshold to be defined in this preregistration before label collection. **The v1.1 threshold of +0.050 is NOT automatically carried forward to v1.2.**

2. **Statistical Significance:** Two-sided paired permutation test $p < \alpha$, where $\alpha$ is a v1.2-specific threshold to be defined before label collection. **The v1.1 threshold of p < 0.050 is NOT automatically carried forward to v1.2.**

3. **Zone-Level Non-Regression (if applicable):** For every individual zone $z$ with sufficient scenarios for statistical power, the zone-level mean NDCG@3 difference must be non-negative: $\Delta \overline{\text{NDCG@3}}_z \ge 0.000$.

**Assumptions behind proposed numeric criteria:** No numeric thresholds are set in this preregistration. The research team must define $\delta_{\text{min}}$ and $\alpha$ before v1.2 label collection, with explicit justification for each value. No thresholds may be inferred from v1.1 results or from pilot examination of v1.2 labels.

---

## 7. Feature-Ablation Comparisons (Preregistered)

The following feature-set ablations are pre-registered for v1.2:

- **Ablation 1 (primary model):** Include `immediate_need` as legitimate farmer context; exclude `immediate_need_matches_heuristic_primary` and `archetype_id`.
- **Ablation 2 (sensitivity):** Same as Ablation 1 but without `immediate_need`.
- Compare LOAO results on held-out crisis types between Ablation 1 and Ablation 2.
- Compare both against the deterministic heuristic baseline on identical candidate sets, scenarios, labels, and metrics.

---

## 8. Execution Sequence & Enforcement Gate

```
[1. v1.2 Design Review Complete]  <── (Current Gate: NO-GO pending research-team approval)
         │
         ▼
[2. v1.2 Pre-Registration Filed]  <── (This document; requires research-team approval)
         │
         ▼
[3. Scenario Generation via Eligibility Engine]
         │
         ▼
[4. Diversity Audit Completed]
         │
         ▼
[5. Independent E1 & E2 Human Ratings Collection]
         │
         ▼
[6. Raw Data Validation & Archive (Section B score-disabled)]
         │
         ▼
[7. Inter-Annotator Agreement Assessment (Kappa >= 0.61, Alpha >= 0.67)]
         │
         ▼
[8. Disagreement Adjudication (|E1 - E2| >= 2) & Consensus Label Freeze]
         │
         ▼
[9. Evaluate Deterministic Baseline under v1.2 Pre-Registered Metrics]
         │
         ▼
[10. Learned Ranker Evaluation vs. v1.2 Acceptance Criteria]
```

---

## 9. Preservation Statement

All v1.1 artifacts preserved unchanged:
- `src/models/benchmark_v1_1/ranker.py` — ML model code
- `scripts/train_exploratory_ranker_v1_1.py` — v1.1.0 training script
- `scripts/ablate_ml_ranker_v1_1.py` — v1.1.1 ablation script
- `data/benchmarks/v1.1/ml_experiment/` — all v1.1.0 and v1.1.1 outputs
- `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` — annotation file
- `src/eligibility/engine.py` — frozen eligibility engine
- `research/dataset_research/evaluation_preregistration.md` — v1.1 preregistered gates (frozen, applies only to v1.0.4 scenarios S011–S070)

Nothing has been committed or pushed. v1.2 pre-registration is a proposal only; no implementation has begun.

**Release gate: NO-GO** — pending research-team approval of this v1.2 pre-registration document, including acceptance criteria thresholds ($\delta_{\text{min}}$ and $\alpha$) and the single-annotator deviation process.
