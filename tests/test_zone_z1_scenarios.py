"""
Targeted consistency and execution validation tests for Zone Z1 Profiles (S011-S016).
Validates schema compliance, assignment matrix consistency, physical capacity rules,
and reproducible execution through the frozen deterministic EligibilityEngine.
"""

import os
import json
import pytest
from src.eligibility.models import (
    FarmerScenario,
    EligibilityStatus,
    AvailabilityState,
    BorewellElectricStatus
)
from src.eligibility.engine import EligibilityEngine
from src.eligibility.availability import AvailabilityFilter
from research.dataset_research.validate_benchmark_matrix import scenarios

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Z1_DIR = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", "z1")
Z1_IDS = ["S011", "S012", "S013", "S014", "S015", "S016"]


@pytest.fixture(scope="module")
def z1_profiles():
    profiles = {}
    for sid in Z1_IDS:
        filepath = os.path.join(Z1_DIR, f"{sid}.json")
        assert os.path.exists(filepath), f"Profile file missing: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            profiles[sid] = json.load(f)
    return profiles


@pytest.fixture(scope="module")
def matrix_scenarios_by_id():
    return {s["sid"]: s for s in scenarios if s["sid"] in Z1_IDS}


def test_zone_z1_files_exist():
    """Verify all 6 JSON and Markdown profiles exist."""
    for sid in Z1_IDS:
        json_file = os.path.join(Z1_DIR, f"{sid}.json")
        md_file = os.path.join(Z1_DIR, f"{sid}.md")
        assert os.path.exists(json_file), f"Missing {json_file}"
        assert os.path.exists(md_file), f"Missing {md_file}"
        assert os.path.getsize(json_file) > 100
        assert os.path.getsize(md_file) > 100

    batch_json = os.path.join(Z1_DIR, "z1_scenarios.json")
    assert os.path.exists(batch_json)


def test_zone_z1_matrix_consistency(z1_profiles, matrix_scenarios_by_id):
    """Verify each profile exactly matches its row in the benchmark assignment matrix."""
    for sid in Z1_IDS:
        prof = z1_profiles[sid]
        mat = matrix_scenarios_by_id[sid]

        assert prof["scenario_id"] == mat["sid"]
        assert prof["district"] == mat["dist"]
        assert prof["crop_primary"] == mat["crop"]
        assert prof["immediate_need"] == mat["need"]
        assert prof["land_size_acres"] == mat["total_holding"]
        assert prof["landholding_details"]["qualifying_parcel_acres"] == mat["qual_parcel"]

        # Social category mapping (matrix uses "OBC", "GM", "SC", "ST")
        mat_soc = mat["social"]
        if mat_soc == "OBC":
            assert prof["social_category"] == "OBC (2A)"
        elif mat_soc == "GM":
            assert prof["social_category"] == "General (OC)"
        else:
            assert prof["social_category"] == mat_soc

        # Land type mapping
        if mat["land_type"] == "Dryland":
            assert prof["land_type"] == "Dryland (Rainfed)"
        elif mat["land_type"] == "Canal-irrigated":
            assert prof["land_type"] == "Irrigated (Canal)"

        # Farmer category mapping
        if mat["lclass"] == "Marginal":
            assert "Marginal" in prof["farmer_category"]
        elif mat["lclass"] == "Small":
            assert "Small" in prof["farmer_category"]


def test_zone_z1_physical_capacity(z1_profiles):
    """Verify physical capacity: requested subsidized area <= qualifying parcel in hectares."""
    for sid, prof in z1_profiles.items():
        req_ha = prof["landholding_details"]["requested_subsidized_area_ha"]
        parcel_ac = prof["landholding_details"]["qualifying_parcel_acres"]
        if req_ha is not None:
            max_ha = parcel_ac * 0.404686
            assert req_ha <= max_ha + 1e-4, f"{sid}: requested {req_ha} ha exceeds parcel {parcel_ac} ac ({max_ha} ha)"


def test_zone_z1_solar_prerequisites(z1_profiles):
    """Verify S012 has explicit unenergized borewell and off-grid electric status."""
    s012 = z1_profiles["S012"]
    assert "Borewell (Non-energized)" in s012["existing_assets"]
    assert s012["borewell_electric_status"] == "UNENERGIZED_OFF_GRID"

    # Other Z1 scenarios do not have borewells
    for sid in ["S011", "S013", "S014", "S015", "S016"]:
        assert z1_profiles[sid]["borewell_electric_status"] == "NONE"


def test_zone_z1_engine_execution_reproducibility(z1_profiles):
    """Execute through EligibilityEngine and AvailabilityFilter and verify rule determinations."""
    engine = EligibilityEngine()
    avail = AvailabilityFilter()

    engine_keys = {
        "scenario_id", "agro_climatic_zone", "district", "crop_primary",
        "land_size_acres", "land_type", "social_category", "farmer_category",
        "existing_assets", "annual_family_income_lakh", "immediate_need",
        "paid_income_tax_last_assessment_year", "govt_employee_category",
        "superannuated_pensioner_monthly_amount", "pensioner_is_mts_exempt",
        "registered_professional", "land_ownership_cutoff_pre_feb_2019",
        "is_pure_tenant_without_land_title", "borewell_electric_status",
        "prior_micro_irrigation_subsidy_years_ago", "prior_farm_pond_subsidy_years_ago",
        "prior_machinery_subsidy_years_ago", "prior_ganga_kalyana_in_family",
        "community_pool_acres", "community_pool_beneficiaries_count",
        "crop_secondary", "farming_stage", "season", "kcc_query_text_example"
    }

    for sid in Z1_IDS:
        prof = z1_profiles[sid]
        filtered = {k: prof[k] for k in engine_keys if k in prof}
        scenario = FarmerScenario.from_dict(filtered)

        raw = engine.evaluate_scenario(scenario, include_children=True)
        raw = avail.apply_availability(raw, as_of_date="2026-10-15")
        actionable = engine.resolve_actionable_determinations(raw)

        raw_map = {d.scheme_id: d for d in raw}
        act_map = {d.scheme_id: d for d in actionable}

        # PM-KISAN: All S011-S016 are clean positive
        assert raw_map["SCH001"].status == EligibilityStatus.ELIGIBLE
        assert "PMKISAN_LAND_SIZE_POSITIVE" in raw_map["SCH001"].rule_keys_fired

        # PMFBY: All crops notified
        assert raw_map["SCH002"].status == EligibilityStatus.ELIGIBLE
        assert "PMFBY_NOTIFIED_CROP_VERIFIED" in raw_map["SCH002"].rule_keys_fired

        # Parent deduplication: SCH008 parent must be suppressed since SCH008_CENTRAL is actionable
        assert "SCH008" not in act_map
        assert "SCH008_CENTRAL" in act_map
        assert act_map["SCH008_CENTRAL"].status == EligibilityStatus.ELIGIBLE

        # Scenario-specific tests:
        if sid == "S011":
            # OBC -> Devaraj Urs child eligible
            assert raw_map["SCH010_DEVARAJ_URS"].status == EligibilityStatus.ELIGIBLE
            assert raw_map["SCH010_AMBEDKAR"].status == EligibilityStatus.INELIGIBLE
            assert "SCH010" not in act_map  # Deduplicated

        elif sid == "S012":
            # Solar pump: PM-KUSUM B eligible
            assert raw_map["SCH006"].status == EligibilityStatus.ELIGIBLE
            assert "KUSUM_B_OFF_GRID_VERIFIED" in raw_map["SCH006"].rule_keys_fired
            # Ganga Kalyana: Ineligible due to existing borewell
            assert raw_map["SCH010"].status == EligibilityStatus.INELIGIBLE
            assert "GK_PARENT_EXISTING_BOREWELL_EXCLUSION" in raw_map["SCH010"].rule_keys_fired

        elif sid == "S013":
            # Sugarcane, Canal-irrigated, 5.0 acres, GM
            assert raw_map["SCH009"].status == EligibilityStatus.ELIGIBLE  # Soil Health Card
            assert raw_map["SCH005"].status == EligibilityStatus.INELIGIBLE  # Krishi Bhagya not dryland
            assert "KRISHI_BHAGYA_NOT_DRYLAND" in raw_map["SCH005"].rule_keys_fired
            assert raw_map["SCH010"].status == EligibilityStatus.INELIGIBLE  # GK General Merit
            assert "GK_PARENT_REGISTRY_CORPORATION_MISMATCH" in raw_map["SCH010"].rule_keys_fired

        elif sid == "S014":
            # ST -> Valmiki child eligible
            assert raw_map["SCH010_VALMIKI"].status == EligibilityStatus.ELIGIBLE
            # Karnataka Coop credit requires verification (provisional)
            assert raw_map["SCH008_KA_COOP"].status == EligibilityStatus.REQUIRES_VERIFICATION
            assert "KCC_KA_COOP_PROVISIONAL_PENDING_GO" in raw_map["SCH008_KA_COOP"].rule_keys_fired

        elif sid == "S015":
            # SC -> Ambedkar child eligible at 1.5 ac boundary
            assert raw_map["SCH010_AMBEDKAR"].status == EligibilityStatus.ELIGIBLE
            assert "GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID" in raw_map["SCH010_AMBEDKAR"].rule_keys_fired
            # PM-KISAN eligible for income support
            assert raw_map["SCH001"].status == EligibilityStatus.ELIGIBLE

        elif sid == "S016":
            # SC 4.5 ac -> Ambedkar child eligible
            assert raw_map["SCH010_AMBEDKAR"].status == EligibilityStatus.ELIGIBLE
            assert "GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID" in raw_map["SCH010_AMBEDKAR"].rule_keys_fired
            assert "SCH010" not in act_map  # Deduplicated
