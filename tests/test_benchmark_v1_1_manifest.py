"""
test_benchmark_v1_1_manifest.py
--------------------------------
Comprehensive test suite validating Benchmark v1.1 Scenario Manifest,
engine-backed candidate generation results, preflight audit, and research isolation.
"""

import json
import os
import sys
from pathlib import Path
import pytest
from dataclasses import fields

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.eligibility.models import FarmerScenario, EligibilityStatus
from src.eligibility.engine import EligibilityEngine
from src.eligibility.governance import apply_governance_safeguard
from research.dataset_research.validate_benchmark_v1_1_manifest import (
    run_preflight_audit,
    CANONICAL_ZONES,
    EXPECTED_SIDS,
    REQUIRED_SCENARIO_KEYS,
    REQUIRED_COMPOUND_KEYS,
    HISTORICAL_FORBIDDEN_SIDS,
)

V1_1_DIR = REPO_ROOT / "data" / "benchmarks" / "v1.1"
SCENARIO_MATRIX_PATH = V1_1_DIR / "scenario_matrix.json"
CANDIDATE_RESULTS_PATH = V1_1_DIR / "candidate_generation_results.json"
MANIFEST_MD_PATH = REPO_ROOT / "research" / "dataset_research" / "benchmark_v1.1_scenario_manifest.md"
PREFLIGHT_REPORT_PATH = REPO_ROOT / "reports" / "benchmark_v1.1_preflight_audit.md"


@pytest.fixture(scope="module")
def scenario_matrix():
    assert SCENARIO_MATRIX_PATH.exists(), f"Scenario matrix missing at {SCENARIO_MATRIX_PATH}"
    with open(SCENARIO_MATRIX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def candidate_results():
    assert CANDIDATE_RESULTS_PATH.exists(), f"Candidate generation results missing at {CANDIDATE_RESULTS_PATH}"
    with open(CANDIDATE_RESULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_scenario_cardinality_and_ordered_ids(scenario_matrix):
    """Verify exactly 60 scenarios with ordered IDs S071 through S130."""
    assert len(scenario_matrix) == 60
    sids = [s["scenario_id"] for s in scenario_matrix]
    assert sids == EXPECTED_SIDS
    assert len(sids) == len(set(sids)), "Duplicate scenario IDs detected"


def test_zone_distribution_and_canonical_names(scenario_matrix):
    """Verify exactly 6 scenarios in each of the 10 zones with valid canonical names."""
    from collections import Counter
    zone_counts = Counter(s["zone_id"] for s in scenario_matrix)
    
    assert set(zone_counts.keys()) == set(CANONICAL_ZONES.keys())
    for z_code, count in zone_counts.items():
        assert count == 6, f"Zone {z_code} has {count} scenarios, expected 6"

    for s in scenario_matrix:
        z_code = s["zone_id"]
        assert s["agro_climatic_zone"] == CANONICAL_ZONES[z_code]


def test_rejection_of_historical_scenario_ids(scenario_matrix):
    """Ensure no historical IDs (S001–S070) overlap with v1.1 matrix."""
    v1_1_ids = {s["scenario_id"] for s in scenario_matrix}
    overlap = v1_1_ids.intersection(HISTORICAL_FORBIDDEN_SIDS)
    assert not overlap, f"Forbidden historical IDs present in v1.1 matrix: {overlap}"


def test_compound_need_metadata_completeness(scenario_matrix):
    """Verify all required scenario keys and compound-need details are populated."""
    for s in scenario_matrix:
        sid = s["scenario_id"]
        for k in REQUIRED_SCENARIO_KEYS:
            assert k in s, f"{sid}: Missing required scenario key '{k}'"

        c_details = s["compound_need_details"]
        for ck in REQUIRED_COMPOUND_KEYS:
            assert ck in c_details, f"{sid}: Missing compound_need_details key '{ck}'"
            val = c_details[ck]
            if isinstance(val, (str, list)):
                assert len(val) > 0, f"{sid}: compound_need_details key '{ck}' is empty"


def test_valid_engine_input_instantiation(scenario_matrix):
    """Verify all 60 scenarios cleanly instantiate the FarmerScenario engine model."""
    valid_fields = {f.name for f in fields(FarmerScenario)}
    for s in scenario_matrix:
        sid = s["scenario_id"]
        engine_dict = {k: v for k, v in s.items() if k in valid_fields}
        try:
            f_sc = FarmerScenario.from_dict(engine_dict)
            assert f_sc.scenario_id == sid
            assert f_sc.land_size_acres > 0
            assert f_sc.immediate_need in [
                "SOLAR_PUMP_INSTALLATION",
                "CROP_INSURANCE",
                "PROTECTED_HORTICULTURE",
                "FARM_MECHANIZATION",
                "RAINWATER_HARVESTING",
                "SOIL_HEALTH_AND_FERTILIZER"
            ]
        except Exception as e:
            pytest.fail(f"Failed to instantiate FarmerScenario for {sid}: {e}")


def test_candidate_provenance_and_engine_determinism(scenario_matrix, candidate_results):
    """Verify candidate generation results exactly match fresh frozen EligibilityEngine run."""
    engine = EligibilityEngine()
    valid_fields = {f.name for f in fields(FarmerScenario)}

    for s in scenario_matrix:
        sid = s["scenario_id"]
        assert sid in candidate_results, f"Scenario {sid} missing from candidate generation results"
        
        stored_res = candidate_results[sid]
        stored_sec_a_ids = [c["scheme_id"] for c in stored_res["section_a_candidates"]]
        
        # Fresh engine run
        engine_dict = {k: v for k, v in s.items() if k in valid_fields}
        f_sc = FarmerScenario.from_dict(engine_dict)
        raw_dets = engine.evaluate_scenario(f_sc)
        actionable_dets = engine.resolve_actionable_determinations(raw_dets)
        
        fresh_sec_a_ids = []
        for d in actionable_dets:
            is_prov = d.scheme_id in ["SCH008_KA_COOP", "SCH010_VALMIKI", "SCH010_DEVARAJ_URS", "SCH010_KMDC"]
            gov = apply_governance_safeguard(d, sid, s, is_prov=is_prov)
            if gov["allow_numerical_scoring"] and gov["presentation_section"].startswith("Section A"):
                fresh_sec_a_ids.append(d.scheme_id)
        
        assert set(stored_sec_a_ids) == set(fresh_sec_a_ids), (
            f"Provenance mismatch in {sid}: stored {stored_sec_a_ids} vs fresh {fresh_sec_a_ids}"
        )


def test_parent_deduplication(candidate_results):
    """Ensure abstract parents SCH008 and SCH010 never appear in Section A."""
    for sid, res in candidate_results.items():
        sec_a_ids = [c["scheme_id"] for c in res["section_a_candidates"]]
        assert "SCH008" not in sec_a_ids, f"{sid}: Generic parent SCH008 in Section A"
        assert "SCH010" not in sec_a_ids, f"{sid}: Generic parent SCH010 in Section A"


def test_section_a_and_b_scoring_isolation(candidate_results):
    """Ensure Section A has scoring enabled, while Section B and disqualified schemes have scoring disabled."""
    for sid, res in candidate_results.items():
        # Section A
        for c in res["section_a_candidates"]:
            assert c["allow_numerical_scoring"] is True, f"{sid}: Section A {c['scheme_id']} scoring is False"
            assert c["governance_status"] == "ELIGIBLE", f"{sid}: Section A {c['scheme_id']} status != ELIGIBLE"

        # Section B
        for c in res["section_b_candidates"]:
            assert c["allow_numerical_scoring"] is False, f"{sid}: Section B {c['scheme_id']} scoring is True"
            assert c["governance_status"] in ["REQUIRES_VERIFICATION", "INELIGIBLE"]

        # Disqualified
        for c in res["disqualified_candidates"]:
            assert c["allow_numerical_scoring"] is False, f"{sid}: Disqualified {c['scheme_id']} scoring is True"
            assert c["governance_status"] == "INELIGIBLE"


def test_statistical_and_label_isolation(scenario_matrix, candidate_results):
    """Confirm zero prepopulated scores, rationales, consensus labels, or rankings."""
    forbidden_keys = {
        "relevance_score", "consensus_score", "annotation", "rationale",
        "expert_rating", "predicted_rank", "heuristic_score"
    }
    for s in scenario_matrix:
        for fk in forbidden_keys:
            assert fk not in s, f"{s['scenario_id']}: Contained forbidden label key '{fk}'"

    for sid, res in candidate_results.items():
        for group in ["section_a_candidates", "section_b_candidates", "disqualified_candidates"]:
            for item in res[group]:
                for fk in forbidden_keys:
                    assert fk not in item, f"{sid} {item.get('scheme_id')}: Contained forbidden label key '{fk}'"


def test_missing_scheme_master_fail_closed(monkeypatch, tmp_path):
    """Verify validator fails closed with BLOCKED status when scheme master is missing."""
    import research.dataset_research.validate_benchmark_v1_1_manifest as vmod
    fake_root = tmp_path / "fake_repo"
    fake_root.mkdir()
    monkeypatch.setattr(vmod, "REPO_ROOT", fake_root)
    
    status, summary, errors, warnings = vmod.run_preflight_audit()
    assert status == "BLOCKED"
    assert any("Scheme master not found" in e for e in errors)


def test_preflight_audit_execution_and_pass_status():
    """Execute preflight audit and assert PASS status with zero errors."""
    status, summary, errors, warnings = run_preflight_audit()
    assert status == "PASS", f"Preflight audit failed with errors: {errors}"
    assert len(errors) == 0
    assert summary["total_scenarios"] == 60
    assert summary["section_a_min"] >= 2
    assert summary["section_a_max"] <= 10
    assert summary["section_a_mean"] > 3.0


def test_safe_versioned_output_paths():
    """Verify all v1.1 output paths are isolated under v1.1 directories and preserve v1.0.4."""
    assert SCENARIO_MATRIX_PATH.parent.name == "v1.1"
    assert CANDIDATE_RESULTS_PATH.parent.name == "v1.1"
    
    # Historical v1.0.4 files must remain intact
    v1_0_4_dir = REPO_ROOT / "data" / "annotations" / "benchmark_v1.0.4"
    assert v1_0_4_dir.exists(), "Historical v1.0.4 annotations directory was modified or removed"
    assert (v1_0_4_dir / "consensus_labels_final.csv").exists(), "Historical consensus_labels_final.csv missing"


def test_authorized_blank_annotation_packets(candidate_results):
    """Verify authorized blank annotation packets E1_v1.1_blank.csv and E2_v1.1_blank.csv."""
    import csv
    v1_1_ann_dir = REPO_ROOT / "data" / "annotations" / "benchmark_v1.1"
    e1_file = v1_1_ann_dir / "E1_v1.1_blank.csv"
    e2_file = v1_1_ann_dir / "E2_v1.1_blank.csv"
    sec_b_file = v1_1_ann_dir / "section_b_qualitative_review_packet.csv"

    assert e1_file.exists(), f"E1 blank packet missing at {e1_file}"
    assert e2_file.exists(), f"E2 blank packet missing at {e2_file}"
    assert sec_b_file.exists(), f"Section B packet missing at {sec_b_file}"

    with open(e1_file, "r", encoding="utf-8") as f:
        e1_rows = list(csv.DictReader(f))
    with open(e2_file, "r", encoding="utf-8") as f:
        e2_rows = list(csv.DictReader(f))

    assert len(e1_rows) == 269, f"Expected 269 candidate rows, got {len(e1_rows)}"
    assert len(e2_rows) == 269, f"Expected 269 candidate rows, got {len(e2_rows)}"

    for r1, r2 in zip(e1_rows, e2_rows):
        assert r1["scenario_id"] == r2["scenario_id"]
        assert r1["scheme_id"] == r2["scheme_id"]
        assert r1["scheme_name"] == r2["scheme_name"]
        assert r1["rater_id"] == "E1"
        assert r2["rater_id"] == "E2"
        # Must be strictly blank (zero scores / leakage)
        assert r1["relevance_score"] == ""
        assert r2["relevance_score"] == ""
        assert r1["relevance_rationale"] == ""
        assert r2["relevance_rationale"] == ""
        assert r1["complementarity_notes"] == ""
        assert r2["complementarity_notes"] == ""
