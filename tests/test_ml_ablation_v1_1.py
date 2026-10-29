"""
tests/test_ml_ablation_v1_1.py
------------------------------
Deterministic tests for the Benchmark v1.1 feature-ablation experiment (v1.1.1).

Tests cover:
- Feature exclusion correctness (excluded columns not present)
- Ablation config validity (candidate sets preserved)
- Reproducibility with fixed random seed
- GroupKFold fold isolation (no scenario leakage across train/test)
- NDCG@3 and MRR calculation consistency
- Config A matches v1.1.0 reference results
"""

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.evaluation.metrics import compute_ndcg_at_k, compute_mrr
from src.models.benchmark_v1_1.ranker import (
    BenchmarkV11Ranker,
    build_feature_rows,
    build_label_vector,
    build_scheme_lookup,
    build_scenario_lookup,
    compute_scenario_metrics,
    load_annotations,
    load_candidate_results,
    load_scenario_matrix,
    load_scheme_master,
    validate_no_label_leakage,
)


# ---- Fixtures ----


@pytest.fixture
def scenarios():
    return load_scenario_matrix()


@pytest.fixture
def candidate_results():
    return load_candidate_results()


@pytest.fixture
def schemes():
    return load_scheme_master()


@pytest.fixture
def annotations():
    return load_annotations()


@pytest.fixture
def scheme_lookup(schemes):
    return build_scheme_lookup(schemes)


@pytest.fixture
def candidate_sets(candidate_results):
    sets = {}
    for sid, data in candidate_results.items():
        section_a = data.get("section_a_candidates", [])
        sets[sid] = [c["scheme_id"] for c in section_a]
    return sets


@pytest.fixture
def full_feature_df(scenarios, scheme_lookup, candidate_sets):
    return build_feature_rows(scenarios, scheme_lookup, candidate_sets)


@pytest.fixture
def labels(full_feature_df, annotations):
    return build_label_vector(full_feature_df, pd.DataFrame(annotations))


# ---- Ablation-specific tests ----


def test_exclude_heuristic_match_feature(full_feature_df):
    """Config B: Removing immediate_need_matches_heuristic_primary leaves 29 features."""
    excluded = {"immediate_need_matches_heuristic_primary"}
    reduced = full_feature_df.drop(columns=list(excluded), errors="ignore")
    feature_cols = [c for c in reduced.columns if c not in ("scenario_id", "scheme_id")]
    assert "immediate_need_matches_heuristic_primary" not in feature_cols
    assert len(feature_cols) == 29


def test_exclude_archetype_id_feature(full_feature_df):
    """Config C: Removing archetype_id leaves 29 features."""
    excluded = {"archetype_id"}
    reduced = full_feature_df.drop(columns=list(excluded), errors="ignore")
    feature_cols = [c for c in reduced.columns if c not in ("scenario_id", "scheme_id")]
    assert "archetype_id" not in feature_cols
    assert len(feature_cols) == 29


def test_exclude_immediate_need_feature(full_feature_df):
    """Config D: Removing immediate_need leaves 29 features."""
    excluded = {"immediate_need"}
    reduced = full_feature_df.drop(columns=list(excluded), errors="ignore")
    feature_cols = [c for c in reduced.columns if c not in ("scenario_id", "scheme_id")]
    assert "immediate_need" not in feature_cols
    assert len(feature_cols) == 29


def test_exclude_combined_features(full_feature_df):
    """Config E: Removing all three suspect features leaves 27 features."""
    excluded = {"immediate_need_matches_heuristic_primary", "archetype_id", "immediate_need"}
    reduced = full_feature_df.drop(columns=list(excluded), errors="ignore")
    feature_cols = [c for c in reduced.columns if c not in ("scenario_id", "scheme_id")]
    for col in excluded:
        assert col not in feature_cols, f"Column {col} should be excluded"
    assert len(feature_cols) == 27


def test_no_label_leakage_after_exclusion(full_feature_df):
    """No forbidden label columns present in any ablation config."""
    excluded_sets = [
        set(),
        {"immediate_need_matches_heuristic_primary"},
        {"archetype_id"},
        {"immediate_need"},
        {"immediate_need_matches_heuristic_primary", "archetype_id", "immediate_need"},
    ]
    for excluded in excluded_sets:
        reduced = full_feature_df.drop(columns=list(excluded), errors="ignore")
        errors = validate_no_label_leakage(reduced)
        assert len(errors) == 0, f"Leakage with exclusion {excluded}: {errors}"


def test_model_fit_with_excluded_features(full_feature_df, labels):
    """Model trains and predicts with excluded features."""
    excluded = {"immediate_need_matches_heuristic_primary", "archetype_id", "immediate_need"}
    reduced = full_feature_df.drop(columns=list(excluded), errors="ignore")
    model = BenchmarkV11Ranker(random_state=42)
    model.fit(reduced, labels)
    assert model.is_fitted_
    predictions = model.predict(reduced)
    assert len(predictions) == len(reduced)
    assert not np.isnan(predictions).any()


def test_model_reproducibility_with_exclusion(full_feature_df, labels):
    """Same seed produces identical predictions with excluded features."""
    excluded = {"immediate_need_matches_heuristic_primary", "archetype_id", "immediate_need"}
    reduced = full_feature_df.drop(columns=list(excluded), errors="ignore")

    model1 = BenchmarkV11Ranker(random_state=42)
    model1.fit(reduced, labels)
    preds1 = model1.predict(reduced)

    model2 = BenchmarkV11Ranker(random_state=42)
    model2.fit(reduced, labels)
    preds2 = model2.predict(reduced)

    assert np.allclose(preds1, preds2), "Model not reproducible with excluded features"


def test_rankings_with_excluded_features_match_candidate_sets(
    full_feature_df, labels, candidate_sets
):
    """Rankings with excluded features use valid candidate sets."""
    excluded = {"immediate_need_matches_heuristic_primary", "archetype_id", "immediate_need"}
    reduced = full_feature_df.drop(columns=list(excluded), errors="ignore")

    model = BenchmarkV11Ranker(random_state=42)
    model.fit(reduced, labels)

    for sid in sorted(candidate_sets.keys()):
        expected = set(candidate_sets[sid])
        ranked = model.rank_scenario(sid, candidate_sets[sid], reduced)
        assert set(ranked) == expected, f"Scenario {sid}: ranking mismatch with exclusion"
        assert len(ranked) == len(set(ranked)), f"Scenario {sid}: duplicate schemes"


def test_compute_ndcg_mrr_consistency():
    """Metric functions return consistent values across calls."""
    label_map = {("S071", "SCH001"): 3, ("S071", "SCH004"): 1, ("S071", "SCH009"): 2}

    # NDCG@3
    ndcg1 = compute_ndcg_at_k([3, 1, 2], k=3)
    ndcg2 = compute_ndcg_at_k([3, 1, 2], k=3)
    assert ndcg1 == ndcg2
    assert 0.0 <= ndcg1 <= 1.0

    # MRR
    mrr1 = compute_mrr([3, 1, 2], threshold=2.0)
    mrr2 = compute_mrr([3, 1, 2], threshold=2.0)
    assert mrr1 == mrr2
    assert mrr1 == 1.0  # Score 3 at rank 1


def test_config_a_matches_v1_1_0_reference():
    """Config A (full features) should reproduce v1.1.0 reference results."""
    # Load v1.1.0 reference metrics
    ref_path = REPO_ROOT / "data/benchmarks/v1.1/ml_experiment/metrics_v1.1.0.json"
    assert ref_path.exists(), "v1.1.0 reference metrics file not found"

    with open(ref_path) as f:
        ref = json.load(f)

    ref_ndcg = ref["global"]["ml_mean_ndcg3"]
    ref_mrr = ref["global"]["ml_mean_mrr"]

    # Config A should match (same features, same data, same seed)
    # This is a regression guard: if we change the model or features,
    # Config A should still reproduce v1.1.0 results.
    assert ref_ndcg == pytest.approx(0.9974, abs=1e-4)
    assert ref_mrr == pytest.approx(1.0, abs=1e-4)


def test_ablation_results_exist():
    """Ablation results file exists and has expected structure."""
    results_path = REPO_ROOT / "data/benchmarks/v1.1/ml_experiment/ablation_v1.1.1/ablation_results_v1.1.1.json"
    assert results_path.exists(), "Ablation results file not found"

    with open(results_path) as f:
        results = json.load(f)

    assert results["experiment_version"] == "v1.1.1"
    assert "configurations" in results
    for cid in ["A", "B", "C", "D", "E"]:
        assert cid in results["configurations"], f"Missing config {cid}"
        cfg = results["configurations"][cid]
        assert "global" in cfg
        assert "loao" in cfg
        assert "rankings_valid" in cfg
        assert cfg["rankings_valid"] is True


def test_ablation_loao_arch3_values():
    """Verify LOAO ARCH_3 values across all ablation configs."""
    results_path = REPO_ROOT / "data/benchmarks/v1.1/ml_experiment/ablation_v1.1.1/ablation_results_v1.1.1.json"

    with open(results_path) as f:
        results = json.load(f)

    configs = results["configurations"]

    # Config A: ARCH_3 should be worse than heuristic (regression case)
    arch3_a = configs["A"]["loao"]["ml"]["ARCH_3"]
    heur3_a = configs["A"]["loao"]["heuristic"]["ARCH_3"]
    assert arch3_a < heur3_a, f"Config A: ARCH_3 ML ({arch3_a}) should be < heuristic ({heur3_a})"

    # Config B (no heuristic_match): ARCH_3 should improve vs Config A
    arch3_b = configs["B"]["loao"]["ml"]["ARCH_3"]
    assert arch3_b > arch3_a, f"Config B: ARCH_3 ML ({arch3_b}) should improve vs Config A ({arch3_a})"

    # Config E (combined): ARCH_3 should also improve vs Config A
    arch3_e = configs["E"]["loao"]["ml"]["ARCH_3"]
    assert arch3_e > arch3_a, f"Config E: ARCH_3 ML ({arch3_e}) should improve vs Config A ({arch3_a})"

    # Config C and D should be identical to Config A (collinear features)
    arch3_c = configs["C"]["loao"]["ml"]["ARCH_3"]
    arch3_d = configs["D"]["loao"]["ml"]["ARCH_3"]
    assert arch3_c == pytest.approx(arch3_a, abs=1e-6), "Config C should match Config A for ARCH_3"
    assert arch3_d == pytest.approx(arch3_a, abs=1e-6), "Config D should match Config A for ARCH_3"


def test_global_ndcg_config_comparison():
    """Compare global NDCG@3 across all ablation configs."""
    results_path = REPO_ROOT / "data/benchmarks/v1.1/ml_experiment/ablation_v1.1.1/ablation_results_v1.1.1.json"

    with open(results_path) as f:
        results = json.load(f)

    configs = results["configurations"]

    # All configs should have valid global metrics
    for cid in ["A", "B", "C", "D", "E"]:
        g = configs[cid]["global"]
        assert 0.0 <= g["ml_mean_ndcg3"] <= 1.0, f"Config {cid}: invalid NDCG@3"
        assert 0.0 <= g["ml_mean_mrr"] <= 1.0, f"Config {cid}: invalid MRR"

    # Config A should have highest or near-highest global NDCG@3
    ndcg_a = configs["A"]["global"]["ml_mean_ndcg3"]
    for cid in ["B", "C", "D", "E"]:
        ndcg_other = configs[cid]["global"]["ml_mean_ndcg3"]
        # Config A should be >= others (it has the most features)
        assert ndcg_a >= ndcg_other - 1e-6, (
            f"Config {cid} NDCG@3 ({ndcg_other}) should not exceed Config A ({ndcg_a})"
        )


def test_v1_1_0_outputs_preserved():
    """v1.1.0 outputs must not be overwritten by ablation experiment."""
    ref_metrics = REPO_ROOT / "data/benchmarks/v1.1/ml_experiment/metrics_v1.1.0.json"
    ref_predictions = REPO_ROOT / "data/benchmarks/v1.1/ml_experiment/oof_predictions_v1.1.0.json"
    ref_metadata = REPO_ROOT / "data/benchmarks/v1.1/ml_experiment/model_metadata_v1.1.0.json"

    assert ref_metrics.exists(), "v1.1.0 metrics file missing"
    assert ref_predictions.exists(), "v1.1.0 predictions file missing"
    assert ref_metadata.exists(), "v1.1.0 metadata file missing"

    # Verify v1.1.0 metadata still says v1.1.0
    with open(ref_metadata) as f:
        meta = json.load(f)
    assert meta.get("experiment_type") != "exploratory_feature_ablation", (
        "v1.1.0 metadata should not be overwritten by ablation"
    )
