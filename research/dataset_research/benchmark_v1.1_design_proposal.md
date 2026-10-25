# Benchmark v1.1 Design Proposal: Compound-Need Agricultural Subsidy Ranking Benchmark

**Document Version:** `benchmark-v1.1-proposal-draft`  
**Status:** Pre-Experimental Architecture & Evaluation Specification  
**Predecessor Milestone:** Benchmark `v1.0.4-EXP` Feasibility Audit (`commit 691d6bc`)  
**Target Domain:** Karnataka Agricultural Welfare Subsidy & Benefit Discovery Engine  
**Date:** October 2026  

---

## 1. Executive Context & Evolutionary Rationale

### 1.1 Lessons from Benchmark v1.0.4-EXP
Benchmark `v1.0.4-EXP` successfully established the technical pipeline for deterministic statutory eligibility checking, intake validation, immutable archival, and inter-rater agreement computation. However, the subsequent feasibility audit ([`benchmark_v1.0.4_candidate_set_audit.md`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/research/dataset_research/benchmark_v1.0.4_candidate_set_audit.md)) uncovered a fundamental structural limitation in the evaluation design:

1. **Candidate Pool Compression:** Upstream eligibility filtering compressed the 16-scheme master catalog down to an average of **$4.72$ candidates per scenario**.
2. **Single-Need Artificiality:** Scenarios were constructed around a single isolated `immediate_need` (e.g. `SOLAR_PUMP_INSTALLATION` or `FARM_MECHANIZATION`).
3. **The Heuristic Ceiling Effect:** Because each candidate pool contained exactly one scheme matching that single need, a transparent 1-line heuristic achieved a near-ceiling mean NDCG@3 of **$0.9818$**.
4. **Pre-Registration Infeasibility:** At a baseline of $0.9818$, the pre-registered requirement of $\Delta \overline{\text{NDCG@3}} \ge +0.050$ required reaching an NDCG@3 of $1.0318$, which is mathematically impossible.

### 1.2 Purpose of Benchmark v1.1
Benchmark `v1.1` preserves the frozen deterministic statutory engine (`src/eligibility/engine.py` at commit `7724fa7`), but fundamentally transforms the **ranking challenge** by replacing single-need synthetic archetypes with **realistic, multi-dimensional, compound farmer crisis profiles**. 

In Benchmark `v1.1`, the ranking stage encounters genuine clinical trade-offs between multiple viable, eligible schemes competing for top-3 presentation cards.

---

## 2. Structural Design Principles of Benchmark v1.1

```mermaid
flowchart TD
    subgraph S1 [1. Real-World Farmer Input]
        F1[Compound Needs: Multi-Stress Profile<br/>e.g. Borewell Failure + Seasonal Debt + Pest Attack]
    end

    subgraph S2 [2. Upstream Frozen Engine]
        F1 --> E1[Deterministic Statutory Eligibility Filter<br/>3-Valued Logic: ELIGIBLE / INELIGIBLE / REQUIRES_VERIFICATION]
        E1 --> SEC_A[Section A: Expanded Eligible Pool<br/>6 to 10 Viable Schemes Per Scenario]
        E1 --> SEC_B[Section B: Qualitative Policy Review<br/>Decoupled Schemes & Unknown Titles]
    end

    subgraph S3 [3. Downstream Ranking Challenge]
        SEC_A --> R1[Competing Plausible Choices<br/>Direct Trade-offs between High-Impact Interventions]
        R1 --> M1[Baseline Heuristic: Keyword Lookups Struggle on Multi-Need Ties]
        R1 --> M2[Learned Ranker: Optimizes Multi-Objective Prioritization]
    end
```

### Principle 1: Expanded Candidate Space (Target: 6–10 Eligible Schemes)
In production, farmers qualify for multiple concurrent schemes. Benchmark `v1.1` scenarios are sampled from agrarian profiles with broader asset bases and farming operations (e.g., mixed cropping, horticulture + livestock, dryland + partial lift), ensuring that **6 to 10 valid statutory schemes** qualify into Section A.

### Principle 2: Compound Farmer Needs Architecture
Rather than assigning a singular need string, each scenario in `v1.1` features a **primary acute crisis** accompanied by **secondary acute constraints**:

$$\text{Profile Need} = \{\text{Primary Acute Crisis}, \text{Secondary Working Capital}, \text{Infrastructure Barrier}\}$$

### Principle 3: Elimination of Heuristic Target Collusion
In `v1.0.4-EXP`, the target scheme was unique in the candidate pool. In `v1.1`, every scenario contains **at least two directly competing schemes** with overlapping utility, requiring prioritization based on farm economics, implementation timeline, and cost barriers rather than trivial keyword lookup.

---

## 3. Compound Agrarian Need Archetypes

Benchmark `v1.1` formalizes four realistic agrarian multi-stress archetypes across Karnataka's 10 agro-climatic zones:

### Archetype A: Water Infrastructure Failure + Working Capital Crisis
- **Narrative Context:** A borewell has dried up mid-season in the Central Dry Zone (Zone 4) or Northern Dry Zone (Zone 3); the farmer has standing crops withering, zero water security, and mounting short-term input debt.
- **Competing Eligible Schemes in Section A:**
  1. `SCH006` (PM-KUSUM Component B standalone solar pump — if off-grid source certified)
  2. `SCH005` (Krishi Bhagya farm pond + diesel/solar pump lifting package)
  3. `SCH003` (PMKSY-PDMC micro-irrigation drip to stretch remaining moisture)
  4. `SCH008_CENTRAL` (KCC-MISS subsidized short-term crop credit to reschedule debt)
  5. `SCH001` (PM-KISAN direct income liquidity)
- **Ranking Challenge:** Should the engine prioritize acute water drilling/pumping (`SCH006`/`SCH005`), water conservation (`SCH003`), or emergency credit liquidity (`SCH008_CENTRAL`)? Simple need lookups tie or miss the critical operational sequencing.

### Archetype B: Pest/Climate Damage + Working Capital Liquidity + Mechanization
- **Narrative Context:** A marginal redgram/cotton farmer in Bidar/Kalaburagi (Zone 1/2) experiences severe pink bollworm or pod borer infestation, flower dropping, and cash exhaustion for pesticide sprays.
- **Competing Eligible Schemes in Section A:**
  1. `SCH001` (PM-KISAN unconditional emergency cash transfer)
  2. `SCH004` (SMAM battery/power-operated plant protection sprayers subsidy)
  3. `SCH008_CENTRAL` (KCC-MISS concessional working capital loan for inputs)
  4. `SCH009` (Soil Health Card diagnostic testing)
- **Ranking Challenge:** In the absence of immediate PMFBY indemnity payout (quarantined in Section B), does the farmer benefit more immediately from direct cash liquidity (`SCH001`), spray equipment procurement (`SCH004`), or crop loan restructuring (`SCH008_CENTRAL`)?

### Archetype C: Horticulture Transition + Water Scarcity + High Capital Barrier
- **Narrative Context:** A smallholder in Tumakuru or Kolar (Zone 5) transitioning from rainfed millets to commercial pomegranate/tomato horticulture, facing severe groundwater depletion and high initial capital costs.
- **Competing Eligible Schemes in Section A:**
  1. `SCH007` (MIDH shade-net / polyhouse protected cultivation subsidy)
  2. `SCH003` (PMKSY-PDMC micro-irrigation drip installation)
  3. `SCH005` (Krishi Bhagya farm pond rainwater harvesting)
  4. `SCH009` (Soil Health Card micronutrient testing for horticulture)
  5. `SCH008_CENTRAL` (KCC term credit for plantation development)
- **Ranking Challenge:** Multi-component capital sequencing: micro-irrigation (`SCH003`) is technically useless without water storage (`SCH005`), while protected cultivation (`SCH007`) requires substantial beneficiary co-funding.

### Archetype D: Informal Oral Tenancy + Mechanization Bottleneck
- **Narrative Context:** A tenant farmer in Mandya/Mysuru (Zone 6) operating on oral lease without RTC title deeds, facing acute labor shortage during paddy transplanting/harvesting and high private moneylender rates.
- **Competing Eligible Schemes in Section A:**
  1. `SCH004` (SMAM Custom Hiring Center equipment access)
  2. `SCH009` (Soil Health Card free diagnostic nutrient management)
  3. Other non-title statutory schemes.
- **Ranking Challenge:** Differentiating title-restricted schemes from asset-accessible operational services under legal constraints.

---

## 4. Benchmark Specifications & Quota Matrix

| Dimension | Specification in Benchmark v1.1 |
| :--- | :--- |
| **Total Production Scenarios** | **$N = 60$** (S071 to S130) |
| **Agro-Climatic Coverage** | Exactly 6 scenarios in each of the 10 Agro-Climatic Zones ($Z1$–$Z10$) |
| **Candidate Scheme Pool** | 6 to 10 Section A eligible schemes per scenario ($> 400$ total rating pairs) |
| **Need Complexity** | 100% Compound Needs (Primary Need + Secondary Operational Constraint) |
| **Calibration Pilot** | S001–S010 permanently held separate as historical calibration data |
| **Benchmark Freeze** | S011–S070 preserved immutably as `Benchmark v1.0.4-EXP` baseline reference |

---

## 5. Dual-Human Annotation Protocol (v1.2)

To guarantee uncompromised scientific provenance:
1. **Zero AI Initialization:** Blinded annotation packets (`E1_v1.1_blank.csv` and `E2_v1.1_blank.csv`) will be distributed directly to independent agricultural domain experts without LLM-generated seed scores or suggestions.
2. **Clinical Decision Framework (0–3 Ordinal Scale):**
   - **Score 3 (High Priority Top Recommendation):** Solves the most acute bottleneck with immediate practical impact given the multi-stress profile.
   - **Score 2 (Valuable Secondary Support):** High-utility secondary scheme that synergizes directly with the primary intervention.
   - **Score 1 (Marginal / Low Priority):** Statutorily eligible, but tangential or difficult to operationalize amid compound distress.
   - **Score 0 (Irrelevant / Counterproductive):** Eligible on paper, but inappropriate (e.g. debt-inducing loan when farmer is in insolvency, or unrequested civil works).
3. **Mandatory Audit Rationales:** Every single rating must include clinical reasoning justifying the ranking relative to the competing eligible schemes.
4. **Inter-Rater Reliability Thresholds (Fail-Closed Gates):**
   - **Quadratic Weighted Cohen's Kappa:** $\kappa_w \ge 0.610$
   - **Ordinal Krippendorff's Alpha:** $\alpha_{\text{ord}} \ge 0.670$
   - **Disagreement Adjudication:** Mandatory human panel resolution for all cases where $|E1 - E2| \ge 2$.

---

## 6. Pre-Registered Evaluation Protocol & Acceptance Gate

### 6.1 Baseline Ranking Specification
- **Baseline 1 (Keyword Heuristic):** Standard static need lookup (expected to experience significant degradation from 0.9818 due to compound need ties).
- **Baseline 2 (Interpretable Heuristic with Need + Asset + Complexity Weights):** Transparent deterministic baseline taking compound factors into account, locked before model training.

### 6.2 Pre-Registered Model Acceptance Gate
A learned machine learning ranking model (e.g., LightGBM / LambdaMART, RankNet) will be deemed superior and approved for deployment **if and only if** it satisfies all three pre-registered gates simultaneously:

1. **Substantive Gain Gate:**
   $$\Delta \overline{\text{NDCG@3}} = \overline{\text{NDCG@3}}_{\text{model}} - \overline{\text{NDCG@3}}_{\text{baseline}} \ge +0.050$$
   *(Feasible in v1.1 because the baseline NDCG@3 on compound multi-candidate sets is expected to lie in the range $[0.65, 0.80]$, leaving $> 0.20$ of headroom).*
2. **Statistical Significance Gate:**
   Two-sided paired permutation test on scenario differences ($N=60$, $B=10,000$ sign-flip permutations):
   $$p < 0.050$$
3. **Strict Zone Non-Regression Gate:**
   For every agro-climatic zone $z \in \{Z1 \dots Z10\}$:
   $$\Delta \overline{\text{NDCG@3}}_z \ge 0.000$$

---

## 7. Implementation Roadmap & Governance

| Phase | Milestone Deliverable | Criteria for Progression |
| :---: | :--- | :--- |
| **Phase A** | **Benchmark v1.1 Matrix Specification** | Reconcile 60 compound-need profiles across 10 zones in a formal matrix. |
| **Phase B** | **Eligibility Engine Execution** | Run S071–S130 through frozen `EligibilityEngine`; verify 6–10 candidates per scenario. |
| **Phase C** | **Independent Dual Human Annotation** | Collect fresh E1 and E2 ratings from independent experts with zero AI initialization. |
| **Phase D** | **Agreement Gate & Consensus Freeze** | Confirm $\kappa_w \ge 0.61$, $\alpha \ge 0.67$, adjudicate $|\Delta| \ge 2$, freeze SHA-256 manifest. |
| **Phase E** | **Heuristic Baseline Evaluation** | Evaluate Baseline 1 and 2 on frozen v1.1 consensus ground truth. |
| **Phase F** | **ML Exploration vs. Acceptance Gate** | Train learned ranker using template-grouped CV; evaluate against pre-registered $+0.05$ gate. |

---

## 8. Preserved Historical Invariants
- `v1.0.4-EXP` remains immutably frozen at commit [`691d6bc`](https://github.com/Karthiknayak26/subsidy/commit/691d6bc) as a documented feasibility study.
- S001–S010 calibration pilot remains quarantined in `data/annotations/`.
- Section B policy review schemes remain strictly decoupled from numerical relevance scoring.
