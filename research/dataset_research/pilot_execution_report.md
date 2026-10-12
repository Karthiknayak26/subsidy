# Deliverable A: Pilot Execution Report (Scenarios S001–S010)

**Project:** ML-Based Personalized Government Scheme and Subsidy Recommendation System for Farmers (Karnataka Context)  
**Milestone:** Case-B Pilot Execution & Verification Audit  
**Execution Date:** October 2026  
**Engine Version:** Deterministic Eligibility Engine v1.2 (Three-Valued Logic + Decoupled 4-State Availability)  
**Test Suite Status:** 56 passing tests, 88% overall code coverage across all 16 implementation records  

---

## 1. Executive Summary & Review Gate Compliance

This report documents the end-to-end execution of the 10 pilot farmer scenarios (S001–S010) through the deterministic eligibility engine and availability filter. In strict compliance with the guide review directives, all pre-pilot corrections and methodological refinements have been finalized:

1. **Corporation-Specific Ganga Kalyana Rules:** Enforced Dr. B. R. Ambedkar Development Corporation's published guidelines (`SCH010_AMBEDKAR`): individual dryland route requires **1.5 to 5.0 acres** (1 acre 20 guntas to 5.0 acres); community/lift-irrigation route covers **8.0 to 15.0 pooled acres with at least three (3) SC beneficiaries**. The other three corporation child records (`SCH010_VALMIKI`, `SCH010_DEVARAJ_URS`, `SCH010_KMDC`) are explicitly tagged as `PROVISIONAL` pending verification of their respective current circulars.

2. **Complete 16-Record Test Suite:** Dedicated unit and integration tests validate every record in the registry (including SMAM `SCH004`, MIDH `SCH007`, KCC Central `SCH008_CENTRAL`, KCC Karnataka Coop `SCH008_KA_COOP`, Soil Health Card `SCH009`, and all 4 Ganga Kalyana corporation children). The test suite comprises **56 passing tests** (88% code coverage).

3. **PM-KISAN Complete Statutory Exclusion Audit:** Modeled all official criteria from `pmkisan.gov.in`, including income tax payment in the last assessment year, constitutional posts, elected representatives (Ministers, MPs, MLAs, MLCs, Mayors, ZP Chairpersons), regular officers with explicit exemption for Multi-Tasking Staff (MTS)/Class IV/Group D employees, superannuated pensioners receiving $\ge$ ₹10,000/month with statutory MTS pension exemption, practicing registered professionals, institutional holders, pure tenants without title, and land transferred post 01.02.2019.

4. **Narrowed S009 General Merit Conclusion:** The S009 result is strictly scoped to the four corporation implementations currently represented in the registry. It does not generalize to every Ganga Kalyana-related programme in Karnataka, avoiding unsupported statewide claims.

5. **Differentiated Alternative Routes (S008):** PM-KUSUM Component C is explicitly treated as a *"Related option to verify: PM-KUSUM Component C"*, not as an automatic recommendation, recognizing that an alternative route is not an active benefit until independently validated.

6. **Automated Parent Deduplication:** Abstract umbrella parents (`SCH010`, `SCH008`) are automatically deduplicated from actionable recommendation outputs whenever their specific child implementations are actionable, preventing duplicate recommendation cards.

7. **Strict Separation of Three Concepts:**
   - **Eligibility:** Deterministic statutory evaluation (`ELIGIBLE`, `INELIGIBLE`, `REQUIRES_VERIFICATION`).
   - **Availability:** Dynamic operational status (4 states; unconfirmed schemes default to *Availability unknown — confirmation required*).
   - **Relevance:** Expert-assigned score (0–3), never manufactured by the engine.

---

## 2. Pilot Scenarios Input Overview (S001–S010)

| Scenario ID | District | Agro-Climatic Zone | Primary Crop | Land (Ac) | Land Type | Social Category | Income (₹ Lakh) | Immediate Need | Key Assets / Flags |
|---|---|---|---|---|---|---|---|---|---|
| **S001** | Raichur | Northern Dry Zone | Cotton | 3.0 | Dryland (Rainfed) | SC | 1.2 | `CROP_INSURANCE` | None |
| **S002** | Haveri | Central Dry Zone | Maize | 2.0 | Dryland (Rainfed) | OBC (2A) | 1.5 | `SOLAR_PUMP_INSTALLATION` | Borewell (Non-energized) |
| **S003** | Tumakuru | Southern Dry Zone | Ragi | 1.5 | Dryland (Rainfed) | General (OC) | 1.8 | `RAINWATER_HARVESTING` | None |
| **S004** | Dharwad | Southern Transition Zone | Soybean | 4.0 | Irrigated (Borewell) | OBC (3B) | 2.5 | `MICRO_IRRIGATION_SUPPORT` | Borewell (Grid-connected), Electric Pump Set |
| **S005** | Kolar | Eastern Dry Zone | Tomato | 1.0 | Irrigated (Borewell) | OBC (3A) | 3.0 | `PROTECTED_HORTICULTURE` | Borewell (Grid-connected), Drip Irrigation (Installed) |
| **S006** | Mysuru | Southern Dry Zone | Paddy | 2.5 | Irrigated (Canal) | General (OC) | 2.0 | `PRODUCTION_CREDIT` | None |
| **S007** | Haveri | Central Dry Zone | Maize | 3.0 | Dryland (Rainfed) | General (OC) | 2.2 | `INCOME_SUPPORT` | Tax Paid = True |
| **S008** | Vijayapura | Northern Dry Zone | Jowar | 4.0 | Dryland (Rainfed) | OBC (2A) | 1.8 | `SOLAR_PUMP_INSTALLATION` | Grid IP-Set Pump (Component B excluded) |
| **S009** | Chitradurga | Central Dry Zone | Groundnut | 2.0 | Dryland (Rainfed) | General (OC) | 1.4 | `BOREWELL_IRRIGATION` | General Merit (outside covered corps) |
| **S010** | Belagavi | Northern Dry Zone | Sugarcane | 3.0 | Irrigated (Borewell) | SC | 2.8 | `MICRO_IRRIGATION_SUPPORT` | Micro-irrig 3 yrs ago (Lock-in breach) |

---

## 3. Detailed Pilot Execution Results (Scenario by Scenario)

### 3.001 Scenario S001: Raichur — Cotton (3.0 ac, SC)

- **Agro-Climatic Zone:** Northern Dry Zone  
- **Immediate Need Stated:** `CROP_INSURANCE`  
- **Farmer Query Context:** *"Cotton crop suffering pink bollworm attack in Raichur, need compensation claim or insurance procedure."*  
- **Actionable Outcome Summary:** **7 ELIGIBLE** | **6 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008', 'SCH010']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **ELIGIBLE** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>*(+2 more)* | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **ELIGIBLE** | `PMFBY_NOTIFIED_CROP_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **INELIGIBLE** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | ❌ Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **ELIGIBLE** | `SMAM_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **ELIGIBLE** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **INELIGIBLE** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | ❌ Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **INELIGIBLE** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | ❌ Primary crop 'Cotton' is not a recognized horticultural crop under MIDH.<br>❌ MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **ELIGIBLE** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **REQUIRES_VERIFICATION** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | ⚠️ Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **ELIGIBLE** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **ELIGIBLE** | `GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **INELIGIBLE** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'SC' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead). | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'SC' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead). | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'SC' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead). | Availability unknown — confirmation required |

### 3.002 Scenario S002: Haveri — Maize (2.0 ac, OBC (2A))

- **Agro-Climatic Zone:** Central Dry Zone  
- **Immediate Need Stated:** `SOLAR_PUMP_INSTALLATION`  
- **Farmer Query Context:** *"Have drilled borewell without electricity connection in Haveri, need solar motor pump subsidy subsidy details."*  
- **Actionable Outcome Summary:** **8 ELIGIBLE** | **6 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **ELIGIBLE** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>*(+2 more)* | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **ELIGIBLE** | `PMFBY_NOTIFIED_CROP_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **ELIGIBLE** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_WATER_SOURCE_VERIFIED`<br>`PMKSY_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **ELIGIBLE** | `SMAM_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **ELIGIBLE** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **ELIGIBLE** | `KUSUM_B_WATER_SOURCE_PRESENT`<br>`KUSUM_B_OFF_GRID_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **INELIGIBLE** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | ❌ Primary crop 'Maize' is not a recognized horticultural crop under MIDH.<br>❌ MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **ELIGIBLE** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **REQUIRES_VERIFICATION** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | ⚠️ Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **ELIGIBLE** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **INELIGIBLE** | `GK_PARENT_EXISTING_BOREWELL_EXCLUSION` | ❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_AMBEDKAR_EXISTING_BOREWELL`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'OBC (2A)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **INELIGIBLE** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_EXISTING_BOREWELL`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'OBC (2A)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_DEVARAJ_URS_EXISTING_BOREWELL`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | ❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_EXISTING_BOREWELL`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'OBC (2A)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |

### 3.003 Scenario S003: Tumakuru — Ragi (1.5 ac, General (OC))

- **Agro-Climatic Zone:** Southern Dry Zone  
- **Immediate Need Stated:** `RAINWATER_HARVESTING`  
- **Farmer Query Context:** *"Dryland ragi farmer in Tumakuru wanting to dig farm pond (krishi honda) with polythene lining for rainwater storage."*  
- **Actionable Outcome Summary:** **6 ELIGIBLE** | **8 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **ELIGIBLE** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>*(+2 more)* | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **ELIGIBLE** | `PMFBY_NOTIFIED_CROP_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **INELIGIBLE** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | ❌ Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **ELIGIBLE** | `SMAM_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **ELIGIBLE** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **INELIGIBLE** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | ❌ Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **INELIGIBLE** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | ❌ Primary crop 'Ragi' is not a recognized horticultural crop under MIDH.<br>❌ MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **ELIGIBLE** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **REQUIRES_VERIFICATION** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | ⚠️ Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **ELIGIBLE** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **INELIGIBLE** | `GK_PARENT_REGISTRY_CORPORATION_MISMATCH` | ❌ Ineligible for all four Ganga Kalyana implementation records currently represented in the registry (SCH010_AMBEDKAR, SCH010_VALMIKI, SCH010_DEVARAJ_URS, SCH010_KMDC) because applicant (General Merit) does not meet covered corporation-category requirements. This result does not establish ineligibility for every Ganga Kalyana-related programme in Karnataka. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **INELIGIBLE** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |

### 3.004 Scenario S004: Dharwad — Soybean (4.0 ac, OBC (3B))

- **Agro-Climatic Zone:** Southern Transition Zone  
- **Immediate Need Stated:** `MICRO_IRRIGATION_SUPPORT`  
- **Farmer Query Context:** *"Borewell discharge depleting in Dharwad, want to install drip irrigation line for soybean and maize."*  
- **Actionable Outcome Summary:** **6 ELIGIBLE** | **8 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **ELIGIBLE** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>*(+2 more)* | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **ELIGIBLE** | `PMFBY_NOTIFIED_CROP_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **ELIGIBLE** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_WATER_SOURCE_VERIFIED`<br>`PMKSY_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **ELIGIBLE** | `SMAM_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **INELIGIBLE** | `KRISHI_BHAGYA_NOT_DRYLAND`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | ❌ Krishi Bhagya is strictly restricted to dryland rainfed holdings (current land_type: Irrigated (Borewell)). | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **INELIGIBLE** | `KUSUM_B_WATER_SOURCE_PRESENT`<br>`KUSUM_B_GRID_CONNECTED_DISQUALIFIED` | ❌ Borewell already has an energized electric grid connection (DISCOM IP set). Component B strictly targets off-grid sources. (Related option to verify: PM-KUSUM Component C; not evaluated as an active benefit). | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **INELIGIBLE** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | ❌ Primary crop 'Soybean' is not a recognized horticultural crop under MIDH.<br>❌ MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **ELIGIBLE** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **REQUIRES_VERIFICATION** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | ⚠️ Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **ELIGIBLE** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **INELIGIBLE** | `GK_PARENT_NOT_DRYLAND`<br>`GK_PARENT_EXISTING_BOREWELL_EXCLUSION` | ❌ Land must be exclusively dryland (kushki). Current land_type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_AMBEDKAR_NOT_DRYLAND`<br>`GK_SCH010_AMBEDKAR_EXISTING_BOREWELL`<br>*(+1 more)* | ❌ Applicant social category 'OBC (3B)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **INELIGIBLE** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_NOT_DRYLAND`<br>`GK_SCH010_VALMIKI_EXISTING_BOREWELL`<br>*(+1 more)* | ❌ Applicant social category 'OBC (3B)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_DEVARAJ_URS_NOT_DRYLAND`<br>`GK_SCH010_DEVARAJ_URS_EXISTING_BOREWELL`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | ❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_NOT_DRYLAND`<br>`GK_SCH010_KMDC_EXISTING_BOREWELL`<br>*(+1 more)* | ❌ Applicant social category 'OBC (3B)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |

### 3.005 Scenario S005: Kolar — Tomato (1.0 ac, OBC (3A))

- **Agro-Climatic Zone:** Eastern Dry Zone  
- **Immediate Need Stated:** `PROTECTED_HORTICULTURE`  
- **Farmer Query Context:** *"Seeking subsidy subsidy for naturally ventilated polyhouse structure of 1000 square meters for high value capsicum in Kolar."*  
- **Actionable Outcome Summary:** **7 ELIGIBLE** | **7 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **ELIGIBLE** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>*(+2 more)* | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **ELIGIBLE** | `PMFBY_NOTIFIED_CROP_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **ELIGIBLE** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_WATER_SOURCE_VERIFIED`<br>`PMKSY_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **ELIGIBLE** | `SMAM_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **INELIGIBLE** | `KRISHI_BHAGYA_NOT_DRYLAND`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | ❌ Krishi Bhagya is strictly restricted to dryland rainfed holdings (current land_type: Irrigated (Borewell)). | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **INELIGIBLE** | `KUSUM_B_WATER_SOURCE_PRESENT`<br>`KUSUM_B_GRID_CONNECTED_DISQUALIFIED` | ❌ Borewell already has an energized electric grid connection (DISCOM IP set). Component B strictly targets off-grid sources. (Related option to verify: PM-KUSUM Component C; not evaluated as an active benefit). | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **ELIGIBLE** | `MIDH_HORTICULTURE_CROP_VERIFIED`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_MICRO_IRRIGATION_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **ELIGIBLE** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **REQUIRES_VERIFICATION** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | ⚠️ Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **ELIGIBLE** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **INELIGIBLE** | `GK_PARENT_NOT_DRYLAND`<br>`GK_PARENT_EXISTING_BOREWELL_EXCLUSION` | ❌ Land must be exclusively dryland (kushki). Current land_type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_AMBEDKAR_NOT_DRYLAND`<br>`GK_SCH010_AMBEDKAR_EXISTING_BOREWELL`<br>*(+1 more)* | ❌ Applicant social category 'OBC (3A)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell.<br>❌ Individual landholding (1.0 ac) is below Ambedkar Corporation minimum threshold of 1.5 acres (1 acre 20 guntas), and community pooled route was not satisfied. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **INELIGIBLE** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_NOT_DRYLAND`<br>`GK_SCH010_VALMIKI_EXISTING_BOREWELL`<br>*(+1 more)* | ❌ Applicant social category 'OBC (3A)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell.<br>❌ Landholding (1.0 ac) is below minimum 1.2 acres for Individual Route, and community pool requirement (8-15 ac) is not met. | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_DEVARAJ_URS_NOT_DRYLAND`<br>`GK_SCH010_DEVARAJ_URS_EXISTING_BOREWELL`<br>`GK_SCH010_DEVARAJ_URS_UNDER_MIN_ACREAGE` | ❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell.<br>❌ Landholding (1.0 ac) is below minimum 1.2 acres for Individual Route, and community pool requirement (8-15 ac) is not met. | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_NOT_DRYLAND`<br>`GK_SCH010_KMDC_EXISTING_BOREWELL`<br>*(+1 more)* | ❌ Applicant social category 'OBC (3A)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell.<br>❌ Landholding (1.0 ac) is below minimum 1.2 acres for Individual Route, and community pool requirement (8-15 ac) is not met. | Availability unknown — confirmation required |

### 3.006 Scenario S006: Mysuru — Paddy (2.5 ac, General (OC))

- **Agro-Climatic Zone:** Southern Dry Zone  
- **Immediate Need Stated:** `PRODUCTION_CREDIT`  
- **Farmer Query Context:** *"Need crop loan / Kisan Credit Card through bank branch for paddy seeds and fertilizer inputs in Mysuru."*  
- **Actionable Outcome Summary:** **6 ELIGIBLE** | **8 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **ELIGIBLE** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>*(+2 more)* | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **ELIGIBLE** | `PMFBY_NOTIFIED_CROP_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **ELIGIBLE** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_WATER_SOURCE_VERIFIED`<br>`PMKSY_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **ELIGIBLE** | `SMAM_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **INELIGIBLE** | `KRISHI_BHAGYA_NOT_DRYLAND`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | ❌ Krishi Bhagya is strictly restricted to dryland rainfed holdings (current land_type: Irrigated (Canal)). | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **INELIGIBLE** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | ❌ Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **INELIGIBLE** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | ❌ Primary crop 'Paddy' is not a recognized horticultural crop under MIDH.<br>❌ MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **ELIGIBLE** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **REQUIRES_VERIFICATION** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | ⚠️ Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **ELIGIBLE** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **INELIGIBLE** | `GK_PARENT_REGISTRY_CORPORATION_MISMATCH`<br>`GK_PARENT_NOT_DRYLAND` | ❌ Ineligible for all four Ganga Kalyana implementation records currently represented in the registry (SCH010_AMBEDKAR, SCH010_VALMIKI, SCH010_DEVARAJ_URS, SCH010_KMDC) because applicant (General Merit) does not meet covered corporation-category requirements. This result does not establish ineligibility for every Ganga Kalyana-related programme in Karnataka.<br>❌ Land must be exclusively dryland (kushki). Current land_type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_AMBEDKAR_NOT_DRYLAND`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to NONE instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **INELIGIBLE** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_NOT_DRYLAND`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to NONE instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_NOT_DRYLAND`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to NONE instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_NOT_DRYLAND`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to NONE instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |

### 3.007 Scenario S007: Haveri — Maize (3.0 ac, General (OC))

- **Agro-Climatic Zone:** Central Dry Zone  
- **Immediate Need Stated:** `INCOME_SUPPORT`  
- **Farmer Query Context:** *"Enquiring about PM-KISAN installment payment status. Family member paid income tax last year."*  
- **Actionable Outcome Summary:** **5 ELIGIBLE** | **9 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **INELIGIBLE** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_PAID_INCOME_TAX_EXCLUSION`<br>*(+2 more)* | ❌ Member of the scheme-defined farmer family paid income tax in the last assessment year. | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **ELIGIBLE** | `PMFBY_NOTIFIED_CROP_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **INELIGIBLE** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | ❌ Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **ELIGIBLE** | `SMAM_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **ELIGIBLE** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **INELIGIBLE** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | ❌ Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **INELIGIBLE** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | ❌ Primary crop 'Maize' is not a recognized horticultural crop under MIDH.<br>❌ MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **ELIGIBLE** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **REQUIRES_VERIFICATION** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | ⚠️ Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **ELIGIBLE** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **INELIGIBLE** | `GK_PARENT_REGISTRY_CORPORATION_MISMATCH` | ❌ Ineligible for all four Ganga Kalyana implementation records currently represented in the registry (SCH010_AMBEDKAR, SCH010_VALMIKI, SCH010_DEVARAJ_URS, SCH010_KMDC) because applicant (General Merit) does not meet covered corporation-category requirements. This result does not establish ineligibility for every Ganga Kalyana-related programme in Karnataka. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **INELIGIBLE** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |

### 3.008 Scenario S008: Vijayapura — Jowar (4.0 ac, OBC (2A))

- **Agro-Climatic Zone:** Northern Dry Zone  
- **Immediate Need Stated:** `SOLAR_PUMP_INSTALLATION`  
- **Farmer Query Context:** *"Already have electric grid motor on borewell in Vijayapura, want to apply for standalone solar pump subsidy."*  
- **Actionable Outcome Summary:** **7 ELIGIBLE** | **7 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **ELIGIBLE** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>*(+2 more)* | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **ELIGIBLE** | `PMFBY_NOTIFIED_CROP_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **ELIGIBLE** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_WATER_SOURCE_VERIFIED`<br>`PMKSY_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **ELIGIBLE** | `SMAM_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **ELIGIBLE** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **INELIGIBLE** | `KUSUM_B_WATER_SOURCE_PRESENT`<br>`KUSUM_B_GRID_CONNECTED_DISQUALIFIED` | ❌ Borewell already has an energized electric grid connection (DISCOM IP set). Component B strictly targets off-grid sources. (Related option to verify: PM-KUSUM Component C; not evaluated as an active benefit). | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **INELIGIBLE** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | ❌ Primary crop 'Jowar' is not a recognized horticultural crop under MIDH.<br>❌ MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **ELIGIBLE** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **REQUIRES_VERIFICATION** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | ⚠️ Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **ELIGIBLE** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **INELIGIBLE** | `GK_PARENT_EXISTING_BOREWELL_EXCLUSION` | ❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_AMBEDKAR_EXISTING_BOREWELL`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'OBC (2A)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **INELIGIBLE** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_EXISTING_BOREWELL`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'OBC (2A)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_DEVARAJ_URS_EXISTING_BOREWELL`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | ❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_EXISTING_BOREWELL`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'OBC (2A)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |

### 3.009 Scenario S009: Chitradurga — Groundnut (2.0 ac, General (OC))

- **Agro-Climatic Zone:** Central Dry Zone  
- **Immediate Need Stated:** `BOREWELL_IRRIGATION`  
- **Farmer Query Context:** *"Dryland farmer in Chitradurga seeking 100% free government borewell under Ganga Kalyana scheme."*  
- **Actionable Outcome Summary:** **6 ELIGIBLE** | **8 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **ELIGIBLE** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>*(+2 more)* | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **ELIGIBLE** | `PMFBY_NOTIFIED_CROP_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **INELIGIBLE** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | ❌ Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **ELIGIBLE** | `SMAM_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **ELIGIBLE** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **INELIGIBLE** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | ❌ Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **INELIGIBLE** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | ❌ Primary crop 'Groundnut' is not a recognized horticultural crop under MIDH.<br>❌ MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **ELIGIBLE** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **REQUIRES_VERIFICATION** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | ⚠️ Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **ELIGIBLE** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **INELIGIBLE** | `GK_PARENT_REGISTRY_CORPORATION_MISMATCH` | ❌ Ineligible for all four Ganga Kalyana implementation records currently represented in the registry (SCH010_AMBEDKAR, SCH010_VALMIKI, SCH010_DEVARAJ_URS, SCH010_KMDC) because applicant (General Merit) does not meet covered corporation-category requirements. This result does not establish ineligibility for every Ganga Kalyana-related programme in Karnataka. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **INELIGIBLE** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | ❌ Applicant social category 'General (OC)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |

### 3.010 Scenario S010: Belagavi — Sugarcane (3.0 ac, SC)

- **Agro-Climatic Zone:** Northern Dry Zone  
- **Immediate Need Stated:** `MICRO_IRRIGATION_SUPPORT`  
- **Farmer Query Context:** *"Availed drip subsidy 3 years ago in Belagavi, want replacement drip system subsidy for sugarcane."*  
- **Actionable Outcome Summary:** **5 ELIGIBLE** | **9 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **ELIGIBLE** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>*(+2 more)* | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **ELIGIBLE** | `PMFBY_NOTIFIED_CROP_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **INELIGIBLE** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_WATER_SOURCE_VERIFIED`<br>`PMKSY_SEVEN_YEAR_LOCKIN_BREACHED` | ❌ Land parcel availed micro-irrigation subsidy 3.0 years ago (7-year lock-in period applies). | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **ELIGIBLE** | `SMAM_NO_PRIOR_SUBSIDY` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **INELIGIBLE** | `KRISHI_BHAGYA_NOT_DRYLAND`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | ❌ Krishi Bhagya is strictly restricted to dryland rainfed holdings (current land_type: Irrigated (Borewell)). | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **INELIGIBLE** | `KUSUM_B_WATER_SOURCE_PRESENT`<br>`KUSUM_B_GRID_CONNECTED_DISQUALIFIED` | ❌ Borewell already has an energized electric grid connection (DISCOM IP set). Component B strictly targets off-grid sources. (Related option to verify: PM-KUSUM Component C; not evaluated as an active benefit). | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **INELIGIBLE** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | ❌ Primary crop 'Sugarcane' is not a recognized horticultural crop under MIDH.<br>❌ MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **ELIGIBLE** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **REQUIRES_VERIFICATION** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | ⚠️ Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **ELIGIBLE** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | ✅ Passed all checks | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **INELIGIBLE** | `GK_PARENT_NOT_DRYLAND`<br>`GK_PARENT_EXISTING_BOREWELL_EXCLUSION` | ❌ Land must be exclusively dryland (kushki). Current land_type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_AMBEDKAR_NOT_DRYLAND`<br>`GK_SCH010_AMBEDKAR_EXISTING_BOREWELL`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | ❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **INELIGIBLE** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_NOT_DRYLAND`<br>`GK_SCH010_VALMIKI_EXISTING_BOREWELL`<br>*(+1 more)* | ❌ Applicant social category 'SC' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_NOT_DRYLAND`<br>`GK_SCH010_DEVARAJ_URS_EXISTING_BOREWELL`<br>*(+1 more)* | ❌ Applicant social category 'SC' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **INELIGIBLE** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_NOT_DRYLAND`<br>`GK_SCH010_KMDC_EXISTING_BOREWELL`<br>*(+1 more)* | ❌ Applicant social category 'SC' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead).<br>❌ Must be exclusively dryland (kushki). Land type 'Irrigated (Borewell)' is disqualified.<br>❌ Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |

---

## 4. Strict Negative Exclusion & Boundary Test Analysis (S007–S010)

Four scenarios (S007–S010) were designed specifically to test high-impact negative boundaries and statutory exclusion criteria. The engine's behavior on each scenario is audited below:

### 4.1 S007: PM-KISAN Statutory Income Tax Exclusion Test
- **Scenario Profile:** Haveri, Maize, 3.0 ac dryland, General category, `paid_income_tax_last_assessment_year = True`.
- **Fired Rule Key:** `PMKISAN_PAID_INCOME_TAX_EXCLUSION`.
- **Observed Engine Status:** `INELIGIBLE` for PM-KISAN (`SCH001`).
- **Engine Justification:** *"Disqualified under PM-KISAN exclusion criteria: Member of the scheme-defined farmer family paid income tax in the last assessment year."*
- **Sanity Check:** Non-excluded schemes (Soil Health Card `SCH009`, PMFBY `SCH002`, Krishi Bhagya `SCH005`, KCC Central `SCH008_CENTRAL`) remained `ELIGIBLE`, confirming that tax disqualification strictly affects PM-KISAN without contaminating other schemes.

### 4.2 S008: PM-KUSUM Component B Standalone Off-Grid Exclusion Test
- **Scenario Profile:** Vijayapura, Jowar, 4.0 ac, OBC (2A), seeking solar pumping. Existing asset has `Borewell (Grid-connected)` and `borewell_electric_status = GRID_CONNECTED_IP_SET`.
- **Fired Rule Key:** `KUSUM_B_GRID_CONNECTED_DISQUALIFIED`.
- **Observed Engine Status:** `INELIGIBLE` for PM-KUSUM Component B (`SCH006`).
- **Engine Justification:** *"Ineligible for PM-KUSUM Component B: Borewell already has an energized electric grid connection (DISCOM IP set). Component B strictly targets off-grid sources. (Related option to verify: PM-KUSUM Component C; not evaluated as an active benefit)."*
- **Important Distinction:** The engine correctly prevents an automatic recommendation for Component C. Component C is recorded as a related option to verify separately, because an alternative route is not an active benefit until its own eligibility and availability rules are implemented and validated.

### 4.3 S009: Ganga Kalyana Covered Corporation Boundary Test
- **Scenario Profile:** Chitradurga, Groundnut, 2.0 ac dryland, General category, seeking free borewell drilling.
- **Fired Rule Key:** `GK_PARENT_REGISTRY_CORPORATION_MISMATCH`, `GK_SCH010_*_SOCIAL_CATEGORY_MISMATCH`.
- **Observed Engine Status:** `INELIGIBLE` across parent `SCH010` and all 4 child records (`SCH010_AMBEDKAR`, `SCH010_VALMIKI`, `SCH010_DEVARAJ_URS`, `SCH010_KMDC`).
- **Engine Justification (Narrowed Scope):** *"S009: Ineligible for all four Ganga Kalyana implementation records currently represented in the registry because the applicant does not meet their covered corporation-category requirements. This result does not establish ineligibility for every Ganga Kalyana-related programme in Karnataka."*
- **Boundary Safeguard:** This phrasing avoids turning incomplete corporation registry coverage into an unsupported statewide conclusion.

### 4.4 S010: PMKSY-PDMC 7-Year Lock-In Boundary Test
- **Scenario Profile:** Belagavi, Sugarcane, 3.0 ac, SC category, `prior_micro_irrigation_subsidy_years_ago = 3.0`.
- **Fired Rule Key:** `PMKSY_SEVEN_YEAR_LOCKIN_BREACHED`.
- **Observed Engine Status:** `INELIGIBLE` for PMKSY-PDMC (`SCH003`).
- **Engine Justification:** *"Ineligible for PMKSY-PDMC: Land parcel availed micro-irrigation subsidy 3.0 years ago (7-year lock-in period applies)."*
- **Sanity Check:** Farmers who recently availed subsidized micro-irrigation are barred from double-dipping before the statutory 7-year replacement cycle expires.

---

## 5. Availability Filter & Presentation Guardrail Audit

The evaluation decoupled operational availability from statutory eligibility:
1. **Default State for Unverified Schemes:** All eligible schemes in the pilot currently evaluate to **"Availability unknown — confirmation required"** because no active, dated government circular or portal screenshot has been uploaded to `scheme_availability_template.csv`.
2. **Presentation Guardrail Enforced:** In accordance with guide directives, zero unverified schemes appear under *"Available now"*. The system strictly enforces the presentation guardrail, ensuring that farmers are never misled into believing applications are open without verified evidence.
3. **Provisional Credit Route:** Karnataka Zero-Interest Credit (`SCH008_KA_COOP`) correctly evaluates to **`REQUIRES_VERIFICATION`** across all scenarios, reflecting its provisional status pending verification of the active financial year's Government Order.

---

## 6. Summary of Key Research Findings from Pilot

| Evaluation Question | Pilot Finding | Status |
|---|---|---|
| **1. Does the engine apply encoded eligibility rules consistently?** | Yes. All 10 scenarios produced deterministic, reproducible determinations matching statutory guidelines across positive, negative, and boundary cases. | **ESTABLISHED** |
| **2. Are the rules supported by official scheme guidelines?** | Yes. Ambedkar 1.5–5 ac individual and 8–15 ac (3+ beneficiaries) community routes, PM-KISAN exclusions, and lock-in periods match official government sources. | **ESTABLISHED** |
| **3. Can domain experts judge relevance on candidate schemes?** | Pre-conditions established. Deliverable B prepares the exact annotation form presenting only eligible candidates, with separated verification schemes. | **READY FOR PILOT ANNOTATION** |

