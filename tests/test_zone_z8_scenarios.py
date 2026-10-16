"""
Targeted consistency, execution validation, and governance safeguard tests for Zone Z8 Profiles (S053-S058).
Validates schema compliance, assignment matrix consistency, Krishi Bhagya farm pond in rainfed Dharwad (S053),
MIDH protected horticulture shade-net in wetland Belagavi (S054),
Challenge 3 regular government officer statutory exclusion isolation (S055),
Challenge 4 three-valued logic and UNKNOWN title governance handling (S056),
Challenge 8 SMAM tiered machinery subsidy for large canal sugarcane (S057),
Challenge 8 & boundary test PMKSY-PDMC 5.00 ha ceiling on large holding (S058),
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
Z8_DIR = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", "z8")
REPORTS_DIR = os.path.join(WORKSPACE_ROOT, "reports")
Z8_IDS = ["S053", "S054", "S055", "S056", "S057", "S058"]


@pytest.fixture(scope="module")
def z8_profiles():
    profiles = {}
    for sid in Z8_IDS:
        filepath = os.path.join(Z8_DIR, f"{sid}.json")
        assert os.path.exists(filepath), f"Profile file missing: {filepath}"
        with open(filepath, "r", encoding="utf-8") as f:
            profiles[sid] = json.load(f)
    return profiles


@pytest.fixture(scope="module")
def z8_execution_results():
    filepath = os.path.join(Z8_DIR, "z8_execution_results.json")
    assert os.path.exists(filepath), f"Execution results missing: {filepath}"
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def matrix_scenarios_by_id():
    return {s["sid"]: s for s in scenarios if s["sid"] in Z8_IDS}


def test_zone_z8_files_exist():
    """Verify all 6 JSON and Markdown profiles exist, along with batch, execution JSONs and report."""
    for sid in Z8_IDS:
        json_file = os.path.join(Z8_DIR, f"{sid}.json")
        md_file = os.path.join(Z8_DIR, f"{sid}.md")
        assert os.path.exists(json_file), f"Missing {json_file}"
        assert os.path.exists(md_file), f"Missing {md_file}"
        assert os.path.getsize(json_file) > 100
        assert os.path.getsize(md_file) > 100

    batch_json = os.path.join(Z8_DIR, "z8_scenarios.json")
    assert os.path.exists(batch_json)
    
    exec_json = os.path.join(Z8_DIR, "z8_execution_results.json")
    assert os.path.exists(exec_json)

    report_md = os.path.join(REPORTS_DIR, "zone_z8_execution_report.md")
    assert os.path.exists(report_md)
    assert os.path.getsize(report_md) > 1000


def test_zone_z8_matrix_consistency(z8_profiles, matrix_scenarios_by_id):
    """Verify each profile exactly matches its row in the benchmark assignment matrix."""
    for sid in Z8_IDS:
        prof = z8_profiles[sid]
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
        elif mat_tenure == "Unknown Title Status":
            assert prof["land_ownership_cutoff_pre_feb_2019"] is None
            assert prof["is_pure_tenant_without_land_title"] is False


def test_zone_z8_parent_suppression_and_actionable_reconciliation(z8_execution_results):
    """Verify denominator accounting: 16 raw evaluations, exact parent deduplication, and section sums."""
    for item in z8_execution_results["results"]:
        sid = item["scenario_id"]
        raws = item["raw_determinations"]
        acts = item["actionable_determinations"]

        assert len(raws) == 16, f"{sid}: Must evaluate exactly 16 raw scheme records"

        # Check actionable counts based on abstract parent deduplication
        if sid == "S056":
            # Parent SCH008 suppressed, Parent SCH010 suppressed (actionable child SCH010_VALMIKI in Section B)
            assert len(acts) == 14, f"{sid}: Must display exactly 14 actionable schemes (both abstract parents suppressed)"
        elif sid in ["S053", "S054", "S055", "S057", "S058"]:
            # Parent SCH008 suppressed, Parent SCH010 retained as ineligible umbrella
            assert len(acts) == 15, f"{sid}: Must display exactly 15 actionable schemes (SCH008 suppressed, SCH010 retained as ineligible)"

        # Check section accounting sum
        sa = sum(1 for d in acts if d["presentation_section"].startswith("Section A"))
        sb = sum(1 for d in acts if d["presentation_section"].startswith("Section B"))
        dq = sum(1 for d in acts if d["presentation_section"].startswith("Disqualified"))

        assert sa + sb + dq == len(acts), f"{sid}: Section sums ({sa} + {sb} + {dq}) must equal total actionable ({len(acts)})"

        # Check scoring flag consistency
        for d in acts:
            if d["presentation_section"].startswith("Section A"):
                assert d["allow_numerical_scoring"] is True
                assert d["governance_status"] == "ELIGIBLE"
            else:
                assert d["allow_numerical_scoring"] is False
                assert d["governance_status"] in ["REQUIRES_VERIFICATION", "INELIGIBLE"]


def test_zone_z8_availability_decoupling(z8_execution_results):
    """Verify that every determination carries AvailabilityState.AVAILABILITY_UNKNOWN and none are marked Available now."""
    for item in z8_execution_results["results"]:
        sid = item["scenario_id"]
        for d in item["actionable_determinations"]:
            assert d["availability_state"] == AvailabilityState.AVAILABILITY_UNKNOWN.value, (
                f"{sid} - {d['scheme_id']}: Expected AVAILABILITY_UNKNOWN, got '{d['availability_state']}'"
            )
            assert d["availability_state"] != AvailabilityState.VERIFIED_AVAILABLE_NOW.value


def test_zone_z8_crop_insurance_governance_decoupling(z8_execution_results):
    """Verify PMFBY (SCH002) is routed to Section B with scoring disabled across all S053–S058 scenarios."""
    for item in z8_execution_results["results"]:
        sid = item["scenario_id"]
        pmfby = next((d for d in item["actionable_determinations"] if d["scheme_id"] == "SCH002"), None)
        assert pmfby is not None, f"PMFBY missing in actionable determinations for {sid}"
        assert pmfby["governance_status"] == "REQUIRES_VERIFICATION"
        assert pmfby["presentation_section"].startswith("Section B")
        assert pmfby["allow_numerical_scoring"] is False
        assert len(pmfby["missing_verifications"]) > 0
        assert any("Insurance Unit" in mv for mv in pmfby["missing_verifications"])


def test_zone_z8_provisional_schemes_quarantined(z8_execution_results):
    """Verify all provisional corporation schemes are quarantined in Section B with scoring disabled."""
    provisional_ids = {"SCH008_KA_COOP", "SCH010_VALMIKI", "SCH010_DEVARAJ_URS", "SCH010_KMDC"}
    for item in z8_execution_results["results"]:
        sid = item["scenario_id"]
        for d in item["actionable_determinations"]:
            if d["scheme_id"] in provisional_ids:
                if d["governance_status"] != "INELIGIBLE":
                    assert d["governance_status"] == "REQUIRES_VERIFICATION", (
                        f"{sid} - {d['scheme_id']}: Provisional scheme must be REQUIRES_VERIFICATION, got {d['governance_status']}"
                    )
                    assert d["presentation_section"].startswith("Section B")
                    assert d["allow_numerical_scoring"] is False


def test_zone_z8_s053_krishi_bhagya_rainwater_harvesting(z8_execution_results, z8_profiles):
    """Verify S053 Medium Minority dryland soybean farmer in Dharwad qualifies for Krishi Bhagya farm pond."""
    s053_res = next(r for r in z8_execution_results["results"] if r["scenario_id"] == "S053")
    acts = {d["scheme_id"]: d for d in s053_res["actionable_determinations"]}

    # Krishi Bhagya qualifies in Section A
    kb = acts["SCH005"]
    assert kb["raw_engine_status"] == "ELIGIBLE"
    assert kb["governance_status"] == "ELIGIBLE"
    assert kb["presentation_section"].startswith("Section A")
    assert kb["allow_numerical_scoring"] is True
    assert "KRISHI_BHAGYA_DRYLAND_VERIFIED" in kb["rule_keys_fired"]
    assert "KRISHI_BHAGYA_DISTRICT_NOTIFIED" in kb["rule_keys_fired"]

    # KMDC individual route exceeds 5.0 ac ceiling -> INELIGIBLE in Disqualified
    kmdc = acts["SCH010_KMDC"]
    assert kmdc["raw_engine_status"] == "INELIGIBLE"
    assert kmdc["governance_status"] == "INELIGIBLE"
    assert kmdc["presentation_section"].startswith("Disqualified")
    assert "GK_SCH010_KMDC_EXCEEDS_5_AC" in kmdc["rule_keys_fired"]

    # Parent SCH010 retained as ineligible umbrella
    assert "SCH010" in acts
    assert acts["SCH010"]["raw_engine_status"] == "INELIGIBLE"

    # Water infrastructure
    p = z8_profiles["S053"]
    assert p["water_and_irrigation"]["borewell_electric_status"] == "NONE"
    assert p["landholding_details"]["physical_area_consistency"].startswith("PASS")


def test_zone_z8_s054_midh_protected_horticulture(z8_execution_results, z8_profiles):
    """Verify S054 SC marginal chilli farmer in Belagavi qualifies for MIDH shade-net in Section A."""
    s054_res = next(r for r in z8_execution_results["results"] if r["scenario_id"] == "S054")
    acts = {d["scheme_id"]: d for d in s054_res["actionable_determinations"]}

    # MIDH shade-net qualifies in Section A
    midh = acts["SCH007"]
    assert midh["raw_engine_status"] == "ELIGIBLE"
    assert midh["governance_status"] == "ELIGIBLE"
    assert midh["presentation_section"].startswith("Section A")
    assert midh["allow_numerical_scoring"] is True
    assert "MIDH_HORTICULTURE_CROP_VERIFIED" in midh["rule_keys_fired"]

    # Krishi Bhagya disqualified due to wetland/valley land type
    kb = acts["SCH005"]
    assert kb["raw_engine_status"] == "INELIGIBLE"
    assert "KRISHI_BHAGYA_NOT_DRYLAND" in kb["rule_keys_fired"]

    # Ganga Kalyana disqualified due to existing borewell
    gk_ambedkar = acts["SCH010_AMBEDKAR"]
    assert gk_ambedkar["raw_engine_status"] == "INELIGIBLE"
    assert "GK_SCH010_AMBEDKAR_EXISTING_BOREWELL" in gk_ambedkar["rule_keys_fired"]

    # PM-KUSUM B disqualified due to grid-connected IP set
    kusum = acts["SCH006"]
    assert kusum["raw_engine_status"] == "INELIGIBLE"
    assert "KUSUM_B_GRID_CONNECTED_DISQUALIFIED" in kusum["rule_keys_fired"]


def test_zone_z8_s055_govt_officer_statutory_exclusion_isolation(z8_execution_results, z8_profiles):
    """Verify S055 regular government officer is strictly excluded from PM-KISAN without spillover."""
    s055_res = next(r for r in z8_execution_results["results"] if r["scenario_id"] == "S055")
    acts = {d["scheme_id"]: d for d in s055_res["actionable_determinations"]}

    # PM-KISAN strictly INELIGIBLE
    pmkisan = acts["SCH001"]
    assert pmkisan["raw_engine_status"] == "INELIGIBLE"
    assert pmkisan["governance_status"] == "INELIGIBLE"
    assert pmkisan["presentation_section"].startswith("Disqualified")
    assert pmkisan["allow_numerical_scoring"] is False
    assert "PMKISAN_REGULAR_OFFICER_EXCLUSION" in pmkisan["rule_keys_fired"]

    # Exclusion is isolated: non-statutorily excluded schemes qualify in Section A
    smam = acts["SCH004"]
    assert smam["governance_status"] == "ELIGIBLE"
    assert smam["presentation_section"].startswith("Section A")

    shc = acts["SCH009"]
    assert shc["governance_status"] == "ELIGIBLE"
    assert shc["presentation_section"].startswith("Section A")

    kb = acts["SCH005"]
    assert kb["governance_status"] == "ELIGIBLE"
    assert kb["presentation_section"].startswith("Section A")


def test_zone_z8_s056_unknown_title_three_valued_logic_governance(z8_execution_results, z8_profiles):
    """Verify S056 with UNKNOWN land title enforces three-valued logic in PM-KISAN and routes title-dependent schemes to Section B."""
    s056_res = next(r for r in z8_execution_results["results"] if r["scenario_id"] == "S056")
    acts = {d["scheme_id"]: d for d in s056_res["actionable_determinations"]}

    # PM-KISAN strictly REQUIRES_VERIFICATION in Section B
    pmkisan = acts["SCH001"]
    assert pmkisan["raw_engine_status"] == "REQUIRES_VERIFICATION"
    assert pmkisan["governance_status"] == "REQUIRES_VERIFICATION"
    assert pmkisan["presentation_section"].startswith("Section B")
    assert pmkisan["allow_numerical_scoring"] is False
    assert "PMKISAN_CUTOFF_DATE_UNKNOWN" in pmkisan["rule_keys_fired"]
    assert any("title record date" in mv for mv in pmkisan["missing_verifications"])

    # Soil Health Card qualifies in Section A as universal diagnostic service
    shc = acts["SCH009"]
    assert shc["raw_engine_status"] == "ELIGIBLE"
    assert shc["governance_status"] == "ELIGIBLE"
    assert shc["presentation_section"].startswith("Section A")
    assert shc["allow_numerical_scoring"] is True

    # Krishi Bhagya title-dependent capital scheme routed to Section B
    kb = acts["SCH005"]
    assert kb["raw_engine_status"] == "ELIGIBLE"
    assert kb["governance_status"] == "REQUIRES_VERIFICATION"
    assert kb["presentation_section"].startswith("Section B")
    assert kb["allow_numerical_scoring"] is False

    # Valmiki Corporation routed to Section B as REQUIRES_VERIFICATION
    gk_valmiki = acts["SCH010_VALMIKI"]
    assert gk_valmiki["raw_engine_status"] == "ELIGIBLE"
    assert gk_valmiki["governance_status"] == "REQUIRES_VERIFICATION"
    assert gk_valmiki["presentation_section"].startswith("Section B")
    assert gk_valmiki["allow_numerical_scoring"] is False

    # Ambedkar Corporation is disqualified by social category mismatch (ST != SC)
    gk_ambedkar = acts["SCH010_AMBEDKAR"]
    assert gk_ambedkar["governance_status"] == "INELIGIBLE"
    assert gk_ambedkar["presentation_section"].startswith("Disqualified")


def test_zone_z8_s057_smam_large_holding_tiered_rates(z8_execution_results, z8_profiles):
    """Verify S057 Large holding (12.0 ac) qualifies for SMAM without blanket large-farmer exclusion."""
    s057_res = next(r for r in z8_execution_results["results"] if r["scenario_id"] == "S057")
    acts = {d["scheme_id"]: d for d in s057_res["actionable_determinations"]}

    # SMAM qualifies in Section A
    smam = acts["SCH004"]
    assert smam["raw_engine_status"] == "ELIGIBLE"
    assert smam["governance_status"] == "ELIGIBLE"
    assert smam["presentation_section"].startswith("Section A")
    assert smam["allow_numerical_scoring"] is True

    # Krishi Bhagya disqualified due to canal irrigation
    kb = acts["SCH005"]
    assert kb["raw_engine_status"] == "INELIGIBLE"
    assert "KRISHI_BHAGYA_NOT_DRYLAND" in kb["rule_keys_fired"]

    # Ganga Kalyana disqualified due to canal command
    gk_parent = acts["SCH010"]
    assert gk_parent["raw_engine_status"] == "INELIGIBLE"


def test_zone_z8_s058_pmksy_pdmc_large_holding_boundary_test(z8_execution_results, z8_profiles):
    """Verify S058 Large holding (12.5 ac) PMKSY-PDMC boundary test at exactly 5.00 ha statutory ceiling."""
    s058_res = next(r for r in z8_execution_results["results"] if r["scenario_id"] == "S058")
    acts = {d["scheme_id"]: d for d in s058_res["actionable_determinations"]}

    # Raw engine determination preserved as INELIGIBLE (PMKSY_LAND_ABOVE_5_HA)
    pdmc = acts["SCH003"]
    assert pdmc["raw_engine_status"] == "INELIGIBLE"
    assert "PMKSY_LAND_ABOVE_5_HA" in pdmc["rule_keys_fired"]

    # Governance presentation qualifies PMKSY-PDMC in Section A at 5.00 ha ceiling
    assert pdmc["governance_status"] == "ELIGIBLE"
    assert pdmc["presentation_section"].startswith("Section A")
    assert pdmc["allow_numerical_scoring"] is True
    assert "5.00 ha" in pdmc["governance_note"]

    # Physical area consistency check
    p = z8_profiles["S058"]
    req_ha = p["landholding_details"]["requested_subsidized_area_ha"]
    qual_ac = p["landholding_details"]["qualifying_parcel_acres"]
    assert req_ha == 5.00, "Requested subsidized area must be exactly 5.00 ha"
    assert req_ha <= (qual_ac * 0.404686), f"Requested {req_ha} ha must not exceed physical parcel {qual_ac} ac"

    # Ganga Kalyana disqualified by existing borewell and General category
    gk_parent = acts["SCH010"]
    assert gk_parent["governance_status"] == "INELIGIBLE"

    # PM-KUSUM B disqualified by grid connection
    kusum = acts["SCH006"]
    assert kusum["governance_status"] == "INELIGIBLE"
    assert "KUSUM_B_GRID_CONNECTED_DISQUALIFIED" in kusum["rule_keys_fired"]


def test_zone_z8_s058_subsidy_history_and_statutory_guidelines_regression(z8_execution_results, z8_profiles):
    """Verify S058 micro-irrigation subsidy history data contract and PMKSY-PDMC 2023 Guidelines §§ 7.9 & 7.10 citations."""
    p = z8_profiles["S058"]
    s058_res = next(r for r in z8_execution_results["results"] if r["scenario_id"] == "S058")
    acts = {d["scheme_id"]: d for d in s058_res["actionable_determinations"]}
    pdmc = acts["SCH003"]

    # 1. Explicit data contract: prior_micro_irrigation_subsidy_years_ago = None declared as EXPLICIT_NO_PRIOR_SUBSIDY
    assert "prior_subsidy_history" in p, "S058 must contain explicit prior_subsidy_history contract"
    psh = p["prior_subsidy_history"]
    assert psh["interpretation"] == "EXPLICIT_NO_PRIOR_SUBSIDY"
    assert psh["prior_micro_irrigation_subsidy_years_ago"] is None
    assert "First-time micro-irrigation applicant" in psh["factual_declaration"]

    # 2. Statutory Guidelines citations in profile
    assert "PMKSY-PDMC Revised Operational Guidelines 2023" in psh["regulatory_framework"]
    assert "Section 7.9" in psh["statutory_clauses"]["section_7_9_area_ceiling"]
    assert "Section 7.10" in psh["statutory_clauses"]["section_7_10_repeat_subsidy_restriction"]

    # 3. Engine rule check: null mapped to PMKSY_NO_PRIOR_SUBSIDY
    assert "PMKSY_NO_PRIOR_SUBSIDY" in pdmc["rule_keys_fired"], (
        "Engine must fire PMKSY_NO_PRIOR_SUBSIDY for confirmed first-time applicant"
    )

    # 4. Governance note citations to Sections 7.9 and 7.10
    gov_note = pdmc["governance_note"]
    assert "Section 7.9" in gov_note
    assert "Section 7.10" in gov_note
    assert "PMKSY-PDMC Revised Operational Guidelines 2023" in gov_note
    assert "first-time applicant status" in gov_note
    assert "7-year" in gov_note
