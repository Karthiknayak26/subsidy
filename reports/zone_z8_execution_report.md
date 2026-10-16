# Deliverable: Zone Z8 Execution Report (Scenarios S053–S058)

**Benchmark Version:** `v1.0.4`  
**Execution Date:** October 16, 2026  
**Agro-Climatic Zone:** Northern Transition Zone (Zone Z8 — Dharwad, Belagavi, Haveri)  
**Total Scenarios Evaluated:** Exactly 6 (`S053`–`S058`)  
**Audit Scope:** Exactly six detailed scenarios (`S053`–`S058`) evaluated across all 16 scheme records (6 parent/standalone + 10 child/standalone).  

## 1. Executive Summary & Project Invariants

This report documents the rule-validation and governance audit of the eighth batch of six benchmark scenarios (S053–S058) representing the **Northern Transition Zone (Zone Z8)**. In strict adherence to project invariants:

1. **Preservation of Frozen Engine (`src/eligibility/engine.py`):** The frozen engine is completely untouched and preserved at baseline commit `7724fa7`. Raw three-valued logic outcomes (`ELIGIBLE`, `INELIGIBLE`, `REQUIRES_VERIFICATION`) are evaluated deterministically.
2. **Preservation of Scheme Master (`scheme_database/processed/scheme_master.json`):** Scheme definitions, hierarchies, and metadata are unmodified.
3. **Preservation of Pilot Scenarios & Protocol:** Pilot scenarios `S001`–`S010` and annotation protocol `v1.1` remain strictly preserved.
4. **Benchmark Design v1.0.4 Compliance:** Strictly fulfills all representation quotas, cross-field area validations, solar pump prerequisites, and statutory inheritance definitions established in `benchmark_v1_design.md` v1.0.4.
5. **Operational Availability Safeguard:** Eligibility verified in Section A does **NOT** equate to active application window availability. All determinations carry availability state `Availability unknown — confirmation required`.
6. **Crop Insurance Decoupling (PMFBY/RWBCIS):** Static whitelist results from the raw engine are decoupled from governance presentation across all six scenarios. Unverified seasonal Insurance Unit (Gram Panchayat/Hobli level) notifications are strictly routed to Section B as `REQUIRES_VERIFICATION` with numerical scoring disabled.
7. **Provisional Schemes Quarantine:** Corporation schemes (`SCH008_KA_COOP`, `SCH010_VALMIKI`, `SCH010_KMDC`) are strictly quarantined in Section B without clinical scoring.
8. **Challenge 4: Three-Valued Logic & Unknown Title Handling (S056):** Missing land title cut-off date (`land_ownership_cutoff_pre_feb_2019 = None`) strictly returns `REQUIRES_VERIFICATION` in PM-KISAN (`PMKISAN_CUTOFF_DATE_UNKNOWN`) and routes title-dependent capital schemes (Krishi Bhagya, Valmiki Corporation) to Section B. Universal diagnostic access for Soil Health Card (`SCH009`) is preserved in Section A.
9. **Challenge 8 & Boundary Test: Large Holding PMKSY-PDMC Area Cap (S058):** The raw engine determination (`INELIGIBLE` under `PMKSY_LAND_ABOVE_5_HA`) is strictly preserved. In governance presentation, PMKSY-PDMC qualifies in Section A at the 5.00 ha statutory ceiling because the applicant requested exactly 5.00 ha, cleanly accommodated by the 12.5-acre qualifying parcel ($5.00 \le 12.5 \times 0.404686 = 5.059$ ha).
10. **Challenge 3: Regular Government Officer Exclusion (S055):** Regular government officer is strictly disqualified from PM-KISAN under `PMKISAN_REGULAR_OFFICER_EXCLUSION`, with no spillover to universal or non-statutorily excluded schemes.

## 2. Zone Z8 Scenario Input Overview (S053–S058)

| Scenario ID | District | Primary Crop | Holding (ac) | Land Type | Social Category | Farmer Class | Immediate Need | Operational Water Source | Benchmark Test Purpose |
|:---|:---|:---|:---:|:---|:---:|:---:|:---|:---|:---|
| **S053** | Dharwad | Soybean | 5.5 | Dryland (Rainfed) | Minority (Muslim) | Medium (5-10 acres) | `RAINWATER_HARVESTING` | Dug Well (Seasonal, dries Feb-May) | Krishi Bhagya farm pond for medium Minority dryland soybean;... |
| **S054** | Belagavi | Chilli | 1.5 | Wetland/valley | SC | Marginal (< 2.5 acres) | `PROTECTED_HORTICULTURE` | Borewell (Grid-connected) | MIDH shade-net for SC marginal chilli wetland; Krishi Bhagya... |
| **S055** | Haveri | Cotton | 3.0 | Dryland (Rainfed) | General (OC) | Small (2.5-5 acres) | `INCOME_SUPPORT` | Dug Well (Seasonal) | Challenge 3: regular government officer excluded from PM-KIS... |
| **S056** | Dharwad | Wheat | 4.0 | Dryland (Rainfed) | ST | Small (2.5-5 acres) | `SOIL_HEALTH_AND_FERTILIZER` | Farm Pond (Rainfed) | Challenge 4 three-valued logic: UNKNOWN land title; PM-KISAN... |
| **S057** | Belagavi | Sugarcane | 12.0 | Irrigated (Canal) | OBC | Large (> 10 acres) | `FARM_MECHANIZATION` | Canal Command & Sump | Challenge 8: SMAM for large OBC sugarcane canal; no blanket ... |
| **S058** | Haveri | Soybean | 12.5 | Irrigated (Borewell) | General (OC) | Large (> 10 acres) | `MICRO_IRRIGATION_SUPPORT` | Borewell (Grid-connected) | Challenge 8 and boundary test: PMKSY-PDMC 5.00 ha ceiling at... |

## 3. Governance Presentation Accounting & Reconciled Denominators

| Scenario | District | Primary Crop | Immediate Need | Section A (Confirmed) | Section B (Review / Unverified) | Disqualified Candidates | Total Actionable | Reconciled Formula |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **S053** | Dharwad | Soybean | `RAINWATER_HARVESTING` | **5** | **2** | **8** | **15** | 5 + 2 + 8 = 15 |
| **S054** | Belagavi | Chilli | `PROTECTED_HORTICULTURE` | **6** | **2** | **7** | **15** | 6 + 2 + 7 = 15 |
| **S055** | Haveri | Cotton | `INCOME_SUPPORT` | **4** | **2** | **9** | **15** | 4 + 2 + 9 = 15 |
| **S056** | Dharwad | Wheat | `SOIL_HEALTH_AND_FERTILIZER` | **3** | **5** | **6** | **14** | 3 + 5 + 6 = 14 |
| **S057** | Belagavi | Sugarcane | `FARM_MECHANIZATION` | **5** | **2** | **8** | **15** | 5 + 2 + 8 = 15 |
| **S058** | Haveri | Soybean | `MICRO_IRRIGATION_SUPPORT` | **5** | **2** | **8** | **15** | 5 + 2 + 8 = 15 |

### Denominator Reconciliations & Abstract Parent Suppression:
Every scenario evaluates exactly 16 raw scheme records. The number of displayed actionable schemes (14 in S056; 15 in S053, S054, S055, S057, and S058) is explicitly reconciled based on whether child records of abstract parents (`SCH008`, `SCH010`) are actionable:

- In **S053, S054, S055, S057, S058**: Parent `SCH008` is suppressed (children actionable). All four Ganga Kalyana children are disqualified (`INELIGIBLE`). Because zero children are actionable, abstract parent `SCH010` is retained in the table as an ineligible umbrella record $\implies$ **15 actionable schemes displayed**.
- In **S056**: Parent `SCH008` is suppressed (children actionable). Parent `SCH010` is suppressed (child `SCH010_VALMIKI` actionable in Section B) $\implies$ **14 actionable schemes displayed**.

## 4. Scenario-by-Scenario Detailed Governance Audits

### 4.3 Scenario S053: Dharwad — Soybean (5.5 ac, Minority (Muslim))

- **Context & Need:** Krishi Bhagya farm pond for medium Minority dryland soybean; KMDC individual route exceeds 5.0 ac ceiling; PMFBY routed to Section B.
- **Physical Area Consistency:** `PASS: 5.5 ac holding matches parcel`
- **Water Infrastructure:** Dug Well (Seasonal, dries Feb-May) (`NONE`)
- **Statutory Flags:** Tenure=`RTC registered pre-February 2019 in Navalgund taluk, Dharwad district`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned ELIGIBLE based on static crop whitelist, but commercial crop... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
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

### 4.4 Scenario S054: Belagavi — Chilli (1.5 ac, SC)

- **Context & Need:** MIDH shade-net for SC marginal chilli wetland; Krishi Bhagya dryland exclusion; Ganga Kalyana existing-borewell disqualification; PM-KUSUM B grid disqualification.
- **Physical Area Consistency:** `PASS: 1.5 ac holding matches parcel`
- **Water Infrastructure:** Borewell (Grid-connected) (`GRID_CONNECTED_IP_SET`)
- **Statutory Flags:** Tenure=`RTC registered pre-February 2019 in Athani taluk, Belagavi district`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned INELIGIBLE because Chilli is absent from the engine's static... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010` | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

### 4.5 Scenario S055: Haveri — Cotton (3.0 ac, General (OC))

- **Context & Need:** Challenge 3: regular government officer excluded from PM-KISAN; no spill-over to SMAM, SHC, Krishi Bhagya, PMKSY-PDMC.
- **Physical Area Consistency:** `PASS: 3.0 ac holding matches parcel`
- **Water Infrastructure:** Dug Well (Seasonal) (`NONE`)
- **Statutory Flags:** Tenure=`RTC registered pre-February 2019 in Hangal taluk, Haveri district`, Income Tax=`False`, Govt Employee=`OFFICER_REGULAR`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned ELIGIBLE based on static crop whitelist, but cotton insuranc... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
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

### 4.6 Scenario S056: Dharwad — Wheat (4.0 ac, ST)

- **Context & Need:** Challenge 4 three-valued logic: UNKNOWN land title; PM-KISAN REQUIRES_VERIFICATION in Section B; title-dependent capital schemes routed to Section B; Soil Health Card ELIGIBLE in Section A.
- **Physical Area Consistency:** `PASS: 4.0 ac holding matches parcel`
- **Water Infrastructure:** Farm Pond (Rainfed) (`NONE`)
- **Statutory Flags:** Tenure=`Ancestral land title partition deed pending mutation in Kalghatgi taluk; ownership record date unconfirmed (UNKNOWN)`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Unresolved Statutory Evidence / Land Title Required) | No | Raw engine returned REQUIRES_VERIFICATION due to explicit UNKNOWN tenure cut-off... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `INELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned ELIGIBLE based on static crop whitelist, but commercial food... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Field Evidence / Land Title Required) | No | Raw engine returned ELIGIBLE based on rainfed dryland and acreage in notified Dh... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Provisional Scheme / Land Title Required) | No | Raw engine returned ELIGIBLE based on ST social category, dryland acreage, and z... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

### 4.7 Scenario S057: Belagavi — Sugarcane (12.0 ac, OBC)

- **Context & Need:** Challenge 8: SMAM for large OBC sugarcane canal; no blanket large-farm exclusion; PMKSY-PDMC qualifies in Section A; Krishi Bhagya and Ganga Kalyana disqualified by canal command.
- **Physical Area Consistency:** `PASS: 12.0 ac holding matches parcel`
- **Water Infrastructure:** Canal Command & Sump (`NONE`)
- **Statutory Flags:** Tenure=`RTC registered pre-February 2019 in Gokak taluk, Belagavi district`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned ELIGIBLE based on static crop whitelist, but commercial suga... |
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

### 4.8 Scenario S058: Haveri — Soybean (12.5 ac, General (OC))

- **Context & Need:** Challenge 8 and boundary test: PMKSY-PDMC 5.00 ha ceiling at exactly 5.00 ha requested; 12.5 ac / 5.059 ha physical capacity PASS; PMKSY-PDMC qualifies in Section A; Ganga Kalyana and PM-KUSUM B disqualified by existing grid borewell.
- **Physical Area Consistency:** `PASS: requested 5.00 ha <= 12.5 ac (5.059 ha) qualifying parcel; satisfies PMKSY-PDMC 5.00 ha statutory ceiling`
- **Water Infrastructure:** Borewell (Grid-connected) (`GRID_CONNECTED_IP_SET`)
- **Statutory Flags:** Tenure=`RTC registered pre-February 2019 in Savanur taluk, Haveri district`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned ELIGIBLE based on static crop whitelist, but PMFBY claims ar... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Governance Area Capping Determination: Raw engine returned INELIGIBLE due to tot... |
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

The following verification dependencies remain active and are enforced across Zone Z8:

### S053 (Dharwad — Soybean)
- Verification of GoK Kharif 2026 PMFBY Insurance Unit notification for Soybean in Dharwad district
- KMDC administrative circular and community borewell operational guidelines verification
- Dharwad taluk Krishi Bhagya application portal status and current GO for FY 2026-27

### S054 (Belagavi — Chilli)
- Verification of GoK Kharif 2026 PMFBY Insurance Unit notification for Chilli in Athani taluk, Belagavi district
- Belagavi District Horticulture Department MIDH shade-net FY 2026-27 application window confirmation

### S055 (Haveri — Cotton)
- Verification of GoK Kharif 2026 PMFBY Insurance Unit notification for Cotton in Hangal taluk, Haveri district
- Haveri District Agriculture Joint Director SMAM FY 2026-27 target allocation circular

### S056 (Dharwad — Wheat)
- Revenue Department certification of land title record date (RTC mutation extract) for Kalghatgi taluk
- Verification of GoK Rabi 2026-27 PMFBY Insurance Unit notification for Wheat in Dharwad district
- Valmiki ST Development Corporation administrative circular and perennial water source adjacency verification
- Kalghatgi Taluk Agriculture Office Soil Health Card sample collection schedule

### S057 (Belagavi — Sugarcane)
- Verification of GoK Kharif 2026 PMFBY Insurance Unit notification for Sugarcane in Gokak taluk, Belagavi district
- Belagavi District Agriculture Joint Director SMAM FY 2026-27 specialized machinery quota circular

### S058 (Haveri — Soybean)
- Verification of GoK Kharif 2026 PMFBY Insurance Unit notification for Soybean in Savanur taluk, Haveri district
- Haveri District Agriculture office PMKSY-PDMC FY 2026-27 drip/sprinkler target allocation and empanelled vendor confirmation

## 6. Frozen Invariants Check

| Invariant Component | Status | Verification Summary |
|:---|:---:|:---|
| `src/eligibility/engine.py` | **PRESERVED** | Untouched; raw evaluations deterministic |
| `scheme_database/processed/scheme_master.json` | **PRESERVED** | Untouched; 16 scheme records intact |
| Pilot Scenarios `S001`–`S010` | **PRESERVED** | Untouched; baseline calibration valid |
| Annotation Protocol `v1.1` | **PRESERVED** | Untouched; governance presentation standards maintained |
| Benchmark Design `v1.0.4` | **COMPLIANT** | All Z8 quotas, area caps, and tenure rules strictly satisfied |

