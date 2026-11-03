# Applying Probability and Statistics to Evaluate a Machine Learning Model
## Academic Assignment Guide & Experiment Documentation

**Project:** ML-Based Personalized Government Scheme and Subsidy Recommendation System for Farmers in Karnataka  
**Milestone:** Applied Probability & Statistics Assignment  
**Repository:** `farmer-benefit-ml`  
**Evaluation Target:** Benchmark v1.2 ($N = 90$ scenarios, $n = 369$ candidate pairs across 10 agro-climatic zones)  
**Date:** October 2026  
**Final Verdict:** `PASS WITH WARNINGS` (Methodologically sound, zero data leakage; warnings apply regarding single-annotator label provenance and lack of statistical significance).

---

## 1. Objective & Research Question

This assignment investigates the foundational machine learning evaluation question:

$$\text{"Does an improved machine learning model perform better than a baseline model, or could the observed difference be due to variation in the test sample?"}$$

### Key Principles Demonstrated:
1. **Separation of Statutory Eligibility vs. Predictive Priority:** The frozen deterministic eligibility engine (`src/eligibility/engine.py`) enforces official legal scheme rules (land ceilings, exclusions, caste corporation prerequisites). Machine learning is downstream and prioritizes actionable Section A candidates without overriding statutory exclusions.
2. **Cluster-Preserving Sampling:** Prevents data leakage by splitting at the farmer scenario level ($0\%$ scenario overlap between train and test).
3. **Paired Evaluation:** Tests both baseline and candidate models on the exact same held-out test units ($N = 18$ scenarios, $n = 72$ candidate pairs).
4. **Statistical Estimation (Confidence Intervals):** Uses $10,000$ paired bootstrap replicates (both row-level and cluster-aware) to quantify estimation uncertainty.
5. **Hypothesis Testing (McNemar's Test):** Uses an exact two-sided binomial test on paired discordant predictions to test $H_0: P(\text{Error}_{\text{RF}}) = P(\text{Error}_{\text{LR}})$.
6. **Scientific Integrity & Evidence-Based Decision:** Distinguishes statistical significance from practical significance, reporting honest results without forcing false claims of success.

---

## 2. Experimental Results Summary

Evaluated on the held-out test split ($N = 18$ scenarios, $n = 72$ candidate pairs):

| Evaluation Metric | Baseline Model (Logistic Regression) | Candidate Model (Random Forest) | Measured Gain ($\Delta$) | Statistical Significance |
|---|:---:|:---:|:---:|:---:|
| **Accuracy (Primary)** | **73.61%** (53/72) | **76.39%** (55/72) | **+2.78%** (+0.0278) | $p = 0.8036$ (Not Significant) |
| **Precision** | 0.7407 | 0.8000 | +0.0593 | — |
| **Recall (Sensitivity)** | 0.6250 | 0.6250 | +0.0000 | — |
| **Specificity** | 0.8250 | 0.8750 | +0.0500 | — |
| **F1-Score** | 0.6780 | 0.7018 | +0.0238 | — |
| **ROC-AUC** | 0.8070 | 0.8156 | +0.0086 | — |

### Statistical Inference:
- **Observed Accuracy Difference:** $\Delta = +0.0278$ (+2.78 percentage points, exactly +2 correct predictions out of 72).
- **Cluster-Aware 95% Bootstrap CI ($B = 10,000$):** $[-0.0649, +0.1250]$ (spans zero).
- **Row-Level 95% Bootstrap CI ($B = 10,000$):** $[-0.0833, +0.1389]$ (spans zero).
- **McNemar's Test Contingency Matrix:**
  - $a$ (Both Correct): 46 pairs
  - $b$ (LR Correct, RF Wrong): 7 pairs
  - $c$ (RF Correct, LR Wrong): 9 pairs
  - $d$ (Both Wrong): 10 pairs
  - Total Discordant ($b + c$): 16 pairs
- **Exact Binomial $p$-value:** $p = 0.8036 \gg 0.05$.
- **Decision:** **FAIL TO REJECT $H_0$**. The observed improvement is not statistically significant and is fully consistent with test-sample variation.

---

## 3. Repository Artifacts & Deliverables

All generated submission deliverables are version-controlled and located as follows:

| Deliverable | File Path | Description |
|---|---|---|
| **Jupyter Notebook** | `APS_ASSIGNMENT/subsidy_probability_statistics_assignment.ipynb` | Fully executed, 12-section notebook with rich explanations, KaTeX math, tables, and embedded plots. |
| **Standalone Python Script** | `APS_ASSIGNMENT/subsidy_probability_statistics_assignment.py` | Independent, reproducible Python CLI script that runs the entire pipeline and outputs full statistical results. |
| **Word Report Document** | `APS_ASSIGNMENT/subsidy_probability_statistics_report_formatted.docx` | Formatted academic report including executive summary, problem statement, methodology, metrics, and answers. |
| **PDF Report Document** | `APS_ASSIGNMENT/subsidy_probability_statistics_report_formatted.pdf` | Multipage, publication-ready formatted PDF report with embedded figures and tables. |
| **Figure 1 (Confusion Matrices)** | `APS_ASSIGNMENT/reports/fig1_confusion_matrices.png` | Side-by-side confusion matrices for Logistic Regression and Random Forest. |
| **Figure 2 (ROC Curves)** | `APS_ASSIGNMENT/reports/fig2_roc_curves.png` | ROC curves comparing AUC for both models against the chance diagonal. |
| **Figure 3 (Bootstrap Distribution)** | `APS_ASSIGNMENT/reports/fig3_bootstrap_ci.png` | Bootstrap sampling distribution of accuracy difference with 95% CI bounds and zero effect line. |
| **Figure 4 (McNemar Matrix)** | `APS_ASSIGNMENT/reports/fig4_mcnemar_contingency.png` | 2x2 contingency matrix heatmap illustrating concordant and discordant prediction counts. |

---

## 4. Execution Instructions

### Prerequisites
Ensure dependencies are installed:
```bash
pip install numpy pandas scikit-learn scipy matplotlib seaborn python-docx nbformat nbconvert
```

### Option A: Run the Standalone Python Script
Execute the independent evaluation pipeline from the repository root:
```bash
python APS_ASSIGNMENT/subsidy_probability_statistics_assignment.py
```
This script will:
1. Load the Benchmark v1.2 candidate pair dataset.
2. Partition scenarios into 72 train and 18 held-out test scenarios with zero leakage.
3. Train Logistic Regression (Baseline) and Random Forest (Candidate) models.
4. Compute accuracy, precision, recall, specificity, F1-score, and ROC-AUC.
5. Perform 10,000 paired bootstrap replicates (both row-level and cluster-aware).
6. Execute McNemar's exact binomial test and compute contingency counts.
7. Save updated publication figures into `reports/`.
8. Print a structured terminal report with the final verdict.

### Option B: Execute the Jupyter Notebook
To re-run the complete Jupyter notebook from a clean kernel:
```bash
python -m nbconvert --to notebook --execute --inplace APS_ASSIGNMENT/subsidy_probability_statistics_assignment.ipynb
```
Or open and run it interactively via Jupyter Lab / Notebook:
```bash
jupyter notebook APS_ASSIGNMENT/subsidy_probability_statistics_assignment.ipynb
```

---

## 5. Answers to the Core Evaluation Questions

1. **Did the candidate model achieve a higher observed primary metric?**  
   Yes. Accuracy was 76.39% for Random Forest vs. 73.61% for Logistic Regression.
2. **What was the measured difference?**  
   $\Delta = +0.0278$ (+2.78 percentage points; +2 additional correct predictions out of 72).
3. **What does its 95% confidence interval indicate?**  
   The cluster-aware 95% CI is $[-0.0649, +0.1250]$. Because it encompasses zero, the true difference cannot be distinguished from zero.
4. **What did the hypothesis test conclude?**  
   McNemar's exact paired test yielded $p = 0.8036$. We fail to reject the null hypothesis of equal error probabilities.
5. **Is there statistically significant evidence of improvement at the 5% level?**  
   No ($p = 0.8036 \gg 0.05$).
6. **Is the measured improvement practically meaningful?**  
   No. A net gain of 2 scheme recommendations across 18 diverse farmer profiles does not warrant deploying a non-linear ensemble over an interpretable linear model.
7. **What limitations remain?**  
   Small test sample size ($N = 18$ scenarios, 16 discordant pairs) gives low statistical power (<15% to detect a 3% difference). Furthermore, single-annotator labels lack independent inter-rater reliability.
8. **Does the result establish real-world scheme eligibility or successful subsidy receipt?**  
   No. The experiment evaluates rule-concordance and policy relevance agreement within statutorily filtered candidates, not actual government fund disbursement.

