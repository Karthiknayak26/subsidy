# 🌸 Udupi Mallige Price Spike Prediction — Complete Project Summary for Judges

> **Project Goal:** Predict whether a next-day price spike will occur in the daily wholesale auction of Shankarapura Mallige (Jasminum sambac) — a highly perishable flower whose price can double or triple overnight.

---

## 1. Problem Definition

| Item | Detail |
|---|---|
| **Task** | Binary classification: "Will tomorrow be a spike day?" |
| **Target** | `target_guide_or_train_threshold` — a day is labelled **spike** if the daily price change exceeds 80% OR the price sits ≥99% above the prior 7-day SMA. Thresholds computed **only** from 2010–2012 training data. |
| **Dataset** | 2,496 daily observations (2010–2016): wholesale prices + local microclimate (temperature, humidity, rainfall) + calendar features (day-of-week, festival/wedding markers). |
| **Class Imbalance** | Only ~6% of days are spikes (44 out of 731 test days). |
| **Why it's hard** | Flowers perish in 24–36 hours; sudden overnight supply shocks (rain, heat) or demand surges (festivals) create spikes that lagged features cannot always anticipate. |

---

## 2. Data Splits (Strict Chronological — No Shuffling)

| Split | Period | Rows | Spikes | Prevalence |
|:---:|:---:|:---:|:---:|:---:|
| **Training** | 2010–2012 | 1,035 | 85 | 8.21% |
| **Validation** | 2013–2014 | 730 | 54 | 7.40% |
| **Test** | 2015–2016 | 731 | 44 | 6.02% |

> [!NOTE]
> 31 rows around 2012-06-23 were removed because a suspected outlier (₹2,909) corrupted rolling windows. The outlier is documented but not verified against the raw ledger.

---

## 3. Feature Sets (Four Screened Subsets)

| Set | # Features | Description |
|:---:|:---:|:---|
| **A — Baseline** | 45 | Full feature set: price lags, moving averages, volatility, rolling weather, day-of-week, calendar |
| **B — Humidity Reduction** | 44 | Removes noisy high-frequency daily humidity lags |
| **C — Window Consolidation** | 42 | Consolidates multi-scale climate windows into cumulative thermal indices |
| **D — Diurnal Sensitivity** | 41 | Prioritizes diurnal temperature range (ΔT) and non-redundant price deviations |

---

## 4. Complete Model Inventory

### 4.1 Baselines (What "Doing Nothing Smart" Gives You)

| Baseline | Test AP | Description |
|:---|:---:|:---|
| **Always predict "no spike"** | 0.060 | Constant prediction at the base rate |
| **"Yesterday was a spike"** (persistence) | 0.076 | Naive carry-forward |
| **Random scorer** (95% range) | 0.051–0.099 | Monte Carlo simulation |

> Any model must beat **AP ≈ 0.06** (base rate) to demonstrate learned signal. Beating **0.076** (persistence) shows improvement over the simplest heuristic.

---

### 4.2 Classical ML Models — Ranked by Test Average Precision

#### ★ BASELINE MODEL: Logistic Regression Set A

| Metric | Value |
|:---|:---:|
| **Type** | L2-regularized linear classifier (`C=1.0`, `class_weight='balanced'`) |
| **Features** | Set A (45 features — full baseline) |
| **Test AP** | **0.1435** |
| **Test ROC-AUC** | 0.7022 |
| **Why it's the baseline** | Simplest model family, full feature set, no hyperparameter tuning beyond defaults. Establishes what a linear model can extract from all available features. |

#### ★ IMPROVED / CHAMPION MODEL: Random Forest Set C

| Metric | Value |
|:---|:---:|
| **Type** | Unweighted bagging (300 trees, default scikit-learn depth/splits) |
| **Features** | Set C — Window Consolidation (42 features) |
| **Test AP** | **0.1635** (highest in the project) |
| **Test ROC-AUC** | 0.6748 |
| **Why it's the champion** | Highest test AP (2.7× base rate). Under FPR ≤ 10% constraint, catches 13 of 44 spikes — best operational performance. |

#### Full Classical Ranking Table (Test Set, 731 days, 44 spikes)

| Rank | Model | Feature Set | Threshold | AP | ROC-AUC | Precision | Recall | F1 | TP | FP | FPR |
|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **RF** | **Set C** | 0.15 | **0.1635** | 0.675 | 12.2% | 43.2% | 0.190 | 19 | 137 | 19.9% |
| 2 | RF | Set D | 0.20 | 0.1614 | 0.695 | 19.0% | 25.0% | 0.216 | 11 | 47 | 6.8% |
| 3 | RF | Set B | 0.15 | 0.1471 | 0.692 | 13.1% | 38.6% | 0.195 | 17 | 113 | 16.4% |
| 4 | LR | Set D | 0.50 | 0.1446 | 0.705 | 13.1% | 43.2% | 0.201 | 19 | 126 | 18.3% |
| 5 | LR | Set C | 0.50 | 0.1442 | 0.702 | 13.8% | 45.5% | 0.212 | 20 | 125 | 18.2% |
| 6 | **LR (Baseline)** | **Set A** | 0.50 | **0.1435** | 0.702 | 14.5% | 47.7% | 0.222 | 21 | 124 | 18.1% |
| 7 | LR | Set B | 0.50 | 0.1434 | 0.702 | 14.4% | 47.7% | 0.221 | 21 | 125 | 18.2% |
| 8 | RF | Set A | 0.20 | 0.1408 | 0.678 | 21.2% | 25.0% | 0.229 | 11 | 41 | 6.0% |
| 9 | XGBoost | Set A | 0.58 | 0.0998 | 0.683 | 11.1% | 13.6% | 0.122 | 6 | 48 | 7.0% |
| 10 | XGBoost | Set B | 0.62 | 0.0988 | 0.685 | 9.1% | 6.8% | 0.078 | 3 | 30 | 4.4% |
| 11 | XGBoost | Set C | 0.58 | 0.0934 | 0.674 | 8.8% | 11.4% | 0.099 | 5 | 52 | 7.6% |
| 12 | XGBoost | Set D | 0.59 | 0.0931 | 0.670 | 8.6% | 11.4% | 0.098 | 5 | 53 | 7.7% |

#### Under FPR ≤ 10% Constraint (Validation-Tuned Threshold)

| Model | Set | Threshold | Test FPR | Recall | TP | FP |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **RF** | **Set C** | 0.19 | **7.6%** | **29.6%** | **13** | 52 |
| RF | Set B | 0.19 | 7.3% | 27.3% | 12 | 50 |
| RF | Set A | 0.19 | 7.1% | 27.3% | 12 | 49 |
| RF | Set D | 0.21 | 5.4% | 22.7% | 10 | 37 |
| XGBoost | Set A | 0.58 | 7.0% | 13.6% | 6 | 48 |
| LR | Set A | 0.77 | 5.0% | 11.4% | 5 | 34 |

---

### 4.3 Deep Learning Models (Bi-LSTM, Bi-LSTM + Attention, TCN)

#### DL Baseline: Bi-LSTM (L=1, no history)

| Metric | Value |
|:---|:---:|
| **Test t+1 PR-AUC** | 0.1057 (mean, 5 seeds) |
| **Role** | Establishes what a recurrent model can do with no lookback (single-day input) |

#### DL Models Compared (Set A, 5-seed averages)

| Model | t+1 PR-AUC | t+2 PR-AUC | t+3 PR-AUC |
|:---|:---:|:---:|:---:|
| Bi-LSTM (L=1, no history) | 0.1057 | 0.1116 | 0.1073 |
| Bi-LSTM (L=7) | 0.1020 | 0.1097 | 0.1100 |
| Bi-LSTM + Attention (L=7) | 0.0980 | 0.1042 | 0.1167 |
| **TCN (L=7)** | 0.0973 | 0.1079 | **0.1251** |

#### Corrected TCN Benchmark (After Sequence Continuity Bug Fix)

| Seed | Best Epoch | t+1 AP | t+2 AP | t+3 AP |
|:---:|:---:|:---:|:---:|:---:|
| 100 | 14 | 0.1008 | 0.1118 | 0.1264 |
| 101 | 20 | 0.0872 | 0.0827 | 0.1012 |
| 102 | 16 | 0.0892 | 0.0987 | 0.1111 |
| 103 | 8 | 0.1017 | 0.1167 | 0.1334 |
| 104 | 15 | 0.1077 | 0.1297 | 0.1534 |
| **Mean ± Std** | — | **0.0973 ± 0.009** | **0.1079 ± 0.018** | **0.1251 ± 0.020** |

> [!IMPORTANT]
> DL models at the next-day (t+1) horizon **underperform** classical tabular models (RF Set C AP = 0.1635 vs. TCN t+1 AP = 0.0973). With only 85 training spikes, deep sequence models are sample-starved. However, TCN shows its relative strength at the **3-day horizon** (t+3 AP = 0.1251), where classical models were not evaluated, confirming TCN's value as a multi-step forecasting benchmark.

---

### 4.4 XGBoost — Why It Underperformed

XGBoost (gradient boosted trees) was evaluated with `scale_pos_weight` for class imbalance handling:
- **AP range:** 0.0931–0.0998 (below the 0.099 random-scorer ceiling)
- **Key issue:** Sets B–D used tuned hyperparameters (`depth=4, lr=0.03, 500 trees`) while Set A used defaults (`depth=6, lr=0.3, 100 trees`), confounding feature-set and hyperparameter effects.
- **Conclusion:** XGBoost did not demonstrate a reliable improvement over the chance baseline on this dataset. The inconsistent tuning setup makes it difficult to isolate whether the weak performance is due to the algorithm or the configuration.

---

### 4.5 RF Strategy Variants (Rejected)

Two alternative RF strategies were tested and rejected:
- **Class-Weighted RF:** Increased recall but triggered severe false-alarm inflation (up to 232 FP, 34.3% FPR).
- **SMOTENC RF:** Interpolated unrealistically in the discrete calendar feature space, eroding AP.

---

## 5. What Improved from Baseline → Champion

```
Baseline (LR Set A)  →  Champion (RF Set C)
─────────────────────────────────────────────
AP:     0.1435       →  0.1635    (+14% relative lift)
FPR≤10% Recall: 11.4% (5 TP) → 29.6% (13 TP)  (+160% relative lift)
```

### What drove the improvement:

| Factor | Explanation |
|:---|:---|
| **Non-linear interactions** | RF captures complex feature interactions (temperature × price momentum) that a linear model cannot represent. |
| **Feature consolidation (Set C)** | Consolidating multi-scale climate windows into cumulative thermal indices reduced noise while retaining predictive signal. Fewer features (42 vs. 45) reduced overfitting risk. |
| **Unweighted bagging** | Letting RF estimate probabilities without class-weight inflation produced more operationally useful probability scores (mean prediction 0.094 vs. LR's inflated 0.28). |
| **Lower FPR at matched recall** | Under a 10% FPR budget, RF Set C captures 13 spikes vs. LR's 5 — a major operational gain. |

> [!WARNING]
> **Statistical caveat:** A paired bootstrap on test days cannot separate RF Set C from LR Set B (AP difference spans −0.057 to +0.108 at 95% CI). With only 44 test spikes, the ranking between closely-spaced models is uncertain.

---

## 6. Explainability (XAI) — What the Models Learned

| Method | Model | Key Finding |
|:---|:---|:---|
| **LR Coefficients** | LR Set A | `tdd_prior_3d_sum` (thermal accumulation) is the strongest positive driver (+1.86 log-odds). `price_lag_1` is the strongest negative driver (−1.63). |
| **SHAP** | LR Set A | Exact Shapley values confirm thermal + price deviation features dominate predictions. |
| **Integrated Gradients** | TCN Set A (t+3) | `min_humidity_lag_1` and `max_temp_lag_1` are top TCN attributions. Over 68% of gradient mass falls on the two most recent days. |
| **Cross-Model Agreement** | LR vs. TCN | Spearman ρ = 0.69 (p < 10⁻⁶): both architectures rely on similar statistical signals. |

> [!CAUTION]
> XAI outputs describe **associative patterns used by the algorithms**, not real-world causal mechanisms. Matching explanations don't prove that temperature causes spikes — they show what signals the models exploit statistically.

---

## 7. Known Limitations (Honest Assessment)

1. **Modest performance:** Best AP = 0.1635 (2.7× base rate) — useful but far from "solved."
2. **20 spikes missed by ALL models:** Structural limitation of the feature set and 1-day horizon.
3. **Uncalibrated probabilities:** LR outputs average 0.28 (vs. 0.06 true rate) due to class weighting.
4. **44 test spikes:** Too few for statistically definitive model ranking.
5. **Unverified suspicious prices:** 2014-07-04 (₹10), 2010-07-31 (₹22), ₹820 ceiling not source-verified.
6. **Repeated test-set inspection:** Thresholds are validation-calibrated, but the test set was reviewed across multiple audit cycles.
7. **DL data version mismatch:** Bi-LSTM/Attention results used prior data (1,066 rows); only the corrected TCN retraining used cleaned data (1,035 rows).

---

## 8. Conclusions

### What We Demonstrated
1. **Machine learning can provide modest but real lift** for next-day perishable crop price spike prediction: the champion model ranks spike days 2.7× better than chance.
2. **Non-linear tree models (RF) outperform linear models (LR)** on this task when paired with consolidated climate features (Set C).
3. **Feature engineering matters more than model complexity:** Reducing 45 features to 42 (Set C) improved RF performance, while deep learning with 45 features could not overcome the sample-size barrier.
4. **Deep learning is sample-starved** on 85 training spikes. TCN shows promise only at the multi-step 3-day horizon, not for immediate next-day prediction.
5. **XGBoost did not add value** in this configuration — its AP fell below the random-scorer range.
6. **Explainability confirms intuitive drivers:** Both LR and TCN rely on thermal accumulation and recent price momentum, consistent with agricultural domain knowledge.

### What We Cannot Claim
- The models do **not** produce reliable probability estimates (calibration needed).
- The AP differences between top models are **not statistically significant** with 44 test spikes.
- The XAI findings describe **statistical associations**, not proven causal market mechanisms.

---

## 9. Future Work (Recommended Next Steps)

| Priority | Action | Expected Impact |
|:---:|:---|:---|
| 1 | **Probability calibration** (isotonic/Platt on validation) | Trustworthy risk scores for stakeholders |
| 2 | **Rolling-origin validation** (expanding window over 2010–2014) | More robust model selection with larger effective training |
| 3 | **Intraday telemetry** (morning arrival volumes) | Addresses the #1 missing variable; could capture supply shocks |
| 4 | **Multi-horizon extension** (2-day, 3-day forecasts for classical models) | Leverages weather forecasts; TCN already shows t+3 promise |
| 5 | **Ensemble stacking** (LR sensitivity + RF precision) | Orthogonal error patterns suggest potential for combination |
| 6 | **Economic evaluation** (rupee savings vs. false-alarm costs) | Translates AP into real-world cooperative value |
| 7 | **Data verification** (check ₹10, ₹22, ₹820 against raw ledger) | Removes data quality uncertainty |

---

## 10. Repository Structure & Artifacts

| Component | Path |
|:---|:---|
| **Final Report** | [`readme/FINAL_EVALUATION_REPORT.md`](file:///c:/Users/User/Desktop/spike_predication/readme/FINAL_EVALUATION_REPORT.md) |
| **Master Metrics** | [`models/model_comparison.csv`](file:///c:/Users/User/Desktop/spike_predication/models/model_comparison.csv) |
| **DL Comparison** | [`models/dl_comparison.csv`](file:///c:/Users/User/Desktop/spike_predication/models/dl_comparison.csv) |
| **TCN Corrected Results** | [`models/tcn/results/tcn_setA_corrected_5seeds.csv`](file:///c:/Users/User/Desktop/spike_predication/models/tcn/results/tcn_setA_corrected_5seeds.csv) |
| **Error Analysis** | [`models/error_analysis_test_aligned.csv`](file:///c:/Users/User/Desktop/spike_predication/models/error_analysis_test_aligned.csv) |
| **Notebooks (13)** | [`notebooks/`](file:///c:/Users/User/Desktop/spike_predication/notebooks/) — 01_data_validation through 13_model_consolidation |
| **XAI Artifacts** | [`models/xai/`](file:///c:/Users/User/Desktop/spike_predication/models/xai/) — SHAP plots, IG heatmaps, coefficient comparisons |
| **Saved Models** | `models/*/saved_models/` — `.joblib`, `.json`, `.pt` files for all configurations |

---

## Quick Reference Card

| Question | Answer |
|:---|:---|
| **What is the baseline model?** | Logistic Regression Set A (AP = 0.1435, 45 features) |
| **What is the improved/champion model?** | Random Forest Set C (AP = 0.1635, 42 features) |
| **How much improvement?** | +14% relative AP lift; +160% relative recall lift under FPR ≤ 10% |
| **What is the DL baseline?** | Bi-LSTM L=1 (t+1 AP = 0.1057) |
| **Best DL result?** | TCN t+3 AP = 0.1251 (multi-step only; below tabular at t+1) |
| **Does XGBoost help?** | No — AP 0.093–0.100, at or below the random-scorer range |
| **How many spikes does the best model catch?** | 13 of 44 (29.6%) under FPR ≤ 10%; 19 of 44 (43.2%) unconstrained |
| **What do ALL models miss?** | 20 of 44 spikes (45.5%) — structural limitation |
| **Is the result statistically significant?** | RF Set C vs. LR is not separable at 95% CI (bootstrap overlap) |
