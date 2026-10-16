# Deliverable: Zone Z9 Execution Report (Scenarios S059–S064)

**Benchmark Version:** `v1.0.4`  
**Execution Date:** October 16, 2026  
**Agro-Climatic Zone:** Hilly Zone (Zone Z9 — Kodagu, Chikkamagaluru, Uttara Kannada)  
**Total Scenarios Evaluated:** Exactly 6 (`S059`–`S064`)  
**Audit Scope:** Exactly six detailed scenarios (`S059`–`S064`) evaluated across all 16 scheme records (8 standalone records, 2 parent records, and 6 child records).  

## 1. Executive Summary & Project Invariants

This report documents the rule-validation and governance audit of the ninth batch of six benchmark scenarios (S059–S064) representing the **Hilly Zone (Zone Z9)**. In strict adherence to project invariants:

1. **Preservation of Frozen Engine (`src/eligibility/engine.py`):** The frozen engine is completely untouched and preserved at baseline commit `7724fa7`. Raw three-valued logic outcomes (`ELIGIBLE`, `INELIGIBLE`, `REQUIRES_VERIFICATION`) are evaluated deterministically.
2. **Preservation of Scheme Master (`scheme_database/processed/scheme_master.json`):** Scheme definitions, hierarchies, and metadata are unmodified.
3. **Preservation of Pilot Scenarios & Protocol:** Pilot scenarios `S001`–`S010` and annotation protocol `v1.1` remain strictly preserved.
4. **Benchmark Design v1.0.4 Compliance:** Strictly fulfills all representation quotas, cross-field area validations, solar pump prerequisites, and statutory inheritance definitions established in `benchmark_v1_design.md` v1.0.4.
5. **Operational Availability Safeguard:** Eligibility verified in Section A does **NOT** equate to active application window availability. All determinations carry availability state `Availability unknown — confirmation required`.
6. **Crop Insurance Decoupling (PMFBY/RWBCIS):** Static whitelist results from the raw engine are decoupled from governance presentation across all six scenarios. Unverified seasonal Insurance Unit (Gram Panchayat/Hobli level) notifications are strictly routed to Section B as `REQUIRES_VERIFICATION` with numerical scoring disabled.
7. **Provisional Schemes Quarantine:** Corporation schemes (`SCH008_KA_COOP`) are strictly quarantined in Section B without clinical scoring.
8. **Challenge 4: Three-Valued Logic & Unknown Title Handling (S062):** Missing land title cut-off date (`land_ownership_cutoff_pre_feb_2019 = None`) strictly returns `REQUIRES_VERIFICATION` in PM-KISAN (`PMKISAN_CUTOFF_DATE_UNKNOWN`) and routes title-dependent schemes to Section B. Universal diagnostic access for Soil Health Card (`SCH009`) is preserved in Section A.
9. **S064 Statutory Inheritance Succession (Clause 3(d)):** Ownership acquired post-01.02.2019 is strictly verified under `transfer_basis = INHERITANCE_DUE_TO_DEATH` resulting from parent demise (Nov 2021), supported by registered death certificate, legal heir order, and Bhoomi mutation extract. Distinct from ineligible post-cutoff partition deeds; qualifies for PM-KISAN in Section A.
10. **S063 Solar Pump Prerequisites & Boundary Test:** Landholding is exactly 2.5 acres (boundary value classified as Small [2.5, 5.0]). Operational water source verified as `Borewell (Non-energized)` and electric status as `UNENERGIZED_OFF_GRID`, qualifying for PM-KUSUM Component B in Section A.
11. **S061 Pure Tenancy Routing (Challenge 5):** Pure tenant without title deed is statutorily excluded from PM-KISAN (`PMKISAN_PURE_TENANT_EXCLUSION`), but qualifies for institutional crop loan credit under KCC (`SCH008_CENTRAL`) tenant guidelines.

## 2. Zone Z9 Scenario Input Overview (S059–S064)

| Scenario ID | District | Primary Crop | Holding (ac) | Land Type | Social Category | Farmer Class | Immediate Need | Operational Water Source | Benchmark Test Purpose |
|:---|:---|:---|:---:|:---|:---:|:---:|:---|:---|:---|
| **S059** | Kodagu | Coffee | 4.5 | Hilly/terraced | General (OC) | Small (2.5-5 acres) | `SOIL_HEALTH_AND_FERTILIZER` | Hillside Stream Catchment | Soil Health Card soil testing for plantation coffee in Hilly... |
| **S060** | Chikkamagaluru | Cardamom | 2.0 | Hilly/terraced | ST | Marginal (< 2.5 acres) | `RAINWATER_HARVESTING` | Hillside Stream Catchment | Water harvesting storage structure for hillside cardamom pla... |
| **S061** | Uttara Kannada | Paddy | 3.0 | Wetland/valley | SC | Small (2.5-5 acres) | `PRODUCTION_CREDIT` | Valley Natural Flow | Challenge 5: Hill zone valley paddy pure tenant; PM-KISAN st... |
| **S062** | Kodagu | Black Pepper | 1.8 | Hilly/terraced | General (OC) | Marginal (< 2.5 acres) | `CROP_INSURANCE` | Hillside Rainfed | Challenge 4: Land title UNKNOWN -> PM-KISAN and title-depend... |
| **S063** | Chikkamagaluru | Coffee | 2.5 | Hilly/terraced | Minority (Muslim) | Small (2.5-5 acres) | `SOLAR_PUMP_INSTALLATION` | Borewell (Non-energized) | Boundary test: Exactly 2.5 ac (Small); water source: unenerg... |
| **S064** | Uttara Kannada | Paddy | 8.0 | Irrigated (Canal) | OBC (2A) | Medium (5-10 acres) | `FARM_MECHANIZATION` | Canal Command | SMAM power tiller/paddy transplanter subsidy; medium holding... |

## 3. Governance Presentation Accounting & Reconciled Denominators

| Scenario | District | Primary Crop | Immediate Need | Section A (Confirmed) | Section B (Review / Unverified) | Disqualified Candidates | Total Actionable | Reconciled Formula |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **S059** | Kodagu | Coffee | `SOIL_HEALTH_AND_FERTILIZER` | **4** | **2** | **9** | **15** | 4 + 2 + 9 = 15 |
| **S060** | Chikkamagaluru | Cardamom | `RAINWATER_HARVESTING` | **4** | **2** | **9** | **15** | 4 + 2 + 9 = 15 |
| **S061** | Uttara Kannada | Paddy | `PRODUCTION_CREDIT` | **3** | **2** | **10** | **15** | 3 + 2 + 10 = 15 |
| **S062** | Kodagu | Black Pepper | `CROP_INSURANCE` | **3** | **3** | **9** | **15** | 3 + 3 + 9 = 15 |
| **S063** | Chikkamagaluru | Coffee | `SOLAR_PUMP_INSTALLATION` | **6** | **2** | **7** | **15** | 6 + 2 + 7 = 15 |
| **S064** | Uttara Kannada | Paddy | `FARM_MECHANIZATION` | **5** | **2** | **8** | **15** | 5 + 2 + 8 = 15 |

### Denominator Reconciliations & Abstract Parent Suppression:
Every scenario evaluates exactly 16 raw scheme records. The number of displayed actionable schemes (exactly 15 in all six scenarios S059–S064) is explicitly reconciled based on whether child records of abstract parents (`SCH008`, `SCH010`) are actionable:

- In **all six scenarios (S059–S064)**: Abstract parent `SCH008` is suppressed because child credit records (`SCH008_CENTRAL`, `SCH008_KA_COOP`) are actionable. In contrast, all four Ganga Kalyana child corporation records are disqualified (`INELIGIBLE`) due to non-dryland topography (Hilly/terraced, Wetland/valley, or Canal command) or category/asset restrictions. Because zero child records are actionable, abstract parent `SCH010` is retained as an ineligible umbrella record $\implies 16 - 1 = \mathbf{15}$ actionable schemes displayed.

## 4. Scenario-by-Scenario Detailed Governance Audits

### 4.9 Scenario S059: Kodagu — Coffee (4.5 ac, General (OC))

- **Context & Need:** Soil Health Card soil testing for plantation coffee in Hilly Zone; universal diagnostic access verified in Section A; Krishi Bhagya and Ganga Kalyana terrain exclusions enforced.
- **Physical Area Consistency:** `PASS: 4.5 ac holding matches parcel`
- **Water Infrastructure:** Hillside Stream Catchment (`NONE`)
- **Statutory Flags:** Tenure=`RTC registered pre-February 2019 in Somwarpet taluk, Kodagu district`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `INELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned INELIGIBLE because Coffee is absent from static crop whiteli... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010` | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

### 4.0 Scenario S060: Chikkamagaluru — Cardamom (2.0 ac, ST)

- **Context & Need:** Water harvesting storage structure for hillside cardamom plantation; ST marginal holding; Krishi Bhagya dryland restriction and Ganga Kalyana terrain exclusions verified.
- **Physical Area Consistency:** `PASS: 2.0 ac holding matches parcel`
- **Water Infrastructure:** Hillside Stream Catchment (`NONE`)
- **Statutory Flags:** Tenure=`RTC registered pre-February 2019 in Mudigere taluk, Chikkamagaluru district`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `INELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned INELIGIBLE because Cardamom is not in the static whitelist. ... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010` | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

### 4.1 Scenario S061: Uttara Kannada — Paddy (3.0 ac, SC)

- **Context & Need:** Challenge 5: Hill zone valley paddy pure tenant; PM-KISAN statutorily excluded; KCC tenant route qualifies in Section A; PMFBY routed to Section B pending lease verification.
- **Physical Area Consistency:** `PASS: 3.0 ac holding matches parcel`
- **Water Infrastructure:** Valley Natural Flow (`NONE`)
- **Statutory Flags:** Tenure=`Informal lease agreement / oral tenancy with village panchayat certificate in Sirsi taluk; no recorded title (Pure Tenant)`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Pure tenant farmer without recorded land ownership title is statutorily excluded... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned ELIGIBLE based on static crop whitelist for Paddy, but appli... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010` | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

### 4.2 Scenario S062: Kodagu — Black Pepper (1.8 ac, General (OC))

- **Context & Need:** Challenge 4: Land title UNKNOWN -> PM-KISAN and title-dependent schemes trigger REQUIRES_VERIFICATION in Section B; PMFBY routed to Section B; Soil Health Card ELIGIBLE in Section A.
- **Physical Area Consistency:** `PASS: 1.8 ac holding matches parcel`
- **Water Infrastructure:** Hillside Rainfed (`NONE`)
- **Statutory Flags:** Tenure=`Ancestral land title partition deed pending mutation in Virajpet taluk; record date unverified on RTC (UNKNOWN)`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Unresolved Statutory Evidence / Land Title Required) | No | Raw engine returned REQUIRES_VERIFICATION due to explicit UNKNOWN tenure cut-off... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `INELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned INELIGIBLE due to static whitelist, but Black Pepper is cove... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010` | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

### 4.3 Scenario S063: Chikkamagaluru — Coffee (2.5 ac, Minority (Muslim))

- **Context & Need:** Boundary test: Exactly 2.5 ac (Small); water source: unenergized borewell; electric status: UNENERGIZED_OFF_GRID; PM-KUSUM B solar pump qualifies in Section A; Minority.
- **Physical Area Consistency:** `PASS: 2.5 ac holding matches parcel`
- **Water Infrastructure:** Borewell (Non-energized) (`UNENERGIZED_OFF_GRID`)
- **Statutory Flags:** Tenure=`RTC registered pre-February 2019 in Koppa taluk, Chikkamagaluru district`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `INELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned INELIGIBLE due to static crop whitelist, but Coffee is cover... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Solar Pump Prerequisite Verification: Landholding is exactly 2.5 acres (boundary... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010` | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

### 4.4 Scenario S064: Uttara Kannada — Paddy (8.0 ac, OBC (2A))

- **Context & Need:** SMAM power tiller/paddy transplanter subsidy; medium holding (8.0 ac); post-2019 statutory inheritance upon demise of parent (transfer_basis=INHERITANCE_DUE_TO_DEATH, legal heir cert & mutation verified; distinct from ineligible partition deed); PM-KISAN qualifies in Section A.
- **Physical Area Consistency:** `PASS: 8.0 ac holding matches parcel`
- **Water Infrastructure:** Canal Command (`NONE`)
- **Statutory Flags:** Tenure=`Title acquired via registered inheritance succession following demise of father in Nov 2021; Death Cert No. DC/UK/2021/8841, Legal Heir Certificate LHC/UK/2022/412, and Bhoomi mutation Form 16 MR No. 2022-T209 (18.03.2022) verified`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Statutory Inheritance Compliance: Title acquired post-01.02.2019 strictly satisf... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned ELIGIBLE based on static crop whitelist, but commercial crop... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010` | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

## 5. Unresolved Dependencies & Verification Log

The following verification dependencies remain active and are enforced across Zone Z9:

### S059 (Kodagu — Coffee)
- Verification of GoK Kharif 2026 RWBCIS/PMFBY Insurance Unit notification for plantation crops in Somwarpet taluk, Kodagu district
- Kodagu District Agriculture Department Soil Health Card laboratory schedule for Somwarpet taluk

### S060 (Chikkamagaluru — Cardamom)
- Verification of GoK Kharif 2026 RWBCIS/PMFBY Insurance Unit notification for Cardamom in Mudigere taluk, Chikkamagaluru district
- Chikkamagaluru District Horticulture Department on-farm water storage structure subsidy guidelines for FY 2026-27

### S061 (Uttara Kannada — Paddy)
- Verification of GoK Kharif 2026 PMFBY Insurance Unit notification and tenant declaration protocol for Paddy in Sirsi taluk, Uttara Kannada district
- Lead District Bank / Commercial bank PACS tenant crop loan documentation verification for Sirsi taluk

### S062 (Kodagu — Black Pepper)
- Revenue Department certification of land title record date (RTC mutation extract) for Virajpet taluk
- Verification of GoK Kharif 2026 RWBCIS Insurance Unit notification for Black Pepper in Virajpet taluk, Kodagu district

### S063 (Chikkamagaluru — Coffee)
- Verification of GoK Kharif 2026 RWBCIS/PMFBY Insurance Unit notification for Coffee in Koppa taluk, Chikkamagaluru district
- KREDL PM-KUSUM Component B FY 2026-27 vendor empannelment and beneficiary portal status

### S064 (Uttara Kannada — Paddy)
- Verification of GoK Kharif 2026 PMFBY Insurance Unit notification for Paddy in Yellapur taluk, Uttara Kannada district
- Uttara Kannada District Agriculture Joint Director SMAM FY 2026-27 power tiller/transplanter target circular

## 6. Frozen Invariants Check

| Invariant Component | Status | Verification Summary |
|:---|:---:|:---|
| `src/eligibility/engine.py` | **PRESERVED** | Untouched; raw evaluations deterministic |
| `scheme_database/processed/scheme_master.json` | **PRESERVED** | Untouched; 16 scheme records intact |
| Pilot Scenarios `S001`–`S010` | **PRESERVED** | Untouched; baseline calibration valid |
| Annotation Protocol `v1.1` | **PRESERVED** | Untouched; governance presentation standards maintained |
| Benchmark Design `v1.0.4` | **COMPLIANT** | All Z9 quotas, area caps, and tenure rules strictly satisfied |

