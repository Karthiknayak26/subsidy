# Machine Learning Problem Formulation & Empirical Validation

## Status: Implemented, Evaluated & Validated (Benchmark v1.2 & APS Milestone)

The machine learning formulation has progressed from initial exploratory research (Phase 0) to a fully implemented, cross-validated, and empirically benchmarked pipeline (Benchmark v1.2 and APS Assignment). 

The system adopts **Formulation 3: Two-Stage Hybrid (Deterministic Statutory Engine + Availability Safeguards + Section A ML Contextual Ranker)**.

---

## 1. The Two-Stage Hybrid Architecture

To guarantee legal validity and prevent hallucinations, the machine learning model is strictly isolated from statutory eligibility decisions:

```
┌────────────────────────────────────────────────────────┐
│               Farmer Profile Query (Q)                 │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│       Stage 1: Deterministic Statutory Engine          │
│             (`src/eligibility/engine.py`)              │
│  - Evaluates land limits, caste, income tax exclusions │
│  - 3-Valued Logic: ELIGIBLE / INELIGIBLE / VERIFY      │
└─────────────┬────────────────────────────┬─────────────┘
              │                            │
              ▼                            ▼
┌───────────────────────────┐┌───────────────────────────┐
│   Disqualified Schemes    ││   Section B: Provisional  │
│ (Explicit statutory keys) ││ (Score-quarantined; y=N/A)│
└───────────────────────────┘└───────────────────────────┘
              │
              ▼
┌────────────────────────────────────────────────────────┐
│     Stage 2: Section A Contextual ML Ranker            │
│          (`src/models/benchmark_v1_2/`)                │
│  - Actionable candidates (2 to 6 schemes per scenario) │
│  - HistGradientBoosting Ranker / Regressor             │
│  - Contextual feature interactions (need × scheme)     │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│               Ranked Top-K Recommendations             │
│               NDCG@3 = 0.8993 | MRR = 0.8120           │
└────────────────────────────────────────────────────────┘
```

---

## 2. Mathematical Problem Formulation

### 2.1 Primary Learning-to-Rank Formulation (Benchmark v1.2)
- **Query $Q_j$:** Structured farmer scenario profile:
  $$Q_j = \{\text{district}_j, \text{zone}_j, \text{land\_acres}_j, \text{farmer\_category}_j, \text{social\_category}_j, \text{primary\_crop}_j, \text{irrigation}_j, \text{electrification}_j, \text{need}_j\}$$
- **Candidate Pool $D(Q_j)$:** Set of Section A actionable schemes that passed statutory eligibility and operational availability filters:
  $$D(Q_j) = \{d_{j,1}, d_{j,2}, \dots, d_{j,m_j}\}, \quad 2 \le m_j \le 6$$
- **Target Variable:** Expert relevance rating $y_{j,i} \in \{0, 1, 2, 3\}$:
  - $0$: Irrelevant or non-urgent given the immediate crisis.
  - $1$: Marginally relevant (secondary benefit).
  - $2$: Relevant (directly addresses operational constraints).
  - $3$: Critically urgent (primary, optimal intervention for immediate distress).
- **Objective Function:** Learn scoring function $f(Q_j, d_{j,i}; \theta)$ such that for any candidate pair $(d_a, d_b)$ where $y_{j,a} > y_{j,b}$, $f(Q_j, d_a) > f(Q_j, d_b)$.

### 2.2 Feature Representation Matrix
The feature extraction pipeline (`src/models/benchmark_v1_2/features.py`) constructs dense feature vectors for each $(Q_j, d_i)$ pair:
1. **Farmer Attributes:** Encoded land holding size, social category one-hot, agro-climatic zone index, primary crop category, irrigation status, income proxy.
2. **Scheme Attributes:** Subsidy type (capital grant, interest subvention, recurring DBT), nodal department, statutory land cap, benefit monetary scale.
3. **Contextual Affinity Interactions:**
   - Need-Scheme semantic matching indicators (e.g., `need_matches_scheme_primary_domain`).
   - Borewell-pump alignment indicators (e.g., dryland farmer + solar pump match).
   - Tenancy compatibility flags.

---

## 3. Training & Cross-Validation Methodology

To prevent data leakage and simulate real-world generalization across Karnataka:

### 3.1 Scenario-Grouped Cross-Validation (GroupKFold)
Candidate pairs from the same farmer scenario $Q_j$ must never span both training and evaluation splits. GroupKFold (grouped on `scenario_id`, $k=5$) ensures that all candidate schemes for any given farmer are evaluated strictly out-of-fold.

### 3.2 Leave-One-Zone-Out (LOZO) Validation
To evaluate transferability to unseen geographic regions, a 10-fold LOZO protocol trains on 9 agro-climatic zones and tests on the completely held-out 10th zone ($Z_1$ through $Z_{10}$).

---

## 4. Evaluation Metrics & Statistical Testing

1. **Normalized Discounted Cumulative Gain (NDCG@3):**
   $$\text{DCG@3} = \sum_{k=1}^{\min(3, m)} \frac{2^{y_{(k)}} - 1}{\log_2(k + 1)}, \quad \text{NDCG@3} = \frac{\text{DCG@3}}{\text{IDCG@3}}$$
   Where $\text{IDCG@3}$ is computed over all actionable Section A candidates for scenario $j$.
2. **Mean Reciprocal Rank (MRR):**
   $$\text{RR} = \frac{1}{\min \{k : y_{(k)} \ge \tau\}}, \quad \tau = 2.0$$
3. **Paired Permutation Test:**
   Non-parametric test with $B = 10,000$ paired permutations evaluates whether $\Delta\text{NDCG@3} = \text{NDCG}_{\text{ML}} - \text{NDCG}_{\text{Base}}$ is significantly greater than zero.

---

## 5. Empirical Results Summary

### 5.1 Benchmark v1.2 Performance ($N=90$, $n=369$)

| Metric | Heuristic Baseline | HistGradientBoosting ML Ranker | Measured Gain ($\Delta$) | Statistical Significance |
|---|:---:|:---:|:---:|:---:|
| **NDCG@3** | 0.7803 | **0.8993** | **+0.1190** | **$p = 0.0001$** ($B = 10{,}000$) |
| **MRR ($\tau \ge 2$)** | 0.7131 | **0.8120** | **+0.0989** | — |
| **LOZO Non-Regression** | — | **10 / 10 Zones** | $\ge 0.000$ in all zones | Passed Gate 3 |

### 5.2 APS Academic Binary Classification Milestone ($N=18$, $n=72$)
Evaluated on a pre-registered held-out scenario split:
- **Logistic Regression (Baseline):** Accuracy = 73.61%, Precision = 0.7407, ROC-AUC = 0.8070
- **Random Forest (Candidate):** Accuracy = 76.39%, Precision = 0.8000, ROC-AUC = 0.8156
- **Observed Accuracy Gain:** $\Delta = +0.0278$ (+2.78%, 2 additional correct predictions out of 72)
- **McNemar's Exact Binomial Test:** $p = 0.8036$ (Fail to reject $H_0$; demonstrates scientific integrity against overclaiming under sample constraints).
- **Cluster-Aware 95% Bootstrap CI ($B=10,000$):** $[-0.0649, +0.1250]$.

---

## 6. Engineering Implementation Files

- **Features & Encoders:** [`src/models/benchmark_v1_2/features.py`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/src/models/benchmark_v1_2/features.py)
- **Model Training & Inference:** [`src/models/benchmark_v1_2/ranker.py`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/src/models/benchmark_v1_2/ranker.py)
- **Ablation Studies:** [`src/models/benchmark_v1_1/ablation.py`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/src/models/benchmark_v1_1/ablation.py)
- **Evaluation Metrics:** [`src/evaluation/metrics.py`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/src/evaluation/metrics.py)
- **Statistical Pipeline:** [`scripts/subsidy_probability_statistics_assignment.py`](file:///c:/Users/User/Desktop/subsidy/farmer-benefit-ml/scripts/subsidy_probability_statistics_assignment.py)
