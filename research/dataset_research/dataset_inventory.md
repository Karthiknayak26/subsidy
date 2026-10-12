# Dataset Inventory & Feasibility Assessment

**Milestone:** Phase 0 → Phase 2 — Data Feasibility Investigation  
**Core Question:** *What data can actually teach the model what a "good recommendation" is?*

> [!IMPORTANT]
> All findings in this document are based on **direct inspection** of each dataset or official source.  
> Findings are timestamped. Cells marked `?` have not yet been independently verified.  
> The critical distinction maintained throughout: **data collected by a government system ≠ data publicly available for ML training.**

---

## Master Inventory Table

| Dataset | Source | Inspection Status | Real Farmers? | Scheme Info? | Farmer Need? | Labels? | Useful For |
|---|---|---|---|---|---|---|---|
| KCC Karnataka (Dec 2024) | data.gov.in | ✅ Inspected (Sep 15, 2026) | ✅ Indirect (district, crop, block) | ❌ / Limited | ✅ Query intent | ❌ | Intent analysis; query taxonomy |
| KCC multi-year / multi-state | data.gov.in (district-wise catalog) | ⚠️ Partially inspected (Sep 15, 2026) | ✅ Indirect | ❌ / Limited | ✅ | ❌ | Additional intent data — **further download needed** |
| PM-KISAN (OGD) | data.gov.in | ✅ Investigated (Sep 15, 2026) | ❌ Only village-level counts | ❌ | ❌ | ❌ | Beneficiary count statistics only |
| PM-KISAN (portal, individual) | pmkisan.gov.in | ✅ Investigated (Sep 15, 2026) | ✅ (Admin-only access) | ✅ (Admin-only) | ❌ | ❌ | **NOT publicly downloadable. Privacy-protected.** |
| PMFBY (OGD) | data.gov.in / pmfby.gov.in | ✅ Investigated (Sep 15, 2026) | ❌ Aggregate only | ✅ Aggregate | ❌ | ❌ | State/crop-wise enrollment statistics |
| PMFBY (portal, individual) | pmfby.gov.in | ✅ Investigated (Sep 15, 2026) | ✅ (Registration system) | ✅ (Registration system) | ❌ | ❌ | **NOT publicly downloadable. Privacy-protected.** |
| FRUITS (Karnataka) | fruits.karnataka.gov.in | ✅ Investigated (Sep 15, 2026) | ✅ (Admin-only) | ✅ (Admin-only) | ❌ | ❌ | **NOT publicly downloadable. PII-protected.** |
| NSS 77th Round (Schedule 33.1 SAS) | MoSPI Microdata Portal | ✅ Inspected (Sep 15, 2026) | ✅ ~3,000 Karnataka agri households | ⚠️ Only 3 specific schemes (PMFBY, KCC, Soil Health Card) | ❌ Historical uptake, not need | ❌ Insufficient for multi-scheme recommendation | Profile distributions & demographic priors; **Case A closed** |
| Scheme Master (to be curated) | Official Govt portals | ⏳ Pending (Phase 1) | ❌ | ✅ | ❌ | Rules only | Eligibility rule engine (Stage 1) |
| Case B — Expert-Annotated Scenario Benchmark | KVK / Agricultural officers | ⏳ Planned | N/A | ✅ | N/A | ✅ (Human expert annotated) | **Case B Benchmark — human expert annotated relevance labels on constructed farmer scenarios** |

---

## Section 1: KCC Dataset — Karnataka, December 2024 (Directly Inspected)

**Source:** data.gov.in (official open data portal, Ministry of Agriculture & Farmers Welfare)  
**Inspection Date:** September 15, 2026

### Structural Facts

| Property | Value |
|---|---|
| Total Records | 5,079 |
| Columns | 15 |
| Coverage Period | December 2024 only (single month) |
| States Covered | Karnataka only |
| Unique Districts | 28 |
| Unique Blocks/Taluks | 177 |
| `Season` column | **100% null — unusable** |

### What KCC Can Contribute

| Use | Supported? | Confidence | Basis |
|---|---|---|---|
| Farmer query categories and language | ✅ Yes | High | 44 QueryType labels, 5,079 real records |
| Geographic distribution of farmer needs | ✅ Yes | High | District coverage confirmed |
| Crop-level information need patterns | ✅ Partial | Medium | Crop field is `"Others"` in 98% of scheme queries |
| Seasonal query context | ❌ No | — | `Season` column 100% null |
| Farmer attributes (land, category) | ❌ No | — | Fields do not exist |
| Ranking ground truth ("Scheme A > Scheme B for Farmer X") | ❌ No | — | KCC records query intent only; no scheme outcome, eligibility, or benefit data present |

### Additional KCC Extracts Available

The official data.gov.in KCC catalog — *"District wise and month wise queries of farmers in Kisan Call Centre (KCC)"* — is an active catalog updated as of **June 2026**. The existing Karnataka December 2024 extract is one slice. Multi-month and multi-state extracts are available from the same catalog. However, confirmed via search evidence that:
- Standard KCC extract columns do **not** include `LandHolding`, `SocialCategory`, or `FarmerCategory`
- Additional extracts would expand query volume and time coverage but would not add farmer profile dimensions

**Action required:** Download additional KCC Karnataka extracts for other months/years to increase query coverage and validate that column schema is consistent across extracts.

---

## Section 2: PM-KISAN — P1 Investigation Result

**Investigation Date:** September 15, 2026  
**Sources consulted:** data.gov.in, pmkisan.gov.in (public-facing), web search for individual-level data availability

### Finding: Individual-Level Data NOT Publicly Available

| Data Type | Granularity | Available? | Notes |
|---|---|---|---|
| Village + Gender beneficiary counts | Village-level aggregate | ✅ OGD public | Resource: "Village and Gender-wise Beneficiaries Count under PM-KISAN Scheme" (updated Sep 2, 2026) |
| State/district disbursement statistics | District aggregate | ✅ Public | Usable only for population statistics |
| Individual farmer records (name, Aadhaar, land, crop, bank) | Farmer-level | ❌ NOT public | Privacy-protected under government data security norms |
| Farmer → scheme outcome linkage | Farmer-level | ❌ NOT public | Same restriction |

### Assessment

> [!WARNING]
> The public PM-KISAN OGD dataset is a **count dataset**, not an individual farmer table.  
> It cannot provide the `(farmer_profile → scheme_received)` labels needed for supervised ML.  
> PM-KISAN individual records are collected by the administrative system but are not released publicly, consistent with personal data protection practice.

**Case A status from PM-KISAN:** ❌ **Not established.**

What it can provide: Beneficiary count statistics useful for understanding scheme reach and population priors by district and gender.

---

## Section 3: PMFBY — P1 Investigation Result

**Investigation Date:** September 15, 2026  
**Sources consulted:** data.gov.in, pmfby.gov.in dashboard, web search

### Finding: Aggregate Dashboard Data Available, Individual Records NOT Public

| Data Type | Granularity | Available? | Notes |
|---|---|---|---|
| State/UT-wise farmer application & claim counts | State aggregate | ✅ Dashboard | pmfby.gov.in/adminStatistics/dashboard |
| Crop-wise enrollment statistics | Crop + State level | ✅ Dashboard | Useful for understanding which crops have high insurance uptake |
| District-wise coverage statistics | District aggregate | ✅ Partial | May vary by reporting season |
| Individual farmer enrollment records (caste, type, district, crop, bank) | Farmer-level | ❌ NOT public | Fields are collected during registration but NOT downloadable |
| Farmer → insurance outcome (claim paid, crop loss, amount) | Farmer-level | ❌ NOT public | Privacy-protected |

> **Key research distinction confirmed:**  
> PMFBY registration collects detailed farmer fields (caste category, farmer type, district, village, crop sown area, bank details). But the existence of those fields on the registration form does not mean the corresponding individual records are publicly downloadable.

### Assessment

**Case A status from PMFBY:** ❌ **Not established.**

What it can provide: Crop-wise and state-wise enrollment statistics useful for understanding which crops and regions have high insurance scheme awareness and uptake — a proxy for scheme relevance by crop-region combination.

---

## Section 4: FRUITS (Karnataka) — P1 Investigation Result

**Investigation Date:** September 15, 2026  
**Sources consulted:** fruits.karnataka.gov.in, web search for public data availability

### Finding: Administrative System — NO Public Dataset Available

FRUITS (Farmer Registration and Unified Beneficiary Information System) is developed by the Government of Karnataka / NIC as the "golden record" system for farmer identity, land records (linked to Bhoomi/RTC), bank details, and scheme DBT delivery. It is the backbone of all Karnataka agricultural DBT.

| Data Type | Available Publicly? | Notes |
|---|---|---|
| Individual farmer records (Aadhaar, RTC, crop, bank) | ❌ NOT public | PII-protected; access restricted to authorized government departments and banks |
| Scheme → farmer disbursement records | ❌ NOT public | Same restriction |
| Aggregate farmer count statistics | ✅ In annual reports | Not structured for ML training |

**Research access path:** Researchers typically rely on (a) secondary data from government reports, (b) institutional partnerships requiring formal approval from Dept. of Agriculture Karnataka, or (c) primary field surveys. The FRUITS microdata is NOT available through any public portal.

### Assessment

**Case A status from FRUITS:** ❌ **Not established through public channels.**

---

## Section 5: NSS 77th Round — Newly Identified Dataset (To Be Investigated)

## Section 5: NSS 77th Round — Schedule 33.1 Inspection (Directly Evaluated)

**Source:** MoSPI Microdata Portal — Central Data Catalog ([microdata.gov.in](https://microdata.gov.in/NADA/))  
**Survey Title:** Situation Assessment of Agricultural Households and Land and Livestock Holdings of Households in Rural India, 2019  
**Survey Schedule:** Schedule 33.1 (Integrated SAS + Land & Livestock Holdings)  
**Survey Period:** January 2019 – December 2019 (Agricultural Year: July 2018 – June 2019)  
**Inspection Date:** September 15, 2026  
**Status:** ✅ Evaluated via official codebook, field instructions (Vol. I), questionnaire, and fixed-width data layout guides (`NSS_77th_Layout_Sch_33.1_mult_post.xls`)

---

### The Five Decisive Questions & Empirical Findings

#### Q1: Can we download it?
* **Answer:** **Yes.**
* **Mechanism:** Available on the MoSPI Microdata Portal under public use / registered access. Requires free portal user registration, agreeing to the MoSPI Data Access Agreement, and direct download of fixed-width ASCII text files (`r77s331v1*.txt`, `r77s331v2*.txt`) and layout documentation.

#### Q2: How many Karnataka agricultural households are available?
* **Answer:** **Approximately 3,000 agricultural households.**
* **Basis (Report No. 587, Statement 1 & sample design):**
  * Total rural First Stage Units (FSUs/villages) allocated and surveyed in Karnataka: **490 FSUs**.
  * At 8 households canvassed per FSU, total rural households surveyed in Karnataka is ~3,920 across two visits.
  * Meeting the strict SAS agricultural household definition (producing > ₹4,000 value of agricultural produce and at least one member self-employed in farming): **~3,000 sample agricultural households** in Karnataka (nationwide: 45,716 agricultural households across 58,035 rural households).

#### Q3: What farmer-profile variables exist?
* **Answer:** **Exceptionally rich profile features.** Schedule 33.1 provides an authoritative socio-economic profile of rural Indian farming households:
  * **Geographic:** State (Karnataka code 29), District code, Sub-district/Tehsil, Village/FSU code.
  * **Demographic & Social:** Household size, religion, social group / caste category (Scheduled Caste, Scheduled Tribe, OBC, Others) [Block 3 / Level 02, 03].
  * **Landholdings:** Land owned, leased-in, leased-out, total operational holding size (hectares/acres), irrigated vs. un-irrigated land parcels [Block 5 / Level 04, 05].
  * **Crop Profile:** Specific crops cultivated during Kharif, Rabi, and summer seasons, area cultivated under each crop, output quantity, and gross production value [Block 6 / Level 06].
  * **Irrigation & Productive Assets:** Sources of irrigation (canal, borewell, open well, tank, lift), ownership of farm implements and equipment (pump sets, drip irrigation, sprinkler sets, power tillers, tractors) [Block 5, 12].
  * **Livestock Holdings:** Number and type of cattle, buffalo, sheep, goats, poultry, and dairy output [Block 8, 9, 10].
  * **Economic Indicators:** Household monthly consumption expenditure (MPCE proxy), total indebtedness, outstanding institutional vs. non-institutional loan liabilities [Block 4, 13].
  * **Institutional Membership:** Active membership in registered farmers' organizations, SHGs, or FPOs [Block 4].

#### Q4: What exact scheme-access variables exist?
* **Answer:** **Only 3 specific agricultural schemes/cards, plus rural employment and general banking.**
  
  Inspection of Block 4 (*Household Characteristics*), Block 14 (*Crop Marketing & MSP*), and Block 15 (*Access to Technical Advice*) reveals the following exact variables:
  
  | Block / Level | Variable / Item Description | Response Values | Scheme Identified |
  |---|---|---|---|
  | Block 4, Item 16/17 | Possession of Kisan Credit Card (KCC) | Binary: Yes (1) / No (2) | Kisan Credit Card |
  | Block 4, Item 21 / Block 6 | Crop insurance status under PM Fasal Bima Yojana | 1 = Insured under PMFBY, 2 = Insured under other scheme, 3 = Not insured | PMFBY |
  | Block 4, Item 18 | Possession of Soil Health Card (SHC) | Binary: Yes (1) / No (2) | Soil Health Card |
  | Block 4, Item 19 | Application of fertilizers/nutrients as per SHC recommendations | Binary: Yes (1) / No (2) | SHC Adoption |
  | Block 4, Item 20 | Possession of Animal Health Card (*Nakul Swasthya Patra*) | Binary: Yes (1) / No (2) | Animal Health Card |
  | Block 4, Item 14/15 | Possession of MGNREG job card & work undertaken | Binary: Yes (1) / No (2) | MGNREGA (Wage labor) |
  | Block 4, Item 13 | Possession of bank account by any member | Binary: Yes (1) / No (2) | Financial inclusion |
  | Block 14 | Awareness of Minimum Support Price (MSP) & sale to procurement agency | Aware: Yes/No; Agency: FCI, Mandi, APMC, Trader | MSP Procurement |
  | Block 15 | Access to technical advice / extension services | Source (Govt extension, KVK, Agri Uni, FPO, Media); Topic (seeds, fertilizer, plant protection) | Agricultural Extension |

  **What is NOT captured in Schedule 33.1:**
  * ❌ **PM-KISAN:** Not surveyed (survey designed in 2018; PM-KISAN was announced in Feb 2019).
  * ❌ **Irrigation Subsidies:** No program-level indicator for PMKSY (Per Drop More Crop) or Karnataka state micro-irrigation subsidies (only asset ownership of drip/sprinkler is asked).
  * ❌ **Farm Mechanization Subsidies:** No variable for SMAM (Sub-Mission on Agricultural Mechanization) or custom hiring center schemes (only physical possession of tractors/implements is asked).
  * ❌ **Horticulture / Specialty Subsidies:** Zero coverage of MIDH, PKVY (organic farming), or National Bamboo Mission.
  * ❌ **Karnataka State Welfare Schemes:** Zero coverage of Krishi Bhagya, Ganga Kalyana, Raitha Siri, or Raitha Sanjeevini.

#### Q5: Are those scheme variables specific enough to become ML targets? (The Decisive Question)
* **Answer:** **NO. Case A cannot be salvaged by NSS 77th Round.**

**Why this fails as an ML recommendation target:**
1. **Grossly insufficient scheme space:** A recommendation system cannot be trained when only three agricultural schemes (KCC, PMFBY, Soil Health Card) are labeled in the entire dataset. Recommending between 3 universally available programs does not constitute personalized multi-scheme recommendation.
2. **Missing key intervention domains:** The catalog lacks any record of mechanization subsidies, micro-irrigation subsidies, horticulture schemes, post-harvest infrastructure, or state-specific benefits.
3. **Almost universal eligibility vs. selective recommendation:** KCC and Soil Health Cards are broadly targeted to all landholding cultivators; whether a household held them in 2019 reflects administrative camp coverage and bank branch density, not personalized scheme relevance.
4. **Historical uptake ≠ normative recommendation:** Past survey uptake is confounded by local awareness, historical debt status, and administrative friction. Training a supervised classifier on "historical access" would teach the model past systemic exclusion patterns rather than optimal farmer-benefit matching.

---

## Section 6: Definitive Decision on Case A, B, and C

### Empirical Conclusion on Case A (Supervised Learning on Real Historical Scheme Outcomes)

```
PM-KISAN public OGD:        ❌ Village/gender count data only
PMFBY dashboard:            ❌ Aggregate state/crop statistics only
FRUITS Karnataka:           ❌ Private administrative portal (protected PII)
KCC Call Center Data:       ❌ Query text & categories only; no scheme outcomes
NSS 77th Round (SAS):       ❌ Only 3 schemes (KCC, PMFBY, SHC); no multi-scheme targets
─────────────────────────────────────────────────────────────────────────────
CASE A OUTCOME:             🔴 DEFINITIVELY CLOSED — Public ground truth does not exist.
```

> [!CAUTION]
> **Academic Integrity Ruling for Viva and Project Report:**  
> No legitimate, public, individual-level dataset exists in India that connects detailed farmer profiles to multi-scheme subsidy enrollment or recommendation outcomes. Any project claiming to have trained a supervised "Scheme Recommender" on public farmer outcome data is either misrepresenting aggregate counts, learning over a trivial 2–3 scheme binary target, or training on unverified synthetic outputs. We will state this finding openly in the report as an empirical contribution.

---

## Section 7: The Path Forward — Case B & Repurposed KCC

With Case A closed, the project moves to a scientifically rigorous, defensible two-pillar research design:

### 1. Case B — Expert-Annotated Scenario Benchmark
Rather than calling human expert evaluation "synthetic labels," we establish:
**Case B — Expert-Annotated Scenario Benchmark** (Human-in-the-Loop Ground Truth).

* **Concept:** Construct a realistic set of farmer scenarios grounded in the distributions observed in NSS 77th Round and KCC data, and collect independent relevance judgments from qualified agricultural domain experts.
* **Benchmark Architecture:**
  * **50–100 Farmer Scenarios:** Derived across Karnataka's agro-climatic zones (e.g., dryland farmer in Raichur, arecanut grower in Shivamogga, smallholder horticulture farmer in Kolar, coastal paddy farmer in Udupi).
  * **Candidate Schemes (10–15):** Curated from official state and central scheme guidelines (PMFBY, PMKSY, KCC, SMAM, Krishi Bhagya, Ganga Kalyana, etc.).
  * **Expert Annotators (2–3):** Agricultural extension officers, KVK scientists, or UAS (University of Agricultural Sciences) agronomists.
  * **Scoring Rubric (0–3 scale):**
    * `3` = Highly Relevant & Immediate Priority (meets all criteria, addresses acute need)
    * `2` = Relevant & Eligible (clear benefit, but secondary priority)
    * `1` = Marginally Relevant / Technically Eligible (weak fit with immediate requirements)
    * `0` = Ineligible or Irrelevant
  * **Statistical Agreement Measurement:** Compute Fleiss' Kappa / Cohen's Kappa or Kendall's W to prove inter-annotator reliability before forming consensus ground truth.
  * **ML Role:** Evaluates ranking algorithms (e.g., RankNet / XGBoost Ranker / multi-attribute utility scoring) against expert ground truth.

### 2. Repurposing KCC: Farmer Intent & Query Understanding
KCC is not discarded. It is repurposed for what it actually contains: **authentic farmer language and real information queries.**

* **Role:** A farmer does not arrive at a system thinking "I need Scheme Code 14B." They say:
  > *"Drip irrigation ge subsidy sigutta?"* (Is subsidy available for drip irrigation?)  
  > *"Borewell failure aagide, solar pump scheme ideya?"* (Borewell failed, is there a solar pump scheme?)  
  > *"Arecanut yellow leaf disease, crop compensation how to apply?"*
* **Two-Part System Pipeline:**
  ```
                     FARMER
                       ↓
               Query / Profile
                  ↙         ↘
       [Part 1: NLP Intent]   [Farmer Profile Features]
         (Trained on KCC)       (Land, Crop, Category, District)
                  ↘         ↙
             Candidate Schemes
                     ↓
       [Stage 1: Eligibility Engine]
         (Deterministic Rules on Scheme Master)
                     ↓
       [Stage 2: Relevance Ranker]
         (ML Ranker evaluated against Case B Benchmark)
                     ↓
             Top-K Recommendations
  ```

---

## Section 8: Action Items & Milestone Update

| Priority | Task | Status | Output / Deliverable |
|---|---|---|---|
| ~~P1~~ | ~~NSS 77th Round Schedule 33.1 inspection~~ | ✅ Completed | Sections 5 & 6 updated; Case A closed |
| **P1** | Build the 10-Scheme Master Curation ([Phase 1 requirement]) | ⏳ Next | `data/schemes/scheme_master.json` + rule sheets |
| **P1** | Specify Case B Farmer Scenario Templates (50–100 profiles) | ⏳ Next | `research/dataset_research/case_b_scenario_spec.md` |
| **P2** | Define KCC Query Intent Taxonomy (mapping 44 KCC categories → scheme intent) | ⏳ Planned | `research/dataset_research/kcc_intent_mapping.md` |
| **P2** | Draft Expert Annotation Protocol & Rubric (for KVK / UAS reviewers) | ⏳ Planned | `research/evaluation/expert_annotation_protocol.md` |

---

*Document last updated: September 15, 2026*  
*Investigation performed by: Project Team — direct official microdata and codebook audit*

