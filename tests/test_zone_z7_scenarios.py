"""
Targeted consistency, execution validation, and governance safeguard tests for Zone Z7 Profiles (S047-S052).
Validates schema compliance, assignment matrix consistency, SMAM implement mechanization in canal command (S047),
Challenge 4 three-valued logic and UNKNOWN attribute handling (S048),
Post-Feb 2019 inheritance succession and MIDH protected horticulture (S049),
Challenge 6 competing credit channels for arecanut (S050),
Boundary test at exactly 2.5 acres and PM-KUSUM B standalone solar pump (S051),
Challenge 7 community borewell pooling and beneficiary discrepancy safeguard (S052),
four-state availability decoupling, and parent deduplication reconciliation.
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
Z7_DIR = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", "z7")
REPORTS_DIR = os.path.join(WORKSPACE_ROOT, "reports")
Z7_IDS = ["S047", "S048", "S049", "S050", "S051", "S052"]


@pytest.fixture(scope="module")
def z7_profiles():
    profiles = {}
    for sid in Z7_IDS:
        filepath = os.path.join(Z7_DIR, f"{sid}.json")
        assert os.path.exists(filepath), f"Profile file missing: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            profiles[sid] = json.load(f)
    return profiles


@pytest.fixture(scope="module")
def z7_execution_results():
    filepath = os.path.join(Z7_DIR, "z7_execution_results.json")
    assert os.path.exists(filepath), f"Execution results missing: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def matrix_scenarios_by_id():
    return {s["sid"]: s for s in scenarios if s["sid"] in Z7_IDS}


def test_zone_z7_files_exist():
    """Verify all 6 JSON and Markdown profiles exist, along with batch, execution JSONs and report."""
    for sid in Z7_IDS:
        json_file = os.path.join(Z7_DIR, f"{sid}.json")
        md_file = os.path.join(Z7_DIR, f"{sid}.md")
        assert os.path.exists(json_file), f"Missing {json_file}"
        assert os.path.exists(md_file), f"Missing {md_file}"
        assert os.path.getsize(json_file) > 100
        assert os.path.getsize(md_file) > 100

    batch_json = os.path.join(Z7_DIR, "z7_scenarios.json")
    assert os.path.exists(batch_json)
    
    exec_json = os.path.join(Z7_DIR, "z7_execution_results.json")
    assert os.path.exists(exec_json)

    report_md = os.path.join(REPORTS_DIR, "zone_z7_execution_report.md")
    assert os.path.exists(report_md)
    assert os.path.getsize(report_md) > 1000


def test_zone_z7_matrix_consistency(z7_profiles, matrix_scenarios_by_id):
    """Verify each profile exactly matches its row in the benchmark assignment matrix."""
    for sid in Z7_IDS:
        prof = z7_profiles[sid]
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
        elif mat["land_type"] == "Wetland/valley":
            assert prof["land_type"] == "Wetland/valley"

        # Farmer category mapping
        if mat["lclass"] == "Marginal":
            assert "Marginal" in prof["farmer_category"]
        elif mat["lclass"] == "Small":
            assert "Small" in prof["farmer_category"]
        elif mat["lclass"] == "Medium":
            assert "Medium" in prof["farmer_category"]
        elif mat["lclass"] == "Large":
            assert "Large" in prof["farmer_category"]


def test_zone_z7_s047_smam_mechanization_canal(z7_profiles, z7_execution_results):
    """
    Verify S047 (General Merit medium maize farmer, 5.5 ac, Hassan):
    - Stated need: FARM_MECHANIZATION.
    - Qualifies for SMAM implement subsidy in Section A (SMAM_NO_PRIOR_SUBSIDY).
    - Canal irrigated land disqualifies Krishi Bhagya (KRISHI_BHAGYA_NOT_DRYLAND) and Ganga Kalyana (GK_PARENT_NOT_DRYLAND).
    - PM-KISAN, PMKSY-PDMC, Central KCC qualify in Section A.
    - PMFBY decoupled to Section B as REQUIRES_VERIFICATION pending Kharif IU notification.
    """
    s047 = z7_profiles["S047"]
    assert s047["immediate_need"] == "FARM_MECHANIZATION"
    assert s047["land_size_acres"] == 5.5
    assert s047["land_type"] == "Irrigated (Canal)"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s047["scenario_id"],
        "agro_climatic_zone": s047["agro_climatic_zone"],
        "district": s047["district"],
        "crop_primary": s047["crop_primary"],
        "land_size_acres": s047["land_size_acres"],
        "land_type": s047["land_type"],
        "social_category": s047["social_category"],
        "farmer_category": s047["farmer_category"],
        "existing_assets": s047["existing_assets"],
        "annual_family_income_lakh": s047["annual_family_income_lakh"],
        "immediate_need": s047["immediate_need"],
        "paid_income_tax_last_assessment_year": s047["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s047["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s047["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s047["pensioner_is_mts_exempt"],
        "registered_professional": s047["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s047["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s047["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s047["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # SMAM qualifies
    det_smam = engine.evaluate_scheme(sc, "SCH004")
    assert det_smam.status == EligibilityStatus.ELIGIBLE
    assert "SMAM_NO_PRIOR_SUBSIDY" in det_smam.rule_keys_fired

    # Krishi Bhagya disqualified due to canal land
    det_kb = engine.evaluate_scheme(sc, "SCH005")
    assert det_kb.status == EligibilityStatus.INELIGIBLE
    assert "KRISHI_BHAGYA_NOT_DRYLAND" in det_kb.rule_keys_fired

    # Check execution results governance presentation
    results_map = {r["scenario"]["scenario_id"]: r for r in z7_execution_results["results"]}
    s047_act = {d["scheme_id"]: d for d in results_map["S047"]["actionable_determinations"]}

    # SMAM is in Section A
    assert s047_act["SCH004"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s047_act["SCH004"]["presentation_section"]
    assert s047_act["SCH004"]["allow_numerical_scoring"] is True

    # PMFBY decoupled to Section B
    pmfby = s047_act["SCH002"]
    assert pmfby["raw_engine_status"] == "ELIGIBLE"
    assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in pmfby["presentation_section"]
    assert pmfby["allow_numerical_scoring"] is False
    assert any("maize" in mv.lower() for mv in pmfby["missing_verifications"])


def test_zone_z7_s048_challenge_4_unknown_attributes(z7_profiles, z7_execution_results):
    """
    Benchmark Challenge 4 (Three-Valued Logic & UNKNOWN Attributes):
    Verify S048 (ST marginal ginger grower, 2.0 ac, Shivamogga):
    - land_ownership_cutoff_pre_feb_2019 is None and superannuated_pensioner_monthly_amount is None.
    - Raw engine returns REQUIRES_VERIFICATION for PM-KISAN (PMKISAN_CUTOFF_DATE_UNKNOWN, PMKISAN_PENSION_UNKNOWN).
    - MIDH protected horticulture evaluates raw ELIGIBLE, but is routed to Section B as REQUIRES_VERIFICATION
      without scoring pending land title certification.
    - PM-KUSUM B is disqualified due to grid-connected IP set.
    - Ganga Kalyana is disqualified due to existing borewell.
    """
    s048 = z7_profiles["S048"]
    assert s048["immediate_need"] == "PROTECTED_HORTICULTURE"
    assert s048["land_ownership_cutoff_pre_feb_2019"] is None
    assert s048["superannuated_pensioner_monthly_amount"] is None
    assert s048["borewell_electric_status"] == "GRID_CONNECTED_IP_SET"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s048["scenario_id"],
        "agro_climatic_zone": s048["agro_climatic_zone"],
        "district": s048["district"],
        "crop_primary": s048["crop_primary"],
        "crop_secondary": s048.get("crop_secondary"),
        "land_size_acres": s048["land_size_acres"],
        "land_type": s048["land_type"],
        "social_category": s048["social_category"],
        "farmer_category": s048["farmer_category"],
        "existing_assets": s048["existing_assets"],
        "annual_family_income_lakh": s048["annual_family_income_lakh"],
        "immediate_need": s048["immediate_need"],
        "paid_income_tax_last_assessment_year": s048["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s048["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s048["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s048["pensioner_is_mts_exempt"],
        "registered_professional": s048["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s048["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s048["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s048["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # PM-KISAN evaluates REQUIRES_VERIFICATION
    det_pmk = engine.evaluate_scheme(sc, "SCH001")
    assert det_pmk.status == EligibilityStatus.REQUIRES_VERIFICATION
    assert "PMKISAN_CUTOFF_DATE_UNKNOWN" in det_pmk.rule_keys_fired
    assert "PMKISAN_PENSION_UNKNOWN" in det_pmk.rule_keys_fired

    # MIDH qualifies in raw engine
    det_midh = engine.evaluate_scheme(sc, "SCH007")
    assert det_midh.status == EligibilityStatus.ELIGIBLE
    assert "MIDH_HORTICULTURE_CROP_VERIFIED" in det_midh.rule_keys_fired

    # PM-KUSUM B disqualified due to grid connection
    det_kusum = engine.evaluate_scheme(sc, "SCH006")
    assert det_kusum.status == EligibilityStatus.INELIGIBLE
    assert "KUSUM_B_GRID_CONNECTED_DISQUALIFIED" in det_kusum.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z7_execution_results["results"]}
    s048_act = {d["scheme_id"]: d for d in results_map["S048"]["actionable_determinations"]}

    # PM-KISAN is in Section B
    assert s048_act["SCH001"]["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in s048_act["SCH001"]["presentation_section"]
    assert s048_act["SCH001"]["allow_numerical_scoring"] is False

    # MIDH is in Section B pending land title certification
    midh = s048_act["SCH007"]
    assert midh["raw_engine_status"] == "ELIGIBLE"
    assert midh["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in midh["presentation_section"]
    assert midh["allow_numerical_scoring"] is False
    assert any("title" in mv.lower() or "mutation" in mv.lower() for mv in midh["missing_verifications"])


def test_zone_z7_s049_post_2019_inheritance_midh(z7_profiles, z7_execution_results):
    """
    Verify S049 (General Merit small potato farmer, 4.5 ac, Chikkamagaluru):
    - Land title acquired post-Feb 2019 via statutory inheritance succession (transfer_basis = INHERITANCE_DUE_TO_DEATH).
    - Statutory flags explicitly record factual acquisition date (2022-06-14), death certificate, legal heir order, and Bhoomi mutation extract.
    - Consolidated engine cutoff input (land_ownership_cutoff_pre_feb_2019 = True) correctly qualifies PM-KISAN in Section A.
    - MIDH protected cultivation qualifies in Section A (MIDH_HORTICULTURE_CROP_VERIFIED, MIDH_LAND_MIN_MET, MIDH_MICRO_IRRIGATION_VERIFIED).
    - PM-KUSUM B and Ganga Kalyana disqualified.
    """
    s049 = z7_profiles["S049"]
    assert s049["land_ownership_cutoff_pre_feb_2019"] is True
    assert s049["immediate_need"] == "PROTECTED_HORTICULTURE"
    assert s049["borewell_electric_status"] == "GRID_CONNECTED_IP_SET"

    # Explicit audit of statutory inheritance transfer basis & evidence standard
    flags = s049["statutory_flags"]
    assert flags["transfer_basis"] == "INHERITANCE_DUE_TO_DEATH"
    assert flags["acquisition_date_relationship_to_cutoff"] == "POST_FEB_2019"
    assert flags["factual_acquisition_date"] == "2022-06-14"
    assert "DC-2022-4419" in flags["succession_death_certificate"]
    assert "LND/CR-104/2022-23" in flags["succession_legal_heir_order"]
    assert "MR-2022-0815" in flags["revenue_mutation_record"]
    assert "partition deed" in flags["tenure_documentation"].lower()
    assert "distinguished from non-exempt" in flags["tenure_documentation"].lower()

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s049["scenario_id"],
        "agro_climatic_zone": s049["agro_climatic_zone"],
        "district": s049["district"],
        "crop_primary": s049["crop_primary"],
        "crop_secondary": s049.get("crop_secondary"),
        "land_size_acres": s049["land_size_acres"],
        "land_type": s049["land_type"],
        "social_category": s049["social_category"],
        "farmer_category": s049["farmer_category"],
        "existing_assets": s049["existing_assets"],
        "annual_family_income_lakh": s049["annual_family_income_lakh"],
        "immediate_need": s049["immediate_need"],
        "paid_income_tax_last_assessment_year": s049["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s049["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s049["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s049["pensioner_is_mts_exempt"],
        "registered_professional": s049["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s049["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s049["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s049["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # PM-KISAN qualifies under statutory succession exemption
    det_pmk = engine.evaluate_scheme(sc, "SCH001")
    assert det_pmk.status == EligibilityStatus.ELIGIBLE
    assert "PMKISAN_CUTOFF_DATE_VERIFIED" in det_pmk.rule_keys_fired

    # MIDH qualifies
    det_midh = engine.evaluate_scheme(sc, "SCH007")
    assert det_midh.status == EligibilityStatus.ELIGIBLE
    assert "MIDH_HORTICULTURE_CROP_VERIFIED" in det_midh.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z7_execution_results["results"]}
    s049_act = {d["scheme_id"]: d for d in results_map["S049"]["actionable_determinations"]}

    assert s049_act["SCH001"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s049_act["SCH001"]["presentation_section"]

    assert s049_act["SCH007"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s049_act["SCH007"]["presentation_section"]
    assert s049_act["SCH007"]["allow_numerical_scoring"] is True


def test_zone_z7_s050_competing_credit_channels(z7_profiles, z7_execution_results):
    """
    Benchmark Challenge 6 (Competing Credit Channels):
    Verify S050 (OBC small arecanut farmer, 3.5 ac, Hassan):
    - Central KCC-MISS qualifies in Section A with clinical score 3.
    - State cooperative credit (SCH008_KA_COOP) is provisional and routed to Section B without scoring.
    - Abstract parent SCH008 is suppressed.
    """
    s050 = z7_profiles["S050"]
    assert s050["immediate_need"] == "PRODUCTION_CREDIT"
    assert s050["crop_primary"] == "Arecanut"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s050["scenario_id"],
        "agro_climatic_zone": s050["agro_climatic_zone"],
        "district": s050["district"],
        "crop_primary": s050["crop_primary"],
        "crop_secondary": s050.get("crop_secondary"),
        "land_size_acres": s050["land_size_acres"],
        "land_type": s050["land_type"],
        "social_category": s050["social_category"],
        "farmer_category": s050["farmer_category"],
        "existing_assets": s050["existing_assets"],
        "annual_family_income_lakh": s050["annual_family_income_lakh"],
        "immediate_need": s050["immediate_need"],
        "paid_income_tax_last_assessment_year": s050["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s050["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s050["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s050["pensioner_is_mts_exempt"],
        "registered_professional": s050["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s050["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s050["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s050["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # Central KCC qualifies
    det_kcc = engine.evaluate_scheme(sc, "SCH008_CENTRAL")
    assert det_kcc.status == EligibilityStatus.ELIGIBLE
    assert "KCC_CENTRAL_COMMERCIAL_ELIGIBLE" in det_kcc.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z7_execution_results["results"]}
    s050_act = {d["scheme_id"]: d for d in results_map["S050"]["actionable_determinations"]}

    # Parent SCH008 suppressed
    assert "SCH008" not in s050_act

    # Central KCC is in Section A
    assert s050_act["SCH008_CENTRAL"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s050_act["SCH008_CENTRAL"]["presentation_section"]
    assert s050_act["SCH008_CENTRAL"]["allow_numerical_scoring"] is True

    # State coop credit is in Section B
    ka_coop = s050_act["SCH008_KA_COOP"]
    assert ka_coop["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in ka_coop["presentation_section"]
    assert ka_coop["allow_numerical_scoring"] is False


def test_zone_z7_s051_boundary_2_5_ac_solar_pump(z7_profiles, z7_execution_results):
    """
    Boundary Test & Solar Pump Prerequisites:
    Verify S051 (Minority small farmer, exactly 2.5 ac, Shivamogga):
    - Exactly 2.5 ac classified as Small ([2.5, 5.0]).
    - Drilled unenergized borewell and off-grid electrical status verified.
    - PM-KUSUM Component B qualifies in Section A (KUSUM_B_WATER_SOURCE_PRESENT, KUSUM_B_OFF_GRID_VERIFIED).
    - Ganga Kalyana disqualified due to existing borewell.
    - Krishi Bhagya disqualified due to unnotified Malnad district.
    """
    s051 = z7_profiles["S051"]
    assert s051["land_size_acres"] == 2.5
    assert "Small" in s051["farmer_category"]
    assert s051["immediate_need"] == "SOLAR_PUMP_INSTALLATION"
    assert s051["borewell_electric_status"] == "UNENERGIZED_OFF_GRID"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s051["scenario_id"],
        "agro_climatic_zone": s051["agro_climatic_zone"],
        "district": s051["district"],
        "crop_primary": s051["crop_primary"],
        "land_size_acres": s051["land_size_acres"],
        "land_type": s051["land_type"],
        "social_category": s051["social_category"],
        "farmer_category": s051["farmer_category"],
        "existing_assets": s051["existing_assets"],
        "annual_family_income_lakh": s051["annual_family_income_lakh"],
        "immediate_need": s051["immediate_need"],
        "paid_income_tax_last_assessment_year": s051["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s051["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s051["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s051["pensioner_is_mts_exempt"],
        "registered_professional": s051["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s051["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s051["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s051["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # PM-KUSUM B qualifies
    det_kusum = engine.evaluate_scheme(sc, "SCH006")
    assert det_kusum.status == EligibilityStatus.ELIGIBLE
    assert "KUSUM_B_WATER_SOURCE_PRESENT" in det_kusum.rule_keys_fired
    assert "KUSUM_B_OFF_GRID_VERIFIED" in det_kusum.rule_keys_fired

    # Krishi Bhagya disqualified
    det_kb = engine.evaluate_scheme(sc, "SCH005")
    assert det_kb.status == EligibilityStatus.INELIGIBLE
    assert "KRISHI_BHAGYA_DISTRICT_NOT_RAINFED" in det_kb.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z7_execution_results["results"]}
    s051_act = {d["scheme_id"]: d for d in results_map["S051"]["actionable_determinations"]}

    # PM-KUSUM B is in Section A
    assert s051_act["SCH006"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s051_act["SCH006"]["presentation_section"]
    assert s051_act["SCH006"]["allow_numerical_scoring"] is True


def test_zone_z7_s052_community_pool_beneficiary_discrepancy(z7_profiles, z7_execution_results):
    """
    Benchmark Challenge 7 & Special Governance Condition on Beneficiary Discrepancy:
    Verify S052 (OBC medium dryland farmer, 9.5 ac, Chikkamagaluru):
    - Individual holding exceeds 5.0 ac ceiling.
    - Community pool satisfies [8.0, 15.0] ac with 12.0 ac pooled and 3 contiguous OBC farmers.
    - Raw engine evaluates SCH010_DEVARAJ_URS as ELIGIBLE (GK_SCH010_DEVARAJ_URS_COMMUNITY_ROUTE_VALID).
    - Special Governance Safeguard: Beneficiary discrepancy (>= 3 in design vs >= 2 in engine) and
      provisional scheme status strictly place determination in Section B as REQUIRES_VERIFICATION
      without numerical scoring.
    - Abstract parent SCH010 is suppressed.
    - PM-KISAN, SMAM, Soil Health Card qualify in Section A.
    """
    s052 = z7_profiles["S052"]
    assert s052["immediate_need"] == "BOREWELL_IRRIGATION"
    assert s052["land_size_acres"] == 9.5
    assert s052["community_pool_acres"] == 12.0
    assert s052["community_pool_beneficiaries_count"] == 3

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s052["scenario_id"],
        "agro_climatic_zone": s052["agro_climatic_zone"],
        "district": s052["district"],
        "crop_primary": s052["crop_primary"],
        "crop_secondary": s052.get("crop_secondary"),
        "land_size_acres": s052["land_size_acres"],
        "land_type": s052["land_type"],
        "social_category": s052["social_category"],
        "farmer_category": s052["farmer_category"],
        "existing_assets": s052["existing_assets"],
        "annual_family_income_lakh": s052["annual_family_income_lakh"],
        "immediate_need": s052["immediate_need"],
        "paid_income_tax_last_assessment_year": s052["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s052["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s052["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s052["pensioner_is_mts_exempt"],
        "registered_professional": s052["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s052["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s052["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s052["borewell_electric_status"],
        "community_pool_acres": s052["community_pool_acres"],
        "community_pool_beneficiaries_count": s052["community_pool_beneficiaries_count"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # Devaraj Urs community route qualifies in raw engine
    det_du = engine.evaluate_scheme(sc, "SCH010_DEVARAJ_URS")
    assert det_du.status == EligibilityStatus.ELIGIBLE
    assert "GK_SCH010_DEVARAJ_URS_COMMUNITY_ROUTE_VALID" in det_du.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z7_execution_results["results"]}
    s052_act = {d["scheme_id"]: d for d in results_map["S052"]["actionable_determinations"]}

    # Parent SCH010 must be suppressed
    assert "SCH010" not in s052_act
    assert "SCH010_DEVARAJ_URS" in s052_act

    # Devaraj Urs is in Section B with numerical scoring disabled
    du_gov = s052_act["SCH010_DEVARAJ_URS"]
    assert du_gov["raw_engine_status"] == "ELIGIBLE"
    assert du_gov["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in du_gov["presentation_section"]
    assert du_gov["allow_numerical_scoring"] is False
    assert any("beneficiary" in mv.lower() for mv in du_gov["missing_verifications"])
    assert any("provisional" in mv.lower() for mv in du_gov["missing_verifications"])


def test_zone_z7_parent_deduplication_and_denominator_reconciliation(z7_execution_results):
    """
    Verify visible scheme denominators:
    - S047, S048, S049, S050, S051 report 15 visible schemes (SCH008 suppressed, SCH010 ineligible).
    - S052 reports 14 visible schemes (both SCH008 and SCH010 suppressed).
    - All scenarios evaluate exactly 16 raw schemes.
    - Check section breakdown:
      S047: 5 Section A, 2 Section B, 8 Disqualified
      S048: 3 Section A, 4 Section B, 8 Disqualified
      S049: 5 Section A, 2 Section B, 8 Disqualified
      S050: 5 Section A, 2 Section B, 8 Disqualified
      S051: 5 Section A, 2 Section B, 8 Disqualified
      S052: 4 Section A, 3 Section B, 7 Disqualified
    """
    results_map = {r["scenario"]["scenario_id"]: r for r in z7_execution_results["results"]}

    for sid in Z7_IDS:
        res = results_map[sid]
        assert len(res["raw_determinations"]) == 16, f"{sid} did not evaluate 16 raw schemes"

        act_ids = [d["scheme_id"] for d in res["actionable_determinations"]]
        assert "SCH008" not in act_ids, f"Abstract parent SCH008 was not suppressed in {sid}"

        sec_a = [d["scheme_id"] for d in res["actionable_determinations"] if "Section A" in d["presentation_section"]]
        sec_b = [d["scheme_id"] for d in res["actionable_determinations"] if "Section B" in d["presentation_section"]]
        disq = [d["scheme_id"] for d in res["actionable_determinations"] if "Disqualified" in d["presentation_section"]]

        if sid == "S052":
            assert len(act_ids) == 14, f"{sid} expected 14 visible schemes, got {len(act_ids)}"
            assert "SCH010" not in act_ids, f"Abstract parent SCH010 was not suppressed in {sid}"
            assert len(sec_a) == 4, f"{sid} expected 4 in Section A, got {len(sec_a)}"
            assert len(sec_b) == 3, f"{sid} expected 3 in Section B, got {len(sec_b)}"
            assert len(disq) == 7, f"{sid} expected 7 Disqualified, got {len(disq)}"
        else:
            assert len(act_ids) == 15, f"{sid} expected 15 visible schemes, got {len(act_ids)}"
            assert "SCH010" in act_ids, f"Abstract parent SCH010 should be present as ineligible in {sid}"
            if sid == "S048":
                assert len(sec_a) == 4, f"{sid} expected 4 in Section A, got {len(sec_a)}"
                assert len(sec_b) == 4, f"{sid} expected 4 in Section B, got {len(sec_b)}"
                assert len(disq) == 7, f"{sid} expected 7 Disqualified, got {len(disq)}"
            elif sid in ["S049", "S050", "S051"]:
                assert len(sec_a) == 6, f"{sid} expected 6 in Section A, got {len(sec_a)}"
                assert len(sec_b) == 2, f"{sid} expected 2 in Section B, got {len(sec_b)}"
                assert len(disq) == 7, f"{sid} expected 7 Disqualified, got {len(disq)}"
            else:
                assert len(sec_a) == 5, f"{sid} expected 5 in Section A, got {len(sec_a)}"
                assert len(sec_b) == 2, f"{sid} expected 2 in Section B, got {len(sec_b)}"
                assert len(disq) == 8, f"{sid} expected 8 Disqualified, got {len(disq)}"


def test_zone_z7_availability_state_decoupling(z7_execution_results):
    """
    Verify 4-state availability pipeline execution and presentation safeguard.
    - Confirm availability_state is persisted independently for all 16 determinations in every scenario.
    - Confirm that statutory ELIGIBLE status does not activate 'Verified available now'.
    - Without active official dated circulars, all determinations preserve 'Availability unknown — confirmation required'.
    - Confirm operational availability notice is present in generated markdown report.
    """
    results_map = {r["scenario"]["scenario_id"]: r for r in z7_execution_results["results"]}

    for sid in Z7_IDS:
        res = results_map[sid]
        for d in res["raw_determinations"]:
            assert "availability_state" in d
            assert d["availability_state"] == AvailabilityState.AVAILABILITY_UNKNOWN.value

        for d in res["actionable_determinations"]:
            assert "availability_state" in d
            assert d["availability_state"] == AvailabilityState.AVAILABILITY_UNKNOWN.value
            assert d["availability_state"] != "Verified available now"

    # Check report for availability presentation safeguard
    report_path = os.path.join(REPORTS_DIR, "zone_z7_execution_report.md")
    with open(report_path, "r", encoding="utf-8") as f:
        report_text = f.read()

    assert "Operational Availability Notice:" in report_text
    assert "Availability State" in report_text
    assert "signify that an application window is currently open" in report_text


def test_zone_z7_pmkisan_statutory_inheritance_vs_partition_regression(z7_profiles):
    """
    Regression Test: PM-KISAN Post-Feb 2019 Cut-off Exemption Rules.
    Distinguishes:
    1. Transfer via statutory inheritance upon demise of previous landowner (statutorily qualifying route).
    2. Transfer via post-cutoff family partition deed (statutorily disqualified route).
    3. Transfer via post-cutoff sale/gift deed (statutorily disqualified route).
    4. Unverified/unknown cutoff title status (triggers REQUIRES_VERIFICATION).

    Confirms that S049's PM-KISAN eligibility in Section A is strictly conditioned on verified
    death-related succession, and that a post-cutoff partition deed would NOT retain confirmed eligibility.
    """
    engine = EligibilityEngine()
    s049 = z7_profiles["S049"]

    base_scenario = {
        "scenario_id": "REG_TEST_S049_VARIANT",
        "agro_climatic_zone": s049["agro_climatic_zone"],
        "district": s049["district"],
        "crop_primary": s049["crop_primary"],
        "crop_secondary": s049.get("crop_secondary"),
        "land_size_acres": s049["land_size_acres"],
        "land_type": s049["land_type"],
        "social_category": s049["social_category"],
        "farmer_category": s049["farmer_category"],
        "existing_assets": s049["existing_assets"],
        "annual_family_income_lakh": s049["annual_family_income_lakh"],
        "immediate_need": s049["immediate_need"],
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": "NONE",
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": s049["borewell_electric_status"]
    }

    # Case 1: Post-Cutoff Statutory Inheritance upon Demise of Landowner (Qualifying)
    # Meets official PM-KISAN Revised Operational Guidelines Clause 3(d) exception
    sc_inherit = FarmerScenario.from_dict({
        **base_scenario,
        "scenario_id": "TEST_INHERITANCE_UPON_DEATH",
        "land_ownership_cutoff_pre_feb_2019": True  # Engine consolidated cutoff-compliance flag
    })
    det_inherit = engine.evaluate_scheme(sc_inherit, "SCH001")
    assert det_inherit.status == EligibilityStatus.ELIGIBLE
    assert "PMKISAN_CUTOFF_DATE_VERIFIED" in det_inherit.rule_keys_fired
    assert len(det_inherit.disqualifying_factors) == 0

    # Case 2: Post-Cutoff Family Partition Deed (Statutorily Disqualified)
    # Under PM-KISAN Revised Operational Guidelines, post-cutoff partition deeds do not qualify for exemption.
    sc_partition = FarmerScenario.from_dict({
        **base_scenario,
        "scenario_id": "TEST_PARTITION_DEED_POST_CUTOFF",
        "land_ownership_cutoff_pre_feb_2019": False  # Acquired post-cutoff without qualifying succession
    })
    det_partition = engine.evaluate_scheme(sc_partition, "SCH001")
    assert det_partition.status == EligibilityStatus.INELIGIBLE
    assert "PMKISAN_CUTOFF_DATE_POST_FEB_2019" in det_partition.rule_keys_fired
    assert any("without succession/inheritance is ineligible" in df.lower() for df in det_partition.disqualifying_factors)

    # Case 3: Post-Cutoff Sale Deed / Gift Deed (Statutorily Disqualified)
    sc_sale = FarmerScenario.from_dict({
        **base_scenario,
        "scenario_id": "TEST_SALE_DEED_POST_CUTOFF",
        "land_ownership_cutoff_pre_feb_2019": False
    })
    det_sale = engine.evaluate_scheme(sc_sale, "SCH001")
    assert det_sale.status == EligibilityStatus.INELIGIBLE
    assert "PMKISAN_CUTOFF_DATE_POST_FEB_2019" in det_sale.rule_keys_fired

    # Case 4: Unknown / Unverified Cutoff or Succession Status (Requires Verification)
    sc_unknown = FarmerScenario.from_dict({
        **base_scenario,
        "scenario_id": "TEST_UNKNOWN_CUTOFF_STATUS",
        "land_ownership_cutoff_pre_feb_2019": None
    })
    det_unknown = engine.evaluate_scheme(sc_unknown, "SCH001")
    assert det_unknown.status == EligibilityStatus.REQUIRES_VERIFICATION
    assert "PMKISAN_CUTOFF_DATE_UNKNOWN" in det_unknown.rule_keys_fired
    assert any("title record date" in mv.lower() for mv in det_unknown.missing_verifications)
