# System Architecture (Conceptual)

```
+-------------------------------------------------------------+
|                        Farmer Inputs                        |
|  (Location, Land Holding, Category, Crop, Irrigation, Need)  |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                  Stage 1: Rule-Based Engine                 |
|             (Deterministic Statutory Filtering)             |
|   - Evaluates mandatory rules from verified Scheme Master   |
|   - Rejects strictly ineligible schemes                     |
+-------------------------------------------------------------+
                              |
                              v [Candidate Eligible Schemes]
+-------------------------------------------------------------+
|                  Stage 2: ML Ranking Engine                 |
|       (Personalized Context Matching & Scoring)             |
|   - Feature extraction & profile-scheme affinity scoring    |
|   - Computes Top-K scheme rankings                          |
+-------------------------------------------------------------+
                              |
                              v [Ranked Scheme Recommendations]
+-------------------------------------------------------------+
|              Stage 3: Explanation & Delivery                |
|   - Transparent justification ("Why this is recommended")   |
|   - Benefit calculation & required documentation list       |
|   - Multilingual generation (Kannada / English)             |
|   - Channel adapters (Web, Future SMS / IVR)                |
+-------------------------------------------------------------+
```

### Core Architecture Tenet
**No Hallucinated Policies:** The ML model is isolated from policy generation. It strictly operates as a ranker/scorer over verified schemes supplied by verified government databases.
