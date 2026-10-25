"""
src/evaluation/metrics.py
-------------------------
Executable reference implementation of the pre-registered ranking and evaluation
metrics for Benchmark v1.0.4, as specified in:
research/dataset_research/evaluation_preregistration.md

All metric definitions, edge cases, and statistical tests in this module
are permanently locked in accordance with pre-registration protocol.
"""

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple
import numpy as np


def compute_dcg_at_k(scores: Sequence[float], k: int = 3) -> float:
    """
    Computes Discounted Cumulative Gain at rank cutoff k using exponential gain.
    DCG@k = sum_{i=1}^{min(k, len(scores))} (2^y_i - 1) / log2(i + 1)
    """
    dcg = 0.0
    limit = min(k, len(scores))
    for i in range(limit):
        rel = scores[i]
        gain = (2.0 ** rel) - 1.0
        discount = math.log2(i + 2.0)  # i=0 -> rank 1 -> log2(2) = 1.0
        dcg += gain / discount
    return dcg


def compute_ndcg_at_k(scores: Sequence[float], k: int = 3) -> float:
    """
    Computes Normalized Discounted Cumulative Gain at rank cutoff k.
    
    PRE-REGISTERED CONVENTIONS:
    - Gain formulation: 2^y - 1
    - Discount factor: 1 / log2(rank + 1)
    - Edge Case 1: If IDCG@k == 0 (all candidate scores are 0), NDCG@k is defined as 0.0.
    - Edge Case 2: If len(scores) < k, DCG and IDCG evaluate over all available candidates.
    """
    if not scores:
        return 0.0
    
    dcg = compute_dcg_at_k(scores, k=k)
    ideal_scores = sorted(scores, reverse=True)
    idcg = compute_dcg_at_k(ideal_scores, k=k)
    
    if idcg <= 0.0:
        return 0.0
    
    return dcg / idcg


def compute_mrr(scores: Sequence[float], threshold: float = 2.0) -> float:
    """
    Computes Reciprocal Rank for a scenario ranking list.
    
    PRE-REGISTERED CONVENTIONS:
    - Success threshold tau: score >= 2.0 (Relevant or Highly Relevant).
    - If hit occurs at rank r (1-indexed), RR = 1 / r.
    - Edge Case 3: If no candidate achieves score >= threshold, RR is defined as 0.0.
    """
    for rank_idx, rel in enumerate(scores, start=1):
        if rel >= threshold:
            return 1.0 / rank_idx
    return 0.0


def paired_permutation_test(
    diffs: Sequence[float],
    n_permutations: int = 10000,
    seed: Optional[int] = 42
) -> Tuple[float, float]:
    """
    Performs a two-sided paired permutation (randomization) test on per-scenario
    metric differences: d_s = metric_model(s) - metric_baseline(s).
    
    Observation unit: Individual scenario queries (N=60 for Benchmark v1.0.4).
    Null hypothesis: Metric differences are symmetric about 0.
    
    Returns:
        (mean_diff, p_value)
    """
    arr = np.asarray(diffs, dtype=float)
    n = len(arr)
    if n == 0:
        return 0.0, 1.0
    
    obs_mean = float(np.mean(arr))
    obs_stat = abs(obs_mean)
    
    rng = np.random.default_rng(seed)
    
    # Generate random Rademacher signs: c_s in {-1, +1}
    # signs shape: (n_permutations, n)
    signs = rng.choice([-1.0, 1.0], size=(n_permutations, n))
    perm_means = np.mean(signs * arr, axis=1)
    
    extreme_count = np.sum(np.abs(perm_means) >= obs_stat)
    p_value = float((extreme_count + 1) / (n_permutations + 1))
    
    return obs_mean, p_value


def evaluate_model_acceptance_criteria(
    baseline_ndcg_by_scenario: Dict[str, float],
    model_ndcg_by_scenario: Dict[str, float],
    scenario_to_zone_map: Dict[str, int]
) -> Dict[str, Any]:
    """
    Evaluates whether a candidate model satisfies all pre-registered acceptance gates:
    1. Global mean Delta NDCG@3 >= +0.050
    2. Two-sided paired permutation test p < 0.050 (B=10,000)
    3. Zone-level mean Delta NDCG@3_z >= 0.000 for all 10 zones (Z1-Z10).
    """
    EXPECTED_SCENARIOS = {f"S{i:03d}" for i in range(11, 71)}
    
    # 1. Validate exact scenario key sets
    base_keys = set(baseline_ndcg_by_scenario.keys())
    if base_keys != EXPECTED_SCENARIOS:
        missing = EXPECTED_SCENARIOS - base_keys
        extra = base_keys - EXPECTED_SCENARIOS
        raise ValueError(
            f"Baseline scenario keys mismatch Benchmark v1.0.4. Missing: {sorted(missing)}, Extra: {sorted(extra)}"
        )
    
    model_keys = set(model_ndcg_by_scenario.keys())
    if model_keys != EXPECTED_SCENARIOS:
        missing = EXPECTED_SCENARIOS - model_keys
        extra = model_keys - EXPECTED_SCENARIOS
        raise ValueError(
            f"Model scenario keys mismatch Benchmark v1.0.4. Missing: {sorted(missing)}, Extra: {sorted(extra)}"
        )
    
    zone_keys = set(scenario_to_zone_map.keys())
    if zone_keys != EXPECTED_SCENARIOS:
        missing = EXPECTED_SCENARIOS - zone_keys
        extra = zone_keys - EXPECTED_SCENARIOS
        raise ValueError(
            f"Scenario-to-zone map keys mismatch Benchmark v1.0.4. Missing: {sorted(missing)}, Extra: {sorted(extra)}"
        )
    
    diffs = []
    zone_diffs: Dict[int, List[float]] = {z: [] for z in range(1, 11)}
    
    # 2. Validate zone IDs and populate per-scenario and per-zone deltas
    for sid in sorted(EXPECTED_SCENARIOS):
        b_val = baseline_ndcg_by_scenario[sid]
        m_val = model_ndcg_by_scenario[sid]
        delta = m_val - b_val
        diffs.append(delta)
        
        zone = scenario_to_zone_map[sid]
        if zone not in zone_diffs:
            raise ValueError(f"Invalid zone ID: {zone} for scenario {sid}. Must be integer 1 to 10.")
        zone_diffs[zone].append(delta)
    
    # 3. Fail closed on missing or uneven zone scenario allocations (must be exactly 6 per zone)
    for z in range(1, 11):
        count = len(zone_diffs[z])
        if count != 6:
            raise ValueError(
                f"Zone Z{z} has {count} scenarios; expected exactly 6 scenarios for Benchmark v1.0.4."
            )
    
    global_mean_delta, p_value = paired_permutation_test(diffs, n_permutations=10000, seed=42)
    
    zone_means = {}
    zone_regressions = {}
    for z in range(1, 11):
        z_mean = float(np.mean(zone_diffs[z]))
        zone_means[z] = z_mean
        # Fail closed: reject if mean is negative OR NaN
        if math.isnan(z_mean) or z_mean < 0.0:
            zone_regressions[z] = z_mean
    
    gate1_passed = bool(global_mean_delta >= 0.050)
    gate2_passed = bool(p_value < 0.050)
    gate3_passed = bool(len(zone_regressions) == 0)
    
    overall_accepted = gate1_passed and gate2_passed and gate3_passed
    
    return {
        "overall_accepted": overall_accepted,
        "global_mean_delta_ndcg3": global_mean_delta,
        "p_value": p_value,
        "gate1_passed_substantive_gain": gate1_passed,
        "gate2_passed_statistical_significance": gate2_passed,
        "gate3_passed_zone_non_regression": gate3_passed,
        "zone_mean_deltas": zone_means,
        "regressed_zones": zone_regressions
    }
