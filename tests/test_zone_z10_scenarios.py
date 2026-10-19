"""
Targeted consistency, execution validation, and governance safeguard tests for Zone Z10 Profiles (S065-S070).
Validates schema compliance, assignment matrix consistency, universal Soil Health Card access in Coastal Zone (S065),
Challenge 7 community borewell pooling safeguard with corporation rules and beneficiary threshold verification (S066),
Cashew weather-based crop insurance (RWBCIS) and Valmiki Corporation individual borewell provisional quarantine (S067),
Challenge 5 pure tenant statutory exclusion from PM-KISAN with KCC institutional credit routing to Section B (S068),
PM-KISAN statutory inheritance succession (Clause 3(d)) vs post-cutoff partition deed regression safeguard,
MIDH protected horticulture, and off-grid solar pump replacement (S069),
Challenge 8 & Challenge 4 area limit (4.80 ha) physical capacity verification, explicit 7-year lock-in history,
and UNKNOWN title three-valued logic preservation in Section B for PM-KISAN and PMKSY-PDMC (S070),
operational availability decoupling, and parent deduplication reconciliation.
"""

import os
import json
import pytest
from src.eligibility.models import (
    FarmerScenario,
    EligibilityStatus,
    AvailabilityState,
    BorewellElectricStatus,
    GovtEmployeeCategory
)
from src.eligibility.engine import EligibilityEngine
from src.eligibility.availability import AvailabilityFilter
from research.dataset_research.validate_benchmark_matrix import scenarios

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Z10_DIR = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", "z10")
REPORTS_DIR = os.path.join(WORKSPACE_ROOT, "reports")
Z10_IDS = ["S065", "S066", "S067", "S068", "S069", "S070"]


@pytest.fixture(scope="module")
def z10_profiles():
    profiles = {}
    for sid in Z10_IDS:
        filepath = os.path.join(Z10_DIR, f"{sid}.json")
        assert os.path.exists(filepath), f"Profile file missing: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            profiles[sid] = json.load(f)
    return profiles


@pytest.fixture(scope="module")
def z10_execution_results():
    filepath = os.path.join(Z10_DIR, "z10_execution_results.json")
    assert os.path.exists(filepath), f"Execution results missing: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def matrix_scenarios_by_id():
    return {s["sid"]: s for s in scenarios if s["sid"] in Z10_IDS}


def test_zone_z10_files_exist():
    """Verify all 6 JSON and Markdown profiles exist, along with batch, execution JSONs and report."""
    for sid in Z10_IDS:
        json_file = os.path.join(Z10_DIR, f"{sid}.json")
        md_file = os.path.join(Z10_DIR, f"{sid}.md")
        assert os.path.exists(json_file), f"Missing scenario JSON: {json_file}"
        assert os.path.exists(md_file), f"Missing scenario MD: {md_file}"

    scenarios_json = os.path.join(Z10_DIR, "z10_scenarios.json")
    results_json = os.path.join(Z10_DIR, "z10_execution_results.json")
    report_md = os.path.join(REPORTS_DIR, "zone_z10_execution_report.md")

    assert os.path.exists(scenarios_json), f"Missing z10_scenarios.json: {scenarios_json}"
    assert os.path.exists(results_json), f"Missing z10_execution_results.json: {results_json}"
    assert os.path.exists(report_md), f"Missing zone_z10_execution_report.md: {report_md}"


def test_zone_z10_profiles_schema_valid(z10_profiles):
    """Verify all 6 profiles conform to FarmerScenario schema and instantiate correctly."""
    required_keys = [
        "scenario_id", "benchmark_version", "zone_id", "agro_climatic_zone",
        "district", "crop_primary", "land_size_acres", "land_type",
        "social_category", "farmer_category", "existing_assets",
        "annual_family_income_lakh", "immediate_need",
        "paid_income_tax_last_assessment_year", "govt_employee_category",
        "superannuated_pensioner_monthly_amount", "pensioner_is_mts_exempt",
        "registered_professional", "land_ownership_cutoff_pre_feb_2019",
        "is_pure_tenant_without_land_title", "borewell_electric_status",
        "farming_stage", "season", "kcc_query_text_example",
        "landholding_details", "water_and_irrigation", "statutory_flags",
        "attribute_provenance", "intended_test_purpose", "unresolved_dependencies"
    ]

    for sid, p in z10_profiles.items():
        assert p["scenario_id"] == sid
        assert p["benchmark_version"] == "v1.0.4"
        assert p["zone_id"] == "Z10"
        assert p["agro_climatic_zone"] == "Coastal Zone"

        for k in required_keys:
            assert k in p, f"{sid} missing key: {k}"

        # Instantiate FarmerScenario domain model to verify types
        scenario_data = {
            "scenario_id": p["scenario_id"],
            "agro_climatic_zone": p["agro_climatic_zone"],
            "district": p["district"],
            "crop_primary": p["crop_primary"],
            "land_size_acres": p["land_size_acres"],
            "land_type": p["land_type"],
            "social_category": p["social_category"],
            "farmer_category": p["farmer_category"],
            "existing_assets": p["existing_assets"],
            "annual_family_income_lakh": p["annual_family_income_lakh"],
            "immediate_need": p["immediate_need"],
            "paid_income_tax_last_assessment_year": p["paid_income_tax_last_assessment_year"],
            "govt_employee_category": p["govt_employee_category"],
            "superannuated_pensioner_monthly_amount": p["superannuated_pensioner_monthly_amount"],
            "pensioner_is_mts_exempt": p["pensioner_is_mts_exempt"],
            "registered_professional": p["registered_professional"],
            "land_ownership_cutoff_pre_feb_2019": p["land_ownership_cutoff_pre_feb_2019"],
            "is_pure_tenant_without_land_title": p["is_pure_tenant_without_land_title"],
            "borewell_electric_status": p["borewell_electric_status"],
            "prior_micro_irrigation_subsidy_years_ago": p.get("prior_micro_irrigation_subsidy_years_ago"),
            "prior_farm_pond_subsidy_years_ago": p.get("prior_farm_pond_subsidy_years_ago"),
            "prior_machinery_subsidy_years_ago": p.get("prior_machinery_subsidy_years_ago"),
            "prior_ganga_kalyana_in_family": p.get("prior_ganga_kalyana_in_family", False),
            "community_pool_acres": p.get("community_pool_acres", 0.0),
            "community_pool_beneficiaries_count": p.get("community_pool_beneficiaries_count", 0),
            "crop_secondary": p.get("crop_secondary"),
            "farming_stage": p.get("farming_stage"),
            "season": p.get("season"),
            "kcc_query_text_example": p.get("kcc_query_text_example")
        }
        obj = FarmerScenario.from_dict(scenario_data)
        assert obj.scenario_id == sid


def test_zone_z10_matrix_consistency(z10_profiles, matrix_scenarios_by_id):
    """Verify all 6 scenarios align exactly with Benchmark v1.0.4 assignment matrix."""
    for sid, p in z10_profiles.items():
        mat = matrix_scenarios_by_id[sid]
        assert p["district"] == mat["dist"]
        assert p["crop_primary"] == ("Paddy" if mat["crop"] == "Coastal Paddy" else mat["crop"])
        assert p["land_size_acres"] == mat["total_holding"]
        assert p["immediate_need"] == mat["need"]
        assert p["water_and_irrigation"]["operational_water_source"] == mat["water_source"]
        assert p["borewell_electric_status"] == mat["electric_status"]

        # Social category alignment
        if mat["social"] == "GM":
            assert p["social_category"] == "General (OC)"
        else:
            assert p["social_category"] == mat["social"]

        # Community pool alignment
        if mat["pool"].startswith("Yes"):
            assert p["community_pool_acres"] > 0
            assert p["community_pool_beneficiaries_count"] >= 3
        else:
            assert p["community_pool_acres"] == 0.0
            assert p["community_pool_beneficiaries_count"] == 0

        # Physical capacity cross-field check
        details = p["landholding_details"]
        assert details["total_operational_holding_acres"] == mat["total_holding"]
        assert details["qualifying_parcel_acres"] == mat["qual_parcel"]
        assert details["physical_area_consistency"].startswith("PASS")


def test_zone_z10_parent_suppression_and_actionable_reconciliation(z10_execution_results):
    """
    Verify exact reconciliation of actionable determinations and abstract parent suppression:
    - S065: SA=4, SB=2, DQ=9, Total=15 (SCH008 suppressed by credit children; SCH010 retained as ineligible)
    - S066: SA=4, SB=3, DQ=7, Total=14 (SCH008 suppressed; SCH010 suppressed by SCH010_AMBEDKAR)
    - S067: SA=4, SB=3, DQ=7, Total=14 (SCH008 suppressed; SCH010 suppressed by SCH010_VALMIKI)
    - S068: SA=2, SB=3, DQ=10, Total=15 (SCH008 suppressed; SCH010 retained as ineligible)
    - S069: SA=6, SB=2, DQ=7, Total=15 (SCH008 suppressed; SCH010 retained as ineligible)
    - S070: SA=3, SB=4, DQ=8, Total=15 (SCH008 suppressed; SCH010 retained as ineligible)
    """
    expected_breakdowns = {
        "S065": {"sa": 4, "sb": 2, "dq": 9, "total": 15},
        "S066": {"sa": 4, "sb": 3, "dq": 7, "total": 14},
        "S067": {"sa": 4, "sb": 3, "dq": 7, "total": 14},
        "S068": {"sa": 2, "sb": 3, "dq": 10, "total": 15},
        "S069": {"sa": 6, "sb": 2, "dq": 7, "total": 15},
        "S070": {"sa": 3, "sb": 4, "dq": 8, "total": 15},
    }

    for item in z10_execution_results["results"]:
        sid = item["scenario_id"]
        raws = item["raw_determinations"]
        acts = item["actionable_determinations"]

        assert len(raws) == 16, f"{sid}: Must evaluate exactly 16 raw scheme records"

        sa = sum(1 for d in acts if d["presentation_section"].startswith("Section A"))
        sb = sum(1 for d in acts if d["presentation_section"].startswith("Section B"))
        dq = sum(1 for d in acts if d["presentation_section"].startswith("Disqualified"))

        exp = expected_breakdowns[sid]
        assert len(acts) == exp["total"], f"{sid}: Expected {exp['total']} actionable schemes, got {len(acts)}"
        assert sa == exp["sa"], f"{sid}: Expected Section A={exp['sa']}, got {sa}"
        assert sb == exp["sb"], f"{sid}: Expected Section B={exp['sb']}, got {sb}"
        assert dq == exp["dq"], f"{sid}: Expected Disqualified={exp['dq']}, got {dq}"
        assert sa + sb + dq == exp["total"], f"{sid}: Section sum must equal {exp['total']}"

        # Check scoring flag consistency
        for d in acts:
            if d["presentation_section"].startswith("Section A"):
                assert d["allow_numerical_scoring"] is True
                assert d["governance_status"] == "ELIGIBLE"
            else:
                assert d["allow_numerical_scoring"] is False
                assert d["governance_status"] in ["REQUIRES_VERIFICATION", "INELIGIBLE"]


def test_zone_z10_availability_decoupling(z10_execution_results):
    """Verify that every determination carries AvailabilityState.AVAILABILITY_UNKNOWN and none are marked Available now."""
    for item in z10_execution_results["results"]:
        sid = item["scenario_id"]
        for d in item["actionable_determinations"]:
            assert d["availability_state"] == AvailabilityState.AVAILABILITY_UNKNOWN.value, (
                f"{sid} - {d['scheme_id']}: Expected AVAILABILITY_UNKNOWN, got '{d['availability_state']}'"
            )
            assert d["availability_state"] != AvailabilityState.VERIFIED_AVAILABLE_NOW.value


def test_zone_z10_crop_insurance_governance_decoupling(z10_execution_results):
    """Verify PMFBY (SCH002) is routed to Section B with scoring disabled across all S065–S070 scenarios."""
    for item in z10_execution_results["results"]:
        sid = item["scenario_id"]
        pmfby = next((d for d in item["actionable_determinations"] if d["scheme_id"] == "SCH002"), None)
        assert pmfby is not None, f"PMFBY missing in actionable determinations for {sid}"
        assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
        assert pmfby["presentation_section"].startswith("Section B")
        assert pmfby["allow_numerical_scoring"] is False
        assert len(pmfby["missing_verifications"]) > 0
        assert any("Insurance Unit" in mv or "RWBCIS" in mv or "insurance" in mv.lower()
                   for mv in pmfby["missing_verifications"])


def test_zone_z10_provisional_schemes_quarantined(z10_execution_results):
    """Verify all provisional corporation schemes are quarantined in Section B with scoring disabled."""
    provisional_ids = {"SCH008_KA_COOP", "SCH010_VALMIKI", "SCH010_DEVARAJ_URS", "SCH010_KMDC"}
    for item in z10_execution_results["results"]:
        sid = item["scenario_id"]
        for d in item["actionable_determinations"]:
            if d["scheme_id"] in provisional_ids:
                if d["governance_status"] != "INELIGIBLE":
                    assert d["governance_status"] == "REQUIRES_VERIFICATION", (
                        f"{sid} - {d['scheme_id']}: Provisional scheme must be REQUIRES_VERIFICATION, got {d['governance_status']}"
                    )
                    assert d["presentation_section"].startswith("Section B")
                    assert d["allow_numerical_scoring"] is False


def test_zone_z10_s065_soil_health_card_universal(z10_execution_results, z10_profiles):
    """Verify S065 Large GM Coconut grower in Dakshina Kannada qualifies for Soil Health Card in Section A."""
    s065_res = next(r for r in z10_execution_results["results"] if r["scenario_id"] == "S065")
    acts = {d["scheme_id"]: d for d in s065_res["actionable_determinations"]}

    # Soil Health Card qualifies in Section A
    shc = acts["SCH009"]
    assert shc["raw_engine_status"] == "ELIGIBLE"
    assert shc["governance_status"] == "ELIGIBLE"
    assert shc["presentation_section"].startswith("Section A")
    assert shc["allow_numerical_scoring"] is True

    # PM-KISAN, SMAM, Central KCC qualify in Section A
    assert acts["SCH001"]["governance_status"] == "ELIGIBLE"
    assert acts["SCH004"]["governance_status"] == "ELIGIBLE"
    assert acts["SCH008_CENTRAL"]["governance_status"] == "ELIGIBLE"

    # Krishi Bhagya disqualified due to unnotified coastal district
    kb = acts["SCH005"]
    assert kb["raw_engine_status"] == "INELIGIBLE"
    assert "KRISHI_BHAGYA_DISTRICT_NOT_RAINFED" in kb["rule_keys_fired"]

    # Ganga Kalyana parent and children disqualified (GM category)
    assert acts["SCH010"]["governance_status"] == "INELIGIBLE"
    assert acts["SCH010_AMBEDKAR"]["governance_status"] == "INELIGIBLE"


def test_zone_z10_s066_community_borewell_safeguard(z10_execution_results, z10_profiles):
    """
    Verify S066 SC medium arecanut farmer with community borewell pooling:
    - 4 SC farmers pooling 14.0 contiguous dryland acres, qualifying parcel 3.5 ac.
    - Raw engine evaluates ELIGIBLE (GK_AMBEDKAR_COMMUNITY_ROUTE_VALID).
    - Governance safeguard decouples determination to Section B as REQUIRES_VERIFICATION
      with scoring disabled until applicable corporation rules and beneficiary thresholds are verified.
    - Abstract parent SCH010 is suppressed from actionable recommendations.
    - Section A: 4 (PM-KISAN, SMAM, Central KCC, Soil Health Card).
    - Section B: 3 (PMFBY, KA Coop, Ambedkar Community Borewell).
    - Disqualified: 7. Total Actionable: 14.
    """
    p = z10_profiles["S066"]
    s066_res = next(r for r in z10_execution_results["results"] if r["scenario_id"] == "S066")
    acts = {d["scheme_id"]: d for d in s066_res["actionable_determinations"]}

    # Profile assertions
    assert p["land_size_acres"] == 5.5
    assert p["community_pool_acres"] == 14.0
    assert p["community_pool_beneficiaries_count"] == 4
    assert p["social_category"] == "SC"

    # Ambedkar Community Borewell: raw ELIGIBLE, governance REQUIRES_VERIFICATION in Section B
    amb = acts["SCH010_AMBEDKAR"]
    assert amb["raw_engine_status"] == "ELIGIBLE", "Raw engine must evaluate community route as ELIGIBLE"
    assert "GK_AMBEDKAR_COMMUNITY_ROUTE_VALID" in amb["rule_keys_fired"]
    assert amb["governance_status"] == "REQUIRES_VERIFICATION", (
        "Governance safeguard must place determination in REQUIRES_VERIFICATION pending threshold verification"
    )
    assert amb["presentation_section"].startswith("Section B"), (
        "Ambedkar community borewell must appear in Section B, not Section A"
    )
    assert amb["allow_numerical_scoring"] is False, "Scoring must be disabled"
    assert len(amb["missing_verifications"]) > 0
    assert any("beneficiary" in mv.lower() or "threshold" in mv.lower() or "corporation" in mv.lower()
               for mv in amb["missing_verifications"])

    # Abstract parent SCH010 must be suppressed from actionable recommendations
    assert "SCH010" not in acts, "Abstract parent SCH010 must be suppressed when SCH010_AMBEDKAR is actionable"

    # Section A schemes
    sa_schemes = {d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section A")}
    assert sa_schemes == {"SCH001", "SCH004", "SCH008_CENTRAL", "SCH009"}

    # Section B schemes
    sb_schemes = {d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section B")}
    assert sb_schemes == {"SCH002", "SCH008_KA_COOP", "SCH010_AMBEDKAR"}


def test_zone_z10_s067_cashew_rwbcis_and_valmiki_quarantine(z10_execution_results, z10_profiles):
    """
    Verify S067 ST marginal cashew farmer in Dakshina Kannada:
    - Cashew is not in static PMFBY whitelist; raw INELIGIBLE routed to Section B pending RWBCIS notification.
    - Valmiki Corporation individual borewell: raw ELIGIBLE (coastal threshold 1.0-5.0 ac).
    - Governance safeguard: quarantined in Section B as provisional scheme with scoring disabled.
    - Abstract parent SCH010 suppressed. Total Actionable: 14.
    """
    p = z10_profiles["S067"]
    s067_res = next(r for r in z10_execution_results["results"] if r["scenario_id"] == "S067")
    acts = {d["scheme_id"]: d for d in s067_res["actionable_determinations"]}

    # Profile checks
    assert p["crop_primary"] == "Cashew"
    assert p["social_category"] == "ST"
    assert p["land_size_acres"] == 2.0

    # PMFBY decoupled to Section B
    pmfby = acts["SCH002"]
    assert pmfby["raw_engine_status"] == "INELIGIBLE"
    assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
    assert pmfby["presentation_section"].startswith("Section B")

    # Valmiki Corporation borewell: raw ELIGIBLE, governance Section B (provisional)
    valmiki = acts["SCH010_VALMIKI"]
    assert valmiki["raw_engine_status"] == "ELIGIBLE"
    assert "GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID" in valmiki["rule_keys_fired"]
    assert valmiki["governance_status"] == "REQUIRES_VERIFICATION"
    assert valmiki["presentation_section"].startswith("Section B")
    assert valmiki["allow_numerical_scoring"] is False

    # Abstract parent SCH010 suppressed
    assert "SCH010" not in acts, "Abstract parent SCH010 must be suppressed when child is actionable"

    # Section counts
    sa_schemes = {d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section A")}
    assert sa_schemes == {"SCH001", "SCH004", "SCH008_CENTRAL", "SCH009"}
    sb_schemes = {d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section B")}
    assert sb_schemes == {"SCH002", "SCH008_KA_COOP", "SCH010_VALMIKI"}


def test_zone_z10_s068_pure_tenancy_routing(z10_execution_results, z10_profiles):
    """
    Verify S068 Minority pure tenant in Udupi:
    - Excluded from PM-KISAN under PMKISAN_PURE_TENANT_EXCLUSION.
    - Central KCC raw engine is ELIGIBLE under RBI/NABARD tenant credit guidelines, but
      governance routes it to Section B (REQUIRES_VERIFICATION) pending tenant crop-loan documentation.
    - Section A: 2 (SMAM, Soil Health Card); Section B: 3 (PMFBY, KCC Central, KA Coop); DQ: 10. Total: 15.
    """
    s068_res = next(r for r in z10_execution_results["results"] if r["scenario_id"] == "S068")
    acts = {d["scheme_id"]: d for d in s068_res["actionable_determinations"]}

    # PM-KISAN strictly INELIGIBLE
    pmk = acts["SCH001"]
    assert pmk["raw_engine_status"] == "INELIGIBLE"
    assert pmk["governance_status"] == "INELIGIBLE"
    assert pmk["presentation_section"].startswith("Disqualified")
    assert "PMKISAN_PURE_TENANT_EXCLUSION" in pmk["rule_keys_fired"]

    # Central KCC: raw ELIGIBLE, governance Section B
    kcc = acts["SCH008_CENTRAL"]
    assert kcc["raw_engine_status"] == "ELIGIBLE"
    assert kcc["governance_status"] == "REQUIRES_VERIFICATION"
    assert kcc["presentation_section"].startswith("Section B")
    assert kcc["allow_numerical_scoring"] is False
    assert len(kcc["missing_verifications"]) > 0
    assert any("tenant" in mv.lower() or "oral" in mv.lower() or "crop-loan" in mv.lower()
               for mv in kcc["missing_verifications"])

    # Section A has exactly 2 schemes: SMAM and Soil Health Card
    sa_schemes = {d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section A")}
    assert sa_schemes == {"SCH004", "SCH009"}

    # Section B has exactly 3 schemes: PMFBY, KCC Central, KA Coop
    sb_schemes = {d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section B")}
    assert sb_schemes == {"SCH002", "SCH008_CENTRAL", "SCH008_KA_COOP"}


def test_zone_z10_s069_statutory_inheritance_midh_kusum(z10_execution_results, z10_profiles):
    """
    Verify S069 Large Minority Coconut grower in Dakshina Kannada:
    - Post-Feb 2019 statutory succession (Clause 3(d)): transfer_basis=INHERITANCE_DUE_TO_DEATH,
      actual acquisition date 2022-04-12, death cert DC/DK/2022/6104, legal heir LHC/DK/2022/339,
      Bhoomi mutation Form 16 MR No. 2022-T771. Distinct from ineligible partition deeds.
    - PM-KISAN qualifies in Section A.
    - MIDH qualifies in Section A for shaded nursery / protected horticulture with installed drip.
    - PM-KUSUM Component B qualifies in Section A for off-grid open well replacing diesel pump.
    - SMAM, Central KCC, Soil Health Card qualify in Section A (Total Section A = 6).
    - Total Section B = 2 (PMFBY, KA Coop). Total Actionable = 15.
    """
    p = z10_profiles["S069"]
    s069_res = next(r for r in z10_execution_results["results"] if r["scenario_id"] == "S069")
    acts = {d["scheme_id"]: d for d in s069_res["actionable_determinations"]}

    # 1. Statutory succession data contract
    assert "statutory_succession_details" in p
    ssd = p["statutory_succession_details"]
    assert ssd["transfer_basis"] == "INHERITANCE_DUE_TO_DEATH"
    assert ssd["actual_acquisition_date"] == "2022-04-12"
    assert ssd["death_certificate_number"] == "DC/DK/2022/6104"
    assert ssd["legal_heir_certificate_number"] == "LHC/DK/2022/339"
    assert ssd["mutation_extract_form_16"] == "MR No. 2022-T771 (22.06.2022)"
    assert "Clause 3(d)" in ssd["statutory_authority"]
    assert "partition" in ssd["statutory_distinction"].lower()

    # 2. PM-KISAN qualifies in Section A
    pmk = acts["SCH001"]
    assert pmk["raw_engine_status"] == "ELIGIBLE"
    assert pmk["governance_status"] == "ELIGIBLE"
    assert pmk["presentation_section"].startswith("Section A")
    assert "PMKISAN_CUTOFF_DATE_VERIFIED" in pmk["rule_keys_fired"]

    # 3. MIDH protected horticulture qualifies in Section A
    midh = acts["SCH007"]
    assert midh["raw_engine_status"] == "ELIGIBLE"
    assert midh["governance_status"] == "ELIGIBLE"
    assert midh["presentation_section"].startswith("Section A")
    assert midh["allow_numerical_scoring"] is True
    assert "MIDH_HORTICULTURE_CROP_VERIFIED" in midh["rule_keys_fired"]
    assert "MIDH_MICRO_IRRIGATION_VERIFIED" in midh["rule_keys_fired"]

    # 4. PM-KUSUM Component B qualifies in Section A
    kusum = acts["SCH006"]
    assert kusum["raw_engine_status"] == "ELIGIBLE"
    assert kusum["governance_status"] == "ELIGIBLE"
    assert kusum["presentation_section"].startswith("Section A")
    assert "KUSUM_B_WATER_SOURCE_PRESENT" in kusum["rule_keys_fired"]
    assert "KUSUM_B_OFF_GRID_VERIFIED" in kusum["rule_keys_fired"]

    # 5. Section A contains 6 schemes
    sa_schemes = {d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section A")}
    assert sa_schemes == {"SCH001", "SCH004", "SCH006", "SCH007", "SCH008_CENTRAL", "SCH009"}


def test_zone_z10_s070_unknown_title_and_area_limit(z10_execution_results, z10_profiles):
    """
    Verify S070 Large SC arecanut farmer in Udupi:
    - Large holding 12.5 acres (> 10.0 ac); requested subsidized area 4.80 ha <= 12.5 ac * 0.404686 = 5.0586 ha
      physical parcel capacity PASS; <= 5.00 ha PMKSY ceiling PASS.
    - Explicit first-time applicant declaration: prior_micro_irrigation_subsidy_years_ago is None
      (mapped to PMKSY_NO_PRIOR_SUBSIDY), satisfying 7-year lock-in restriction.
    - Land title record date is UNKNOWN (land_ownership_cutoff_pre_feb_2019 = None):
      PM-KISAN and PMKSY-PDMC preserve three-valued logic in Section B as REQUIRES_VERIFICATION
      with scoring disabled pending title regularization.
    - Section A: 3 (SMAM, Central KCC, Soil Health Card).
    - Section B: 4 (PM-KISAN, PMFBY, PMKSY-PDMC, KA Coop).
    - Disqualified: 8. Total Actionable: 15.
    """
    p = z10_profiles["S070"]
    s070_res = next(r for r in z10_execution_results["results"] if r["scenario_id"] == "S070")
    acts = {d["scheme_id"]: d for d in s070_res["actionable_determinations"]}

    # 1. Physical area consistency and 5.0 ha statutory ceiling
    assert p["land_size_acres"] == 12.5
    assert p["landholding_details"]["requested_subsidized_area_ha"] == 4.8
    assert p["landholding_details"]["qualifying_parcel_acres"] == 12.5
    assert p["landholding_details"]["physical_area_consistency"].startswith("PASS")
    # Verify 4.80 ha <= 12.5 ac (5.059 ha)
    max_phys_ha = 12.5 * 0.40468564224
    assert 4.8 <= max_phys_ha

    # 2. Explicit prior subsidy history
    assert "prior_subsidy_history" in p
    psh = p["prior_subsidy_history"]
    assert psh["interpretation"] == "EXPLICIT_NO_PRIOR_SUBSIDY"
    assert "7-year" in psh["statutory_clauses"]["section_7_10_repeat_subsidy_restriction"]
    assert "5.0 hectares" in psh["statutory_clauses"]["section_7_9_area_ceiling"]

    # 3. PMKSY-PDMC: raw INELIGIBLE (land > 12.35 ac), governance Section B (REQUIRES_VERIFICATION)
    pdmc = acts["SCH003"]
    assert pdmc["raw_engine_status"] == "INELIGIBLE"
    assert "PMKSY_LAND_ABOVE_5_HA" in pdmc["rule_keys_fired"]
    assert pdmc["governance_status"] == "REQUIRES_VERIFICATION"
    assert pdmc["presentation_section"].startswith("Section B")
    assert pdmc["allow_numerical_scoring"] is False
    assert len(pdmc["missing_verifications"]) > 0
    assert any("title" in mv.lower() or "mutation" in mv.lower() for mv in pdmc["missing_verifications"])

    # 4. PM-KISAN: raw REQUIRES_VERIFICATION (UNKNOWN cut-off date), governance Section B
    pmk = acts["SCH001"]
    assert pmk["raw_engine_status"] == "REQUIRES_VERIFICATION"
    assert "PMKISAN_CUTOFF_DATE_UNKNOWN" in pmk["rule_keys_fired"]
    assert pmk["governance_status"] == "REQUIRES_VERIFICATION"
    assert pmk["presentation_section"].startswith("Section B")
    assert pmk["allow_numerical_scoring"] is False

    # 5. Grid-connected borewell excludes PM-KUSUM Component B
    kusum = acts["SCH006"]
    assert kusum["raw_engine_status"] == "INELIGIBLE"
    assert "KUSUM_B_GRID_CONNECTED_DISQUALIFIED" in kusum["rule_keys_fired"]

    # 6. Section counts
    sa_schemes = {d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section A")}
    assert sa_schemes == {"SCH004", "SCH008_CENTRAL", "SCH009"}
    sb_schemes = {d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section B")}
    assert sb_schemes == {"SCH001", "SCH002", "SCH003", "SCH008_KA_COOP"}
