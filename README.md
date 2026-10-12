# ML-Based Personalized Government Scheme and Subsidy Recommendation System for Farmers

[![Status: Phase 0 (Data & Feasibility)](https://img.shields.io/badge/Status-Phase_0:_Data_&_Problem_Feasibility-blue.svg)](#current-status)
[![Research: College Project](https://img.shields.io/badge/Type-Academic_ML_Research-green.svg)](#project-overview)
[![Focus: Verified Schemes](https://img.shields.io/badge/Ground_Truth-Official_Government_Sources-orange.svg)](#data-integrity-and-trust)

---

## 1. Project Title
**ML-Based Personalized Government Scheme and Subsidy Recommendation System for Farmers**  
*A research-first, data-driven initiative to connect Indian farmers with verifiable government agricultural assistance programs using personalized machine learning ranking.*

---

## 2. Project Overview
Agriculture is the economic backbone for millions of households, yet farmers face continuous financial and operational risks across cropping cycles. Central and state governments introduce substantial financial relief packages, equipment subsidies, input cost concessions, crop insurance, and modernization grants to mitigate these risks.

However, in everyday reality, farmers spend the vast majority of their working hours managing critical farming operations—land preparation, irrigation, pest control, weeding, and harvesting. Most farmers do not have the time or technical means to continually monitor bureaucratic gazettes, ministerial press releases, and complex online portals. Because of this lack of awareness or difficulty finding relevant information, a farmer may sometimes pay the full market price for machinery, seeds, fertilizers, or micro-irrigation equipment even when generous government subsidies and support schemes are actively available for their exact situation.

This project is an academic machine learning research initiative aimed at designing a personalized discovery and recommendation system that Bridges this critical information divide.

---

## 3. Problem Statement
There is an acute informational and accessibility gap between government agricultural support mechanisms and the farming communities eligible to benefit from them.

Specifically:
- **Centralized schemes vs. decentralized awareness:** Comprehensive scheme catalogs exist across various department websites (Agriculture, Horticulture, Rural Development, Water Resources), but they are neither consolidated nor proactively communicated in a tailored manner to the individual cultivator.
- **Rule complexity:** Official guidelines feature complex eligibility rubrics involving combinations of landholding size, caste/social classifications, crop types, agro-climatic zones, and irrigation infrastructure.
- **Mismatch between search and need:** Farmers conceptualize problems around practical needs (e.g., *"I need a borewell pump"*, *"How can I get drip irrigation support for 2 acres of banana?"*), while government portals index schemes strictly by administrative program names and budget heads.

---

## 4. Motivation
The impetus behind developing this system includes:
- **Farmers' Limited Time:** Agricultural management is demanding and seasonal; farmers cannot spend extensive time researching bureaucratic administrative procedures.
- **Fragmented Information:** Scheme announcements are dispersed across Central ministries and State departments, making unified discovery nearly impossible without expert assistance.
- **Difficulty Understanding Eligibility:** Legal, financial, and administrative wording in government circulars is often difficult to parse, leading eligible farmers to assume they do not qualify.
- **Difficulty Finding Relevant Schemes:** Out of dozens of available schemes, locating the specific one or two programs that match a farmer's immediate seasonal need and operational scale is challenging.
- **Lack of Easy Access for Marginalized Farmers:** Small, marginal, and tenant farmers often face literacy barriers, digital divide challenges, and limited institutional advisory access.
- **Potential Benefit of Personalized Recommendations:** By taking a structured profile of a farmer's operational realities, machine learning and rule-based filtering can prune irrelevant noise and surface high-utility assistance programs that directly lower input costs and improve livelihoods.

---

## 5. Proposed Solution
The proposed architecture decouples statutory eligibility verification from relevance ranking to guarantee zero policy hallucination while delivering intelligent personalization:

```
[ Farmer Profile ]
(District, Land Holding, Category, Crop, Irrigation, Immediate Need)
                        │
                        ▼
[ Verified Government Scheme Database ]
(Official Criteria, Quotas, Subsidies, Application Modes)
                        │
                        ▼
[ Stage 1: Eligibility / Statutory Rule Filtering ]
(Deterministic validation against hard constraints: land cap, crop applicability, category)
                        │
                        ▼  [ Candidate Applicable Schemes ]
[ Stage 2: ML Recommendation / Ranking Engine ]
(Relevance scoring based on farmer context, seasonal needs, and profile affinity)
                        │
                        ▼
[ Relevant Ranked Schemes (Top-K) ]
                        │
                        ▼
[ Explanation & Official Actionable Information ]
(Plain-language rationale, verified subsidy amount, required documents, official portal URL)
```

---

## 6. ML Component
The machine learning component is designed to solve a **personalized recommendation and ranking problem**, surfacing the most pertinent schemes for a specific farmer from a filtered pool of eligible candidates.

> **Research Stage Disclosure:**  
> The exact ML formulation has **not** been prematurely finalized. The project team will first complete thorough exploratory data analysis (EDA) on available agricultural query and beneficiary datasets. Based on the empirical distribution, sparsity, and ground-truth structure of the data, the team will formally decide whether a **Multi-Label Classification**, **Learning-to-Rank (LTR)**, or **Hybrid Filter-Ranker** formulation is most scientifically sound and viable.

ML is strictly used to optimize relevance and ranking. Machine learning will **never** be used to invent eligibility conditions or generate speculative subsidy amounts.

---

## 7. Data Sources
This repository maintains rigorous data provenance standards. Official government sources represent the primary source of truth. Any third-party reference sources may only be consulted for initial discovery and must be cross-verified against official portals before entering the project database.

| Source Category | Planned Source / Portal | Purpose in Project |
|---|---|---|
| **Official Government Schemes** | Department of Agriculture & Farmers Welfare, Ministry of Agriculture (agricoop.nic.in, myscheme.gov.in) | Authoritative scheme master criteria and benefits |
| **National Open Data** | [data.gov.in](https://data.gov.in) | Open agricultural statistics, district soil/climate indices, and public scheme records |
| **Kisan Call Centre (KCC)** | Ministry of Agriculture & Farmers Welfare (via data.gov.in) | Real-world farmer queries, crop queries, and regional demand patterns |
| **Karnataka State Sources** | Karnataka Raitha Siri, K-Kisan, Seva Sindhu, Department of Horticulture GoK | State-specific agricultural schemes, subsidy rates, and local requirements |
| **Verified Agricultural Repositories** | ICAR, Krishi Vigyan Kendra (KVK) advisories | Verification of crop cycle conventions and regional terminology |
| **Farmer Survey Data** | Primary field/farmer interactions (if required) | Validation of usability, language clarity, and recommendation relevance |

---

## 8. Kisan Call Centre (KCC) Dataset
The official **Kisan Call Centre (KCC)** dataset (obtained via official open-data channels) logs farmer calls across Indian states and districts, detailing:
- Caller administrative location (State, District, Taluk/Block)
- Sector and Category (Agriculture, Horticulture, Cereals, Fruits, etc.)
- Specific Crop (e.g., Paddy, Banana, Tomato, Maize)
- Query Text & Query Category (Weather, Nutrient Management, Cultural Practices, Subsidies, etc.)
- Official expert answer provided

**Role in Project:**  
The KCC dataset will initially be analyzed to understand the distribution of farmer information needs, regional crop concentrations, and seasonal query spikes. **It is not claimed to be the final ML training dataset.** It serves as an exploratory diagnostic asset to ensure our feature engineering and recommendation logic mirror real farmer inquiries.

---

## 9. Planned Development Phases

- **Phase 0 – Problem Validation & Feasibility:** Define constraints, establish repository structure, inspect initial data assets, and align architectural goals.
- **Phase 1 – Government Scheme Research:** Manually review and catalog the initial set of verified Central and Karnataka state schemes into `scheme_master.xlsx` with official citations.
- **Phase 2 – Dataset Investigation:** Perform comprehensive EDA on the KCC query dataset and relevant agricultural registries; map feature availability and missingness.
- **Phase 3 – ML Problem Formulation:** Determine the formal mathematical formulation (Classification vs. Learning-to-Rank vs. Two-Stage Candidate Retrieval).
- **Phase 4 – Dataset Construction:** Construct structured, reproducible training and evaluation sets with transparent ground-truth labeling and zero synthetic hallucinations.
- **Phase 5 – Baseline Recommendation System:** Implement a transparent, heuristic/rule-based baseline (e.g., TF-IDF / BM25 / deterministic filter) to establish an evaluation benchmark.
- **Phase 6 – ML Model Development:** Train candidate ML ranking/recommendation models against the established baseline.
- **Phase 7 – Rigorous Evaluation:** Evaluate models on held-out test splits using offline information retrieval and ranking metrics.
- **Phase 8 – Farmer Application Prototype:** Build an accessible, clean prototype interface (web/mobile accessible) for inputting farmer profiles and reviewing ranked outputs.
- **Phase 9 – Kannada / SMS / IVR Extension:** Integrate Kannada natural language translation/transliteration and investigate headless telephony/SMS integrations for feature phone accessibility.
- **Phase 10 – Farmer/User Validation:** Conduct pilot feedback sessions with actual cultivators and agricultural extension officers to assess clarity and utility.

---

## 10. Current Status

> **Current Milestone: Phase 0 – Data and Problem Feasibility**

- [x] Research repository structure initialized.
- [x] Documentation templates and data governance principles established.
- [x] Kisan Call Centre dataset identified and downloaded for exploratory inquiry analysis.
- [ ] Scheme research initiated: first 10 verified government schemes under curation with official gazette/portal links.
- [ ] **ML model training has NOT started.** (No models or synthetic profiles have been created).

---

## 11. Planned Evaluation
Evaluation will be conducted rigorously based on the selected ML formulation once Phase 3 is completed.

Potential offline evaluation metrics under consideration:
- **Classification Formulation:** Precision, Recall, Macro/Micro F1-Score.
- **Ranking Formulation:**
  - **Precision@K** ($P@K$) and **Recall@K** ($R@K$) for top-3 and top-5 recommendations.
  - **Mean Reciprocal Rank (MRR)**.
  - **Normalized Discounted Cumulative Gain (NDCG@K)** to reward placing the most crucial schemes at rank 1.

*Note: No experimental metrics or performance numbers are claimed at this stage.*

---

## 12. Data Integrity and Trust
To maintain scientific validity and social trust, the project adheres strictly to the following principles:
1. **Primary Source Reliance:** Every scheme must trace directly to an official `.gov.in`, `.nic.in`, or verified state government publication.
2. **Provenance Tracking:** Every record in `scheme_master.xlsx` must include the official source URL, date of verification, and reviewer ID.
3. **Zero Fabrication:** Under no circumstances will synthetic scheme rules, non-existent benefits, or fabricated eligibility conditions be fed to models.
4. **Transparent Labeling:** If synthetic or augmented farmer scenarios are used for stress-testing ranking algorithms in later stages, they will be strictly demarcated from real-world data.
5. **Clear Model Boundaries:** The ML model is never described as "approving" or "awarding" a subsidy; it is strictly an advisory ranking engine.

---

## 13. Future Accessibility
Because the digital divide is most acute among rural cultivators, the project roadmap includes:
- **Kannada First-Class Localization:** Complete UI translation and scheme explanations rendered in natural, accessible Kannada.
- **Smartphone & Web Application:** Responsive, low-bandwidth web interface with intuitive dropdowns and minimal typing requirement.
- **SMS Integration:** Pushing concise top recommendations and application deadlines via standard SMS.
- **IVR / Voice for Keypad Phones:** Exploring interactive voice response (IVR) so farmers using non-smartphone keypad devices can state their crop and location to receive spoken scheme summaries.

---

## 14. Future Scope
Following core system validation, the project scope may expand to:
- **Geographic Expansion:** Extending scheme coverage from Karnataka to additional states and agro-climatic zones.
- **Crop Diversity:** Incorporating sericulture, floriculture, medicinal crops, and animal husbandry schemes.
- **Real-Time Portal Scraping:** Developing safe, automated monitors for new government scheme notifications.
- **Field Testing:** Partnering with local agricultural colleges, KVKs, and farmers' producer organizations (FPOs) for real-world usability studies.

---

## 15. Project Status / Roadmap

- [x] Project folder initialized and documented
- [ ] Problem validation & literature review
- [ ] Research existing subsidy discovery systems
- [ ] Collect and verify first 10 government schemes
- [ ] Exploratory Data Analysis on KCC dataset
- [ ] Investigate available agricultural datasets
- [ ] Finalize ML problem formulation
- [ ] Construct validated benchmark dataset
- [ ] Build baseline recommendation pipeline
- [ ] Train candidate ML models
- [ ] Offline evaluation & metric benchmarking
- [ ] Build end-user prototype interface
- [ ] Implement Kannada localization
- [ ] Explore SMS / IVR telephony adapters
- [ ] User testing & validation with farmers and field experts
