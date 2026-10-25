# Candidate-Set Design & Heuristic Baseline Mechanism Audit

**Document:** `benchmark_v1.0.4_candidate_set_audit.md`  
**Milestone:** Phase 5 Evaluation Design Review & Architectural Retrospective  
**Date:** October 2026  
**Status:** Completed & Committed  

---

## 1. Executive Summary: The Candidate-Set Mechanism

This audit investigates **why** the deterministic heuristic baseline achieves a near-ceiling mean NDCG@3 of **0.9818** on Benchmark v1.0.4-EXP, and evaluates whether this reflects genuine baseline sufficiency or candidate-selection artifacts.

### Key Finding:
The near-perfect baseline performance is driven by the structural interaction between two architectural design choices:
1. **Aggressive Upstream Statutory Filtering:** The statutory eligibility engine reduces the full catalog of 16 schemes down to an average of **4.72 candidates per scenario** (min 2, max 7).
2. **Single-Need Archetype Construction:** Each benchmark scenario was authored with an explicit, singular `immediate_need` designed to test a specific statutory boundary.

Together, these choices produce **low-entropy candidate sets**:
- In **63.3% of scenarios** (38/60), the primary target scheme is present in a 4-item pool and easily identified by a 1-rule lookup.
- In **36.7% of scenarios** (22/60), the scenario serves as a negative boundary test (the primary target was statutorily disqualified or decoupled to Section B), leaving only generic statutory schemes (scores 0 or 1), where any plausible ordering achieves NDCG@3 near 1.0.

---

## 2. Quantitative Candidate-Set Composition

### Candidate Set Size Distribution ($N=60$ Scenarios)
Out of 16 total scheme implementations in the Karnataka registry:

| Section A Candidate Count | Scenario Count | Percentage | Cumulative |
| :---: | :---: | :---: | :---: |
| **2 candidates** | 4 | 6.7% | 6.7% |
| **3 candidates** | 4 | 6.7% | 13.3% |
| **4 candidates** | 12 | 20.0% | 33.3% |
| **5 candidates** | 26 | 43.3% | 76.7% |
| **6 candidates** | 13 | 21.7% | 98.3% |
| **7 candidates** | 1 | 1.7% | 100.0% |

- **Mean candidate pool size:** $4.72 \pm 1.07$ schemes.
- Over **76% of scenarios** present 5 or fewer candidates to the ranker.

---

## 3. Dissecting the Two Candidate-Set Regimes

### Regime 1: Positive Target Scenarios (38 / 60 scenarios, 63.3%)
- **Condition:** The farmer’s primary statutory scheme passes deterministic eligibility and enters Section A.
- **Examples:**
  - `SOLAR_PUMP_INSTALLATION` on off-grid borewell $\rightarrow$ `SCH006` (PM-KUSUM B) is the sole solar scheme.
  - `FARM_MECHANIZATION` $\rightarrow$ `SCH004` (SMAM) is the sole machinery scheme.
  - `RAINWATER_HARVESTING` $\rightarrow$ `SCH005` (Krishi Bhagya) is the sole farm pond scheme.
  - `PROTECTED_HORTICULTURE` $\rightarrow$ `SCH007` (MIDH) is the sole polyhouse/shade-net scheme.
- **Ranker Task:** The ranker must select 1 obvious match out of 4 candidates. A static 1-line lookup accomplishes this with 100% precision, resulting in **NDCG@3 = 1.0000**.

### Regime 2: Negative Boundary Scenarios (22 / 60 scenarios, 36.7%)
- **Condition:** The primary statutory scheme was disqualified by the eligibility engine (e.g. tax paying disqualification, existing borewell exclusion, pure tenancy) or decoupled to Section B (e.g. PMFBY crop insurance pending seasonal notification).
- **Candidates Present:** Only secondary or universal support schemes remain (`SCH001` PM-KISAN, `SCH008_CENTRAL` KCC-MISS, `SCH009` Soil Health Card, or unrequested capital works).
- **Consensus Label Distribution:** The highest consensus label in the candidate set is only $y=1$ (or $y=2$ for cash liquidity).
- **Metric Consequence:** When the ground-truth scores are $[1, 1, 0, 0]$, any ranking that places the two score-1 items in the top 3 achieves an **ideal DCG@3 normalization**, yielding **NDCG@3 = 1.0000**.
- **Result:** The heuristic baseline achieves perfect NDCG@3 even when no highly relevant ($y=3$) scheme exists in the pool.

---

## 4. Synthesis: Scope of the Research Claim

The audit justifies the following refined scientific conclusion:

> **Formal Research Finding:**  
> In exploratory feasibility testing across 60 single-need farmer scenarios and their curated Section A candidate sets, a deterministic eligibility-and-ranking pipeline achieved a reported mean NDCG@3 of 0.9818. This near-ceiling result made the pre-registered minimum improvement of 0.05 unattainable for the tested baseline. The finding motivates further investigation of candidate-set construction and the conditions under which learned ranking provides incremental value; it does not establish general redundancy of machine learning for government-scheme recommendation.

### Boundary Conditions Limiting Generalization:
1. **Curated Candidate Size:** In production deployments with hundreds of state, central, and district welfare schemes, candidate sets will be larger, increasing ambiguity.
2. **Single vs. Compound Farmer Needs:** Real farmers frequently present overlapping, competing needs (e.g., debt distress + borewell failure + pest loss simultaneously), where deterministic 1-to-1 lookups fail to optimize trade-offs.
3. **Exploratory Label Provenance:** Results reflect feasibility dataset `v1.0.4-EXP` and await formal validation against independent human annotations.
