"""
Targeted consistency and execution validation tests for Zone Z2 Profiles (S017-S022).
Validates schema compliance, assignment matrix consistency, Challenge 3 boundary condition,
Challenge 4 three-valued logic, and reproducible execution through the frozen deterministic EligibilityEngine.
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
Z2_DIR = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", "z2")
Z2_IDS = ["S017", "S018", "S019", "S020", "S021", "S022"]


@pytest.fixture(scope="module")
def z2_profiles():
    profiles = {}
    for sid in Z2_IDS:
        filepath = os.path.join(Z2_DIR, f"{sid}.json")
        assert os.path.exists(filepath), f"Profile file missing: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            profiles[sid] = json.load(f)
    return profiles


@pytest.fixture(scope="module")
def matrix_scenarios_by_id():
    return {s["sid"]: s for s in scenarios if s["sid"] in Z2_IDS}


def test_zone_z2_files_exist():
    """Verify all 6 JSON and Markdown profiles exist, along with batch and execution JSONs."""
    for sid in Z2_IDS:
        json_file = os.path.join(Z2_DIR, f"{sid}.json")
        md_file = os.path.join(Z2_DIR, f"{sid}.md")
        assert os.path.exists(json_file), f"Missing {json_file}"
        assert os.path.exists(md_file), f"Missing {md_file}"
        assert os.path.getsize(json_file) > 100
        assert os.path.getsize(md_file) > 100

    batch_json = os.path.join(Z2_DIR, "z2_scenarios.json")
    assert os.path.exists(batch_json)
    
    exec_json = os.path.join(Z2_DIR, "z2_execution_results.json")
    assert os.path.exists(exec_json)


def test_zone_z2_matrix_consistency(z2_profiles, matrix_scenarios_by_id):
    """Verify each profile exactly matches its row in the benchmark assignment matrix."""
    for sid in Z2_IDS:
        prof = z2_profiles[sid]
        mat = matrix_scenarios_by_id[sid]

        assert prof["scenario_id"] == mat["sid"]
        assert prof["zone_id"] == mat["zone"]
        assert prof["district"] == mat["dist"]
        assert prof["crop_primary"] == mat["crop"]
        assert prof["immediate_need"] == mat["need"]
        assert prof["land_size_acres"] == mat["total_holding"]
        assert prof["landholding_details"]["qualifying_parcel_acres"] == mat["qual_parcel"]

        # Social category mapping
        mat_soc = mat["social"]
        if mat_soc == "OBC":
            assert prof["social_category"] == "OBC (2A)"
        elif mat_soc == "GM":
            assert prof["social_category"] == "General (OC)"
        elif mat_soc == "Minority":
            assert prof["social_category"] == "Minority (Muslim)"
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
        elif mat["lclass"] == "Medium":
            assert "Medium" in prof["farmer_category"]


def test_zone_z2_challenge3_s018_pension_boundary(z2_profiles):
    """
    Verify Challenge 3: PM-KISAN pension exclusion at exactly Rs. 10,000/month.
    The threshold is inclusive (>= Rs. 10,000) and must trigger INELIGIBLE
    with rule key PMKISAN_PENSION_OVER_10K_EXCLUSION.
    """
    s018 = z2_profiles["S018"]
    assert s018["superannuated_pensioner_monthly_amount"] == 10000.0
    assert s018["pensioner_is_mts_exempt"] is False
    assert s018["statutory_flags"]["superannuated_pensioner_monthly_amount"] == 10000.0
    assert s018["statutory_flags"]["pensioner_is_mts_exempt"] is False

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s018["scenario_id"],
        "agro_climatic_zone": s018["agro_climatic_zone"],
        "district": s018["district"],
        "crop_primary": s018["crop_primary"],
        "land_size_acres": s018["land_size_acres"],
        "land_type": s018["land_type"],
        "social_category": s018["social_category"],
        "farmer_category": s018["farmer_category"],
        "existing_assets": s018["existing_assets"],
        "annual_family_income_lakh": s018["annual_family_income_lakh"],
        "immediate_need": s018["immediate_need"],
        "superannuated_pensioner_monthly_amount": s018["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s018["pensioner_is_mts_exempt"],
        "paid_income_tax_last_assessment_year": s018["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s018["govt_employee_category"],
        "registered_professional": s018["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s018["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s018["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s018["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)
    det = engine.evaluate_scheme(sc, "SCH001")
    assert det.status == EligibilityStatus.INELIGIBLE
    assert "PMKISAN_PENSION_OVER_10K_EXCLUSION" in det.rule_keys_fired
    assert any("Rs. 10,000" in d for d in det.disqualifying_factors)


def test_zone_z2_challenge4_s020_three_valued_logic(z2_profiles):
    """
    Verify Challenge 4: Three-Valued Logic under UNKNOWN attributes.
    Borewell electric status is UNKNOWN -> PM-KUSUM B returns REQUIRES_VERIFICATION.
    Income tax assessment is UNKNOWN -> PM-KISAN returns REQUIRES_VERIFICATION.
    """
    s020 = z2_profiles["S020"]
    assert s020["borewell_electric_status"] == "UNKNOWN"
    assert s020["paid_income_tax_last_assessment_year"] is None
    assert "Borewell (Non-energized)" in s020["existing_assets"]

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s020["scenario_id"],
        "agro_climatic_zone": s020["agro_climatic_zone"],
        "district": s020["district"],
        "crop_primary": s020["crop_primary"],
        "land_size_acres": s020["land_size_acres"],
        "land_type": s020["land_type"],
        "social_category": s020["social_category"],
        "farmer_category": s020["farmer_category"],
        "existing_assets": s020["existing_assets"],
        "annual_family_income_lakh": s020["annual_family_income_lakh"],
        "immediate_need": s020["immediate_need"],
        "superannuated_pensioner_monthly_amount": s020["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s020["pensioner_is_mts_exempt"],
        "paid_income_tax_last_assessment_year": s020["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s020["govt_employee_category"],
        "registered_professional": s020["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s020["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s020["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s020["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # 1. PM-KUSUM Component B: REQUIRES_VERIFICATION due to unknown electric status
    det_kusum = engine.evaluate_scheme(sc, "SCH006")
    assert det_kusum.status == EligibilityStatus.REQUIRES_VERIFICATION
    assert "KUSUM_B_GRID_STATUS_UNKNOWN" in det_kusum.rule_keys_fired
    assert "KUSUM_B_WATER_SOURCE_PRESENT" in det_kusum.rule_keys_fired

    # 2. PM-KISAN: REQUIRES_VERIFICATION due to unknown income tax
    det_kisan = engine.evaluate_scheme(sc, "SCH001")
    assert det_kisan.status == EligibilityStatus.REQUIRES_VERIFICATION
    assert "PMKISAN_INCOME_TAX_UNKNOWN" in det_kisan.rule_keys_fired

    # 3. Ganga Kalyana: INELIGIBLE due to existing borewell and 6.5 ac > 5.0 ac ceiling
    det_gk = engine.evaluate_scheme(sc, "SCH010")
    assert det_gk.status == EligibilityStatus.INELIGIBLE
    assert "GK_PARENT_EXISTING_BOREWELL_EXCLUSION" in det_gk.rule_keys_fired
    assert "GK_PARENT_EXCEEDS_5_ACRES" in det_gk.rule_keys_fired


def test_zone_z2_engine_execution_reproducibility(z2_profiles):
    """Execute all Zone Z2 profiles through EligibilityEngine and verify reproducible behaviour."""
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

    for sid in Z2_IDS:
        prof = z2_profiles[sid]
        filtered = {k: prof[k] for k in engine_keys if k in prof}
        scenario = FarmerScenario.from_dict(filtered)

        raw = engine.evaluate_scenario(scenario, include_children=True)
        raw = avail.apply_availability(raw, as_of_date="2026-10-15")
        actionable = engine.resolve_actionable_determinations(raw)

        raw_map = {d.scheme_id: d for d in raw}
        act_map = {d.scheme_id: d for d in actionable}

        # Parent deduplication check:
        # SCH008 must always be suppressed in actionable determinations because SCH008_CENTRAL is actionable
        assert "SCH008" not in act_map
        assert "SCH008_CENTRAL" in act_map

        # S019 routes to D. Devaraj Urs Corporation under Ganga Kalyana, so SCH010 parent is suppressed
        if sid == "S019":
            assert "SCH010" not in act_map
            assert "SCH010_DEVARAJ_URS" in act_map
            assert act_map["SCH010_DEVARAJ_URS"].status == EligibilityStatus.ELIGIBLE
            assert "GK_SCH010_DEVARAJ_URS_INDIVIDUAL_ROUTE_VALID" in act_map["SCH010_DEVARAJ_URS"].rule_keys_fired

        # S021 is canal-irrigated: Krishi Bhagya must be INELIGIBLE
        if sid == "S021":
            assert raw_map["SCH005"].status == EligibilityStatus.INELIGIBLE
            assert "KRISHI_BHAGYA_NOT_DRYLAND" in raw_map["SCH005"].rule_keys_fired
            # SMAM is ELIGIBLE
            assert raw_map["SCH004"].status == EligibilityStatus.ELIGIBLE
            assert "SMAM_NO_PRIOR_SUBSIDY" in raw_map["SCH004"].rule_keys_fired

        # S022 Soil Health Card: universal access
        if sid == "S022":
            assert raw_map["SCH009"].status == EligibilityStatus.ELIGIBLE
            assert "SHC_UNIVERSAL_ACCESS_VERIFIED" in raw_map["SCH009"].rule_keys_fired
