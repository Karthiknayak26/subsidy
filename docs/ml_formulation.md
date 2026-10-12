# Machine Learning Problem Formulation (Research Stage)

## Status: Under Investigation (Phase 0/3)
The project is currently in the data-feasibility and research phase. The final ML formulation has **not** been prematurely decided. Multiple candidate formulations are being evaluated based on dataset characteristics.

## Candidate Formulations

### Formulation 1: Multi-Label Classification
- **Input:** Feature vector derived from farmer profile (location, land size, crop category, irrigation type, socio-demographic features, need category).
- **Target:** Multi-hot vector over verified government schemes $[y_1, y_2, ..., y_K]$.
- **Pros:** Clear probabilistic interpretation of scheme applicability.
- **Challenges:** Requires ground-truth farmer-scheme enrollment or multi-scheme suitability labels.

### Formulation 2: Learning-to-Rank (LTR) / Information Retrieval
- **Input:** Query $Q$ (Farmer Profile + Current Need) and Document candidate pool $D = \{d_1, d_2, ..., d_m\}$ (Eligible Schemes passing hard rules).
- **Target:** Relevance score $r(Q, d_i) \in \{0, 1, 2, 3\}$.
- **Candidate Models:** RankNet, LambdaMART, CatBoost Ranking, Cross-Encoders.
- **Pros:** Matches real-world decision making where a ranked list of top-$K$ recommendations is required.

### Formulation 3: Two-Stage Hybrid (Rule-Based Filter + Relevance Ranker)
- **Stage 1 (Deterministic Eligibility Filter):** Enforces statutory government requirements (land size limits, category prerequisites, district availability) to eliminate non-eligible schemes.
- **Stage 2 (ML Personalization & Ranking):** Computes context-aware relevance scores between the farmer's immediate need/crop/season context and the eligible schemes.

## Next Steps
1. Conduct exploratory data analysis on the Kisan Call Centre (KCC) query log to examine farmer intention clustering.
2. Verify the size and variance of the candidate scheme master database.
3. Determine feasibility of obtaining historical DBT / scheme beneficiary logs vs. curated scenario evaluation sets.
