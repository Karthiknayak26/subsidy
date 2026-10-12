# Scheme Master Database (10 Core Schemes + 6 Implementation Records)

**Milestone:** Phase 1 — Ground-Truth Scheme Database Curation  
**Scope:** Government of India & Government of Karnataka Agricultural Welfare & Subsidy Schemes  
**Architecture:** Parent-Child Implementation Taxonomy (10 Conceptual Schemes, 6 Implementation Variants)  
**Last Verified:** September 15, 2026 (Audit Updated: October 12, 2026)

---

## 1. Objective & Strategic Selection

Rather than gathering arbitrary policies, these 10 core schemes were selected strategically to cover the complete spectrum of distinct farmer information needs, asset requirements, and agro-climatic circumstances in Karnataka. Following the pre-implementation policy audit, multi-agency schemes (`SCH008` Credit and `SCH010` Ganga Kalyana) are structured with explicit child implementation records.

### Core Scheme Registry (10 Conceptual Schemes)

| Scheme ID | Scheme Name | Record Type | Primary Need / Domain | Implementing Level | Key Benefit Metric |
|---|---|---|---|---|---|
| **SCH001** | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | `STANDALONE` | Direct Income Support | Central | ₹6,000 / year (DBT in 3 installments) |
| **SCH002** | Pradhan Mantri Fasal Bima Yojana (PMFBY) | `STANDALONE` | Crop Insurance & Risk Mitigation | Central-State (50:50) | Capped farmer premium (1.5%–5%), balance govt support |
| **SCH003** | PMKSY - Per Drop More Crop (PDMC) | `STANDALONE` | Micro-Irrigation (Drip / Sprinkler) | Central-State (60:40) | 55% base subsidy (SMF), 45% (Others) up to 5 ha; SC/ST state top-up |
| **SCH004** | Sub-Mission on Agricultural Mechanization (SMAM) | `STANDALONE` | Farm Machinery & Implements | Central-State (60:40) | 50% subsidy (SMF/Women/SC/ST), 40% (Others) with machine caps |
| **SCH005** | Krishi Bhagya Yojana | `STANDALONE` | Rainwater Harvesting / Dryland Package | State (Karnataka) | 90% (SC/ST), 80% (General) for Farm Pond + Lining + Pump |
| **SCH006** | PM-KUSUM Component B | `STANDALONE` | Standalone Solar Agriculture Pumps | Central-State (30:30) | 60% total subsidy for off-grid solar pumps up to 7.5 HP |
| **SCH007** | Mission for Integrated Dev. of Horticulture (MIDH) | `STANDALONE` | Protected Cultivation / Polyhouse | Central-State (60:40) | 50% cost norm subsidy for Polyhouse / Shade Net up to 4,000 m² |
| **SCH008** | Kisan Credit Card (KCC) & Crop Credit | `PARENT` | Concessional Production Credit | Central & State Routes | Umbrella credit category; implemented via 2 child routes below |
| **SCH009** | Soil Health Card Scheme | `STANDALONE` | Scientific Soil Nutrient Advisory | Central-State (60:40) | 100% free 12-parameter soil diagnostic card every 2–3 yrs |
| **SCH010** | Ganga Kalyana Scheme | `PARENT` | Free Borewell & Pump Package | State (Karnataka Corporations) | Umbrella borewell category; implemented via 4 corporation routes below |

### Child Implementation Registry (6 Implementation Records)

| Child ID | Parent ID | Implementation Title | Target Community / Channel | Key Route Rules | Audit Status |
|---|---|---|---|---|---|
| **SCH008_CENTRAL** | `SCH008` | Central KCC-MISS | Commercial Banks / RRBs (All Farmers) | 4% effective interest up to ₹3 Lakh upon prompt repayment | `VERIFIED_HISTORICAL_BASELINE` |
| **SCH008_KA_COOP** | `SCH008` | Karnataka Baddi Rahitha Bele Sala | PACS / DCCBs (Karnataka Coop Members) | 0% interest up to ₹5 Lakh upon prompt repayment | `PROVISIONAL_PENDING_ANNUAL_GO` |
| **SCH010_AMBEDKAR** | `SCH010` | Ganga Kalyana — Dr. B.R. Ambedkar Corp | Scheduled Castes (SC) | Individual (1.0/1.20–5.0 ac); Community (8–15 ac pooled) | `VERIFIED` |
| **SCH010_VALMIKI** | `SCH010` | Ganga Kalyana — Maharshi Valmiki Corp | Scheduled Tribes (ST) | Individual (1.0/1.20–5.0 ac); Community (8–15 ac pooled) | `VERIFIED` |
| **SCH010_DEVARAJ_URS**| `SCH010` | Ganga Kalyana — D. Devaraj Urs Corp | Backward Classes (Cat 1, 2A, 3A, 3B) | Individual (1.0/1.20–5.0 ac); Community (8–15 ac pooled) | `VERIFIED` |
| **SCH010_KMDC** | `SCH010` | Ganga Kalyana — Minorities Corp | Religious Minorities (Muslim, Christian, etc.) | Individual (1.0/1.20–5.0 ac); Community (8–15 ac pooled) | `VERIFIED` |

*Note on Ganga Kalyana Scope:* Additional state corporations in Karnataka also administer Ganga Kalyana variants (e.g. Arya Vysya, Brahmin, Veerashaiva-Lingayat, Maratha, Kadugolla Development Corporations). This benchmark models the four primary corporations and does not imply exhaustive statewide coverage.

---

## 2. Master Schema Definition (31 Attributes)

Each scheme in [`scheme_master.xlsx`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/scheme_database/scheme_master.xlsx) strictly adheres to the 31-column standardized schema:

1. `scheme_id`: Unique identifier (`SCH001` – `SCH010`, plus child records `SCH008_*`, `SCH010_*`)
2. `scheme_name`: Full official scheme title
3. `record_type`: Taxonomy tier (`STANDALONE`, `PARENT`, or `CHILD`)
4. `parent_scheme_id`: Foreign key reference to parent (`SCH008`, `SCH010`, or `None`)
5. `government_level`: Administrative tier (`Central`, `State (Government of Karnataka)`, or `Central-State Co-sponsored`)
6. `department`: Responsible nodal ministry / state department / corporation
7. `benefit_type`: Functional classification of assistance
8. `target_crops`: Crop eligibility scope (Crop-agnostic, notified crops, horticulture, dryland crops)
9. `target_activities`: Sowing, equipment purchase, borewell drilling, pond excavation, etc.
10. `state`: Geographical applicability (`Karnataka` or `All India`)
11. `district_scope`: Specific district coverage (`All 31 districts`, notified GP units, or rainfed taluks)
12. `farmer_categories`: Social and operational categories (`Small & Marginal`, `SC/ST`, `Women`, `All`)
13. `min_land`: Minimum landholding required (distinguishing Individual vs Community routes)
14. `max_land`: Maximum landholding ceiling (distinguishing Individual vs Community routes)
15. `irrigation_requirements`: Condition of water access (`Dryland only`, `Assured water source required`, `None`)
16. `existing_asset_requirements`: Mandatory or excluded prior assets (e.g. must own tractor, must NOT have grid electric pump)
17. `eligible_conditions`: Explicit positive criteria (including statutory ownership cut-off dates like 01.02.2019 for PM-KISAN)
18. `excluded_conditions`: Negative criteria resulting in automatic disqualification (including statutory exceptions like MTS exemption)
19. `benefit_rate`: Percentage or fixed rate of assistance
20. `maximum_benefit`: Monetary or physical ceiling on benefit
21. `benefit_formula`: Mathematical/operational rule used to calculate assistance
22. `upfront_benefit_support`: Guaranteed upfront government subsidy / interest rebate
23. `contingent_benefit_clause`: Risk payout / claim indemnity clause (applicable to PMFBY; non-guaranteed)
24. `claim_disclaimer`: Explicit legal disclaimer (mandatory for insurance to avoid misleading farmers)
25. `application_period`: Baseline operational window (continuous, seasonal deadline, pre-monsoon, tender-based)
26. `application_method`: Portal/department channels (FRUITS, Seva Sindhu, Samrakshane, RSK, Banks)
27. `required_documents`: Compulsory verifications (RTC/Pahani, Aadhaar, Caste RD, Income RD, Bank passbook)
28. `official_source_url`: Official government portal URL
29. `official_document_url`: URL of the official Gazette notification or Operational Guidelines PDF
30. `audit_status`: Official verification standing (`VERIFIED`, `PARENT_CATEGORY`, `VERIFIED_HISTORICAL_BASELINE`, `PROVISIONAL_PENDING_ANNUAL_GO`)
31. `verification_date`: Timestamp of official source verification (`2026-09-15`)

---

## 3. Directory Layout & Deliverables

```
scheme_database/
├── raw/                              <- 16 traceable raw JSON records (10 core + 6 impl)
│   ├── SCH001_PM_KISAN.json
│   ├── SCH002_PMFBY.json
│   ├── SCH003_PMKSY_PDMC.json
│   ├── SCH004_SMAM.json
│   ├── SCH005_Krishi_Bhagya.json
│   ├── SCH006_PM_KUSUM_B.json
│   ├── SCH007_MIDH.json
│   ├── SCH008_KCC_MISS.json
│   ├── SCH008_CENTRAL_KCC_MISS.json
│   ├── SCH008_KA_COOP_Zero_Interest.json
│   ├── SCH009_Soil_Health_Card.json
│   ├── SCH010_Ganga_Kalyana.json
│   ├── SCH010_AMBEDKAR_Ganga_Kalyana.json
│   ├── SCH010_VALMIKI_Ganga_Kalyana.json
│   ├── SCH010_DEVARAJ_URS_Ganga_Kalyana.json
│   └── SCH010_KMDC_Ganga_Kalyana.json
├── processed/                        <- Clean consolidated programmatic formats
│   ├── scheme_master.json            (16 records, complete 31-attribute schema)
│   ├── scheme_master.csv             (16 records, flat tabular dataset)
│   └── scheme_availability_template.csv (Separate dynamic availability tracking layer)
├── scheme_master.xlsx                <- Formatted Master Excel Workbook (Review Deliverable)
├── build_scheme_master.py            <- Reproducible generation script
└── README.md                         <- Schema & architecture documentation
```

---

## 4. Availability Layer Decoupling

In strict compliance with audit safeguards:
- The Scheme Master records **do not contain live availability status flags**.
- Dynamic availability (open/closed dates, seasonal cut-offs, budget quotas) is tracked exclusively in [`scheme_availability_template.csv`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/scheme_database/processed/scheme_availability_template.csv).
- Every recommendation surfaces schemes across four discrete states:
  1. `Verified available now`
  2. `Eligible, but currently closed`
  3. `Upcoming, with an officially confirmed date`
  4. `Availability unknown — confirmation required`
