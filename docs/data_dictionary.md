# Data Dictionary & Formal Schema Specifications

## Status: Complete & Verified Across All 10 Agro-Climatic Zones

This document defines the comprehensive data schemas used across the **farmer-benefit-ml** recommendation pipeline, covering farmer profiles, scheme master databases, eligibility statuses, availability partitions, and machine learning feature representations.

---

## 1. Farmer Profile Schema (`FarmerProfile`)

Represents the input state characterizing a farmer scenario, defined in `src/eligibility/models.py`:

| Attribute Name | Data Type | Permitted / Expected Values | Description |
|---|---|---|---|
| `scenario_id` | String | e.g. `S001`, `S131` | Unique scenario identifier across benchmarks |
| `zone` | String | `Z1` to `Z10` | One of Karnataka's 10 Agro-Climatic Zones |
| `district` | String | e.g. `Raichur`, `Tumkur`, `Bidar` | District of cultivation in Karnataka |
| `taluk_block` | String | e.g. `Manvi`, `Madhugiri` | Administrative sub-district / Taluk |
| `land_size_acres` | Float | $\ge 0.0$ | Operational agricultural land area in acres |
| `farmer_category` | Enum | `MARGINAL` ($<2.5$ ac), `SMALL` ($2.5-5.0$ ac), `MEDIUM` ($5-10$ ac), `LARGE` ($>10$ ac) | Statutory landholding classification |
| `social_category` | Enum | `GENERAL`, `OBC`, `SC`, `ST`, `MINORITY` | Social group (governs caste corporation eligibility) |
| `primary_crop` | String | e.g. `Paddy`, `Cotton`, `Ragi`, `Tomato` | Primary standing or planned crop |
| `crop_category` | Enum | `CEREAL`, `PULSE`, `OILSEED`, `COMMERCIAL`, `HORTICULTURE` | Agronomic crop classification |
| `season` | Enum | `KHARIF`, `RABI`, `SUMMER`, `PERENNIAL` | Cultivation season |
| `irrigation_type` | Enum | `RAINFED`, `BOREWELL`, `CANAL`, `DRIP`, `OPEN_WELL` | Primary source of water |
| `water_source` | String | `None`, `Borewell`, `Canal`, `Pond`, `River` | Physical water asset availability |
| `electricity_status`| Enum | `GRID_CONNECTED`, `OFF_GRID`, `NO_ELECTRICITY` | Energization status of agricultural pumpset |
| `tenancy_status` | Enum | `OWNER`, `TENANT`, `MIXED` | Land tenure status |
| `annual_income` | Float | Numeric $\ge 0.0$ | Gross household annual income |
| `income_tax_payer` | Boolean | `True`, `False` | Mandatory statutory disqualifier for PM-KISAN |
| `stated_needs` | List[String] | e.g. `["IRRIGATION_EQUIPMENT"]`, `["CROP_DAMAGE_RELIEF"]` | Immediate stated operational requirements |

---

## 2. Scheme Master Schema (31 Attributes)

Defined in [`scheme_master.xlsx`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/scheme_database/scheme_master.xlsx), [`scheme_master.json`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/scheme_database/processed/scheme_master.json), and [`scheme_master.csv`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/scheme_database/processed/scheme_master.csv):

| Column # | Column Name | Data Type | Description | Example Value |
|:---:|---|---|---|---|
| 1 | `scheme_id` | String | Unique statutory scheme code | `SCH001`, `SCH010_AMBEDKAR` |
| 2 | `scheme_name` | String | Full official title | `Pradhan Mantri Kisan Samman Nidhi` |
| 3 | `record_type` | Enum | Architecture hierarchy | `STANDALONE`, `PARENT`, `CHILD` |
| 4 | `parent_scheme_id` | String | ID of umbrella scheme (if child) | `SCH010` (or `null`) |
| 5 | `government_level` | Enum | Jurisdictional authority | `CENTRAL`, `STATE`, `CENTRAL_STATE` |
| 6 | `state` | String | Applicable state | `Karnataka` or `All India` |
| 7 | `nodal_department` | String | Administering ministry/dept | `Department of Agriculture, GoK` |
| 8 | `objective_summary` | String | Official purpose | Income support to landholding farmers |
| 9 | `primary_need_domain` | Enum | Primary operational domain | `DIRECT_INCOME`, `MICRO_IRRIGATION`, `CREDIT` |
| 10 | `eligible_crops` | String | Permitted crops | `All Crops` or `Notified Horticultural Crops` |
| 11 | `eligible_farmer_categories`| String | Land size eligibility | `Small, Marginal` or `All` |
| 12 | `eligible_social_categories`| String | Caste/social eligibility | `SC`, `ST`, `OBC`, or `All` |
| 13 | `min_land_acres` | Float | Minimum landholding cutoff | `0.0` or `1.0` |
| 14 | `max_land_acres` | Float | Maximum landholding cutoff | `5.0` or `None` |
| 15 | `irrigation_criteria` | String | Water/irrigation conditions | `Dryland / Rainfed only` |
| 16 | `electricity_criteria` | String | Power grid requirements | `Must NOT have energized grid connection` |
| 17 | `tenancy_allowed` | Boolean | Whether tenants qualify | `False` (for PM-KISAN), `True` (for KCC) |
| 18 | `income_ceiling` | Float | Maximum annual income cap | `200000.0` (or `None`) |
| 19 | `benefit_type` | Enum | Mechanism of subsidy | `DBT_CASH`, `CAPITAL_SUBSIDY`, `INTEREST_SUBVENTION` |
| 20 | `subsidy_percentage` | Float | Percentage of capital cost | `50.0`, `60.0`, `90.0` |
| 21 | `max_benefit_amount` | Float | Monetary ceiling in INR | `6000.0`, `25000.0` |
| 22 | `eligibility_rules_summary`| String | Full statutory requirements text | Detailed legal rule breakdown |
| 23 | `required_documents` | String | Mandatory documentation checklist| RTC/Pahani, Aadhaar, Caste Cert, Bank Passbook |
| 24 | `application_mode` | Enum | Submission route | `ONLINE`, `OFFLINE`, `HYBRID` |
| 25 | `portal_name` | String | Official portal name | `PM-KISAN Portal`, `Seva Sindhu`, `FRUITS` |
| 26 | `official_source_url` | String | Verification URL | `https://pmkisan.gov.in/` |
| 27 | `verification_date` | String | Date audited against gazette | `2026-10-12` |
| 28 | `verified_by` | String | Auditor identity | `Pair Programmer / Research Team` |
| 29 | `audit_status` | Enum | Evidence level | `VERIFIED`, `PROVISIONAL_PENDING_ANNUAL_GO` |
| 30 | `statutory_lockin_years`| Integer | Repeat application lockout | `3` or `5` years |
| 31 | `remarks` | String | Special conditions / caveats | Budget quota subject to taluk allocation |

---

## 3. Eligibility Engine Output Schema (`EligibilityResult`)

Computed per `(farmer_scenario, scheme)` by `src/eligibility/engine.py`:

| Field | Data Type | Values | Description |
|---|---|---|---|
| `status` | Enum | `ELIGIBLE`, `INELIGIBLE`, `REQUIRES_VERIFICATION` | Three-valued logic result |
| `disqualification_reasons`| List[String] | e.g. `["EXCLUSION_INCOME_TAX_PAYER"]` | Explicit fired statutory rule violation keys |
| `verification_needed` | List[String] | e.g. `["LAND_OWNERSHIP_UNVERIFIED"]` | Missing attributes required for final determination |
| `eligible_child_routes` | List[String] | e.g. `["SCH010_AMBEDKAR"]` | Applicable child implementation routes |

---

## 4. Availability & Governance Output Schema

Computed by `src/availability/`:

| Attribute | Data Type | Values | Description |
|---|---|---|---|
| `availability_status` | Enum | `AVAILABLE_NOW`, `TIMING_PENDING`, `REQUIRES_VERIFICATION`, `CLOSED` | Operational portal status |
| `section_assignment` | Enum | `SECTION_A`, `SECTION_B`, `DISQUALIFIED` | Section A: Actionable, Section B: Provisional |
| `allow_numerical_scoring` | Boolean | `True` (Section A only), `False` (Section B & Disqualified) | Guardrail protecting provisional schemes from ML ranking |

---

## 5. Machine Learning Dataset Schema (Benchmark v1.2)

Formulated for contextual ranking across 90 scenarios ($N=90$, $n=369$ candidate pairs):

| Column Name | Type | Description |
|---|---|---|
| `scenario_id` | String | Group identifier for cross-validation splitting |
| `scheme_id` | String | Target candidate scheme identifier |
| `zone` | Categorical | Agro-climatic zone ($Z_1$ to $Z_{10}$) |
| `relevance_label` | Integer ($0$ to $3$) | Ground-truth relevance rating from domain expert review |
| `is_high_relevance` | Binary ($0$ or $1$) | Binary target for APS classification ($1$ if relevance $\ge 2$, else $0$) |
| `model_score` | Float | Predicted continuous priority score from HistGradientBoostingRanker |
| `predicted_rank` | Integer | Ranked position among actionable Section A schemes ($1, 2, \dots$) |
