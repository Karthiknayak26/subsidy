# Complete Project Audit and Beginner-to-Advanced Teaching Guide

## Project: ML-Based Personalized Government Scheme and Subsidy Recommendation System for Farmers

[![Status: Phase 1/2 Benchmark Freeze](https://img.shields.io/badge/Status-Phase_1%2F2:_Benchmark_Freeze_v1.0-blue.svg)](#part-11--repository-audit-status-matrix--gap-analysis)
[![Tests: 56 Passing](https://img.shields.io/badge/Tests-56_Passed_(88%25_Coverage)-brightgreen.svg)](#part-8--automated-test-suite--code-coverage-audit)
[![Architecture: Decoupled Filter-Ranker](https://img.shields.io/badge/Architecture-Decoupled_Rule_Engine_%2B_Availability_%2B_ML_Ranker-orange.svg)](#part-3--repository-architecture-reconstruction)
[![Ground Truth: Verified Official Sources](https://img.shields.io/badge/Ground_Truth-Official_Gazette_%26_Govt_Portals-darkgreen.svg)](#part-4--data-pipeline-trace-from-raw-data-to-registry)

---

## Master Table of Contents

- [Part 1 — Audit Ground Rules & Evidence Classification](#part-1--audit-ground-rules--evidence-classification)
- [Part 2 — The Project Explained from Zero](#part-2--the-project-explained-from-zero)
- [Part 3 — Repository Architecture Reconstruction](#part-3--repository-architecture-reconstruction)
- [Part 4 — Data Pipeline Trace: From Raw Data to Registry](#part-4--data-pipeline-trace-from-raw-data-to-registry)
- [Part 5 — The Deterministic Eligibility Engine Explained from Scratch](#part-5--the-deterministic-eligibility-engine-explained-from-scratch)
- [Part 6 — The Availability Pipeline & Evidence Guardrails](#part-6--the-availability-pipeline--evidence-guardrails)
- [Part 7 — Pilot Scenarios S001–S010 Audit & Negative Boundary Analysis](#part-7--pilot-scenarios-s001s010-audit--negative-boundary-analysis)
- [Part 8 — Automated Test Suite & Code Coverage Audit](#part-8--automated-test-suite--code-coverage-audit)
- [Part 9 — The Expert Annotation Protocol & Inter-Rater Reliability](#part-9--the-expert-annotation-protocol--inter-rater-reliability)
- [Part 10 — Where Machine Learning Fits (And What Is Deferred)](#part-10--where-machine-learning-fits-and-what-is-deferred)
- [Part 11 — Repository Audit: Status Matrix & Gap Analysis](#part-11--repository-audit-status-matrix--gap-analysis)
- [Part 12 — Complete End-to-End Scenario Walkthrough (S001 Full Trace)](#part-12--complete-end-to-end-scenario-walkthrough-s001-full-trace)
- [Part 13 — Technical Glossary (Tailored to This Codebase)](#part-13--technical-glossary-tailored-to-this-codebase)
- [Part 14 — Staged Learning Roadmap](#part-14--staged-learning-roadmap)
- [Part 15 — Comprehensive Viva Voce Preparation (15 Defense Questions & Answers)](#part-15--comprehensive-viva-voce-preparation-15-defense-questions--answers)

---

## Part 1 — Audit Ground Rules & Evidence Classification

Every claim, rule, metric, and architectural component throughout this teaching guide is explicitly classified using one of five evidentiary labels:

- **`[Implemented]`**: Directly verified in executable Python modules, scripts, JSON records, or data files in the repository.
- **`[Tested]`**: Directly verified by an automated test in `tests/test_eligibility_engine.py` that executed and passed in the live environment.
- **`[Documented but unverified]`**: Recorded in Markdown documentation or project notes, but lacking programmatic enforcement or external legal confirmation.
- **`[Planned]`**: Outlined as a future deliverable in roadmaps or research specifications, with no working code or active data in the current codebase.
- **`[Potential issue]`**: A design risk, code omission, untested branch, policy assumption, or data gap requiring remediation.

> [!IMPORTANT]
> **Legal Validity vs. Software Consistency:** Passing all 56 automated unit tests proves that the Python code is *internally consistent with its encoded rules*. It does **not** prove that the underlying government policies are currently in force, legally complete, or free of unstated administrative circulars in Karnataka.

---

## Part 2 — The Project Explained from Zero

### 2.1 The Real-World Agricultural Problem
Imagine an Indian smallholder farmer named Basavaraj cultivating 3 acres of rainfed cotton in Raichur district, Karnataka. A severe pink bollworm infestation threatens his crop. Basavaraj urgently needs financial relief and risk compensation.

In the real world:
- He spends daylight hours in the field managing weeds, pests, and irrigation.
- He does not read the *Karnataka Gazette*, visit ministerial websites (`agricoop.nic.in`), or browse portals like *Samrakshane* or *Seva Sindhu*.
- When he visits the local agricultural office (Raitha Samparka Kendra - RSK) or a cooperative bank, he may be told about one specific scheme or none at all, depending on administrative awareness and quotas.
- He may pay out-of-pocket for drip irrigation pipes or crop insurance premiums, unaware that he qualifies for a 90% capital subsidy under PMKSY-PDMC or subsidized coverage under PMFBY.

Government portals index programmes by **administrative budget heads** (e.g., *"Centrally Sponsored Scheme for Micro-Irrigation Component B"*), whereas farmers express needs in **practical operational terms** (e.g., *"My borewell has no electricity connection; I need a solar pump"*).

```
   Farmer Reality                                Government Portal Reality
┌───────────────────────────┐                 ┌─────────────────────────────┐
│ "I need drip irrigation   │                 │ Department of Horticulture  │
│ for 2 acres of tomato.    │      GAP        │ Budget Head: 2401-00-119-01 │
│ What can I get?"          │ <=============> │ Guidelines: 48-page PDF     │
│ - No gazette awareness    │                 │ Index: Statutory scheme name│
│ - Constrained cash flow   │                 │ Form: FRUITS registration   │
└───────────────────────────┘                 └─────────────────────────────┘
```

### 2.2 The Non-Technical Analogy: The Hospital Triage Desk
Think of this project as a **two-desk hospital outpatient service**:
1. **Desk 1: Triage Nurse (Deterministic Eligibility Engine `[Implemented]`):**  
   The nurse checks objective constraints: age, blood group, vital signs, whether you have insurance, and whether you are allergic to penicillin. If you do not meet the strict criteria for a specific clinical trial, you cannot enter. The nurse **never guesses** or uses probabilities. If your blood pressure is unknown, the nurse does not guess it is normal; they order a blood pressure test (`REQUIRES_VERIFICATION`).
2. **Desk 2: Senior Specialist Doctor (Machine Learning Relevance Ranker `[Planned]`):**  
   From the set of 5 treatments you strictly qualify for, which one will best resolve your primary symptom today? The doctor uses contextual judgment and clinical experience (learned patterns) to rank the most relevant intervention at the top.

### 2.3 Answers to Foundational Architectural Questions

#### What exact problem is this project solving?
It bridges the information gap between complex, fragmented government agricultural schemes and individual farmers by evaluating statutory eligibility, isolating current operational availability, and ranking schemes by relevance to the farmer's immediate operational need.

#### Who is the intended user?
Primary beneficiaries are small, marginal, and marginalized farmers in Karnataka. Intermediate users include Agricultural Extension Officers (AEOs) at Raitha Samparka Kendras (RSK) and Krishi Vigyan Kendra (KVK) scientists counseling farmers.

#### What is the input?
A structured farmer scenario: location (district, agro-climatic zone), landholding (acres, rainfed vs. irrigated), crop, social category, existing assets (borewell type, pump, tractor), annual income, and an immediate stated need (`[Implemented]` in `src/eligibility/models.py`).

#### What is the output?
A deduplicated, explainable list of actionable schemes categorized into:
- *Verified Available Now* (active window with dated proof)
- *Timing or Verification Required* (eligible but closed, upcoming, or requiring documentation)
- *Ineligible* (with explicit disqualification reasons and fired rule keys)

#### Why is a static scheme catalogue insufficient?
A static list displays 50 schemes indiscriminately. A farmer cannot determine if their 3 acres exceed the 2-hectare cap, whether having a grid-connected borewell disqualifies them from solar pump assistance, or whether their crop is notified in their gram panchayat.

#### What distinguishes our system from a simple rule-based eligibility checker?
A simple rule checker answers only: *"Are you eligible? Yes/No."*  
A farmer might be eligible for 7 schemes simultaneously (e.g., PM-KISAN, PMFBY, Soil Health Card, SMAM, Krishi Bhagya, KCC Credit, Ganga Kalyana). An eligibility checker outputs all 7 indiscriminately. Our system introduces:
- Three-valued logic (`REQUIRES_VERIFICATION` for missing information)
- Decoupled administrative availability tracking
- Human-expert relevance ranking to prioritize the scheme that resolves the farmer's specific need

#### Why do we need Machine Learning if we already have an eligibility engine?
Statutory eligibility is a **hard filter**, not a **prioritization engine**. A farmer needing emergency pest compensation does not need a free Soil Health Card test as their primary recommendation, even though they strictly qualify for both. Machine learning is needed to rank the eligible subset based on contextual relevance, crop affinity, and urgency.

#### What makes this system trustworthy to an actual farmer?
1. **Zero Policy Hallucination:** Rules are deterministic Python functions derived from official `.gov.in` operational guidelines.
2. **Transparent Deduplication:** Abstract parent categories are suppressed in favor of concrete implementation routes.
3. **Traceability:** Every decision exposes the exact rule keys fired and official document links.

---

## Part 3 — Repository Architecture Reconstruction

### 3.1 Directory Tree
```
farmer-benefit-ml/
├── README.md                                  # Conceptual overview & roadmap [Documented]
├── document.md                                # Comprehensive 15-Part Technical Teaching Master [Implemented]
├── docs/                                      # Conceptual documentation [Documented]
│   ├── architecture.md
│   ├── data_dictionary.md
│   ├── ml_formulation.md
│   ├── problem_statement.md
│   └── project_scope.md
├── scheme_database/                           # Scheme Data Core [Implemented]
│   ├── build_scheme_master.py                 # Generates raw, processed & Excel files [Implemented]
│   ├── scheme_master.xlsx                     # Formatted 31-column master spreadsheet [Implemented]
│   ├── raw/                                   # 16 individual scheme JSON files [Implemented]
│   │   ├── SCH001_PM_KISAN.json
│   │   ├── SCH002_PMFBY.json
│   │   ├── SCH003_PMKSY_PDMC.json
│   │   ├── SCH004_SMAM.json
│   │   ├── SCH005_Krishi_Bhagya.json
│   │   ├── SCH006_PM_KUSUM_B.json
│   │   ├── SCH007_MIDH.json
│   │   ├── SCH008_KCC_MISS.json               # Parent record
│   │   ├── SCH008_CENTRAL_KCC_MISS.json       # Child record
│   │   ├── SCH008_KA_COOP_Zero_Interest.json  # Child record
│   │   ├── SCH009_Soil_Health_Card.json
│   │   ├── SCH010_Ganga_Kalyana.json          # Parent record
│   │   ├── SCH010_AMBEDKAR_Ganga_Kalyana.json # Child record
│   │   ├── SCH010_VALMIKI_Ganga_Kalyana.json  # Child record
│   │   ├── SCH010_DEVARAJ_URS_Ganga_Kalyana.json # Child record
│   │   └── SCH010_KMDC_Ganga_Kalyana.json     # Child record
│   └── processed/
│       ├── scheme_master.json                 # Consolidated 16-record JSON [Implemented]
│       ├── scheme_master.csv                  # Tabular 16-record CSV [Implemented]
│       └── scheme_availability_template.csv   # 25-column availability tracking template [Implemented]
├── src/                                       # Core Source Code [Implemented, Tested]
│   └── eligibility/
│       ├── __init__.py
│       ├── models.py                          # Data models, Enums, Scenarios [Implemented, Tested]
│       ├── engine.py                          # Deterministic eligibility engine [Implemented, Tested]
│       └── availability.py                    # 4-state availability filter [Implemented, Tested]
├── tests/                                     # Automated Test Suite [Implemented, Tested]
│   └── test_eligibility_engine.py             # 56 unit & integration tests [Tested]
├── research/dataset_research/                 # Research Benchmarking [Implemented]
│   ├── case_b_scenario_spec.md                # Case B benchmark specification [Implemented]
│   ├── case_b_scenario_spec_availability_updated.md
│   ├── dataset_inventory.md                   # Public data feasibility study [Implemented]
│   ├── expert_annotation_form.md              # 10-scenario pilot annotation instrument [Implemented]
│   ├── pilot_execution_results.json           # Raw JSON output of S001-S010 run [Implemented]
│   ├── pilot_execution_report.md              # Detailed audit report of pilot [Implemented]
│   ├── pilot_version_freeze.md                # Frozen benchmark state at commit 7724fa7 [Implemented]
│   └── pilot_coordinator_guide.md             # Standard Operating Procedure for study [Implemented]
├── scripts/                                   # Operational & Analysis CLI Scripts [Implemented]
│   ├── run_pilot_execution.py                 # Executes S001-S010 through engine [Implemented]
│   ├── generate_pilot_deliverables.py         # Generates Markdown deliverables [Implemented]
│   ├── run_annotation_session.py              # Interactive 2-phase CLI for experts [Implemented]
│   ├── compute_agreement.py                   # Computes Alpha, Kappa, Kendall, Fleiss [Implemented]
│   └── smoke_test_agreement_pipeline.py       # End-to-end verification script [Implemented]
├── data/
│   └── annotations/                           # Directory for expert responses [Planned - Currently Empty]
└── reports/                                   # Target directory for statistical outputs [Planned]
```

### 3.2 Deep-Dive Module Breakdown

```
+---------------------------------------------------------------------------------------------------------+
|                                    MODULE ARCHITECTURE AUDIT                                            |
+------------------------------+---------------------------+------------------------+---------------------+
| Module File                  | Inputs                    | Outputs / Modifies     | Status              |
+------------------------------+---------------------------+------------------------+---------------------+
| build_scheme_master.py       | Hardcoded python list of  | 16 raw JSONs,          | [Implemented]       |
|                              | 16 scheme dicts           | master.json, .csv,     | [Tested via build]  |
|                              |                           | scheme_master.xlsx     |                     |
|                              |                           |                        |                     |
| src/eligibility/models.py    | Raw dictionaries          | FarmerScenario,        | [Implemented]       |
|                              |                           | SchemeDetermination,   | [Tested: 92% cov]   |
|                              |                           | Enums                  |                     |
|                              |                           |                        |                     |
| src/eligibility/engine.py    | FarmerScenario,           | List[SchemeDetermination] [Implemented]       |
|                              | scheme_master.json        | with rule keys, status | [Tested: 87% cov]   |
|                              |                           | and disqualifications  |                     |
|                              |                           |                        |                     |
| src/eligibility/availability.py| SchemeDetermination list,| Enriched list with 4   | [Implemented]       |
|                              | availability CSV          | availability states,   | [Tested: 84% cov]   |
|                              |                           | presentation partitions|                     |
|                              |                           |                        |                     |
| scripts/compute_agreement.py | Expert JSON files         | AgreementMetrics,      | [Implemented]       |
|                              | in data/annotations/      | Krippendorff's alpha,  | [Tested via smoke]  |
|                              |                           | Weighted Kappa, tables |                     |
+------------------------------+---------------------------+------------------------+---------------------+
```

### 3.3 End-to-End System Flowchart

```
[ Stage 1: Offline Ground-Truth Data Curation ]
Official Gazettes & Portals (agricoop, pmkisan, fruits)
            │
            ▼
build_scheme_master.py ───┬───> scheme_master.json (10 Parents + 6 Children = 16 Records)
                          ├───> scheme_master.xlsx
                          └───> scheme_availability_template.csv (Administrative Windows)

[ Stage 2: Deterministic Eligibility Engine ]
Farmer Query Profile (District, Land, Crop, Category, Need)
            │
            ▼
FarmerScenario Dataclass (src/eligibility/models.py)
            │
            ▼
EligibilityEngine.evaluate_scenario() (src/eligibility/engine.py)
            │
            ├──> Evaluates hard statutory constraints
            ├──> Three-Valued Logic (ELIGIBLE / INELIGIBLE / REQUIRES_VERIFICATION)
            └──> resolve_actionable_determinations() (Suppresses Parents SCH008/SCH010)

[ Stage 3: Availability Filtering Gate ]
AvailabilityFilter.apply_availability() (src/eligibility/availability.py)
            │
            ├──> Matches open dates, notice URLs, and publication timestamps
            └──> Partitions: Verified Available Now / Timing & Verification Required / Ineligible

[ Stage 4: Human-in-the-Loop Benchmark ]
Eligible Candidate Pool
            │
            ▼
run_annotation_session.py (Two-Phase Blinded Protocol)
            │
            ├──> Phase 1: Blind to availability (Relevance Score 0 to 3)
            └──> Phase 2: Availability revealed (Actionability Confirmation)
            │
            ▼
compute_agreement.py (Krippendorff's alpha, Weighted kappa, Kendall's W)

[ Stage 5: Future ML Ranking & Localized Delivery (Planned) ]
Validated Training Benchmark (Alpha >= 0.70)
            │
            ▼
Learning-to-Rank Model (LambdaMART / GBDT Ranker)
            │
            ▼
Top-K Ranked Personalized Recommendations + Localized Kannada Delivery
```

---

## Part 4 — Data Pipeline Trace: From Raw Data to Registry

### 4.1 Scheme-Master Generation Process
The scheme registry is generated deterministically by `scheme_database/build_scheme_master.py`.

The build lifecycle follows this flow:
```
In-memory Python Curated Records (16 dicts)
                    │
                    ├──> 1. Writes 16 individual raw JSON files to scheme_database/raw/
                    │       (Preserves granular versioning and git diff traceability)
                    │
                    ├──> 2. Writes consolidated scheme_master.json to scheme_database/processed/
                    │       (Directly consumed by EligibilityEngine)
                    │
                    ├──> 3. Writes tabular scheme_master.csv to scheme_database/processed/
                    │       (For inspection and tabular analysis)
                    │
                    └──> 4. Generates formatted scheme_master.xlsx in scheme_database/
                            (Formatted for human audit with openpyxl styling)
```

#### Why Store Both Raw and Consolidated Files?
- **Granular Git Versioning:** If the operational rules for PMKSY-PDMC (`SCH003`) change in a future circular, editing that specific record produces a clean git diff in `raw/SCH003_PMKSY_PDMC.json` rather than an unwieldy diff across a monolithic 1,000-line JSON file.
- **Engine Ingestion Speed:** Loading a single consolidated `scheme_master.json` into memory on engine startup is an $O(1)$ single file read, rather than iterating through directory walks and parsing 16 separate files.

#### Validation & Referential Integrity
- **Script Validation Scope `[Implemented]`:** The script validates basic structure: tabular array length, field presence across all 31 columns, and CSV/JSON/Excel output consistency.
- **Policy Validation Limitation `[Potential issue]`:** The script **does not semantically validate policy rules**. It does not verify whether an official URL is live (returns HTTP 200) or check whether a stated subsidy percentage matches the current gazette. It is a data consolidation and formatting script, not an active government policy scraper.

### 4.2 The 16-Record Scheme Registry Architecture
The registry consists of **10 conceptual parent-level scheme IDs (`SCH001`–`SCH010`)** and **6 implementation-level child records**, totaling 16 records.

```
                                 [ SCHEME REGISTRY TAXONOMY ]
                                              │
              ┌───────────────────────────────┴───────────────────────────────┐
              ▼                                                               ▼
     STANDALONE SCHEMES (8)                                         PARENT SCHEMES (2)
  ┌─────────────────────────┐                                 ┌───────────────────────────────┐
  │ SCH001: PM-KISAN        │                                 │ SCH008: Credit Umbrella       │
  │ SCH002: PMFBY           │                                 │ SCH010: Ganga Kalyana Umbrella│
  │ SCH003: PMKSY-PDMC      │                                 └───────────────┬───────────────┘
  │ SCH004: SMAM            │                                                 │
  │ SCH005: Krishi Bhagya   │                                                 ▼
  │ SCH006: PM-KUSUM B      │                                      CHILD IMPLEMENTATIONS (6)
  │ SCH007: MIDH            │                                 ┌───────────────────────────────┐
  │ SCH009: Soil Health Card│                                 │ SCH008_CENTRAL (Commercial)   │
  └─────────────────────────┘                                 │ SCH008_KA_COOP (PACS/DCCB)    │
                                                              │ SCH010_AMBEDKAR (SC)          │
                                                              │ SCH010_VALMIKI (ST)           │
                                                              │ SCH010_DEVARAJ_URS (OBC)      │
                                                              │ SCH010_KMDC (Minorities)      │
                                                              └───────────────────────────────┘
```

#### Standalone Scheme vs. Conceptual Parent vs. Implementation Child

1. **Standalone Scheme Record:** A complete, self-contained programme whose implementing channel, guidelines, and funding operate as a single route (e.g., `SCH001` PM-KISAN, `SCH002` PMFBY).
2. **Conceptual Parent Record:** An abstract policy umbrella representing a general category of assistance. It cannot be applied for directly; application requires selecting a specific operational channel.
   - `SCH008` (Agricultural Credit): Represents production credit broadly.
   - `SCH010` (Ganga Kalyana): Represents free borewell and irrigation packages funded by the Karnataka government.
3. **Implementation Child Record:** The concrete operational route through which a parent programme is actually executed. It carries distinct eligibility criteria, funding channels, application portals, and audit statuses:
   - `SCH008_CENTRAL`: Central KCC-MISS via commercial banks (4% effective interest upon prompt repayment). Audit status: `VERIFIED_HISTORICAL_BASELINE`.
   - `SCH008_KA_COOP`: Karnataka Baddi Rahitha Bele Sala via PACS/DCCBs (0% interest up to ₹5 Lakh). Audit status: `PROVISIONAL_PENDING_ANNUAL_GO`.
   - `SCH010_AMBEDKAR`: Dr. B.R. Ambedkar Development Corporation (SC farmers: 1.5–5.0 ac individual; 8–15 ac with $\ge 3$ beneficiaries for community route).
   - `SCH010_VALMIKI`: Maharshi Valmiki ST Development Corporation (ST farmers).
   - `SCH010_DEVARAJ_URS`: D. Devaraj Urs Backward Classes Development Corporation (OBC Cat 1, 2A, 3A, 3B).
   - `SCH010_KMDC`: Karnataka Minorities Development Corporation (Religious minorities).
4. **Actionable Recommendation:** A scheme presented to a farmer with concrete application instructions. Conceptual parent records are suppressed when their children are actionable to prevent duplicate recommendation cards.

#### Foreign Key Linkage in the Scheme Database
In relational database design, a **Foreign Key** is an attribute in one table that links to the **Primary Key** of another table.

In our repository (`build_scheme_master.py` and `src/eligibility/models.py`):
```python
# Child Record:
{
    "scheme_id": "SCH010_AMBEDKAR",        # Primary Key of Child
    "record_type": "CHILD",
    "parent_scheme_id": "SCH010",          # Foreign Key linking to Primary Key of Parent
    ...
}
```
If a parent ID is misspelled (e.g., `SCH099`), referential integrity is violated. The engine's resolution logic checks this link:
```python
# If any child with parent_scheme_id == "SCH010" is actionable,
# suppress "SCH010" from final presentation.
```

### 4.3 Key Scheme Fields Schema Definition
The 31 standardized attributes defined in `scheme_database/README.md` serve distinct architectural roles:

| Field | Meaning in Plain English | Example from Repository | Used By | Important Caveat |
|---|---|---|---|---|
| `scheme_id` | Unique alphanumeric primary key | `"SCH001"`, `"SCH010_AMBEDKAR"` | Engine dispatch, Tests, UI tracking | Must remain stable across migrations; never altered dynamically. |
| `record_type` | Tier in scheme taxonomy | `"STANDALONE"`, `"PARENT"`, `"CHILD"` | Deduplication resolver (`engine.py`) | Abstract parents must not be directly recommended to farmers. |
| `parent_scheme_id` | Pointer to parent scheme | `"SCH010"` or `None` | Engine deduplication resolver | Acts as a foreign key; must match an existing parent ID. |
| `min_land` / `max_land` | Statutory landholding boundary constraints | `"> 0 acres"`, `"5.0 hectares (approx 12.35 acres)"` | Eligibility Engine (`_eval_*`) | Values vary between individual and community routes. |
| `social_category` | Target caste or demographic group | `"SC"`, `"ST"`, `"OBC"`, `"All"` | Ganga Kalyana routing, Subsidy rate tiers | S009 General Merit test confirms mismatch handling. |
| `existing_asset_requirements` | Mandatory presence or absence of farm infrastructure | `"Must possess an operational water pump set"` | Engine equipment gating | Presence of grid connection disqualifies PM-KUSUM B. |
| `upfront_benefit_support` | Guaranteed direct subsidy or interest subvention | `"Direct cash grant of Rs. 6,000 per annum in 3 installments"` | Presentation / UI explanation | Factual statutory benefit, distinct from contingent claims. |
| `contingent_benefit_clause` | Conditional indemnity payout triggered only by loss | `"Contingent Shortfall Indemnity Claim = Max(0, (TY - AY)/TY) * SI"` | Presentation disclaimer | **Never guaranteed**; applies to insurance (PMFBY). |
| `claim_disclaimer` | Mandatory warning against misinterpreting insurance as a grant | `"CLAIM INDEMNITY IS NEVER GUARANTEED..."` | UI presentation guardrail | Prevents farmer from assuming insurance guarantees cash. |
| `audit_status` | Verification standing of the scheme rules | `"VERIFIED"`, `"PROVISIONAL_PENDING_ANNUAL_GO"` | Eligibility disposition | Provisional status flags uncertain state credit routes. |
| `official_source_url` | Web link to authoritative government portal | `"https://pmkisan.gov.in/"` | UI, Expert Form, Traceability | Must be an official government domain (`.gov.in`, `.nic.in`). |

---

## Part 5 — The Deterministic Eligibility Engine Explained from Scratch

### 5.1 Deterministic Systems vs. Probabilistic Models
A **deterministic rule engine** is a software system where given an identical set of inputs, the output is guaranteed to be 100% identical and explainable every single time, executing formal boolean logic:
$$\text{Output} = f(\text{Inputs}) \quad \text{where } f \text{ is a closed, non-probabilistic logical function}$$

In contrast, a **probabilistic machine learning model** predicts an output based on statistical patterns and learned weights:
$$\hat{y} = \arg\max P(Y \mid X; \theta)$$

#### Why We Must Never Ask ML to Decide Statutory Eligibility:
1. **Hallucination Risk:** A neural network or language model might learn that "farmers with 15 acres usually get tractor subsidies" and approve an applicant who exceeds the legal 5-hectare cap.
2. **Lack of Legal Recourse:** A government official cannot accept: *"The random forest model output 0.82 probability of eligibility."* Eligibility requires statutory auditability: *"Applicant disqualified under Section 3(b) of PM-KISAN: monthly pension exceeds ₹10,000."*
3. **Zero Tolerance for False Approvals:** Misleading a farmer into purchasing equipment on a promised subsidy that is legally denied causes immediate financial harm.

### 5.2 Three-Valued Logic (`ELIGIBLE`, `INELIGIBLE`, `REQUIRES_VERIFICATION`)
In standard boolean computer logic, a variable is either `True` or `False`. If an attribute is missing, poorly written software often defaults it to `False`.

In welfare policy, **unknown information must not be assumed clean**:
- If a farmer does not know whether their family paid income tax, defaulting to `False` (tax not paid) would approve an ineligible applicant.
- Defaulting to `True` (tax paid) would unfairly deny a qualifying smallholder.

Our engine implements **Kleene Three-Valued Logic** (`src/eligibility/models.py`):
```
           ┌──────────────────────┐
           │ Value in Scenario    │
           └──────────┬───────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
      True          False         None / "UNKNOWN"
        │             │             │
        ▼             ▼             ▼
   [Evaluated]   [Evaluated]   REQUIRES_VERIFICATION
                                    │
                                    ▼
                         "Requires verification of
                          Form 16 / ITR assessment"
```

If an unknown input is encountered on a statutory exclusion, the engine sets status to `REQUIRES_VERIFICATION`, populates `missing_verifications`, and records the specific document required (`src/eligibility/engine.py:189-192`).

### 5.3 Detailed Scheme Rule Traces Through Code

#### Case 1: PM-KISAN (`SCH001`) — Statutory Exclusions & Exemptions
Located in `src/eligibility/engine.py:161-244`.

```
Farmer Profile Input:
  - land_size_acres: 3.0
  - is_pure_tenant_without_land_title: False
  - land_ownership_cutoff_pre_feb_2019: True
  - paid_income_tax_last_assessment_year: False
  - govt_employee_category: MTS_CLASS_IV_GROUP_D
  - superannuated_pensioner_monthly_amount: 14000.0
  - pensioner_is_mts_exempt: True
```
*Step-by-Step Code Evaluation:*
1. **Land Check:** `s.land_size_acres > 0` $\rightarrow$ Passes (`PMKISAN_LAND_SIZE_POSITIVE`).
2. **Tenancy Check:** `s.is_pure_tenant_without_land_title == False` $\rightarrow$ Passes.
3. **Cut-off Date:** `s.land_ownership_cutoff_pre_feb_2019 == True` $\rightarrow$ Passes (`PMKISAN_CUTOFF_DATE_VERIFIED`).
4. **Income Tax Check:** `s.paid_income_tax_last_assessment_year == False` $\rightarrow$ Passes (`PMKISAN_NO_INCOME_TAX_PAID`).
5. **Government Employee Category:** Matches `GovtEmployeeCategory.MTS_CLASS_IV_GROUP_D`.  
   *Code Branch:* While regular officers (`OFFICER_REGULAR`) are disqualified, line 211 fires:
   ```python
   elif s.govt_employee_category == GovtEmployeeCategory.MTS_CLASS_IV_GROUP_D:
       rules.append("PMKISAN_MTS_EXEMPTION_APPLIED")
   ```
   The statutory exclusion is bypassed.
6. **Pension Amount Check:** Pension is ₹14,000 ($\ge ₹10,000$). Normally disqualified, but line 219 checks:
   ```python
   if s.pensioner_is_mts_exempt:
       rules.append("PMKISAN_MTS_PENSION_EXEMPTION_APPLIED")
   ```
   Disqualification is prevented.
7. **Final Status:** `ELIGIBLE`.

#### Case 2: PM-KUSUM Component B (`SCH006`) — Grid Exclusion
Located in `src/eligibility/engine.py:378-409`.

```
Farmer Profile Input:
  - land_size_acres: 4.0
  - existing_assets: ["Borewell (Grid-connected)"]
  - borewell_electric_status: GRID_CONNECTED_IP_SET
```
*Step-by-Step Code Evaluation:*
1. **Land Check:** $4.0 \ge 0.5$ acres $\rightarrow$ Passes.
2. **Drilled Water Source:** `"Borewell (Grid-connected)"` is in assets $\rightarrow$ Passes (`KUSUM_B_WATER_SOURCE_PRESENT`).
3. **Grid Electric Status:** Line 394 executes:
   ```python
   if s.borewell_electric_status == BorewellElectricStatus.GRID_CONNECTED_IP_SET or "Borewell (Grid-connected)" in s.existing_assets:
       disq.append("Borewell already has an energized electric grid connection (DISCOM IP set). Component B strictly targets off-grid sources. (Related option to verify: PM-KUSUM Component C; not evaluated as an active benefit).")
       rules.append("KUSUM_B_GRID_CONNECTED_DISQUALIFIED")
   ```
4. **Final Status:** `INELIGIBLE`.  
   *Design Decision:* The engine does not automatically convert this into a recommendation for Component C, because Component C is an alternative route with separate feeder solarization rules that are not currently implemented.

#### Case 3: PMKSY-PDMC (`SCH003`) — Boundary & Lock-in Constraints
Located in `src/eligibility/engine.py:271-305`.

```
Farmer Profile Input:
  - land_size_acres: 3.0
  - existing_assets: ["Borewell (Grid-connected)", "Electric Pump Set"]
  - prior_micro_irrigation_subsidy_years_ago: 3.0
```
*Step-by-Step Code Evaluation:*
1. **Land Range:** $0.5 \le 3.0 \le 12.35$ acres ($0.2 \text{ ha} \le \text{area} \le 5.0 \text{ ha}$) $\rightarrow$ Passes (`PMKSY_LAND_RANGE_VALID`).
2. **Water Source:** Operational pump present $\rightarrow$ Passes (`PMKSY_WATER_SOURCE_VERIFIED`).
3. **Lock-In Verification:** Line 293 checks prior subsidy timing:
   ```python
   if s.prior_micro_irrigation_subsidy_years_ago is not None:
       if s.prior_micro_irrigation_subsidy_years_ago < 7.0:
           disq.append(f"Land parcel availed micro-irrigation subsidy {s.prior_micro_irrigation_subsidy_years_ago} years ago (7-year lock-in period applies).")
           rules.append("PMKSY_SEVEN_YEAR_LOCKIN_BREACHED")
   ```
4. **Final Status:** `INELIGIBLE`.

#### Case 4: Ganga Kalyana (`SCH010`) — Multi-Corporation Resolution
Located in `src/eligibility/engine.py:472-595`.

```
Farmer Profile Input:
  - social_category: "SC"
  - land_type: "Dryland (Rainfed)"
  - land_size_acres: 2.0
  - existing_assets: []
  - prior_ganga_kalyana_in_family: False
```
*Step-by-Step Code Evaluation:*
1. **Category Routing:** `_map_social_category_to_gk_child("SC")` returns `"SCH010_AMBEDKAR"`.
2. **Child Dispatch:** The engine evaluates child `SCH010_AMBEDKAR`.
3. **Corporation Land Boundary Rules (Ambedkar Corporation Specific):**  
   Lines 547–569 enforce published guidelines:
   - Individual Route: Requires $1.5 \le \text{acres} \le 5.0$. Since $2.0 \in [1.5, 5.0]$, line 560 fires: `rules.append("GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID")`.
   - Community Route (Alternative): Requires $8.0 \le \text{pooled acres} \le 15.0$ and $\text{beneficiaries} \ge 3$.
4. **Final Status:** `SCH010_AMBEDKAR` is `ELIGIBLE`.  
   Other corporation children (`SCH010_VALMIKI`, `SCH010_DEVARAJ_URS`, `SCH010_KMDC`) evaluate to `INELIGIBLE` due to category mismatch.

#### Case 5: PMFBY (`SCH002`) — Upfront Support vs. Contingent Indemnity
Located in `src/eligibility/engine.py:248-267`.

```
Farmer Profile Input:
  - primary_crop: "Cotton"
  - district: "Raichur"
  - land_size_acres: 3.0
```
*Step-by-Step Code Evaluation:*
1. **Notified Crop:** `"Cotton"` is in `NOTIFIED_PMFBY_CROPS` $\rightarrow$ Passes (`PMFBY_NOTIFIED_CROP_VERIFIED`).
2. **Benefit Representation Guardrail:** The engine output distinguishes:
   - `upfront_benefit_support`: Premium subsidy where farmer pays only statutorily capped rate (e.g., 2% for Kharif food/oilseeds, 5% for commercial crops like Cotton); government funds the balance actuarial premium.
   - `contingent_benefit_clause`: Claim indemnity payout triggered only if actual yield falls below threshold yield during crop cutting experiments (CCEs).
   - `claim_disclaimer`: *"CLAIM INDEMNITY IS NEVER GUARANTEED..."*

### 5.4 Deduplication of Abstract Parent Records
When `evaluate_scenario()` runs, both `SCH010` (parent) and `SCH010_AMBEDKAR` (child) evaluate to `ELIGIBLE`. Presenting both would show two separate cards for the same borewell programme.

Method `resolve_actionable_determinations` resolves this:
```python
child_parents_with_actionable_children = set()
for d in determinations:
    if d.record_type == "CHILD" and d.status in [EligibilityStatus.ELIGIBLE, EligibilityStatus.REQUIRES_VERIFICATION]:
        if d.parent_scheme_id:
            child_parents_with_actionable_children.add(d.parent_scheme_id)

actionable = []
for d in determinations:
    if d.record_type == "PARENT" and d.scheme_id in child_parents_with_actionable_children:
        continue  # Suppress abstract parent
    actionable.append(d)
```
*Result:* Abstract parents (`SCH008`, `SCH010`) are removed, leaving only concrete, actionable implementation records.

---

## Part 6 — The Availability Pipeline & Evidence Guardrails

### 6.1 Decoupling Statutory Eligibility from Operational Availability
- **Eligibility (Statutory Law):** *Does the farmer qualify under published government criteria?* (Changes rarely; defined by gazettes and scheme guidelines).
- **Availability (Administrative Reality):** *Is the portal accepting applications for this crop in this district today?* (Changes seasonally; subject to budget windows, portal opening dates, and district targets).

A farmer may be legally eligible for PMFBY, but if the seasonal cut-off date (e.g., July 31 for Kharif) passed two weeks ago, they cannot apply today.

### 6.2 The Four Discrete Availability States
Implemented in `src/eligibility/models.py` and `src/eligibility/availability.py`:

1. **`Verified available now`**: Application portal is actively accepting submissions, verified with a dated circular and official notice URL.
2. **`Eligible, but currently closed`**: The farmer statutorily qualifies, but the seasonal or annual application window has closed.
3. **`Upcoming, with an officially confirmed date`**: The scheme has an officially announced opening date in the future.
4. **`Availability unknown — confirmation required`**: The farmer qualifies, but no active notification is indexed. Farmers are directed to verify status at local offices (RSK/Bank).

### 6.3 Operational Availability Guardrail
Method `apply_availability` enforces an evidence gate:
```python
if app_status == "OPEN" and notice_url and pub_date:
    det.availability_state = AvailabilityState.VERIFIED_AVAILABLE_NOW
elif app_status == "CLOSED":
    det.availability_state = AvailabilityState.ELIGIBLE_BUT_CLOSED
elif app_status == "UPCOMING" and rec.get("application_open_date"):
    det.availability_state = AvailabilityState.UPCOMING_CONFIRMED
else:
    det.availability_state = AvailabilityState.AVAILABILITY_UNKNOWN
```

> [!IMPORTANT]
> **Strict Guardrail:** A scheme **cannot** enter `Verified available now` unless it has an active status, an official circular URL, and a published verification date. Because `scheme_availability_template.csv` is currently an unpopulated template, **all schemes in pilot runs safely default to `Availability unknown — confirmation required`**, preventing premature recommendations.

---

## Part 7 — Pilot Scenarios S001–S010 Audit & Negative Boundary Analysis

### 7.1 Scenario Design Matrix
Defined in `research/dataset_research/case_b_scenario_spec.md` and evaluated in `research/dataset_research/pilot_execution_report.md`:

| Scenario | Location & Crop | Stated Need | Social & Land Profile | Key Rules Tested | Engine Outcome | Important Caveat |
|---|---|---|---|---|---|---|
| **S001** | Raichur Cotton | `CROP_INSURANCE` | SC, 3.0 ac Dryland | Baseline positive; PMFBY, PM-KISAN, Krishi Bhagya, Ambedkar Corp | 7 Eligible, 6 Ineligible, 1 Req. Verif | PMKSY ineligible (no water source). |
| **S002** | Haveri Maize | `SOLAR_PUMP_INSTALLATION` | OBC (2A), 2.0 ac Dryland | Off-grid borewell triggers PM-KUSUM B | 8 Eligible, 6 Ineligible, 1 Req. Verif | Ganga Kalyana ineligible (existing borewell). |
| **S003** | Tumakuru Ragi | `RAINWATER_HARVESTING` | General (OC), 1.5 ac Dryland | Krishi Bhagya dryland package (80% Gen) | 6 Eligible, 8 Ineligible, 1 Req. Verif | MIDH ineligible (field crop). |
| **S004** | Dharwad Soybean | `MICRO_IRRIGATION_SUPPORT` | OBC (3B), 4.0 ac Irrigated | PMKSY drip subsidy with operational well | 7 Eligible, 7 Ineligible, 1 Req. Verif | Krishi Bhagya ineligible (not dryland). |
| **S005** | Kolar Tomato | `PROTECTED_HORTICULTURE` | OBC (3A), 1.0 ac Irrigated | MIDH polyhouse requires micro-irrigation | 6 Eligible, 8 Ineligible, 1 Req. Verif | Requires existing drip in assets. |
| **S006** | Mysuru Paddy | `PRODUCTION_CREDIT` | General (OC), 2.5 ac Canal | Central KCC-MISS via commercial bank | 6 Eligible, 8 Ineligible, 1 Req. Verif | Karnataka Coop route requires verification. |
| **S007** | Haveri Maize | `INCOME_SUPPORT` | General (OC), 3.0 ac Dryland | **PM-KISAN Tax Exclusion:** `paid_tax=True` | 5 Eligible, 9 Ineligible, 1 Req. Verif | Tax status does not taint other schemes. |
| **S008** | Vijayapura Jowar | `SOLAR_PUMP_INSTALLATION` | OBC (2A), 4.0 ac Dryland | **PM-KUSUM B Grid Exclusion:** Grid IP-set | 7 Eligible, 7 Ineligible, 1 Req. Verif | Component C noted as unverified option. |
| **S009** | Chitradurga Groundnut | `BOREWELL_IRRIGATION` | General (OC), 2.0 ac Dryland | **Ganga Kalyana Category Exclusion:** General | 6 Eligible, 8 Ineligible, 1 Req. Verif | Scoped to 4 represented corporations. |
| **S010** | Belagavi Sugarcane | `MICRO_IRRIGATION_SUPPORT` | SC, 3.0 ac Irrigated | **PMKSY 7-Year Lock-In:** Subsidized 3 yrs ago | 5 Eligible, 9 Ineligible, 1 Req. Verif | Disqualification is plot-specific. |

### 7.2 Detailed Walkthrough of Key Negative Cases

#### S007: PM-KISAN Tax Exclusion
- *Test Purpose:* Verify that statutory income tax payment strictly disqualifies the applicant from PM-KISAN without disqualifying them from unrelated welfare schemes.
- *Fired Rule:* `PMKISAN_PAID_INCOME_TAX_EXCLUSION`.
- *Result:* `SCH001` is `INELIGIBLE`. Non-tax-gated schemes (`SCH002` PMFBY, `SCH005` Krishi Bhagya, `SCH008_CENTRAL` Credit, `SCH009` Soil Health Card) remain `ELIGIBLE`.

#### S008: PM-KUSUM Component B Grid Exclusion
- *Test Purpose:* Verify that possessing an energized borewell prevents standalone solar pump allocation under Component B.
- *Fired Rule:* `KUSUM_B_GRID_CONNECTED_DISQUALIFIED`.
- *Result:* `SCH006` is `INELIGIBLE`.  
- *Guardrail Check:* The system records: *"Related option to verify: PM-KUSUM Component C; not evaluated as an active benefit."* Component C is not automatically approved.

#### S009: General Merit Ganga Kalyana Category Exclusion
- *Test Purpose:* Verify that a General Category applicant is rejected across the four corporation implementations represented in the registry.
- *Fired Rule:* `GK_PARENT_REGISTRY_CORPORATION_MISMATCH`.
- *Result:* `SCH010` and its four child records are `INELIGIBLE`.
- *Documented Scope Caveat:* The report explicitly notes: *"Ineligible for all four Ganga Kalyana implementation records currently represented in the registry... This result does not establish ineligibility for every Ganga Kalyana-related programme in Karnataka."* Other corporations (e.g., Karnataka Arya Vysya, Maratha, or Brahmin Development Corporations) are outside current benchmark scope.

#### S010: PMKSY 7-Year Lock-In Breach
- *Test Purpose:* Ensure applicants cannot repeatedly claim micro-irrigation capital subsidies for the same land parcel within the statutory lock-in window.
- *Fired Rule:* `PMKSY_SEVEN_YEAR_LOCKIN_BREACHED`.
- *Result:* `SCH003` is `INELIGIBLE` because subsidy was availed 3.0 years ago ($< 7.0$ years).

### 7.3 Conceptual Distinctions in Data Engineering
1. **Scenario Definition:** A structured specification of a hypothetical or real farmer's operational profile (`FarmerScenario`).
2. **Engine Execution Result:** The deterministic evaluation output (`SchemeDetermination`) indicating eligibility and fired rules.
3. **Test Fixture:** A fixed data baseline used in automated testing (`@pytest.fixture base_scenario_dict`) to verify code branches under predictable inputs.
4. **Expert Annotation:** An independent judgment assigned by a human specialist (e.g., relevance score 0–3) evaluating practical utility.
5. **ML Training Example:** A paired feature vector and target label $(x, y)$ used to train a model. In our project:
   - $x = [\text{Farmer Features}, \text{Scheme Metadata}]$
   - $y = \text{Consensus Expert Relevance Score } (0 \le y \le 3)$

---

## Part 8 — Automated Test Suite & Code Coverage Audit

### 8.1 Live Test Suite Results
Executed via `pytest` on October 12, 2026:
- **Total Tests:** **56 passed in 1.76 seconds**
- **Test File:** `tests/test_eligibility_engine.py`
- **Code Coverage Breakdown:**

```
Name                              Stmts   Miss  Cover   Missing Lines
---------------------------------------------------------------------
src\eligibility\__init__.py           4      0   100%   -
src\eligibility\availability.py      55      9    84%   37-40, 72-77
src\eligibility\engine.py           356     47    87%   70, 86, 101, 110-112, 168-169, 180-181...
src\eligibility\models.py            97      8    92%   83-84, 89-90, 94, 96, 98, 100
---------------------------------------------------------------------
TOTAL                               512     64    88%
```

### 8.2 What the Test Categories Verify

```
+-----------------------------------------------------------------------------------------------------+
|                                   TEST TAXONOMY IN REPOSITORY                                       |
+--------------------------+-------------------------------------+------------------------------------+
| Test Type                | Code Example                        | Purpose Checked                    |
+--------------------------+-------------------------------------+------------------------------------+
| Positive Test            | test_clean_positive                 | Validates that a fully qualifying  |
|                          | (test_eligibility_engine.py:72)     | farmer receives ELIGIBLE.          |
|                          |                                     |                                    |
| Negative Exclusion Test  | test_paid_income_tax_excluded       | Validates that statutory exclusion |
|                          | (test_eligibility_engine.py:78)     | flags trigger INELIGIBLE.          |
|                          |                                     |                                    |
| Boundary Test            | test_individual_acreage_boundaries  | Tests exact numerical limits       |
|                          | (test_eligibility_engine.py:461)    | (1.5 ac, 5.0 ac, 12.35 ac).        |
|                          |                                     |                                    |
| Unknown-Input Test       | test_income_tax_unknown...          | Ensures missing values return      |
|                          | (test_eligibility_engine.py:92)     | REQUIRES_VERIFICATION, not False.  |
|                          |                                     |                                    |
| Statutory Exemption Test | test_mts_class_iv_employee_is_exempt| Verifies legal exception to rule   |
|                          | (test_eligibility_engine.py:99)     | (MTS exempt from govt exclusion).  |
|                          |                                     |                                    |
| Architectural Guardrail  | test_unverified_schemes_do_not_leak | Verifies that unconfirmed schemes  |
|                          | (test_eligibility_engine.py:586)    | cannot enter Available Now list.   |
+--------------------------+-------------------------------------+------------------------------------+
```

### 8.3 Coverage Metrics vs. Policy Correctness
- **Line Coverage (88% in our repo):** Indicates that 88% of executable statements ran during pytest execution. It does **not** prove that every combination of conditions was tested.
- **Rule Coverage:** Indicates whether every legal clause from official guidelines is represented in code.
- **Policy Correctness:** Proves that an encoded rule is legally valid. Passing tests on `SCH008_KA_COOP` (Karnataka 0% crop loan) proves that the code checks for annual Government Orders; it does **not** prove that the Karnataka Department of Cooperation has issued the order for the current financial year.

### 8.4 Scheme Rules vs. Test Coverage Matrix

| Scheme ID | Key Policy Rule Encoded | Test Method in Test Suite | Uncovered / Vulnerable Edge Cases |
|---|---|---|---|
| `SCH001` | Paid income tax disqualifies; MTS exempt | `test_paid_income_tax_excluded`<br>`test_mts_class_iv_employee...` | Land inherited after Feb 1, 2019 (death of titleholder succession pathway). |
| `SCH002` | Notified crop required in notified unit | `test_notified_crop_eligible`<br>`test_non_notified_crop_ineligible` | Gram-panchayat-level insurance unit exclusions; cut-off date boundary checks. |
| `SCH003` | 0.2–5.0 ha range, water source, 7-yr lock-in | `test_boundary_land_size`<br>`test_seven_year_lockin` | Mixed parcels where one plot has prior subsidy and another does not. |
| `SCH004` | Tractor RC required for tractor implements | `test_clean_positive`<br>`test_five_year_lockin_breached` | Distinct machinery power caps (e.g. 8 HP power tiller vs 40 HP tractor). |
| `SCH005` | Rainfed dryland only; 1.0–12.35 ac | `test_dryland_required`<br>`test_coastal_district_excluded` | Multi-crop holdings with partial canal command. |
| `SCH006` | Standalone off-grid pump; grid pump excluded | `test_unenergized_borewell_eligible`<br>`test_grid_connected_borewell...` | Solarizing existing grid pump (Component C rules not implemented). |
| `SCH007` | Protected horticulture; existing drip required | `test_clean_positive`<br>`test_missing_micro_irrigation...` | Greenhouse structures exceeding 4,000 m² ceiling. |
| `SCH008` | Central KCC vs Karnataka Coop route | `test_central_commercial_child...`<br>`test_karnataka_coop_child...` | Scale of Finance district-level credit limits. |
| `SCH009` | Universal 100% diagnostic soil testing | `test_universal_diagnostic_access` | Soil testing cycle intervals (2-year retesting cap). |
| `SCH010` | Corporation-specific acreages and pooling | `test_sc_dryland_routes_to_ambedkar`<br>`test_individual_acreage_boundaries` | Community pooling involving mixed-caste contiguous plots (not handled). |

---

## Part 9 — The Expert Annotation Protocol & Inter-Rater Reliability

### 9.1 Why Human Experts Are Required
Statutory eligibility filters out what is legally prohibited. It **cannot** determine what is agronomic best practice:
- If Basavaraj's cotton crop is actively infested by pink bollworm, both PM-KISAN (direct cash) and PMFBY (crop insurance claim) are `ELIGIBLE`.
- Only an agricultural scientist knows that PMFBY is **critically relevant (Score 3)** to mitigate crop loss, while a free Soil Health Card test is **low priority (Score 1)** during an active pest disaster.

### 9.2 The Three Separate Evaluation Dimensions
Documented in `research/dataset_research/expert_annotation_form.md`:
1. **Eligibility:** Evaluated by the **rule engine**. Experts do not score this.
2. **Relevance (The Target Variable):** Evaluated by **human domain experts** on an ordinal scale of 0 to 3.
3. **Actionability:** Evaluated by the **availability pipeline** across 4 discrete states.

#### The 0 to 3 Ordinal Relevance Scale:
- **`3` — Highly Relevant / High Priority:** Directly addresses the farmer's primary stated need with immediate, high-impact practical benefit. Should appear in top-3 recommendation cards.
- **`2` — Relevant / Secondary Priority:** Provides genuine practical benefit, but does not solve the urgent stated need (e.g., general income support when urgent need is insurance).
- **`1` — Marginally Relevant / Low Priority:** Technically eligible, but provides minor or distant value in the current seasonal context (e.g., soil diagnostic testing during an active pest attack).
- **`0` — Irrelevant / Not Useful:** Despite passing eligibility rules, provides no meaningful practical benefit given the farmer's operational profile.

### 9.3 Statistical Inter-Rater Reliability Metrics
Implemented in `scripts/compute_agreement.py`:

#### 1. Krippendorff’s Alpha ($\alpha$) with Ordinal Distance Metric
The primary evaluation metric for this benchmark. Unlike percent agreement, it corrects for chance agreement and handles ordinal distance:
$$\alpha = 1 - \frac{D_o}{D_e}$$
where $D_o$ is observed disagreement and $D_e$ is expected disagreement by chance.  
- With ordinal distance, an annotator disagreement between **Score 3** and **Score 2** incurs a penalty of $(3-2)^2 = 1$.
- A disagreement between **Score 3** and **Score 0** incurs a penalty of $(3-0)^2 = 9$.
- **Interpretation Thresholds:** $\alpha \ge 0.80$ indicates strong agreement; $0.667 \le \alpha < 0.80$ allows tentative conclusions; $\alpha < 0.667$ requires protocol revision.

#### 2. Quadratic Weighted Cohen’s Kappa ($\kappa_w$)
Measures agreement between pairwise raters, penalizing larger score discrepancies quadratically:
$$w_{ij} = 1 - \frac{(i - j)^2}{(k - 1)^2}$$

#### 3. Kendall’s Coefficient of Concordance ($W$)
Evaluates whether multiple experts rank schemes in the same relative order across scenarios (ranges from 0 = complete divergence to 1 = unanimous ranking).

#### 4. Fleiss’ Kappa ($\kappa_f$)
Supplementary nominal metric. Treats labels as unordered categories; useful as a conservative lower-bound check.

### 9.4 Methodological Safeguards in Protocol
- **Blinded Availability (Phase 1 vs. Phase 2):** In Phase 1, experts evaluate relevance without seeing whether the application portal is open today. This prevents annotators from giving a score of 0 to a vital crop insurance scheme merely because its portal closed yesterday.
- **Isolation of Provisional Schemes:** Schemes pending verification (e.g., `SCH008_KA_COOP`) are separated into Section B for qualitative feedback, preventing uncertain legal items from contaminating the numerical relevance dataset.

---

## Part 10 — Where Machine Learning Fits (And What Is Deferred)

### 10.1 The Progression of Agricultural Discovery Systems
To understand this system, consider the progression from simple catalogues to personalized ML:

```
[Level 1: Static Scheme Catalogue]
  └─ Lists schemes alphabetically or by department. Zero filtering.
     Status: Obsolete for personalized advisory.

[Level 2: Deterministic Statutory Filter]
  └─ Evaluates hard constraints (land caps, crop lists, category rules).
     Status: [Implemented and Tested in our repository].

[Level 3: Rule-Based Priority Heuristics]
  └─ Sorts eligible schemes using hardcoded keyword matching on immediate need.
     Status: [Planned as baseline benchmark].

[Level 4: Expert-Annotated Relevance Dataset]
  └─ Multi-expert consensus scores (0-3) on candidate scheme utility.
     Status: [Infrastructure Implemented; Data Collection Planned].

[Level 5: Trained ML Ranking Model]
  └─ Supervised Learning-to-Rank (LTR) or Ordinal Classifier trained on expert labels.
     Status: [Planned / Future Work].

[Level 6: End-to-End Multilingual Delivery Application]
  └─ Production web/mobile/IVR application with live portal monitoring.
     Status: [Planned Roadmap].
```

### 10.2 Future ML Formulation: Feature Representation
When expert labels are collected, the training dataset will pair farmer contexts with scheme records:

```
                          HYPOTHETICAL TRAINING INSTANCE
┌────────────────────────────────────────────────────────────────────────┐
│ Farmer Features (x_farmer):                                            │
│   - land_size_acres: 3.0                                               │
│   - agro_climatic_zone: "Northern Dry Zone"                            │
│   - social_category: "SC"                                              │
│   - immediate_need_encoded: NEED_CROP_INSURANCE                        │
│   - has_operational_pump: 0                                            │
│                                                                        │
│ Scheme Candidate Features (x_scheme):                                  │
│   - scheme_id: "SCH002" (PMFBY)                                        │
│   - benefit_type: "Crop Insurance"                                     │
│   - subsidy_rate_type: PERCENTAGE_PREMIUM_CAP                          │
│                                                                        │
│ Interaction Features (x_cross):                                        │
│   - need_matches_benefit_type: 1.0 (Exact semantic match)              │
│   - crop_matches_notified: 1.0                                         │
│   - asset_match_score: 1.0                                             │
│                                                                        │
│ TARGET LABEL (y):                                                      │
│   - expert_relevance_score: 3 (Consensus ground truth: Highly Relevant)│
└────────────────────────────────────────────────────────────────────────┘
```

### 10.3 Learning-to-Rank (LTR) vs. Ordinal Classification
1. **Ordinal Classification (e.g., Ordinal Logistic Regression, Mord):** Predicts discrete rating $y \in \{0, 1, 2, 3\}$ for each scheme independently. Accounts for ordering ($3 > 2 > 1 > 0$) without assuming uniform intervals between scores.
2. **Learning-to-Rank (e.g., LambdaMART / LightGBM Ranker):** Optimizes the relative ordering of candidate schemes for a specific farmer query, directly maximizing ranking metrics such as **NDCG@3** (Normalized Discounted Cumulative Gain).

#### ML Safeguards and Deferral
- **Why Model Training Must Remain Deferred:** Training a model on 10 pilot scenarios (which yield only $\sim 70$ scheme pairs) will result in extreme overfitting. Machine learning should only be introduced after collecting sufficient multi-expert annotations across diverse scenarios.
- **Baseline Requirement:** Before claiming an ML model works, it must be evaluated against a **Deterministic Keyword / Need-Matching Baseline** on held-out test scenarios. If a simple heuristic achieves 0.91 NDCG@3, deploying a complex neural network is unjustified.

---

## Part 11 — Repository Audit: Status Matrix & Gap Analysis

### 11.1 Truthful Repository Status Matrix

| Component | What Exists Now | Evidence Inspected | Tested? | Limitations | Next Milestone Action |
|---|---|---|---|---|---|
| **Scheme Database** | 16 records (10 core, 6 impl) across 31 attributes | `scheme_master.json`, `.csv`, `.xlsx` | `[Implemented]` | Static snapshot; no live scraping of government circulars. | Maintain manual audit log for circular updates. |
| **Master Builder** | Openpyxl & Pandas generation script | `build_scheme_master.py` | `[Implemented]` | Validates structure, not policy correctness or URL liveness. | Add automated HTTP schema/URL validation check. |
| **Eligibility Models** | Strongly typed dataclasses & enums | `models.py` | `[Tested]` (92% cov) | Scenario schema assumes single primary crop & asset list. | Add support for multi-parcel holdings. |
| **Eligibility Engine** | Deterministic rule evaluators with 3-valued logic | `engine.py` | `[Tested]` (87% cov, 56 tests) | Complex rules hardcoded in Python methods rather than external rule DSL. | Decouple rules into configuration rule-cards. |
| **Parent Deduplication** | Automated suppressor of abstract parents | `engine.py:132-156` | `[Tested]` (56 tests) | Only handles 1-level parent-child hierarchy (`SCH008`, `SCH010`). | Support multi-tier departmental hierarchies. |
| **Availability Filter** | Decoupled 4-state availability filter | `availability.py` | `[Tested]` (84% cov) | `scheme_availability_template.csv` is currently unpopulated. | Populate template with current circulars from KSDA/RSK. |
| **Pilot Scenarios** | 10 defined and executed scenarios (S001–S010) | `case_b_scenario_spec.md`, `pilot_execution_report.md` | `[Implemented]` | Limited sample size (10); covers Karnataka dryland crops primarily. | Expand scenario benchmark to 50–100 cases. |
| **Annotation Tools** | 2-phase CLI & agreement computation script | `run_annotation_session.py`, `compute_agreement.py` | `[Implemented]` (smoke-tested) | `data/annotations/` is currently empty; awaiting live expert inputs. | Recruit 3 RSK/KVK agricultural experts. |
| **ML Models & Training** | None | Non-existent in repository | `[Planned]` | **Model training deliberately deferred** until annotations collected. | Establish deterministic baseline first. |
| **User Interface / API** | None | Non-existent in repository | `[Planned]` | No web application, FastAPI server, or CLI for farmers yet. | Build Streamlit or FastAPI prototype. |
| **Kannada Localization**| Translation notes in documentation | Documentation references only | `[Planned]` | No translation tables, gettext files, or Kannada strings in code. | Create Kannada string resource catalog. |
| **Live Portal Monitor** | None | Non-existent in repository | `[Planned]` | No real-time scraping of Seva Sindhu or Samrakshane portals. | Design headless alert scraper. |

### 11.2 The Five Highest-Priority Technical and Methodological Risks

#### 1. Unpopulated Availability Layer Defaulting to Unknown
- *Risk:* `scheme_availability_template.csv` has no populated rows. All recommendations default to `Availability unknown — confirmation required`. While safe against false claims, the system cannot confirm active application windows.
- *Remediation:* Manually audit current season notifications across Karnataka portals (Samrakshane, FRUITS) and populate verified dates.

#### 2. Model Training with Insufficient Expert Data
- *Risk:* Training an ML model on only 10 pilot scenarios ($N=10$) will lead to memorization and severe overfitting.
- *Remediation:* Defer ML training until 50–100 scenarios are annotated by multiple independent experts with verified inter-rater agreement ($\alpha \ge 0.70$).

#### 3. General Merit Policy Scope Misinterpretation (S009)
- *Risk:* Assuming S009 proves General category farmers are excluded from *all* borewell schemes across Karnataka.
- *Remediation:* Maintain explicit documentation clarifying that the registry currently models only four specific corporation child routes (`SCH010_AMBEDKAR`, `SCH010_VALMIKI`, `SCH010_DEVARAJ_URS`, `SCH010_KMDC`).

#### 4. Hardcoded Rule Logic in Python Methods
- *Risk:* Rules are embedded directly in Python code (`engine.py:161-595`). Modifying a rule requires code changes and redeployment.
- *Remediation:* Refactor scheme rules into declarative JSON or YAML rule-card specifications.

#### 5. Lack of Farmer Interface or Localized Delivery
- *Risk:* The system currently exists as Python modules and terminal scripts, inaccessible to rural cultivators.
- *Remediation:* Develop a clean web or mobile interface with Kannada localization.

---

## Part 12 — Complete End-to-End Scenario Walkthrough (S001 Full Trace)

Let us trace **Pilot Scenario S001** through the entire system:

### 1. Farmer Input Profile
- **Farmer:** Basavaraj, Scheduled Caste smallholder in Raichur (Northern Dry Zone).
- **Land:** 3.0 acres, Dryland (Rainfed).
- **Crops:** Primary: Cotton; Secondary: Redgram.
- **Assets:** None.
- **Income:** ₹1.2 Lakh.
- **Immediate Stated Need:** `CROP_INSURANCE`.
- **Query:** *"Cotton crop suffering pink bollworm attack in Raichur, need compensation claim or insurance procedure."*

### 2. Python Object Construction
```python
scenario = FarmerScenario(
    scenario_id="S001",
    agro_climatic_zone="Northern Dry Zone",
    district="Raichur",
    crop_primary="Cotton",
    crop_secondary="Redgram",
    land_size_acres=3.0,
    land_type="Dryland (Rainfed)",
    social_category="SC",
    farmer_category="Small (2.5-5 acres)",
    existing_assets=[],
    annual_family_income_lakh=1.2,
    immediate_need="CROP_INSURANCE",
    paid_income_tax_last_assessment_year=False,
    govt_employee_category=GovtEmployeeCategory.NONE,
    superannuated_pensioner_monthly_amount=0.0,
    land_ownership_cutoff_pre_feb_2019=True,
    is_pure_tenant_without_land_title=False,
    borewell_electric_status=BorewellElectricStatus.NONE
)
```

### 3. Eligibility Engine Evaluation
`engine.evaluate_scenario(scenario)` runs across all 16 records:
- **`SCH001` (PM-KISAN):** `ELIGIBLE`. Passes land ownership, cut-off date, and statutory exclusion checks.
- **`SCH002` (PMFBY):** `ELIGIBLE`. Cotton is a notified crop in Raichur.
- **`SCH003` (PMKSY-PDMC):** `INELIGIBLE`. Fails water source check (no well or pump in assets).
- **`SCH004` (SMAM):** `ELIGIBLE`. Qualifying landholding; no prior machinery subsidy.
- **`SCH005` (Krishi Bhagya):** `ELIGIBLE`. Rainfed dryland in notified district.
- **`SCH006` (PM-KUSUM B):** `INELIGIBLE`. No drilled water source.
- **`SCH007` (MIDH):** `INELIGIBLE`. Cotton is not a horticultural crop.
- **`SCH008` (Credit Parent):** `ELIGIBLE`. Resolves to children.
  - `SCH008_CENTRAL`: `ELIGIBLE`.
  - `SCH008_KA_COOP`: `REQUIRES_VERIFICATION`. Pending annual Government Order.
- **`SCH009` (Soil Health Card):** `ELIGIBLE`. Universal diagnostic access.
- **`SCH010` (Ganga Kalyana Parent):** `ELIGIBLE`. Routes to Ambedkar Corporation.
  - `SCH010_AMBEDKAR`: `ELIGIBLE`. SC category; $1.5 \le 3.0 \le 5.0$ ac individual dryland route.
  - `SCH010_VALMIKI`: `INELIGIBLE`. Category mismatch.
  - `SCH010_DEVARAJ_URS`: `INELIGIBLE`. Category mismatch.
  - `SCH010_KMDC`: `INELIGIBLE`. Category mismatch.

### 4. Parent Deduplication
`resolve_actionable_determinations()` suppresses abstract parents `SCH008` and `SCH010` because their children (`SCH008_CENTRAL`, `SCH010_AMBEDKAR`) are actionable.

### 5. Availability Filtering
`apply_availability()` evaluates the candidates against `scheme_availability_template.csv`. Because no active circular is indexed, all schemes safely default to `Availability unknown — confirmation required`.

### 6. Actionable Candidate Set
The farmer qualifies for 7 actionable schemes:
1. `SCH001` (PM-KISAN)
2. `SCH002` (PMFBY)
3. `SCH004` (SMAM)
4. `SCH005` (Krishi Bhagya)
5. `SCH008_CENTRAL` (Central KCC-MISS)
6. `SCH009` (Soil Health Card)
7. `SCH010_AMBEDKAR` (Ganga Kalyana SC)

Plus 1 scheme requiring verification:
- `SCH008_KA_COOP` (Karnataka Coop 0% credit)

### 7. Human Expert Scoring Simulation
Presented to an agricultural expert via `scripts/run_annotation_session.py`:
- Expert evaluates farmer need: `CROP_INSURANCE` for pink bollworm damage.
- **`SCH002` (PMFBY):** Assigned **Score 3 (Highly Relevant)**. Directly addresses crop damage relief.
- **`SCH001` (PM-KISAN):** Assigned **Score 2 (Relevant)**. Provides general cash support for inputs.
- **`SCH008_CENTRAL` (Credit):** Assigned **Score 2 (Relevant)**. Helps finance next season's inputs.
- **`SCH005` (Krishi Bhagya):** Assigned **Score 1 (Marginally Relevant)**. Rainwater harvesting does not resolve active bollworm disaster.
- **`SCH010_AMBEDKAR` (Borewell):** Assigned **Score 1 (Marginally Relevant)**. Long-term asset; does not resolve current crop loss.
- **`SCH009` (Soil Health Card):** Assigned **Score 1 (Marginally Relevant)**. Diagnostic testing is low priority during active loss.
- **`SCH004` (SMAM):** Assigned **Score 0 (Irrelevant)**. Machinery procurement is not useful during crop disaster.

### 8. Machine Learning Ranking Outcome
When trained, an ML ranking model will optimize scoring to place `SCH002` (PMFBY) at **Rank 1**, delivering targeted recommendations to the farmer:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TOP RECOMMENDATIONS FOR S001                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. [RANK 1] Pradhan Mantri Fasal Bima Yojana (PMFBY)                   │
│    Benefit: Subsidized crop insurance against pest/yield loss          │
│    Farmer Premium: Statutorily capped at 5.0% for Cotton               │
│    Action: File localized calamity intimation via Samrakshane portal   │
│                                                                        │
│ 2. [RANK 2] PM-KISAN Direct Income Support                             │
│    Benefit: ₹6,000 / year in 3 DBT installments                        │
│    Action: Verify e-KYC on pmkisan.gov.in                              │
│                                                                        │
│ 3. [RANK 3] Central Kisan Credit Card (KCC-MISS)                       │
│    Benefit: Production credit at 4% effective interest                 │
│    Action: Contact commercial bank / RRB branch                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Part 13 — Technical Glossary (Tailored to This Codebase)

- **`Dataclass` (`src/eligibility/models.py:41`):** A Python class decorator (`@dataclass`) that automatically generates boilerplate methods (`__init__`, `__repr__`, `__eq__`) for structured data storage.
- **`Enum` (`src/eligibility/models.py:12`):** A symbolic name bound to unique, constant values, preventing invalid strings (e.g., typos like `"Eligible"` vs `"ELIGIBLE"`).
- **`Three-Valued Logic` (`src/eligibility/models.py:12-16`):** A logic system with three truth values: True, False, and Unknown. Used to flag missing documentation without false rejections or approvals.
- **`Foreign Key` (`scheme_master.json`):** A reference attribute (`parent_scheme_id`) linking a child implementation record to its parent umbrella scheme.
- **`Parent Deduplication` (`src/eligibility/engine.py:132`):** Logic that suppresses abstract parent records from user-facing output when specific child implementations are actionable.
- **`Unit Test` (`tests/test_eligibility_engine.py:72`):** An isolated test verifying the correctness of an individual function or rule branch.
- **`Assertion` (`tests/test_eligibility_engine.py:75`):** A boolean check in testing (`assert condition`) that raises an error if an expected outcome is not met.
- **`Line Coverage`:** The percentage of code statements executed during test runs (88% in this repository).
- **`Branch Coverage`:** The percentage of decision branches (`if/else` paths) executed during test runs.
- **`Inter-Rater Reliability` (`scripts/compute_agreement.py:102`):** Statistical measurement of the degree of agreement among independent human annotators.
- **`Krippendorff's Alpha`:** A chance-corrected reliability metric supporting ordinal distance penalties.
- **`Learning-to-Rank (LTR)`:** A supervised machine learning formulation that optimizes the relative ordering of candidate items rather than predicting isolated scores.
- **`NDCG@K` (Normalized Discounted Cumulative Gain):** An information retrieval metric evaluating ranking quality, heavily rewarding placing relevant items at top ranks.
- **`Data Leakage`:** Flaw where information from outside the training dataset (such as target relevance or future availability) contaminates model inputs.

---

## Part 14 — Staged Learning Roadmap

```
                                  [ YOUR 7-STAGE MASTERY ROADMAP ]
                                                 │
          ┌──────────────────────────────────────┴──────────────────────────────────────┐
          ▼                                                                             ▼
   [FOUNDATION PHASES]                                                           [ADVANCED PHASES]
Stage 1: Repository & Data Architecture                                   Stage 5: ML Dataset Construction
Stage 2: Deterministic Eligibility Engine                                 Stage 6: Ranking Model Development
Stage 3: Testing & Policy Evidence                                        Stage 7: Production Delivery & UI
Stage 4: Pilot Scenarios & Expert Annotation
```

### Stage 1: Repository & Data Architecture
- **What to Learn:** Master JSON/CSV/Excel data pipelines, 31-column schema design, and parent-child foreign key relationships.
- **Files to Study:** `scheme_database/build_scheme_master.py`, `scheme_database/README.md`.
- **Practical Exercise:** Add an 11th standalone scheme dictionary (e.g., National Beekeeping & Honey Mission) to `build_scheme_master.py`, run the script, and verify that raw JSON, processed JSON, and Excel workbook are generated correctly.
- **Self-Test Check:** Can you explain why we maintain both raw individual JSON files and consolidated JSON/CSV formats?

### Stage 2: Deterministic Eligibility Engine
- **What to Learn:** Understand Three-Valued Logic, dataclass models, enum enforcement, and rule dispatching.
- **Files to Study:** `src/eligibility/models.py`, `src/eligibility/engine.py`.
- **Practical Exercise:** Trace a scenario where `paid_income_tax_last_assessment_year` is `None` vs `True` vs `False`, and observe the changes in status, disqualification factors, and missing verification lists.
- **Self-Test Check:** Why must an unknown attribute never default to `False`?

### Stage 3: Testing & Policy Evidence
- **What to Learn:** Learn how unit, boundary, negative, and integration tests work; understand why 88% code coverage does not guarantee legal policy validity.
- **Files to Study:** `tests/test_eligibility_engine.py`.
- **Practical Exercise:** Write a new unit test for `SCH004` (SMAM) checking an applicant applying for a tractor implement who does not own a tractor. Verify that it fails properly and passes under pytest.
- **Self-Test Check:** What is the difference between line coverage and policy rule correctness?

### Stage 4: Pilot Scenarios & Expert Annotation
- **What to Learn:** Understand scenario benchmark design, the 0–3 ordinal relevance scale, blinded availability protocols, and Krippendorff's alpha.
- **Files to Study:** `research/dataset_research/expert_annotation_form.md`, `scripts/compute_agreement.py`.
- **Practical Exercise:** Run `scripts/smoke_test_agreement_pipeline.py`, inspect the generated synthetic agreement metrics, and observe how ordinal distance penalizes score disagreements.
- **Self-Test Check:** Why do we omit ineligible schemes from the expert annotation form?

### Stage 5: ML Dataset Construction
- **What to Learn:** Learn feature engineering for agricultural recommender systems, feature-label separation, and preventing data leakage.
- **Files to Study:** `research/dataset_research/case_b_scenario_spec.md`.
- **Practical Exercise:** Write a Python function that transforms a `FarmerScenario` and `SchemeDetermination` into a flat numerical feature vector suitable for machine learning.
- **Self-Test Check:** Why should current operational availability be excluded from features predicting relevance?

### Stage 6: Ranking Model Development & Evaluation
- **What to Learn:** Understand baseline ranking heuristics, Learning-to-Rank formulations, NDCG@K evaluation, and small-data validation risks.
- **Files to Study:** `docs/ml_formulation.md`.
- **Practical Exercise:** Build a simple heuristic ranker based on keyword matching against `immediate_need`, and compute its NDCG@3 score on a dummy dataset.
- **Self-Test Check:** Under what circumstances would an ML ranking model fail to outperform a simple heuristic baseline?

### Stage 7: Production Delivery & UI
- **What to Learn:** Understand user-facing presentation partitioning, explainability generation, Kannada localization, and live availability tracking.
- **Files to Study:** `src/eligibility/availability.py`, `docs/architecture.md`.
- **Practical Exercise:** Build a basic prototype interface (e.g. using Streamlit) that takes farmer inputs, runs `EligibilityEngine`, and displays recommendations separated into *Available Now* and *Timing/Verification Required*.
- **Self-Test Check:** How does the system prevent a closed scheme from appearing in the *Available Now* section?

---

## Part 15 — Comprehensive Viva Voce Preparation (15 Defense Questions & Answers)

#### 1. Why is this project called an "ML-Based Recommendation System" when the core code currently runs on deterministic rules?
**Answer:** The architecture uses a two-stage design. Stage 1 is a deterministic eligibility engine, because statutory rules are legally binding and cannot be left to probabilistic approximations. Stage 2 is an ML ranking engine designed to rank eligible schemes by personalized relevance. Because training an ML model requires high-quality ground truth, and no public farmer-scheme dataset exists in India (Case A closed), we built the rule engine and annotation infrastructure first to collect human-expert ground truth (Case B) before training the model.

#### 2. Why couldn't we use an end-to-end Large Language Model (LLM) or deep neural network to evaluate eligibility directly?
**Answer:** An end-to-end neural network or LLM can hallucinate eligibility criteria, miss statutory cut-off dates (e.g., February 1, 2019 for PM-KISAN), and provide non-deterministic outputs. A farmer could be promised a ₹2,00,000 subsidy only to have it rejected by the department. Our system guarantees zero policy hallucination by evaluating rules deterministically.

#### 3. Explain the Three-Valued Logic in your engine. Why not simply use True and False?
**Answer:** Standard boolean logic forces missing data into either True or False. If a farmer's income tax status is unknown, assuming False would falsely approve an ineligible applicant; assuming True would deny a qualifying farmer. Our engine returns `REQUIRES_VERIFICATION`, identifying the specific missing document needed (e.g., Form 16 / ITR assessment order).

#### 4. How do you distinguish between parent and child schemes, and why is this necessary?
**Answer:** Schemes like Ganga Kalyana (`SCH010`) and Agricultural Credit (`SCH008`) are umbrella programmes implemented through multiple agencies with distinct rules. If left as single records, their eligibility criteria would be oversimplified. We model them as parent records with child implementation records (`SCH010_AMBEDKAR`, `SCH010_VALMIKI`, `SCH008_CENTRAL`, etc.). The engine automatically deduplicates abstract parent records from user recommendations when concrete children are actionable.

#### 5. Does passing all 56 tests prove that your system is legally accurate according to current Karnataka government policies?
**Answer:** No. Passing unit tests proves **internal software consistency** with the rules encoded in the codebase. It does not prove legal validity. For instance, `SCH008_KA_COOP` passes tests verifying that it checks for annual Government Orders, but only an administrative inquiry can verify whether the Department of Cooperation has issued the order for the current financial year.

#### 6. What did your pilot test scenario S007 prove?
**Answer:** S007 tested PM-KISAN statutory tax exclusion (`paid_income_tax_last_assessment_year = True`). It verified that the applicant was disqualified from PM-KISAN (`SCH001`) while remaining eligible for non-tax-gated schemes like PMFBY (`SCH002`) and Soil Health Card (`SCH009`), proving that disqualifications are properly scoped.

#### 7. Why does scenario S009 show ineligibility for Ganga Kalyana, and what is the caveat?
**Answer:** S009 models a General Merit applicant. The four child records currently in our registry (`SCH010_AMBEDKAR` for SC, `SCH010_VALMIKI` for ST, `SCH010_DEVARAJ_URS` for OBC, `SCH010_KMDC` for Minorities) do not cover General category farmers. The engine correctly evaluates them as ineligible. The caveat is that this does not prove ineligibility across *all* Ganga Kalyana programmes in Karnataka, as other corporations (such as the Karnataka Arya Vysya or Brahmin Development Corporations) are outside our current benchmark scope.

#### 8. Why is operational availability kept completely separate from statutory eligibility?
**Answer:** Statutory eligibility is governed by permanent gazette notifications; administrative availability depends on current financial year budgets, seasonal cut-off dates, and portal opening windows. A farmer may be eligible for PMFBY, but if the Kharif cut-off date passed last week, they cannot apply today. Decoupling them prevents closed schemes from being recommended as immediately actionable.

#### 9. What is the guardrail preventing unverified schemes from appearing in the "Available Now" list?
**Answer:** Method `apply_availability` in `availability.py` requires three conditions for `Verified available now`: status must be `OPEN`, an official notice URL must exist, and a verified publication date must be present. Because our availability template is currently unpopulated, all recommendations safely default to `Availability unknown — confirmation required`.

#### 10. Why do you use Krippendorff’s Alpha instead of simple percentage agreement to evaluate expert annotators?
**Answer:** Percent agreement does not account for agreement by chance. Furthermore, simple Cohen's kappa treats labels as unordered categories. Krippendorff's Alpha with an ordinal distance metric accounts for chance agreement and penalizes larger discrepancies quadratically: a disagreement between Score 3 and Score 0 incurs nine times the penalty of a disagreement between Score 3 and Score 2.

#### 11. Why are ineligible schemes omitted from the Expert Annotation Form?
**Answer:** Ineligible schemes cannot legally be granted to the farmer. Asking experts to rate the practical relevance of an illegal scheme wastes expert time and risks training the ranking model on candidates the farmer cannot receive.

#### 12. What is the difference between upfront support and contingent claims in PMFBY?
**Answer:** Upfront support is a guaranteed government premium subsidy where the government pays the balance of the actuarial premium beyond the capped farmer share (1.5%–5%). A contingent claim is an indemnity payment triggered only if actual yield falls below threshold yield during crop cutting experiments. Conflating the two would mislead farmers into expecting a guaranteed cash payout from insurance.

#### 13. How does your system handle pure tenant farmers?
**Answer:** In accordance with official guidelines, PM-KISAN strictly excludes pure tenant farmers lacking land ownership records (`is_pure_tenant_without_land_title = True`). In contrast, PMFBY and Central KCC allow tenant farmers cultivating notified crops to enroll via tenancy agreements or sowing certificates. Our engine evaluates tenancy conditions per scheme rather than applying a blanket exclusion.

#### 14. What baseline model will you use to evaluate your future ML ranking model?
**Answer:** We will use a **Deterministic Keyword / Need-Matching Baseline** that scores eligible schemes using hardcoded semantic rules matching the farmer's stated immediate need. If an ML ranking model cannot achieve higher NDCG@K scores than this simple heuristic on held-out test scenarios, deploying machine learning is unjustified.

#### 15. What are the primary technical risks and limitations of your project in its current state?
**Answer:**
1. The dynamic availability layer is currently an unpopulated template.
2. The benchmark dataset currently consists of 10 pilot scenarios, requiring expansion to 50–100 scenarios before model training.
3. Ganga Kalyana modeling covers four corporations, rather than statewide coverage.
4. Rules are currently hardcoded in Python methods rather than a declarative rule DSL.
5. The system lacks a user-facing web/mobile interface and Kannada localization for direct farmer use.
