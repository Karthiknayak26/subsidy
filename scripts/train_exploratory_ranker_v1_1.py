#!/usr/bin/env python3
"""
Train exploratory ML-based scheme ranker for Benchmark v1.1 (S071-S130).

This script:
1. Loads the single-annotator human_reviewer_annotations.csv (preserves it unchanged).
2. Builds candidate-level features by joining scenario context with scheme metadata.
3. Validates no label leakage in features.
4. Trains a scikit-learn HistGradientBoostingRegressor pipeline.
5. Runs out-of-fold evaluation grouped by scenario_id (GroupKFold).
6. Also runs archetype-grouped evaluation for stricter generalization testing.
7. Generates out-of-fold rankings for held-out scenarios.
8. Compares ML model vs heuristic baseline using NDCG@3 and MRR.
9. Produces per-scenario, aggregate, and zone-level metrics.
10. Saves model metadata, OOF predictions, metrics, and report.

IMPORTANT LIMITATIONS:
- Labels come from human_reviewer_annotations.csv (single annotator).
- All 269 annotation scores exactly match an earlier AI practice file
  (documented provenance limitation). Labels are exploratory training targets only.
- Small dataset: 60 scenarios, 269 candidate pairs. Results are exploratory.
- No formal preregistered acceptance gates are evaluated.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

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
    get_heuristic_primary_scheme,
    load_annotations,
    load_candidate_results,
    load_scenario_matrix,
    load_scheme_master,
    run_out_of_fold_evaluation,
    validate_feature_alignment,
    validate_group_leakage,
    validate_no_label_leakage,
)
from src.models.heuristic_baseline import rank_scenario_candidates

# ---- Paths ----
ANNOTATION_CSV = REPO_ROOT / "data/annotations/benchmark_v1.1/human_reviewer_annotations.csv"
SCENARIO_MATRIX = REPO_ROOT / "data/benchmarks/v1.1/scenario_matrix.json"
CANDIDATE_RESULTS = REPO_ROOT / "data/benchmarks/v1.1/candidate_generation_results.json"
SCHEME_MASTER = REPO_ROOT / "scheme_database/processed/scheme_master.json"

ML_EXPERIMENT_DIR = REPO_ROOT / "data/benchmarks/v1.1/ml_experiment"
MODEL_METADATA_PATH = ML_EXPERIMENT_DIR / "model_metadata_v1.1.0.json"
OOF_PREDICTIONS_PATH = ML_EXPERIMENT_DIR / "oof_predictions_v1.1.0.json"
METRICS_OUTPUT_PATH = ML_EXPERIMENT_DIR / "metrics_v1.1.0.json"
REPORT_OUT = REPO_ROOT / "reports/benchmark_v1.1_ml_experiment.md"

# Zone name mapping (reused from v1.0.4 baseline evaluation script)
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

ZONE_ID_TO_INT = {f"Z{i}": i for i in range(1, 11)}


def load_annotation_rows(path):
    """Load annotation CSV rows as list of dicts."""
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def build_label_map(annotation_rows):
    """Build (scenario_id, scheme_id) -> score lookup."""
    label_map = {}
    for row in annotation_rows:
        label_map[(row["scenario_id"], row["scheme_id"])] = int(row["relevance_score"])
    return label_map


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


def compute_scenario_metrics_from_ranking(ranked_schemes, label_map):
    """Compute NDCG@3 and MRR for a single scenario."""
    score_vector = [float(label_map.get((ranked_schemes[0]["scenario_id"] if isinstance(ranked_schemes[0], dict) else ranked_schemes[0], s), 0)) for s in ranked_schemes]
    # Fix: ranked_schemes is a list of scheme_ids, label_map keyed by (sid, sch)
    # We need scenario_id for this ranking
    return None  # placeholder, not used


def compute_metrics_for_scenario(sid, ranked_schemes, label_map):
    """Compute NDCG@3 and MRR for a scenario given ranked scheme_ids and label_map."""
    score_vector = [float(label_map.get((sid, s), 0)) for s in ranked_schemes]
    ndcg = compute_ndcg_at_k(score_vector, k=3)
    mrr = compute_mrr(score_vector, threshold=2.0)
    return ndcg, mrr, score_vector


def main():
    print("=" * 70)
    print("Benchmark v1.1 ML Exploratory Ranker Training")
    print("=" * 70)

    # ---- Step 1: Load data ----
    print("\n[1/9] Loading data sources...")
    scenarios = load_scenario_matrix(SCENARIO_MATRIX)
    candidate_results = load_candidate_results(CANDIDATE_RESULTS)
    schemes = load_scheme_master(SCHEME_MASTER)
    annotation_rows = load_annotation_rows(ANNOTATION_CSV)

    # Build candidate sets: scenario_id -> list of scheme_ids (Section A only)
    candidate_sets = {}
    for sid, data in candidate_results.items():
        section_a = data.get("section_a_candidates", [])
        candidate_sets[sid] = [c["scheme_id"] for c in section_a]

    print(f"  Scenarios: {len(scenarios)}")
    print(f"  Candidate sets: {len(candidate_sets)}")
    print(f"  Schemes in master: {len(schemes)}")
    print(f"  Annotation rows: {len(annotation_rows)}")

    # ---- Step 2: Build features ----
    print("\n[2/9] Building candidate-level features...")
    scheme_lookup = build_scheme_lookup(schemes)
    feature_df = build_feature_rows(scenarios, scheme_lookup, candidate_sets)
    print(f"  Feature rows: {len(feature_df)}")
    print(f"  Feature columns: {list(feature_df.columns)}")

    # ---- Step 3: Validate no label leakage ----
    print("\n[3/9] Validating no label leakage...")
    leakage_errors = validate_no_label_leakage(feature_df)
    alignment_errors = validate_feature_alignment(feature_df, candidate_sets)
    if leakage_errors:
        print("  LEAKAGE ERRORS:")
        for e in leakage_errors:
            print(f"    - {e}")
    else:
        print("  No label leakage detected: PASS")
    if alignment_errors:
        print("  ALIGNMENT ERRORS:")
        for e in alignment_errors:
            print(f"    - {e}")
    else:
        print("  Feature alignment with candidate sets: PASS")

    # ---- Step 4: Build labels ----
    print("\n[4/9] Building relevance score labels...")
    label_map = build_label_map(annotation_rows)
    labels = build_label_vector(feature_df, pd.DataFrame(annotation_rows))
    print(f"  Labels: {len(labels)} rows")
    print(f"  Score distribution: {labels.value_counts().sort_index().to_dict()}")
    print(f"  Missing labels (defaulted to 0): {(labels == 0).sum()}")

    # ---- Step 5: Out-of-fold evaluation grouped by scenario ----
    print("\n[5/9] Running out-of-fold evaluation (GroupKFold by scenario)...")
    oof_result = run_out_of_fold_evaluation(
        feature_df,
        labels,
        n_splits=5,
        random_state=42,
    )
    oof_scores = oof_result["oof_scores"]
    feature_df = feature_df.copy()
    feature_df["oof_predicted_score"] = oof_scores

    # Check for NaN OOF scores (scenarios not covered by any fold test set)
    nan_count = int(np.isnan(oof_scores).sum())
    print(f"  OOF predictions with NaN: {nan_count}")
    if nan_count > 0:
        print("  WARNING: Some rows lack OOF predictions (GroupKFold may not cover all).")

    # ---- Step 6: Build OOF rankings per scenario ----
    print("\n[6/9] Building out-of-fold rankings per scenario...")
    ml_rankings = {}
    for sid in sorted(candidate_sets.keys()):
        subset = feature_df[feature_df["scenario_id"] == sid].copy()
        if subset.empty:
            continue
        # Drop rows with NaN predictions
        valid = subset.dropna(subset=["oof_predicted_score"])
        if valid.empty:
            print(f"  WARNING: No valid OOF predictions for {sid}")
            continue
        ranked = valid.sort_values(
            by=["oof_predicted_score", "scheme_id"],
            ascending=[False, True],
        )
        ml_rankings[sid] = ranked["scheme_id"].tolist()

    print(f"  Scenarios with ML rankings: {len(ml_rankings)}")

    # ---- Step 7: Heuristic baseline rankings ----
    print("\n[7/9] Generating heuristic baseline rankings...")
    scenario_lookup = build_scenario_lookup(scenarios)
    heuristic_rankings = generate_heuristic_rankings(scenario_lookup, candidate_sets)
    print(f"  Scenarios with heuristic rankings: {len(heuristic_rankings)}")

    # ---- Step 8: Compute metrics for both models ----
    print("\n[8/9] Computing NDCG@3 and MRR metrics...")
    ml_ndcg = {}
    ml_mrr = {}
    heur_ndcg = {}
    heur_mrr = {}

    # Build scenario-level label existence check
    label_scenarios = set(sid for sid, _ in label_map.keys())

    for sid in sorted(candidate_sets.keys()):
        if sid in ml_rankings and sid in label_scenarios:
            n, m, _ = compute_metrics_for_scenario(sid, ml_rankings[sid], label_map)
            ml_ndcg[sid] = n
            ml_mrr[sid] = m
        if sid in heuristic_rankings and sid in label_scenarios:
            n, m, _ = compute_metrics_for_scenario(sid, heuristic_rankings[sid], label_map)
            heur_ndcg[sid] = n
            heur_mrr[sid] = m

    ml_global_ndcg = float(np.mean(list(ml_ndcg.values()))) if ml_ndcg else 0.0
    ml_global_mrr = float(np.mean(list(ml_mrr.values()))) if ml_mrr else 0.0
    heur_global_ndcg = float(np.mean(list(heur_ndcg.values()))) if heur_ndcg else 0.0
    heur_global_mrr = float(np.mean(list(heur_mrr.values()))) if heur_mrr else 0.0

    print(f"  ML Global Mean NDCG@3: {ml_global_ndcg:.4f}")
    print(f"  ML Global Mean MRR:    {ml_global_mrr:.4f}")
    print(f"  Heuristic Global Mean NDCG@3: {heur_global_ndcg:.4f}")
    print(f"  Heuristic Global Mean MRR:    {heur_global_mrr:.4f}")
    print(f"  Delta NDCG@3: {ml_global_ndcg - heur_global_ndcg:+.4f}")
    print(f"  Delta MRR:    {ml_global_mrr - heur_global_mrr:+.4f}")

    # Zone-level metrics
    zone_ml_ndcg = defaultdict(list)
    zone_heur_ndcg = defaultdict(list)
    for sid in sorted(candidate_sets.keys()):
        z = ZONE_ID_TO_INT.get(scenario_lookup[sid]["zone_id"])
        if z is None:
            continue
        if sid in ml_ndcg:
            zone_ml_ndcg[z].append(ml_ndcg[sid])
        if sid in heur_ndcg:
            zone_heur_ndcg[z].append(heur_ndcg[sid])

    print("\n  Zone-level comparison:")
    print(f"  {'Zone':<6} {'ML NDCG@3':<12} {'Heur NDCG@3':<14} {'Delta':<10}")
    for z in sorted(zone_ml_ndcg.keys()):
        ml_z = float(np.mean(zone_ml_ndcg[z]))
        heur_z = float(np.mean(zone_heur_ndcg.get(z, [0.0])))
        print(f"  Z{z:<5} {ml_z:<12.4f} {heur_z:<14.4f} {ml_z - heur_z:+.4f}")

    # ---- Step 9: Archetype-grouped evaluation ----
    print("\n[9/9] Archetype-grouped generalization evaluation...")
    from sklearn.model_selection import GroupKFold

    # Group by archetype
    archetype_groups = {}
    for sid in scenario_lookup:
        arch = scenario_lookup[sid].get("archetype_id", "UNKNOWN")
        archetype_groups.setdefault(arch, []).append(sid)

    archetypes = sorted(archetype_groups.keys())
    print(f"  Archetypes: {archetypes}")
    print(f"  Scenarios per archetype: { {a: len(archetype_groups[a]) for a in archetypes} }")

    # Leave-one-archetype-out evaluation
    loao_ml_ndcg = {}
    loao_heur_ndcg = {}
    for arch in archetypes:
        held_out_sids = set(archetype_groups[arch])
        train_sids = set(scenario_lookup.keys()) - held_out_sids

        # Train model on non-held-out scenarios
        train_mask = feature_df["scenario_id"].isin(train_sids)
        train_df = feature_df[train_mask]
        train_labels = labels[train_mask]

        if train_df.empty or len(train_sids) < 2:
            print(f"  Skipping {arch}: insufficient training scenarios")
            continue

        fold_model = BenchmarkV11Ranker(random_state=42)
        fold_model.fit(train_df, train_labels)

        # Predict on held-out scenarios
        arch_ml_ndcg = []
        arch_heur_ndcg = []
        for sid in sorted(held_out_sids):
            subset = feature_df[feature_df["scenario_id"] == sid].copy()
            if subset.empty:
                continue
            subset = subset.copy()
            subset["predicted_score"] = fold_model.predict(subset)
            ranked = subset.sort_values(
                by=["predicted_score", "scheme_id"],
                ascending=[False, True],
            )
            ml_rank = ranked["scheme_id"].tolist()
            heur_rank = heuristic_rankings.get(sid, [])

            if ml_rank:
                n, _, _ = compute_metrics_for_scenario(sid, ml_rank, label_map)
                arch_ml_ndcg.append(n)
            if heur_rank:
                n, _, _ = compute_metrics_for_scenario(sid, heur_rank, label_map)
                arch_heur_ndcg.append(n)

        if arch_ml_ndcg:
            loao_ml_ndcg[arch] = float(np.mean(arch_ml_ndcg))
        if arch_heur_ndcg:
            loao_heur_ndcg[arch] = float(np.mean(arch_heur_ndcg))

    print("  Leave-one-archetype-out NDCG@3:")
    for arch in archetypes:
        ml_v = loao_ml_ndcg.get(arch, float("nan"))
        heur_v = loao_heur_ndcg.get(arch, float("nan"))
        print(f"    {arch}: ML={ml_v:.4f}, Heuristic={heur_v:.4f}, Delta={ml_v - heur_v:+.4f}")

    # ---- Step 10: Save outputs ----
    print("\n[10/9] Saving outputs...")
    ML_EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)

    # Model metadata
    model_metadata = {
        "model_type": "HistGradientBoostingRegressor",
        "pipeline": "ColumnTransformer + StandardScaler + OneHotEncoder + HistGradientBoostingRegressor",
        "random_state": 42,
        "n_scenarios": len(scenarios),
        "n_candidate_pairs": len(feature_df),
        "n_schemes": len(scheme_lookup),
        "feature_columns": [c for c in feature_df.columns if c not in ("scenario_id", "scheme_id", "oof_predicted_score")],
        "label_source": "human_reviewer_annotations.csv (single annotator)",
        "provenance_limitation": "All 269 annotation scores match an earlier AI practice file (269/269). Labels are exploratory training targets only.",
        "cv_strategy": "GroupKFold by scenario_id (n_splits=5) + leave-one-archetype-out",
        "evaluation_type": "exploratory",
    }
    with open(MODEL_METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(model_metadata, f, indent=2)
    print(f"  Model metadata: {MODEL_METADATA_PATH}")

    # OOF predictions
    oof_output = {
        "benchmark_version": "v1.1",
        "model": "BenchmarkV11Ranker",
        "evaluation_type": "exploratory_out_of_fold",
        "n_scenarios": len(ml_rankings),
        "global_mean_ndcg3": ml_global_ndcg,
        "global_mean_mrr": ml_global_mrr,
        "heuristic_global_mean_ndcg3": heur_global_ndcg,
        "heuristic_global_mean_mrr": heur_global_mrr,
        "delta_ndcg3": ml_global_ndcg - heur_global_ndcg,
        "delta_mrr": ml_global_mrr - heur_global_mrr,
        "rankings": {sid: ml_rankings[sid] for sid in sorted(ml_rankings.keys())},
        "oof_scores": {sid: feature_df[feature_df["scenario_id"] == sid]["oof_predicted_score"].tolist() for sid in sorted(ml_rankings.keys())},
        "ml_ndcg_by_scenario": ml_ndcg,
        "ml_mrr_by_scenario": ml_mrr,
        "heuristic_ndcg_by_scenario": heur_ndcg,
        "heuristic_mrr_by_scenario": heur_mrr,
        "zone_mean_ndcg3_ml": {str(z): float(np.mean(v)) for z, v in sorted(zone_ml_ndcg.items())},
        "zone_mean_ndcg3_heuristic": {str(z): float(np.mean(v)) for z, v in sorted(zone_heur_ndcg.items())},
        "leave_one_archetype_out_ml": loao_ml_ndcg,
        "leave_one_archetype_out_heuristic": loao_heur_ndcg,
    }
    with open(OOF_PREDICTIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(oof_output, f, indent=2)
    print(f"  OOF predictions: {OOF_PREDICTIONS_PATH}")

    # Metrics summary
    metrics_output = {
        "benchmark_version": "v1.1",
        "model": "BenchmarkV11Ranker",
        "comparison_model": "heuristic_baseline",
        "global": {
            "ml_mean_ndcg3": ml_global_ndcg,
            "ml_mean_mrr": ml_global_mrr,
            "heuristic_mean_ndcg3": heur_global_ndcg,
            "heuristic_mean_mrr": heur_global_mrr,
            "delta_ndcg3": ml_global_ndcg - heur_global_ndcg,
            "delta_mrr": ml_global_mrr - heur_global_mrr,
        },
        "by_scenario": {
            sid: {
                "ml_ndcg3": ml_ndcg.get(sid),
                "ml_mrr": ml_mrr.get(sid),
                "heuristic_ndcg3": heur_ndcg.get(sid),
                "heuristic_mrr": heur_mrr.get(sid),
            }
            for sid in sorted(candidate_sets.keys())
        },
        "zone_level": {
            "ml": {str(z): float(np.mean(v)) for z, v in sorted(zone_ml_ndcg.items())},
            "heuristic": {str(z): float(np.mean(v)) for z, v in sorted(zone_heur_ndcg.items())},
        },
        "leave_one_archetype_out": {
            "ml": loao_ml_ndcg,
            "heuristic": loao_heur_ndcg,
        },
        "provenance_limitation": "All 269 annotation scores match an earlier AI practice file (269/269). Results are exploratory only.",
    }
    with open(METRICS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_output, f, indent=2)
    print(f"  Metrics: {METRICS_OUTPUT_PATH}")

    # ---- Step 11: Generate report ----
    print("\n[11/9] Generating report...")

    report_lines = [
        "# Benchmark v1.1 ML Exploratory Ranking Experiment",
        "",
        "**Benchmark Version:** `v1.1` (S071–S130, N=60 scenarios)",
        "**Experiment Type:** Exploratory ML ranking (NOT formal pre-registered evaluation)",
        "**Model:** BenchmarkV11Ranker (HistGradientBoostingRegressor pipeline)",
        "**Baseline:** Heuristic baseline (need-to-scheme mapping)",
        "**Labels Source:** `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` (single annotator)",
        "",
        "## Important Limitations",
        "",
        "### Provenance Limitation",
        "All 269 relevance scores in the annotation file match an earlier AI practice file "
        "row-for-row (269/269 identical scores). The quality-control report records this "
        "without assuming authorship. These labels are treated as exploratory training "
        "targets only and MUST NOT be described as verified independent human gold labels. "
        "Any model trained on these labels inherits this provenance limitation.",
        "",
        "### Single-Annotator Dataset",
        "The annotation file has a single rater_id (`human reviewer`). No inter-rater "
        "reliability (Cohen's kappa, Krippendorff's alpha) is available or computed.",
        "",
        "### Small Dataset",
        "Only 60 scenarios and 269 candidate pairs are available. This is too small for "
        "robust ML generalization estimates. Results should be treated as a prototype, "
        "not evidence of production readiness.",
        "",
        "### No Formal Acceptance Gates Evaluated",
        "The preregistered acceptance criteria (ΔNDCG@3 ≥ +0.050, paired permutation "
        "test p < 0.050, zone-level non-regression) are NOT evaluated here. Those gates "
        "require two independent systems and resolved annotation provenance.",
        "",
        "## Feature Engineering",
        "",
        "Features are derived from scenario context (`scenario_matrix.json`) and scheme "
        "metadata (`scheme_master.json`) only. No label information (relevance scores, "
        "rationales, complementarity notes) is used as input. The heuristic score itself "
        "is NOT included as a feature to prevent leakage.",
        "",
        "### Scenario Features",
        f"- Numeric: {', '.join(['land_size_acres', 'annual_family_income_lakh', 'secondary_constraint_count'])}",
        f"- Categorical: {', '.join(['zone_id', 'district', 'crop_primary', 'crop_secondary', 'land_type', 'social_category', 'farmer_category', 'operational_water_source', 'borewell_electric_status', 'immediate_need', 'archetype_id'])}",
        f"- Boolean: {', '.join(['is_pure_tenant_without_land_title', 'land_ownership_cutoff_pre_feb_2019', 'paid_income_tax_last_assessment_year', 'pensioner_is_mts_exempt', 'registered_professional_is_none'])}",
        "",
        "### Scheme Features",
        f"- Numeric: {', '.join(['min_land_acres', 'max_land_acres'])}",
        f"- Categorical: {', '.join(['scheme_id', 'government_level', 'benefit_type', 'target_crops', 'irrigation_requirements', 'record_type', 'parent_scheme_id'])}",
        "",
        "### Interaction Features",
        "- land_size_within_scheme_range",
        "- water_source_compatible",
        "- immediate_need_matches_heuristic_primary",
        "",
        "## Cross-Validation Strategy",
        "",
        "- Primary: GroupKFold (n_splits=5) grouped by scenario_id. All candidates from "
          "one scenario stay in the same fold to prevent leakage.",
        "- Secondary: Leave-one-archetype-out (6 archetypes, 10 scenarios each). Stricter "
          "test of generalization across farmer need profiles.",
        "",
        "## Results",
        "",
        f"### Global Metrics",
        f"- ML Model Mean NDCG@3: **{ml_global_ndcg:.4f}**",
        f"- ML Model Mean MRR: **{ml_global_mrr:.4f}**",
        f"- Heuristic Baseline Mean NDCG@3: **{heur_global_ndcg:.4f}**",
        f"- Heuristic Baseline Mean MRR: **{heur_global_mrr:.4f}**",
        f"- Delta NDCG@3 (ML - Heuristic): **{ml_global_ndcg - heur_global_ndcg:+.4f}**",
        f"- Delta MRR (ML - Heuristic): **{ml_global_mrr - heur_global_mrr:+.4f}**",
        "",
        "### Zone-Level Summary",
        "",
        "| Zone | Zone Name | Scenarios | ML NDCG@3 | Heuristic NDCG@3 | Delta |",
        "|------|-----------|-----------|-----------|------------------|-------|",
    ]

    for z in sorted(zone_ml_ndcg.keys()):
        zone_label = f"Z{z}"
        zone_name = ZONE_NAMES.get(z, "Unknown")
        n_ml = len(zone_ml_ndcg[z])
        ml_v = float(np.mean(zone_ml_ndcg[z]))
        heur_v = float(np.mean(zone_heur_ndcg.get(z, [0.0])))
        report_lines.append(
            f"| {zone_label} | {zone_name} | {n_ml} | {ml_v:.4f} | {heur_v:.4f} | {ml_v - heur_v:+.4f} |"
        )

    report_lines.extend([
        "",
        "### Leave-One-Archetype-Out NDCG@3",
        "",
        "| Archetype | ML NDCG@3 | Heuristic NDCG@3 | Delta |",
        "|-----------|-----------|------------------|-------|",
    ])

    for arch in archetypes:
        ml_v = loao_ml_ndcg.get(arch, float("nan"))
        heur_v = loao_heur_ndcg.get(arch, float("nan"))
        report_lines.append(
            f"| {arch} | {ml_v:.4f} | {heur_v:.4f} | {ml_v - heur_v:+.4f} |"
        )

    report_lines.extend([
        "",
        "### Per-Scenario Results",
        "",
        "| Scenario | Zone | District | ML NDCG@3 | Heuristic NDCG@3 | Delta |",
        "|----------|------|----------|-----------|------------------|-------|",
    ])

    for sid in sorted(candidate_sets.keys()):
        ctx = scenario_lookup[sid]
        zone_label = ctx["zone_id"]
        district = ctx["district"]
        ml_v = ml_ndcg.get(sid, float("nan"))
        heur_v = heur_ndcg.get(sid, float("nan"))
        report_lines.append(
            f"| {sid} | {zone_label} | {district} | {ml_v:.4f} | {heur_v:.4f} | {ml_v - heur_v:+.4f} |"
        )

    report_lines.extend([
        "",
        "## Interpretation",
        "",
        "- These are **exploratory** results on single-annotator labels with a documented "
          "provenance limitation.",
        "- The ML model uses GroupKFold out-of-fold predictions, so each scenario is ranked "
          "by a model that did not train on that scenario's candidates.",
        "- No statistical significance testing is performed (requires proper train/test "
          "separation and more data).",
        "- The heuristic baseline is a deterministic need-to-scheme mapping with no learning.",
        "- Delta NDCG@3 close to 0 suggests the ML model does not clearly outperform the "
          "heuristic on this small exploratory dataset.",
        "",
        "## Outputs",
        "",
        f"- Model metadata: `{MODEL_METADATA_PATH}`",
        f"- OOF predictions: `{OOF_PREDICTIONS_PATH}`",
        f"- Metrics: `{METRICS_OUTPUT_PATH}`",
        f"- Report: `{REPORT_OUT}`",
        "",
        "## Reproducibility",
        "",
        "- Random seed: 42",
        "- scikit-learn version: 1.8.0",
        "- All data loaded from repository sources (no external downloads)",
        "",
        "---",
        "*Generated by train_exploratory_ranker_v1_1.py. Exploratory only — not a formal pre-registered evaluation.*",
    ])

    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"  Report: {REPORT_OUT}")

    print("\n" + "=" * 70)
    print("ML exploratory training complete.")
    print("=" * 70)

    return {
        "ml_global_ndcg3": ml_global_ndcg,
        "ml_global_mrr": ml_global_mrr,
        "heuristic_global_ndcg3": heur_global_ndcg,
        "heuristic_global_mrr": heur_global_mrr,
        "delta_ndcg3": ml_global_ndcg - heur_global_ndcg,
        "delta_mrr": ml_global_mrr - heur_global_mrr,
    }


if __name__ == "__main__":
    results = main()
