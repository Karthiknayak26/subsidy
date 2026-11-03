# System Architecture & Technical Specifications

## Current Status: Implemented, Validated & Tested (329 Automated Tests Passing)

The **farmer-benefit-ml** recommendation platform operates on a decoupled **Two-Desk Triage / Four-Layer Architecture** designed to deliver personalized agricultural scheme recommendations while providing a mathematical guarantee against policy hallucination.

---

## 1. High-Level Architectural Diagram

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Farmer Profile Input                            │
│  - Location (District, Agro-Climatic Zone Z1-Z10)                      │
│  - Operational Landholding (Acres, Dryland/Rainfed, Irrigated)         │
│  - Crop Details (Primary Crop, Crop Category, Season)                  │
│  - Socio-Demographic (Social Category, Annual Income)                  │
│  - Operational Constraints (Borewell Status, Three-Phase Power, Need)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               LAYER 1: Deterministic Eligibility Engine                │
│                     (`src/eligibility/engine.py`)                      │
│  - Codified statutory rules from Official Gazettes & Govt Portals      │
│  - 16 Schemes (10 Core + 6 Implementation Routes)                      │
│  - Three-Valued Logic: ELIGIBLE / INELIGIBLE / REQUIRES_VERIFICATION   │
│  - Hard Constraints: Land caps, caste corporations, tax disqualifier   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
┌───────────────────────────────────┐ ┌───────────────────────────────────┐
│       Disqualified Schemes        │ │        Eligible Candidates        │
│  - Full audit trail               │ │  (Passes all statutory criteria)  │
│  - Exact fired rule keys reported │ └─────────────────┬─────────────────┘
└───────────────────────────────────┘                   │
                                                        ▼
┌────────────────────────────────────────────────────────────────────────┐
│               LAYER 2: Operational Availability Filter                 │
│                     (`src/availability/`)                             │
│  - 4-State Filter: AVAILABLE_NOW / TIMING_PENDING / VERIFY / CLOSED    │
│  - Section A (Actionable): Ready for immediate submission              │
│  - Section B (Provisional/Seasonal): Quarantined from numerical ranks  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
┌───────────────────────────────────┐ ┌───────────────────────────────────┐
│   Section B: Provisional Corpus   │ │  Section A: Actionable Candidate  │
│  - Seasonal window closed/unclear │ │  - allow_numerical_scoring = True │
│  - Displayed as advisory notes    │ │  - 2 to 6 schemes per scenario    │
│  - Strictly score-quarantined     │ └─────────────────┬─────────────────┘
└───────────────────────────────────┘                   │
                                                        ▼
┌────────────────────────────────────────────────────────────────────────┐
│               LAYER 3: Contextual ML Priority Ranker                   │
│                   (`src/models/benchmark_v1_2/`)                      │
│  - HistGradientBoosting Ranker trained on Benchmark v1.2               │
│  - Feature Extraction: Need-to-scheme affinity, drought interaction    │
│  - Leave-One-Zone-Out (LOZO) validated across 10 agro-climatic zones   │
│  - NDCG@3 = 0.8993 | MRR = 0.8120 (gain Δ = +0.1190 over baseline)     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│            LAYER 4: Explainability & Presentation Layer                │
│            (`app.py` & `scripts/run_recommendation_demo.py`)           │
│  - Clear rationale: "Why this scheme is prioritized for you"          │
│  - Required documentation checklist & official portal URLs             │
│  - Streamlit Web App (4 Tabs) + Headless CLI runner                    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Layer-by-Layer Detailed Breakdown

### Layer 1: Deterministic Eligibility Engine (`src/eligibility/`)
- **Philosophy:** Hard legal rules must never be approximated by machine learning.
- **Three-Valued Logic:**
  - `ELIGIBLE`: The farmer satisfies every statutory requirement.
  - `INELIGIBLE`: The farmer violates at least one statutory rule (e.g., income-tax payer for PM-KISAN, or $>5$ acres for marginal-farmer programs).
  - `REQUIRES_VERIFICATION`: The profile lacks sufficient data to confirm eligibility. The engine asks for missing data rather than guessing.
- **Parent-Child Deduplication:** Schemes like KCC (`SCH008`) and Ganga Kalyana (`SCH010`) resolve into specific institutional routes (`SCH008_CENTRAL`, `SCH008_KA_COOP`, `SCH010_AMBEDKAR`, etc.) based on caste and banking preferences.

### Layer 2: Availability & Governance Layer (`src/availability/`)
- Separates **statutory entitlement** from **operational portal status**.
- Prevents the system from recommending schemes where application windows have lapsed.
- **Section A vs. Section B Partitioning:**
  - **Section A (Actionable):** Active or rolling schemes ready for application. Eligible for downstream ML ranking.
  - **Section B (Provisional/Seasonal):** Schemes awaiting window opening, budget release, or field verification. Recommending them as "top priority" would misdirect farmers; they are displayed with advisory notices and quarantined from numerical scoring.

### Layer 3: Contextual Machine Learning Ranker (`src/models/`)
- **Model:** Gradient-boosted decision trees (`HistGradientBoostingRegressor`) with custom pairwise / point-wise loss formulation.
- **Features:** 40+ dense features combining farmer constraints (drought exposure, pump status, landholding) with scheme subsidy characteristics (capital grant vs. recurring credit).
- **Validation:** 
  - GroupKFold on scenarios ($k=5$) to prevent scenario leakage.
  - Leave-One-Zone-Out (LOZO) cross-validation across all 10 Karnataka zones ($Z_1$ to $Z_{10}$).

### Layer 4: Explainability & Delivery (`app.py`, `scripts/`)
- **Streamlit Application:**
  - Tab 1: Section A (Actionable schemes ranked by ML, with document checklists and official portals).
  - Tab 2: Section B (Provisional/Upcoming schemes).
  - Tab 3: Disqualified schemes with explicit rule keys (e.g. `EXCLUSION_INCOME_TAX_PAYER`).
  - Tab 4: Engine Debug Trace (complete JSON dump).
- **CLI Runner:** Pre-configured demo profiles (`DEMO_S131`, `DEMO_S132`, `DEMO_S136`, `DEMO_S137`, `DEMO_EXCLUSION_BOUNDARY`).

---

## 3. Core Architectural Invariants

1. **Zero Policy Hallucination:** No generative model or neural network synthesizes or modifies eligibility criteria.
2. **Deterministic Reproducibility:** Every execution on a given farmer profile produces identical eligibility classifications and ranking scores.
3. **Graceful Handling of Edge Cases:** Dual-exclusion profiles (e.g. income tax payer with energized grid borewell) correctly disqualify both PM-KISAN and PM-KUSUM Component B simultaneously.
4. **Complete Test Suite:** 329 passing automated unit, scenario, integration, and ablation tests verify this architecture continuously.
