# Expert Annotation Protocol Specification — Version 1.1

**Protocol Version:** `annotation-protocol-v1.1`  
**Supersedes:** `pilot-v1.0` (commit `7724fa7`)  
**Status:** Approved for 50–100 Scenario Benchmark Expansion  
**Date:** October 2026  
**Target Domain:** Karnataka Agricultural Welfare Subsidy & Benefit Discovery Engine  

---

## 1. Executive Context & Evolution

During the 10-scenario initial pilot calibration (`pilot-v1.0`), independent expert raters (E1 and E2) completed 63 paired scheme determinations across 10 diverse farmer scenarios, achieving:
- **Quadratic Weighted Cohen's Kappa:** $\kappa_w = 0.8306$ (Target $\ge 0.61$)
- **Ordinal Krippendorff's Alpha:** $\alpha = 0.8311$ (Target $\ge 0.67$)
- **Exact Agreement:** $88.9\%$ | **Adjacent Agreement ($|\Delta| \le 1$):** $96.8\%$
- **Investigated Disagreements ($|\Delta| \ge 2$):** 2 cases

The quantitative agreement confirmed protocol clarity, but qualitative investigation of the 2 boundary disagreements revealed two specific ambiguities in the original relevance rubric. Protocol version 1.1 incorporates these calibrated rules to ensure maximum label quality across the expanded 50–100 scenario benchmark.

> [!IMPORTANT]
> **Data Boundary Safeguard:**
> The original 10 pilot scenarios (S001–S010) are permanently designated as **Pilot Calibration Data**. They must not be blended into the held-out test evaluation set of the upcoming 50–100 benchmark.

---

## 2. Calibrated Relevance Scoring Rubric (0–3 Scale)

Each scheme in **Section A** (passing deterministic eligibility) is evaluated on a 0–3 ordinal scale based on the farmer's stated need, crop, and asset profile:

| Score | Rating Level | Definition & Clinical Criteria |
|:---:|:---|:---|
| **3** | **Highly Relevant / High Priority** | Directly solves the farmer's primary stated need with immediate, high-impact practical benefit. Should appear in the top-3 recommendation cards. |
| **2** | **Relevant / Secondary Priority** | Provides genuine practical benefit and valuable secondary support, but does not directly resolve the immediate acute crisis. |
| **1** | **Marginally Relevant / Low Priority** | Technically applicable and statutory criteria satisfied, but provides minor, distant, or tangential value in the current context. |
| **0** | **Irrelevant / Not Useful** | Despite passing statutory eligibility rules, the scheme provides no meaningful practical benefit given the farmer's specific asset profile, crop, or situation. |

---

## 3. Protocol Refinement Rules (New in v1.1)

### Rule 1: Infrastructure, Civil Works & Implementation Complexity
*Derived from S002 disagreement (Krishi Bhagya vs. Standalone Solar Pump).*

- **Finding:** A package scheme may contain a relevant sub-component (e.g. pump lifting unit) while requiring large unrequested physical assets (e.g. digging a farm pond on rainfed land).
- **Calibrated Rule:**
  - A scheme must **not** be scored high solely because it contains an eligible sub-component.
  - When obtaining the desired component requires major unrequested civil works, extensive infrastructure excavation, or co-dependencies that reduce practical usability for the farmer's stated situation, annotators must score the scheme as **Marginal (`1`)** or **Irrelevant (`0`)** depending on the severity of the barrier.
  - *Note:* This is **not** an automatic score penalty based solely on another scheme's existence; rather, the penalty applies when the additional prerequisites genuinely reduce practical relevance for the farmer's stated request.

### Rule 2: Non-Repayable Income Relief vs. Working Capital Debt
*Derived from S007 disagreement (KCC Modified Interest Subvention vs. Income Support).*

- **Finding:** Conflating liquidity obtained through debt with non-repayable welfare assistance.
- **Calibrated Rule:**
  - Strict semantic distinction must be maintained between **`INCOME_SUPPORT`** (direct benefit transfers, non-repayable cash assistance like PM-KISAN) and **`PRODUCTION_CREDIT` / `WORKING_CAPITAL`** (repayable crop loans like KCC-MISS or PACS loans).
  - Credit and borrowing facilities must **not** receive score `3` (Highly Relevant) when the farmer's stated need is purely non-repayable income support (`INCOME_SUPPORT`), unless the query explicitly requests loan rescheduling, seasonal borrowing, or input working capital.

---

## 4. Handling Section B (Provisional Schemes)

Schemes classified by the eligibility engine as **`REQUIRES_VERIFICATION`** (such as `SCH008_KA_COOP` — Karnataka Zero-Interest PACS Crop Loan) are governed by the following rules:

1. **Strict Exclusion from Numerical Scoring:** Annotators must never assign numerical relevance scores (0–3) to Section B schemes.
2. **Qualitative Policy Review Only:** Annotators provide operational guidance on state Government Orders (GOs), district cooperative credit limit sanctions, and ground PACS membership rules.
3. **Deduplicated Policy Handling:** Multiple scenario reviews reflecting the same policy prerequisite are summarized as a unified operational finding rather than multiple statistical confirmations.
4. **User-Facing System Output:** Ground systems must render Section B schemes as conditional advisories prompting the farmer to verify local terms at the Raitha Samparka Kendra (RSK) or PACS society before assuming eligibility.

---

## 5. Architectural Quality Safeguards

1. **Two-Phase Availability Blinding:**
   - **Phase 1:** Relevance is scored with operational availability states hidden. Raters evaluate pure agronomic and policy fit.
   - **Phase 2:** Availability is revealed for operational commenting, ensuring ratings reflect permanent scheme merit rather than transient portal window closures.
2. **Machine Learning Model Deferral:**
   - Model training remains strictly blocked until the 50–100 scenario expansion is annotated, validated for multi-rater agreement ($\kappa_w \ge 0.61$, $\alpha \ge 0.67$), and evaluated against rule-based heuristic baselines.
