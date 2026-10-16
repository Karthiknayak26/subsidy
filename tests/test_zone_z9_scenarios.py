"""
Targeted consistency, execution validation, and governance safeguard tests for Zone Z9 Profiles (S059-S064).
Validates schema compliance, assignment matrix consistency, universal Soil Health Card access in Hilly Zone (S059),
rainwater harvesting and hillside terrain exclusions for farm ponds (S060),
Challenge 5 pure tenant statutory exclusion from PM-KISAN with KCC institutional credit routing (S061),
Challenge 4 three-valued logic and UNKNOWN title governance handling (S062),
boundary test (2.5 ac Small) and PM-KUSUM Component B solar pump prerequisites (S063),
statutory inheritance succession (Clause 3(d)) vs post-cutoff partition deed regression safeguard (S064),
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
Z9_DIR = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", "z9")
REPORTS_DIR = os.path.join(WORKSPACE_ROOT, "reports")
Z9_IDS = ["S059", "S060", "S061", "S062", "S063", "S064"]


@pytest.fixture(scope="module")
def z9_profiles():
    profiles = {}
    for sid in Z9_IDS:
        filepath = os.path.join(Z9_DIR, f"{sid}.json")
        assert os.path.exists(filepath), f"Profile file missing: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            profiles[sid] = json.load(f)
    return profiles


@pytest.fixture(scope="module")
def z9_execution_results():
    filepath = os.path.join(Z9_DIR, "z9_execution_results.json")
    assert os.path.exists(filepath), f"Execution results missing: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def matrix_scenarios_by_id():
    return {s["sid"]: s for s in scenarios if s["sid"] in Z9_IDS}


def test_zone_z9_files_exist():
    """Verify all 6 JSON and Markdown profiles exist, along with batch, execution JSONs and report."""
    for sid in Z9_IDS:
        json_file = os.path.join(Z9_DIR, f"{sid}.json")
        md_file = os.path.join(Z9_DIR, f"{sid}.md")
        assert os.path.exists(json_file), f"Missing {json_file}"
        assert os.path.exists(md_file), f"Missing {md_file}"
        assert os.path.getsize(json_file) > 100
        assert os.path.getsize(md_file) > 100

    batch_json = os.path.join(Z9_DIR, "z9_scenarios.json")
    assert os.path.exists(batch_json)
    
    exec_json = os.path.join(Z9_DIR, "z9_execution_results.json")
    assert os.path.exists(exec_json)

    report_md = os.path.join(REPORTS_DIR, "zone_z9_execution_report.md")
    assert os.path.exists(report_md)
    assert os.path.getsize(report_md) > 1000


def test_zone_z9_matrix_consistency(z9_profiles, matrix_scenarios_by_id):
    """Verify each profile exactly matches its row in the benchmark assignment matrix."""
    for sid in Z9_IDS:
        prof = z9_profiles[sid]
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
            assert prof["social_category"] in ["OBC", "OBC (2A)", "OBC (2B)", "OBC (3A)", "OBC (3B)"]
        elif mat_soc == "GM":
            assert prof["social_category"] == "General (OC)"
        elif mat_soc == "Minority":
            assert prof["social_category"] in ["Minority", "Minority (Muslim)", "Minority (Christian)"]
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
        elif mat["land_type"] == "Hilly":
            assert prof["land_type"] == "Hilly/terraced"
        else:
            assert prof["land_type"] == mat["land_type"]

        # Farmer category interval check
        lclass = mat["lclass"]
        size = prof["land_size_acres"]
        if lclass == "Marginal":
            assert 0.0 < size <= 2.5
        elif lclass == "Small":
            assert 2.5 <= size <= 5.0
        elif lclass == "Medium":
            assert 5.0 < size <= 10.0
        elif lclass == "Large":
            assert size > 10.0

        # Tenure check
        mat_tenure = mat["tenure"]
        if mat_tenure == "Pre-Feb 2019":
            assert prof["land_ownership_cutoff_pre_feb_2019"] is True
            assert prof["is_pure_tenant_without_land_title"] is False
        elif mat_tenure == "Post-Feb 2019 Inheritance":
            assert prof["land_ownership_cutoff_pre_feb_2019"] is True
            assert prof["is_pure_tenant_without_land_title"] is False
            assert "statutory_succession_details" in prof
        elif mat_tenure == "Pure Tenant":
            assert prof["is_pure_tenant_without_land_title"] is True
        elif mat_tenure == "Unknown Title Status":
            assert prof["land_ownership_cutoff_pre_feb_2019"] is None
            assert prof["is_pure_tenant_without_land_title"] is False


def test_zone_z9_parent_suppression_and_actionable_reconciliation(z9_execution_results):
    """Verify denominator accounting: 16 raw evaluations, exact parent deduplication, and section sums."""
    expected_breakdowns = {
        "S059": {"sa": 4, "sb": 2, "dq": 9, "total": 15},
        "S060": {"sa": 4, "sb": 2, "dq": 9, "total": 15},
        "S061": {"sa": 2, "sb": 3, "dq": 10, "total": 15},
        "S062": {"sa": 3, "sb": 3, "dq": 9, "total": 15},
        "S063": {"sa": 6, "sb": 2, "dq": 7, "total": 15},
        "S064": {"sa": 5, "sb": 2, "dq": 8, "total": 15},
    }

    for item in z9_execution_results["results"]:
        sid = item["scenario_id"]
        raws = item["raw_determinations"]
        acts = item["actionable_determinations"]

        assert len(raws) == 16, f"{sid}: Must evaluate exactly 16 raw scheme records"
        assert len(acts) == 15, f"{sid}: Must display exactly 15 actionable schemes (SCH008 suppressed, SCH010 retained as ineligible)"

        sa = sum(1 for d in acts if d["presentation_section"].startswith("Section A"))
        sb = sum(1 for d in acts if d["presentation_section"].startswith("Section B"))
        dq = sum(1 for d in acts if d["presentation_section"].startswith("Disqualified"))

        exp = expected_breakdowns[sid]
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


def test_zone_z9_availability_decoupling(z9_execution_results):
    """Verify that every determination carries AvailabilityState.AVAILABILITY_UNKNOWN and none are marked Available now."""
    for item in z9_execution_results["results"]:
        sid = item["scenario_id"]
        for d in item["actionable_determinations"]:
            assert d["availability_state"] == AvailabilityState.AVAILABILITY_UNKNOWN.value, (
                f"{sid} - {d['scheme_id']}: Expected AVAILABILITY_UNKNOWN, got '{d['availability_state']}'"
            )
            assert d["availability_state"] != AvailabilityState.VERIFIED_AVAILABLE_NOW.value


def test_zone_z9_crop_insurance_governance_decoupling(z9_execution_results):
    """Verify PMFBY (SCH002) is routed to Section B with scoring disabled across all S059–S064 scenarios."""
    for item in z9_execution_results["results"]:
        sid = item["scenario_id"]
        pmfby = next((d for d in item["actionable_determinations"] if d["scheme_id"] == "SCH002"), None)
        assert pmfby is not None, f"PMFBY missing in actionable determinations for {sid}"
        assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
        assert pmfby["presentation_section"].startswith("Section B")
        assert pmfby["allow_numerical_scoring"] is False
        assert len(pmfby["missing_verifications"]) > 0
        assert any("Insurance Unit" in mv for mv in pmfby["missing_verifications"])


def test_zone_z9_provisional_schemes_quarantined(z9_execution_results):
    """Verify all provisional corporation schemes are quarantined in Section B with scoring disabled."""
    provisional_ids = {"SCH008_KA_COOP", "SCH010_VALMIKI", "SCH010_DEVARAJ_URS", "SCH010_KMDC"}
    for item in z9_execution_results["results"]:
        sid = item["scenario_id"]
        for d in item["actionable_determinations"]:
            if d["scheme_id"] in provisional_ids:
                if d["governance_status"] != "INELIGIBLE":
                    assert d["governance_status"] == "REQUIRES_VERIFICATION", (
                        f"{sid} - {d['scheme_id']}: Provisional scheme must be REQUIRES_VERIFICATION, got {d['governance_status']}"
                    )
                    assert d["presentation_section"].startswith("Section B")
                    assert d["allow_numerical_scoring"] is False


def test_zone_z9_s059_soil_health_card_universal(z9_execution_results, z9_profiles):
    """Verify S059 Small OC Coffee planter in Kodagu qualifies for Soil Health Card in Section A."""
    s059_res = next(r for r in z9_execution_results["results"] if r["scenario_id"] == "S059")
    acts = {d["scheme_id"]: d for d in s059_res["actionable_determinations"]}

    # Soil Health Card qualifies in Section A
    shc = acts["SCH009"]
    assert shc["raw_engine_status"] == "ELIGIBLE"
    assert shc["governance_status"] == "ELIGIBLE"
    assert shc["presentation_section"].startswith("Section A")
    assert shc["allow_numerical_scoring"] is True

    # Krishi Bhagya disqualified due to terrain (Hilly/terraced)
    kb = acts["SCH005"]
    assert kb["raw_engine_status"] == "INELIGIBLE"
    assert "KRISHI_BHAGYA_NOT_DRYLAND" in kb["rule_keys_fired"]

    # Ganga Kalyana parent and children disqualified due to terrain / non-dryland
    gk_parent = acts["SCH010"]
    assert gk_parent["raw_engine_status"] == "INELIGIBLE"

    # PM-KISAN qualifies in Section A
    pmk = acts["SCH001"]
    assert pmk["raw_engine_status"] == "ELIGIBLE"
    assert pmk["governance_status"] == "ELIGIBLE"


def test_zone_z9_s060_rainwater_harvesting_terrain_exclusions(z9_execution_results, z9_profiles):
    """Verify S060 Marginal ST Cardamom farmer in Chikkamagaluru with need RAINWATER_HARVESTING."""
    s060_res = next(r for r in z9_execution_results["results"] if r["scenario_id"] == "S060")
    acts = {d["scheme_id"]: d for d in s060_res["actionable_determinations"]}

    # Krishi Bhagya is disqualified due to Hilly/terraced topography
    kb = acts["SCH005"]
    assert kb["raw_engine_status"] == "INELIGIBLE"
    assert "KRISHI_BHAGYA_NOT_DRYLAND" in kb["rule_keys_fired"]

    # Valmiki Corporation is disqualified due to non-dryland/hilly terrain
    gk_valmiki = acts["SCH010_VALMIKI"]
    assert gk_valmiki["raw_engine_status"] == "INELIGIBLE"
    assert "GK_SCH010_VALMIKI_NOT_DRYLAND" in gk_valmiki["rule_keys_fired"]

    # Parent SCH010 retained as ineligible umbrella
    assert acts["SCH010"]["governance_status"] == "INELIGIBLE"

    # PM-KISAN, SMAM, Central KCC, and Soil Health Card qualify in Section A
    assert acts["SCH001"]["governance_status"] == "ELIGIBLE"
    assert acts["SCH004"]["governance_status"] == "ELIGIBLE"
    assert acts["SCH008_CENTRAL"]["governance_status"] == "ELIGIBLE"
    assert acts["SCH009"]["governance_status"] == "ELIGIBLE"
    assert acts["SCH003"]["governance_status"] == "INELIGIBLE"


def test_zone_z9_s061_pure_tenancy_routing(z9_execution_results, z9_profiles):
    """Verify S061 SC pure tenant in Uttara Kannada is excluded from PM-KISAN.
    KCC Central raw engine is ELIGIBLE under RBI/NABARD tenant guidelines, but
    governance routes it to Section B (REQUIRES_VERIFICATION) because tenant
    crop-loan documentation (oral-lease / JLG evidence) has not been verified.
    Section A: 2 (SMAM, Soil Health Card); Section B: 3 (PMFBY, KCC Central, KA Coop).
    """
    s061_res = next(r for r in z9_execution_results["results"] if r["scenario_id"] == "S061")
    acts = {d["scheme_id"]: d for d in s061_res["actionable_determinations"]}

    # PM-KISAN is strictly INELIGIBLE under PMKISAN_PURE_TENANT_EXCLUSION
    pmk = acts["SCH001"]
    assert pmk["raw_engine_status"] == "INELIGIBLE"
    assert pmk["governance_status"] == "INELIGIBLE"
    assert pmk["presentation_section"].startswith("Disqualified")
    assert "PMKISAN_PURE_TENANT_EXCLUSION" in pmk["rule_keys_fired"]

    # Central KCC: raw engine ELIGIBLE (borrower category qualifies), but governance
    # routes to Section B because oral-lease / JLG crop-loan documentation is unverified.
    kcc = acts["SCH008_CENTRAL"]
    assert kcc["raw_engine_status"] == "ELIGIBLE", (
        "Raw engine must preserve ELIGIBLE for SCH008_CENTRAL (tenant borrower category)"
    )
    assert kcc["governance_status"] == "REQUIRES_VERIFICATION", (
        "Governance must route SCH008_CENTRAL to REQUIRES_VERIFICATION pending documentation"
    )
    assert kcc["presentation_section"].startswith("Section B"), (
        "SCH008_CENTRAL must appear in Section B, not Section A"
    )
    assert kcc["allow_numerical_scoring"] is False
    assert len(kcc["missing_verifications"]) > 0
    assert any("tenant" in mv.lower() or "oral" in mv.lower() or "JLG" in mv or "crop-loan" in mv.lower()
               for mv in kcc["missing_verifications"]), (
        "missing_verifications must reference tenant crop-loan / oral-lease / JLG documentation"
    )

    # Ganga Kalyana Ambedkar Corporation is disqualified (requires clear land title + dryland)
    gk_amb = acts["SCH010_AMBEDKAR"]
    assert gk_amb["raw_engine_status"] == "INELIGIBLE"
    assert gk_amb["governance_status"] == "INELIGIBLE"

    # Section B must contain PMFBY, KCC Central, and KA Coop (total 3)
    sb_schemes = {d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section B")}
    assert "SCH002" in sb_schemes, "PMFBY must be in Section B"
    assert "SCH008_CENTRAL" in sb_schemes, "KCC Central must be in Section B"
    assert "SCH008_KA_COOP" in sb_schemes, "KA Coop must be in Section B"
    assert len(sb_schemes) == 3, f"Expected 3 Section B schemes, got {len(sb_schemes)}: {sb_schemes}"

    # Section A must contain only SMAM and Soil Health Card (total 2)
    sa_schemes = {d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section A")}
    assert "SCH004" in sa_schemes, "SMAM must be in Section A"
    assert "SCH009" in sa_schemes, "Soil Health Card must be in Section A"
    assert len(sa_schemes) == 2, f"Expected 2 Section A schemes, got {len(sa_schemes)}: {sa_schemes}"

    # Profile verifies pure tenancy flag
    p = z9_profiles["S061"]
    assert p["is_pure_tenant_without_land_title"] is True


def test_zone_z9_s062_unknown_title_three_valued_logic(z9_execution_results, z9_profiles):
    """Verify S062 Marginal OC Pepper farmer in Kodagu with UNKNOWN title date routes to Section B."""
    s062_res = next(r for r in z9_execution_results["results"] if r["scenario_id"] == "S062")
    acts = {d["scheme_id"]: d for d in s062_res["actionable_determinations"]}

    # PM-KISAN returns REQUIRES_VERIFICATION and is routed to Section B
    pmk = acts["SCH001"]
    assert pmk["raw_engine_status"] == "REQUIRES_VERIFICATION"
    assert pmk["governance_status"] == "REQUIRES_VERIFICATION"
    assert pmk["presentation_section"].startswith("Section B")
    assert pmk["allow_numerical_scoring"] is False
    assert "PMKISAN_CUTOFF_DATE_UNKNOWN" in pmk["rule_keys_fired"]

    # Soil Health Card qualifies in Section A (universal diagnostic access)
    shc = acts["SCH009"]
    assert shc["governance_status"] == "ELIGIBLE"
    assert shc["presentation_section"].startswith("Section A")
    assert shc["allow_numerical_scoring"] is True

    # SMAM and Central KCC also qualify in Section A
    assert acts["SCH004"]["governance_status"] == "ELIGIBLE"
    assert acts["SCH008_CENTRAL"]["governance_status"] == "ELIGIBLE"

    # Total Section B count must be exactly 3 (PM-KISAN, PMFBY, KA Coop)
    sb_schemes = [d["scheme_id"] for d in acts.values() if d["presentation_section"].startswith("Section B")]
    assert set(sb_schemes) == {"SCH001", "SCH002", "SCH008_KA_COOP"}


def test_zone_z9_s063_solar_pump_prerequisites_and_boundary_test(z9_execution_results, z9_profiles):
    """Verify S063 boundary test (2.5 ac Small) and PM-KUSUM Component B solar pump prerequisites."""
    p = z9_profiles["S063"]
    s063_res = next(r for r in z9_execution_results["results"] if r["scenario_id"] == "S063")
    acts = {d["scheme_id"]: d for d in s063_res["actionable_determinations"]}

    # Boundary test: holding exactly 2.5 ac classified as Small
    assert p["land_size_acres"] == 2.5
    assert p["farmer_category"] == "Small (2.5-5 acres)"

    # Operational water source & electric status verified
    assert p["water_and_irrigation"]["operational_water_source"] == "Borewell (Non-energized)"
    assert p["water_and_irrigation"]["borewell_electric_status"] == "UNENERGIZED_OFF_GRID"

    # PM-KUSUM Component B qualifies in Section A
    kusum = acts["SCH006"]
    assert kusum["raw_engine_status"] == "ELIGIBLE"
    assert kusum["governance_status"] == "ELIGIBLE"
    assert kusum["presentation_section"].startswith("Section A")
    assert kusum["allow_numerical_scoring"] is True
    assert "KUSUM_B_WATER_SOURCE_PRESENT" in kusum["rule_keys_fired"]
    assert "KUSUM_B_OFF_GRID_VERIFIED" in kusum["rule_keys_fired"]

    # KMDC Ganga Kalyana disqualified due to existing borewell and terrain
    kmdc = acts["SCH010_KMDC"]
    assert kmdc["raw_engine_status"] == "INELIGIBLE"
    assert kmdc["governance_status"] == "INELIGIBLE"
    assert "GK_SCH010_KMDC_HAS_EXISTING_BOREWELL" in kmdc["rule_keys_fired"] or "GK_SCH010_KMDC_NOT_DRYLAND" in kmdc["rule_keys_fired"]


def test_zone_z9_s064_statutory_inheritance_vs_partition_regression(z9_execution_results, z9_profiles):
    """Verify S064 statutory succession (Clause 3(d)) vs post-cutoff partition deed regression safeguard."""
    p = z9_profiles["S064"]
    s064_res = next(r for r in z9_execution_results["results"] if r["scenario_id"] == "S064")
    acts = {d["scheme_id"]: d for d in s064_res["actionable_determinations"]}

    # 1. Statutory succession details data contract
    assert "statutory_succession_details" in p, "S064 must contain statutory_succession_details contract"
    ssd = p["statutory_succession_details"]
    assert ssd["transfer_basis"] == "INHERITANCE_DUE_TO_DEATH"
    assert ssd["actual_acquisition_date"] == "2021-11-14"
    assert ssd["death_certificate_number"] == "DC/UK/2021/8841"
    assert ssd["legal_heir_certificate_number"] == "LHC/UK/2022/412"
    assert ssd["mutation_extract_form_16"] == "MR No. 2022-T209 (18.03.2022)"
    assert "Clause 3(d)" in ssd["statutory_authority"]
    assert "partition" in ssd["statutory_distinction"].lower()

    # 2. Engine mapping: land_ownership_cutoff_pre_feb_2019 is True
    assert p["land_ownership_cutoff_pre_feb_2019"] is True
    assert p["statutory_flags"]["land_ownership_cutoff_pre_feb_2019"] is True

    # 3. PM-KISAN qualifies in Section A
    pmk = acts["SCH001"]
    assert pmk["raw_engine_status"] == "ELIGIBLE"
    assert pmk["governance_status"] == "ELIGIBLE"
    assert pmk["presentation_section"].startswith("Section A")
    assert pmk["allow_numerical_scoring"] is True
    assert "PMKISAN_CUTOFF_DATE_VERIFIED" in pmk["rule_keys_fired"]

    # 4. SMAM power tiller qualifies in Section A for primary need FARM_MECHANIZATION
    smam = acts["SCH004"]
    assert smam["raw_engine_status"] == "ELIGIBLE"
    assert smam["governance_status"] == "ELIGIBLE"
    assert smam["presentation_section"].startswith("Section A")
    assert smam["allow_numerical_scoring"] is True

    # 5. Krishi Bhagya & Ganga Kalyana disqualified due to canal command
    assert acts["SCH005"]["governance_status"] == "INELIGIBLE"
    assert acts["SCH010"]["governance_status"] == "INELIGIBLE"
