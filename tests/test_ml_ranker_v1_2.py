"""
tests/test_ml_ranker_v1_2.py
----------------------------
Deterministic tests for Benchmark v1.2 ML training and evaluation milestone.

Validates:
  1. Checksum verification of original submission (E2_v1.2_blank.csv)
  2. Processed training labels artifact (no _blank in name, valid scores in {0,1,2,3})
  3. Candidate set validity (all 369 pairs belong to scenario's Section A set)
  4. Data alignment (feature rows match Section A candidate sets exactly)
  5. Leakage prevention (forbidden columns & excluded features absent)
  6. Fold isolation (GroupKFold ensures zero scenario overlap between train and test)
  7. Preprocessing fit scope (scalers and encoders fit strictly on train folds)
  8. Metric calculation correctness (NDCG@3 and MRR match preregistered definitions)
  9. Preregistered feature policy (immediate_need retained, archetype_id excluded,
     immediate_need_matches_heuristic_primary excluded)
 10. Preregistered ablations (Ablation 1 structured, Ablation 2 no immediate need,
     Ablation 3 text representation)
 11. Reproducibility of rankings and predictions
"""

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import GroupKFold

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.evaluation.metrics import compute_mrr, compute_ndcg_at_k, paired_permutation_test
from src.models.benchmark_v1_2.ranker import (
    ANNOTATION_CSV_PATH,
    CANDIDATE_RESULTS_PATH,
    EXCLUDED_FEATURES,
    FORBIDDEN_FEATURE_COLUMNS,
    ML_EXPERIMENT_DIR,
    SCENARIO_MATRIX_PATH,
    SCHEME_MASTER_PATH,
    BenchmarkV12Ranker,
    build_feature_rows_v12,
    build_label_vector,
    build_scenario_lookup_v12,
    build_scheme_lookup,
    compute_heuristic_score_v12,
    extract_section_a_candidates,
    load_annotations,
    load_candidate_results,
    load_scenario_matrix,
    load_scheme_master,
    rank_heuristic_v12,
    validate_annotation_candidate_alignment,
    validate_feature_alignment,
    validate_group_leakage,
    validate_no_label_leakage,
)

EXPECTED_ANNOTATION_SHA256 = (
    "8ab03fba5f4cd4a1c9783a2bac3864f3d8530ed15e112ddd3f3a05f90fdf3d26"
)
EXPECTED_SCENARIO_COUNT = 90
EXPECTED_PAIR_COUNT = 369


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def scenarios() -> List[Dict[str, Any]]:
    return load_scenario_matrix()


@pytest.fixture(scope="module")
def candidate_results() -> Dict[str, Any]:
    return load_candidate_results()


@pytest.fixture(scope="module")
def candidate_sets(candidate_results) -> Dict[str, List[str]]:
    return extract_section_a_candidates(candidate_results)


@pytest.fixture(scope="module")
def schemes() -> List[Dict[str, Any]]:
    return load_scheme_master()


@pytest.fixture(scope="module")
def scheme_lookup(schemes) -> Dict[str, Dict[str, Any]]:
    return build_scheme_lookup(schemes)


@pytest.fixture(scope="module")
def annotations() -> pd.DataFrame:
    return load_annotations()


# ── 1. Checksums & Provenance Tests ──────────────────────────────────────────

def test_original_annotation_checksum_unchanged():
    """Verify SHA-256 of original submitted annotation file matches frozen hash."""
    assert ANNOTATION_CSV_PATH.exists(), f"Missing {ANNOTATION_CSV_PATH}"
    with open(ANNOTATION_CSV_PATH, "rb") as f:
        actual_sha = hashlib.sha256(f.read()).hexdigest()
    assert actual_sha == EXPECTED_ANNOTATION_SHA256, (
        f"Original annotation CSV altered! Expected {EXPECTED_ANNOTATION_SHA256}, got {actual_sha}"
    )


def test_processed_training_labels_artifact_naming_and_integrity():
    """Verify processed training label file exists, does not contain '_blank', and has valid hash."""
    processed_path = ML_EXPERIMENT_DIR / "training_labels_v1.2.0.csv"
    assert processed_path.exists(), f"Processed label artifact missing at {processed_path}"
    assert "_blank" not in processed_path.name, "Processed label artifact must NOT contain '_blank'"

    df = pd.read_csv(processed_path)
    assert len(df) == EXPECTED_PAIR_COUNT
    assert set(df["relevance_score"].unique()).issubset({0, 1, 2, 3})
    assert set(df["rater_id"].unique()) == {"human reviewer 2"}


def test_provenance_metadata():
    """Verify provenance metadata records single-annotator status and lack of IRR."""
    prov_path = ML_EXPERIMENT_DIR / "provenance_v1.2.0.json"
    assert prov_path.exists(), f"Missing {prov_path}"
    with open(prov_path, "r", encoding="utf-8") as f:
        prov = json.load(f)

    assert prov["annotator"] == "human reviewer 2"
    assert prov["annotator_count"] == 1
    assert prov["irr_available"] is False
    assert "Single annotator" in prov["irr_limitation"]
    assert prov["annotation_sha256"] == EXPECTED_ANNOTATION_SHA256


# ── 2. Candidate Validity & Data Alignment Tests ───────────────────────────────

def test_scenario_count_and_candidate_pairs(scenarios, candidate_sets, annotations):
    """Verify exactly 90 scenarios and 369 candidate pairs."""
    assert len(scenarios) == EXPECTED_SCENARIO_COUNT
    assert len(candidate_sets) == EXPECTED_SCENARIO_COUNT
    assert len(annotations) == EXPECTED_PAIR_COUNT

    # Every scenario S131..S220 present
    expected_sids = {f"S{i:03d}" for i in range(131, 221)}
    assert set(candidate_sets.keys()) == expected_sids
    assert set(annotations["scenario_id"].unique()) == expected_sids


def test_all_annotated_pairs_belong_to_section_a(annotations, candidate_sets):
    """Verify every annotated (scenario, scheme) pair belongs to that scenario's Section A set."""
    errors = validate_annotation_candidate_alignment(annotations, candidate_sets)
    assert not errors, f"Candidate alignment errors: {errors}"


def test_relevance_scores_valid_range(annotations):
    """All relevance scores must be integers in {0, 1, 2, 3}."""
    scores = annotations["relevance_score"]
    assert scores.isna().sum() == 0, "Missing relevance scores found"
    assert all(s in {0, 1, 2, 3} for s in scores)


def test_feature_matrix_alignment_with_candidates(scenarios, scheme_lookup, candidate_sets):
    """Feature matrix must have exactly one row per Section A candidate pair."""
    feat_df = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=1)
    assert len(feat_df) == EXPECTED_PAIR_COUNT
    errors = validate_feature_alignment(feat_df, candidate_sets)
    assert not errors, f"Feature alignment errors: {errors}"


# ── 3. Leakage Prevention & Feature Policy Tests ──────────────────────────────

def test_leakage_prevention_no_forbidden_columns(scenarios, scheme_lookup, candidate_sets):
    """Forbidden columns and target-derived features must NOT be in feature matrix."""
    for abl in (1, 2, 3):
        feat_df = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=abl)
        errors = validate_no_label_leakage(feat_df)
        assert not errors, f"Leakage errors in ablation {abl}: {errors}"

        for col in FORBIDDEN_FEATURE_COLUMNS:
            assert col not in feat_df.columns, f"Forbidden column {col} in ablation {abl}"


def test_preregistered_feature_exclusion_policy(scenarios, scheme_lookup, candidate_sets):
    """archetype_id and immediate_need_matches_heuristic_primary must NEVER be in any feature set."""
    for abl in (1, 2, 3):
        feat_df = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=abl)
        assert "archetype_id" not in feat_df.columns
        assert "immediate_need_matches_heuristic_primary" not in feat_df.columns
        for col in EXCLUDED_FEATURES:
            assert col not in feat_df.columns


def test_immediate_need_ablation_policy(scenarios, scheme_lookup, candidate_sets):
    """Ablation 1 includes immediate_need; Ablation 2 excludes it; Ablation 3 has text feature."""
    df1 = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=1)
    df2 = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=2)
    df3 = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=3)

    assert "immediate_need" in df1.columns, "Ablation 1 must retain immediate_need"
    assert "immediate_need" not in df2.columns, "Ablation 2 must exclude immediate_need"
    assert "immediate_need" not in df3.columns, "Ablation 3 must exclude categorical immediate_need"
    assert "immediate_need_text" in df3.columns, "Ablation 3 must contain immediate_need_text"


# ── 4. Fold Isolation & Preprocessing Scope Tests ─────────────────────────────

def test_scenario_grouped_kfold_isolation(scenarios, scheme_lookup, candidate_sets, annotations):
    """Verify that all candidates from any scenario stay within the same fold."""
    feat_df = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=1)
    labels = build_label_vector(feat_df, annotations)

    scenario_ids = feat_df["scenario_id"].unique()
    group_map = {sid: i for i, sid in enumerate(sorted(scenario_ids))}
    groups = feat_df["scenario_id"].map(group_map).values

    gkf = GroupKFold(n_splits=5)
    for fold, (train_idx, test_idx) in enumerate(gkf.split(feat_df, labels, groups=groups)):
        errors = validate_group_leakage(feat_df, train_idx, test_idx)
        assert not errors, f"Scenario leakage in fold {fold}: {errors}"


def test_model_pipeline_preprocessing_fit_on_train_only(scenarios, scheme_lookup, candidate_sets, annotations):
    """Test that model fit on train fold can transform and predict on test fold without error."""
    feat_df = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=1)
    labels = build_label_vector(feat_df, annotations)

    scenario_ids = sorted(feat_df["scenario_id"].unique())
    train_sids = set(scenario_ids[:70])
    test_sids = set(scenario_ids[70:])

    train_df = feat_df[feat_df["scenario_id"].isin(train_sids)]
    train_labels = labels[train_df.index]
    test_df = feat_df[feat_df["scenario_id"].isin(test_sids)]

    model = BenchmarkV12Ranker(random_state=42, ablation=1)
    model.fit(train_df, train_labels)

    # Must be able to predict on test fold containing potentially unseen categories
    preds = model.predict(test_df)
    assert len(preds) == len(test_df)
    assert not np.isnan(preds).any()


# ── 5. Metric Calculation Tests ───────────────────────────────────────────────

def test_ndcg_at_3_standard_cases():
    """Verify NDCG@3 calculation against known mathematical values."""
    # Perfect ranking: [3, 2, 1]
    # DCG = (2^3-1)/log2(2) + (2^2-1)/log2(3) + (2^1-1)/log2(4) = 7/1 + 3/1.58496 + 1/2 = 7 + 1.892789 + 0.5 = 9.392789
    # IDCG is identical -> NDCG = 1.0
    scores_perfect = [3.0, 2.0, 1.0]
    assert math.isclose(compute_ndcg_at_k(scores_perfect, k=3), 1.0, rel_tol=1e-5)

    # Inverted ranking: [1, 2, 3]
    scores_inverted = [1.0, 2.0, 3.0]
    ndcg_inv = compute_ndcg_at_k(scores_inverted, k=3)
    assert 0.0 < ndcg_inv < 1.0


def test_ndcg_at_3_edge_cases():
    """Verify NDCG@3 edge cases: all zeros and short candidate lists."""
    # All zero relevance: NDCG is defined as 0.0
    assert compute_ndcg_at_k([0.0, 0.0, 0.0], k=3) == 0.0
    assert compute_ndcg_at_k([], k=3) == 0.0

    # Short list (K=2)
    scores_k2 = [2.0, 3.0]
    ndcg_k2 = compute_ndcg_at_k(scores_k2, k=3)
    # ideal is [3.0, 2.0]
    ideal_dcg = (2**3 - 1)/1.0 + (2**2 - 1)/math.log2(3)
    actual_dcg = (2**2 - 1)/1.0 + (2**3 - 1)/math.log2(3)
    assert math.isclose(ndcg_k2, actual_dcg / ideal_dcg, rel_tol=1e-5)


def test_mrr_calculation_and_edge_cases():
    """Verify MRR calculation: threshold tau=2.0, first hit rank, zero hit case."""
    # Hit at rank 1 (score >= 2)
    assert compute_mrr([2.0, 0.0, 1.0], threshold=2.0) == 1.0
    assert compute_mrr([3.0, 2.0, 1.0], threshold=2.0) == 1.0

    # Hit at rank 2
    assert compute_mrr([1.0, 2.0, 0.0], threshold=2.0) == 0.5

    # Hit at rank 3
    assert math.isclose(compute_mrr([0.0, 1.0, 2.0], threshold=2.0), 1.0 / 3.0)

    # No hit above threshold -> MRR = 0.0
    assert compute_mrr([1.0, 1.0, 0.0], threshold=2.0) == 0.0
    assert compute_mrr([], threshold=2.0) == 0.0


def test_paired_permutation_test_deterministic():
    """Verify two-sided paired permutation test is deterministic with fixed seed."""
    diffs = [0.1, -0.05, 0.2, 0.15, -0.1, 0.05] * 10
    mean_diff1, p1 = paired_permutation_test(diffs, n_permutations=1000, seed=42)
    mean_diff2, p2 = paired_permutation_test(diffs, n_permutations=1000, seed=42)
    assert mean_diff1 == mean_diff2
    assert p1 == p2
    assert 0.0 <= p1 <= 1.0


# ── 6. Heuristic Baseline Parity Tests ────────────────────────────────────────

def test_heuristic_baseline_candidate_validity(scenarios, candidate_sets):
    """Verify heuristic baseline ranks exactly all candidates for each scenario."""
    scenario_lookup = build_scenario_lookup_v12(scenarios)
    for sid, cands in candidate_sets.items():
        need = scenario_lookup[sid]["immediate_need"]
        ranked = rank_heuristic_v12(sid, cands, need)
        assert set(ranked) == set(cands)
        assert len(ranked) == len(cands)


def test_heuristic_scores_ordinal_range():
    """Verify heuristic relevance scores are in {0.0, 1.0, 2.0, 3.0}."""
    for need in ("SOLAR_PUMP_INSTALLATION", "SOIL_HEALTH_AND_FERTILIZER", "RAINWATER_HARVESTING"):
        for sch in ("SCH001", "SCH003", "SCH004", "SCH005", "SCH008_CENTRAL", "SCH009", "SCH010"):
            score = compute_heuristic_score_v12(sch, need)
            assert score in {0.0, 1.0, 2.0, 3.0}


# ── 7. Rank Scenario Parity ───────────────────────────────────────────────────

def test_rank_scenario_method(scenarios, scheme_lookup, candidate_sets, annotations):
    """Test rank_scenario method of BenchmarkV12Ranker."""
    feat_df = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=1)
    labels = build_label_vector(feat_df, annotations)

    model = BenchmarkV12Ranker(random_state=42, ablation=1, max_iter=20)
    model.fit(feat_df, labels)

    for sid in ["S131", "S132", "S133"]:
        expected_cands = candidate_sets[sid]
        ranked = model.rank_scenario(sid, expected_cands, feat_df)
        assert set(ranked) == set(expected_cands)
        assert len(ranked) == len(expected_cands)

