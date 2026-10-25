"""
test_benchmark_consensus_and_baseline.py
----------------------------------------
Regression tests validating the frozen consensus ground truth labels
and deterministic heuristic baseline evaluation for Benchmark v1.0.4.
"""

import csv
import hashlib
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.evaluation.benchmark_candidates import FROZEN_BENCHMARK_SECTION_A_CANDIDATES
from src.evaluation.metrics import evaluate_standalone_ranking_system, FROZEN_BENCHMARK_ZONE_MAP
from src.models.heuristic_baseline import generate_baseline_rankings
CONSENSUS_CSV = REPO_ROOT / "data/annotations/benchmark_v1.0.4/consensus_labels_final.csv"
EXPECTED_SHA256 = "00e8be8c5b72cdb9c86c43da9d38531641c32d0856ddcc55992712eabb3e1081"


def test_frozen_consensus_labels_integrity():
    """Verify consensus_labels_final.csv exists, matches frozen SHA-256, and adheres to schema."""
    assert CONSENSUS_CSV.exists(), "consensus_labels_final.csv does not exist"
    
    with open(CONSENSUS_CSV, "rb") as f:
        file_sha = hashlib.sha256(f.read()).hexdigest()
    assert file_sha == EXPECTED_SHA256, f"SHA-256 mismatch: got {file_sha}, expected {EXPECTED_SHA256}"
    
    with open(CONSENSUS_CSV, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        
    assert len(rows) == 283, f"Expected 283 rows, got {len(rows)}"
    
    by_scenario = {}
    for r in rows:
        sid = r["scenario_id"]
        sch = r["scheme_id"]
        score = int(r["consensus_score"])
        rat = r["consensus_rationale"]
        
        assert score in (0, 1, 2, 3), f"Invalid score {score} for {sid}, {sch}"
        assert len(rat.strip()) > 0, f"Empty rationale for {sid}, {sch}"
        by_scenario.setdefault(sid, {})[sch] = score
        
    for sid, exp_schemes in FROZEN_BENCHMARK_SECTION_A_CANDIDATES.items():
        assert sid in by_scenario, f"Missing scenario {sid}"
        assert set(by_scenario[sid].keys()) == set(exp_schemes), f"Candidate mismatch in {sid}"


def test_heuristic_baseline_evaluation():
    """Verify deterministic baseline produces valid rankings and evaluates cleanly."""
    rankings = generate_baseline_rankings()
    assert len(rankings) == 60
    
    consensus_labels = {}
    with open(CONSENSUS_CSV, "r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            consensus_labels.setdefault(r["scenario_id"], {})[r["scheme_id"]] = int(r["consensus_score"])
            
    res = evaluate_standalone_ranking_system(
        rankings_by_scenario=rankings,
        consensus_labels_by_scenario=consensus_labels,
        scenario_to_zone_map=FROZEN_BENCHMARK_ZONE_MAP,
        allow_top_k=False
    )
    
    assert 0.95 <= res["global_mean_ndcg3"] <= 1.00
    assert 0.60 <= res["global_mean_mrr"] <= 1.00
    assert len(res["zone_mean_ndcg3"]) == 10
    assert len(res["zone_mean_mrr"]) == 10
