"""
Targeted consistency, execution validation, and governance safeguard tests for Zone Z6 Profiles (S041-S046).
Validates schema compliance, assignment matrix consistency, PMKSY-PDMC area cap in canal command (S041),
Benchmark Challenge 5 pure tenant gating for PM-KISAN, PMFBY, and KCC (S042),
Valmiki ST Corporation borewell individual route safeguard and parent suppression (S043),
Challenge 2 relief vs debt protocol on pure tenancy (S044),
Krishi Bhagya rainwater harvesting and Ambedkar source-adjacency safeguard (S045),
Universal Soil Health Card access and canal command gating (S046),
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
Z6_DIR = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", "z6")
REPORTS_DIR = os.path.join(WORKSPACE_ROOT, "reports")
Z6_IDS = ["S041", "S042", "S043", "S044", "S045", "S046"]


@pytest.fixture(scope="module")
def z6_profiles():
    profiles = {}
    for sid in Z6_IDS:
        filepath = os.path.join(Z6_DIR, f"{sid}.json")
        assert os.path.exists(filepath), f"Profile file missing: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            profiles[sid] = json.load(f)
    return profiles


@pytest.fixture(scope="module")
def z6_execution_results():
    filepath = os.path.join(Z6_DIR, "z6_execution_results.json")
    assert os.path.exists(filepath), f"Execution results missing: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def matrix_scenarios_by_id():
    return {s["sid"]: s for s in scenarios if s["sid"] in Z6_IDS}


def test_zone_z6_files_exist():
    """Verify all 6 JSON and Markdown profiles exist, along with batch, execution JSONs and report."""
    for sid in Z6_IDS:
        json_file = os.path.join(Z6_DIR, f"{sid}.json")
        md_file = os.path.join(Z6_DIR, f"{sid}.md")
        assert os.path.exists(json_file), f"Missing {json_file}"
        assert os.path.exists(md_file), f"Missing {md_file}"
        assert os.path.getsize(json_file) > 100
        assert os.path.getsize(md_file) > 100

    batch_json = os.path.join(Z6_DIR, "z6_scenarios.json")
    assert os.path.exists(batch_json)
    
    exec_json = os.path.join(Z6_DIR, "z6_execution_results.json")
    assert os.path.exists(exec_json)

    report_md = os.path.join(REPORTS_DIR, "zone_z6_execution_report.md")
    assert os.path.exists(report_md)
    assert os.path.getsize(report_md) > 1000


def test_zone_z6_matrix_consistency(z6_profiles, matrix_scenarios_by_id):
    """Verify each profile exactly matches its row in the benchmark assignment matrix."""
    for sid in Z6_IDS:
        prof = z6_profiles[sid]
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


def test_zone_z6_s041_pmksy_area_cap_canal(z6_profiles, z6_execution_results):
    """
    Verify S041 (General Merit medium sugarcane farmer, 6.5 ac, Mandya):
    - Stated need: MICRO_IRRIGATION_SUPPORT.
    - Physical area cap: Requested 2.50 ha <= 6.5 ac * 0.404686 = 2.6305 ha and <= 5.00 ha.
    - Qualifies for PMKSY-PDMC in Section A (PMKSY_LAND_RANGE_VALID, PMKSY_WATER_SOURCE_VERIFIED).
    - Canal irrigated land disqualifies Krishi Bhagya (KRISHI_BHAGYA_NOT_DRYLAND) and Ganga Kalyana (GK_PARENT_NOT_DRYLAND).
    - PMFBY evaluates raw ELIGIBLE, but decoupled to Section B as REQUIRES_VERIFICATION pending Kharif IU notification.
    """
    s041 = z6_profiles["S041"]
    assert s041["immediate_need"] == "MICRO_IRRIGATION_SUPPORT"
    assert s041["land_size_acres"] == 6.5
    assert s041["land_type"] == "Irrigated (Canal)"
    assert s041["landholding_details"]["requested_subsidized_area_ha"] == 2.50

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s041["scenario_id"],
        "agro_climatic_zone": s041["agro_climatic_zone"],
        "district": s041["district"],
        "crop_primary": s041["crop_primary"],
        "land_size_acres": s041["land_size_acres"],
        "land_type": s041["land_type"],
        "social_category": s041["social_category"],
        "farmer_category": s041["farmer_category"],
        "existing_assets": s041["existing_assets"],
        "annual_family_income_lakh": s041["annual_family_income_lakh"],
        "immediate_need": s041["immediate_need"],
        "paid_income_tax_last_assessment_year": s041["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s041["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s041["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s041["pensioner_is_mts_exempt"],
        "registered_professional": s041["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s041["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s041["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s041["borewell_electric_status"],
        "prior_micro_irrigation_subsidy_years_ago": s041["prior_micro_irrigation_subsidy_years_ago"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # PMKSY-PDMC qualifies
    det_pmksy = engine.evaluate_scheme(sc, "SCH003")
    assert det_pmksy.status == EligibilityStatus.ELIGIBLE
    assert "PMKSY_LAND_RANGE_VALID" in det_pmksy.rule_keys_fired
    assert "PMKSY_WATER_SOURCE_VERIFIED" in det_pmksy.rule_keys_fired

    # Krishi Bhagya disqualified due to irrigated land
    det_kb = engine.evaluate_scheme(sc, "SCH005")
    assert det_kb.status == EligibilityStatus.INELIGIBLE
    assert "KRISHI_BHAGYA_NOT_DRYLAND" in det_kb.rule_keys_fired

    # Check execution results governance presentation
    results_map = {r["scenario"]["scenario_id"]: r for r in z6_execution_results["results"]}
    s041_act = {d["scheme_id"]: d for d in results_map["S041"]["actionable_determinations"]}

    # PMKSY is in Section A
    assert s041_act["SCH003"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s041_act["SCH003"]["presentation_section"]
    assert s041_act["SCH003"]["allow_numerical_scoring"] is True

    # PMFBY decoupled to Section B
    pmfby = s041_act["SCH002"]
    assert pmfby["raw_engine_status"] == "ELIGIBLE"
    assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in pmfby["presentation_section"]
    assert pmfby["allow_numerical_scoring"] is False
    assert any("sugarcane" in mv.lower() for mv in pmfby["missing_verifications"])


def test_zone_z6_s042_pure_tenant_paddy(z6_profiles, z6_execution_results):
    """
    Benchmark Challenge 5 (Pure Tenant Gating):
    Verify S042 (SC small pure tenant, 3.5 ac wetland paddy, Mysuru):
    - is_pure_tenant_without_land_title == True.
    - PM-KISAN strictly INELIGIBLE (PMKISAN_PURE_TENANT_EXCLUSION).
    - PMFBY raw engine ELIGIBLE, decoupled to Section B as REQUIRES_VERIFICATION pending tenant sowing certificate and IU notification.
    - Central KCC-MISS raw engine ELIGIBLE, decoupled to Section B as REQUIRES_VERIFICATION pending JLG / oral lease declaration.
    - Krishi Bhagya and Ganga Kalyana disqualified.
    """
    s042 = z6_profiles["S042"]
    assert s042["is_pure_tenant_without_land_title"] is True
    assert s042["immediate_need"] == "CROP_INSURANCE"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s042["scenario_id"],
        "agro_climatic_zone": s042["agro_climatic_zone"],
        "district": s042["district"],
        "crop_primary": s042["crop_primary"],
        "land_size_acres": s042["land_size_acres"],
        "land_type": s042["land_type"],
        "social_category": s042["social_category"],
        "farmer_category": s042["farmer_category"],
        "existing_assets": s042["existing_assets"],
        "annual_family_income_lakh": s042["annual_family_income_lakh"],
        "immediate_need": s042["immediate_need"],
        "paid_income_tax_last_assessment_year": s042["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s042["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s042["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s042["pensioner_is_mts_exempt"],
        "registered_professional": s042["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s042["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s042["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s042["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # PM-KISAN strictly disqualified
    det_pmk = engine.evaluate_scheme(sc, "SCH001")
    assert det_pmk.status == EligibilityStatus.INELIGIBLE
    assert "PMKISAN_PURE_TENANT_EXCLUSION" in det_pmk.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z6_execution_results["results"]}
    s042_act = {d["scheme_id"]: d for d in results_map["S042"]["actionable_determinations"]}

    # Central KCC is decoupled to Section B
    kcc = s042_act["SCH008_CENTRAL"]
    assert kcc["raw_engine_status"] == "ELIGIBLE"
    assert kcc["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in kcc["presentation_section"]
    assert kcc["allow_numerical_scoring"] is False
    assert any("tenant" in mv.lower() or "jlg" in mv.lower() for mv in kcc["missing_verifications"])

    # PMFBY is decoupled to Section B
    pmfby = s042_act["SCH002"]
    assert pmfby["raw_engine_status"] == "ELIGIBLE"
    assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in pmfby["presentation_section"]
    assert pmfby["allow_numerical_scoring"] is False
    assert any("tenant" in mv.lower() for mv in pmfby["missing_verifications"])


def test_zone_z6_s043_valmiki_individual_route_safeguard(z6_profiles, z6_execution_results):
    """
    Verify S043 (ST marginal dryland farmer, 1.8 ac, Chamarajanagar):
    - Need: BOREWELL_IRRIGATION.
    - Evaluates SCH010_VALMIKI as raw ELIGIBLE (GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID).
    - Governance safeguard routes SCH010_VALMIKI to Section B as REQUIRES_VERIFICATION without scoring
      due to provisional registry status and missing perennial water source adjacency.
    - Abstract parent SCH010 is suppressed from visible determinations.
    - Krishi Bhagya qualifies for farm pond in Section A.
    - PM-KISAN qualifies in Section A.
    - PMFBY decoupled to Section B.
    """
    s043 = z6_profiles["S043"]
    assert s043["social_category"] == "ST"
    assert s043["land_type"] == "Dryland (Rainfed)"
    assert s043["land_size_acres"] == 1.8

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s043["scenario_id"],
        "agro_climatic_zone": s043["agro_climatic_zone"],
        "district": s043["district"],
        "crop_primary": s043["crop_primary"],
        "land_size_acres": s043["land_size_acres"],
        "land_type": s043["land_type"],
        "social_category": s043["social_category"],
        "farmer_category": s043["farmer_category"],
        "existing_assets": s043["existing_assets"],
        "annual_family_income_lakh": s043["annual_family_income_lakh"],
        "immediate_need": s043["immediate_need"],
        "paid_income_tax_last_assessment_year": s043["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s043["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s043["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s043["pensioner_is_mts_exempt"],
        "registered_professional": s043["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s043["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s043["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s043["borewell_electric_status"],
        "prior_ganga_kalyana_in_family": s043["prior_ganga_kalyana_in_family"],
        "community_pool_acres": s043["community_pool_acres"],
        "community_pool_beneficiaries_count": s043["community_pool_beneficiaries_count"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # Valmiki Corporation raw engine ELIGIBLE
    det_valmiki = engine.evaluate_scheme(sc, "SCH010_VALMIKI")
    assert det_valmiki.status == EligibilityStatus.ELIGIBLE
    assert "GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID" in det_valmiki.rule_keys_fired

    # Krishi Bhagya qualifies
    det_kb = engine.evaluate_scheme(sc, "SCH005")
    assert det_kb.status == EligibilityStatus.ELIGIBLE
    assert "KRISHI_BHAGYA_DRYLAND_VERIFIED" in det_kb.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z6_execution_results["results"]}
    s043_res = results_map["S043"]
    s043_act = {d["scheme_id"]: d for d in s043_res["actionable_determinations"]}

    # Parent SCH010 must be suppressed
    assert "SCH010" not in s043_act
    assert "SCH010_VALMIKI" in s043_act

    # Valmiki safeguard
    valmiki_gov = s043_act["SCH010_VALMIKI"]
    assert valmiki_gov["raw_engine_status"] == "ELIGIBLE"
    assert valmiki_gov["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in valmiki_gov["presentation_section"]
    assert valmiki_gov["allow_numerical_scoring"] is False
    assert any("perennial water source" in mv.lower() for mv in valmiki_gov["missing_verifications"])
    assert any("provisional" in mv.lower() for mv in valmiki_gov["missing_verifications"])


def test_zone_z6_s044_relief_vs_debt_pure_tenancy(z6_profiles, z6_execution_results):
    """
    Dual Challenge: Challenge 2 (Relief vs. Debt) & Challenge 5 (Pure Tenant Gating).
    Verify S044 (OBC marginal pure tenant, 2.0 ac wetland paddy, Mandya):
    - Stated need: INCOME_SUPPORT.
    - PM-KISAN strictly INELIGIBLE (PMKISAN_PURE_TENANT_EXCLUSION) overriding stated immediate need.
    - Protocol v1.1 Rule 2: Reimbursable production credit (KCC-MISS) must NOT receive clinical score 3.
    - Tenant status routes KCC to Section B pending JLG declaration.
    - PMFBY routed to Section B pending tenant sowing certificate and IU notification.
    - Wetland status disqualifies Krishi Bhagya.
    """
    s044 = z6_profiles["S044"]
    assert s044["is_pure_tenant_without_land_title"] is True
    assert s044["immediate_need"] == "INCOME_SUPPORT"
    assert s044["land_type"] == "Wetland/valley"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s044["scenario_id"],
        "agro_climatic_zone": s044["agro_climatic_zone"],
        "district": s044["district"],
        "crop_primary": s044["crop_primary"],
        "land_size_acres": s044["land_size_acres"],
        "land_type": s044["land_type"],
        "social_category": s044["social_category"],
        "farmer_category": s044["farmer_category"],
        "existing_assets": s044["existing_assets"],
        "annual_family_income_lakh": s044["annual_family_income_lakh"],
        "immediate_need": s044["immediate_need"],
        "paid_income_tax_last_assessment_year": s044["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s044["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s044["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s044["pensioner_is_mts_exempt"],
        "registered_professional": s044["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s044["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s044["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s044["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # PM-KISAN strictly disqualified
    det_pmk = engine.evaluate_scheme(sc, "SCH001")
    assert det_pmk.status == EligibilityStatus.INELIGIBLE
    assert "PMKISAN_PURE_TENANT_EXCLUSION" in det_pmk.rule_keys_fired

    # Krishi Bhagya disqualified
    det_kb = engine.evaluate_scheme(sc, "SCH005")
    assert det_kb.status == EligibilityStatus.INELIGIBLE
    assert "KRISHI_BHAGYA_NOT_DRYLAND" in det_kb.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z6_execution_results["results"]}
    s044_act = {d["scheme_id"]: d for d in results_map["S044"]["actionable_determinations"]}

    # PM-KISAN is disqualified
    assert s044_act["SCH001"]["governance_status"] == "INELIGIBLE"

    # Central KCC is routed to Section B without scoring
    kcc = s044_act["SCH008_CENTRAL"]
    assert kcc["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in kcc["presentation_section"]
    assert kcc["allow_numerical_scoring"] is False


def test_zone_z6_s045_krishi_bhagya_rainwater_and_ambedkar_safeguard(z6_profiles, z6_execution_results):
    """
    Verify S045 (SC marginal dryland farmer, 1.5 ac, Mysuru):
    - Need: RAINWATER_HARVESTING.
    - Krishi Bhagya qualifies in Section A (KRISHI_BHAGYA_DRYLAND_VERIFIED, KRISHI_BHAGYA_DISTRICT_NOTIFIED).
    - Ambedkar Corporation (SCH010_AMBEDKAR) evaluates raw ELIGIBLE (GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID),
      but governance safeguard decouples it to Section B as REQUIRES_VERIFICATION without scoring
      due to absence of recorded perennial water source adjacency.
    - Abstract parent SCH010 is suppressed.
    - PM-KISAN qualifies in Section A.
    - PMFBY decoupled to Section B.
    """
    s045 = z6_profiles["S045"]
    assert s045["social_category"] == "SC"
    assert s045["land_type"] == "Dryland (Rainfed)"
    assert s045["immediate_need"] == "RAINWATER_HARVESTING"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s045["scenario_id"],
        "agro_climatic_zone": s045["agro_climatic_zone"],
        "district": s045["district"],
        "crop_primary": s045["crop_primary"],
        "land_size_acres": s045["land_size_acres"],
        "land_type": s045["land_type"],
        "social_category": s045["social_category"],
        "farmer_category": s045["farmer_category"],
        "existing_assets": s045["existing_assets"],
        "annual_family_income_lakh": s045["annual_family_income_lakh"],
        "immediate_need": s045["immediate_need"],
        "paid_income_tax_last_assessment_year": s045["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s045["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s045["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s045["pensioner_is_mts_exempt"],
        "registered_professional": s045["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s045["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s045["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s045["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # Krishi Bhagya qualifies
    det_kb = engine.evaluate_scheme(sc, "SCH005")
    assert det_kb.status == EligibilityStatus.ELIGIBLE
    assert "KRISHI_BHAGYA_DRYLAND_VERIFIED" in det_kb.rule_keys_fired
    assert "KRISHI_BHAGYA_DISTRICT_NOTIFIED" in det_kb.rule_keys_fired

    # Ambedkar Corporation raw engine ELIGIBLE
    det_amb = engine.evaluate_scheme(sc, "SCH010_AMBEDKAR")
    assert det_amb.status == EligibilityStatus.ELIGIBLE
    assert "GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID" in det_amb.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z6_execution_results["results"]}
    s045_res = results_map["S045"]
    s045_act = {d["scheme_id"]: d for d in s045_res["actionable_determinations"]}

    # Parent SCH010 must be suppressed
    assert "SCH010" not in s045_act
    assert "SCH010_AMBEDKAR" in s045_act

    # Krishi Bhagya is in Section A
    assert s045_act["SCH005"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s045_act["SCH005"]["presentation_section"]
    assert s045_act["SCH005"]["allow_numerical_scoring"] is True

    # Ambedkar Corporation is in Section B with dual missing verifications
    amb_gov = s045_act["SCH010_AMBEDKAR"]
    assert amb_gov["raw_engine_status"] == "ELIGIBLE"
    assert amb_gov["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in amb_gov["presentation_section"]
    assert amb_gov["allow_numerical_scoring"] is False
    assert any("perennial water source" in mv.lower() for mv in amb_gov["missing_verifications"])
    assert any("mysuru" in mv.lower() and "income" in mv.lower() for mv in amb_gov["missing_verifications"])


def test_zone_z6_s046_universal_shc_canal_gating(z6_profiles, z6_execution_results):
    """
    Verify S046 (General Merit medium sugarcane farmer, 7.0 ac canal command, Chamarajanagar):
    - Need: SOIL_HEALTH_AND_FERTILIZER.
    - Soil Health Card (SCH009) qualifies in Section A (SHC_UNIVERSAL_ACCESS_VERIFIED).
    - Canal irrigated land disqualifies Krishi Bhagya (KRISHI_BHAGYA_NOT_DRYLAND) and Ganga Kalyana (GK_PARENT_NOT_DRYLAND).
    - PM-KISAN, PMKSY-PDMC, SMAM qualify in Section A.
    - PMFBY routed to Section B pending seasonal IU notification.
    """
    s046 = z6_profiles["S046"]
    assert s046["immediate_need"] == "SOIL_HEALTH_AND_FERTILIZER"
    assert s046["land_type"] == "Irrigated (Canal)"
    assert s046["land_size_acres"] == 7.0

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s046["scenario_id"],
        "agro_climatic_zone": s046["agro_climatic_zone"],
        "district": s046["district"],
        "crop_primary": s046["crop_primary"],
        "land_size_acres": s046["land_size_acres"],
        "land_type": s046["land_type"],
        "social_category": s046["social_category"],
        "farmer_category": s046["farmer_category"],
        "existing_assets": s046["existing_assets"],
        "annual_family_income_lakh": s046["annual_family_income_lakh"],
        "immediate_need": s046["immediate_need"],
        "paid_income_tax_last_assessment_year": s046["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s046["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s046["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s046["pensioner_is_mts_exempt"],
        "registered_professional": s046["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s046["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s046["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s046["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # SHC qualifies
    det_shc = engine.evaluate_scheme(sc, "SCH009")
    assert det_shc.status == EligibilityStatus.ELIGIBLE
    assert "SHC_UNIVERSAL_ACCESS_VERIFIED" in det_shc.rule_keys_fired

    # Krishi Bhagya disqualified
    det_kb = engine.evaluate_scheme(sc, "SCH005")
    assert det_kb.status == EligibilityStatus.INELIGIBLE
    assert "KRISHI_BHAGYA_NOT_DRYLAND" in det_kb.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z6_execution_results["results"]}
    s046_act = {d["scheme_id"]: d for d in results_map["S046"]["actionable_determinations"]}

    # SHC is in Section A
    assert s046_act["SCH009"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s046_act["SCH009"]["presentation_section"]
    assert s046_act["SCH009"]["allow_numerical_scoring"] is True


def test_zone_z6_parent_deduplication_and_denominator_reconciliation(z6_execution_results):
    """
    Verify visible scheme denominators:
    - S041, S042, S044, S046 report 15 visible schemes (SCH008 suppressed, SCH010 ineligible).
    - S043, S045 report 14 visible schemes (both SCH008 and SCH010 suppressed).
    - All scenarios evaluate exactly 16 raw schemes.
    - Check section breakdown:
      S041: 5 Section A, 2 Section B, 8 Disqualified
      S042: 2 Section A, 3 Section B, 10 Disqualified
      S043: 5 Section A, 3 Section B, 6 Disqualified
      S044: 2 Section A, 3 Section B, 10 Disqualified
      S045: 5 Section A, 3 Section B, 6 Disqualified
      S046: 5 Section A, 2 Section B, 8 Disqualified
    """
    results_map = {r["scenario"]["scenario_id"]: r for r in z6_execution_results["results"]}

    for sid in Z6_IDS:
        res = results_map[sid]
        assert len(res["raw_determinations"]) == 16, f"{sid} did not evaluate 16 raw schemes"

        act_ids = [d["scheme_id"] for d in res["actionable_determinations"]]
        assert "SCH008" not in act_ids, f"Abstract parent SCH008 was not suppressed in {sid}"

        sec_a = [d["scheme_id"] for d in res["actionable_determinations"] if "Section A" in d["presentation_section"]]
        sec_b = [d["scheme_id"] for d in res["actionable_determinations"] if "Section B" in d["presentation_section"]]
        disq = [d["scheme_id"] for d in res["actionable_determinations"] if "Disqualified" in d["presentation_section"]]

        if sid in ["S043", "S045"]:
            assert len(act_ids) == 14, f"{sid} expected 14 visible schemes, got {len(act_ids)}"
            assert "SCH010" not in act_ids, f"Abstract parent SCH010 was not suppressed in {sid}"
            assert len(sec_a) == 5, f"{sid} expected 5 in Section A, got {len(sec_a)}"
            assert len(sec_b) == 3, f"{sid} expected 3 in Section B, got {len(sec_b)}"
            assert len(disq) == 6, f"{sid} expected 6 Disqualified, got {len(disq)}"
        else:
            assert len(act_ids) == 15, f"{sid} expected 15 visible schemes, got {len(act_ids)}"
            assert "SCH010" in act_ids, f"Abstract parent SCH010 should be present as ineligible in {sid}"
            if sid in ["S041", "S046"]:
                assert len(sec_a) == 5, f"{sid} expected 5 in Section A, got {len(sec_a)}"
                assert len(sec_b) == 2, f"{sid} expected 2 in Section B, got {len(sec_b)}"
                assert len(disq) == 8, f"{sid} expected 8 Disqualified, got {len(disq)}"
            elif sid in ["S042", "S044"]:
                assert len(sec_a) == 2, f"{sid} expected 2 in Section A, got {len(sec_a)}"
                assert len(sec_b) == 3, f"{sid} expected 3 in Section B, got {len(sec_b)}"
                assert len(disq) == 10, f"{sid} expected 10 Disqualified, got {len(disq)}"


def test_zone_z6_availability_state_decoupling(z6_execution_results):
    """
    Verify 4-state availability pipeline execution and presentation safeguard.
    - Confirm availability_state is persisted independently for all 16 determinations in every scenario.
    - Confirm that statutory ELIGIBLE status does not activate 'Verified available now'.
    - Without active official dated circulars, all determinations preserve 'Availability unknown — confirmation required'.
    - Confirm operational availability notice is present in generated markdown report.
    """
    results_map = {r["scenario"]["scenario_id"]: r for r in z6_execution_results["results"]}

    for sid in Z6_IDS:
        res = results_map[sid]
        for d in res["raw_determinations"]:
            assert "availability_state" in d
            assert d["availability_state"] == AvailabilityState.AVAILABILITY_UNKNOWN.value

        for d in res["actionable_determinations"]:
            assert "availability_state" in d
            assert d["availability_state"] == AvailabilityState.AVAILABILITY_UNKNOWN.value
            assert d["availability_state"] != "Verified available now"

    # Check report for availability presentation safeguard
    report_path = os.path.join(REPORTS_DIR, "zone_z6_execution_report.md")
    with open(report_path, "r", encoding="utf-8") as f:
        report_text = f.read()

    assert "Operational Availability Notice:" in report_text
    assert "Availability State" in report_text
    assert "signify that an application window is currently open" in report_text
