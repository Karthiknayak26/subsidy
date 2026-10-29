# Benchmark v1.1 Formal Methodology Sign-Off Record

**Document Version:** `benchmark-v1.1-signoff-v1.0`  
**Milestone:** Benchmark v1.1 Formal Methodology Sign-Off & Annotation Packet Authorization  
**Target Benchmark:** Benchmark v1.1 (`S071`–`S130`, 60 Compound-Need Scenarios across Zones Z1–Z10)  
**Approver / Reviewing Authority:** Research Methodology Review Panel & Lead Agricultural Systems Reviewer  
**Date:** October 25, 2026  
**Final Status:** **FORMALLY APPROVED (HUMAN ANNOTATION PACKETS AUTHORIZED)**  

---

## 1. Executive Context & Scope of Approval

Following the technical completion of the Benchmark v1.1 scenario matrix (`S071`–`S130`), candidate generation execution, preflight audit verification, and calibration rubric refinement, this document formally records the research team's substantive methodology sign-off.

Automated test execution (12/12 passing v1.1 tests) established technical pipeline reproducibility; this document records the **substantive scientific and governance decisions** required before distributing annotation packets to human reviewers E1 and E2.

---

## 2. Formal Sign-Off Decisions

### Decision 1: Candidate Pool Distribution Acceptance
- **Recorded Decision:** **ACCEPTED WITHOUT ARTIFICIAL INFLATION**
- **Empirical Findings:** The frozen [EligibilityEngine](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/src/eligibility/engine.py) applied to the 16-record master catalog generates an observed Section A candidate pool of **mean 4.48 candidates per scenario** (range 2 to 7 schemes; total 269 Section A candidate determinations across 60 scenarios).
- **Substantive Rationale:** With 5 schemes quarantined in Section B (PMFBY + 4 provisional corporation records), at most 11 non-provisional schemes exist in the registry. Statutory land title, irrigation status, and social category constraints naturally compress eligible options. The initial 6–10 candidate target was an empirical hypothesis, not a statutory requirement. The observed distribution is accepted as a genuine reflection of catalog capacity. No schemes will be artificially injected or statutory filters relaxed.

### Decision 2: Scoring Rubric Approval (Primary Crisis Primacy & Score 3 Boundary)
- **Recorded Decision:** **APPROVED**
- **Rubric Standard:** Formal adoption of the four-level operational rubric defined in [benchmark_v1.1_calibration_rubric.md](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/research/dataset_research/benchmark_v1.1_calibration_rubric.md):
  - **Score 3:** Direct and material resolution of the stated **Primary Acute Crisis** is sufficient for Score 3. Secondary-need alignment strengthens the rationale, but is not mandatory.
  - **Score 2:** Directly addresses an important **Secondary Operational Constraint** without resolving the primary crisis (strictly capped at Score 2 under Primary Crisis Primacy); OR provides material but **incomplete mitigation** of the primary crisis.
  - **Score 1:** Contextually relevant, indirect, or marginal practical support.
  - **Score 0:** Mismatched, untimely, unrequested capital burden, or foreseeably counterproductive impact.
- **Substantive Rationale:** Resolves previous ambiguity by establishing that an intervention providing high-impact relief to an acute emergency (e.g. water pumping to save crops) is not penalized simply because it does not simultaneously provide input credit. Secondary-only interventions remain strictly capped at Score 2. Ordinal relevance scores are decoupled from ranking positions and NDCG@3 metrics.

### Decision 3: Calibration Anchors & Evidence Approval
- **Recorded Decision:** **APPROVED**
- **Scope:** Synthetic calibration anchors `CALIB-01` through `CALIB-06` are approved as standard training fixtures, completely partitioned from test scenarios `S071`–`S130`.
- **Evidence Review:**
  - `CALIB-01` (PM-KUSUM Component B): Sourced to `pmkusum.mnre.gov.in`. Reviewers are instructed to evaluate implementation lag case-by-case based on seasonal crop timing rather than assuming an unverified turnaround window.
  - `CALIB-02` (Central KCC-MISS): Sourced to `financialservices.gov.in`. Bounded as seasonal input credit (Score 2 cap), not debt relief.
  - `CALIB-03` (PMKSY-PDMC): Sourced to `pmksy.gov.in`. Describes root-zone emitter delivery stretching remaining water conditionally based on canopy demand, without unsourced numerical percentage claims.
  - `CALIB-04` (Soil Health Card): Sourced to `soilhealth.dac.gov.in`. Universal access but long lab turnaround; marginal (Score 1) for acute standing crop blight.
  - `CALIB-05` (PMKSY-PDMC mismatch): Score 0 for waterless rainfed parcel facing drought.
  - `CALIB-06` (Complementarity): Score 2 for secondary fertigation fit, with SMAM power-weeder synergy captured in notes without score inflation.

### Decision 4: Evaluation Governance & Protocol Invariants
- **Recorded Decision:** **CONFIRMED & PRESERVED**
- **Section B Isolation:** Section B candidates (`PMFBY`, provisional schemes, unverified oral tenancy credit) remain strictly qualitative-only with numerical scoring disabled.
- **Raw Ratings Preservation Mandate:** Reviewer submissions `E1_raw.csv` and `E2_raw.csv` will be frozen immutably upon receipt. Inter-rater reliability statistics ($\kappa_w \ge 0.61$, $\alpha_{\text{ord}} \ge 0.67$) must be computed strictly on original independent ratings **before** any consensus discussion or adjudication.
- **Preregistered Gates Locked:** All preregistered parameters in [evaluation_preregistration.md](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/research/dataset_research/evaluation_preregistration.md) ($\Delta \overline{\text{NDCG@3}} \ge +0.050$, permutation test $p < 0.050$, zero zone regressions) remain immutably locked.

---

## 3. Sign-Off Authorization Table

| Review Area | Decision | Approver | Date | Conditions & Next Action |
| :--- | :---: | :--- | :---: | :--- |
| **Candidate Pool Size** | **APPROVED** | Research Review Panel | 2026-10-25 | Accept mean 4.48, range 2–7. No artificial schemes added. |
| **Scoring Rubric (0–3)** | **APPROVED** | Lead Methodology Reviewer | 2026-10-25 | Primary crisis sufficiency for Score 3; secondary capped at 2. |
| **Calibration Anchors** | **APPROVED** | Lead Agronomy Reviewer | 2026-10-25 | Sourcing verified; case-by-case timing and root-zone delivery adopted. |
| **Section B Governance** | **APPROVED** | Compliance Officer | 2026-10-25 | Qualitative only; strictly excluded from numerical scoring. |
| **Annotation Packet Issuance** | **AUTHORIZED** | Research Review Panel | 2026-10-25 | Generate `E1_v1.1_blank.csv` and `E2_v1.1_blank.csv` for distribution. |

---

## 4. Immediate Authorized Implementation Step

With this formal record executed, the project is authorized to generate the blinded annotation templates:
- **Target Files:** `data/annotations/benchmark_v1.1/E1_v1.1_blank.csv` and `data/annotations/benchmark_v1.1/E2_v1.1_blank.csv`.
- **Content:** Identical 269 candidate pairs across `S071`–`S130`.
- **Columns:** `scenario_id`, `scheme_id`, `scheme_name`, `rater_id`, `relevance_score` (blank), `relevance_rationale` (blank), `complementarity_notes` (blank).
- **Blinding:** Zero prefilled scores, zero AI predictions, zero shared ratings between reviewers.

*(Formal methodology sign-off record complete and registered in repository.)*
