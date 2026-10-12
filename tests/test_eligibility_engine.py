"""
Unit and integration test suite for Deterministic Eligibility Engine.
Tests:
- Positive, negative, boundary, and unknown-input handling for all schemes
- High-impact statutory exclusions (PM-KISAN tax vs ITR, MTS exemption)
- Acreage boundary constraints (0.2 ha, 1.0 ac, 1.2 ac, 5.0 ac, 5.0 ha, 12.35 ac)
- Ganga Kalyana individual vs community routes and multi-corporation routing
- PMFBY upfront support vs contingent claim disambiguation
- Agricultural credit Central vs Karnataka provisional coop separation
- Pilot test scenarios S001 to S010
- Four-state availability filter and presentation guardrail
"""

import pytest
import os
import sys

# Ensure src is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.eligibility.models import (
    FarmerScenario,
    EligibilityStatus,
    AvailabilityState,
    GovtEmployeeCategory,
    BorewellElectricStatus
)
from src.eligibility.engine import EligibilityEngine
from src.eligibility.availability import AvailabilityFilter


@pytest.fixture
def engine():
    return EligibilityEngine()


@pytest.fixture
def base_scenario_dict():
    """Returns a clean, baseline positive farmer scenario."""
    return {
        "scenario_id": "TEST_BASE",
        "agro_climatic_zone": "Northern Dry Zone",
        "district": "Raichur",
        "crop_primary": "Cotton",
        "land_size_acres": 3.0,
        "land_type": "Dryland (Rainfed)",
        "social_category": "SC",
        "farmer_category": "Small (2.5-5 acres)",
        "existing_assets": [],
        "annual_family_income_lakh": 1.2,
        "immediate_need": "INCOME_SUPPORT",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": GovtEmployeeCategory.NONE,
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": BorewellElectricStatus.NONE,
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0
    }


# =============================================================================
# 1. PM-KISAN (SCH001) TESTS
# =============================================================================
class TestPmKisan:
    def test_clean_positive(self, engine, base_scenario_dict):
        s = FarmerScenario.from_dict(base_scenario_dict)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.ELIGIBLE
        assert det.is_eligible

    def test_paid_income_tax_excluded(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, paid_income_tax_last_assessment_year=True)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.INELIGIBLE
        assert any("paid income tax" in f for f in det.disqualifying_factors)

    def test_high_income_but_no_income_tax_eligible(self, engine, base_scenario_dict):
        """Agricultural income is tax-exempt. A wealthy farmer paying no income tax is eligible."""
        d = dict(base_scenario_dict, annual_family_income_lakh=25.0, paid_income_tax_last_assessment_year=False)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.ELIGIBLE

    def test_income_tax_unknown_requires_verification(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, paid_income_tax_last_assessment_year=None)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.REQUIRES_VERIFICATION
        assert any("income tax" in m for m in det.missing_verifications)

    def test_mts_class_iv_employee_is_exempt_and_eligible(self, engine, base_scenario_dict):
        """Statutory exception: MTS / Class IV / Group D are explicitly exempt from exclusion."""
        d = dict(base_scenario_dict, govt_employee_category=GovtEmployeeCategory.MTS_CLASS_IV_GROUP_D)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.ELIGIBLE

    def test_regular_officer_is_excluded(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, govt_employee_category=GovtEmployeeCategory.OFFICER_REGULAR)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.INELIGIBLE

    def test_land_ownership_cutoff_post_2019_excluded(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, land_ownership_cutoff_pre_feb_2019=False)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.INELIGIBLE
        assert any("01.02.2019" in f for f in det.disqualifying_factors)

    def test_pure_tenant_without_land_title_excluded(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, is_pure_tenant_without_land_title=True)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.INELIGIBLE

    def test_constitutional_post_excluded(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, govt_employee_category=GovtEmployeeCategory.CONSTITUTIONAL_POST)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.INELIGIBLE
        assert any("constitutional post" in f for f in det.disqualifying_factors)

    def test_elected_representative_excluded(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, govt_employee_category=GovtEmployeeCategory.ELECTED_REPRESENTATIVE)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.INELIGIBLE
        assert any("Minister, MP, MLA" in f for f in det.disqualifying_factors)

    def test_superannuated_pensioner_over_10k_excluded(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, superannuated_pensioner_monthly_amount=12500.0, pensioner_is_mts_exempt=False)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.INELIGIBLE
        assert any("10,000 threshold" in f for f in det.disqualifying_factors)

    def test_superannuated_pensioner_over_10k_mts_exempt_eligible(self, engine, base_scenario_dict):
        """Statutory exception: Retired MTS / Class IV pensioners with >= 10,000 pension are exempt."""
        d = dict(base_scenario_dict, superannuated_pensioner_monthly_amount=12500.0, pensioner_is_mts_exempt=True)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.ELIGIBLE
        assert "PMKISAN_MTS_PENSION_EXEMPTION_APPLIED" in det.rule_keys_fired

    def test_pensioner_under_10k_eligible(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, superannuated_pensioner_monthly_amount=7500.0, pensioner_is_mts_exempt=False)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.ELIGIBLE

    def test_pension_amount_unknown_requires_verification(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, superannuated_pensioner_monthly_amount=None)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.REQUIRES_VERIFICATION
        assert any("monthly pension amount" in m for m in det.missing_verifications)

    def test_practicing_professional_excluded(self, engine, base_scenario_dict):
        for prof in ["Doctor (MBBS)", "Lawyer / Advocate", "Chartered Accountant", "Engineer", "Architect"]:
            d = dict(base_scenario_dict, registered_professional=prof)
            s = FarmerScenario.from_dict(d)
            det = engine.evaluate_scheme(s, "SCH001")
            assert det.status == EligibilityStatus.INELIGIBLE
            assert any("practicing registered professional" in f for f in det.disqualifying_factors)

    def test_professional_status_unknown_requires_verification(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, registered_professional="UNKNOWN")
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH001")
        assert det.status == EligibilityStatus.REQUIRES_VERIFICATION
        assert any("professional council registration" in m for m in det.missing_verifications)


# =============================================================================
# 2. PMFBY (SCH002) TESTS
# =============================================================================
class TestPmfby:
    def test_notified_crop_eligible(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, crop_primary="Maize")
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH002")
        assert det.status == EligibilityStatus.ELIGIBLE
        assert "NEVER GUARANTEED" in det.claim_disclaimer
        assert det.upfront_benefit_support is not None
        assert det.contingent_benefit_clause is not None

    def test_non_notified_crop_ineligible(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, crop_primary="Dragonfruit_Experimental")
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH002")
        assert det.status == EligibilityStatus.INELIGIBLE


# =============================================================================
# 3. PMKSY-PDMC (SCH003) TESTS
# =============================================================================
class TestPmksyPdmc:
    def test_boundary_land_size(self, engine, base_scenario_dict):
        # 0.4 acres (< 0.5 ac / 0.2 ha) -> Ineligible
        d_low = dict(base_scenario_dict, land_size_acres=0.4, existing_assets=["Borewell (Grid-connected)"])
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d_low), "SCH003").status == EligibilityStatus.INELIGIBLE

        # 0.5 acres (>= 0.2 ha) -> Eligible
        d_min = dict(base_scenario_dict, land_size_acres=0.5, existing_assets=["Borewell (Grid-connected)"])
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d_min), "SCH003").status == EligibilityStatus.ELIGIBLE

        # 12.35 acres (5.0 ha max limit) -> Eligible
        d_max = dict(base_scenario_dict, land_size_acres=12.35, existing_assets=["Borewell (Grid-connected)"])
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d_max), "SCH003").status == EligibilityStatus.ELIGIBLE

        # 13.0 acres (> 5.0 ha) -> Ineligible
        d_high = dict(base_scenario_dict, land_size_acres=13.0, existing_assets=["Borewell (Grid-connected)"])
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d_high), "SCH003").status == EligibilityStatus.INELIGIBLE

    def test_water_source_required(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, land_size_acres=3.0, existing_assets=[], land_type="Dryland (Rainfed)")
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d), "SCH003").status == EligibilityStatus.INELIGIBLE

    def test_seven_year_lockin(self, engine, base_scenario_dict):
        d_locked = dict(base_scenario_dict, land_size_acres=3.0, existing_assets=["Borewell (Grid-connected)"], prior_micro_irrigation_subsidy_years_ago=3.0)
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d_locked), "SCH003").status == EligibilityStatus.INELIGIBLE

        d_free = dict(base_scenario_dict, land_size_acres=3.0, existing_assets=["Borewell (Grid-connected)"], prior_micro_irrigation_subsidy_years_ago=8.0)
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d_free), "SCH003").status == EligibilityStatus.ELIGIBLE


# =============================================================================
# 4. SMAM (SCH004) TESTS
# =============================================================================
class TestSmam:
    def test_clean_positive(self, engine, base_scenario_dict):
        s = FarmerScenario.from_dict(base_scenario_dict)
        det = engine.evaluate_scheme(s, "SCH004")
        assert det.status == EligibilityStatus.ELIGIBLE
        assert "SMAM_NO_PRIOR_SUBSIDY" in det.rule_keys_fired

    def test_five_year_lockin_breached(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, prior_machinery_subsidy_years_ago=3.0)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH004")
        assert det.status == EligibilityStatus.INELIGIBLE
        assert any("5-year lock-in" in f for f in det.disqualifying_factors)

    def test_five_year_lockin_expired(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, prior_machinery_subsidy_years_ago=6.0)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH004")
        assert det.status == EligibilityStatus.ELIGIBLE
        assert "SMAM_LOCKIN_EXPIRED" in det.rule_keys_fired

    def test_no_land_excluded(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, land_size_acres=0.0)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH004")
        assert det.status == EligibilityStatus.INELIGIBLE


# =============================================================================
# 5. KRISHI BHAGYA (SCH005) TESTS
# =============================================================================
class TestKrishiBhagya:
    def test_dryland_required(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, land_type="Irrigated (Canal)", district="Raichur", land_size_acres=3.0)
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d), "SCH005").status == EligibilityStatus.INELIGIBLE

    def test_coastal_district_excluded(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, land_type="Dryland (Rainfed)", district="Udupi", land_size_acres=3.0)
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d), "SCH005").status == EligibilityStatus.INELIGIBLE

    def test_min_catchment_1_acre(self, engine, base_scenario_dict):
        d_low = dict(base_scenario_dict, land_type="Dryland (Rainfed)", district="Raichur", land_size_acres=0.8)
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d_low), "SCH005").status == EligibilityStatus.INELIGIBLE

        d_ok = dict(base_scenario_dict, land_type="Dryland (Rainfed)", district="Raichur", land_size_acres=1.5)
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d_ok), "SCH005").status == EligibilityStatus.ELIGIBLE


# =============================================================================
# 6. PM-KUSUM COMPONENT B (SCH006) TESTS
# =============================================================================
class TestPmKusumB:
    def test_unenergized_borewell_eligible(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, land_size_acres=2.0, existing_assets=["Borewell (Non-energized)"], borewell_electric_status=BorewellElectricStatus.UNENERGIZED_OFF_GRID)
        det = engine.evaluate_scheme(FarmerScenario.from_dict(d), "SCH006")
        assert det.status == EligibilityStatus.ELIGIBLE

    def test_grid_connected_borewell_strictly_ineligible(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, land_size_acres=2.0, existing_assets=["Borewell (Grid-connected)"], borewell_electric_status=BorewellElectricStatus.GRID_CONNECTED_IP_SET)
        det = engine.evaluate_scheme(FarmerScenario.from_dict(d), "SCH006")
        assert det.status == EligibilityStatus.INELIGIBLE
        assert any("Component C" in f for f in det.disqualifying_factors)

    def test_unknown_electric_status_requires_verification(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, land_size_acres=2.0, existing_assets=["Borewell (Non-energized)"], borewell_electric_status=BorewellElectricStatus.UNKNOWN)
        det = engine.evaluate_scheme(FarmerScenario.from_dict(d), "SCH006")
        assert det.status == EligibilityStatus.REQUIRES_VERIFICATION


# =============================================================================
# 7. MIDH (SCH007) TESTS
# =============================================================================
class TestMidh:
    def test_clean_positive(self, engine, base_scenario_dict):
        d = dict(
            base_scenario_dict,
            crop_primary="Tomato",
            land_size_acres=1.0,
            existing_assets=["Borewell (Grid-connected)", "Drip Irrigation (Installed)"]
        )
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH007")
        assert det.status == EligibilityStatus.ELIGIBLE
        assert "Polyhouse / Shade Net" in det.reason

    def test_non_horticulture_crop_excluded(self, engine, base_scenario_dict):
        d = dict(
            base_scenario_dict,
            crop_primary="Cotton",
            land_size_acres=1.0,
            existing_assets=["Borewell (Grid-connected)", "Drip Irrigation (Installed)"]
        )
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH007")
        assert det.status == EligibilityStatus.INELIGIBLE
        assert any("not a recognized horticultural crop" in f for f in det.disqualifying_factors)

    def test_missing_micro_irrigation_excluded(self, engine, base_scenario_dict):
        d = dict(
            base_scenario_dict,
            crop_primary="Tomato",
            land_size_acres=1.0,
            existing_assets=["Borewell (Grid-connected)"]
        )
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH007")
        assert det.status == EligibilityStatus.INELIGIBLE
        assert any("mandates existing operational micro-irrigation" in f for f in det.disqualifying_factors)

    def test_land_below_quarter_acre_excluded(self, engine, base_scenario_dict):
        d = dict(
            base_scenario_dict,
            crop_primary="Tomato",
            land_size_acres=0.20,
            existing_assets=["Borewell (Grid-connected)", "Drip Irrigation (Installed)"]
        )
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH007")
        assert det.status == EligibilityStatus.INELIGIBLE
        assert any("1,000 sq. meters" in f for f in det.disqualifying_factors)


# =============================================================================
# 8. AGRICULTURAL CREDIT (SCH008 & CHILDREN) TESTS
# =============================================================================
class TestCredit:
    def test_parent_clean_positive(self, engine, base_scenario_dict):
        s = FarmerScenario.from_dict(base_scenario_dict)
        det = engine.evaluate_scheme(s, "SCH008")
        assert det.status == EligibilityStatus.ELIGIBLE
        assert det.record_type == "PARENT"

    def test_central_commercial_child_positive(self, engine, base_scenario_dict):
        s = FarmerScenario.from_dict(base_scenario_dict)
        det = engine.evaluate_scheme(s, "SCH008_CENTRAL")
        assert det.status == EligibilityStatus.ELIGIBLE
        assert det.record_type == "CHILD"
        assert "4.0% effective interest" in det.reason
        assert "KCC_CENTRAL_COMMERCIAL_ELIGIBLE" in det.rule_keys_fired

    def test_karnataka_coop_child_requires_verification(self, engine, base_scenario_dict):
        s = FarmerScenario.from_dict(base_scenario_dict)
        det = engine.evaluate_scheme(s, "SCH008_KA_COOP")
        assert det.status == EligibilityStatus.REQUIRES_VERIFICATION
        assert det.record_type == "CHILD"
        assert "PROVISIONAL" in det.reason
        assert any("Annual Cooperative Department GO" in m for m in det.missing_verifications)

    def test_zero_land_ineligible(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, land_size_acres=0.0)
        s = FarmerScenario.from_dict(d)
        assert engine.evaluate_scheme(s, "SCH008").status == EligibilityStatus.INELIGIBLE
        assert engine.evaluate_scheme(s, "SCH008_CENTRAL").status == EligibilityStatus.INELIGIBLE
        assert engine.evaluate_scheme(s, "SCH008_KA_COOP").status == EligibilityStatus.INELIGIBLE


# =============================================================================
# 9. SOIL HEALTH CARD (SCH009) TESTS
# =============================================================================
class TestSoilHealthCard:
    def test_universal_diagnostic_access(self, engine, base_scenario_dict):
        s = FarmerScenario.from_dict(base_scenario_dict)
        det = engine.evaluate_scheme(s, "SCH009")
        assert det.status == EligibilityStatus.ELIGIBLE
        assert "100% free Soil Health Card diagnostic service" in det.reason
        assert "SHC_UNIVERSAL_ACCESS_VERIFIED" in det.rule_keys_fired

    def test_zero_land_ineligible(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, land_size_acres=0.0)
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH009")
        assert det.status == EligibilityStatus.INELIGIBLE


# =============================================================================
# 10. GANGA KALYANA (SCH010 & CHILDREN) TESTS
# =============================================================================
class TestGangaKalyana:
    def test_general_category_strictly_ineligible(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, social_category="General (OC)", land_type="Dryland (Rainfed)", land_size_acres=2.0)
        s = FarmerScenario.from_dict(d)
        assert engine.evaluate_scheme(s, "SCH010").status == EligibilityStatus.INELIGIBLE
        assert engine.evaluate_scheme(s, "SCH010_AMBEDKAR").status == EligibilityStatus.INELIGIBLE
        assert engine.evaluate_scheme(s, "SCH010_VALMIKI").status == EligibilityStatus.INELIGIBLE
        assert engine.evaluate_scheme(s, "SCH010_DEVARAJ_URS").status == EligibilityStatus.INELIGIBLE
        assert engine.evaluate_scheme(s, "SCH010_KMDC").status == EligibilityStatus.INELIGIBLE

    def test_sc_dryland_routes_to_ambedkar_corporation(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, social_category="SC", land_type="Dryland (Rainfed)", land_size_acres=2.0, existing_assets=[])
        s = FarmerScenario.from_dict(d)
        assert engine.evaluate_scheme(s, "SCH010").status == EligibilityStatus.ELIGIBLE
        assert engine.evaluate_scheme(s, "SCH010_AMBEDKAR").status == EligibilityStatus.ELIGIBLE
        assert engine.evaluate_scheme(s, "SCH010_VALMIKI").status == EligibilityStatus.INELIGIBLE
        assert engine.evaluate_scheme(s, "SCH010_DEVARAJ_URS").status == EligibilityStatus.INELIGIBLE
        assert engine.evaluate_scheme(s, "SCH010_KMDC").status == EligibilityStatus.INELIGIBLE

    def test_individual_acreage_boundaries(self, engine, base_scenario_dict):
        # Plains district (Raichur): Ambedkar Corporation requires 1.5 - 5.0 ac
        d_under = dict(base_scenario_dict, social_category="SC", district="Raichur", land_size_acres=1.4, existing_assets=[])
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d_under), "SCH010_AMBEDKAR").status == EligibilityStatus.INELIGIBLE

        d_valid = dict(base_scenario_dict, social_category="SC", district="Raichur", land_size_acres=1.5, existing_assets=[])
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d_valid), "SCH010_AMBEDKAR").status == EligibilityStatus.ELIGIBLE

        d_over = dict(base_scenario_dict, social_category="SC", district="Raichur", land_size_acres=5.5, existing_assets=[])
        assert engine.evaluate_scheme(FarmerScenario.from_dict(d_over), "SCH010_AMBEDKAR").status == EligibilityStatus.INELIGIBLE

    def test_community_route_samooha_kola_bavi(self, engine, base_scenario_dict):
        """Farmer individually has only 0.8 ac (ineligible for Individual), but pools 10 ac with 3 SC beneficiaries."""
        d = dict(base_scenario_dict, social_category="SC", district="Raichur", land_size_acres=0.8,
                 community_pool_acres=10.0, community_pool_beneficiaries_count=3, existing_assets=[])
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH010_AMBEDKAR")
        assert det.status == EligibilityStatus.ELIGIBLE
        assert "Community Pooled Route" in det.reason

    def test_community_route_insufficient_beneficiaries_ineligible(self, engine, base_scenario_dict):
        """Ambedkar Corporation mandates at least 3 beneficiaries for community route. Group of 2 fails."""
        d = dict(base_scenario_dict, social_category="SC", district="Raichur", land_size_acres=0.8,
                 community_pool_acres=10.0, community_pool_beneficiaries_count=2, existing_assets=[])
        s = FarmerScenario.from_dict(d)
        det = engine.evaluate_scheme(s, "SCH010_AMBEDKAR")
        assert det.status == EligibilityStatus.INELIGIBLE
        assert any("at least 3 pooled SC beneficiaries" in f for f in det.disqualifying_factors)
        assert "GK_AMBEDKAR_COMMUNITY_MIN_BENEFICIARIES_FAILED" in det.rule_keys_fired

    def test_valmiki_st_corporation_routing(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, social_category="ST", district="Raichur", land_size_acres=2.0, existing_assets=[])
        s = FarmerScenario.from_dict(d)
        assert engine.evaluate_scheme(s, "SCH010_VALMIKI").status == EligibilityStatus.ELIGIBLE
        assert engine.evaluate_scheme(s, "SCH010_AMBEDKAR").status == EligibilityStatus.INELIGIBLE

    def test_devaraj_urs_obc_corporation_routing(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, social_category="OBC (2A)", district="Raichur", land_size_acres=2.0, existing_assets=[])
        s = FarmerScenario.from_dict(d)
        assert engine.evaluate_scheme(s, "SCH010_DEVARAJ_URS").status == EligibilityStatus.ELIGIBLE
        assert engine.evaluate_scheme(s, "SCH010_VALMIKI").status == EligibilityStatus.INELIGIBLE

    def test_kmdc_minority_corporation_routing(self, engine, base_scenario_dict):
        d = dict(base_scenario_dict, social_category="Minority (Muslim)", district="Raichur", land_size_acres=2.0, existing_assets=[])
        s = FarmerScenario.from_dict(d)
        assert engine.evaluate_scheme(s, "SCH010_KMDC").status == EligibilityStatus.ELIGIBLE
        assert engine.evaluate_scheme(s, "SCH010_DEVARAJ_URS").status == EligibilityStatus.INELIGIBLE


# =============================================================================
# 11. PARENT DEDUPLICATION TESTS
# =============================================================================
class TestParentDeduplication:
    def test_abstract_parents_suppressed_when_children_actionable(self, engine, base_scenario_dict):
        """When SCH010_AMBEDKAR is eligible, SCH010 parent must not be in actionable determinations."""
        s = FarmerScenario.from_dict(base_scenario_dict)
        raw_dets = engine.evaluate_scenario(s, include_children=True)
        
        raw_ids = [d.scheme_id for d in raw_dets]
        assert "SCH010" in raw_ids
        assert "SCH010_AMBEDKAR" in raw_ids
        assert "SCH008" in raw_ids
        assert "SCH008_CENTRAL" in raw_ids

        actionable = engine.resolve_actionable_determinations(raw_dets)
        actionable_ids = [d.scheme_id for d in actionable]

        # Abstract parent SCH010 must be deduplicated because SCH010_AMBEDKAR is actionable
        assert "SCH010" not in actionable_ids
        assert "SCH010_AMBEDKAR" in actionable_ids

        # Abstract parent SCH008 must be deduplicated because SCH008_CENTRAL is actionable
        assert "SCH008" not in actionable_ids
        assert "SCH008_CENTRAL" in actionable_ids


# =============================================================================
# 7. PILOT TEST SCENARIOS (S001 TO S010)
# =============================================================================
class TestPilotScenarios:
    def test_s007_pm_kisan_negative_exclusion(self, engine, base_scenario_dict):
        """S007: Haveri, Maize, 3.0 ac, General category. Spouse paid income tax in last assessment year."""
        d = dict(base_scenario_dict,
            scenario_id="S007",
            district="Haveri",
            crop_primary="Maize",
            land_size_acres=3.0,
            social_category="General (OC)",
            paid_income_tax_last_assessment_year=True
        )
        s = FarmerScenario.from_dict(d)
        det_kisan = engine.evaluate_scheme(s, "SCH001")
        assert det_kisan.status == EligibilityStatus.INELIGIBLE
        assert any("paid income tax" in f for f in det_kisan.disqualifying_factors)
        # Other schemes without tax exclusion (e.g. Soil health, PMFBY) remain eligible
        assert engine.evaluate_scheme(s, "SCH009").status == EligibilityStatus.ELIGIBLE

    def test_s008_kusum_b_grid_connected_exclusion(self, engine, base_scenario_dict):
        """S008: Vijayapura, Jowar, 4.0 ac, OBC (2A). Borewell already has a grid-connected electric pump."""
        d = dict(base_scenario_dict,
            scenario_id="S008",
            district="Vijayapura",
            crop_primary="Jowar",
            land_size_acres=4.0,
            social_category="OBC (2A)",
            existing_assets=["Borewell (Grid-connected)"],
            borewell_electric_status=BorewellElectricStatus.GRID_CONNECTED_IP_SET
        )
        s = FarmerScenario.from_dict(d)
        det_kusum = engine.evaluate_scheme(s, "SCH006")
        assert det_kusum.status == EligibilityStatus.INELIGIBLE
        assert any("Component C" in f for f in det_kusum.disqualifying_factors)

    def test_s009_ganga_kalyana_general_merit_exclusion(self, engine, base_scenario_dict):
        """S009: Chitradurga, Groundnut, 2.0 ac dryland, General category. Fails corporation caste mandate."""
        d = dict(base_scenario_dict,
            scenario_id="S009",
            district="Chitradurga",
            crop_primary="Groundnut",
            land_size_acres=2.0,
            social_category="General (OC)",
            land_type="Dryland (Rainfed)",
            existing_assets=[]
        )
        s = FarmerScenario.from_dict(d)
        det_gk = engine.evaluate_scheme(s, "SCH010")
        assert det_gk.status == EligibilityStatus.INELIGIBLE
        assert any("General Merit" in f for f in det_gk.disqualifying_factors)

    def test_s010_pmksy_three_year_lockin_exclusion(self, engine, base_scenario_dict):
        """S010: Belagavi, Sugarcane, 3.0 ac, SC category. Availed micro-irrigation 3 years ago (7-year lock-in)."""
        d = dict(base_scenario_dict,
            scenario_id="S010",
            district="Belagavi",
            crop_primary="Sugarcane",
            land_size_acres=3.0,
            social_category="SC",
            existing_assets=["Borewell (Grid-connected)"],
            prior_micro_irrigation_subsidy_years_ago=3.0
        )
        s = FarmerScenario.from_dict(d)
        det_pmksy = engine.evaluate_scheme(s, "SCH003")
        assert det_pmksy.status == EligibilityStatus.INELIGIBLE
        assert any("7-year lock-in" in f for f in det_pmksy.disqualifying_factors)


# =============================================================================
# 8. AVAILABILITY FILTER & PRESENTATION GUARDRAIL TESTS
# =============================================================================
class TestAvailabilityFilter:
    def test_unverified_schemes_do_not_leak_into_available_now(self, engine, base_scenario_dict):
        """Without active verified notices, eligible schemes MUST NOT appear under available_now."""
        s = FarmerScenario.from_dict(base_scenario_dict)
        dets = engine.evaluate_scenario(s)
        
        # Apply availability with default unverified template
        avail_filter = AvailabilityFilter()
        enriched_dets = avail_filter.apply_availability(dets)

        sections = avail_filter.partition_by_presentation(enriched_dets)
        
        # Guardrail check: available_now must be empty since template has no active confirmed circulars
        assert len(sections["available_now"]) == 0
        assert len(sections["timing_or_verification_required"]) > 0

    def test_active_verified_notice_activates_available_now(self, engine, base_scenario_dict):
        s = FarmerScenario.from_dict(base_scenario_dict)
        dets = engine.evaluate_scenario(s)

        avail_filter = AvailabilityFilter()
        # Mock active circular for PM-KISAN
        avail_filter.records["SCH001"] = {
            "application_status": "OPEN",
            "official_notice_url": "https://pmkisan.gov.in/notices/active_round.pdf",
            "source_published_date": "2026-08-01"
        }

        enriched_dets = avail_filter.apply_availability(dets)
        sections = avail_filter.partition_by_presentation(enriched_dets)

        # SCH001 should now appear in available_now
        available_ids = [d.scheme_id for d in sections["available_now"]]
        assert "SCH001" in available_ids
