# 🌾 Farmer Benefit ML — Personalized Government Scheme & Subsidy Recommendation System for Karnataka Farmers

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/Tests-208%20Passed-brightgreen)](tests/)
[![Coverage](https://img.shields.io/badge/Coverage-88%25-yellowgreen)](tests/)
[![Architecture](https://img.shields.io/badge/Architecture-Deterministic%20Engine%20%2B%20ML%20Ranker-orange)](#architecture)
[![Status](https://img.shields.io/badge/Phase-Benchmark%20v1.2%20ML%20Training%20Complete-blue)](#project-phases)

---

## Table of Contents

- [What Is This Project?](#what-is-this-project)
- [The Real Problem It Solves](#the-real-problem-it-solves)
- [How It Was Developed — Phase by Phase](#how-it-was-developed--phase-by-phase)
- [System Architecture](#system-architecture)
- [The APS Assignment Connection](#the-aps-assignment-connection)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Key Components Explained](#key-components-explained)
- [The 10 Government Schemes Covered](#the-10-government-schemes-covered)
- [Running the Application](#running-the-application)
- [Running the Tests](#running-the-tests)
- [ML Training Pipeline](#ml-training-pipeline)
- [Design Decisions & Guardrails](#design-decisions--guardrails)
- [Limitations & Future Work](#limitations--future-work)

---

## What Is This Project?

This is a **two-stage intelligent recommendation system** that helps smallholder farmers in Karnataka, India discover and apply for government subsidies and welfare schemes they are legally eligible for.

The system combines:

1. **A deterministic eligibility rule engine** — verifies legal qualification using official government guidelines with zero hallucination risk.
2. **A trained ML relevance ranker (Benchmark v1.2)** — ranks eligible schemes by how relevant they are to the farmer's specific, immediate need using a `HistGradientBoostingRegressor` model trained on 90 human-expert-annotated scenarios (369 scheme-farmer pairs).
3. **A Streamlit web interface** — makes the entire pipeline accessible to agricultural extension officers (AEOs) and field workers at Raitha Samparka Kendras (RSK).

> **Academic Disclaimer:** All demo profiles are synthetic benchmark scenarios for research demonstration. Recommendations do not constitute legal guarantee of subsidy sanction.

---

## The Real Problem It Solves

Imagine Basavaraj, a Scheduled Caste farmer with 3 acres of rainfed cotton in Raichur district. Pink bollworm has devastated his crop. He needs financial relief — **now**.

The reality he faces:

| Farmer's World | Government Portal World |
|---|---|
| "My cotton crop failed — what help can I get?" | "Scheme: PMFBY (Pradhan Mantri Fasal Bima Yojana), Budget Head 2401-00..." |
| Works in the field all day, no gazette access | 48-page PDF guidelines indexed by department budget codes |
| Visits RSK office and may be told about 1 scheme or none | 10+ overlapping schemes, unclear which applies to him |
| Needs to know if portal is open **today** | Seasonal cut-off dates buried in circulars |

**This system bridges that gap** by:
- Evaluating all 10 government schemes (16 implementation records) automatically against his profile
- Explaining **why** each scheme is eligible or ineligible using exact rule keys
- Ranking the eligible schemes by urgency and relevance to his stated need
- Separating schemes available **right now** from those needing timing verification

---

## How It Was Developed — Phase by Phase

### Phase 1 — Problem Research & Data Curation

**What was done:** Researched 10 government agricultural schemes from official Karnataka and Central government portals (`.gov.in`, `.nic.in`). Each scheme was documented in a structured 31-column schema capturing eligibility rules, land boundaries, social category requirements, benefit rates, and official source URLs.

**Key output:** `scheme_database/build_scheme_master.py` — a deterministic script generating:
- 16 individual raw JSON scheme files in `scheme_database/raw/`
- A consolidated `scheme_master.json` consumed by the engine
- A formatted `scheme_master.xlsx` for human audit

**Why 16 records for 10 schemes?** Two schemes (Agricultural Credit — `SCH008`, and Ganga Kalyana — `SCH010`) are umbrella programmes with multiple implementation channels routed through different corporations (Ambedkar, Valmiki, Devaraj Urs, KMDC). Each channel has distinct eligibility criteria, so they are modelled as parent + child records.

---

### Phase 2 — Deterministic Eligibility Engine

**What was done:** Built `src/eligibility/engine.py` — a pure Python deterministic rule engine that evaluates any farmer's profile against all 16 scheme records and returns one of three statuses per scheme:

| Status | Meaning |
|---|---|
| `ELIGIBLE` | All statutory constraints satisfied |
| `INELIGIBLE` | At least one hard constraint violated (with exact rule key and reason) |
| `REQUIRES_VERIFICATION` | A critical attribute is unknown and cannot be assumed |

**The key innovation — Three-Valued Logic:**  
Standard code uses `True`/`False`. If a farmer doesn't know whether their family paid income tax, you cannot assume `False` (would approve an ineligible person) or `True` (would deny a qualifying farmer). The engine uses `None` → `REQUIRES_VERIFICATION`, identifying the exact missing document required.

**Parent deduplication:** When both `SCH010` (Ganga Kalyana umbrella) and `SCH010_AMBEDKAR` (the specific SC implementation) are eligible, the abstract parent is suppressed from output — only the actionable child is shown to the farmer.

---

### Phase 3 — Availability Filter

**What was done:** Built `src/eligibility/availability.py` — a decoupled second gate that checks whether an eligible scheme is currently accepting applications.

Statutory eligibility (fixed by gazette) ≠ administrative availability (changes seasonally). A farmer may legally qualify for PMFBY but be unable to apply because the Kharif cut-off date passed last week.

Four availability states:
1. **Verified Available Now** — active portal, dated circular, official URL
2. **Eligible but Currently Closed** — seasonal window closed
3. **Upcoming (Confirmed Date)** — officially announced opening date
4. **Availability Unknown** — verification required at RSK/bank

**Guardrail:** A scheme cannot enter "Verified Available Now" without all three: active status + official notice URL + verified publication date.

---

### Phase 4 — Benchmark Design & Pilot Scenarios (S001–S010)

**What was done:** Designed 10 pilot scenarios (`S001`–`S010`) spanning Karnataka's 10 agro-climatic zones, diverse social categories, land profiles, and immediate needs. These scenarios were:
- Executed through the eligibility engine to produce `research/dataset_research/pilot_execution_results.json`
- Used to validate negative boundary cases (tax exclusion, grid borewell exclusion, 7-year lock-in)
- Frozen as `Benchmark v1.0.4` — the calibration pilot used to test annotation infrastructure

**Key negative boundary tests proven:**
- **S007:** Income tax payment correctly disqualifies only PM-KISAN, not other schemes
- **S008:** Grid-connected borewell correctly disqualifies only PM-KUSUM Component B
- **S009:** General Merit farmers correctly rejected by all four corporation Ganga Kalyana routes
- **S010:** Prior PMKSY subsidy within 7 years correctly triggers lock-in disqualification

---

### Phase 5 — Expert Annotation Protocol & Inter-Rater Reliability

**What was done:** Built a two-phase human annotation pipeline to collect ground truth relevance labels (0–3 scale) from agricultural domain experts.

- **Phase 1 (Blind):** Experts score each eligible scheme's relevance without seeing availability status, preventing portal closure from biasing relevance scores.
- **Phase 2:** Availability revealed; experts confirm actionability.

**Inter-rater reliability metrics implemented** (`scripts/compute_agreement.py`):

| Metric | Purpose |
|---|---|
| Krippendorff's Alpha (ordinal) | Primary: corrects for chance, penalizes large disagreements |
| Quadratic Weighted Cohen's Kappa | Pairwise agreement with ordinal distance penalty |
| Kendall's W | Whether experts agree on relative ranking order |
| Fleiss' Kappa | Conservative nominal lower-bound check |

---

### Phase 6 — Benchmark v1.2 ML Training

**What was done:** Expanded benchmark to 90 scenarios (S011–S070 across Zones Z1–Z10, plus supplementary scenarios), producing 369 annotated scheme-farmer pairs. Trained and evaluated a `HistGradientBoostingRegressor` model.

**Training script:** `scripts/train_benchmark_v1_2_ranker.py`

**Evaluation protocol:**
- SHA-256 checksum verification of frozen annotation file before training
- 5-fold GroupKFold cross-validation (grouped by `scenario_id` to prevent data leakage)
- LOZO (Leave-One-Zone-Out) evaluation — tests generalization across agro-climatic zones
- Crisis-type holdout (`SOIL_HEALTH_AND_FERTILIZER` — largest group)
- Land-tenure holdout (`is_pure_tenant_without_land_title=True`)
- Scenario-level 20% holdout
- Heuristic baseline comparison on identical candidate sets

**Model artifact:** `data/benchmarks/v1.2/ml_experiment/model_v1.2.0.joblib`

---

### Phase 7 — Web Application (Streamlit UI)

**What was done:** Built `app.py` — a full Streamlit web application integrating all components.

**Application flow:**
1. Farmer (or field officer) fills in profile: district, social category, land size, crop, assets, immediate need, statutory flags
2. System runs the frozen eligibility engine across all 16 scheme records
3. Applies governance safeguards → Section A (actionable, ML-ranked) vs Section B (advisory, pending verification)
4. Section A candidates ranked by the v1.2 ML model (or heuristic baseline fallback if model unavailable)
5. Each recommendation card shows: rank, score, department, benefit rate, required documents, statutory disclaimer, and official source link

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FARMER INPUTS (Streamlit UI / app.py)                 │
│   District · Social Category · Land · Crop · Assets · Immediate Need    │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              DESK 1: DETERMINISTIC ELIGIBILITY ENGINE                    │
│              src/eligibility/engine.py                                   │
│                                                                         │
│  • Evaluates all 16 scheme records                                       │
│  • Three-valued logic: ELIGIBLE / INELIGIBLE / REQUIRES_VERIFICATION    │
│  • Fires exact rule keys for every decision                              │
│  • Deduplicates abstract parent records (SCH008, SCH010)                │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              GOVERNANCE SAFEGUARD PIPELINE                               │
│              src/eligibility/governance.py                               │
│                                                                         │
│  Section A: Eligible + Verified → numerical ML ranking allowed          │
│  Section B: Provisional / Requires Verification → advisory only          │
│  Disqualified: Hard rule violation → reason + rule keys shown           │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │ Section A candidates only
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              DESK 2: BENCHMARK v1.2 ML RANKER                           │
│              src/models/benchmark_v1_2/ranker.py                        │
│                                                                         │
│  • HistGradientBoostingRegressor trained on 369 annotated pairs         │
│  • Features: farmer context + scheme metadata + need×scheme interaction  │
│  • Predicts relevance score (0–3 scale)                                 │
│  • Fallback: registered heuristic baseline if model unavailable         │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              RANKED RECOMMENDATION CARDS                                 │
│                                                                         │
│  #1 PMFBY — Score: 2.84  (Directly targets: CROP_INSURANCE need)        │
│  #2 PM-KISAN — Score: 2.11  (General income support)                    │
│  #3 KCC-MISS — Score: 1.73  (Production credit)                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## The APS Assignment

This project is directly connected to and fulfills the **APS (Algorithm and Problem Solving / Applied Probabilistic Systems) assignment** requirements. Here's exactly how:

### What the Assignment Required

The APS assignment required demonstrating the application of probability, statistics, and algorithmic problem-solving to a real-world domain problem, including:

1. **Probabilistic modelling and statistical analysis**
2. **Algorithm design and complexity reasoning**
3. **Data-driven decision making**
4. **Evaluation methodology with statistical rigor**

### How This Project Fulfills Each Requirement

#### 1. Probabilistic Modelling — The Relevance Scoring Problem

The core ML problem is formulated as a **supervised ordinal regression / ranking problem**:

$$P(Y = k \mid x) \quad \text{where } k \in \{0, 1, 2, 3\}$$

Each scheme-farmer pair $(x_{farmer}, x_{scheme}, x_{cross})$ is assigned a relevance label $y \in \{0, 1, 2, 3\}$ by human experts. The `HistGradientBoostingRegressor` learns a continuous approximation of this distribution, predicting the expected relevance score for any new pair.

The **three-valued logic** (`ELIGIBLE` / `INELIGIBLE` / `REQUIRES_VERIFICATION`) is itself a form of probabilistic reasoning under incomplete information — a core APS topic:
- Unknown attribute → Do not assume a probability; flag as requiring evidence.
- This prevents Type I errors (approving ineligible farmers) and Type II errors (denying eligible farmers).

#### 2. Statistical Analysis — Inter-Rater Reliability

The annotation pipeline (`scripts/compute_agreement.py`) implements full statistical inter-rater reliability analysis — a direct APS assignment topic:

**Krippendorff's Alpha** with ordinal distance metric:
$$\alpha = 1 - \frac{D_o}{D_e}$$

Where $D_o$ is observed disagreement and $D_e$ is expected disagreement by chance. The ordinal distance function penalizes large disagreements quadratically:
- Disagreement between Score 3 and Score 2: penalty = $(3-2)^2 = 1$
- Disagreement between Score 3 and Score 0: penalty = $(3-0)^2 = 9$

**Quadratic Weighted Cohen's Kappa** for pairwise annotator agreement:
$$w_{ij} = 1 - \frac{(i - j)^2}{(k-1)^2}$$

**Kendall's Coefficient of Concordance (W)** for multi-rater ranking agreement.

These are not trivial applications — they represent rigorous statistical methodology applied to a real annotation dataset.

#### 3. Algorithm Design — The Eligibility Engine

The eligibility engine (`src/eligibility/engine.py`) demonstrates classical **algorithm design principles**:

- **Decision Trees as Code:** Each scheme's evaluation is a structured boolean decision tree with deterministic branching based on farmer attributes.
- **Three-Valued Logic (Kleene Logic):** Implements a formal extension of boolean logic to handle incomplete information — a direct theoretical APS topic.
- **Deduplication Algorithm:** `resolve_actionable_determinations()` uses set operations to suppress abstract parent records when children are actionable:

```python
# O(n) algorithm where n = number of determinations
child_parents_with_actionable_children = set()
for d in determinations:
    if d.record_type == "CHILD" and d.status in ACTIONABLE_STATUSES:
        child_parents_with_actionable_children.add(d.parent_scheme_id)

actionable = [d for d in determinations
              if not (d.record_type == "PARENT"
                      and d.scheme_id in child_parents_with_actionable_children)]
```

#### 4. Machine Learning Evaluation — NDCG and Ranking Metrics

The ML evaluation (`src/evaluation/metrics.py`) implements **Normalized Discounted Cumulative Gain (NDCG@K)** — a standard information retrieval ranking metric directly relevant to APS:

$$\text{NDCG@K} = \frac{\text{DCG@K}}{\text{IDCG@K}}$$
$$\text{DCG@K} = \sum_{i=1}^{K} \frac{2^{rel_i} - 1}{\log_2(i + 1)}$$

Where $rel_i$ is the relevance score of the item ranked at position $i$. NDCG@3 measures whether the three most relevant schemes are placed at the top — the real-world test of recommendation quality.

The evaluation also implements **Mean Reciprocal Rank (MRR)** and **paired permutation tests** for statistical significance of ML vs heuristic baseline comparisons.

#### 5. The Notebook — `subsidy_probability_statistics_assignment.ipynb`

The Jupyter notebook `notebooks/subsidy_probability_statistics_assignment.ipynb` is the dedicated APS assignment deliverable. It provides:

- **Exploratory Data Analysis** of the scheme dataset and annotation distributions
- **Statistical visualizations** of annotator agreement patterns
- **Probability distributions** of relevance scores across need types and crop categories
- **Comparative analysis** of ML model vs heuristic baseline across all evaluation protocols
- **Formal mathematical derivations** of the metrics used

This notebook is the direct submission artifact for the APS assignment, showing the statistical reasoning behind every design decision in this project.

#### 6. Benchmark v1.2 Preregistration — Scientific Rigor

The evaluation was **preregistered** (`research/dataset_research/benchmark_v1.2_evaluation_preregistration.md`) before training, specifying all evaluation protocols, metrics, and holdout strategies in advance. This mirrors the APS principle of designing experiments before observing results to prevent p-hacking.

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Core Language | Python 3.10+ | All modules |
| Web UI | Streamlit | Interactive farmer input and recommendation display |
| ML Model | scikit-learn `HistGradientBoostingRegressor` | Relevance ranking |
| Data Engineering | Pandas, NumPy | Feature construction, annotation processing |
| Scheme Database | JSON, CSV, Excel (openpyxl) | Scheme registry storage |
| Model Serialization | joblib | Trained model artifact persistence |
| Testing | pytest | 208-test automated suite |
| Statistical Analysis | scipy, krippendorff | Inter-rater reliability computation |
| Notebooks | Jupyter | APS assignment analysis and visualization |

---

## Repository Structure

```
farmer-benefit-ml/
├── app.py                                    # Streamlit web application
├── README.md                                 # This file
│
├── scheme_database/                          # Government scheme data registry
│   ├── build_scheme_master.py                # Generates all scheme data files
│   ├── scheme_master.xlsx                    # Human-readable 31-column audit sheet
│   ├── raw/                                  # 16 individual scheme JSON files
│   │   ├── SCH001_PM_KISAN.json
│   │   ├── SCH002_PMFBY.json
│   │   ├── SCH003_PMKSY_PDMC.json
│   │   ├── SCH004_SMAM.json
│   │   ├── SCH005_Krishi_Bhagya.json
│   │   ├── SCH006_PM_KUSUM_B.json
│   │   ├── SCH007_MIDH.json
│   │   ├── SCH008_KCC_MISS.json              # Parent: Agricultural Credit
│   │   ├── SCH008_CENTRAL_KCC_MISS.json      # Child: Central commercial bank route
│   │   ├── SCH008_KA_COOP_Zero_Interest.json # Child: Karnataka PACS/DCCB route
│   │   ├── SCH009_Soil_Health_Card.json
│   │   ├── SCH010_Ganga_Kalyana.json         # Parent: Ganga Kalyana umbrella
│   │   ├── SCH010_AMBEDKAR_Ganga_Kalyana.json # Child: SC farmers
│   │   ├── SCH010_VALMIKI_Ganga_Kalyana.json  # Child: ST farmers
│   │   ├── SCH010_DEVARAJ_URS_Ganga_Kalyana.json # Child: OBC farmers
│   │   └── SCH010_KMDC_Ganga_Kalyana.json    # Child: Religious minorities
│   └── processed/
│       ├── scheme_master.json                # Engine-consumed consolidated registry
│       ├── scheme_master.csv                 # Tabular inspection format
│       └── scheme_availability_template.csv  # Availability tracking template
│
├── src/
│   ├── eligibility/
│   │   ├── models.py                         # FarmerScenario, SchemeDetermination, Enums
│   │   ├── engine.py                         # Deterministic rule engine (87% test coverage)
│   │   ├── availability.py                   # 4-state availability filter (84% test coverage)
│   │   └── governance.py                     # Section A/B/Disqualified partitioning
│   ├── models/
│   │   └── benchmark_v1_2/
│   │       └── ranker.py                     # ML ranker, feature engineering, heuristic baseline
│   ├── evaluation/
│   │   ├── metrics.py                        # NDCG@K, MRR, permutation tests
│   │   └── benchmark_candidates.py           # Frozen 283-pair Section A candidate sets
│   └── app/
│       ├── service.py                        # End-to-end recommendation service
│       └── demo_profiles.py                  # District→Zone mapping, synthetic presets
│
├── tests/                                    # 208-test automated test suite
│   ├── test_eligibility_engine.py            # 56 unit & integration tests
│   ├── test_benchmark_matrix.py              # 11 benchmark validation tests
│   ├── test_zone_z1_scenarios.py             # (×10 zones) Zone-specific scenario tests
│   ├── test_benchmark_annotation_packets.py  # 5 annotation integrity tests
│   ├── test_evaluation_metrics.py            # 13 metric validation tests
│   ├── test_ingest_benchmark_annotations.py  # 8 ingestion pipeline tests
│   └── test_compute_benchmark_agreement.py   # 13 agreement computation tests
│
├── scripts/
│   ├── train_benchmark_v1_2_ranker.py        # ML training & evaluation script
│   ├── run_pilot_execution.py                # Runs S001–S010 through engine
│   ├── run_annotation_session.py             # 2-phase expert annotation CLI
│   ├── compute_agreement.py                  # Krippendorff's Alpha, Kappa, Kendall's W
│   └── smoke_test_agreement_pipeline.py      # End-to-end pipeline verification
│
├── notebooks/
│   └── subsidy_probability_statistics_assignment.ipynb  # APS Assignment notebook
│
├── research/dataset_research/
│   ├── case_b_scenario_spec.md               # 90-scenario benchmark design spec
│   ├── expert_annotation_form.md             # Annotation instrument for experts
│   ├── pilot_execution_results.json          # S001–S010 engine output
│   ├── pilot_execution_report.md             # Detailed pilot audit report
│   ├── benchmark_v1.2_evaluation_preregistration.md  # Pre-registered evaluation protocol
│   └── annotation_protocol_v1.1.md           # Expert annotation standard operating procedure
│
├── data/
│   ├── annotations/                          # Expert annotation JSON files
│   └── benchmarks/v1.2/ml_experiment/
│       └── model_v1.2.0.joblib               # Trained ML model artifact
│
└── docs/
    ├── architecture.md
    ├── data_dictionary.md
    ├── ml_formulation.md
    └── problem_statement.md
```

---

## Key Components Explained

### The Eligibility Engine (`src/eligibility/engine.py`)

The heart of the system. For each scheme, a dedicated evaluation method (`_eval_pm_kisan`, `_eval_pmfby`, etc.) checks every statutory constraint in sequence and either:
- Adds a **rule key** (e.g., `PMKISAN_MTS_EXEMPTION_APPLIED`) to the passed-rules list
- Adds a **disqualifying factor** with human-readable explanation to the disqualified list

When any disqualifying factor is added, the scheme status is set to `INELIGIBLE`. When a required attribute is `None`, status is set to `REQUIRES_VERIFICATION` with the specific missing document listed.

### The ML Ranker (`src/models/benchmark_v1_2/ranker.py`)

Built around scikit-learn's `HistGradientBoostingRegressor` (handles missing values natively, suited for small datasets). Features include:

| Feature Category | Examples |
|---|---|
| Farmer context | `land_size_acres`, `agro_climatic_zone_encoded`, `social_category_encoded` |
| Scheme metadata | `benefit_type_encoded`, `subsidy_rate_category`, `record_type_encoded` |
| Need × scheme interaction | `need_matches_benefit_type` (binary), `crop_is_notified` |
| Ablation flag | `ablation=1` (includes `immediate_need`), `ablation=2` (excludes it) |

### The Governance Safeguard (`src/eligibility/governance.py`)

Implements strict separation between:
- **Section A** — statistically reliable recommendations eligible for ML ranking and numerical scoring
- **Section B** — advisory items where statutory documentation is pending (e.g., provisional annual Government Orders, succession certificates)

Numerical scoring is **strictly disabled** for Section B to prevent the UI from presenting an uncertain item with a misleading confidence score.

---

## The 10 Government Schemes Covered

| ID | Scheme | Benefit | Key Eligibility Rule |
|---|---|---|---|
| SCH001 | PM-KISAN | ₹6,000/year direct transfer | Non-income-tax-payer; land title pre-Feb 2019 |
| SCH002 | PMFBY | Subsidized crop insurance | Notified crop in notified unit |
| SCH003 | PMKSY-PDMC | Up to 90% micro-irrigation subsidy | Operational water source; 7-year lock-in |
| SCH004 | SMAM | Farm machinery subsidy | No machinery subsidy in past 5 years |
| SCH005 | Krishi Bhagya | Farm pond + drip package | Dryland (rainfed) only |
| SCH006 | PM-KUSUM B | Solar pump subsidy | Off-grid borewell only (grid-connected excluded) |
| SCH007 | MIDH | Protected horticulture subsidy | Horticultural crop with micro-irrigation |
| SCH008 | KCC / Crop Credit | Subsidized production credit | Via commercial bank or PACS/DCCB |
| SCH009 | Soil Health Card | Free soil testing | Universal — no eligibility barrier |
| SCH010 | Ganga Kalyana | Free borewell + irrigation | SC/ST/OBC/Minority only; corporation-specific land rules |

---

## Running the Application

### Prerequisites

```bash
pip install -r requirements.txt
```

### Launch the Streamlit Web App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`. Use the sidebar presets to load synthetic benchmark scenarios instantly, or fill in a custom farmer profile manually.

**If the ML model is available** at `data/benchmarks/v1.2/ml_experiment/model_v1.2.0.joblib`, the app shows:
> ✅ **Benchmark v1.2 ML Ranker Active**

**If not available**, it falls back to the registered heuristic baseline automatically:
> ⚠️ **Heuristic Fallback Active**

---

## Running the Tests

```bash
pytest tests/ -v
```

Expected output: **208 tests passed** in under 3 seconds.

To see code coverage:

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

| Module | Coverage |
|---|---|
| `src/eligibility/models.py` | 92% |
| `src/eligibility/engine.py` | 87% |
| `src/eligibility/availability.py` | 84% |
| Overall | 88% |

> [!NOTE]
> 88% line coverage proves internal code consistency with encoded rules. It does **not** prove that the underlying Karnataka government policies are currently in force or legally complete.

---

## ML Training Pipeline

To reproduce the Benchmark v1.2 model training:

```bash
python scripts/train_benchmark_v1_2_ranker.py
```

This script:
1. Verifies the SHA-256 checksum of the frozen annotation file before loading
2. Validates annotation-to-candidate-set alignment (no leakage)
3. Trains the `HistGradientBoostingRegressor` on 369 pairs
4. Runs all 6 evaluation protocols (5-fold CV, LOZO, crisis holdout, tenure holdout, scenario holdout, baseline comparison)
5. Saves the model artifact and full evaluation report

> [!IMPORTANT]
> The training data consists of 90 scenarios annotated by a single human reviewer. This is a small dataset. Results are exploratory; the model should not be deployed in production without multi-expert annotation achieving Krippendorff's Alpha ≥ 0.70.

---

## Design Decisions & Guardrails

### Why Not Use an LLM for Eligibility?

A Large Language Model can hallucinate eligibility criteria, miss statutory cut-off dates (e.g., PM-KISAN's February 1, 2019 land title cut-off), and produce non-deterministic outputs. A farmer promised a ₹2,00,000 subsidy that is legally rejected causes immediate financial harm. The deterministic engine guarantees zero policy hallucination.

### Why Separate Eligibility from Availability?

Statutory eligibility is defined by government gazettes and changes rarely. Administrative availability (application windows, seasonal cut-off dates, portal opening notices) changes every season. Conflating them would cause closed schemes to appear as available, misleading farmers.

### Why Three-Valued Logic?

Unknown ≠ False. If a farmer doesn't know their income tax status, assuming they are not a taxpayer would approve an ineligible applicant. The third value (`REQUIRES_VERIFICATION`) identifies the exact document needed without making an assumption.

### Why Suppress Parent Scheme Records?

Showing both `SCH010` (Ganga Kalyana umbrella) and `SCH010_AMBEDKAR` (the SC corporation route) would present two recommendation cards for the same borewell programme. The deduplication logic ensures only actionable, concrete implementation routes are shown.

---

## Limitations & Future Work

| Limitation | Current State | Planned Remediation |
|---|---|---|
| Availability data | Template unpopulated; all schemes default to "Unknown" | Populate with current Karnataka portal circulars |
| Single annotator | v1.2 trained on one reviewer's labels | Conduct independent E1 & E2 annotation sessions (Protocol v1.1) |
| Small training set | 90 scenarios, 369 pairs | Expand to 200+ scenarios across all zones |
| No farmer-facing UI localization | English only | Build Kannada string resource catalog |
| No live portal monitoring | Static scheme data | Design headless Seva Sindhu / Samrakshane scraper |
| Hardcoded rules in Python | Rules embedded in `engine.py` | Refactor to declarative JSON/YAML rule cards |
| No mobile / IVR interface | Desktop web only | Build mobile-first UI for field officers |

---

## Citation & Acknowledgements

Government scheme data sourced from official portals:
- [pmkisan.gov.in](https://pmkisan.gov.in/) — PM-KISAN
- [pmfby.gov.in](https://pmfby.gov.in/) — PMFBY
- [pmkusum.mnre.gov.in](https://pmkusum.mnre.gov.in/) — PM-KUSUM
- [agricoop.nic.in](https://agricoop.nic.in/) — SMAM, PMKSY
- [hortnet.gov.in](https://hortnet.gov.in/) — MIDH
- Karnataka State Government portals: Samrakshane, FRUITS, Seva Sindhu

All eligibility rules are derived from official published guidelines. This is an academic research project; recommendations do not constitute legal advice or guarantee of subsidy sanction.
