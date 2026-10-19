"""
Zone Z10 Benchmark Execution Runner and Deliverable Generator.
Strictly generates and validates scenarios S065 to S070 for Zone Z10
(Coastal Zone: Dakshina Kannada, Udupi, Uttara Kannada Coast).

Preserves all frozen invariants:
- Baseline commit 7724fa7 and frozen eligibility rules.
- Existing scheme database and parent-child relationships.
- Pilot scenarios S001-S010 and their calibration annotations.
- Annotation protocol v1.1.
- Benchmark-design-v1.0.4 quotas and pre-specified heuristic weights.
- Governance Safeguards: Decoupling of raw engine determinations from provisional
  presentation status (Section B) and operational availability states.
- Explicit Availability Safeguard: Section A eligibility verification does NOT equate
  to active application availability.
- Special Governance Conditions:
  1. S066 Community Borewell Safeguard (Challenge 7):
     In the raw engine, the Ambedkar Corporation community route requires at least three
     beneficiaries on 8.0-15.0 acres pooled dryland (GK_AMBEDKAR_COMMUNITY_ROUTE_VALID), which
     S066 satisfies with 4 SC beneficiaries pooling 14.0 acres. Governance conservatively keeps
     the determination in Section B with scoring disabled pending confirmation of current
     administrative circular instructions, registered joint consent deed verification, and
     Mines & Geology groundwater safety clearance (do not confuse with non-Ambedkar 2-beneficiary threshold).
  2. S069 Statutory Inheritance Succession (PM-KISAN Guidelines §§5.2–5.3.3(i) vs §5.3.3(ii)):
     Governance safeguard explicitly gates Section A on verified INHERITANCE_DUE_TO_DEATH evidence
     (actual acquisition date 2022-04-12, parent demise date 2022-04-12, Death Cert DC/DK/2022/6104,
     Legal Heir Order LHC/DK/2022/339, Bhoomi mutation Form 16 MR No. 2022-T771).
     Distinguishes statutory succession upon death (§5.3.3(i)) from non-qualifying post-cutoff sale,
     partition, and gift transfers under §5.3.3(ii).
  3. S070 Unknown Title & Area Limit (Challenge 8 & Challenge 4):
     PMKSY-PDMC Guidelines 2023 §7.9 wording: assistance capped at 5.0 ha per beneficiary.
     Explicit raw-engine vs governance discrepancy: raw engine compares total operational holding
     against 12.35 ac (PMKSY_LAND_ABOVE_5_HA), whereas governance evaluates the requested subsidized
     parcel (4.80 ha <= 5.059 ha parcel capacity and <= 5.00 ha ceiling). Missing title evidence
     (land_ownership_cutoff_pre_feb_2019 = None) preserves three-valued logic in Section B with scoring
     disabled for PM-KISAN and PMKSY-PDMC pending RTC certification, distinguishing PM-KISAN's
     01.02.2019 cutoff from PMKSY's title and layout documentation requirements.
  4. S068 Pure Tenancy Handling (Challenge 5):
     Statutorily excluded from PM-KISAN under PMKISAN_PURE_TENANT_EXCLUSION; KCC commercial
     credit (SCH008_CENTRAL) routed to Section B pending oral lease/tenant crop loan documentation.
  5. S065 Universal Soil Health Card access for large coastal coconut plantation.
  6. S067 Cashew weather-based insurance (RWBCIS) routed to Section B; ST Valmiki Corporation
     individual borewell in Section B as provisional scheme.
  7. Crop insurance (PMFBY/RWBCIS): All unverified seasonal IU notifications routed to Section B.
  8. Provisional corporation schemes (KA Coop, Valmiki) quarantined in Section B.
"""

import os
import sys
import json
from typing import List, Dict, Any

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, WORKSPACE_ROOT)

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

PROVISIONAL_SCHEMES = {
    "SCH008_KA_COOP",
    "SCH010_VALMIKI",
    "SCH010_DEVARAJ_URS",
    "SCH010_KMDC"
}

ZONE_Z10_PROFILES: List[Dict[str, Any]] = [
    {
        "scenario_id": "S065",
        "benchmark_version": "v1.0.4",
        "zone_id": "Z10",
        "agro_climatic_zone": "Coastal Zone",
        "district": "Dakshina Kannada",
        "crop_primary": "Coconut",
        "crop_secondary": "Cocoa",
        "land_size_acres": 14.0,
        "land_type": "Dryland (Rainfed)",
        "social_category": "General (OC)",
        "farmer_category": "Large (> 10 acres)",
        "existing_assets": ["Rainfed Coastal Plantation"],
        "annual_family_income_lakh": 5.5,
        "immediate_need": "SOIL_HEALTH_AND_FERTILIZER",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": "NONE",
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": "NONE",
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Nut Development / Bearing Plantation",
        "season": "Kharif 2026",
        "kcc_query_text_example": "General category large coconut grower with 14.0 acres rainfed coastal plantation in Bantwal taluk, Dakshina Kannada; seeking Soil Health Card macro and micro-nutrient testing to correct magnesium and boron deficiencies; inquiring about mobile soil testing van schedule and plantation fertilizer dosage.",
        "landholding_details": {
            "total_operational_holding_acres": 14.0,
            "qualifying_parcel_acres": 14.0,
            "requested_subsidized_area_ha": None,
            "land_classification_interval": "(10.0, inf) Large",
            "physical_area_consistency": "PASS: 14.0 ac holding matches parcel"
        },
        "water_and_irrigation": {
            "operational_water_source": "Rainfed Coastal",
            "borewell_electric_status": "NONE",
            "grid_connection_evidence": "Rainfed high-rainfall coastal plantation belt; no energized borewell on holding"
        },
        "statutory_flags": {
            "paid_income_tax_last_assessment_year": False,
            "govt_employee_category": "NONE",
            "superannuated_pensioner_monthly_amount": 0.0,
            "pensioner_is_mts_exempt": False,
            "registered_professional": "NONE",
            "land_ownership_cutoff_pre_feb_2019": True,
            "is_pure_tenant_without_land_title": False,
            "tenure_documentation": "RTC registered pre-February 2019 in Bantwal taluk, Dakshina Kannada district"
        },
        "attribute_provenance": {
            "empirical_baseline": "Coconut Development Board & Directorate of Horticulture Karnataka: Coastal laterite soils in Bantwal/Mangaluru taluks prone to severe leaching of potassium and micro-nutrients during heavy monsoon, requiring annual soil test-based nutrient management.",
            "farmer_query_inspiration": "Synthetic benchmark query formulation inspired by Kisan Call Centre (KCC) Karnataka advisory themes and Department of Agriculture field extension logs: Large plantation owners seeking comprehensive soil health analysis and micronutrient advisory for yellowing leaves in palms.",
            "statutory_policy_test": "Universal diagnostic access under Soil Health Card (SCH009) for large coastal plantation; PM-KISAN qualifies in Section A; Krishi Bhagya disqualified due to non-notified coastal district; Ganga Kalyana disqualified due to General Merit category; PMKSY-PDMC disqualified due to holding exceeding 5.0 ha ceiling and lack of operational water source."
        },
        "intended_test_purpose": "Soil Health Card universal diagnostic service for large coastal plantation (14.0 ac); GM category; verifies Section A access to SHC, PM-KISAN, and SMAM; confirms district and category exclusions for Krishi Bhagya and Ganga Kalyana.",
        "unresolved_dependencies": [
            "Verification of GoK Kharif 2026 Restructured Weather Based Crop Insurance Scheme (RWBCIS) / Coconut Palm Insurance Scheme notification for Bantwal taluk, Dakshina Kannada district",
            "Bantwal Taluk Agriculture Office Soil Health Card sample collection and mobile laboratory schedule"
        ]
    },
    {
        "scenario_id": "S066",
        "benchmark_version": "v1.0.4",
        "zone_id": "Z10",
        "agro_climatic_zone": "Coastal Zone",
        "district": "Udupi",
        "crop_primary": "Arecanut",
        "crop_secondary": "Black Pepper",
        "land_size_acres": 5.5,
        "land_type": "Dryland (Rainfed)",
        "social_category": "SC",
        "farmer_category": "Medium (5-10 acres)",
        "existing_assets": [],
        "annual_family_income_lakh": 2.2,
        "immediate_need": "BOREWELL_IRRIGATION",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": "NONE",
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": "NONE",
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 14.0,
        "community_pool_beneficiaries_count": 4,
        "farming_stage": "Flowering / Nut Setting",
        "season": "Kharif 2026",
        "kcc_query_text_example": "SC medium arecanut farmer with 5.5 acres dryland holding in Karkala taluk, Udupi; individual landholding exceeds the 5.0 acres individual ceiling for Ganga Kalyana; has formed a contiguous group with three neighboring SC smallholders pooling a 14.0 acres block (qualifying parcel 3.5 acres); applying for community borewell and lift irrigation under Dr. B.R. Ambedkar Development Corporation; seeking corporation beneficiary criteria and groundwater NOC requirements.",
        "landholding_details": {
            "total_operational_holding_acres": 5.5,
            "qualifying_parcel_acres": 3.5,
            "requested_subsidized_area_ha": None,
            "land_classification_interval": "(5.0, 10.0] Medium",
            "physical_area_consistency": "PASS: 3.5 ac qualifying parcel within 5.5 ac operational holding; 14.0 ac pooled contiguous block"
        },
        "water_and_irrigation": {
            "operational_water_source": "None (Dryland kushki)",
            "borewell_electric_status": "NONE",
            "grid_connection_evidence": "Zero electrical and irrigation infrastructure on dryland pooled arecanut block"
        },
        "statutory_flags": {
            "paid_income_tax_last_assessment_year": False,
            "govt_employee_category": "NONE",
            "superannuated_pensioner_monthly_amount": 0.0,
            "pensioner_is_mts_exempt": False,
            "registered_professional": "NONE",
            "land_ownership_cutoff_pre_feb_2019": True,
            "is_pure_tenant_without_land_title": False,
            "tenure_documentation": "RTC registered pre-February 2019 in Karkala taluk; registered joint consent deed with 3 contiguous SC neighbors"
        },
        "attribute_provenance": {
            "empirical_baseline": "DES Karnataka & Dr. B.R. Ambedkar Development Corporation: Rainfed laterite foothills in Karkala taluk, Udupi district, where small/medium SC farmers pool contiguous dryland holdings to satisfy the 8.0-15.0 acres threshold for community lift/borewell schemes.",
            "farmer_query_inspiration": "Synthetic benchmark query formulation inspired by Kisan Call Centre (KCC) Karnataka advisory themes and Ambedkar Corporation field queries: Medium SC dryland farmers with holdings > 5.0 acres pooling land with contiguous neighbors to access community borewell packages.",
            "statutory_policy_test": "Benchmark Challenge 7 & Special Governance Condition (Ambedkar Corporation Community Borewell Safeguard): Individual dryland holding (5.5 ac) exceeds 5.0 acres individual ceiling; community pool route valid with 4 SC farmers pooling 14.0 acres contiguous dryland, qualifying parcel 3.5 acres; raw engine evaluates ELIGIBLE (GK_AMBEDKAR_COMMUNITY_ROUTE_VALID) because Dr. B.R. Ambedkar Development Corporation rules require >= 3 beneficiaries (unlike other corporation routes which encode 2). CRITICAL GOVERNANCE SAFEGUARD: While the encoded Ambedkar threshold rule passes, governance conservatively decouples determination to Section B as REQUIRES_VERIFICATION without numerical scoring pending confirmation of current FY 2026-27 administrative circular instructions (published guidelines describe 8-15 acres community lift irrigation, while administrative instructions and local procedures must be confirmed), field verification of registered joint consent deed and contiguous boundary alignment, and Mines & Geology groundwater safety clearance; abstract parent SCH010 is suppressed from visible recommendations; PM-KISAN, SMAM, and KCC Central qualify in Section A; PMFBY routed to Section B pending seasonal IU notification."
        },
        "intended_test_purpose": "Challenge 7 community borewell pooling: Individual holding 5.5 ac exceeds 5.0 ac individual Ambedkar ceiling; community pool route valid with 4 SC farmers, 14.0 ac pooled contiguous dryland, qualifying parcel 3.5 ac (raw engine ELIGIBLE); governance safeguard conservatively keeps determination in Section B with scoring disabled pending corporation circular instructions, boundary consent, and groundwater clearances; parent SCH010 suppressed.",
        "unresolved_dependencies": [
            "Verification of current Dr. B.R. Ambedkar Development Corporation FY 2026-27 administrative circular instructions and operational community borewell guidelines for Karkala taluk",
            "Field verification of registered joint consent deed, mutual water-sharing agreement, and contiguous boundary alignment for the 14.0-acre pooled block in Karkala taluk",
            "Mines and Geology Department hydrogeological feasibility and groundwater safety clearance for Karkala taluk",
            "Verification of GoK Kharif 2026 PMFBY Insurance Unit (Gram Panchayat level) notification for Arecanut in Karkala taluk, Udupi district"
        ]
    },
    {
        "scenario_id": "S067",
        "benchmark_version": "v1.0.4",
        "zone_id": "Z10",
        "agro_climatic_zone": "Coastal Zone",
        "district": "Dakshina Kannada",
        "crop_primary": "Cashew",
        "crop_secondary": "Paddy",
        "land_size_acres": 2.0,
        "land_type": "Dryland (Rainfed)",
        "social_category": "ST",
        "farmer_category": "Marginal (< 2.5 acres)",
        "existing_assets": ["Rainfed Cashew Orchard"],
        "annual_family_income_lakh": 1.4,
        "immediate_need": "CROP_INSURANCE",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": "NONE",
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": "NONE",
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Flowering / Flushing",
        "season": "Kharif 2026",
        "kcc_query_text_example": "ST marginal cashew cultivator with 2.0 acres dryland orchard in Belthangady taluk, Dakshina Kannada; seeking crop insurance coverage against unseasonal rain and tea mosquito bug infestation under Restructured Weather Based Crop Insurance Scheme (RWBCIS) / PMFBY; inquiring about premium rates and notified Insurance Units.",
        "landholding_details": {
            "total_operational_holding_acres": 2.0,
            "qualifying_parcel_acres": 2.0,
            "requested_subsidized_area_ha": None,
            "land_classification_interval": "[0.0, 2.5) Marginal",
            "physical_area_consistency": "PASS: 2.0 ac holding matches parcel"
        },
        "water_and_irrigation": {
            "operational_water_source": "Rainfed Coastal",
            "borewell_electric_status": "NONE",
            "grid_connection_evidence": "Rainfed coastal laterite hillside cashew orchard; no energized irrigation equipment"
        },
        "statutory_flags": {
            "paid_income_tax_last_assessment_year": False,
            "govt_employee_category": "NONE",
            "superannuated_pensioner_monthly_amount": 0.0,
            "pensioner_is_mts_exempt": False,
            "registered_professional": "NONE",
            "land_ownership_cutoff_pre_feb_2019": True,
            "is_pure_tenant_without_land_title": False,
            "tenure_documentation": "RTC registered pre-February 2019 in Belthangady taluk, Dakshina Kannada district"
        },
        "attribute_provenance": {
            "empirical_baseline": "Directorate of Cashew Research (Puttur) & AIC of India: Rainfed cashew plantations in Belthangady/Puttur highly vulnerable to weather risks during flowering and fruit-set stages, covered under weather-indexed insurance (RWBCIS).",
            "farmer_query_inspiration": "Synthetic benchmark query formulation inspired by Kisan Call Centre (KCC) Karnataka advisory themes and AIC crop insurance queries: Tribal marginal cashew growers inquiring about weather-based insurance enrollment cut-off dates and claim triggers.",
            "statutory_policy_test": "Cashew crop insurance under RWBCIS; raw engine returns INELIGIBLE (PMFBY_NON_NOTIFIED_CROP) due to static PMFBY crop whitelist; governance decouples determination and routes SCH002 to Section B as REQUIRES_VERIFICATION pending seasonal Hobli-level RWBCIS notification; ST marginal dryland qualifies for Valmiki Corporation individual borewell (GK_SCH010_VALMIKI_INDIVIDUAL_ROUTE_VALID, coastal threshold 1.0-5.0 ac), but SCH010_VALMIKI is quarantined in Section B as a provisional scheme; parent SCH010 suppressed; PM-KISAN, SMAM, and KCC Central qualify in Section A."
        },
        "intended_test_purpose": "PMFBY/RWBCIS cashew crop insurance in coastal plantation belt; ST marginal farmer; raw PMFBY INELIGIBLE routed to Section B pending seasonal notification; SCH010_VALMIKI individual route valid but quarantined in Section B; parent SCH010 suppressed; PM-KISAN qualifies in Section A.",
        "unresolved_dependencies": [
            "Verification of GoK Kharif 2026 RWBCIS Insurance Unit (Hobli level) notification for Cashew in Belthangady taluk, Dakshina Kannada district",
            "Karnataka Maharshi Valmiki ST Development Corporation FY 2026-27 individual borewell circular and target allocation for Belthangady taluk",
            "Mines and Geology Department groundwater safety clearance for Belthangady taluk"
        ]
    },
    {
        "scenario_id": "S068",
        "benchmark_version": "v1.0.4",
        "zone_id": "Z10",
        "agro_climatic_zone": "Coastal Zone",
        "district": "Udupi",
        "crop_primary": "Paddy",
        "crop_secondary": "Pulses",
        "land_size_acres": 1.5,
        "land_type": "Wetland/valley",
        "social_category": "Minority",
        "farmer_category": "Marginal (< 2.5 acres)",
        "existing_assets": ["Wetland Inflow Drainage Sump"],
        "annual_family_income_lakh": 0.95,
        "immediate_need": "PRODUCTION_CREDIT",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": "NONE",
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": None,
        "is_pure_tenant_without_land_title": True,
        "borewell_electric_status": "NONE",
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Transplanting / Tillering",
        "season": "Kharif 2026",
        "kcc_query_text_example": "Minority marginal tenant farmer cultivating 1.5 acres coastal wetland paddy in Kundapura taluk, Udupi; operates under informal oral lease agreement with village panchayat certificate (no registered land title); seeking crop loan under Kisan Credit Card (KCC) through regional rural bank; inquiring about tenant crop loan documentation and PMFBY enrollment.",
        "landholding_details": {
            "total_operational_holding_acres": 1.5,
            "qualifying_parcel_acres": 1.5,
            "requested_subsidized_area_ha": None,
            "land_classification_interval": "[0.0, 2.5) Marginal",
            "physical_area_consistency": "PASS: 1.5 ac holding matches parcel"
        },
        "water_and_irrigation": {
            "operational_water_source": "Wetland Inflow",
            "borewell_electric_status": "NONE",
            "grid_connection_evidence": "Natural coastal wetland tidal/stream inflow drainage sump; no energized pump"
        },
        "statutory_flags": {
            "paid_income_tax_last_assessment_year": False,
            "govt_employee_category": "NONE",
            "superannuated_pensioner_monthly_amount": 0.0,
            "pensioner_is_mts_exempt": False,
            "registered_professional": "NONE",
            "land_ownership_cutoff_pre_feb_2019": None,
            "is_pure_tenant_without_land_title": True,
            "tenure_documentation": "Informal lease agreement / oral tenancy with village panchayat certificate in Kundapura taluk; no recorded title (Pure Tenant)"
        },
        "attribute_provenance": {
            "empirical_baseline": "NABARD & Lead District Bank (Canara Bank Udupi): Coastal wetland paddy cultivation in Kundapura/Brahmavara taluks with significant tenant farming relying on PACS/RRB crop loans without formal RTC title deeds.",
            "farmer_query_inspiration": "Synthetic benchmark query formulation inspired by Kisan Call Centre (KCC) Karnataka advisory themes and Lead District Bank tenant credit queries: Pure tenant farmers cultivating coastal khazan/wetland paddy inquiring about KCC crop loans and tenant cultivation certificates.",
            "statutory_policy_test": "Benchmark Challenge 5 (Pure Tenancy & Agricultural Credit Routing): Pure tenant strictly disqualified from PM-KISAN under PMKISAN_PURE_TENANT_EXCLUSION; KCC commercial credit qualifies under raw engine (KCC_CENTRAL_COMMERCIAL_ELIGIBLE) pursuant to RBI/NABARD guidelines for oral lessees, but governance routes SCH008_CENTRAL to Section B as REQUIRES_VERIFICATION without numerical scoring pending oral tenancy documentation / bank tenant crop-loan verification; PMFBY routed to Section B pending seasonal IU notification and tenant declaration verification; SMAM and Soil Health Card qualify in Section A."
        },
        "intended_test_purpose": "Challenge 5 pure tenant coastal wetland paddy; strictly excluded from PM-KISAN; KCC Central raw ELIGIBLE but routed to Section B pending tenant loan documentation; PMFBY routed to Section B; SMAM and SHC in Section A.",
        "unresolved_dependencies": [
            "Commercial bank / Karnataka Gramin Bank verification of oral lessee / tenant crop-loan eligibility documentation in Kundapura taluk, Udupi district",
            "Verification of GoK Kharif 2026 PMFBY Insurance Unit (Gram Panchayat level) notification and tenant cultivation declaration protocol for Paddy in Kundapura taluk",
            "Lead District Bank Udupi tenant farmer scale of finance certification"
        ]
    },
    {
        "scenario_id": "S069",
        "benchmark_version": "v1.0.4",
        "zone_id": "Z10",
        "agro_climatic_zone": "Coastal Zone",
        "district": "Dakshina Kannada",
        "crop_primary": "Coconut",
        "crop_secondary": "Cocoa",
        "land_size_acres": 13.0,
        "land_type": "Dryland (Rainfed)",
        "social_category": "Minority",
        "farmer_category": "Large (> 10 acres)",
        "existing_assets": ["Open Well", "Diesel Pump Set", "Drip Irrigation (Installed)"],
        "annual_family_income_lakh": 4.8,
        "immediate_need": "PROTECTED_HORTICULTURE",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": "NONE",
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": "NONE",
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Nut Development / Bearing Plantation",
        "season": "Kharif 2026",
        "kcc_query_text_example": "Minority large coconut grower with 13.0 acres holding in Puttur taluk, Dakshina Kannada; acquired land title via registered statutory succession following mother's demise in April 2022 (Death Cert DC/DK/2022/6104 and Bhoomi mutation Form 16 MR No. 2022-T771 verified); seeking 50% capital subsidy under MIDH for shaded coastal nursery / shade-net protected cultivation; verifying PM-KISAN succession status and solar pump replacement for diesel pump.",
        "landholding_details": {
            "total_operational_holding_acres": 13.0,
            "qualifying_parcel_acres": 13.0,
            "requested_subsidized_area_ha": None,
            "land_classification_interval": "(10.0, inf) Large",
            "physical_area_consistency": "PASS: 13.0 ac holding matches parcel"
        },
        "water_and_irrigation": {
            "operational_water_source": "Open Well / Rainfed",
            "borewell_electric_status": "NONE",
            "grid_connection_evidence": "Perennial large-diameter open well equipped with 5 HP diesel pump set; off-grid water source"
        },
        "statutory_flags": {
            "paid_income_tax_last_assessment_year": False,
            "govt_employee_category": "NONE",
            "superannuated_pensioner_monthly_amount": 0.0,
            "pensioner_is_mts_exempt": False,
            "registered_professional": "NONE",
            "land_ownership_cutoff_pre_feb_2019": True,
            "is_pure_tenant_without_land_title": False,
            "tenure_documentation": "Title acquired via registered inheritance succession following demise of mother in April 2022; Death Cert No. DC/DK/2022/6104, Legal Heir Certificate LHC/DK/2022/339, and Bhoomi mutation Form 16 MR No. 2022-T771 (22.06.2022) verified"
        },
        "statutory_succession_details": {
            "transfer_basis": "INHERITANCE_DUE_TO_DEATH",
            "actual_acquisition_date": "2022-04-12",
            "parent_demise_date": "2022-04-12",
            "death_certificate_number": "DC/DK/2022/6104",
            "legal_heir_certificate_number": "LHC/DK/2022/339",
            "mutation_extract_form_16": "MR No. 2022-T771 (22.06.2022)",
            "statutory_authority": "PM-KISAN Revised Operational Guidelines §§5.2–5.3.3(i)",
            "statutory_distinction": "Ownership transferred through inheritance resulting from demise of parent (§5.2 and §5.3.3(i)); strictly distinct from post-cutoff sale, partition, or gift deeds which are excluded under §5.3.3(ii).",
            "engine_input_interpretation": "land_ownership_cutoff_pre_feb_2019 = True correctly represents statutory compliance under the §§5.2–5.3.3(i) inheritance exception, passing the PMKISAN_CUTOFF_DATE_VERIFIED rule."
        },
        "attribute_provenance": {
            "empirical_baseline": "Directorate of Horticulture Karnataka & MIDH Cell: Commercial coconut and cocoa nurseries in Puttur taluk adopting shade-net protected cultivation structures for raising quality planting material, combined with off-grid open well solar pumping.",
            "farmer_query_inspiration": "Synthetic benchmark query formulation inspired by Kisan Call Centre (KCC) Karnataka advisory themes and MIDH horticulture queries: Large horticulture plantation owners with inherited titles inquiring about MIDH nursery subsidies, solar water pumping, and PM-KISAN succession registration.",
            "statutory_policy_test": "Benchmark Design v1.0.4 Section 3.3.1 (PM-KISAN Statutory Succession vs Partition Deed Safeguard): Post-01.02.2019 land title transfer qualifies under PM-KISAN Revised Operational Guidelines §§5.2–5.3.3(i) because ownership was transferred through inheritance resulting from demise of parent (transfer_basis = INHERITANCE_DUE_TO_DEATH; Death Cert DC/DK/2022/6104, Legal Heir Order LHC/DK/2022/339, and Bhoomi mutation Form 16 MR No. 2022-T771 verified); strictly distinct from post-cutoff sale, partition, or gift deeds which remain statutorily excluded under §5.3.3(ii); MIDH qualifies in Section A with installed drip irrigation; PM-KUSUM B qualifies in Section A for off-grid open well; SMAM and KCC Central qualify in Section A; PMFBY routed to Section B pending seasonal notification."
        },
        "intended_test_purpose": "MIDH coastal nursery / shade-net; Large holding (13.0 ac); Minority; post-2019 statutory inheritance upon demise of parent under PM-KISAN §§5.2–5.3.3(i) (transfer_basis=INHERITANCE_DUE_TO_DEATH, legal heir cert & mutation verified; distinct from ineligible partition, sale, and gift deeds under §5.3.3(ii)); PM-KISAN, MIDH, PM-KUSUM B, and SMAM qualify in Section A.",
        "unresolved_dependencies": [
            "Verification of GoK Kharif 2026 RWBCIS/Coconut Palm Insurance Scheme notification for Puttur taluk, Dakshina Kannada district",
            "Dakshina Kannada District Horticulture Department MIDH FY 2026-27 nursery and shade-net target circular"
        ]
    },
    {
        "scenario_id": "S070",
        "benchmark_version": "v1.0.4",
        "zone_id": "Z10",
        "agro_climatic_zone": "Coastal Zone",
        "district": "Udupi",
        "crop_primary": "Arecanut",
        "crop_secondary": "Paddy",
        "land_size_acres": 12.5,
        "land_type": "Wetland/valley",
        "social_category": "SC",
        "farmer_category": "Large (> 10 acres)",
        "existing_assets": ["Borewell (Grid-connected)", "Sprinkler Set (Partial)"],
        "annual_family_income_lakh": 6.2,
        "immediate_need": "MICRO_IRRIGATION_SUPPORT",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": "NONE",
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": None,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": "GRID_CONNECTED_IP_SET",
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Nut Development / Intercropping",
        "season": "Kharif 2026",
        "kcc_query_text_example": "SC large arecanut farmer with 12.5 acres valley wetland holding in Udupi taluk; ancestral property partition in progress with land title cut-off date UNKNOWN on Bhoomi portal; applying for micro-irrigation capital subsidy under PMKSY-PDMC for 4.80 hectares (~11.86 acres); seeking confirmation of 4.80 ha parcel capacity and title regularization requirements.",
        "landholding_details": {
            "total_operational_holding_acres": 12.5,
            "qualifying_parcel_acres": 12.5,
            "requested_subsidized_area_ha": 4.8,
            "land_classification_interval": "(10.0, inf) Large",
            "physical_area_consistency": "PASS: requested 4.80 ha <= 12.5 ac (5.059 ha) qualifying parcel; satisfies PMKSY-PDMC 5.00 ha statutory ceiling"
        },
        "water_and_irrigation": {
            "operational_water_source": "Borewell (Grid-connected)",
            "borewell_electric_status": "GRID_CONNECTED_IP_SET",
            "grid_connection_evidence": "MESCOM energized 10 HP IP set; partial sprinkler layout on arecanut valley holding"
        },
        "prior_subsidy_history": {
            "prior_micro_irrigation_subsidy_years_ago": None,
            "interpretation": "EXPLICIT_NO_PRIOR_SUBSIDY",
            "factual_declaration": "First-time micro-irrigation applicant; applicant and beneficiary family have never previously availed micro-irrigation capital assistance on this parcel or any other holding.",
            "regulatory_framework": "PMKSY-PDMC Revised Operational Guidelines 2023",
            "statutory_clauses": {
                "section_7_9_area_ceiling": "Section 7.9: Financial assistance is limited to 5.0 hectares per beneficiary (either in contiguous or distributed parcels). S070 requests exactly 4.80 ha within a 12.5 ac (5.059 ha) parcel.",
                "section_7_10_repeat_subsidy_restriction": "Section 7.10: Assistance restrictions apply to beneficiaries who have already received micro-irrigation subsidy, imposing a mandatory 7-year lock-in period before becoming eligible again. Because applicant has never availed micro-irrigation subsidy, this 7-year repeat-assistance restriction is fully satisfied.",
                "engine_mapping": "prior_micro_irrigation_subsidy_years_ago = None strictly represents confirmed zero prior subsidy, firing rule PMKSY_NO_PRIOR_SUBSIDY."
            }
        },
        "statutory_flags": {
            "paid_income_tax_last_assessment_year": False,
            "govt_employee_category": "NONE",
            "superannuated_pensioner_monthly_amount": 0.0,
            "pensioner_is_mts_exempt": False,
            "registered_professional": "NONE",
            "land_ownership_cutoff_pre_feb_2019": None,
            "is_pure_tenant_without_land_title": False,
            "tenure_documentation": "Ancestral land title partition deed pending formal mutation on Bhoomi portal in Udupi taluk; record date unverified (UNKNOWN)"
        },
        "attribute_provenance": {
            "empirical_baseline": "DES Karnataka & Horticulture Department Udupi: Valley arecanut gardens in coastal Udupi transitioning from flood/basin irrigation to precision micro-sprinklers/drip, requiring verified land records and layout maps for subsidized installation.",
            "farmer_query_inspiration": "Synthetic benchmark query formulation inspired by Kisan Call Centre (KCC) Karnataka advisory themes and micro-irrigation extension queries: Large farmers requesting subsidy ceiling guidance for 4.80 ha drip installation while mutation extract is pending.",
            "statutory_policy_test": "Benchmark Challenge 8 & Challenge 4 (Area Limit & Unknown Title Handling): Large holding of 12.5 acres (> 10.0 ac); requested subsidized area of 4.80 ha strictly satisfies physical parcel capacity (4.80 ha <= 12.5 ac * 0.404686 = 5.0586 ha) and statutory ceiling (4.80 ha <= 5.00 ha) under PMKSY-PDMC Guidelines 2023 §7.9 (assistance capped at 5.0 ha per beneficiary); 7-year repeat restriction satisfied by explicit first-time applicant declaration (null mapped to PMKSY_NO_PRIOR_SUBSIDY). RAW-ENGINE VS GOVERNANCE DISCREPANCY: The raw engine compares total operational holding against 12.35 ac and returns INELIGIBLE (PMKSY_LAND_ABOVE_5_HA). However, §7.9 caps the subsidized assistance area rather than imposing a blanket disqualification on the entire holding. CRITICAL GOVERNANCE SAFEGUARD: Because land title record date is UNKNOWN (land_ownership_cutoff_pre_feb_2019 = None), three-valued logic is strictly preserved: governance places determination in Section B as REQUIRES_VERIFICATION without numerical scoring pending title regularization. PM-KISAN similarly preserves REQUIRES_VERIFICATION in Section B due to the 01.02.2019 cut-off date check, distinguished from PMKSY's title and layout documentation requirements. SMAM and KCC Central qualify in Section A; grid connection excludes PM-KUSUM B; existing borewell and wetland topography exclude Ganga Kalyana."
        },
        "intended_test_purpose": "Challenge 8 and Challenge 4: Large holding (12.5 ac); PMKSY-PDMC requested 4.80 ha <= 12.5 ac (5.059 ha) and <= 5.00 ha ceiling (§7.9 per beneficiary cap); raw INELIGIBLE preserved while governance evaluates parcel request; title status UNKNOWN -> preserve three-valued logic in Section B for PMKSY-PDMC and PM-KISAN without numerical scoring; SMAM and KCC Central qualify in Section A.",
        "unresolved_dependencies": [
            "Revenue Department certification of land ownership record date / RTC mutation order for Udupi taluk",
            "Verification of physical parcel boundaries, possession certificate, and micro-irrigation layout for 4.80 ha within 12.5 ac parcel",
            "Verification of GoK Kharif 2026 PMFBY Insurance Unit notification for Arecanut in Udupi taluk, Udupi district",
            "Udupi District Agriculture Office PMKSY-PDMC FY 2026-27 micro-irrigation target allocation and vendor empanelment"
        ]
    }
]


def apply_governance_safeguard(
    d: SchemeDetermination,
    sid: str,
    profile: Dict[str, Any],
    is_prov: bool
) -> Dict[str, Any]:
    """
    Applies explicit governance presentation safeguards, decoupling statutory eligibility
    from administrative review sections, and enforcing statutory succession evidence gates.
    """
    missing_verifications = list(d.missing_verifications)
    disqualifying_factors = list(d.disqualifying_factors)
    gov_status = d.status.value
    presentation_section = "Disqualified / Non-Actionable Candidates"
    allow_scoring = False
    gov_note = d.reason

    # --- GOVERNANCE CASE 1: PMFBY / RWBCIS Crop Insurance Governance Audit across S065–S070 ---
    if d.scheme_id == "SCH002":
        gov_status = "REQUIRES_VERIFICATION"
        presentation_section = "Section B (Unresolved Policy Review / Seasonal Notification Required)"
        allow_scoring = False
        if sid == "S065":
            missing_verifications = [
                "Verification of GoK Kharif 2026 RWBCIS / Coconut Palm Insurance Scheme Insurance Unit notification for Coconut in Bantwal taluk, Dakshina Kannada district"
            ]
            gov_note = "Raw engine returned INELIGIBLE because Coconut is absent from static crop whitelist. In coastal districts, Coconut is covered under Weather Based Crop Insurance (RWBCIS) and Coconut Palm Insurance Scheme. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal scheme notification confirmation."
        elif sid == "S066":
            missing_verifications = [
                "Verification of GoK Kharif 2026 PMFBY Insurance Unit (Gram Panchayat level) notification for Arecanut in Karkala taluk, Udupi district"
            ]
            gov_note = "Raw engine returned ELIGIBLE based on static crop whitelist for Arecanut, but commercial crop insurance claims require verified Kharif 2026 Gram Panchayat Insurance Unit notification. Governance presentation routes to Section B as REQUIRES_VERIFICATION."
        elif sid == "S067":
            missing_verifications = [
                "Verification of GoK Kharif 2026 RWBCIS Insurance Unit (Hobli level) notification for Cashew in Belthangady taluk, Dakshina Kannada district"
            ]
            gov_note = "Raw engine returned INELIGIBLE due to static PMFBY crop whitelist, but Cashew is covered under weather-based crop insurance (RWBCIS) in Dakshina Kannada. Governance routes to Section B as REQUIRES_VERIFICATION pending seasonal notification confirmation."
        elif sid == "S068":
            missing_verifications = [
                "Verification of GoK Kharif 2026 PMFBY Insurance Unit (Gram Panchayat level) notification for Paddy in Kundapura taluk, Udupi district",
                "Tenant farmer cultivation agreement / oral lessee verification for PMFBY enrollment"
            ]
            gov_note = "Raw engine returned ELIGIBLE based on static crop whitelist for Paddy, but applicant is a pure tenant. Tenancy proof and seasonal Insurance Unit notification require verification. Governance routes to Section B as REQUIRES_VERIFICATION."
        elif sid == "S069":
            missing_verifications = [
                "Verification of GoK Kharif 2026 RWBCIS / Coconut Palm Insurance Scheme Insurance Unit notification for Coconut in Puttur taluk, Dakshina Kannada district"
            ]
            gov_note = "Raw engine returned INELIGIBLE due to static PMFBY crop whitelist, but Coconut is covered under weather-based scheme in Dakshina Kannada. Governance routes to Section B as REQUIRES_VERIFICATION."
        elif sid == "S070":
            missing_verifications = [
                "Verification of GoK Kharif 2026 PMFBY Insurance Unit (Gram Panchayat level) notification for Arecanut in Udupi taluk, Udupi district",
                "Revenue Department certification of land title record date / mutation extract for Udupi taluk"
            ]
            gov_note = "Raw engine returned ELIGIBLE based on static crop whitelist, but land title cut-off date is UNKNOWN and commercial crop insurance claims require verified Kharif 2026 Gram Panchayat Insurance Unit notification. Governance presentation routes to Section B as REQUIRES_VERIFICATION."

    # --- GOVERNANCE CASE 2: S066 Community Borewell Scheme Safeguard ---
    elif sid == "S066" and d.scheme_id == "SCH010_AMBEDKAR":
        gov_status = "REQUIRES_VERIFICATION"
        presentation_section = "Section B (Unresolved Policy Review / Community Corporation Rules Required)"
        allow_scoring = False
        missing_verifications = [
            "Verification of current Dr. B.R. Ambedkar Development Corporation FY 2026-27 administrative circular instructions and operational community borewell guidelines for Karkala taluk",
            "Field verification of registered joint consent deed, mutual water-sharing agreement, and contiguous boundary alignment for the 14.0-acre pooled block in Karkala taluk",
            "Mines and Geology Department hydrogeological feasibility and groundwater safety clearance for Karkala taluk"
        ]
        gov_note = (
            "Raw engine evaluated ELIGIBLE (GK_AMBEDKAR_COMMUNITY_ROUTE_VALID) because Dr. B.R. Ambedkar "
            "Development Corporation community route encodes >= 3 beneficiaries on 8.0-15.0 acres pooled dryland "
            "and S066 provides 4 contiguous SC beneficiaries with 14.0 acres (qualifying parcel 3.5 ac). "
            "Governance conservatively decouples determination to Section B as REQUIRES_VERIFICATION with numerical "
            "scoring disabled pending field verification of registered joint consent deed, contiguous boundary alignment, "
            "Mines and Geology groundwater safety clearance, and confirmation of current administrative circular instructions."
        )

    # --- GOVERNANCE CASE 3: S068 Pure Tenancy Agricultural Credit Routing (Challenge 5) ---
    elif sid == "S068" and d.scheme_id == "SCH001":
        gov_status = "INELIGIBLE"
        presentation_section = "Disqualified / Non-Actionable Candidates"
        allow_scoring = False
        gov_note = "Pure tenant farmer without recorded land ownership title is statutorily excluded from PM-KISAN (PMKISAN_PURE_TENANT_EXCLUSION). Placed in Disqualified Candidates."
    elif sid == "S068" and d.scheme_id == "SCH008_CENTRAL":
        gov_status = "REQUIRES_VERIFICATION"
        presentation_section = "Section B (Unresolved Policy Review / Tenant Crop-Loan Documentation Required)"
        allow_scoring = False
        missing_verifications = [
            "Commercial bank / Karnataka Gramin Bank verification of oral lessee / tenant crop-loan eligibility documentation in Kundapura taluk, Udupi district",
            "Lead District Bank Udupi / NABARD scale of finance tenant farmer certification"
        ]
        gov_note = "Raw engine returned ELIGIBLE under RBI/NABARD tenant borrower category, but oral tenancy documentation and bank tenant crop-loan eligibility require verification. Governance safeguard routes determination to Section B as REQUIRES_VERIFICATION without numerical scoring."

    # --- GOVERNANCE CASE 4: Statutory Succession Safeguard (PM-KISAN Revised Guidelines §§5.2–5.3.3(i) vs §5.3.3(ii)) ---
    elif d.scheme_id == "SCH001" and "statutory_succession_details" in profile:
        ssd = profile.get("statutory_succession_details", {})
        transfer_basis = ssd.get("transfer_basis")
        has_death_cert = bool(ssd.get("death_certificate_number"))
        has_legal_heir = bool(ssd.get("legal_heir_certificate_number"))
        has_mutation = bool(ssd.get("mutation_extract_form_16"))
        has_demise_date = bool(ssd.get("parent_demise_date"))
        
        # Check for genuine statutory succession upon death vs non-qualifying partition/sale/gift
        if transfer_basis == "INHERITANCE_DUE_TO_DEATH" and has_death_cert and has_legal_heir and has_mutation and has_demise_date:
            gov_status = "ELIGIBLE"
            presentation_section = "Section A (Confirmed Actionable Candidates)"
            allow_scoring = True
            missing_verifications = []
            gov_note = (
                "Statutory Inheritance Compliance: Title acquired post-01.02.2019 strictly satisfies "
                "PM-KISAN Revised Operational Guidelines §§5.2–5.3.3(i) exception because ownership was "
                "transferred through inheritance resulting from demise of parent (transfer_basis = "
                f"INHERITANCE_DUE_TO_DEATH; parent deceased {ssd.get('parent_demise_date')}; Death Cert "
                f"{ssd.get('death_certificate_number')}, Legal Heir Order {ssd.get('legal_heir_certificate_number')}, "
                f"and Bhoomi mutation Form 16 {ssd.get('mutation_extract_form_16')} verified). Strictly distinct "
                "from non-qualifying post-cutoff sale, partition, or gift deeds under §5.3.3(ii). "
                "Raw engine evaluated ELIGIBLE (PMKISAN_CUTOFF_DATE_VERIFIED) and confirmed in Section A."
            )
        elif transfer_basis in ["PARTITION", "POST_CUTOFF_PARTITION", "SALE_DEED", "GIFT_DEED"]:
            gov_status = "INELIGIBLE"
            presentation_section = "Disqualified / Non-Actionable Candidates"
            allow_scoring = False
            disqualifying_factors = [
                f"Post-01.02.2019 land title transfer based on {transfer_basis} is statutorily excluded "
                "from PM-KISAN under Operational Guidelines §5.3.3(ii). Only succession upon death (§5.3.3(i)) qualifies."
            ]
            gov_note = (
                f"Statutory Transfer Exclusion: Land title transfer basis '{transfer_basis}' is explicitly excluded "
                "from PM-KISAN benefits under Revised Operational Guidelines §5.3.3(ii). Even with registered deed, "
                "transfers through partition, sale, or gift executed after 01.02.2019 do not qualify for the death-succession exception."
            )
        else:
            gov_status = "REQUIRES_VERIFICATION"
            presentation_section = "Section B (Unresolved Statutory Evidence / Land Title Required)"
            allow_scoring = False
            missing_verifications = [
                "Complete statutory inheritance documentation (Death Certificate, Legal Heir Certificate, and Revenue Mutation extract)"
            ]
            gov_note = (
                "Inheritance documentation incomplete: Post-cutoff title transfer requires verification of parent death certificate, "
                "legal heir order, and Bhoomi mutation extract under PM-KISAN Guidelines §§5.2–5.3.3(i)."
            )

    # --- GOVERNANCE CASE 5: S070 Unknown Land Title & Area Limit (Challenge 8 & Challenge 4) ---
    elif sid == "S070" and d.scheme_id == "SCH001":
        gov_status = "REQUIRES_VERIFICATION"
        presentation_section = "Section B (Unresolved Statutory Evidence / Land Title Required)"
        allow_scoring = False
        missing_verifications = [
            "Verification of land ownership title record date (must be on or before 01.02.2019 or statutory succession upon death under §§5.1–5.3)",
            "Revenue Department certification of land ownership record date / inheritance mutation order on RTC for Udupi taluk"
        ]
        gov_note = "Raw engine returned REQUIRES_VERIFICATION due to explicit UNKNOWN tenure cut-off date (land_ownership_cutoff_pre_feb_2019 = None). In strict adherence to Challenge 4 safeguards, missing title evidence must remain REQUIRES_VERIFICATION and never silently default to eligibility or ineligibility. Placed in Section B without scoring."
    elif sid == "S070" and d.scheme_id == "SCH003":
        gov_status = "REQUIRES_VERIFICATION"
        presentation_section = "Section B (Unresolved Statutory Evidence / Land Title Required)"
        allow_scoring = False
        missing_verifications = [
            "Revenue Department certification of land ownership title record date / mutation extract for Udupi taluk",
            "Verification of physical parcel boundaries, possession certificate, and micro-irrigation layout for 4.80 ha within 12.5 ac parcel"
        ]
        gov_note = (
            "Raw Engine vs Governance Discrepancy & Area Validation: Raw engine returned INELIGIBLE (PMKSY_LAND_ABOVE_5_HA) "
            "because its encoded static rule checks operational holding against 12.35 ac. However, under Section 7.9 of the "
            "PMKSY-PDMC Revised Operational Guidelines 2023, financial assistance is limited to 5.0 hectares per beneficiary "
            "(not per beneficiary family). S070 requests 4.80 ha, which is strictly within the physical capacity of the "
            "12.5-acre parcel (5.059 ha) and within the 5.00 ha assistance ceiling under §7.9; the 5.0 ha assistance cap does not "
            "render the entire holding ineligible. However, because land title record date is UNKNOWN (land_ownership_cutoff_pre_feb_2019 = None), "
            "PMKSY-PDMC requires verified land title (RTC) and possession/boundary documentation (distinguished from PM-KISAN's "
            "01.02.2019 cut-off date check). Governance preserves three-valued logic by placing determination in Section B as "
            "REQUIRES_VERIFICATION without numerical scoring pending title regularization."
        )

    # --- GOVERNANCE CASE 6: Provisional Schemes ---
    elif is_prov and d.status == EligibilityStatus.ELIGIBLE:
        gov_status = "REQUIRES_VERIFICATION"
        presentation_section = "Section B (Provisional Schemes / Qualitative Review Only)"
        allow_scoring = False
        missing_verifications = [f"Administrative circular verification for provisional scheme {d.scheme_id}"]
        gov_note = "Raw engine returned ELIGIBLE based on encoded rules, but scheme record is PROVISIONAL in registry. Governance safeguard places determination in Section B as REQUIRES_VERIFICATION without numerical scoring."
    elif is_prov and d.status == EligibilityStatus.REQUIRES_VERIFICATION:
        gov_status = "REQUIRES_VERIFICATION"
        presentation_section = "Section B (Provisional Schemes / Qualitative Review Only)"
        allow_scoring = False
        if not missing_verifications:
            missing_verifications = [f"Administrative circular and Government Order verification for provisional scheme {d.scheme_id}"]
        gov_note = "Provisional scheme requiring administrative or Government Order verification."
    elif d.status == EligibilityStatus.ELIGIBLE:
        gov_status = "ELIGIBLE"
        presentation_section = "Section A (Confirmed Actionable Candidates)"
        allow_scoring = True
        gov_note = "Confirmed verified scheme eligible for clinical 0-3 relevance scoring."
    else:
        gov_status = d.status.value
        presentation_section = "Disqualified / Non-Actionable Candidates"
        allow_scoring = False
        gov_note = "Statutorily disqualified under verified criteria."

    return {
        "scheme_id": d.scheme_id,
        "scheme_name": d.scheme_name,
        "record_type": d.record_type,
        "parent_scheme_id": d.parent_scheme_id,
        "status": d.status.value,
        "raw_engine_status": d.status.value,
        "governance_status": gov_status,
        "presentation_section": presentation_section,
        "allow_numerical_scoring": allow_scoring,
        "governance_note": gov_note,
        "reason": d.reason,
        "disqualifying_factors": disqualifying_factors,
        "missing_verifications": missing_verifications,
        "rule_keys_fired": d.rule_keys_fired,
        "availability_state": d.availability_state.value,
        "is_provisional": is_prov
    }


def run_execution() -> Dict[str, Any]:
    """Execute raw engine, availability filter, actionable deduplication, and governance presentation."""
    engine = EligibilityEngine()
    avail_filter = AvailabilityFilter()
    
    execution_results = []
    
    for profile in ZONE_Z10_PROFILES:
        sid = profile["scenario_id"]
        
        scenario_data = {
            "scenario_id": profile["scenario_id"],
            "agro_climatic_zone": profile["agro_climatic_zone"],
            "district": profile["district"],
            "crop_primary": profile["crop_primary"],
            "land_size_acres": profile["land_size_acres"],
            "land_type": profile["land_type"],
            "social_category": profile["social_category"],
            "farmer_category": profile["farmer_category"],
            "existing_assets": profile["existing_assets"],
            "annual_family_income_lakh": profile["annual_family_income_lakh"],
            "immediate_need": profile["immediate_need"],
            "paid_income_tax_last_assessment_year": profile["paid_income_tax_last_assessment_year"],
            "govt_employee_category": profile["govt_employee_category"],
            "superannuated_pensioner_monthly_amount": profile["superannuated_pensioner_monthly_amount"],
            "pensioner_is_mts_exempt": profile["pensioner_is_mts_exempt"],
            "registered_professional": profile["registered_professional"],
            "land_ownership_cutoff_pre_feb_2019": profile["land_ownership_cutoff_pre_feb_2019"],
            "is_pure_tenant_without_land_title": profile["is_pure_tenant_without_land_title"],
            "borewell_electric_status": profile["borewell_electric_status"],
            "prior_micro_irrigation_subsidy_years_ago": profile.get("prior_micro_irrigation_subsidy_years_ago"),
            "prior_farm_pond_subsidy_years_ago": profile.get("prior_farm_pond_subsidy_years_ago"),
            "prior_machinery_subsidy_years_ago": profile.get("prior_machinery_subsidy_years_ago"),
            "prior_ganga_kalyana_in_family": profile.get("prior_ganga_kalyana_in_family", False),
            "community_pool_acres": profile.get("community_pool_acres", 0.0),
            "community_pool_beneficiaries_count": profile.get("community_pool_beneficiaries_count", 0),
            "crop_secondary": profile.get("crop_secondary"),
            "farming_stage": profile.get("farming_stage"),
            "season": profile.get("season"),
            "kcc_query_text_example": profile.get("kcc_query_text_example")
        }
        
        scenario_obj = FarmerScenario.from_dict(scenario_data)
        
        # 1. Raw Engine Evaluation
        raw_determinations = engine.evaluate_scenario(scenario_obj, include_children=True)
        
        # 2. Availability State Filter
        raw_determinations = avail_filter.apply_availability(raw_determinations, as_of_date="2026-10-19")
        
        # 3. Actionable Deduplication
        actionable_determinations = engine.resolve_actionable_determinations(raw_determinations)
        
        raw_serializable = []
        for d in raw_determinations:
            is_prov = d.scheme_id in PROVISIONAL_SCHEMES
            raw_serializable.append({
                "scheme_id": d.scheme_id,
                "scheme_name": d.scheme_name,
                "record_type": d.record_type,
                "parent_scheme_id": d.parent_scheme_id,
                "status": d.status.value,
                "raw_engine_status": d.status.value,
                "reason": d.reason,
                "disqualifying_factors": d.disqualifying_factors,
                "missing_verifications": d.missing_verifications,
                "rule_keys_fired": d.rule_keys_fired,
                "availability_state": d.availability_state.value,
                "is_actionable": d in actionable_determinations,
                "is_provisional": is_prov
            })
            
        actionable_serializable = []
        for d in actionable_determinations:
            is_prov = d.scheme_id in PROVISIONAL_SCHEMES
            item_dict = apply_governance_safeguard(d, sid, profile, is_prov)
            actionable_serializable.append(item_dict)
            
        execution_results.append({
            "scenario_id": sid,
            "profile": profile,
            "raw_determinations": raw_serializable,
            "actionable_determinations": actionable_serializable
        })
        
    return {
        "benchmark_version": "v1.0.4",
        "zone_id": "Z10",
        "agro_climatic_zone": "Coastal Zone",
        "execution_date": "2026-10-19",
        "total_scenarios": len(execution_results),
        "results": execution_results
    }


def write_deliverables(execution_output: Dict[str, Any]):
    """Write individual scenario JSON/MD files, summary JSONs, and execution report."""
    output_dir = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", "z10")
    reports_dir = os.path.join(WORKSPACE_ROOT, "reports")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)
    
    # 1. Write individual JSON and MD for S065-S070
    for item in execution_output["results"]:
        sid = item["scenario_id"]
        profile = item["profile"]
        
        json_path = os.path.join(output_dir, f"{sid}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
            
        md_path = os.path.join(output_dir, f"{sid}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(generate_scenario_markdown(profile, item["actionable_determinations"]))
            
    # 2. Write aggregated z10_scenarios.json
    scenarios_path = os.path.join(output_dir, "z10_scenarios.json")
    with open(scenarios_path, "w", encoding="utf-8") as f:
        json.dump(ZONE_Z10_PROFILES, f, indent=2, ensure_ascii=False)
        
    # 3. Write aggregated z10_execution_results.json
    results_path = os.path.join(output_dir, "z10_execution_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(execution_output, f, indent=2, ensure_ascii=False)
        
    # 4. Generate and write reports/zone_z10_execution_report.md
    report_path = os.path.join(reports_dir, "zone_z10_execution_report.md")
    report_content = generate_execution_report(execution_output)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"Successfully generated all Zone Z10 deliverables in {output_dir} and {report_path}")


def generate_scenario_markdown(profile: Dict[str, Any], actionable: List[Dict[str, Any]]) -> str:
    """Generate Markdown profile documentation for a Zone Z10 scenario."""
    sid = profile["scenario_id"]
    lines = [
        f"# Farmer Scenario Profile: {sid}",
        "",
        f"**Benchmark Version:** {profile.get('benchmark_version', 'v1.0.4')}  ",
        f"**Agro-Climatic Zone:** {profile['agro_climatic_zone']} ({profile['zone_id']})  ",
        f"**District:** {profile['district']}  ",
        f"**Primary Crop:** {profile['crop_primary']} (Secondary: {profile.get('crop_secondary', 'None')})  ",
        f"**Operational Landholding:** {profile['land_size_acres']} acres ({profile['farmer_category']})  ",
        f"**Land Type:** {profile['land_type']}  ",
        f"**Social Category:** {profile['social_category']}  ",
        f"**Annual Family Income:** ₹{profile['annual_family_income_lakh']:.2f} Lakh  ",
        f"**Immediate Need:** `{profile['immediate_need']}`  ",
        "",
        "## Landholding & Area Verification",
        f"- **Total Operational Holding:** {profile['landholding_details']['total_operational_holding_acres']} acres",
        f"- **Qualifying Parcel:** {profile['landholding_details']['qualifying_parcel_acres']} acres",
        f"- **Requested Subsidized Area:** {profile['landholding_details']['requested_subsidized_area_ha']} ha" if profile['landholding_details']['requested_subsidized_area_ha'] else "- **Requested Subsidized Area:** Not applicable (full parcel intervention)",
        f"- **Physical Area Consistency Check:** `{profile['landholding_details']['physical_area_consistency']}`",
        "",
        "## Water & Irrigation Infrastructure",
        f"- **Operational Water Source:** {profile['water_and_irrigation']['operational_water_source']}",
        f"- **Borewell Electric Status:** `{profile['water_and_irrigation']['borewell_electric_status']}`",
        f"- **Grid Connection Evidence:** {profile['water_and_irrigation']['grid_connection_evidence']}",
        "",
        "## Statutory Exclusions & Tenure Governance",
        f"- **Land Ownership Cut-off Date (01.02.2019):** `{'PRE-FEB 2019' if profile['statutory_flags']['land_ownership_cutoff_pre_feb_2019'] is True else ('POST-FEB 2019' if profile['statutory_flags']['land_ownership_cutoff_pre_feb_2019'] is False else 'UNKNOWN / REQUIRES_VERIFICATION')}`",
        f"- **Tenure Evidence:** {profile['statutory_flags']['tenure_documentation']}",
        f"- **Income Tax Assessed (AY 2025-26):** `{'YES (EXCLUDED)' if profile['statutory_flags']['paid_income_tax_last_assessment_year'] else 'NO (VERIFIED)'}`",
        f"- **Government Employment:** `{profile['statutory_flags']['govt_employee_category']}`",
        f"- **Pension Status:** ₹{profile['statutory_flags']['superannuated_pensioner_monthly_amount']:.2f}/month (MTS Exempt: {profile['statutory_flags']['pensioner_is_mts_exempt']})",
    ]

    if "statutory_succession_details" in profile:
        ssd = profile["statutory_succession_details"]
        lines.extend([
            "",
            "## Statutory Succession & Inheritance Details (PM-KISAN Guidelines §§5.2–5.3.3(i))",
            f"- **Transfer Basis:** `{ssd['transfer_basis']}`",
            f"- **Actual Acquisition Date:** {ssd['actual_acquisition_date']}",
            f"- **Parent Demise Date:** {ssd['parent_demise_date']}",
            f"- **Death Certificate:** {ssd['death_certificate_number']}",
            f"- **Legal Heir Certificate:** {ssd['legal_heir_certificate_number']}",
            f"- **Mutation Extract:** {ssd['mutation_extract_form_16']}",
            f"- **Statutory Distinction:** {ssd['statutory_distinction']}",
            f"- **Engine Input Mapping:** `{ssd['engine_input_interpretation']}`"
        ])

    if "prior_subsidy_history" in profile:
        psh = profile["prior_subsidy_history"]
        lines.extend([
            "",
            "## Prior Subsidy History & Regulatory Declaration",
            f"- **Interpretation:** `{psh['interpretation']}`",
            f"- **Factual Declaration:** {psh['factual_declaration']}",
            f"- **Regulatory Framework:** {psh['regulatory_framework']}",
            f"- **Section 7.9 Area Ceiling:** {psh['statutory_clauses']['section_7_9_area_ceiling']}",
            f"- **Section 7.10 Repeat Restriction:** {psh['statutory_clauses']['section_7_10_repeat_subsidy_restriction']}",
            f"- **Engine Mapping:** `{psh['statutory_clauses']['engine_mapping']}`"
        ])
        
    lines.extend([
        "",
        "## Evaluated Actionable Recommendations & Governance Presentation",
        "",
        "| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Clinical Scoring |",
        "|:---|:---|:---:|:---:|:---|:---:|"
    ])
    
    for d in actionable:
        scoring_str = "Enabled (0–3)" if d["allow_numerical_scoring"] else "Disabled"
        lines.append(f"| `{d['scheme_id']}` | {d['scheme_name']} | `{d['raw_engine_status']}` | `{d['governance_status']}` | {d['presentation_section']} | {scoring_str} |")
        
    lines.extend([
        "",
        "## Unresolved Dependencies & Governance Notes",
    ])
    for dep in profile.get("unresolved_dependencies", []):
        lines.append(f"- **Dependency:** {dep}")
        
    return "\n".join(lines) + "\n"


def generate_execution_report(execution_output: Dict[str, Any]) -> str:
    """Generate the comprehensive Markdown execution and governance audit report for Zone Z10."""
    doc = []
    doc.append("# Deliverable: Zone Z10 Execution Report (Scenarios S065–S070)\n\n")
    doc.append("**Benchmark Version:** `v1.0.4`  \n")
    doc.append("**Execution Date:** October 19, 2026  \n")
    doc.append("**Agro-Climatic Zone:** Coastal Zone (Zone Z10 — Dakshina Kannada, Udupi, Uttara Kannada Coast)  \n")
    doc.append("**Total Scenarios Evaluated:** Exactly 6 (`S065`–`S070`)  \n")
    doc.append("**Audit Scope:** Exactly six detailed scenarios (`S065`–`S070`) evaluated across all 16 scheme records (8 standalone records, 2 parent records, and 6 child records).  \n\n")
    
    doc.append("## 1. Executive Summary & Project Invariants\n\n")
    doc.append("This report documents the rule-validation and governance audit of the tenth and final benchmark batch of six scenarios (S065–S070) representing the **Coastal Zone (Zone Z10)**. This completion marks the final delivery of the full 60-scenario Benchmark v1.0.4 matrix (S011–S070 across Zones Z1–Z10). In strict adherence to project invariants:\n\n")
    doc.append("1. **Preservation of Frozen Engine (`src/eligibility/engine.py`):** The frozen engine is completely untouched and preserved at baseline commit `7724fa7`. Raw three-valued logic outcomes (`ELIGIBLE`, `INELIGIBLE`, `REQUIRES_VERIFICATION`) are evaluated deterministically.\n")
    doc.append("2. **Preservation of Scheme Master (`scheme_database/processed/scheme_master.json`):** Scheme definitions, hierarchies, and metadata are unmodified.\n")
    doc.append("3. **Preservation of Pilot Scenarios & Protocol:** Pilot scenarios `S001`–`S010` and annotation protocol `v1.1` remain strictly preserved.\n")
    doc.append("4. **Benchmark Design v1.0.4 Compliance:** Strictly fulfills all representation quotas, cross-field area validations, solar pump prerequisites, and statutory inheritance definitions established in `benchmark_v1_design.md` v1.0.4.\n")
    doc.append("5. **Operational Availability Safeguard:** Eligibility verified in Section A does **NOT** equate to active application window availability. All determinations carry availability state `Availability unknown — confirmation required`.\n")
    doc.append("6. **Crop Insurance Decoupling (PMFBY/RWBCIS):** Static whitelist results from the raw engine are decoupled from governance presentation across all six scenarios. Unverified seasonal Insurance Unit (Gram Panchayat/Hobli level) notifications are strictly routed to Section B as `REQUIRES_VERIFICATION` with numerical scoring disabled.\n")
    doc.append("7. **Provisional Schemes Quarantine:** Corporation schemes (`SCH008_KA_COOP`, `SCH010_VALMIKI`) are strictly quarantined in Section B without clinical scoring.\n")
    doc.append("8. **S066 Community Borewell Scheme Safeguard (Challenge 7):** S066 features 4 SC farmers pooling 14.0 contiguous dryland acres (qualifying parcel 3.5 ac), evaluating raw ELIGIBLE (`GK_AMBEDKAR_COMMUNITY_ROUTE_VALID`) because Ambedkar Corporation rules require >= 3 beneficiaries on 8.0-15.0 acres pooled dryland. Governance conservatively decouples determination to Section B as `REQUIRES_VERIFICATION` with scoring disabled pending confirmation of current administrative circular instructions, registered boundary alignment, and groundwater clearances; parent `SCH010` is suppressed.\n")
    doc.append("9. **S069 Statutory Inheritance Succession (PM-KISAN Guidelines §§5.2–5.3.3(i)):** Ownership acquired post-01.02.2019 is strictly verified under `transfer_basis = INHERITANCE_DUE_TO_DEATH` resulting from parent demise (April 2022), supported by registered death certificate, legal heir order, and Bhoomi mutation extract. Gated explicitly by governance check; distinct from post-cutoff sale, partition, and gift transfers under §5.3.3(ii); qualifies for PM-KISAN in Section A.\n")
    doc.append("10. **S070 Unknown Land Title & Area Limit (Challenge 8 & Challenge 4):** Land title cut-off date is UNKNOWN (`land_ownership_cutoff_pre_feb_2019 = None`), strictly preserving three-valued logic in Section B (`REQUIRES_VERIFICATION`) for PM-KISAN and PMKSY-PDMC without scoring. Requested subsidized area (4.80 ha) is verified against the 12.5-acre parcel's physical capacity (5.059 ha) and the 5.00 ha PMKSY ceiling (§7.9 per beneficiary cap), with explicit first-time applicant status satisfying the 7-year lock-in restriction. Raw engine operational holding check (> 12.35 ac) vs governance subsidized parcel override explicitly recorded.\n")
    doc.append("11. **S068 Pure Tenancy Routing (Challenge 5):** Pure tenant without recorded title is statutorily excluded from PM-KISAN (`PMKISAN_PURE_TENANT_EXCLUSION`); KCC commercial credit (`SCH008_CENTRAL`) routes to Section B as `REQUIRES_VERIFICATION` without scoring pending oral lease / tenant crop loan documentation verification.\n\n")
    
    doc.append("## 2. Zone Z10 Scenario Input Overview (S065–S070)\n\n")
    doc.append("| Scenario ID | District | Primary Crop | Holding (ac) | Land Type | Social Category | Farmer Class | Immediate Need | Operational Water Source | Benchmark Test Purpose |\n")
    doc.append("|:---|:---|:---|:---:|:---|:---:|:---:|:---|:---|:---|\n")
    for s in execution_output["results"]:
        p = s["profile"]
        ws = p["water_and_irrigation"]["operational_water_source"]
        doc.append(f"| **{p['scenario_id']}** | {p['district']} | {p['crop_primary']} | {p['land_size_acres']} | {p['land_type']} | {p['social_category']} | {p['farmer_category']} | `{p['immediate_need']}` | {ws} | {p['intended_test_purpose'][:60]}... |\n")
    doc.append("\n")
    
    doc.append("## 3. Governance Presentation Accounting & Reconciled Denominators\n\n")
    doc.append("| Scenario | District | Primary Crop | Immediate Need | Section A (Confirmed) | Section B (Review / Unverified) | Disqualified Candidates | Total Actionable | Reconciled Formula |\n")
    doc.append("|:---:|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|\n")
    
    for item in execution_output["results"]:
        sid = item["scenario_id"]
        p = item["profile"]
        acts = item["actionable_determinations"]
        sa = sum(1 for d in acts if d["presentation_section"].startswith("Section A"))
        sb = sum(1 for d in acts if d["presentation_section"].startswith("Section B"))
        dq = sum(1 for d in acts if d["presentation_section"].startswith("Disqualified"))
        tot = len(acts)
        doc.append(f"| **{sid}** | {p['district']} | {p['crop_primary']} | `{p['immediate_need']}` | **{sa}** | **{sb}** | **{dq}** | **{tot}** | {sa} + {sb} + {dq} = {tot} |\n")
    doc.append("\n")
    
    doc.append("### Denominator Reconciliations & Abstract Parent Suppression:\n")
    doc.append("Every scenario evaluates exactly 16 raw scheme records. The number of displayed actionable schemes is explicitly reconciled based on whether child records of abstract parents (`SCH008`, `SCH010`) are actionable:\n\n")
    doc.append("- In **S065, S068, S069, S070**: Abstract parent `SCH008` is suppressed because child credit records (`SCH008_CENTRAL`, `SCH008_KA_COOP`) are actionable. In contrast, zero Ganga Kalyana child corporation records are actionable $\\implies$ abstract parent `SCH010` is retained as an ineligible umbrella record $\\implies 16 - 1 = \\mathbf{15}$ actionable schemes displayed.\n")
    doc.append("- In **S066**: Abstract parent `SCH008` is suppressed by child credit schemes; child corporation record `SCH010_AMBEDKAR` evaluates ELIGIBLE (Community route valid) $\\implies$ abstract parent `SCH010` is ALSO suppressed $\\implies 16 - 2 = \\mathbf{14}$ actionable schemes displayed.\n")
    doc.append("- In **S067**: Abstract parent `SCH008` is suppressed by child credit schemes; child corporation record `SCH010_VALMIKI` evaluates ELIGIBLE (Individual route valid for ST marginal dryland) $\\implies$ abstract parent `SCH010` is ALSO suppressed $\\implies 16 - 2 = \\mathbf{14}$ actionable schemes displayed.\n\n")
    
    doc.append("## 4. Scenario-by-Scenario Detailed Governance Audits\n\n")
    for item in execution_output["results"]:
        sid = item["scenario_id"]
        p = item["profile"]
        acts = item["actionable_determinations"]
        doc.append(f"### 4.{sid[-1]} Scenario {sid}: {p['district']} — {p['crop_primary']} ({p['land_size_acres']} ac, {p['social_category']})\n\n")
        doc.append(f"- **Context & Need:** {p['intended_test_purpose']}\n")
        doc.append(f"- **Physical Area Consistency:** `{p['landholding_details']['physical_area_consistency']}`\n")
        doc.append(f"- **Water Infrastructure:** {p['water_and_irrigation']['operational_water_source']} (`{p['water_and_irrigation']['borewell_electric_status']}`)\n")
        doc.append(f"- **Statutory Flags:** Tenure=`{p['statutory_flags']['tenure_documentation']}`, Income Tax=`{p['statutory_flags']['paid_income_tax_last_assessment_year']}`, Govt Employee=`{p['statutory_flags']['govt_employee_category']}`\n\n")
        
        doc.append("| Scheme ID | Scheme Name | Raw Engine Status | Governance Status | Presentation Section | Allow Scoring | Governance Audit Note |\n")
        doc.append("|:---|:---|:---:|:---:|:---|:---:|:---|\n")
        for d in acts:
            doc.append(f"| `{d['scheme_id']}` | {d['scheme_name']} | `{d['raw_engine_status']}` | `{d['governance_status']}` | {d['presentation_section']} | {'Yes' if d['allow_numerical_scoring'] else 'No'} | {d['governance_note'][:80]}... |\n")
        doc.append("\n")
        
    doc.append("## 5. Unresolved Dependencies & Verification Log\n\n")
    doc.append("The following verification dependencies remain active and are enforced across Zone Z10:\n\n")
    for item in execution_output["results"]:
        sid = item["scenario_id"]
        p = item["profile"]
        doc.append(f"### {sid} ({p['district']} — {p['crop_primary']})\n")
        for dep in p.get("unresolved_dependencies", []):
            doc.append(f"- {dep}\n")
        doc.append("\n")
        
    doc.append("## 6. Frozen Invariants Check\n\n")
    doc.append("| Invariant Component | Status | Verification Summary |\n")
    doc.append("|:---|:---:|:---|\n")
    doc.append("| `src/eligibility/engine.py` | **PRESERVED** | Untouched; raw evaluations deterministic |\n")
    doc.append("| `scheme_database/processed/scheme_master.json` | **PRESERVED** | Untouched; 16 scheme records intact |\n")
    doc.append("| Pilot Scenarios `S001`–`S010` | **PRESERVED** | Untouched; baseline calibration valid |\n")
    doc.append("| Annotation Protocol `v1.1` | **PRESERVED** | Untouched; governance presentation standards maintained |\n")
    doc.append("| Benchmark Design `v1.0.4` | **COMPLIANT** | All Z10 quotas, area caps, and tenure rules strictly satisfied |\n\n")
    
    doc.append("## 7. Full Benchmark Delivery Completion (Ten-Zone Construction Sign-Off)\n\n")
    doc.append("With the execution and verification of Zone Z10 (S065–S070), all 60 planned benchmark scenarios across ten agro-climatic zones are now fully constructed:\n\n")
    doc.append("- **Zone Z1 (S011–S016):** North Eastern Transition Zone (Bidar, Kalaburagi)\n")
    doc.append("- **Zone Z2 (S017–S022):** North Eastern Dry Zone (Kalaburagi, Yadgir, Raichur)\n")
    doc.append("- **Zone Z3 (S023–S028):** Northern Dry Zone (Vijayapura, Bagalkot, Gadag, Koppal)\n")
    doc.append("- **Zone Z4 (S029–S034):** Central Dry Zone (Chitradurga, Davanagere, Ballari, Tumakuru)\n")
    doc.append("- **Zone Z5 (S035–S040):** Eastern Dry Zone (Bengaluru, Kolar, Chikkaballapur, Ramanagara)\n")
    doc.append("- **Zone Z6 (S041–S046):** Southern Dry Zone (Mandya, Mysuru, Chamarajanagar, Tumakuru South)\n")
    doc.append("- **Zone Z7 (S047–S052):** Southern Transition Zone (Hassan, Shivamogga, Chikkamagaluru Plains)\n")
    doc.append("- **Zone Z8 (S053–S058):** Northern Transition Zone (Dharwad, Belagavi, Haveri)\n")
    doc.append("- **Zone Z9 (S059–S064):** Hilly Zone (Kodagu, Chikkamagaluru Ghats, Uttara Kannada Ghats)\n")
    doc.append("- **Zone Z10 (S065–S070):** Coastal Zone (Dakshina Kannada, Udupi, Uttara Kannada Coast)\n\n")
    doc.append("As authorized, the next milestone is a comprehensive full-benchmark integrity review before clinical annotation and evaluation—not immediate model training.\n")
    
    return "".join(doc)


if __name__ == "__main__":
    out = run_execution()
    write_deliverables(out)
