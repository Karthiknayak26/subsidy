# Expert Annotation Pilot — Inter-Rater Agreement Report

**Pilot Version:** pilot-v1.0 (git commit: `7724fa7`)
**Experts:** E1, E2
**Scenarios:** S001–S010 (10 pilot scenarios)
**Total Section A (scenario, scheme) pairs rated:** 63

> [!NOTE]
> This report covers 10 pilot scenarios only. Ratings from the same
> scenarios are not fully independent observations. These results are
> **diagnostic evidence** to evaluate the annotation protocol, not a
> definitive inter-rater reliability claim.

---

## 1. Overall Agreement Metrics

### 1.1 Krippendorff's Alpha (Ordinal Distance, All Raters)

**alpha (ordinal) = 0.8311**

| Threshold | Interpretation |
|:---|:---|
| alpha >= 0.80 | Good reliability — proceed to larger benchmark |
| 0.67 <= alpha < 0.80 | Tentative reliability — review disagreements, revise protocol |
| alpha < 0.67 | Low reliability — do not use as training labels until resolved |

> [!TIP] Alpha >= 0.80: Good reliability. Proceed to scaling after reviewing disagreements.

### 1.2 Pairwise Quadratic Weighted Cohen's Kappa

| Rater Pair | Shared Pairs | kappa_w | Exact Agreement | Adjacent Agreement |
|:---|---:|---:|---:|---:|
| E1 vs E2 | 63 | 0.8306 | 88.9% | 96.8% |

> kappa_w interpretation: >= 0.81 = Almost Perfect, 0.61-0.80 = Substantial, 0.41-0.60 = Moderate, < 0.41 = Fair/Poor

---

## 2. Coverage

- Total unique (scenario, scheme) pairs across all experts: **63**
- Pairs rated by all 2 expert(s): **63**
- Pairs with missing scores (one or more experts did not rate): **0**

---

## 3. Disagreement Analysis

**Disagreements flagged** (score range >= 2 points): **2**

| Scenario | Scheme | Score Range | Per-Expert Scores | Priority |
|:---|:---|:---:|:---|:---|
| S002 | SCH005 | 2 | E1=2 | E2=0 | MEDIUM |
| S007 | SCH008_CENTRAL | 2 | E1=3 | E2=1 | MEDIUM |

### 3.1 Disagrement Investigation Prompts

For each HIGH/MEDIUM disagreement, review:
1. Did the experts interpret the farmer's *stated need* differently?
2. Did one expert use agronomic context the annotation form did not make explicit?
3. Is the scheme description in the annotation form ambiguous for this crop/district?
4. Is this a genuine difference in expert judgment, or a protocol ambiguity?

---

## 4. Per-Scenario Summary

| Scenario | Pairs Rated | Mean Score (all experts) | Std Dev | Max Range |
|:---|---:|---:|---:|---:|
| S001 | 7 | 1.64 | 0.72 | 1 |
| S002 | 8 | 1.50 | 0.94 | 2 |
| S003 | 6 | 1.75 | 0.72 | 1 |
| S004 | 6 | 1.83 | 0.69 | 0 |
| S005 | 7 | 1.93 | 0.70 | 1 |
| S006 | 6 | 1.75 | 0.72 | 1 |
| S007 | 5 | 1.20 | 0.87 | 2 |
| S008 | 7 | 1.43 | 0.73 | 0 |
| S009 | 6 | 1.33 | 0.75 | 0 |
| S010 | 5 | 1.50 | 0.50 | 1 |

---

## 5. Section B: Provisional Scheme Policy Feedback

The following qualitative feedback was collected for schemes with `REQUIRES_VERIFICATION` status.
These entries do **NOT** contribute to numerical agreement metrics.
*(Note: Per-scenario records are preserved in the raw session CSVs; below is the deduplicated synthesis grouped by scheme and policy issue to avoid treating repetitive entry as multiple independent confirmations).*

### Deduplicated Policy Summary: `SCH008_KA_COOP` (Karnataka Zero-Interest Crop Loan)

| Expert | Core Ground Finding | Ground Operational Requirement | Practical System Recommendation |
|:---|:---|:---|:---|
| **E1** | Lending window opens upon annual district DCCB target notifications (issued in April). | Farmer must hold active Primary Agricultural Credit Society (PACS) membership in their village jurisdiction. | Do **not** rank numerically. Present as conditional advisory with explicit prompt: *"Verify current PACS lending window & DCCB sanction limits at local society office."* |
| **E2** | Zero-interest benefit is vital for Karnataka farmers, but fund disbursement is strictly contingent on annual state budget Government Orders (GOs). | PACS secretaries require physical land RTC (Pahani) and no-dues certificate across commercial banks. | Provide non-committal guidance: direct farmer to verify whether current year interest subvention subsidy GO is notified before assuming 0% rate. |

---

## 6. Protocol Revision Recommendations (Protocol v1.1)

Based on the investigation of the two flagged disagreements (score range $\ge 2$), the following calibration rules are incorporated into **`annotation-protocol-v1.1`** before scaling to the 50–100 scenario expansion:

| # | Topic | Ground Finding | Revised Protocol Rule (v1.1) |
|:---|:---|:---|:---|
| 1 | **Infrastructure & Civil Works Complexity** | In S002, E1 scored Krishi Bhagya `2` (component match for pump lift), while E2 scored `0` (irrelevant because farmer requested standalone solar borewell pump without farm pond). | **Civil Works / Complexity Rule:** A scheme must not be scored high solely because it includes a useful sub-component. When obtaining the benefit requires major unrequested civil works, infrastructure excavation (e.g. farm pond), or co-dependencies that reduce practical usability, raters must score it as **Marginal (`1`)** or **Irrelevant (`0`)** depending on whether those preconditions represent an impractical barrier. |
| 2 | **Income Support vs. Operational Debt** | In S007, E1 scored KCC `3` (treating crop credit as liquidity during distress), while E2 scored `1` (noting credit adds repayment debt to a distressed farmer). | **Relief vs. Debt Distinction:** Distinguish non-repayable income transfers (`INCOME_SUPPORT`, e.g. PM-KISAN) from debt/credit facilities (`PRODUCTION_CREDIT` / `WORKING_CAPITAL`, e.g. KCC). Credit schemes must **not** receive score `3` (Highly Relevant) when the stated need is purely non-repayable income support unless the farmer explicitly requests loan/operational financing. |
| 3 | **Section B Provisional Boundary** | Both experts agreed that `SCH008_KA_COOP` cannot be statistically ranked without real-time state GO and DCCB target verification. | **Architectural Decoupling:** Maintain complete separation between deterministic eligibility, machine-learned relevance ranking (Section A), and provisional administrative advisories (Section B). Never collapse administrative contingencies into numeric training targets. |

---

## 7. Decision Gate

| Criterion | Metric Role | Required Threshold | Evaluated Result | Status |
|:---|:---|:---:|:---:|:---:|
| Quadratic weighted kappa | **Primary (2 raters)** | $\ge 0.61$ | $\kappa_w = 0.8306$ | **PASS** |
| Krippendorff's alpha (ordinal) | **Supplementary (2 raters)** | $\ge 0.67$ | $\alpha = 0.8311$ | **PASS** |
| Flagged Disagreements (spread $\ge 2$) | Protocol Calibration | All investigated | 2 investigated (S002, S007) | **[x] COMPLETED** |
| Section B Qualitative Policy Review | Policy Review | Reviewed & deduplicated | Grouped PACS/DCCB GO review | **[x] COMPLETED** |
| Protocol Revision Documentation | Scaling Precondition | Formally published | Protocol v1.1 rules defined | **[x] COMPLETED** |
| Model Training Deferral | Research Integrity | Strictly deferred | ML training blocked | **[x] COMPLETED** |

> **Decision Gate Rule:** Meeting statistical agreement thresholds confirms that annotation rubrics are sufficiently calibrated to expand from the 10-scenario pilot to the 50–100 scenario benchmark. It does not replace qualitative adjudication or allow premature model training.

---

## 8. Scaling Decision Record (Benchmark Expansion Approval)

- **Decision:** **APPROVED FOR 50–100 SCENARIO EXPANSION**
- **Effective Version:** `annotation-protocol-v1.1`
- **Data Boundary:** The 10 pilot scenarios (S001–S010) are permanently designated as **Pilot Calibration Data** and will not be mixed into future held-out test evaluation benchmarks.
- **Evidence Limitations Acknowledged:** 10 scenarios across 2 raters demonstrate protocol clarity and inter-rater calibration, but do not represent all 10 agro-climatic zones or complex multi-tenant boundary cases in Karnataka.
- **Next Milestone Actions:**
  1. Author 50–100 diverse, non-duplicative farmer scenario specifications covering diverse zones, tenancy structures, and social categories.
  2. Deploy `annotation-protocol-v1.1` guidelines to expert raters.
  3. Defer all ML model training until the expanded benchmark annotations are collected, audited, and benchmarked against simple rule baselines.
