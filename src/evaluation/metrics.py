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
    scenarios = sorted(baseline_ndcg_by_scenario.keys())
    assert len(scenarios) == 60, f"Expected 60 scenarios, got {len(scenarios)}"
    
    diffs = []
    zone_diffs: Dict[int, List[float]] = {z: [] for z in range(1, 11)}
    
    for sid in scenarios:
        b_val = baseline_ndcg_by_scenario[sid]
        m_val = model_ndcg_by_scenario[sid]
        delta = m_val - b_val
        diffs.append(delta)
        
        zone = scenario_to_zone_map[sid]
        zone_diffs[zone].append(delta)
    
    global_mean_delta, p_value = paired_permutation_test(diffs, n_permutations=10000, seed=42)
    
    zone_means = {z: float(np.mean(zone_diffs[z])) for z in range(1, 11)}
    zone_regressions = {z: m for z, m in zone_means.items() if m < 0.0}
    
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
