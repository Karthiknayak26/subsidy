# Formal Statistical & Metric Pre-Registration Specification

**Document Version:** `preregistration-v1.0`  
**Status:** Frozen & Approved Prior to Expert Label Inspection  
**Benchmark Target:** Benchmark v1.0.4 (`S011`–`S070`, $N=60$ scenarios)  
**Calibration Partition:** Pilot `S001`–`S010` (held strictly separate)  
**Date:** October 2026  

---

## 1. Executive Summary & Purpose

This document formally pre-registers all evaluation metrics, mathematical formulations, edge-case conventions, statistical hypothesis test procedures, and model acceptance gates for the **Karnataka Agricultural Welfare Subsidy & Benefit Discovery Engine**.

In accordance with scientific best practice in machine learning and information retrieval, all evaluation parameters defined herein are permanently locked prior to the inspection, adjudication, or unblinding of expert relevance labels for scenarios `S011`–`S070`.

---

## 2. Benchmark Scope & Frozen Invariants

1. **Evaluation Set ($N=60$):**
   The benchmark consists strictly of the 60 continuous scenarios `S011`–`S070` across the 10 Karnataka Agro-Climatic Zones ($Z1$–$Z10$, 6 scenarios per zone).
2. **Calibration Pilot Exclusion:**
   Pilot scenarios `S001`–`S010` are permanently reserved as calibration/training development fixtures and must never be blended into test evaluations.
3. **Section A Numerical Scoring Boundary:**
   Only schemes determined as **Section A** (`presentation_section == "SECTION_A"` and `allow_numerical_scoring == True`) are eligible for relevance scoring ($y \in \{0, 1, 2, 3\}$).
4. **Section B Provisional Exclusion:**
   Schemes classified under **Section B** (e.g. `SCH008_KA_COOP`, `SCH010_VALMIKI` in S056, PMFBY Seasonal IU reviews) remain strictly score-disabled ($y$ is undefined). They are never scored, ranked, or penalized in numerical evaluation.

---

## 3. Mathematical Metric Formulations & Edge Case Conventions

### 3.1 Normalized Discounted Cumulative Gain at Cutoff 3 (NDCG@3)

The primary ranking metric is **NDCG@3** using standard exponential relevance gain and logarithmic position discounting:

$$\text{DCG}@3 = \sum_{i=1}^{\min(3, K)} \frac{2^{y_{(i)}} - 1}{\log_2(i + 1)}$$

where:
- $K$ is the number of Section A actionable candidate schemes for the scenario.
- $y_{(i)} \in \{0, 1, 2, 3\}$ is the ground truth consensus relevance score of the scheme placed at rank position $i$ by the ranking system under evaluation.
- $\log_2(i + 1)$ is the position discount factor (for $i=1$, discount is $\log_2(2) = 1.0$; for $i=2$, $\log_2(3) \approx 1.585$; for $i=3$, $\log_2(4) = 2.0$).

The Ideal Discounted Cumulative Gain ($\text{IDCG}@3$) is computed by sorting all candidate scores in descending order ($y^*_{(1)} \ge y^*_{(2)} \ge \dots \ge y^*_{(K)}$):

$$\text{IDCG}@3 = \sum_{i=1}^{\min(3, K)} \frac{2^{y^*_{(i)}} - 1}{\log_2(i + 1)}$$

The scenario NDCG@3 is defined as:

$$\text{NDCG}@3 = \begin{cases} \frac{\text{DCG}@3}{\text{IDCG}@3} & \text{if } \text{IDCG}@3 > 0 \\ 0.0 & \text{if } \text{IDCG}@3 = 0 \end{cases}$$

#### Pre-Registered Edge Case Conventions for NDCG@3:
- **Edge Case 1 (All Irrelevant, $\text{IDCG}@3 = 0$):** If every actionable scheme in Section A for a scenario receives score $0$, $\text{IDCG}@3 = 0$. By pre-registered convention, **$\text{NDCG}@3 \equiv 0.0$** (not undefined, and not $1.0$).
- **Edge Case 2 (Short Lists, $K < 3$):** If a scenario has fewer than 3 actionable candidates in Section A, DCG and IDCG are summed over all $K$ candidates ($i=1 \dots K$).

---

### 3.2 Mean Reciprocal Rank (MRR)

Mean Reciprocal Rank evaluates the system's ability to place at least one genuinely relevant scheme at the top of the recommendation list:

$$\text{RR} = \begin{cases} \frac{1}{r^*} & \text{if } \exists i \in \{1 \dots K\} \text{ such that } y_{(i)} \ge \tau \\ 0.0 & \text{otherwise} \end{cases}$$

where:
- $r^*$ is the minimum rank index ($1 \le r^* \le K$) where the retrieved scheme achieves relevance score $y_{(r^*)} \ge \tau$.
- **Pre-Registered Relevance Threshold ($\tau$):** **$\tau \equiv 2$** (a scheme must be rated at least `Relevant / Secondary Priority` ($y=2$) or `Highly Relevant` ($y=3$) to qualify as a successful hit).
- **Edge Case 3 (No Hit):** If no candidate in the top-K ranking reaches $y \ge 2$, **$\text{RR} \equiv 0.0$**.

---

## 4. Exact Statistical Hypothesis Testing Specification

To determine whether a learned model provides a statistically significant improvement over the deterministic heuristic baseline:

1. **Observation Unit:**
   The observation unit is the individual farmer scenario query ($s \in \{S011, \dots, S070\}$, sample size $N=60$). Individual candidate scheme ratings ($N=283$) are **not** independent and must never be treated as degrees of freedom.
2. **Paired Metric Difference:**
   For each scenario $s$, compute the paired difference:
   $$d_s = \text{NDCG@3}_{\text{model}}(s) - \text{NDCG@3}_{\text{baseline}}(s)$$
3. **Statistical Test Procedure:**
   A **two-sided paired permutation test** (randomization test) on scenario differences:
   - **Null Hypothesis ($H_0$):** The distribution of scenario metric differences $d_s$ is symmetric about zero (the model and baseline have identical ranking quality).
   - **Alternative Hypothesis ($H_1$):** The mean scenario metric difference $\bar{d} \ne 0$.
   - **Test Statistic:** $T_{\text{obs}} = |\bar{d}| = \left| \frac{1}{N} \sum_{s=1}^N d_s \right|$.
   - **Permutation Procedure:** Conduct $B = 10,000$ Monte Carlo resamplings where each paired difference $d_s$ is independently multiplied by a Rademacher sign variable $c_s \in \{-1, +1\}$ with equal probability ($P(c_s = 1) = 0.5$).
   - **Permutation p-value:**
     $$p = \frac{1 + \sum_{b=1}^B \mathbb{I}\left( |T^{(b)}| \ge T_{\text{obs}} \right)}{B + 1}$$
4. **Significance Threshold:** Two-sided $\alpha = 0.05$. The gain is statistically significant if $p < 0.05$.

---

## 5. Grouping Strategy & Data Leakage Controls

### 5.1 Primary Cross-Validation Strategy: Template-Grouped K-Fold
To prevent data leakage caused by agrarian archetypes sharing similar parameter templates:
- All scenarios originating from the same structural profile archetype or need template are assigned to the same fold.
- Folds are balanced across agro-climatic zones so that training and validation distributions retain representative regional diversity.
- Feature preprocessing, categorical encodings, and scaling parameters must be fitted strictly on training folds.

### 5.2 Out-of-Domain Generalization: Leave-One-Zone-Out (LOZO)
In addition to template-grouped cross-validation, the model must be evaluated on Leave-One-Zone-Out (LOZO) splits across all 10 zones ($Z1$ through $Z10$), where each zone ($N=6$ scenarios) serves as an unseen held-out regional test set.

---

## 6. Pre-Registered Model Acceptance Criteria

A machine learning ranking model will be considered superior to the deterministic baseline and approved for deployment **if and only if** it satisfies all three of the following conditions simultaneously:

1. **Substantive Global Gain:**
   $$\Delta \overline{\text{NDCG@3}} = \overline{\text{NDCG@3}}_{\text{model}} - \overline{\text{NDCG@3}}_{\text{baseline}} \ge +0.050$$
2. **Statistical Significance:**
   Two-sided paired permutation test $p < 0.050$ ($B = 10,000$ permutations).
3. **Strict Zone-Level Non-Regression:**
   For every individual agro-climatic zone $z \in \{Z1, Z2, \dots, Z10\}$, the zone-level mean NDCG@3 difference must be non-negative:
   $$\Delta \overline{\text{NDCG@3}}_z = \overline{\text{NDCG@3}}_{\text{model}, z} - \overline{\text{NDCG@3}}_{\text{baseline}, z} \ge 0.000 \quad \forall z \in \{1 \dots 10\}$$
   A model that achieves global $+0.05$ gain by improving 8 zones but regressing in 2 zones is strictly rejected.

---

## 7. Execution Sequence & Enforcement Gate

```
[Packet Staging: commit fe6bfd6]
         │
         ▼
[Statistical Pre-Registration: preregistration-v1.0]  <── (Current Gate: LOCKED)
         │
         ▼
[Independent E1 & E2 Human Ratings Collection]
         │
         ▼
[Raw Data Validation & Archive (283 rows each, Section B score-disabled)]
         │
         ▼
[Inter-Annotator Agreement Assessment (Kappa >= 0.61, Alpha >= 0.67)]
         │
         ▼
[Disagreement Adjudication (|E1 - E2| >= 2) & Consensus Label Freeze]
         │
         ▼
[Evaluate Deterministic Baseline under Pre-Registered Metrics]
         │
         ▼
[Learned Ranker Exploration vs. Acceptance Gate (+0.05 gain, p < 0.05, no zone regressions)]
```
