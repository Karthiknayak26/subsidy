# Benchmark v1.0.4 — Blinded Expert Relevance Annotation Dossier

**Benchmark Version:** `v1.0.4`  
**Annotation Protocol:** `annotation-protocol-v1.1`  
**Target Benchmark:** S011–S070 (60 production scenarios across 10 agro-climatic zones)  
**Calibration Set:** S001–S010 (strictly partitioned and held separate)  

---

## 1. Instructions & Rating Rubric (0–3 Scale)

Please evaluate each candidate scheme presented under **Section A** based *strictly* on the farmer's stated need, crop, and farm asset profile.
Operational portal availability has been blinded for this phase. Do not lower or adjust scores based on whether an application window is open or closed.

| Score | Rating Level | Definition & Clinical Decision Rule |
|:---:|:---|:---|
| **3** | **Highly Relevant / High Priority** | Directly addresses the farmer's primary stated need with immediate, high-impact benefit. Should be a top recommendation. |
| **2** | **Relevant / Secondary Priority** | Provides genuine practical benefit and valuable secondary support, but does not directly solve the immediate acute crisis. |
| **1** | **Marginally Relevant / Low Priority** | Technically applicable and eligible, but offers minor, distant, or tangential value in the current context. |
| **0** | **Irrelevant / Not Useful** | Despite passing statutory eligibility, provides no meaningful practical benefit given the farmer's specific circumstances. |

### Protocol v1.1 Guardrail Rules:
1. **Infrastructure & Civil Works Complexity:** A scheme must NOT receive a high score solely because it includes an eligible sub-component. If obtaining the benefit requires major unrequested civil works (e.g. farm pond excavation) that reduce practical usability, score **1** or **0**.
2. **Income Support vs. Repayable Credit:** Repayable crop credit / loans (e.g. KCC-MISS, PACS credit) must NOT receive score **3** when the farmer's stated need is purely non-repayable income relief (`INCOME_SUPPORT`), unless the farmer explicitly requests borrowing or loan rescheduling.
3. **Section B (Provisional Schemes):** Section B schemes (e.g. PACS zero-interest credit requiring annual GO verification, unconfirmed title cases) are **strictly excluded from numerical scoring (0–3)**. They appear only in the qualitative review section.

---

## 2. Farmer Scenarios & Section A Candidate Schemes (Blinded)

### Scenario S011 (Zone 1 — North Eastern Transition Zone)
- **Location:** Bidar District (Zone 1)
- **Social Category & Tenure:** OBC (2A) | Tenure: Registered Owner
- **Landholding & Land Type:** 1.8 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Redgram, Soybean
- **Water Infrastructure:** Rainfed Dryland (No borewell or open well present) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`CROP_INSURANCE`**
- **Farmer Narrative / Stated Circumstance:** *"Redgram crop in Aurad taluk, Bidar suffering from severe pod borer and wilt attack; flower dropping observed; need immediate compensation claim procedure under PMFBY and advisory."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Redgram, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_DEVARAJ_URS` | **Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on encoded rules, but scheme record is PROVISIONAL in registry. Governance safeguard places determination in Section B as REQUIRES_VERIFICATION without numerical scoring. |

---

### Scenario S012 (Zone 1 — North Eastern Transition Zone)
- **Location:** Kalaburagi District (Zone 1)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 3.0 acres (Small (2.5-5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Maize, Redgram
- **Water Infrastructure:** Borewell (Non-energized) | Power/Grid: UNENERGIZED_OFF_GRID
- **Existing Assets:** Borewell (Non-energized)
- **PRIMARY STATED NEED:** **`SOLAR_PUMP_INSTALLATION`**
- **Farmer Narrative / Stated Circumstance:** *"Drilled 400ft borewell in Aland taluk, Kalaburagi with good yield but no electricity line nearby; GESCOM waiting list is long; need standalone solar pump subsidy under PM-KUSUM Component B."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | | |
| `SCH006` | **PM-KUSUM Component B (Standalone Solar Agriculture Pumps)** | Qualifies for PM-KUSUM Component B standalone solar agriculture pump (60% subsidy up to 7.5 HP). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Maize, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S013 (Zone 1 — North Eastern Transition Zone)
- **Location:** Bidar District (Zone 1)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 5.0 acres (Small (2.5-5 acres)) | Land Type: Irrigated (Canal)
- **Crops:** Sugarcane
- **Water Infrastructure:** Irrigated (Canal) — Karanja Command Area | Power/Grid: NONE
- **Existing Assets:** Canal Water Delivery Siphon / Furrow Network
- **PRIMARY STATED NEED:** **`SOIL_HEALTH_AND_FERTILIZER`**
- **Farmer Narrative / Stated Circumstance:** *"Sugarcane crop in Karanja command area, Bhalki taluk showing leaf chlorosis and stunted cane girth; excessive urea applied over past 3 seasons; need soil testing and balanced NPK micronutrient advisory under Soil Health Card."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Sugarcane, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S014 (Zone 1 — North Eastern Transition Zone)
- **Location:** Kalaburagi District (Zone 1)
- **Social Category & Tenure:** ST | Tenure: Registered Owner
- **Landholding & Land Type:** 2.2 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Soybean, Redgram
- **Water Infrastructure:** Rainfed Dryland (No operational water source) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`PRODUCTION_CREDIT`**
- **Farmer Narrative / Stated Circumstance:** *"Marginal tribal farmer in Sedam, Kalaburagi preparing for Kharif soybean sowing; need short-term crop loan for seeds and fertilizer; want to know interest subvention rate between Grameena Bank KCC and local PACS cooperative society."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Soybean, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_VALMIKI` | **Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on encoded rules, but scheme record is PROVISIONAL in registry. Governance safeguard places determination in Section B as REQUIRES_VERIFICATION without numerical scoring. |

---

### Scenario S015 (Zone 1 — North Eastern Transition Zone)
- **Location:** Bidar District (Zone 1)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 1.5 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Jowar, Bengalgram
- **Water Infrastructure:** Rainfed Dryland (No operational water source) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`INCOME_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"Dryland jowar in Humnabad taluk, Bidar facing severe moisture stress; family has acute cash shortage for daily food and medicine; need non-repayable government cash assistance or pension relief, cannot take more bank debt."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |
| `SCH010_AMBEDKAR` | **Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC)** | Qualifies for Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) under Individual Borewell Route. 100% subsidized borewell, pump, and electrification package. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Jowar, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S016 (Zone 1 — North Eastern Transition Zone)
- **Location:** Kalaburagi District (Zone 1)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 4.5 acres (Small (2.5-5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Redgram
- **Water Infrastructure:** None (Completely rainfed dryland; seeking groundwater exploration) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`BOREWELL_IRRIGATION`**
- **Farmer Narrative / Stated Circumstance:** *"SC dryland farmer in Afzalpur taluk, Kalaburagi with 4.5 acres dryland; completely dependent on erratic rainfall for redgram; have no borewell or open well; need free borewell drilling and pump under Ganga Kalyana Scheme Dr. B. R. Ambedkar Corporation."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |
| `SCH010_AMBEDKAR` | **Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC)** | Qualifies for Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) under Individual Borewell Route. 100% subsidized borewell, pump, and electrification package. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Redgram, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S017 (Zone 2 — North Eastern Dry Zone)
- **Location:** Yadgir District (Zone 2)
- **Social Category & Tenure:** ST | Tenure: Registered Owner
- **Landholding & Land Type:** 6.0 acres (Medium (5-10 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Cotton, Redgram
- **Water Infrastructure:** Rainfed (None) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`CROP_INSURANCE`**
- **Farmer Narrative / Stated Circumstance:** *"Cotton crop in Shorapur taluk, Yadgir severely infested by pink bollworm and whitefly; boll rot observed following dry-spell; enrolled in PMFBY via Samrakshane portal; need claim assessment procedure and localized calamity survey details."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Cotton, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S018 (Zone 2 — North Eastern Dry Zone)
- **Location:** Raichur District (Zone 2)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 2.0 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Sunflower
- **Water Infrastructure:** Rainfed (None) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`INCOME_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"Retired non-MTS state board employee with 2.0 acres rainfed sunflower in Manvi taluk, Raichur; receiving exactly ₹10,000 per month pension; registered on FRUITS portal but PM-KISAN 17th installment rejected at state nodal verification; need reason for rejection and grievance procedure."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Sunflower, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S019 (Zone 2 — North Eastern Dry Zone)
- **Location:** Kalaburagi District (Zone 2)
- **Social Category & Tenure:** OBC (2A) | Tenure: Registered Owner
- **Landholding & Land Type:** 1.2 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Bajra, Redgram
- **Water Infrastructure:** Rainfed Catchment (No borewell or pond) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`RAINWATER_HARVESTING`**
- **Farmer Narrative / Stated Circumstance:** *"Marginal Kuruba (OBC 2A) farmer with 1.2 acres dryland bajra in Afzalpur taluk, Kalaburagi; recurrent dry spells destroying crops; need 80% subsidy for constructing farm pond (Krishi Honda) with polythene lining and diesel pump under Krishi Bhagya."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Bajra is absent from static crop whitelist. In this agro-climatic zone, Bajra is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_DEVARAJ_URS` | **Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on encoded rules, but scheme record is PROVISIONAL in registry. Governance safeguard places determination in Section B as REQUIRES_VERIFICATION without numerical scoring. |

---

### Scenario S020 (Zone 2 — North Eastern Dry Zone)
- **Location:** Yadgir District (Zone 2)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 6.5 acres (Medium (5-10 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Redgram, Bajra
- **Water Infrastructure:** Borewell (Unconfirmed) | Power/Grid: UNKNOWN
- **Existing Assets:** Borewell (Non-energized)
- **PRIMARY STATED NEED:** **`SOLAR_PUMP_INSTALLATION`**
- **Farmer Narrative / Stated Circumstance:** *"SC farmer with 6.5 acres redgram in Yadgir taluk; drilled borewell 6 months ago with yield but grid connection status from GESCOM is unconfirmed; tax assessment documentation not submitted; need standalone solar pump subsidy under PM-KUSUM Component B."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Redgram, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S021 (Zone 2 — North Eastern Dry Zone)
- **Location:** Raichur District (Zone 2)
- **Social Category & Tenure:** Minority (Muslim) | Tenure: Registered Owner
- **Landholding & Land Type:** 4.0 acres (Small (2.5-5 acres)) | Land Type: Irrigated (Canal)
- **Crops:** Cotton
- **Water Infrastructure:** Canal Distributary (Tungabhadra Left Bank Canal) | Power/Grid: NONE
- **Existing Assets:** Canal Siphon / Field Channels, Knapsack Manual Sprayer
- **PRIMARY STATED NEED:** **`FARM_MECHANIZATION`**
- **Farmer Narrative / Stated Circumstance:** *"Cotton farmer with 4.0 acres canal-irrigated land in Sindhanoor taluk, Raichur; facing severe sucking pest and bollworm pressure; manual spraying is labour intensive and slow; need subsidy under SMAM for purchasing a power sprayer / boom sprayer."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Cotton, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S022 (Zone 2 — North Eastern Dry Zone)
- **Location:** Kalaburagi District (Zone 2)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 1.8 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Sunflower, Bengalgram
- **Water Infrastructure:** Rainfed (None) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`SOIL_HEALTH_AND_FERTILIZER`**
- **Farmer Narrative / Stated Circumstance:** *"Marginal farmer with 1.8 acres dryland black cotton soil in Jewargi taluk, Kalaburagi preparing for sunflower/Bengalgram sowing; yield has dropped over last 2 years despite DAP application; need soil sample testing and Soil Health Card nutrient recommendations."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Sunflower, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S023 (Zone 3 — Northern Dry Zone)
- **Location:** Vijayapura District (Zone 3)
- **Social Category & Tenure:** Minority (Muslim) | Tenure: Registered Owner
- **Landholding & Land Type:** 3.5 acres (Small (2.5-5 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Pomegranate
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected), Drip Irrigation (Installed)
- **PRIMARY STATED NEED:** **`MICRO_IRRIGATION_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"Pomegranate grower in Indi taluk, Vijayapura with 3.5 acres under functional borewell; existing lateral drip lines damaged by hard water salinity; applying for capital subsidy under PMKSY-PDMC for 1.41 ha inline drip replacement; need online portal procedure."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH007` | **Mission for Integrated Development of Horticulture (MIDH)** | Qualifies for MIDH Protected Cultivation subsidy (50% cost norm for Polyhouse / Shade Net up to 4,000 m²). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Pomegranate is absent from static crop whitelist. In this agro-climatic zone, Pomegranate is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S024 (Zone 3 — Northern Dry Zone)
- **Location:** Bagalkot District (Zone 3)
- **Social Category & Tenure:** ST | Tenure: Registered Owner
- **Landholding & Land Type:** 2.0 acres (Marginal (< 2.5 acres)) | Land Type: Irrigated (Canal)
- **Crops:** Maize, Bengalgram
- **Water Infrastructure:** Borewell (Non-energized) | Power/Grid: UNENERGIZED_OFF_GRID
- **Existing Assets:** Borewell (Non-energized)
- **PRIMARY STATED NEED:** **`SOLAR_PUMP_INSTALLATION`**
- **Farmer Narrative / Stated Circumstance:** *"Marginal ST farmer in Badami taluk, Bagalkot with 2.0 acres; privately sunk borewell has water but no electric line nearby; HESCOM grid waiting list is over 2 years; need 60% subsidy for standalone solar pump under PM-KUSUM Component B."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH006` | **PM-KUSUM Component B (Standalone Solar Agriculture Pumps)** | Qualifies for PM-KUSUM Component B standalone solar agriculture pump (60% subsidy up to 7.5 HP). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Maize, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S025 (Zone 3 — Northern Dry Zone)
- **Location:** Gadag District (Zone 3)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 1.5 acres (Marginal (< 2.5 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Onion, Chilli
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected), Drip Irrigation (Installed)
- **PRIMARY STATED NEED:** **`PROTECTED_HORTICULTURE`**
- **Farmer Narrative / Stated Circumstance:** *"SC marginal farmer in Ron taluk, Gadag with 1.5 acres borewell-irrigated onion and chilli; existing drip installed; heavy sunscald and thrips damaging crops; applying for 50% capital subsidy under MIDH for 1,000 m² shade net structure; need DPR guidelines."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH007` | **Mission for Integrated Development of Horticulture (MIDH)** | Qualifies for MIDH Protected Cultivation subsidy (50% cost norm for Polyhouse / Shade Net up to 4,000 m²). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Onion, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S026 (Zone 3 — Northern Dry Zone)
- **Location:** Koppal District (Zone 3)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 2.5 acres (Small (2.5-5 acres)) | Land Type: Irrigated (Canal)
- **Crops:** Bengalgram, Paddy
- **Water Infrastructure:** Canal Command (Tungabhadra Left Bank Canal) | Power/Grid: NONE
- **Existing Assets:** Canal Siphon / Furrow Network
- **PRIMARY STATED NEED:** **`PRODUCTION_CREDIT`**
- **Farmer Narrative / Stated Circumstance:** *"Tenant cultivator farming 2.5 acres canal land in Gangavathi, Koppal under oral lease agreement; preparing for Rabi Bengalgram; no land title RTC in my name; applying for short-term crop loan at Prathama Grameena Bank; need tenant KCC eligibility rules."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Bengalgram, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE under RBI/NABARD tenant borrower category, but oral tenancy documentation and bank tenant crop-loan eligibility require verification. Governance safeguard routes determination to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S027 (Zone 3 — Northern Dry Zone)
- **Location:** Vijayapura District (Zone 3)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 6.5 acres (Medium (5-10 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Pomegranate, Bajra
- **Water Infrastructure:** Rainfed Catchment | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`RAINWATER_HARVESTING`**
- **Farmer Narrative / Stated Circumstance:** *"SC farmer with 6.5 acres dryland pomegranate and bajra in Muddebihal taluk, Vijayapura; facing acute dry spells and water distress; applying for Krishi Honda farm pond with 90% SC subsidy under Krishi Bhagya; need taluk office sanction timeline."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Pomegranate is absent from static crop whitelist. In this agro-climatic zone, Pomegranate is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S028 (Zone 3 — Northern Dry Zone)
- **Location:** Bagalkot District (Zone 3)
- **Social Category & Tenure:** OBC (2A) | Tenure: Registered Owner
- **Landholding & Land Type:** 10.0 acres (Medium (5-10 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Onion, Sorghum
- **Water Infrastructure:** None (Dryland kushki) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`BOREWELL_IRRIGATION`**
- **Farmer Narrative / Stated Circumstance:** *"OBC (2A Kuruba) farmer in Bilagi taluk, Bagalkot with 10.0 acres dryland; individual borewell rejected due to > 5.0 acre ceiling; joined 2 adjacent small OBC farmers to pool 9.0 contiguous dryland acres for community borewell under D. Devaraj Urs Corporation; need joint application procedure."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Onion, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH005` | **Krishi Bhagya Yojana** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE due to string-matching mismatch ('Bagalkote' vs 'Bagalkot'). Bagalkot is officially a notified Bayaluseeme dryland district under GoK Krishi Bhagya guidelines. Governance presentation routes to REQUIRES_VERIFICATION pending taluk-level notification check. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_DEVARAJ_URS` | **Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on encoded community route rules (9.0 ac, 3 beneficiaries), but scheme record is PROVISIONAL in registry. Governance safeguard places determination in Section B as REQUIRES_VERIFICATION without numerical scoring. |

---

### Scenario S029 (Zone 4 — Central Dry Zone)
- **Location:** Chitradurga District (Zone 4)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 2.0 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Groundnut, Redgram
- **Water Infrastructure:** None (Dryland kushki) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`BOREWELL_IRRIGATION`**
- **Farmer Narrative / Stated Circumstance:** *"SC marginal dryland farmer with 2.0 acres rainfed groundnut in Challakere taluk, Chitradurga; facing acute groundwater drought and crop failure; applying for free individual borewell package under Dr. B.R. Ambedkar Development Corporation Ganga Kalyana; need offline application checklist."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Groundnut, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_AMBEDKAR` | **Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on demographic land interval [1.5, 5.0] ac and encoded income ceiling, but parcel lacks recorded evidence of perennial water source adjacency, and the applicable Chitradurga district income order requires administrative confirmation. Governance presentation routes to REQUIRES_VERIFICATION in Section B without numerical scoring. |

---

### Scenario S030 (Zone 4 — Central Dry Zone)
- **Location:** Davanagere District (Zone 4)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 3.8 acres (Small (2.5-5 acres)) | Land Type: Irrigated (Canal)
- **Crops:** Maize, Paddy
- **Water Infrastructure:** Borewell (Non-energized) | Power/Grid: UNENERGIZED_OFF_GRID
- **Existing Assets:** Borewell (Non-energized)
- **PRIMARY STATED NEED:** **`SOLAR_PUMP_INSTALLATION`**
- **Farmer Narrative / Stated Circumstance:** *"Small farmer with 3.8 acres in Harihar taluk, Davanagere; tail-end canal command with highly erratic releases; drilled private borewell 4 months ago but BESCOM electric line is 1.2 km away; applying for 60% subsidy for 5 HP standalone solar pump under PM-KUSUM Component B; need quotation format."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH006` | **PM-KUSUM Component B (Standalone Solar Agriculture Pumps)** | Qualifies for PM-KUSUM Component B standalone solar agriculture pump (60% subsidy up to 7.5 HP). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Maize, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S031 (Zone 4 — Central Dry Zone)
- **Location:** Tumakuru District (Zone 4)
- **Social Category & Tenure:** ST | Tenure: Registered Owner
- **Landholding & Land Type:** 1.8 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Ragi, Fieldbean
- **Water Infrastructure:** Rainfed Catchment | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`RAINWATER_HARVESTING`**
- **Farmer Narrative / Stated Circumstance:** *"ST marginal dryland farmer with 1.8 acres rainfed ragi in Pavagada taluk, Tumakuru; severe recurring drought; applying for Krishi Honda farm pond under Krishi Bhagya with 90% ST subsidy; also asking about Valmiki corporation borewell scheme eligibility."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Ragi, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_VALMIKI` | **Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on encoded rules, but scheme record is PROVISIONAL in registry. Governance safeguard places determination in Section B as REQUIRES_VERIFICATION without numerical scoring. |

---

### Scenario S032 (Zone 4 — Central Dry Zone)
- **Location:** Chitradurga District (Zone 4)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 2.5 acres (Small (2.5-5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Groundnut, Onion
- **Water Infrastructure:** Rainfed (None) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`INCOME_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"Farmer with exactly 2.5 acres dryland in Hiriyur, Chitradurga; filed ITR-4 last assessment year with taxable business income; facing crop loss; asking why PM-KISAN ₹6,000 installment was rejected by village accountant; also asking about KCC crop loan eligibility."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Groundnut, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S033 (Zone 4 — Central Dry Zone)
- **Location:** Davanagere District (Zone 4)
- **Social Category & Tenure:** OBC (2A) | Tenure: Registered Owner
- **Landholding & Land Type:** 7.5 acres (Medium (5-10 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Arecanut, Banana
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected)
- **PRIMARY STATED NEED:** **`FARM_MECHANIZATION`**
- **Farmer Narrative / Stated Circumstance:** *"OBC (2A) planter with 7.5 acres borewell-irrigated arecanut in Channagiri taluk, Davanagere; facing acute skilled climber labor shortage; applying for 40-50% subsidy under SMAM for arecanut dehusker and power sprayer; need approved dealer list."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Arecanut, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S034 (Zone 4 — Central Dry Zone)
- **Location:** Tumakuru District (Zone 4)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 11.0 acres (Large (> 10 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Maize, Groundnut
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected)
- **PRIMARY STATED NEED:** **`MICRO_IRRIGATION_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"Large farmer with 11.0 acres borewell-irrigated land in Tiptur, Tumakuru; expanding commercial maize cultivation; applying for micro-irrigation subsidy under PMKSY-PDMC for 4.45 hectares; need clarification on 5.0 ha statutory ceiling and subsidy slab."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Maize, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S035 (Zone 5 — Eastern Dry Zone)
- **Location:** Kolar District (Zone 5)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 1.5 acres (Marginal (< 2.5 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Tomato, Capsicum
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected), Drip Irrigation (Installed)
- **PRIMARY STATED NEED:** **`PROTECTED_HORTICULTURE`**
- **Farmer Narrative / Stated Circumstance:** *"SC marginal horticulture farmer with 1.5 acres borewell-irrigated land in Srinivaspur taluk, Kolar; cultivating hybrid tomatoes and capsicum with drip irrigation; applying for 50% capital subsidy under MIDH for 1,000 sq m naturally ventilated polyhouse structure; need technical specification and subsidy quotation guidelines."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH007` | **Mission for Integrated Development of Horticulture (MIDH)** | Qualifies for MIDH Protected Cultivation subsidy (50% cost norm for Polyhouse / Shade Net up to 4,000 m²). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Tomato, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S036 (Zone 5 — Eastern Dry Zone)
- **Location:** Chikkaballapura District (Zone 5)
- **Social Category & Tenure:** Minority | Tenure: Registered Owner
- **Landholding & Land Type:** 3.0 acres (Small (2.5-5 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Mulberry, Vegetables
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected), Silkworm Rearing House
- **PRIMARY STATED NEED:** **`PRODUCTION_CREDIT`**
- **Farmer Narrative / Stated Circumstance:** *"Minority small sericulture farmer with 3.0 acres irrigated mulberry garden in Sidlaghatta, Chikkaballapura; seeking working capital credit for dfl silkworm seed purchase and disinfection; inquiring about Central KCC crop loan at 4% interest subvention vs Karnataka PACS 0% interest cooperative loan."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Mulberry is absent from static crop whitelist. In this agro-climatic zone, Mulberry is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S037 (Zone 5 — Eastern Dry Zone)
- **Location:** Bengaluru Rural District (Zone 5)
- **Social Category & Tenure:** ST | Tenure: Registered Owner
- **Landholding & Land Type:** 2.5 acres (Small (2.5-5 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Mango
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected)
- **PRIMARY STATED NEED:** **`MICRO_IRRIGATION_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"ST small orchard farmer with exactly 2.5 acres borewell-irrigated Alphonso mango plantation in Doddaballapura, Bengaluru Rural; applying for drip irrigation subsidy for 1.01 hectares under PMKSY-PDMC; seeking quotation and subsidy rate confirmation for ST category."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Mango is absent from static crop whitelist. In this agro-climatic zone, Mango is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S038 (Zone 5 — Eastern Dry Zone)
- **Location:** Kolar District (Zone 5)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 1.2 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Tomato
- **Water Infrastructure:** None (Rainfed dryland) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`INCOME_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"Marginal dryland tomato farmer with 1.2 acres in Bangarapet, Kolar; suffered complete crop loss and price collapse where tomatoes fetched ₹2/kg against ₹12/kg cost of cultivation; facing severe household distress and mounting input dealer debt; urgently seeking non-repayable income support and DBT relief under PM-KISAN."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Tomato, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S039 (Zone 5 — Eastern Dry Zone)
- **Location:** Chikkaballapura District (Zone 5)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 2.0 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Ragi, Groundnut
- **Water Infrastructure:** None (Rainfed dryland) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`CROP_INSURANCE`**
- **Farmer Narrative / Stated Circumstance:** *"SC marginal dryland farmer with 2.0 acres rainfed ragi in Bagepalli, Chikkaballapura; acquired land title strictly via succession upon death of father (registered Death Certificate and Bhoomi mutation extract Form 12); applying for PMFBY crop insurance against drought and seeking PM-KISAN registration; inquiring whether succession upon death is exempt from post-Feb 2019 cut-off."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Ragi, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_AMBEDKAR` | **Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on demographic land interval [1.5, 5.0] ac and encoded income ceiling, but parcel lacks recorded evidence of perennial water source adjacency, and the applicable district income order requires administrative confirmation. Governance presentation routes to REQUIRES_VERIFICATION in Section B without numerical scoring. |

---

### Scenario S040 (Zone 5 — Eastern Dry Zone)
- **Location:** Bengaluru Rural District (Zone 5)
- **Social Category & Tenure:** OBC (2A) | Tenure: Registered Owner
- **Landholding & Land Type:** 5.0 acres (Small (2.5-5 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Mango, Vegetables
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected)
- **PRIMARY STATED NEED:** **`FARM_MECHANIZATION`**
- **Farmer Narrative / Stated Circumstance:** *"OBC small farmer with exactly 5.0 acres borewell-irrigated mango and intercropped vegetable orchard in Hosakote, Bengaluru Rural; applying for 50% subsidy under SMAM for power tiller and high-pressure orchard sprayer; need tractor RC requirements and subsidy slab verification."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Mango is absent from static crop whitelist. In this agro-climatic zone, Mango is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S041 (Zone 6 — Southern Dry Zone)
- **Location:** Mandya District (Zone 6)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 6.5 acres (Medium (5-10 acres)) | Land Type: Irrigated (Canal)
- **Crops:** Sugarcane, Paddy
- **Water Infrastructure:** Canal & Storage Tank | Power/Grid: NONE
- **Existing Assets:** Canal Outlet, Farm Storage Tank, Diesel Pump Set
- **PRIMARY STATED NEED:** **`MICRO_IRRIGATION_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"General category medium sugarcane grower with 6.5 acres canal command land in Maddur taluk, Mandya; facing intermittent rotational canal supply from Visvesvaraya canal; applying for drip irrigation subsidy for 2.50 hectares under PMKSY-PDMC; seeking quotation requirements and water source verification protocol."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Sugarcane, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S042 (Zone 6 — Southern Dry Zone)
- **Location:** Mysuru District (Zone 6)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 3.5 acres (Small (2.5-5 acres)) | Land Type: Wetland/valley
- **Crops:** Paddy, Pulses
- **Water Infrastructure:** Canal Flow | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`CROP_INSURANCE`**
- **Farmer Narrative / Stated Circumstance:** *"SC tenant farmer cultivating 3.5 acres wetland paddy in T. Narasipura, Mysuru on oral lease agreement without registered title deed; seeking crop insurance coverage under PMFBY against flood and pest infestation; inquiring about tenant farmer enrollment documents and landlord declaration format."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Paddy, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE under RBI/NABARD tenant borrower category, but oral tenancy documentation and bank tenant crop-loan eligibility require verification. Governance safeguard routes determination to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S043 (Zone 6 — Southern Dry Zone)
- **Location:** Chamarajanagar District (Zone 6)
- **Social Category & Tenure:** ST | Tenure: Registered Owner
- **Landholding & Land Type:** 1.8 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Banana, Turmeric
- **Water Infrastructure:** None (Dryland kushki) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`BOREWELL_IRRIGATION`**
- **Farmer Narrative / Stated Circumstance:** *"ST marginal dryland farmer with 1.8 acres rainfed land in Gundlupet, Chamarajanagar; planning to cultivate tissue-culture banana but facing complete lack of irrigation; applying for free individual borewell and submersible pump package under Karnataka Maharshi Valmiki ST Development Corporation Ganga Kalyana scheme; need offline application checklist."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Banana is absent from static crop whitelist. In this agro-climatic zone, Banana is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_VALMIKI` | **Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on encoded rules, but scheme record is PROVISIONAL in registry, and parcel lacks recorded evidence of perennial water source adjacency. Governance safeguard places determination in Section B as REQUIRES_VERIFICATION without numerical scoring. |

---

### Scenario S044 (Zone 6 — Southern Dry Zone)
- **Location:** Mandya District (Zone 6)
- **Social Category & Tenure:** OBC (2A) | Tenure: Registered Owner
- **Landholding & Land Type:** 2.0 acres (Marginal (< 2.5 acres)) | Land Type: Wetland/valley
- **Crops:** Paddy
- **Water Infrastructure:** Canal Flow | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`INCOME_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"OBC tenant farmer cultivating 2.0 acres wetland paddy in Malavalli, Mandya on oral lease; suffered acute crop failure and submergence loss; facing severe debt distress and requesting non-repayable cash assistance under PM-KISAN; inquiring whether landless tenant farmers can apply."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Paddy, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE under RBI/NABARD tenant borrower category, but oral tenancy documentation and bank tenant crop-loan eligibility require verification. Governance safeguard routes determination to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S045 (Zone 6 — Southern Dry Zone)
- **Location:** Mysuru District (Zone 6)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 1.5 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Ragi, Cowpea
- **Water Infrastructure:** Rainfed Catchment | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`RAINWATER_HARVESTING`**
- **Farmer Narrative / Stated Circumstance:** *"SC marginal dryland farmer with 1.5 acres rainfed ragi in H.D. Kote, Mysuru; dependent entirely on erratic rainfall; applying for Krishi Honda (farm pond) with polythene lining and diesel pump package under Krishi Bhagya; seeking subsidy percentage and RSK application procedure."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Ragi, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_AMBEDKAR` | **Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on demographic land interval [1.5, 5.0] ac and encoded income ceiling, but parcel lacks recorded evidence of perennial water source adjacency and the applicable Mysuru rural family income ceiling remains an unverified administrative policy dependency. Governance presentation routes to REQUIRES_VERIFICATION in Section B without numerical scoring. |

---

### Scenario S046 (Zone 6 — Southern Dry Zone)
- **Location:** Chamarajanagar District (Zone 6)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 7.0 acres (Medium (5-10 acres)) | Land Type: Irrigated (Canal)
- **Crops:** Sugarcane, Banana
- **Water Infrastructure:** Canal Command | Power/Grid: NONE
- **Existing Assets:** Canal Sump, Electric Pump Set
- **PRIMARY STATED NEED:** **`SOIL_HEALTH_AND_FERTILIZER`**
- **Farmer Narrative / Stated Circumstance:** *"General category sugarcane grower with 7.0 acres canal command land in Kollegal, Chamarajanagar; observing declining sugarcane tonnage and soil salinization; applying for Soil Health Card diagnostic testing and micronutrient advisory; inquiring about RSK soil sample collection protocol."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Sugarcane, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S047 (Zone 7 — Southern Transition Zone)
- **Location:** Hassan District (Zone 7)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 5.5 acres (Medium (5-10 acres)) | Land Type: Irrigated (Canal)
- **Crops:** Maize, Potato
- **Water Infrastructure:** Canal Command | Power/Grid: NONE
- **Existing Assets:** Canal Outlet, Intermediate Storage Sump, Diesel Engine Pump
- **PRIMARY STATED NEED:** **`FARM_MECHANIZATION`**
- **Farmer Narrative / Stated Circumstance:** *"General category medium maize farmer with 5.5 acres canal command in Holenarasipura, Hassan; seeking 40% capital subsidy on multi-crop power thresher and tractor-mounted disc plough under Sub-Mission on Agricultural Mechanization (SMAM); inquiring about registered dealer empanelment and online application window on KSAMB portal."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Maize, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S048 (Zone 7 — Southern Transition Zone)
- **Location:** Shivamogga District (Zone 7)
- **Social Category & Tenure:** ST | Tenure: Registered Owner
- **Landholding & Land Type:** 2.0 acres (Marginal (< 2.5 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Ginger, Spices
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected), Drip Irrigation (Installed), Storage Shed
- **PRIMARY STATED NEED:** **`PROTECTED_HORTICULTURE`**
- **Farmer Narrative / Stated Circumstance:** *"ST marginal commercial ginger grower with 2.0 acres borewell-irrigated land in Shikaripura, Shivamogga; family inherited land title records pending mutation certification; applicant's father receives government pension with unconfirmed monthly amount / MTS designation; seeking 50% subsidy for shade-net protected cultivation under MIDH to prevent rhizome rot; inquiring about title regularization requirements."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | `REQUIRES_VERIFICATION` | Raw engine returned REQUIRES_VERIFICATION due to explicit UNKNOWN tenure cut-off date (land_ownership_cutoff_pre_feb_2019 = None). In strict adherence to Challenge 4 safeguards, missing title evidence must remain REQUIRES_VERIFICATION and never silently default to eligibility or ineligibility. Placed in Section B without scoring. |
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Ginger is absent from static crop whitelist. In this agro-climatic zone, Ginger is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH007` | **Mission for Integrated Development of Horticulture (MIDH)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on horticultural crop, minimum land size, and operational drip irrigation, but applicant's land title mutation remains pending (UNKNOWN title status). In accordance with Challenge 4 safeguards, title-dependent capital subsidy schemes are routed to Section B as REQUIRES_VERIFICATION without scoring until title documentation is evidenced. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S049 (Zone 7 — Southern Transition Zone)
- **Location:** Chikkamagaluru District (Zone 7)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 4.5 acres (Small (2.5-5 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Potato, Vegetables
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected), Drip Irrigation (Installed), Storage Shed
- **PRIMARY STATED NEED:** **`PROTECTED_HORTICULTURE`**
- **Farmer Narrative / Stated Circumstance:** *"General category small potato grower with 4.5 acres borewell-irrigated land in Tarikere, Chikkamagaluru; holding inherited in June 2022 following demise of father with registered legal heir certificate and updated Pahani; applying for 50% subsidy under MIDH for 2,000 sq. meter shade-net house for certified seed potato multiplication; seeking confirmation of post-2019 succession eligibility for PM-KISAN and MIDH."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH007` | **Mission for Integrated Development of Horticulture (MIDH)** | Qualifies for MIDH Protected Cultivation subsidy (50% cost norm for Polyhouse / Shade Net up to 4,000 m²). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Potato is absent from static crop whitelist. In this agro-climatic zone, Potato is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S050 (Zone 7 — Southern Transition Zone)
- **Location:** Hassan District (Zone 7)
- **Social Category & Tenure:** OBC (2A) | Tenure: Registered Owner
- **Landholding & Land Type:** 3.5 acres (Small (2.5-5 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Arecanut, Pepper
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected), Drip Irrigation (Installed)
- **PRIMARY STATED NEED:** **`PRODUCTION_CREDIT`**
- **Farmer Narrative / Stated Circumstance:** *"OBC small arecanut farmer with 3.5 acres irrigated plantation in Belur, Hassan; needing short-term production credit of ₹2.5 lakh for intercultural operations, fertilizer, and copper sulphate spraying; inquiring whether to apply for Central KCC via Canara Bank or State Cooperative interest-free loan via local PACS; seeking interest subvention and scale-of-finance terms."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH007` | **Mission for Integrated Development of Horticulture (MIDH)** | Qualifies for MIDH Protected Cultivation subsidy (50% cost norm for Polyhouse / Shade Net up to 4,000 m²). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Arecanut, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S051 (Zone 7 — Southern Transition Zone)
- **Location:** Shivamogga District (Zone 7)
- **Social Category & Tenure:** Minority | Tenure: Registered Owner
- **Landholding & Land Type:** 2.5 acres (Small (2.5-5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Maize, Pulses
- **Water Infrastructure:** Borewell (Non-energized) | Power/Grid: UNENERGIZED_OFF_GRID
- **Existing Assets:** Borewell (Non-energized)
- **PRIMARY STATED NEED:** **`SOLAR_PUMP_INSTALLATION`**
- **Farmer Narrative / Stated Circumstance:** *"Minority small farmer with exactly 2.5 acres dryland in Bhadravati, Shivamogga; has newly drilled non-energized borewell with proven yield of 2.5 inches; facing 3-year waiting list for regular IP set energization under MESCOM; applying for 60% subsidy on 5 HP standalone solar pump under PM-KUSUM Component B; seeking MNRE vendor portal registration steps."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH006` | **PM-KUSUM Component B (Standalone Solar Agriculture Pumps)** | Qualifies for PM-KUSUM Component B standalone solar agriculture pump (60% subsidy up to 7.5 HP). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Maize, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S052 (Zone 7 — Southern Transition Zone)
- **Location:** Chikkamagaluru District (Zone 7)
- **Social Category & Tenure:** OBC (2A) | Tenure: Registered Owner
- **Landholding & Land Type:** 9.5 acres (Medium (5-10 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Potato, Pulses
- **Water Infrastructure:** None (Dryland kushki) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`BOREWELL_IRRIGATION`**
- **Farmer Narrative / Stated Circumstance:** *"OBC medium dryland farmer with 9.5 acres rainfed holding in Kadur, Chikkamagaluru; individual land exceeds 5.0 acres ceiling for individual borewell; has formed a contiguous group with two neighboring OBC small farmers pooling a 12.0 acres block (qualifying parcel 4.0 acres); applying for shared community borewell and lift irrigation under D. Devaraj Urs Backward Classes Development Corporation; seeking group registration requirements and beneficiary criteria."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Potato is absent from static crop whitelist. In this agro-climatic zone, Potato is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_DEVARAJ_URS` | **Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on pooled acreage [8.0, 15.0] ac and encoded rule >= 2 beneficiaries. CRITICAL GOVERNANCE SAFEGUARD: The benchmark design requires >= 3 beneficiaries, scheme is PROVISIONAL in registry, and contiguous grouping requires registered joint deed verification. Governance presentation strictly places determination in Section B as REQUIRES_VERIFICATION with numerical scoring disabled. |

---

### Scenario S053 (Zone 8 — Northern Transition Zone)
- **Location:** Dharwad District (Zone 8)
- **Social Category & Tenure:** Minority (Muslim) | Tenure: Registered Owner
- **Landholding & Land Type:** 5.5 acres (Medium (5-10 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Soybean, Jowar
- **Water Infrastructure:** Dug Well (Seasonal, dries Feb-May) | Power/Grid: NONE
- **Existing Assets:** Dug Well (Seasonal), Sprinkler Set (Partial)
- **PRIMARY STATED NEED:** **`RAINWATER_HARVESTING`**
- **Farmer Narrative / Stated Circumstance:** *"Minority medium dryland soybean farmer with 5.5 acres in Navalgund taluk, Dharwad; seasonal dug well dries up by February; seeking 80% capital subsidy on farm pond (Krishi Honda) with polythene lining and diesel pump set under Krishi Bhagya; inquiring about Dharwad taluk portal opening and KMDC corporation borewell criteria."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Soybean, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S054 (Zone 8 — Northern Transition Zone)
- **Location:** Belagavi District (Zone 8)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 1.5 acres (Marginal (< 2.5 acres)) | Land Type: Wetland/valley
- **Crops:** Chilli, Vegetables
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected), Drip Irrigation (Installed)
- **PRIMARY STATED NEED:** **`PROTECTED_HORTICULTURE`**
- **Farmer Narrative / Stated Circumstance:** *"SC marginal chilli farmer with 1.5 acres Krishna river valley wetland in Athani taluk, Belagavi; operational grid-connected borewell and drip network installed; seeking 50% capital subsidy on naturally ventilated polyhouse / shade-net structure under Mission for Integrated Development of Horticulture (MIDH); checking crop insurance notification."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH007` | **Mission for Integrated Development of Horticulture (MIDH)** | Qualifies for MIDH Protected Cultivation subsidy (50% cost norm for Polyhouse / Shade Net up to 4,000 m²). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Chilli, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S055 (Zone 8 — Northern Transition Zone)
- **Location:** Haveri District (Zone 8)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 3.0 acres (Small (2.5-5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Cotton, Jowar
- **Water Infrastructure:** Dug Well (Seasonal) | Power/Grid: NONE
- **Existing Assets:** Dug Well (Seasonal)
- **PRIMARY STATED NEED:** **`INCOME_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"General category farmer with 3.0 acres dryland in Hangal taluk, Haveri; serving as regular government employee (State Commercial Taxes Department Officer); inquiring about eligibility for PM-KISAN annual income support of Rs. 6,000 and farm machinery support under SMAM."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH005` | **Krishi Bhagya Yojana** | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Cotton, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S056 (Zone 8 — Northern Transition Zone)
- **Location:** Dharwad District (Zone 8)
- **Social Category & Tenure:** ST | Tenure: Registered Owner
- **Landholding & Land Type:** 4.0 acres (Small (2.5-5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Wheat, Bengalgram
- **Water Infrastructure:** Farm Pond (Rainfed) | Power/Grid: NONE
- **Existing Assets:** Farm Pond (Rainfed)
- **PRIMARY STATED NEED:** **`SOIL_HEALTH_AND_FERTILIZER`**
- **Farmer Narrative / Stated Circumstance:** *"ST small wheat cultivator with 4.0 acres dryland in Kalghatgi taluk, Dharwad; ancestral land title partition in progress with record date unverified on Bhoomi portal; seeking Soil Health Card testing and macro/micro nutrient recommendations; inquiring about PM-KISAN and Valmiki Corporation borewell."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | `REQUIRES_VERIFICATION` | Raw engine returned REQUIRES_VERIFICATION due to explicit UNKNOWN tenure cut-off date (land_ownership_cutoff_pre_feb_2019 = None). In strict adherence to Challenge 4 safeguards, missing title evidence must remain REQUIRES_VERIFICATION and never silently default to eligibility or ineligibility. Placed in Section B without scoring. |
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Wheat is absent from static crop whitelist. In this agro-climatic zone, Wheat is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH005` | **Krishi Bhagya Yojana** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on rainfed dryland and acreage in notified Dharwad taluk, but applicant's land title record date is UNKNOWN. In accordance with Challenge 4 safeguards, title-dependent capital subsidy schemes are routed to Section B as REQUIRES_VERIFICATION without scoring until title documentation is evidenced. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_VALMIKI` | **Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on ST social category, dryland acreage, and zero existing borewells. However, scheme is PROVISIONAL in registry, perennial water source adjacency is unverified, and land title status is UNKNOWN. Governance presentation strictly places determination in Section B as REQUIRES_VERIFICATION with numerical scoring disabled. |

---

### Scenario S057 (Zone 8 — Northern Transition Zone)
- **Location:** Belagavi District (Zone 8)
- **Social Category & Tenure:** OBC | Tenure: Registered Owner
- **Landholding & Land Type:** 12.0 acres (Large (> 10 acres)) | Land Type: Irrigated (Canal)
- **Crops:** Sugarcane, Maize
- **Water Infrastructure:** Canal Command & Sump | Power/Grid: NONE
- **Existing Assets:** Canal Outlet, Intermediate Storage Sump, Tractor (45 HP)
- **PRIMARY STATED NEED:** **`FARM_MECHANIZATION`**
- **Farmer Narrative / Stated Circumstance:** *"OBC large sugarcane farmer with 12.0 acres canal command land in Gokak taluk, Belagavi; Ghataprabha right bank canal distributary; owns 45 HP tractor; seeking 40% capital subsidy on tractor-mounted sugarcane stubble shaver, ratoon manager, and rotavator under SMAM; verifying whether large holdings face blanket exclusion."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Sugarcane, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S058 (Zone 8 — Northern Transition Zone)
- **Location:** Haveri District (Zone 8)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 12.5 acres (Large (> 10 acres)) | Land Type: Irrigated (Borewell)
- **Crops:** Soybean, Cotton
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected), Sprinkler Set (Partial)
- **PRIMARY STATED NEED:** **`MICRO_IRRIGATION_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"General category large farmer with 12.5 acres borewell-irrigated land in Savanur taluk, Haveri; applying for micro-irrigation capital subsidy under PMKSY-PDMC for exactly 5.00 hectares (~12.36 acres); seeking confirmation of 5.00 ha statutory ceiling compliance and vendor quotation requirements."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Ineligible for PMKSY-PDMC: Landholding (12.5 ac) exceeds maximum subsidized limit of 5.0 hectares (~12.35 acres). | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Soybean, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S059 (Zone 9 — Hilly Zone)
- **Location:** Kodagu District (Zone 9)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 4.5 acres (Small (2.5-5 acres)) | Land Type: Hilly/terraced
- **Crops:** Coffee, Black Pepper
- **Water Infrastructure:** Hillside Stream Catchment | Power/Grid: NONE
- **Existing Assets:** Hillside Stream Catchment, Storage Tank
- **PRIMARY STATED NEED:** **`SOIL_HEALTH_AND_FERTILIZER`**
- **Farmer Narrative / Stated Circumstance:** *"General category small coffee planter with 4.5 acres terraced plantation in Somwarpet taluk, Kodagu; seeking Soil Health Card testing for soil acidity (pH), organic carbon, and customized NPK/lime recommendations; inquiring about soil testing laboratory mobile van schedule."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Coffee is absent from static crop whitelist. In this agro-climatic zone, Coffee is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S060 (Zone 9 — Hilly Zone)
- **Location:** Chikkamagaluru District (Zone 9)
- **Social Category & Tenure:** ST | Tenure: Registered Owner
- **Landholding & Land Type:** 2.0 acres (Marginal (< 2.5 acres)) | Land Type: Hilly/terraced
- **Crops:** Cardamom, Coffee
- **Water Infrastructure:** Hillside Stream Catchment | Power/Grid: NONE
- **Existing Assets:** Hillside Stream Catchment, Storage Tank
- **PRIMARY STATED NEED:** **`RAINWATER_HARVESTING`**
- **Farmer Narrative / Stated Circumstance:** *"ST marginal cardamom grower with 2.0 acres terraced hillside in Mudigere taluk, Chikkamagaluru; stream flow diminishes sharply post-monsoon; seeking rainwater harvesting storage structure / masonry tank assistance for dry spell life-saving irrigation; checking applicable horticulture/tribal welfare schemes."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Cardamom is absent from static crop whitelist. In this agro-climatic zone, Cardamom is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S061 (Zone 9 — Hilly Zone)
- **Location:** Uttara Kannada District (Zone 9)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 3.0 acres (Small (2.5-5 acres)) | Land Type: Wetland/valley
- **Crops:** Paddy, Pulses
- **Water Infrastructure:** Valley Natural Flow | Power/Grid: NONE
- **Existing Assets:** Natural Stream Inflow
- **PRIMARY STATED NEED:** **`PRODUCTION_CREDIT`**
- **Farmer Narrative / Stated Circumstance:** *"SC tenant farmer cultivating 3.0 acres valley paddy in Sirsi taluk, Uttara Kannada under informal tenancy agreement without recorded land title; seeking Kisan Credit Card (KCC) crop loan for seeds, fertilizers, and operational credit; checking oral lessee / Joint Liability Group (JLG) documentation requirements."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Paddy, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE under RBI/NABARD tenant borrower category, but oral tenancy documentation and bank tenant crop-loan eligibility require verification. Governance safeguard routes determination to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S062 (Zone 9 — Hilly Zone)
- **Location:** Kodagu District (Zone 9)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 1.8 acres (Marginal (< 2.5 acres)) | Land Type: Hilly/terraced
- **Crops:** Black Pepper, Coffee
- **Water Infrastructure:** Hillside Rainfed | Power/Grid: NONE
- **Existing Assets:** Hillside Rainfed Plot
- **PRIMARY STATED NEED:** **`CROP_INSURANCE`**
- **Farmer Narrative / Stated Circumstance:** *"General category marginal spice grower with 1.8 acres terraced holding in Virajpet taluk, Kodagu; ancestral partition pending formal mutation on Bhoomi portal (record date UNKNOWN); seeking crop insurance coverage against quick wilt disease under Restructured Weather Based Crop Insurance Scheme (RWBCIS) / PMFBY."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | `REQUIRES_VERIFICATION` | Raw engine returned REQUIRES_VERIFICATION due to explicit UNKNOWN tenure cut-off date (land_ownership_cutoff_pre_feb_2019 = None). In strict adherence to Challenge 4 safeguards, missing title evidence must remain REQUIRES_VERIFICATION and never silently default to eligibility or ineligibility. Placed in Section B without scoring. |
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Black Pepper is absent from static crop whitelist. In this agro-climatic zone, Black Pepper is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S063 (Zone 9 — Hilly Zone)
- **Location:** Chikkamagaluru District (Zone 9)
- **Social Category & Tenure:** Minority (Muslim) | Tenure: Registered Owner
- **Landholding & Land Type:** 2.5 acres (Small (2.5-5 acres)) | Land Type: Hilly/terraced
- **Crops:** Coffee, Black Pepper
- **Water Infrastructure:** Borewell (Non-energized) | Power/Grid: UNENERGIZED_OFF_GRID
- **Existing Assets:** Borewell (Non-energized)
- **PRIMARY STATED NEED:** **`SOLAR_PUMP_INSTALLATION`**
- **Farmer Narrative / Stated Circumstance:** *"Minority small coffee planter with exactly 2.5 acres terraced plantation in Koppa taluk, Chikkamagaluru; drilled functional borewell without electricity connection; off-grid location without grid line proximity; applying for 60% capital subsidy on 5 HP standalone solar photovoltaic water pumping system under PM-KUSUM Component B; verifying prerequisite attributes."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH006` | **PM-KUSUM Component B (Standalone Solar Agriculture Pumps)** | Qualifies for PM-KUSUM Component B standalone solar agriculture pump (60% subsidy up to 7.5 HP). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Coffee is absent from static crop whitelist. In this agro-climatic zone, Coffee is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S064 (Zone 9 — Hilly Zone)
- **Location:** Uttara Kannada District (Zone 9)
- **Social Category & Tenure:** OBC (2A) | Tenure: Registered Owner
- **Landholding & Land Type:** 8.0 acres (Medium (5-10 acres)) | Land Type: Irrigated (Canal)
- **Crops:** Paddy, Groundnut
- **Water Infrastructure:** Canal Command | Power/Grid: NONE
- **Existing Assets:** Canal Outlet, Intermediate Storage Sump
- **PRIMARY STATED NEED:** **`FARM_MECHANIZATION`**
- **Farmer Narrative / Stated Circumstance:** *"OBC medium paddy grower with 8.0 acres canal command in Yellapur taluk, Uttara Kannada; acquired land title via registered statutory succession following father's demise in November 2021 (Death Cert DC/UK/2021/8841 and Bhoomi mutation Form 16 MR No. 2022-T209 verified); seeking 40% capital subsidy on power tiller and walk-behind paddy transplanter under SMAM; verifying PM-KISAN succession status."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Paddy, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S065 (Zone 10 — Coastal Zone)
- **Location:** Dakshina Kannada District (Zone 10)
- **Social Category & Tenure:** General (OC) | Tenure: Registered Owner
- **Landholding & Land Type:** 14.0 acres (Large (> 10 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Coconut, Cocoa
- **Water Infrastructure:** Rainfed Coastal | Power/Grid: NONE
- **Existing Assets:** Rainfed Coastal Plantation
- **PRIMARY STATED NEED:** **`SOIL_HEALTH_AND_FERTILIZER`**
- **Farmer Narrative / Stated Circumstance:** *"General category large coconut grower with 14.0 acres rainfed coastal plantation in Bantwal taluk, Dakshina Kannada; seeking Soil Health Card macro and micro-nutrient testing to correct magnesium and boron deficiencies; inquiring about mobile soil testing van schedule and plantation fertilizer dosage."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Coconut is absent from static crop whitelist. In this agro-climatic zone, Coconut is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S066 (Zone 10 — Coastal Zone)
- **Location:** Udupi District (Zone 10)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 5.5 acres (Medium (5-10 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Arecanut, Black Pepper
- **Water Infrastructure:** None (Dryland kushki) | Power/Grid: NONE
- **Existing Assets:** []
- **PRIMARY STATED NEED:** **`BOREWELL_IRRIGATION`**
- **Farmer Narrative / Stated Circumstance:** *"SC medium arecanut farmer with 5.5 acres dryland holding in Karkala taluk, Udupi; individual landholding exceeds the 5.0 acres individual ceiling for Ganga Kalyana; has formed a contiguous group with three neighboring SC smallholders pooling a 14.0 acres block (qualifying parcel 3.5 acres); applying for community borewell and lift irrigation under Dr. B.R. Ambedkar Development Corporation; seeking corporation beneficiary criteria and groundwater NOC requirements."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Arecanut, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_AMBEDKAR` | **Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC)** | `REQUIRES_VERIFICATION` | Raw engine evaluated ELIGIBLE (GK_AMBEDKAR_COMMUNITY_ROUTE_VALID) because Dr. B.R. Ambedkar Development Corporation community route encodes >= 3 beneficiaries on 8.0-15.0 acres pooled dryland and S066 provides 4 contiguous SC beneficiaries with 14.0 acres (qualifying parcel 3.5 ac). Governance conservatively decouples determination to Section B as REQUIRES_VERIFICATION with numerical scoring disabled pending field verification of registered joint consent deed, contiguous boundary alignment, Mines and Geology groundwater safety clearance, and confirmation of current administrative circular instructions. |

---

### Scenario S067 (Zone 10 — Coastal Zone)
- **Location:** Dakshina Kannada District (Zone 10)
- **Social Category & Tenure:** ST | Tenure: Registered Owner
- **Landholding & Land Type:** 2.0 acres (Marginal (< 2.5 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Cashew, Paddy
- **Water Infrastructure:** Rainfed Coastal | Power/Grid: NONE
- **Existing Assets:** Rainfed Cashew Orchard
- **PRIMARY STATED NEED:** **`CROP_INSURANCE`**
- **Farmer Narrative / Stated Circumstance:** *"ST marginal cashew cultivator with 2.0 acres dryland orchard in Belthangady taluk, Dakshina Kannada; seeking crop insurance coverage against unseasonal rain and tea mosquito bug infestation under Restructured Weather Based Crop Insurance Scheme (RWBCIS) / PMFBY; inquiring about premium rates and notified Insurance Units."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Cashew is absent from static crop whitelist. In this agro-climatic zone, Cashew is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |
| `SCH010_VALMIKI` | **Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on encoded rules, but scheme record is PROVISIONAL in registry. Governance safeguard places determination in Section B as REQUIRES_VERIFICATION without numerical scoring. |

---

### Scenario S068 (Zone 10 — Coastal Zone)
- **Location:** Udupi District (Zone 10)
- **Social Category & Tenure:** Minority | Tenure: Registered Owner
- **Landholding & Land Type:** 1.5 acres (Marginal (< 2.5 acres)) | Land Type: Wetland/valley
- **Crops:** Paddy, Pulses
- **Water Infrastructure:** Wetland Inflow | Power/Grid: NONE
- **Existing Assets:** Wetland Inflow Drainage Sump
- **PRIMARY STATED NEED:** **`PRODUCTION_CREDIT`**
- **Farmer Narrative / Stated Circumstance:** *"Minority marginal tenant farmer cultivating 1.5 acres coastal wetland paddy in Kundapura taluk, Udupi; operates under informal oral lease agreement with village panchayat certificate (no registered land title); seeking crop loan under Kisan Credit Card (KCC) through regional rural bank; inquiring about tenant crop loan documentation and PMFBY enrollment."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Paddy, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE under RBI/NABARD tenant borrower category, but oral tenancy documentation and bank tenant crop-loan eligibility require verification. Governance safeguard routes determination to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S069 (Zone 10 — Coastal Zone)
- **Location:** Dakshina Kannada District (Zone 10)
- **Social Category & Tenure:** Minority | Tenure: Registered Owner
- **Landholding & Land Type:** 13.0 acres (Large (> 10 acres)) | Land Type: Dryland (Rainfed)
- **Crops:** Coconut, Cocoa
- **Water Infrastructure:** Open Well / Rainfed | Power/Grid: NONE
- **Existing Assets:** Open Well, Diesel Pump Set, Drip Irrigation (Installed)
- **PRIMARY STATED NEED:** **`PROTECTED_HORTICULTURE`**
- **Farmer Narrative / Stated Circumstance:** *"Minority large coconut grower with 13.0 acres holding in Puttur taluk, Dakshina Kannada; acquired land title via registered statutory succession following mother's demise in April 2022 (Death Cert DC/DK/2022/6104 and Bhoomi mutation Form 16 MR No. 2022-T771 verified); seeking 50% capital subsidy under MIDH for shaded coastal nursery / shade-net protected cultivation; verifying PM-KISAN succession status and solar pump replacement for diesel pump."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | | |
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH006` | **PM-KUSUM Component B (Standalone Solar Agriculture Pumps)** | Qualifies for PM-KUSUM Component B standalone solar agriculture pump (60% subsidy up to 7.5 HP). | | |
| `SCH007` | **Mission for Integrated Development of Horticulture (MIDH)** | Qualifies for MIDH Protected Cultivation subsidy (50% cost norm for Polyhouse / Shade Net up to 4,000 m²). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned INELIGIBLE because Coconut is absent from static crop whitelist. In this agro-climatic zone, Coconut is covered under weather-based (RWBCIS) or special plantation insurance schemes. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---

### Scenario S070 (Zone 10 — Coastal Zone)
- **Location:** Udupi District (Zone 10)
- **Social Category & Tenure:** SC | Tenure: Registered Owner
- **Landholding & Land Type:** 12.5 acres (Large (> 10 acres)) | Land Type: Wetland/valley
- **Crops:** Arecanut, Paddy
- **Water Infrastructure:** Borewell (Grid-connected) | Power/Grid: GRID_CONNECTED_IP_SET
- **Existing Assets:** Borewell (Grid-connected), Sprinkler Set (Partial)
- **PRIMARY STATED NEED:** **`MICRO_IRRIGATION_SUPPORT`**
- **Farmer Narrative / Stated Circumstance:** *"SC large arecanut farmer with 12.5 acres valley wetland holding in Udupi taluk; ancestral property partition in progress with land title cut-off date UNKNOWN on Bhoomi portal; applying for micro-irrigation capital subsidy under PMKSY-PDMC for 4.80 hectares (~11.86 acres); seeking confirmation of 4.80 ha parcel capacity and title regularization requirements."*

#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)
| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |
|:---|:---|:---|:---:|:---|
| `SCH004` | **Sub-Mission on Agricultural Mechanization (SMAM)** | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | | |
| `SCH008_CENTRAL` | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)** | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | | |
| `SCH009` | **Soil Health Card Scheme** | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | | |

#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)
| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |
|:---|:---|:---|:---|
| `SCH001` | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)** | `REQUIRES_VERIFICATION` | Raw engine returned REQUIRES_VERIFICATION due to explicit UNKNOWN tenure cut-off date (land_ownership_cutoff_pre_feb_2019 = None). In strict adherence to Challenge 4 safeguards, missing title evidence must remain REQUIRES_VERIFICATION and never silently default to eligibility or ineligibility. Placed in Section B without scoring. |
| `SCH002` | **Pradhan Mantri Fasal Bima Yojana (PMFBY)** | `REQUIRES_VERIFICATION` | Raw engine returned ELIGIBLE based on static crop whitelist for Arecanut, but commercial crop insurance claims strictly require verified Kharif 2026 Insurance Unit notification orders. Governance presentation routes to Section B as REQUIRES_VERIFICATION without numerical scoring. |
| `SCH003` | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)** | `REQUIRES_VERIFICATION` | Raw Engine vs Governance Discrepancy & Area Validation: Raw engine returned INELIGIBLE (PMKSY_LAND_ABOVE_5_HA) because its encoded static rule checks operational holding against 12.35 ac. However, under Section 7.9 of the PMKSY-PDMC Revised Operational Guidelines 2023, financial assistance is limited to 5.0 hectares per beneficiary (not per beneficiary family). S070 requests 4.80 ha, which is strictly within the physical capacity of the 12.5-acre parcel (5.059 ha) and within the 5.00 ha assistance ceiling under §7.9; the 5.0 ha assistance cap does not render the entire holding ineligible. However, because land title record date is UNKNOWN (land_ownership_cutoff_pre_feb_2019 = None), PMKSY-PDMC requires verified land title (RTC) and possession/boundary documentation (distinguished from PM-KISAN's 01.02.2019 cut-off date check). Governance preserves three-valued logic by placing determination in Section B as REQUIRES_VERIFICATION without numerical scoring pending title regularization. |
| `SCH008_KA_COOP` | **Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)** | `REQUIRES_VERIFICATION` | Provisional scheme requiring administrative or Government Order verification. |

---
