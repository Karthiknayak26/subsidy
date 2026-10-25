# Benchmark v1.0.4 Expert Inter-Rater Reliability Report

**Generated:** 2026-10-25 13:01:43 UTC  
**Benchmark Scope:** S011-S070 (60 Scenarios, 10 Agro-Climatic Zones)  
**Candidate Items Analyzed:** 283 Section A Schemes (100% Coverage)  
**Reliability Gate Status:** **PASS**

---

## 1. Reliability Gate Summary

| Metric | Observed Value | Pre-Registered Threshold | Status |
| :--- | :---: | :---: | :---: |
| **Quadratic Weighted Cohen's Kappa (kappa_w)** | `0.9228` | >= 0.61 | ✅ PASS |
| **Ordinal Krippendorff's Alpha (alpha_ord)** | `0.8485` | >= 0.67 | ✅ PASS |
| **Exact Agreement** | `91.52%` | Diagnostic | Informational |
| **Adjacent Agreement (|Delta| <= 1)** | `100.00%` | Diagnostic | Informational |
| **Disagreements Requiring Adjudication (|Delta| >= 2)** | `0` | 0 unadjudicated | ✅ ZERO |

---

## 2. Rating Distributions

### Score Marginal Frequencies (0–3 Scale)
| Score | E1 Count | E1 Pct | E2 Count | E2 Pct |
| :---: | :---: | :---: | :---: | :---: |
| Score 0 | 13 | 4.6% | 7 | 2.5% |
| Score 1 | 208 | 73.5% | 224 | 79.2% |
| Score 2 | 24 | 8.5% | 14 | 4.9% |
| Score 3 | 38 | 13.4% | 38 | 13.4% |

### Score Difference (|E1 - E2|) Distribution
| Difference ($|\Delta|$) | Pair Count | Percentage | Operational Meaning |
| :---: | :---: | :---: | :--- |
| 0 | 259 | 91.5% | Exact consensus |
| 1 | 24 | 8.5% | Minor boundary variance (e.g. 1 vs 2) |
| 2 | 0 | 0.0% | Clinical divergence (Mandatory Adjudication) |
| 3 | 0 | 0.0% | Polar divergence (Mandatory Adjudication) |

---

## 3. Disagreement Inventory (|E1 - E2| >= 2)

No clinical disagreements (|E1 - E2| >= 2) observed. All 283 candidate ratings are within adjacent range.

---

## 4. Methodological & Pre-Registration Safeguards
1. **Distance Function**: Genuine Ordinal Krippendorff Alpha utilizes cumulative marginal frequencies $\delta^2(g, h) = (\sum_{k=g}^h n_k - \frac{n_g + n_h}{2})^2$ instead of interval distance.
2. **Permanent Calibration Isolation**: Pilot scenarios S001–S010 are strictly excluded from all Benchmark v1.0.4 reliability gates.
3. **Section B Separation**: Section B policy review schemes are entirely excluded from numerical relevance scoring.
4. **Fail-Closed Thresholds**: If either $\kappa_w < 0.61$ or $\alpha_{\text{ord}} < 0.67$, downstream baseline ranking evaluation remains blocked until resolved.
