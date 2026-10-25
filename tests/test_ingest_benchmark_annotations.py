"""
tests/test_ingest_benchmark_annotations.py
------------------------------------------
Automated test suite verifying the ingestion, validation, and disagreement
extraction pipeline for Benchmark v1.0.4 expert annotations.
"""

import copy
import pytest
from scripts.ingest_benchmark_annotations import (
    load_canonical_template_pairs,
    validate_submission_rows,
    ingest_annotations
)


@pytest.fixture
def canonical_template_pairs():
    return load_canonical_template_pairs()


@pytest.fixture
def valid_submission_rows(canonical_template_pairs):
    rows = []
    for sid, scheme_id in canonical_template_pairs:
        rows.append({
            "scenario_id": sid,
            "scheme_id": scheme_id,
            "scheme_name": f"Scheme {scheme_id}",
            "rater_id": "E1",
            "relevance_score": "2",
            "rationale": "Directly supports seasonal crop production."
        })
    return rows


def test_load_canonical_template_pairs(canonical_template_pairs):
    """Verify exactly 283 template pairs loaded, all within S011-S070."""
    assert len(canonical_template_pairs) == 283
    for sid, _ in canonical_template_pairs:
        assert 11 <= int(sid[1:]) <= 70


def test_validate_clean_submission(valid_submission_rows, canonical_template_pairs):
    """Verify clean valid submission passes validation."""
    clean = validate_submission_rows(valid_submission_rows, "E1", canonical_template_pairs)
    assert len(clean) == 283
    assert clean[0]["relevance_score"] == 2
    assert clean[0]["rater_id"] == "E1"


def test_reject_pilot_scenario_leak(valid_submission_rows, canonical_template_pairs):
    """Verify pilot scenario S001 is strictly rejected if leaked into benchmark."""
    bad_rows = copy.deepcopy(valid_submission_rows)
    bad_rows[0]["scenario_id"] = "S001"
    with pytest.raises(ValueError, match=r"Pilot scenario S001 detected.*S001-S010 must not be in benchmark evaluation"):
        validate_submission_rows(bad_rows, "E1", canonical_template_pairs)


def test_reject_invalid_score_range(valid_submission_rows, canonical_template_pairs):
    """Verify scores outside {0, 1, 2, 3} (e.g. 4 or -1) are rejected."""
    bad_rows = copy.deepcopy(valid_submission_rows)
    bad_rows[0]["relevance_score"] = "4"
    with pytest.raises(ValueError, match=r"Invalid relevance score '4'"):
        validate_submission_rows(bad_rows, "E1", canonical_template_pairs)


def test_reject_missing_rationale(valid_submission_rows, canonical_template_pairs):
    """Verify empty rationale is rejected under Protocol v1.1."""
    bad_rows = copy.deepcopy(valid_submission_rows)
    bad_rows[0]["rationale"] = ""
    with pytest.raises(ValueError, match=r"Missing audit rationale"):
        validate_submission_rows(bad_rows, "E1", canonical_template_pairs)


def test_reject_rater_id_mismatch(valid_submission_rows, canonical_template_pairs):
    """Verify rater ID mismatch is rejected."""
    with pytest.raises(ValueError, match=r"Rater ID mismatch"):
        validate_submission_rows(valid_submission_rows, "E2", canonical_template_pairs)


def test_reject_duplicate_candidate_pair(valid_submission_rows, canonical_template_pairs):
    """Verify duplicate (scenario_id, scheme_id) pairs are rejected."""
    bad_rows = copy.deepcopy(valid_submission_rows)
    bad_rows[1]["scenario_id"] = bad_rows[0]["scenario_id"]
    bad_rows[1]["scheme_id"] = bad_rows[0]["scheme_id"]
    with pytest.raises(ValueError, match=r"Duplicate candidate scheme pair detected"):
        validate_submission_rows(bad_rows, "E1", canonical_template_pairs)


def test_dry_run_writes_no_files(tmp_path, canonical_template_pairs):
    """Verify --dry-run performs validation only and writes zero files to disk."""
    import csv as csv_mod

    # Build minimal valid E1 and E2 CSVs in a temp directory
    fields = ["scenario_id", "scheme_id", "scheme_name", "rater_id", "relevance_score", "rationale"]
    for rater in ("E1", "E2"):
        rows = [
            {
                "scenario_id": sid,
                "scheme_id": scheme_id,
                "scheme_name": f"Scheme {scheme_id}",
                "rater_id": rater,
                "relevance_score": "2",
                "rationale": "Adequate crop alignment and operational fit."
            }
            for sid, scheme_id in canonical_template_pairs
        ]
        out = tmp_path / f"{rater}_submission.csv"
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv_mod.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    archive_dir = tmp_path / "archive"
    output_dir = tmp_path / "output"

    result = ingest_annotations(
        e1_path=tmp_path / "E1_submission.csv",
        e2_path=tmp_path / "E2_submission.csv",
        archive_dir=archive_dir,
        output_dir=output_dir,
        dry_run=True
    )

    assert result["status"] == "DRY_RUN_PASSED"

    # archive_dir and output_dir must not exist (no files written at all)
    assert not archive_dir.exists(), "dry-run must not create the archive directory"
    assert not output_dir.exists() or not any(output_dir.iterdir()), (
        "dry-run must not write output files"
    )

