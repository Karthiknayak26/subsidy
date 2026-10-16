# Deliverable: Zone Z2 Execution Report (Scenarios S017–S022)

**Project:** ML-Based Personalized Government Scheme and Subsidy Recommendation System for Farmers (Karnataka Context)  
**Milestone:** Benchmark v1.0.3 — Zone Z2 Scenario Generation & Rule-Validation Audit  
**Zone:** Zone Z2 — North Eastern Dry Zone (Kalaburagi, Yadgir, Raichur)  
**Execution Date:** October 2026  
**Engine Version:** Deterministic Eligibility Engine v1.2 (Frozen Commit `7724fa7`)  
**Availability Filter:** 4-State Decoupled Availability Pipeline (Snapshot `2026-10-15`)  
**Audit Scope:** Exactly six detailed scenarios (`S017`–`S022`) evaluated across all 16 scheme records (6 parent/standalone + 10 child/standalone).  

---

## 1. Executive Summary & Verification Audit

This report documents the rigorous rule-validation of the second batch of six benchmark scenarios (S017–S022) representing the **North Eastern Dry Zone (Zone Z2)**. In strict adherence to the project invariants:

1. **Zero Modifications to Frozen Engine:** The eligibility engine (`src/eligibility/engine.py`) and scheme master (`scheme_database/processed/scheme_master.json`) were executed byte-for-byte without altering any rule to force passing.
2. **Zero Synthetic Annotations:** No machine learning models were trained, no synthetic ratings were fabricated, and no expert scores were predicted. These scenarios are validated deterministically before independent expert annotation.
3. **100% Assignment Table Fidelity:** Every scenario preserves its assigned district, crop, land size, land type, social category, tenure status, and primary policy challenge from `benchmark-design-v1.0.3`.
4. **Exact Statutory Boundary Testing (Challenge 3):** Scenario `S018` rigorously tests the PM-KISAN pensioner exclusion threshold at exactly ₹10,000/month. The frozen engine fires `PMKISAN_PENSION_OVER_10K_EXCLUSION`, returning `INELIGIBLE` for a non-MTS pensioner despite 2.0 acres of registered landholding.
5. **Three-Valued Logic & Explicit UNKNOWN Attributes (Challenge 4):** Scenario `S020` models unconfirmed borewell grid electricity (`borewell_electric_status = UNKNOWN`) and unknown family tax assessment (`paid_income_tax_last_assessment_year = None`). The frozen engine strictly returns `REQUIRES_VERIFICATION` for both PM-KUSUM Component B (`KUSUM_B_GRID_STATUS_UNKNOWN`) and PM-KISAN (`PMKISAN_INCOME_TAX_UNKNOWN`) without silent default imputation.
6. **Parent Deduplication Enforced:** Abstract parent records (`SCH008`, `SCH010`) are automatically suppressed from actionable recommendations when their concrete child implementations are actionable.
7. **Explicit Separation of Eligibility vs Availability:** Statutory qualifications are evaluated via Three-Valued Logic (`ELIGIBLE`, `INELIGIBLE`, `REQUIRES_VERIFICATION`), while operational availability is maintained in four separate states.

---

## 2. Zone Z2 Scenario Input Overview (S017–S022)

| Scenario ID | District | Primary Crop | Land (Ac) | Land Type | Social Cat. | Farmer Class | Immediate Need | Operational Water Source | Key Statutory Test |
|---|---|---|---|---|---|---|---|---|---|
| **S017** | Yadgir | Cotton | 6.0 | Dryland (Rainfed) | ST | Medium (5-10 acres) | `CROP_INSURANCE` | Rainfed (None) | Evaluate cotton crop-insurance relevance and confirmation re... |
| **S018** | Raichur | Sunflower | 2.0 | Dryland (Rainfed) | General (OC) | Marginal (< 2.5 acres) | `INCOME_SUPPORT` | Rainfed (None) | Evaluate PM-KISAN pension exclusion boundary at exactly ₹10,... |
| **S019** | Kalaburagi | Bajra | 1.2 | Dryland (Rainfed) | OBC (2A) | Marginal (< 2.5 acres) | `RAINWATER_HARVESTING` | Rainfed Catchment (No borewell or pond) | Evaluate Krishi Bhagya integrated farm-pond package eligibil... |
| **S020** | Yadgir | Redgram | 6.5 | Dryland (Rainfed) | SC | Medium (5-10 acres) | `SOLAR_PUMP_INSTALLATION` | Borewell (Unconfirmed) | Evaluate Three-Valued Logic handling under explicit UNKNOWN ... |
| **S021** | Raichur | Cotton | 4.0 | Irrigated (Canal) | Minority (Muslim) | Small (2.5-5 acres) | `FARM_MECHANIZATION` | Canal Distributary (Tungabhadra Left Bank Canal) | Evaluate SMAM mechanization subsidy for plant protection equ... |
| **S022** | Kalaburagi | Sunflower | 1.8 | Dryland (Rainfed) | General (OC) | Marginal (< 2.5 acres) | `SOIL_HEALTH_AND_FERTILIZER` | Rainfed (None) | Evaluate universal access to Soil Health Card diagnostic pro... |

---

## 3. Scenario-by-Scenario Detailed Execution Results

### 3.1 Scenario S017: Yadgir — Cotton (6.0 ac, ST)

- **Agro-Climatic Zone:** North Eastern Dry Zone (Z2)  
- **Stated Need:** `CROP_INSURANCE`  
- **Farmer Query:** *"Cotton crop in Shorapur taluk, Yadgir severely infested by pink bollworm and whitefly; boll rot observed following dry-spell; enrolled in PMFBY via Samrakshane portal; need claim assessment procedure and localized calamity survey details."*  
- **Actionable Outcome Summary:** **6 ELIGIBLE** | **8 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **`ELIGIBLE`** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>`PMKISAN_PENSION_UNDER_10K_OR_NONE`<br>`PMKISAN_NO_PROFESSIONAL_EXCLUSION` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **`ELIGIBLE`** | `PMFBY_NOTIFIED_CROP_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **`INELIGIBLE`** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | **Disq:** Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **`ELIGIBLE`** | `SMAM_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **`ELIGIBLE`** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **`INELIGIBLE`** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | **Disq:** Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Cotton' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **`INELIGIBLE`** | `GK_PARENT_EXCEEDS_5_ACRES` | **Disq:** Landholding (6.0 ac) exceeds maximum ceiling of 5.0 acres for Individual Borewells. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_AMBEDKAR_INDIVIDUAL_OVER_5_AC` | **Disq:** Applicant social category 'ST' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to SCH010_VALMIKI instead).<br>**Disq:** Individual landholding (6.0 ac) exceeds Ambedkar Corporation individual ceiling of 5.0 acres. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_VALMIKI_EXCEEDS_5_AC` | **Disq:** Individual landholding (6.0 ac) exceeds maximum 5.0 acres ceiling. | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_EXCEEDS_5_AC` | **Disq:** Applicant social category 'ST' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to SCH010_VALMIKI instead).<br>**Disq:** Individual landholding (6.0 ac) exceeds maximum 5.0 acres ceiling. | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_EXCEEDS_5_AC` | **Disq:** Applicant social category 'ST' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_VALMIKI instead).<br>**Disq:** Individual landholding (6.0 ac) exceeds maximum 5.0 acres ceiling. | Availability unknown — confirmation required |

### 3.2 Scenario S018: Raichur — Sunflower (2.0 ac, General (OC))

- **Agro-Climatic Zone:** North Eastern Dry Zone (Z2)  
- **Stated Need:** `INCOME_SUPPORT`  
- **Farmer Query:** *"Retired non-MTS state board employee with 2.0 acres rainfed sunflower in Manvi taluk, Raichur; receiving exactly ₹10,000 per month pension; registered on FRUITS portal but PM-KISAN 17th installment rejected at state nodal verification; need reason for rejection and grievance procedure."*  
- **Actionable Outcome Summary:** **5 ELIGIBLE** | **9 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **`INELIGIBLE`** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>`PMKISAN_PENSION_OVER_10K_EXCLUSION`<br>`PMKISAN_NO_PROFESSIONAL_EXCLUSION` | **Disq:** Family member receives monthly pension of Rs. 10,000 (>= Rs. 10,000 threshold). | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **`ELIGIBLE`** | `PMFBY_NOTIFIED_CROP_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **`INELIGIBLE`** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | **Disq:** Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **`ELIGIBLE`** | `SMAM_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **`ELIGIBLE`** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **`INELIGIBLE`** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | **Disq:** Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Sunflower' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **`INELIGIBLE`** | `GK_PARENT_REGISTRY_CORPORATION_MISMATCH` | **Disq:** Ineligible for all four Ganga Kalyana implementation records currently represented in the registry (SCH010_AMBEDKAR, SCH010_VALMIKI, SCH010_DEVARAJ_URS, SCH010_KMDC) because applicant (General Merit) does not meet covered corporation-category requirements. This result does not establish ineligibility for every Ganga Kalyana-related programme in Karnataka. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |

### 3.3 Scenario S019: Kalaburagi — Bajra (1.2 ac, OBC (2A))

- **Agro-Climatic Zone:** North Eastern Dry Zone (Z2)  
- **Stated Need:** `RAINWATER_HARVESTING`  
- **Farmer Query:** *"Marginal Kuruba (OBC 2A) farmer with 1.2 acres dryland bajra in Afzalpur taluk, Kalaburagi; recurrent dry spells destroying crops; need 80% subsidy for constructing farm pond (Krishi Honda) with polythene lining and diesel pump under Krishi Bhagya."*  
- **Actionable Outcome Summary:** **6 ELIGIBLE** | **7 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008', 'SCH010']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **`ELIGIBLE`** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>`PMKISAN_PENSION_UNDER_10K_OR_NONE`<br>`PMKISAN_NO_PROFESSIONAL_EXCLUSION` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **`INELIGIBLE`** | `PMFBY_NON_NOTIFIED_CROP` | **Disq:** Primary crop 'Bajra' is not among notified food, oilseed, or commercial crops in Karnataka insurance units. | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **`INELIGIBLE`** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | **Disq:** Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **`ELIGIBLE`** | `SMAM_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **`ELIGIBLE`** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **`INELIGIBLE`** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | **Disq:** Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Bajra' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_AMBEDKAR_INDIVIDUAL_UNDER_1_5_AC` | **Disq:** Applicant social category 'OBC (2A)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead).<br>**Disq:** Individual landholding (1.2 ac) is below Ambedkar Corporation minimum threshold of 1.5 acres (1 acre 20 guntas), and community pooled route was not satisfied. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'OBC (2A)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead). | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`ELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'OBC (2A)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead). | Availability unknown — confirmation required |

### 3.4 Scenario S020: Yadgir — Redgram (6.5 ac, SC)

- **Agro-Climatic Zone:** North Eastern Dry Zone (Z2)  
- **Stated Need:** `SOLAR_PUMP_INSTALLATION`  
- **Farmer Query:** *"SC farmer with 6.5 acres redgram in Yadgir taluk; drilled borewell 6 months ago with yield but grid connection status from GESCOM is unconfirmed; tax assessment documentation not submitted; need standalone solar pump subsidy under PM-KUSUM Component B."*  
- **Actionable Outcome Summary:** **6 ELIGIBLE** | **6 INELIGIBLE** | **3 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **`REQUIRES_VERIFICATION`** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_INCOME_TAX_UNKNOWN`<br>`PMKISAN_PENSION_UNDER_10K_OR_NONE`<br>`PMKISAN_NO_PROFESSIONAL_EXCLUSION` | **Missing:** Verification of income tax assessment status for farmer family members. | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **`ELIGIBLE`** | `PMFBY_NOTIFIED_CROP_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **`ELIGIBLE`** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_WATER_SOURCE_VERIFIED`<br>`PMKSY_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **`ELIGIBLE`** | `SMAM_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **`ELIGIBLE`** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **`REQUIRES_VERIFICATION`** | `KUSUM_B_WATER_SOURCE_PRESENT`<br>`KUSUM_B_GRID_STATUS_UNKNOWN` | **Missing:** Certificate from ESCOM confirming no grid electricity connection exists for this water source. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Redgram' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **`INELIGIBLE`** | `GK_PARENT_EXISTING_BOREWELL_EXCLUSION`<br>`GK_PARENT_EXCEEDS_5_ACRES` | **Disq:** Land parcel already possesses an existing borewell.<br>**Disq:** Landholding (6.5 ac) exceeds maximum ceiling of 5.0 acres for Individual Borewells. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_AMBEDKAR_EXISTING_BOREWELL`<br>`GK_AMBEDKAR_INDIVIDUAL_OVER_5_AC` | **Disq:** Land parcel already possesses an existing borewell.<br>**Disq:** Individual landholding (6.5 ac) exceeds Ambedkar Corporation individual ceiling of 5.0 acres. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_EXISTING_BOREWELL`<br>`GK_SCH010_VALMIKI_EXCEEDS_5_AC` | **Disq:** Applicant social category 'SC' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead).<br>**Disq:** Land parcel already possesses an existing borewell.<br>**Disq:** Individual landholding (6.5 ac) exceeds maximum 5.0 acres ceiling. | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_EXISTING_BOREWELL`<br>`GK_SCH010_DEVARAJ_URS_EXCEEDS_5_AC` | **Disq:** Applicant social category 'SC' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead).<br>**Disq:** Land parcel already possesses an existing borewell.<br>**Disq:** Individual landholding (6.5 ac) exceeds maximum 5.0 acres ceiling. | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_EXISTING_BOREWELL`<br>`GK_SCH010_KMDC_EXCEEDS_5_AC` | **Disq:** Applicant social category 'SC' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead).<br>**Disq:** Land parcel already possesses an existing borewell.<br>**Disq:** Individual landholding (6.5 ac) exceeds maximum 5.0 acres ceiling. | Availability unknown — confirmation required |

### 3.5 Scenario S021: Raichur — Cotton (4.0 ac, Minority (Muslim))

- **Agro-Climatic Zone:** North Eastern Dry Zone (Z2)  
- **Stated Need:** `FARM_MECHANIZATION`  
- **Farmer Query:** *"Cotton farmer with 4.0 acres canal-irrigated land in Sindhanoor taluk, Raichur; facing severe sucking pest and bollworm pressure; manual spraying is labour intensive and slow; need subsidy under SMAM for purchasing a power sprayer / boom sprayer."*  
- **Actionable Outcome Summary:** **6 ELIGIBLE** | **8 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **`ELIGIBLE`** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>`PMKISAN_PENSION_UNDER_10K_OR_NONE`<br>`PMKISAN_NO_PROFESSIONAL_EXCLUSION` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **`ELIGIBLE`** | `PMFBY_NOTIFIED_CROP_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **`ELIGIBLE`** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_WATER_SOURCE_VERIFIED`<br>`PMKSY_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **`ELIGIBLE`** | `SMAM_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **`INELIGIBLE`** | `KRISHI_BHAGYA_NOT_DRYLAND`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | **Disq:** Krishi Bhagya is strictly restricted to dryland rainfed holdings (current land_type: Irrigated (Canal)). | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **`INELIGIBLE`** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | **Disq:** Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Cotton' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **`INELIGIBLE`** | `GK_PARENT_NOT_DRYLAND` | **Disq:** Land must be exclusively dryland (kushki). Current land_type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_AMBEDKAR_NOT_DRYLAND`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'Minority (Muslim)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to SCH010_KMDC instead).<br>**Disq:** Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_NOT_DRYLAND`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'Minority (Muslim)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_KMDC instead).<br>**Disq:** Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_NOT_DRYLAND`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'Minority (Muslim)' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to SCH010_KMDC instead).<br>**Disq:** Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_NOT_DRYLAND`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | **Disq:** Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |

### 3.6 Scenario S022: Kalaburagi — Sunflower (1.8 ac, General (OC))

- **Agro-Climatic Zone:** North Eastern Dry Zone (Z2)  
- **Stated Need:** `SOIL_HEALTH_AND_FERTILIZER`  
- **Farmer Query:** *"Marginal farmer with 1.8 acres dryland black cotton soil in Jewargi taluk, Kalaburagi preparing for sunflower/Bengalgram sowing; yield has dropped over last 2 years despite DAP application; need soil sample testing and Soil Health Card nutrient recommendations."*  
- **Actionable Outcome Summary:** **6 ELIGIBLE** | **8 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **`ELIGIBLE`** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>`PMKISAN_PENSION_UNDER_10K_OR_NONE`<br>`PMKISAN_NO_PROFESSIONAL_EXCLUSION` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **`ELIGIBLE`** | `PMFBY_NOTIFIED_CROP_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **`INELIGIBLE`** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | **Disq:** Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **`ELIGIBLE`** | `SMAM_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **`ELIGIBLE`** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **`INELIGIBLE`** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | **Disq:** Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Sunflower' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **`INELIGIBLE`** | `GK_PARENT_REGISTRY_CORPORATION_MISMATCH` | **Disq:** Ineligible for all four Ganga Kalyana implementation records currently represented in the registry (SCH010_AMBEDKAR, SCH010_VALMIKI, SCH010_DEVARAJ_URS, SCH010_KMDC) because applicant (General Merit) does not meet covered corporation-category requirements. This result does not establish ineligibility for every Ganga Kalyana-related programme in Karnataka. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to NONE instead). | Availability unknown — confirmation required |

---

## 4. Policy Rules & Statutory Boundary Analysis

### 4.1 Challenge 3: PM-KISAN Pension Exclusion Boundary Test (Scenario S018)

- **Scenario Context:** S018 represents a marginal farmer (2.0 ac, Raichur) who retired from a state institutional board, receiving superannuated monthly pension of **exactly ₹10,000**.
- **Statutory Guideline:** Under Clause 2(d)(iv) of the PM-KISAN operational guidelines, all superannuated/retired pensioners whose monthly pension is ₹10,000 or more (excluding MTS/Class IV/Group D employees) are excluded from the scheme definition of eligible farmer family.
- **Explicit Schema Attributes:** Represented explicitly with `superannuated_pensioner_monthly_amount = 10000.0` and `pensioner_is_mts_exempt = False`. No attribute inference or synthetic default was applied.
- **Engine Execution Result:** The frozen engine evaluated the condition `s.superannuated_pensioner_monthly_amount >= 10000`. Since the amount is exactly 10,000 and MTS exemption is `False`, the rule key **`PMKISAN_PENSION_OVER_10K_EXCLUSION`** fired cleanly, returning **`INELIGIBLE`**.
- **Rule Key Documentation Alignment:** In `benchmark_v1_design.md` §2.2 (Table line 121), the descriptive narrative originally contained a typo referencing `(PMKISAN_PENSION_UNDER_10K_OR_NONE)`. This has been corrected in the design document to match the engine's true rule key: `PMKISAN_PENSION_OVER_10K_EXCLUSION`.
- **Potential Future Naming Improvement:** As noted during policy review, `PMKISAN_PENSION_OVER_10K_EXCLUSION` could be misinterpreted as strictly greater than (> ₹10,000), whereas the statutory rule and implementation are inclusive (>= ₹10,000). For a future engine release (post-freeze), renaming the key to `PMKISAN_PENSION_GE_10K_EXCLUSION` or `PMKISAN_PENSION_THRESHOLD_EXCLUSION` is recommended. The frozen engine remains untouched.

### 4.2 Challenge 4: Three-Valued Logic & Explicit UNKNOWN Handling (Scenario S020)

- **Scenario Context:** S020 represents a medium SC farmer (6.5 ac, Yadgir) with a privately drilled borewell seeking standalone solar pump subsidy under PM-KUSUM Component B.
- **Three-Valued Electric Status:** `borewell_electric_status = BorewellElectricStatus.UNKNOWN`. The engine does not assume off-grid or grid-connected status. It verifies that a drilled physical source exists (`KUSUM_B_WATER_SOURCE_PRESENT`), but flags that ESCOM non-energization certificate is unverified, firing **`KUSUM_B_GRID_STATUS_UNKNOWN`** and returning **`REQUIRES_VERIFICATION`**.
- **Three-Valued Income Tax Status:** `paid_income_tax_last_assessment_year = None`. The engine does not infer tax payment from annual family income (₹2.2 Lakh). It fires **`PMKISAN_INCOME_TAX_UNKNOWN`**, returning **`REQUIRES_VERIFICATION`** for PM-KISAN.
- **Ganga Kalyana Disqualification:** Despite SC social category, S020 is disqualified from Ganga Kalyana on two distinct statutory grounds: existing borewell (`GK_PARENT_EXISTING_BOREWELL_EXCLUSION`) and landholding exceeding the 5.0-acre individual ceiling (`GK_PARENT_EXCEEDS_5_ACRES`).

### 4.3 Krishi Bhagya & District Notification Audit

- All three Zone Z2 districts (**Kalaburagi**, **Yadgir**, and **Raichur**) are verified in the frozen engine's `RAINFED_DRYLAND_DISTRICTS` set.
- **Dryland Scenarios (`S017`, `S018`, `S019`, `S020`, `S022`):** All qualify for Krishi Bhagya package (`KRISHI_BHAGYA_DRYLAND_VERIFIED`, `KRISHI_BHAGYA_DISTRICT_NOTIFIED`, `KRISHI_BHAGYA_ACREAGE_VALID`). In `S019` (stated need `RAINWATER_HARVESTING`, 1.2 ac), the 1.0-acre minimum catchment is satisfied.
- **Canal-Irrigated Scenario (`S021`):** Land type is `Irrigated (Canal)`. The frozen engine strictly disqualifies Krishi Bhagya with **`KRISHI_BHAGYA_NOT_DRYLAND`**, demonstrating proper hydrological gating.

### 4.4 Crop Insurance (PMFBY) & Bajra Policy Review (Scenario S019)

- **Notified Crops in Z2:** Cotton (`S017`, `S021`), Sunflower (`S018`, `S022`), and Redgram (`S020`) are present in `NOTIFIED_PMFBY_CROPS` in `engine.py`, firing `PMFBY_NOTIFIED_CROP_VERIFIED` and returning `ELIGIBLE`.
- **S019 Bajra Exclusion Analysis:** For scenario S019 (Kalaburagi, primary crop Bajra / pearl millet / sajje), the engine returned `INELIGIBLE` with rule key **`PMFBY_NON_NOTIFIED_CROP`**.
- **Policy Status vs Engine Artifact:** In the frozen `engine.py` (line 45), `NOTIFIED_PMFBY_CROPS` is a simplified static set of 16 crops. While coarse cereals such as Ragi and Jowar are included, Bajra is omitted. However, official Karnataka Department of Agriculture notifications and national PMFBY portal historical schedules regularly notify Bajra as an insurable Kharif cereal in northern dryland districts, including Kalaburagi, Yadgir, Vijayapura, and Koppal.
- **Audit Finding:** The rejection `PMFBY_NON_NOTIFIED_CROP` is an artifact of the engine's static whitelist rather than verified ground-truth exclusion for Kalaburagi in Kharif 2026. Therefore, this result must **not** be treated as a legally verified exclusion. It is recorded as an **Unresolved Policy-Validation Dependency** requiring district-level gazette verification before concluding ineligibility. In accordance with frozen invariants, the engine was not altered.

### 4.5 Ganga Kalyana Corporation Provisional Status Audit (Scenarios S017 & S019)

The 16-scheme master database designates corporation records with distinct audit statuses:
- `SCH010_AMBEDKAR` (Dr. B.R. Ambedkar Development Corporation — SC): **`VERIFIED`** (official government rules verified: 1.5–5.0 ac individual, 8–15 ac with $\ge 3$ beneficiaries pooled).
- `SCH010_VALMIKI` (Maharshi Valmiki ST Development Corporation — ST): **`PROVISIONAL`**.
- `SCH010_DEVARAJ_URS` (D. Devaraj Urs Backward Classes Development Corporation — OBC): **`PROVISIONAL`**.
- `SCH010_KMDC` (Karnataka Minorities Development Corporation — Minority): **`PROVISIONAL`**.

**Audit of S017 (ST, 6.0 ac, Yadgir):**
- S017 routes to `SCH010_VALMIKI`. The engine evaluated 6.0 ac against the 5.0-acre ceiling and returned `INELIGIBLE` (`GK_SCH010_VALMIKI_EXCEEDS_5_AC`).
- *Critical Policy Caveat:* Because `SCH010_VALMIKI` is provisional, applying a 5.0-acre ceiling extrapolated from Ambedkar Corporation rules cannot be treated as definitive legal proof of Valmiki Corporation's operational policy. Valmiki Corporation operational circulars for FY 2026-27 remain an unverified dependency.

**Audit of S019 (OBC 2A, 1.2 ac, Kalaburagi):**
- S019 routes to `SCH010_DEVARAJ_URS`. The engine evaluated 1.2 ac and returned `ELIGIBLE` (`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID`).
- *Critical Benchmark Governance Caveat:* Because `SCH010_DEVARAJ_URS` has `audit_status: PROVISIONAL`, it must be classified under **Section B (Provisional Schemes / Qualitative Review)** in the benchmark evaluation sheets rather than presented as a verified, confirmed entitlement. Under Annotation Protocol v1.1 §4, Section B schemes are strictly excluded from numerical scoring (0–3) by expert raters and must carry explicit verification disclaimers for end-user farmers.

---

## 5. Automated Parent Deduplication Audit

The deduplication engine (`resolve_actionable_determinations`) executed across all 6 scenarios with zero failures:

| Scenario | Parent IDs Evaluated | Actionable Children Detected | Suppressed Parent Records | Audit Outcome |
|:---:|:---|:---|:---|:---:|
| **S017** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP` (GK parent is Ineligible) | `['SCH008']` | **PASS (Suppressed)** |
| **S018** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP` (GK parent is Ineligible) | `['SCH008']` | **PASS (Suppressed)** |
| **S019** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` | `['SCH008', 'SCH010']` | **PASS (Suppressed)** |
| **S020** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP` (GK parent is Ineligible) | `['SCH008']` | **PASS (Suppressed)** |
| **S021** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP` (GK parent is Ineligible) | `['SCH008']` | **PASS (Suppressed)** |
| **S022** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP` (GK parent is Ineligible) | `['SCH008']` | **PASS (Suppressed)** |

Zero abstract parents appear alongside their concrete children in the actionable recommendations table.

---

## 6. Evidence-Based Governance & Action Proposals Before Zone Z3

1. **Documentation Alignment (Completed):** Corrected `benchmark_v1_design.md` §2.2 (line 121) to cite `PMKISAN_PENSION_OVER_10K_EXCLUSION`. Logged a post-freeze recommendation to rename this rule key to `PMKISAN_PENSION_GE_10K_EXCLUSION`.
2. **S019 PMFBY Policy Clarification (Logged):** Explicitly documented in S019 profile notes and Section 4.4 that `PMFBY_NON_NOTIFIED_CROP` reflects an engine whitelist constraint and must not be used as definitive evidence of Kharif 2026 Bajra exclusion in Kalaburagi.
3. **Provisional Corporation Protection (Formalized):** In upcoming expert annotation sheets for S011–S070, all determinations under `SCH010_VALMIKI`, `SCH010_DEVARAJ_URS`, and `SCH010_KMDC` (along with `SCH008_KA_COOP`) will be segregated into Section B (`REQUIRES_VERIFICATION` / Provisional Policy Review) and shielded from numerical 0–3 relevance scoring until primary circulars are verified.

---

*(Report automatically generated by `scripts/run_benchmark_z2_execution.py`)*
