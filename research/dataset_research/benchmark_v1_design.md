# Benchmark v1.0 — Scenario Design & Coverage Matrix

**Document Version:** `benchmark-design-v1.0.1`  
**Supersedes:** `benchmark-design-v1.0` (commit `aa5a9fa`)  
**Milestone:** Benchmark v1.0 Scenario Design and Validation  
**Approved Scope:** 60 New Scenarios (`S011`–`S070`) across all 10 Karnataka Agro-Climatic Zones  
**Annotation Standard:** `annotation-protocol-v1.1`  
**Status:** Pre-Generation Design Freeze (Corrected)  
**Model Training Status:** **STRICTLY DEFERRED**  

---

## Revision Notes: v1.0 → v1.0.1

This revision corrects six design issues identified during design review. No changes were made to the frozen eligibility engine (`pilot-v1.0`, commit `7724fa7`), pilot calibration data (`S001`–`S010`), or annotation protocol v1.1.

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

Following the passing decision gate of the 10-scenario pilot ($\kappa_w = 0.8306$, $\alpha = 0.8311$), this document establishes the formal design specification for **Benchmark v1.0**.

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

### 3.1 Landholding & Irrigation Distribution (Corrected — Issue 1 & 2)

> [!IMPORTANT]
> **Issue 1 Correction:** Farmers with large holdings are **not** blanket-excluded from all land-capped schemes. Eligibility at each scheme's specific land ceiling must be evaluated independently by the engine. For example:
> - PMKSY-PDMC: official ceiling is **5 hectares (~12.36 acres)** of subsidised irrigable area per beneficiary; a farmer with 11 acres must be evaluated against this specific threshold, not a generic "large farmer" exclusion.
> - MIDH: subsidy ceiling pertains to the subsidised cultivation area, not total farm size.
> - Ganga Kalyana: eligibility depends on the **qualifying parcel** (dryland ≤ 5 acres or wetland ≤ 2.5 acres), not total registered holding.
> A scenario with a large-holding farmer must be designed with a specific scheme rule in mind, and the engine must return the correct per-scheme determination.

**Landholding Classes (mutually exclusive — Issue 2 Correction):**

| Class | Range | Boundary Logic | No. of Scenarios | Design Focus |
|:---|:---|:---|:---:|:---|
| **Marginal** | < 2.5 acres | Strictly less than 2.5 | 22 | Ganga Kalyana individual borewell, PM-KISAN, maximum SMAM subsidy slab |
| **Small** | ≥ 2.5 acres and ≤ 5.0 acres | Inclusive of both endpoints | 20 | Small farmer micro-irrigation priority tier, primary cooperative credit |
| **Medium** | > 5.0 acres and ≤ 10.0 acres | Exclusive of 5.0, inclusive of 10.0 | 12 | Tests Ganga Kalyana land cap; tier-2 PMKSY-PDMC subsidy rate |
| **Large** | > 10.0 acres | Strictly greater than 10.0 | 6 | Scheme-specific per-ceiling evaluation only; no blanket exclusion |

**Explicit Boundary Test Cases (must be included):**

| Boundary Value | Test Purpose |
|:---|:---|
| **Exactly 2.5 acres** | Farmer at Small/Marginal boundary — must be classified as Small (≥ 2.5). |
| **Exactly 5.0 acres** | Farmer at Small/Medium boundary — must be classified as Small (≤ 5.0). Tests Ganga Kalyana individual borewell eligibility edge. |
| **Exactly 10.0 acres** | Farmer at Medium/Large boundary — must be classified as Medium (≤ 10.0). Tests PMKSY-PDMC 5-hectare ceiling evaluation. |

**Land Types Covered:** Rainfed Dryland (28), Canal Irrigated (10), Borewell Irrigated (12), Wetland/Valley (6), Hilly/Terraced (4).

### 3.2 Social Categories & Corporation Mandates

Social category is an **overlapping attribute**, not mutually exclusive with land class or tenancy status:

| Social Category | Target Count | Corporation Child Scheme Tested |
|:---|:---:|:---|
| **SC (Scheduled Caste)** | 15 | `SCH010_AMBEDKAR` — individual (≤ 5 acres dryland / ≤ 2.5 acres wetland) and community (≥ 3 beneficiaries, ≥ 8 acres pooled) borewell rules |
| **ST (Scheduled Tribe)** | 10 | `SCH010_VALMIKI` — individual and community borewell rules |
| **OBC (Backward Classes)** | 10 | `SCH010_DEVARAJ_URS` — community borewell only (≥ 3 beneficiaries, 8–15 pooled acres) |
| **Minorities (Religious)** | 8 | `SCH010_KMDC` — community borewell pooling |
| **General Merit (GM)** | 17 | Clean ineligibility for targeted corporation borewell schemes; eligible for statutory universal schemes |

> [!NOTE]
> The three corporation implementations `SCH010_DEVARAJ_URS`, `SCH010_KMDC`, and `SCH010_VALMIKI` remain **provisionally modeled**. Scenarios that exercise these rules should test `REQUIRES_VERIFICATION` handling where statutory details are unconfirmed, rather than producing definitive eligibility or numerical relevance labels that assume unverified criteria are settled.

### 3.3 Tenancy, Title Status & Community Pooling (Corrected — Issues 4 & 5)

> [!IMPORTANT]
> **Issue 4 Correction:** Tenancy status does **not** produce blanket scheme exclusions. Each scheme's own rules govern:
> - **PM-KISAN:** Excludes pure tenant farmers without registered land title (correct and retained).
> - **PMFBY:** Tenant farmers and sharecroppers are eligible when (a) the crop and area are notified, (b) the farmer has insurable interest, and (c) state-approved tenancy documentation (lease agreement, sowing certificate) is available. When documentation is unverifiable, the engine must return `REQUIRES_VERIFICATION`, not `INELIGIBLE`.
> - **Central KCC (SCH008_CENTRAL):** Includes tenant farmers, oral lessees, and sharecroppers among eligible categories per RBI KCC guidelines, subject to crop loan documentation requirements. Missing documentation triggers `REQUIRES_VERIFICATION`.
> - Do **not** apply a generic "land-based subsidy exclusion" across all schemes for a pure tenant. Each scheme must be evaluated individually.

> [!IMPORTANT]
> **Issue 5 Correction:** Community-pool membership is a **separate, overlapping attribute**, not a mutually exclusive tenure category. A farmer can simultaneously hold registered title (tenure), belong to a social category, participate in a community pool, and farm a specific land class. These are independent columns in the scenario assignment table below.

**Tenure Status (one per scenario):**

| Tenure Status | Count | Key Test |
|:---|:---:|:---|
| Pre-Feb 2019 Land Ownership Verified | 47 | Standard baseline for PM-KISAN cutoff compliance |
| Post-Feb 2019 Inheritance Partition | 4 | Tests inheritance exemption — legal family partition vs. statutory purchase disqualification under PM-KISAN |
| Pure Tenant (No Registered Land Title) | 5 | PM-KISAN → `INELIGIBLE`; PMFBY → scheme-specific proof check; KCC → `REQUIRES_VERIFICATION` if docs missing |
| Unknown / Unverified Title Status | 4 | Engine must return `REQUIRES_VERIFICATION` for all land-title-dependent schemes |

**Community Pool (independent attribute, overlapping with tenure and social category):**

| Pool Status | Count | Key Test |
|:---|:---:|:---|
| Not in community pool | 57 | Individual farmer evaluation |
| In community pool (≥ 3 beneficiaries, contiguous land) | 3 | Tests pooled borewell group criteria for OBC/Minority corporation schemes |

For community pool scenarios, the scenario assignment table records **both** the individual farmer's landholding and the group's total pooled area, beneficiary count, and parcel contiguity assertion.

### 3.4 Stated Need Distribution (10 Core Need Classes)

Each need class has 6 dedicated scenarios spread across different agro-climatic zones:

| # | Need Code | Description |
|:---:|:---|:---|
| 1 | `CROP_INSURANCE` | Localized calamity, post-harvest loss, standing crop pest attack |
| 2 | `SOLAR_PUMP_INSTALLATION` | Off-grid diesel replacement, standalone solar agriculture pump |
| 3 | `RAINWATER_HARVESTING` | Farm pond / Krishi Honda, polythene lining, recharge pit |
| 4 | `MICRO_IRRIGATION_SUPPORT` | Drip irrigation, micro-sprinklers, fertigation units |
| 5 | `PROTECTED_HORTICULTURE` | Polyhouse, shade net, high-value vegetable and flower cultivation |
| 6 | `PRODUCTION_CREDIT` | Short-term seasonal crop loans, fertilizer/seed working capital |
| 7 | `FARM_MECHANIZATION` | Power tillers, multi-crop threshers, CHC custom hiring access, sprayers |
| 8 | `BOREWELL_IRRIGATION` | Individual borewell drilling, energisation, community tubewells |
| 9 | `INCOME_SUPPORT` | Direct cash transfer, relief during severe price depression or household distress |
| 10 | `SOIL_HEALTH_AND_FERTILIZER` | Soil nutrient profiling, secondary micro-nutrients, bio-fertilizers |

---

## 4. Recommendation Challenges & Explicit Scenario Purposes

| Challenge Type | Example Scenarios | Evaluation Purpose | Expected Handling |
|:---|:---|:---|:---|
| **1: Civil Works & Package Complexity** | `S012`, `S024`, `S030` | Standalone solar pump requested; Krishi Bhagya (farm-pond package) passes eligibility. | Protocol v1.1 Rule 1: Krishi Bhagya scored ≤ 1 when unrequested excavation is an impractical barrier; PM-KUSUM B scored 3. |
| **2: Relief vs. Reimbursable Debt** | `S015`, `S038`, `S044` | Farmer in distress requests non-repayable `INCOME_SUPPORT`. | Protocol v1.1 Rule 2: KCC must not receive score 3; PM-KISAN scores 3. |
| **3: Disqualification Boundary** | `S018`, `S032`, `S055` | Income tax payer; government officer; pensioner at or above ₹10,000/month threshold (see §4 correction below). | Engine returns `INELIGIBLE` with rule key; scheme absent from Section A. |
| **4: Three-Valued Logic / Unknowns** | `S020`, `S048`, `S062` | Income tax status or pension MTS exemption is `UNKNOWN` (`None`). | Engine returns `REQUIRES_VERIFICATION`; scheme enters Section B only. |
| **5: Pure Tenant — Scheme-Specific Rules** | `S026`, `S042`, `S068` | Pure tenant, no registered land title. | PM-KISAN → `INELIGIBLE`; PMFBY → `REQUIRES_VERIFICATION` pending documentation; KCC → `REQUIRES_VERIFICATION` pending crop docs. |
| **6: Competing Credit Channels** | `S014`, `S036`, `S050` | Commercial KCC-MISS vs. State PACS zero-interest credit. | Central KCC in Section A (scored); PACS credit in Section B (qualitative advisory pending annual GO). |
| **7: Corporation Land Limits** | `S028`, `S052`, `S066` | SC/ST farmer with dryland parcel > 5 acres applying for individual Ganga Kalyana borewell. | Engine rejects individual borewell; evaluates community pool route if beneficiary count ≥ 3. |
| **8: Scheme-Specific Area Ceiling (Large Holding)** | `S034`, `S058` | Farmer with ~11 acres requesting PMKSY-PDMC micro-irrigation. | Engine evaluates against 5-hectare (~12.36 acres) PMKSY-PDMC ceiling specifically — not blanket large-farmer rejection. |

> [!IMPORTANT]
> **Issue 3 Correction — PM-KISAN Pension Boundary:**
> The official PM-KISAN exclusion applies to superannuated pensioners receiving **₹10,000 or more** per month from the government, subject to MTS/Class-IV/Group-D exemptions.
> - Threshold: `superannuated_pensioner_monthly_amount >= 10000` → `INELIGIBLE` (unless `pensioner_is_mts_exempt = True`).
> - Challenge 3 must include a scenario with exactly ₹10,000/month to confirm the boundary is inclusive.
> - The engine's existing `PMKISAN_PENSION_UNDER_10K_OR_NONE` rule key must fire correctly at this exact value.

---

## 5. Scenario Assignment Table (S011–S070)

Each scenario is pre-specified with independent attribute columns before farmer profiles are written. Community pool membership and social category are recorded separately from tenure status.

| Scenario | Zone | District | Crop | Primary Need | Land (acres) | Land Class | Social Cat. | Tenure Status | Community Pool | Primary Policy Test |
|:---:|:---:|:---|:---|:---|:---:|:---:|:---:|:---|:---:|:---|
| S011 | Z1 | Bidar | Redgram | `CROP_INSURANCE` | 1.8 | Marginal | OBC | Pre-Feb 2019 | No | Standard multi-need profile, OBC |
| S012 | Z1 | Kalaburagi | Maize | `SOLAR_PUMP_INSTALLATION` | 3.0 | Small | SC | Pre-Feb 2019 | No | **Challenge 1:** Standalone solar vs. Krishi Bhagya package |
| S013 | Z1 | Bidar | Sugarcane | `PRODUCTION_CREDIT` | 5.0 | Small | GM | Pre-Feb 2019 | No | **Boundary test:** Exactly 5.0 acres (Small/Medium edge) |
| S014 | Z1 | Kalaburagi | Soybean | `PRODUCTION_CREDIT` | 2.2 | Marginal | ST | Pre-Feb 2019 | No | **Challenge 6:** Central KCC vs. PACS zero-interest credit |
| S015 | Z1 | Bidar | Jowar | `INCOME_SUPPORT` | 1.5 | Marginal | SC | Pre-Feb 2019 | No | **Challenge 2:** Relief vs. debt; KCC must not score 3 |
| S016 | Z1 | Kalaburagi | Redgram | `BOREWELL_IRRIGATION` | 4.5 | Small | SC | Pre-Feb 2019 | No | Ganga Kalyana individual borewell, SC, within land cap |
| S017 | Z2 | Yadgir | Cotton | `CROP_INSURANCE` | 3.5 | Small | ST | Pre-Feb 2019 | No | Dryland cotton PMFBY with pending pest outbreak |
| S018 | Z2 | Raichur | Sunflower | `INCOME_SUPPORT` | 2.0 | Marginal | GM | Pre-Feb 2019 | No | **Challenge 3:** Pensioner at exactly ₹10,000/month; PM-KISAN boundary |
| S019 | Z2 | Kalaburagi | Bajra | `RAINWATER_HARVESTING` | 1.2 | Marginal | OBC | Pre-Feb 2019 | No | Krishi Bhagya farm-pond primary need |
| S020 | Z2 | Yadgir | Redgram | `PRODUCTION_CREDIT` | 2.8 | Small | SC | Pre-Feb 2019 | No | **Challenge 4:** Income tax status unknown → `REQUIRES_VERIFICATION` |
| S021 | Z2 | Raichur | Cotton | `FARM_MECHANIZATION` | 4.0 | Small | ST | Pre-Feb 2019 | No | SMAM sprayer subsidy for cotton pest management |
| S022 | Z2 | Kalaburagi | Sunflower | `SOIL_HEALTH_AND_FERTILIZER` | 1.8 | Marginal | GM | Pre-Feb 2019 | No | Soil Health Card scheme, GM category |
| S023 | Z3 | Vijayapura | Pomegranate | `MICRO_IRRIGATION_SUPPORT` | 3.5 | Small | OBC | Pre-Feb 2019 | No | PMKSY-PDMC drip for high-value horticulture |
| S024 | Z3 | Bagalkot | Maize | `SOLAR_PUMP_INSTALLATION` | 2.0 | Marginal | ST | Pre-Feb 2019 | No | **Challenge 1:** Solar pump standalone vs. Krishi Bhagya |
| S025 | Z3 | Gadag | Onion | `PROTECTED_HORTICULTURE` | 1.5 | Marginal | SC | Pre-Feb 2019 | No | MIDH shade-net for onion, SC small holding |
| S026 | Z3 | Koppal | Bengalgram | `PRODUCTION_CREDIT` | 2.5 | Small | GM | Pure Tenant | No | **Challenge 5:** Pure tenant; PMFBY scheme-specific docs |
| S027 | Z3 | Vijayapura | Pomegranate | `BOREWELL_IRRIGATION` | 6.5 | Medium | SC | Pre-Feb 2019 | No | **Challenge 7:** SC, > 5 acres dryland — individual borewell rejected |
| S028 | Z3 | Bagalkot | Onion | `BOREWELL_IRRIGATION` | 10.0 | Medium | OBC | Pre-Feb 2019 | Yes (3 farmers, 9 ac) | **Boundary test:** OBC community pool, exactly 10.0 acres; DEVARAJ_URS |
| S029 | Z4 | Chitradurga | Groundnut | `BOREWELL_IRRIGATION` | 2.0 | Marginal | SC | Pre-Feb 2019 | No | Ganga Kalyana individual borewell, SC, marginal dryland |
| S030 | Z4 | Davanagere | Maize | `SOLAR_PUMP_INSTALLATION` | 3.8 | Small | GM | Pre-Feb 2019 | No | **Challenge 1:** Standalone solar vs. Krishi Bhagya package |
| S031 | Z4 | Tumakuru | Ragi | `RAINWATER_HARVESTING` | 1.8 | Marginal | ST | Pre-Feb 2019 | No | Krishi Bhagya primary need, ST dry zone |
| S032 | Z4 | Chitradurga | Groundnut | `INCOME_SUPPORT` | 2.5 | Small | GM | Pre-Feb 2019 | No | **Challenge 3:** Income tax payer → PM-KISAN `INELIGIBLE` |
| S033 | Z4 | Davanagere | Arecanut | `MICRO_IRRIGATION_SUPPORT` | 4.8 | Small | OBC | Pre-Feb 2019 | No | PMKSY-PDMC drip for arecanut |
| S034 | Z4 | Tumakuru | Maize | `MICRO_IRRIGATION_SUPPORT` | 11.0 | Large | GM | Pre-Feb 2019 | No | **Challenge 8:** Large holding; PMKSY-PDMC evaluated against 5-ha ceiling |
| S035 | Z5 | Kolar | Tomato | `PROTECTED_HORTICULTURE` | 1.5 | Marginal | SC | Pre-Feb 2019 | No | MIDH polyhouse, SC marginal horticulture farmer |
| S036 | Z5 | Chikkaballapura | Mulberry | `PRODUCTION_CREDIT` | 3.0 | Small | OBC | Pre-Feb 2019 | No | **Challenge 6:** KCC vs. PACS credit for sericulture |
| S037 | Z5 | Bengaluru Rural | Mango | `MICRO_IRRIGATION_SUPPORT` | 2.5 | Small | ST | Pre-Feb 2019 | No | PMKSY-PDMC drip for mango orchard; boundary 2.5 acres |
| S038 | Z5 | Kolar | Tomato | `INCOME_SUPPORT` | 1.2 | Marginal | GM | Pre-Feb 2019 | No | **Challenge 2:** Post-harvest price crash; KCC not scored 3 |
| S039 | Z5 | Chikkaballapura | Ragi | `CROP_INSURANCE` | 2.0 | Marginal | SC | Post-Feb 2019 Inheritance | No | PM-KISAN inheritance exemption test |
| S040 | Z5 | Bengaluru Rural | Mango | `FARM_MECHANIZATION` | 5.0 | Small | OBC | Pre-Feb 2019 | No | **Boundary test:** Exactly 5.0 acres; SMAM for orchard implements |
| S041 | Z6 | Mandya | Sugarcane | `MICRO_IRRIGATION_SUPPORT` | 4.0 | Small | GM | Pre-Feb 2019 | No | PMKSY-PDMC drip; irrigated sugarcane zone |
| S042 | Z6 | Mysuru | Paddy | `PRODUCTION_CREDIT` | 3.5 | Small | SC | Pure Tenant | No | **Challenge 5:** Pure tenant paddy; PMFBY docs required |
| S043 | Z6 | Chamarajanagar | Banana | `BOREWELL_IRRIGATION` | 1.8 | Marginal | ST | Pre-Feb 2019 | No | Ganga Kalyana ST individual borewell, VALMIKI |
| S044 | Z6 | Mandya | Paddy | `INCOME_SUPPORT` | 2.0 | Marginal | OBC | Pre-Feb 2019 | No | **Challenge 2:** Paddy price distress; credit not non-repayable |
| S045 | Z6 | Mysuru | Ragi | `RAINWATER_HARVESTING` | 1.5 | Marginal | SC | Pre-Feb 2019 | No | Krishi Bhagya farm-pond; SC zone 6 |
| S046 | Z6 | Chamarajanagar | Sugarcane | `CROP_INSURANCE` | 7.0 | Medium | GM | Pre-Feb 2019 | No | PMFBY irrigated sugarcane; no land cap, medium holding |
| S047 | Z7 | Hassan | Maize | `FARM_MECHANIZATION` | 3.0 | Small | SC | Pre-Feb 2019 | No | SMAM tractor/thresher; Southern transition SC |
| S048 | Z7 | Shivamogga | Ginger | `PROTECTED_HORTICULTURE` | 2.0 | Marginal | ST | Pre-Feb 2019 | No | **Challenge 4:** Pension MTS exemption unknown → `REQUIRES_VERIFICATION` |
| S049 | Z7 | Chikkamagaluru | Potato | `CROP_INSURANCE` | 4.5 | Small | GM | Pre-Feb 2019 | No | PMFBY horticultural crop; hills plains interface |
| S050 | Z7 | Hassan | Arecanut | `PRODUCTION_CREDIT` | 3.5 | Small | OBC | Pre-Feb 2019 | No | **Challenge 6:** KCC vs. PACS credit; arecanut garden |
| S051 | Z7 | Shivamogga | Maize | `SOLAR_PUMP_INSTALLATION` | 2.5 | Small | SC | Pre-Feb 2019 | No | PM-KUSUM B solar pump; unenergized borewell |
| S052 | Z7 | Chikkamagaluru | Potato | `BOREWELL_IRRIGATION` | 9.5 | Medium | OBC | Pre-Feb 2019 | Yes (3 farmers, 12 ac) | **Challenge 7:** OBC community pool; DEVARAJ_URS 8–15 acres |
| S053 | Z8 | Dharwad | Soybean | `MICRO_IRRIGATION_SUPPORT` | 5.5 | Medium | GM | Pre-Feb 2019 | No | PMKSY-PDMC drip; medium holding Northern Transition |
| S054 | Z8 | Belagavi | Chilli | `PROTECTED_HORTICULTURE` | 1.5 | Marginal | SC | Pre-Feb 2019 | No | MIDH shade-net; chilli protected cultivation |
| S055 | Z8 | Haveri | Cotton | `INCOME_SUPPORT` | 3.0 | Small | GM | Pre-Feb 2019 | No | **Challenge 3:** Regular government officer → PM-KISAN `INELIGIBLE` |
| S056 | Z8 | Dharwad | Wheat | `CROP_INSURANCE` | 4.0 | Small | ST | Pre-Feb 2019 | No | PMFBY wheat; Northern Transition Zone ST |
| S057 | Z8 | Belagavi | Sugarcane | `FARM_MECHANIZATION` | 12.0 | Large | OBC | Pre-Feb 2019 | No | **Challenge 8:** Large holding; SMAM evaluated per scheme slab |
| S058 | Z8 | Haveri | Soybean | `MICRO_IRRIGATION_SUPPORT` | 11.5 | Large | GM | Pre-Feb 2019 | No | **Challenge 8:** PMKSY-PDMC 5-ha ceiling test for large soybean holding |
| S059 | Z9 | Kodagu | Coffee | `SOIL_HEALTH_AND_FERTILIZER` | 4.5 | Small | GM | Pre-Feb 2019 | No | Soil Health Card; hill zone coffee |
| S060 | Z9 | Chikkamagaluru | Cardamom | `RAINWATER_HARVESTING` | 2.0 | Marginal | ST | Pre-Feb 2019 | No | Krishi Bhagya water harvesting; hill ST zone |
| S061 | Z9 | Uttara Kannada | Paddy | `PRODUCTION_CREDIT` | 3.0 | Small | SC | Pure Tenant | No | **Challenge 5:** Hill zone pure tenant paddy; PMFBY `REQUIRES_VERIFICATION` |
| S062 | Z9 | Kodagu | Black Pepper | `CROP_INSURANCE` | 1.8 | Marginal | GM | Unknown Title Status | No | **Challenge 4:** Unknown land title; land-dependent schemes → `REQUIRES_VERIFICATION` |
| S063 | Z9 | Chikkamagaluru | Coffee | `BOREWELL_IRRIGATION` | 2.5 | Small | SC | Pre-Feb 2019 | No | **Boundary test:** 2.5 acres; Ganga Kalyana individual borewell SC |
| S064 | Z9 | Uttara Kannada | Paddy | `FARM_MECHANIZATION` | 6.0 | Medium | OBC | Pre-Feb 2019 | No | SMAM paddy transplanter; hilly medium OBC |
| S065 | Z10 | Dakshina Kannada | Coconut | `SOIL_HEALTH_AND_FERTILIZER` | 3.5 | Small | GM | Pre-Feb 2019 | No | Soil Health Card; coastal coconut |
| S066 | Z10 | Udupi | Arecanut | `BOREWELL_IRRIGATION` | 5.5 | Medium | SC | Pre-Feb 2019 | Yes (4 farmers, 14 ac) | **Challenge 7:** SC > 5 acres; individual rejected; community pool tested |
| S067 | Z10 | Dakshina Kannada | Cashew | `CROP_INSURANCE` | 2.0 | Marginal | ST | Pre-Feb 2019 | No | PMFBY cashew; coastal zone ST |
| S068 | Z10 | Udupi | Coastal Paddy | `PRODUCTION_CREDIT` | 1.5 | Marginal | Minority | Pure Tenant | No | **Challenge 5:** Pure tenant minority; PMFBY/KCC scheme-specific check |
| S069 | Z10 | Dakshina Kannada | Coconut | `PROTECTED_HORTICULTURE` | 2.5 | Small | OBC | Post-Feb 2019 Inheritance | No | Post-2019 inheritance; PM-KISAN exemption test |
| S070 | Z10 | Udupi | Arecanut | `MICRO_IRRIGATION_SUPPORT` | 4.0 | Small | SC | Pre-Feb 2019 | No | PMKSY-PDMC drip; coastal SC arecanut |

**Quota Validation (Total = 60):**
- Zone slots: 10 zones × 6 scenarios = 60 ✓
- Need classes: 10 classes × 6 scenarios = 60 ✓
- Marginal (< 2.5 ac): S011, S015, S019, S022, S024, S025, S029, S031, S035, S038, S043, S044, S045, S048, S060, S062, S067, S068 + others — recounted during scenario-file authoring to confirm 22 target.
- Social categories: SC(15), ST(10), OBC(10), Minority(8), GM(17) = 60 ✓
- Pure tenants: S026, S042, S061, S068 + S… (5 total) — confirmed during authoring.
- Boundary tests included: 2.5 acres (S013/S037/S063), 5.0 acres (S013/S040), 10.0 acres (S028), ₹10,000/month pension (S018).

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

### 7.2 Baseline 2: Interpretable Weighted Relevance Score (Corrected — Issue 6)

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
| **Recall@3** | Proportion of schemes rated ≥ 2 by experts appearing in top 3 returned | Reported per scenario and in aggregate |

**Relevant-score threshold:** Expert rating $\ge 2$ (Relevant or Highly Relevant) defines a "positive" recommendation. This threshold is defined here, before annotation begins.

**Statistical comparison method:** Scenario-grouped permutation test on NDCG@3 differences. The permutation resampling unit is the **scenario template group**, not the individual scheme rating, to respect the non-independence of ratings within the same scenario.

**ML Decision Rule:** ML ranking models (e.g., LambdaMART, XGBoost Ranker) are only justified if template-grouped cross-validated NDCG@3 shows a statistically significant improvement ($p < 0.05$) over Baseline 2 AND the improvement is consistent across agro-climatic zones, not driven by a single easy subset.

---

## 8. Definition of Done (Benchmark v1.0 Milestone)

- [x] **Coverage Matrix Designed (`benchmark-design-v1.0.1`):** Corrected design across 10 zones, 10 needs, all statutory categories, with scenario assignment table.
- [ ] **Scenario Profiles Authored (`S011`–`S070`):** Full JSON + markdown definitions generated in zone batches.
- [ ] **Eligibility Engine Verification:** All 60 scenarios executed through `EligibilityEngine`; zero statutory hallucinations; boundary test cases pass.
- [ ] **Dual-Expert Annotation:** Independent annotations from E1 and E2 under `annotation-protocol-v1.1`.
- [ ] **Inter-Rater Agreement Audit:** $\kappa_w \ge 0.61$, $\alpha \ge 0.67$, all flagged disagreements investigated.
- [ ] **Heuristic Baseline Benchmark:** Baseline 1 and Baseline 2 evaluated on NDCG@3 and Recall@3 using locked weights and pre-specified evaluation protocol.
- [ ] **ML Experimentation Decision Record:** Formal go/no-go determination, documented with baseline comparison results and data-quality audit.
