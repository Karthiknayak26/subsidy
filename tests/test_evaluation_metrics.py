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


def test_acceptance_criteria_metric_values_validation():
    """Verify evaluator rejects out-of-range, non-finite, boolean, and non-numeric NDCG@3 values."""
    valid_zone_map = {f"S{i:03d}": (i - 11) // 6 + 1 for i in range(11, 71)}
    valid_base = {f"S{i:03d}": 0.60 for i in range(11, 71)}
    valid_model = {f"S{i:03d}": 0.68 for i in range(11, 71)}

    # 1. Out of range: model score > 1.0 (e.g. 5.60)
    corrupted_high = dict(valid_model)
    corrupted_high["S011"] = 5.60
    with pytest.raises(ValueError, match=r"Invalid model NDCG@3 value for scenario S011: 5\.6.*Must be a finite float in \[0\.0, 1\.0\]"):
        evaluate_model_acceptance_criteria(valid_base, corrupted_high, valid_zone_map)

    # 2. Out of range: baseline score < 0.0 (e.g. -0.10)
    corrupted_low = dict(valid_base)
    corrupted_low["S011"] = -0.10
    with pytest.raises(ValueError, match=r"Invalid baseline NDCG@3 value for scenario S011: -0\.1.*Must be a finite float in \[0\.0, 1\.0\]"):
        evaluate_model_acceptance_criteria(corrupted_low, valid_model, valid_zone_map)

    # 3. Non-finite: NaN in model
    corrupted_nan = dict(valid_model)
    corrupted_nan["S011"] = float("nan")
    with pytest.raises(ValueError, match=r"Invalid model NDCG@3 value for scenario S011: nan.*Must be a finite float in \[0\.0, 1\.0\]"):
        evaluate_model_acceptance_criteria(valid_base, corrupted_nan, valid_zone_map)

    # 4. Non-finite: inf in baseline
    corrupted_inf = dict(valid_base)
    corrupted_inf["S011"] = float("inf")
    with pytest.raises(ValueError, match=r"Invalid baseline NDCG@3 value for scenario S011: inf.*Must be a finite float in \[0\.0, 1\.0\]"):
        evaluate_model_acceptance_criteria(corrupted_inf, valid_model, valid_zone_map)

    # 5. Boolean value (True)
    corrupted_bool = dict(valid_model)
    corrupted_bool["S011"] = True
    with pytest.raises(ValueError, match=r"Invalid model NDCG@3 value for scenario S011: True.*Must be a finite float in \[0\.0, 1\.0\]"):
        evaluate_model_acceptance_criteria(valid_base, corrupted_bool, valid_zone_map)


def test_evaluate_standalone_ranking_system_full_and_topk():
    """Verify evaluate_standalone_ranking_system computes accurate metrics for both full and top-k rankings."""
    from src.evaluation.metrics import (
        evaluate_standalone_ranking_system,
        FROZEN_BENCHMARK_SECTION_A_CANDIDATES,
        FROZEN_BENCHMARK_ZONE_MAP
    )

    # Build canonical consensus labels (all integer scores in {0, 1, 2, 3})
    valid_labels = {}
    full_rankings = {}
    top3_rankings = {}

    for sid in [f"S{i:03d}" for i in range(11, 71)]:
        cands = list(FROZEN_BENCHMARK_SECTION_A_CANDIDATES[sid])
        # Assign descending integer scores
        sc_map = {}
        for idx, cid in enumerate(cands):
            sc_map[cid] = max(0, 3 - idx)
        valid_labels[sid] = sc_map
        full_rankings[sid] = cands  # perfect full ranking
        top3_rankings[sid] = cands[:3]  # perfect top-3 ranking

    # 1. Full ranking evaluation
    res_full = evaluate_standalone_ranking_system(full_rankings, valid_labels, allow_top_k=False)
    assert math.isclose(res_full["global_mean_ndcg3"], 1.0, rel_tol=1e-5)
    assert math.isclose(res_full["global_mean_mrr"], 1.0, rel_tol=1e-5)
    assert len(res_full["ndcg3_by_scenario"]) == 60
    assert len(res_full["mrr_by_scenario"]) == 60
    assert len(res_full["zone_mean_ndcg3"]) == 10
    for z in range(1, 11):
        assert math.isclose(res_full["zone_mean_ndcg3"][z], 1.0, rel_tol=1e-5)

    # 2. Top-3 ranking evaluation with IDCG from all candidate labels
    res_top3 = evaluate_standalone_ranking_system(top3_rankings, valid_labels, allow_top_k=True)
    assert math.isclose(res_top3["global_mean_ndcg3"], 1.0, rel_tol=1e-5)
    assert math.isclose(res_top3["global_mean_mrr"], 1.0, rel_tol=1e-5)


def test_evaluate_standalone_idcg_computed_from_all_candidates():
    """Verify IDCG is computed from all Section A candidates, properly penalizing sub-optimal top-3."""
    from src.evaluation.metrics import evaluate_standalone_ranking_system, FROZEN_BENCHMARK_SECTION_A_CANDIDATES

    # Create scenario labels where top candidate has score 3, but ranking supplies bottom 3 candidates
    valid_labels = {}
    suboptimal_top3 = {}

    for sid in [f"S{i:03d}" for i in range(11, 71)]:
        cands = list(FROZEN_BENCHMARK_SECTION_A_CANDIDATES[sid])
        sc_map = {cid: 0 for cid in cands}
        # First candidate is highly relevant (3), others are 0 or 1
        sc_map[cands[0]] = 3
        if len(cands) > 1:
            sc_map[cands[1]] = 1
        valid_labels[sid] = sc_map
        # System omitted the score-3 candidate and returns worst candidates
        suboptimal_top3[sid] = cands[1:4] if len(cands) >= 4 else cands[1:]

    res = evaluate_standalone_ranking_system(suboptimal_top3, valid_labels, allow_top_k=True)
    # NDCG should be substantially lower than 1.0 because ideal DCG includes the omitted score-3 candidate
    assert res["global_mean_ndcg3"] < 0.60


def test_evaluate_standalone_candidate_set_negative_tests():
    """Verify negative validation paths: missing candidates, unknown schemes, duplicates, invalid scores, malformed zones."""
    from src.evaluation.metrics import evaluate_standalone_ranking_system, FROZEN_BENCHMARK_SECTION_A_CANDIDATES

    valid_labels = {}
    valid_rankings = {}
    for sid in [f"S{i:03d}" for i in range(11, 71)]:
        cands = list(FROZEN_BENCHMARK_SECTION_A_CANDIDATES[sid])
        valid_labels[sid] = {cid: 2 for cid in cands}
        valid_rankings[sid] = list(cands)

    # 1. Missing candidate in ranking when allow_top_k=False
    bad_rankings = dict(valid_rankings)
    bad_rankings["S011"] = valid_rankings["S011"][:-1]
    with pytest.raises(ValueError, match=r"Scenario S011 ranking must contain each expected Section A candidate exactly once\. Missing:"):
        evaluate_standalone_ranking_system(bad_rankings, valid_labels, allow_top_k=False)

    # 2. Unknown scheme ID in ranking
    bad_rankings_unknown = dict(valid_rankings)
    bad_rankings_unknown["S011"] = list(valid_rankings["S011"]) + ["SCH999_UNKNOWN"]
    with pytest.raises(ValueError, match=r"Scenario S011 ranking contains unknown scheme IDs: \['SCH999_UNKNOWN'\]"):
        evaluate_standalone_ranking_system(bad_rankings_unknown, valid_labels, allow_top_k=False)

    # 3. Duplicate scheme ID in ranking
    bad_rankings_dup = dict(valid_rankings)
    bad_rankings_dup["S011"] = [valid_rankings["S011"][0]] + list(valid_rankings["S011"])
    with pytest.raises(ValueError, match=r"Scenario S011 ranking contains duplicate scheme IDs"):
        evaluate_standalone_ranking_system(bad_rankings_dup, valid_labels, allow_top_k=False)

    # 4. Missing candidate in consensus labels
    bad_labels_missing = dict(valid_labels)
    bad_labels_missing["S011"] = {k: v for k, v in valid_labels["S011"].items() if k != "SCH001"}
    with pytest.raises(ValueError, match=r"Scenario S011 consensus labels mismatch expected Section A candidates\. Missing: \['SCH001'\]"):
        evaluate_standalone_ranking_system(valid_rankings, bad_labels_missing)

    # 5. Unknown scheme in consensus labels
    bad_labels_unknown = dict(valid_labels)
    bad_labels_unknown["S011"] = dict(valid_labels["S011"])
    bad_labels_unknown["S011"]["SCH999_FAKE"] = 2
    with pytest.raises(ValueError, match=r"Scenario S011 consensus labels mismatch expected Section A candidates.*Extra: \['SCH999_FAKE'\]"):
        evaluate_standalone_ranking_system(valid_rankings, bad_labels_unknown)

    # 6. Invalid consensus score: non-integer float (2.5)
    bad_labels_float = dict(valid_labels)
    bad_labels_float["S011"] = dict(valid_labels["S011"])
    bad_labels_float["S011"]["SCH001"] = 2.5
    with pytest.raises(ValueError, match=r"Invalid consensus relevance score for scenario S011, scheme SCH001: 2\.5"):
        evaluate_standalone_ranking_system(valid_rankings, bad_labels_float)

    # 7. Invalid consensus score: boolean True
    bad_labels_bool = dict(valid_labels)
    bad_labels_bool["S011"] = dict(valid_labels["S011"])
    bad_labels_bool["S011"]["SCH001"] = True
    with pytest.raises(ValueError, match=r"Invalid consensus relevance score for scenario S011, scheme SCH001: True"):
        evaluate_standalone_ranking_system(valid_rankings, bad_labels_bool)

    # 8. Invalid consensus score: out of range (4)
    bad_labels_high = dict(valid_labels)
    bad_labels_high["S011"] = dict(valid_labels["S011"])
    bad_labels_high["S011"]["SCH001"] = 4
    with pytest.raises(ValueError, match=r"Invalid consensus relevance score for scenario S011, scheme SCH001: 4"):
        evaluate_standalone_ranking_system(valid_rankings, bad_labels_high)

    # 9. Malformed zone mapping: boolean zone ID
    valid_zone_map = {f"S{i:03d}": (i - 11) // 6 + 1 for i in range(11, 71)}
    bad_zone_bool = dict(valid_zone_map)
    bad_zone_bool["S011"] = True
    with pytest.raises(ValueError, match=r"Invalid zone ID type for scenario S011: True \(bool\)\. Must be integer\."):
        evaluate_standalone_ranking_system(valid_rankings, valid_labels, bad_zone_bool)

    # 10. Malformed zone mapping: zone swap
    swapped_zone = dict(valid_zone_map)
    swapped_zone["S011"] = 2
    with pytest.raises(ValueError, match=r"Scenario S011 is assigned to zone 2, expected zone 1"):
        evaluate_standalone_ranking_system(valid_rankings, valid_labels, swapped_zone)





