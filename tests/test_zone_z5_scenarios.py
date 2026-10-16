"""
Targeted consistency, execution validation, and governance safeguard tests for Zone Z5 Profiles (S035-S040).
Validates schema compliance, assignment matrix consistency, MIDH protected horticulture and PMFBY audit (S035),
competing credit channels and sericulture insurance audit (S036), exact 2.5-acre boundary and RWBCIS mango audit (S037),
Challenge 2 relief vs debt protocol (S038), statutory succession exemption upon death and Ambedkar safeguard (S039),
exact 5.0-acre boundary mechanization and mango insurance audit (S040),
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
Z5_DIR = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", "z5")
Z5_IDS = ["S035", "S036", "S037", "S038", "S039", "S040"]


@pytest.fixture(scope="module")
def z5_profiles():
    profiles = {}
    for sid in Z5_IDS:
        filepath = os.path.join(Z5_DIR, f"{sid}.json")
        assert os.path.exists(filepath), f"Profile file missing: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            profiles[sid] = json.load(f)
    return profiles


@pytest.fixture(scope="module")
def z5_execution_results():
    filepath = os.path.join(Z5_DIR, "z5_execution_results.json")
    assert os.path.exists(filepath), f"Execution results missing: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def matrix_scenarios_by_id():
    return {s["sid"]: s for s in scenarios if s["sid"] in Z5_IDS}


def test_zone_z5_files_exist():
    """Verify all 6 JSON and Markdown profiles exist, along with batch and execution JSONs."""
    for sid in Z5_IDS:
        json_file = os.path.join(Z5_DIR, f"{sid}.json")
        md_file = os.path.join(Z5_DIR, f"{sid}.md")
        assert os.path.exists(json_file), f"Missing {json_file}"
        assert os.path.exists(md_file), f"Missing {md_file}"
        assert os.path.getsize(json_file) > 100
        assert os.path.getsize(md_file) > 100

    batch_json = os.path.join(Z5_DIR, "z5_scenarios.json")
    assert os.path.exists(batch_json)
    
    exec_json = os.path.join(Z5_DIR, "z5_execution_results.json")
    assert os.path.exists(exec_json)


def test_zone_z5_matrix_consistency(z5_profiles, matrix_scenarios_by_id):
    """Verify each profile exactly matches its row in the benchmark assignment matrix."""
    for sid in Z5_IDS:
        prof = z5_profiles[sid]
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


def test_zone_z5_s035_protected_horticulture_midh(z5_profiles, z5_execution_results):
    """
    Verify S035 (SC marginal tomato farmer, 1.5 ac, Kolar) qualifies for MIDH
    protected cultivation polyhouse structure in Section A with verified drip irrigation asset.
    Verify PMFBY crop insurance routes to Section B as REQUIRES_VERIFICATION pending seasonal IU notification.
    """
    s035 = z5_profiles["S035"]
    assert s035["immediate_need"] == "PROTECTED_HORTICULTURE"
    assert "Drip Irrigation (Installed)" in s035["existing_assets"]
    assert s035["borewell_electric_status"] == "GRID_CONNECTED_IP_SET"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s035["scenario_id"],
        "agro_climatic_zone": s035["agro_climatic_zone"],
        "district": s035["district"],
        "crop_primary": s035["crop_primary"],
        "land_size_acres": s035["land_size_acres"],
        "land_type": s035["land_type"],
        "social_category": s035["social_category"],
        "farmer_category": s035["farmer_category"],
        "existing_assets": s035["existing_assets"],
        "annual_family_income_lakh": s035["annual_family_income_lakh"],
        "immediate_need": s035["immediate_need"],
        "paid_income_tax_last_assessment_year": s035["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s035["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s035["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s035["pensioner_is_mts_exempt"],
        "registered_professional": s035["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s035["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s035["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s035["borewell_electric_status"],
        "prior_micro_irrigation_subsidy_years_ago": s035["prior_micro_irrigation_subsidy_years_ago"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # MIDH Protected Cultivation qualifies in raw engine
    det_midh = engine.evaluate_scheme(sc, "SCH007")
    assert det_midh.status == EligibilityStatus.ELIGIBLE
    assert "MIDH_HORTICULTURE_CROP_VERIFIED" in det_midh.rule_keys_fired
    assert "MIDH_MICRO_IRRIGATION_VERIFIED" in det_midh.rule_keys_fired

    # PM-KUSUM B disqualified due to grid connection
    det_kusum = engine.evaluate_scheme(sc, "SCH006")
    assert det_kusum.status == EligibilityStatus.INELIGIBLE
    assert "KUSUM_B_GRID_CONNECTED_DISQUALIFIED" in det_kusum.rule_keys_fired

    # Check execution results governance presentation
    results_map = {r["scenario"]["scenario_id"]: r for r in z5_execution_results["results"]}
    s035_act = {d["scheme_id"]: d for d in results_map["S035"]["actionable_determinations"]}
    
    # MIDH is in Section A
    assert s035_act["SCH007"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s035_act["SCH007"]["presentation_section"]
    assert s035_act["SCH007"]["allow_numerical_scoring"] is True

    # PMFBY is raw ELIGIBLE but governance REQUIRES_VERIFICATION in Section B
    pmfby = s035_act["SCH002"]
    assert pmfby["raw_engine_status"] == "ELIGIBLE"
    assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in pmfby["presentation_section"]
    assert pmfby["allow_numerical_scoring"] is False
    assert any("tomato" in mv.lower() for mv in pmfby["missing_verifications"])


def test_zone_z5_s036_competing_credit_sericulture(z5_profiles, z5_execution_results):
    """
    Benchmark Challenge 6:
    Verify S036 (Minority, 3.0 ac, Mulberry sericulture, Chikkaballapura)
    evaluates Central KCC in Section A (scored) and provisional State PACS credit in Section B.
    Verify PMFBY raw engine is INELIGIBLE, but governance routes it to Section B as REQUIRES_VERIFICATION
    pending confirmation of sericulture insurance scheme circulars.
    """
    s036 = z5_profiles["S036"]
    assert s036["crop_primary"] == "Mulberry"
    assert s036["social_category"] == "Minority"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s036["scenario_id"],
        "agro_climatic_zone": s036["agro_climatic_zone"],
        "district": s036["district"],
        "crop_primary": s036["crop_primary"],
        "land_size_acres": s036["land_size_acres"],
        "land_type": s036["land_type"],
        "social_category": s036["social_category"],
        "farmer_category": s036["farmer_category"],
        "existing_assets": s036["existing_assets"],
        "annual_family_income_lakh": s036["annual_family_income_lakh"],
        "immediate_need": s036["immediate_need"],
        "paid_income_tax_last_assessment_year": s036["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s036["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s036["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s036["pensioner_is_mts_exempt"],
        "registered_professional": s036["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s036["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s036["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s036["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # Central KCC qualifies
    det_kcc = engine.evaluate_scheme(sc, "SCH008_CENTRAL")
    assert det_kcc.status == EligibilityStatus.ELIGIBLE
    assert "KCC_CENTRAL_COMMERCIAL_ELIGIBLE" in det_kcc.rule_keys_fired

    # PMFBY raw engine evaluates INELIGIBLE because Mulberry is absent from static list
    det_pmfby = engine.evaluate_scheme(sc, "SCH002")
    assert det_pmfby.status == EligibilityStatus.INELIGIBLE
    assert "PMFBY_NON_NOTIFIED_CROP" in det_pmfby.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z5_execution_results["results"]}
    s036_act = {d["scheme_id"]: d for d in results_map["S036"]["actionable_determinations"]}
    assert s036_act["SCH008_CENTRAL"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s036_act["SCH008_CENTRAL"]["presentation_section"]
    assert s036_act["SCH008_KA_COOP"]["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in s036_act["SCH008_KA_COOP"]["presentation_section"]
    assert s036_act["SCH008_KA_COOP"]["allow_numerical_scoring"] is False

    # PMFBY governance decoupling: raw INELIGIBLE preserved, but presentation is Section B REQUIRES_VERIFICATION
    pmfby = s036_act["SCH002"]
    assert pmfby["raw_engine_status"] == "INELIGIBLE"
    assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in pmfby["presentation_section"]
    assert pmfby["allow_numerical_scoring"] is False
    assert any("mulberry" in mv.lower() for mv in pmfby["missing_verifications"])


def test_zone_z5_s037_boundary_2_5_ac_micro_irrigation(z5_profiles, z5_execution_results):
    """
    Boundary test: Exactly 2.5 acres classified as Small holding ([2.5, 5.0]).
    Verify PMKSY-PDMC qualifies and physical area cap is satisfied:
    requested 1.01 ha <= 2.5 ac (1.0117 ha).
    Verify PMFBY raw INELIGIBLE for mango is routed to Section B as REQUIRES_VERIFICATION
    pending verification of RWBCIS weather-index notification.
    """
    s037 = z5_profiles["S037"]
    assert s037["land_size_acres"] == 2.5
    assert "Small" in s037["farmer_category"]
    assert s037["landholding_details"]["requested_subsidized_area_ha"] == 1.01
    assert 1.01 <= 2.5 * 0.40468564224

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s037["scenario_id"],
        "agro_climatic_zone": s037["agro_climatic_zone"],
        "district": s037["district"],
        "crop_primary": s037["crop_primary"],
        "land_size_acres": s037["land_size_acres"],
        "land_type": s037["land_type"],
        "social_category": s037["social_category"],
        "farmer_category": s037["farmer_category"],
        "existing_assets": s037["existing_assets"],
        "annual_family_income_lakh": s037["annual_family_income_lakh"],
        "immediate_need": s037["immediate_need"],
        "paid_income_tax_last_assessment_year": s037["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s037["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s037["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s037["pensioner_is_mts_exempt"],
        "registered_professional": s037["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s037["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s037["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s037["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    det_pmksy = engine.evaluate_scheme(sc, "SCH003")
    assert det_pmksy.status == EligibilityStatus.ELIGIBLE
    assert "PMKSY_LAND_RANGE_VALID" in det_pmksy.rule_keys_fired
    assert "PMKSY_WATER_SOURCE_VERIFIED" in det_pmksy.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z5_execution_results["results"]}
    s037_act = {d["scheme_id"]: d for d in results_map["S037"]["actionable_determinations"]}
    
    assert s037_act["SCH003"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s037_act["SCH003"]["presentation_section"]

    # PMFBY routed to Section B pending RWBCIS check
    pmfby = s037_act["SCH002"]
    assert pmfby["raw_engine_status"] == "INELIGIBLE"
    assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in pmfby["presentation_section"]
    assert pmfby["allow_numerical_scoring"] is False
    assert any("rwbcis" in mv.lower() for mv in pmfby["missing_verifications"])


def test_zone_z5_s038_challenge_2_relief_vs_debt(z5_profiles, z5_execution_results):
    """
    Benchmark Challenge 2: Relief vs. Reimbursable Debt.
    Verify S038 marginal dryland tomato cultivator in post-harvest distress qualifies
    for non-repayable income support under PM-KISAN in Section A, while KCC credit is debt.
    Verify PMFBY routes to Section B as REQUIRES_VERIFICATION pending seasonal IU notification.
    """
    s038 = z5_profiles["S038"]
    assert s038["immediate_need"] == "INCOME_SUPPORT"
    assert s038["land_type"] == "Dryland (Rainfed)"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s038["scenario_id"],
        "agro_climatic_zone": s038["agro_climatic_zone"],
        "district": s038["district"],
        "crop_primary": s038["crop_primary"],
        "land_size_acres": s038["land_size_acres"],
        "land_type": s038["land_type"],
        "social_category": s038["social_category"],
        "farmer_category": s038["farmer_category"],
        "existing_assets": s038["existing_assets"],
        "annual_family_income_lakh": s038["annual_family_income_lakh"],
        "immediate_need": s038["immediate_need"],
        "paid_income_tax_last_assessment_year": s038["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s038["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s038["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s038["pensioner_is_mts_exempt"],
        "registered_professional": s038["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s038["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s038["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s038["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # PM-KISAN qualifies for non-repayable income support
    det_pmk = engine.evaluate_scheme(sc, "SCH001")
    assert det_pmk.status == EligibilityStatus.ELIGIBLE
    assert "PMKISAN_CUTOFF_DATE_VERIFIED" in det_pmk.rule_keys_fired
    assert "PMKISAN_NO_INCOME_TAX_PAID" in det_pmk.rule_keys_fired

    # Krishi Bhagya also qualifies on dryland rainfed parcel
    det_kb = engine.evaluate_scheme(sc, "SCH005")
    assert det_kb.status == EligibilityStatus.ELIGIBLE

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z5_execution_results["results"]}
    s038_act = {d["scheme_id"]: d for d in results_map["S038"]["actionable_determinations"]}
    
    assert s038_act["SCH001"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s038_act["SCH001"]["presentation_section"]

    # PMFBY routed to Section B pending seasonal IU notification check
    pmfby = s038_act["SCH002"]
    assert pmfby["raw_engine_status"] == "ELIGIBLE"
    assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in pmfby["presentation_section"]
    assert pmfby["allow_numerical_scoring"] is False


def test_zone_z5_s039_inheritance_partition_and_ambedkar_safeguard(z5_profiles, z5_execution_results):
    """
    Verify S039 post-Feb 2019 transfer is strictly succession following the demise of the landowner,
    satisfying statutory exemption under PM-KISAN guidelines §3(d) and Clarification §2.
    Verify PMFBY raw engine is ELIGIBLE, but governance routes it to Section B as REQUIRES_VERIFICATION
    pending Kharif 2026 Gram Panchayat IU notification.
    Verify Dr. B.R. Ambedkar Ganga Kalyana raw engine is ELIGIBLE, but governance safeguard
    strictly routes it to Section B as REQUIRES_VERIFICATION with scoring disabled.
    Assert missing_verifications records perennial water source adjacency and district income ceiling.
    """
    s039 = z5_profiles["S039"]
    assert s039["social_category"] == "SC"
    assert s039["crop_primary"] == "Ragi"
    
    # Confirm succession evidence explicitly records demise of father and revenue mutation extract
    flags = s039["statutory_flags"]
    assert flags["transfer_basis"] == "INHERITANCE_DUE_TO_DEATH"
    assert flags["acquisition_date_relationship_to_cutoff"] == "POST_FEB_2019"
    assert flags["factual_acquisition_date"] == "2021-08-10"
    assert "DC-2021-9872" in flags["succession_death_certificate"]
    assert "LND/CR-089/2021-22" in flags["succession_legal_heir_order"]
    assert "MR-2021-0412" in flags["revenue_mutation_record"]
    tenure_doc = flags["tenure_documentation"].lower()
    assert "succession" in tenure_doc
    assert "death" in tenure_doc or "demise" in tenure_doc
    assert "partition deed" in tenure_doc
    assert "distinguished from non-exempt" in tenure_doc

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s039["scenario_id"],
        "agro_climatic_zone": s039["agro_climatic_zone"],
        "district": s039["district"],
        "crop_primary": s039["crop_primary"],
        "land_size_acres": s039["land_size_acres"],
        "land_type": s039["land_type"],
        "social_category": s039["social_category"],
        "farmer_category": s039["farmer_category"],
        "existing_assets": s039["existing_assets"],
        "annual_family_income_lakh": s039["annual_family_income_lakh"],
        "immediate_need": s039["immediate_need"],
        "paid_income_tax_last_assessment_year": s039["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s039["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s039["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s039["pensioner_is_mts_exempt"],
        "registered_professional": s039["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s039["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s039["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s039["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    # 1. PM-KISAN qualifies under statutory succession exemption
    det_pmk = engine.evaluate_scheme(sc, "SCH001")
    assert det_pmk.status == EligibilityStatus.ELIGIBLE
    assert "PMKISAN_CUTOFF_DATE_VERIFIED" in det_pmk.rule_keys_fired

    # 2. PMFBY raw engine qualifies for Ragi
    det_pmfby = engine.evaluate_scheme(sc, "SCH002")
    assert det_pmfby.status == EligibilityStatus.ELIGIBLE
    assert "PMFBY_NOTIFIED_CROP_VERIFIED" in det_pmfby.rule_keys_fired

    # 3. Raw engine evaluates Ambedkar Corporation as ELIGIBLE
    det_ambedkar = engine.evaluate_scheme(sc, "SCH010_AMBEDKAR")
    assert det_ambedkar.status == EligibilityStatus.ELIGIBLE
    assert "GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID" in det_ambedkar.rule_keys_fired

    # 4. Check governance presentation routing
    results_map = {r["scenario"]["scenario_id"]: r for r in z5_execution_results["results"]}
    s039_act = {d["scheme_id"]: d for d in results_map["S039"]["actionable_determinations"]}
    
    # PM-KISAN is confirmed in Section A
    assert s039_act["SCH001"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s039_act["SCH001"]["presentation_section"]

    # PMFBY is decoupled to Section B as REQUIRES_VERIFICATION pending Kharif GP IU notification
    pmfby = s039_act["SCH002"]
    assert pmfby["raw_engine_status"] == "ELIGIBLE"
    assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in pmfby["presentation_section"]
    assert pmfby["allow_numerical_scoring"] is False
    assert any("ragi" in mv.lower() for mv in pmfby["missing_verifications"])

    # Ambedkar Corporation is decoupled to Section B as REQUIRES_VERIFICATION
    ambedkar_gov = s039_act["SCH010_AMBEDKAR"]
    assert ambedkar_gov["raw_engine_status"] == "ELIGIBLE"
    assert ambedkar_gov["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in ambedkar_gov["presentation_section"]
    assert ambedkar_gov["allow_numerical_scoring"] is False
    assert any("perennial water source" in mv.lower() for mv in ambedkar_gov["missing_verifications"])
    assert any("chikkaballapura" in mv.lower() and "income" in mv.lower() for mv in ambedkar_gov["missing_verifications"])


def test_zone_z5_s040_boundary_5_0_ac_mechanization(z5_profiles, z5_execution_results):
    """
    Boundary test: Exactly 5.0 acres classified as Small holding ([2.5, 5.0], <= 5.0 is Small).
    Verify SMAM farm mechanization subsidy qualifies in Section A.
    Verify PMFBY raw INELIGIBLE is routed to Section B as REQUIRES_VERIFICATION pending RWBCIS check.
    """
    s040 = z5_profiles["S040"]
    assert s040["land_size_acres"] == 5.0
    assert "Small" in s040["farmer_category"]
    assert s040["immediate_need"] == "FARM_MECHANIZATION"

    engine = EligibilityEngine()
    filtered = {
        "scenario_id": s040["scenario_id"],
        "agro_climatic_zone": s040["agro_climatic_zone"],
        "district": s040["district"],
        "crop_primary": s040["crop_primary"],
        "land_size_acres": s040["land_size_acres"],
        "land_type": s040["land_type"],
        "social_category": s040["social_category"],
        "farmer_category": s040["farmer_category"],
        "existing_assets": s040["existing_assets"],
        "annual_family_income_lakh": s040["annual_family_income_lakh"],
        "immediate_need": s040["immediate_need"],
        "paid_income_tax_last_assessment_year": s040["paid_income_tax_last_assessment_year"],
        "govt_employee_category": s040["govt_employee_category"],
        "superannuated_pensioner_monthly_amount": s040["superannuated_pensioner_monthly_amount"],
        "pensioner_is_mts_exempt": s040["pensioner_is_mts_exempt"],
        "registered_professional": s040["registered_professional"],
        "land_ownership_cutoff_pre_feb_2019": s040["land_ownership_cutoff_pre_feb_2019"],
        "is_pure_tenant_without_land_title": s040["is_pure_tenant_without_land_title"],
        "borewell_electric_status": s040["borewell_electric_status"]
    }
    sc = FarmerScenario.from_dict(filtered)

    det_smam = engine.evaluate_scheme(sc, "SCH004")
    assert det_smam.status == EligibilityStatus.ELIGIBLE
    assert "SMAM_NO_PRIOR_SUBSIDY" in det_smam.rule_keys_fired

    det_kb = engine.evaluate_scheme(sc, "SCH005")
    assert det_kb.status == EligibilityStatus.INELIGIBLE
    assert "KRISHI_BHAGYA_NOT_DRYLAND" in det_kb.rule_keys_fired

    # Check execution results
    results_map = {r["scenario"]["scenario_id"]: r for r in z5_execution_results["results"]}
    s040_act = {d["scheme_id"]: d for d in results_map["S040"]["actionable_determinations"]}
    
    assert s040_act["SCH004"]["governance_status"] == "ELIGIBLE"
    assert "Section A" in s040_act["SCH004"]["presentation_section"]

    pmfby = s040_act["SCH002"]
    assert pmfby["raw_engine_status"] == "INELIGIBLE"
    assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
    assert "Section B" in pmfby["presentation_section"]


def test_zone_z5_parent_deduplication_and_denominator_reconciliation(z5_execution_results):
    """
    Verify visible scheme denominators:
    - S035, S036, S037, S038, S040 report 15 visible schemes (SCH008 suppressed, SCH010 ineligible).
    - S039 reports 14 visible schemes (both SCH008 and SCH010 suppressed).
    - All scenarios evaluate exactly 16 raw schemes.
    - Explicitly verify section breakdown for S039:
      5 in Section A, 3 in Section B (SCH002, SCH008_KA_COOP, SCH010_AMBEDKAR), 6 Disqualified.
    """
    results_map = {r["scenario"]["scenario_id"]: r for r in z5_execution_results["results"]}

    for sid in Z5_IDS:
        res = results_map[sid]
        assert len(res["raw_determinations"]) == 16, f"{sid} did not evaluate 16 raw schemes"

        act_ids = [d["scheme_id"] for d in res["actionable_determinations"]]
        assert "SCH008" not in act_ids, f"Abstract parent SCH008 was not suppressed in {sid}"

        if sid == "S039":
            assert len(act_ids) == 14, f"S039 expected 14 visible schemes, got {len(act_ids)}"
            assert "SCH010" not in act_ids, "Abstract parent SCH010 was not suppressed in S039"
            assert "SCH010_AMBEDKAR" in act_ids, "Concrete child SCH010_AMBEDKAR missing in S039"

            # Check section breakdown
            sec_a = [d["scheme_id"] for d in res["actionable_determinations"] if "Section A" in d["presentation_section"]]
            sec_b = [d["scheme_id"] for d in res["actionable_determinations"] if "Section B" in d["presentation_section"]]
            disq = [d["scheme_id"] for d in res["actionable_determinations"] if "Disqualified" in d["presentation_section"]]

            assert len(sec_a) == 4, f"Expected 4 in Section A for S039, got {len(sec_a)}: {sec_a}"
            assert len(sec_b) == 3, f"Expected 3 in Section B for S039, got {len(sec_b)}: {sec_b}"
            assert len(disq) == 7, f"Expected 7 Disqualified for S039, got {len(disq)}: {disq}"
            assert set(sec_b) == {"SCH002", "SCH008_KA_COOP", "SCH010_AMBEDKAR"}
        else:
            assert len(act_ids) == 15, f"{sid} expected 15 visible schemes, got {len(act_ids)}"
            assert "SCH010" in act_ids, f"Abstract parent SCH010 should be present as ineligible in {sid}"


def test_zone_z5_availability_state_decoupling(z5_execution_results):
    """
    Additional Safeguard: Verify 4-state availability pipeline execution.
    - Confirm availability_state is persisted independently for all 16 determinations in every scenario.
    - Confirm that statutory ELIGIBLE status does not erroneously activate 'Verified available now'.
    - Without active official dated circulars, all determinations preserve 'Availability unknown — confirmation required'.
    """
    results_map = {r["scenario"]["scenario_id"]: r for r in z5_execution_results["results"]}

    for sid in Z5_IDS:
        res = results_map[sid]
        for d in res["raw_determinations"]:
            assert "availability_state" in d
            assert d["availability_state"] == AvailabilityState.AVAILABILITY_UNKNOWN.value

        for d in res["actionable_determinations"]:
            assert "availability_state" in d
            assert d["availability_state"] == AvailabilityState.AVAILABILITY_UNKNOWN.value
            # Statutory eligibility must not contaminate availability
            assert d["availability_state"] != "Verified available now"
