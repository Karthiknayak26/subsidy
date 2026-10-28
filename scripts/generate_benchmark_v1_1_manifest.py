"""
generate_benchmark_v1_1_manifest.py
-----------------------------------
Generates the 60-scenario compound-need matrix for Benchmark v1.1 (S071–S130),
executes every scenario through the frozen EligibilityEngine, applies statutory
governance presentation rules, and records empirical candidate generation results.
"""

import json
import os
import sys
from dataclasses import fields
from pathlib import Path
from typing import Dict, Any, List

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.eligibility.models import (
    FarmerScenario,
    EligibilityStatus,
    AvailabilityState,
    GovtEmployeeCategory,
    BorewellElectricStatus,
    SchemeDetermination
)
from src.eligibility.engine import EligibilityEngine
from src.eligibility.governance import apply_governance_safeguard, PROVISIONAL_SCHEMES

ZONE_INFO = {
    1: {"name": "North Eastern Transition Zone", "districts": ["Bidar", "Kalaburagi"]},
    2: {"name": "North Eastern Dry Zone", "districts": ["Kalaburagi", "Yadgir", "Raichur"]},
    3: {"name": "Northern Dry Zone", "districts": ["Vijayapura", "Bagalkot", "Gadag", "Koppal"]},
    4: {"name": "Central Dry Zone", "districts": ["Chitradurga", "Davanagere", "Tumakuru"]},
    5: {"name": "Eastern Dry Zone", "districts": ["Kolar", "Chikkaballapura", "Bengaluru Rural", "Ramanagara"]},
    6: {"name": "Southern Dry Zone", "districts": ["Mandya", "Mysuru", "Chamarajanagar"]},
    7: {"name": "Southern Transition Zone", "districts": ["Hassan", "Shivamogga", "Chikkamagaluru"]},
    8: {"name": "Northern Transition Zone", "districts": ["Dharwad", "Belagavi", "Haveri"]},
    9: {"name": "Hilly Zone", "districts": ["Kodagu", "Chikkamagaluru", "Uttara Kannada"]},
    10: {"name": "Coastal Zone", "districts": ["Dakshina Kannada", "Udupi", "Uttara Kannada"]},
}

ARCHETYPES = [
    {
        "id": "ARCH_1",
        "name": "Water Infrastructure Failure + Seasonal Working-Capital Constraints",
        "description": "Borewell failure or water depletion mid-season coupled with urgent cash requirements for crop input purchases.",
        "primary_crisis": "Critical water infrastructure failure (dried/failed borewell or pump burnout during high-demand stage)",
        "secondary_constraints": ["Severe working capital depletion for seasonal inputs", "High cost of emergency private water access"],
        "engine_immediate_need": "SOLAR_PUMP_INSTALLATION",
        "clinical_tradeoff": "Immediate capital water source/pumping intervention vs. short-term crop credit liquidity",
        "hypothesized_competing_schemes": ["SCH006", "SCH005", "SCH003", "SCH008_CENTRAL", "SCH001"]
    },
    {
        "id": "ARCH_2",
        "name": "Crop/Pest/Climate Distress + Liquidity & Mechanization Constraints",
        "description": "Acute localized crop damage or severe pest infestation with deferred insurance compensation, requiring spray equipment and emergency cash.",
        "primary_crisis": "Acute standing crop infestation or weather shock threatening total yield loss",
        "secondary_constraints": ["Exhaustion of liquid funds for plant protection chemicals", "Lack of efficient spraying machinery"],
        "engine_immediate_need": "CROP_INSURANCE",
        "clinical_tradeoff": "Direct unconditional cash transfer vs. plant protection sprayer procurement subsidy vs. seasonal credit",
        "hypothesized_competing_schemes": ["SCH001", "SCH004", "SCH008_CENTRAL", "SCH009"]
    },
    {
        "id": "ARCH_3",
        "name": "Horticulture Transition + Capital & Irrigation Constraints",
        "description": "Commercial transition from subsistence field crops to high-value horticulture under acute groundwater depletion and high setup costs.",
        "primary_crisis": "High upfront capital barrier for protected horticulture structures (shade net/polyhouse)",
        "secondary_constraints": ["Need for precision micro-irrigation installation", "Specialized micronutrient and soil testing"],
        "engine_immediate_need": "PROTECTED_HORTICULTURE",
        "clinical_tradeoff": "Protected structure capital subsidy (MIDH) vs. micro-irrigation capital subsidy (PDMC) vs. rainwater pond (Krishi Bhagya)",
        "hypothesized_competing_schemes": ["SCH007", "SCH003", "SCH005", "SCH008_CENTRAL", "SCH009"]
    },
    {
        "id": "ARCH_4",
        "name": "Informal Tenancy + Labor or Equipment-Access Constraints",
        "description": "Tenant farmer operating on oral lease without recorded RTC land titles, facing acute agricultural labor shortages and credit exclusion.",
        "primary_crisis": "Severe seasonal labor shortages during critical sowing/harvesting operations without land title documentation",
        "secondary_constraints": ["Exclusion from title-tied central cash welfare (PM-KISAN)", "Exclusion from standard commercial mortgage credit"],
        "engine_immediate_need": "FARM_MECHANIZATION",
        "clinical_tradeoff": "Mechanization procurement/CHC subsidy vs. diagnostic soil advisory vs. tenant credit review",
        "hypothesized_competing_schemes": ["SCH004", "SCH009", "SCH008_CENTRAL"]
    },
    {
        "id": "ARCH_5",
        "name": "Dry-Spell Resilience + Competing Water-Management Options",
        "description": "Rainfed drought-vulnerable smallholder seeking water security through farm ponds, community borewells, or drip lines.",
        "primary_crisis": "Recurring prolonged dry-spells threatening rainfed crop survival across critical vegetative stages",
        "secondary_constraints": ["Evaluating physical rainwater harvesting vs. groundwater lift vs. water distribution piping", "Limited beneficiary contribution funds"],
        "engine_immediate_need": "RAINWATER_HARVESTING",
        "clinical_tradeoff": "Farm pond package (Krishi Bhagya) vs. Community borewell (Ganga Kalyana SC) vs. Micro-irrigation (PDMC)",
        "hypothesized_competing_schemes": ["SCH005", "SCH010_AMBEDKAR", "SCH003", "SCH008_CENTRAL", "SCH001"]
    },
    {
        "id": "ARCH_6",
        "name": "Soil-Health & Nutrient Exhaustion + Operational Input Imbalance",
        "description": "Intensive monocropping plot experiencing nutrient depletion, salinity from canal seepage, or excessive fertilizer costs.",
        "primary_crisis": "Acute soil fertility degradation and crop yellowing/deficiency reducing operational margins",
        "secondary_constraints": ["High cost of chemical fertilizers", "Need for soil testing diagnostic and input credit"],
        "engine_immediate_need": "SOIL_HEALTH_AND_FERTILIZER",
        "clinical_tradeoff": "Diagnostic nutrient advisory (SHC) vs. seasonal input working capital credit (KCC-MISS) vs. income liquidity (PM-KISAN)",
        "hypothesized_competing_schemes": ["SCH009", "SCH008_CENTRAL", "SCH001", "SCH004"]
    }
]

# Agrarian crop profiles tailored to Karnataka's 10 zones
ZONE_CROPS = {
    1: {"primary": ["Redgram", "Soybean", "Bengalgram", "Sugarcane", "Jowar", "Cotton"], "hort": "Tomato"},
    2: {"primary": ["Cotton", "Paddy", "Sunflower", "Groundnut", "Bajra", "Redgram"], "hort": "Chilli"},
    3: {"primary": ["Maize", "Bengalgram", "Sunflower", "Jowar", "Groundnut", "Wheat"], "hort": "Pomegranate"},
    4: {"primary": ["Groundnut", "Ragi", "Maize", "Onion", "Sunflower", "Cotton"], "hort": "Papaya"},
    5: {"primary": ["Ragi", "Mulberry", "Maize", "Groundnut", "Tomato", "Capsicum"], "hort": "Capsicum"},
    6: {"primary": ["Sugarcane", "Paddy", "Ragi", "Maize", "Banana", "Turmeric"], "hort": "Banana"},
    7: {"primary": ["Paddy", "Maize", "Arecanut", "Ginger", "Coffee", "Ragi"], "hort": "Ginger"},
    8: {"primary": ["Soybean", "Cotton", "Maize", "Groundnut", "Chilli", "Wheat"], "hort": "Chilli"},
    9: {"primary": ["Coffee", "Black Pepper", "Cardamom", "Arecanut", "Paddy", "Ginger"], "hort": "Black Pepper"},
    10: {"primary": ["Paddy", "Arecanut", "Coconut", "Cashew", "Black Pepper", "Vegetables"], "hort": "Cashew"}
}

SOCIAL_CATEGORIES = ["SC", "ST", "OBC (2A)", "OBC (3A)", "OBC (3B)", "General (OC)", "Minority (Muslim)"]


def build_scenario_profile(scenario_id: str, zone_id: int, arch_idx: int) -> Dict[str, Any]:
    z_info = ZONE_INFO[zone_id]
    arch = ARCHETYPES[arch_idx]
    crops = ZONE_CROPS[zone_id]
    
    # Deterministic rotation of districts, crops, and social categories
    district = z_info["districts"][(arch_idx + zone_id) % len(z_info["districts"])]
    crop_primary = crops["hort"] if arch_idx == 2 else crops["primary"][arch_idx % len(crops["primary"])]
    crop_secondary = crops["primary"][(arch_idx + 1) % len(crops["primary"])]
    social_cat = SOCIAL_CATEGORIES[(zone_id + arch_idx) % len(SOCIAL_CATEGORIES)]
    
    # Archetype specific attributes
    is_pure_tenant = (arch_idx == 3)  # Archetype 4 is oral tenancy
    
    # Water & Asset infrastructure
    if arch_idx == 0:  # Water failure
        # Has an unenergized offgrid borewell needing solar pumping OR dried borewell
        water_src = "Borewell (Non-energized)"
        elec_status = "UNENERGIZED_OFF_GRID"
        assets = ["Borewell (Non-energized, Yield 1.5 inch)"]
        land_type = "Dryland (Rainfed)"
        land_size = 3.0
        farmer_cat = "Small [2.5, 5.0]"
        immediate_need = "SOLAR_PUMP_INSTALLATION"
    elif arch_idx == 1:  # Crop/pest crisis
        water_src = "Rainfed Dryland (No borewell or open well present)"
        elec_status = "NONE"
        assets = []
        land_type = "Dryland (Rainfed)"
        land_size = 2.2
        farmer_cat = "Marginal (< 2.5 acres)"
        immediate_need = "CROP_INSURANCE"
    elif arch_idx == 2:  # Horticulture transition
        water_src = "Open Well / Borewell (Energized IP Set)"
        elec_status = "GRID_CONNECTED_IP_SET"
        assets = ["Open Well", "Diesel Pump"]
        land_type = "Dryland (Rainfed)" if zone_id in [1, 2, 3, 4, 5, 8] else "Canal-irrigated"
        land_size = 3.5
        farmer_cat = "Small [2.5, 5.0]"
        immediate_need = "PROTECTED_HORTICULTURE"
    elif arch_idx == 3:  # Tenancy + equipment
        water_src = "Canal Outlet / Shared Borewell"
        elec_status = "NONE"
        assets = []
        land_type = "Canal-irrigated" if zone_id in [1, 6, 7] else "Dryland (Rainfed)"
        land_size = 2.5
        farmer_cat = "Small [2.5, 5.0]"
        immediate_need = "FARM_MECHANIZATION"
    elif arch_idx == 4:  # Dry-spell resilience
        water_src = "Rainfed Dryland (No borewell or open well present)"
        elec_status = "NONE"
        assets = []
        land_type = "Dryland (Rainfed)"
        land_size = 3.8
        farmer_cat = "Small [2.5, 5.0]"
        immediate_need = "RAINWATER_HARVESTING"
    else:  # Soil health & input constraints
        water_src = "Canal Outlet" if zone_id in [1, 2, 6] else "Borewell (Grid-Connected IP Set)"
        elec_status = "GRID_CONNECTED_IP_SET" if "Borewell" in water_src else "NONE"
        assets = ["Farm Implements"]
        land_type = "Canal-irrigated" if "Canal" in water_src else "Dryland (Rainfed)"
        land_size = 4.2
        farmer_cat = "Small [2.5, 5.0]"
        immediate_need = "SOIL_HEALTH_AND_FERTILIZER"

    # Family income & holding
    income = round(1.2 + (arch_idx * 0.15) + (zone_id * 0.05), 2)
    
    narrative = (
        f"Farmer in {district} ({z_info['name']}) cultivating {crop_primary} and {crop_secondary} on {land_size} acres. "
        f"Primary acute situation: {arch['primary_crisis'].lower()}. "
        f"Compounding constraints: {'; '.join(arch['secondary_constraints']).lower()}."
    )
    
    profile = {
        "scenario_id": scenario_id,
        "benchmark_version": "v1.1",
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
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": "NONE",
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": not is_pure_tenant,
        "is_pure_tenant_without_land_title": is_pure_tenant,
        "borewell_electric_status": elec_status,
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
            "land_classification": farmer_cat
        },
        "water_and_irrigation": {
            "operational_water_source": water_src,
            "borewell_electric_status": elec_status
        },
        "compound_need_details": {
            "archetype_id": arch["id"],
            "archetype_name": arch["name"],
            "primary_acute_crisis": arch["primary_crisis"],
            "secondary_constraints": arch["secondary_constraints"],
            "narrative": narrative,
            "engine_immediate_need_mapping": arch["engine_immediate_need"],
            "clinical_tradeoff_definition": arch["clinical_tradeoff"],
            "hypothesized_competing_schemes": arch["hypothesized_competing_schemes"],
            "statutory_considerations": (
                "KCC-MISS provides concessional short-term crop loans up to Rs. 3 Lakh (4% prompt repayment), not debt restructuring. "
                "SMAM provides capital procurement subsidies for machinery and CHC establishment, not custom hiring access. "
                "PMFBY requires gazetted IU notifications and is held in Section B."
            )
        },
        "source_backed_interventions": {
            "SCH001": "PM-KISAN: Unconditional direct cash transfer (Rs. 6,000/yr in 3 installments) providing emergency farm liquidity (pmkisan.gov.in).",
            "SCH002": "PMFBY: Yield-based crop insurance indemnity claim coverage for notified crops (pmfby.gov.in) — quarantined in Section B pending seasonal IU orders.",
            "SCH003": "PMKSY-PDMC: 45-55% capital subsidy for drip/sprinkler micro-irrigation installation, capped at 5.0 ha per beneficiary (pmksy.gov.in).",
            "SCH004": "SMAM: Capital subsidy (40-50%) for individual farm machinery procurement or Custom Hiring Centre establishment (agrimachinery.nic.in) — distinct from operational equipment hiring.",
            "SCH005": "Krishi Bhagya: In-situ rainwater harvesting package (farm pond, polythene lining, diesel/solar lifting pump) for notified dryland taluks (raitamitra.karnataka.gov.in).",
            "SCH006": "PM-KUSUM Component B: 60% combined subsidy for standalone solar agriculture pumps (up to 7.5 HP) strictly on unenergized off-grid water sources (pmkusum.mnre.gov.in).",
            "SCH007": "MIDH: Capital subsidy for protected cultivation structures (greenhouse, polyhouse, shade net) and quality planting material for horticultural crops (midh.gov.in).",
            "SCH008_CENTRAL": "Central KCC-MISS: Concessional short-term agricultural crop loan up to Rs. 3 Lakh at 4% effective interest upon prompt repayment for seasonal input working capital (financialservices.gov.in) — strictly not debt restructuring.",
            "SCH009": "Soil Health Card: 100% free statutory diagnostic soil nutrient testing and balanced fertilizer recommendations (soilhealth.dac.gov.in)."
        }
    }
    return profile


def generate_all_scenarios() -> List[Dict[str, Any]]:
    scenarios = []
    current_sid = 71
    for z in range(1, 11):
        for arch_idx in range(6):
            sid = f"S{current_sid:03d}"
            sc = build_scenario_profile(sid, z, arch_idx)
            scenarios.append(sc)
            current_sid += 1
    assert len(scenarios) == 60
    assert scenarios[0]["scenario_id"] == "S071"
    assert scenarios[-1]["scenario_id"] == "S130"
    return scenarios


def execute_scenarios_through_engine(scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
    engine = EligibilityEngine()
    results = {}
    
    valid_fields = {f.name for f in fields(FarmerScenario)}
    
    for sc in scenarios:
        sid = sc["scenario_id"]
        # Convert to FarmerScenario dataclass using valid engine input fields
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
                "disqualifying_factors": gov["disqualifying_factors"]
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
            "disqualified_count": len(disqualified)
        }
        
    return results


def write_artifacts(scenarios: List[Dict[str, Any]], results: Dict[str, Any]):
    bench_dir = REPO_ROOT / "data/benchmarks/v1.1"
    bench_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. scenario_matrix.json
    matrix_file = bench_dir / "scenario_matrix.json"
    with open(matrix_file, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, indent=2)
    print(f"[GENERATED] Scenario Matrix: {matrix_file.name} ({len(scenarios)} scenarios)")
    
    # 2. candidate_generation_results.json
    gen_file = bench_dir / "candidate_generation_results.json"
    with open(gen_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"[GENERATED] Candidate Generation Results: {gen_file.name}")
    
    # 3. benchmark_v1.1_scenario_manifest.md
    manifest_md = REPO_ROOT / "research/dataset_research/benchmark_v1.1_scenario_manifest.md"
    generate_markdown_manifest(scenarios, results, manifest_md)
    print(f"[GENERATED] Markdown Manifest: {manifest_md.name}")


def generate_markdown_manifest(
    scenarios: List[Dict[str, Any]],
    results: Dict[str, Any],
    out_path: Path
):
    lines = [
        "# Benchmark v1.1 Scenario Manifest & Candidate Specification",
        "",
        "**Benchmark Version:** `v1.1` (Compound-Need Re-Architecture)  ",
        "**Scenario Range:** `S071` through `S130` ($N = 60$)  ",
        "**Coverage:** 10 Agro-Climatic Zones (Z1–Z10), 6 Scenarios Per Zone  ",
        "**Eligibility Engine:** Deterministic Frozen Engine (`commit 7724fa7`)  ",
        "**Status:** Preflight Candidate Generation Complete — Pending Annotation Packet Distribution  ",
        "",
        "---",
        "",
        "## 1. Candidate Set Size Distribution (Empirically Observed)",
        "",
        "| Section A Candidate Count | Number of Scenarios | Percentage | Clinical Characterization |",
        "| :---: | :---: | :---: | :--- |"
    ]
    
    from collections import Counter
    sec_a_counts = [res["section_a_count"] for res in results.values()]
    dist = Counter(sec_a_counts)
    total_sc = len(scenarios)
    
    for c in sorted(dist.keys()):
        pct = (dist[c] / total_sc) * 100
        desc = "Restricted choice (e.g. oral tenancy title exclusions)" if c <= 3 else (
            "Standard multi-scheme pool (field crops + credit + liquidity)" if c <= 5 else (
                "Rich competitive pool (horticulture/solar + credit + mechanization)"
            )
        )
        lines.append(f"| **{c} schemes** | {dist[c]} | {pct:.1f}% | {desc} |")
        
    mean_sz = sum(sec_a_counts) / len(sec_a_counts)
    lines.extend([
        "",
        f"- **Mean Section A Candidates per Scenario:** `{mean_sz:.2f}` (Observed Empirical Distribution)",
        f"- **Candidate Range:** `{min(sec_a_counts)}` to `{max(sec_a_counts)}` schemes",
        "",
        "---",
        "",
        "## 2. 60-Scenario Master Manifest Table (S071–S130)",
        "",
        "| SID | Zone | District | Archetype | Primary Crop | Land (ac) | Primary Acute Crisis | Section A Candidates (Eligible) | Section B (Review Only) |",
        "| :---: | :---: | :--- | :--- | :--- | :---: | :--- | :--- | :--- |"
    ])
    
    for sc in scenarios:
        sid = sc["scenario_id"]
        res = results[sid]
        z_id = sc["zone_id"]
        dist = sc["district"]
        crop = sc["crop_primary"]
        land = sc["land_size_acres"]
        arch_id = sc["compound_need_details"]["archetype_id"]
        crisis = sc["compound_need_details"]["primary_acute_crisis"][:50] + "..."
        sec_a_str = ", ".join(f"`{c['scheme_id']}`" for c in res["section_a_candidates"])
        sec_b_str = ", ".join(f"`{c['scheme_id']}`" for c in res["section_b_candidates"])
        lines.append(f"| **{sid}** | `{z_id}` | {dist} | `{arch_id}` | {crop} | {land} | {crisis} | {sec_a_str} | {sec_b_str} |")
        
    lines.extend([
        "",
        "---",
        "",
        "## 3. Statutory Intervention Dictionary",
        "",
        "Every candidate scheme's factual intervention is strictly bounded by official government circulars:",
        "",
        "| Scheme ID | Scheme Name | Statutory Intervention Scope | Official Mandate Citation |",
        "| :--- | :--- | :--- | :--- |",
        "| `SCH001` | PM-KISAN | Direct unconditional income support (Rs. 6,000/yr) providing emergency farm liquidity. | `pmkisan.gov.in` |",
        "| `SCH002` | PMFBY | Yield/weather-indexed crop loss indemnity insurance — quarantined in Section B pending seasonal IU orders. | `pmfby.gov.in` |",
        "| `SCH003` | PMKSY-PDMC | 45–55% capital subsidy for drip/sprinkler installation (capped at 5.0 ha per beneficiary). | `pmksy.gov.in` |",
        "| `SCH004` | SMAM | 40–50% capital procurement subsidy for farm machinery and CHC establishment — distinct from hiring service access. | `agrimachinery.nic.in` |",
        "| `SCH005` | Krishi Bhagya | Integrated in-situ rainwater harvesting package (farm pond, lining, diesel/solar lift pump) for notified dryland taluks. | `raitamitra.karnataka.gov.in` |",
        "| `SCH006` | PM-KUSUM B | 60% capital subsidy for standalone solar agriculture pumps strictly on unenergized off-grid water sources. | `pmkusum.mnre.gov.in` |",
        "| `SCH007` | MIDH | Capital assistance for protected cultivation structures (polyhouse, shade net) and quality planting material for horticulture. | `midh.gov.in` |",
        "| `SCH008_CENTRAL` | Central KCC-MISS | Concessional short-term crop credit (up to Rs. 3 Lakh at 4% prompt repayment) for seasonal operational inputs — strictly not debt restructuring. | `financialservices.gov.in` |",
        "| `SCH009` | Soil Health Card | 100% free statutory diagnostic soil nutrient testing and crop-specific fertilizer recommendations. | `soilhealth.dac.gov.in` |",
        "| `SCH010_AMBEDKAR` | Ganga Kalyana (SC) | 100% subsidized individual borewell drilling with pump energization for SC small/marginal dryland farmers (1.5–5.0 ac). | `adcl.karnataka.gov.in` |",
        "",
        "---",
        "",
        "*(Automatically compiled by `scripts/generate_benchmark_v1_1_manifest.py`)*",
        ""
    ])
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    print("[1/3] Generating 60 v1.1 compound-need scenarios (S071–S130)...")
    scenarios = generate_all_scenarios()
    
    print("[2/3] Executing scenarios through frozen EligibilityEngine & Governance...")
    results = execute_scenarios_through_engine(scenarios)
    
    print("[3/3] Writing scenario matrix, execution results, and Markdown manifest...")
    write_artifacts(scenarios, results)
    print("[COMPLETED] Benchmark v1.1 Manifest and Execution Pipeline Finished Cleanly.")


if __name__ == "__main__":
    main()
