# Deliverable: Zone Z10 Execution Report (Scenarios S065–S070)

**Benchmark Version:** `v1.0.4`  
**Execution Date:** October 19, 2026  
**Agro-Climatic Zone:** Coastal Zone (Zone Z10 — Dakshina Kannada, Udupi, Uttara Kannada Coast)  
**Total Scenarios Evaluated:** Exactly 6 (`S065`–`S070`)  
**Audit Scope:** Exactly six detailed scenarios (`S065`–`S070`) evaluated across all 16 scheme records (8 standalone records, 2 parent records, and 6 child records).  

## 1. Executive Summary & Project Invariants

This report documents the rule-validation and governance audit of the tenth and final benchmark batch of six scenarios (S065–S070) representing the **Coastal Zone (Zone Z10)**. This completion marks the final delivery of the full 60-scenario Benchmark v1.0.4 matrix (S011–S070 across Zones Z1–Z10). In strict adherence to project invariants:

1. **Preservation of Frozen Engine (`src/eligibility/engine.py`):** The frozen engine is completely untouched and preserved at baseline commit `7724fa7`. Raw three-valued logic outcomes (`ELIGIBLE`, `INELIGIBLE`, `REQUIRES_VERIFICATION`) are evaluated deterministically.
2. **Preservation of Scheme Master (`scheme_database/processed/scheme_master.json`):** Scheme definitions, hierarchies, and metadata are unmodified.
3. **Preservation of Pilot Scenarios & Protocol:** Pilot scenarios `S001`–`S010` and annotation protocol `v1.1` remain strictly preserved.
4. **Benchmark Design v1.0.4 Compliance:** Strictly fulfills all representation quotas, cross-field area validations, solar pump prerequisites, and statutory inheritance definitions established in `benchmark_v1_design.md` v1.0.4.
5. **Operational Availability Safeguard:** Eligibility verified in Section A does **NOT** equate to active application window availability. All determinations carry availability state `Availability unknown — confirmation required`.
6. **Crop Insurance Decoupling (PMFBY/RWBCIS):** Static whitelist results from the raw engine are decoupled from governance presentation across all six scenarios. Unverified seasonal Insurance Unit (Gram Panchayat/Hobli level) notifications are strictly routed to Section B as `REQUIRES_VERIFICATION` with numerical scoring disabled.
7. **Provisional Schemes Quarantine:** Corporation schemes (`SCH008_KA_COOP`, `SCH010_VALMIKI`) are strictly quarantined in Section B without clinical scoring.
8. **S066 Community Borewell Scheme Safeguard (Challenge 7):** S066 features 4 SC farmers pooling 14.0 contiguous dryland acres (qualifying parcel 3.5 ac), evaluating raw ELIGIBLE (`GK_AMBEDKAR_COMMUNITY_ROUTE_VALID`) because Ambedkar Corporation rules require >= 3 beneficiaries on 8.0-15.0 acres pooled dryland. Governance conservatively decouples determination to Section B as `REQUIRES_VERIFICATION` with scoring disabled pending confirmation of current administrative circular instructions, registered boundary alignment, and groundwater clearances; parent `SCH010` is suppressed.
9. **S069 Statutory Inheritance Succession (PM-KISAN Guidelines §§5.2–5.3.3(i)):** Ownership acquired post-01.02.2019 is strictly verified under `transfer_basis = INHERITANCE_DUE_TO_DEATH` resulting from parent demise (April 2022), supported by registered death certificate, legal heir order, and Bhoomi mutation extract. Gated explicitly by governance check; distinct from post-cutoff sale, partition, and gift transfers under §5.3.3(ii); qualifies for PM-KISAN in Section A.
10. **S070 Unknown Land Title & Area Limit (Challenge 8 & Challenge 4):** Land title cut-off date is UNKNOWN (`land_ownership_cutoff_pre_feb_2019 = None`), strictly preserving three-valued logic in Section B (`REQUIRES_VERIFICATION`) for PM-KISAN and PMKSY-PDMC without scoring. Requested subsidized area (4.80 ha) is verified against the 12.5-acre parcel's physical capacity (5.059 ha) and the 5.00 ha PMKSY ceiling (§7.9 per beneficiary cap), with explicit first-time applicant status satisfying the 7-year lock-in restriction. Raw engine operational holding check (> 12.35 ac) vs governance subsidized parcel override explicitly recorded.
11. **S068 Pure Tenancy Routing (Challenge 5):** Pure tenant without recorded title is statutorily excluded from PM-KISAN (`PMKISAN_PURE_TENANT_EXCLUSION`); KCC commercial credit (`SCH008_CENTRAL`) routes to Section B as `REQUIRES_VERIFICATION` without scoring pending oral lease / tenant crop loan documentation verification.

## 2. Zone Z10 Scenario Input Overview (S065–S070)

| Scenario ID | District | Primary Crop | Holding (ac) | Land Type | Social Category | Farmer Class | Immediate Need | Operational Water Source | Benchmark Test Purpose |
|:---|:---|:---|:---:|:---|:---:|:---:|:---|:---|:---|
| **S065** | Dakshina Kannada | Coconut | 14.0 | Dryland (Rainfed) | General (OC) | Large (> 10 acres) | `SOIL_HEALTH_AND_FERTILIZER` | Rainfed Coastal | Soil Health Card universal diagnostic service for large coas... |
| **S066** | Udupi | Arecanut | 5.5 | Dryland (Rainfed) | SC | Medium (5-10 acres) | `BOREWELL_IRRIGATION` | None (Dryland kushki) | Challenge 7 community borewell pooling: Individual holding 5... |
| **S067** | Dakshina Kannada | Cashew | 2.0 | Dryland (Rainfed) | ST | Marginal (< 2.5 acres) | `CROP_INSURANCE` | Rainfed Coastal | PMFBY/RWBCIS cashew crop insurance in coastal plantation bel... |
| **S068** | Udupi | Paddy | 1.5 | Wetland/valley | Minority | Marginal (< 2.5 acres) | `PRODUCTION_CREDIT` | Wetland Inflow | Challenge 5 pure tenant coastal wetland paddy; strictly excl... |
| **S069** | Dakshina Kannada | Coconut | 13.0 | Dryland (Rainfed) | Minority | Large (> 10 acres) | `PROTECTED_HORTICULTURE` | Open Well / Rainfed | MIDH coastal nursery / shade-net; Large holding (13.0 ac); M... |
| **S070** | Udupi | Arecanut | 12.5 | Wetland/valley | SC | Large (> 10 acres) | `MICRO_IRRIGATION_SUPPORT` | Borewell (Grid-connected) | Challenge 8 and Challenge 4: Large holding (12.5 ac); PMKSY-... |

## 3. Governance Presentation Accounting & Reconciled Denominators

| Scenario | District | Primary Crop | Immediate Need | Section A (Confirmed) | Section B (Review / Unverified) | Disqualified Candidates | Total Actionable | Reconciled Formula |
|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **S065** | Dakshina Kannada | Coconut | `SOIL_HEALTH_AND_FERTILIZER` | **4** | **2** | **9** | **15** | 4 + 2 + 9 = 15 |
| **S066** | Udupi | Arecanut | `BOREWELL_IRRIGATION` | **4** | **3** | **7** | **14** | 4 + 3 + 7 = 14 |
| **S067** | Dakshina Kannada | Cashew | `CROP_INSURANCE` | **4** | **3** | **7** | **14** | 4 + 3 + 7 = 14 |
| **S068** | Udupi | Paddy | `PRODUCTION_CREDIT` | **2** | **3** | **10** | **15** | 2 + 3 + 10 = 15 |
| **S069** | Dakshina Kannada | Coconut | `PROTECTED_HORTICULTURE` | **6** | **2** | **7** | **15** | 6 + 2 + 7 = 15 |
| **S070** | Udupi | Arecanut | `MICRO_IRRIGATION_SUPPORT` | **3** | **4** | **8** | **15** | 3 + 4 + 8 = 15 |

### Denominator Reconciliations & Abstract Parent Suppression:
Every scenario evaluates exactly 16 raw scheme records. The number of displayed actionable schemes is explicitly reconciled based on whether child records of abstract parents (`SCH008`, `SCH010`) are actionable:

- In **S065, S068, S069, S070**: Abstract parent `SCH008` is suppressed because child credit records (`SCH008_CENTRAL`, `SCH008_KA_COOP`) are actionable. In contrast, zero Ganga Kalyana child corporation records are actionable $\implies$ abstract parent `SCH010` is retained as an ineligible umbrella record $\implies 16 - 1 = \mathbf{15}$ actionable schemes displayed.
- In **S066**: Abstract parent `SCH008` is suppressed by child credit schemes; child corporation record `SCH010_AMBEDKAR` evaluates ELIGIBLE (Community route valid) $\implies$ abstract parent `SCH010` is ALSO suppressed $\implies 16 - 2 = \mathbf{14}$ actionable schemes displayed.
- In **S067**: Abstract parent `SCH008` is suppressed by child credit schemes; child corporation record `SCH010_VALMIKI` evaluates ELIGIBLE (Individual route valid for ST marginal dryland) $\implies$ abstract parent `SCH010` is ALSO suppressed $\implies 16 - 2 = \mathbf{14}$ actionable schemes displayed.

## 4. Scenario-by-Scenario Detailed Governance Audits

### 4.5 Scenario S065: Dakshina Kannada — Coconut (14.0 ac, General (OC))

- **Context & Need:** Soil Health Card universal diagnostic service for large coastal plantation (14.0 ac); GM category; verifies Section A access to SHC, PM-KISAN, and SMAM; confirms district and category exclusions for Krishi Bhagya and Ganga Kalyana.
- **Physical Area Consistency:** `PASS: 14.0 ac holding matches parcel`
- **Water Infrastructure:** Rainfed Coastal (`NONE`)
- **Statutory Flags:** Tenure=`RTC registered pre-February 2019 in Bantwal taluk, Dakshina Kannada district`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `INELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned INELIGIBLE because Coconut is absent from static crop whitel... |
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

### 4.6 Scenario S066: Udupi — Arecanut (5.5 ac, SC)

- **Context & Need:** Challenge 7 community borewell pooling: Individual holding 5.5 ac exceeds 5.0 ac individual Ambedkar ceiling; community pool route valid with 4 SC farmers, 14.0 ac pooled contiguous dryland, qualifying parcel 3.5 ac (raw engine ELIGIBLE); governance safeguard conservatively keeps determination in Section B with scoring disabled pending corporation circular instructions, boundary consent, and groundwater clearances; parent SCH010 suppressed.
- **Physical Area Consistency:** `PASS: 3.5 ac qualifying parcel within 5.5 ac operational holding; 14.0 ac pooled contiguous block`
- **Water Infrastructure:** None (Dryland kushki) (`NONE`)
- **Statutory Flags:** Tenure=`RTC registered pre-February 2019 in Karkala taluk; registered joint consent deed with 3 contiguous SC neighbors`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned ELIGIBLE based on static crop whitelist for Arecanut, but co... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Community Corporation Rules Required) | No | Raw engine evaluated ELIGIBLE (GK_AMBEDKAR_COMMUNITY_ROUTE_VALID) because Dr. B.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

### 4.7 Scenario S067: Dakshina Kannada — Cashew (2.0 ac, ST)

- **Context & Need:** PMFBY/RWBCIS cashew crop insurance in coastal plantation belt; ST marginal farmer; raw PMFBY INELIGIBLE routed to Section B pending seasonal notification; SCH010_VALMIKI individual route valid but quarantined in Section B; parent SCH010 suppressed; PM-KISAN qualifies in Section A.
- **Physical Area Consistency:** `PASS: 2.0 ac holding matches parcel`
- **Water Infrastructure:** Rainfed Coastal (`NONE`)
- **Statutory Flags:** Tenure=`RTC registered pre-February 2019 in Belthangady taluk, Dakshina Kannada district`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `INELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned INELIGIBLE due to static PMFBY crop whitelist, but Cashew is... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Raw engine returned ELIGIBLE based on encoded rules, but scheme record is PROVIS... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

### 4.8 Scenario S068: Udupi — Paddy (1.5 ac, Minority)

- **Context & Need:** Challenge 5 pure tenant coastal wetland paddy; strictly excluded from PM-KISAN; KCC Central raw ELIGIBLE but routed to Section B pending tenant loan documentation; PMFBY routed to Section B; SMAM and SHC in Section A.
- **Physical Area Consistency:** `PASS: 1.5 ac holding matches parcel`
- **Water Infrastructure:** Wetland Inflow (`NONE`)
- **Statutory Flags:** Tenure=`Informal lease agreement / oral tenancy with village panchayat certificate in Kundapura taluk; no recorded title (Pure Tenant)`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Pure tenant farmer without recorded land ownership title is statutorily excluded... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned ELIGIBLE based on static crop whitelist for Paddy, but appli... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Tenant Crop-Loan Documentation Required) | No | Raw engine returned ELIGIBLE under RBI/NABARD tenant borrower category, but oral... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010` | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

### 4.9 Scenario S069: Dakshina Kannada — Coconut (13.0 ac, Minority)

- **Context & Need:** MIDH coastal nursery / shade-net; Large holding (13.0 ac); Minority; post-2019 statutory inheritance upon demise of parent under PM-KISAN §§5.2–5.3.3(i) (transfer_basis=INHERITANCE_DUE_TO_DEATH, legal heir cert & mutation verified; distinct from ineligible partition, sale, and gift deeds under §5.3.3(ii)); PM-KISAN, MIDH, PM-KUSUM B, and SMAM qualify in Section A.
- **Physical Area Consistency:** `PASS: 13.0 ac holding matches parcel`
- **Water Infrastructure:** Open Well / Rainfed (`NONE`)
- **Statutory Flags:** Tenure=`Title acquired via registered inheritance succession following demise of mother in April 2022; Death Cert No. DC/DK/2022/6104, Legal Heir Certificate LHC/DK/2022/339, and Bhoomi mutation Form 16 MR No. 2022-T771 (22.06.2022) verified`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Statutory Inheritance Compliance: Title acquired post-01.02.2019 strictly satisf... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `INELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned INELIGIBLE due to static PMFBY crop whitelist, but Coconut i... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH004` | Sub-Mission on Agricultural Mechanization (SMAM) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH005` | Krishi Bhagya Yojana | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH006` | PM-KUSUM Component B (Standalone Solar Agriculture Pumps) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH007` | Mission for Integrated Development of Horticulture (MIDH) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_CENTRAL` | Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs) | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH008_KA_COOP` | Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Provisional Schemes / Qualitative Review Only) | No | Provisional scheme requiring administrative or Government Order verification.... |
| `SCH009` | Soil Health Card Scheme | `ELIGIBLE` | `ELIGIBLE` | Section A (Confirmed Actionable Candidates) | Yes | Confirmed verified scheme eligible for clinical 0-3 relevance scoring.... |
| `SCH010` | Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_AMBEDKAR` | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_VALMIKI` | Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_DEVARAJ_URS` | Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |
| `SCH010_KMDC` | Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC) | `INELIGIBLE` | `INELIGIBLE` | Disqualified / Non-Actionable Candidates | No | Statutorily disqualified under verified criteria.... |

### 4.0 Scenario S070: Udupi — Arecanut (12.5 ac, SC)

- **Context & Need:** Challenge 8 and Challenge 4: Large holding (12.5 ac); PMKSY-PDMC requested 4.80 ha <= 12.5 ac (5.059 ha) and <= 5.00 ha ceiling (§7.9 per beneficiary cap); raw INELIGIBLE preserved while governance evaluates parcel request; title status UNKNOWN -> preserve three-valued logic in Section B for PMKSY-PDMC and PM-KISAN without numerical scoring; SMAM and KCC Central qualify in Section A.
- **Physical Area Consistency:** `PASS: requested 4.80 ha <= 12.5 ac (5.059 ha) qualifying parcel; satisfies PMKSY-PDMC 5.00 ha statutory ceiling`
- **Water Infrastructure:** Borewell (Grid-connected) (`GRID_CONNECTED_IP_SET`)
- **Statutory Flags:** Tenure=`Ancestral land title partition deed pending formal mutation on Bhoomi portal in Udupi taluk; record date unverified (UNKNOWN)`, Income Tax=`False`, Govt Employee=`NONE`

| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |
|:---|:---|:---:|:---:|:---|:---:|:---|
| `SCH001` | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `REQUIRES_VERIFICATION` | `REQUIRES_VERIFICATION` | Section B (Unresolved Statutory Evidence / Land Title Required) | No | Raw engine returned REQUIRES_VERIFICATION due to explicit UNKNOWN tenure cut-off... |
| `SCH002` | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `ELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Policy Review / Seasonal Notification Required) | No | Raw engine returned ELIGIBLE based on static crop whitelist, but land title cut-... |
| `SCH003` | Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC) | `INELIGIBLE` | `REQUIRES_VERIFICATION` | Section B (Unresolved Statutory Evidence / Land Title Required) | No | Raw Engine vs Governance Discrepancy & Area Validation: Raw engine returned INEL... |
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

The following verification dependencies remain active and are enforced across Zone Z10:

### S065 (Dakshina Kannada — Coconut)
- Verification of GoK Kharif 2026 Restructured Weather Based Crop Insurance Scheme (RWBCIS) / Coconut Palm Insurance Scheme notification for Bantwal taluk, Dakshina Kannada district
- Bantwal Taluk Agriculture Office Soil Health Card sample collection and mobile laboratory schedule

### S066 (Udupi — Arecanut)
- Verification of current Dr. B.R. Ambedkar Development Corporation FY 2026-27 administrative circular instructions and operational community borewell guidelines for Karkala taluk
- Field verification of registered joint consent deed, mutual water-sharing agreement, and contiguous boundary alignment for the 14.0-acre pooled block in Karkala taluk
- Mines and Geology Department hydrogeological feasibility and groundwater safety clearance for Karkala taluk
- Verification of GoK Kharif 2026 PMFBY Insurance Unit (Gram Panchayat level) notification for Arecanut in Karkala taluk, Udupi district

### S067 (Dakshina Kannada — Cashew)
- Verification of GoK Kharif 2026 RWBCIS Insurance Unit (Hobli level) notification for Cashew in Belthangady taluk, Dakshina Kannada district
- Karnataka Maharshi Valmiki ST Development Corporation FY 2026-27 individual borewell circular and target allocation for Belthangady taluk
- Mines and Geology Department groundwater safety clearance for Belthangady taluk

### S068 (Udupi — Paddy)
- Commercial bank / Karnataka Gramin Bank verification of oral lessee / tenant crop-loan eligibility documentation in Kundapura taluk, Udupi district
- Verification of GoK Kharif 2026 PMFBY Insurance Unit (Gram Panchayat level) notification and tenant cultivation declaration protocol for Paddy in Kundapura taluk
- Lead District Bank Udupi tenant farmer scale of finance certification

### S069 (Dakshina Kannada — Coconut)
- Verification of GoK Kharif 2026 RWBCIS/Coconut Palm Insurance Scheme notification for Puttur taluk, Dakshina Kannada district
- Dakshina Kannada District Horticulture Department MIDH FY 2026-27 nursery and shade-net target circular

### S070 (Udupi — Arecanut)
- Revenue Department certification of land ownership record date / RTC mutation order for Udupi taluk
- Verification of physical parcel boundaries, possession certificate, and micro-irrigation layout for 4.80 ha within 12.5 ac parcel
- Verification of GoK Kharif 2026 PMFBY Insurance Unit notification for Arecanut in Udupi taluk, Udupi district
- Udupi District Agriculture Office PMKSY-PDMC FY 2026-27 micro-irrigation target allocation and vendor empanelment

## 6. Frozen Invariants Check

| Invariant Component | Status | Verification Summary |
|:---|:---:|:---|
| `src/eligibility/engine.py` | **PRESERVED** | Untouched; raw evaluations deterministic |
| `scheme_database/processed/scheme_master.json` | **PRESERVED** | Untouched; 16 scheme records intact |
| Pilot Scenarios `S001`–`S010` | **PRESERVED** | Untouched; baseline calibration valid |
| Annotation Protocol `v1.1` | **PRESERVED** | Untouched; governance presentation standards maintained |
| Benchmark Design `v1.0.4` | **COMPLIANT** | All Z10 quotas, area caps, and tenure rules strictly satisfied |

## 7. Full Benchmark Delivery Completion (Ten-Zone Construction Sign-Off)

With the execution and verification of Zone Z10 (S065–S070), all 60 planned benchmark scenarios across ten agro-climatic zones are now fully constructed:

- **Zone Z1 (S011–S016):** North Eastern Transition Zone (Bidar, Kalaburagi)
- **Zone Z2 (S017–S022):** North Eastern Dry Zone (Kalaburagi, Yadgir, Raichur)
- **Zone Z3 (S023–S028):** Northern Dry Zone (Vijayapura, Bagalkot, Gadag, Koppal)
- **Zone Z4 (S029–S034):** Central Dry Zone (Chitradurga, Davanagere, Ballari, Tumakuru)
- **Zone Z5 (S035–S040):** Eastern Dry Zone (Bengaluru, Kolar, Chikkaballapur, Ramanagara)
- **Zone Z6 (S041–S046):** Southern Dry Zone (Mandya, Mysuru, Chamarajanagar, Tumakuru South)
- **Zone Z7 (S047–S052):** Southern Transition Zone (Hassan, Shivamogga, Chikkamagaluru Plains)
- **Zone Z8 (S053–S058):** Northern Transition Zone (Dharwad, Belagavi, Haveri)
- **Zone Z9 (S059–S064):** Hilly Zone (Kodagu, Chikkamagaluru Ghats, Uttara Kannada Ghats)
- **Zone Z10 (S065–S070):** Coastal Zone (Dakshina Kannada, Udupi, Uttara Kannada Coast)

As authorized, the next milestone is a comprehensive full-benchmark integrity review before clinical annotation and evaluation—not immediate model training.
