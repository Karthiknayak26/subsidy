"""
Pilot Execution Runner for Scenarios S001 to S010.
Executes scenarios through EligibilityEngine and AvailabilityFilter.
Enforces parent-child deduplication and outputs execution details for Deliverables A & B.
"""

import os
import sys
import json
from typing import List, Dict, Any

# Ensure src is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.eligibility.models import (
    FarmerScenario,
    EligibilityStatus,
    AvailabilityState,
    GovtEmployeeCategory,
    BorewellElectricStatus,
    SchemeDetermination
)
from src.eligibility.engine import EligibilityEngine
from src.eligibility.availability import AvailabilityFilter

PILOT_SCENARIOS: List[Dict[str, Any]] = [
    {
        "scenario_id": "S001",
        "agro_climatic_zone": "Northern Dry Zone",
        "district": "Raichur",
        "crop_primary": "Cotton",
        "crop_secondary": "Redgram",
        "land_size_acres": 3.0,
        "land_type": "Dryland (Rainfed)",
        "social_category": "SC",
        "farmer_category": "Small (2.5-5 acres)",
        "existing_assets": [],
        "annual_family_income_lakh": 1.2,
        "immediate_need": "CROP_INSURANCE",
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
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Standing Crop / Pre-Harvest",
        "season": "Kharif 2026",
        "kcc_query_text_example": "Cotton crop suffering pink bollworm attack in Raichur, need compensation claim or insurance procedure."
    },
    {
        "scenario_id": "S002",
        "agro_climatic_zone": "Central Dry Zone",
        "district": "Haveri",
        "crop_primary": "Maize",
        "crop_secondary": None,
        "land_size_acres": 2.0,
        "land_type": "Dryland (Rainfed)",
        "social_category": "OBC (2A)",
        "farmer_category": "Marginal (< 2.5 acres)",
        "existing_assets": ["Borewell (Non-energized)"],
        "annual_family_income_lakh": 1.5,
        "immediate_need": "SOLAR_PUMP_INSTALLATION",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": GovtEmployeeCategory.NONE,
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": BorewellElectricStatus.UNENERGIZED_OFF_GRID,
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Pre-Sowing / Land Preparation",
        "season": "Kharif 2026",
        "kcc_query_text_example": "Have drilled borewell without electricity connection in Haveri, need solar motor pump subsidy subsidy details."
    },
    {
        "scenario_id": "S003",
        "agro_climatic_zone": "Southern Dry Zone",
        "district": "Tumakuru",
        "crop_primary": "Ragi",
        "crop_secondary": None,
        "land_size_acres": 1.5,
        "land_type": "Dryland (Rainfed)",
        "social_category": "General (OC)",
        "farmer_category": "Marginal (< 2.5 acres)",
        "existing_assets": [],
        "annual_family_income_lakh": 1.8,
        "immediate_need": "RAINWATER_HARVESTING",
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
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Pre-Sowing",
        "season": "Kharif 2026",
        "kcc_query_text_example": "Dryland ragi farmer in Tumakuru wanting to dig farm pond (krishi honda) with polythene lining for rainwater storage."
    },
    {
        "scenario_id": "S004",
        "agro_climatic_zone": "Southern Transition Zone",
        "district": "Dharwad",
        "crop_primary": "Soybean",
        "crop_secondary": "Maize",
        "land_size_acres": 4.0,
        "land_type": "Irrigated (Borewell)",
        "social_category": "OBC (3B)",
        "farmer_category": "Small (2.5-5 acres)",
        "existing_assets": ["Borewell (Grid-connected)", "Electric Pump Set"],
        "annual_family_income_lakh": 2.5,
        "immediate_need": "MICRO_IRRIGATION_SUPPORT",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": GovtEmployeeCategory.NONE,
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": BorewellElectricStatus.GRID_CONNECTED_IP_SET,
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Vegetative Growth",
        "season": "Kharif 2026",
        "kcc_query_text_example": "Borewell discharge depleting in Dharwad, want to install drip irrigation line for soybean and maize."
    },
    {
        "scenario_id": "S005",
        "agro_climatic_zone": "Eastern Dry Zone",
        "district": "Kolar",
        "crop_primary": "Tomato",
        "crop_secondary": "Capsicum",
        "land_size_acres": 1.0,
        "land_type": "Irrigated (Borewell)",
        "social_category": "OBC (3A)",
        "farmer_category": "Marginal (< 2.5 acres)",
        "existing_assets": ["Borewell (Grid-connected)", "Drip Irrigation (Installed)"],
        "annual_family_income_lakh": 3.0,
        "immediate_need": "PROTECTED_HORTICULTURE",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": GovtEmployeeCategory.NONE,
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": BorewellElectricStatus.GRID_CONNECTED_IP_SET,
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Nursery / Transplanting",
        "season": "Rabi 2026-27",
        "kcc_query_text_example": "Seeking subsidy subsidy for naturally ventilated polyhouse structure of 1000 square meters for high value capsicum in Kolar."
    },
    {
        "scenario_id": "S006",
        "agro_climatic_zone": "Southern Dry Zone",
        "district": "Mysuru",
        "crop_primary": "Paddy",
        "crop_secondary": None,
        "land_size_acres": 2.5,
        "land_type": "Irrigated (Canal)",
        "social_category": "General (OC)",
        "farmer_category": "Small (2.5-5 acres)",
        "existing_assets": [],
        "annual_family_income_lakh": 2.0,
        "immediate_need": "PRODUCTION_CREDIT",
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
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Pre-Sowing / Input Procurement",
        "season": "Kharif 2026",
        "kcc_query_text_example": "Need crop loan / Kisan Credit Card through bank branch for paddy seeds and fertilizer inputs in Mysuru."
    },
    {
        "scenario_id": "S007",
        "agro_climatic_zone": "Central Dry Zone",
        "district": "Haveri",
        "crop_primary": "Maize",
        "crop_secondary": None,
        "land_size_acres": 3.0,
        "land_type": "Dryland (Rainfed)",
        "social_category": "General (OC)",
        "farmer_category": "Small (2.5-5 acres)",
        "existing_assets": [],
        "annual_family_income_lakh": 2.2,
        "immediate_need": "INCOME_SUPPORT",
        "paid_income_tax_last_assessment_year": True,  # Disqualifying flag
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
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Sowing",
        "season": "Kharif 2026",
        "kcc_query_text_example": "Enquiring about PM-KISAN installment payment status. Family member paid income tax last year."
    },
    {
        "scenario_id": "S008",
        "agro_climatic_zone": "Northern Dry Zone",
        "district": "Vijayapura",
        "crop_primary": "Jowar",
        "crop_secondary": None,
        "land_size_acres": 4.0,
        "land_type": "Dryland (Rainfed)",
        "social_category": "OBC (2A)",
        "farmer_category": "Small (2.5-5 acres)",
        "existing_assets": ["Borewell (Grid-connected)"],
        "annual_family_income_lakh": 1.8,
        "immediate_need": "SOLAR_PUMP_INSTALLATION",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": GovtEmployeeCategory.NONE,
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": BorewellElectricStatus.GRID_CONNECTED_IP_SET,  # Disqualifying for Kusum B
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Pre-Sowing",
        "season": "Rabi 2026-27",
        "kcc_query_text_example": "Already have electric grid motor on borewell in Vijayapura, want to apply for standalone solar pump subsidy."
    },
    {
        "scenario_id": "S009",
        "agro_climatic_zone": "Central Dry Zone",
        "district": "Chitradurga",
        "crop_primary": "Groundnut",
        "crop_secondary": None,
        "land_size_acres": 2.0,
        "land_type": "Dryland (Rainfed)",
        "social_category": "General (OC)",  # Disqualifying for Ganga Kalyana
        "farmer_category": "Marginal (< 2.5 acres)",
        "existing_assets": [],
        "annual_family_income_lakh": 1.4,
        "immediate_need": "BOREWELL_IRRIGATION",
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
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Pre-Sowing",
        "season": "Kharif 2026",
        "kcc_query_text_example": "Dryland farmer in Chitradurga seeking 100% free government borewell under Ganga Kalyana scheme."
    },
    {
        "scenario_id": "S010",
        "agro_climatic_zone": "Northern Dry Zone",
        "district": "Belagavi",
        "crop_primary": "Sugarcane",
        "crop_secondary": None,
        "land_size_acres": 3.0,
        "land_type": "Irrigated (Borewell)",
        "social_category": "SC",
        "farmer_category": "Small (2.5-5 acres)",
        "existing_assets": ["Borewell (Grid-connected)"],
        "annual_family_income_lakh": 2.8,
        "immediate_need": "MICRO_IRRIGATION_SUPPORT",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": GovtEmployeeCategory.NONE,
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": BorewellElectricStatus.GRID_CONNECTED_IP_SET,
        "prior_micro_irrigation_subsidy_years_ago": 3.0,  # Disqualifying flag (7-year lock-in breached)
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Vegetative Growth",
        "season": "Kharif 2026",
        "kcc_query_text_example": "Availed drip subsidy 3 years ago in Belagavi, want replacement drip system subsidy for sugarcane."
    }
]


def run_pilot():
    engine = EligibilityEngine()
    avail_filter = AvailabilityFilter()

    results = []

    print("=" * 80)
    print("PILOT EXECUTION OF SCENARIOS S001 TO S010")
    print("=" * 80)

    for sc_dict in PILOT_SCENARIOS:
        scenario = FarmerScenario.from_dict(sc_dict)
        raw_dets = engine.evaluate_scenario(scenario, include_children=True)
        enriched_dets = avail_filter.apply_availability(raw_dets)
        actionable_dets = engine.resolve_actionable_determinations(enriched_dets)

        # Check deduplication
        raw_ids = [d.scheme_id for d in enriched_dets]
        act_ids = [d.scheme_id for d in actionable_dets]

        dedup_occurred = (set(raw_ids) != set(act_ids))
        suppressed_ids = set(raw_ids) - set(act_ids)

        eligible_count = sum(1 for d in actionable_dets if d.status == EligibilityStatus.ELIGIBLE)
        ineligible_count = sum(1 for d in actionable_dets if d.status == EligibilityStatus.INELIGIBLE)
        req_verif_count = sum(1 for d in actionable_dets if d.status == EligibilityStatus.REQUIRES_VERIFICATION)

        print(f"\nScenario {scenario.scenario_id} ({scenario.district}, {scenario.crop_primary}, {scenario.land_size_acres} ac, {scenario.social_category}):")
        print(f"  Immediate Need: {scenario.immediate_need}")
        print(f"  Raw Determinations: {len(raw_dets)} | Actionable Recommendations: {len(actionable_dets)}")
        if dedup_occurred:
            print(f"  [DEDUPLICATION PASSED] Suppressed abstract parent records: {list(suppressed_ids)}")
        print(f"  Status Summary -> ELIGIBLE: {eligible_count} | INELIGIBLE: {ineligible_count} | REQUIRES_VERIFICATION: {req_verif_count}")

        scenario_res = {
            "scenario": sc_dict,
            "raw_determinations": [
                {
                    "scheme_id": d.scheme_id,
                    "scheme_name": d.scheme_name,
                    "record_type": d.record_type,
                    "parent_scheme_id": d.parent_scheme_id,
                    "status": d.status.value,
                    "reason": d.reason,
                    "disqualifying_factors": d.disqualifying_factors,
                    "missing_verifications": d.missing_verifications,
                    "rule_keys_fired": d.rule_keys_fired,
                    "availability_state": d.availability_state.value,
                    "is_actionable": (d.scheme_id in act_ids)
                }
                for d in enriched_dets
            ],
            "actionable_determinations": [
                {
                    "scheme_id": d.scheme_id,
                    "scheme_name": d.scheme_name,
                    "record_type": d.record_type,
                    "parent_scheme_id": d.parent_scheme_id,
                    "status": d.status.value,
                    "reason": d.reason,
                    "rule_keys_fired": d.rule_keys_fired,
                    "missing_verifications": d.missing_verifications,
                    "availability_state": d.availability_state.value
                }
                for d in actionable_dets
            ]
        }
        results.append(scenario_res)

    # Save to JSON
    output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "research", "dataset_research", "pilot_execution_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nExecution complete. Saved structured JSON results to {output_path}")
    return results


if __name__ == "__main__":
    run_pilot()
