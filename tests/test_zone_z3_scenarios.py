"""
Targeted consistency, execution validation, and governance safeguard tests for Zone Z3 Profiles (S023-S028).
Validates schema compliance, assignment matrix consistency, physical capacity rules (S023),
solar pump prerequisites (S024), pure tenant exclusion (S026), and the critical governance safeguard
decoupling raw engine determinations from provisional presentation status (S028).
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
Z3_DIR = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", "z3")
Z3_IDS = ["S023", "S024", "S025", "S026", "S027", "S028"]


@pytest.fixture(scope="module")
def z3_profiles():
    profiles = {}
    for sid in Z3_IDS:
        filepath = os.path.join(Z3_DIR, f"{sid}.json")
        assert os.path.exists(filepath), f"Profile file missing: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            profiles[sid] = json.load(f)
    return profiles


@pytest.fixture(scope="module")
def z3_execution_results():
    filepath = os.path.join(Z3_DIR, "z3_execution_results.json")
    assert os.path.exists(filepath), f"Execution results missing: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def matrix_scenarios_by_id():
    return {s["sid"]: s for s in scenarios if s["sid"] in Z3_IDS}


def test_zone_z3_files_exist():
    """Verify all 6 JSON and Markdown profiles exist, along with batch and execution JSONs."""
    for sid in Z3_IDS:
        json_file = os.path.join(Z3_DIR, f"{sid}.json")
        md_file = os.path.join(Z3_DIR, f"{sid}.md")
        assert os.path.exists(json_file), f"Missing {json_file}"
        assert os.path.exists(md_file), f"Missing {md_file}"
        assert os.path.getsize(json_file) > 100
        assert os.path.getsize(md_file) > 100

    batch_json = os.path.join(Z3_DIR, "z3_scenarios.json")
    assert os.path.exists(batch_json)
    
    exec_json = os.path.join(Z3_DIR, "z3_execution_results.json")
    assert os.path.exists(exec_json)


def test_zone_z3_matrix_consistency(z3_profiles, matrix_scenarios_by_id):
    """Verify each profile exactly matches its row in the benchmark assignment matrix."""
    for sid in Z3_IDS:
        prof = z3_profiles[sid]
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
        elif mat["land_type"] == "Borewell-irrigated":
            assert prof["land_type"] == "Irrigated (Borewell)"

        # Farmer category mapping
        if mat["lclass"] == "Marginal":
            assert "Marginal" in prof["farmer_category"]
        elif mat["lclass"] == "Small":
            assert "Small" in prof["farmer_category"]
        elif mat["lclass"] == "Medium":
            assert "Medium" in prof["farmer_category"]


def test_zone_z3_s023_physical_capacity(z3_profiles):
    """Verify S023 requested subsidized area (1.41 ha) does not exceed qualifying parcel capacity (3.5 ac = 1.4164 ha)."""
    s023 = z3_profiles["S023"]
    req_ha = s023["landholding_details"]["requested_subsidized_area_ha"]
    parcel_ac = s023["landholding_details"]["qualifying_parcel_acres"]
    
    assert req_ha == 1.41
    assert parcel_ac == 3.5
    max_phys_ha = parcel_ac * 0.404686
    assert req_ha <= max_phys_ha + 1e-4, f"Requested {req_ha} ha exceeds parcel capacity {max_phys_ha} ha"


def test_zone_z3_s024_solar_prerequisites(z3_profiles):
    """Verify S024 has explicit unenergized borewell and off-grid electric status for PM-KUSUM B."""
    s024 = z3_profiles["S024"]
    assert "Borewell (Non-energized)" in s024["existing_assets"]
    assert s024["borewell_electric_status"] == "UNENERGIZED_OFF_GRID"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s024["scenario_id"],
        "agro_climatic_zone": s024["agro_climatic_zone"],
        "district": s024["district"],
        "crop_primary": s024["crop_primary"],
        "land_size_acres": s024["land_size_acres"],
        "land_type": s024["land_type"],
        "social_category": s024["social_category"],
        "farmer_category": s024["farmer_category"],
        "existing_assets": s024["existing_assets"],
        "annual_family_income_lakh": s024["annual_family_income_lakh"],
        "immediate_need": s024["immediate_need"],
        "superannuated_pensioner_monthly_amount": s024["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s024["pensioner_is_mts_exempt"],
        "paid_income_tax_last_assessment_year": s024["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s024["govt_employee_category"],
        "registered_professional": s024["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s024["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s024["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s024["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)
    det = engine.evaluate_scheme(sc, "SCH006")
    assert det.status == EligibilityStatus.ELIGIBLE
    assert "KUSUM_B_WATER_SOURCE_PRESENT" in det.rule_keys_fired
    assert "KUSUM_B_OFF_GRID_VERIFIED" in det.rule_keys_fired


def test_zone_z3_s026_pure_tenant_exclusion(z3_profiles):
    """Verify S026 pure tenant flag triggers PM-KISAN exclusion while Central KCC credit remains accessible."""
    s026 = z3_profiles["S026"]
    assert s026["is_pure_tenant_without_land_title"] is True
    assert s026["land_size_acres"] == 2.5
    assert "Small" in s026["farmer_category"]

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s026["scenario_id"],
        "agro_climatic_zone": s026["agro_climatic_zone"],
        "district": s026["district"],
        "crop_primary": s026["crop_primary"],
        "land_size_acres": s026["land_size_acres"],
        "land_type": s026["land_type"],
        "social_category": s026["social_category"],
        "farmer_category": s026["farmer_category"],
        "existing_assets": s026["existing_assets"],
        "annual_family_income_lakh": s026["annual_family_income_lakh"],
        "immediate_need": s026["immediate_need"],
        "superannuated_pensioner_monthly_amount": s026["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s026["pensioner_is_mts_exempt"],
        "paid_income_tax_last_assessment_year": s026["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s026["govt_employee_category"],
        "registered_professional": s026["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s026["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s026["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s026["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # PM-KISAN: Pure tenant exclusion
    det_kisan = engine.evaluate_scheme(sc, "SCH001")
    assert det_kisan.status == EligibilityStatus.INELIGIBLE
    assert "PMKISAN_PURE_TENANT_EXCLUSION" in det_kisan.rule_keys_fired

    # Credit Child: Central KCC-MISS accessible to sharecroppers/tenants
    det_kcc = engine.evaluate_scheme(sc, "SCH008_CENTRAL")
    assert det_kcc.status == EligibilityStatus.ELIGIBLE


def test_zone_z3_provisional_governance_safeguard(z3_execution_results):
    """
    CRITICAL GOVERNANCE SAFEGUARD:
    Verify that provisional corporation records appear in Section B as REQUIRES_VERIFICATION
    and receive no numerical relevance score, while preserving raw determinations separately.
    Covers BOTH:
    1. An ELIGIBLE raw result for a provisional scheme (S028 SCH010_DEVARAJ_URS)
    2. An INELIGIBLE raw result for a provisional scheme (S024 SCH010_VALMIKI)
    """
    results_map = {r["scenario"]["scenario_id"]: r for r in z3_execution_results["results"]}

    # Case 1: S028 - Raw ELIGIBLE for provisional SCH010_DEVARAJ_URS
    s028_act = {d["scheme_id"]: d for d in results_map["S028"]["actionable_determinations"]}
    devaraj = s028_act["SCH010_DEVARAJ_URS"]
    
    assert devaraj["is_provisional"] is True
    # Raw engine determination is preserved as ELIGIBLE
    assert devaraj["raw_engine_status"] == "ELIGIBLE"
    assert "GK_SCH010_DEVARAJ_URS_COMMUNITY_ROUTE_VALID" in devaraj["rule_keys_fired"]
    # Governance presentation status is decoupled to REQUIRES_VERIFICATION
    assert devaraj["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in devaraj["presentation_section"]
    assert devaraj["allow_numerical_scoring"] is False

    # Case 2: S024 - Raw INELIGIBLE for provisional SCH010_VALMIKI (canal land)
    s024_act = {d["scheme_id"]: d for d in results_map["S024"]["actionable_determinations"]}
    valmiki = s024_act["SCH010_VALMIKI"]
    
    assert valmiki["is_provisional"] is True
    # Raw engine determination is INELIGIBLE
    assert valmiki["raw_engine_status"] == "INELIGIBLE"
    assert "GK_SCH010_VALMIKI_NOT_DRYLAND" in valmiki["rule_keys_fired"]
    # Governance status reflects disqualification without confirmed entitlement
    assert valmiki["governance_status"] == "INELIGIBLE"
    assert valmiki["allow_numerical_scoring"] is False


def test_zone_z3_engine_execution_reproducibility(z3_profiles):
    """Execute all Zone Z3 profiles through EligibilityEngine and verify reproducible rule firings."""
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

    for sid in Z3_IDS:
        prof = z3_profiles[sid]
        filtered = {k: prof[k] for k in engine_keys if k in prof}
        scenario = FarmerScenario.from_dict(filtered)

        raw = engine.evaluate_scenario(scenario, include_children=True)
        raw = avail.apply_availability(raw, as_of_date="2026-10-15")
        actionable = engine.resolve_actionable_determinations(raw)

        raw_map = {d.scheme_id: d for d in raw}
        act_map = {d.scheme_id: d for d in actionable}

        # Parent deduplication check:
        # SCH008 must always be suppressed in actionable determinations
        assert "SCH008" not in act_map
        assert "SCH008_CENTRAL" in act_map

        # S023: PMKSY-PDMC is ELIGIBLE
        if sid == "S023":
            assert raw_map["SCH003"].status == EligibilityStatus.ELIGIBLE
            assert "PMKSY_WATER_SOURCE_VERIFIED" in raw_map["SCH003"].rule_keys_fired

        # S025: MIDH is ELIGIBLE
        if sid == "S025":
            assert raw_map["SCH007"].status == EligibilityStatus.ELIGIBLE
            assert "MIDH_MICRO_IRRIGATION_VERIFIED" in raw_map["SCH007"].rule_keys_fired

        # S027: Krishi Bhagya is ELIGIBLE
        if sid == "S027":
            assert raw_map["SCH005"].status == EligibilityStatus.ELIGIBLE
            assert "KRISHI_BHAGYA_DRYLAND_VERIFIED" in raw_map["SCH005"].rule_keys_fired


def test_zone_z3_pmfby_pomegranate_governance(z3_profiles, z3_execution_results):
    """
    Priority 1 Regression Test:
    Verify that PMFBY for pomegranate in S023 and S027 preserves raw INELIGIBLE (static whitelist omission)
    while governance presentation decouples to REQUIRES_VERIFICATION in Section B, pending seasonal notification.
    """
    engine = EligibilityEngine()
    results_map = {r["scenario"]["scenario_id"]: r for r in z3_execution_results["results"]}

    for sid in ["S023", "S027"]:
        prof = z3_profiles[sid]
        assert prof["crop_primary"] == "Pomegranate"

        # Raw engine check
        sc = FarmerScenario.from_dict({
            "scenario_id": prof["scenario_id"],
            "agro_climatic_zone": prof["agro_climatic_zone"],
            "district": prof["district"],
            "crop_primary": prof["crop_primary"],
            "land_size_acres": prof["land_size_acres"],
            "land_type": prof["land_type"],
            "social_category": prof["social_category"],
            "farmer_category": prof["farmer_category"],
            "existing_assets": prof["existing_assets"],
            "annual_family_income_lakh": prof["annual_family_income_lakh"],
            "immediate_need": prof["immediate_need"],
            "paid_income_tax_last_assessment_year": prof["paid_income_tax_last_assessment_year"],
            "govt_employee_category": prof["govt_employee_category"],
            "superannuated_pensioner_monthly_amount": prof["superannuated_pensioner_monthly_amount"],
            "pensioner_is_mts_exempt": prof["pensioner_is_mts_exempt"],
            "registered_professional": prof["registered_professional"],
            "land_ownership_cutoff_pre_feb_2019": prof["land_ownership_cutoff_pre_feb_2019"],
            "is_pure_tenant_without_land_title": prof["is_pure_tenant_without_land_title"],
            "borewell_electric_status": prof["borewell_electric_status"]
        })
        raw_pmfby = engine.evaluate_scheme(sc, "SCH002")
        assert raw_pmfby.status == EligibilityStatus.INELIGIBLE
        assert "PMFBY_NON_NOTIFIED_CROP" in raw_pmfby.rule_keys_fired

        # Governance presentation check
        act_dets = {d["scheme_id"]: d for d in results_map[sid]["actionable_determinations"]}
        gov_pmfby = act_dets["SCH002"]
        assert gov_pmfby["raw_engine_status"] == "INELIGIBLE"
        assert gov_pmfby["governance_status"] == "REQUIRES_VERIFICATION"
        assert "Section B" in gov_pmfby["presentation_section"]
        assert gov_pmfby["allow_numerical_scoring"] is False
        assert any("Pomegranate" in m for m in gov_pmfby["missing_verifications"])


def test_zone_z3_s026_tenant_kcc_documentation_governance(z3_profiles, z3_execution_results):
    """
    Priority 3 Regression Test:
    Verify that S026 pure tenant without recorded loan documentation preserves raw ELIGIBLE for Central KCC,
    but governance presentation routes to REQUIRES_VERIFICATION in Section B.
    """
    s026 = z3_profiles["S026"]
    assert s026["is_pure_tenant_without_land_title"] is True
    # Verify no formal bank tenant declaration or JLG agreement is recorded in profile
    assert "JLG" not in str(s026["existing_assets"])
    assert "Bank oral lease declaration" not in s026["statutory_flags"]["tenure_documentation"]

    results_map = {r["scenario"]["scenario_id"]: r for r in z3_execution_results["results"]}
    s026_act = {d["scheme_id"]: d for d in results_map["S026"]["actionable_determinations"]}
    kcc = s026_act["SCH008_CENTRAL"]

    # Raw engine status preserved as ELIGIBLE
    assert kcc["raw_engine_status"] == "ELIGIBLE"
    # Governance presentation routes to REQUIRES_VERIFICATION in Section B
    assert kcc["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in kcc["presentation_section"]
    assert kcc["allow_numerical_scoring"] is False
    assert any("Tenant farmer crop loan documentation" in m for m in kcc["missing_verifications"])


def test_zone_z3_s028_beneficiary_threshold_discrepancy(z3_profiles, z3_execution_results):
    """
    Priority 2 Regression Test:
    Document and test the discrepancy between the benchmark design (minimum 3 community beneficiaries)
    and the frozen engine implementation (_eval_ganga_kalyana_child line 576 accepting >= 2 for Devaraj Urs).
    Preserves raw ELIGIBLE and provisional REQUIRES_VERIFICATION governance presentation for S028.
    """
    engine = EligibilityEngine()
    s028 = z3_profiles["S028"]

    # S028 as defined (3 beneficiaries, 9.0 acres) satisfies both thresholds
    assert s028["community_pool_acres"] == 9.0
    assert s028["community_pool_beneficiaries_count"] == 3

    # Test frozen engine behavior with a 2-beneficiary OBC group (regression test for discrepancy)
    two_beneficiary_data = {
        "scenario_id": "S028_TWO_BENEFICIARY_TEST",
        "agro_climatic_zone": "Northern Dry Zone",
        "district": "Bagalkot",
        "crop_primary": "Onion",
        "land_size_acres": 10.0,
        "land_type": "Dryland (Rainfed)",
        "social_category": "OBC (2A)",
        "farmer_category": "Medium (5-10 acres)",
        "existing_assets": [],
        "annual_family_income_lakh": 3.0,
        "immediate_need": "BOREWELL_IRRIGATION",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": "NONE",
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": "NONE",
        "community_pool_acres": 9.0,
        "community_pool_beneficiaries_count": 2  # 2 beneficiaries tests the discrepancy
    }
    sc_two = FarmerScenario.from_dict(two_beneficiary_data)
    det_two = engine.evaluate_scheme(sc_two, "SCH010_DEVARAJ_URS")
    
    # Frozen engine accepts >= 2 beneficiaries for Devaraj Urs
    assert det_two.status == EligibilityStatus.ELIGIBLE
    assert "GK_SCH010_DEVARAJ_URS_COMMUNITY_ROUTE_VALID" in det_two.rule_keys_fired

    # Confirm that Ambedkar corporation in contrast strictly rejects < 3 beneficiaries
    sc_two_sc = FarmerScenario.from_dict({**two_beneficiary_data, "social_category": "SC"})
    det_ambedkar = engine.evaluate_scheme(sc_two_sc, "SCH010_AMBEDKAR")
    assert "GK_AMBEDKAR_COMMUNITY_MIN_BENEFICIARIES_FAILED" in det_ambedkar.rule_keys_fired

    # Verify S028 governance status and missing verifications in execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z3_execution_results["results"]}
    s028_act = {d["scheme_id"]: d for d in results_map["S028"]["actionable_determinations"]}
    devaraj = s028_act["SCH010_DEVARAJ_URS"]
    
    assert devaraj["raw_engine_status"] == "ELIGIBLE"
    assert devaraj["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in devaraj["presentation_section"]
    assert devaraj["allow_numerical_scoring"] is False
    # Ensure missing verifications is NOT empty and specifically records the 2 vs 3 discrepancy
    assert len(devaraj["missing_verifications"]) > 0
    assert any("2 vs 3 beneficiaries" in m for m in devaraj["missing_verifications"])


def test_zone_z3_s028_bagalkot_location_normalization_governance(z3_execution_results):
    """
    Priority 4 Regression Test:
    Verify that Krishi Bhagya for S028 is preserved as raw INELIGIBLE (due to 'Bagalkote' vs 'Bagalkot')
    while governance presentation decouples to REQUIRES_VERIFICATION in Section B as an unresolved location-policy dependency.
    """
    results_map = {r["scenario"]["scenario_id"]: r for r in z3_execution_results["results"]}
    s028_act = {d["scheme_id"]: d for d in results_map["S028"]["actionable_determinations"]}
    kb = s028_act["SCH005"]

    assert kb["raw_engine_status"] == "INELIGIBLE"
    assert "KRISHI_BHAGYA_DISTRICT_NOT_RAINFED" in kb["rule_keys_fired"]
    assert kb["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in kb["presentation_section"]
    assert kb["allow_numerical_scoring"] is False
    assert any("Bagalkote" in m for m in kb["missing_verifications"])
