#!/usr/bin/env python3
"""
generate_benchmark_v1_2_scenarios.py
-------------------------------------
Generates Benchmark v1.2 compound-need scenario matrix using the frozen eligibility
engine and governance pipeline.

Design principles (from benchmark_v1.2_design_proposal.md):
- Scenario diversity over repetition: attributes vary independently across
  crop, land tenure, land size, water access, electricity access, income,
  primary crisis, secondary needs, and urgency.
- No label quota: candidate sets arise from the eligibility engine only;
  scenarios are NOT selected based on expected relevance scores.
- All attributes traceable to source material or marked as synthetic
  assumptions. No invented statutory scheme conditions, benefits, or source URLs.
- Scenario-grouped structure preserved for evaluation.

Outputs (versioned v1.2-specific paths):
- data/benchmarks/v1.2/scenario_matrix.json
- data/benchmarks/v1.2/candidate_generation_results.json
- reports/benchmark_v1_2_scenario_generation_report.md
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from dataclasses import fields
from pathlib import Path
from typing import Any, Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.eligibility.models import (
    FarmerScenario,
    EligibilityStatus,
    GovtEmployeeCategory,
    BorewellElectricStatus,
)
from src.eligibility.engine import EligibilityEngine
from src.eligibility.governance import apply_governance_safeguard, PROVISIONAL_SCHEMES

# ---------------------------------------------------------------------------
# Versioned output paths (v1.2-specific, do not touch v1.1)
# ---------------------------------------------------------------------------
BENCH_DIR = REPO_ROOT / "data/benchmarks/v1.2"
SCENARIO_MATRIX_PATH = BENCH_DIR / "scenario_matrix.json"
CANDIDATE_RESULTS_PATH = BENCH_DIR / "candidate_generation_results.json"
GENERATION_REPORT_PATH = REPO_ROOT / "reports/benchmark_v1_2_scenario_generation_report.md"

# ---------------------------------------------------------------------------
# Attribute pools (v1.2 diversity)
# These define the independent attribute space. Values are drawn from
# repository-supported enumerations (scheme_master, eligibility engine
# constants, v1.1 scenario matrix patterns). Where a value is a synthetic
# assumption rather than a source fact, it is flagged as such in the
# provenance metadata.
# ---------------------------------------------------------------------------

ZONE_INFO = {
    1: {"name": "North Eastern Transition Zone", "districts": ["Bidar", "Kalaburagi", "Yadgir"]},
    2: {"name": "North Eastern Dry Zone", "districts": ["Raichur", "Koppal", "Bagalkot"]},
    3: {"name": "Northern Dry Zone", "districts": ["Vijayapura", "Gadag", "Davanagere"]},
    4: {"name": "Central Dry Zone", "districts": ["Tumakuru", "Chitradurga", "Chikkaballapura"]},
    5: {"name": "Eastern Dry Zone", "districts": ["Kolar", "Bengaluru Rural", "Ramanagara"]},
    6: {"name": "Southern Dry Zone", "districts": ["Mandya", "Mysuru", "Chamarajanagar"]},
    7: {"name": "Southern Transition Zone", "districts": ["Hassan", "Shivamogga", "Chikkamagaluru"]},
    8: {"name": "Northern Transition Zone", "districts": ["Dharwad", "Belagavi", "Haveri"]},
    9: {"name": "Hilly Zone", "districts": ["Kodagu", "Uttara Kannada", "Dakshina Kannada"]},
    10: {"name": "Coastal Zone", "districts": ["Udupi", "Dakshina Kannada", "Uttara Kannada"]},
}

PRIMARY_CROPS = [
    "Redgram", "Soybean", "Bengalgram", "Sugarcane", "Jowar", "Cotton",
    "Paddy", "Maize", "Ragi", "Groundnut", "Sunflower", "Pigeonpea",
    "Tomato", "Onion", "Chilli", "Turmeric", "Banana", "Mango",
    "Arecanut", "Coconut", "Papaya", "Pomegranate", "Grapes",
    "Capsicum", "Cucumber", "Flowers", "Black Pepper", "Cardamom", "Cashew",
    "Vegetables", "Wheat", "Bajra", "Millets",
]

HORTICULTURE_CROPS = {
    "Tomato", "Onion", "Chilli", "Turmeric", "Banana", "Mango", "Arecanut",
    "Coconut", "Papaya", "Pomegranate", "Grapes", "Capsicum", "Cucumber",
    "Flowers", "Vegetables", "Black Pepper", "Cardamom", "Cashew",
}

NOTIFIED_PMFBY_CROPS = {
    "Paddy", "Maize", "Ragi", "Jowar", "Groundnut", "Redgram", "Cotton",
    "Sugarcane", "Arecanut", "Chilli", "Turmeric", "Sunflower", "Soybean",
    "Bengalgram", "Onion", "Tomato",
}

LAND_TENURE_TYPES = [
    "Titled (FRUITS/Bhoomi recorded)",
    "Pure tenant (oral lessee, no land title)",
    "Shared tenancy (registered lease)",
    "Inherited (succession deed)",
    "Community pooled (mutual agreement)",
]

WATER_ACCESS_TYPES = [
    "Non-energized borewell",
    "Grid-connected borewell",
    "Open well",
    "Canal outlet",
    "Rainfed (no source)",
    "Farm pond",
    "Seasonal stream/lift",
]

ELECTRICITY_ACCESS_TYPES = [
    "Grid-connected IP set",
    "Non-energized (off-grid)",
    "Solar pump",
    "Diesel pump",
    "No electricity",
]

PRIMARY_CRISES = [
    "Critical water infrastructure failure (dried/failed borewell or pump burnout during high-demand stage)",
    "Acute standing crop infestation or weather shock threatening total yield loss",
    "High upfront capital barrier for protected horticulture structures (shade net/polyhouse)",
    "Severe seasonal labor shortages during critical sowing/harvesting operations without land title documentation",
    "Recurring prolonged dry-spells threatening rainfed crop survival across critical vegetative stages",
    "Acute soil fertility degradation and crop yellowing/deficiency reducing operational margins",
    "Critical debt burden with non-institutional loan default risk",
    "Post-harvest storage and market access crisis during price crash",
]

SECONDARY_CONSTRAINTS_POOL = [
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

IMMEDIATE_NEEDS = [
    "SOLAR_PUMP_INSTALLATION",
    "CROP_INSURANCE",
    "PROTECTED_HORTICULTURE",
    "FARM_MECHANIZATION",
    "RAINWATER_HARVESTING",
    "SOIL_HEALTH_AND_FERTILIZER",
    "DEBT_RELIEF",
    "POST_HARVEST_STORAGE",
]

# Attribute-to-crisis mapping for plausibility constraints
CRISIS_WATER_DEPENDENT = {
    "SOLAR_PUMP_INSTALLATION", "RAINWATER_HARVESTING",
}

CRISIS_LAND_TITLE_DEPENDENT = {
    "FARM_MECHANIZATION",
}

CRISIS_HORTICULTURE_DEPENDENT = {
    "PROTECTED_HORTICULTURE",
}

# ---------------------------------------------------------------------------
# Attribute sampling helpers
# ---------------------------------------------------------------------------

import random


class ScenarioRNG:
    """Deterministic random generator for reproducible scenario generation."""

    def __init__(self, seed: int = 20261028):
        self.rng = random.Random(seed)

    def choice(self, seq):
        return self.rng.choice(seq)

    def choices(self, seq, k=1, weights=None):
        return self.rng.choices(seq, weights=weights, k=k)

    def uniform(self, a, b):
        return self.rng.uniform(a, b)

    def randint(self, a, b):
        return self.rng.randint(a, b)

    def random(self):
        return self.rng.random()

    def shuffle(self, seq):
        self.rng.shuffle(seq)


def land_size_bucket(acres: float) -> str:
    """Bucket land size for reporting and diversity tracking."""
    if acres < 1.0:
        return "Marginal (< 1.0 acre)"
    elif acres < 2.5:
        return "Marginal (1.0-2.5 acres)"
    elif acres <= 5.0:
        return "Small (2.5-5.0 acres)"
    else:
        return "Medium/Large (> 5.0 acres)"


def plausible_water_access(land_type: str, immediate_need: str) -> str:
    """Return a plausible water access given land type and immediate need."""
    if immediate_need == "SOLAR_PUMP_INSTALLATION":
        # Needs an existing (possibly non-energized) borewell
        return rng.choice(["Non-energized borewell", "Grid-connected borewell", "Open well"])
    if immediate_need == "PROTECTED_HORTICULTURE":
        # Needs reliable water
        return rng.choice(["Grid-connected borewell", "Open well", "Canal outlet", "Farm pond"])
    if immediate_need == "RAINWATER_HARVESTING":
        # Rainfed, no assured source
        return "Rainfed (no source)"
    if immediate_need == "SOIL_HEALTH_AND_FERTILIZER":
        return rng.choice(["Non-energized borewell", "Open well", "Canal outlet", "Grid-connected borewell"])
    if immediate_need == "FARM_MECHANIZATION":
        return rng.choice(["Canal outlet", "Open well", "Borewell (Non-energized)", "Grid-connected borewell"])
    if immediate_need == "CROP_INSURANCE":
        return rng.choice(["Rainfed (no source)", "Non-energized borewell", "Open well", "Canal outlet"])
    return rng.choice(WATER_ACCESS_TYPES)


def plausible_electricity(water_access: str, immediate_need: str) -> str:
    """Return plausible electricity access given water access."""
    if water_access == "Rainfed (no source)":
        return "No electricity"
    if water_access == "Non-energized borewell":
        return "Non-energized (off-grid)"
    if water_access == "Grid-connected borewell":
        return "Grid-connected IP set"
    if water_access == "Open well":
        return rng.choice(["Non-energized (off-grid)", "Grid-connected IP set", "Diesel pump"])
    if water_access == "Canal outlet":
        return rng.choice(["Grid-connected IP set", "Diesel pump", "No electricity"])
    if water_access == "Farm pond":
        return rng.choice(["Diesel pump", "Solar pump", "No electricity"])
    return rng.choice(ELECTRICITY_ACCESS_TYPES)


def plausible_land_type(water_access: str) -> str:
    """Return plausible land type given water access."""
    if water_access == "Rainfed (no source)":
        return "Dryland (Rainfed)"
    if water_access in ["Canal outlet", "Grid-connected borewell", "Open well"]:
        return rng.choice(["Canal-irrigated", "Dryland (Rainfed)"])
    if water_access == "Non-energized borewell":
        return "Dryland (Rainfed)"
    if water_access == "Farm pond":
        return rng.choice(["Dryland (Rainfed)", "Canal-irrigated"])
    return "Dryland (Rainfed)"


def plausible_social_category(tenant: bool) -> str:
    """Return social category; pure tenants more likely from marginalized groups."""
    if tenant:
        return rng.choice(["SC", "ST", "OBC (2A)", "OBC (3A)", "Minority (Muslim)"])
    return rng.choice([
        "SC", "ST", "OBC (2A)", "OBC (2B)", "OBC (3A)", "OBC (3B)",
        "General (OC)", "Minority (Muslim)", "Minority (Christian)",
    ])


def plausible_farmer_category(land_size: float) -> str:
    """Return farmer category consistent with land size."""
    if land_size < 1.0:
        return "Marginal (< 1.0 acre)"
    elif land_size < 2.5:
        return "Marginal (1.0-2.5 acres)"
    elif land_size <= 5.0:
        return "Small (2.5-5.0 acres)"
    else:
        return "Medium/Large (> 5.0 acres)"


def plausible_income(land_size: float, social_category: str) -> float:
    """Return plausible annual family income (lakh Rs) consistent with land and category."""
    base = land_size * 0.35 + 0.5
    if social_category in ["SC", "ST"]:
        base *= 0.85
    elif social_category == "General (OC)":
        base *= 1.15
    return round(base + rng.uniform(-0.3, 0.5), 2)


def plausible_crisis(water_access: str, land_size: float, social_category: str,
                     crop_primary: str, tenant: bool) -> str:
    """Return a plausible primary acute crisis given scenario attributes."""
    # Water-dependent crises need water access
    if water_access == "Rainfed (no source)" and tenant:
        # Tenant with no water - likely crop insurance or debt
        return rng.choice(["CROP_INSURANCE", "DEBT_RELIEF"])
    if water_access in ["Non-energized borewell", "Grid-connected borewell", "Open well"]:
        return rng.choice(list(IMMEDIATE_NEEDS))
    if water_access == "Canal outlet":
        return rng.choice([
            "CROP_INSURANCE", "FARM_MECHANIZATION", "SOIL_HEALTH_AND_FERTILIZER",
            "PROTECTED_HORTICULTURE", "RAINWATER_HARVESTING"
        ])
    if water_access == "Farm pond":
        return rng.choice(["SOLAR_PUMP_INSTALLATION", "RAINWATER_HARVESTING", "FARM_MECHANIZATION"])
    return rng.choice(list(IMMEDIATE_NEEDS))


def plausible_secondary(crisis: str, water_access: str, crop_primary: str) -> List[str]:
    """Return 1-3 secondary constraints consistent with primary crisis."""
    all_constraints = list(SECONDARY_CONSTRAINTS_POOL)
    rng.shuffle(all_constraints)
    n = rng.randint(1, 3)
    return all_constraints[:n]


def plausible_assets(water_access: str, land_size: float, immediate_need: str) -> List[str]:
    """Return plausible existing assets given scenario attributes."""
    assets = []
    if "borewell" in water_access.lower():
        assets.append(f"Borewell ({water_access.split(' ')[0]}, Yield {rng.uniform(0.5, 3.0):.1f} inch)")
    if "open well" in water_access.lower():
        assets.append("Open Well")
    if water_access == "Canal outlet":
        assets.append("Canal Outlet")
    if immediate_need == "FARM_MECHANIZATION":
        assets.append("Farm Implements")
    if immediate_need == "PROTECTED_HORTICULTURE":
        if rng.random() < 0.5:
            assets.append("Diesel Pump")
        if rng.random() < 0.3:
            assets.append("Drip Irrigation (Installed)")
    if land_size > 4.0:
        assets.append("Tractor")
    if rng.random() < 0.3:
        assets.append("Farm Implements")
    return assets


def plausible_urgency(immediate_need: str) -> str:
    """Return plausible urgency based on immediate need."""
    urgency_map = {
        "SOLAR_PUMP_INSTALLATION": "Immediate (crop at risk within 2-4 weeks)",
        "CROP_INSURANCE": "Immediate (standing crop threatened)",
        "PROTECTED_HORTICULTURE": "Seasonal (next planting cycle 4-8 weeks)",
        "FARM_MECHANIZATION": "Seasonal (sowing/harvest window 2-6 weeks)",
        "RAINWATER_HARVESTING": "Seasonal (pre-monsoon window 4-8 weeks)",
        "SOIL_HEALTH_AND_FERTILIZER": "Seasonal (post-harvest 2-4 weeks)",
        "DEBT_RELIEF": "Immediate (loan recovery notice received)",
        "POST_HARVEST_STORAGE": "Seasonal (harvest in 2-6 weeks)",
    }
    return urgency_map.get(immediate_need, "Seasonal")


rng = ScenarioRNG(seed=20261028)


def generate_scenario_profile(scenario_id: str, zone_id: int) -> Dict[str, Any]:
    """Generate a single v1.2 scenario profile with independently varied attributes."""
    z_info = ZONE_INFO[zone_id]
    district = rng.choice(z_info["districts"])

    # Independently sample attributes (no archetype locking)
    crop_primary = rng.choice(PRIMARY_CROPS)
    crop_secondary = rng.choice([c for c in PRIMARY_CROPS if c != crop_primary])

    land_size = round(rng.uniform(0.5, 8.0), 1)
    social_cat = plausible_social_category(False)
    farmer_cat = plausible_farmer_category(land_size)
    income = plausible_income(land_size, social_cat)

    # Immediate need first - drives water/electricity requirements
    immediate_need = rng.choice(IMMEDIATE_NEEDS)

    # Water access depends on immediate need (plausible pairing)
    # Note: land_type param is not used in plausible_water_access body,
    # so pass empty string; land_type is derived from water_access below.
    water_access = plausible_water_access("", immediate_need)
    electricity = plausible_electricity(water_access, immediate_need)
    land_type = plausible_land_type(water_access)

    # Tenancy - independent but correlated with social category
    is_tenant = rng.random() < 0.25  # ~25% tenants
    if is_tenant:
        social_cat = plausible_social_category(True)
        farmer_cat = plausible_farmer_category(land_size)

    # Assets
    assets = plausible_assets(water_access, land_size, immediate_need)

    # Crisis and constraints
    primary_crisis = plausible_crisis(water_access, land_size, social_cat, crop_primary, is_tenant)
    secondary = plausible_secondary(immediate_need, water_access, crop_primary)

    # Narrative
    narrative = (
        f"Farmer in {district} ({z_info['name']}) cultivating {crop_primary} "
        f"and {crop_secondary} on {land_size} acres. Primary acute situation: "
        f"{primary_crisis.lower()}. Compounding constraints: "
        f"{'; '.join(secondary).lower()}."
    )

    # Build source-backed interventions from scheme master
    # (populated later after scheme master load)

    profile = {
        "scenario_id": scenario_id,
        "benchmark_version": "v1.2",
        "zone_id": f"Z{zone_id}",
        "agro_climatic_zone": z_info["name"],
        "district": district,
        "crop_primary": crop_primary,
        "crop_secondary": crop_secondary,
        "land_size_acres": land_size,
        "land_type": land_type,
        "social_category": social_cat,
        "farmer_category": farmer_cat,
        "existing_assets": assets,
        "annual_family_income_lakh": income,
        "immediate_need": immediate_need,
        "paid_income_tax_last_assessment_year": rng.random() < 0.15,
        "govt_employee_category": "NONE",
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": not is_tenant,
        "is_pure_tenant_without_land_title": is_tenant,
        "borewell_electric_status": electricity,
        "prior_micro_irrigation_subsidy_years_ago": None,
        "prior_farm_pond_subsidy_years_ago": None,
        "prior_machinery_subsidy_years_ago": None,
        "prior_ganga_kalyana_in_family": False,
        "community_pool_acres": 0.0,
        "community_pool_beneficiaries_count": 0,
        "farming_stage": "Vegetative / Reproductive",
        "season": "Kharif 2026",
        "kcc_query_text_example": narrative,
        "landholding_details": {
            "total_operational_holding_acres": land_size,
            "qualifying_parcel_acres": land_size,
            "land_classification": farmer_cat,
        },
        "water_and_irrigation": {
            "operational_water_source": water_access,
            "borewell_electric_status": electricity,
        },
        "compound_need_details": {
            "archetype_id": f"V12_{immediate_need}",
            "archetype_name": immediate_need.replace("_", " ").title(),
            "primary_acute_crisis": primary_crisis,
            "secondary_constraints": secondary,
            "narrative": narrative,
            "engine_immediate_need_mapping": immediate_need,
            "clinical_tradeoff_definition": (
                f"Competing interventions for {immediate_need.lower().replace('_', ' ')} "
                f"in {district} district."
            ),
            "hypothesized_competing_schemes": [],
            "statutory_considerations": (
                "Statutory eligibility determined by frozen EligibilityEngine. "
                "Section A schemes allow numerical scoring; Section B schemes "
                "are quarantined pending verification."
            ),
        },
        "source_backed_interventions": {},
        "provenance": {
            "scenario_id": scenario_id,
            "attributes_sourced_from": "Repository scheme_master.json, eligibility engine constants, v1.1 scenario matrix patterns",
            "synthetic_attributes": [
                "land_size_acres", "annual_family_income_lakh", "existing_assets",
                "primary_acute_crisis", "secondary_constraints", "narrative",
                "urgency", "immediate_need",
            ],
            "source_attributes": [
                "zone_id", "agro_climatic_zone", "district",
                "social_category", "farmer_category", "land_type",
                "water_access", "electricity_access",
            ],
        },
    }
    return profile


def generate_all_scenarios(n_per_zone: int = 9) -> List[Dict[str, Any]]:
    """Generate n_per_zone scenarios per zone (10 zones = n_per_zone * 10 total)."""
    scenarios = []
    current_sid = 131  # v1.1 ends at S130
    for z in range(1, 11):
        for _ in range(n_per_zone):
            sid = f"S{current_sid:03d}"
            sc = generate_scenario_profile(sid, z)
            scenarios.append(sc)
            current_sid += 1
    return scenarios


def execute_scenarios_through_engine(scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Run every scenario through the frozen EligibilityEngine + governance."""
    engine = EligibilityEngine()
    results = {}

    valid_fields = {f.name for f in fields(FarmerScenario)}

    for sc in scenarios:
        sid = sc["scenario_id"]
        engine_dict = {k: v for k, v in sc.items() if k in valid_fields}
        f_sc = FarmerScenario.from_dict(engine_dict)

        # Run frozen deterministic engine
        raw_dets = engine.evaluate_scenario(f_sc)
        # Deduplicate parent records
        actionable_dets = engine.resolve_actionable_determinations(raw_dets)

        # Apply governance presentation
        section_a = []
        section_b = []
        disqualified = []

        for d in actionable_dets:
            is_prov = d.scheme_id in PROVISIONAL_SCHEMES
            gov = apply_governance_safeguard(d, sid, sc, is_prov=is_prov)

            sch_info = {
                "scheme_id": d.scheme_id,
                "scheme_name": d.scheme_name,
                "record_type": d.record_type,
                "raw_engine_status": d.status.value,
                "governance_status": gov["governance_status"],
                "presentation_section": gov["presentation_section"],
                "allow_numerical_scoring": gov["allow_numerical_scoring"],
                "governance_note": gov["governance_note"],
                "rule_keys_fired": d.rule_keys_fired,
                "missing_verifications": gov["missing_verifications"],
                "disqualifying_factors": gov["disqualifying_factors"],
            }

            if gov["allow_numerical_scoring"] and gov["presentation_section"].startswith("Section A"):
                section_a.append(sch_info)
            elif gov["presentation_section"].startswith("Section B"):
                section_b.append(sch_info)
            else:
                disqualified.append(sch_info)

        results[sid] = {
            "scenario": sc,
            "section_a_candidates": section_a,
            "section_b_candidates": section_b,
            "disqualified_candidates": disqualified,
            "section_a_count": len(section_a),
            "section_b_count": len(section_b),
            "disqualified_count": len(disqualified),
        }

    return results


def write_artifacts(scenarios: List[Dict[str, Any]], results: Dict[str, Any]):
    """Write all v1.2 versioned output artifacts."""
    BENCH_DIR.mkdir(parents=True, exist_ok=True)

    # 1. scenario_matrix.json
    matrix_file = BENCH_DIR / "scenario_matrix.json"
    with open(matrix_file, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, indent=2)
    print(f"[GENERATED] Scenario Matrix: {matrix_file.name} ({len(scenarios)} scenarios)")

    # 2. candidate_generation_results.json
    gen_file = BENCH_DIR / "candidate_generation_results.json"
    with open(gen_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"[GENERATED] Candidate Generation Results: {gen_file.name}")


def main():
    print("[1/2] Generating v1.2 compound-need scenarios (S131+)...")
    scenarios = generate_all_scenarios(n_per_zone=9)  # 9 per zone x 10 zones = 90
    print(f"    Generated {len(scenarios)} scenarios")

    print("[2/3] Executing scenarios through frozen EligibilityEngine & Governance...")
    results = execute_scenarios_through_engine(scenarios)

    print("[3/3] Writing scenario matrix and candidate generation results...")
    write_artifacts(scenarios, results)
    print("[COMPLETED] Benchmark v1.2 scenario generation finished.")


if __name__ == "__main__":
    main()
