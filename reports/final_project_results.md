# Final Research Results Report: ML-Based Personalized Government Scheme and Subsidy Recommendation System for Farmers

**Project:** ML-Based Personalized Government Scheme and Subsidy Recommendation System for Farmers  
**Repository:** `farmer-benefit-ml`  
**Evaluation Milestone:** Benchmark v1.2 Consolidated Final Research Report  
**Date:** October 2026  
**Status:** Complete (Frozen Research Prototype & Evaluation)  
**Authors/Contributors:** AI Pair Programmer & Research Team  
**Governing Protocols:**  
- `research/dataset_research/benchmark_v1.2_evaluation_preregistration.md` (Approved 2026-10-28)  
- `reports/benchmark_v1.2_design_readiness_checklist.md` (Gate: GO 2026-10-28)  
- `reports/benchmark_v1.2_annotation_readiness_audit.md` (Verdict: PASS 2026-10-28)  
- `reports/benchmark_v1.2_ml_evaluation.md` (Generated 2026-10-29)

---

## Executive Summary

This report documents the consolidated research methodology, benchmark evolution, machine learning formulation, empirical results, and formal acceptance-criteria verdicts for the **farmer-benefit-ml** recommendation system.

The project evaluates whether a contextual machine learning ranking model can reliably prioritize actionable government agricultural subsidies for smallholder and tenant farmers across Karnataka's ten agro-climatic zones, operating downstream of a deterministic statutory eligibility engine.

### Key Headline Findings

1. **Ranking Performance:** On the Benchmark v1.2 evaluation set ($N=90$ scenarios, 369 candidate pairs), the pre-registered primary gradient-boosted ranker (Ablation 1) achieved an out-of-fold **NDCG@3 of 0.8993** and an **MRR of 0.8120**, improving upon the deterministic need-based heuristic baseline (**NDCG@3 of 0.7803**, **MRR of 0.7131**) by **$\Delta\text{NDCG@3} = +0.1190$** ($p = 0.0001$ via two-sided paired permutation test, $B=10{,}000$).
2. **Regional Generalization:** In true held-out Leave-One-Zone-Out (LOZO) cross-validation where the model is evaluated on zones completely absent from its training split, the ML ranker achieved non-negative gains across **all ten zones (10 of 10)**, with regional $\Delta\text{NDCG@3}$ ranging from $+0.0351$ to $+0.3385$.
3. **Preregistered Acceptance Criteria:**
   - **Gate 1 (Substantive Minimum Gain):** **COULD NOT BE EVALUATED** — the pre-registered protocol required $\delta_{\text{min}}$ to be fixed before label collection, but no numerical value was specified in the approved document.
   - **Gate 2 (Statistical Significance Threshold):** **COULD NOT BE EVALUATED** — the pre-registered significance threshold $\alpha$ was similarly not locked prior to label collection.
   - **Gate 3 (Zone-Level Non-Regression):** **MET** — all ten agro-climatic zones demonstrated non-regressive ranking quality ($\Delta\overline{\text{NDCG@3}}_z \ge 0.000$) in LOZO evaluation.
4. **Methodological Boundaries:** Training and evaluation were conducted against single-annotator labels (`human reviewer 2`). Because a second independent expert could not be secured, **independent human inter-rater reliability is unavailable**. While the model demonstrates strong capacity to learn this expert's prioritization logic, this result constitutes evidence of model expressiveness, **not proof of real-world farmer welfare improvement or production readiness**.

---

## 1. Problem and Objectives

### 1.1 Context and Problem Statement
Indian smallholder and marginal farmers operate under severe socio-economic, agronomic, and climatic constraints. In Karnataka, the agricultural landscape spans ten distinct agro-climatic zones—ranging from the arid North Eastern Dry Zone to the humid Coastal and Hilly Zones. Multiple tiers of government (Central, State, and Parastatal boards) administer dozens of agricultural support schemes, including input cash transfers, capital equipment subsidies, micro-irrigation grants, subsidized credit, and emergency infrastructure assistance.

Despite substantial statutory funding, subsidy absorption is severely hindered by two structural bottlenecks:
1. **The Statutory Complexity Barrier:** Scheme guidelines impose strict, multi-layered statutory rules (e.g., landownership thresholds, caste-corporation alignments, income-tax exclusion criteria, energized borewell restrictions, and multi-year subsidy lock-in intervals). Farmers and village-level extension workers frequently struggle to assess baseline eligibility, leading to disqualified applications or misdirected effort.
2. **The Contextual Prioritization Problem:** Even when a farmer is eligible for 3 to 6 schemes, their immediate acute crisis (such as extreme mid-season drought, standing crop failure, or pump-set burnout) requires urgent capital deployment. Generic need mappings fail to resolve compounding secondary constraints (e.g., credit lockouts, lack of three-phase power, or insecure tenancy).

### 1.2 System Objectives
The objective of this project is to develop, formalize, and empirically evaluate a two-stage personalized decision-support framework:
- **Stage 1 (Eligibility Screening & Statutory Governance):** A deterministic, rule-based statutory engine that screens candidate schemes against codified policy guidelines, segregating schemes into actionable candidates (Section A), provisionally eligible schemes requiring administrative verification (Section B), and definitively disqualified schemes.
- **Stage 2 (Contextual Priority Ranking):** A machine learning ranking model that prioritizes actionable Section A candidates according to multi-dimensional farmer context, outperforming transparent heuristic baselines while preventing template memorization and data leakage.

---

## 2. System Architecture

The recommendation architecture is partitioned into strict functional layers to separate legal eligibility constraints from learned empirical preferences:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Farmer Profile Query                            │
│  (10 Zones, Crop, Tenure, Water Source, Electric Status, Needs, Income)│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               Stage 1: Frozen Eligibility Engine                       │
│                   (`src/eligibility/engine.py`)                        │
│  - Codified statutory rules for 16 Karnataka agricultural schemes      │
│  - Deterministic evaluation of land limits, exclusions, tax status     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
┌───────────────────────────────────┐ ┌───────────────────────────────────┐
│       Disqualified Schemes        │ │   Section B: Provisional Corpus   │
│  (Definitive statutory exclusions │ │ (Requires documentary/field check;│
│  e.g., Income Tax, Grid KUSUM-B)  │ │  Score-Disabled; y undefined)     │
└───────────────────────────────────┘ └───────────────────────────────────┘
                  │
                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│               Section A: Actionable Candidate Corpus                   │
│         (`allow_numerical_scoring == True`, 2 to 6 schemes)             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
┌───────────────────────────────────┐ ┌───────────────────────────────────┐
│     Deterministic Baseline        │ │    Experimental ML Ranker         │
│ (`src/models/heuristic_baseline`) │ │ (`src/models/benchmark_v1_2`)     │
│ - Static Need-to-Scheme mapping   │ │ - HistGradientBoosting pipeline   │
│ - Transparent priority rules      │ │ - GroupKFold / LOZO evaluation    │
└─────────────────┬─────────────────┘ └─────────────────┬─────────────────┘
                  │                                   │
                  └─────────────────┬─────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 Stage 2: Ranking & Evaluation Engine                   │
│                     (`src/evaluation/metrics.py`)                      │
│  - NDCG@3 (Exponential Gain, IDCG over all Section A candidates)       │
│  - MRR (Relevance Hit Threshold tau = 2.0)                             │
│  - Two-Sided Paired Permutation Test (B = 10,000, seed = 42)           │
└────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Frozen Statutory Eligibility Engine
The eligibility engine (`src/eligibility/engine.py`) enforces codified government notifications for central and state schemes:
- **Universal & Income Support:** PM-KISAN (SCH001) with strict statutory exclusions (income tax payees, superannuated pensioners $>₹10{,}000$ without MTS exemption, professional practitioners, constitutional post holders, and land ownership transfers post-February 2019).
- **Irrigation & Infrastructure:** PMKSY-PDMC (SCH003; 7-year lock-in, assured water source), PM-KUSUM Component B (SCH006; strictly for non-energized or off-grid water sources; grid-connected borewells definitively disqualified), Krishi Bhagya (SCH005; rainfed taluks only, 1.0-acre minimum catchment, non-coastal).
- **Mechanization & Credit:** SMAM (SCH004; 5-year lock-in, landownership verified), KCC-MISS (SCH008_CENTRAL; crop loan interest subvention via Commercial/RRB channels).
- **Parastatal Targeted Development:** Dr. B.R. Ambedkar Development Corporation Ganga Kalyana Scheme (SCH010_AMBEDKAR; restricted to SC small/marginal farmers with dryland parcels, individual and community borewell routes).
- **Diagnostics:** Soil Health Card Scheme (SCH009; universal agricultural parcel access).

### 2.2 Governance Status & Section B Separation
The engine outputs three mutually exclusive categories per scenario:
- **`ELIGIBLE` / `SECTION_A`:** Clear statutory entitlement. Permitted for numerical relevance scoring ($y \in \{0, 1, 2, 3\}$).
- **`REQUIRES_VERIFICATION` / `SECTION_B`:** Schemes where fundamental criteria may be satisfied, but conditional statutory prerequisites cannot be verified from the initial profile (e.g., PMFBY notified crop-district insurance listings, cooperative bank membership for Karnataka KCC zero-interest tiers, or groundwater feasibility clearances). To prevent misleading automated recommendations, **Section B schemes are strictly score-disabled ($y$ is undefined) and permanently excluded from numerical ranking evaluation**.
- **`INELIGIBLE` / Disqualified:** Hard policy exclusion based on verified negative criteria.

---

## 3. Benchmark Development & Dataset Evolution

The evaluation benchmark evolved across three successive iterations to eliminate methodological vulnerabilities:

| Benchmark Iteration | Scenario IDs | Scenarios ($N$) | Candidate Pairs | Sections Scored | Key Methodological Learning / Vulnerability Identified |
|---|---|:---:|:---:|:---:|---|
| **v1.0.4** | S011–S070 | 60 | 258 | Section A | Initial baseline validation; established frozen Section A candidates and metric code. |
| **v1.1** | S071–S130 | 60 | 269 | Section A | **Vulnerability:** 6 rigid archetypes caused template memorization. Feature `immediate_need_matches_heuristic_primary` directly encoded heuristic logic. Annotation scores (269/269) matched AI practice file row-for-row. |
| **v1.2 (Current)** | S131–S220 | 90 | 369 | Section A | **Reformed Protocol:** Pre-registered feature exclusion, diversity audit ($88$ distinct multi-attribute cells), single-annotator deviation approved, zero AI-practice leakage. |

### 3.1 Benchmark v1.2 Scenario Synthesis & Diversity Audit
Benchmark v1.2 comprises 90 scenarios (`S131`–`S220`), synthesized via demographic profiles and vetted against Karnataka agricultural statistics:
- **Agro-Climatic Coverage:** Exactly 9 scenarios allocated to each of the 10 zones (`Z1` through `Z10`).
- **Land Tenure Balance:** 24 pure tenant scenarios (`is_pure_tenant_without_land_title == True`) and 66 owner-operator scenarios.
- **Crisis Distribution:** Primary acute situations distributed across 8 domains: Soil Health & Fertilizer (17), Solar Pump Installation (13), Crop Insurance (12), Protected Horticulture (12), Debt Relief (10), Farm Mechanization (10), Post-Harvest Storage (9), and Rainwater Harvesting (7).
- **Joint-Attribute Independence:** The pre-finalization diversity audit (`data/benchmarks/v1.2/diversity_audit.json`) confirmed 88 distinct cells across the joint distribution of $(\text{crop} \times \text{tenure} \times \text{water access} \times \text{immediate need} \times \text{electricity access})$, eliminating the collinearity that undermined v1.1.

### 3.2 Section A Candidate Distribution
Across the 90 scenarios, the frozen eligibility engine identified **369 candidate pairs** spanning **8 unique schemes**:
- `SCH001` (PM-KISAN): 66 pairs
- `SCH003` (PMKSY-PDMC): 34 pairs
- `SCH004` (SMAM): 66 pairs
- `SCH005` (Krishi Bhagya): 28 pairs
- `SCH008_CENTRAL` (KCC-MISS Commercial/RRB): 66 pairs
- `SCH009` (Soil Health Card): 89 pairs
- `SCH010` (Ganga Kalyana Parent Category): 8 pairs
- `SCH010_AMBEDKAR` (Ganga Kalyana Ambedkar Corp): 12 pairs

Candidate set sizes per scenario range from 2 to 6, with a mean of 4.10 schemes per scenario.

---

## 4. Annotation Methodology & Provenance

### 4.1 Approved Single-Annotator Protocol
Per the approved Benchmark v1.2 design readiness checklist (Resolution Item 4, approved 2026-10-28), a single-annotator route was formally authorized due to the unavailability of dual independent agricultural policy raters. 

The submission file `data/annotations/benchmark_v1.2/E2_v1.2_blank.csv` was completed by `human reviewer 2`. The raw file was preserved immutably, and its SHA-256 checksum was logged:
```
8ab03fba5f4cd4a1c9783a2bac3864f3d8530ed15e112ddd3f3a05f90fdf3d26
```
To prevent confusion with blank templates, the processed training artifact was created without `_blank` in the filename at:
`data/benchmarks/v1.2/ml_experiment/training_labels_v1.2.0.csv` (identical SHA-256).

### 4.2 Score Distribution and Label Characteristics
All 369 candidate pairs were annotated with an integer relevance score $y \in \{0, 1, 2, 3\}$ accompanied by qualitative rationales:
- **Score 0 (Irrelevant / Asset Mismatch):** 61 pairs (16.5%)
- **Score 1 (Marginal / Tangential Relevance):** 157 pairs (42.5%)
- **Score 2 (Relevant / Secondary Need Mitigation):** 116 pairs (31.4%)
- **Score 3 (Highly Relevant / Primary Crisis Resolution):** 35 pairs (9.5%)

### 4.3 Provenance and Scientific Integrity Caveats
1. **Absence of Inter-Rater Reliability (IRR):** Because only a single rater evaluated the dataset, **no inter-annotator agreement metrics (neither Cohen's quadratic-weighted $\kappa$ nor ordinal Krippendorff's $\alpha$) exist or can be computed**.
2. **Not an Independent Gold Standard:** These labels reflect the subjective policy judgments of one qualified annotator. High model performance against this dataset indicates that the model has successfully approximated this annotator's scoring function; **it does not constitute empirical proof of optimal real-world subsidy delivery**.
3. **Contrast with v1.1 Provenance:** In Benchmark v1.1, all 269 annotation scores identically matched an earlier AI training packet (269/269 identical rows). Benchmark v1.2 resolved this anomaly by generating an entirely new scenario set and collecting fresh human reviewer evaluations without an AI intermediary.

---

## 5. Machine Learning Formulation & Training Pipeline

### 5.1 Model Architecture
The primary ranking system (`src/models/benchmark_v1_2/ranker.py`) is implemented as an end-to-end scikit-learn regressor pipeline using **Histogram-Based Gradient Boosting** (`HistGradientBoostingRegressor`):
- **Base Estimator:** `HistGradientBoostingRegressor(max_iter=200, random_state=42)`
- **Loss Function:** Squared error (approximating expected relevance score $y \in [0, 3]$)
- **Inference Ranking Rule:** For any scenario query $s$, candidates are ranked by descending predicted relevance score $\hat{y}_{s, c}$, with deterministic tie-breaking by alphabetical `scheme_id`.

### 5.2 Feature Policy & Anti-Leakage Controls
The approved v1.2 feature policy strictly prevents data leakage while preserving legitimate farmer context:

| Feature Category | Features Included | Preprocessing / Encoding |
|---|---|---|
| **Scenario Numeric (3)** | `land_size_acres`, `annual_family_income_lakh`, `secondary_constraint_count` | `StandardScaler()` |
| **Scenario Boolean (5)** | `is_pure_tenant_without_land_title`, `land_ownership_cutoff_pre_feb_2019`, `paid_income_tax_last_assessment_year`, `pensioner_is_mts_exempt`, `registered_professional_is_none` | `OneHotEncoder(drop='if_binary', handle_unknown='ignore')` |
| **Scenario Categorical (11)** | `zone_id`, `district`, `crop_primary`, `crop_secondary`, `land_type`, `social_category`, `farmer_category`, `operational_water_source`, `borewell_electric_status`, `immediate_need` (farmer context), `primary_crisis` | `OneHotEncoder(handle_unknown='ignore')` |
| **Scheme Numeric (2)** | `min_land_acres`, `max_land_acres` | `StandardScaler()` |
| **Scheme Categorical (7)** | `scheme_id`, `government_level`, `benefit_type`, `target_crops`, `irrigation_requirements`, `record_type`, `parent_scheme_id` | `OneHotEncoder(handle_unknown='ignore')` |
| **Interactions (2)** | `land_size_within_scheme_range`, `water_source_compatible` | Numeric / Boolean passthrough |

#### Mandatory Feature Exclusions
- **`immediate_need_matches_heuristic_primary`:** Permanently excluded. In v1.1, this feature directly encoded the heuristic baseline's internal decision rule, creating severe circular leakage.
- **`archetype_id`:** Permanently excluded. Prevents the tree ensemble from memorizing scenario cluster IDs.
- **Target Fields:** Relevance scores, human rationales, complementarity notes, and baseline ranks are forbidden as inputs.

### 5.3 Preregistered Need Representation Comparison
To assess whether complex text embeddings offer advantages over structured categorization, three configurations were implemented and evaluated across identical folds:
- **Ablation 1 (Primary Model):** Structured one-hot encoding of `immediate_need` (29 features).
- **Ablation 2 (Sensitivity Baseline):** Complete removal of `immediate_need` (28 features).
- **Ablation 3 (Text Representation):** Replacement of categorical `immediate_need` with an in-pipeline `TfidfVectorizer()` operating on lowercased natural language need descriptions, fitted strictly within the training fold (29 features).

### 5.4 Preprocessing Scope & Group Isolation
- **Scenario-Group Isolation:** All candidates belonging to a scenario are strictly constrained to the same split. In 5-fold cross-validation (`GroupKFold`), zero scenarios appear in both training and test folds.
- **Fold Pipeline Encapsulation:** Encoders, scalers, and TF-IDF vectorizers are fit exclusively on the training partition of each fold, ensuring that test-fold category frequencies and vocabulary never leak into training.

---

## 6. Empirical Results

All evaluations were executed deterministically with `random_state=42`. All ranking metrics were calculated against ground-truth labels scored by `human reviewer 2`.

### 6.1 Global Ranking Performance (5-Fold GroupKFold Out-of-Fold)

| System | Configuration / Need Feature | NDCG@3 | MRR ($\tau=2.0$) | $\Delta\text{NDCG@3}$ vs. Heuristic |
|---|---|:---:|:---:|:---:|
| **ML Ablation 1** | **Primary Model (Structured `immediate_need`)** | **0.8993** | **0.8120** | **+0.1190** |
| **ML Ablation 3** | Text Representation (`immediate_need_text` TF-IDF) | **0.8993** | **0.8120** | **+0.1190** |
| **ML Ablation 2** | Sensitivity Baseline (Excludes `immediate_need`) | **0.8886** | **0.7893** | **+0.1083** |
| **Heuristic Baseline**| Deterministic Need-to-Scheme Mapping | **0.7803** | **0.7131** | — |

#### Statistical Significance
- **Mean Scenario Difference ($\bar{d}$):** $+0.1190$ NDCG@3
- **Two-Sided Paired Permutation Test ($B = 10{,}000$ resamples, Rademacher sign randomization):** $p = \mathbf{0.0001}$
- Under the null hypothesis that scenario metric differences are symmetric about zero, the probability of observing an effect size of $|\bar{d}| \ge 0.1190$ is approximately 1 in 10,000.

#### Representation Ablation Finding
- **Structured vs. Text ($\Delta = 0.0000$):** In Benchmark v1.2, structured categorical encoding and in-pipeline TF-IDF vectorization achieved identical out-of-fold NDCG@3 and MRR. Because the immediate need vocabulary in v1.2 consists of 8 standardized categorical strings, TF-IDF unigrams map 1:1 with one-hot categories, confirming mathematical equivalence in this data regime.
- **Value of Need Context ($\Delta = +0.0108$):** Retaining `immediate_need` (Ablation 1 vs. Ablation 2) improves NDCG@3 by $+0.0108$ and MRR by $+0.0227$, verifying that farmer-stated needs provide legitimate predictive signal without causing the circular memorization observed in v1.1.

---

### 6.2 Leave-One-Zone-Out (LOZO) Generalization

To test regional transferability, 10 separate models were trained—each leaving out all 9 scenarios from one agro-climatic zone. The model was evaluated exclusively on the unseen held-out zone:

| Zone ID | Agro-Climatic Zone Name | Scenarios | ML NDCG@3 (Held-Out) | Baseline NDCG@3 | Regional Gain ($\Delta$) | Non-Regression ($\Delta \ge 0$) |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Z1** | North Eastern Transition Zone | 9 | 0.9522 | 0.6136 | **+0.3385** | ✅ Pass |
| **Z2** | North Eastern Dry Zone | 9 | 0.9184 | 0.7381 | **+0.1802** | ✅ Pass |
| **Z3** | Northern Dry Zone | 9 | 0.9376 | 0.7491 | **+0.1885** | ✅ Pass |
| **Z4** | Central Dry Zone | 9 | 0.9135 | 0.8355 | **+0.0781** | ✅ Pass |
| **Z5** | Eastern Dry Zone | 9 | 0.8433 | 0.8083 | **+0.0351** | ✅ Pass |
| **Z6** | Southern Dry Zone | 9 | 0.9377 | 0.8134 | **+0.1243** | ✅ Pass |
| **Z7** | Southern Transition Zone | 9 | 0.9445 | 0.8432 | **+0.1013** | ✅ Pass |
| **Z8** | Northern Transition Zone | 9 | 0.9297 | 0.8222 | **+0.1075** | ✅ Pass |
| **Z9** | Hilly Zone | 9 | 0.9174 | 0.8522 | **+0.0652** | ✅ Pass |
| **Z10** | Coastal Zone | 9 | 0.8781 | 0.7275 | **+0.1506** | ✅ Pass |
| **Mean** | **Statewide LOZO Average** | **90** | **0.9172** | **0.7803** | **+0.1369** | **10 / 10 Met** |

**LOZO Findings:**
- The ML ranker achieved non-regressive performance across **all 10 agro-climatic zones**.
- The largest improvements occurred in the dry and transition zones (Z1: $+0.3385$, Z3: $+0.1885$, Z2: $+0.1802$), where multi-scheme competition between SMAM mechanization, Krishi Bhagya water harvesting, and KCC credit is most acute and where static heuristic rules perform poorly.

---

### 6.3 Held-Out Group Generalization

To evaluate robustness against distribution shifts along demographic and operational dimensions, dedicated holdout experiments were executed:

| Holdout Dimension | Partition Definition | Train $N$ | Test $N$ | ML NDCG@3 | Baseline NDCG@3 | $\Delta\text{NDCG@3}$ |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Crisis-Type Holdout** | Complete exclusion of `SOIL_HEALTH_AND_FERTILIZER` | 301 pairs (73 sc) | 68 pairs (17 sc) | **0.8353** | 0.8099 | **+0.0254** |
| **Land-Tenure Holdout** | Complete exclusion of pure tenant farmers | 304 pairs (66 sc) | 65 pairs (24 sc) | **0.9789** | 0.9419 | **+0.0370** |
| **Random Scenario 20%** | Every 5th scenario alphabetically | 303 pairs (72 sc) | 66 pairs (18 sc) | **0.9627** | 0.7775 | **+0.1852** |

**Holdout Observations:**
- **Tenure Transfer:** When trained exclusively on landowners, the model accurately ranked tenant farmer schemes (NDCG@3 of 0.9789). Because the eligibility engine had already disqualified asset-mismatched schemes (e.g. land-title requiring grants), the ranker correctly prioritized tenant-accessible working capital (KCC-MISS) and universal diagnostics (Soil Health Card).
- **Unseen Crisis Transfer:** When evaluated on an unseen primary crisis (`SOIL_HEALTH_AND_FERTILIZER`), the model retained a positive gain ($\Delta = +0.0254$) over the baseline, indicating that secondary constraint counts, land size, and water source compatibility provide transferable ranking signal even without direct training on that crisis class.

---

## 7. Pre-Registered Acceptance Criteria Verdict

The approved evaluation pre-registration (`research/dataset_research/benchmark_v1.2_evaluation_preregistration.md`, Section 6) defines three formal acceptance gates. The official verdicts are recorded as follows:

| Acceptance Gate | Pre-Registered Condition | Observed Empirical Value | Official Audit Verdict | Reason / Justification |
|---|---|:---:|:---:|---|
| **Gate 1: Substantive Global Gain** | $\Delta\overline{\text{NDCG@3}} \ge \delta_{\text{min}}$ | $\Delta = \mathbf{+0.1190}$ | ⚠️ **COULD NOT BE EVALUATED** | The approved v1.2 preregistration explicitly stated that $\delta_{\text{min}}$ must be set before label collection. Because no numerical threshold was registered in advance, the gate cannot be formally passed or failed without post-hoc bias. |
| **Gate 2: Statistical Significance** | Two-sided permutation test $p < \alpha$ | $p = \mathbf{0.0001}$ | ⚠️ **COULD NOT BE EVALUATED** | The approved v1.2 preregistration did not fix a numerical significance threshold $\alpha$ prior to label collection. Post-hoc assignment of $\alpha=0.05$ is prohibited by protocol. |
| **Gate 3: Regional Non-Regression** | $\Delta\overline{\text{NDCG@3}}_z \ge 0.000$ for all zones in LOZO | Range: $[+0.0351, +0.3385]$ across all 10 zones | ✅ **MET** | Evaluated via true out-of-distribution LOZO cross-validation. All 10 zones demonstrated strictly non-negative ranking delta over the baseline. |

### Research Ethics & Pre-Registration Governance Statement
In strict accordance with open science practices, **no retroactive thresholds ($\delta_{\text{min}}$ or $\alpha$) have been fabricated** to force Gates 1 and 2 into passed states. The observed effect size ($+0.1190$) and permutation $p$-value ($0.0001$) are reported transparently as empirical findings of an exploratory benchmark milestone.

---

## 8. Limitations & Threat Analysis

### 8.1 Single-Annotator Ground Truth Uncertainty
The most substantial limitation of Benchmark v1.2 is the reliance on a single human expert (`human reviewer 2`). Without a second independent rater, it is impossible to calculate inter-rater reliability. The model's high NDCG@3 (0.8993) demonstrates that it has fitted this individual rater's scoring rubric; it does not prove that these rankings reflect agricultural consensus or ground truth welfare optimization for farmers.

### 8.2 Sample Size and Scheme Representation
The benchmark comprises 90 scenarios and 369 candidate pairs across 8 active Section A schemes. While sufficient for initial statistical testing, 90 scenarios cannot fully represent the multi-million farmer population of Karnataka or capture rare micro-climatic crop-failure edge cases.

### 8.3 Section B Deferral
Section B contains provisionally eligible schemes with substantial potential benefit (e.g., PMFBY yield insurance, cooperative crop loans, micro-irrigation capital grants). Because documentary and field prerequisites could not be validated from synthetic scenario profiles, these schemes were score-disabled. In a real-world setting, deferring Section B schemes shifts the burden of verification entirely onto extension workers.

### 8.4 Mathematical Ranking vs. Real-World Farmer Welfare
High NDCG@3 measures ordinal alignment with expert preference scores. It does not measure:
- Whether the recommended scheme has fiscal budget remaining in the taluk treasury.
- Whether application processing time matches the acute crisis deadline (e.g., emergency pump replacement within 5 days).
- Actual subsidy disbursement, crop yield preservation, or farmer household debt reduction.

---

## 9. Reproducibility & Artifact Inventory

The evaluation pipeline is fully deterministic, auditable, and reproducible without external network dependencies.

### 9.1 SHA-256 Checksum Manifest

| Artifact Path | Description | SHA-256 Checksum |
|---|---|---|
| `data/annotations/benchmark_v1.2/E2_v1.2_blank.csv` | Original human submission | `8ab03fba5f4cd4a1c9783a2bac3864f3d8530ed15e112ddd3f3a05f90fdf3d26` |
| `data/benchmarks/v1.2/ml_experiment/training_labels_v1.2.0.csv` | Versioned training labels | `8ab03fba5f4cd4a1c9783a2bac3864f3d8530ed15e112ddd3f3a05f90fdf3d26` |
| `data/benchmarks/v1.2/scenario_matrix.json` | 90 scenario profiles | `1ee4fb22f10bc233f0950ba540babab268c4067008511a1f1c2c477165595d33` |
| `data/benchmarks/v1.2/candidate_generation_results.json` | Section A candidate sets | `fa9c2eec72498ab26f5bd2c5b9d4fa526c6130059b6af7ab6aac9552ecb95cf1` |
| `data/benchmarks/v1.2/ml_experiment/model_metadata_v1.2.0.json` | Model configuration | `1035dac561a00e6c805f15d5ee0794924dd68535ceaf79af32baf144b307365b` |
| `data/benchmarks/v1.2/ml_experiment/metrics_v1.2.0.json` | Complete evaluation metrics | `34752e5ef0ff04ff43c1697a89eeb5e0d1333b2b8ef5ec7a9ceb121cbefefc60` |
| `data/benchmarks/v1.2/ml_experiment/provenance_v1.2.0.json` | Provenance & attribution | `45d06a059d18065546bf9ca5c8d2fddd60254e162bec9af1e5e15495cb2113af` |
| `research/dataset_research/benchmark_v1.2_evaluation_preregistration.md` | Approved preregistration | `ad00eb7645e2bf0063653b036de13b40279ece95b4117bde633e32fc9815401a` |

### 9.2 Reproducibility Execution Commands
All results and test suites can be verified via PowerShell:

1. **Re-run the Complete Training & Evaluation Pipeline:**
   ```powershell
   python scripts/train_benchmark_v1_2_ranker.py
   ```
2. **Execute the Focused v1.2 Benchmark Test Suite:**
   ```powershell
   python -m pytest tests/test_benchmark_v1_2_scenarios.py tests/test_benchmark_v1_2_annotation_readiness.py tests/test_ml_ranker_v1_2.py -v
   ```
   *Result:* **58 passed in 8.90s** (validating checksums, candidate validity, group isolation, leakage prevention, metric formulas, and pipeline fits).
3. **Execute the Statutory Eligibility Engine & Core Metric Suite:**
   ```powershell
   python -m pytest tests/test_eligibility_engine.py tests/test_evaluation_metrics.py tests/test_benchmark_matrix.py tests/test_compute_benchmark_agreement.py tests/test_zone_z1_scenarios.py -v
   ```
   *Result:* **98 passed in 2.36s** (validating frozen eligibility logic across all 16 schemes and permutation test determinism).

---

## 10. Conclusion and Next Steps

### 10.1 What the Evidence Supports
- **Viability of Learned Contextual Ranking:** A gradient-boosted tree regressor operating downstream of an eligibility engine successfully prioritizes subsidies based on nuanced farmer context, outperforming static heuristic mapping by $+0.1190$ NDCG@3 ($p = 0.0001$).
- **Regional Robustness:** The model demonstrates consistent out-of-distribution transfer across all 10 Karnataka agro-climatic zones under strict Leave-One-Zone-Out conditions.
- **Representation Parity:** Structured categorical encoding of farmer needs is mathematically and empirically equivalent to in-pipeline TF-IDF text vectorization when standard need taxonomies are employed.

### 10.2 What the Evidence Does Not Establish
- **Production Readiness:** The current model is an offline research prototype. It has not undergone prospective live trials, multi-annotator validation, or pilot field testing.
- **Ground Truth Generalizability:** Because labels derive from a single expert reviewer, universal consensus cannot be claimed.

### 10.3 Prospective Roadmap Before Deployment
1. **Multi-Annotator Consensus Benchmark (v1.3):** Recruit two independent agricultural extension officers, define $\delta_{\text{min}} \ge +0.050$ and $\alpha \le 0.050$ prospectively, and compute inter-rater agreement ($\kappa \ge 0.65$) prior to label unblinding.
2. **Integration into Extension Worker Interface:** Decouple the ranking backend into an API service connected to a simple, mobile-responsive farmer profile questionnaire (with multilingual Kannada/English support and Section B document checklists).
3. **Dynamic Scheme Availability:** Integrate real-time administrative status (open portal windows, taluk quota exhaustion) into Stage 1 candidate generation.

---

*Report certified as complete, reproducible, and compliant with approved pre-registration protocols.*

