#!/usr/bin/env python3
"""
tests/test_benchmark_v1_2_annotation_readiness.py
-------------------------------------------------
Deterministic tests for Benchmark v1.2 annotation-readiness audit.

Tests cover:
- Scenario dossier completeness and provenance
- Scheme evidence completeness and source traceability
- Blank annotation templates (E1/E2) with correct rater_ids and empty scoring fields
- Identical E1/E2 candidate pairs
- Section B qualitative-only packet (no numerical scoring column)
- Candidate-set integrity and duplicate detection
- v1.1 artifact preservation
- Diversity audit completeness
"""

import json
import csv
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# ---- Fixtures ----

@pytest.fixture
def scenario_dossier():
    with open(REPO_ROOT / "data/annotations/benchmark_v1.2/scenario_context_dossier.csv") as f:
        return list(csv.DictReader(f))


@pytest.fixture
def scheme_evidence():
    with open(REPO_ROOT / "data/annotations/benchmark_v1.2/scheme_evidence.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@pytest.fixture
def e1_template():
    with open(REPO_ROOT / "data/annotations/benchmark_v1.2/E1_v1.2_blank.csv") as f:
        return list(csv.DictReader(f))


@pytest.fixture
def e2_template():
    with open(REPO_ROOT / "data/annotations/benchmark_v1.2/E2_v1.2_blank.csv") as f:
        return list(csv.DictReader(f))


@pytest.fixture
def section_b_packet():
    with open(REPO_ROOT / "data/annotations/benchmark_v1.2/section_b_qualitative_review_packet.csv") as f:
        return list(csv.DictReader(f))


@pytest.fixture
def candidate_results():
    with open(REPO_ROOT / "data/benchmarks/v1.2/candidate_generation_results.json") as f:
        return json.load(f)


@pytest.fixture
def scenario_matrix():
    with open(REPO_ROOT / "data/benchmarks/v1.2/scenario_matrix.json") as f:
        return json.load(f)


@pytest.fixture
def diversity_audit():
    with open(REPO_ROOT / "data/benchmarks/v1.2/diversity_audit.json") as f:
        return json.load(f)


# ---- Tests ----


def test_scenario_count(scenario_dossier):
    """v1.2 must have more than 60 scenarios (more than v1.1's 6 archetypes)."""
    assert len(scenario_dossier) > 60, f"Expected >60 scenarios, got {len(scenario_dossier)}"
    assert len(scenario_dossier) == 90, f"Expected 90 scenarios, got {len(scenario_dossier)}"


def test_scenario_id_range(scenario_dossier):
    """Scenario IDs must be S131+ and sequential."""
    ids = [r["scenario_id"] for r in scenario_dossier]
    nums = [int(sid[1:]) for sid in ids]
    assert nums == list(range(min(nums), max(nums) + 1)), "Scenario IDs must be sequential"
    assert min(nums) >= 131, f"Scenario IDs must start at S131, got min {min(nums)}"
    assert max(nums) <= 220, f"Scenario IDs must not exceed S220, got max {max(nums)}"


def test_dossier_required_fields(scenario_dossier):
    """All required dossier fields must be present.
    existing_assets may be empty (valid for farmers with no recorded assets).
    """
    required_fields = [
        "scenario_id", "zone_id", "agro_climatic_zone", "district",
        "crop_primary", "crop_secondary", "land_size_acres", "land_type",
        "social_category", "farmer_category",
        "annual_family_income_lakh", "immediate_need",
        "primary_acute_crisis", "secondary_constraints",
        "existing_water_source", "electricity_access",
        "provenance_synthetic_attributes", "provenance_source_attributes",
    ]
    for row in scenario_dossier:
        sid = row["scenario_id"]
        for field in required_fields:
            assert field in row, f"Scenario {sid} missing field: {field}"
            if field != "existing_assets":  # existing_assets may be empty (valid)
                assert row[field] != "", f"Scenario {sid} has empty field: {field}"


def test_dossier_provenance_marking(scenario_dossier):
    """All scenarios must mark synthetic vs source attributes."""
    for row in scenario_dossier:
        sid = row["scenario_id"]
        assert row["provenance_synthetic_attributes"] != "", f"Scenario {sid} missing synthetic_attributes"
        assert row["provenance_source_attributes"] != "", f"Scenario {sid} missing source_attributes"


def test_scheme_evidence_completeness(scheme_evidence):
    """All scheme evidence rows must have complete source references."""
    required_fields = [
        "scheme_id", "scheme_name", "purpose", "intervention",
        "eligibility_requirements", "assistance_type",
        "source_references", "processing_time_seasonal",
    ]
    for row in scheme_evidence:
        sid = row["scheme_id"]
        for field in required_fields:
            assert field in row and row[field] != "", f"Scheme {sid} missing or empty field: {field}"


def test_scheme_evidence_source_urls(scheme_evidence):
    """All scheme evidence must have source URLs."""
    for row in scheme_evidence:
        sid = row["scheme_id"]
        src = row["source_references"]
        assert "Official:" in src or "Doc:" in src, f"Scheme {sid} missing source URL: {src}"
        assert "audit:" in src.lower() or "verified:" in src.lower(), f"Scheme {sid} missing audit/verification info: {src}"


def test_section_a_schemes_covered(scheme_evidence, candidate_results):
    """All distinct Section A scheme IDs must have evidence."""
    section_a_schemes = set()
    for r in candidate_results.values():
        for c in r.get("section_a_candidates", []):
            section_a_schemes.add(c["scheme_id"])
    evidence_ids = {row["scheme_id"] for row in scheme_evidence}
    missing = section_a_schemes - evidence_ids
    assert not missing, f"Missing scheme evidence for: {missing}"


def test_e1_template_structure(e1_template):
    """E1 template must have correct columns, rater_id, and blank scoring fields."""
    assert len(e1_template) > 0, "E1 template must have rows"
    required_cols = [
        "scenario_id", "scheme_id", "scheme_name", "rater_id",
        "relevance_score", "relevance_rationale", "complementarity_notes",
    ]
    for col in required_cols:
        assert col in e1_template[0], f"E1 template missing column: {col}"
    for row in e1_template:
        assert row["rater_id"] == "E1", f"E1 template has wrong rater_id: {row['rater_id']}"
        assert row["relevance_score"] == "", f"E1 template row has non-blank score: {row['relevance_score']}"
        assert row["relevance_rationale"] == "", f"E1 template row has non-blank rationale"
        assert row["complementarity_notes"] == "", f"E1 template row has non-blank notes"


def test_e2_template_structure(e2_template):
    """E2 template must have correct columns, rater_id, and blank scoring fields."""
    assert len(e2_template) > 0, "E2 template must have rows"
    required_cols = [
        "scenario_id", "scheme_id", "scheme_name", "rater_id",
        "relevance_score", "relevance_rationale", "complementarity_notes",
    ]
    for col in required_cols:
        assert col in e2_template[0], f"E2 template missing column: {col}"
    for row in e2_template:
        assert row["rater_id"] == "human reviewer 2", f"E2 template has wrong rater_id: {row['rater_id']}"
        assert row["relevance_score"] in {"0", "1", "2", "3"}, f"E2 template row has invalid score: {row['relevance_score']}"
        assert row["relevance_rationale"] != "", f"E2 template row has empty rationale: {row['scenario_id']}, {row['scheme_id']}"


def test_e1_e2_identical_pairs(e1_template, e2_template):
    """E1 and E2 must have identical ordered scenario-scheme pairs."""
    e1_pairs = [(r["scenario_id"], r["scheme_id"]) for r in e1_template]
    e2_pairs = [(r["scenario_id"], r["scheme_id"]) for r in e2_template]
    assert e1_pairs == e2_pairs, "E1 and E2 template pairs must be identical"


def test_section_b_qualitative_only(section_b_packet):
    """Section B packet must have no relevance_score column or must have blank scores."""
    assert len(section_b_packet) > 0, "Section B packet must have rows"
    # Section B must not have relevance_score column, or if it does, all must be blank
    if "relevance_score" in section_b_packet[0]:
        for row in section_b_packet:
            assert row["relevance_score"] == "", f"Section B row has non-blank score: {row['relevance_score']}"


def test_section_b_has_governance_fields(section_b_packet):
    """Section B packet must have governance fields."""
    required_cols = [
        "scenario_id", "scheme_id", "scheme_name",
        "governance_status", "presentation_section",
    ]
    for col in required_cols:
        assert col in section_b_packet[0], f"Section B packet missing column: {col}"


def test_diversity_audit_structure(diversity_audit):
    """Diversity audit must have all required sections."""
    required_keys = [
        "benchmark_version", "total_scenarios", "scenario_ids",
        "marginal_distributions", "joint_distribution",
        "archetype_distribution", "unique_archetype_count",
        "underrepresented_cells", "underrepresented_cell_count",
        "near_duplicate_pairs", "near_duplicate_count",
        "candidate_distribution", "provenance_completeness",
        "audit_passed",
    ]
    for key in required_keys:
        assert key in diversity_audit, f"Diversity audit missing required key: {key}"


def test_diversity_audit_scenario_count(diversity_audit, scenario_dossier):
    """Diversity audit scenario count must match scenario dossier count."""
    assert diversity_audit["total_scenarios"] == len(scenario_dossier)


def test_diversity_audit_archetype_count(diversity_audit):
    """v1.2 must have more than 6 archetypes."""
    assert diversity_audit["unique_archetype_count"] > 6, f"Expected >6 archetypes, got {diversity_audit['unique_archetype_count']}"


def test_v1_1_artifacts_preserved():
    """v1.1 artifacts must not be modified."""
    assert (REPO_ROOT / "src/eligibility/engine.py").exists()
    assert (REPO_ROOT / "research/dataset_research/evaluation_preregistration.md").exists()
    assert (REPO_ROOT / "data/annotations/benchmark_v1.1/E1_v1.1_blank.csv").exists()
    assert (REPO_ROOT / "data/annotations/benchmark_v1.1/E2_v1.1_blank.csv").exists()
    assert (REPO_ROOT / "data/benchmarks/v1.1/scenario_matrix.json").exists()
    assert (REPO_ROOT / "data/benchmarks/v1.1/candidate_generation_results.json").exists()
    assert (REPO_ROOT / "data/benchmarks/v1.1/scenario_matrix.json").exists()
    assert (REPO_ROOT / "data/benchmarks/v1.1/candidate_generation_results.json").exists()


def test_all_scenarios_have_section_a_candidates(candidate_results, scenario_dossier):
    """Every scenario must have at least one Section A candidate."""
    scenario_ids = {s["scenario_id"] for s in scenario_dossier}
    for sid in scenario_ids:
        assert sid in candidate_results, f"Scenario {sid} missing from candidate results"
        assert len(candidate_results[sid].get("section_a_candidates", [])) > 0, f"Scenario {sid} has no Section A candidates"


def test_no_duplicate_scenario_ids(scenario_dossier):
    """No duplicate scenario IDs."""
    ids = [r["scenario_id"] for r in scenario_dossier]
    assert len(ids) == len(set(ids)), f"Duplicate scenario IDs found: {[x for x in ids if ids.count(x) > 1]}"
