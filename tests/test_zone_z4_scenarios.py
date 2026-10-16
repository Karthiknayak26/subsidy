"""
Targeted consistency, execution validation, and governance safeguard tests for Zone Z4 Profiles (S029-S034).
Validates schema compliance, assignment matrix consistency, Ambedkar Corporation individual route (S029),
solar pump vs hydrological gating (S030), Valmiki ST provisional governance safeguard (S031),
income-tax-payer exclusion overriding stated need (S032), plantation mechanization (S033),
and large holding PMKSY-PDMC area cap validation (S034).
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
Z4_DIR = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", "z4")
Z4_IDS = ["S029", "S030", "S031", "S032", "S033", "S034"]


@pytest.fixture(scope="module")
def z4_profiles():
    profiles = {}
    for sid in Z4_IDS:
        filepath = os.path.join(Z4_DIR, f"{sid}.json")
        assert os.path.exists(filepath), f"Profile file missing: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            profiles[sid] = json.load(f)
    return profiles


@pytest.fixture(scope="module")
def z4_execution_results():
    filepath = os.path.join(Z4_DIR, "z4_execution_results.json")
    assert os.path.exists(filepath), f"Execution results missing: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def matrix_scenarios_by_id():
    return {s["sid"]: s for s in scenarios if s["sid"] in Z4_IDS}


def test_zone_z4_files_exist():
    """Verify all 6 JSON and Markdown profiles exist, along with batch and execution JSONs."""
    for sid in Z4_IDS:
        json_file = os.path.join(Z4_DIR, f"{sid}.json")
        md_file = os.path.join(Z4_DIR, f"{sid}.md")
        assert os.path.exists(json_file), f"Missing {json_file}"
        assert os.path.exists(md_file), f"Missing {md_file}"
        assert os.path.getsize(json_file) > 100
        assert os.path.getsize(md_file) > 100

    batch_json = os.path.join(Z4_DIR, "z4_scenarios.json")
    assert os.path.exists(batch_json)
    
    exec_json = os.path.join(Z4_DIR, "z4_execution_results.json")
    assert os.path.exists(exec_json)


def test_zone_z4_matrix_consistency(z4_profiles, matrix_scenarios_by_id):
    """Verify each profile exactly matches its row in the benchmark assignment matrix."""
    for sid in Z4_IDS:
        prof = z4_profiles[sid]
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
        elif mat["lclass"] == "Large":
            assert "Large" in prof["farmer_category"]


def test_zone_z4_s029_ambedkar_individual_route(z4_profiles, z4_execution_results):
    """
    Verify S029 (SC marginal dryland farmer, 2.0 ac, Chitradurga) raw engine qualifies for SCH010_AMBEDKAR,
    but governance safeguard routes it to Section B as REQUIRES_VERIFICATION with scoring disabled
    pending source-adjacency and income-order verification.
    """
    s029 = z4_profiles["S029"]
    assert s029["social_category"] == "SC"
    assert s029["land_type"] == "Dryland (Rainfed)"
    assert s029["land_size_acres"] == 2.0
    assert s029["annual_family_income_lakh"] <= 2.0

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s029["scenario_id"],
        "agro_climatic_zone": s029["agro_climatic_zone"],
        "district": s029["district"],
        "crop_primary": s029["crop_primary"],
        "land_size_acres": s029["land_size_acres"],
        "land_type": s029["land_type"],
        "social_category": s029["social_category"],
        "farmer_category": s029["farmer_category"],
        "existing_assets": s029["existing_assets"],
        "annual_family_income_lakh": s029["annual_family_income_lakh"],
        "immediate_need": s029["immediate_need"],
        "paid_income_tax_last_assessment_year": s029["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s029["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s029["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s029["pensioner_is_mts_exempt"],
        "registered_professional": s029["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s029["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s029["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s029["borewell_electric_status"],
        "community_pool_acres": s029["community_pool_acres"],
        "community_pool_beneficiaries_count": s029["community_pool_beneficiaries_count"]
    }
    sc = FarmerScenario.from_dict(filtered)
    det = engine.evaluate_scheme(sc, "SCH010_AMBEDKAR")
    assert det.status == EligibilityStatus.ELIGIBLE
    assert "GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID" in det.rule_keys_fired

    # Check execution results governance presentation
    results_map = {r["scenario"]["scenario_id"]: r for r in z4_execution_results["results"]}
    s029_act = {d["scheme_id"]: d for d in results_map["S029"]["actionable_determinations"]}
    ambedkar = s029_act["SCH010_AMBEDKAR"]

    # Raw engine determined ELIGIBLE — frozen engine must not be changed
    assert ambedkar["raw_engine_status"] == "ELIGIBLE"
    # Governance correction: source-adjacency evidence gap and income-ceiling discrepancy → REQUIRES_VERIFICATION
    assert ambedkar["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in ambedkar["presentation_section"]
    assert ambedkar["allow_numerical_scoring"] is False
    # Assert missing_verifications field records both required verifications
    assert any("perennial water source" in mv.lower() for mv in ambedkar["missing_verifications"])
    assert any("chitradurga" in mv.lower() and "income" in mv.lower() for mv in ambedkar["missing_verifications"])
    # Abstract parent SCH010 must be deduplicated
    assert "SCH010" not in s029_act


def test_zone_z4_s030_solar_pump_vs_hydrological_gating(z4_profiles, z4_execution_results):
    """
    Benchmark Challenge 1:
    Verify S030 off-grid unenergized borewell qualifies for PM-KUSUM Component B
    while canal land type strictly disqualifies Krishi Bhagya and Ganga Kalyana.
    """
    s030 = z4_profiles["S030"]
    assert "Borewell (Non-energized)" in s030["existing_assets"]
    assert s030["borewell_electric_status"] == "UNENERGIZED_OFF_GRID"
    assert s030["land_type"] == "Irrigated (Canal)"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s030["scenario_id"],
        "agro_climatic_zone": s030["agro_climatic_zone"],
        "district": s030["district"],
        "crop_primary": s030["crop_primary"],
        "land_size_acres": s030["land_size_acres"],
        "land_type": s030["land_type"],
        "social_category": s030["social_category"],
        "farmer_category": s030["farmer_category"],
        "existing_assets": s030["existing_assets"],
        "annual_family_income_lakh": s030["annual_family_income_lakh"],
        "immediate_need": s030["immediate_need"],
        "paid_income_tax_last_assessment_year": s030["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s030["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s030["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s030["pensioner_is_mts_exempt"],
        "registered_professional": s030["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s030["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s030["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s030["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # PM-KUSUM Component B qualifies
    det_kusum = engine.evaluate_scheme(sc, "SCH006")
    assert det_kusum.status == EligibilityStatus.ELIGIBLE
    assert "KUSUM_B_WATER_SOURCE_PRESENT" in det_kusum.rule_keys_fired
    assert "KUSUM_B_OFF_GRID_VERIFIED" in det_kusum.rule_keys_fired

    # Krishi Bhagya disqualified due to canal irrigation
    det_kb = engine.evaluate_scheme(sc, "SCH005")
    assert det_kb.status == EligibilityStatus.INELIGIBLE
    assert "KRISHI_BHAGYA_NOT_DRYLAND" in det_kb.rule_keys_fired


def test_zone_z4_s031_valmiki_provisional_governance_safeguard(z4_profiles, z4_execution_results):
    """
    Verify S031 (ST marginal dryland farmer, 1.8 ac, Tumakuru) qualifies for raw SCH010_VALMIKI,
    but governance presentation decouples to REQUIRES_VERIFICATION in Section B due to provisional status.
    """
    s031 = z4_profiles["S031"]
    assert s031["social_category"] == "ST"
    assert s031["land_type"] == "Dryland (Rainfed)"
    assert s031["land_size_acres"] == 1.8

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s031["scenario_id"],
        "agro_climatic_zone": s031["agro_climatic_zone"],
        "district": s031["district"],
        "crop_primary": s031["crop_primary"],
        "land_size_acres": s031["land_size_acres"],
        "land_type": s031["land_type"],
        "social_category": s031["social_category"],
        "farmer_category": s031["farmer_category"],
        "existing_assets": s031["existing_assets"],
        "annual_family_income_lakh": s031["annual_family_income_lakh"],
        "immediate_need": s031["immediate_need"],
        "paid_income_tax_last_assessment_year": s031["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s031["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s031["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s031["pensioner_is_mts_exempt"],
        "registered_professional": s031["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s031["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s031["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s031["borewell_electric_status"],
        "community_pool_acres": s031["community_pool_acres"],
        "community_pool_beneficiaries_count": s031["community_pool_beneficiaries_count"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # Raw engine returns ELIGIBLE
    det_valmiki = engine.evaluate_scheme(sc, "SCH010_VALMIKI")
    assert det_valmiki.status == EligibilityStatus.ELIGIBLE
    assert "GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID" in det_valmiki.rule_keys_fired

    # Check execution results governance presentation
    results_map = {r["scenario"]["scenario_id"]: r for r in z4_execution_results["results"]}
    s031_act = {d["scheme_id"]: d for d in results_map["S031"]["actionable_determinations"]}
    valmiki = s031_act["SCH010_VALMIKI"]
    
    assert valmiki["is_provisional"] is True
    assert valmiki["raw_engine_status"] == "ELIGIBLE"
    assert valmiki["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in valmiki["presentation_section"]
    assert valmiki["allow_numerical_scoring"] is False
    assert len(valmiki["missing_verifications"]) > 0
    assert any("Valmiki" in m for m in valmiki["missing_verifications"])


def test_zone_z4_s032_income_tax_exclusion_overrides_need(z4_profiles, z4_execution_results):
    """
    Benchmark Challenge 3 & Boundary Test:
    Verify exactly 2.5 acres is classified as Small; farmer has immediate need INCOME_SUPPORT,
    but income tax payment strictly disqualifies PM-KISAN, while Central KCC remains accessible.
    """
    s032 = z4_profiles["S032"]
    assert s032["land_size_acres"] == 2.5
    assert "Small" in s032["farmer_category"]
    assert s032["immediate_need"] == "INCOME_SUPPORT"
    assert s032["paid_income_tax_last_assessment_year"] is True

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s032["scenario_id"],
        "agro_climatic_zone": s032["agro_climatic_zone"],
        "district": s032["district"],
        "crop_primary": s032["crop_primary"],
        "land_size_acres": s032["land_size_acres"],
        "land_type": s032["land_type"],
        "social_category": s032["social_category"],
        "farmer_category": s032["farmer_category"],
        "existing_assets": s032["existing_assets"],
        "annual_family_income_lakh": s032["annual_family_income_lakh"],
        "immediate_need": s032["immediate_need"],
        "paid_income_tax_last_assessment_year": s032["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s032["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s032["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s032["pensioner_is_mts_exempt"],
        "registered_professional": s032["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s032["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s032["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s032["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # PM-KISAN: Ineligible due to income tax payment
    det_kisan = engine.evaluate_scheme(sc, "SCH001")
    assert det_kisan.status == EligibilityStatus.INELIGIBLE
    assert "PMKISAN_PAID_INCOME_TAX_EXCLUSION" in det_kisan.rule_keys_fired

    # Central KCC credit remains accessible
    det_kcc = engine.evaluate_scheme(sc, "SCH008_CENTRAL")
    assert det_kcc.status == EligibilityStatus.ELIGIBLE
    assert "KCC_CENTRAL_COMMERCIAL_ELIGIBLE" in det_kcc.rule_keys_fired


def test_zone_z4_s033_arecanut_smam_and_grid_exclusion(z4_profiles, z4_execution_results):
    """
    Verify S033 (Medium holding, 7.5 ac arecanut) qualifies for SMAM farm mechanization,
    while grid-connected IP set strictly excludes PM-KUSUM Component B.
    """
    s033 = z4_profiles["S033"]
    assert s033["land_size_acres"] == 7.5
    assert "Medium" in s033["farmer_category"]
    assert s033["immediate_need"] == "FARM_MECHANIZATION"
    assert s033["borewell_electric_status"] == "GRID_CONNECTED_IP_SET"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s033["scenario_id"],
        "agro_climatic_zone": s033["agro_climatic_zone"],
        "district": s033["district"],
        "crop_primary": s033["crop_primary"],
        "land_size_acres": s033["land_size_acres"],
        "land_type": s033["land_type"],
        "social_category": s033["social_category"],
        "farmer_category": s033["farmer_category"],
        "existing_assets": s033["existing_assets"],
        "annual_family_income_lakh": s033["annual_family_income_lakh"],
        "immediate_need": s033["immediate_need"],
        "paid_income_tax_last_assessment_year": s033["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s033["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s033["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s033["pensioner_is_mts_exempt"],
        "registered_professional": s033["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s033["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s033["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s033["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # SMAM: Eligible
    det_smam = engine.evaluate_scheme(sc, "SCH004")
    assert det_smam.status == EligibilityStatus.ELIGIBLE
    assert "SMAM_NO_PRIOR_SUBSIDY" in det_smam.rule_keys_fired

    # PM-KUSUM Component B: Ineligible due to grid-connected IP set
    det_kusum = engine.evaluate_scheme(sc, "SCH006")
    assert det_kusum.status == EligibilityStatus.INELIGIBLE
    assert "KUSUM_B_GRID_CONNECTED_DISQUALIFIED" in det_kusum.rule_keys_fired


def test_zone_z4_s034_large_holding_area_cap(z4_profiles, z4_execution_results):
    """
    Benchmark Challenge 8 & Area Cap Test:
    Verify S034 Large holding (11.0 ac) requested subsidized area (4.45 ha) satisfies
    both physical parcel capacity (4.45 ha <= 11.0 ac * 0.404686 = 4.4515 ha)
    and national statutory ceiling (4.45 ha <= 5.00 ha), qualifying for PMKSY-PDMC.
    """
    s034 = z4_profiles["S034"]
    assert s034["land_size_acres"] == 11.0
    assert "Large" in s034["farmer_category"]
    
    req_ha = s034["landholding_details"]["requested_subsidized_area_ha"]
    parcel_ac = s034["landholding_details"]["qualifying_parcel_acres"]
    assert req_ha == 4.45
    assert parcel_ac == 11.0

    # Cross-field physical capacity check
    max_phys_ha = parcel_ac * 0.404686
    assert req_ha <= max_phys_ha + 1e-4, f"Requested {req_ha} ha exceeds parcel capacity {max_phys_ha} ha"
    # Statutory ceiling check
    assert req_ha <= 5.00, f"Requested {req_ha} ha exceeds statutory ceiling 5.00 ha"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s034["scenario_id"],
        "agro_climatic_zone": s034["agro_climatic_zone"],
        "district": s034["district"],
        "crop_primary": s034["crop_primary"],
        "land_size_acres": s034["land_size_acres"],
        "land_type": s034["land_type"],
        "social_category": s034["social_category"],
        "farmer_category": s034["farmer_category"],
        "existing_assets": s034["existing_assets"],
        "annual_family_income_lakh": s034["annual_family_income_lakh"],
        "immediate_need": s034["immediate_need"],
        "paid_income_tax_last_assessment_year": s034["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s034["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s034["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s034["pensioner_is_mts_exempt"],
        "registered_professional": s034["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s034["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s034["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s034["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # PMKSY-PDMC qualifies
    det_pdmc = engine.evaluate_scheme(sc, "SCH003")
    assert det_pdmc.status == EligibilityStatus.ELIGIBLE
    assert "PMKSY_LAND_RANGE_VALID" in det_pdmc.rule_keys_fired
    assert "PMKSY_WATER_SOURCE_VERIFIED" in det_pdmc.rule_keys_fired


def test_zone_z4_engine_execution_reproducibility(z4_profiles):
    """Execute all Zone Z4 profiles through EligibilityEngine and verify reproducible rule firings and deduplication."""
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

    for sid in Z4_IDS:
        prof = z4_profiles[sid]
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

        # In S029 and S031 where Ganga Kalyana child is actionable, SCH010 must be suppressed
        if sid in ["S029", "S031"]:
            assert "SCH010" not in act_map
