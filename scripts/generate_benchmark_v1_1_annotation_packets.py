"""
generate_benchmark_v1_1_annotation_packets.py
---------------------------------------------
Generates blinded, independent Expert Annotation Packets for Benchmark v1.1 (S071–S130)
in strict compliance with the formally approved Calibration Rubric and Methodology Sign-Off.

Generates:
- data/annotations/benchmark_v1.1/E1_v1.1_blank.csv (269 Section A candidate rows)
- data/annotations/benchmark_v1.1/E2_v1.1_blank.csv (269 Section A candidate rows)
- data/annotations/benchmark_v1.1/section_b_qualitative_review_packet.csv (Section B qualitative rows)
"""

import csv
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

RESULTS_PATH = REPO_ROOT / "data" / "benchmarks" / "v1.1" / "candidate_generation_results.json"
MATRIX_PATH = REPO_ROOT / "data" / "benchmarks" / "v1.1" / "scenario_matrix.json"
OUTPUT_DIR = REPO_ROOT / "data" / "annotations" / "benchmark_v1.1"


def generate_v1_1_packets():
    if not RESULTS_PATH.exists():
        raise FileNotFoundError(f"Missing candidate generation results at {RESULTS_PATH}")
    if not MATRIX_PATH.exists():
        raise FileNotFoundError(f"Missing scenario matrix at {MATRIX_PATH}")

    with open(RESULTS_PATH, "r", encoding="utf-8") as f:
        gen_results = json.load(f)
    with open(MATRIX_PATH, "r", encoding="utf-8") as f:
        scenario_matrix = json.load(f)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    e1_rows = []
    e2_rows = []
    sec_b_rows = []

    # Process in strict numerical order S071 to S130
    for sc in scenario_matrix:
        sid = sc["scenario_id"]
        res = gen_results.get(sid, {})
        sec_a = res.get("section_a_candidates", [])
        sec_b = res.get("section_b_candidates", [])

        for c in sec_a:
            scheme_id = c["scheme_id"]
            scheme_name = c["scheme_name"]

            e1_rows.append({
                "scenario_id": sid,
                "scheme_id": scheme_id,
                "scheme_name": scheme_name,
                "rater_id": "E1",
                "relevance_score": "",
                "relevance_rationale": "",
                "complementarity_notes": ""
            })

            e2_rows.append({
                "scenario_id": sid,
                "scheme_id": scheme_id,
                "scheme_name": scheme_name,
                "rater_id": "E2",
                "relevance_score": "",
                "relevance_rationale": "",
                "complementarity_notes": ""
            })

        for b in sec_b:
            sec_b_rows.append({
                "scenario_id": sid,
                "scheme_id": b["scheme_id"],
                "scheme_name": b["scheme_name"],
                "governance_status": b["governance_status"],
                "presentation_section": b["presentation_section"],
                "missing_verifications": "; ".join(b.get("missing_verifications", [])),
                "disqualifying_factors": "; ".join(b.get("disqualifying_factors", [])),
                "operational_policy_advisory": ""
            })

    assert len(e1_rows) == len(e2_rows), "Row count mismatch between E1 and E2"
    assert len(e1_rows) == 269, f"Expected 269 Section A candidate rows, got {len(e1_rows)}"

    fieldnames = [
        "scenario_id",
        "scheme_id",
        "scheme_name",
        "rater_id",
        "relevance_score",
        "relevance_rationale",
        "complementarity_notes"
    ]

    e1_path = OUTPUT_DIR / "E1_v1.1_blank.csv"
    e2_path = OUTPUT_DIR / "E2_v1.1_blank.csv"
    sec_b_path = OUTPUT_DIR / "section_b_qualitative_review_packet.csv"

    # Write E1 blank packet
    with open(e1_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(e1_rows)

    # Write E2 blank packet
    with open(e2_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(e2_rows)

    # Write Section B qualitative review packet
    sec_b_fields = [
        "scenario_id",
        "scheme_id",
        "scheme_name",
        "governance_status",
        "presentation_section",
        "missing_verifications",
        "disqualifying_factors",
        "operational_policy_advisory"
    ]
    with open(sec_b_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sec_b_fields)
        writer.writeheader()
        writer.writerows(sec_b_rows)

    print(f"[PACKET GENERATION] Successfully wrote E1 blank packet: {e1_path} ({len(e1_rows)} candidate rows)")
    print(f"[PACKET GENERATION] Successfully wrote E2 blank packet: {e2_path} ({len(e2_rows)} candidate rows)")
    print(f"[PACKET GENERATION] Successfully wrote Section B packet: {sec_b_path} ({len(sec_b_rows)} review rows)")


if __name__ == "__main__":
    generate_v1_1_packets()
