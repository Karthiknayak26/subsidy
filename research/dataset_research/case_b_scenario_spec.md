# Case B — Expert-Annotated Scenario Benchmark: Design Specification

**Document Type:** Research Dataset Design Specification  
**Milestone:** Phase 1 → Phase 2 — Benchmark Construction  
**Status:** Draft for Guide Review (Do Not Generate Scenarios Until Approved)  
**Last Updated:** October 11, 2026

---

## 1. Purpose

The purpose of Case B is to provide **human-expert relevance ground truth** for the ML Relevance Ranking component of this project.

Phase 0 established that no credible public, individual-level farmer-to-multi-scheme outcome dataset exists in India. Specifically:

- **PM-KISAN** public data exposes only village-level and gender-wise beneficiary counts.
- **PMFBY** public data exposes only state/crop aggregate enrollment statistics.
- **FRUITS Karnataka** is an administrative system protected by privacy obligations.
- **KCC Karnataka (Dec 2024)** contains farmer query intent categories but no scheme enrollment or ranking outcomes.
- **NSS 77th Round (Schedule 33.1)** contains rich farmer profiles but labels only three schemes (KCC, PMFBY, Soil Health Card), which is an insufficient scheme space for a multi-scheme recommendation system and records historical administrative uptake rather than ideal relevance judgments.

**Case A is therefore definitively closed.**

Case B does not substitute fabricated or synthetic data for real ground truth. Instead, it constructs a **Human-in-the-Loop Evaluation Benchmark** by:

1. Defining realistic farmer scenarios grounded in empirical distributions from the NSS 77th Round and KCC Call Centre data.
2. Running each scenario through a deterministic eligibility engine derived from the verified 10-scheme master.
3. Presenting each scenario and its eligible candidate schemes to qualified agricultural domain experts.
4. Recording independent expert relevance judgments (on a 0–3 ordinal scale) as the training and evaluation ground truth.

This methodology is consistent with established practices in information retrieval and recommender system research (e.g., TREC relevance pools, LETOR benchmark construction), adapted to the agricultural welfare domain.

---

## 2. Research Question

The core research question that the Case B benchmark is designed to evaluate is:

> **"Given a realistic farmer profile and a set of schemes that pass deterministic eligibility rules, which schemes are most relevant to the farmer's current situation?"**

This question is deliberately split into two stages:

- **Stage 1 — Eligibility (Deterministic):** Which schemes does this farmer statutorily qualify for?
- **Stage 2 — Relevance Ranking (ML + Expert-Annotated):** Among the eligible schemes, how should they be ranked by immediate practical usefulness to this specific farmer?

The benchmark provides human-expert relevance labels for Stage 2. The expert annotation task is therefore **not about determining legal eligibility** — that is handled by the rule engine in Stage 1.

---

## 3. Scenario Schema

Each scenario record describes a single anonymous farmer at a specific point in time, with sufficient detail to:
1. Determine statutory eligibility against each scheme using the deterministic rule engine.
2. Handle incomplete or unknown information transparently without silent assumptions.
3. Assess the relevance of eligible schemes to that farmer's current situation.

### 3.1 Schema Table

| Field | Data Type | Status | Allowed Values / Range | Statutory / Domain Justification |
|---|---|---|---|---|
| `scenario_id` | String | **Required** | `S001` – `S100` (format: `S` + zero-padded integer) | Internal tracking identifier |
| `agro_climatic_zone` | String (Enum) | **Required** | `Northern Dry Zone`, `Central Dry Zone`, `Southern Dry Zone`, `Southern Transition Zone`, `Eastern Dry Zone`, `Hilly Zone (Malnad)`, `Coastal Zone` | Karnataka Dept. of Agriculture classification; determines climatic context (e.g., Krishi Bhagya restricted to rainfed dryland zones) |
| `district` | String (Enum) | **Required** | Any of Karnataka's 31 districts (e.g., `Raichur`, `Haveri`, `Udupi`, `Tumakuru`, `Dharwad`, `Mysuru`) | NSS 77th Round district codes (State Code 29); representative distribution across all zones |
| `crop_primary` | String (Enum) | **Required** | `Paddy`, `Maize`, `Ragi`, `Jowar`, `Groundnut`, `Redgram`, `Cotton`, `Sugarcane`, `Arecanut`, `Coconut`, `Banana`, `Mango`, `Tomato`, `Onion`, `Chilli`, `Turmeric`, `Sunflower`, `Soybean` | NSS 77th Round Block 6 crop codes; KCC query distribution |
| `crop_secondary` | String (Enum) | Optional | Same list as `crop_primary`, or `None` | Intercropping patterns from NSS 77th Round |
| `land_size_acres` | Float | **Required** | `0.5` to `20.0` (continuous, recorded in acres) | NSS 77th Round Block 5 operational holding size. Inspected by scheme-specific numeric bounds |
| `land_type` | String (Enum) | **Required** | `Dryland (Rainfed)`, `Irrigated (Canal)`, `Irrigated (Borewell)`, `Irrigated (Open Well)`, `Mixed (Partial Irrigation)` | Directly gates Krishi Bhagya (dryland required), Ganga Kalyana (dryland required), PMKSY (water source required), MIDH (irrigation mandatory) |
| `social_category` | String (Enum) | **Required** | `General (OC)`, `OBC (2A)`, `OBC (2B)`, `OBC (3A)`, `OBC (3B)`, `SC`, `ST`, `Minority (Muslim)`, `Minority (Christian)` | Gates Ganga Kalyana corporation children, and activates SC/ST subsidy tiers in SMAM, Krishi Bhagya, and PMKSY |
| `farmer_category` | String (Enum) | **Required** | `Marginal (< 2.5 acres)`, `Small (2.5–5 acres)`, `Medium (5–12.5 acres)`, `Large (> 12.5 acres)` | Demographic classification; evaluated alongside numeric landholding |
| `existing_assets` | List[String] | **Required** | One or more of: `Borewell (Non-energized)`, `Borewell (Grid-connected)`, `Open Well`, `Farm Pond (Existing/Funded)`, `Drip Irrigation (Installed)`, `Sprinkler (Installed)`, `Diesel Pump Set`, `Electric Pump Set`, `Solar Pump`, `Tractor (Owned)`, `Power Tiller`, `None` | Gates equipment subsidies (SMAM tractor requirement, PM-KUSUM unenergized water source requirement, PMKSY water source requirement) |
| `annual_family_income_lakh` | Float | **Required** | `0.5` – `12.0` (in Rs. Lakh) | Evaluated against corporation-specific income limits (e.g. Ganga Kalyana) |
| `immediate_need` | String (Enum) | **Required** | `CROP_INSURANCE`, `MICRO_IRRIGATION_SUPPORT`, `FARM_MECHANIZATION`, `RAINWATER_HARVESTING`, `SOLAR_PUMP_INSTALLATION`, `PROTECTED_HORTICULTURE`, `PRODUCTION_CREDIT`, `SOIL_NUTRIENT_ADVISORY`, `BOREWELL_IRRIGATION`, `INCOME_SUPPORT` | Derived from KCC 44 QueryType taxonomy |
| `paid_income_tax_last_assessment_year` | Boolean / String | **Required** | `True`, `False`, `UNKNOWN` | **Statutory PM-KISAN Exclusion:** Explicitly reflects whether any member of the scheme-defined family paid income tax in the last assessment year. Merely filing an ITR without tax liability does not trigger exclusion. Never inferred from gross agricultural income |
| `govt_employee_category` | String (Enum) | **Required** | `NONE`, `MTS_CLASS_IV_GROUP_D`, `OFFICER_REGULAR`, `CONSTITUTIONAL_POST`, `UNKNOWN` | **Statutory Public Service Exclusion:** Distinguishes disqualifying government posts from statutory exemptions. Multi-Tasking Staff (MTS), Class IV, and Group D employees are explicitly **EXEMPT** from exclusion |
| `superannuated_pensioner_monthly_amount` | Float / String | Optional | Numeric (e.g., `0.0`, `12500.0`) or `UNKNOWN` | **Statutory Pension Exclusion:** Pensioners with monthly pension ≥ Rs. 10,000 are excluded from PM-KISAN, **EXCEPT** MTS / Class IV / Group D pensioners |
| `registered_professional` | String (Enum) | Optional | `NONE`, `DOCTOR`, `ENGINEER`, `LAWYER`, `CA`, `ARCHITECT`, `UNKNOWN` | Statutory professional practice exclusion under PM-KISAN |
| `land_ownership_cutoff_pre_feb_2019` | Boolean / String | **Required** | `True`, `False`, `UNKNOWN` | **PM-KISAN Ownership Cut-Off:** Land title recorded on or before 01.02.2019 (or acquired via inheritance/succession). Purchases after this date are excluded |
| `is_pure_tenant_without_land_title` | Boolean | **Required** | `True`, `False` | Disqualifies pure tenant farmers from PM-KISAN, while permitting them for PMFBY and KCC-MISS |
| `borewell_electric_status` | String (Enum) | **Required** | `NONE`, `UNENERGIZED_OFF_GRID`, `GRID_CONNECTED_IP_SET`, `UNKNOWN` | **PM-KUSUM B Exclusion:** Off-grid standalone pumps strictly require un-energized borewells. Grid-connected borewells are disqualified for Component B |
| `prior_micro_irrigation_subsidy_years_ago` | Float / String | Optional | Numeric years (e.g., `3.0`, `8.0`, `None`) or `UNKNOWN` | **PMKSY 7-Year Lock-In:** Disqualifies if subsidy availed for the same parcel within past 7 years |
| `prior_farm_pond_subsidy_years_ago` | Float / String | Optional | Numeric years (e.g., `2.0`, `6.0`, `None`) or `UNKNOWN` | **Krishi Bhagya 5-Year Lock-In:** Disqualifies if farm pond subsidy received within past 5 years |
| `prior_machinery_subsidy_years_ago` | Float / String | Optional | Numeric years (e.g., `3.0`, `6.0`, `None`) or `UNKNOWN` | **SMAM 5-Year Lock-In:** Disqualifies for the same machinery type within past 5 years |
| `prior_ganga_kalyana_in_family` | Boolean / String | **Required** | `True`, `False`, `UNKNOWN` | Disqualifies household if any member previously received Ganga Kalyana borewell assistance |
| `community_pool_acres` | Float | Optional | `0.0` or `8.0` to `15.0` | **Ganga Kalyana Community Route:** Pooled contiguous acreage for groups of 2+ small/marginal farmers (Samooha Kola Bavi) |
| `farming_stage` | String (Enum) | Optional | `Pre-sowing`, `Sowing`, `Mid-season`, `Pre-harvest`, `Post-harvest`, `Fallow` | Optional seasonal stage |
| `season` | String (Enum) | Optional | `Kharif`, `Rabi`, `Summer`, `Annual` | Determines PMFBY premium tier |
| `kcc_query_text_example` | String | Optional | Free text (Kannada or English) | Illustrative real farmer language from KCC dataset |

### 3.2 Definition of Scheme-Defined Family Boundary
In accordance with official government guidelines (Section 2 of PM-KISAN guidelines and corporation operational rules), the **Farmer Family** is strictly defined as:
$$\text{Farmer Family} = \{\text{Farmer, Spouse, Minor Children}\}$$
- Statutory exclusions (e.g., income tax payment, government employment, prior scheme benefits) apply **exclusively to members of this defined family unit**.
- Adult married children with separate households, adult independent siblings, or extended relatives living in the same ancestral house do **not** automatically disqualify the applicant unless their names are co-registered on the specific land RTC/Pahani.

### 3.3 Three-Valued Logic for Incomplete or Unknown Information
To ensure trust and prevent false promises, the eligibility engine implements **Three-Valued Logic** (`ELIGIBLE`, `INELIGIBLE`, `REQUIRES_VERIFICATION`):
- If a statutory exclusion attribute is marked `UNKNOWN` (or `None`), the engine **MUST NOT silently treat it as False** (i.e., assuming the applicant is clean).
- Instead, the scheme disposition is set to **`REQUIRES_VERIFICATION`**, accompanied by an explicit prompt detailing the exact missing document (e.g., *"Requires verification of Form 16 / ITR assessment order"* or *"Requires ESCOM non-energization certificate"*).

---

## 4. Data Grounding & Feasibility

Each scenario field is categorized by its empirical feasibility:

### 4.1 Empirically Sampled from Public Microdata
The following fields are grounded directly in the distributions from **NSS 77th Round (Schedule 33.1 SAS, Karnataka subset)** and the **KCC Karnataka Dataset (Dec 2024)**:
- `district` (NSS Block 1 / KCC District)
- `land_size_acres` (NSS Block 5 operational holding distribution)
- `land_type` (NSS Block 5 irrigation distribution)
- `social_category` (NSS Block 3 social group distribution)
- `farmer_category` (Derived from NSS land size)
- `crop_primary` & `crop_secondary` (NSS Block 6 / KCC Crop column)
- `immediate_need` (KCC 44 QueryType taxonomy)
- `annual_family_income_lakh` (NSS Block 4 calibration range)

### 4.2 Explicitly Constructed Statutory Operational Flags
The audit confirmed that **public surveys do not collect statutory welfare exclusion criteria**. The following fields cannot be extracted from NSS or KCC and are **explicitly constructed** in benchmark scenarios to rigorously test the eligibility engine:
- `paid_income_tax_last_assessment_year`: NSS does not record ITR filing or tax payments. (The prior "income > 10 Lakh" proxy is formally abolished).
- `govt_employee_category`: NSS occupation codes do not distinguish MTS/Class IV exemptions from regular officers.
- `land_ownership_cutoff_pre_feb_2019`: Administrative land registration timestamp.
- `borewell_electric_status`: NSS tracks tubewell ownership but not ESCOM grid-energization status.
### 4.3 Mapping Scenario Fields to Scheme Family Rules

| Scheme / Family | Primary Driving Scenario Fields | Key Statutory / Boundary Rules Evaluated |
|---|---|---|
| **SCH001 (PM-KISAN)** | `paid_income_tax_last_assessment_year`, `govt_employee_category`, `land_ownership_cutoff_pre_feb_2019`, `is_pure_tenant_without_land_title`, `land_size_acres` | • Excluded if `paid_income_tax == True`.<br>• Excluded if `govt_employee_category` in {`OFFICER_REGULAR`, `CONSTITUTIONAL_POST`} (MTS exempt).<br>• Excluded if acquired after 01.02.2019 without inheritance.<br>• Excluded if pure tenant without land title.<br>• Requires `land_size_acres > 0`. |
| **SCH002 (PMFBY)** | `crop_primary`, `land_type`, `season` | • Requires notified crop in notified insurance unit.<br>• Covers both irrigated and rainfed holdings. |
| **SCH003 (PMKSY-PDMC)** | `land_size_acres`, `existing_assets`, `prior_micro_irrigation_subsidy_years_ago` | • Requires `land_size_acres` between 0.2 ha (0.5 ac) and 5.0 ha (12.35 ac).<br>• Requires operational water source.<br>• Excluded if prior subsidy received within 7 years. |
| **SCH004 (SMAM)** | `existing_assets`, `social_category`, `prior_machinery_subsidy_years_ago` | • Requires registered tractor for tractor-drawn implements.<br>• 5-year lock-in for identical machinery type. |
| **SCH005 (Krishi Bhagya)** | `land_type`, `district`, `land_size_acres`, `existing_assets`, `prior_farm_pond_subsidy_years_ago` | • Requires `land_type == "Dryland (Rainfed)"`.<br>• District must be in designated rainfed taluks.<br>• Requires `land_size_acres >= 1.0` and `<= 5.0 ha` (12.35 ac).<br>• Excluded if existing funded pond or subsidy within 5 years. |
| **SCH006 (PM-KUSUM B)** | `existing_assets`, `borewell_electric_status`, `land_size_acres` | • Requires existing un-energized water source.<br>• **Strictly excluded if `borewell_electric_status == GRID_CONNECTED_IP_SET`**.<br>• Does NOT fund borewell drilling. |
| **SCH007 (MIDH)** | `crop_primary`, `land_size_acres`, `existing_assets`, `land_type` | • Requires horticulture crop.<br>• Protected structure area: 1,000 to 4,000 m² (0.25 to 1.0 acre).<br>• Requires assured irrigation + micro-irrigation installed. |
| **SCH008 (KCC Credit)** | `is_pure_tenant_without_land_title`, `land_size_acres` | • Open to both owner cultivators and recorded tenants.<br>• Child `SCH008_CENTRAL` (4%) vs `SCH008_KA_COOP` (0% provisional). |
| **SCH009 (Soil Health)** | `land_size_acres` | • Universal access for operational agricultural holdings (`land_size_acres > 0`). |
| **SCH010 (Ganga Kalyana)** | `social_category`, `land_type`, `land_size_acres`, `existing_assets`, `annual_family_income_lakh`, `prior_ganga_kalyana_in_family`, `community_pool_acres` | • Excluded if `social_category == General (OC)`.<br>• Must be 100% dryland (`kushki`) with no existing borewell/pump.<br>• Individual Route: 1.0/1.20 to 5.0 acres.<br>• Community Route: 8.0 to 15.0 acres pooled by 2+ farmers.<br>• Child routing: Ambedkar (SC), Valmiki (ST), Devaraj Urs (OBC), KMDC (Minorities). |


## 5. Scenario Design Principles

Scenarios are constructed to form a realistic, diverse, and analytically useful benchmark. The following principles govern scenario construction:

### 5.1 Realism Constraints

- All scenario combinations must be **agronomically plausible** in Karnataka.
  - Example valid: Arecanut farmer in Udupi district, Coastal Zone, 3.0 acres, borewell irrigation.
  - Example invalid: Cotton farmer in Coastal Zone (cotton is a Northern/Central dry zone crop in Karnataka).
- Land type must be consistent with the crop.
  - Example: Paddy cultivation requires irrigation; a paddy farmer with `land_type = Dryland (Rainfed)` with no water source is plausible only in limited monsoon-dependent scenarios (Bhadra command area tail-end).

### 5.2 Coverage Principles

The benchmark must cover:

- **All 7 agro-climatic zones** of Karnataka (at least 1–2 scenarios per zone).
- **At least 8 distinct crops** from the 18-crop list, including both food crops and horticulture crops.
- **All land size tiers**: Marginal (< 2.5 acres), Small (2.5–5 acres), Medium (5–12.5 acres), Large (> 12.5 acres).
- **All social categories** used in scheme differentiation: General, OBC, SC, ST, Minority.
- **All irrigation types**: Dryland (rainfed), Borewell (non-energized), Borewell (grid-connected), Open Well, Canal, Mixed.
- **All 10 immediate need categories** (one per scheme domain), so that every scheme in the master is evaluated at least once in a context where it is highly relevant.
- **Both positive and negative eligibility cases**: For each scheme, at least one scenario where the farmer does NOT qualify must be included (to test that the eligibility engine correctly filters exclusions — e.g., a Ganga Kalyana scenario where `social_category = General (OC)`, which makes the farmer ineligible, testing the system's exclusion logic).
- **No scheme should dominate**: No single scheme should appear as the top-1 expert-annotated scheme in more than 20% of scenarios.
- **No single district, crop, or agro-climatic zone** should represent more than 20% of scenarios.

### 5.3 Realism Without Fabrication

- All farmer-profile value ranges are drawn from NSS 77th Round Karnataka distributions or from scheme eligibility thresholds.
- No field value is invented beyond what these two sources support.
- Scenario combinations that violate known agronomic or geographic reality are excluded.

---

## 6. Coverage Matrix

The final 50–100 scenario set will be balanced against the following matrix dimensions. **Exact cell counts will be determined after consulting NSS 77th Round distributions; this matrix defines the dimensions to balance — not the specific numbers.**

```
Primary Matrix Dimensions:
   Rows → Agro-climatic zone (7 zones)
   Columns → Immediate Need Category (10 needs)

Secondary Balancing Dimensions (within cells):
   ▸ Crop type (≥ 8 distinct crops across full set)
   ▸ Land size tier (Marginal / Small / Medium / Large)
   ▸ Social category (General / OBC / SC / ST / Minority)
   ▸ Irrigation / land type (Rainfed / Borewell / Canal / Mixed)
```

**Coverage Matrix Skeleton (Agro-Climatic Zone × Immediate Need):**

|  | CROP_INSURANCE | MICRO_IRRIGATION | MECHANIZATION | RAINWATER_HARVESTING | SOLAR_PUMP | PROTECTED_HORT. | CREDIT | SOIL_ADVISORY | BOREWELL_IRRIGATION | INCOME_SUPPORT |
|---|---|---|---|---|---|---|---|---|---|---|
| **Northern Dry Zone** | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ |
| **Central Dry Zone** | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ |
| **Southern Dry Zone** | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Southern Transition Zone** | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| **Eastern Dry Zone** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Hilly Zone (Malnad)** | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| **Coastal Zone** | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | ✓ | — | ✓ |

`✓` = Agronomically feasible cell; `—` = Not agronomically typical (e.g., Rainwater Harvesting / Krishi Bhagya is not applicable in Coastal Zone which receives 3000+ mm rainfall without dryland scarcity).

This matrix will be populated with actual scenario counts only after NSS 77th Round Karnataka district/crop/land distributions are extracted and reviewed.

---

## 7. Pilot Set

### 7.1 Rationale for a Pilot

Before constructing the full 50–100 scenario benchmark, a **pilot set of 10 scenarios** will be created and reviewed for the following reasons:

1. **Schema validation:** Confirm that the 13 required fields are sufficient to run the deterministic eligibility engine without ambiguity.
2. **Annotation task validation:** Confirm that the relevance annotation question is clearly understood by expert annotators, using the pilot as a calibration set during expert briefing.
3. **Inter-annotator feasibility:** A quick preliminary assessment of annotator agreement on 10 scenarios can identify annotation guideline gaps before they propagate across 100 scenarios.
4. **Guide review gate:** Per project protocol, the pilot set will be reviewed by the project guide before the full 50–100 scenarios are constructed. This is the **current next step**.

### 7.2 Pilot Set Design & Scenario Profiles (S001–S010)

In accordance with project guide decisions, exactly **four of the 10 pilot scenarios (S007–S010) are allocated for strict negative exclusion and boundary testing**, while six scenarios (S001–S006) represent diverse positive cases across agro-climatic zones and need categories:

#### Part A: Positive Diverse Scenarios (S001–S006)
- **S001 (Northern Dry Zone, Raichur):** Cotton & Redgram, 3.0 acres, SC category, `Dryland (Rainfed)`. Assets: `None`. Income: ₹1.2L. Immediate Need: `CROP_INSURANCE`. All statutory exclusions clean (`paid_income_tax = False`, `govt_employee = NONE`, owned pre-2019). Positive match for PMFBY, PM-KISAN, KCC-MISS, Soil Health Card.
- **S002 (Central Dry Zone, Haveri):** Maize, 2.0 acres, OBC (2A), `Dryland (Rainfed)` with an existing un-energized borewell (`borewell_electric_status = UNENERGIZED_OFF_GRID`). Assets: `Borewell (Non-energized)`. Income: ₹1.5L. Immediate Need: `SOLAR_PUMP_INSTALLATION`. Positive match for PM-KUSUM Component B, PM-KISAN, Soil Health Card.
- **S003 (Southern Dry Zone, Tumakuru):** Ragi, 1.5 acres, General category, `Dryland (Rainfed)`. Assets: `None`. Income: ₹1.8L. Immediate Need: `RAINWATER_HARVESTING`. Positive match for Krishi Bhagya (dryland taluk, catchment ≥ 1.0 ac), PM-KISAN, Soil Health Card.
- **S004 (Southern Transition Zone, Dharwad):** Soybean & Maize, 4.0 acres, OBC (3B), `Irrigated (Borewell)`. Assets: `Borewell (Grid-connected)`, `Electric Pump Set`. Income: ₹2.5L. Immediate Need: `MICRO_IRRIGATION_SUPPORT`. Positive match for PMKSY-PDMC (water source present, 7-year clean), PM-KISAN, Soil Health Card.
- **S005 (Eastern Dry Zone, Kolar):** Tomato & Capsicum, 1.0 acre (4,000 m²), OBC (3A), `Irrigated (Borewell)`. Assets: `Borewell (Grid-connected)`, `Drip Irrigation (Installed)`. Income: ₹3.0L. Immediate Need: `PROTECTED_HORTICULTURE`. Positive match for MIDH Polyhouse/Shade Net (meets 1,000–4,000 m² norm with micro-irrigation), PM-KISAN, Soil Health Card.
- **S006 (Southern Dry Zone, Mysuru):** Paddy, 2.5 acres, General category, `Irrigated (Canal)`. Assets: `None`. Income: ₹2.0L. Immediate Need: `PRODUCTION_CREDIT`. Positive match for Central KCC-MISS (Commercial Bank) and Soil Health Card.

#### Part B: Strict Negative Exclusion & Boundary Test Scenarios (S007–S010)
- **S007 [PM-KISAN Statutory Exclusion Test]:**
  - Profile: Haveri, Maize, 3.0 acres, General category, `Dryland (Rainfed)`. Immediate Need: `INCOME_SUPPORT`.
  - Disqualifying Flag: Spouse in the scheme-defined family paid income tax in the last assessment year (`paid_income_tax_last_assessment_year = True`).
  - Expected Engine Output: **PM-KISAN (SCH001) → `INELIGIBLE`** (statutory tax exclusion triggered). Other non-excluded schemes (Soil Health, PMFBY) remain eligible.
- **S008 [PM-KUSUM Component B Off-Grid Exclusion Test]:**
  - Profile: Vijayapura, Jowar, 4.0 acres, OBC (2A), `Dryland (Rainfed)` seeking solar pumping. Immediate Need: `SOLAR_PUMP_INSTALLATION`.
  - Disqualifying Flag: Applicant's existing borewell already possesses an energized electric grid connection (`borewell_electric_status = GRID_CONNECTED_IP_SET`).
  - Expected Engine Output: **PM-KUSUM Component B (SCH006) → `INELIGIBLE`** (grid-connected borewells are disqualified under Component B rules; presented as a *related option to verify: PM-KUSUM Component C*, not an automatic recommendation).
- **S009 [Ganga Kalyana Caste & Corporation Mandate Exclusion Test]:**
  - Profile: Chitradurga, Groundnut, 2.0 acres dryland (`kushki`), no existing borewell, seeking borewell drilling. Immediate Need: `BOREWELL_IRRIGATION`.
  - Disqualifying Flag: Applicant belongs to General Merit category (`social_category = General (OC)`).
  - Expected Engine Output: **Ganga Kalyana (SCH010 and all 4 child records) → `INELIGIBLE`** (Ineligible for all four Ganga Kalyana implementation records currently represented in the registry because applicant does not meet covered corporation-category requirements; does not establish ineligibility for every Ganga Kalyana-related programme in Karnataka).
- **S010 [PMKSY-PDMC & Lock-In Boundary Exclusion Test]:**
  - Profile: Belagavi, Sugarcane, 3.0 acres, SC category, `Irrigated (Borewell)` seeking drip irrigation subsidy. Immediate Need: `MICRO_IRRIGATION_SUPPORT`.
  - Disqualifying Flag: Applicant received micro-irrigation subsidy for the same parcel 3 years ago (`prior_micro_irrigation_subsidy_years_ago = 3.0`).
  - Expected Engine Output: **PMKSY-PDMC (SCH003) → `INELIGIBLE`** (violates statutory 7-year lock-in period).


---

## 8. Candidate Scheme Generation Pipeline

The workflow from farmer scenario to annotatable scheme list is:

```
FARMER SCENARIO (structured profile)
           │
           ▼
┌─────────────────────────────────────────┐
│  Stage 1: Deterministic Eligibility     │
│  Engine (Rule-based Python functions)   │
│                                         │
│  For each of 10 schemes in master:      │
│  eligible_conditions.evaluate(scenario) │
│  excluded_conditions.evaluate(scenario) │
│                                         │
│  → Boolean: Eligible (1) / Ineligible (0)│
└─────────────────────────────────────────┘
           │
           ▼
  ELIGIBLE CANDIDATE SCHEMES
  (subset of 10, determined purely by
  official scheme criteria — no ML)
           │
           ▼
┌─────────────────────────────────────────┐
│  Stage 2: Expert Annotation Task        │
│  Present:                               │
│   - Full farmer scenario profile        │
│   - Each eligible scheme (name,         │
│     benefit type, brief description)    │
│                                         │
│  Expert assigns relevance score 0–3     │
│  for each eligible scheme independently │
└─────────────────────────────────────────┘
           │
           ▼
  EXPERT RELEVANCE LABELS
  (farmer_id, scheme_id, annotator_id, score)
```

**Critical design constraint:** Experts annotate only the schemes determined eligible by the rule engine. They do **not** determine statutory eligibility — that responsibility belongs entirely to the deterministic engine, which is derived from verified official scheme criteria. Experts are explicitly told: *"These schemes have already been determined eligible for this farmer. Your task is to judge how relevant each scheme is to this farmer's current situation."*

---

## 9. Expert Annotation Task

### 9.1 The Annotation Question

For each (scenario, eligible scheme) pair, each expert is asked:

> **"How relevant is this eligible scheme to this farmer's current situation?"**

This question is answered on the following ordinal scale:

| Score | Label | Definition |
|---|---|---|
| **3** | **Highly Relevant / High Priority** | This scheme directly addresses the farmer's primary stated need. The farmer would receive immediate and substantial practical benefit. This should be among the first schemes recommended. |
| **2** | **Relevant / Secondary Priority** | This scheme provides genuine benefit to this farmer, but it is not the most direct match for the immediate need. The farmer would benefit, but it may not be the top priority given the current situation. |
| **1** | **Marginally Relevant / Low Priority** | This scheme is technically applicable but provides limited practical value in the current context. The farmer might benefit eventually, but it is not urgent or well-matched to the stated need. |
| **0** | **Irrelevant / Not Useful** | Despite passing the eligibility filter, this scheme provides no practical benefit in the current context of this farmer's situation, crop, assets, or stated need. |

### 9.2 Score 0 Boundary Clarification

Score **0 (Irrelevant)** is possible even for an eligible scheme. This handles cases where:
- The eligibility engine may pass broad eligibility criteria (e.g., PM-KISAN is eligible for nearly all farmers), but the scheme provides no targeted value to the farmer's immediate and specific situation (e.g., if the farmer's urgent need is crop insurance after a reported pest outbreak, PM-KISAN income support is eligible but irrelevant to the immediate problem).
- Experts must use 0 to indicate "this scheme should not appear in the top recommendation list for this farmer."

---

## 10. Annotation Guidelines

Experts will receive a written briefing document before annotation. The following factors should guide each relevance score:

### What to Consider (Score Higher):
- **Directness of match to the farmer's immediate need:** A score of 3 requires that the scheme directly addresses the primary stated need (e.g., PMKSY-PDMC scores 3 for a farmer whose immediate need is MICRO_IRRIGATION_SUPPORT and who has a borewell but no drip system).
- **Expected practical usefulness:** Will this farmer realistically be able to use this scheme given their assets, land type, and location?
- **Scale fit:** Is the subsidy amount or benefit level meaningful relative to the farmer's land size? (e.g., a 3-acre farmer would see greater proportional benefit from Krishi Bhagya than a 15-acre large farmer).
- **Urgency:** Does the farmer's situation suggest time-sensitive need (e.g., PMFBY is highly relevant for a farmer in a seasonal sowing window with a pending insurance deadline)?
- **Existing infrastructure alignment:** If the scheme requires a water source and the farmer already has a borewell, that is a positive match factor.
- **Relative priority among eligible schemes:** When multiple schemes are eligible, use the relative scoring to rank them — not all eligible schemes can score 3.

### What NOT to Do:
- **Do not re-evaluate statutory eligibility.** The eligibility engine has already determined the farmer qualifies. Do not use the annotation to override or second-guess those rules.
- **Do not score based on awareness or administrative convenience.** Score on the basis of practical relevance to the farmer's situation, not on whether the scheme is easy to apply for.
- **Do not assign all schemes the same score.** Scores must discriminate between more and less relevant options.
- **Do not coordinate with other annotators** before submitting your scores. Annotation is independent.

---

## 11. Multi-Annotator Design

### 11.1 Number of Annotators

The benchmark will use **2 to 3 independent expert annotators**.

At minimum 2 annotators are required for inter-rater agreement calculation. A third annotator is strongly preferred to allow majority-vote tie-breaking and more reliable agreement statistics.

### 11.2 Annotator Qualifications

Target annotators will be recruited from one or more of the following categories:
- Agricultural Extension Officers with ≥ 5 years of experience in Karnataka's Department of Agriculture.
- Scientists at Krishi Vigyan Kendras (KVKs) in Karnataka with experience in farmer advisory.
- Faculty at University of Agricultural Sciences (UAS), Bangalore / Raichur / Dharwad with expertise in agronomy or agricultural economics.
- Agricultural Development Officers (ADOs) at Karnataka Raitha Samparka Kendras (RSKs).

### 11.3 Independence Protocol

- Each annotator receives the annotation form independently.
- Annotators must **not** view each other's scores before final submission.
- The annotation interface (whether physical form or digital spreadsheet) will be structured so that the annotator's column is the only scoring column visible during annotation.
- Annotators will complete a single round of annotation before a review meeting where disagreements are discussed (but not changed retroactively — the original independent scores are preserved as the research record).

---

## 12. Agreement Metrics

After collecting independent relevance scores from 2–3 annotators, inter-rater reliability will be quantified before the expert labels are aggregated into benchmark ground truth.

The appropriate agreement statistic will be selected based on the annotation structure:

### Candidate Metrics

| Annotation Design | Primary Agreement Metric | Conditions for Selection & Methodological Rationale |
|---|---|---|
| **Two experts assigning ordinal scores (0–3)** | **Weighted Cohen's Kappa ($\kappa_w$)** | Pairwise annotation with ordinal differences penalized quadratically ($\kappa_{w, \text{quadratic}}$) or linearly. |
| **Three or more experts assigning ordinal scores (with potential missing ratings)** | **Krippendorff's Alpha ($\alpha$) with Ordinal Metric** | Standard metric for multi-annotator ordinal ratings and missing data, applying metric difference $\delta^2(c, k)$ to preserve scale spacing. |
| **Experts explicitly ranking candidate schemes** | **Kendall's Coefficient of Concordance ($W$)** | Appropriate when analyzing relative prioritization / ranking order of candidate schemes within each scenario. |
| **Supplementary nominal check** | **Fleiss' Kappa ($\kappa$) (Optional)** | Supplementary check for nominal categorical agreement only; explicitly noted that it does not penalize distance between ordinal categories (treats 0 vs 1 identically to 0 vs 3). |

**Reporting Standards:** Rather than reporting a single statistic as proof of reliability, benchmark reports must document: (1) Number of expert annotators $m$, (2) Number of jointly rated items $N$, (3) Count and pattern of missing ratings, (4) Observed score distribution across 0, 1, 2, 3, and (5) Disagreement/confusion matrices.

### Acceptability Threshold

As a working guideline, we will aim for:
- **κ or κ_w ≥ 0.40** (Moderate agreement, minimum acceptable for academic benchmark)
- **κ or κ_w ≥ 0.60** (Substantial agreement, preferred target)

If pilot set agreement falls below 0.40, annotation guidelines will be revised and the pilot annotation will be repeated before proceeding to the full 50–100 scenarios.

---

## 13. Ground Truth Construction

After independent annotation and inter-rater agreement analysis, expert scores will be aggregated into the final benchmark ground truth.

### 13.1 Aggregation Approach (Preliminary)

The specific aggregation formula will be finalized after reviewing the pilot annotation data. The following approaches will be evaluated:

| Approach | Description | When Appropriate |
|---|---|---|
| **Mean Score** | Average of all annotators' scores per (scenario, scheme) pair | When scores are close and agreement is high (κ ≥ 0.60) |
| **Majority Vote (Mode)** | Most common score across annotators | When scores are clearly categorical and majority is clear |
| **Weighted Average** | Expert scores weighted by annotator expertise tier | If annotators have significantly different experience levels |
| **Consensus After Discussion** | Annotators resolve disagreements collaboratively for disputed items | Appropriate for items where at least two annotators differ by ≥ 2 score points |

**No final formula will be prescribed until pilot annotation data is available.** The choice will be made transparently and documented in the benchmark paper.

### 13.2 Preserving Raw Scores

Regardless of the aggregation method chosen, **all individual annotator scores will be preserved in the dataset** as separate columns (`relevance_annotator_A`, `relevance_annotator_B`, `relevance_annotator_C`) alongside the aggregated ground truth (`relevance_consensus`). This ensures reproducibility and allows other researchers to apply alternative aggregation methods.

---

## 14. Data Split and Leakage Prevention

### 14.1 Split Rationale

The annotated benchmark will be split into:
- **Train set (~60%):** Used to fit ML ranking/scoring models.
- **Validation set (~20%):** Used for hyperparameter tuning and model selection.
- **Test set (~20%):** Held out entirely for final performance evaluation. Not inspected during model development.

For a 100-scenario benchmark: approximately 60 train / 20 validation / 20 test scenarios.  
For a 50-scenario benchmark: approximately 30 train / 10 validation / 10 test scenarios.

### 14.2 Leakage Prevention

The primary leakage risk in this benchmark is **near-duplicate farmer profiles crossing splits**. For example, two scenarios with `(Raichur, Cotton, 3.0 acres, SC, Dryland, CROP_INSURANCE)` and `(Raichur, Cotton, 3.5 acres, SC, Dryland, CROP_INSURANCE)` are functionally near-identical and should not appear in both training and test splits.

Leakage prevention will be enforced by:

1. **Stratified split on `agro_climatic_zone × immediate_need`:** All scenarios with the same zone and need category are assigned to the same split where possible, preventing a model from learning the same farm-type pattern in both train and test.

2. **Template diversity enforcement:** The full 50–100 scenarios will be constructed from deliberately distinct scenario templates. Two scenarios may share a crop but must differ in at least two other primary fields (`district`, `land_size_acres`, `social_category`, `immediate_need`, `land_type`).

3. **Manual review of split assignments:** Before finalizing splits, the scenario list will be reviewed to confirm no two scenarios in different splits are within the same "demographic cluster" as defined by: {agro_climatic_zone, crop_primary, farmer_category, immediate_need, land_type}.

---

## 15. Research Integrity

The following integrity commitments apply to this benchmark and all downstream outputs:

| Commitment | Operationalization |
|---|---|
| **Real data is clearly labeled as real** | KCC (5,079 farmer queries, Dec 2024, Karnataka, directly downloaded from data.gov.in) and NSS 77th Round (Schedule 33.1, MoSPI official microdata) are cited by name, source URL, download date, and record count in all publications. |
| **Derived data is labeled as derived** | Farmer scenario profiles are described as "derived from NSS 77th Round distributions and KCC query taxonomy." They are never described as "real farmer records." |
| **Expert-annotated data is labeled as expert-annotated** | All ground truth labels are labeled as `expert_relevance_label` with annotator category recorded. They are never described as "real farmer preference data." |
| **No fabricated government eligibility facts** | Every eligibility rule in the deterministic engine is traceable to a field in `scheme_master.xlsx`, which references official government portal URLs and operational guideline PDFs verified on 2026-09-15. |
| **No fabricated eligibility rules** | No eligibility criterion is inferred, extrapolated, or invented. If a rule is ambiguous in the official guideline, it is marked `[AMBIGUOUS — VERIFY]` and excluded from the engine until officially confirmed. |
| **No fabricated expert labels** | No relevance label is generated by a language model, rule function, or any automated method. All scores come from physically/digitally recorded human expert responses. |
| **Scheme facts are traceable to official sources** | `official_source_url` and `official_document_url` fields in `scheme_master.xlsx` are the sole basis for any eligibility fact used in this project. |

---

## 16. Expected Benchmark Output Format

The final benchmark dataset will be a structured flat file in the following schema:

```
benchmark_record {
    scenario_id           : String          (e.g., "S001")
    [all 13 required scenario fields]       (from Section 3.1)
    [optional scenario fields]              (if populated)
    scheme_id             : String          (e.g., "SCH003")
    scheme_name           : String          (full name)
    eligibility_passed    : Boolean         (from Stage 1 engine, always True in benchmark)
    relevance_annotator_A : Integer (0–3)   (raw score)
    relevance_annotator_B : Integer (0–3)   (raw score)
    relevance_annotator_C : Integer (0–3)   (raw score, if 3rd annotator available)
    relevance_consensus   : Float           (aggregated ground truth, defined after pilot)
    split                 : Enum            ("train", "validation", "test")
}
```

Each scenario will generate **one row per eligible scheme**. If a scenario has 6 eligible schemes, it will produce 6 rows with the same scenario fields and different `scheme_id` and `relevance_*` fields.

**Expected scale:**
- Scenarios: 50–100
- Eligible schemes per scenario: typically 3–7 (out of 10 total), based on eligibility engine outputs
- Total annotatable (scenario, scheme) pairs: approximately 200–500

---

## 17. Next Steps After Approval

This specification is **not a license to generate scenarios immediately.** The following ordered steps apply:

### Step 1 — Guide Review of This Specification (Current Step)
The project guide reviews this document and:
- Approves or amends the schema (Section 3).
- Approves the annotation scale (Section 9).
- Confirms the expert annotator selection criteria (Section 11).
- Confirms the pilot size and coverage (Section 7).

### Step 2 — Build the Deterministic Eligibility Engine
Code the rule functions for each of the 10 schemes in `src/eligibility/engine.py`, derived strictly from `scheme_master.xlsx`. Test against boundary cases before constructing any scenarios.

### Step 3 — Construct 10 Pilot Scenarios
Construct the first 10 pilot scenarios manually, following the schema and design principles in this document. Run each through the eligibility engine to produce the candidate scheme list for each scenario.

### Step 4 — Prepare Expert Annotation Form
Create the annotation form (physical PDF or Google Sheets) for the 10 pilot scenarios × eligible schemes, implementing the annotation protocol from Sections 9–11.

### Step 5 — Pilot Annotation & Agreement Review
Recruit 2–3 expert annotators, administer the pilot annotation under independence protocol, and compute preliminary inter-rater agreement on the pilot set.

### Step 6 — Revise or Proceed
If pilot agreement is satisfactory (κ ≥ 0.40), proceed to construct the full 50–100 scenario set and full annotation. If not, revise annotation guidelines and repeat the pilot.

### Step 7 — Full Benchmark Construction
Construct 50–100 scenarios following the coverage matrix, run the eligibility engine, and administer the full annotation round.

---

*Document prepared by: Project Team*  
*Based on: NSS 77th Round Schedule 33.1 official codebook, KCC Karnataka Dec-2024 dataset (data.gov.in), 10-scheme verified master (scheme_master.xlsx, verification date: 2026-09-15)*
