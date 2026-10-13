# Benchmark v1.0 — Scenario Design & Coverage Matrix

**Document Version:** `benchmark-design-v1.0`  
**Milestone:** Benchmark v1.0 Scenario Design and Validation  
**Approved Scope:** 60 New Scenarios (`S011`–`S070`) across all 10 Karnataka Agro-Climatic Zones  
**Annotation Standard:** `annotation-protocol-v1.1`  
**Status:** Pre-Generation Design Freeze  
**Model Training Status:** **STRICTLY DEFERRED**  

---

## 1. Executive Milestone Objectives

Following the passing decision gate of the 10-scenario pilot ($\kappa_w = 0.8306$, $\alpha = 0.8311$), this document establishes the formal design specification for **Benchmark v1.0**. 

The goal of Benchmark v1.0 is **not** to create training data for immediate neural model fitting. The goal is to build a rigorous, diverse, and policy-grounded testbed that proves whether a subsidy recommendation system can generate useful, explainable, and legally sound advice across Karnataka's diverse farming conditions—and whether an ML ranker can outperform transparent heuristic baselines.

### 1.1 Dataset Partitioning & Anti-Leakage Safeguards
To maintain scientific validity:
1. **Pilot Calibration Data (`S001`–`S010`):** Permanently isolated as pilot calibration data. It will **not** be included in the held-out test evaluation sets of Benchmark v1.0.
2. **Benchmark v1.0 (`S011`–`S070`):** 60 newly constructed scenarios.
3. **Partitioning Strategy:** To prevent data leakage between synthetically related scenarios, dataset splitting must use **Template-Grouped Partitioning** (scenarios sharing agricultural templates or district-crop pairs are grouped together in either train or test folds, rather than naive random splitting).

---

## 2. Geographic Coverage Matrix (10 Agro-Climatic Zones)

The 60 scenarios are distributed equally across all **10 official Agro-Climatic Zones of Karnataka** (6 scenarios per zone), matching real cropping patterns, rainfall regimes, and district-level administrative practices.

| Zone ID | Official Agro-Climatic Zone | Representative Districts | Primary Crops Represented | Scenario ID Range |
|:---:|:---|:---|:---|:---:|
| **Z1** | **North Eastern Transition Zone** | Bidar, Kalaburagi (North) | Redgram, Sugarcane, Soybean, Jowar | `S011`–`S016` |
| **Z2** | **North Eastern Dry Zone** | Kalaburagi, Yadgir, Raichur | Redgram, Cotton, Bajra, Sunflower | `S017`–`S022` |
| **Z3** | **Northern Dry Zone** | Vijayapura, Bagalkot, Gadag, Koppal | Maize, Bengalgram, Pomegranate, Onion | `S023`–`S028` |
| **Z4** | **Central Dry Zone** | Chitradurga, Davanagere, Tumakuru (North) | Groundnut, Maize, Ragi, Arecanut | `S029`–`S034` |
| **Z5** | **Eastern Dry Zone** | Kolar, Chikkaballapura, Bengaluru Rural | Tomato, Mulberry (Sericulture), Mango, Ragi | `S035`–`S040` |
| **Z6** | **Southern Dry Zone** | Mandya, Mysuru, Chamarajanagar | Sugarcane, Paddy, Banana, Ragi | `S041`–`S046` |
| **Z7** | **Southern Transition Zone** | Hassan, Shivamogga, Chikkamagaluru (Plains) | Maize, Ginger, Potato, Arecanut | `S047`–`S052` |
| **Z8** | **Northern Transition Zone** | Dharwad, Belagavi, Haveri | Soybean, Cotton, Chilli, Wheat | `S053`–`S058` |
| **Z9** | **Hilly Zone** | Kodagu, Chikkamagaluru, Uttara Kannada (Ghats) | Coffee, Black Pepper, Cardamom, Paddy | `S059`–`S064` |
| **Z10** | **Coastal Zone** | Dakshina Kannada, Udupi, Uttara Kannada (Coast) | Coconut, Cashew, Coastal Paddy, Arecanut | `S065`–`S070` |

---

## 3. Multi-Dimensional Farmer Diversity Matrix

To ensure the benchmark tests genuine recommendation quality across varied farmer profiles, scenarios must systematically sample from the following parameter distributions:

### 3.1 Landholding & Irrigation Distribution
- **Marginal (< 2.5 acres):** 24 scenarios (40%) — Primary target for Ganga Kalyana, PM-KISAN, and maximum SMAM subsidy slabs.
- **Small (2.5 – 5.0 acres):** 20 scenarios (33.3%) — Boundary for small farmer micro-irrigation and priority cooperative credit.
- **Medium (5.0 – 10.0 acres):** 10 scenarios (16.7%) — Tests exclusion boundaries for Ganga Kalyana (> 5 acres) and tier-2 subsidy rates for micro-irrigation.
- **Large (> 10.0 acres):** 6 scenarios (10%) — Disqualified from land-capped schemes; tests whether the engine cleanly restricts recommendations to PMFBY and commercial KCC.
- **Land Types Covered:** Rainfed Dryland (30), Canal Irrigated (10), Borewell Irrigated (12), Wetland/Valley (5), Hilly/Terraced (3).

### 3.2 Social Categories & Corporation Mandates
- **SC (Scheduled Caste):** 15 scenarios (25%) $\rightarrow$ Evaluates `SCH010_AMBEDKAR` individual and community borewell rules.
- **ST (Scheduled Tribe):** 10 scenarios (16.7%) $\rightarrow$ Evaluates `SCH010_VALMIKI` individual and community borewell rules.
- **OBC (Backward Classes):** 15 scenarios (25%) $\rightarrow$ Evaluates `SCH010_DEVARAJ_URS` (community borewell only, $\ge 3$ beneficiaries, $\ge 8$ to 15 acres).
- **Minorities (Religious):** 8 scenarios (13.3%) $\rightarrow$ Evaluates `SCH010_KMDC` community borewell pooling.
- **General Merit (GM):** 12 scenarios (20%) $\rightarrow$ Tests clean ineligibility for targeted corporation schemes while retaining statutory universal schemes.

### 3.3 Tenancy & Statutory Title Status
- **Pre-Feb 2019 Land Ownership Verified:** 48 scenarios (80%) $\rightarrow$ Standard baseline.
- **Post-Feb 2019 Land Title Partition / Transfer:** 4 scenarios (6.7%) $\rightarrow$ Evaluates inheritance exemption vs. statutory purchase disqualification under PM-KISAN.
- **Pure Tenant Farmers (No Land Title):** 5 scenarios (8.3%) $\rightarrow$ Tests exclusion from PM-KISAN and land-based subsidies, while confirming eligibility for PMFBY and Central KCC crop loans.
- **Community Pool Beneficiaries:** 3 scenarios (5%) $\rightarrow$ Tests pooled group criteria ($\ge 3$ marginal farmers with contiguous land).

### 3.4 Stated Need Distribution (10 Core Need Classes)
Each need class has 6 dedicated scenarios across different agro-climatic zones:
1. `CROP_INSURANCE` (Localized calamity, post-harvest loss, standing crop pest attack)
2. `SOLAR_PUMP_INSTALLATION` (Off-grid diesel replacement, standalone solar agriculture pump)
3. `RAINWATER_HARVESTING` (Farm pond / Krishi Honda, polythene lining, recharge pit)
4. `MICRO_IRRIGATION_SUPPORT` (Drip irrigation, micro-sprinklers, fertigation units)
5. `PROTECTED_HORTICULTURE` (Polyhouse, shade net, high-value vegetable and flower cultivation)
6. `PRODUCTION_CREDIT` (Short-term seasonal crop loans, fertilizer/seed working capital)
7. `FARM_MECHANIZATION` (Power tillers, multi-crop threshers, CHC custom hiring access, sprayers)
8. `BOREWELL_IRRIGATION` (Individual borewell drilling, energisation, community tubewells)
9. `INCOME_SUPPORT` (Direct cash transfer, relief during severe price depression or household distress)
10. `SOIL_HEALTH_AND_FERTILIZER` (Soil nutrient profiling, secondary micro-nutrients, bio-fertilizers)

---

## 4. Recommendation Challenges & Explicit Scenario Purposes

Each scenario in `S011`–`S070` is engineered to test a specific policy rule, trade-off, or annotation calibration challenge:

| Challenge Type | Target Scenarios (Examples) | Explicit Evaluation Purpose | Expected Protocol v1.1 Handling |
|:---|:---|:---|:---|
| **Challenge 1: Civil Works & Package Complexity** | `S012`, `S024`, `S030` | Tests farmer requesting a standalone solar pump where Krishi Bhagya (farm pond package) passes statutory eligibility. | Protocol v1.1 Rule 1: Krishi Bhagya must be scored $\le 1$ if unrequested civil works create an impractical barrier; PM-KUSUM B scores 3. |
| **Challenge 2: Relief vs. Reimbursable Debt** | `S015`, `S038`, `S044` | Tests farmer in acute distress requesting non-repayable cash income support (`INCOME_SUPPORT`). | Protocol v1.1 Rule 2: Reimbursable credit (KCC) must not receive score 3; PM-KISAN scores 3. KCC scores $\le 2$. |
| **Challenge 3: Disqualification Boundary Enforcements** | `S018`, `S032`, `S055` | Tests statutory exclusions: Income tax payers, retired pensioners > ₹10,000/month, regular government officers. | Engine must output `INELIGIBLE` with exact rule keys; scheme must not appear in Section A. |
| **Challenge 4: Three-Valued Logic / Unknowns** | `S020`, `S048`, `S062` | Income tax status or pension MTS exemption is `UNKNOWN` (`None`). | Engine outputs `REQUIRES_VERIFICATION` (Section B), preventing premature approval or false rejection. |
| **Challenge 5: Pure Tenant Protection** | `S026`, `S042`, `S068` | Farmer is a pure tenant cultivating leased land with no registered land title. | PM-KISAN rejected; PMFBY and Central KCC accepted with tenancy agreement proof. |
| **Challenge 6: Competing Credit Channels** | `S014`, `S036`, `S050` | Commercial Bank KCC-MISS (`SCH008_CENTRAL`) vs. State PACS zero-interest credit (`SCH008_KA_COOP`). | Engine keeps Central KCC in Section A (scored) and PACS credit in Section B (qualitative guidance on annual GO/PACS window). |
| **Challenge 7: Corporation Land Limits** | `S028`, `S052`, `S066` | SC/ST farmer owning > 5 acres dryland applying for Ganga Kalyana. | Engine rejects individual borewell (`SCH010_AMBEDKAR` cap is 5 acres dryland / 2.5 acres wetland); directs to community pool if applicable. |

---

## 5. Data Lineage & Attribute Provenance Architecture

To maintain absolute scientific integrity, scenario fields are categorized by their authentic source lineage:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   SCENARIO ATTRIBUTE PROVENANCE                        │
├────────────────────────────────┬───────────────────────────────────────┤
│ 1. Empirical Distributions     │ Source: NSS 77th Round (Karnataka)    │
│    - Land size ranges          │ Distributes landholding, crop mixes,  │
│    - Baseline income estimates │ and social group prevalence by agro-  │
│    - Common cropping patterns  │ climatic zone.                        │
├────────────────────────────────┼───────────────────────────────────────┤
│ 2. Farmer Voice & Query Intent │ Source: Kisan Call Centre (KCC) Query │
│    - Query phrasing & dialect  │ Realistic farmer vernacular, seasonal │
│    - Immediate stated need     │ distress articulation, and specific   │
│    - Crop crisis context       │ pest/weather symptom descriptions.    │
├────────────────────────────────┼───────────────────────────────────────┤
│ 3. Explicitly Constructed      │ Source: Policy Statutory Rules        │
│    Policy Exclusion Flags      │ NOT extrapolated from demographics.   │
│    - ITR payment status        │ Synthetically authored to test legal  │
│    - Land title cut-off date   │ boundaries (e.g. Feb 2019 title,      │
│    - Prior subsidy tenure      │ pension amounts, prior subsidy years).│
└────────────────────────────────┴───────────────────────────────────────┘
```

> [!CAUTION]
> **Lineage Invariant:** An estimated family income of ₹1.5 Lakh must **never** be automatically converted into an assumed "Income Tax: False" flag. Statutory flags must be explicitly declared as `True`, `False`, or `None` (Unknown) with clear test rationale.

---

## 6. Heuristic Recommendation Baselines (Pre-ML Evaluation Standard)

Before any machine learning model (e.g., LambdaMART, XGBoost Ranker, or Bi-Encoder) is considered, the expanded benchmark will evaluate two transparent heuristic baselines:

### 6.1 Baseline 1: Deterministic Need-to-Scheme Mapping
A transparent lookup mapping the farmer's stated need to primary scheme families:
$$\text{Score}_{\text{B1}}(s, \text{need}) = \begin{cases} 3 & \text{if scheme } s \text{ is primary match for } \text{need} \\ 2 & \text{if scheme } s \text{ is related secondary support} \\ 1 & \text{if scheme } s \text{ is generic statutory support (e.g. PM-KISAN, Soil Card)} \\ 0 & \text{otherwise} \end{cases}$$

### 6.2 Baseline 2: Interpretable Weighted Relevance Score
A linear combination of four explicit domain factors:
$$\text{Score}_{\text{B2}} = w_1 \cdot \text{NeedAlignment} + w_2 \cdot \text{CropSuitability} + w_3 \cdot \text{AssetSynergy} - w_4 \cdot \text{ImplementationComplexity}$$
- **NeedAlignment $\in [0, 1]$:** Directness of matching immediate need.
- **CropSuitability $\in [0, 1]$:** Scheme applicability to the specific crop (e.g., drip for sugarcane = 1.0, drip for wetland paddy = 0.2).
- **AssetSynergy $\in [0, 1]$:** Enhances existing farm assets without unrequested prerequisite burden.
- **ImplementationComplexity $\in [0, 1]$:** Penalizes heavy civil works when farmer requested standalone equipment (Protocol v1.1 Rule 1).

### 6.3 Evaluation Metrics & ML Justification Gate
Both baselines will be benchmarked against expert ground-truth labels using:
1. **NDCG@3 (Normalized Discounted Cumulative Gain at Top 3):** Evaluates ranking quality of top recommendations.
2. **Recall@3 (Relevant Schemes in Top 3):** Proportion of schemes with expert rating $\ge 2$ appearing in the top 3 cards.
3. **ML Decision Rule:** Machine learning models are only justified if cross-validated ML ranking achieves a statistically significant improvement ($\Delta \text{NDCG@3} \ge 0.05$, $p < 0.05$) over Baseline 2 on held-out evaluation splits.

---

## 7. Definition of Done (Benchmark v1.0 Milestone)

The Benchmark v1.0 milestone will be complete when:
- [x] **Coverage Matrix Designed:** Documented distribution across 10 zones, 10 needs, and all statutory categories.
- [ ] **Scenario Specifications Authored:** Complete JSON and markdown definitions for `S011`–`S070`.
- [ ] **Deterministic Engine Verification:** All 60 scenarios executed through `EligibilityEngine`, verifying zero statutory hallucinations.
- [ ] **Dual-Expert Annotation:** Independent annotations collected from E1 and E2 under `annotation-protocol-v1.1`.
- [ ] **Inter-Rater Agreement Audit:** Quadratic weighted kappa ($\kappa_w \ge 0.61$) and Krippendorff's alpha ($\alpha \ge 0.67$) evaluated with all disagreements investigated.
- [ ] **Heuristic Baseline Benchmark:** Baseline 1 and Baseline 2 evaluated on NDCG@3 and Recall@3.
- [ ] **ML Experimentation Decision Record:** Formal determination of whether data quantity, label quality, and baseline gaps justify training an ML model.
