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


def test_acceptance_criteria_validation_fail_closed():
    """Verify acceptance gate fails closed when inputs, scenario keys, or zones are malformed."""
    valid_zone_map = {f"S{i:03d}": (i - 11) // 6 + 1 for i in range(11, 71)}
    valid_base = {f"S{i:03d}": 0.60 for i in range(11, 71)}
    valid_model = {f"S{i:03d}": 0.68 for i in range(11, 71)}

    # 1. Missing scenario in baseline (59 scenarios)
    incomplete_base = {k: v for k, v in valid_base.items() if k != "S011"}
    with pytest.raises(ValueError, match="Baseline scenario keys mismatch"):
        evaluate_model_acceptance_criteria(incomplete_base, valid_model, valid_zone_map)

    # 2. Missing scenario in model
    incomplete_model = {k: v for k, v in valid_model.items() if k != "S070"}
    with pytest.raises(ValueError, match="Model scenario keys mismatch"):
        evaluate_model_acceptance_criteria(valid_base, incomplete_model, valid_zone_map)

    # 3. Invalid zone ID (e.g. Zone 11)
    bad_zone_map = dict(valid_zone_map)
    bad_zone_map["S011"] = 11
    with pytest.raises(ValueError, match="Invalid zone ID: 11"):
        evaluate_model_acceptance_criteria(valid_base, valid_model, bad_zone_map)

    # 4. Empty/missing zone (e.g. S065-S070 mapped to Zone 9 instead of Zone 10, leaving Zone 10 with 0 scenarios)
    missing_z10_map = dict(valid_zone_map)
    for sid in [f"S{i:03d}" for i in range(65, 71)]:
        missing_z10_map[sid] = 9  # Zone 9 gets 12 scenarios, Zone 10 gets 0
    with pytest.raises(ValueError, match=r"Scenario S\d+ is assigned to zone 9, expected zone 10"):
        evaluate_model_acceptance_criteria(valid_base, valid_model, missing_z10_map)


def test_acceptance_criteria_zone_id_strict_types():
    """Verify Gap A: zone IDs must strictly be integers (reject bool True/False, float 1.0, etc.)."""
    valid_zone_map = {f"S{i:03d}": (i - 11) // 6 + 1 for i in range(11, 71)}
    valid_base = {f"S{i:03d}": 0.60 for i in range(11, 71)}
    valid_model = {f"S{i:03d}": 0.68 for i in range(11, 71)}

    # Test True (which in Python compares equal to 1)
    bool_map = dict(valid_zone_map)
    bool_map["S011"] = True
    with pytest.raises(ValueError, match=r"Invalid zone ID type for scenario S011: True \(bool\)\. Must be integer\."):
        evaluate_model_acceptance_criteria(valid_base, valid_model, bool_map)

    # Test float 1.0 (which compares equal to 1)
    float_map = dict(valid_zone_map)
    float_map["S011"] = 1.0
    with pytest.raises(ValueError, match=r"Invalid zone ID type for scenario S011: 1\.0 \(float\)\. Must be integer\."):
        evaluate_model_acceptance_criteria(valid_base, valid_model, float_map)


def test_acceptance_criteria_balanced_but_incorrect_zone_swap():
    """Verify Gap B: swapping 6 scenarios between Zone 1 and Zone 2 is strictly rejected."""
    valid_zone_map = {f"S{i:03d}": (i - 11) // 6 + 1 for i in range(11, 71)}
    valid_base = {f"S{i:03d}": 0.60 for i in range(11, 71)}
    valid_model = {f"S{i:03d}": 0.68 for i in range(11, 71)}

    # Swap Zone 1 (S011-S016) and Zone 2 (S017-S022) assignments
    # Counts remain exactly 6 per zone, but mappings are wrong
    swapped_map = dict(valid_zone_map)
    for sid in [f"S{i:03d}" for i in range(11, 17)]:
        swapped_map[sid] = 2
    for sid in [f"S{i:03d}" for i in range(17, 23)]:
        swapped_map[sid] = 1

    with pytest.raises(ValueError, match=r"Scenario S011 is assigned to zone 2, expected zone 1 per Benchmark v1\.0\.4 specification\."):
        evaluate_model_acceptance_criteria(valid_base, valid_model, swapped_map)


