"""
src/app/demo_profiles.py
------------------------
Taxonomy definitions and pre-configured synthetic demonstration profiles
for the Farmer Scheme Recommendation Application.

IMPORTANT DISCLAIMER:
  All demonstration profiles in this module are SYNTHETIC BENCHMARK SCENARIOS
  synthesized for algorithmic testing and academic demonstration.
  THEY DO NOT REPRESENT REAL INDIVIDUAL FARMERS OR FIELD-VALIDATION EVIDENCE.
"""

from typing import Any, Dict, List

# ── Geographic and Agronomic Taxonomies ───────────────────────────────────────

DISTRICTS = [
    "Bagalkot", "Belagavi", "Bengaluru Rural", "Bidar", "Chamarajanagar",
    "Chikkaballapura", "Chikkamagaluru", "Chitradurga", "Dakshina Kannada",
    "Davanagere", "Dharwad", "Gadag", "Hassan", "Haveri", "Kalaburagi",
    "Kodagu", "Kolar", "Koppal", "Mandya", "Mysuru", "Raichur", "Ramanagara",
    "Shivamogga", "Tumakuru", "Udupi", "Uttara Kannada", "Vijayapura", "Yadgir"
]

ZONE_TO_NAME = {
    "Z1": "North Eastern Transition Zone",
    "Z2": "North Eastern Dry Zone",
    "Z3": "Northern Dry Zone",
    "Z4": "Central Dry Zone",
    "Z5": "Eastern Dry Zone",
    "Z6": "Southern Dry Zone",
    "Z7": "Southern Transition Zone",
    "Z8": "Northern Transition Zone",
    "Z9": "Hilly Zone",
    "Z10": "Coastal Zone",
}

DISTRICT_TO_ZONE = {
    "Bidar": "Z1",
    "Yadgir": "Z1",
    "Kalaburagi": "Z1",
    "Raichur": "Z2",
    "Koppal": "Z2",
    "Vijayapura": "Z3",
    "Bagalkot": "Z3",
    "Gadag": "Z3",
    "Davanagere": "Z4",
    "Chitradurga": "Z4",
    "Tumakuru": "Z4",
    "Kolar": "Z5",
    "Chikkaballapura": "Z5",
    "Bengaluru Rural": "Z5",
    "Ramanagara": "Z5",
    "Mandya": "Z6",
    "Mysuru": "Z6",
    "Chamarajanagar": "Z6",
    "Hassan": "Z7",
    "Shivamogga": "Z7",
    "Dharwad": "Z8",
    "Haveri": "Z8",
    "Belagavi": "Z8",
    "Chikkamagaluru": "Z9",
    "Kodagu": "Z9",
    "Uttara Kannada": "Z10",
    "Udupi": "Z10",
    "Dakshina Kannada": "Z10",
}

CROPS = [
    "Arecanut", "Banana", "Bengalgram", "Black Pepper", "Cardamom", "Cashew",
    "Chilli", "Coconut", "Cotton", "Cucumber", "Flowers", "Grapes",
    "Groundnut", "Jowar", "Maize", "Millets", "Onion", "Paddy", "Papaya",
    "Pigeonpea", "Pomegranate", "Ragi", "Redgram", "Soybean", "Sugarcane",
    "Sunflower", "Tomato", "Turmeric", "Vegetables", "Wheat"
]

LAND_TYPES = [
    "Dryland (Rainfed)",
    "Canal-irrigated",
]

FARMER_CATEGORIES = [
    "Marginal (< 1.0 acre)",
    "Marginal (1.0-2.5 acres)",
    "Small (2.5-5.0 acres)",
    "Medium/Large (> 5.0 acres)",
]

SOCIAL_CATEGORIES = [
    "General (OC)",
    "OBC (2A)",
    "OBC (2B)",
    "OBC (3A)",
    "OBC (3B)",
    "SC",
    "ST",
    "Minority (Muslim)",
    "Minority (Christian)",
]

WATER_SOURCES = [
    "Rainfed (no source)",
    "Open well",
    "Borewell (Non-energized)",
    "Non-energized borewell",
    "Grid-connected borewell",
    "Canal outlet",
    "Farm pond",
    "Seasonal stream/lift",
]

ELECTRICITY_STATUSES = [
    "No electricity",
    "Non-energized (off-grid)",
    "Diesel pump",
    "Solar pump",
    "Grid-connected IP set",
]

IMMEDIATE_NEEDS = [
    "RAINWATER_HARVESTING",
    "SOIL_HEALTH_AND_FERTILIZER",
    "FARM_MECHANIZATION",
    "CROP_INSURANCE",
    "SOLAR_PUMP_INSTALLATION",
    "DEBT_RELIEF",
    "PROTECTED_HORTICULTURE",
    "POST_HARVEST_STORAGE",
]

SECONDARY_CONSTRAINTS = [
    "Severe working capital depletion for seasonal inputs",
    "High cost of emergency private water access",
    "Exhaustion of liquid funds for plant protection chemicals",
    "Lack of efficient spraying machinery",
    "Need for precision micro-irrigation installation",
    "Specialized micronutrient and soil testing",
    "Exclusion from title-tied central cash welfare (PM-KISAN)",
    "Exclusion from standard commercial mortgage credit",
    "Limited beneficiary contribution funds",
    "High cost of chemical fertilizers",
    "Need for soil testing diagnostic and input credit",
    "Limited access to seasonal credit",
    "High cost of emergency private water tanker delivery",
    "Post-harvest storage infrastructure gap",
    "Market price volatility and distress sale pressure",
]


# ── Synthetic Demonstration Profiles ──────────────────────────────────────────

DEMO_PROFILES: Dict[str, Dict[str, Any]] = {
    "DEMO_S131": {
        "title": "S131: Rainfed Marginal Tenant (Yadgir, Z1) - Rainwater Need",
        "description": "Synthetic Profile: 0.8 acres rainfed Bengalgram/Chilli in Yadgir. Pure tenant without land title, no electricity. Urgent rainwater harvesting need.",
        "profile": {
            "scenario_id": "DEMO_S131",
            "benchmark_version": "v1.2",
            "zone_id": "Z1",
            "agro_climatic_zone": "North Eastern Transition Zone",
            "district": "Yadgir",
            "crop_primary": "Bengalgram",
            "crop_secondary": "Chilli",
            "land_size_acres": 0.8,
            "land_type": "Dryland (Rainfed)",
            "social_category": "ST",
            "farmer_category": "Marginal (< 1.0 acre)",
            "existing_assets": [],
            "annual_family_income_lakh": 0.59,
            "immediate_need": "RAINWATER_HARVESTING",
            "paid_income_tax_last_assessment_year": False,
            "govt_employee_category": "NONE",
            "superannuated_pensioner_monthly_amount": 0.0,
            "pensioner_is_mts_exempt": False,
            "registered_professional": "NONE",
            "land_ownership_cutoff_pre_feb_2019": False,
            "is_pure_tenant_without_land_title": True,
            "borewell_electric_status": "No electricity",
            "water_and_irrigation": {
                "operational_water_source": "Rainfed (no source)",
                "borewell_electric_status": "No electricity",
            },
            "compound_need_details": {
                "primary_acute_crisis": "CROP_INSURANCE",
                "secondary_constraints": [
                    "Need for precision micro-irrigation installation"
                ],
                "narrative": "Farmer in Yadgir cultivating Bengalgram on 0.8 acres rainfed land.",
            },
        },
    },
    "DEMO_S132": {
        "title": "S132: Canal-Irrigated SC Smallholder (Bidar, Z1) - Soil Health Need",
        "description": "Synthetic Profile: 2.0 acres canal-irrigated Bengalgram/Paddy in Bidar. SC landowner with open well, off-grid electricity. High chemical fertilizer costs.",
        "profile": {
            "scenario_id": "DEMO_S132",
            "benchmark_version": "v1.2",
            "zone_id": "Z1",
            "agro_climatic_zone": "North Eastern Transition Zone",
            "district": "Bidar",
            "crop_primary": "Bengalgram",
            "crop_secondary": "Paddy",
            "land_size_acres": 2.0,
            "land_type": "Canal-irrigated",
            "social_category": "SC",
            "farmer_category": "Marginal (1.0-2.5 acres)",
            "existing_assets": ["Borewell"],
            "annual_family_income_lakh": 0.94,
            "immediate_need": "SOIL_HEALTH_AND_FERTILIZER",
            "paid_income_tax_last_assessment_year": False,
            "govt_employee_category": "NONE",
            "superannuated_pensioner_monthly_amount": 0.0,
            "pensioner_is_mts_exempt": False,
            "registered_professional": "NONE",
            "land_ownership_cutoff_pre_feb_2019": True,
            "is_pure_tenant_without_land_title": False,
            "borewell_electric_status": "Non-energized (off-grid)",
            "water_and_irrigation": {
                "operational_water_source": "Open well",
                "borewell_electric_status": "Non-energized (off-grid)",
            },
            "compound_need_details": {
                "primary_acute_crisis": "PROTECTED_HORTICULTURE",
                "secondary_constraints": [
                    "High cost of chemical fertilizers"
                ],
                "narrative": "SC farmer in Bidar with 2.0 acres seeking fertilizer guidance.",
            },
        },
    },
    "DEMO_S136": {
        "title": "S136: Medium Landowner (Yadgir, Z1) - Post-Harvest Storage Crisis",
        "description": "Synthetic Profile: 6.6 acres canal-irrigated Ragi/Bajra in Yadgir. OBC (3A) owner with multiple secondary liquidity & fertilizer constraints.",
        "profile": {
            "scenario_id": "DEMO_S136",
            "benchmark_version": "v1.2",
            "zone_id": "Z1",
            "agro_climatic_zone": "North Eastern Transition Zone",
            "district": "Yadgir",
            "crop_primary": "Ragi",
            "crop_secondary": "Millets",
            "land_size_acres": 6.6,
            "land_type": "Canal-irrigated",
            "social_category": "OBC (3A)",
            "farmer_category": "Medium/Large (> 5.0 acres)",
            "existing_assets": ["Tractor"],
            "annual_family_income_lakh": 2.10,
            "immediate_need": "FARM_MECHANIZATION",
            "paid_income_tax_last_assessment_year": False,
            "govt_employee_category": "NONE",
            "superannuated_pensioner_monthly_amount": 0.0,
            "pensioner_is_mts_exempt": False,
            "registered_professional": "NONE",
            "land_ownership_cutoff_pre_feb_2019": True,
            "is_pure_tenant_without_land_title": False,
            "borewell_electric_status": "Non-energized (off-grid)",
            "water_and_irrigation": {
                "operational_water_source": "Open well",
                "borewell_electric_status": "Non-energized (off-grid)",
            },
            "compound_need_details": {
                "primary_acute_crisis": "POST_HARVEST_STORAGE",
                "secondary_constraints": [
                    "Limited access to seasonal credit",
                    "Need for precision micro-irrigation installation",
                    "High cost of chemical fertilizers"
                ],
                "narrative": "Medium farmer with acute storage and working capital constraints.",
            },
        },
    },
    "DEMO_S137": {
        "title": "S137: Rainfed Solar Pump Need (Bidar, Z1) - Water Lift Crisis",
        "description": "Synthetic Profile: 5.6 acres dryland Wheat/Soybean in Bidar. General category farmer with seasonal lift water source and urgent solar pump requirement.",
        "profile": {
            "scenario_id": "DEMO_S137",
            "benchmark_version": "v1.2",
            "zone_id": "Z1",
            "agro_climatic_zone": "North Eastern Transition Zone",
            "district": "Bidar",
            "crop_primary": "Wheat",
            "crop_secondary": "Soybean",
            "land_size_acres": 5.6,
            "land_type": "Dryland (Rainfed)",
            "social_category": "General (OC)",
            "farmer_category": "Medium/Large (> 5.0 acres)",
            "existing_assets": [],
            "annual_family_income_lakh": 1.45,
            "immediate_need": "DEBT_RELIEF",
            "paid_income_tax_last_assessment_year": False,
            "govt_employee_category": "NONE",
            "superannuated_pensioner_monthly_amount": 0.0,
            "pensioner_is_mts_exempt": False,
            "registered_professional": "NONE",
            "land_ownership_cutoff_pre_feb_2019": True,
            "is_pure_tenant_without_land_title": False,
            "borewell_electric_status": "Solar pump",
            "water_and_irrigation": {
                "operational_water_source": "Seasonal stream/lift",
                "borewell_electric_status": "Solar pump",
            },
            "compound_need_details": {
                "primary_acute_crisis": "SOLAR_PUMP_INSTALLATION",
                "secondary_constraints": [
                    "High cost of emergency private water tanker delivery"
                ],
                "narrative": "Farmer needing solar water pumping capital support.",
            },
        },
    },
    "DEMO_EXCLUSION_BOUNDARY": {
        "title": "Synthetic Exclusion Boundary: Income Tax Payee with Grid Borewell",
        "description": "Synthetic Negative Boundary: Farmer paid income tax in last assessment year and has grid-connected IP set. Demonstrates strict statutory disqualification from PM-KISAN and PM-KUSUM-B.",
        "profile": {
            "scenario_id": "DEMO_NEG01",
            "benchmark_version": "v1.2",
            "zone_id": "Z5",
            "agro_climatic_zone": "Eastern Dry Zone",
            "district": "Kolar",
            "crop_primary": "Tomato",
            "crop_secondary": "Vegetables",
            "land_size_acres": 4.5,
            "land_type": "Canal-irrigated",
            "social_category": "General (OC)",
            "farmer_category": "Small (2.5-5.0 acres)",
            "existing_assets": ["Borewell"],
            "annual_family_income_lakh": 6.50,
            "immediate_need": "SOLAR_PUMP_INSTALLATION",
            "paid_income_tax_last_assessment_year": True,  # Disqualifies PM-KISAN
            "govt_employee_category": "NONE",
            "superannuated_pensioner_monthly_amount": 0.0,
            "pensioner_is_mts_exempt": False,
            "registered_professional": "NONE",
            "land_ownership_cutoff_pre_feb_2019": True,
            "is_pure_tenant_without_land_title": False,
            "borewell_electric_status": "Grid-connected IP set",  # Disqualifies PM-KUSUM B
            "water_and_irrigation": {
                "operational_water_source": "Grid-connected borewell",
                "borewell_electric_status": "Grid-connected IP set",
            },
            "compound_need_details": {
                "primary_acute_crisis": "SOLAR_PUMP_INSTALLATION",
                "secondary_constraints": [
                    "High cost of chemical fertilizers"
                ],
                "narrative": "Tax paying farmer with grid-connected IP set seeking subsidies.",
            },
        },
    },
}

