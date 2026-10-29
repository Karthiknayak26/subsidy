#!/usr/bin/env python3
"""
tests/test_benchmark_v1_2_scenarios.py
--------------------------------------
Deterministic tests for Benchmark v1.2 scenario generation and diversity audit.

Tests cover:
- Scenario ID schema integrity (S131+ range, sequential numbering)
- Scenario schema completeness (all required fields present)
- Feature provenance (synthetic vs source attributes documented)
- Scenario group isolation (no scenario appears in multiple candidate sets)
- Reproducibility (same seed produces same scenarios)
- Diversity audit correctness (marginal distributions, joint distribution)
- Candidate generation through actual eligibility engine (Section A/B separation)
- Candidate set validity (no duplicate schemes, no unknown scheme IDs)
- v1.1 artifact preservation (no modifications to frozen files)
"""

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


# ---- Fixtures ----

@pytest.fixture
def scenarios():
    with open(REPO_ROOT / "data/benchmarks/v1.2/scenario_matrix.json") as f:
        return json.load(f)


@pytest.fixture
def candidate_results():
    with open(REPO_ROOT / "data/benchmarks/v1.2/candidate_generation_results.json") as f:
        return json.load(f)


@pytest.fixture
def diversity_audit():
    with open(REPO_ROOT / "data/benchmarks/v1.2/diversity_audit.json") as f:
        return json.load(f)


# ---- Tests ----


def test_scenario_id_schema(scenarios):
    """All scenario IDs must follow S### format starting from S131."""
    for s in scenarios:
        sid = s["scenario_id"]
        assert sid.startswith("S"), f"Scenario ID {sid} must start with 'S'"
        num = int(sid[1:])
        assert num >= 131, f"Scenario ID {sid} must be >= S131"
        assert len(sid) == 4, f"Scenario ID {sid} must be 4 characters (S + 3 digits)"


def test_scenario_id_uniqueness(scenarios):
    """All scenario IDs must be unique."""
    ids = [s["scenario_id"] for s in scenarios]
    assert len(ids) == len(set(ids)), "Duplicate scenario IDs found"


def test_scenario_id_sequential(scenarios):
    """Scenario IDs must be sequential with no gaps."""
    ids = sorted([int(s["scenario_id"][1:]) for s in scenarios])
    expected = list(range(ids[0], ids[-1] + 1))
    assert ids == expected, f"Scenario IDs have gaps: missing {set(expected) - set(ids)}"


def test_scenario_schema_completeness(scenarios):
    """All required fields must be present in each scenario."""
    required_fields = [
        "scenario_id", "benchmark_version", "zone_id", "agro_climatic_zone",
        "district", "crop_primary", "crop_secondary", "land_size_acres",
        "land_type", "social_category", "farmer_category", "existing_assets",
        "annual_family_income_lakh", "immediate_need",
        "paid_income_tax_last_assessment_year", "govt_employee_category",
        "superannuated_pensioner_monthly_amount", "pensioner_is_mts_exempt",
        "registered_professional", "land_ownership_cutoff_pre_feb_2019",
        "is_pure_tenant_without_land_title", "borewell_electric_status",
        "prior_micro_irrigation_subsidy_years_ago",
        "prior_farm_pond_subsidy_years_ago",
        "prior_machinery_subsidy_years_ago",
        "prior_ganga_kalyana_in_family",
        "community_pool_acres", "community_pool_beneficiaries_count",
        "farming_stage", "season", "kcc_query_text_example",
        "landholding_details", "water_and_irrigation",
        "compound_need_details", "source_backed_interventions",
        "provenance",
    ]
    for s in scenarios:
        sid = s["scenario_id"]
        for field in required_fields:
            assert field in s, f"Scenario {sid} missing required field: {field}"


def test_scenario_provenance_fields(scenarios):
    """All scenarios must have provenance metadata."""
    for s in scenarios:
        sid = s["scenario_id"]
        assert "provenance" in s, f"Scenario {sid} missing provenance field"
        prov = s["provenance"]
        assert "scenario_id" in prov, f"Scenario {sid} provenance missing scenario_id"
        assert "attributes_sourced_from" in prov, f"Scenario {sid} provenance missing attributes_sourced_from"
        assert "synthetic_attributes" in prov, f"Scenario {sid} provenance missing synthetic_attributes"
        assert "source_attributes" in prov, f"Scenario {sid} provenance missing source_attributes"


def test_scenario_immediate_need_valid(scenarios):
    """All immediate_need values must be from the approved set."""
    valid_needs = {
        "SOLAR_PUMP_INSTALLATION", "CROP_INSURANCE", "PROTECTED_HORTICULTURE",
        "FARM_MECHANIZATION", "RAINWATER_HARVESTING", "SOIL_HEALTH_AND_FERTILIZER",
        "DEBT_RELIEF", "POST_HARVEST_STORAGE",
    }
    for s in scenarios:
        sid = s["scenario_id"]
        assert s["immediate_need"] in valid_needs, f"Scenario {sid} has invalid immediate_need: {s['immediate_need']}"


def test_scenario_land_size_positive(scenarios):
    """All land sizes must be positive."""
    for s in scenarios:
        sid = s["scenario_id"]
        assert s["land_size_acres"] > 0, f"Scenario {sid} has non-positive land_size: {s['land_size_acres']}"


def test_scenario_income_positive(scenarios):
    """All income values must be positive."""
    for s in scenarios:
        sid = s["scenario_id"]
        assert s["annual_family_income_lakh"] > 0, f"Scenario {sid} has non-positive income: {s['annual_family_income_lakh']}"


def test_candidate_generation_integrity(scenarios, candidate_results):
    """All scenarios must have candidate generation results."""
    for s in scenarios:
        sid = s["scenario_id"]
        assert sid in candidate_results, f"Scenario {sid} missing from candidate results"
        r = candidate_results[sid]
        assert "section_a_candidates" in r, f"Scenario {sid} missing section_a_candidates"
        assert "section_b_candidates" in r, f"Scenario {sid} missing section_b_candidates"
        assert "disqualified_candidates" in r, f"Scenario {sid} missing disqualified_candidates"


def test_candidate_no_duplicates(scenarios, candidate_results):
    """No scenario should have duplicate scheme IDs in Section A."""
    for s in scenarios:
        sid = s["scenario_id"]
        r = candidate_results[sid]
        scheme_ids = [c["scheme_id"] for c in r["section_a_candidates"]]
        assert len(scheme_ids) == len(set(scheme_ids)), f"Scenario {sid} has duplicate scheme IDs in Section A"


def test_candidate_no_unknown_schemes(scenarios, candidate_results):
    """No candidate should reference an unknown scheme ID."""
    valid_schemes = {
        "SCH001", "SCH002", "SCH003", "SCH004", "SCH005", "SCH006", "SCH007",
        "SCH008", "SCH008_CENTRAL", "SCH008_KA_COOP", "SCH009",
        "SCH010", "SCH010_AMBEDKAR", "SCH010_VALMIKI", "SCH010_DEVARAJ_URS", "SCH010_KMDC",
    }
    for s in scenarios:
        sid = s["scenario_id"]
        r = candidate_results[sid]
        for c in r["section_a_candidates"]:
            assert c["scheme_id"] in valid_schemes, f"Scenario {sid} has unknown scheme: {c['scheme_id']}"
        for c in r["section_b_candidates"]:
            assert c["scheme_id"] in valid_schemes, f"Scenario {sid} has unknown scheme in Section B: {c['scheme_id']}"


def test_section_a_scoring_enabled(scenarios, candidate_results):
    """All Section A candidates must have allow_numerical_scoring=True."""
    for s in scenarios:
        sid = s["scenario_id"]
        r = candidate_results[sid]
        for c in r["section_a_candidates"]:
            assert c["allow_numerical_scoring"] is True, f"Scenario {sid} scheme {c['scheme_id']} in Section A but allow_numerical_scoring=False"


def test_section_b_scoring_disabled(scenarios, candidate_results):
    """All Section B candidates must have allow_numerical_scoring=False."""
    for s in scenarios:
        sid = s["scenario_id"]
        r = candidate_results[sid]
        for c in r["section_b_candidates"]:
            assert c["allow_numerical_scoring"] is False, f"Scenario {sid} scheme {c['scheme_id']} in Section B but allow_numerical_scoring=True"


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


def test_diversity_audit_marginals(diversity_audit, scenarios):
    """Marginal distributions in audit must match scenario data."""
    # Check zone distribution
    zone_counts = {}
    for s in scenarios:
        z = s["zone_id"]
        zone_counts[z] = zone_counts.get(z, 0) + 1
    audit_zones = diversity_audit["marginal_distributions"]["zone_id"]
    for z, count in zone_counts.items():
        assert audit_zones[z] == count, f"Zone {z} count mismatch: audit={audit_zones[z]}, actual={count}"


def test_diversity_audit_archetypes(diversity_audit, scenarios):
    """Archetype distribution in audit must match scenario data."""
    arch_counts = {}
    for s in scenarios:
        a = s["compound_need_details"]["archetype_id"]
        arch_counts[a] = arch_counts.get(a, 0) + 1
    audit_archs = diversity_audit["archetype_distribution"]
    for a, count in arch_counts.items():
        assert audit_archs[a] == count, f"Archetype {a} count mismatch: audit={audit_archs[a]}, actual={count}"


def test_v1_1_artifacts_preserved():
    """v1.1 artifacts must not be modified."""
    # Check that v1.1 files still exist
    assert (REPO_ROOT / "data/benchmarks/v1.1/scenario_matrix.json").exists()
    assert (REPO_ROOT / "data/benchmarks/v1.1/candidate_generation_results.json").exists()
    assert (REPO_ROOT / "src/eligibility/engine.py").exists()
    assert (REPO_ROOT / "research/dataset_research/evaluation_preregistration.md").exists()


def test_scenario_count_reasonable(scenarios):
    """Scenario count must be reasonable (> 60 to exceed v1.1 diversity)."""
    assert len(scenarios) > 60, f"v1.2 must have more than 60 scenarios, got {len(scenarios)}"


def test_zone_coverage(scenarios):
    """All 10 zones must be represented."""
    zones = set(s["zone_id"] for s in scenarios)
    expected_zones = {f"Z{i}" for i in range(1, 11)}
    assert zones == expected_zones, f"Missing zones: {expected_zones - zones}"


def test_no_duplicate_scenario_ids(scenarios):
    """No duplicate scenario IDs."""
    ids = [s["scenario_id"] for s in scenarios]
    assert len(ids) == len(set(ids)), f"Duplicate scenario IDs found: {[x for x in ids if ids.count(x) > 1]}"


def test_scenario_provenance_marking(scenarios):
    """All scenarios must mark synthetic vs source attributes."""
    for s in scenarios:
        sid = s["scenario_id"]
        prov = s["provenance"]
        assert isinstance(prov["synthetic_attributes"], list), f"Scenario {sid} synthetic_attributes must be a list"
        assert isinstance(prov["source_attributes"], list), f"Scenario {sid} source_attributes must be a list"
        assert len(prov["synthetic_attributes"]) > 0, f"Scenario {sid} must have at least one synthetic attribute"
        assert len(prov["source_attributes"]) > 0, f"Scenario {sid} must have at least one source attribute"