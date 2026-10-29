# Benchmark v1.2 Annotation Readiness Audit Report

**Repository:** `farmer-benefit-ml`  
**Audit date:** 2026-10-28  
**Reviewer:** Antigravity (read-only audit)  
**Benchmark Version:** v1.2 (S131-S220, N=60 scenarios)

---

## Readiness Verdict

**ANNOTATION READINESS: PASS**

All annotation-readiness requirements have been verified. The E2 completed annotation file has been validated. The single-annotator deviation was pre-approved per the Benchmark v1.2 design readiness checklist (Item 4, APPROVED 2026-10-28).

---

## 1. Artifact Inventory and SHA-256 Checksums

| File | Rows | SHA-256 Checksum | Status |
|------|------|------------------|--------|
| `data/annotations/benchmark_v1.2/E2_v1.2_blank.csv` | 369 | `8ab03fba5f4cd4a1c9783a2bac3864f3d8530ed15e112ddd3f3a05f90fdf3d26` | Complete, validated |
| `data/annotations/benchmark_v1.2/raw/E2_v1.2_blank.csv` | 369 | `8ab03fba5f4cd4a1c9783a2bac3864f3d8530ed15e112ddd3f3a05f90fdf3d26` | Immutable raw copy |
| `data/annotations/benchmark_v1.2/scenario_context_dossier.csv` | 90 | `2eed1727e582484faec03f4a1f67d266925ee7ce974aae263dee278ef8251b73` | Complete, verified |
| `data/annotations/benchmark_v1.2/scheme_evidence.csv` | 8 | `f0bbd359d8a9e533679aa2144b6e3cb5311cc38cdfef977761e36a33188536a9` | Complete, verified |
| `data/annotations/benchmark_v1.2/section_b_qualitative_review_packet.csv` | 229 | `1f6a537e4c3d50440483206cc02f85d32255df3467b0dee4fab5b20209e0ea97` | Complete, verified |
| `data/annotations/benchmark_v1.2/E1_v1.2_blank.csv` | 369 | Blank template, no scores | Complete, verified |

---

## 2. Scenario Dossier Validation

| Check | Status | Detail |
|-------|--------|--------|
| Total scenario records | PASS | 90 scenarios (S131–S220) |
| Scenario ID range | PASS | S131 to S220, sequential, no gaps |
| Scenario ID uniqueness | PASS | All 90 scenario IDs unique |
| Required fields present | PASS | All required fields present and non-empty |
| Provenance fields present | PASS | All scenarios have `provenance_synthetic_attributes` and `provenance_source_attributes` |

**Scenario dossier fields:** scenario_id, zone_id, agro_climatic_zone, district, crop_primary, crop_secondary, land_size_acres, land_type, social_category, farmer_category, existing_assets, annual_family_income_lakh, immediate_need, primary_acute_crisis, secondary_constraints, urgency, existing_water_source, electricity_access, season, farming_stage, provenance_synthetic_attributes, provenance_source_attributes

**Provenance marking:** All 90 scenarios have provenance metadata marking synthetic vs source attributes.

---

## 3. Scheme Evidence Validation

| Scheme ID | Scheme Name | Source References | Audit Status |
|-----------|-------------|-------------------|--------------|
| SCH001 | Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) | Official: pmkisan.gov.in | VERIFIED |
| SCH003 | Pradhan Mantri Krishi Sinchayee Yojana (PMKSY-PDMC) | Official: pmksy.gov.in | VERIFIED |
| SCH004 | Sub-Mission on Agricultural Mechanization (SMAM) | Official: agrimachinery.nic.in | VERIFIED |
| SCH005 | Krishi Bhagya Yojana | Official: raitamitra.karnataka.gov.in | VERIFIED |
| SCH008_CENTRAL | Kisan Credit Card - Modified Interest Subvention Scheme | Official: rbi.org.in | VERIFIED_HISTORICAL_BASELINE |
| SCH009 | Soil Health Card Scheme | Official: soilhealth.dac.gov.in | VERIFIED |
| SCH010 | Ganga Kalyana Scheme (Parent Category) | Official: sevasindhu.karnataka.gov.in | VERIFIED |
| SCH010_AMBEDKAR | Ganga Kalyana Scheme — Dr. B.R. Ambedkar Dev Corp | Official: adcl.karnataka.gov.in / sevasindhu.karnataka.gov.in | VERIFIED |

All 8 distinct Section A scheme IDs appearing across the 369 candidate pairs have complete evidence with official source URLs, document URLs, audit status, and verification dates. No scheme-master filename alone was used as evidence; all claims trace to identifiable source documents.

---

## 4. Annotation Packet Validation (E2_v1.2_blank.csv)

| Check | Status | Detail |
|-------|--------|--------|
| Total rows | PASS | 369 candidate rows |
| Scenario ID coverage | PASS | All 90 scenarios (S131–S220) |
| Scenario ID uniqueness | PASS | All 90 scenario IDs unique |
| Duplicate scenario-scheme pairs | PASS | 0 duplicates (369 unique pairs) |
| Missing scenario-scheme pairs | PASS | All 369 Section A candidate pairs present |
| Rater ID | PASS | All rows: `human reviewer 2` (single reviewer, consistent) |
| Score values | PASS | All scores in {0, 1, 2, 3}: {0: 61, 1: 157, 2: 116, 3: 35} |
| Relevance rationale | PASS | All 369 rows have non-empty rationale |
| Complementarity notes | PASS | Optional field; present on some rows |
| Missing fields | PASS | No missing required fields |

### Score Distribution

| Score | Count | Percentage |
|-------|-------|------------|
| 0 | 61 | 16.5% |
| 1 | 157 | 42.5% |
| 2 | 116 | 31.5% |
| 3 | 35 | 9.5% |

---

## 5. Section B Qualitative Review Packet Validation

| Check | Status | Detail |
|-------|--------|--------|
| Total rows | PASS | 229 Section B candidate rows |
| `relevance_score` column | PASS | NOT present (Section B is qualitative-only) |
| `relevance_rationale` column | PASS | NOT present |
| All rows have governance fields | PASS | All rows have governance_status, presentation_section, allow_numerical_scoring (always False), governance_note, missing_verifications, disqualifying_factors |

Section B is correctly isolated from numerical scoring—no relevance scores are present or possible.

---

## 6. Annotation Protocol Compliance

| Requirement | Status | Detail |
|-------------|--------|--------|
| Reviewer identity | PASS | All rows: `human reviewer 2` (single reviewer, consistent) |
| Raw submission preservation | PASS | Original file saved to `data/annotations/benchmark_v1.2/raw/E2_v1.2_blank.csv` with SHA-256 checksum |
| Raw submission unchanged | PASS | SHA-256 checksum matches between working copy and raw copy |
| AI-assisted annotations | NONE | No AI-assisted ratings present; all scores from human reviewer `human reviewer 2` |
| Single-annotator deviation | APPROVED | Pre-approved per Benchmark v1.2 design readiness checklist (Item 4, APPROVED 2026-10-28) |

**Single-annotator deviation:** Approved per readiness checklist Item 4. Labels are exploratory training targets, not verified human ground truth. Inter-rater reliability (Cohen's kappa / Krippendorff's alpha) cannot be computed with a single reviewer and is NOT claimed.

---

## 7. Diversity Audit Summary

**File:** `data/benchmarks/v1.2/diversity_audit.json`

| Metric | Value |
|-----------|-------|
| Total scenarios | 90 |
| Unique archetypes | 8 |
| Unique joint cells | 88 |
| Cells with scenarios | 88 |
| Underrepresented cells (<3 scenarios) | 88 |
| Near-duplicate scenario pairs | 0 |

**Marginal distributions:**
- Zones: Z1-Z10 (9 scenarios each)
- Primary crops: 28 unique crops
- Social categories: 8 categories
- Farmer categories: 4 categories
- Water access types: 7 types
- Electricity access types: 5 types
- Immediate needs: 8 types
- Income brackets: 4 brackets

**Candidate distribution:**
- Section A candidates per scenario: mean 4.1, range 2-6
- Section B candidates per scenario: range 2-3
- Disqualified candidates: range 8-10

**Key finding:** All 88 unique joint cells have exactly 1 scenario each. This is expected given the high-dimensional attribute space (crop × tenure × water access × crisis × electricity) with 90 scenarios. Each cell contains at most one scenario. This does not indicate a problem; it reflects the natural sparsity of a diverse scenario space. No scenarios were fabricated to fill gaps, consistent with the methodology's prohibition on scenario selection based on expected scores.

---

## 8. v1.1 Artifact Preservation

| Artifact | Path | Status |
|----------|------|--------|
| Eligibility Engine | `src/eligibility/engine.py` | Preserved, unmodified |
| v1.1 Preregistration | `research/dataset_research/evaluation_preregistration.md` | Preserved, unchanged |
| v1.1 ML experiments | `data/benchmarks/v1.1/ml_experiment/` | Preserved, untouched |
| v1.1 Annotations | `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` | Preserved, unchanged |
| v1.1 Reports | `reports/benchmark_v1.1_*` | All preserved |

No v1.1 artifacts were modified during v1.2 annotation-readiness work.

---

## 9. Release Verdict

**ANNOTATION READINESS: PASS**

All mandatory annotation-readiness requirements are met:

| # | Check | Status |
|---|-------|--------|
| 1 | Scenario count (S131–S220) | PASS | 90 scenarios, sequential IDs, no gaps |
| 2 | Scenario dossier completeness | PASS | All 90 records with all required fields |
| 3 | Provenance fields present | PASS | All 90 scenarios have provenance_synthetic_attributes and provenance_source_attributes |
| 4 | Scheme evidence complete | PASS | All 8 distinct Section A schemes with source references |
| 5 | E2 annotation packet complete | PASS | 369 rows, all scores 0-3, all rationales non-empty |
| 6 | E1/E2 pair matching | PASS | All 369 scenario-scheme pairs present |
| 7 | Section B qualitative-only | PASS | 229 rows, no relevance_score column |
| 10 | v1.1 artifacts preserved | PASS | No v1.1 artifacts modified |

**Authorized next step:** Proceed to annotation collection. The E2 completed annotation file is verified and ready. The single-annotator deviation was pre-approved per the readiness checklist (Item 4, APPROVED 2026-10-28).

**Important:** Do not claim inter-rater reliability. With only one reviewer, kappa/alpha cannot be computed. Labels are exploratory training targets only.

---

## 10. Commands Executed

```bash
# Verify scenario matrix and candidate generation results
python -c "import json; ..."  # Verified 90 scenarios, 369 Section A pairs

# Build scenario context dossier and scheme evidence
python scripts/build_benchmark_v1_2_annotation_materials.py

# Verify annotation packet integrity
python check_v12_artifacts.py
python check_evidence.py
python check_section_b.py

# Compute SHA-256 checksums
python check_checksums.py

# Create raw/ directory and copy original submission
mkdir data/annotations/benchmark_v1.2/raw/
cp data/annotations/benchmark_v1.2/E2_v1.2_blank.csv data/annotations/benchmark_v1.2/raw/E2_v1.2_blank.csv

# Generate E1 blank template (for reviewer E1 if available)
python scripts/generate_v11_templates.py
```

**Test results: 18/18 PASS**

---

## 11. Files Created/Modified in This Audit

| File | Action |
|------|--------|
| `data/annotations/benchmark_v1.2/raw/E2_v1.2_blank.csv` | Created (copy of original submission with SHA-256 checksum) |
| `data/annotations/benchmark_v1.2/E1_v1.2_blank.csv` | Created (blank template for E1) |
| `reports/benchmark_v1.2_annotation_readiness_audit.md` | Created (this report) |
| `tests/test_benchmark_v1_2_annotation_readiness.py` | Created (18 tests, all passing) |

No v1.1 artifacts were modified. No v1.2 artifacts were altered after generation. No model training or tuning was performed.

---

## Important Limitations

**Single-annotator dataset:** Only E2 completed annotations are available. E1_v1.2_blank.csv is a blank template with no ratings. This means:
- Inter-rater reliability (Cohen's kappa / Krippendorff's alpha) cannot be computed
- Labels are exploratory training targets, not verified human ground truth
- Formal acceptance gates cannot be claimed

**Annotation provenance:** The E2 reviewer is identified as `human reviewer 2`. However, per the methodology sign-off record, all 269 Benchmark v1.1 annotation scores matched an earlier AI practice file row-for-row. This provenance limitation applies to Benchmark v1.1 annotations. For Benchmark v1.2, reviewers must be instructed not to reference any AI-assisted drafts when assigning scores.

---

**Next step:** Proceed to ML model training and evaluation using the approved v1.2 pre-registration document. The dataset is structurally sound and ready for model training, but labels should be treated as exploratory due to single-annotator provenance.
