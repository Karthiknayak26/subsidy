"""
Unit test for Benchmark v1.0.4 Scenario Assignment Matrix.
Validates all 8 quota and boundary dimensions plus statutory succession definitions:
1. Scenario count and ID continuity (60 scenarios, S011-S070)
2. Agro-climatic zone distribution (10 zones, 6 each)
3. Landholding classes (22 Marginal, 20 Small, 12 Medium, 6 Large) and exact boundaries
4. Social categories (15 SC, 10 ST, 10 OBC, 8 Minority, 17 GM)
5. Primary needs (6 each across 10 categories)
6. Tenure statuses (47 Pre-Feb 2019, 4 Post-Feb 2019 Inheritance, 5 Pure Tenant, 4 Unknown Title Status)
7. Statutory succession vs. partition definition verification for post-Feb 2019 inheritance (S039, S049, S064, S069)
8. Community pool membership (3 Yes: S028, S052, S066; 57 No)
9. Land types (28 Dryland, 10 Canal-irrigated, 12 Borewell-irrigated, 6 Wetland/valley, 4 Hilly/terraced)
"""

import os
import sys
import json
import pytest

sys.path.insert(0, os.path.abspath("."))
from research.dataset_research.validate_benchmark_matrix import scenarios, validate_matrix
from research.dataset_research.validate_benchmark_artifacts import validate_all_benchmark_artifacts
from src.eligibility.models import SchemeDetermination, EligibilityStatus
from src.eligibility.governance import (
    apply_inheritance_succession_safeguard,
    apply_governance_safeguard
)


def test_benchmark_matrix_all_dimensions():
    """Verify that the benchmark v1.0.4 matrix satisfies all declared quotas and statutory rules."""
    success = validate_matrix(scenarios)
    assert success is True, "Benchmark v1.0.4 assignment matrix failed one or more quota checks."


def test_boundary_cases_preserved():
    """Verify explicit boundary test cases are present and classified correctly."""
    # 2.5 acre boundary -> Small (>= 2.5 and <= 5.0)
    boundary_2_5 = [s for s in scenarios if s["total_holding"] == 2.5]
    assert len(boundary_2_5) >= 3, f"Expected >= 3 boundary test cases at 2.5 acres, found {len(boundary_2_5)}"
    for s in boundary_2_5:
        assert s["lclass"] == "Small", f"{s['sid']} at 2.5 ac must be classified Small"

    # 5.0 acre boundary -> Small (>= 2.5 and <= 5.0)
    boundary_5_0 = [s for s in scenarios if s["total_holding"] == 5.0]
    assert len(boundary_5_0) >= 2, f"Expected >= 2 boundary test cases at 5.0 acres, found {len(boundary_5_0)}"
    for s in boundary_5_0:
        assert s["lclass"] == "Small", f"{s['sid']} at 5.0 ac must be classified Small"

    # 10.0 acre boundary -> Medium (> 5.0 and <= 10.0)
    boundary_10_0 = [s for s in scenarios if s["total_holding"] == 10.0]
    assert len(boundary_10_0) >= 1, f"Expected >= 1 boundary test cases at 10.0 acres, found {len(boundary_10_0)}"
    for s in boundary_10_0:
        assert s["lclass"] == "Medium", f"{s['sid']} at 10.0 ac must be classified Medium"


def test_community_pool_clarifications():
    """Verify S028, S052, S066 community pool attributes and provisional status labeling."""
    pool_scenarios = {s["sid"]: s for s in scenarios if s["pool"].startswith("Yes")}
    assert set(pool_scenarios.keys()) == {"S028", "S052", "S066"}

    # S028: Devaraj Urs (OBC) provisional
    s028 = pool_scenarios["S028"]
    assert s028["social"] == "OBC"
    assert "Devaraj Urs" in s028["policy"]
    assert "REQUIRES_VERIFICATION" in s028["policy"]
    assert s028["qual_parcel"] == 3.0
    assert "9.0 ac" in s028["pool"]

    # S052: Devaraj Urs (OBC) provisional
    s052 = pool_scenarios["S052"]
    assert s052["social"] == "OBC"
    assert "Devaraj Urs" in s052["policy"]
    assert "REQUIRES_VERIFICATION" in s052["policy"]
    assert s052["qual_parcel"] == 4.0
    assert "12.0 ac" in s052["pool"]

    # S066: Ambedkar (SC)
    s066 = pool_scenarios["S066"]
    assert s066["social"] == "SC"
    assert "Ambedkar" in s066["policy"]
    assert s066["qual_parcel"] == 3.5
    assert "14.0 ac" in s066["pool"]


def test_cross_field_subsidized_area_within_qualifying_parcel():
    """Verify requested subsidized area (ha) never exceeds qualifying parcel (converted to ha)."""
    ha_per_acre = 0.40468564224
    subsidized_cases = [s for s in scenarios if s["subsidized_ha"] != "—"]
    assert len(subsidized_cases) == 6, f"Expected 6 subsidized area boundary cases, found {len(subsidized_cases)}"

    for s in subsidized_cases:
        req_ha = float(s["subsidized_ha"])
        max_phys_ha = s["qual_parcel"] * ha_per_acre
        assert req_ha <= (max_phys_ha + 1e-4), (
            f"Cross-field failure in {s['sid']}: requested {req_ha} ha exceeds "
            f"qualifying parcel {s['qual_parcel']} ac ({max_phys_ha:.4f} ha)"
        )


def test_solar_pump_scenario_prerequisites():
    """Verify that all 6 solar pump scenarios specify explicit water-source and electric status."""
    solar_scenarios = [s for s in scenarios if s["need"] == "SOLAR_PUMP_INSTALLATION"]
    assert len(solar_scenarios) == 6
    expected_sids = {"S012", "S020", "S024", "S030", "S051", "S063"}
    assert set(s["sid"] for s in solar_scenarios) == expected_sids

    for s in solar_scenarios:
        assert s.get("water_source") and s["water_source"] != "Rainfed (None)", (
            f"{s['sid']} must have explicit operational water source"
        )
        assert s.get("electric_status"), f"{s['sid']} must have explicit electric status"

        if s["sid"] == "S020":
            # Three-valued logic test: electric status UNKNOWN must trigger REQUIRES_VERIFICATION
            assert s["electric_status"] == "UNKNOWN"
            assert "REQUIRES_VERIFICATION" in s["policy"]
        else:
            # Off-grid standalone solar pump must be UNENERGIZED_OFF_GRID
            assert s["electric_status"] == "UNENERGIZED_OFF_GRID"
            assert "UNENERGIZED_OFF_GRID" in s["policy"]


def test_post_feb_2019_statutory_succession_definitions():
    """Verify that all 4 post-Feb 2019 inheritance scenarios (S039, S049, S064, S069)
    explicitly model statutory succession upon death/demise and distinguish from partition deeds (v1.0.4)."""
    inherit_scenarios = [s for s in scenarios if s["tenure"] == "Post-Feb 2019 Inheritance"]
    assert len(inherit_scenarios) == 4
    assert [s["sid"] for s in inherit_scenarios] == ["S039", "S049", "S064", "S069"]
    for s in inherit_scenarios:
        pol = s["policy"].lower()
        assert "death" in pol or "demise" in pol, f"{s['sid']} policy must mention death/demise of landowner"
        assert "partition" in pol or "distinct from" in pol, f"{s['sid']} policy must distinguish from partition deeds"


def test_benchmark_artifacts_integrity():
    """
    Verify that all 60 committed scenario profiles and execution results on disk
    meet benchmark v1.0.4 integrity requirements:
    - 60/60 profiles declare v1.0.4 and match assignment matrix attributes.
    - All 10 zone batch files and execution results declare v1.0.4 with uniform governance schema.
    - S039, S049, S064, S069 have structured succession details referencing §§5.2-5.3.3(i) vs §5.3.3(ii).
    - Section A has allow_numerical_scoring=True; Section B & Disqualified have allow_numerical_scoring=False.
    - Parent deduplication suppresses SCH008 across all scenarios, and SCH010 when corporation child is actionable.
    """
    success, errors = validate_all_benchmark_artifacts()
    assert success is True, (
        f"Benchmark v1.0.4 committed artifacts integrity failed with {len(errors)} error(s):\n"
        + "\n".join(errors[:20])
    )


@pytest.mark.parametrize("sid,zone", [
    ("S039", "z5"),
    ("S049", "z7"),
    ("S064", "z9"),
    ("S069", "z10")
])
def test_inheritance_safeguard_strict_status_precedence(sid, zone):
    """
    Verify across all 4 inheritance scenarios (S039, S049, S064, S069) that:
    1. Valid succession documents CANNOT override an unrelated statutory disqualification
       (e.g., income tax payer, constitutional post, government employee, pension >= 10k,
       registered professional, pure tenant).
    2. Valid succession documents CANNOT override unresolved engine conditions (REQUIRES_VERIFICATION).
    3. Non-qualifying transfer types (POST_CUTOFF_PARTITION, SALE_DEED, GIFT_DEED) are routed to Disqualified under §5.3.3(ii).
    4. Incomplete succession evidence (missing death cert or mutation extract) routes to Section B as REQUIRES_VERIFICATION.
    5. Clean succession with raw ELIGIBLE routes to Section A with allow_numerical_scoring=True.
    """
    profile_path = os.path.join(".", "data", "benchmarks", zone, f"{sid}.json")
    with open(profile_path, "r", encoding="utf-8") as f:
        profile = json.load(f)

    ssd = profile["statutory_succession_details"]

    # 1. Negative Test: Raw engine is INELIGIBLE due to statutory exclusion (e.g. Income Tax Payer)
    det_disq = SchemeDetermination(
        scheme_id="SCH001",
        scheme_name="Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        status=EligibilityStatus.INELIGIBLE,
        reason="Disqualified by Income Tax Payer exclusion",
        disqualifying_factors=["PMKISAN_INCOME_TAX_PAYER_EXCLUSION: Applicant paid income tax in last assessment year"],
        missing_verifications=[],
        rule_keys_fired=["PMKISAN_INCOME_TAX_PAYER_EXCLUSION"],
        record_type="STANDALONE",
        parent_scheme_id=None
    )
    res_disq = apply_governance_safeguard(det_disq, sid, profile, False)
    assert res_disq["governance_status"] == "INELIGIBLE", f"{sid}: Valid succession must not override statutory ineligibility"
    assert res_disq["presentation_section"].startswith("Disqualified"), f"{sid}: Disqualified status must route to Disqualified section"
    assert res_disq["allow_numerical_scoring"] is False, f"{sid}: Numerical scoring must be disabled for disqualified"
    assert any("PMKISAN_INCOME_TAX_PAYER_EXCLUSION" in df for df in res_disq["disqualifying_factors"])

    # 2. Negative Test: Raw engine is INELIGIBLE due to Government Employee exclusion
    det_govt = SchemeDetermination(
        scheme_id="SCH001",
        scheme_name="Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        status=EligibilityStatus.INELIGIBLE,
        reason="Disqualified by Government Employee exclusion",
        disqualifying_factors=["PMKISAN_GOVT_EMPLOYEE_EXCLUSION: Applicant is Group A officer"],
        missing_verifications=[],
        rule_keys_fired=["PMKISAN_GOVT_EMPLOYEE_EXCLUSION"],
        record_type="STANDALONE",
        parent_scheme_id=None
    )
    res_govt = apply_governance_safeguard(det_govt, sid, profile, False)
    assert res_govt["governance_status"] == "INELIGIBLE"
    assert res_govt["presentation_section"].startswith("Disqualified")
    assert res_govt["allow_numerical_scoring"] is False

    # 3. Negative Test: Raw engine has unresolved condition (REQUIRES_VERIFICATION)
    det_unresolved = SchemeDetermination(
        scheme_id="SCH001",
        scheme_name="Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        status=EligibilityStatus.REQUIRES_VERIFICATION,
        reason="Unresolved land record verification",
        disqualifying_factors=[],
        missing_verifications=["Revenue land ownership record clarification required"],
        rule_keys_fired=[],
        record_type="STANDALONE",
        parent_scheme_id=None
    )
    res_unresolved = apply_governance_safeguard(det_unresolved, sid, profile, False)
    assert res_unresolved["governance_status"] == "REQUIRES_VERIFICATION"
    assert res_unresolved["presentation_section"].startswith("Section B")
    assert res_unresolved["allow_numerical_scoring"] is False

    # 4. Negative Test: Non-qualifying transfer types under §5.3.3(ii)
    for bad_transfer in ["POST_CUTOFF_PARTITION", "SALE_DEED", "GIFT_DEED"]:
        bad_profile = json.loads(json.dumps(profile))
        bad_profile["statutory_succession_details"]["transfer_basis"] = bad_transfer
        det_clean = SchemeDetermination(
            scheme_id="SCH001",
            scheme_name="Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
            status=EligibilityStatus.ELIGIBLE,
            reason="Qualifies for PM-KISAN",
            disqualifying_factors=[],
            missing_verifications=[],
            rule_keys_fired=["PMKISAN_LAND_SIZE_POSITIVE", "PMKISAN_CUTOFF_DATE_VERIFIED"],
            record_type="STANDALONE",
            parent_scheme_id=None
        )
        res_bad_transfer = apply_governance_safeguard(det_clean, sid, bad_profile, False)
        assert res_bad_transfer["governance_status"] == "INELIGIBLE", f"{sid} with {bad_transfer} must be INELIGIBLE"
        assert res_bad_transfer["presentation_section"].startswith("Disqualified")
        assert res_bad_transfer["allow_numerical_scoring"] is False
        assert any("5.3.3(ii)" in df for df in res_bad_transfer["disqualifying_factors"])

    # 5. Negative Test: Missing succession evidence -> Section B
    missing_docs_profile = json.loads(json.dumps(profile))
    missing_docs_profile["statutory_succession_details"]["death_certificate_number"] = ""
    res_missing = apply_governance_safeguard(det_clean, sid, missing_docs_profile, False)
    assert res_missing["governance_status"] == "REQUIRES_VERIFICATION"
    assert res_missing["presentation_section"].startswith("Section B")
    assert res_missing["allow_numerical_scoring"] is False

    # 6. Positive Test: Clean genuine succession with raw ELIGIBLE -> Section A
    res_clean = apply_governance_safeguard(det_clean, sid, profile, False)
    assert res_clean["governance_status"] == "ELIGIBLE"
    assert res_clean["presentation_section"].startswith("Section A")
    assert res_clean["allow_numerical_scoring"] is True



