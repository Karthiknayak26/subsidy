# Government Scheme Master Data Audit Report

**Document Type:** Agricultural Policy Data Audit & ML Architecture Review  
**Milestone:** Phase 1 (Data Foundation) → Pre-Implementation Gate (Eligibility & Availability Engine)  
**Status:** Complete Audit Report — Awaiting Project Guide Decisions  
**Auditor:** Senior Agricultural-Policy Data Auditor & ML Research Mentor  
**Date of Audit:** October 12, 2026  
**Audited Artifacts:**
- `scheme_database/raw/SCH*.json` (10 raw scheme files)
- `scheme_database/processed/scheme_master.json`
- `scheme_database/processed/scheme_master.csv`
- `scheme_database/scheme_master.xlsx`
- `scheme_database/build_scheme_master.py`
- `scheme_database/processed/scheme_availability_template.csv`
- `research/dataset_research/case_b_scenario_spec.md`

---

## 1. Executive Summary & Audit Overview

Before writing the first line of the deterministic eligibility engine (`src/eligibility/engine.py`) or implementing availability filtering, a rigorous audit of the 10 curated schemes in `scheme_database/` was conducted against official Government of India (GoI) and Government of Karnataka (GoK) operational guidelines, statutory notifications, and departmental orders.

### 1.1 Core Audit Finding
The 10-scheme master is fundamentally sound in its domain coverage and captures the broad realities of agricultural welfare in Karnataka. However, several critical policy nuances, formula ambiguities, and multi-agency structural complexities were identified that, if left uncorrected, would cause the deterministic eligibility engine to generate false positives or false negatives, and distort the ML relevance ranker.

### 1.2 Summary of Scheme Audit Statuses

| Scheme ID | Scheme Name | Audit Status | Key Finding / Action Item |
|---|---|---|---|
| **SCH001** | PM-KISAN | **PROVISIONAL** | Exclusions are officially verified; cut-off date (01.02.2019) missing; invalid income-proxy proposed in scenario spec must be replaced with statutory flags. |
| **SCH002** | PMFBY | **CONFLICT** | `benefit_formula` currently records the contingent yield indemnity formula, conflating contingent insurance claims with the guaranteed upfront government premium subsidy. |
| **SCH003** | PMKSY-PDMC | **VERIFIED** | Central 55%/45% cost norms and 5 ha limit verified; Karnataka state top-up (up to 90% for SC/ST) verified; 7-year lock-in period verified. |
| **SCH004** | SMAM | **VERIFIED** | 50%/40% subsidy tiers, 2 ha threshold, and tractor ownership prerequisite for tractor-drawn implements verified. |
| **SCH005** | Krishi Bhagya | **VERIFIED** | 90%/80% subsidy rates, 131 rainfed taluks scope, dryland requirement, and 1.0-acre minimum catchment verified. |
| **SCH006** | PM-KUSUM Component B | **VERIFIED** | 60% total subsidy, 7.5 HP cap, and mandatory off-grid / un-energized water source condition verified. |
| **SCH007** | MIDH | **VERIFIED** | 50% cost norm, 1,000–4,000 m² boundaries for protected structures, and micro-irrigation prerequisite verified. |
| **SCH008** | KCC-MISS | **PROVISIONAL** | Central 4% effective interest (Rs. 3 Lakh cap) verified; Karnataka state cooperative 0% interest scheme (Rs. 5 Lakh cap) omitted. |
| **SCH009** | Soil Health Card | **VERIFIED** | 100% free diagnostic service, 12 chemical parameters, and open landholding access verified. |
| **SCH010** | Ganga Kalyana | **CONFLICT / AMBIGUOUS** | Single record lumps 6+ distinct development corporations with separate budgets/portals; ignores Community Borewell mode (8–15 acres). |

---

## 2. Audit Methodology & Standards

Every scheme attribute was evaluated against the following strict evidentiary hierarchy:
1. **Primary Authority:** Official Gazette Notifications, Ministry Operational Guidelines (PDFs), Reserve Bank of India Master Circulars, and Karnataka Government Orders (GOs).
2. **Secondary Authority:** Official departmental portals (DA&FW, PMFBY, KREDL, KMDC, Raitha Mitra, Samrakshane, Seva Sindhu).
3. **Excluded as Evidence:** Third-party aggregators, commercial farm blogs, and unofficial summaries (including NegiluKrishi).
4. **Audit Status Definitions:**
   - **VERIFIED:** Completely backed by official operational guidelines without contradiction.
   - **PROVISIONAL:** Generally accurate, but missing statutory cut-offs or operational constraints.
   - **CONFLICT:** Direct contradiction between policy reality and database representation (e.g., formula or multi-agency lumping).
   - **OUTDATED:** Fact was formerly true but has been superseded by a recent government amendment.
   - **AMBIGUOUS:** Guidelines leave criteria open to local administrative interpretation.

---

## 3. Scheme-by-Scheme Audit

### SCH001: Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)
- **Official Portals:** `https://pmkisan.gov.in/`
- **Official Guidelines:** *Operational Guidelines of Pradhan Mantri Kisan Samman Nidhi (DA&FW, MoA&FW, Govt. of India, Revised 2020)*
- **Document References:** Section 2 (Definition of Family), Section 3 (Eligibility & Cut-off Date), Section 3(b) (Exclusion Categories).
- **Audit Status:** **PROVISIONAL**

#### Findings & Detailed Audit Check:
1. **Farmer Categories & Land Ceiling:**
   - Launched in Feb 2019 exclusively for Small and Marginal Farmers (up to 2 ha).
   - Cabinet decision of May 31, 2019 expanded coverage to **all cultivable landholding farmer families** regardless of size.
   - The master's representation (`min_land: "> 0 acres"`, `max_land: "No limit"`) is **VERIFIED**.
2. **Statutory Cut-Off Date:**
   - Under Section 3.2, land ownership must be established as of **February 1, 2019**. Any transfer of land title after 01.02.2019 (except by succession/inheritance due to death of the titleholder) is ineligible for PM-KISAN for 5 years.
   - *Issue:* The master omits this cut-off rule.
3. **Statutory Exclusions vs. Income Proxies:**
   - Under Section 3(b), exclusions are strictly institutional/professional:
     - Institutional landholders.
     - Former/present constitutional post holders, Ministers, MPs, MLAs, MLCs, Mayors, ZP Chairpersons.
     - Serving/retired officers & employees of Central/State Govt/PSEs/Local bodies (excluding Multi-Tasking Staff / Class IV / Group D).
     - Pensioners with monthly pension ≥ Rs. 10,000 (excluding MTS/Group D).
     - Persons who paid Income Tax in the last assessment year.
     - Professionals (Doctors, Engineers, Lawyers, CAs, Architects).
   - *Critical Finding:* There is **NO general income limit** (e.g., no poverty line or Rs. 2 Lakh ceiling) in PM-KISAN. A wealthy farmer with Rs. 50 Lakh purely agricultural income who pays no income tax and holds no disqualified post is legally eligible.
4. **Tenant Farmers & Landless Laborers:**
   - Pure tenant farmers and landless agricultural laborers are **strictly ineligible**. The beneficiary family must have title to cultivable land in state land records.
- **Recommended Correction:**
  - Retain the exact statutory exclusion flags.
  - Update `eligible_conditions` to explicitly specify: *"Beneficiary must hold cultivable land ownership recorded on or before 01.02.2019 (or acquired via inheritance). Tenant farmers without land title are ineligible."*

---

### SCH002: Pradhan Mantri Fasal Bima Yojana (PMFBY)
- **Official Portals:** `https://pmfby.gov.in/` | `https://samrakshane.karnataka.gov.in/`
- **Official Guidelines:** *Revised Operational Guidelines of PMFBY (DA&FW, MoA&FW, 2020 / Rev. 2023)*
- **Document References:** Section II (Coverage of Crops), Section III (Coverage of Farmers), Section VI (Premium Rates), Section XI (Assessment of Loss).
- **Audit Status:** **CONFLICT**

#### Findings & Detailed Audit Check:
1. **Voluntary Enrollment:**
   - Since Kharif 2020, enrollment is 100% voluntary for all farmers (loanee and non-loanee).
2. **Benefit Formula vs. Claim Indemnity (THE CONFLICT):**
   - The master records: `Claim = [(Threshold Yield - Actual Yield) / Threshold Yield] * Sum Insured`.
   - *Conflict:* This is the **Indemnity Claim Settlement formula** for area-based yield losses. It is **NOT** the guaranteed government subsidy.
   - The guaranteed welfare assistance provided to every enrolled farmer is the **Upfront Premium Subsidy**:
     $$\text{Upfront Government Premium Subsidy} = (\text{Actuarial Premium Rate} - \text{Capped Farmer Rate}) \times \text{Sum Insured}$$
     Where the farmer's share is statutorily capped at:
     - 2.0% for Kharif Food & Oilseed crops
     - 1.5% for Rabi Food & Oilseed crops
     - 5.0% for Annual Commercial & Horticultural crops
     The balance actuarial premium (often 10%–35%) is paid 50:50 by Central and State Governments.
   - The insurance claim indemnity is a **contingent risk payout** that triggers only upon crop loss across 5 distinct peril stages:
     1. Prevented Sowing / Planting (up to 25% of sum insured)
     2. Mid-Season Adversity (immediate on-account payment up to 25% of likely claims)
     3. End-of-Season Yield Shortfall (Area approach via Crop Cutting Experiments)
     4. Post-Harvest Losses (up to 14 days for unbundled drying crops)
     5. Localized Calamities (Hailstorm, landslide, inundation, cloudburst)
- **Recommended Correction:**
  - Rename/reframe `benefit_rate` to explicitly define the **Guaranteed Premium Subsidy Rate**.
  - Update `benefit_formula` to state:
    - *Guaranteed Benefit:* `Government_Premium_Subsidy = (Actuarial_Rate - Farmer_Capped_Rate) * Sum_Insured`
    - *Contingent Indemnity:* `Claim_Payout = [(Threshold_Yield - Actual_Yield) / Threshold_Yield] * Sum_Insured` (plus localized/prevented sowing provisions).

---

### SCH003: Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)
- **Official Portals:** `https://pmksy.gov.in/`
- **Official Guidelines:** *Operational Guidelines of Per Drop More Crop (DA&FW, MoA&FW, 2022)*
- **Document References:** Chapter 3 (Pattern of Assistance), Chapter 4 (Eligibility Criteria), Annexure I (Indicative Cost Norms).
- **Audit Status:** **VERIFIED**

#### Findings & Detailed Audit Check:
1. **Central Pattern of Assistance:**
   - Small & Marginal Farmers (≤ 2.0 ha): 55% of indicative unit cost.
   - Other Farmers (> 2.0 ha): 45% of indicative unit cost.
   - Maximum land ceiling: 5.0 hectares per beneficiary family.
   - Minimum land threshold: 0.2 hectares (approx. 0.5 acres).
2. **Karnataka State Top-Up:**
   - In Karnataka, under the State Horticulture / Agriculture Mission, an additional state top-up subsidy is provided:
     - SC/ST Farmers: Total effective subsidy up to 90%.
     - General SMF: Total effective subsidy up to 70%–75% (subject to annual state budget allocation).
3. **Asset & Lock-In Requirements:**
   - Farmer must possess an assured irrigation source (borewell, open well, farm pond, river lift) with an operational pump.
   - **7-Year Lock-In:** Land parcel must not have received micro-irrigation subsidy in the previous 7 years.
- **Recommended Correction:**
  - Clarify in `benefit_formula` that the Central baseline is 55%/45% and the 90% rate for SC/ST is a Karnataka State top-up component.

---

### SCH004: Sub-Mission on Agricultural Mechanization (SMAM)
- **Official Portals:** `https://agrimachinery.nic.in/`
- **Official Guidelines:** *Operational Guidelines of Sub-Mission on Agricultural Mechanization (DA&FW, MoA&FW, Revised)*
- **Document References:** Component 3 (Financial Assistance for Procurement of Agricultural Machinery), Annexure II (Permissible Subsidy Pattern).
- **Audit Status:** **VERIFIED**

#### Findings & Detailed Audit Check:
1. **Subsidy Structure:**
   - 50% of machine cost (subject to category cap) for SC, ST, Small & Marginal farmers (≤ 2 ha), and Women.
   - 40% of machine cost (subject to category cap) for Other / General farmers (> 2 ha).
2. **Equipment Prerequisites & Landholding:**
   - No statutory minimum landholding for manual/small powered equipment (power weeders, knapsack sprayers, power tillers).
   - For tractor-drawn equipment (rotavators, seed drills, threshers): The farmer **must own a registered tractor** (RC copy in beneficiary's name).
   - For tractor subsidy: Karnataka Farmech portal requires ownership of cultivable land (typically min. 2.0–3.0 acres).
3. **Lock-In Period:**
   - 5 to 7 years between subsidies for the same machinery type.
- **Recommended Correction:**
  - The master is accurate. Retain requirement that tractor ownership is an asset prerequisite for tractor-drawn implements.

---

### SCH005: Krishi Bhagya Yojana
- **Official Portals:** `https://raitamitra.karnataka.gov.in/`
- **Official Guidelines:** *Krishi Bhagya Scheme Guidelines, Department of Agriculture, Government of Karnataka*
- **Document References:** Scheme Framework (Farm Pond, Polythene Lining, Lifting Pump, Micro-irrigation).
- **Audit Status:** **VERIFIED**

#### Findings & Detailed Audit Check:
1. **Geographic & Agro-Climatic Scope:**
   - Restricted to **rainfed and dryland areas** of Karnataka, specifically covering 131 dryland taluks across 25+ districts (Bayaluseeme / North & Central Karnataka).
   - Coastal districts (Dakshina Kannada, Udupi) and heavy rainfall/command areas (Malnad/Canal commands) are excluded.
2. **Package Subsidy Components:**
   - Component 1: Krishi Honda (Farm pond excavation: 10×10×3m up to 21×21×3m).
   - Component 2: Polythene geomembrane lining (UV stabilized 300/500 micron).
   - Component 3: Diesel or Solar pump set for lifting stored water.
   - Component 4: Micro-irrigation equipment (Drip/Sprinkler).
   - Component 5: Protective shade net / chain-link fence.
3. **Subsidy Rates & Land Boundaries:**
   - 90% subsidy for SC and ST farmers.
   - 80% subsidy for General dryland farmers.
   - Minimum landholding: 1.0 acre (to provide sufficient rainfall catchment).
   - Maximum landholding: 5.0 hectares (12.35 acres).
4. **Current Policy Validity:**
   - Relaunched in Karnataka State Budget 2023-24 and continued in 2024-25 / 2025-26 with designated budgetary outlays.
- **Recommended Correction:**
  - Fully verified. Ensure eligibility engine checks both `land_type == "Dryland (Rainfed)"` and that `district` belongs to notified rainfed taluks.

---

### SCH006: PM-KUSUM Component B (Standalone Solar Agriculture Pumps)
- **Official Portals:** `https://pmkusum.mnre.gov.in/` | `https://kredl.karnataka.gov.in/`
- **Official Guidelines:** *Guidelines for Implementation of PM-KUSUM Scheme (MNRE, Govt. of India, 2019 / Rev. 2023)*
- **Document References:** Component B (Installation of Standalone Solar Pumps), Section 3.2 (Pattern of Assistance).
- **Audit Status:** **VERIFIED**

#### Findings & Detailed Audit Check:
1. **Subsidy Breakdown:**
   - Central Financial Assistance (CFA): 30% of benchmark cost.
   - State Subsidy (KREDL / Govt. of Karnataka): 30%.
   - Beneficiary Share: 40% (can obtain bank loan up to 30%, direct cash contribution 10%).
   - Total Subsidy: 60%.
2. **Critical Statutory Prerequisite (Off-Grid Condition):**
   - The scheme targets **off-grid, non-electrified areas**.
   - The water source (borewell/open well) **MUST NOT have an existing grid electricity connection (DISCOM IP set)**.
   - An NOC / certificate from the local ESCOM (BESCOM, HESCOM, GESCOM, MESCOM, CESC) confirming that no grid connection exists for that survey number is mandatory.
   - Farmers with existing electric pump sets are covered under **Component C** (Solarisation of grid-connected pumps), NOT Component B.
3. **Borewell Drilling Exclusion:**
   - PM-KUSUM **does not drill borewells**. The applicant must already possess a functional water source with tested water yield.
4. **Capacity Ceiling:**
   - Subsidy is capped at 7.5 HP pump capacity. Higher capacity pumps may be installed, but the subsidy is capped at the 7.5 HP benchmark cost.
- **Recommended Correction:**
  - Fully verified. In the eligibility engine, `existing_assets` must contain `Borewell (Non-energized)` or `Open Well` and must **exclude** `Borewell (Grid-connected)`.

---

### SCH007: Mission for Integrated Development of Horticulture (MIDH)
- **Official Portals:** `https://midh.gov.in/`
- **Official Guidelines:** *Operational Guidelines of MIDH (DA&FW, MoA&FW)*
- **Document References:** National Horticulture Mission (NHM) Component, Protected Cultivation Cost Norms.
- **Audit Status:** **VERIFIED**

#### Findings & Detailed Audit Check:
1. **Protected Cultivation Norms:**
   - Naturally Ventilated Polyhouse: Cost norm Rs. 844 to Rs. 1,060 per m².
   - Shade Net House: Cost norm Rs. 710 per m².
   - Subsidy Rate: 50% of cost norm.
2. **Area Limits:**
   - Minimum area: 1,000 m² (approx. 0.25 acres).
   - Maximum area: 4,000 m² (approx. 1.0 acre) per beneficiary family.
3. **Mandatory Infrastructure:**
   - Must have an assured perennial irrigation source with an operational micro-irrigation system installed.
   - Prior sanction letter from District Horticulture Officer is mandatory before commencing work.
- **Recommended Correction:**
  - Fully verified. High precision in cost norms and land area limits.

---

### SCH008: Kisan Credit Card - Modified Interest Subvention Scheme (KCC-MISS)
- **Official Portals:** `https://www.rbi.org.in/` | `https://jansamarth.in/`
- **Official Guidelines:** *RBI Master Circular — Kisan Credit Card (FIDD.CO.FSD.BC.No.12/05.05.010/2018-19) & DA&FW Interest Subvention Guidelines*
- **Document References:** Scale of Finance Norms, Interest Subvention Rate, Prompt Repayment Incentive.
- **Audit Status:** **PROVISIONAL / CONFLICT**

#### Findings & Detailed Audit Check:
1. **Central Scheme Interest Structure:**
   - Base lending rate: 9.0% p.a.
   - GoI 2% Interest Subvention to banks brings nominal rate to 7.0% p.a.
   - Prompt Repayment Incentive (PRI) of 3.0% brings effective rate to **4.0% p.a.** for farmers repaying within 365 days.
   - Upper limit for 4% rate: **Rs. 3,00,000 (Rs. 3.00 Lakh)**. (Allied activities sub-limit: Rs. 2.00 Lakh).
   - Collateral-free limit: Rs. 1,60,000.
2. **Omission of Karnataka State Zero-Interest Scheme (The Conflict):**
   - The master describes Central KCC-MISS via commercial banks/RRBs, but completely omits Karnataka’s flagship cooperative credit scheme:
     - Under the **Karnataka State Zero-Interest Crop Loan Scheme (Baddi Rahitha Bele Sala)**, disbursed via Primary Agricultural Credit Societies (PACS) and DCCBs, the Government of Karnataka provides an additional interest subvention.
     - Eligible Karnataka farmers receive short-term crop loans up to **Rs. 5,00,000 at 0% (zero) interest**!
   - *Impact on Recommendation System:* A farmer seeking credit in Karnataka should be informed of both:
     - Commercial Bank / RRB route: 4% effective interest up to Rs. 3 Lakh (Central KCC-MISS).
     - Cooperative / PACS route: 0% interest up to Rs. 5 Lakh (GoK Baddi Rahitha Bele Sala).
- **Recommended Correction:**
  - Update `benefit_rate` and `benefit_formula` in SCH008 to document the 0% Cooperative alternative alongside the 4% Commercial Bank Central baseline.

---

### SCH009: Soil Health Card Scheme
- **Official Portals:** `https://soilhealth.dac.gov.in/`
- **Official Guidelines:** *Operational Guidelines of Soil Health Card Scheme (DA&FW, MoA&FW)*
- **Document References:** Soil Sampling Norms, 12 Parameter Matrix.
- **Audit Status:** **VERIFIED**

#### Findings & Detailed Audit Check:
1. **Service Nature & Parameters:**
   - 100% free diagnostic service.
   - 12 parameters tested:
     - Macro-nutrients: Nitrogen (N), Phosphorus (P), Potassium (K)
     - Secondary nutrient: Sulphur (S)
     - Micro-nutrients: Zinc (Zn), Iron (Fe), Copper (Cu), Manganese (Mn), Boron (Bo)
     - Physical parameters: pH, Electrical Conductivity (EC), Organic Carbon (OC)
2. **Access & Landholding:**
   - Universal access for all operational agricultural landholders. No minimum or maximum land limit.
- **Recommended Correction:**
  - Fully verified. Retain current record.

---

### SCH010: Ganga Kalyana Scheme
- **Official Portals:** `https://kmdc.karnataka.gov.in/` | `https://adcl.karnataka.gov.in/` | `https://sevasindhu.karnataka.gov.in/`
- **Official Guidelines:** *Ganga Kalyana Scheme Guidelines (KMDC / Dr. B.R. Ambedkar Dev. Corp / D. Devaraj Urs Dev. Corp)*
- **Document References:** Eligibility Criteria, Unit Cost Norms, Landholding Minimums & Ceilings.
- **Audit Status:** **CONFLICT / AMBIGUOUS**

#### Findings & Detailed Audit Check:
1. **Multi-Corporation Institutional Fragmentation (THE MAJOR CONFLICT):**
   - Ganga Kalyana is **not** a single scheme administered by the Agriculture Department. It is administered independently by **at least 6 different statutory caste/community development corporations**:
     1. *Karnataka Minorities Development Corporation (KMDC):* Religious Minorities (Muslims, Christians, Jains, Buddhists, Sikhs, Parsis).
     2. *Dr. B.R. Ambedkar Development Corporation:* Scheduled Castes (SC).
     3. *Karnataka Maharshi Valmiki ST Development Corporation:* Scheduled Tribes (ST).
     4. *D. Devaraj Urs Backward Classes Development Corporation:* Backward Classes (Cat-1, 2A, 3A, 3B).
     5. *Karnataka Arya Vysya Community Development Corporation:* Arya Vysya community.
     6. *Karnataka State Brahmin Development Board:* Economically backward Brahmins.
   - Each corporation has:
     - Its own annual state budget allotment.
     - Its own distinct application service on the Karnataka Seva Sindhu portal.
     - Specific community certificates required (RD-numbered caste certificate).
   - An SC farmer applying via KMDC will be rejected; an OBC farmer applying via Ambedkar Corp will be rejected.
2. **Individual vs. Community / Group Borewell Modes:**
   - The master describes only the **Individual Borewell** mode.
   - In reality, all corporations operate two distinct modes:
     - **Individual Borewell Scheme:** Farmer must own contiguous dryland:
       - Coastal / Malnad districts: 1.00 to 5.00 acres.
       - Plain / Dryland districts: 1 acre 20 guntas (1.50 acres) to 5.00 acres.
     - **Community / Group Borewell Scheme (Samooha Kola Bavi):** For small/marginal farmers with less than 1.5 acres:
       - A group of 2 or more farmers belonging to the target community who jointly pool **8.0 to 15.0 acres** of adjacent dryland can obtain a collective community borewell with an underground distribution network.
3. **Income Ceiling Discrepancy:**
   - The master specifies an annual family income ceiling of Rs. 6,00,000 (Rs. 6 Lakh).
   - *Audit Check:* In Ambedkar Corp and Devaraj Urs Corp operational guidelines, the rural income ceiling has historically been set at Rs. 1.50 Lakh to Rs. 2.00 Lakh, with recent enhancements for specific non-taxpayer brackets. Treating Rs. 6.00 Lakh as a universal limit across all corporations is ambiguous and requires corporation-specific verification.
4. **Mandatory Exclusions:**
   - Land must be 100% dryland (*kushki*). Any parcel with an existing borewell, open well, or canal irrigation is strictly disqualified.
   - Government employees, income tax payers, and families with prior Ganga Kalyana beneficiaries are strictly excluded.
- **Recommended Correction:**
  - See Section 4.3 for architectural decision options.

---

## 4. Special Investigative Topics

### 4.1 Conflation of Farmer Land-Size Classifications vs. Scheme Eligibility Thresholds
A critical conceptual error in agricultural recommender systems is conflating **demographic landholding classifications** with **statutory scheme eligibility boundaries**.

#### Demographic Baseline (Agricultural Census of India / FAO):
- **Marginal Farmer:** $< 1.00$ hectare ($< 2.47$ acres, standard operational cutoff: $< 2.5$ acres)
- **Small Farmer:** $1.00$ to $2.00$ hectares ($2.47$ to $4.94$ acres, standard cutoff: $2.5$ to $5.0$ acres)
- **Semi-Medium Farmer:** $2.00$ to $4.00$ hectares ($5.0$ to $10.0$ acres)
- **Medium Farmer:** $4.00$ to $10.00$ hectares ($10.0$ to $25.0$ acres)
- **Large Farmer:** $> 10.00$ hectares ($> 25.0$ acres)
- **Small & Marginal Farmers (SMF) combined:** $\le 2.00$ hectares ($\le 5.0$ acres)

#### Comparison with Scheme-Specific Statutory Boundaries:

| Scheme | Statutory Land Min | Statutory Land Max | Subsidy Rate Boundary | Conflation Risk |
|---|---|---|---|---|
| **PM-KISAN** | $> 0$ acres | No limit | None (Uniform Rs. 6,000) | **High:** Pre-June 2019 rules had a 2 ha ceiling; models often wrongly reject > 5-acre farmers. |
| **PMFBY** | $> 0$ acres | Holding size | None (Capped % of Sum Insured) | None. |
| **PMKSY-PDMC** | 0.2 ha (~0.5 ac) | **5.0 ha (~12.35 ac)** | 55% for $\le 2$ ha; 45% for $> 2$ ha | **Severe:** 5.0 ha (12.35 acres) is the subsidy ceiling, NOT the 5-acre SMF demographic cutoff. |
| **SMAM** | $> 0$ ac (2–3 ac for tractor) | No limit | 50% for $\le 2$ ha; 40% for $> 2$ ha | Moderate: Machine caps vary; tractor requires minimum land. |
| **Krishi Bhagya** | **1.0 acre** | **5.0 ha (~12.35 ac)** | 90% SC/ST; 80% General | **Severe:** If max land is confused as "5 acres" instead of "5 hectares", a 6-acre dryland farmer would be falsely rejected. |
| **PM-KUSUM B** | ~0.5 acres | No ceiling | Capped at 7.5 HP cost | None. |
| **MIDH** | **0.25 acres** (1,000 m²) | **1.00 acre** (4,000 m²) | 50% of cost norm | **Severe:** Maximum subsidized area is only 1.0 acre, completely independent of total farm size. |
| **Ganga Kalyana** | **1.0 / 1.20 acres** | **5.00 acres** | 100% Grant | **Critical:** Strictly limited to Small & Marginal farmers ($\le 5$ acres). Farmer with 5.1 acres is disqualified. |
| **KCC-MISS** | $> 0$ acres | No limit | Scales with Scale of Finance | None. |
| **Soil Health** | $> 0$ acres | No limit | Free service | None. |

**Audit Conclusion:** The eligibility engine must **never** use a single generic `is_small_farmer` boolean to gate all schemes. Each scheme rule must inspect the numeric `land_size_acres` against its own statutory lower and upper bounds.

---

### 4.2 PMFBY Benefit and Claim Formula Representation
The audit confirms that `scheme_master.json` currently represents PMFBY incorrectly by stating that the `benefit_formula` is the Crop Cutting Experiment yield indemnity formula.

#### Why This Is a Critical Defect:
1. **Subsidy vs. Insurance Payout:** The government's guaranteed social welfare contribution is the **Premium Subsidy**. If an actuarial premium is 18% and the farmer pays 2%, the government immediately contributes 16% of the Sum Insured.
2. **Contingent Nature of Claims:** A claim payout is not guaranteed; it is paid only if an insured calamity occurs.
3. **Multi-Peril Structure:** The threshold yield formula applies only to widespread end-of-season yield shortfalls (Area Approach). It does not represent localized calamities (individual farm survey) or prevented sowing (lump-sum 25%).

#### Standardized Representation to Implement:
- `benefit_type`: `Insurance Premium Subsidy (Upfront) & Risk Indemnity (Contingent)`
- `guaranteed_benefit_formula`: `Govt_Premium_Subsidy = (Actuarial_Premium_Rate - Farmer_Capped_Rate) * Sum_Insured_per_ha * Area`
- `contingent_claim_formula`: `Shortfall_Claim = Max(0, (Threshold_Yield - Actual_Yield) / Threshold_Yield) * Sum_Insured`

---

### 4.3 Ganga Kalyana Implementations Across Development Corporations
Task 4 explicitly requested an investigation into whether Ganga Kalyana implementations for different development corporations should be split into separate records or retained as a single record.

#### Architectural Comparison:

```
Option A: Single Umbrella Record (Current)
   SCH010: Ganga Kalyana Scheme
      ├── Logic: If SC/ST/OBC/Minority AND Land 1.20–5.0 ac AND Kushki → Eligible
      └── Downstream Issue: Recommendation output says "Apply to Ganga Kalyana"
          without identifying WHICH Corporation, WHICH Seva Sindhu Service ID,
          or WHICH application window applies.

Option B: Corporation-Specific Scheme Records (Recommended for Implementation)
   SCH010_SC_ST    : Ganga Kalyana (Dr. B.R. Ambedkar & Valmiki Corporations)
   SCH010_OBC      : Ganga Kalyana (D. Devaraj Urs BC Development Corporation)
   SCH010_MINORITY : Ganga Kalyana (Karnataka Minorities Development Corporation)
      ├── Logic: Strict 1-to-1 mapping with social category, Seva Sindhu endpoint,
      │          and distinct corporation budget.
      └── Recommendation output gives exact corporation portal and RD certificate type.
```

**Audit Recommendation:** For Phase 1 / Phase 2, retain `SCH010` as a parent identifier in the master dataset to preserve the 10-scheme benchmark, but enrich its metadata with a `corporation_routing_table` attribute that explicitly maps `social_category` to the responsible corporation and Seva Sindhu service code.

---

### 4.4 PM-KISAN Statutory Exclusions vs. Income Proxies
In `case_b_scenario_spec.md`, Section 4.1 stated:
> `income_tax_payer: Proxy: households with total annual income > Rs. 10 Lakh, derived from Block 4 income estimate`

#### The Legal and Policy Reality:
- Agricultural income in India is exempt from Central Income Tax under Section 10(1) of the Income Tax Act, 1961.
- A commercial farmer earning Rs. 25 Lakh exclusively from crop cultivation is **not legally required to pay income tax** and is **100% eligible for PM-KISAN**.
- Conversely, a small farmer earning Rs. 3.5 Lakh from a non-farm trading business who files an ITR-3/4 is **statutorily excluded from PM-KISAN**, regardless of farm distress.
- Using an "income > 10 Lakh" proxy conflates household wealth with statutory tax-filing status.

**Audit Conclusion:** Scenario profiles in Case B must **explicitly supply** a boolean flag `income_tax_payer: True/False` based on statutory criteria, rather than deriving it from an artificial income threshold.

---

### 4.5 Feasibility of Deriving Scenario Fields from NSS 77th Round and KCC Microdata
The audit verified what attributes can genuinely be extracted from NSS 77th Round (Schedule 33.1) and KCC Call Centre data, versus what must be explicitly constructed:

| Scenario Field | Feasible from NSS 77th Round? | Feasible from KCC Dec-2024? | Required Action in Case B Benchmark |
|---|---|---|---|
| `district` | **Yes** (Block 1, District Code) | **Yes** (District column) | Sampled from empirical distribution |
| `land_size_acres` | **Yes** (Block 5, Operational Holding) | No | Sampled from empirical distribution |
| `land_type` (Irrigated / Rainfed) | **Yes** (Block 5, Irrigated Area) | No | Sampled from empirical distribution |
| `social_category` (SC/ST/OBC/Gen) | **Yes** (Block 3, Social Group) | No | Sampled from empirical distribution |
| `crop_primary` | **Yes** (Block 6, Crop Codes) | **Yes** (Crop column) | Sampled from empirical distribution |
| `annual_family_income_lakh` | **Yes** (Block 4/6/10/11 Total Income) | No | Sampled from empirical distribution |
| `immediate_need` | No | **Yes** (QueryType taxonomy) | Mapped from KCC QueryType taxonomy |
| `income_tax_payer` | **NO** (NSS does not record ITR filing) | No | **Must be explicitly supplied / constructed** |
| `govt_employee_family` | **NO** (NSS has generic industry codes) | No | **Must be explicitly supplied / constructed** |
| `borewell_grid_status` (Off-grid vs Grid) | **NO** (NSS only records tubewell presence) | No | **Must be explicitly supplied / constructed** |
| `prior_subsidy_received` (7-yr lock-in) | **NO** (NSS does not track subsidy dates) | No | **Must be explicitly supplied / constructed** |
| `fruits_id_registration` | **NO** (Administrative database) | No | **Must be explicitly supplied / constructed** |

**Audit Conclusion:** The Case B specification correctly recognized that NSS and KCC cannot supply all exclusion and infrastructure flags. Scenarios must construct realistic combinations of these operational flags to test the engine's edge cases.

---

## 5. Availability Specification & Implementation Gate

The template [`scheme_availability_template.csv`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/scheme_database/processed/scheme_availability_template.csv) was inspected against the 10 scheme records and official operational realities.

### 5.1 Architecture: Strict Separation of Master Scheme Logic and Availability
The availability layer **must remain strictly separated** from the core scheme master.
- **Scheme Master:** Defines statutory eligibility criteria, benefit formulas, target crops, and administrative rules (relatively stable across policy cycles).
- **Availability Layer:** Captures dynamic, localized, and temporal constraints (budget quotas, seasonal cut-off dates, portal application windows).

As evidenced by the official **PMFBY Premium Calculator**, a generic nationwide or statewide "open" flag is fundamentally invalid. Calculating PMFBY parameters requires six granular inputs:
1. `Year` (e.g., 2026)
2. `Season` (Kharif vs. Rabi vs. Summer)
3. `State` (Karnataka)
4. `District` (e.g., Haveri, Raichur)
5. `Crop` (e.g., Maize, Cotton)
6. `Area` (in hectares/acres)

Cut-off dates and insurance company allocations differ down to the taluk/hobli and crop level. Applying a static binary "Open" flag across an entire state would lead to severe recommendations of closed or expired schemes.

### 5.2 The Four Mandatory Availability States
For every recommendation surfaced by the system, the architecture must classify each eligible scheme into one of exactly **four distinct availability states**:

1. **`Verified available now`**: Active application window officially confirmed through verified, dated circulars or live portal notices.
2. **`Eligible, but currently closed`**: Farmer statutorily qualifies, but the current seasonal or financial-year window has closed (e.g., PMFBY past Kharif cut-off date).
3. **`Upcoming, with an officially confirmed date`**: Official notification has announced a future opening date (e.g., Krishi Bhagya pre-monsoon portal opening on May 15).
4. **`Availability unknown — confirmation required`**: Eligibility is confirmed, but current operational availability cannot be verified against an official current notice.

### 5.3 User-Facing Presentation & Evidence Constraints
- **Strict Guardrail:** ONLY schemes in the state **`Verified available now`** may appear under the user-facing "Available Now" recommendation list.
- Schemes that are closed, upcoming, or unconfirmed must be displayed in a separate "Eligible Schemes (Timing / Verification Required)" section.
- **Evidence Requirement:** Every `Verified available now` record must store:
  - `official_status_source_url`
  - `official_notice_url`
  - `source_published_date`
  - `checked_at` timestamp

---

## 6. Prioritized Correction List

Before implementing the deterministic eligibility engine (`src/eligibility/engine.py`), the following corrections must be carried out across the scheme records:

### Priority 1: High (Directly Affects Eligibility Rule Engine & Architecture)
1. **[SCH001 PM-KISAN]:** Add explicit statutory ownership cut-off date (01.02.2019) to `eligible_conditions`, and clarify that pure tenant farmers without land records are ineligible.
2. **[SCH006 PM-KUSUM B]:** Ensure `existing_asset_requirements` explicitly distinguishes `Borewell (Non-energized / Off-grid)` from `Borewell (Grid-connected)`. Grid-connected pumps must trigger disqualification for Component B.
3. **[SCH010 Ganga Kalyana]:** Retain `SCH010` as parent; create verified child implementation records (`SCH010_AMBEDKAR`, `SCH010_VALMIKI`, `SCH010_DEVARAJ_URS`, `SCH010_KMDC`) capturing corporation-specific social categories, Seva Sindhu routes, and Individual vs. Community modes.
4. **[Agricultural Credit]:** Split credit into two distinct implementation records:
   - `SCH008_CENTRAL`: KCC-MISS (Commercial Banks/RRBs, 4% effective interest up to Rs. 3 Lakh).
   - `SCH008_KA_COOP`: Karnataka Cooperative Credit (PACS/DCCB, 0% interest up to Rs. 5 Lakh, maintained as provisional pending current-year notification verification).

### Priority 2: Medium (Affects Benefit Formulas & Explanations)
5. **[SCH002 PMFBY]:** Restructure `benefit_rate` and `benefit_formula` to prioritize estimated farmer premium and applicable government premium support, showing Sum Insured separately. Never guarantee a claim payout.
6. **[SCH003 PMKSY-PDMC]:** Clarify that the 90% SC/ST rate is a Karnataka State top-up, with 55% being the Central baseline.

### Priority 3: Low (Scenario Spec & Documentation Alignment)
7. **[Case B Spec Alignment]:** Update Section 4.1 of `case_b_scenario_spec.md` to remove the "income > 10 Lakh" proxy for PM-KISAN, replacing it with explicit statutory flags.
8. **[Pilot Scenario Calibration]:** Allocate 4 out of the 10 pilot scenarios for negative exclusion and boundary testing.

---

## 7. Project Guide Final Decisions & Architectural Resolutions

The project guide has reviewed the audit findings and rendered the following binding architectural and policy decisions:

### Decision 1: Ganga Kalyana Representation
- **Resolution:** **Retain SCH010 as the parent scheme record; create implementation-level child records.**
- **Implementation Detail:**
  - `SCH010` remains the parent conceptual scheme in the 10-scheme master taxonomy.
  - Implementation child records will be established for verified corporations:
    - `SCH010_AMBEDKAR` (Dr. B.R. Ambedkar Dev Corp — Scheduled Castes)
    - `SCH010_VALMIKI` (Maharshi Valmiki ST Dev Corp — Scheduled Tribes)
    - `SCH010_DEVARAJ_URS` (D. Devaraj Urs BC Dev Corp — Backward Classes Cat-1, 2A, 3A, 3B)
    - `SCH010_KMDC` (Karnataka Minorities Dev Corp — Religious Minorities)
  - Both **Individual Borewell** (1.20–5.0 acres) and **Community Borewell** (8–15 acres pooled) routes will be explicitly structured.

### Decision 2: PMFBY Benefit & Claim Framing
- **Resolution:** **Prioritize estimated farmer premium and applicable government premium support, with Sum Insured shown separately. Never guarantee a claim.**
- **Implementation Detail:**
  - Upfront financial metric: *Farmer Premium Payable* (e.g., 2% Kharif) vs. *Government Premium Support* (balance actuarial premium borne 50:50 by Center & State).
  - Risk metric: *Maximum Sum Insured* (DLTC scale of finance per hectare).
  - Claim calculation ($[(\text{Threshold} - \text{Actual})/\text{Threshold}] \times \text{Sum Insured}$) is presented strictly as a *Contingent Indemnity Clause*, accompanied by an explicit disclaimer that payouts occur only upon surveyed crop loss.

### Decision 3: Agricultural Credit (Dual-Record Structure)
- **Resolution:** **Maintain Central KCC/MISS and Karnataka Cooperative Credit as separate implementation records. Verify current-year limits and rates before activating the Karnataka option.**
- **Implementation Detail:**
  - `SCH008_CENTRAL`: Central KCC-MISS via Commercial Banks and RRBs (4% effective interest up to Rs. 3,00,000).
  - `SCH008_KA_COOP`: Karnataka Baddi Rahitha Bele Sala via PACS/DCCBs (0% interest up to Rs. 5,00,000).
  - Status for `SCH008_KA_COOP`: Maintained with `PROVISIONAL_PENDING_ANNUAL_GO` status until the active financial-year government order is attached.

### Decision 4: Negative Testing & Pilot Scenario Allocation
- **Resolution:** **Use four of the 10 pilot scenarios for exclusion and boundary coverage, supplemented by dedicated automated unit tests for every high-impact rule.**
- **Implementation Detail:**
  - Pilot scenarios S001–S006: Positive / diverse eligibility cases across distinct agro-climatic zones and need categories.
  - Pilot scenarios S007–S010: Deliberate negative exclusion boundary tests:
    - *S007 (PM-KISAN Exclusion):* Landholding family where a member filed Income Tax / holds government employment.
    - *S008 (PM-KUSUM B Exclusion):* Off-grid solar applicant whose borewell already has a grid-connected electric pump (DISCOM IP set).
    - *S009 (Ganga Kalyana Exclusion):* Small dryland farmer belonging to General Merit category (fails corporation caste mandate).
    - *S010 (PMKSY / Krishi Bhagya Lock-In):* Farmer who availed micro-irrigation subsidy 3 years ago (violates 7-year lock-in).

---

## 8. Pre-Implementation Correction Plan

Before modifying the master dataset or writing the rule engine, the execution plan is structured into five controlled phases:

```
┌──────────────────────────────────────────────────────────┐
│ Phase 1: Review & Approval of Correction Plan (Current)  │
│  - Verify schema extension for Parent/Child records      │
│  - Confirm exact field edits and disclaimer text         │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ Phase 2: Update Build Script & Regenerate Master Data    │
│  - Modify build_scheme_master.py                         │
│  - Regenerate raw JSONs, scheme_master.json, .csv, .xlsx │
│  - Maintain full backward compatibility for SCH001–SCH010│
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ Phase 3: Update Case B Scenario Specification            │
│  - Remove income proxy (> 10L) in case_b_scenario_spec.md│
│  - Add explicit statutory flags to scenario schema       │
│  - Formalize 4 negative pilot test scenario profiles     │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ Phase 4: Implement Deterministic Rule Engine             │
│  - Code src/eligibility/engine.py against corrected data │
│  - Implement 4-state availability filter                 │
│  - Implement automated unit tests for all exclusion rules│
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│ Phase 5: Pilot Benchmark Execution & Expert Review       │
│  - Run engine on 10 pilot scenarios (6 positive, 4 neg)  │
│  - Generate pilot annotation sheets for domain experts   │
└──────────────────────────────────────────────────────────┘
```

### 8.1 Detailed Schema Refinements to Apply
1. **Add `parent_scheme_id` and `record_type`:**
   - Standard schemes: `record_type: "STANDALONE"`
   - Parent schemes: `record_type: "PARENT"` (`SCH008`, `SCH010`)
   - Child schemes: `record_type: "CHILD"`, referencing `parent_scheme_id`
2. **Refine Benefit Fields in `build_scheme_master.py`:**
   - Add `upfront_subsidy_description`
   - Add `contingent_benefit_description`
   - Add `claim_disclaimer`
3. **Refine Statutory Exclusion Flags:**
   - Add machine-readable `rule_keys` to enable deterministic code mapping.

---

*Report prepared by: Senior Agricultural-Policy Data Auditor & ML Research Mentor*  
*Verified against: DA&FW, MNRE, RBI, GoK Department of Agriculture, and Karnataka Development Corporation Guidelines.*
