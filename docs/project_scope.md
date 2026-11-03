# Project Scope & Boundary Specifications

## Current Implementation Status: Complete (Phases 1–5 Delivered, 329 Tests Passing)

This document establishes the precise functional boundaries, completed milestones, and future roadmap for the **farmer-benefit-ml** recommendation system.

---

## 1. In-Scope Deliverables (Implemented & Validated)

### 1.1 Domain & Geographic Coverage
- **Geography:** State of Karnataka, spanning all 10 Agro-Climatic Zones ($Z_1$ North Eastern Transition to $Z_{10}$ Coastal).
- **Target Beneficiaries:** Smallholder, marginal, tenant, and community-pooled farmers facing operational crises (pest attacks, drought, equipment deficits, power unreliability).
- **Scheme Corpus:** 16 verified records (10 core conceptual schemes + 6 implementation child routes) encompassing Direct Benefit Transfers (DBT), micro-irrigation, solar pumps, mechanization, subsidized credit, crop insurance, and soil health diagnostics.

### 1.2 Dual-Stage System Architecture
1. **Deterministic Statutory Filtering:**
   - Evaluates mandatory legal criteria from verified government gazettes and official department orders.
   - Implements Three-Valued Logic (`ELIGIBLE`, `INELIGIBLE`, `REQUIRES_VERIFICATION`).
   - Sifts out strictly disqualified schemes and logs explicit rule violation keys.
2. **Operational Availability & Governance Layer:**
   - 4-state availability pipeline (`AVAILABLE_NOW`, `TIMING_PENDING`, `REQUIRES_VERIFICATION`, `CLOSED`).
   - Partitions output into Section A (Actionable, ready for ML scoring) and Section B (Provisional/Seasonal, quarantined from numerical scoring).
3. **Machine Learning Contextual Ranker:**
   - Gradient-boosted ranking (`HistGradientBoostingRegressor`) over actionable Section A schemes.
   - Out-of-fold NDCG@3 = 0.8993 (gain $\Delta = +0.1190$ over deterministic heuristic baseline).
   - Validated via GroupKFold and Leave-One-Zone-Out (LOZO) cross-validation.
4. **Transparent Explainability:**
   - Explains *why* a scheme is prioritized.
   - Enumerates required documentation (RTC/Pahani, caste certificate, bank passbook).
   - Direct links to official government application portals (`.gov.in`).
5. **Demonstrable Delivery:**
   - Streamlit interactive Web UI (`app.py`) with 4 diagnostic tabs.
   - Headless CLI demo runner (`scripts/run_recommendation_demo.py`) with preset profiles.

---

## 2. Explicit Out-of-Scope Boundaries (Current Phase)

1. **Automated Scheme Approval & Disbursement:**
   - The platform is an advisory and decision-support recommendation system.
   - It does not submit applications to government portals, sign forms, or disburse funds.
2. **Policy Invention by Machine Learning:**
   - Machine learning models are strictly prohibited from determining eligibility criteria, income thresholds, or subsidy amounts.
   - Legal rules remain 100% deterministic and traceable to statutory source files.
3. **Synthetic Scheme Hallucination:**
   - No fictitious schemes, fake grants, or hypothetical welfare programs are admitted into the knowledge base.
4. **Direct Autonomous Banking Integration:**
   - The system does not interface directly with Core Banking Solutions (CBS) or credit bureau APIs (e.g. CIBIL).

---

## 3. Post-Phase 5 Roadmap (Future Deployments)

| Capability | Target Milestone | Description |
|---|:---:|---|
| **Kannada UI & Voice Localization** | Phase 6 | Complete Kannada translation of farmer inputs, scheme titles, explanation strings, and speech-to-text / text-to-speech for RSK kiosks. |
| **Independent Multi-Expert IRR** | Phase 6 | Scale expert annotation pool across multiple independent Agricultural Extension Officers (AEOs) to establish formal Krippendorff's $\alpha \ge 0.70$. |
| **Live Portal Scraping & API Sync** | Phase 7 | Automated ingestion pipelines monitoring Karnataka's *Seva Sindhu*, *K-Kisan*, and *FRUITS* portals for real-time application window open/close alerts. |
| **Low-Connectivity SMS / IVR Engine** | Phase 8 | Lightweight USSD and interactive voice response (IVR) adapter for non-smartphone users in remote rural drylands. |
