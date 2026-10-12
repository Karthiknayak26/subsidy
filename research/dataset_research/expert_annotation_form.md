# Deliverable B: Expert Annotation Form & Protocol (Pilot Benchmark S001–S010)

**Project:** ML-Based Personalized Government Scheme and Subsidy Recommendation System for Farmers (Karnataka Context)  
**Document Type:** Expert Annotation Instrument & Protocol  
**Target Annotators:** Agricultural Extension Officers (RSK/KSDA), KVK Subject Matter Specialists, UAS Faculty  
**Annotation Scope:** 10 Pilot Farmer Scenarios (S001–S010) across eligible candidate schemes  
**Protocol Date:** October 2026  

---

## 1. Instructions & Protocol for Expert Annotators

### 1.1 Objective & Separation of Three Core Questions
You are participating in an expert annotation study to establish the ground truth for an agricultural recommendation benchmark. To protect the methodological integrity of the benchmark, the system strictly separates three distinct questions:

1. **Eligibility (Does the farmer qualify statutorily?):** This is determined **solely by the deterministic rule engine** based on verified government guidelines. You do **not** determine statutory eligibility.
2. **Relevance (How well does an eligible scheme address the farmer's stated agricultural need?):** This is the **only question you are asked to score** (using the 0–3 scale below). Score this independently of whether the application window happens to be open today.
3. **Actionability (Is the scheme open right now?):** This is an operational determination maintained separately by the availability pipeline (4 discrete availability states). Do not downgrade a scheme's relevance score just because its seasonal portal cycle is closed.

> [!IMPORTANT]
> **Strict Boundary Conditions:**
> - **Do NOT score ineligible schemes:** Schemes determined ineligible by the engine have been omitted. No ineligible scheme will appear on your scoring sheets.
> - **Schemes Requiring Verification:** Schemes where statutory verification is pending (e.g. Karnataka Cooperative credit pending annual Government Order) appear in a **separate review section (Section B)**. Do NOT assign a numerical relevance score to them; instead, provide qualitative feedback on policy/administrative conditions.
> - **Statutory Family Definition:** In accordance with official guidelines (`pmkisan.gov.in`), the scheme-defined family consists of **husband, wife, and minor children**. Statutory exclusion flags (e.g. income tax payment, public service posts) apply across all members of this family unit.
> - **Independence Protocol:** Complete your ratings independently without consulting other annotators. Independent scores will be recorded separately to calculate inter-rater agreement.

### 1.2 The Relevance Rating Scale (0 to 3)

| Score | Label | Operational Definition |
|:---:|:---|:---|
| **3** | **Highly Relevant / High Priority** | Directly addresses the farmer's primary stated need. Provides immediate, high-impact practical benefit. Should appear in the top-3 recommendation cards. |
| **2** | **Relevant / Secondary Priority** | Provides genuine practical benefit to the farmer, but does not directly solve the urgent stated need (e.g., general income support when urgent need is crop insurance). Valuable secondary recommendation. |
| **1** | **Marginally Relevant / Low Priority** | Technically applicable and eligible, but provides minor or distant value in the current context (e.g., diagnostic soil testing when the farmer has an active pest disaster). |
| **0** | **Irrelevant / Not Useful** | Despite passing statutory eligibility, this scheme provides no meaningful practical benefit given the farmer's specific asset profile, crop, or situation. Should NOT be recommended. |

### 1.3 How to Complete Each Annotation Sheet
For each scenario:
1. **Read the Farmer Profile Card:** Review the district, crop, land size, land type, social category, existing assets, and the farmer's verbatim query/need.
2. **Evaluate Each Candidate Scheme in Section A:** Assign a score (0, 1, 2, or 3) in the `Score (0-3)` column.
3. **Provide Expert Reasoning:** Write 1–2 sentences explaining your agronomic / practical rationale.
4. **Indicate Confidence:** Select your confidence level (`High`, `Medium`, or `Low`).
5. **Review Section B (Pending Verification Items):** Provide qualitative policy feedback on whether and how the scheme should be recommended once verified.

---

## 2. Pilot Annotation Sheets (Scenarios S001 to S010)

### Farmer Scenario Profile: S001

```yaml
Scenario ID: S001
Location: Raichur, Karnataka (Northern Dry Zone)
Primary Crop: Cotton | Secondary: Redgram
Landholding: 3.0 acres | Land Type: Dryland (Rainfed)
Social Category: SC | Farmer Category: Small (2.5-5 acres)
Existing Assets: None
Annual Family Income: ₹1.2 Lakh
Farming Stage & Season: Standing Crop / Pre-Harvest | Kharif 2026
Immediate Stated Need: CROP_INSURANCE
Farmer Query Text: "Cotton crop suffering pink bollworm attack in Raichur, need compensation claim or insurance procedure."
```

#### Section A: Eligible Candidate Schemes for Scenario S001 (Assign Scores 0–3)

| Candidate Scheme ID | Scheme Name & Official Department | Official Portal Link | Engine Eligibility Rationale | Expert Relevance Score (0–3) | Expert Agronomic Reasoning / Justification | Expert Confidence (High / Med / Low) |
|---|---|---|---|:---:|---|:---:|---|
| **SCH001** | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), Ministry of Agriculture & Farmers Welfare* | [SCH001 Portal](https://pmkisan.gov.in/) | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH002** | **Pradhan Mantri Fasal Bima Yojana (PMFBY)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH002 Portal](https://pmfby.gov.in/) | Qualifies for PMFBY crop insurance for Cotton. Premium subsidized by Center & State; claim indemnity contingent upon surveyed loss. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH004** | **Sub-Mission on Agricultural Mechanization (SMAM)**<br>*Mechanization and Technology Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH004 Portal](https://agrimachinery.nic.in/) | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH005** | **Krishi Bhagya Yojana**<br>*Department of Agriculture, Government of Karnataka* | [SCH005 Portal](https://raitamitra.karnataka.gov.in/) | Qualifies for Krishi Bhagya integrated package (90% for SC/ST subsidy for Krishi Honda, lining, pump). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH008_CENTRAL** | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW in collaboration with RBI and NABARD* | [SCH008_CENTRAL Portal](https://www.rbi.org.in/) | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH009** | **Soil Health Card Scheme**<br>*Integrated Nutrient Management Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH009 Portal](https://soilhealth.dac.gov.in/) | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH010_AMBEDKAR** | **Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC)**<br>*Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka* | [SCH010_AMBEDKAR Portal](https://adcl.karnataka.gov.in/ / https://sevasindhu.karnataka.gov.in/) | Qualifies for Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC) under Individual Borewell Route. 100% subsidized borewell, pump, and electrification package. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |

#### Section B: Schemes Requiring Verification for Scenario S001 (Do NOT Score as Eligible)

> [!NOTE]
> The following scheme(s) cannot be confirmed as active without pending statutory/administrative verification. They are NOT included in the candidate scoring above. Please review the pending condition:
>
> - **SCH008_KA_COOP: Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)**  
>   *Pending Verification:* Annual Cooperative Department GO verification  
>   *Engine Status Note:* Qualifies in principle for Karnataka Zero-Interest Credit via PACS/DCCBs (0% up to Rs. 5 Lakh). Marked PROVISIONAL pending active financial year Government Order verification.  
>   *Expert Policy Feedback Prompt:* Explain uncertain eligibility or policy interpretations. Should this facility be conditionally recommended in advisory notices pending active PACS circulars? `[ Comments / Rationale: __________ ]`  
>

---

### Farmer Scenario Profile: S002

```yaml
Scenario ID: S002
Location: Haveri, Karnataka (Central Dry Zone)
Primary Crop: Maize
Landholding: 2.0 acres | Land Type: Dryland (Rainfed)
Social Category: OBC (2A) | Farmer Category: Marginal (< 2.5 acres)
Existing Assets: Borewell (Non-energized)
Annual Family Income: ₹1.5 Lakh
Farming Stage & Season: Pre-Sowing / Land Preparation | Kharif 2026
Immediate Stated Need: SOLAR_PUMP_INSTALLATION
Farmer Query Text: "Have drilled borewell without electricity connection in Haveri, need solar motor pump subsidy subsidy details."
```

#### Section A: Eligible Candidate Schemes for Scenario S002 (Assign Scores 0–3)

| Candidate Scheme ID | Scheme Name & Official Department | Official Portal Link | Engine Eligibility Rationale | Expert Relevance Score (0–3) | Expert Agronomic Reasoning / Justification | Expert Confidence (High / Med / Low) |
|---|---|---|---|:---:|---|:---:|---|
| **SCH001** | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), Ministry of Agriculture & Farmers Welfare* | [SCH001 Portal](https://pmkisan.gov.in/) | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH002** | **Pradhan Mantri Fasal Bima Yojana (PMFBY)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH002 Portal](https://pmfby.gov.in/) | Qualifies for PMFBY crop insurance for Maize. Premium subsidized by Center & State; claim indemnity contingent upon surveyed loss. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH003** | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Horticulture & Agriculture, Govt of Karnataka* | [SCH003 Portal](https://pmksy.gov.in/) | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH004** | **Sub-Mission on Agricultural Mechanization (SMAM)**<br>*Mechanization and Technology Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH004 Portal](https://agrimachinery.nic.in/) | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH005** | **Krishi Bhagya Yojana**<br>*Department of Agriculture, Government of Karnataka* | [SCH005 Portal](https://raitamitra.karnataka.gov.in/) | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH006** | **PM-KUSUM Component B (Standalone Solar Agriculture Pumps)**<br>*Ministry of New and Renewable Energy (MNRE), Govt of India / Karnataka Renewable Energy Development Limited (KREDL), Govt of Karnataka* | [SCH006 Portal](https://pmkusum.mnre.gov.in/) | Qualifies for PM-KUSUM Component B standalone solar agriculture pump (60% subsidy up to 7.5 HP). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH008_CENTRAL** | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW in collaboration with RBI and NABARD* | [SCH008_CENTRAL Portal](https://www.rbi.org.in/) | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH009** | **Soil Health Card Scheme**<br>*Integrated Nutrient Management Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH009 Portal](https://soilhealth.dac.gov.in/) | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |

#### Section B: Schemes Requiring Verification for Scenario S002 (Do NOT Score as Eligible)

> [!NOTE]
> The following scheme(s) cannot be confirmed as active without pending statutory/administrative verification. They are NOT included in the candidate scoring above. Please review the pending condition:
>
> - **SCH008_KA_COOP: Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)**  
>   *Pending Verification:* Annual Cooperative Department GO verification  
>   *Engine Status Note:* Qualifies in principle for Karnataka Zero-Interest Credit via PACS/DCCBs (0% up to Rs. 5 Lakh). Marked PROVISIONAL pending active financial year Government Order verification.  
>   *Expert Policy Feedback Prompt:* Explain uncertain eligibility or policy interpretations. Should this facility be conditionally recommended in advisory notices pending active PACS circulars? `[ Comments / Rationale: __________ ]`  
>

---

### Farmer Scenario Profile: S003

```yaml
Scenario ID: S003
Location: Tumakuru, Karnataka (Southern Dry Zone)
Primary Crop: Ragi
Landholding: 1.5 acres | Land Type: Dryland (Rainfed)
Social Category: General (OC) | Farmer Category: Marginal (< 2.5 acres)
Existing Assets: None
Annual Family Income: ₹1.8 Lakh
Farming Stage & Season: Pre-Sowing | Kharif 2026
Immediate Stated Need: RAINWATER_HARVESTING
Farmer Query Text: "Dryland ragi farmer in Tumakuru wanting to dig farm pond (krishi honda) with polythene lining for rainwater storage."
```

#### Section A: Eligible Candidate Schemes for Scenario S003 (Assign Scores 0–3)

| Candidate Scheme ID | Scheme Name & Official Department | Official Portal Link | Engine Eligibility Rationale | Expert Relevance Score (0–3) | Expert Agronomic Reasoning / Justification | Expert Confidence (High / Med / Low) |
|---|---|---|---|:---:|---|:---:|---|
| **SCH001** | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), Ministry of Agriculture & Farmers Welfare* | [SCH001 Portal](https://pmkisan.gov.in/) | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH002** | **Pradhan Mantri Fasal Bima Yojana (PMFBY)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH002 Portal](https://pmfby.gov.in/) | Qualifies for PMFBY crop insurance for Ragi. Premium subsidized by Center & State; claim indemnity contingent upon surveyed loss. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH004** | **Sub-Mission on Agricultural Mechanization (SMAM)**<br>*Mechanization and Technology Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH004 Portal](https://agrimachinery.nic.in/) | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH005** | **Krishi Bhagya Yojana**<br>*Department of Agriculture, Government of Karnataka* | [SCH005 Portal](https://raitamitra.karnataka.gov.in/) | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH008_CENTRAL** | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW in collaboration with RBI and NABARD* | [SCH008_CENTRAL Portal](https://www.rbi.org.in/) | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH009** | **Soil Health Card Scheme**<br>*Integrated Nutrient Management Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH009 Portal](https://soilhealth.dac.gov.in/) | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |

#### Section B: Schemes Requiring Verification for Scenario S003 (Do NOT Score as Eligible)

> [!NOTE]
> The following scheme(s) cannot be confirmed as active without pending statutory/administrative verification. They are NOT included in the candidate scoring above. Please review the pending condition:
>
> - **SCH008_KA_COOP: Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)**  
>   *Pending Verification:* Annual Cooperative Department GO verification  
>   *Engine Status Note:* Qualifies in principle for Karnataka Zero-Interest Credit via PACS/DCCBs (0% up to Rs. 5 Lakh). Marked PROVISIONAL pending active financial year Government Order verification.  
>   *Expert Policy Feedback Prompt:* Explain uncertain eligibility or policy interpretations. Should this facility be conditionally recommended in advisory notices pending active PACS circulars? `[ Comments / Rationale: __________ ]`  
>

---

### Farmer Scenario Profile: S004

```yaml
Scenario ID: S004
Location: Dharwad, Karnataka (Southern Transition Zone)
Primary Crop: Soybean | Secondary: Maize
Landholding: 4.0 acres | Land Type: Irrigated (Borewell)
Social Category: OBC (3B) | Farmer Category: Small (2.5-5 acres)
Existing Assets: Borewell (Grid-connected), Electric Pump Set
Annual Family Income: ₹2.5 Lakh
Farming Stage & Season: Vegetative Growth | Kharif 2026
Immediate Stated Need: MICRO_IRRIGATION_SUPPORT
Farmer Query Text: "Borewell discharge depleting in Dharwad, want to install drip irrigation line for soybean and maize."
```

#### Section A: Eligible Candidate Schemes for Scenario S004 (Assign Scores 0–3)

| Candidate Scheme ID | Scheme Name & Official Department | Official Portal Link | Engine Eligibility Rationale | Expert Relevance Score (0–3) | Expert Agronomic Reasoning / Justification | Expert Confidence (High / Med / Low) |
|---|---|---|---|:---:|---|:---:|---|
| **SCH001** | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), Ministry of Agriculture & Farmers Welfare* | [SCH001 Portal](https://pmkisan.gov.in/) | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH002** | **Pradhan Mantri Fasal Bima Yojana (PMFBY)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH002 Portal](https://pmfby.gov.in/) | Qualifies for PMFBY crop insurance for Soybean. Premium subsidized by Center & State; claim indemnity contingent upon surveyed loss. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH003** | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Horticulture & Agriculture, Govt of Karnataka* | [SCH003 Portal](https://pmksy.gov.in/) | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH004** | **Sub-Mission on Agricultural Mechanization (SMAM)**<br>*Mechanization and Technology Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH004 Portal](https://agrimachinery.nic.in/) | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH008_CENTRAL** | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW in collaboration with RBI and NABARD* | [SCH008_CENTRAL Portal](https://www.rbi.org.in/) | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH009** | **Soil Health Card Scheme**<br>*Integrated Nutrient Management Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH009 Portal](https://soilhealth.dac.gov.in/) | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |

#### Section B: Schemes Requiring Verification for Scenario S004 (Do NOT Score as Eligible)

> [!NOTE]
> The following scheme(s) cannot be confirmed as active without pending statutory/administrative verification. They are NOT included in the candidate scoring above. Please review the pending condition:
>
> - **SCH008_KA_COOP: Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)**  
>   *Pending Verification:* Annual Cooperative Department GO verification  
>   *Engine Status Note:* Qualifies in principle for Karnataka Zero-Interest Credit via PACS/DCCBs (0% up to Rs. 5 Lakh). Marked PROVISIONAL pending active financial year Government Order verification.  
>   *Expert Policy Feedback Prompt:* Explain uncertain eligibility or policy interpretations. Should this facility be conditionally recommended in advisory notices pending active PACS circulars? `[ Comments / Rationale: __________ ]`  
>

---

### Farmer Scenario Profile: S005

```yaml
Scenario ID: S005
Location: Kolar, Karnataka (Eastern Dry Zone)
Primary Crop: Tomato | Secondary: Capsicum
Landholding: 1.0 acres | Land Type: Irrigated (Borewell)
Social Category: OBC (3A) | Farmer Category: Marginal (< 2.5 acres)
Existing Assets: Borewell (Grid-connected), Drip Irrigation (Installed)
Annual Family Income: ₹3.0 Lakh
Farming Stage & Season: Nursery / Transplanting | Rabi 2026-27
Immediate Stated Need: PROTECTED_HORTICULTURE
Farmer Query Text: "Seeking subsidy subsidy for naturally ventilated polyhouse structure of 1000 square meters for high value capsicum in Kolar."
```

#### Section A: Eligible Candidate Schemes for Scenario S005 (Assign Scores 0–3)

| Candidate Scheme ID | Scheme Name & Official Department | Official Portal Link | Engine Eligibility Rationale | Expert Relevance Score (0–3) | Expert Agronomic Reasoning / Justification | Expert Confidence (High / Med / Low) |
|---|---|---|---|:---:|---|:---:|---|
| **SCH001** | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), Ministry of Agriculture & Farmers Welfare* | [SCH001 Portal](https://pmkisan.gov.in/) | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH002** | **Pradhan Mantri Fasal Bima Yojana (PMFBY)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH002 Portal](https://pmfby.gov.in/) | Qualifies for PMFBY crop insurance for Tomato. Premium subsidized by Center & State; claim indemnity contingent upon surveyed loss. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH003** | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Horticulture & Agriculture, Govt of Karnataka* | [SCH003 Portal](https://pmksy.gov.in/) | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH004** | **Sub-Mission on Agricultural Mechanization (SMAM)**<br>*Mechanization and Technology Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH004 Portal](https://agrimachinery.nic.in/) | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH007** | **Mission for Integrated Development of Horticulture (MIDH)**<br>*Horticulture Division, DA&FW, MoA&FW / Department of Horticulture, Government of Karnataka* | [SCH007 Portal](https://midh.gov.in/) | Qualifies for MIDH Protected Cultivation subsidy (50% cost norm for Polyhouse / Shade Net up to 4,000 m²). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH008_CENTRAL** | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW in collaboration with RBI and NABARD* | [SCH008_CENTRAL Portal](https://www.rbi.org.in/) | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH009** | **Soil Health Card Scheme**<br>*Integrated Nutrient Management Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH009 Portal](https://soilhealth.dac.gov.in/) | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |

#### Section B: Schemes Requiring Verification for Scenario S005 (Do NOT Score as Eligible)

> [!NOTE]
> The following scheme(s) cannot be confirmed as active without pending statutory/administrative verification. They are NOT included in the candidate scoring above. Please review the pending condition:
>
> - **SCH008_KA_COOP: Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)**  
>   *Pending Verification:* Annual Cooperative Department GO verification  
>   *Engine Status Note:* Qualifies in principle for Karnataka Zero-Interest Credit via PACS/DCCBs (0% up to Rs. 5 Lakh). Marked PROVISIONAL pending active financial year Government Order verification.  
>   *Expert Policy Feedback Prompt:* Explain uncertain eligibility or policy interpretations. Should this facility be conditionally recommended in advisory notices pending active PACS circulars? `[ Comments / Rationale: __________ ]`  
>

---

### Farmer Scenario Profile: S006

```yaml
Scenario ID: S006
Location: Mysuru, Karnataka (Southern Dry Zone)
Primary Crop: Paddy
Landholding: 2.5 acres | Land Type: Irrigated (Canal)
Social Category: General (OC) | Farmer Category: Small (2.5-5 acres)
Existing Assets: None
Annual Family Income: ₹2.0 Lakh
Farming Stage & Season: Pre-Sowing / Input Procurement | Kharif 2026
Immediate Stated Need: PRODUCTION_CREDIT
Farmer Query Text: "Need crop loan / Kisan Credit Card through bank branch for paddy seeds and fertilizer inputs in Mysuru."
```

#### Section A: Eligible Candidate Schemes for Scenario S006 (Assign Scores 0–3)

| Candidate Scheme ID | Scheme Name & Official Department | Official Portal Link | Engine Eligibility Rationale | Expert Relevance Score (0–3) | Expert Agronomic Reasoning / Justification | Expert Confidence (High / Med / Low) |
|---|---|---|---|:---:|---|:---:|---|
| **SCH001** | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), Ministry of Agriculture & Farmers Welfare* | [SCH001 Portal](https://pmkisan.gov.in/) | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH002** | **Pradhan Mantri Fasal Bima Yojana (PMFBY)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH002 Portal](https://pmfby.gov.in/) | Qualifies for PMFBY crop insurance for Paddy. Premium subsidized by Center & State; claim indemnity contingent upon surveyed loss. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH003** | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Horticulture & Agriculture, Govt of Karnataka* | [SCH003 Portal](https://pmksy.gov.in/) | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH004** | **Sub-Mission on Agricultural Mechanization (SMAM)**<br>*Mechanization and Technology Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH004 Portal](https://agrimachinery.nic.in/) | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH008_CENTRAL** | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW in collaboration with RBI and NABARD* | [SCH008_CENTRAL Portal](https://www.rbi.org.in/) | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH009** | **Soil Health Card Scheme**<br>*Integrated Nutrient Management Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH009 Portal](https://soilhealth.dac.gov.in/) | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |

#### Section B: Schemes Requiring Verification for Scenario S006 (Do NOT Score as Eligible)

> [!NOTE]
> The following scheme(s) cannot be confirmed as active without pending statutory/administrative verification. They are NOT included in the candidate scoring above. Please review the pending condition:
>
> - **SCH008_KA_COOP: Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)**  
>   *Pending Verification:* Annual Cooperative Department GO verification  
>   *Engine Status Note:* Qualifies in principle for Karnataka Zero-Interest Credit via PACS/DCCBs (0% up to Rs. 5 Lakh). Marked PROVISIONAL pending active financial year Government Order verification.  
>   *Expert Policy Feedback Prompt:* Explain uncertain eligibility or policy interpretations. Should this facility be conditionally recommended in advisory notices pending active PACS circulars? `[ Comments / Rationale: __________ ]`  
>

---

### Farmer Scenario Profile: S007

```yaml
Scenario ID: S007
Location: Haveri, Karnataka (Central Dry Zone)
Primary Crop: Maize
Landholding: 3.0 acres | Land Type: Dryland (Rainfed)
Social Category: General (OC) | Farmer Category: Small (2.5-5 acres)
Existing Assets: None
Annual Family Income: ₹2.2 Lakh
Farming Stage & Season: Sowing | Kharif 2026
Immediate Stated Need: INCOME_SUPPORT
Farmer Query Text: "Enquiring about PM-KISAN installment payment status. Family member paid income tax last year."
```

#### Section A: Eligible Candidate Schemes for Scenario S007 (Assign Scores 0–3)

| Candidate Scheme ID | Scheme Name & Official Department | Official Portal Link | Engine Eligibility Rationale | Expert Relevance Score (0–3) | Expert Agronomic Reasoning / Justification | Expert Confidence (High / Med / Low) |
|---|---|---|---|:---:|---|:---:|---|
| **SCH002** | **Pradhan Mantri Fasal Bima Yojana (PMFBY)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH002 Portal](https://pmfby.gov.in/) | Qualifies for PMFBY crop insurance for Maize. Premium subsidized by Center & State; claim indemnity contingent upon surveyed loss. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH004** | **Sub-Mission on Agricultural Mechanization (SMAM)**<br>*Mechanization and Technology Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH004 Portal](https://agrimachinery.nic.in/) | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH005** | **Krishi Bhagya Yojana**<br>*Department of Agriculture, Government of Karnataka* | [SCH005 Portal](https://raitamitra.karnataka.gov.in/) | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH008_CENTRAL** | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW in collaboration with RBI and NABARD* | [SCH008_CENTRAL Portal](https://www.rbi.org.in/) | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH009** | **Soil Health Card Scheme**<br>*Integrated Nutrient Management Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH009 Portal](https://soilhealth.dac.gov.in/) | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |

#### Section B: Schemes Requiring Verification for Scenario S007 (Do NOT Score as Eligible)

> [!NOTE]
> The following scheme(s) cannot be confirmed as active without pending statutory/administrative verification. They are NOT included in the candidate scoring above. Please review the pending condition:
>
> - **SCH008_KA_COOP: Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)**  
>   *Pending Verification:* Annual Cooperative Department GO verification  
>   *Engine Status Note:* Qualifies in principle for Karnataka Zero-Interest Credit via PACS/DCCBs (0% up to Rs. 5 Lakh). Marked PROVISIONAL pending active financial year Government Order verification.  
>   *Expert Policy Feedback Prompt:* Explain uncertain eligibility or policy interpretations. Should this facility be conditionally recommended in advisory notices pending active PACS circulars? `[ Comments / Rationale: __________ ]`  
>

---

### Farmer Scenario Profile: S008

```yaml
Scenario ID: S008
Location: Vijayapura, Karnataka (Northern Dry Zone)
Primary Crop: Jowar
Landholding: 4.0 acres | Land Type: Dryland (Rainfed)
Social Category: OBC (2A) | Farmer Category: Small (2.5-5 acres)
Existing Assets: Borewell (Grid-connected)
Annual Family Income: ₹1.8 Lakh
Farming Stage & Season: Pre-Sowing | Rabi 2026-27
Immediate Stated Need: SOLAR_PUMP_INSTALLATION
Farmer Query Text: "Already have electric grid motor on borewell in Vijayapura, want to apply for standalone solar pump subsidy."
```

#### Section A: Eligible Candidate Schemes for Scenario S008 (Assign Scores 0–3)

| Candidate Scheme ID | Scheme Name & Official Department | Official Portal Link | Engine Eligibility Rationale | Expert Relevance Score (0–3) | Expert Agronomic Reasoning / Justification | Expert Confidence (High / Med / Low) |
|---|---|---|---|:---:|---|:---:|---|
| **SCH001** | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), Ministry of Agriculture & Farmers Welfare* | [SCH001 Portal](https://pmkisan.gov.in/) | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH002** | **Pradhan Mantri Fasal Bima Yojana (PMFBY)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH002 Portal](https://pmfby.gov.in/) | Qualifies for PMFBY crop insurance for Jowar. Premium subsidized by Center & State; claim indemnity contingent upon surveyed loss. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH003** | **Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Horticulture & Agriculture, Govt of Karnataka* | [SCH003 Portal](https://pmksy.gov.in/) | Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH004** | **Sub-Mission on Agricultural Mechanization (SMAM)**<br>*Mechanization and Technology Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH004 Portal](https://agrimachinery.nic.in/) | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH005** | **Krishi Bhagya Yojana**<br>*Department of Agriculture, Government of Karnataka* | [SCH005 Portal](https://raitamitra.karnataka.gov.in/) | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH008_CENTRAL** | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW in collaboration with RBI and NABARD* | [SCH008_CENTRAL Portal](https://www.rbi.org.in/) | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH009** | **Soil Health Card Scheme**<br>*Integrated Nutrient Management Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH009 Portal](https://soilhealth.dac.gov.in/) | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |

#### Section B: Schemes Requiring Verification for Scenario S008 (Do NOT Score as Eligible)

> [!NOTE]
> The following scheme(s) cannot be confirmed as active without pending statutory/administrative verification. They are NOT included in the candidate scoring above. Please review the pending condition:
>
> - **SCH008_KA_COOP: Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)**  
>   *Pending Verification:* Annual Cooperative Department GO verification  
>   *Engine Status Note:* Qualifies in principle for Karnataka Zero-Interest Credit via PACS/DCCBs (0% up to Rs. 5 Lakh). Marked PROVISIONAL pending active financial year Government Order verification.  
>   *Expert Policy Feedback Prompt:* Explain uncertain eligibility or policy interpretations. Should this facility be conditionally recommended in advisory notices pending active PACS circulars? `[ Comments / Rationale: __________ ]`  
>

---

### Farmer Scenario Profile: S009

```yaml
Scenario ID: S009
Location: Chitradurga, Karnataka (Central Dry Zone)
Primary Crop: Groundnut
Landholding: 2.0 acres | Land Type: Dryland (Rainfed)
Social Category: General (OC) | Farmer Category: Marginal (< 2.5 acres)
Existing Assets: None
Annual Family Income: ₹1.4 Lakh
Farming Stage & Season: Pre-Sowing | Kharif 2026
Immediate Stated Need: BOREWELL_IRRIGATION
Farmer Query Text: "Dryland farmer in Chitradurga seeking 100% free government borewell under Ganga Kalyana scheme."
```

#### Section A: Eligible Candidate Schemes for Scenario S009 (Assign Scores 0–3)

| Candidate Scheme ID | Scheme Name & Official Department | Official Portal Link | Engine Eligibility Rationale | Expert Relevance Score (0–3) | Expert Agronomic Reasoning / Justification | Expert Confidence (High / Med / Low) |
|---|---|---|---|:---:|---|:---:|---|
| **SCH001** | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), Ministry of Agriculture & Farmers Welfare* | [SCH001 Portal](https://pmkisan.gov.in/) | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH002** | **Pradhan Mantri Fasal Bima Yojana (PMFBY)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH002 Portal](https://pmfby.gov.in/) | Qualifies for PMFBY crop insurance for Groundnut. Premium subsidized by Center & State; claim indemnity contingent upon surveyed loss. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH004** | **Sub-Mission on Agricultural Mechanization (SMAM)**<br>*Mechanization and Technology Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH004 Portal](https://agrimachinery.nic.in/) | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH005** | **Krishi Bhagya Yojana**<br>*Department of Agriculture, Government of Karnataka* | [SCH005 Portal](https://raitamitra.karnataka.gov.in/) | Qualifies for Krishi Bhagya integrated package (80% for General dryland subsidy for Krishi Honda, lining, pump). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH008_CENTRAL** | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW in collaboration with RBI and NABARD* | [SCH008_CENTRAL Portal](https://www.rbi.org.in/) | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH009** | **Soil Health Card Scheme**<br>*Integrated Nutrient Management Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH009 Portal](https://soilhealth.dac.gov.in/) | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |

#### Section B: Schemes Requiring Verification for Scenario S009 (Do NOT Score as Eligible)

> [!NOTE]
> The following scheme(s) cannot be confirmed as active without pending statutory/administrative verification. They are NOT included in the candidate scoring above. Please review the pending condition:
>
> - **SCH008_KA_COOP: Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)**  
>   *Pending Verification:* Annual Cooperative Department GO verification  
>   *Engine Status Note:* Qualifies in principle for Karnataka Zero-Interest Credit via PACS/DCCBs (0% up to Rs. 5 Lakh). Marked PROVISIONAL pending active financial year Government Order verification.  
>   *Expert Policy Feedback Prompt:* Explain uncertain eligibility or policy interpretations. Should this facility be conditionally recommended in advisory notices pending active PACS circulars? `[ Comments / Rationale: __________ ]`  
>

---

### Farmer Scenario Profile: S010

```yaml
Scenario ID: S010
Location: Belagavi, Karnataka (Northern Dry Zone)
Primary Crop: Sugarcane
Landholding: 3.0 acres | Land Type: Irrigated (Borewell)
Social Category: SC | Farmer Category: Small (2.5-5 acres)
Existing Assets: Borewell (Grid-connected)
Annual Family Income: ₹2.8 Lakh
Farming Stage & Season: Vegetative Growth | Kharif 2026
Immediate Stated Need: MICRO_IRRIGATION_SUPPORT
Farmer Query Text: "Availed drip subsidy 3 years ago in Belagavi, want replacement drip system subsidy for sugarcane."
```

#### Section A: Eligible Candidate Schemes for Scenario S010 (Assign Scores 0–3)

| Candidate Scheme ID | Scheme Name & Official Department | Official Portal Link | Engine Eligibility Rationale | Expert Relevance Score (0–3) | Expert Agronomic Reasoning / Justification | Expert Confidence (High / Med / Low) |
|---|---|---|---|:---:|---|:---:|---|
| **SCH001** | **Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), Ministry of Agriculture & Farmers Welfare* | [SCH001 Portal](https://pmkisan.gov.in/) | Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH002** | **Pradhan Mantri Fasal Bima Yojana (PMFBY)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH002 Portal](https://pmfby.gov.in/) | Qualifies for PMFBY crop insurance for Sugarcane. Premium subsidized by Center & State; claim indemnity contingent upon surveyed loss. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH004** | **Sub-Mission on Agricultural Mechanization (SMAM)**<br>*Mechanization and Technology Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH004 Portal](https://agrimachinery.nic.in/) | Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH008_CENTRAL** | **Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)**<br>*Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW in collaboration with RBI and NABARD* | [SCH008_CENTRAL Portal](https://www.rbi.org.in/) | Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment). | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |
| **SCH009** | **Soil Health Card Scheme**<br>*Integrated Nutrient Management Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka* | [SCH009 Portal](https://soilhealth.dac.gov.in/) | Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations. | `[   ]` | *(Write 1-2 sentences on practical relevance)* | `[ H / M / L ]` |

#### Section B: Schemes Requiring Verification for Scenario S010 (Do NOT Score as Eligible)

> [!NOTE]
> The following scheme(s) cannot be confirmed as active without pending statutory/administrative verification. They are NOT included in the candidate scoring above. Please review the pending condition:
>
> - **SCH008_KA_COOP: Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)**  
>   *Pending Verification:* Annual Cooperative Department GO verification  
>   *Engine Status Note:* Qualifies in principle for Karnataka Zero-Interest Credit via PACS/DCCBs (0% up to Rs. 5 Lakh). Marked PROVISIONAL pending active financial year Government Order verification.  
>   *Expert Policy Feedback Prompt:* Explain uncertain eligibility or policy interpretations. Should this facility be conditionally recommended in advisory notices pending active PACS circulars? `[ Comments / Rationale: __________ ]`  
>

---

## 3. Post-Pilot Inter-Expert Agreement Protocol

Once independent annotators have completed the pilot sheets above, raw scores will be compiled into separate independent columns (`relevance_annotator_A`, `relevance_annotator_B`, `relevance_annotator_C`) before any aggregate ground truth is derived.

### 3.1 Alignment of Agreement Metrics with Annotation Design

To prevent reporting misleading statistics, agreement analyses will match the exact structure of data collected:

| Annotation Structure | Primary Statistical Metric | Methodological Rationale |
|---|---|---|
| **Two experts assigning ordinal scores (0–3)** | **Weighted Cohen's Kappa ($\kappa_w$)** | Applies quadratic weighting $(\kappa_{w, \text{quadratic}})$ to penalize large score discrepancies (e.g. 0 vs 3) more heavily than adjacent differences (e.g. 2 vs 3). |
| **Three or more experts assigning ordinal scores (with potential missing ratings)** | **Krippendorff's Alpha ($\alpha$) with Ordinal Metric** | Handles arbitrary numbers of raters and missing data gracefully, utilizing the metric difference function $\delta^2(c, k)$ to respect the ordinal spacing of the 0–3 scale. |
| **Experts explicitly ranking candidate schemes** | **Kendall's Coefficient of Concordance ($W$)** | Measures rank agreement across candidate schemes within each scenario, testing whether experts agree on scheme prioritization order. |
| **Supplementary categorical check** | **Fleiss' Kappa ($\kappa$) (Optional)** | Reported only as an unweighted supplementary check for nominal agreement; explicitly noted that it treats differences between 0 and 1 identically to differences between 0 and 3. |

### 3.2 Reporting Standards (No Single-Statistic Claims)
In accordance with research integrity standards, the study will **not** report a single agreement number as sole proof that the annotations are reliable. The pilot report will present:
1. **Number of experts ($m$):** Total qualified domain reviewers.
2. **Jointly rated items ($N$):** Total (scenario, scheme) pairs independently annotated by all reviewers.
3. **Missing ratings:** Exact count and pattern of omitted ratings.
4. **Observed score distribution:** Histogram of ratings across 0, 1, 2, and 3 to test for score-compression bias (e.g., reluctance to use 0 or 3).
5. **Confusion / Disagreement Matrix:** Cross-tabulation of ratings between reviewers to identify systematic divergences in agronomic interpretation.

### 3.3 Decision Gates for Expanding to Full Benchmark (50–100 Scenarios)
- **$\alpha \ge 0.60$ / $\kappa_w \ge 0.60$ (Substantial Agreement):** Proceed directly to full benchmark annotation.
- **$0.40 \le \alpha < 0.60$ / $0.40 \le \kappa_w < 0.60$ (Moderate Agreement):** Conduct a calibration review on disputed items, clarify rubric boundaries for ambiguous cases, and proceed.
- **$\alpha < 0.40$ / $\kappa_w < 0.40$ (Poor Agreement):** Stop pipeline; revise guideline instructions and conduct a second pilot before full dataset generation.
