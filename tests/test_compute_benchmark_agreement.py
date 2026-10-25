"""
tests/test_compute_benchmark_agreement.py
-----------------------------------------
Automated test suite verifying the Benchmark v1.0.4 inter-rater reliability runner,
including genuine ordinal Krippendorff's alpha, quadratic weighted Cohen's kappa,
CSV format ingestion, and pre-registered acceptance gate thresholds.
"""

import copy
import csv
import math
from pathlib import Path
import numpy as np
import pytest

from scripts.compute_benchmark_agreement import (
    compute_quadratic_weighted_kappa,
    compute_ordinal_krippendorff_alpha,
    load_canonical_template_pairs,
    load_paired_annotations_from_csv,
    evaluate_benchmark_agreement,
    generate_markdown_report,
    TARGET_KAPPA_QUADRATIC,
    TARGET_ORDINAL_ALPHA
)


# ---------------------------------------------------------------------------
# 1. Statistical Core Tests: Ordinal Krippendorff's Alpha
# ---------------------------------------------------------------------------

def test_ordinal_krippendorff_alpha_perfect_agreement():
    """Verify alpha is exactly 1.0 under complete agreement across categories."""
    ratings = np.array([
        [0, 1, 2, 3, 0, 1, 2, 3],
        [0, 1, 2, 3, 0, 1, 2, 3]
    ], dtype=float)
    alpha = compute_ordinal_krippendorff_alpha(ratings)
    assert math.isclose(alpha, 1.0, rel_tol=1e-5)


def test_ordinal_krippendorff_alpha_systematic_disagreement():
    """Verify alpha is strongly negative when raters systematically diverge maximally."""
    ratings = np.array([
        [0, 0, 0, 0],
        [3, 3, 3, 3]
    ], dtype=float)
    alpha = compute_ordinal_krippendorff_alpha(ratings)
    assert alpha < 0.0


def test_ordinal_krippendorff_alpha_scale_invariance():
    """Verify ordinal alpha is invariant to uniform shift of category labels."""
    ratings1 = np.array([
        [0, 1, 2, 3, 1, 2],
        [0, 2, 2, 3, 1, 3]
    ], dtype=float)
    ratings2 = ratings1 + 10.0  # Shift {0, 1, 2, 3} to {10, 11, 12, 13}
    
    alpha1 = compute_ordinal_krippendorff_alpha(ratings1)
    alpha2 = compute_ordinal_krippendorff_alpha(ratings2)
    assert math.isclose(alpha1, alpha2, rel_tol=1e-5)


def test_ordinal_krippendorff_alpha_missing_values():
    """Verify missing values (np.nan) are properly handled without corrupting valid pairs."""
    ratings = np.array([
        [0, 1, np.nan, 3, 2],
        [0, np.nan, 2, 3, 2]
    ], dtype=float)
    # Valid pairs at columns 0, 3, 4 are identical [0,0], [3,3], [2,2]
    alpha = compute_ordinal_krippendorff_alpha(ratings)
    assert math.isclose(alpha, 1.0, rel_tol=1e-5)


# ---------------------------------------------------------------------------
# 2. Statistical Core Tests: Quadratic Weighted Cohen's Kappa
# ---------------------------------------------------------------------------

def test_quadratic_weighted_kappa_perfect_agreement():
    """Verify kappa is exactly 1.0 under identical scoring."""
    r1 = [0, 1, 2, 3, 1, 2, 0, 3]
    r2 = [0, 1, 2, 3, 1, 2, 0, 3]
    kappa = compute_quadratic_weighted_kappa(r1, r2, 0, 3)
    assert math.isclose(kappa, 1.0, rel_tol=1e-5)


def test_quadratic_weighted_kappa_adjacent_penalty():
    """Verify adjacent disagreement (e.g. 1 vs 2) receives small quadratic penalty compared to polar."""
    # Near agreement: only adjacent differences
    r1 = [0, 1, 2, 3, 1, 2]
    r_adj = [0, 2, 2, 2, 1, 2]
    kappa_adj = compute_quadratic_weighted_kappa(r1, r_adj, 0, 3)

    # Polar disagreement: 0 vs 3
    r_polar = [3, 1, 2, 0, 1, 2]
    kappa_polar = compute_quadratic_weighted_kappa(r1, r_polar, 0, 3)

    assert kappa_adj > kappa_polar


# ---------------------------------------------------------------------------
# 3. CSV Dataset Loading & Protocol Validation Tests
# ---------------------------------------------------------------------------

@pytest.fixture
def canonical_template_pairs():
    return load_canonical_template_pairs()


@pytest.fixture
def valid_paired_csv(tmp_path, canonical_template_pairs):
    """Generates a temporary valid paired_annotations_pre_adjudication.csv with 283 rows."""
    file_path = tmp_path / "paired_annotations_pre_adjudication.csv"
    fields = [
        "scenario_id", "scheme_id", "scheme_name",
        "e1_score", "e1_rationale",
        "e2_score", "e2_rationale",
        "score_delta", "requires_adjudication"
    ]
    rows = []
    for idx, (sid, scheme_id) in enumerate(canonical_template_pairs):
        score = idx % 4
        rows.append({
            "scenario_id": sid,
            "scheme_id": scheme_id,
            "scheme_name": f"Scheme {scheme_id}",
            "e1_score": score,
            "e1_rationale": "Strong crop alignment.",
            "e2_score": score,
            "e2_rationale": "Direct operational benefit.",
            "score_delta": 0,
            "requires_adjudication": False
        })
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return file_path


def test_load_paired_annotations_clean(valid_paired_csv):
    """Verify clean 283-row paired CSV loads without error."""
    rows = load_paired_annotations_from_csv(valid_paired_csv)
    assert len(rows) == 283
    assert rows[0]["e1_score"] == 0
    assert rows[0]["e2_score"] == 0
    assert rows[0]["score_delta"] == 0


def test_load_paired_annotations_reject_pilot_leak(tmp_path, canonical_template_pairs):
    """Verify pilot scenario S001 is strictly rejected from benchmark agreement."""
    file_path = tmp_path / "bad_pilot.csv"
    fields = [
        "scenario_id", "scheme_id", "scheme_name",
        "e1_score", "e1_rationale", "e2_score", "e2_rationale",
        "score_delta", "requires_adjudication"
    ]
    rows = []
    for idx, (sid, scheme_id) in enumerate(canonical_template_pairs):
        target_sid = "S001" if idx == 0 else sid
        rows.append({
            "scenario_id": target_sid,
            "scheme_id": scheme_id,
            "scheme_name": f"Scheme {scheme_id}",
            "e1_score": 2,
            "e1_rationale": "Rationale",
            "e2_score": 2,
            "e2_rationale": "Rationale",
            "score_delta": 0,
            "requires_adjudication": False
        })
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    with pytest.raises(ValueError, match=r"Pilot scenario S001 detected.*Pilot scenarios S001-S010 must not be included"):
        load_paired_annotations_from_csv(file_path)


def test_load_paired_annotations_reject_invalid_scores(tmp_path, canonical_template_pairs):
    """Verify scores outside {0, 1, 2, 3} are rejected."""
    file_path = tmp_path / "bad_score.csv"
    fields = [
        "scenario_id", "scheme_id", "scheme_name",
        "e1_score", "e1_rationale", "e2_score", "e2_rationale",
        "score_delta", "requires_adjudication"
    ]
    rows = []
    for idx, (sid, scheme_id) in enumerate(canonical_template_pairs):
        e1_sc = 4 if idx == 0 else 2
        rows.append({
            "scenario_id": sid,
            "scheme_id": scheme_id,
            "scheme_name": f"Scheme {scheme_id}",
            "e1_score": e1_sc,
            "e1_rationale": "Rationale",
            "e2_score": 2,
            "e2_rationale": "Rationale",
            "score_delta": 0,
            "requires_adjudication": False
        })
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    with pytest.raises(ValueError, match=r"Scores out of range"):
        load_paired_annotations_from_csv(file_path)


def test_load_paired_annotations_reject_incomplete_row_count(tmp_path, canonical_template_pairs):
    """Verify submission with fewer than 283 rows is rejected."""
    file_path = tmp_path / "incomplete.csv"
    fields = [
        "scenario_id", "scheme_id", "scheme_name",
        "e1_score", "e1_rationale", "e2_score", "e2_rationale",
        "score_delta", "requires_adjudication"
    ]
    rows = []
    for sid, scheme_id in canonical_template_pairs[:-1]:  # 282 rows
        rows.append({
            "scenario_id": sid,
            "scheme_id": scheme_id,
            "scheme_name": f"Scheme {scheme_id}",
            "e1_score": 2,
            "e1_rationale": "Rationale",
            "e2_score": 2,
            "e2_rationale": "Rationale",
            "score_delta": 0,
            "requires_adjudication": False
        })
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    with pytest.raises(ValueError, match=r"Expected exactly 283 paired rows, got 282"):
        load_paired_annotations_from_csv(file_path)


# ---------------------------------------------------------------------------
# 4. End-to-End Evaluation & Report Generation Tests
# ---------------------------------------------------------------------------

def test_evaluate_benchmark_agreement_and_report(valid_paired_csv, tmp_path):
    """Verify evaluation and Markdown report generation on 283 paired rows."""
    rows = load_paired_annotations_from_csv(valid_paired_csv)
    
    # Introduce controlled variations to test metric sensitivity
    # Row 0: adjacent variance (3 vs 2) -> delta=1
    rows[0]["e1_score"] = 3
    rows[0]["e2_score"] = 2
    rows[0]["score_delta"] = 1
    # Row 1: clinical disagreement (3 vs 1) -> delta=2 (requires adjudication)
    rows[1]["e1_score"] = 3
    rows[1]["e2_score"] = 1
    rows[1]["score_delta"] = 2
    rows[1]["requires_adjudication"] = True

    metrics = evaluate_benchmark_agreement(rows)
    assert metrics["total_pairs"] == 283
    assert metrics["scenarios_covered"] == 60
    assert metrics["disagreements_count"] == 1
    assert metrics["quadratic_weighted_kappa"] >= TARGET_KAPPA_QUADRATIC
    assert metrics["ordinal_krippendorff_alpha"] >= TARGET_ORDINAL_ALPHA
    assert metrics["reliability_passed"] is True

    report_path = tmp_path / "test_report.md"
    report_content = generate_markdown_report(metrics, report_path)
    assert report_path.exists()
    assert "# Benchmark v1.0.4 Expert Inter-Rater Reliability Report" in report_content
    assert "Quadratic Weighted Cohen's Kappa" in report_content
    assert "Ordinal Krippendorff's Alpha" in report_content
    assert "| S011 |" in report_content  # Disagreement item in table
