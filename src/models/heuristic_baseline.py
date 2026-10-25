"""
heuristic_baseline.py
---------------------
Deterministic Heuristic Baseline Ranking Model for Benchmark v1.0.4.
Implements the pre-specified Baseline 1 (Need-to-Scheme Mapping) and
Baseline 2 (Transparent Weighted Heuristic) from benchmark_v1_design.md.
"""

import json
from pathlib import Path
from typing import Dict, List, Sequence, Any, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

PRIMARY_NEED_SCHEME_MAP = {
    "SOLAR_PUMP_INSTALLATION": {"SCH006"},
    "SOIL_HEALTH_AND_FERTILIZER": {"SCH009"},
    "PRODUCTION_CREDIT": {"SCH008_CENTRAL"},
    "INCOME_SUPPORT": {"SCH001"},
    "BOREWELL_IRRIGATION": {"SCH010_AMBEDKAR", "SCH010_VALMIKI", "SCH010_DEVARAJ_URS", "SCH010_KMDC"},
    "RAINWATER_HARVESTING": {"SCH005"},
    "FARM_MECHANIZATION": {"SCH004"},
    "MICRO_IRRIGATION_SUPPORT": {"SCH003"},
    "PROTECTED_HORTICULTURE": {"SCH007"},
}

SECONDARY_NEED_SCHEME_MAP = {
    "CROP_INSURANCE": {"SCH001", "SCH008_CENTRAL"},
    "PRODUCTION_CREDIT": {"SCH001"},
    "SOLAR_PUMP_INSTALLATION": {"SCH003", "SCH008_CENTRAL"},
    "RAINWATER_HARVESTING": {"SCH003"},
    "MICRO_IRRIGATION_SUPPORT": {"SCH005", "SCH008_CENTRAL"},
    "BOREWELL_IRRIGATION": {"SCH003", "SCH008_CENTRAL"},
}


def compute_heuristic_relevance(scheme_id: str, immediate_need: str) -> float:
    """Computes the static heuristic relevance score on a 0-3 ordinal scale."""
    if scheme_id in PRIMARY_NEED_SCHEME_MAP.get(immediate_need, set()):
        return 3.0
    if scheme_id in SECONDARY_NEED_SCHEME_MAP.get(immediate_need, set()):
        return 2.0
    if scheme_id in {"SCH001", "SCH009"}:
        return 1.0
    return 0.0


def rank_scenario_candidates(
    scenario_id: str,
    candidate_schemes: Sequence[str],
    immediate_need: str
) -> List[str]:
    """
    Ranks Section A candidate schemes for a single scenario:
    Sorts by heuristic score descending, with deterministic tie-breaking by scheme ID ascending.
    """
    return sorted(
        candidate_schemes,
        key=lambda s: (-compute_heuristic_relevance(s, immediate_need), s)
    )


def generate_baseline_rankings(
    scenario_needs_map: Optional[Dict[str, str]] = None
) -> Dict[str, List[str]]:
    """Generates deterministic heuristic rankings for all Benchmark v1.0.4 scenarios (S011-S070)."""
    from src.evaluation.benchmark_candidates import FROZEN_BENCHMARK_SECTION_A_CANDIDATES
    
    if scenario_needs_map is None:
        scenario_needs_map = {}
        for z in range(1, 11):
            z_path = REPO_ROOT / f"data/benchmarks/z{z}/z{z}_scenarios.json"
            if z_path.exists():
                with open(z_path, "r", encoding="utf-8") as f:
                    for sc in json.load(f):
                        scenario_needs_map[sc["scenario_id"]] = sc["immediate_need"]
                        
    rankings: Dict[str, List[str]] = {}
    for sid, candidates in FROZEN_BENCHMARK_SECTION_A_CANDIDATES.items():
        need = scenario_needs_map.get(sid)
        if not need:
            raise KeyError(f"Missing immediate need for scenario {sid}")
        rankings[sid] = rank_scenario_candidates(sid, candidates, need)
        
    return rankings
