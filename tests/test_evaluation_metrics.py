"""
tests/test_evaluation_metrics.py
--------------------------------
Automated test suite verifying the mathematical correctness and edge cases
of pre-registered evaluation metrics and acceptance gates.
"""

import math
import pytest
from src.evaluation.metrics import (
    compute_dcg_at_k,
    compute_ndcg_at_k,
    compute_mrr,
    paired_permutation_test,
    evaluate_model_acceptance_criteria
)


def test_ndcg_exponential_gain_and_discount():
    """Verify standard exponential gain (2^y - 1) and logarithmic discounting."""
    # Scores: [3, 2, 1]
    # Gains: [7, 3, 1]
    # Discounts: [log2(2)=1, log2(3)=1.58496..., log2(4)=2.0]
    expected_dcg = 7.0 / 1.0 + 3.0 / math.log2(3) + 1.0 / 2.0
    actual_dcg = compute_dcg_at_k([3, 2, 1], k=3)
    assert math.isclose(actual_dcg, expected_dcg, rel_tol=1e-5)

    # Perfect ranking NDCG@3 must be exactly 1.0
    assert math.isclose(compute_ndcg_at_k([3, 2, 1], k=3), 1.0, rel_tol=1e-5)


def test_ndcg_edge_case_all_zero_idcg():
    """Verify Edge Case 1: when all candidate scores are 0, NDCG@3 is defined as 0.0."""
    scores = [0, 0, 0, 0]
    assert compute_ndcg_at_k(scores, k=3) == 0.0
    assert compute_ndcg_at_k([], k=3) == 0.0


def test_ndcg_edge_case_short_lists():
    """Verify Edge Case 2: short candidate lists (K < 3) evaluate over available items."""
    scores = [2, 1]  # K=2
    # Ideal: [2, 1] -> perfect order -> 1.0
    assert math.isclose(compute_ndcg_at_k(scores, k=3), 1.0, rel_tol=1e-5)
    # Reverse order: [1, 2]
    dcg = (2**1 - 1) / 1.0 + (2**2 - 1) / math.log2(3)
    idcg = (2**2 - 1) / 1.0 + (2**1 - 1) / math.log2(3)
    assert math.isclose(compute_ndcg_at_k([1, 2], k=3), dcg / idcg, rel_tol=1e-5)


def test_mrr_threshold_and_edge_case():
    """Verify MRR threshold tau=2.0 and Edge Case 3 (no hit -> 0.0)."""
    # Hit at rank 1 (score 3 >= 2)
    assert compute_mrr([3, 1, 0], threshold=2.0) == 1.0
    # Hit at rank 2 (score 1 < 2, score 2 >= 2)
    assert compute_mrr([1, 2, 0], threshold=2.0) == 0.5
    # Hit at rank 3 (score 0, 1, 2)
    assert math.isclose(compute_mrr([0, 1, 2], threshold=2.0), 1.0 / 3.0, rel_tol=1e-5)
    # Edge Case 3: No score >= 2 -> 0.0
    assert compute_mrr([1, 0, 1], threshold=2.0) == 0.0
    assert compute_mrr([], threshold=2.0) == 0.0


def test_paired_permutation_test_properties():
    """Verify paired permutation test calculation."""
    # Null case: all differences zero
    mean_diff, p_val = paired_permutation_test([0.0] * 60, n_permutations=1000, seed=42)
    assert mean_diff == 0.0
    assert p_val == 1.0

    # Significant case: large positive differences
    diffs = [0.15] * 60
    mean_diff, p_val = paired_permutation_test(diffs, n_permutations=1000, seed=42)
    assert math.isclose(mean_diff, 0.15)
    assert p_val < 0.005


def test_acceptance_criteria_gate_logic():
    """Verify acceptance criteria requires all 3 gates simultaneously."""
    scenario_to_zone = {f"S{i:03d}": (i - 11) // 6 + 1 for i in range(11, 71)}
    
    # Case A: Passes all 3 gates (+0.08 uniform gain across all zones)
    base_ndcg = {f"S{i:03d}": 0.60 for i in range(11, 71)}
    model_pass = {f"S{i:03d}": 0.68 for i in range(11, 71)}
    res_pass = evaluate_model_acceptance_criteria(base_ndcg, model_pass, scenario_to_zone)
    assert res_pass["overall_accepted"] is True
    assert res_pass["gate1_passed_substantive_gain"] is True
    assert res_pass["gate2_passed_statistical_significance"] is True
    assert res_pass["gate3_passed_zone_non_regression"] is True

    # Case B: High global gain (+0.07) but Zone 3 regresses (-0.02)
    model_regressed = dict(model_pass)
    # Zone 3 scenarios: S023 - S028
    for sid in [f"S{i:03d}" for i in range(23, 29)]:
        model_regressed[sid] = 0.58  # 0.58 - 0.60 = -0.02
    res_fail_zone = evaluate_model_acceptance_criteria(base_ndcg, model_regressed, scenario_to_zone)
    assert res_fail_zone["gate3_passed_zone_non_regression"] is False
    assert res_fail_zone["overall_accepted"] is False
    assert 3 in res_fail_zone["regressed_zones"]
