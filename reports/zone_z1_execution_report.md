# Deliverable 3: Zone Z1 Execution Report (Scenarios S011–S016)

**Project:** ML-Based Personalized Government Scheme and Subsidy Recommendation System for Farmers (Karnataka Context)  
**Milestone:** Benchmark v1.0.3 — Zone Z1 Scenario Generation & Rule-Validation Audit  
**Zone:** Zone Z1 — North Eastern Transition Zone (Bidar & Kalaburagi)  
**Execution Date:** October 2026  
**Engine Version:** Deterministic Eligibility Engine v1.2 (Frozen Commit `7724fa7`)  
**Availability Filter:** 4-State Decoupled Availability Pipeline (Snapshot `2026-10-15`)  
**Audit Scope:** Exactly six detailed scenarios (`S011`–`S016`) evaluated across all 16 scheme records (6 parent/standalone + 10 child/standalone).  

---

## 1. Executive Summary & Verification Audit

This report documents the rigorous rule-validation of the first batch of six benchmark scenarios (S011–S016) representing the **North Eastern Transition Zone (Zone Z1)**. In strict adherence to the project invariants:

1. **Zero Modifications to Frozen Engine:** The eligibility engine (`src/eligibility/engine.py`) and scheme master (`scheme_database/processed/scheme_master.json`) were executed byte-for-byte without altering any rule to force passing.
2. **Zero Synthetic Annotations:** No machine learning models were trained, no synthetic ratings were fabricated, and no expert scores were predicted. These scenarios are validated deterministically before independent expert annotation.
3. **100% Assignment Table Fidelity:** Every scenario preserves its assigned district, crop, land size, land type, social category, tenure status, and primary policy challenge from `benchmark-design-v1.0.3`.
4. **Parent Deduplication Enforced:** Abstract parent records (`SCH008`, `SCH010`) are automatically suppressed from actionable recommendations when their concrete child implementations are actionable.
5. **Explicit Separation of Eligibility vs Availability:** Statutory qualifications are evaluated via Three-Valued Logic (`ELIGIBLE`, `INELIGIBLE`, `REQUIRES_VERIFICATION`), while operational availability is maintained in four separate states.

---

## 2. Zone Z1 Scenario Input Overview (S011–S016)

| Scenario ID | District | Primary Crop | Land (Ac) | Land Type | Social Cat. | Farmer Class | Immediate Need | Operational Water Source | Key Statutory Test |
|---|---|---|---|---|---|---|---|---|---|
| **S011** | Bidar | Redgram | 1.8 | Dryland (Rainfed) | OBC (2A) | Marginal (< 2.5 acres) | `CROP_INSURANCE` | Rainfed Dryland (No borewell or open well present) | Standard multi-need rainfed pulse profile in Zone Z1; valida... |
| **S012** | Kalaburagi | Maize | 3.0 | Dryland (Rainfed) | SC | Small (2.5-5 acres) | `SOLAR_PUMP_INSTALLATION` | Borewell (Non-energized) | Evaluate PM-KUSUM Component B standalone solar pump eligibil... |
| **S013** | Bidar | Sugarcane | 5.0 | Irrigated (Canal) | General (OC) | Small (2.5-5 acres) | `SOIL_HEALTH_AND_FERTILIZER` | Irrigated (Canal) — Karanja Command Area | Validate boundary condition at exactly 5.0 acres; verify can... |
| **S014** | Kalaburagi | Soybean | 2.2 | Dryland (Rainfed) | ST | Marginal (< 2.5 acres) | `PRODUCTION_CREDIT` | Rainfed Dryland (No operational water source) | Evaluate Challenge 6 credit routing; confirm ST routing unde... |
| **S015** | Bidar | Jowar | 1.5 | Dryland (Rainfed) | SC | Marginal (< 2.5 acres) | `INCOME_SUPPORT` | Rainfed Dryland (No operational water source) | Evaluate Challenge 2 handling for income distress; verify PM... |
| **S016** | Kalaburagi | Redgram | 4.5 | Dryland (Rainfed) | SC | Small (2.5-5 acres) | `BOREWELL_IRRIGATION` | None (Completely rainfed dryland; seeking groundwater exploration) | Validate Ambedkar Corporation individual borewell route as p... |

---

## 3. Scenario-by-Scenario Detailed Execution Results

### 3.1 Scenario S011: Bidar — Redgram (1.8 ac, OBC (2A))

- **Agro-Climatic Zone:** North Eastern Transition Zone (Z1)  
- **Stated Need:** `CROP_INSURANCE`  
- **Farmer Query:** *"Redgram crop in Aurad taluk, Bidar suffering from severe pod borer and wilt attack; flower dropping observed; need immediate compensation claim procedure under PMFBY and advisory."*  
- **Actionable Outcome Summary:** **7 ELIGIBLE** | **6 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008', 'SCH010']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **`ELIGIBLE`** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>`PMKISAN_PENSION_UNDER_10K_OR_NONE`<br>`PMKISAN_NO_PROFESSIONAL_EXCLUSION` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **`ELIGIBLE`** | `PMFBY_NOTIFIED_CROP_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **`INELIGIBLE`** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | **Disq:** Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **`ELIGIBLE`** | `SMAM_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **`ELIGIBLE`** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **`INELIGIBLE`** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | **Disq:** Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Redgram' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'OBC (2A)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead). | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'OBC (2A)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead). | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`ELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'OBC (2A)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_DEVARAJ_URS instead). | Availability unknown — confirmation required |

### 3.2 Scenario S012: Kalaburagi — Maize (3.0 ac, SC)

- **Agro-Climatic Zone:** North Eastern Transition Zone (Z1)  
- **Stated Need:** `SOLAR_PUMP_INSTALLATION`  
- **Farmer Query:** *"Drilled 400ft borewell in Aland taluk, Kalaburagi with good yield but no electricity line nearby; GESCOM waiting list is long; need standalone solar pump subsidy under PM-KUSUM Component B."*  
- **Actionable Outcome Summary:** **8 ELIGIBLE** | **6 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **`ELIGIBLE`** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>`PMKISAN_PENSION_UNDER_10K_OR_NONE`<br>`PMKISAN_NO_PROFESSIONAL_EXCLUSION` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **`ELIGIBLE`** | `PMFBY_NOTIFIED_CROP_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **`ELIGIBLE`** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_WATER_SOURCE_VERIFIED`<br>`PMKSY_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **`ELIGIBLE`** | `SMAM_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **`ELIGIBLE`** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **`ELIGIBLE`** | `KUSUM_B_WATER_SOURCE_PRESENT`<br>`KUSUM_B_OFF_GRID_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Maize' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **`INELIGIBLE`** | `GK_PARENT_EXISTING_BOREWELL_EXCLUSION` | **Disq:** Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_AMBEDKAR_EXISTING_BOREWELL`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | **Disq:** Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_EXISTING_BOREWELL`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'SC' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead).<br>**Disq:** Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_EXISTING_BOREWELL`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'SC' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead).<br>**Disq:** Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_EXISTING_BOREWELL`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'SC' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead).<br>**Disq:** Land parcel already possesses an existing borewell. | Availability unknown — confirmation required |

### 3.3 Scenario S013: Bidar — Sugarcane (5.0 ac, General (OC))

- **Agro-Climatic Zone:** North Eastern Transition Zone (Z1)  
- **Stated Need:** `SOIL_HEALTH_AND_FERTILIZER`  
- **Farmer Query:** *"Sugarcane crop in Karanja command area, Bhalki taluk showing leaf chlorosis and stunted cane girth; excessive urea applied over past 3 seasons; need soil testing and balanced NPK micronutrient advisory under Soil Health Card."*  
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
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Sugarcane' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010** | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `PARENT` | **`INELIGIBLE`** | `GK_PARENT_REGISTRY_CORPORATION_MISMATCH`<br>`GK_PARENT_NOT_DRYLAND` | **Disq:** Ineligible for all four Ganga Kalyana implementation records currently represented in the registry (SCH010_AMBEDKAR, SCH010_VALMIKI, SCH010_DEVARAJ_URS, SCH010_KMDC) because applicant (General Merit) does not meet covered corporation-category requirements. This result does not establish ineligibility for every Ganga Kalyana-related programme in Karnataka.<br>**Disq:** Land must be exclusively dryland (kushki). Current land_type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_AMBEDKAR_NOT_DRYLAND`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to NONE instead).<br>**Disq:** Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_NOT_DRYLAND`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to NONE instead).<br>**Disq:** Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_NOT_DRYLAND`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to NONE instead).<br>**Disq:** Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_NOT_DRYLAND`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'General (OC)' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to NONE instead).<br>**Disq:** Must be exclusively dryland (kushki). Land type 'Irrigated (Canal)' is disqualified. | Availability unknown — confirmation required |

### 3.4 Scenario S014: Kalaburagi — Soybean (2.2 ac, ST)

- **Agro-Climatic Zone:** North Eastern Transition Zone (Z1)  
- **Stated Need:** `PRODUCTION_CREDIT`  
- **Farmer Query:** *"Marginal tribal farmer in Sedam, Kalaburagi preparing for Kharif soybean sowing; need short-term crop loan for seeds and fertilizer; want to know interest subvention rate between Grameena Bank KCC and local PACS cooperative society."*  
- **Actionable Outcome Summary:** **7 ELIGIBLE** | **6 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008', 'SCH010']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **`ELIGIBLE`** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>`PMKISAN_PENSION_UNDER_10K_OR_NONE`<br>`PMKISAN_NO_PROFESSIONAL_EXCLUSION` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **`ELIGIBLE`** | `PMFBY_NOTIFIED_CROP_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **`INELIGIBLE`** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | **Disq:** Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **`ELIGIBLE`** | `SMAM_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **`ELIGIBLE`** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **`INELIGIBLE`** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | **Disq:** Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Soybean' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_AMBEDKAR_SOCIAL_CATEGORY_MISMATCH`<br>`GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'ST' does not fall under Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka. (Routes to SCH010_VALMIKI instead). | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`ELIGIBLE`** | `GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'ST' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to SCH010_VALMIKI instead). | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'ST' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_VALMIKI instead). | Availability unknown — confirmation required |

### 3.5 Scenario S015: Bidar — Jowar (1.5 ac, SC)

- **Agro-Climatic Zone:** North Eastern Transition Zone (Z1)  
- **Stated Need:** `INCOME_SUPPORT`  
- **Farmer Query:** *"Dryland jowar in Humnabad taluk, Bidar facing severe moisture stress; family has acute cash shortage for daily food and medicine; need non-repayable government cash assistance or pension relief, cannot take more bank debt."*  
- **Actionable Outcome Summary:** **7 ELIGIBLE** | **6 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008', 'SCH010']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **`ELIGIBLE`** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>`PMKISAN_PENSION_UNDER_10K_OR_NONE`<br>`PMKISAN_NO_PROFESSIONAL_EXCLUSION` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **`ELIGIBLE`** | `PMFBY_NOTIFIED_CROP_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **`INELIGIBLE`** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | **Disq:** Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **`ELIGIBLE`** | `SMAM_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **`ELIGIBLE`** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **`INELIGIBLE`** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | **Disq:** Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Jowar' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`ELIGIBLE`** | `GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'SC' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead). | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'SC' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead). | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'SC' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead). | Availability unknown — confirmation required |

### 3.6 Scenario S016: Kalaburagi — Redgram (4.5 ac, SC)

- **Agro-Climatic Zone:** North Eastern Transition Zone (Z1)  
- **Stated Need:** `BOREWELL_IRRIGATION`  
- **Farmer Query:** *"SC dryland farmer in Afzalpur taluk, Kalaburagi with 4.5 acres dryland; completely dependent on erratic rainfall for redgram; have no borewell or open well; need free borewell drilling and pump under Ganga Kalyana Scheme Dr. B. R. Ambedkar Corporation."*  
- **Actionable Outcome Summary:** **7 ELIGIBLE** | **6 INELIGIBLE** | **1 REQUIRES_VERIFICATION**  
- **Automated Parent Deduplication:** Suppressed abstract parent records `['SCH008', 'SCH010']` to prevent duplicate cards alongside resolved children.  

| Scheme ID | Resolved Implementation Scheme Name | Record Type | Eligibility Status | Rule Keys Fired | Missing Verifications / Disqualifications | Availability State |
|---|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | **`ELIGIBLE`** | `PMKISAN_LAND_SIZE_POSITIVE`<br>`PMKISAN_CUTOFF_DATE_VERIFIED`<br>`PMKISAN_NO_INCOME_TAX_PAID`<br>`PMKISAN_PENSION_UNDER_10K_OR_NONE`<br>`PMKISAN_NO_PROFESSIONAL_EXCLUSION` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | **`ELIGIBLE`** | `PMFBY_NOTIFIED_CROP_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH003** | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `STANDALONE` | **`INELIGIBLE`** | `PMKSY_LAND_RANGE_VALID`<br>`PMKSY_NO_WATER_SOURCE`<br>`PMKSY_NO_PRIOR_SUBSIDY` | **Disq:** Must possess an assured operational water source with pump machinery. | Availability unknown — confirmation required |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | **`ELIGIBLE`** | `SMAM_NO_PRIOR_SUBSIDY` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | **`ELIGIBLE`** | `KRISHI_BHAGYA_DRYLAND_VERIFIED`<br>`KRISHI_BHAGYA_DISTRICT_NOTIFIED`<br>`KRISHI_BHAGYA_ACREAGE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH006** | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `STANDALONE` | **`INELIGIBLE`** | `KUSUM_B_NO_WATER_SOURCE`<br>`KUSUM_B_OFF_GRID_VERIFIED` | **Disq:** Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling. | Availability unknown — confirmation required |
| **SCH007** | Mission for Integrated Development of Horticulture (MIDH) | `STANDALONE` | **`INELIGIBLE`** | `MIDH_NON_HORTICULTURE_CROP`<br>`MIDH_LAND_MIN_MET`<br>`MIDH_NO_MICRO_IRRIGATION` | **Disq:** Primary crop 'Redgram' is not a recognized horticultural crop under MIDH.<br>**Disq:** MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot. | Availability unknown — confirmation required |
| **SCH008_CENTRAL** | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `CHILD` | **`ELIGIBLE`** | `KCC_CENTRAL_COMMERCIAL_ELIGIBLE` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH008_KA_COOP** | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `CHILD` | **`REQUIRES_VERIFICATION`** | `KCC_KA_COOP_PROVISIONAL_PENDING_GO` | **Missing:** Annual Cooperative Department GO verification | Availability unknown — confirmation required |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | **`ELIGIBLE`** | `SHC_UNIVERSAL_ACCESS_VERIFIED` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010_AMBEDKAR** | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `CHILD` | **`ELIGIBLE`** | `GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID` | None (Fully Verified) | Availability unknown — confirmation required |
| **SCH010_VALMIKI** | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_VALMIKI_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'SC' does not fall under Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead). | Availability unknown — confirmation required |
| **SCH010_DEVARAJ_URS** | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_DEVARAJ_URS_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'SC' does not fall under D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead). | Availability unknown — confirmation required |
| **SCH010_KMDC** | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `CHILD` | **`INELIGIBLE`** | `GK_SCH010_KMDC_SOCIAL_CATEGORY_MISMATCH`<br>`GK_SCH010_KMDC_INDIVIDUAL_ROUTE_VALID` | **Disq:** Applicant social category 'SC' does not fall under Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka. (Routes to SCH010_AMBEDKAR instead). | Availability unknown — confirmation required |

---

## 4. Policy Rules & Corporation Status Summary

### 4.1 Ganga Kalyana Implementation Routing

- **`S011` (Bidar, OBC):** Routes to D. Devaraj Urs Backward Classes Development Corporation (`SCH010_DEVARAJ_URS`). Individual route passes acreage window ($1.2 \le 1.8 \le 5.0$). Other corporation children (`SCH010_AMBEDKAR`, `SCH010_VALMIKI`, `SCH010_KMDC`) cleanly disqualified for social category mismatch. Devaraj Urs rules remain **PROVISIONAL** pending official annual notification.
- **`S012` (Kalaburagi, SC):** Disqualified from Ganga Kalyana parent and children (`GK_PARENT_EXISTING_BOREWELL_EXCLUSION`, `GK_SCH010_AMBEDKAR_EXISTING_BOREWELL`). The farmer already possesses an unenergized borewell; Ganga Kalyana strictly funds borewell drilling for borewell-less plots.
- **`S013` (Bidar, General Merit):** Disqualified from Ganga Kalyana parent and children due to General Merit exclusion (`GK_PARENT_REGISTRY_CORPORATION_MISMATCH`) and canal irrigation (`GK_PARENT_NOT_DRYLAND`).
- **`S014` (Kalaburagi, ST):** Routes to Maharshi Valmiki Scheduled Tribes Development Corporation (`SCH010_VALMIKI`). Individual route passes acreage window ($1.2 \le 2.2 \le 5.0$). Rules remain **PROVISIONAL**.
- **`S015` (Bidar, SC):** Routes to Dr. B. R. Ambedkar Development Corporation (`SCH010_AMBEDKAR`). Evaluates the lower individual acreage bound ($1.5 \le 1.5 \le 5.0$). Valid individual route.
- **`S016` (Kalaburagi, SC):** Routes to Dr. B. R. Ambedkar Development Corporation (`SCH010_AMBEDKAR`). Evaluates 4.5 acres ($1.5 \le 4.5 \le 5.0$). Valid individual route.

### 4.2 Competing Credit Routes (Challenge 6)

Across all six scenarios, credit eligibility divides into two distinct channels:
1. **`SCH008_CENTRAL` (Central KCC-MISS via Commercial Banks / RRBs):** Evaluated as **`ELIGIBLE`** (4.0% effective interest up to ₹3 Lakh upon prompt repayment). Appears in Section A of expert sheets.
2. **`SCH008_KA_COOP` (Karnataka Zero-Interest Crop Loan via PACS / DCCBs):** Evaluated as **`REQUIRES_VERIFICATION`** (0% interest up to ₹5 Lakh). Retained in Section B as PROVISIONAL pending verification of the active financial year Government Order.

### 4.3 Solar Pump Prerequisite Audit (Challenge 1 & PM-KUSUM B)

- Only **`S012`** satisfies the strict statutory prerequisites for PM-KUSUM Component B: drilled water source present (`Borewell (Non-energized)`) AND certified off-grid status (`UNENERGIZED_OFF_GRID`). Result: **`ELIGIBLE`**.
- `S011`, `S013`, `S014`, `S015`, and `S016` do not possess a drilled borewell (`KUSUM_B_NO_WATER_SOURCE`) and are cleanly evaluated as **`INELIGIBLE`**.

---

## 5. Automated Parent Deduplication Audit

The deduplication engine (`resolve_actionable_determinations`) executed across all 6 scenarios with zero failures:

| Scenario | Parent IDs Evaluated | Actionable Children Detected | Suppressed Parent Records | Audit Outcome |
|:---:|:---|:---|:---|:---:|
| **S011** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` | `['SCH008', 'SCH010']` | **PASS (Suppressed)** |
| **S012** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP` (GK parent is Ineligible) | `['SCH008']` | **PASS (Suppressed)** |
| **S013** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP` (GK parent is Ineligible) | `['SCH008']` | **PASS (Suppressed)** |
| **S014** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP`, `SCH010_VALMIKI` | `['SCH008', 'SCH010']` | **PASS (Suppressed)** |
| **S015** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP`, `SCH010_AMBEDKAR` | `['SCH008', 'SCH010']` | **PASS (Suppressed)** |
| **S016** | `SCH008`, `SCH010` | `SCH008_CENTRAL`, `SCH008_KA_COOP`, `SCH010_AMBEDKAR` | `['SCH008', 'SCH010']` | **PASS (Suppressed)** |

Zero abstract parents appear alongside their concrete children in the actionable recommendations table.

---

*(Report automatically generated by `scripts/run_benchmark_z1_execution.py`)*
