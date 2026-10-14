# Benchmark v1.0 — Scenario Design & Coverage Matrix

**Document Version:** `benchmark-design-v1.0.2`  
**Supersedes:** `benchmark-design-v1.0.1` (commit `2d06675`)  
**Milestone:** Benchmark v1.0 Scenario Design and Validation  
**Approved Scope:** 60 New Scenarios (`S011`–`S070`) across all 10 Karnataka Agro-Climatic Zones  
**Annotation Standard:** `annotation-protocol-v1.1`  
**Status:** Pre-Generation Design Freeze (Reconciled & Validated)  
**Model Training Status:** **STRICTLY DEFERRED**  

---

## Revision Notes: v1.0.1 → v1.0.2

This revision reconciles the scenario assignment matrix with all declared target quotas, adds explicit holding/parcel/subsidy area columns, clarifies community-pool assignments, and adds automated validation tests (`validate_benchmark_matrix.py` and `tests/test_benchmark_matrix.py`). No changes were made to the frozen eligibility engine (`pilot-v1.0`, commit `7724fa7`), scheme database, pilot calibration data (`S001`–`S010`), or annotation protocol v1.1. Pre-specified heuristic baseline weights and evaluation methodology remain strictly unchanged.

| Dimension | Target Quota | v1.0.1 Actual | v1.0.2 Reconciled | Reconciliation Actions Applied |
|:---|:---:|:---:|:---:|:---|
| **Total Scenarios** | 60 | 60 | **60** | Unique and continuous `S011`–`S070` maintained across all revisions. |
| **Zone Distribution** | 6 / zone (10 zones) | 6 / zone | **6 / zone** | Maintained exactly 6 slots per zone (`Z1`–`Z10`). |
| **Landholding Classes** | 22 Mar, 20 Sm, 12 Med, 6 Lrg | 22 Mar, 28 Sm, 7 Med, 3 Lrg | **22 Mar, 20 Sm, 12 Med, 6 Lrg** | Converted 5 Small to Medium (S017, S020, S027, S041, S047) and 3 Small to Large (S065, S069, S070). Mutually exclusive intervals preserved. |
| **Social Categories** | 15 SC, 10 ST, 10 OBC, 8 Min, 17 GM | 18 SC, 11 ST, 13 OBC, 1 Min, 17 GM | **15 SC, 10 ST, 10 OBC, 8 Min, 17 GM** | Reallocated under-represented Minorities from 1 to 8 (S021, S023, S036, S051, S053, S063, S068, S069) from surplus SC (-3), ST (-1), and OBC (-3); GM preserved at 17. |
| **Primary Needs** | 6 per category (10 categories) | 9 Credit, 8 Insur, 8 Bore, 8 Micro, 6 Inc, 5 Mech, 5 Hort, 4 Sol, 4 Rain, 3 Soil | **6 per category (all 10 categories)** | Rebalanced surplus needs (Credit -3, Insurance -2, Borewell -2, Micro -2) to deficit categories (Solar +2, Rainwater +2, Soil Card +3, Mech +1, Hort +1). Every need has exactly 6 scenarios. |
| **Tenure Statuses** | 47 Pre-19, 4 Inherit, 5 Tenant, 4 Unknown | 53 Pre-19, 2 Inherit, 4 Tenant, 1 Unknown | **47 Pre-19, 4 Inherit, 5 Tenant, 4 Unknown** | Reallocated 6 Pre-Feb 2019 scenarios to Post-Feb 2019 Inheritance (+2: S049, S064), Pure Tenant (+1: S044), and Unknown Title Status (+3: S048, S056, S070). |
| **Community Pool** | 3 Yes, 57 No | 3 Yes, 57 No | **3 Yes, 57 No** | Preserved S028, S052, S066. Clarified individual qualifying parcel vs. pooled acreage, group size, contiguity, and labeled provisional rules as `REQUIRES_VERIFICATION`. |
| **Land Types** | 28 Dry, 10 Canal, 12 Bore, 6 Wet, 4 Hill | *Missing as table column* | **28 Dry, 10 Canal, 12 Bore, 6 Wet, 4 Hill** | Added explicit `Land Type` column to scenario assignment table and validated all 60 assignments. |
| **Holding & Area Columns** | Explicit columns | *Only generic Land (ac)* | **Total Holding, Qual Parcel, Subsidized Area (ha)** | Added explicit `Total Holding (ac)`, `Qualifying Parcel (ac)`, and `Req Subsidized Area (ha)` for boundary testing. |
| **Validation Checks** | Automated check | *Manual inspection* | **Automated CLI + Pytest suite** | Added `validate_benchmark_matrix.py` and `tests/test_benchmark_matrix.py` (59/59 passing). |

---

## Historical Revision Notes: v1.0 → v1.0.1

| Issue | Section Affected | Correction Summary |
|:---:|:---|:---|
| 1 | §3.1 Landholding | Removed blanket large-farm exclusion. Scheme-specific land limits now govern each scheme independently. |
| 2 | §3.1 Landholding | Made landholding categories mutually exclusive with exact boundary test cases at 2.5, 5.0, and 10.0 acres. |
| 3 | §4 Challenge 3 | Corrected PM-KISAN pension threshold to **≥ ₹10,000/month** (not *> ₹10,000*) with an explicit exact-boundary test. |
| 4 | §3.3 Tenancy | Replaced blanket tenant exclusion rules with scheme-specific eligibility and `REQUIRES_VERIFICATION` for missing proof. |
| 5 | §3.3 Tenancy | Made community-pool membership a separate overlapping attribute column in the scenario assignment table. |
| 6 | §6.2 Baseline 2 | Pre-specified numerical weights, factor bounds, tie-breaking, and missing-data handling for Baseline 2. |

---

## 1. Executive Milestone Objectives

Following the passing decision gate of the 10-scenario pilot ($\kappa_w = 0.8306$, $lpha = 0.8311$), this document establishes the formal design specification for **Benchmark v1.0**.

The goal of Benchmark v1.0 is **not** to create training data for immediate neural model fitting. The goal is to build a rigorous, diverse, and policy-grounded testbed that proves whether a subsidy recommendation system can generate useful, explainable, and legally sound advice across Karnataka's diverse farming conditions—and whether an ML ranker can outperform transparent heuristic baselines.

### 1.1 Dataset Partitioning & Anti-Leakage Safeguards

1. **Pilot Calibration Data (`S001`–`S010`):** Permanently isolated as pilot calibration data. **Not** included in any Benchmark v1.0 evaluation split.
2. **Benchmark v1.0 (`S011`–`S070`):** 60 newly constructed scenarios.
3. **Partitioning Strategy:** Template-Grouped Partitioning — scenarios that share a district-crop agricultural template are grouped together in either train or evaluation folds, preventing cross-split leakage. With 60 scenarios, scenario-grouped cross-validation is the preferred resampling unit; a single aggregate performance number across all 60 is insufficient.

---

## 2. Geographic Coverage Matrix (10 Agro-Climatic Zones)

60 scenarios are distributed equally across all **10 official Agro-Climatic Zones of Karnataka** (6 scenarios per zone).

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

### 3.1 Landholding & Irrigation Distribution

> [!IMPORTANT]
> **Distinction Between Demographic Landholding Classes and Scheme Ceilings:**
> - **Landholding Class** is a demographic categorization of the farmer's **Total Operational Holding** (`total_operational_holding_acres`), structured into four mutually exclusive mathematical intervals with endpoints at 2.5, 5.0, and 10.0 acres.
> - **Scheme Ceilings** govern specific program entitlements independently of demographic classification. For example:
>   - **PMKSY-PDMC:** Statutory ceiling is **5.0 hectares (~12.36 acres)** of subsidized micro-irrigation area per beneficiary (`requested_subsidized_area_ha`). A Large farmer with 11.5 acres requesting 5.0 ha is evaluated against the 5-ha ceiling, not disqualified by farm size.
>   - **Ganga Kalyana:** Eligibility evaluates the **Qualifying Parcel** (`qualifying_parcel_acres`), requiring dryland $\le 5.0$ acres for individual borewells, or 8.0–15.0 pooled acres with $\ge 3$ beneficiaries for community borewells.
>   - **MIDH Protected Cultivation:** Subsidy is capped by physical structure area (typically up to 4,000 m² / ~1.0 acre), not total farm size.
>   - **SMAM:** Implements tiered subsidy percentages based on landholding class (higher for Marginal/Small, standard for Medium/Large), rather than blanket exclusions.

**Landholding Classes (Mutually Exclusive Intervals — Reconciled to 60 Scenarios):**

| Class | Mathematical Interval | Endpoint Handling | Target Quota | Actual v1.0.2 | Representative Boundary Scenarios |
|:---|:---|:---|:---:|:---:|:---|
| **Marginal** | $[0.0, 2.5)$ | Strictly less than 2.5 acres | 22 | **22** | S011, S014, S015, S018, S019, S022, S024, S025, S029, S031, S035, S038, S039, S043, S044, S045, S048, S054, S060, S062, S067, S068 |
| **Small** | $[2.5, 5.0]$ | Inclusive of both 2.5 and 5.0 acres | 20 | **20** | **2.5 ac boundary:** S026, S032, S037, S051, S063; **5.0 ac boundary:** S013, S040; Others: S012, S016, S021, S030, S036, S042, S049, S050, S055, S056, S059, S061 |
| **Medium** | $(5.0, 10.0]$ | Strictly greater than 5.0, inclusive of 10.0 acres | 12 | **12** | **10.0 ac boundary:** S028; Others: S017, S020, S027, S033, S041, S046, S047, S052, S053, S064, S066 |
| **Large** | $(10.0, \infty)$ | Strictly greater than 10.0 acres | 6 | **6** | S034 (11.0 ac), S057 (12.0 ac), S058 (11.5 ac), S065 (14.0 ac), S069 (13.0 ac), S070 (12.5 ac) |
| **Total** | | | **60** | **60** | **100% Target Reconciled** |

**Explicit Boundary Test Cases:**

| Boundary Value | Dimension Tested | Scenario IDs | Expected Classification & Rule Evaluation |
|:---|:---|:---:|:---|
| **Exactly 2.5 acres** | Small / Marginal boundary | `S026`, `S032`, `S037`, `S051`, `S063` | Classified as **Small** ($\ge 2.5$). Tests Small farmer tier in PMKSY-PDMC and SMAM. |
| **Exactly 5.0 acres** | Small / Medium boundary | `S013`, `S040` | Classified as **Small** ($\le 5.0$). Tests maximum individual holding for Ganga Kalyana dryland ceiling. |
| **Exactly 10.0 acres** | Medium / Large boundary | `S028` | Classified as **Medium** ($\le 10.0$). Tests medium demographic status while pooling contiguous parcel for community borewell. |
| **Exactly 5.00 ha** | PMKSY-PDMC subsidy ceiling | `S058` | Requested subsidized area exactly matches 5.00 ha (~12.36 acres) statutory ceiling for large holding. |
| **Exactly ₹10,000/mo** | PM-KISAN pension exclusion | `S018` | Pensioner receiving exactly ₹10,000/month; inclusive threshold fires statutory exclusion (`PMKISAN_PENSION_UNDER_10K_OR_NONE`). |

**Land Types Covered (Reconciled to 60 Scenarios):**

| Land Type | Target Quota | Actual v1.0.2 | Key Statutory Gating Role |
|:---|:---:|:---:|:---|
| **Dryland (Rainfed Dryland)** | 28 | **28** | Mandatory for Ganga Kalyana individual/community borewells; mandatory for Krishi Bhagya farm ponds. |
| **Canal-irrigated** | 10 | **10** | High-intensity command areas (Tungabhadra, UKP, Cauvery, Malaprabha, Hemavathi); tests credit, crop insurance, and mechanization. |
| **Borewell-irrigated** | 12 | **12** | Existing functional borewells; prerequisite for PMKSY-PDMC drip/sprinkler and MIDH protected structures. |
| **Wetland/valley** | 6 | **6** | Lowland/river basin paddy (Mandya, Mysuru, Belagavi, Uttara Kannada, Udupi); tests PMFBY and tenant crop credit. |
| **Hilly/terraced** | 4 | **4** | High-altitude plantation crops (Kodagu, Chikkamagaluru Ghats); tests soil diagnostic profiling, water storage, and off-grid solar. |
| **Total** | **60** | **60** | **100% Target Reconciled** |

---

### 3.2 Social Categories & Corporation Mandates

Social category is an **overlapping attribute**, not mutually exclusive with land class, tenure status, or land type.

| Social Category | Target Quota | Actual v1.0.2 | Covered Corporation Scheme / Policy Mandate |
|:---|:---:|:---:|:---|
| **SC (Scheduled Caste)** | 15 | **15** | `SCH010_AMBEDKAR` — Individual borewell ($\le 5.0$ ac dryland) and community borewell ($\ge 3$ beneficiaries, 8–15 pooled acres). Enhanced subsidy slabs under SMAM and Krishi Bhagya. |
| **ST (Scheduled Tribe)** | 10 | **10** | `SCH010_VALMIKI` — Individual and community borewell rules (provisionally modeled). Enhanced subsidy slabs under SMAM and Krishi Bhagya. |
| **OBC (Backward Classes)** | 10 | **10** | `SCH010_DEVARAJ_URS` — Community borewell only ($\ge 3$ beneficiaries, 8–15 pooled acres; provisionally modeled). Standard subsidy slabs under universal schemes. |
| **Minorities (Religious)** | 8 | **8** | `SCH010_KMDC` — Community borewell pooling (provisionally modeled); universal statutory access across all general programs. |
| **General Merit (GM)** | 17 | **17** | Ineligible for targeted caste/minority corporation schemes; fully eligible for universal statutory schemes (PM-KISAN, PMFBY, PMKSY, KCC, SHC). |
| **Total** | **60** | **60** | **100% Target Reconciled** |

> [!NOTE]
> The three corporation implementations `SCH010_DEVARAJ_URS`, `SCH010_KMDC`, and `SCH010_VALMIKI` remain **provisionally modeled**. Scenarios that exercise these rules (`S028`, `S043`, `S052`) are explicitly labeled as testing `REQUIRES_VERIFICATION` handling where operational guidelines are unconfirmed, rather than asserting definitive eligibility.

---

### 3.3 Tenancy, Title Status & Community Pooling

**Tenure Status (Mutually Exclusive — Reconciled to 60 Scenarios):**

| Tenure Status | Target Quota | Actual v1.0.2 | Statutory Test Purpose & Handling |
|:---|:---:|:---:|:---|
| **Pre-Feb 2019 Land Ownership Verified** | 47 | **47** | Baseline for PM-KISAN cut-off date compliance and registered land RTC verification. |
| **Post-Feb 2019 Inheritance Partition** | 4 | **4** | Tests inheritance partition exemption: legal succession/family partition is exempt from PM-KISAN cut-off disqualification. Scenarios: `S039`, `S049`, `S064`, `S069`. |
| **Pure Tenant (No Registered Land Title)** | 5 | **5** | Tests scheme-specific tenancy rules: PM-KISAN $	o$ `INELIGIBLE`; PMFBY $	o$ `REQUIRES_VERIFICATION` pending crop agreement/sowing certificate; KCC $	o$ `REQUIRES_VERIFICATION` pending crop loan documentation. Scenarios: `S026`, `S042`, `S044`, `S061`, `S068`. |
| **Unknown / Unverified Title Status** | 4 | **4** | Tests Three-Valued Logic: all land-dependent schemes return `REQUIRES_VERIFICATION` rather than false eligibility. Scenarios: `S048`, `S056`, `S062`, `S070`. |
| **Total** | **60** | **60** | **100% Target Reconciled** |

**Community Pool Assignments (Clarified — S028, S052, S066):**

Community-pool membership is an independent overlapping attribute (3 Yes, 57 No). For all community pool scenarios, both the applicant's individual operational holding, individual qualifying parcel, total pooled area, group size, contiguity assertion, and corporation routing are explicitly recorded:

| Scenario | Zone & District | Social Cat. & Corporation | Individual Total Holding | Individual Qualifying Parcel | Pooled Area & Group Size | Contiguity & Route Status | Regulatory / Engine Handling |
|:---:|:---|:---|:---:|:---:|:---|:---|:---|
| **S028** | Z3 Bagalkot | OBC (`SCH010_DEVARAJ_URS`) | 10.0 ac (Medium) | 3.0 ac dryland | 9.0 ac pooled (3 farmers) | Contiguous dryland parcels verified | Individual route rejected ($> 5.0$ ac). Community pool satisfies 8–15 ac and $\ge 3$ members. Labeled **`REQUIRES_VERIFICATION`** due to provisional Devaraj Urs corporation modeling. |
| **S052** | Z7 Chikkamagaluru | OBC (`SCH010_DEVARAJ_URS`) | 9.5 ac (Medium) | 4.0 ac dryland | 12.0 ac pooled (3 farmers) | Contiguous dryland parcels verified | Individual route rejected ($> 5.0$ ac). Community pool satisfies 8–15 ac and $\ge 3$ members. Labeled **`REQUIRES_VERIFICATION`** due to provisional Devaraj Urs corporation modeling. |
| **S066** | Z10 Udupi | SC (`SCH010_AMBEDKAR`) | 5.5 ac (Medium) | 3.5 ac dryland | 14.0 ac pooled (4 farmers) | Contiguous dryland parcels verified | Individual route rejected ($5.5 > 5.0$ ac individual ceiling). Codified Ambedkar community route valid ($\ge 3$ beneficiaries, 8–15 ac dryland). Labeled as requiring verification of field parcel contiguity and ESCOM groundwater feasibility. |

---

### 3.4 Stated Need Distribution (10 Core Need Classes)

Each of the 10 core need classes has **exactly 6 dedicated scenarios** distributed across zones:

| # | Need Code | Description | Target Quota | Actual v1.0.2 | Scenario IDs |
|:---:|:---|:---|:---:|:---:|:---|
| 1 | `CROP_INSURANCE` | Calamity, post-harvest loss, standing crop pest attack | 6 | **6** | `S011`, `S017`, `S039`, `S042`, `S062`, `S067` |
| 2 | `SOLAR_PUMP_INSTALLATION` | Standalone off-grid solar agriculture pump (PM-KUSUM B) | 6 | **6** | `S012`, `S020`, `S024`, `S030`, `S051`, `S063` |
| 3 | `RAINWATER_HARVESTING` | Farm pond (Krishi Honda), polythene lining, recharge pit | 6 | **6** | `S019`, `S027`, `S031`, `S045`, `S053`, `S060` |
| 4 | `MICRO_IRRIGATION_SUPPORT` | Drip irrigation, micro-sprinklers (PMKSY-PDMC) | 6 | **6** | `S023`, `S034`, `S037`, `S041`, `S058`, `S070` |
| 5 | `PROTECTED_HORTICULTURE` | Polyhouse, shade net, commercial horticulture (MIDH) | 6 | **6** | `S025`, `S035`, `S048`, `S049`, `S054`, `S069` |
| 6 | `PRODUCTION_CREDIT` | Short-term seasonal crop loans (KCC-MISS, State PACS) | 6 | **6** | `S014`, `S026`, `S036`, `S050`, `S061`, `S068` |
| 7 | `FARM_MECHANIZATION` | Power tillers, sprayers, transplanters, tractors (SMAM) | 6 | **6** | `S021`, `S033`, `S040`, `S047`, `S057`, `S064` |
| 8 | `BOREWELL_IRRIGATION` | Individual & community borewells (Ganga Kalyana) | 6 | **6** | `S016`, `S028`, `S029`, `S043`, `S052`, `S066` |
| 9 | `INCOME_SUPPORT` | Direct cash transfer, severe distress relief (PM-KISAN) | 6 | **6** | `S015`, `S018`, `S032`, `S038`, `S044`, `S055` |
| 10 | `SOIL_HEALTH_AND_FERTILIZER` | Soil nutrient profiling, micro-nutrients (Soil Health Card) | 6 | **6** | `S013`, `S022`, `S046`, `S056`, `S059`, `S065` |
| **Total** | | | **60** | **60** | **100% Target Reconciled** |

---

## 4. Recommendation Challenges & Explicit Scenario Purposes

| Challenge Type | Scenario IDs | Evaluation Purpose | Expected Handling |
|:---|:---|:---|:---|
| **1: Civil Works & Package Complexity** | `S012`, `S024`, `S030` | Standalone solar pump requested; Krishi Bhagya passes eligibility. | Protocol v1.1 Rule 1: Krishi Bhagya scored $\le 1$ when unrequested excavation is an impractical barrier; PM-KUSUM B scored 3. |
| **2: Relief vs. Reimbursable Debt** | `S015`, `S038`, `S044` | Farmer in distress requests non-repayable `INCOME_SUPPORT`. | Protocol v1.1 Rule 2: KCC must not receive score 3; PM-KISAN scores 3 (or evaluated against tenancy in `S044`). |
| **3: Disqualification Boundary** | `S018`, `S032`, `S055` | Income tax payer (`S032`); regular government officer (`S055`); pensioner at exactly ₹10,000/month (`S018`). | Engine returns `INELIGIBLE` with explicit rule key; scheme absent from Section A. |
| **4: Three-Valued Logic / Unknowns** | `S020`, `S048`, `S056`, `S062` | Income tax status unknown (`S020`); pension MTS exemption unknown (`S048`); land title unknown (`S048`, `S056`, `S062`, `S070`). | Engine returns `REQUIRES_VERIFICATION`; scheme enters Section B advisory only. |
| **5: Pure Tenant — Scheme-Specific Rules** | `S026`, `S042`, `S044`, `S061`, `S068` | Pure tenant, no registered land title. | PM-KISAN $	o$ `INELIGIBLE`; PMFBY $	o$ `REQUIRES_VERIFICATION` pending documentation; KCC $	o$ `REQUIRES_VERIFICATION` pending crop docs. |
| **6: Competing Credit Channels** | `S014`, `S036`, `S050` | Commercial KCC-MISS vs. State PACS zero-interest credit. | Central KCC in Section A (scored); PACS credit in Section B (qualitative advisory pending annual GO). |
| **7: Corporation Land Limits & Community Pool** | `S028`, `S052`, `S066` | Individual holding $> 5.0$ ac dryland; community pool route ($\ge 3$ members, 8–15 pooled acres). | Engine rejects individual borewell; evaluates community pool route. Provisional corporations return `REQUIRES_VERIFICATION`. |
| **8: Scheme-Specific Area Ceilings (Large Holding)** | `S034`, `S057`, `S058`, `S065`, `S069`, `S070` | Farmers with holding $> 10.0$ acres. | Evaluated per specific scheme ceiling (e.g. PMKSY-PDMC 5.00 ha ceiling in `S034`, `S058`, `S070`; SMAM tiered rates in `S057`; SHC in `S065`; MIDH structure cap in `S069`). No blanket exclusion. |

---

## 5. Scenario Assignment Table (S011–S070)

The table below defines the complete, reconciled 60-scenario matrix with explicit columns for `Land Type`, `Total Holding (ac)`, `Qualifying Parcel (ac)`, and `Req Subsidized Area (ha)`:

| Scenario | Zone | District | Crop | Primary Need | Land Type | Total Holding (ac) | Qualifying Parcel (ac) | Req Subsidized Area (ha) | Land Class | Social Cat. | Tenure Status | Community Pool | Primary Policy Test |
|:---:|:---:|:---|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|:---|:---|
| S011 | Z1 | Bidar | Redgram | `CROP_INSURANCE` | Dryland | 1.8 | 1.8 | — | Marginal | OBC | Pre-Feb 2019 | No | Standard multi-need rainfed pulse profile; OBC category |
| S012 | Z1 | Kalaburagi | Maize | `SOLAR_PUMP_INSTALLATION` | Dryland | 3.0 | 3.0 | — | Small | SC | Pre-Feb 2019 | No | **Challenge 1:** Standalone solar pump vs. Krishi Bhagya package |
| S013 | Z1 | Bidar | Sugarcane | `SOIL_HEALTH_AND_FERTILIZER` | Canal-irrigated | 5.0 | 5.0 | — | Small | GM | Pre-Feb 2019 | No | **Boundary test:** Exactly 5.0 acres (Small/Medium boundary, <= 5.0 is Small); SHC nutrient advisory |
| S014 | Z1 | Kalaburagi | Soybean | `PRODUCTION_CREDIT` | Dryland | 2.2 | 2.2 | — | Marginal | ST | Pre-Feb 2019 | No | **Challenge 6:** Central KCC-MISS commercial credit vs. State PACS zero-interest credit |
| S015 | Z1 | Bidar | Jowar | `INCOME_SUPPORT` | Dryland | 1.5 | 1.5 | — | Marginal | SC | Pre-Feb 2019 | No | **Challenge 2:** Relief vs. debt; KCC must not receive score 3 for income support |
| S016 | Z1 | Kalaburagi | Redgram | `BOREWELL_IRRIGATION` | Dryland | 4.5 | 4.5 | — | Small | SC | Pre-Feb 2019 | No | Ganga Kalyana individual borewell (Ambedkar Corp); SC dryland within <= 5.0 ac ceiling |
| S017 | Z2 | Yadgir | Cotton | `CROP_INSURANCE` | Dryland | 6.0 | 6.0 | — | Medium | ST | Pre-Feb 2019 | No | Dryland cotton PMFBY coverage; medium holding (6.0 ac); notified area pest risk |
| S018 | Z2 | Raichur | Sunflower | `INCOME_SUPPORT` | Dryland | 2.0 | 2.0 | — | Marginal | GM | Pre-Feb 2019 | No | **Challenge 3:** Pensioner at exactly ₹10,000/month; PM-KISAN exclusion threshold test |
| S019 | Z2 | Kalaburagi | Bajra | `RAINWATER_HARVESTING` | Dryland | 1.2 | 1.2 | — | Marginal | OBC | Pre-Feb 2019 | No | Krishi Bhagya farm-pond primary need; dryland Bajra in rainfed dry zone |
| S020 | Z2 | Yadgir | Redgram | `SOLAR_PUMP_INSTALLATION` | Dryland | 6.5 | 6.5 | — | Medium | SC | Pre-Feb 2019 | No | **Challenge 4:** Income tax status UNKNOWN -> REQUIRES_VERIFICATION for PM-KISAN; PM-KUSUM B solar pump |
| S021 | Z2 | Raichur | Cotton | `FARM_MECHANIZATION` | Canal-irrigated | 4.0 | 4.0 | — | Small | Minority | Pre-Feb 2019 | No | SMAM sprayer/equipment subsidy; canal command cotton; Minority category |
| S022 | Z2 | Kalaburagi | Sunflower | `SOIL_HEALTH_AND_FERTILIZER` | Dryland | 1.8 | 1.8 | — | Marginal | GM | Pre-Feb 2019 | No | Soil Health Card diagnostic profiling, dryland sunflower, GM category |
| S023 | Z3 | Vijayapura | Pomegranate | `MICRO_IRRIGATION_SUPPORT` | Borewell-irrigated | 3.5 | 3.5 | 1.42 | Small | Minority | Pre-Feb 2019 | No | PMKSY-PDMC drip for high-value horticulture; Minority category |
| S024 | Z3 | Bagalkot | Maize | `SOLAR_PUMP_INSTALLATION` | Canal-irrigated | 2.0 | 2.0 | — | Marginal | ST | Pre-Feb 2019 | No | **Challenge 1:** Standalone solar pump vs. Krishi Bhagya package |
| S025 | Z3 | Gadag | Onion | `PROTECTED_HORTICULTURE` | Borewell-irrigated | 1.5 | 1.5 | — | Marginal | SC | Pre-Feb 2019 | No | MIDH shade-net structure for commercial onion; SC marginal holding |
| S026 | Z3 | Koppal | Bengalgram | `PRODUCTION_CREDIT` | Canal-irrigated | 2.5 | 2.5 | — | Small | GM | Pure Tenant | No | **Challenge 5 & Boundary test:** Exactly 2.5 ac (Small); Pure tenant; KCC tenant rules, PM-KISAN ineligible |
| S027 | Z3 | Vijayapura | Pomegranate | `RAINWATER_HARVESTING` | Dryland | 6.5 | 6.5 | — | Medium | SC | Pre-Feb 2019 | No | Krishi Bhagya farm pond; SC dryland horticulture holding (6.5 ac) |
| S028 | Z3 | Bagalkot | Onion | `BOREWELL_IRRIGATION` | Dryland | 10.0 | 3.0 | — | Medium | OBC | Pre-Feb 2019 | Yes (3 farmers, 9.0 ac pooled, contiguous) | **Challenge 7 & Boundary test:** Exactly 10.0 ac (Medium); individual dryland > 5 ac ineligible for indiv borewell; community pool route (3 farmers, 9.0 ac pooled contiguous dryland, qualifying parcel 3.0 ac); REQUIRES_VERIFICATION (provisional Devaraj Urs corporation rules) |
| S029 | Z4 | Chitradurga | Groundnut | `BOREWELL_IRRIGATION` | Dryland | 2.0 | 2.0 | — | Marginal | SC | Pre-Feb 2019 | No | Ganga Kalyana individual borewell (Ambedkar Corp); marginal dryland SC farmer |
| S030 | Z4 | Davanagere | Maize | `SOLAR_PUMP_INSTALLATION` | Canal-irrigated | 3.8 | 3.8 | — | Small | GM | Pre-Feb 2019 | No | **Challenge 1:** Standalone solar pump vs. Krishi Bhagya package |
| S031 | Z4 | Tumakuru | Ragi | `RAINWATER_HARVESTING` | Dryland | 1.8 | 1.8 | — | Marginal | ST | Pre-Feb 2019 | No | Krishi Bhagya farm pond; ST dryland farmer in Central Dry Zone |
| S032 | Z4 | Chitradurga | Groundnut | `INCOME_SUPPORT` | Dryland | 2.5 | 2.5 | — | Small | GM | Pre-Feb 2019 | No | **Challenge 3 & Boundary test:** Exactly 2.5 ac (Small); income tax payer -> PM-KISAN INELIGIBLE |
| S033 | Z4 | Davanagere | Arecanut | `FARM_MECHANIZATION` | Borewell-irrigated | 7.5 | 7.5 | — | Medium | OBC | Pre-Feb 2019 | No | SMAM machinery subsidy for arecanut cultivation; Medium holding (7.5 ac); OBC |
| S034 | Z4 | Tumakuru | Maize | `MICRO_IRRIGATION_SUPPORT` | Borewell-irrigated | 11.0 | 11.0 | 4.45 | Large | GM | Pre-Feb 2019 | No | **Challenge 8:** Large holding (11.0 ac); PMKSY-PDMC evaluated against 5-ha (~12.36 ac) ceiling; requested 4.45 ha <= 5.0 ha |
| S035 | Z5 | Kolar | Tomato | `PROTECTED_HORTICULTURE` | Borewell-irrigated | 1.5 | 1.5 | — | Marginal | SC | Pre-Feb 2019 | No | MIDH polyhouse structure; SC marginal horticulture farmer |
| S036 | Z5 | Chikkaballapura | Mulberry | `PRODUCTION_CREDIT` | Borewell-irrigated | 3.0 | 3.0 | — | Small | Minority | Pre-Feb 2019 | No | **Challenge 6:** KCC commercial credit vs. PACS cooperative credit for sericulture; Minority |
| S037 | Z5 | Bengaluru Rural | Mango | `MICRO_IRRIGATION_SUPPORT` | Borewell-irrigated | 2.5 | 2.5 | 1.01 | Small | ST | Pre-Feb 2019 | No | **Boundary test:** Exactly 2.5 ac (Small); PMKSY-PDMC drip for mango orchard |
| S038 | Z5 | Kolar | Tomato | `INCOME_SUPPORT` | Dryland | 1.2 | 1.2 | — | Marginal | GM | Pre-Feb 2019 | No | **Challenge 2:** Post-harvest price collapse distress; KCC debt must not receive score 3 |
| S039 | Z5 | Chikkaballapura | Ragi | `CROP_INSURANCE` | Dryland | 2.0 | 2.0 | — | Marginal | SC | Post-Feb 2019 Inheritance | No | PM-KISAN inheritance partition exemption test; legal family succession verified |
| S040 | Z5 | Bengaluru Rural | Mango | `FARM_MECHANIZATION` | Borewell-irrigated | 5.0 | 5.0 | — | Small | OBC | Pre-Feb 2019 | No | **Boundary test:** Exactly 5.0 acres (Small/Medium boundary, <= 5.0 is Small); SMAM orchard implements |
| S041 | Z6 | Mandya | Sugarcane | `MICRO_IRRIGATION_SUPPORT` | Canal-irrigated | 6.5 | 6.5 | 2.50 | Medium | GM | Pre-Feb 2019 | No | PMKSY-PDMC drip irrigation in irrigated sugarcane canal command; Medium holding (6.5 ac) |
| S042 | Z6 | Mysuru | Paddy | `CROP_INSURANCE` | Wetland/valley | 3.5 | 3.5 | — | Small | SC | Pure Tenant | No | **Challenge 5:** Pure tenant paddy; PMFBY coverage with tenancy documentation verification |
| S043 | Z6 | Chamarajanagar | Banana | `BOREWELL_IRRIGATION` | Dryland | 1.8 | 1.8 | — | Marginal | ST | Pre-Feb 2019 | No | Ganga Kalyana individual borewell (Valmiki Corp); ST marginal dryland farmer; REQUIRES_VERIFICATION (provisional corporation rules) |
| S044 | Z6 | Mandya | Paddy | `INCOME_SUPPORT` | Wetland/valley | 2.0 | 2.0 | — | Marginal | OBC | Pure Tenant | No | **Challenge 2 & Challenge 5:** Pure tenant wetland paddy; PM-KISAN INELIGIBLE due to lack of land title; relief vs. credit |
| S045 | Z6 | Mysuru | Ragi | `RAINWATER_HARVESTING` | Dryland | 1.5 | 1.5 | — | Marginal | SC | Pre-Feb 2019 | No | Krishi Bhagya farm pond; SC dryland farmer in Southern Dry Zone |
| S046 | Z6 | Chamarajanagar | Sugarcane | `SOIL_HEALTH_AND_FERTILIZER` | Canal-irrigated | 7.0 | 7.0 | — | Medium | GM | Pre-Feb 2019 | No | Soil Health Card soil profiling for medium sugarcane holding (7.0 ac); GM |
| S047 | Z7 | Hassan | Maize | `FARM_MECHANIZATION` | Canal-irrigated | 5.5 | 5.5 | — | Medium | GM | Pre-Feb 2019 | No | SMAM tractor/thresher implements subsidy; Medium holding (5.5 ac); GM |
| S048 | Z7 | Shivamogga | Ginger | `PROTECTED_HORTICULTURE` | Borewell-irrigated | 2.0 | 2.0 | — | Marginal | ST | Unknown Title Status | No | **Challenge 4:** Pension MTS exemption unknown & title status UNKNOWN -> REQUIRES_VERIFICATION for land-dependent schemes |
| S049 | Z7 | Chikkamagaluru | Potato | `PROTECTED_HORTICULTURE` | Borewell-irrigated | 4.5 | 4.5 | — | Small | GM | Post-Feb 2019 Inheritance | No | MIDH shade-net structure for commercial seed potato; post-2019 inheritance exemption test |
| S050 | Z7 | Hassan | Arecanut | `PRODUCTION_CREDIT` | Borewell-irrigated | 3.5 | 3.5 | — | Small | OBC | Pre-Feb 2019 | No | **Challenge 6:** KCC commercial credit vs. PACS cooperative credit; arecanut garden |
| S051 | Z7 | Shivamogga | Maize | `SOLAR_PUMP_INSTALLATION` | Dryland | 2.5 | 2.5 | — | Small | Minority | Pre-Feb 2019 | No | **Boundary test:** Exactly 2.5 ac (Small); PM-KUSUM B solar pump; unenergized borewell; Minority |
| S052 | Z7 | Chikkamagaluru | Potato | `BOREWELL_IRRIGATION` | Dryland | 9.5 | 4.0 | — | Medium | OBC | Pre-Feb 2019 | Yes (3 farmers, 12.0 ac pooled, contiguous) | **Challenge 7:** Individual dryland > 5 ac ineligible for indiv borewell; community pool route (3 farmers, 12.0 ac pooled contiguous dryland, qualifying parcel 4.0 ac); REQUIRES_VERIFICATION (provisional Devaraj Urs corporation rules) |
| S053 | Z8 | Dharwad | Soybean | `RAINWATER_HARVESTING` | Dryland | 5.5 | 5.5 | — | Medium | Minority | Pre-Feb 2019 | No | Krishi Bhagya farm pond; medium holding (5.5 ac); Northern Transition Zone; Minority |
| S054 | Z8 | Belagavi | Chilli | `PROTECTED_HORTICULTURE` | Wetland/valley | 1.5 | 1.5 | — | Marginal | SC | Pre-Feb 2019 | No | MIDH shade-net structure for high-value chilli; SC marginal farmer |
| S055 | Z8 | Haveri | Cotton | `INCOME_SUPPORT` | Dryland | 3.0 | 3.0 | — | Small | GM | Pre-Feb 2019 | No | **Challenge 3:** Regular government officer -> PM-KISAN INELIGIBLE statutory exclusion |
| S056 | Z8 | Dharwad | Wheat | `SOIL_HEALTH_AND_FERTILIZER` | Dryland | 4.0 | 4.0 | — | Small | ST | Unknown Title Status | No | **Challenge 4:** Land title UNKNOWN -> SHC accessible; title-dependent schemes trigger REQUIRES_VERIFICATION |
| S057 | Z8 | Belagavi | Sugarcane | `FARM_MECHANIZATION` | Canal-irrigated | 12.0 | 12.0 | — | Large | OBC | Pre-Feb 2019 | No | **Challenge 8:** Large holding (12.0 ac); SMAM evaluated per scheme machinery tier; no blanket exclusion |
| S058 | Z8 | Haveri | Soybean | `MICRO_IRRIGATION_SUPPORT` | Borewell-irrigated | 11.5 | 11.5 | 5.00 | Large | GM | Pre-Feb 2019 | No | **Challenge 8 & Boundary test:** Large holding (11.5 ac); PMKSY-PDMC boundary test at exactly 5.00 ha (~12.36 ac) statutory ceiling |
| S059 | Z9 | Kodagu | Coffee | `SOIL_HEALTH_AND_FERTILIZER` | Hilly/terraced | 4.5 | 4.5 | — | Small | GM | Pre-Feb 2019 | No | Soil Health Card soil testing for plantation coffee in Hilly Zone |
| S060 | Z9 | Chikkamagaluru | Cardamom | `RAINWATER_HARVESTING` | Hilly/terraced | 2.0 | 2.0 | — | Marginal | ST | Pre-Feb 2019 | No | Water harvesting storage structure for hillside cardamom plantation; ST |
| S061 | Z9 | Uttara Kannada | Paddy | `PRODUCTION_CREDIT` | Wetland/valley | 3.0 | 3.0 | — | Small | SC | Pure Tenant | No | **Challenge 5:** Hill zone valley paddy pure tenant; KCC tenant route; PMFBY verification |
| S062 | Z9 | Kodagu | Black Pepper | `CROP_INSURANCE` | Hilly/terraced | 1.8 | 1.8 | — | Marginal | GM | Unknown Title Status | No | **Challenge 4:** Land title UNKNOWN -> land-dependent schemes trigger REQUIRES_VERIFICATION |
| S063 | Z9 | Chikkamagaluru | Coffee | `SOLAR_PUMP_INSTALLATION` | Hilly/terraced | 2.5 | 2.5 | — | Small | Minority | Pre-Feb 2019 | No | **Boundary test:** Exactly 2.5 ac (Small); PM-KUSUM B solar pump for off-grid plantation; Minority |
| S064 | Z9 | Uttara Kannada | Paddy | `FARM_MECHANIZATION` | Canal-irrigated | 8.0 | 8.0 | — | Medium | OBC | Post-Feb 2019 Inheritance | No | SMAM power tiller/paddy transplanter subsidy; medium holding (8.0 ac); post-2019 inheritance partition |
| S065 | Z10 | Dakshina Kannada | Coconut | `SOIL_HEALTH_AND_FERTILIZER` | Dryland | 14.0 | 14.0 | — | Large | GM | Pre-Feb 2019 | No | Soil Health Card universal diagnostic service for large coastal plantation (14.0 ac); GM |
| S066 | Z10 | Udupi | Arecanut | `BOREWELL_IRRIGATION` | Dryland | 5.5 | 3.5 | — | Medium | SC | Pre-Feb 2019 | Yes (4 farmers, 14.0 ac pooled, contiguous) | **Challenge 7:** Individual holding 5.5 ac exceeds 5.0 ac individual Ambedkar ceiling; community pool route valid with 4 SC farmers, 14.0 ac pooled contiguous dryland, qualifying parcel 3.5 ac; requires verification of parcel contiguity & groundwater clearance |
| S067 | Z10 | Dakshina Kannada | Cashew | `CROP_INSURANCE` | Dryland | 2.0 | 2.0 | — | Marginal | ST | Pre-Feb 2019 | No | PMFBY cashew crop insurance in coastal plantation belt; ST marginal farmer |
| S068 | Z10 | Udupi | Coastal Paddy | `PRODUCTION_CREDIT` | Wetland/valley | 1.5 | 1.5 | — | Marginal | Minority | Pure Tenant | No | **Challenge 5:** Pure tenant coastal wetland paddy; KCC crop loan & PMFBY insurance proof check; Minority |
| S069 | Z10 | Dakshina Kannada | Coconut | `PROTECTED_HORTICULTURE` | Dryland | 13.0 | 13.0 | — | Large | Minority | Post-Feb 2019 Inheritance | No | MIDH coastal nursery / shade-net; Large holding (13.0 ac); Minority; post-2019 inheritance exemption test |
| S070 | Z10 | Udupi | Arecanut | `MICRO_IRRIGATION_SUPPORT` | Wetland/valley | 12.5 | 12.5 | 4.80 | Large | SC | Unknown Title Status | No | **Challenge 8:** Large holding (12.5 ac); PMKSY-PDMC requested 4.80 ha <= 5.00 ha; title status UNKNOWN -> REQUIRES_VERIFICATION |

---

### 5.1 Comprehensive Matrix Validation Audit

The matrix has been audited and validated by the automated reproducibility script [`research/dataset_research/validate_benchmark_matrix.py`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/research/dataset_research/validate_benchmark_matrix.py) and verified by unit test suite [`tests/test_benchmark_matrix.py`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/tests/test_benchmark_matrix.py).

```
==================================================
BENCHMARK V1.0.2 MATRIX VALIDATION REPORT
==================================================
Total Scenarios: 60 (Target: 60) -> PASS
Scenario IDs Continuous S011-S070: PASS
Zones Distribution (6 per zone Z1-Z10): PASS
  Z1: 6 / 6
  Z2: 6 / 6
  Z3: 6 / 6
  Z4: 6 / 6
  Z5: 6 / 6
  Z6: 6 / 6
  Z7: 6 / 6
  Z8: 6 / 6
  Z9: 6 / 6
  Z10: 6 / 6

Landholding Classes (Marginal 22, Small 20, Medium 12, Large 6): PASS
  Marginal: 22 / 22
  Small: 20 / 20
  Medium: 12 / 12
  Large: 6 / 6
  Boundary 2.5 ac (classified Small): 5 scenarios (S026, S032, S037, S051, S063)
  Boundary 5.0 ac (classified Small): 2 scenarios (S013, S040)
  Boundary 10.0 ac (classified Medium): 1 scenarios (S028)

Social Categories (SC 15, ST 10, OBC 10, Minority 8, GM 17): PASS
  SC: 15 / 15
  ST: 10 / 10
  OBC: 10 / 10
  Minority: 8 / 8
  GM: 17 / 17

Primary Needs (6 per need, 10 needs): PASS
  CROP_INSURANCE: 6 / 6
  SOLAR_PUMP_INSTALLATION: 6 / 6
  RAINWATER_HARVESTING: 6 / 6
  MICRO_IRRIGATION_SUPPORT: 6 / 6
  PROTECTED_HORTICULTURE: 6 / 6
  PRODUCTION_CREDIT: 6 / 6
  FARM_MECHANIZATION: 6 / 6
  BOREWELL_IRRIGATION: 6 / 6
  INCOME_SUPPORT: 6 / 6
  SOIL_HEALTH_AND_FERTILIZER: 6 / 6

Tenure Statuses (Pre-Feb 2019: 47, Inheritance: 4, Pure Tenant: 5, Unknown: 4): PASS
  Pre-Feb 2019: 47 / 47
  Post-Feb 2019 Inheritance: 4 / 4
  Pure Tenant: 5 / 5
  Unknown Title Status: 4 / 4

Community Pool (3 Yes, 57 No): PASS
  Yes: 3 / 3
  No: 57 / 57
  Pool Scenario IDs: ['S028', 'S052', 'S066']

Land Types (Dryland: 28, Canal: 10, Borewell: 12, Wetland: 6, Hilly: 4): PASS
  Dryland: 28 / 28
  Canal-irrigated: 10 / 10
  Borewell-irrigated: 12 / 12
  Wetland/valley: 6 / 6
  Hilly/terraced: 4 / 4

--------------------------------------------------
OVERALL STATUS: ALL 8 DIMENSIONS PASSED PERFECTLY!
```

---

## 6. Data Lineage & Attribute Provenance Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       SCENARIO ATTRIBUTE PROVENANCE                          │
├────────────────────────────────┬─────────────────────────────────────────────┤
│ 1. Empirical Distributions     │ Source: NSS 77th Round (Karnataka)          │
│    - Land size class ranges    │ Distributes landholding, crop mixes, and    │
│    - Baseline income estimates │ social group prevalence by agro-climatic    │
│    - Common cropping patterns  │ zone. Does NOT supply statutory flags.      │
├────────────────────────────────┼─────────────────────────────────────────────┤
│ 2. Farmer Voice & Query Intent │ Source: Kisan Call Centre (KCC) Data        │
│    - Query phrasing & dialect  │ Realistic farmer vernacular, seasonal       │
│    - Immediate stated need     │ distress articulation, and specific         │
│    - Crop crisis context       │ pest/weather symptom descriptions.          │
├────────────────────────────────┼─────────────────────────────────────────────┤
│ 3. Explicitly Constructed      │ Source: Official Scheme Statutory Documents │
│    Policy Exclusion Flags      │ NOT extrapolated from income estimates.     │
│    - ITR payment status        │ Synthetically authored to test statutory    │
│    - Land title cut-off date   │ boundaries with clear test rationale.       │
│    - Pension amounts           │ Each flag recorded as True/False/None.      │
│    - Prior subsidy tenure      │                                             │
└────────────────────────────────┴─────────────────────────────────────────────┘
```

> [!CAUTION]
> **Lineage Invariant:** An estimated family income of ₹1.5 Lakh must **never** be automatically converted into an assumed "Income Tax: False" flag. Statutory flags must be explicitly declared as `True`, `False`, or `None` (Unknown) with a clear, documented test rationale for each scenario.

---

## 7. Heuristic Recommendation Baselines (Pre-ML Evaluation Standard)

### 7.1 Baseline 1: Deterministic Need-to-Scheme Mapping

A transparent static lookup mapping the farmer's `immediate_need` to scheme families:

$$\text{Score}_{\text{B1}}(s, \text{need}) = \begin{cases} 3 & \text{if } s \text{ is the primary scheme family for } \text{need} \\ 2 & \text{if } s \text{ is a recognised secondary support scheme for } \text{need} \\ 1 & \text{if } s \text{ is a generic statutory support scheme (e.g. PM-KISAN, Soil Card)} \\ 0 & \text{otherwise} \end{cases}$$

The lookup table is authored before benchmark annotation begins and is locked. It will not be revised using held-out evaluation labels.

### 7.2 Baseline 2: Interpretable Weighted Relevance Score

$$\text{Score}_{\text{B2}} = w_1 \cdot f_{\text{NeedAlign}} + w_2 \cdot f_{\text{CropSuit}} + w_3 \cdot f_{\text{AssetSynergy}} - w_4 \cdot f_{\text{Complexity}}$$

**Pre-specified weights (locked before evaluation):**

| Factor | Weight | Range | Definition |
|:---|:---:|:---:|:---|
| $f_{\text{NeedAlign}}$ | $w_1 = 0.45$ | $[0.0, 1.0]$ | Directness of scheme's core purpose matching the stated need. 1.0 = direct statutory match; 0.5 = related/adjacent benefit; 0.0 = unrelated. |
| $f_{\text{CropSuit}}$ | $w_2 = 0.25$ | $[0.0, 1.0]$ | Scheme applicability to the specific crop (e.g., PMKSY-PDMC drip for sugarcane = 1.0; drip for wetland paddy = 0.2). Sourced from crop-scheme suitability matrix authored before annotation. |
| $f_{\text{AssetSynergy}}$ | $w_3 = 0.15$ | $[0.0, 1.0]$ | Degree to which the scheme enhances existing farm assets without requiring unrequested new prerequisites. 1.0 = synergy with existing assets; 0.0 = requires substantial unrequested infrastructure. |
| $f_{\text{Complexity}}$ | $w_4 = 0.15$ | $[0.0, 1.0]$ | Penalises schemes with major unrequested civil works or implementation barriers (Protocol v1.1 Rule 1). 1.0 = heavy civil works impractical for stated need; 0.0 = no complexity barrier. |

**Tie-breaking rule:** In case of equal $\text{Score}_{\text{B2}}$ values, rank by $f_{\text{NeedAlign}}$ descending, then by scheme ID ascending (deterministic).

**Missing-data handling:** If a factor cannot be computed (e.g. crop-suitability entry missing for an uncommon crop), $f_{\text{missing}} = 0.5$ (neutral/ambiguous) is used, and the case is flagged in the evaluation report as an imputed value.

These weights, the crop-scheme suitability matrix, and factor definitions are all **authored and locked before expert annotation begins**. They will not be tuned using the benchmark evaluation labels.

### 7.3 Evaluation Metrics & ML Justification Gate

Both baselines are evaluated at the **scenario level** (not treating each scheme rating as an independent observation):

| Metric | Definition | Threshold for ML Justification |
|:---|:---|:---:|
| **NDCG@3** | Normalised Discounted Cumulative Gain at rank 3; measures quality of top-3 recommendations | $\Delta \text{NDCG@3} \ge 0.05$ over Baseline 2 |
| **Recall@3** | Proportion of schemes rated $\ge 2$ by experts appearing in top 3 returned | Reported per scenario and in aggregate |

**Relevant-score threshold:** Expert rating $\ge 2$ (Relevant or Highly Relevant) defines a "positive" recommendation. This threshold is defined here, before annotation begins.

**Statistical comparison method:** Scenario-grouped permutation test on NDCG@3 differences. The permutation resampling unit is the **scenario template group**, not the individual scheme rating, to respect the non-independence of ratings within the same scenario.

**ML Decision Rule:** ML ranking models (e.g., LambdaMART, XGBoost Ranker) are only justified if template-grouped cross-validated NDCG@3 shows a statistically significant improvement ($p < 0.05$) over Baseline 2 AND the improvement is consistent across agro-climatic zones, not driven by a single easy subset.

---

## 8. Definition of Done (Benchmark v1.0 Milestone)

- [x] **Coverage Matrix Designed (`benchmark-design-v1.0.1`):** Design across 10 zones, 10 needs, statutory categories.
- [x] **Coverage Matrix Reconciled & Validated (`benchmark-design-v1.0.2`):** All 8 quota dimensions reconciled and passing automated test suite (`validate_benchmark_matrix.py` and `tests/test_benchmark_matrix.py`). Explicit holding, parcel, and subsidy-area columns added; community-pool scenarios clarified.
- [ ] **Scenario Profiles Authored (`S011`–`S070`):** Full JSON + markdown definitions generated in zone batches (strictly deferred until matrix review).
- [ ] **Eligibility Engine Verification:** All 60 scenarios executed through `EligibilityEngine`; zero statutory hallucinations; boundary test cases pass.
- [ ] **Dual-Expert Annotation:** Independent annotations from E1 and E2 under `annotation-protocol-v1.1`.
- [ ] **Inter-Rater Agreement Audit:** $\kappa_w \ge 0.61$, $\alpha \ge 0.67$, all flagged disagreements investigated.
- [ ] **Heuristic Baseline Benchmark:** Baseline 1 and Baseline 2 evaluated on NDCG@3 and Recall@3 using locked weights and pre-specified evaluation protocol.
- [ ] **ML Experimentation Decision Record:** Formal go/no-go determination, documented with baseline comparison results and data-quality audit.
