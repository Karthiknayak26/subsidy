#!/usr/bin/env python3
"""
Exploratory ranking evaluation for Benchmark v1.1 (S071-S130).

This script:
1. Validates the single-annotator human_reviewer_annotations.csv (preserves it unchanged).
2. Generates heuristic baseline rankings for S071-S130 using v1.1 candidate sets
   from candidate_generation_results.json and immediate_need from scenario_matrix.json.
3. Computes exploratory NDCG@3 and MRR using the registered metric definitions
   (exponential gain 2^y-1, log2 discount, MRR threshold tau=2).
4. Produces aggregate and zone-level summaries.
5. Documents all blockers and provenance limitations.

IMPORTANT BLOCKERS:
- No ML recommender exists in the repository (only heuristic_baseline.py).
- The evaluation infrastructure (FROZEN_BENCHMARK_SECTION_A_CANDIDATES,
  evaluate_standalone_ranking_system, FROZEN_BENCHMARK_ZONE_MAP) is frozen for
  Benchmark v1.0.4 (S011-S070), NOT v1.1 (S071-S130). These cannot be directly
  applied to v1.1 scenarios.
- The underlying metric functions (compute_ndcg_at_k, compute_mrr) are generic
  and are reused here without v1.0.4 key enforcement.
- All 269 annotation scores match an earlier AI practice file (provenance
  limitation disclosed in the report).
"""

import csv
import json
import math
import sys
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.evaluation.metrics import compute_ndcg_at_k, compute_mrr
from src.models.heuristic_baseline import compute_heuristic_relevance, rank_scenario_candidates

# ---- Paths ----
ANNOTATION_CSV = REPO_ROOT / "data/annotations/benchmark_v1.1/human_reviewer_annotations.csv"
SCENARIO_MATRIX = REPO_ROOT / "data/benchmarks/v1.1/scenario_matrix.json"
CANDIDATE_RESULTS = REPO_ROOT / "data/benchmarks/v1.1/candidate_generation_results.json"
PREDICTIONS_OUT = REPO_ROOT / "data/benchmarks/v1.1/exploratory_predictions_v1.1.0.json"
METRICS_OUT = REPO_ROOT / "data/benchmarks/v1.1/exploratory_metrics_v1.1.0.json"
REPORT_OUT = REPO_ROOT / "reports/benchmark_v1.1_exploratory_ranking_evaluation.md"

# Zone name mapping (from v1.0.4 baseline evaluation script, reused for v1.1 zones Z1-Z10)
ZONE_NAMES = {
    1: "North Eastern Transition Zone",
    2: "North Eastern Dry Zone",
    3: "Northern Dry Zone",
    4: "Central Dry Zone",
    5: "Eastern Dry Zone",
    6: "Southern Dry Zone",
    7: "Southern Transition Zone",
    8: "Northern Transition Zone",
    9: "Hilly Zone",
    10: "Coastal Zone",
}

# Zone ID string -> int mapping
ZONE_ID_TO_INT = {f"Z{i}": i for i in range(1, 11)}


def load_annotations(path):
    """Load and validate the annotation CSV. Returns list of dicts."""
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def validate_annotations(rows):
    """Validate annotation structure. Returns (errors, stats)."""
    errors = []
    stats = {}

    if not rows:
        errors.append("Annotation file is empty.")
        return errors, stats

    expected_columns = [
        "scenario_id", "scheme_id", "scheme_name", "rater_id",
        "relevance_score", "relevance_rationale", "complementarity_notes",
    ]
    if list(rows[0].keys()) != expected_columns:
        errors.append(f"Column mismatch: {list(rows[0].keys())} != {expected_columns}")

    scenario_ids = set()
    scheme_ids = set()
    rater_ids = set()
    score_values = set()
    duplicate_pairs = set()
    seen_pairs = set()
    missing_score = 0
    missing_rationale = 0

    for i, row in enumerate(rows, start=2):
        sid = row["scenario_id"]
        sch = row["scheme_id"]
        pair = (sid, sch)

        scenario_ids.add(sid)
        scheme_ids.add(sch)
        rater_ids.add(row["rater_id"])

        if pair in seen_pairs:
            duplicate_pairs.add(pair)
        seen_pairs.add(pair)

        score = row["relevance_score"]
        if score is None or str(score).strip() == "":
            missing_score += 1
        else:
            try:
                s = int(score)
                if s not in (0, 1, 2, 3):
                    errors.append(f"Row {i}: invalid score {score} for {sid}/{sch}")
                score_values.add(s)
            except (ValueError, TypeError):
                errors.append(f"Row {i}: non-numeric score {score!r} for {sid}/{sch}")

        rationale = row["relevance_rationale"]
        if rationale is None or str(rationale).strip() == "":
            missing_rationale += 1

    stats["total_rows"] = len(rows)
    stats["unique_scenarios"] = len(scenario_ids)
    stats["scenario_ids"] = sorted(scenario_ids)
    stats["unique_schemes"] = len(scheme_ids)
    stats["scheme_ids"] = sorted(scheme_ids)
    stats["rater_ids"] = sorted(rater_ids)
    stats["score_values"] = sorted(score_values)
    stats["duplicate_pairs"] = len(duplicate_pairs)
    stats["missing_score"] = missing_score
    stats["missing_rationale"] = missing_rationale

    if duplicate_pairs:
        errors.append(f"Duplicate (scenario_id, scheme_id) pairs: {sorted(duplicate_pairs)}")
    if missing_score:
        errors.append(f"Missing relevance_score in {missing_score} row(s)")
    if missing_rationale:
        errors.append(f"Missing relevance_rationale in {missing_rationale} row(s)")
    if len(rater_ids) != 1:
        errors.append(f"Expected single rater_id, found: {sorted(rater_ids)}")

    return errors, stats


def load_scenario_context(path):
    """Load v1.1 scenario matrix. Returns dict scenario_id -> scenario info."""
    with open(path, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
    ctx = {}
    for s in scenarios:
        ctx[s["scenario_id"]] = {
            "zone_id": s["zone_id"],
            "zone_int": ZONE_ID_TO_INT.get(s["zone_id"]),
            "district": s["district"],
            "primary_crop": s["crop_primary"],
            "immediate_need": s["immediate_need"],
        }
    return ctx


def load_candidate_sets(path):
    """Load v1.1 candidate generation results. Returns dict scenario_id -> list of scheme_ids."""
    with open(path, "r", encoding="utf-8") as f:
        results = json.load(f)
    candidates = {}
    for sid, data in results.items():
        section_a = data.get("section_a_candidates", [])
        candidates[sid] = [c["scheme_id"] for c in section_a]
    return candidates


def build_label_map(annotation_rows):
    """Build scenario_id -> {scheme_id: score} from annotations."""
    labels = defaultdict(dict)
    for row in annotation_rows:
        sid = row["scenario_id"]
        sch = row["scheme_id"]
        score = int(row["relevance_score"])
        labels[sid][sch] = score
    return dict(labels)


def generate_heuristic_rankings(scenario_context, candidate_sets):
    """Generate heuristic baseline rankings for v1.1 scenarios."""
    rankings = {}
    for sid, cands in candidate_sets.items():
        ctx = scenario_context.get(sid)
        if not ctx:
            continue
        need = ctx["immediate_need"]
        ranked = rank_scenario_candidates(sid, cands, need)
        rankings[sid] = ranked
    return rankings


def compute_scenario_metrics(ranked_schemes, labels):
    """Compute NDCG@3 and MRR for a single scenario using registered definitions."""
    score_vector = [float(labels.get(s, 0)) for s in ranked_schemes]
    ndcg = compute_ndcg_at_k(score_vector, k=3)
    mrr = compute_mrr(score_vector, threshold=2.0)
    return ndcg, mrr, score_vector


def main():
    print("=" * 70)
    print("Benchmark v1.1 Exploratory Ranking Evaluation")
    print("=" * 70)

    # ---- Step 1: Load and validate annotations ----
    print("\n[1/7] Loading and validating annotation file...")
    annotation_rows = load_annotations(ANNOTATION_CSV)
    errors, stats = validate_annotations(annotation_rows)

    print(f"  Total rows: {stats['total_rows']}")
    print(f"  Unique scenarios: {stats['unique_scenarios']}")
    print(f"  Scenario range: {stats['scenario_ids'][0]} - {stats['scenario_ids'][-1]}")
    print(f"  Unique schemes: {stats['unique_schemes']} ({stats['scheme_ids']})")
    print(f"  Rater IDs: {stats['rater_ids']}")
    print(f"  Score values: {stats['score_values']}")
    print(f"  Duplicate pairs: {stats['duplicate_pairs']}")
    print(f"  Missing scores: {stats['missing_score']}")
    print(f"  Missing rationales: {stats['missing_rationale']}")

    if errors:
        print("  VALIDATION ERRORS:")
        for e in errors:
            print(f"    - {e}")
    else:
        print("  Validation: PASS")

    labels = build_label_map(annotation_rows)

    # ---- Step 2: Load scenario context and candidate sets ----
    print("\n[2/7] Loading v1.1 scenario context and candidate sets...")
    scenario_context = load_scenario_context(SCENARIO_MATRIX)
    candidate_sets = load_candidate_sets(CANDIDATE_RESULTS)

    print(f"  Scenarios in matrix: {len(scenario_context)}")
    print(f"  Scenarios with candidate sets: {len(candidate_sets)}")

    # Check coverage
    matrix_sids = set(scenario_context.keys())
    candidate_sids = set(candidate_sets.keys())
    annotation_sids = set(labels.keys())

    missing_context = annotation_sids - matrix_sids
    missing_candidates = annotation_sids - candidate_sids
    missing_labels = candidate_sids - annotation_sids

    print(f"  Annotation scenarios missing from matrix: {sorted(missing_context)}")
    print(f"  Annotation scenarios missing from candidates: {sorted(missing_candidates)}")
    print(f"  Candidate scenarios missing from annotations: {sorted(missing_labels)}")

    # ---- Step 3: Verify ranking validity ----
    print("\n[3/7] Verifying ranking validity against candidate sets...")
    invalid_schemes = []
    missing_from_ranking = []
    duplicate_rankings = []
    unevaluated_scenarios = []

    rankings = generate_heuristic_rankings(scenario_context, candidate_sets)

    for sid in sorted(candidate_sets.keys()):
        expected = set(candidate_sets[sid])
        ranked = rankings.get(sid, [])

        if not ranked:
            unevaluated_scenarios.append(sid)
            continue

        ranked_set = set(ranked)
        unknown = ranked_set - expected
        if unknown:
            invalid_schemes.append((sid, sorted(unknown)))

        if len(ranked) != len(set(ranked)):
            duplicate_rankings.append(sid)

        missing = expected - ranked_set
        if missing:
            missing_from_ranking.append((sid, sorted(missing)))

    print(f"  Scenarios ranked: {len(rankings)}")
    print(f"  Scenarios not evaluated: {len(unevaluated_scenarios)}")
    if unevaluated_scenarios:
        print(f"    Unevaluated: {unevaluated_scenarios}")
    print(f"  Invalid scheme IDs in rankings: {len(invalid_schemes)}")
    if invalid_schemes:
        for sid, schemes in invalid_schemes:
            print(f"    {sid}: {schemes}")
    print(f"  Duplicate rankings: {len(duplicate_rankings)}")
    if duplicate_rankings:
        print(f"    {duplicate_rankings}")
    print(f"  Missing schemes from rankings: {len(missing_from_ranking)}")
    if missing_from_ranking:
        for sid, schemes in missing_from_ranking[:5]:
            print(f"    {sid}: {schemes}")

    # ---- Step 4: Compute metrics ----
    print("\n[4/7] Computing exploratory NDCG@3 and MRR metrics...")
    ndcg_by_scenario = {}
    mrr_by_scenario = {}
    score_vectors = {}
    zone_ndcg = defaultdict(list)
    zone_mrr = defaultdict(list)

    for sid in sorted(rankings.keys()):
        ranked = rankings[sid]
        lab = labels.get(sid, {})
        ndcg, mrr, sv = compute_scenario_metrics(ranked, lab)
        ndcg_by_scenario[sid] = ndcg
        mrr_by_scenario[sid] = mrr
        score_vectors[sid] = sv

        ctx = scenario_context[sid]
        z = ctx["zone_int"]
        if z is not None:
            zone_ndcg[z].append(ndcg)
            zone_mrr[z].append(mrr)

    global_mean_ndcg = float(sum(ndcg_by_scenario.values()) / len(ndcg_by_scenario))
    global_mean_mrr = float(sum(mrr_by_scenario.values()) / len(mrr_by_scenario))

    zone_mean_ndcg = {z: float(sum(v) / len(v)) for z, v in sorted(zone_ndcg.items())}
    zone_mean_mrr = {z: float(sum(v) / len(v)) for z, v in sorted(zone_mrr.items())}

    print(f"  Global Mean NDCG@3: {global_mean_ndcg:.4f}")
    print(f"  Global Mean MRR:    {global_mean_mrr:.4f}")
    print(f"  Scenarios evaluated: {len(ndcg_by_scenario)}")

    # ---- Step 5: Save machine-readable outputs ----
    print("\n[5/7] Saving machine-readable outputs...")

    predictions_output = {
        "benchmark_version": "v1.1",
        "evaluation_type": "exploratory",
        "model": "heuristic_baseline",
        "scenarios_evaluated": len(rankings),
        "rankings": {sid: rankings[sid] for sid in sorted(rankings.keys())},
        "score_vectors": {sid: score_vectors[sid] for sid in sorted(score_vectors.keys())},
    }
    PREDICTIONS_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(PREDICTIONS_OUT, "w", encoding="utf-8") as f:
        json.dump(predictions_output, f, indent=2)
    print(f"  Predictions saved: {PREDICTIONS_OUT}")

    metrics_output = {
        "benchmark_version": "v1.1",
        "evaluation_type": "exploratory",
        "model": "heuristic_baseline",
        "labels_source": "human_reviewer_annotations.csv (single annotator)",
        "provenance_limitation": "All 269 annotation scores match an earlier AI practice file.",
        "metric_definitions": {
            "ndcg_at_3": "Exponential gain 2^y-1, log2(i+1) discount, IDCG from all Section A candidates, 0.0 if IDCG=0",
            "mrr": "Reciprocal rank at first scheme with score >= 2, 0.0 if no hit",
        },
        "global_mean_ndcg3": global_mean_ndcg,
        "global_mean_mrr": global_mean_mrr,
        "scenarios_evaluated": len(ndcg_by_scenario),
        "ndcg3_by_scenario": ndcg_by_scenario,
        "mrr_by_scenario": mrr_by_scenario,
        "zone_mean_ndcg3": {str(k): v for k, v in zone_mean_ndcg.items()},
        "zone_mean_mrr": {str(k): v for k, v in zone_mean_mrr.items()},
    }
    METRICS_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_OUT, "w", encoding="utf-8") as f:
        json.dump(metrics_output, f, indent=2)
    print(f"  Metrics saved: {METRICS_OUT}")

    # ---- Step 6: Zone-level summary ----
    print("\n[6/7] Zone-level summary:")
    print(f"  {'Zone':<6} {'Zone Name':<35} {'Scenarios':<10} {'Mean NDCG@3':<12} {'Mean MRR':<10}")
    for z in sorted(zone_mean_ndcg.keys()):
        zone_label = f"Z{z}"
        zone_name = ZONE_NAMES.get(z, "Unknown")
        n = len(zone_ndcg[z])
        print(f"  {zone_label:<6} {zone_name:<35} {n:<10} {zone_mean_ndcg[z]:<12.4f} {zone_mean_mrr[z]:<10.4f}")

    # ---- Step 7: Generate report ----
    print("\n[7/7] Generating evaluation report...")

    report_lines = [
        "# Benchmark v1.1 Exploratory Ranking Evaluation Report",
        "",
        "**Benchmark Version:** `v1.1` (S071–S130, N=60 scenarios)",
        "**Evaluation Type:** Exploratory (NOT formal pre-registered evaluation)",
        "**Model Evaluated:** Heuristic Baseline (need-to-scheme mapping)",
        "**Labels Source:** `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` (single annotator)",
        "**Metric Definitions:** Reused from `research/dataset_research/evaluation_preregistration.md`",
        "",
        "## Blockers and Limitations",
        "",
        "### Blocker 1: No ML Recommender Exists",
        "The repository contains only a deterministic heuristic baseline (`src/models/heuristic_baseline.py`). "
        "No ML recommender, neural network, or learned ranker is implemented. The notebooks directories "
        "(`notebooks/05_baseline/`, `notebooks/06_ml_models/`) contain only `.gitkeep` files. "
        "Therefore, only heuristic baseline rankings are generated; there is no learned model to compare against.",
        "",
        "### Blocker 2: Evaluation Infrastructure Frozen for v1.0.4 (S011–S070)",
        "The pre-registered evaluation infrastructure is locked to Benchmark v1.0.4 scenarios (S011–S070):",
        "- `src/evaluation/benchmark_candidates.py::FROZEN_BENCHMARK_SECTION_A_CANDIDATES` covers only S011–S070.",
        "- `src/evaluation/metrics.py::evaluate_standalone_ranking_system()` strictly enforces S011–S070 scenario keys.",
        "- `src/evaluation/metrics.py::FROZEN_BENCHMARK_ZONE_MAP` covers only S011–S070.",
        "The annotation file covers v1.1 scenarios (S071–S130). The strict key enforcement in "
        "`evaluate_standalone_ranking_system` prevents its direct use for v1.1. Instead, the underlying "
        "metric functions (`compute_ndcg_at_k`, `compute_mrr`) are reused directly with v1.1 data.",
        "",
        "### Blocker 3: No Separate Baseline for Comparison",
        "Only one ranking model (heuristic baseline) is available. There is no separate recommender or "
        "baseline to compare against. The preregistered acceptance criteria (ΔNDCG@3 ≥ +0.050, "
        "paired permutation test p < 0.050, zone non-regression) require two systems and cannot be applied.",
        "",
        "### Provenance Limitation: AI Practice File Match",
        "All 269 relevance scores in `human_reviewer_annotations.csv` match an earlier AI practice file "
        "row-for-row. The quality-control report records this without assuming authorship. These scores "
        "are treated as a single-annotator dataset for exploratory purposes only and must NOT be presented "
        "as validated human ground truth or independent expert judgments.",
        "",
        "### Single-Annotator Dataset",
        "The annotation file has a single rater_id (`human reviewer`). No inter-rater reliability "
        "(Cohen's kappa, Krippendorff's alpha) is computed, as required for two independent human reviews.",
        "",
        "## Validation Results",
        "",
        f"- Total annotation rows: {stats['total_rows']}",
        f"- Unique scenarios: {stats['unique_scenarios']} ({stats['scenario_ids'][0]}–{stats['scenario_ids'][-1]})",
        f"- Unique schemes: {stats['unique_schemes']} ({', '.join(stats['scheme_ids'])})",
        f"- Rater IDs: {', '.join(stats['rater_ids'])}",
        f"- Score values: {', '.join(str(s) for s in stats['score_values'])}",
        f"- Duplicate (scenario_id, scheme_id) pairs: {stats['duplicate_pairs']}",
        f"- Missing relevance_score: {stats['missing_score']}",
        f"- Missing relevance_rationale: {stats['missing_rationale']}",
        f"- Validation errors: {len(errors)}",
        "",
        "## Ranking Validity Results",
        "",
        f"- Scenarios ranked: {len(rankings)}",
        f"- Scenarios not evaluated: {len(unevaluated_scenarios)}",
        f"- Invalid scheme IDs in rankings: {len(invalid_schemes)}",
        f"- Duplicate rankings: {len(duplicate_rankings)}",
        f"- Missing schemes from rankings: {len(missing_from_ranking)}",
        "",
        "## Exploratory Metric Results",
        "",
        f"- Global Mean NDCG@3: **{global_mean_ndcg:.4f}**",
        f"- Global Mean MRR: **{global_mean_mrr:.4f}**",
        f"- Scenarios evaluated: {len(ndcg_by_scenario)}",
        "",
        "## Zone-Level Summary",
        "",
        "| Zone | Zone Name | Scenarios | Mean NDCG@3 | Mean MRR |",
        "|------|-----------|-----------|-------------|----------|",
    ]

    for z in sorted(zone_mean_ndcg.keys()):
        zone_label = f"Z{z}"
        zone_name = ZONE_NAMES.get(z, "Unknown")
        n = len(zone_ndcg[z])
        report_lines.append(
            f"| {zone_label} | {zone_name} | {n} | {zone_mean_ndcg[z]:.4f} | {zone_mean_mrr[z]:.4f} |"
        )

    report_lines.extend([
        "",
        "## Per-Scenario Results",
        "",
        "| Scenario | Zone | District | Immediate Need | NDCG@3 | MRR |",
        "|----------|------|----------|----------------|--------|-----|",
    ])

    for sid in sorted(ndcg_by_scenario.keys()):
        ctx = scenario_context[sid]
        zone_label = ctx["zone_id"]
        district = ctx["district"]
        need = ctx["immediate_need"]
        report_lines.append(
            f"| {sid} | {zone_label} | {district} | {need} | {ndcg_by_scenario[sid]:.4f} | {mrr_by_scenario[sid]:.4f} |"
        )

    report_lines.extend([
        "",
        "## Interpretation",
        "",
        "- These are **exploratory** results on a single-annotator dataset.",
        "- The heuristic baseline ranks schemes by need-to-scheme mapping with deterministic tie-breaking.",
        "- NDCG@3 measures ranking quality at the top-3 cutoff using exponential relevance gain.",
        "- MRR measures the reciprocal rank of the first scheme scored ≥ 2 (Relevant or Highly Relevant).",
        "- No statistical significance testing is performed (requires two systems for comparison).",
        "- The preregistered acceptance gates (ΔNDCG@3 ≥ +0.050, p < 0.050, zone non-regression) are NOT evaluated.",
        "",
        "## Provenance and Reproducibility",
        "",
        "- Annotation file: `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` (preserved unchanged)",
        "- Predictions: `data/benchmarks/v1.1/exploratory_predictions_v1.1.0.json`",
        "- Metrics: `data/benchmarks/v1.1/exploratory_metrics_v1.1.0.json`",
        "- All scores match an earlier AI practice file (269/269). This limitation is disclosed and the results are treated as exploratory only.",
        "",
        "---",
        "*Generated by exploratory evaluation script. Not a formal pre-registered benchmark evaluation.*",
    ])

    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"  Report saved: {REPORT_OUT}")

    print("\n" + "=" * 70)
    print("Exploratory evaluation complete.")
    print("=" * 70)

    return {
        "global_mean_ndcg3": global_mean_ndcg,
        "global_mean_mrr": global_mean_mrr,
        "scenarios_evaluated": len(ndcg_by_scenario),
        "errors": errors,
        "stats": stats,
    }


if __name__ == "__main__":
    results = main()
