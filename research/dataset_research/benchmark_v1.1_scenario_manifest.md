# Benchmark v1.1 Scenario Manifest & Candidate Specification

**Benchmark Version:** `v1.1` (Compound-Need Re-Architecture)  
**Scenario Range:** `S071` through `S130` ($N = 60$)  
**Coverage:** 10 Agro-Climatic Zones (Z1–Z10), 6 Scenarios Per Zone  
**Eligibility Engine:** Deterministic Frozen Engine (`commit 7724fa7`)  
**Status:** Preflight Candidate Generation Complete — Pending Annotation Packet Distribution  

---

## 1. Candidate Set Size Distribution (Empirically Observed)

| Section A Candidate Count | Number of Scenarios | Percentage | Clinical Characterization |
| :---: | :---: | :---: | :--- |
| **2 schemes** | 5 | 8.3% | Restricted choice (e.g. oral tenancy title exclusions) |
| **3 schemes** | 4 | 6.7% | Restricted choice (e.g. oral tenancy title exclusions) |
| **4 schemes** | 16 | 26.7% | Standard multi-scheme pool (field crops + credit + liquidity) |
| **5 schemes** | 28 | 46.7% | Standard multi-scheme pool (field crops + credit + liquidity) |
| **6 schemes** | 6 | 10.0% | Rich competitive pool (horticulture/solar + credit + mechanization) |
| **7 schemes** | 1 | 1.7% | Rich competitive pool (horticulture/solar + credit + mechanization) |

- **Mean Section A Candidates per Scenario:** `4.48` (Observed Empirical Distribution)
- **Candidate Range:** `2` to `7` schemes

---

## 2. 60-Scenario Master Manifest Table (S071–S130)

| SID | Zone | District | Archetype | Primary Crop | Land (ac) | Primary Acute Crisis | Section A Candidates (Eligible) | Section B (Review Only) |
| :---: | :---: | :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **S071** | `Z1` | Kalaburagi | `ARCH_1` | Redgram | 3.0 | Critical water infrastructure failure (dried/faile... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_VALMIKI` |
| **S072** | `Z1` | Bidar | `ARCH_2` | Soybean | 2.2 | Acute standing crop infestation or weather shock t... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S073** | `Z1` | Kalaburagi | `ARCH_3` | Tomato | 3.5 | High upfront capital barrier for protected horticu... | `SCH001`, `SCH003`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S074** | `Z1` | Bidar | `ARCH_4` | Sugarcane | 2.5 | Severe seasonal labor shortages during critical so... | `SCH004`, `SCH009` | `SCH002`, `SCH008_CENTRAL`, `SCH008_KA_COOP` |
| **S075** | `Z1` | Kalaburagi | `ARCH_5` | Jowar | 3.8 | Recurring prolonged dry-spells threatening rainfed... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S076** | `Z1` | Bidar | `ARCH_6` | Cotton | 4.2 | Acute soil fertility degradation and crop yellowin... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S077** | `Z2` | Raichur | `ARCH_1` | Cotton | 3.0 | Critical water infrastructure failure (dried/faile... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S078** | `Z2` | Kalaburagi | `ARCH_2` | Paddy | 2.2 | Acute standing crop infestation or weather shock t... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S079** | `Z2` | Yadgir | `ARCH_3` | Chilli | 3.5 | High upfront capital barrier for protected horticu... | `SCH001`, `SCH003`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S080** | `Z2` | Raichur | `ARCH_4` | Groundnut | 2.5 | Severe seasonal labor shortages during critical so... | `SCH004`, `SCH005`, `SCH009` | `SCH002`, `SCH008_CENTRAL`, `SCH008_KA_COOP` |
| **S081** | `Z2` | Kalaburagi | `ARCH_5` | Bajra | 3.8 | Recurring prolonged dry-spells threatening rainfed... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_KMDC` |
| **S082** | `Z2` | Yadgir | `ARCH_6` | Redgram | 4.2 | Acute soil fertility degradation and crop yellowin... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S083** | `Z3` | Koppal | `ARCH_1` | Maize | 3.0 | Critical water infrastructure failure (dried/faile... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S084** | `Z3` | Vijayapura | `ARCH_2` | Bengalgram | 2.2 | Acute standing crop infestation or weather shock t... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S085** | `Z3` | Bagalkot | `ARCH_3` | Pomegranate | 3.5 | High upfront capital barrier for protected horticu... | `SCH001`, `SCH003`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S086** | `Z3` | Gadag | `ARCH_4` | Jowar | 2.5 | Severe seasonal labor shortages during critical so... | `SCH004`, `SCH005`, `SCH009` | `SCH002`, `SCH008_CENTRAL`, `SCH008_KA_COOP`, `SCH010_KMDC` |
| **S087** | `Z3` | Koppal | `ARCH_5` | Groundnut | 3.8 | Recurring prolonged dry-spells threatening rainfed... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009`, `SCH010_AMBEDKAR` | `SCH002`, `SCH008_KA_COOP` |
| **S088** | `Z3` | Vijayapura | `ARCH_6` | Wheat | 4.2 | Acute soil fertility degradation and crop yellowin... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_VALMIKI` |
| **S089** | `Z4` | Davanagere | `ARCH_1` | Groundnut | 3.0 | Critical water infrastructure failure (dried/faile... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S090** | `Z4` | Tumakuru | `ARCH_2` | Ragi | 2.2 | Acute standing crop infestation or weather shock t... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S091** | `Z4` | Chitradurga | `ARCH_3` | Papaya | 3.5 | High upfront capital barrier for protected horticu... | `SCH001`, `SCH003`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_KMDC` |
| **S092** | `Z4` | Davanagere | `ARCH_4` | Onion | 2.5 | Severe seasonal labor shortages during critical so... | `SCH004`, `SCH005`, `SCH009`, `SCH010_AMBEDKAR` | `SCH002`, `SCH008_CENTRAL`, `SCH008_KA_COOP` |
| **S093** | `Z4` | Tumakuru | `ARCH_5` | Sunflower | 3.8 | Recurring prolonged dry-spells threatening rainfed... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_VALMIKI` |
| **S094** | `Z4` | Chitradurga | `ARCH_6` | Cotton | 4.2 | Acute soil fertility degradation and crop yellowin... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S095** | `Z5` | Chikkaballapura | `ARCH_1` | Ragi | 3.0 | Critical water infrastructure failure (dried/faile... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S096** | `Z5` | Bengaluru Rural | `ARCH_2` | Mulberry | 2.2 | Acute standing crop infestation or weather shock t... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_KMDC` |
| **S097** | `Z5` | Ramanagara | `ARCH_3` | Capsicum | 3.5 | High upfront capital barrier for protected horticu... | `SCH001`, `SCH003`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009`, `SCH010_AMBEDKAR` | `SCH002`, `SCH008_KA_COOP` |
| **S098** | `Z5` | Kolar | `ARCH_4` | Groundnut | 2.5 | Severe seasonal labor shortages during critical so... | `SCH004`, `SCH005`, `SCH009` | `SCH002`, `SCH008_CENTRAL`, `SCH008_KA_COOP`, `SCH010_VALMIKI` |
| **S099** | `Z5` | Chikkaballapura | `ARCH_5` | Tomato | 3.8 | Recurring prolonged dry-spells threatening rainfed... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S100** | `Z5` | Bengaluru Rural | `ARCH_6` | Capsicum | 4.2 | Acute soil fertility degradation and crop yellowin... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S101** | `Z6` | Mandya | `ARCH_1` | Sugarcane | 3.0 | Critical water infrastructure failure (dried/faile... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_KMDC` |
| **S102** | `Z6` | Mysuru | `ARCH_2` | Paddy | 2.2 | Acute standing crop infestation or weather shock t... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009`, `SCH010_AMBEDKAR` | `SCH002`, `SCH008_KA_COOP` |
| **S103** | `Z6` | Chamarajanagar | `ARCH_3` | Banana | 3.5 | High upfront capital barrier for protected horticu... | `SCH001`, `SCH003`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S104** | `Z6` | Mandya | `ARCH_4` | Maize | 2.5 | Severe seasonal labor shortages during critical so... | `SCH004`, `SCH009` | `SCH002`, `SCH008_CENTRAL`, `SCH008_KA_COOP` |
| **S105** | `Z6` | Mysuru | `ARCH_5` | Banana | 3.8 | Recurring prolonged dry-spells threatening rainfed... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S106** | `Z6` | Chamarajanagar | `ARCH_6` | Turmeric | 4.2 | Acute soil fertility degradation and crop yellowin... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S107** | `Z7` | Shivamogga | `ARCH_1` | Paddy | 3.0 | Critical water infrastructure failure (dried/faile... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009`, `SCH010_AMBEDKAR` | `SCH002`, `SCH008_KA_COOP` |
| **S108** | `Z7` | Chikkamagaluru | `ARCH_2` | Maize | 2.2 | Acute standing crop infestation or weather shock t... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_VALMIKI` |
| **S109** | `Z7` | Hassan | `ARCH_3` | Ginger | 3.5 | High upfront capital barrier for protected horticu... | `SCH001`, `SCH003`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S110** | `Z7` | Shivamogga | `ARCH_4` | Ginger | 2.5 | Severe seasonal labor shortages during critical so... | `SCH004`, `SCH009` | `SCH002`, `SCH008_CENTRAL`, `SCH008_KA_COOP` |
| **S111** | `Z7` | Chikkamagaluru | `ARCH_5` | Coffee | 3.8 | Recurring prolonged dry-spells threatening rainfed... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S112** | `Z7` | Hassan | `ARCH_6` | Ragi | 4.2 | Acute soil fertility degradation and crop yellowin... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S113** | `Z8` | Haveri | `ARCH_1` | Soybean | 3.0 | Critical water infrastructure failure (dried/faile... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_VALMIKI` |
| **S114** | `Z8` | Dharwad | `ARCH_2` | Cotton | 2.2 | Acute standing crop infestation or weather shock t... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S115** | `Z8` | Belagavi | `ARCH_3` | Chilli | 3.5 | High upfront capital barrier for protected horticu... | `SCH001`, `SCH003`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S116** | `Z8` | Haveri | `ARCH_4` | Groundnut | 2.5 | Severe seasonal labor shortages during critical so... | `SCH004`, `SCH005`, `SCH009` | `SCH002`, `SCH008_CENTRAL`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S117** | `Z8` | Dharwad | `ARCH_5` | Chilli | 3.8 | Recurring prolonged dry-spells threatening rainfed... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S118** | `Z8` | Belagavi | `ARCH_6` | Wheat | 4.2 | Acute soil fertility degradation and crop yellowin... | `SCH001`, `SCH004`, `SCH005`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_KMDC` |
| **S119** | `Z9` | Kodagu | `ARCH_1` | Coffee | 3.0 | Critical water infrastructure failure (dried/faile... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S120** | `Z9` | Chikkamagaluru | `ARCH_2` | Black Pepper | 2.2 | Acute standing crop infestation or weather shock t... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S121** | `Z9` | Uttara Kannada | `ARCH_3` | Black Pepper | 3.5 | High upfront capital barrier for protected horticu... | `SCH001`, `SCH003`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S122** | `Z9` | Kodagu | `ARCH_4` | Arecanut | 2.5 | Severe seasonal labor shortages during critical so... | `SCH004`, `SCH009` | `SCH002`, `SCH008_CENTRAL`, `SCH008_KA_COOP` |
| **S123** | `Z9` | Chikkamagaluru | `ARCH_5` | Paddy | 3.8 | Recurring prolonged dry-spells threatening rainfed... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_KMDC` |
| **S124** | `Z9` | Uttara Kannada | `ARCH_6` | Ginger | 4.2 | Acute soil fertility degradation and crop yellowin... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009`, `SCH010_AMBEDKAR` | `SCH002`, `SCH008_KA_COOP` |
| **S125** | `Z10` | Udupi | `ARCH_1` | Paddy | 3.0 | Critical water infrastructure failure (dried/faile... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S126** | `Z10` | Uttara Kannada | `ARCH_2` | Arecanut | 2.2 | Acute standing crop infestation or weather shock t... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_DEVARAJ_URS` |
| **S127** | `Z10` | Dakshina Kannada | `ARCH_3` | Cashew | 3.5 | High upfront capital barrier for protected horticu... | `SCH001`, `SCH003`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP` |
| **S128** | `Z10` | Udupi | `ARCH_4` | Cashew | 2.5 | Severe seasonal labor shortages during critical so... | `SCH004`, `SCH009` | `SCH002`, `SCH008_CENTRAL`, `SCH008_KA_COOP`, `SCH010_KMDC` |
| **S129** | `Z10` | Uttara Kannada | `ARCH_5` | Black Pepper | 3.8 | Recurring prolonged dry-spells threatening rainfed... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009`, `SCH010_AMBEDKAR` | `SCH002`, `SCH008_KA_COOP` |
| **S130** | `Z10` | Dakshina Kannada | `ARCH_6` | Vegetables | 4.2 | Acute soil fertility degradation and crop yellowin... | `SCH001`, `SCH004`, `SCH008_CENTRAL`, `SCH009` | `SCH002`, `SCH008_KA_COOP`, `SCH010_VALMIKI` |

---

## 3. Statutory Intervention Dictionary

Every candidate scheme's factual intervention is strictly bounded by official government circulars:

| Scheme ID | Scheme Name | Statutory Intervention Scope | Official Mandate Citation |
| :--- | :--- | :--- | :--- |
| `SCH001` | PM-KISAN | Direct unconditional income support (Rs. 6,000/yr) providing emergency farm liquidity. | `pmkisan.gov.in` |
| `SCH002` | PMFBY | Yield/weather-indexed crop loss indemnity insurance — quarantined in Section B pending seasonal IU orders. | `pmfby.gov.in` |
| `SCH003` | PMKSY-PDMC | 45–55% capital subsidy for drip/sprinkler installation (capped at 5.0 ha per beneficiary). | `pmksy.gov.in` |
| `SCH004` | SMAM | 40–50% capital procurement subsidy for farm machinery and CHC establishment — distinct from hiring service access. | `agrimachinery.nic.in` |
| `SCH005` | Krishi Bhagya | Integrated in-situ rainwater harvesting package (farm pond, lining, diesel/solar lift pump) for notified dryland taluks. | `raitamitra.karnataka.gov.in` |
| `SCH006` | PM-KUSUM B | 60% capital subsidy for standalone solar agriculture pumps strictly on unenergized off-grid water sources. | `pmkusum.mnre.gov.in` |
| `SCH007` | MIDH | Capital assistance for protected cultivation structures (polyhouse, shade net) and quality planting material for horticulture. | `midh.gov.in` |
| `SCH008_CENTRAL` | Central KCC-MISS | Concessional short-term crop credit (up to Rs. 3 Lakh at 4% prompt repayment) for seasonal operational inputs — strictly not debt restructuring. | `financialservices.gov.in` |
| `SCH009` | Soil Health Card | 100% free statutory diagnostic soil nutrient testing and crop-specific fertilizer recommendations. | `soilhealth.dac.gov.in` |
| `SCH010_AMBEDKAR` | Ganga Kalyana (SC) | 100% subsidized individual borewell drilling with pump energization for SC small/marginal dryland farmers (1.5–5.0 ac). | `adcl.karnataka.gov.in` |

---

*(Automatically compiled by `scripts/generate_benchmark_v1_1_manifest.py`)*
