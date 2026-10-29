#!/usr/bin/env python3
"""
build_benchmark_v1_2_annotation_materials.py
---------------------------------------------
Builds the annotation-ready materials for Benchmark v1.2:

1. scenario_context_dossier.csv - one record per scenario with farmer context
2. scheme_evidence.csv - one record per distinct Section A scheme with statutory evidence
3. E1_v1.2_blank.csv - blank scoring template for reviewer E1
4. E2_v1.2_blank.csv - blank scoring template for reviewer E2
5. section_b_qualitative_review_packet.csv - qualitative-only Section B packet

Design constraints (from benchmark_v1.2_design_proposal.md and preregistration):
- Scenario generation done via frozen eligibility engine (already complete)
- No label quota - candidate sets from eligibility engine only
- Section B remains qualitative-only, score-disabled
- All annotations are blank (no prefilled scores)
- E1 and E2 get identical packet structure with correct rater_ids
- Scheme evidence must be traceable to official sources
"""

from __future__ import annotations

import json
import csv
from pathlib import Path
from collections import Counter, defaultdict
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCH_DIR = REPO_ROOT / "data/benchmarks/v1.2"
ANNOT_DIR = REPO_ROOT / "data/annotations/benchmark_v1.2"
ANNOT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Load sources
# ---------------------------------------------------------------------------
with open(BENCH_DIR / "scenario_matrix.json") as f:
    scenarios = json.load(f)

with open(BENCH_DIR / "candidate_generation_results.json") as f:
    candidate_results = json.load(f)

with open(REPO_ROOT / "scheme_database/processed/scheme_master.json") as f:
    schemes = json.load(f)

scheme_lookup = {s["scheme_id"]: s for s in schemes}

# ---------------------------------------------------------------------------
# 1. Build scenario context dossier
# ---------------------------------------------------------------------------

SCENARIO_DOSSIER_COLUMNS = [
    "scenario_id",
    "zone_id",
    "agro_climatic_zone",
    "district",
    "crop_primary",
    "crop_secondary",
    "land_size_acres",
    "land_type",
    "social_category",
    "farmer_category",
    "existing_assets",
    "annual_family_income_lakh",
    "immediate_need",
    "primary_acute_crisis",
    "secondary_constraints",
    "urgency",
    "existing_water_source",
    "electricity_access",
    "season",
    "farming_stage",
    "provenance_synthetic_attributes",
    "provenance_source_attributes",
]

def build_scenario_dossier(scenarios: list) -> list[dict]:
    """Build one record per scenario for the annotation dossier."""
    rows = []
    for s in scenarios:
        cnd = s.get("compound_need_details", {})
        wtr = s.get("water_and_irrigation", {})
        prov = s.get("provenance", {})

        secondary = cnd.get("secondary_constraints", [])
        if isinstance(secondary, list):
            secondary_str = "; ".join(str(x) for x in secondary)
        else:
            secondary_str = str(secondary) if secondary else ""

        assets = s.get("existing_assets", [])
        if isinstance(assets, list):
            assets_str = "; ".join(str(a) for a in assets)
        else:
            assets_str = str(assets) if assets else ""

        syn_attrs = prov.get("synthetic_attributes", [])
        src_attrs = prov.get("source_attributes", [])

        rows.append({
            "scenario_id": s["scenario_id"],
            "zone_id": s.get("zone_id", ""),
            "agro_climatic_zone": s.get("agro_climatic_zone", ""),
            "district": s.get("district", ""),
            "crop_primary": s.get("crop_primary", ""),
            "crop_secondary": s.get("crop_secondary", ""),
            "land_size_acres": s.get("land_size_acres", ""),
            "land_type": s.get("land_type", ""),
            "social_category": s.get("social_category", ""),
            "farmer_category": s.get("farmer_category", ""),
            "existing_assets": assets_str,
            "annual_family_income_lakh": s.get("annual_family_income_lakh", ""),
            "immediate_need": s.get("immediate_need", ""),
            "primary_acute_crisis": cnd.get("primary_acute_crisis", ""),
            "secondary_constraints": secondary_str,
            "urgency": s.get("urgency", ""),  # urgency field may not exist in matrix
            "existing_water_source": wtr.get("operational_water_source", ""),
            "electricity_access": wtr.get("borewell_electric_status", ""),
            "season": s.get("season", ""),
            "farming_stage": s.get("farming_stage", ""),
            "provenance_synthetic_attributes": "; ".join(syn_attrs) if syn_attrs else "",
            "provenance_source_attributes": "; ".join(src_attrs) if src_attrs else "",
        })
    return rows


# ---------------------------------------------------------------------------
# 2. Build scheme evidence
# ---------------------------------------------------------------------------

SCHEME_EVIDENCE_COLUMNS = [
    "scheme_id",
    "scheme_name",
    "purpose",
    "intervention",
    "eligibility_requirements",
    "assistance_type",
    "source_references",
    "processing_time_seasonal",
]

def build_scheme_evidence(schemes: list, section_a_scheme_ids: set) -> list[dict]:
    """Build one record per distinct Section A scheme with statutory evidence."""
    rows = []
    for s in schemes:
        sid = s["scheme_id"]
        if sid not in section_a_scheme_ids:
            continue

        official_url = s.get("official_source_url", "")
        doc_url = s.get("official_document_url", "")
        audit_status = s.get("audit_status", "")
        verify_date = s.get("verification_date", "")

        # Build source references string
        source_parts = []
        if official_url:
            source_parts.append(f"Official: {official_url}")
        if doc_url:
            source_parts.append(f"Doc: {doc_url}")
        if audit_status:
            source_parts.append(f"Audit: {audit_status}")
        if verify_date:
            source_parts.append(f"Verified: {verify_date}")
        source_str = " | ".join(source_parts) if source_parts else "No source reference available"

        rows.append({
            "scheme_id": sid,
            "scheme_name": s.get("scheme_name", ""),
            "purpose": s.get("benefit_type", ""),
            "intervention": s.get("target_activities", ""),
            "eligibility_requirements": s.get("eligible_conditions", ""),
            "assistance_type": f"{s.get('benefit_type', '')} | {s.get('benefit_rate', '')}".strip(" |"),
            "source_references": source_str,
            "processing_time_seasonal": "not documented",  # scheme_master does not contain processing times
        })
    return rows


# ---------------------------------------------------------------------------
# 3. Build blank annotation templates
# ---------------------------------------------------------------------------

TEMPLATE_COLUMNS = [
    "scenario_id",
    "scheme_id",
    "scheme_name",
    "rater_id",
    "relevance_score",
    "relevance_rationale",
    "complementarity_notes",
]


def build_blank_template(candidate_results: dict, rater_id: str) -> list[dict]:
    """Build a blank scoring template for a reviewer."""
    rows = []
    for sid in sorted(candidate_results.keys()):
        r = candidate_results[sid]
        for c in r.get("section_a_candidates", []):
            rows.append({
                "scenario_id": sid,
                "scheme_id": c["scheme_id"],
                "scheme_name": c["scheme_name"],
                "rater_id": rater_id,
                "relevance_score": "",  # blank
                "relevance_rationale": "",  # blank
                "complementarity_notes": "",  # blank
            })
    return rows


def build_section_b_packet(scenarios: list, candidate_results: dict) -> list[dict]:
    """Build Section B qualitative review packet."""
    rows = []
    for s in scenarios:
        sid = s["scenario_id"]
        r = candidate_results.get(sid, {})
        for c in r.get("section_b_candidates", []):
            rows.append({
                "scenario_id": sid,
                "scheme_id": c["scheme_id"],
                "scheme_name": c["scheme_name"],
                "governance_status": c.get("governance_status", ""),
                "presentation_section": c.get("presentation_section", ""),
                "allow_numerical_scoring": False,  # always False for Section B
                "governance_note": c.get("governance_note", ""),
                "missing_verifications": "; ".join(c.get("missing_verifications", [])),
                "disqualifying_factors": "; ".join(c.get("disqualifying_factors", [])),
            })
    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Collect all distinct Section A scheme IDs
    section_a_scheme_ids = set()
    for sid, r in candidate_results.items():
        for c in r.get("section_a_candidates", []):
            section_a_scheme_ids.add(c["scheme_id"])

    print(f"Total scenarios: {len(scenarios)}")
    print(f"Distinct Section A schemes: {len(section_a_scheme_ids)}: {sorted(section_a_scheme_ids)}")

    # Build dossier
    dossier_rows = build_scenario_dossier(scenarios)
    dossier_path = ANNOT_DIR / "scenario_context_dossier.csv"
    with open(dossier_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SCENARIO_DOSSIER_COLUMNS)
        writer.writeheader()
        writer.writerows(dossier_rows)
    print(f"Wrote {dossier_path} ({len(dossier_rows)} rows)")

    # Build scheme evidence
    evidence_rows = build_scheme_evidence(schemes, section_a_scheme_ids)
    evidence_path = ANNOT_DIR / "scheme_evidence.csv"
    with open(evidence_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SCHEME_EVIDENCE_COLUMNS)
        writer.writeheader()
        writer.writerows(evidence_rows)
    print(f"Wrote {evidence_path} ({len(evidence_rows)} rows)")

    # Build E1 template
    e1_rows = build_blank_template(candidate_results, "E1")
    e1_path = ANNOT_DIR / "E1_v1.2_blank.csv"
    with open(e1_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TEMPLATE_COLUMNS)
        writer.writeheader()
        writer.writerows(e1_rows)
    print(f"Wrote {e1_path} ({len(e1_rows)} rows)")

    # Build E2 template
    e2_rows = build_blank_template(candidate_results, "E2")
    e2_path = ANNOT_DIR / "E2_v1.2_blank.csv"
    with open(e2_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TEMPLATE_COLUMNS)
        writer.writeheader()
        writer.writerows(e2_rows)
    print(f"Wrote {e2_path} ({len(e2_rows)} rows)")

    # Build Section B packet
    sb_rows = build_section_b_packet(scenarios, candidate_results)
    sb_path = ANNOT_DIR / "section_b_qualitative_review_packet.csv"
    with open(sb_path, "w", newline="", encoding="utf-8") as f:
        sb_columns = [
            "scenario_id",
            "scheme_id",
            "scheme_name",
            "governance_status",
            "presentation_section",
            "allow_numerical_scoring",
            "governance_note",
            "missing_verifications",
            "disqualifying_factors",
        ]
        writer = csv.DictWriter(f, fieldnames=sb_columns)
        writer.writeheader()
        writer.writerows(sb_rows)
    print(f"Wrote {sb_path} ({len(sb_rows)} rows)")

    # Build blank templates for v1.1 (from v1.1 candidate generation results)
    v11_candidates_path = REPO_ROOT / "data/benchmarks/v1.1/candidate_generation_results.json"
    if v11_candidates_path.exists():
        with open(v11_candidates_path, "r", encoding="utf-8") as f:
            v11_candidate_results = json.load(f)

        v11_e1_rows = build_blank_template(v11_candidate_results, "E1")
        v11_e2_rows = build_blank_template(v11_candidate_results, "E2")

        v11_e1_path = REPO_ROOT / "data/annotations/benchmark_v1.1/E1_v1.1_blank.csv"
        v11_e2_path = REPO_ROOT / "data/annotations/benchmark_v1.1/E2_v1.1_blank.csv"

        with open(v11_e1_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=TEMPLATE_COLUMNS)
            writer.writeheader()
            writer.writerows(v11_e1_rows)
        print(f"Wrote {v11_e1_path} ({len(v11_e1_rows)} rows)")

        with open(v11_e2_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=TEMPLATE_COLUMNS)
            writer.writeheader()
            writer.writerows(v11_e2_rows)
        print(f"Wrote {v11_e2_path} ({len(v11_e2_rows)} rows)")

    print(f"\nSummary:")
    total_section_a = sum(len(r.get("section_a_candidates", [])) for r in candidate_results.values())
    total_section_b = sum(len(r.get("section_b_candidates", [])) for r in candidate_results.values())
    print(f"\nSummary:")
    print(f"  Total scenarios: {len(scenarios)}")
    print(f"  Total Section A candidate rows: {total_section_a}")
    print(f"  Total Section B candidate rows: {total_section_b}")
    print(f"  Distinct Section A schemes: {len(section_a_scheme_ids)}")
    print(f"  E1 template rows: {len(e1_rows)}")
    print(f"  E2 template rows: {len(e2_rows)}")
    print(f"  Section B rows: {len(sb_rows)}")


if __name__ == "__main__":
    main()
