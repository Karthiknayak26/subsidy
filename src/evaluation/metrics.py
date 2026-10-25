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


FROZEN_BENCHMARK_ZONE_MAP: Dict[str, int] = {
    f"S{i:03d}": (i - 11) // 6 + 1 for i in range(11, 71)
}


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
    
    # 2. Validate metric values, zone ID types, ranges, and exact benchmark zone assignments
    for sid in sorted(EXPECTED_SCENARIOS):
        b_val = baseline_ndcg_by_scenario[sid]
        m_val = model_ndcg_by_scenario[sid]
        
        # Metric value integrity: must be finite numeric values in [0.0, 1.0] (reject bool, NaN, inf, <0, >1)
        if isinstance(b_val, bool) or not isinstance(b_val, (int, float)) or not math.isfinite(b_val) or not (0.0 <= b_val <= 1.0):
            raise ValueError(
                f"Invalid baseline NDCG@3 value for scenario {sid}: {b_val!r}. Must be a finite float in [0.0, 1.0]."
            )
        if isinstance(m_val, bool) or not isinstance(m_val, (int, float)) or not math.isfinite(m_val) or not (0.0 <= m_val <= 1.0):
            raise ValueError(
                f"Invalid model NDCG@3 value for scenario {sid}: {m_val!r}. Must be a finite float in [0.0, 1.0]."
            )

        delta = float(m_val) - float(b_val)
        diffs.append(delta)
        
        zone = scenario_to_zone_map[sid]
        
        # Gap A hardening: Reject booleans, floats, strings, and non-integer types
        if isinstance(zone, bool) or not isinstance(zone, int):
            raise ValueError(
                f"Invalid zone ID type for scenario {sid}: {zone!r} ({type(zone).__name__}). Must be integer."
            )
        
        if zone not in range(1, 11):
            raise ValueError(f"Invalid zone ID: {zone} for scenario {sid}. Must be integer between 1 and 10.")
        
        # Gap B hardening: Validate exact frozen scenario-to-zone assignment
        expected_zone = FROZEN_BENCHMARK_ZONE_MAP[sid]
        if zone != expected_zone:
            raise ValueError(
                f"Scenario {sid} is assigned to zone {zone}, expected zone {expected_zone} per Benchmark v1.0.4 specification."
            )
        
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


from src.evaluation.benchmark_candidates import FROZEN_BENCHMARK_SECTION_A_CANDIDATES


def evaluate_standalone_ranking_system(
    rankings_by_scenario: Dict[str, Sequence[str]],
    consensus_labels_by_scenario: Dict[str, Dict[str, int]],
    scenario_to_zone_map: Optional[Dict[str, int]] = None,
    allow_top_k: bool = False
) -> Dict[str, Any]:
    """
    Evaluates a single ranking system (e.g. the frozen deterministic heuristic baseline)
    independently against frozen consensus relevance ground truth for Benchmark v1.0.4.
    
    STRICT CONTROLS ENFORCED:
    1. Rejects missing/extra benchmark scenario keys (strictly S011-S070).
    2. Enforces exact frozen scenario-to-zone mapping and strict integer zone types (Z1-Z10).
    3. Validates consensus labels: every scenario must have labels for exactly all
       expected Section A candidates, and every label must be an integer in {0, 1, 2, 3}.
    4. Validates rankings:
       - No duplicate scheme IDs.
       - No unknown scheme IDs.
       - Unless allow_top_k is True, must contain each expected Section A candidate exactly once.
       - If allow_top_k is True, must be a non-empty subset of valid Section A candidates.
    5. Calculates IDCG@3 from ALL eligible Section A candidate labels, preventing
       distortion when partial top-k recommendation lists are evaluated.
    """
    if scenario_to_zone_map is None:
        scenario_to_zone_map = FROZEN_BENCHMARK_ZONE_MAP
    
    EXPECTED_SCENARIOS = {f"S{i:03d}": None for i in range(11, 71)}
    expected_keys = set(EXPECTED_SCENARIOS.keys())
    
    # 1. Validate scenario keys
    ranking_keys = set(rankings_by_scenario.keys())
    if ranking_keys != expected_keys:
        missing = expected_keys - ranking_keys
        extra = ranking_keys - expected_keys
        raise ValueError(
            f"Rankings scenario keys mismatch Benchmark v1.0.4. Missing: {sorted(missing)}, Extra: {sorted(extra)}"
        )
    
    consensus_keys = set(consensus_labels_by_scenario.keys())
    if consensus_keys != expected_keys:
        missing = expected_keys - consensus_keys
        extra = consensus_keys - expected_keys
        raise ValueError(
            f"Consensus labels scenario keys mismatch Benchmark v1.0.4. Missing: {sorted(missing)}, Extra: {sorted(extra)}"
        )

    zone_map_keys = set(scenario_to_zone_map.keys())
    if zone_map_keys != expected_keys:
        missing = expected_keys - zone_map_keys
        extra = zone_map_keys - expected_keys
        raise ValueError(
            f"Scenario-to-zone map keys mismatch Benchmark v1.0.4. Missing: {sorted(missing)}, Extra: {sorted(extra)}"
        )

    # 2. Strict Zone Validation
    zone_scenario_counts: Dict[int, int] = {z: 0 for z in range(1, 11)}
    for sid in sorted(expected_keys):
        zone = scenario_to_zone_map[sid]
        if isinstance(zone, bool) or not isinstance(zone, int):
            raise ValueError(
                f"Invalid zone ID type for scenario {sid}: {zone!r} ({type(zone).__name__}). Must be integer."
            )
        if zone not in range(1, 11):
            raise ValueError(f"Invalid zone ID: {zone} for scenario {sid}. Must be integer between 1 and 10.")
        expected_zone = FROZEN_BENCHMARK_ZONE_MAP[sid]
        if zone != expected_zone:
            raise ValueError(
                f"Scenario {sid} is assigned to zone {zone}, expected zone {expected_zone} per Benchmark v1.0.4 specification."
            )
        zone_scenario_counts[zone] += 1

    for z in range(1, 11):
        if zone_scenario_counts[z] != 6:
            raise ValueError(
                f"Zone Z{z} has {zone_scenario_counts[z]} scenarios; expected exactly 6 scenarios for Benchmark v1.0.4."
            )

    # 3. Candidate-Set and Score Integrity Validation
    ndcg_by_scenario: Dict[str, float] = {}
    mrr_by_scenario: Dict[str, float] = {}
    zone_ndcg: Dict[int, List[float]] = {z: [] for z in range(1, 11)}
    zone_mrr: Dict[int, List[float]] = {z: [] for z in range(1, 11)}

    for sid in sorted(expected_keys):
        expected_cands = FROZEN_BENCHMARK_SECTION_A_CANDIDATES[sid]
        expected_set = set(expected_cands)
        labels = consensus_labels_by_scenario[sid]
        ranked_schemes = rankings_by_scenario[sid]
        zone = scenario_to_zone_map[sid]

        # Validate consensus labels candidate set
        label_set = set(labels.keys())
        if label_set != expected_set:
            missing_labels = sorted(expected_set - label_set)
            extra_labels = sorted(label_set - expected_set)
            raise ValueError(
                f"Scenario {sid} consensus labels mismatch expected Section A candidates. "
                f"Missing: {missing_labels}, Extra: {extra_labels}"
            )

        # Validate consensus label score values: integer in {0, 1, 2, 3}
        for scheme_id, score in labels.items():
            if isinstance(score, bool) or not isinstance(score, int) or score not in (0, 1, 2, 3):
                raise ValueError(
                    f"Invalid consensus relevance score for scenario {sid}, scheme {scheme_id}: {score!r}. "
                    f"Must be an integer in {{0, 1, 2, 3}}."
                )

        # Validate rankings
        if not isinstance(ranked_schemes, Sequence) or isinstance(ranked_schemes, (str, bytes)):
            raise ValueError(f"Scenario {sid} ranking must be a sequence of scheme IDs, got {type(ranked_schemes).__name__}.")

        if len(ranked_schemes) != len(set(ranked_schemes)):
            raise ValueError(f"Scenario {sid} ranking contains duplicate scheme IDs: {ranked_schemes}")

        unknown_schemes = sorted(set(ranked_schemes) - expected_set)
        if unknown_schemes:
            raise ValueError(f"Scenario {sid} ranking contains unknown scheme IDs: {unknown_schemes}")

        if not allow_top_k:
            if set(ranked_schemes) != expected_set:
                missing_candidates = sorted(expected_set - set(ranked_schemes))
                raise ValueError(
                    f"Scenario {sid} ranking must contain each expected Section A candidate exactly once. "
                    f"Missing: {missing_candidates}"
                )
        else:
            if len(ranked_schemes) == 0:
                raise ValueError(f"Scenario {sid} ranking cannot be empty.")

        # Compute DCG@3 on the provided ranking
        score_vector = [float(labels[scheme_id]) for scheme_id in ranked_schemes]
        dcg_val = compute_dcg_at_k(score_vector, k=3)

        # IDCG@3 is strictly computed from ALL Section A candidates for this scenario
        all_candidate_scores = [float(labels[c]) for c in expected_cands]
        ideal_scores = sorted(all_candidate_scores, reverse=True)
        idcg_val = compute_dcg_at_k(ideal_scores, k=3)

        ndcg_val = (dcg_val / idcg_val) if idcg_val > 0.0 else 0.0
        mrr_val = compute_mrr(score_vector, threshold=2.0)

        ndcg_by_scenario[sid] = ndcg_val
        mrr_by_scenario[sid] = mrr_val
        zone_ndcg[zone].append(ndcg_val)
        zone_mrr[zone].append(mrr_val)

    global_mean_ndcg = float(np.mean(list(ndcg_by_scenario.values())))
    global_mean_mrr = float(np.mean(list(mrr_by_scenario.values())))

    zone_mean_ndcg = {z: float(np.mean(zone_ndcg[z])) for z in range(1, 11)}
    zone_mean_mrr = {z: float(np.mean(zone_mrr[z])) for z in range(1, 11)}

    return {
        "global_mean_ndcg3": global_mean_ndcg,
        "global_mean_mrr": global_mean_mrr,
        "ndcg3_by_scenario": ndcg_by_scenario,
        "mrr_by_scenario": mrr_by_scenario,
        "zone_mean_ndcg3": zone_mean_ndcg,
        "zone_mean_mrr": zone_mean_mrr
    }


