# Pilot Version Freeze Record

> **IMPORTANT:** This file records the exact state of the system when Expert Annotation Pilot v1 began.
> Do **not** modify eligibility rules, scheme master records, or scenario definitions while annotation is in progress.
> If a correction is unavoidable, create a new freeze record (v2) and re-run the affected scenarios.

---

## Freeze Summary

| Item | Value |
|:---|:---|
| **Freeze Label** | `pilot-v1.0` |
| **Git Commit Hash** | `7724fa7` |
| **Commit Message** | `Pilot freeze v1.0: eligibility engine 56 tests, pilot S001-S010, annotation form` |
| **Freeze Date (IST)** | 2026-10-12 |
| **Annotators Targeted** | 2-3 independent agricultural domain experts |
| **Scenarios in Pilot** | S001-S010 (10 scenarios) |
| **Schemes in Master** | 10 parent records (SCH001-SCH010) + 6 implementation children |
| **Test Suite** | 56 passed / 0 failed (`python -m pytest tests/ -q --tb=no`) |
| **Coverage (reported)** | ~88% |

---

## File Version Checksums

| File | Role |
|:---|:---|
| `src/eligibility/engine.py` | Deterministic eligibility rule engine |
| `src/eligibility/models.py` | FarmerScenario, SchemeDetermination, enums |
| `src/eligibility/availability.py` | Availability state pipeline |
| `scheme_database/processed/scheme_master.json` | 16-record scheme registry |
| `research/dataset_research/expert_annotation_form.md` | Annotation instrument (pilot, S001-S010) |
| `research/dataset_research/pilot_execution_results.json` | Pre-computed engine outputs for all 10 scenarios |
| `research/dataset_research/case_b_scenario_spec.md` | Scenario specification and protocol |
| `tests/test_eligibility_engine.py` | Full test suite (56 tests) |

---

## What Is Frozen

1. **Scenario definitions (S001-S010):** Farmer profiles, crops, districts, asset lists, and stated needs.
2. **Eligibility rules:** All scheme-specific eligibility logic in `engine.py`.
3. **Scheme master records:** All 16 records in `scheme_master.json` (parent + child).
4. **Annotation form:** The rubric, rating scale, and Section A / Section B structure in `expert_annotation_form.md`.
5. **Scoring scale:** 0 (Irrelevant) to 3 (Highly Relevant), as defined in Section 1.2 of the annotation form.

---

## What Is NOT Frozen (Permitted to Evolve)

- `availability.py` may be updated with live availability evidence **without** triggering re-annotation, as experts score relevance independently of availability.
- The annotation response CSV files (outputs from the annotation CLI) accumulate incrementally.
- The agreement report is generated post-annotation.

---

## Annotation Protocol Safeguards in Effect

| Safeguard | Mechanism |
|:---|:---|
| **Availability blinding** | The annotation CLI (`scripts/run_annotation_session.py`) withholds availability states until the expert explicitly locks Phase 1 relevance scores. |
| **Annotator independence** | Each expert runs a **separate session file** in `data/annotations/`. Scores are not shared before all initial submissions are complete. |
| **REQUIRES_VERIFICATION isolation** | Section B items (provisional schemes) appear only after Phase 1 is locked. No numerical score is requested for them. |
| **Three-output separation** | Storage schema keeps `eligibility_status`, `expert_relevance_score`, and `availability_state` in separate fields. |

---

## Eligibility Engine Key Parameters (Frozen)

| Parameter | Frozen Value | Source |
|:---|:---|:---|
| PM-KISAN exclusion - income tax | Payment (not mere filing) of income tax in last assessment year | Official PM-KISAN Operational Guidelines |
| PM-KISAN family definition | Husband, wife, and minor children | pmkisan.gov.in |
| PM-KISAN pensioner threshold | > Rs.10,000/month for non-MTS retirees | Official guidelines |
| Ganga Kalyana - Ambedkar Corp individual route | 1.5-5 acres; 100% subsidy for borewell + pump + electrification | ADCL verified portal |
| Ganga Kalyana - Ambedkar Corp community route | 8-15 acres pooled; >= 3 beneficiaries required | ADCL verified portal |
| GK other corporations (Valmiki, Devaraj Urs, KMDC) | Provisional - REQUIRES_VERIFICATION | Pending official portal confirmation |
| SCH008_KA_COOP | Provisional - annual GO verification required | Karnataka Cooperative Department |
| SCH007_C (PM-KUSUM Component C) | Related option to verify; not auto-recommended | MNRE guidelines |

---

## How to Reproduce the Pilot Engine Outputs

```powershell
# From project root
python scripts/run_pilot_execution.py
# Output: research/dataset_research/pilot_execution_results.json
```

---

## Next Freeze Trigger

A new freeze (`pilot-v1.1` or `pilot-v2.0`) must be created if any of the following change mid-annotation:
- Any eligibility rule in `engine.py`
- Any field in `scheme_master.json` that affects eligibility determination
- Any scenario attribute in S001-S010
- The rating scale or annotation rubric definitions
