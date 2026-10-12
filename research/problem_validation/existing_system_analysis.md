# Existing System Analysis & Comparative Baseline

**Target File:** `research/problem_validation/existing_system_analysis.md`  
**Milestone:** Phase 0 — Problem Validation & Feasibility  
**Core Research Question:** *What can our system learn that a simple government search page or Negilu's current scheme presentation does not already do?*

---

## 1. Government Systems

Official government portals—both Central (e.g., [myScheme.gov.in](https://www.myscheme.gov.in/), [agricoop.nic.in](https://agricoop.nic.in/), [PM-KISAN](https://pmkisan.gov.in/), [PMFBY](https://pmfby.gov.in/)) and State-level platforms in Karnataka (e.g., [FRUITS](https://fruits.karnataka.gov.in/), [K-Kisan](https://kkisan.karnataka.gov.in/), [Seva Sindhu](https://sevasindhu.karnataka.gov.in/), and individual departmental websites)—represent the statutory source of truth. However, their information delivery and discovery architectures exhibit severe systemic limitations:

### Architectural & Operational Characteristics
- **Departmental Fragmentation:** Government schemes are siloed across distinct administrative ministries and directorates (Department of Agriculture, Department of Horticulture, Animal Husbandry & Fisheries, Sericulture, and Water Resources / Minor Irrigation). A farmer must visit multiple separate portals to discover benefits that apply to a single integrated farm holding.
- **Search Paradigm (Name-Based vs. Need-Based):** Government portals primarily index schemes by administrative program acronyms and budgetary heads (e.g., *RKVY-RAFTAAR*, *NFSM*, *SMAM*, *PMKSY-PDMC*, *Krishi Bhagya*). A farmer searching for *"drip pipe support for tomato in rainfed land"* cannot easily map their practical operational need to the correct statutory program acronym.
- **Rigid Boolean Filtering (myScheme style):** Platforms like *myScheme* employ extensive questionnaire funnels (10–15 cascading demographic filters). If an input fails a single rigid Boolean rule or if an edge case is encountered, the system either returns zero results (silent failure) or dumps hundreds of unranked state-wide policies without context.
- **Bureaucratic Presentation:** Scheme outputs are typically published as dense legal guidelines, Government Orders (GOs), or PDF circulars written in administrative English or formal Kannada. They lack dynamic financial benefit calculators tailored to a specific farmer's landholding size or social group.
- **Static Eligibility Declarations:** Portals declare statutory rules in legal phrasing (e.g., *"Assistance limited to 2 ha per beneficiary family as per operational guidelines of Sub-Mission on Agricultural Mechanization"*), requiring the farmer to manually calculate whether they qualify and how much subsidy they actually stand to receive.

---

## 2. Negilu (negilukrishi.in)

[Negilu](https://negilukrishi.in/) is an agricultural web platform and PWA operating primarily in Karnataka. A live technical audit of its dedicated schemes section (`/schemes/`) reveals its design philosophy, strengths, and current functional bounds:

### Observed Features & Strengths
- **Localized Presentation (Kannada-First):** The interface provides bilingual (Kannada/English) titles, scheme summaries, and eligibility highlights with clear typography and agricultural iconography.
- **Curated Catalog:** Directly surfaces approximately 19 high-impact Central and Karnataka schemes (e.g., *PM-Kisan*, *PMFBY*, *FRUITS Portal Registration*, *Krishi Yantrikaran / Tractor Subsidy*).
- **Categorical Navigation:** Organizes schemes into broad navigational chips:
  - *For You* (`ನಿಮಗಾಗಿ`)
  - *Subsidy* (`💰 ಸಹಾಯಧನ`)
  - *Insurance* (`🛡️ ವಿಮೆ`)
  - *Loan* (`🏦 ಸಾಲ`)
  - *Other* (`📋 ಇತರೆ`)
- **Actionable Deep Links:** Every scheme card pairs a short eligibility snippet and benefit highlight with a direct link to the respective official government portal (e.g., `https://pmkisan.gov.in/`, `https://fruits.karnataka.gov.in/`).
- **Location Context:** Negilu features GPS/manual district capture, which is heavily leveraged for market mandi crop prices (`ದರಗಳು`) and local weather.

### Structural & Technical Limitations
- **Static Catalog Presentation:** Schemes are presented as fixed editorial cards. The order of schemes is largely uniform rather than dynamically generated from an individualized farmer profile.
- **No Multi-Attribute Farmer Profiling:** Negilu does not ingest or compute against a farmer's detailed operational parameters:
  - Landholding size (e.g., Marginal $<1$ ha vs. Small $1-2$ ha vs. Large $>2$ ha)
  - Crop & cultivation context (e.g., Arecanut vs. Ragi vs. Banana vs. Polyhouse Vegetables)
  - Water infrastructure (Rainfed, Borewell, Canal, Drip)
  - Social / Farmer Category (SC/ST, Women, Small/Marginal, General)
  - Immediate operational intent or distress point (e.g., seed shortage, borewell drilling, tractor attachment, post-harvest storage)
- **Broad / Generalized Eligibility Tags:** Most cards indicate broad recipient categories such as *"All Farmers"* (`ಎಲ್ಲಾ ರೈತರು · ಎಲ್ಲರಿಗೆ`), omitting specific sub-conditions (such as land ceilings, water availability requirements, or prior-benefit cooling periods).
- **Absence of Dynamic Benefit Computation:** Financial benefits are represented as static strings (e.g., `"Rs 6,000/yr"`, `"2% of sum"`, `"Free registration"`). It does not compute tiered subsidy amounts (e.g., 90% subsidy for SC/ST small farmers vs. 50% for general category farmers for micro-irrigation equipment).
- **No Ranking or Recommendation Engine:** Schemes are not ranked by situational urgency, economic impact, or seasonal relevance to a particular farmer.

---

## 3. Gap Identified for Our Proposed System

### The Fundamental Machine Learning Question
> **"What can our system learn that a simple government search page or Negilu's current scheme presentation does not already do?"**

A simple lookup table or keyword search can match text strings. A static web app like Negilu can display a curated list of 19 popular schemes. Neither solves the **personalized contextual relevance problem**.

Our proposed system bridges this gap through a **two-stage architecture** where Machine Learning plays a precise, justifiable role:

```
[ Traditional Portals ]              [ Negilu ]                     [ Our Proposed System ]
  Keyword / PDF Search         Static 19-Scheme Catalog          Individual Farmer Profile Ingestion
           │                                │                                         │
           ▼                                ▼                                         ▼
 Unranked, legal PDFs             Uniform display cards          Stage 1: Deterministic Rule Verification
 (Overwhelming / Siloed)       (No individual profiling)         (Guarantees zero policy hallucination)
                                                                                      │
                                                                                      ▼
                                                                 Stage 2: ML Personalization & Ranking
                                                                 (Learns latent intent, seasonal priority,
                                                                  and farm-need affinity)
                                                                                      │
                                                                                      ▼
                                                                 Top-K Ranked Recommendations with
                                                                 Dynamic Benefit Estimates & Kannada Explanations
```

### Key Gaps Addressed by the Proposed System

| Dimension | Government Portals (myScheme / State Depts) | Negilu (`negilukrishi.in`) | Proposed ML-Based System |
|---|---|---|---|
| **Discovery Mechanism** | Bureaucratic search, rigid Boolean dropdowns, siloed portals | Static catalog with broad categorical tabs | Personalized multi-attribute profiling + ML ranking |
| **Input Profile** | Form fields isolated to single scheme or tedious 15-question forms | None for schemes (district captured primarily for mandi prices) | Comprehensive: Land size, crop, irrigation, social category, seasonal need |
| **Eligibility Verification** | Manual self-check against statutory circulars | Short general text snippet (`ಎಲ್ಲಾ ರೈತರು`) | **Stage 1 Deterministic Engine:** Evaluates exact verified constraints (land cap, crop list, category) |
| **Relevance & Prioritization** | None (alphabetical or unranked list) | None (static editorial order) | **Stage 2 ML Ranking:** Learns which eligible schemes maximize utility given farmer context and intent |
| **Query Intent Resolution** | Keyword matching on scheme names | None (browse-only) | Semantic understanding of farmer inquiries (inspired by KCC query patterns) |
| **Financial Transparency** | General formulas buried in policy text | Static strings (e.g., `"Rs 6,000/yr"`) | Computed subsidy breakdown based on landholding and farmer category |
| **Explainability** | Legal text | Brief description | Actionable plain-language justification: *"Why recommended for you"*, required documents, and next steps |

### What the ML Model Will Specifically Learn
1. **Latent Query & Intent Mapping:** Learning to bridge the semantic divide between how farmers express problems (as observed in KCC query logs—e.g., *"blight on tomato and high fungicide cost"*, *"micro-irrigation pipeline subsidy"*) and formal statutory scheme definitions.
2. **Context-Aware Relevance Ranking:** From a subset of $N$ schemes that pass hard eligibility constraints, learning to rank the top-$K$ most impactful schemes based on:
   - Seasonal urgency (e.g., input/seed subsidies at pre-sowing vs. crop insurance at mid-season vs. post-harvest processing grants)
   - Crop-specific investment intensity (e.g., high capital investment horticulture vs. rainfed coarse cereals)
   - Operational scale affinity (schemes delivering maximum marginal benefit for a 1.5-acre rainfed holding vs. a 10-acre irrigated orchard)
3. **Robustness to Partial Profiles:** Learning to rank meaningfully even when a farmer provides incomplete initial information, progressively refining recommendations as more profile attributes are supplied.
