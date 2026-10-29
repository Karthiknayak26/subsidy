# Farmer Benefit ML - Project Full README

> **ML-Based Personalized Government Scheme & Subsidy Recommendation System for Karnataka Farmers**
> Deterministic Eligibility Engine + Governance Safeguards + ML Relevance Ranker + Explainable Web UI

[![Tests: 208 Passing](https://img.shields.io/badge/Tests-208_Passed-brightgreen)](#8-automated-test-suite)
[![Architecture: Rule Engine + ML Ranker](https://img.shields.io/badge/Architecture-Rule_Engine_%2B_ML_Ranker-orange)](#5-system-architecture)
[![Status: Phase 5 Expert Annotation](https://img.shields.io/badge/Status-Phase_5_Expert_Annotation-blue)](#12-project-status--roadmap)
[![Ground Truth: Official Govt Portals](https://img.shields.io/badge/Ground_Truth-Official_Govt_Portals-darkgreen)](#3-the-real-world-problem)

---

## Table of Contents

1. [What Is This Project?](#1-what-is-this-project)
2. [How Was It Developed - The Journey](#2-how-was-it-developed---the-journey)
3. [The Real-World Problem](#3-the-real-world-problem)
4. [How the System Solves It](#4-how-the-system-solves-it)
5. [System Architecture](#5-system-architecture)
6. [Repository Structure](#6-repository-structure)
7. [Scheme Database and Data Pipeline](#7-scheme-database-and-data-pipeline)
8. [Automated Test Suite](#8-automated-test-suite)
9. [APS Assignment - Applied Probability and Statistics](#9-aps-assignment---applied-probability-and-statistics)
10. [The ML Ranker Benchmark v1.2](#10-the-ml-ranker-benchmark-v12)
11. [Web Application and CLI](#11-web-application-and-cli)
12. [Project Status and Roadmap](#12-project-status-and-roadmap)
13. [How to Run the Project](#13-how-to-run-the-project)
14. [Key Design Decisions and Limitations](#14-key-design-decisions-and-limitations)
15. [Glossary](#15-glossary)

---

## 1. What Is This Project?

This is an **end-to-end ML-backed recommendation system** that tells Indian smallholder farmers in Karnataka **which government subsidies and welfare schemes they are eligible for** and more importantly **which ones are most urgently relevant to their immediate farming crisis**.

The system bridges a critical gap: thousands of government agricultural schemes exist across central and state portals, but a farmer standing in their field during a crop failure or pest attack has no way to know which ones apply to them, which are open right now, and which actually help their specific situation today.

### What it does in plain English

A cotton farmer in Raichur types or tells a kiosk: "My cotton crop is damaged by pink bollworm. I have 3 acres of dryland. I am SC category. I need crop insurance."

The system evaluates 16 government schemes against that farmer's exact profile, filters to legally eligible ones, ranks them by how relevant they are to the current crisis, and presents the top recommendations with required documents, official portal links, and disclaimers - all traceable to official .gov.in sources.

### What makes it different from a simple scheme list

| Feature | Static Scheme Catalogue | This System |
|---|---|---|
| Personalised to farmer profile | No | Yes (land, crop, category, need) |
| Statutory eligibility filtering | No | Yes (deterministic rules, 3-valued logic) |
| Handles missing/unknown info | No | Yes (REQUIRES_VERIFICATION state) |
| Separates closed schemes | No | Yes (4-state availability filter) |
| Ranks by urgency / relevance | No | Yes (ML Ranker, Benchmark v1.2) |
| Explains every decision | No | Yes (fired rule keys, official URLs) |
| Protects against false approvals | No | Yes (zero policy hallucination guarantee) |

---

## 2. How Was It Developed - The Journey

The project was built iteratively across **5 engineering phases**, each building on the last:

```
Phase 1 --- Scheme Database and Ground Truth Curation
     |        16 schemes encoded from Official Gazettes and gov.in portals
     |        31-column schema; parent-child hierarchy design
     v
Phase 2 --- Deterministic Eligibility Engine
     |        Python rule engine with Three-Valued Logic (ELIGIBLE / INELIGIBLE / REQUIRES_VERIFICATION)
     |        Covers all 10 scheme categories + 6 child implementation routes
     |        208+ automated tests passing
     v
Phase 3 --- Availability and Governance Layer
     |        Decouples statutory eligibility from operational portal availability
     |        4-state availability filter; Section A / Section B governance safeguard
     |        Prevents recommending schemes with closed portals
     v
Phase 4 --- Pilot Scenarios, Benchmark and Expert Annotation Infrastructure
     |        10 calibration pilot scenarios (S001-S010) across Karnataka districts
     |        60-scenario Benchmark v1.0.4 frozen across 10 agro-climatic zones
     |        2-phase blinded annotation CLI; Krippendorff Alpha agreement metrics
     v
Phase 5 --- ML Ranker (Benchmark v1.2) + Web Application (Current Phase)
             HistGradientBoosting Ranker trained on human-annotated relevance labels
             Streamlit Web UI + Headless CLI demo interface
             APS Assignment: Statistical hypothesis testing of ML vs. baseline
```

### Why this build order?

- Phase 1 first because you cannot rank what you have not encoded accurately.
- Phase 2 before ML because statutory eligibility is a hard legal filter - an ML model must never guess legal rules.
- Phase 3 before presenting to users because recommending a scheme whose portal closed yesterday causes real harm.
- Phase 4 before ML training because ML training needs high-quality human-labelled ground truth from independent expert annotation.
- Phase 5 last because a model trained without adequate data is worse than a heuristic.

---

## 3. The Real-World Problem

### The Information Gap

Imagine Basavaraj, a smallholder cotton farmer in Raichur, Karnataka:
- Cultivates 3 acres of rainfed cotton.
- A severe pink bollworm infestation threatens his entire crop.
- He needs financial relief urgently.

In reality:
- He does not read the Karnataka Gazette or browse ministerial portals.
- When he visits the local RSK office, he may be told about one scheme or none depending on the officer's awareness.
- He may pay out-of-pocket for drip pipes or insurance premiums, unaware he qualifies for a 90% capital subsidy or subsidized coverage.

```
   Farmer Reality                          Government Portal Reality
+---------------------------+           +----------------------------------+
| "I need drip irrigation   |           | Department of Horticulture       |
| for 2 acres of tomato.    |   GAP     | Budget Head: 2401-00-119-01      |
| What can I get?"          | <=======> | Guidelines: 48-page PDF          |
| - No gazette awareness    |           | Index: Statutory scheme name     |
| - Constrained cash flow   |           | Form: FRUITS registration        |
+---------------------------+           +----------------------------------+
```

### Why this gap is dangerous

1. A farmer eligible for PMKSY drip irrigation subsidy may install unsubsidised pipes - losing Rs. 50,000+.
2. A farmer with cotton damage may not know to file a PMFBY calamity intimation within 72 hours.
3. A General category farmer may be unaware they are excluded from Ganga Kalyana borewell programmes.
4. A government employee family member may unknowingly apply for PM-KISAN despite statutory exclusion.

---

## 4. How the System Solves It

The system uses a **two-desk triage model**:

### Desk 1 - Deterministic Eligibility Triage (The Nurse)

A deterministic Python rule engine (src/eligibility/engine.py) evaluates every scheme against the farmer's exact statutory profile. Like a nurse who checks objective vitals, it:

- Never guesses - if income tax status is unknown, it flags REQUIRES_VERIFICATION, not a default approval.
- Evaluates all 16 scheme records covering 10 major programmes.
- Returns three-valued output: ELIGIBLE, INELIGIBLE, or REQUIRES_VERIFICATION.
- Fires named rule keys for every decision (e.g., PMKISAN_MTS_PENSION_EXEMPTION_APPLIED), enabling audit traceability.

### Desk 2 - ML Relevance Ranker (The Specialist)

From the eligible pool, a trained ML model (Benchmark v1.2 HistGradientBoostingRegressor) ranks schemes by how relevant they are to the farmer's immediate stated need:

- A farmer needing crop insurance should see PMFBY at Rank 1, not a free soil health card.
- A farmer needing solar pump installation should see PM-KUSUM B at Rank 1, not a machinery subsidy.

### The Governance Safeguard Layer

Between Desk 1 and Desk 2, a governance pipeline (src/eligibility/governance.py) enforces legal presentation rules:
- Routes PMFBY to Section B pending seasonal notification orders.
- Quarantines provisional corporation schemes without numerical scoring.
- Excludes pure tenants from landholder welfare routes.
- Enforces PM-KISAN statutory inheritance succession rules.

---

## 5. System Architecture

```
[ Farmer Input Profile ]
  District, Agro-climatic Zone, Crops, Land, Water Source
  Social Category, Income, Assets, Immediate Need
          |
          v
+============================================================+
|  DESK 1: Deterministic Eligibility Engine                  |
|  src/eligibility/engine.py  (FROZEN - zero hallucination)  |
|  Evaluates 16 scheme records with Three-Valued Logic       |
+============================+===============================+
                             |
                             v
+============================================================+
|  STATUTORY GOVERNANCE PIPELINE                             |
|  src/eligibility/governance.py                             |
|  PMFBY Section B, Tenant routing, Provisional quarantine   |
+===============+================+==========================+
                |                |                |
                v                v                v
    Section A Candidates   Section B        Disqualified
    (Confirmed Actionable)  (Advisory)    (Statutorily Barred)
                |
                v
+============================================================+
|  DESK 2: ML Relevance Ranker (Benchmark v1.2)              |
|  src/models/benchmark_v1_2/ranker.py                       |
|  HistGradientBoostingRegressor - Predicts 0-3 relevance    |
|  Fallback: Heuristic need-matching baseline                |
+============================================================+
                |
                v
    Ranked Recommendations + Document Checklist + Disqualification Log
    (Rank, Score, Official Citations, Statutory Disclaimers)
```

### Three-Valued Logic - Why It Matters

| Farmer's Income Tax Status | Standard Boolean | Our Engine |
|---|---|---|
| False (does not pay tax) | Approved | ELIGIBLE |
| True (pays income tax) | Denied | INELIGIBLE |
| None / Unknown | Falsely Approved | REQUIRES_VERIFICATION - asks for Form 16 |

**Zero Policy Hallucination Guarantee**: The deterministic engine only states what it can derive from the farmer's inputs. Unknown attributes never silently default to approvals - they trigger a verification request with the specific document needed.

---

## 6. Repository Structure

```
farmer-benefit-ml/
+-- app.py                                   # Streamlit Web Application
+-- project_full.md                          # THIS FILE - Full Project README
+-- README.md                                # Comprehensive Technical Teaching Guide
|
+-- scheme_database/                         # Scheme Data Core
|   +-- build_scheme_master.py               # Generates raw JSON, CSV, Excel outputs
|   +-- scheme_master.xlsx                   # 31-column formatted master spreadsheet
|   +-- raw/                                 # 16 individual scheme JSON files
|   |   +-- SCH001_PM_KISAN.json
|   |   +-- SCH002_PMFBY.json
|   |   +-- SCH003_PMKSY_PDMC.json
|   |   +-- SCH004_SMAM.json
|   |   +-- SCH005_Krishi_Bhagya.json
|   |   +-- SCH006_PM_KUSUM_B.json
|   |   +-- SCH007_MIDH.json
|   |   +-- SCH008_KCC_MISS.json             # Parent record
|   |   +-- SCH008_CENTRAL_KCC_MISS.json     # Child: Commercial banks
|   |   +-- SCH008_KA_COOP_Zero_Interest.json  # Child: PACS/DCCB
|   |   +-- SCH009_Soil_Health_Card.json
|   |   +-- SCH010_Ganga_Kalyana.json        # Parent record
|   |   +-- SCH010_AMBEDKAR_Ganga_Kalyana.json   # Child: SC farmers
|   |   +-- SCH010_VALMIKI_Ganga_Kalyana.json    # Child: ST farmers
|   |   +-- SCH010_DEVARAJ_URS_Ganga_Kalyana.json # Child: OBC farmers
|   |   +-- SCH010_KMDC_Ganga_Kalyana.json   # Child: Minorities
|   +-- processed/
|       +-- scheme_master.json               # Consolidated engine input
|       +-- scheme_master.csv                # Tabular inspection copy
|       +-- scheme_availability_template.csv # Availability tracking template
|
+-- src/                                     # Core Source Code
|   +-- eligibility/
|   |   +-- models.py                        # FarmerScenario dataclass, Enums
|   |   +-- engine.py                        # Deterministic eligibility engine
|   |   +-- availability.py                  # 4-state availability filter
|   |   +-- governance.py                    # Section A/B governance safeguards
|   +-- models/
|   |   +-- benchmark_v1_2/
|   |       +-- ranker.py                    # Benchmark v1.2 ML Ranker
|   +-- evaluation/
|       +-- metrics.py                       # NDCG@K, MRR, permutation tests
|       +-- benchmark_candidates.py          # Frozen candidate set (283 pairs)
|
+-- tests/                                   # Automated Test Suite (208 tests)
|   +-- test_eligibility_engine.py           # 56 unit and integration tests
|   +-- test_benchmark_matrix.py             # 11 benchmark matrix tests
|   +-- test_zone_z1_scenarios.py to z10     # 100 scenario zone tests
|   +-- test_evaluation_metrics.py           # 13 metric evaluation tests
|   +-- test_app_integration.py              # End-to-end application tests
|   +-- test_ml_ranker_v1_2.py
|   +-- test_benchmark_v1_2_scenarios.py
|
+-- scripts/                                 # Operational CLI Scripts
|   +-- run_pilot_execution.py               # Runs S001-S010 through engine
|   +-- run_annotation_session.py            # Interactive 2-phase expert annotation CLI
|   +-- compute_agreement.py                 # Krippendorff Alpha, Kappa, Kendall W
|   +-- compute_benchmark_agreement.py       # Benchmark v1.0.4 inter-rater reliability
|   +-- train_benchmark_v1_2_ranker.py       # Preregistered ML training script
|   +-- run_recommendation_demo.py           # Headless CLI demo
|   +-- smoke_test_agreement_pipeline.py     # End-to-end pipeline verification
|
+-- APS_ASSIGNMENT/                          # Applied Probability and Statistics Assignment
|   +-- subsidy_probability_statistics_assignment.py
|
+-- research/dataset_research/              # Research and Benchmarking
|   +-- case_b_scenario_spec.md
|   +-- expert_annotation_form.md
|   +-- pilot_execution_results.json
|   +-- pilot_execution_report.md
|
+-- data/
|   +-- annotations/                         # Expert annotation responses
|   +-- benchmarks/v1.2/ml_experiment/      # ML training artifacts
|
+-- reports/                                 # Statistical output figures
    +-- fig1_confusion_matrices.png
    +-- fig2_roc_curves.png
    +-- fig3_bootstrap_ci.png
    +-- fig4_mcnemar_contingency.png
```

---

## 7. Scheme Database and Data Pipeline

### The 16 Scheme Records

| Scheme ID | Name | Type | Key Benefit |
|---|---|---|---|
| SCH001 | PM-KISAN | Standalone | Rs. 6,000/year direct cash in 3 DBT installments |
| SCH002 | PMFBY | Standalone | Crop insurance; farmer pays 1.5-5% premium cap |
| SCH003 | PMKSY-PDMC | Standalone | Drip/sprinkler subsidy (up to 90% for SC/ST) |
| SCH004 | SMAM | Standalone | Farm machinery subsidy (up to 50%/60% SC/ST) |
| SCH005 | Krishi Bhagya | Standalone | Rainwater harvesting package for dryland farmers |
| SCH006 | PM-KUSUM B | Standalone | Solar pump for off-grid borewells |
| SCH007 | MIDH | Standalone | Protected horticulture / polyhouse subsidy |
| SCH008 | Agricultural Credit | Parent | - |
| SCH008_CENTRAL | KCC-MISS (Commercial) | Child | Kisan Credit Card at 4% effective interest |
| SCH008_KA_COOP | Karnataka 0% Crop Loan | Child | 0% interest crop loan via PACS/DCCBs |
| SCH009 | Soil Health Card | Standalone | Free soil diagnostic testing |
| SCH010 | Ganga Kalyana | Parent | - |
| SCH010_AMBEDKAR | Ganga Kalyana (SC) | Child | Free borewell and irrigation for SC farmers |
| SCH010_VALMIKI | Ganga Kalyana (ST) | Child | Free borewell and irrigation for ST farmers |
| SCH010_DEVARAJ_URS | Ganga Kalyana (OBC) | Child | Free borewell and irrigation for OBC farmers |
| SCH010_KMDC | Ganga Kalyana (Minorities) | Child | Free borewell and irrigation for religious minorities |

### Parent-Child Deduplication

Abstract parents (SCH008, SCH010) are automatically suppressed from user-facing output when their children are actionable, preventing duplicate recommendation cards.

### Data Pipeline Build Lifecycle

```
In-memory Python Curated Records (16 scheme dicts)
                    |
                    +---> 1. 16 raw JSON files  (scheme_database/raw/)
                    +---> 2. scheme_master.json  (processed/ - engine input)
                    +---> 3. scheme_master.csv   (processed/ - tabular inspection)
                    +---> 4. scheme_master.xlsx  (scheme_database/ - human audit)
```

---

## 8. Automated Test Suite

**208 tests passing** across 18 test suites (as of October 2026):

| Test Suite | Tests | What It Verifies |
|---|---|---|
| test_eligibility_engine.py | 56 | Core eligibility rules - positive, negative, boundary, MTS exemptions |
| test_benchmark_matrix.py | 11 | Benchmark scenario matrix consistency |
| test_zone_z1_scenarios.py to z10 | 100 | 100 scenarios across 10 agro-climatic zones |
| test_evaluation_metrics.py | 13 | NDCG@K, MRR, permutation test correctness |
| test_benchmark_annotation_packets.py | 5 | Annotation packet integrity |
| test_ingest_benchmark_annotations.py | 8 | Annotation ingestion pipeline |
| test_compute_benchmark_agreement.py | 13 | Inter-rater reliability pipeline |

**Code coverage**: 88% overall (92% models, 87% engine, 84% availability).

NOTE: 88% code coverage proves internal software consistency - that the code matches its encoded rules. It does NOT prove that the underlying government policies are legally current.

### Test Categories

| Category | Example | Purpose |
|---|---|---|
| Positive Test | test_clean_positive | Fully qualifying farmer receives ELIGIBLE |
| Negative Exclusion | test_paid_income_tax_excluded | Statutory exclusion fires INELIGIBLE |
| Boundary Test | test_individual_acreage_boundaries | Exact limits (1.5 ac, 5.0 ac, 12.35 ac) |
| Unknown-Input Test | test_income_tax_unknown | Missing values return REQUIRES_VERIFICATION |
| Statutory Exemption | test_mts_class_iv_employee_is_exempt | MTS Group D exempt from govt employee exclusion |
| Architectural Guardrail | test_unverified_schemes_do_not_leak | Closed schemes cannot appear in Available Now |

---

## 9. APS Assignment - Applied Probability and Statistics

**File:** APS_ASSIGNMENT/subsidy_probability_statistics_assignment.py

### Research Objective

Does the candidate ML model (Random Forest Classifier) perform statistically significantly better than the baseline (Logistic Regression Classifier) in predicting actionable subsidy fit for Karnataka farmers, or can the observed difference be explained by test-sample variation alone?

### 7-Step Statistical Framework

#### Step 1 - Data Preparation and Cluster-Preserving Sampling
- Loads Benchmark v1.2 candidate pair dataset.
- Strict scenario-level split: 72 training scenarios, 18 held-out test scenarios.
- Zero data leakage - no scenario appears in both train and test sets.

#### Step 2 - Supervised Classification
- Task: Binary classification - predict whether a scheme is Actionable (1) or Marginal/Irrelevant (0).
- Features: 5 numerical + 18 categorical + 7 boolean (land size, income, district, crop, social category, water source, immediate need, scheme metadata).

#### Step 3 - Dual Model Training and Evaluation

| Metric | Baseline (Logistic Regression) | Candidate (Random Forest) | Delta |
|---|---|---|---|
| Accuracy | ~75.00% | ~77.78% | +2.78% (+2 correct out of 72) |

#### Step 4 - Paired Bootstrap Confidence Intervals (B = 10,000)

Two bootstrapping strategies:

1. Row-Level Paired Bootstrap: resamples individual observation rows.
2. Cluster-Aware Scenario-Level Bootstrap: resamples at the scenario level respecting within-scenario dependencies.

```
Observed Delta       = +0.0278 (+2.78%)
95% Cluster-Aware CI = [-0.065, +0.125]
CI spans zero?       = YES -> cannot distinguish from sampling variation alone
```

#### Step 5 - McNemar Paired Hypothesis Test

```
H0: Both models have equal error rates
H1: Models have different error rates

Exact Binomial Two-Sided p-value: p >> 0.05
Decision: FAIL TO REJECT H0
```

The discordant pairs are too few to conclude a statistically significant difference.

#### Step 6 - Visualizations Produced (saved to reports/)

| Figure | File | Content |
|---|---|---|
| Fig 1 | fig1_confusion_matrices.png | Side-by-side confusion matrices (LR vs RF) |
| Fig 2 | fig2_roc_curves.png | ROC curve comparison with AUC values |
| Fig 3 | fig3_bootstrap_ci.png | Bootstrap sampling distribution of accuracy difference |
| Fig 4 | fig4_mcnemar_contingency.png | McNemar 2x2 contingency heatmap |

#### Step 7 - Final Scientific Verdict

```
PASS WITH WARNINGS

STRENGTHS:
  [+] Zero data leakage (strict scenario-level split)
  [+] Accurate bootstrap and McNemar implementation
  [+] Cluster-aware resampling respects data structure
  [+] RF accuracy +2.78% over LR baseline

WARNINGS:
  [!] 95% CI spans zero - cannot confirm superiority at alpha = 0.05
  [!] Single annotator labels (Human Reviewer 2) - no independent IRR
  [!] Small sample size (N = 90 scenarios) limits statistical power
  [!] Labels represent expert policy relevance, NOT real-world farm outcomes
```

### How to Run the APS Assignment

```bash
python APS_ASSIGNMENT/subsidy_probability_statistics_assignment.py
```

---

## 10. The ML Ranker Benchmark v1.2

**Training Script:** scripts/train_benchmark_v1_2_ranker.py
**Ranker Module:** src/models/benchmark_v1_2/ranker.py

### Training Setup

| Parameter | Value |
|---|---|
| Model | HistGradientBoostingRegressor (sklearn) |
| Training scenarios | 72 (80% of 90) |
| Held-out test scenarios | 18 (20%) |
| Candidate pairs | 369 total; 283 in Section A |
| Evaluation | GroupKFold OOF, LOZO, crisis-type holdout, land-tenure holdout |
| Primary metric | NDCG@3 (Normalized Discounted Cumulative Gain at rank 3) |

### Key Results

- NDCG@3 gain over heuristic baseline: +0.1190
- Conclusion: ML ranker provides meaningful lift, but results are exploratory (single annotator, small N).

### Preregistration Safeguards

- SHA-256 checksum verification of frozen annotation file
- Annotation-to-candidate-set alignment validation
- Relevance score integrity checks (values must be in 0, 1, 2, 3)
- Scenario-level holdout with zero leakage
- Heuristic fallback if model artifacts are absent

### The Relevance Scale (Ground Truth for ML)

| Score | Label | Meaning |
|---|---|---|
| 3 | Highly Relevant | Directly addresses primary crisis - must appear in Top-3 |
| 2 | Relevant | Genuine benefit, but secondary to the urgent need |
| 1 | Marginally Relevant | Eligible but minor value in current context |
| 0 | Irrelevant | Eligible but no meaningful practical value right now |

### Expert Annotation Protocol

Annotations collected via 2-phase blinded CLI (scripts/run_annotation_session.py):

- Phase 1 (Blind): Expert scores relevance 0-3 without seeing portal availability dates. This prevents experts from giving a vital scheme a score of 0 just because its portal closed yesterday.
- Phase 2 (Revealed): Availability shown; expert confirms actionability.

Inter-Rater Reliability computed using Krippendorff Alpha (ordinal). Threshold: Alpha >= 0.70 required before ML training.

---

## 11. Web Application and CLI

### Web Application (Streamlit)

```bash
streamlit run app.py
```

**Four presentation tabs:**

| Tab | Name | Content |
|---|---|---|
| 1 | Section A - Actionable | Ranked schemes with ML scores, documents, official citations |
| 2 | Section B - Advisory | Seasonal/provisional schemes; NO numerical scoring |
| 3 | Disqualified Schemes | Ineligible schemes with exact statutory exclusion rule keys |
| 4 | Engine Debug and Trace | Raw JSON payload for technical audit |

### Command-Line Demo

```bash
python scripts/run_recommendation_demo.py --preset DEMO_S131
python scripts/run_recommendation_demo.py --preset all
python scripts/run_recommendation_demo.py --preset DEMO_EXCLUSION_BOUNDARY
python scripts/run_recommendation_demo.py --preset DEMO_S131 --heuristic
python scripts/run_recommendation_demo.py --preset DEMO_S131 --json
```

### Demonstration Profiles

| Preset | Profile | Key Invariant Demonstrated |
|---|---|---|
| DEMO_S131 | Rainfed Marginal Tenant, Yadgir | Pure tenancy PM-KISAN exclusion; KCC to Section B |
| DEMO_S132 | Canal SC Smallholder, Bidar | Soil Health Card + KCC prioritized; provisional quarantined |
| DEMO_S136 | Medium Landowner, Yadgir | Area capping for mechanization schemes (SMAM) |
| DEMO_S137 | Rainfed Solar Need, Bidar | PM-KUSUM B solar pump eligibility |
| DEMO_EXCLUSION_BOUNDARY | Income-Tax Payee + Grid Borewell | PM-KISAN (tax) + PM-KUSUM B (grid) simultaneously disqualified |

---

## 12. Project Status and Roadmap

| Component | Status | Notes |
|---|---|---|
| Scheme Database (16 records) | Done | Static; no live scraping yet |
| Eligibility Engine | Done and Tested | 208 tests passing |
| Parent Deduplication | Done and Tested | SCH008, SCH010 handled |
| Availability Filter | Done | Template unpopulated - all default to Availability Unknown |
| 10 Pilot Scenarios (S001-S010) | Done | Calibration set only |
| 60-Scenario Benchmark v1.0.4 | Frozen | Z1-Z10 zones |
| Annotation Pipeline | Done and Tested | Protocol v1.1 |
| ML Ranker (Benchmark v1.2) | Exploratory | Single annotator; IRR pending |
| Streamlit Web Application | Done | app.py |
| APS Statistical Assignment | Done | See Section 9 |
| Independent Expert Annotation | In Progress | Phase 5 |
| Kannada Localization | Planned | Translation tables not yet built |
| Live Portal Monitoring | Planned | No headless scraper yet |

### 5 Highest-Priority Technical Risks

1. Unpopulated Availability Layer - all recommendations default to Availability Unknown.
2. Single-Annotator ML Labels - IRR collection from independent reviewers is pending.
3. Hardcoded Rules in Python - each policy update requires code changes; declarative rule DSL needed.
4. Small ML Dataset - 90 scenarios, 369 pairs; results are exploratory only.
5. English-Only UI - direct farmer use requires Kannada localization.

---

## 13. How to Run the Project

### Prerequisites

```bash
pip install streamlit scikit-learn pandas numpy scipy matplotlib seaborn joblib openpyxl pytest
```

### Commands

```bash
# Build scheme database
python scheme_database/build_scheme_master.py

# Run full test suite (expect 208 passed)
pytest tests/ -v

# Launch web application
streamlit run app.py

# Run pilot scenarios S001-S010
python scripts/run_pilot_execution.py

# Train the ML ranker (requires annotation data)
python scripts/train_benchmark_v1_2_ranker.py

# Run APS statistical assignment (requires trained ML artifacts)
python APS_ASSIGNMENT/subsidy_probability_statistics_assignment.py

# Run expert annotation session
python scripts/run_annotation_session.py

# Compute inter-rater agreement
python scripts/compute_benchmark_agreement.py
```

---

## 14. Key Design Decisions and Limitations

### Why not use an LLM for eligibility?

An LLM can hallucinate eligibility criteria. For example, it might learn "farmers with 15 acres usually get tractor subsidies" and approve someone who exceeds the legal 5-hectare cap. Our system guarantees zero hallucination because every eligibility decision traces to named Python rule functions derived from official government documents.

### Why Three-Valued Logic?

Missing data is common in rural welfare applications. Defaulting unknown attributes to False would approve ineligible applicants. Defaulting to True would unfairly deny qualifying farmers. The third state, REQUIRES_VERIFICATION, is the only safe honest answer and it tells the farmer exactly which document is needed.

### Why separate Eligibility from Availability?

Statutory eligibility (legal criteria in gazette) changes rarely. Administrative availability (portals open today, seasonal cut-off dates) changes seasonally. Mixing them would produce recommendations like "You are eligible for PMFBY" when the Kharif cut-off date passed last week.

### Why defer ML until expert labels exist?

Training an ML model on 10 pilot scenarios (~70 scheme pairs) would produce a model that memorises training data and generalises to nothing. The annotation infrastructure was built first precisely because the labels do not yet exist.

### Current Limitations

| Limitation | Impact | Planned Mitigation |
|---|---|---|
| Single-annotator ML labels | Results exploratory | Collect independent E1 and E2 annotations |
| Availability template unpopulated | All schemes show Availability Unknown | Manual portal audit; populate CSV |
| Only 4 Ganga Kalyana corporations | May miss eligible corporations | Document scope; expand registry |
| English-only UI | Cannot be used by rural farmers directly | Kannada localization roadmap |
| Rules hardcoded in Python | Code change required per policy update | Migrate to declarative rule DSL |

---

## 15. Glossary

| Term | Definition |
|---|---|
| Deterministic Engine | Software where identical inputs always produce identical, explainable outputs |
| Three-Valued Logic | Logic system with True, False, and Unknown (REQUIRES_VERIFICATION) |
| FarmerScenario | Python dataclass encoding a farmer complete profile for engine evaluation |
| SchemeDetermination | Engine output for one scheme: status, fired rule keys, disqualification reasons |
| Parent / Child Scheme | Parent = abstract policy umbrella; Child = concrete implementation route |
| Parent Deduplication | Automatic suppression of abstract parent records when actionable children exist |
| Section A | Schemes confirmed actionable by governance pipeline - eligible for ML ranking |
| Section B | Schemes requiring seasonal notifications - qualitative advisory only |
| NDCG@K | Normalized Discounted Cumulative Gain at rank K - ranking quality metric |
| Krippendorff Alpha | Chance-corrected inter-rater reliability metric with ordinal distance penalties |
| McNemar Test | Paired statistical test comparing error rates of two classifiers |
| Bootstrap CI | Confidence interval estimated by resampling observed data B=10,000 times |
| Data Leakage | Flaw where information from outside training contaminates model inputs |
| PMKSY-PDMC | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (drip/sprinkler subsidy) |
| PMFBY | Pradhan Mantri Fasal Bima Yojana (national crop insurance) |
| PM-KISAN | Pradhan Mantri Kisan Samman Nidhi (Rs. 6,000/year direct cash to farmers) |
| PM-KUSUM B | PM Kisan Urja Suraksha evam Utthaan Mahabhiyan Component B (solar pumps) |
| SMAM | Sub-Mission on Agricultural Mechanization (farm machinery subsidy) |
| MIDH | Mission for Integrated Development of Horticulture |
| Ganga Kalyana | Karnataka state borewell and irrigation programme via caste-specific corporations |
| RSK | Raitha Samparka Kendra - local agricultural extension office in Karnataka |
| IRR | Inter-Rater Reliability - statistical agreement between independent human annotators |

---

Academic and Research Use Only.
All demonstration scenarios are synthetic profiles developed for verification purposes.
Recommendation scores reflect modelled suitability. All subsidy sanctions remain subject to
official taluk-level biometric verification, land record mutation, and annual budget quota limits.
Ground truth sourced from: pmkisan.gov.in, agricoop.nic.in, samrakshane.karnataka.gov.in, fruits.kar.nic.in
