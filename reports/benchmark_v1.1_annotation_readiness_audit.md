# Benchmark v1.1 Annotation Readiness Audit

**Repository:** `farmer-benefit-ml`  
**Branch:** `feat/benchmark-v1-1-manifest-preflight`  
**Audit date:** 2026-10-28  
**Auditor:** Antigravity (read-only; no edits, commits, or pushes)

---

## 1. Files Used and Source Provenance

| File | Role | Source |
|------|------|--------|
| `data/benchmarks/v1.1/scenario_matrix.json` | Scenario context source (60 records S071–S130) | Repository — frozen eligibility engine output |
| `data/benchmarks/v1.1/candidate_generation_results.json` | Section A / Section B / disqualified candidate sets | Repository — candidate generation results |
| `scheme_database/processed/scheme_master.json` | Scheme evidence source (all statutory fields) | Repository — scheme master, audit_status VERIFIED |
| `data/annotations/benchmark_v1.1/E1_v1.1_blank.csv` | Reviewer E1 blank scoring template (269 rows) | Repository — committed |
| `data/annotations/benchmark_v1.1/E2_v1.1_blank.csv` | Reviewer E2 blank scoring template (269 rows) | Repository — committed |
| `data/annotations/benchmark_v1.1\section_b_qualitative_review_packet.csv` | Section B qualitative packet (165 rows, with farmer details) | Repository — committed |
| `research/dataset_research/benchmark_v1.1_calibration_rubric.md` | Approved 4-level scoring rubric (0–3) | Repository — Signed-Off (status updated from Conditional Proposal) |
| `research/dataset_research/benchmark_v1.1_methodology_signoff.md` | Formal methodology sign-off | Repository — FORMALLY APPROVED |
| `v11_validate_and_agree.py` | Validation + agreement CLI | Repository — preregistered thresholds |
| `test_v11_validate_and_agree.py` | 18 synthetic unit tests | Repository — all pass |

**Generated artifacts (this audit):**
- `data/annotations/benchmark_v1.1/scenario_context_dossier.csv` (v1.1.1) — 60 scenario records, one per S071–S130
- `data/annotations/benchmark_v1.1/scheme_evidence.csv` (v1.1.1) — 7 scheme evidence records for all distinct Section A scheme IDs

---

## 2. Commands Executed

```
python v11_validate_and_agree.py audit-packets \
  --e1 data/annotations/benchmark_v1.1/E1_v1.1_blank.csv \
  --e2 data/annotations/benchmark_v1.1/E2_v1.1_blank.csv \
  --scenarios data/annotations/benchmark_v1.1/scenario_context_dossier.csv \
  --schemes data/annotations/benchmark_v1.1/scheme_evidence.csv
python v11_validate_and_agree.py section-b \
  --file data/annotations/benchmark_v1.1\section_b_qualitative_review_packet.csv
python test_v11_validate_and_agree.py
```

---

## 3. Test Results

**`test_v11_validate_and_agree.py` — 18/18 tests PASS** (synthetic SYNTH_* fixtures only; no human or AI ratings involved)

---

## 4. Packet Validation Results

### `audit-packets` — RESULT: PASS

| Check | Status | Detail |
|-------|--------|--------|
| E1: 269 candidate rows | PASS | 269 data rows + header |
| E2: 269 candidate rows | PASS | 269 data rows + header |
| E1 rater_id uniformly E1 | PASS | All 269 rows |
| E2 rater_id uniformly E2 | PASS | All 269 rows |
| Exact column order | PASS | `scenario_id,scheme_id,scheme_name,rater_id,relevance_score,relevance_rationale,complementarity_notes` |
| E1/E2 identical ordered (scenario_id, scheme_id) pairs | PASS | 269 pairs, zero mismatches |
| Scenario range S071–S130 only | PASS | 60 unique scenarios |
| All scoring fields blank (E1 & E2) | PASS | relevance_score, relevance_rationale, complementarity_notes all empty |
| No forbidden label/model columns | PASS | No model_score, heuristic_rank, ai_rationale, consensus_label, etc. |
| Scenario dossier: 60 records S071–S130 | PASS | All required columns complete |
| Scheme evidence: 7 distinct Section A schemes | PASS | All required columns complete |
| Context completeness (dossier + evidence vs packet) | PASS | No packet scenario/scheme missing from dossier/evidence |

### `section-b` — RESULT: PASS

| Check | Status | Detail |
|-------|--------|--------|
| Section B qualitative-only | PASS | 165 rows; no `relevance_score` column; no numeric/relevance fields populated |
| Section B includes farmer details | PASS | zone, district, primary_crop, land_size, land_type, social_category, farmer_category, water_access, electricity_access, immediate_need added per scenario_id |

---

## 5. Scenario Context Dossier — Field Completeness

Generated from `scenario_matrix.json` (60 records, S071–S130). All `SCENARIO_REQUIRED` columns per the validation script are present and non-blank:

| Column | Source Field | Status |
|--------|-------------|--------|
| scenario_id | `scenario_id` | Complete (60/60) |
| zone | `zone_id` | Complete (60/60) |
| district | `district` | Complete (60/60) |
| primary_crop | `crop_primary` | Complete (60/60) |
| land_size | `land_size_acres` | Complete (60/60) |
| land_type | `land_type` | Complete (60/60) |
| social_category | `social_category` | Complete (60/60) |
| farmer_category | `farmer_category` | Complete (60/60) |
| water_access | `water_and_irrigation.operational_water_source` | Complete (60/60) |
| electricity_access | `borewell_electric_status` | Complete (60/60) |
| immediate_need | `immediate_need` | Complete (60/60) |
| primary_acute_crisis | `compound_need_details.primary_acute_crisis` | Complete (60/60) |
| secondary_constraints | `compound_need_details.secondary_constraints` | Complete (60/60) |
| urgency | No urgency/timing field in source (`season` is uniform "Kharif 2026" for all rows) | **not recorded** (60/60) |
| income_lakh | `annual_family_income_lakh` | Complete (60/60) — relevant for SCH010_AMBEDKAR income limit |

No forbidden context columns (model_score, heuristic_rank, relevance_score, ai_rationale, consensus_label, etc.) are present.

---

## 6. Scheme Evidence — Field Completeness

Generated from `scheme_master.json`. Seven distinct Section A scheme IDs appear across the 269 candidate pairs:

| Scheme ID | Scheme Name | Audit Status | Source |
|-----------|-------------|-------------|--------|
| SCH001 | PM-KISAN | VERIFIED | pmkisan.gov.in |
| SCH003 | PMKSY-PDMC | VERIFIED | pmksy.gov.in |
| SCH004 | SMAM | VERIFIED | agrimachinery.nic.in |
| SCH005 | Krishi Bhagya Yojana | VERIFIED | raitamitra.karnataka.gov.in |
| SCH008_CENTRAL | Central KCC-MISS | VERIFIED_HISTORICAL_BASELINE | financialservices.gov.in / RBI |
| SCH009 | Soil Health Card | VERIFIED | soilhealth.dac.gov.in |
| SCH010_AMBEDKAR | Ganga Kalyana (SC) | VERIFIED | adcl.karnataka.gov.in / sevasindhu.karnataka.gov.in |

All `SCHEME_REQUIRED` columns are complete (7/7 rows): scheme_id, scheme_name, purpose, intervention, eligibility_requirements, assistance_type, source_references. Each `source_references` cell contains the official source URL, official document URL, audit status, and verification date from the scheme master. A `processing_time_seasonal` column is included with value "not documented" for all schemes (the scheme master does not contain processing-time or seasonal turnaround information).

---

## 7. Unresolved Evidence Gaps and Protocol Handling

**Urgency:** No urgency/timing field exists in `scenario_matrix.json` (the `season` field is uniform "Kharif 2026" for all 60 scenarios). The dossier records urgency as "not recorded" for all 60 rows. The approved rubric (Section 4.4, "Missing Urgency and Implementation Timing") instructs reviewers: do not infer deadlines, crop-failure timelines, or scheme-processing times not documented in the scenario or supporting evidence; assess relevance using the recorded primary crisis, secondary constraints, eligibility requirements, and available timing evidence; and if missing timing information materially affects the rating, explain the uncertainty in the rationale rather than inventing a factual assumption.

**Processing-time / seasonal turnaround information:** Marked "not documented" for all 7 Section A schemes. The scheme master contains `application_period` but no specific processing timelines or seasonal cut-off details beyond what is already captured. This is flagged explicitly rather than claimed as resolved.

All other required dossier fields are complete for all 60 scenarios. All other required evidence fields are complete for all 7 Section A schemes.

---

## 8. Distributed Artifact SHA-256 Checksums

| File | SHA-256 |
|------|---------|
| `data/annotations/benchmark_v1.1/E1_v1.1_blank.csv` | `0FADAEC4AA79AA2C1E4B6D7A713B3C4AD916F4746F2424DC8DD3172AE247C8A9` |
| `data/annotations/benchmark_v1.1/E2_v1.1_blank.csv` | `5E11217171B10A39A4E4F9BF88041653F22DBDEA2D8DDAA4F4DAA21CF8A41D8E` |
| `data/annotations/benchmark_v1.1/scenario_context_dossier.csv` | `51F475E0A7ABBEFFB4D6301FA9C6011D68CA95D574C14CD4E95701683B86B0BF` |
| `data/annotations/benchmark_v1.1/scheme_evidence.csv` | `37DA2453789D1254AD3815D537B019B255E48FB40EF39E47D1DA9714DEB1E697` |
| `data/annotations/benchmark_v1.1\section_b_qualitative_review_packet.csv` | `8FE025B3C05BEABC9E47B0AE6CCA3C64E873B3965727AD5BB1F1A057C406B893` |
| `research/dataset_research/benchmark_v1.1_calibration_rubric.md` | `F605A00DA1505662DE90C99BAC81DDAAC586334FBC9A5C3B7E9D9B4A5A45B2C7` |

---

## 9. Readiness Verdict

**ANNOTATION READINESS: PASS**

- The E1 and E2 blank packets are verified: 269 rows each, correct rater_id (E1/E2), exact column order, all scoring fields blank, identical ordered (scenario_id, scheme_id) pairs covering S071–S130 only.
- The scenario context dossier provides complete context for all 60 scenarios from repository sources only; urgency is marked "not recorded" (no source field exists); income is included from `annual_family_income_lakh`.
- The scheme evidence file provides complete, source-traceable evidence for all 7 distinct Section A schemes; processing-time/seasonal info is explicitly marked "not documented".
- Section B is confirmed qualitative-only (no numeric scoring possible) and now includes farmer details per scenario.
- No model predictions, heuristic ranks, AI ratings, or gold labels appear in any reviewer material.
- All 18 synthetic validation tests pass.
- The `audit-packets` command returns PASS with the dossier and evidence supplied.
- The `section-b` command returns PASS.

**Authorized next step:** Distribute `E1_v1.1_blank.csv` only to Reviewer E1 and `E2_v1.1_blank.csv` only to Reviewer E2, each accompanied by the same approved calibration rubric, synthetic calibration anchors, scenario context dossier, and scheme evidence. Do not share the other reviewer's packet.

**When completed files return:** Save the originals unchanged, run the `agreement` command on them, and only then discuss disagreements. Compute preregistered reliability statistics (quadratic weighted Cohen's kappa ≥ 0.610, ordinal Krippendorff's alpha ≥ 0.670) on the original independent ratings before any consensus discussion.

**Do not:** commit, push, generate ratings, write to `raw/`, or run the ranking evaluation until completed human ratings are collected and the preregistered reliability statistics are computed.
