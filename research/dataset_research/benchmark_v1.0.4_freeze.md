# Benchmark Release Freeze Record — Version 1.0.4

> **IMPORTANT:** This document records the immutable benchmark state of the Karnataka Agricultural Welfare Subsidy & Benefit Discovery Engine for Benchmark v1.0.4.
> All scenario definitions, execution outputs, governance rules, and report artifacts are frozen as of commit `2f5a8788ce6cce07e4c2023eea0d7c696b683cf0`.
> Any subsequent modifications must be versioned under a new release tag (`v1.0.5+` or `v2.0.0`) and must never silently overwrite this benchmark.

---

## 1. Freeze Summary & Release Metadata

| Attribute | Specification |
|:---|:---|
| **Release Tag / Label** | `benchmark-v1.0.4` |
| **Git Commit Hash** | `2f5a8788ce6cce07e4c2023eea0d7c696b683cf0` |
| **Commit Message** | `fix(benchmark): unify all zone runners to shared governance and expand artifact validator to individual profiles and reports` |
| **Freeze Date** | October 25, 2026 |
| **Active Branch** | `main` |
| **Repository URL** | `https://github.com/Karthiknayak26/subsidy.git` |
| **Scenarios in Benchmark** | 60 production benchmark scenarios (`S011`–`S070`) across 10 Agro-Climatic Zones (`Z1`–`Z10`) |
| **Pilot Set (Held Separate)** | `S001`–`S010` (strictly designated as calibration pilot; never blended with evaluation set) |
| **Scheme Master Registry** | 10 parent schemes (`SCH001`–`SCH010`) + 6 implementation children (16 records total) |
| **Test Suite Status** | 167 passed / 0 failed (`python -m pytest tests/`) |
| **Artifact Validator Status** | All 60 scenarios & artifacts pass (`validate_benchmark_artifacts.py`) |
| **Matrix Validator Status** | All dimensions & cross-field checks pass (`validate_benchmark_matrix.py`) |

---

## 2. Frozen Invariants & Governance Architecture

The following components are strictly frozen and protected from unauthorized modification:

1. **Eligibility Rule Engine (`src/eligibility/engine.py`):**
   - Pure, deterministic, stateless eligibility logic.
   - Strictly decoupled from scoring, presentation, and machine learning pipelines.
2. **Scheme Master Registry (`scheme_database/processed/scheme_master.json`):**
   - Canonical 16-record registry defining parameters, exclusions, target categories, and benefits.
3. **Calibration Pilot Scenarios (`S001`–`S010`):**
   - Retained exclusively for annotator calibration and protocol verification.
4. **Shared Governance Module (`src/eligibility/governance.py`):**
   - Single point of truth for all post-engine presentation and scoring governance.
   - Enforces PMFBY/RWBCIS seasonal Intensive Unit (IU) presentation in Section B (scoring disabled).
   - Enforces statutory inheritance precedence (§5.3.3(ii)) over tenancy exclusions.
   - Enforces provisional scheme safeguards (`SCH008_KA_COOP`, `SCH010_VALMIKI` in `S056`, etc.).
   - Enforces PMKSY-PDMC area-cap safeguards (`S058`).
   - All 10 zone runners (`scripts/run_benchmark_z1_execution.py` through `scripts/run_benchmark_z10_execution.py`) import and delegate directly to `apply_governance_safeguard`.

---

## 3. Directory & Artifact Manifest

```
farmer-benefit-ml/
├── data/
│   ├── annotations/                      # Pilot annotations (E1, E2) & future Phase 5 annotations
│   │   ├── E1_annotation_session.json
│   │   ├── E1_annotation_session.csv
│   │   ├── E2_annotation_session.json
│   │   └── E2_annotation_session.csv
│   └── benchmarks/                       # 10 Zone benchmark directories
│       ├── z1/ ... z10/
│       │   ├── Sxxx.json                 # Individual canonical scenario profiles (60 total)
│       │   ├── Sxxx.md                   # Scenario markdown profiles (60 total)
│       │   ├── zX_scenarios.json         # Canonical batch scenario profiles
│       │   └── zX_execution_results.json # Full execution results with governance fields
├── reports/
│   ├── zone_z1_execution_report.md       # Zone execution reports declaring v1.0.4,
│   └── ... zone_z10_execution_report.md  # Section A/B breakdowns, and governance summaries
├── research/dataset_research/
│   ├── annotation_protocol_v1.1.md       # Approved protocol for Phase 5 expert annotation
│   ├── benchmark_v1_design.md            # Benchmark design specification
│   ├── validate_benchmark_artifacts.py   # Comprehensive multi-level artifact validator
│   ├── validate_benchmark_matrix.py      # Multi-dimensional assignment matrix validator
│   └── benchmark_v1.0.4_freeze.md        # This freeze record
├── scripts/
│   ├── run_benchmark_z1_execution.py     # Unified zone execution runners (Z1–Z10)
│   └── ... run_benchmark_z10_execution.py
└── src/
    └── eligibility/
        ├── engine.py                     # Frozen deterministic engine
        ├── governance.py                 # Shared governance safeguard module
        └── models.py                     # Pydantic data models
```

---

## 4. Phase 5 Handover Protocol

With Benchmark v1.0.4 frozen, work proceeds to **Phase 5: Expert Relevance Annotation**:

1. **Protocol Specification:** Governed by `annotation_protocol_v1.1.md`.
2. **Annotation Set:** Production benchmark scenarios `S011`–`S070` (60 scenarios).
3. **Core Methodological Invariant:**
   - **Eligibility $\neq$ Relevance:** Legal qualification does not imply immediate relevance to stated acute need.
   - **Section A Schemes:** Scored on the calibrated 0–3 ordinal scale based purely on farmer profile, stated need, and crop context. Availability is blinded during Phase 1 scoring.
   - **Section B Schemes:** Strictly excluded from numerical scoring (0–3); reviewed qualitatively for verification and policy terms only.
4. **Independent Raters:** Two independent domain experts (E1, E2). Disagreements $|\Delta| \ge 2$ must be preserved for expert adjudication.
5. **Agreement Thresholds:** Evaluation baseline calculation and model training remain blocked until:
   - Quadratic Weighted Cohen's Kappa $\kappa_w \ge 0.61$
   - Ordinal Krippendorff's Alpha $\alpha \ge 0.67$

---

## 5. Phase 5 Annotation Packet Staging Record

| Attribute | Specification |
|:---|:---|
| **Packet Staging Commit** | `fe6bfd666c3cee66bf343a7a6998b2fd967dcb56` |
| **Commit Message** | `feat(annotation): generate blinded E1/E2 annotation packets and dossier for benchmark v1.0.4 under protocol v1.1, update README` |
| **Test Suite Status** | 172 passed / 0 failed (`tests/test_benchmark_annotation_packets.py` added) |
| **Staged Packets** | - `data/annotations/benchmark_v1.0.4/E1_annotation_packet_blank.csv` (283 rows)<br>- `data/annotations/benchmark_v1.0.4/E2_annotation_packet_blank.csv` (283 rows)<br>- `data/annotations/benchmark_v1.0.4/E1_E2_combined_packet_blank.csv` (566 rows)<br>- `data/annotations/benchmark_v1.0.4/section_b_policy_review_packet.csv` (146 rows) |
| **Blinded Dossier** | `research/dataset_research/benchmark_v1.0.4_blinded_annotation_dossier.md` (1,659 lines) |
| **Packet Generator** | `scripts/generate_benchmark_annotation_packet.py` |

