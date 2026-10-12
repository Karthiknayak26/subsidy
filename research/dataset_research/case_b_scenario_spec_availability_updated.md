# Case B — Expert-Annotated Scenario Benchmark: Design Specification

**Document Type:** Research Dataset Design Specification  
**Milestone:** Phase 1 → Phase 2 — Benchmark Construction  
**Status:** Draft for Guide Review — availability-aware revision (Do Not Generate Scenarios Until Approved)  
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
2. Checking a separately maintained, timestamped availability record for each scheme and the relevant geography/crop/activity.
3. Running only currently actionable candidates through a deterministic eligibility engine derived from the verified 10-scheme master.
4. Presenting each scenario and its available, eligible candidate schemes to qualified agricultural domain experts.
5. Recording independent expert relevance judgments (on a 0–3 ordinal scale) as the training and evaluation ground truth.

**Farmer-facing availability rule:** A scheme must not be shown as “available now” unless current official evidence supports that status for the relevant application period and geography. Unknown or stale status must never be presented as confirmed availability. Closed, paused, exhausted, or unverified schemes are excluded from the default “Available now” recommendations. The system may explain that status needs verification only when the farmer asks about that scheme; it must not imply that an application or subsidy is currently available.

This methodology is consistent with established practices in information retrieval and recommender system research (e.g., TREC relevance pools, LETOR benchmark construction), adapted to the agricultural welfare domain.

---

## 2. Research Question

The core research question that the Case B benchmark is designed to evaluate is:

> **"As of a specified date, among schemes whose current availability is officially verified and whose eligibility rules the farmer appears to satisfy, which schemes are most relevant to the farmer's current situation?"**

The question is deliberately separated into three checks:

- **Pre-check — Current availability (time-sensitive, source-backed):** Is the scheme actionable now for the relevant geography, crop/activity and application period?
- **Stage 1 — Eligibility (deterministic):** Does the farmer appear to satisfy the published scheme conditions?
- **Stage 2 — Relevance ranking (ML + expert-annotated):** Among schemes that pass both checks, how should they be ranked by practical usefulness to the farmer?

Availability and eligibility are different. A scheme can be active but not accepting applications; a window can be open while allocation/funding status is unpublished; and a farmer can be eligible for a scheme that is not currently actionable. The ML ranker must not infer or override availability or statutory eligibility.

The benchmark provides human-expert relevance labels for Stage 2. The expert annotation task is therefore **not about determining legal eligibility** — that is handled by the rule engine in Stage 1.

---

## 3. Scenario Schema

Each scenario record describes a single anonymous farmer at a specific point in time, with sufficient detail to (a) determine eligibility against each scheme and (b) assess the relevance of eligible schemes to that farmer's current situation.

### 3.1 Schema Table

| Field | Data Type | Status | Allowed Values / Range | Source / Justification |
|---|---|---|---|---|
| `scenario_id` | String | **Required** | `S001` – `S100` (format: `S` + zero-padded integer) | Internal tracking identifier |
| `recommendation_as_of_date` | Date (`YYYY-MM-DD`) | **Required** | Date on which availability and eligibility are evaluated | Prevents time-sensitive status being treated as timeless; must match the availability snapshot used for the scenario |
| `availability_snapshot_id` | String | **Required for benchmark records** | Stable ID/version identifying the exact availability snapshot used | Preserves reproducibility when scheme windows or allocations change; see Section 3.3 |
| `agro_climatic_zone` | String (Enum) | **Required** | `Northern Dry Zone`, `Central Dry Zone`, `Southern Dry Zone`, `Southern Transition Zone`, `Eastern Dry Zone`, `Hilly Zone (Malnad)`, `Coastal Zone` | Karnataka Dept. of Agriculture's 10 Agro-Climatic Zone classification; used to determine climatic context and scheme applicability (e.g., Krishi Bhagya restricted to rainfed/dryland zones) |
| `district` | String (Enum) | **Required** | Any of Karnataka's 31 districts (e.g., `Raichur`, `Haveri`, `Udupi`, `Tumakuru`, `Dharwad`, `Mysuru`) | NSS 77th Round district codes (Karnataka State Code 29); representative examples drawn from each agro-climatic zone |
| `crop_primary` | String (Enum) | **Required** | One of: `Paddy`, `Maize`, `Ragi`, `Jowar`, `Groundnut`, `Redgram`, `Cotton`, `Sugarcane`, `Arecanut`, `Coconut`, `Banana`, `Mango`, `Tomato`, `Onion`, `Chilli`, `Turmeric`, `Sunflower`, `Soybean` | NSS 77th Round Block 6 crop codes (Karnataka subset); KCC query distribution — crops frequently mentioned in scheme-related queries |
| `crop_secondary` | String (Enum) | Optional | Same list as `crop_primary`, or `None` | Intercropping patterns from NSS 77th Round; e.g., Groundnut + Redgram in North Karnataka |
| `land_size_acres` | Float | **Required** | `0.5` to `20.0` (continuous, recorded in acres) | NSS 77th Round Block 5 operational holding size (Karnataka); breakpoints informed by scheme thresholds: < 2.5 acres (marginal), 2.5 – 5.0 acres (small), 5.0 – 12.5 acres (medium/large) |
| `land_type` | String (Enum) | **Required** | `Dryland (Rainfed)`, `Irrigated (Canal)`, `Irrigated (Borewell)`, `Irrigated (Open Well)`, `Mixed (Partial Irrigation)` | NSS 77th Round Block 5 irrigation source data; directly determines eligibility for Krishi Bhagya (dryland required), Ganga Kalyana (dryland required), PMKSY (water source required), PM-KUSUM B (borewell present, no grid connection), and MIDH (irrigation mandatory) |
| `social_category` | String (Enum) | **Required** | `General (OC)`, `OBC (2A)`, `OBC (2B)`, `OBC (3A)`, `OBC (3B)`, `SC`, `ST`, `Minority (Muslim)`, `Minority (Christian)` | NSS 77th Round Block 3 social group code; determines access to Ganga Kalyana (SC/ST/Minority/BC only) and subsidy tiers in SMAM (50% for SC/ST), Krishi Bhagya (90% vs 80%), PMKSY (SC/ST top-up) |
| `farmer_category` | String (Enum) | **Required** | `Marginal (< 2.5 acres)`, `Small (2.5–5 acres)`, `Medium (5–12.5 acres)`, `Large (> 12.5 acres)` | NSS 77th Round classification; GOI statutory definitions applied to `land_size_acres`; determines subsidy rate differentials across SMAM, PMKSY, and Ganga Kalyana |
| `existing_assets` | List[String] | **Required** | One or more of: `Borewell (Non-energized)`, `Borewell (Grid-connected)`, `Open Well`, `Farm Pond (Existing/Funded)`, `Drip Irrigation (Installed)`, `Sprinkler (Installed)`, `Diesel Pump Set`, `Electric Pump Set`, `Solar Pump`, `Tractor (Owned)`, `Power Tiller`, `None` | Derived from NSS 77th Round Block 5 (irrigation sources) and Block 12 (productive assets). Directly gates eligibility for: PM-KUSUM B (borewell present + no grid = eligible; grid connected = ineligible); PMKSY (water source present = eligible); Krishi Bhagya (existing funded farm pond = ineligible); Ganga Kalyana (working borewell/pump = ineligible); SMAM (tractor required for tractor-implement subsidy) |
| `income_tax_payer` | Boolean | **Required** | `True` / `False` | Directly determines PM-KISAN ineligibility per GOI exclusion criteria; NSS 77th Round Block 4 indebtedness + income proxy can inform realistic probability |
| `govt_employee_family` | Boolean | **Required** | `True` / `False` | Determines PM-KISAN ineligibility; included to allow negative eligibility test cases for SCH001 |
| `annual_family_income_lakh` | Float (Approximate) | **Required** | `0.5` – `12.0` (in Rs. Lakh) | Determines Ganga Kalyana income ceiling (≤ Rs. 6 Lakh); NSS 77th Round Block 4 total household income estimate (farm + non-farm income, reference year 2018-19; illustrative scaling to 2026 context) |
| `immediate_need` | String (Enum) | **Required** | One of: `CROP_INSURANCE`, `MICRO_IRRIGATION_SUPPORT`, `FARM_MECHANIZATION`, `RAINWATER_HARVESTING`, `SOLAR_PUMP_INSTALLATION`, `PROTECTED_HORTICULTURE`, `PRODUCTION_CREDIT`, `SOIL_NUTRIENT_ADVISORY`, `BOREWELL_IRRIGATION`, `INCOME_SUPPORT` | Derived from KCC 44 QueryType category taxonomy (mapped to scheme-specific intent categories). Represents the primary problem or need articulated by the farmer. Directly informs which schemes are most relevant at the annotation stage |
| `farming_stage` | String (Enum) | Optional | `Pre-sowing (Land Preparation)`, `Sowing`, `Mid-season (Growing)`, `Pre-harvest`, `Post-harvest`, `Fallow / Off-season` | KCC Karnataka Dec-2024 data contains a `Season` column (100% null in the current extract). **This field is therefore marked Optional and will not be filled until a seasonal KCC extract with non-null Season data is confirmed available.** If filled, it constrains PMFBY application period eligibility. |
| `season` | String (Enum) | Optional | `Kharif`, `Rabi`, `Summer`, `Annual` | Determines PMFBY premium tier (Kharif 2.0% vs Rabi 1.5%) and crop insurance application cut-off relevance; Optional until KCC seasonal data confirmed |
| `kcc_query_text_example` | String | Optional | Free text (Kannada or English) | Illustrative farmer query language from KCC taxonomy; used to ground the intent field in real farmer language; purely illustrative, not used for ML training |

### 3.2 Field Status Summary

| Status | Fields |
|---|---|
| **Required** (all scenarios must have) | `scenario_id`, `recommendation_as_of_date`, `availability_snapshot_id` (for benchmark records), `agro_climatic_zone`, `district`, `crop_primary`, `land_size_acres`, `land_type`, `social_category`, `farmer_category`, `existing_assets`, `income_tax_payer`, `govt_employee_family`, `annual_family_income_lakh`, `immediate_need` |
| **Optional** (included when evidence supports it) | `crop_secondary`, `farming_stage`, `season`, `kcc_query_text_example` |


---

## 3.3 Current Scheme Availability — Mandatory Pre-Check

The system must distinguish a scheme's existence from its **current actionable availability**. The master scheme records are relatively stable reference data; application windows, regional targets and funding status can change. These time-sensitive facts must be maintained separately in `scheme_database/processed/scheme_availability.csv` and must never be guessed by the model.

### Availability record grain

Create a separate record for each combination that can have a different status, such as scheme × state/district/notified area × crop/activity × application period. Do not assume one status applies to every district, crop, season or beneficiary category.

### Required availability fields

The accompanying `scheme_availability_template.csv` defines the initial columns. Key fields are:

- `scheme_id`: links to the verified scheme master.
- `geography_level`, `state`, `district`, `taluk_or_block`, `notified_area`: define the exact coverage of the status evidence; use only applicable fields and leave others blank.
- `crop_scope`, `activity_scope`, `season_or_application_period`: describe the scope of the availability notice, when applicable.
- `program_status`: `ACTIVE`, `PAUSED`, `DISCONTINUED`, or `UNKNOWN`.
- `application_status`: `OPEN`, `UPCOMING`, `CLOSED`, `YEAR_ROUND`, `NOT_APPLICABLE`, or `UNKNOWN`.
- `funding_status`: `AVAILABLE_CONFIRMED`, `EXHAUSTED_CONFIRMED`, `NOT_PUBLISHED`, `NOT_APPLICABLE`, or `UNKNOWN`.
- `application_open_date`, `application_close_date`: use only when an official source states the dates.
- `official_status_source_url`, `official_notice_url`, `source_published_date`, `checked_at`, `valid_until`, and `evidence_note`: preserve provenance and freshness.
- `availability_disposition`: derived by code, not manually guessed. Suggested outputs: `AVAILABLE_NOW`, `UPCOMING`, `CLOSED`, `PAUSED_OR_DISCONTINUED`, `FUNDING_EXHAUSTED`, `UNVERIFIED`.

### Conservative decision policy

A scheme may enter the farmer-facing **“Available now”** list only when:

1. Current official evidence supports that the scheme is active.
2. The application status is officially `OPEN` or explicitly `YEAR_ROUND`, as applicable.
3. The evidence covers the farmer's relevant geography and crop/activity where those restrictions exist.
4. The status record is still within its documented validity period and has not been superseded by a newer official notice.
5. If application depends on a limited allocation/target, no official source indicates that the relevant allocation is exhausted, and funding availability is confirmed when it is publicly reported at that granularity.

If funding availability is not published, record `NOT_PUBLISHED`; do **not** claim “funds are confirmed available.” If the current application status is missing, stale, contradictory or impossible to verify, disposition must be `UNVERIFIED`, and the scheme must not appear in the default “Available now” recommendations. The UI can offer a cautious “status needs confirmation with the department” explanation when appropriate, but must not tell the farmer that the subsidy is available now.

`ACTIVE` does not imply `OPEN`. `OPEN` does not automatically imply funding is available. `ELIGIBLE` does not imply the farmer can apply today. These states must remain separate in storage, code and user-facing explanations.

### User communication / notification policy

- The initial prototype should check status when a farmer requests recommendations and show only currently verified actionable schemes in the default results.
- Do not repeatedly message farmers with the same scheme status.
- Proactive SMS/IVR notifications are a later feature and must be opt-in, event-driven (for example, a verified application window opening), deduplicated, and linked to the official source.
- Every displayed availability claim must show `checked_at` or a clear “last verified” date and an official source link.
- Availability snapshots used in expert annotation and evaluation must be retained, so benchmark results can be reproduced after the live status changes.

### What this means for the Case-B benchmark

Each scenario has `recommendation_as_of_date` and `availability_snapshot_id`. Before expert annotation, the pipeline should:

1. Load the dated availability snapshot applicable to the scenario date.
2. Exclude candidates that are closed, paused/discontinued, funding-exhausted, or unverified from the default “Available now” candidate pool.
3. Evaluate published farmer eligibility conditions for the remaining candidates.
4. Mark any unresolved scheme-specific eligibility condition `NEEDS_MANUAL_VERIFICATION`; do not silently convert it to eligible.
5. Present only schemes that pass both current availability and eligibility checks to the relevance ranker/annotators.

Closed or unverified schemes must **not** be assigned relevance score `0`; they are excluded before annotation. Score `0` remains reserved for a scheme that is available and eligible but not relevant to the farmer's immediate need.

---

## 4. Data Grounding

Each scenario field is grounded in empirical evidence from one or more of our three verified data sources. **NSS 77th Round does not provide scheme recommendation labels and is not used as such.**

### 4.1 NSS 77th Round (Schedule 33.1 SAS — Karnataka Subset, ~3,000 Households)

Used **only** to ground the realistic distribution of farmer-profile characteristics in Karnataka:

| Scenario Field | NSS 77th Round Source Block / Variable |
|---|---|
| `district` | Block 1 — District code (State code 29 = Karnataka; 31 districts) |
| `land_size_acres` | Block 5 — Total operational holding size (owned + leased-in − leased-out), in hectares (converted to acres: × 2.471) |
| `land_type` | Block 5 — Source of irrigation (tube well, open well, canal, unirrigated); irrigated vs rainfed area split |
| `social_category` | Block 3 — Social group code (1 = General, 2 = OBC, 3 = SC, 4 = ST) |
| `farmer_category` | Derived from Block 5 land size using GOI SMF definition (< 2 ha = Marginal/Small) |
| `existing_assets` | Block 5 (irrigation source), Block 12 (purchase of productive assets: pump sets, tractors, drip equipment) |
| `annual_family_income_lakh` | Block 4 — Total household income (farm income from Block 6 + non-farm income from Blocks 10, 11) — provides calibration range |
| `crop_primary` | Block 6 — Crop code × Kharif/Rabi season × Karnataka subset |
| `income_tax_payer` | Proxy: households with total annual income > Rs. 10 Lakh, derived from Block 4 income estimate |

**What NSS is NOT used for:** NSS does not provide multi-scheme recommendation outcomes, scheme rankings, or relevance labels. Those are provided exclusively by human expert annotation.

### 4.2 KCC Karnataka Dataset (Dec 2024, 5,079 Records)

Used **only** to ground realistic farmer information needs and query language:

| Scenario Field | KCC Source Column |
|---|---|
| `immediate_need` (categories) | `QueryType` column — 44 categories mapped to 10 scheme-aligned intent categories |
| `crop_primary` (frequency weighting) | `Crop` column — confirmed most frequent crops by query volume (despite 98% `Others` in scheme-query subset) |
| `kcc_query_text_example` | `KccAns` / `QueryText` columns — illustrative real farmer language |

**What KCC is NOT used for:** KCC does not provide scheme recommendation labels, eligibility outcomes, or scheme rankings.

### 4.3 10-Scheme Master (`scheme_master.xlsx`)

Used to define **exactly which scenario fields are required** to run the deterministic eligibility engine, and to confirm that no scenario attribute is invented beyond what official scheme criteria demand:

| Scheme | Scenario Fields That Drive Eligibility |
|---|---|
| SCH001 PM-KISAN | `income_tax_payer`, `govt_employee_family`, `land_size_acres` (> 0) |
| SCH002 PMFBY | `crop_primary` (must be notified crop), `land_type` (any), `season` (optional, drives premium rate) |
| SCH003 PMKSY-PDMC | `land_size_acres` (≥ 0.5 acres / 0.2 ha), `land_type` / `existing_assets` (water source required), `farmer_category` (drives 55% vs 45%) |
| SCH004 SMAM | `social_category` + `farmer_category` (drives 50% vs 40%), `existing_assets` (tractor needed for tractor-drawn implement) |
| SCH005 Krishi Bhagya | `land_type` (Dryland required), `land_size_acres` (≥ 1.0 acre), `existing_assets` (no funded farm pond), `district` (rainfed taluks) |
| SCH006 PM-KUSUM B | `existing_assets` (borewell present + no grid connection), `land_size_acres` (≥ 0.5 acres) |
| SCH007 MIDH | `crop_primary` (horticulture crops), `land_size_acres` (≥ 0.25 acres), `existing_assets` (micro-irrigation required), `land_type` (irrigation mandatory) |
| SCH008 KCC-MISS | `existing_assets` (no CIBIL default assumed), `land_size_acres` (> 0) |
| SCH009 Soil Health Card | `land_size_acres` (> 0), no other structural restrictions |
| SCH010 Ganga Kalyana | `social_category` (SC/ST/Minority/BC only), `land_type` (dryland/kushki), `land_size_acres` (1.0–5.0 acres), `annual_family_income_lakh` (≤ 6.0 Lakh), `existing_assets` (no working borewell/pump) |

---

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

1. **Schema validation:** Confirm that the required scenario fields are sufficient to run the deterministic eligibility engine without ambiguity.
2. **Annotation task validation:** Confirm that the relevance annotation question is clearly understood by expert annotators, using the pilot as a calibration set during expert briefing.
3. **Inter-annotator feasibility:** A quick preliminary assessment of annotator agreement on 10 scenarios can identify annotation guideline gaps before they propagate across 100 scenarios.
4. **Guide review gate:** Per project protocol, the pilot set will be reviewed by the project guide before the full 50–100 scenarios are constructed. This is the **current next step**.

### 7.2 Pilot Set Design

The 10 pilot scenarios will be constructed to cover:
- At least 5 distinct agro-climatic zones.
- At least 6 distinct immediate needs.
- At least 3 distinct social categories.
- At least 1 scenario where a specific scheme (Ganga Kalyana) is NOT applicable despite superficially similar farmer context (i.e., a deliberate negative eligibility case).
- At least 1 farmer with horticulture crop (for MIDH relevance testing).
- At least 1 farmer with dryland context in Northern Karnataka (for Krishi Bhagya relevance).

**Pilot scenarios will be generated only after this specification document is approved by the project guide.**

---

## 8. Candidate Scheme Generation Pipeline

The workflow from farmer scenario to annotatable scheme list is availability-aware. Availability is checked against a dated official-source snapshot before eligibility rules and relevance annotation.

```
FARMER SCENARIO + AS-OF DATE
           │
           ▼
┌─────────────────────────────────────────┐
│  Pre-check: Official Availability Gate  │
│  Active + actionable now + correct scope│
│  Closed / unknown / stale → do not show │
└─────────────────────────────────────────┘
           │ only verified currently actionable candidates
           ▼
┌─────────────────────────────────────────┐
│  Stage 1: Deterministic Eligibility     │
│  Engine (Rule-based Python functions)   │
│                                         │
│  For each of 10 schemes in master:      │
│  eligible_conditions.evaluate(scenario) │
│  excluded_conditions.evaluate(scenario) │
│                                         │
│  → ELIGIBLE / INELIGIBLE / NEEDS_MANUAL_VERIFICATION      │
└─────────────────────────────────────────┘
           │
           ▼
  AVAILABLE + ELIGIBLE CANDIDATE SCHEMES
  (subset of 10, supported by dated official
  availability evidence and scheme rules — no ML)
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

Score **0 (Irrelevant)** is possible only for a scheme that has passed the current-availability and eligibility gates. Closed, funding-exhausted, stale-status or unverified schemes are excluded before annotation and must not receive a relevance score. For an available and eligible scheme, score 0 handles cases where:
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

| Metric | Applicability | Conditions for Selection |
|---|---|---|
| **Fleiss' Kappa (κ)** | Multi-annotator categorical agreement | Appropriate if scores are treated as nominal categories (0, 1, 2, 3 without assuming ordinal distance) |
| **Weighted Cohen's Kappa (κ_w)** | Two-annotator ordinal agreement | Appropriate for pairwise annotation with ordinal score differences penalized proportionally (linear or quadratic weighting) |
| **Kendall's W (Coefficient of Concordance)** | Multi-annotator ranking agreement | Appropriate if scores are analyzed as relative rankings of schemes per scenario rather than absolute ordinal values |
| **Intraclass Correlation Coefficient (ICC)** | Multi-annotator continuous agreement | Appropriate if scores are treated as continuous measurements rather than ordinal categories |

**Selection will not be made until the annotation format is finalized** and a preliminary review of the pilot set data determines whether annotators' scores resemble ordinal categories, relative ranks, or near-continuous ratings. All four metrics will be computed on the pilot set and the most appropriate one will be reported in the final benchmark paper.

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
| **Scheme facts are traceable to official sources** | `official_source_url` and `official_document_url` fields in `scheme_master.xlsx` are the basis for eligibility facts used in this project. |
| **Availability is time-sensitive and verified separately** | Current application/funding status is recorded in a dated availability file with official evidence; unknown or stale status is never presented as currently available. |

---

## 16. Expected Benchmark Output Format

The final benchmark dataset will be a structured flat file in the following schema:

```
benchmark_record {
    scenario_id           : String          (e.g., "S001")
    recommendation_as_of_date : Date         (YYYY-MM-DD)
    availability_snapshot_id : String        (dated official-status snapshot)
    [all required scenario fields]          (from Section 3.1)
    [optional scenario fields]              (if populated)
    scheme_id             : String          (e.g., "SCH003")
    scheme_name           : String          (full name)
    availability_disposition : Enum        (available_now for benchmark candidate rows)
    application_status    : Enum              (open / year_round as verified)
    funding_status        : Enum              (confirmed / not_published / etc.)
    availability_checked_at : DateTime        (official status check time)
    eligibility_status    : Enum              (eligible for annotated candidate rows)
    relevance_annotator_A : Integer (0–3)   (raw score)
    relevance_annotator_B : Integer (0–3)   (raw score)
    relevance_annotator_C : Integer (0–3)   (raw score, if 3rd annotator available)
    relevance_consensus   : Float           (aggregated ground truth, defined after pilot)
    split                 : Enum            ("train", "validation", "test")
}
```

Each scenario will generate **one row per currently available and eligible scheme**. If a scenario has 6 schemes that pass both availability and eligibility gates, it will produce 6 rows with the same scenario fields and different `scheme_id` and `relevance_*` fields.

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

### Step 2 — Build the Scheme Availability Data Layer
Create and document `scheme_database/processed/scheme_availability.csv` from official status pages/notices. Do not populate statuses without dated official evidence. Implement a conservative availability checker that distinguishes active status, application window, funding/allocation status, and unknown/stale evidence.

### Step 3 — Build the Deterministic Eligibility Engine
Code the rule functions for each of the 10 schemes in `src/eligibility/engine.py`, derived strictly from `scheme_master.xlsx`. Unknown/ambiguous criteria must return `NEEDS_MANUAL_VERIFICATION`, not guessed eligibility. Test boundary cases before constructing any scenarios.

### Step 4 — Construct 10 Pilot Scenarios
Construct the first 10 pilot scenarios manually, each with a recommendation as-of date and availability snapshot. Run availability filtering first, then eligibility, to produce the currently actionable candidate list for each scenario.

### Step 5 — Prepare Expert Annotation Form
Create the annotation form (physical PDF or Google Sheets) for the 10 pilot scenarios × currently available and eligible schemes, implementing the annotation protocol from Sections 9–11.

### Step 6 — Pilot Annotation & Agreement Review
Recruit 2–3 expert annotators, administer the pilot annotation under independence protocol, and compute preliminary inter-rater agreement on the pilot set.

### Step 7 — Revise or Proceed
If pilot agreement is satisfactory (κ ≥ 0.40), proceed to construct the full 50–100 scenario set and full annotation. If not, revise annotation guidelines and repeat the pilot.

### Step 8 — Full Benchmark Construction
Construct 50–100 scenarios following the coverage matrix, run the eligibility engine, and administer the full annotation round.

---

*Document prepared by: Project Team*  
*Based on: NSS 77th Round Schedule 33.1 official codebook, KCC Karnataka Dec-2024 dataset (data.gov.in), 10-scheme verified master (scheme_master.xlsx, verification date: 2026-09-15)*
