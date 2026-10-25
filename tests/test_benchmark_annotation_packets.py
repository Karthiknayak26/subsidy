"""
tests/test_benchmark_annotation_packets.py
-------------------------------------------
Automated test suite verifying the integrity, blinding, and structural compliance
of Benchmark v1.0.4 Annotation Packets under Protocol v1.1.
"""

import csv
from pathlib import Path
import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKET_DIR = REPO_ROOT / "data/annotations/benchmark_v1.0.4"
DOSSIER_PATH = REPO_ROOT / "research/dataset_research/benchmark_v1.0.4_blinded_annotation_dossier.md"


def test_packet_files_exist():
    """Verify that all required annotation packets and dossier exist."""
    assert PACKET_DIR.exists(), f"Packet directory {PACKET_DIR} does not exist"
    assert (PACKET_DIR / "E1_annotation_packet_blank.csv").exists()
    assert (PACKET_DIR / "E2_annotation_packet_blank.csv").exists()
    assert (PACKET_DIR / "E1_E2_combined_packet_blank.csv").exists()
    assert (PACKET_DIR / "section_b_policy_review_packet.csv").exists()
    assert DOSSIER_PATH.exists()


def test_e1_and_e2_relevance_packets():
    """Verify E1 and E2 relevance scoring packets adhere to protocol v1.1."""
    e1_file = PACKET_DIR / "E1_annotation_packet_blank.csv"
    e2_file = PACKET_DIR / "E2_annotation_packet_blank.csv"

    with open(e1_file, "r", encoding="utf-8") as f:
        e1_rows = list(csv.DictReader(f))
    with open(e2_file, "r", encoding="utf-8") as f:
        e2_rows = list(csv.DictReader(f))

    assert len(e1_rows) == 283, f"Expected 283 rows for E1, got {len(e1_rows)}"
    assert len(e2_rows) == 283, f"Expected 283 rows for E2, got {len(e2_rows)}"

    for row in e1_rows:
        assert row["rater_id"] == "E1"
        assert row["relevance_score"] == "", "Relevance score must be blank"
        assert row["rationale"] == "", "Rationale must be blank"
        sid = row["scenario_id"]
        assert sid.startswith("S")
        sid_num = int(sid[1:])
        assert 11 <= sid_num <= 70, f"Scenario {sid} is outside S011-S070 benchmark scope"
        assert "availability_state" not in row, "Availability must remain blinded in Phase 1"

    for row in e2_rows:
        assert row["rater_id"] == "E2"
        assert row["relevance_score"] == "", "Relevance score must be blank"
        assert row["rationale"] == "", "Rationale must be blank"
        sid = row["scenario_id"]
        assert sid.startswith("S")
        sid_num = int(sid[1:])
        assert 11 <= sid_num <= 70, f"Scenario {sid} is outside S011-S070 benchmark scope"
        assert "availability_state" not in row, "Availability must remain blinded in Phase 1"

    # Pairwise symmetry
    for r1, r2 in zip(e1_rows, e2_rows):
        assert r1["scenario_id"] == r2["scenario_id"]
        assert r1["scheme_id"] == r2["scheme_id"]


def test_combined_relevance_packet():
    """Verify combined packet contains exactly 566 interleaved rows (283 for E1 + 283 for E2)."""
    comb_file = PACKET_DIR / "E1_E2_combined_packet_blank.csv"
    with open(comb_file, "r", encoding="utf-8") as f:
        comb_rows = list(csv.DictReader(f))

    assert len(comb_rows) == 566
    e1_sub = [r for r in comb_rows if r["rater_id"] == "E1"]
    e2_sub = [r for r in comb_rows if r["rater_id"] == "E2"]
    assert len(e1_sub) == 283
    assert len(e2_sub) == 283


def test_section_b_policy_review_packet():
    """Verify Section B items are strictly isolated with scoring disabled."""
    sec_b_file = PACKET_DIR / "section_b_policy_review_packet.csv"
    with open(sec_b_file, "r", encoding="utf-8") as f:
        sec_b_rows = list(csv.DictReader(f))

    assert len(sec_b_rows) == 146, f"Expected 146 Section B rows, got {len(sec_b_rows)}"
    for row in sec_b_rows:
        assert "relevance_score" not in row, "Section B must never have numerical relevance score column"
        assert row["governance_status"] == "REQUIRES_VERIFICATION"
        assert len(row["governance_note"]) > 0
        sid_num = int(row["scenario_id"][1:])
        assert 11 <= sid_num <= 70


def test_calibration_pilot_partitioning():
    """Verify calibration pilot scenarios S001-S010 are strictly excluded from Phase 5 packets."""
    e1_file = PACKET_DIR / "E1_annotation_packet_blank.csv"
    sec_b_file = PACKET_DIR / "section_b_policy_review_packet.csv"

    with open(e1_file, "r", encoding="utf-8") as f:
        e1_sids = {r["scenario_id"] for r in csv.DictReader(f)}
    with open(sec_b_file, "r", encoding="utf-8") as f:
        sec_b_sids = {r["scenario_id"] for r in csv.DictReader(f)}

    for pilot_num in range(1, 11):
        pilot_id = f"S{pilot_num:03d}"
        assert pilot_id not in e1_sids, f"Pilot scenario {pilot_id} leaked into evaluation packet"
        assert pilot_id not in sec_b_sids, f"Pilot scenario {pilot_id} leaked into Section B packet"

    assert len(e1_sids) == 60, "All 60 scenarios S011-S070 must have Section A candidates"
