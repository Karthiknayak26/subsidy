# Benchmark v1.0.4 Integrity & Feasibility Audit Report

**Date:** October 2026  
**Status:** Audit Completed  
**Branch / Commit:** `main` (`d90ca9b`)  
**Scope:** Provenance Classification, Data Leakage Audit, and Acceptance Threshold Feasibility  

---

## 1. Provenance Classification: Exploratory Status (`v1.0.4-EXP`)

### Audit Finding
- The completed submissions originated from files titled `AI_R1_annotation_packet_completed.csv` and `AI_R2_annotation_packet_completed.csv`.
- Although these files underwent review and were restructured into `E1` and `E2` formats, their original generation involved AI assistance rather than purely blinded, independent human annotation from scratch.

### Preserved Protocol Boundary
1. **Classification:** The current consensus labels in `data/annotations/benchmark_v1.0.4/consensus_labels_final.csv` are formally designated as **Exploratory / Feasibility Ground Truth (`v1.0.4-EXP`)**.
2. **Human Annotation Milestone:** Official, definitive human benchmark status is reserved until independent human experts produce fresh ratings without seeing or being initialized from AI-generated outputs.
3. **No Premature Claims:** No claims of passing official human agreement gates or proving production-grade human consensus will be made using this exploratory dataset.

---

## 2. Baseline Data Leakage & Mechanism Audit

### Code Audit of `src/models/heuristic_baseline.py`
A line-by-line inspection of the deterministic heuristic baseline confirmed:
- **Input Features Used:** Strictly the farmer's stated `immediate_need` string (from scenario definitions) and candidate scheme identifiers.
- **Labels Accessed:** **Zero.** The baseline ranking function does not import, load, or query `consensus_labels_final.csv`, `paired_annotations_pre_adjudication.csv`, or any annotation scores.
- **Independence:** Rankings are generated deterministically prior to and independent of evaluation.

### Root Cause of High Baseline Performance (NDCG@3 = 0.9818)
The deterministic heuristic baseline achieves a global mean NDCG@3 of **0.9818**:
- **56 of 60 scenarios (93.3%)** achieve a **perfect NDCG@3 of 1.0000**.
- Only **4 scenarios** deviate from 1.0:
  - `S015` (Zone 1): NDCG@3 = `0.9385`
  - `S032` (Zone 4): NDCG@3 = `0.3631`
  - `S055` (Zone 8): NDCG@3 = `0.7003`
  - `S069` (Zone 10): NDCG@3 = `0.9038`

### Explanation (The Decoupled Filter Effect)
In the decoupled architecture, statutory eligibility evaluation occurs **before** ranking. By the time schemes reach Section A, the engine has already pruned dozens of ineligible schemes down to only 2–7 viable candidates per scenario. Because exactly one or two schemes in this small pool directly match the stated need (e.g. `SCH006` for solar pump, `SCH004` for mechanization), a simple need-to-scheme lookup places the highest-utility scheme at rank 1 in nearly every case.

---

## 3. Mathematical Infeasibility of the Pre-Registered ML Acceptance Gate

### Pre-Registered Gate
Under `research/dataset_research/evaluation_preregistration.md` §6:
$$\Delta \overline{\text{NDCG@3}} = \overline{\text{NDCG@3}}_{\text{model}} - \overline{\text{NDCG@3}}_{\text{baseline}} \ge +0.050$$

### Mathematical Ceiling Analysis
| Quantity | Value |
| :--- | :---: |
| Baseline Mean NDCG@3 | `0.9818` |
| Pre-Registered Required Gain ($\Delta$) | `+0.0500` |
| Required Model NDCG@3 | **`1.0318`** |
| Maximum Theoretically Possible NDCG@3 | `1.0000` |
| Maximum Physically Attainable Gain | **`+0.0182`** |

### Audit Determination
- **The +0.050 acceptance threshold is mathematically unattainable on this benchmark.**
- **Protocol Integrity Safeguard:** We do **not** silently lower the pre-registered threshold to artificially declare an ML model "accepted." 
- The +0.050 threshold was pre-registered under the assumption that the baseline would score between 0.70 and 0.85. The high empirical baseline score (0.9818) invalidates this prerequisite assumption.

---

## 4. Scientific Conclusions & Recommended Path Forward

1. **System Sufficiency Finding:**
   In statutory agricultural subsidy discovery, when an accurate deterministic eligibility filter is applied upstream, a transparent deterministic heuristic baseline provides near-optimal recommendations ($0.9818$ NDCG@3), making complex ML rankers largely redundant for standard single-need queries.

2. **Dual-Path Strategy:**
   - **Path A (Primary Milestone):** Document this benchmark as a **Baseline Sufficiency & Feasibility Study**, highlighting that deterministic rules eliminate the hallucination risk of learned models while delivering 98.2% ranking efficiency.
   - **Path B (Exploratory ML Study):** If an ML model (e.g., LightGBM / RankNet) is trained, it must be evaluated as an **Exploratory Comparative Analysis** targeting specific failure modes (e.g., scenarios S032 and S055 where the heuristic dropped, or optimizing MRR from 0.6958 to > 0.85), clearly acknowledging that the pre-registered +0.05 NDCG@3 gate is infeasible due to the baseline ceiling effect.
