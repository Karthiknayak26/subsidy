#!/usr/bin/env python3
"""
Controlled feature-ablation experiment for Benchmark v1.1 ML ranker (v1.1.1).

This script evaluates five feature configurations to diagnose the poor
leave-one-archetype-out result for ARCH_3:

  A. Full existing feature set (30 features) — reference result from v1.1.0
  B. Exclude immediate_need_matches_heuristic_primary (29 features)
  C. Exclude archetype_id (29 features)
  D. Exclude immediate_need (29 features) — interaction feature retained
  E. Combined ablation excluding all three suspect groups (27 features)

Protocol:
- Same scenario-grouped CV folds (GroupKFold, n_splits=5) across all configs
- Same leave-one-archetype-out partitions (6 archetypes)
- Preprocessing/encoding/model fit independently inside each training fold
- No hyperparameter tuning against held-out data
- Same NDCG@3 and MRR definitions, same candidate-set validity checks
- Same heuristic baseline for all comparisons
- v1.1.0 outputs preserved unchanged; ablation outputs in ablation_v1.1.1/

IMPORTANT LIMITATIONS:
- Labels from human_reviewer_annotations.csv (single annotator)
- All 269 annotation scores match an earlier AI practice file (269/269)
- Six archetypes only; ablation findings are exploratory, not definitive
- Model-selection bias acknowledged: choosing a feature set based on these
  results would overfit to this diagnostic comparison
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
from sklearn.model_selection import GroupKFold

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
)
from src.models.heuristic_baseline import rank_scenario_candidates

# ---- Paths (v1.1.1 ablation, separate from v1.1.0) ----
ANNOTATION_CSV = REPO_ROOT / "data/annotations/benchmark_v1.1/human_reviewer_annotations.csv"
SCENARIO_MATRIX = REPO_ROOT / "data/benchmarks/v1.1/scenario_matrix.json"
CANDIDATE_RESULTS = REPO_ROOT / "data/benchmarks/v1.1/candidate_generation_results.json"
SCHEME_MASTER = REPO_ROOT / "scheme_database/processed/scheme_master.json"

ABLATION_DIR = REPO_ROOT / "data/benchmarks/v1.1/ml_experiment/ablation_v1.1.1"
ABLATION_METADATA_PATH = ABLATION_DIR / "ablation_metadata_v1.1.1.json"
ABLATION_RESULTS_PATH = ABLATION_DIR / "ablation_results_v1.1.1.json"
REPORT_OUT = REPO_ROOT / "reports/benchmark_v1.1_feature_ablation.md"

# Zone name mapping
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

RANDOM_STATE = 42
N_SPLITS = 5

# ---- Ablation configurations ----
# Each config specifies which feature column names to exclude.
# Column names must match those produced by build_feature_rows().
ABLATION_CONFIGS = {
    "A": {
        "name": "full_feature_set",
        "description": "All 30 features (reference, same as v1.1.0)",
        "exclude": [],
    },
    "B": {
        "name": "no_heuristic_match",
        "description": "Exclude immediate_need_matches_heuristic_primary (29 features)",
        "exclude": ["immediate_need_matches_heuristic_primary"],
    },
    "C": {
        "name": "no_archetype_id",
        "description": "Exclude archetype_id (29 features)",
        "exclude": ["archetype_id"],
    },
    "D": {
        "name": "no_immediate_need",
        "description": "Exclude immediate_need (29 features). "
        "Interaction feature immediate_need_matches_heuristic_primary retained "
        "because it is computed independently from scenario data.",
        "exclude": ["immediate_need"],
    },
    "E": {
        "name": "combined_ablation",
        "description": "Exclude immediate_need_matches_heuristic_primary, "
        "archetype_id, and immediate_need (27 features)",
        "exclude": [
            "immediate_need_matches_heuristic_primary",
            "archetype_id",
            "immediate_need",
        ],
    },
}


def load_annotation_rows(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def build_label_map(annotation_rows):
    label_map = {}
    for row in annotation_rows:
        label_map[(row["scenario_id"], row["scheme_id"])] = int(row["relevance_score"])
    return label_map


def generate_heuristic_rankings(scenario_context, candidate_sets):
    rankings = {}
    for sid, cands in candidate_sets.items():
        ctx = scenario_context.get(sid)
        if not ctx:
            continue
        ranked = rank_scenario_candidates(sid, cands, ctx["immediate_need"])
        rankings[sid] = ranked
    return rankings


def compute_metrics_for_scenario(sid, ranked_schemes, label_map):
    score_vector = [float(label_map.get((sid, s), 0)) for s in ranked_schemes]
    ndcg = compute_ndcg_at_k(score_vector, k=3)
    mrr = compute_mrr(score_vector, threshold=2.0)
    return ndcg, mrr, score_vector


def run_oof_evaluation_for_config(feature_df, labels, n_splits=N_SPLITS,
                                  random_state=RANDOM_STATE):
    """Run GroupKFold OOF evaluation. Returns per-scenario rankings and scores."""
    scenario_ids = feature_df["scenario_id"].unique()
    group_map = {sid: i for i, sid in enumerate(sorted(scenario_ids))}
    groups = feature_df["scenario_id"].map(group_map).values

    gkf = GroupKFold(n_splits=n_splits)

    oof_scores = np.full(len(feature_df), np.nan)
    oof_indices_map = defaultdict(list)

    for fold_idx, (train_idx, test_idx) in enumerate(gkf.split(feature_df, labels, groups=groups)):
        train_df = feature_df.iloc[train_idx]
        train_labels = labels.iloc[train_idx]
        test_df = feature_df.iloc[test_idx]

        fold_model = BenchmarkV11Ranker(random_state=random_state)
        fold_model.fit(train_df, train_labels)

        test_subset = test_df.copy()
        test_subset.loc[:, "predicted_score"] = fold_model.predict(test_subset)

        for sid in test_subset["scenario_id"].unique():
            sid_rows = test_subset[test_subset["scenario_id"] == sid]
            oof_scores[sid_rows.index.values] = sid_rows["predicted_score"].values
            oof_indices_map[sid].extend(sid_rows.index.values)

    # Build rankings per scenario from OOF scores
    rankings = {}
    for sid in sorted(feature_df["scenario_id"].unique()):
        subset = feature_df.loc[oof_indices_map[sid]].copy()
        if subset.empty:
            continue
        subset = subset.copy()
        subset["predicted_score"] = oof_scores[subset.index.values]
        ranked = subset.sort_values(
            by=["predicted_score", "scheme_id"],
            ascending=[False, True],
        )
        rankings[sid] = ranked["scheme_id"].tolist()

    return rankings


def run_loao_for_config(feature_df, labels, scenario_lookup, candidate_sets,
                        heuristic_rankings, label_map, random_state=RANDOM_STATE):
    """Leave-one-archetype-out evaluation. Returns per-archetype metrics."""
    archetype_groups = defaultdict(list)
    for sid in scenario_lookup:
        arch = scenario_lookup[sid].get("archetype_id", "UNKNOWN")
        archetype_groups[arch].append(sid)

    archetypes = sorted(archetype_groups.keys())
    loao_ml = {}
    loao_heur = {}

    for arch in archetypes:
        held_out_sids = set(archetype_groups[arch])
        train_sids = set(scenario_lookup.keys()) - held_out_sids

        train_mask = feature_df["scenario_id"].isin(train_sids)
        train_df = feature_df[train_mask]
        train_labels = labels[train_mask]

        if train_df.empty or len(train_sids) < 2:
            continue

        fold_model = BenchmarkV11Ranker(random_state=random_state)
        fold_model.fit(train_df, train_labels)

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
                n, _, _ = compute_scenario_metrics(sid, ml_rank, label_map)
                arch_ml_ndcg.append(n)
            if heur_rank:
                n, _, _ = compute_scenario_metrics(sid, heur_rank, label_map)
                arch_heur_ndcg.append(n)

        if arch_ml_ndcg:
            loao_ml[arch] = float(np.mean(arch_ml_ndcg))
        if arch_heur_ndcg:
            loao_heur[arch] = float(np.mean(arch_heur_ndcg))

    return archetypes, loao_ml, loao_heur


def validate_rankings(rankings, candidate_sets):
    """Verify all rankings use valid candidate sets."""
    errors = []
    for sid, ranking in rankings.items():
        expected = set(candidate_sets.get(sid, []))
        actual = set(ranking)
        if expected != actual:
            errors.append(f"{sid}: candidate set mismatch")
        if len(ranking) != len(set(ranking)):
            errors.append(f"{sid}: duplicate schemes in ranking")
    return errors


def main():
    print("=" * 70)
    print("Benchmark v1.1 Feature-Ablation Experiment (v1.1.1)")
    print("=" * 70)

    # ---- Step 1: Load data ----
    print("\n[1/6] Loading data sources...")
    scenarios = load_scenario_matrix(SCENARIO_MATRIX)
    candidate_results = load_candidate_results(CANDIDATE_RESULTS)
    schemes = load_scheme_master(SCHEME_MASTER)
    annotation_rows = load_annotation_rows(ANNOTATION_CSV)

    candidate_sets = {}
    for sid, data in candidate_results.items():
        section_a = data.get("section_a_candidates", [])
        candidate_sets[sid] = [c["scheme_id"] for c in section_a]

    print(f"  Scenarios: {len(scenarios)}")
    print(f"  Candidate sets: {len(candidate_sets)}")
    print(f"  Schemes in master: {len(schemes)}")
    print(f"  Annotation rows: {len(annotation_rows)}")

    # ---- Step 2: Build full feature matrix ----
    print("\n[2/6] Building full feature matrix (30 features)...")
    scheme_lookup = build_scheme_lookup(schemes)
    full_feature_df = build_feature_rows(scenarios, scheme_lookup, candidate_sets)
    print(f"  Feature rows: {len(full_feature_df)}")
    print(f"  Full feature columns: {len(full_feature_df.columns) - 2} "
          f"(excluding scenario_id, scheme_id)")
    feature_cols = [c for c in full_feature_df.columns
                    if c not in ("scenario_id", "scheme_id")]
    print(f"  Columns: {feature_cols}")

    # ---- Step 3: Build labels ----
    print("\n[3/6] Building relevance score labels...")
    label_map = build_label_map(annotation_rows)
    labels = build_label_vector(full_feature_df, pd.DataFrame(annotation_rows))
    label_scenarios = set(sid for sid, _ in label_map.keys())
    print(f"  Labels: {len(labels)} rows")
    print(f"  Score distribution: {labels.value_counts().sort_index().to_dict()}")

    # ---- Step 4: Heuristic baseline ----
    print("\n[4/6] Generating heuristic baseline rankings...")
    scenario_lookup = build_scenario_lookup(scenarios)
    heuristic_rankings = generate_heuristic_rankings(scenario_lookup, candidate_sets)
    print(f"  Heuristic rankings: {len(heuristic_rankings)} scenarios")

    heur_ndcg = {}
    heur_mrr = {}
    for sid in sorted(candidate_sets.keys()):
        if sid in heuristic_rankings and sid in label_scenarios:
            n, m, _ = compute_metrics_for_scenario(sid, heuristic_rankings[sid], label_map)
            heur_ndcg[sid] = n
            heur_mrr[sid] = m
    heur_global_ndcg = float(np.mean(list(heur_ndcg.values()))) if heur_ndcg else 0.0
    heur_global_mrr = float(np.mean(list(heur_mrr.values()))) if heur_mrr else 0.0
    print(f"  Heuristic Mean NDCG@3: {heur_global_ndcg:.4f}")
    print(f"  Heuristic Mean MRR:    {heur_global_mrr:.4f}")

    # ---- Step 5: Run ablation configurations ----
    print("\n[5/6] Running ablation configurations...")
    all_results = {}

    for config_id in sorted(ABLATION_CONFIGS.keys()):
        config = ABLATION_CONFIGS[config_id]
        exclude = set(config["exclude"])
        print(f"\n  Config {config_id}: {config['name']}")
        print(f"    {config['description']}")
        print(f"    Excluding: {exclude if exclude else '(none)'}")

        # Build reduced feature dataframe
        reduced_df = full_feature_df.drop(columns=list(exclude), errors="ignore")
        n_features = len([c for c in reduced_df.columns
                          if c not in ("scenario_id", "scheme_id")])
        print(f"    Feature count: {n_features}")

        # Validate no label leakage
        from src.models.benchmark_v1_1.ranker import validate_no_label_leakage
        leakage_errors = validate_no_label_leakage(reduced_df)
        if leakage_errors:
            print(f"    LEAKAGE ERRORS: {leakage_errors}")
        else:
            print(f"    No label leakage: PASS")

        # OOF evaluation
        ml_rankings = run_oof_evaluation_for_config(reduced_df, labels)
        print(f"    Scenarios with ML rankings: {len(ml_rankings)}")

        # Validate rankings
        ranking_errors = validate_rankings(ml_rankings, candidate_sets)
        if ranking_errors:
            print(f"    RANKING ERRORS: {ranking_errors[:5]}")
        else:
            print(f"    Candidate-set validity: PASS")

        # Compute metrics
        ml_ndcg = {}
        ml_mrr = {}
        for sid in sorted(candidate_sets.keys()):
            if sid in ml_rankings and sid in label_scenarios:
                n, m, _ = compute_metrics_for_scenario(sid, ml_rankings[sid], label_map)
                ml_ndcg[sid] = n
                ml_mrr[sid] = m

        ml_global_ndcg = float(np.mean(list(ml_ndcg.values()))) if ml_ndcg else 0.0
        ml_global_mrr = float(np.mean(list(ml_mrr.values()))) if ml_mrr else 0.0

        print(f"    ML Mean NDCG@3: {ml_global_ndcg:.4f}")
        print(f"    ML Mean MRR:    {ml_global_mrr:.4f}")
        print(f"    Delta NDCG@3 vs heuristic: {ml_global_ndcg - heur_global_ndcg:+.4f}")

        # LOAO
        archetypes, loao_ml, loao_heur = run_loao_for_config(
            reduced_df, labels, scenario_lookup, candidate_sets,
            heuristic_rankings, label_map,
        )
        loao_ml_mean = float(np.mean(list(loao_ml.values()))) if loao_ml else 0.0
        loao_heur_mean = float(np.mean(list(loao_heur.values()))) if loao_heur else 0.0
        print(f"    LOAO ML mean NDCG@3: {loao_ml_mean:.4f}")
        print(f"    LOAO Heuristic mean NDCG@3: {loao_heur_mean:.4f}")
        print(f"    LOAO Delta: {loao_ml_mean - loao_heur_mean:+.4f}")
        for arch in sorted(loao_ml.keys()):
            print(f"      {arch}: ML={loao_ml[arch]:.4f}, Heur={loao_heur[arch]:.4f}, "
                  f"Delta={loao_ml[arch] - loao_heur[arch]:+.4f}")

        all_results[config_id] = {
            "name": config["name"],
            "description": config["description"],
            "exclude": sorted(exclude),
            "n_features": n_features,
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
            "loao": {
                "archetypes": archetypes,
                "ml": loao_ml,
                "heuristic": loao_heur,
                "ml_mean": loao_ml_mean,
                "heuristic_mean": loao_heur_mean,
                "delta": loao_ml_mean - loao_heur_mean,
            },
            "rankings_valid": len(ranking_errors) == 0,
            "leakage_free": len(leakage_errors) == 0,
        }

    # ---- Step 6: Save outputs ----
    print("\n[6/6] Saving ablation outputs...")
    ABLATION_DIR.mkdir(parents=True, exist_ok=True)

    ablation_metadata = {
        "experiment_version": "v1.1.1",
        "experiment_type": "feature_ablation",
        "reference_version": "v1.1.0",
        "random_state": RANDOM_STATE,
        "n_splits": N_SPLITS,
        "n_scenarios": len(scenarios),
        "n_candidate_pairs": len(full_feature_df),
        "n_schemes": len(scheme_lookup),
        "label_source": "human_reviewer_annotations.csv (single annotator)",
        "provenance_limitation": "All 269 annotation scores match an earlier AI practice file "
                                 "(269/269). Labels are exploratory training targets only.",
        "configurations": {
            cid: {
                "name": ABLATION_CONFIGS[cid]["name"],
                "description": ABLATION_CONFIGS[cid]["description"],
                "exclude": ABLATION_CONFIGS[cid]["exclude"],
            }
            for cid in sorted(ABLATION_CONFIGS.keys())
        },
        "cv_strategy": "GroupKFold by scenario_id (n_splits=5) + leave-one-archetype-out",
        "evaluation_type": "exploratory_feature_ablation",
    }
    with open(ABLATION_METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(ablation_metadata, f, indent=2)
    print(f"  Metadata: {ABLATION_METADATA_PATH}")

    ablation_output = {
        "benchmark_version": "v1.1",
        "experiment_version": "v1.1.1",
        "experiment_type": "exploratory_feature_ablation",
        "random_state": RANDOM_STATE,
        "n_splits": N_SPLITS,
        "provenance_limitation": "All 269 annotation scores match an earlier AI practice file "
                                 "(269/269). Results are exploratory only.",
        "configurations": all_results,
    }
    with open(ABLATION_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(ablation_output, f, indent=2)
    print(f"  Results: {ABLATION_RESULTS_PATH}")

    # ---- Step 7: Generate report ----
    print("\n[7/7] Generating ablation report...")
    report_lines = [
        "# Benchmark v1.1 Feature-Ablation Experiment (v1.1.1)",
        "",
        "**Benchmark Version:** `v1.1` (S071–S130, N=60 scenarios)",
        "**Experiment Type:** Exploratory feature-ablation (NOT formal pre-registered evaluation)",
        "**Model:** BenchmarkV11Ranker (HistGradientBoostingRegressor pipeline)",
        "**Baseline:** Heuristic baseline (need-to-scheme mapping)",
        "**Labels Source:** `data/annotations/benchmark_v1.1/human_reviewer_annotations.csv` "
        "(single annotator)",
        "**Reference:** v1.1.0 full experiment preserved unchanged",
        "",
        "## Important Limitations",
        "",
        "### Provenance Limitation",
        "All 269 relevance scores in the annotation file match an earlier AI practice file "
        "row-for-row (269/269 identical scores). These labels are treated as exploratory "
        "training targets only and MUST NOT be described as verified independent human gold "
        "labels. Any model trained on these labels inherits this provenance limitation.",
        "",
        "### Single-Annotator Dataset",
        "The annotation file has a single rater_id (`human reviewer`). No inter-rater "
        "reliability is computed.",
        "",
        "### Small Dataset",
        "Only 60 scenarios and 269 candidate pairs. Six archetypes with 10 scenarios each. "
        "Results are exploratory and should not be treated as definitive.",
        "",
        "### Model-Selection Bias",
        "The six archetypes are also used for diagnostic comparisons. Choosing a feature set "
        "based on these ablation results would constitute model-selection bias and overfit "
        "to this diagnostic comparison.",
        "",
        "### No Formal Acceptance Gates",
        "The preregistered acceptance criteria (ΔNDCG@3 ≥ +0.050, paired permutation test "
        "p < 0.050, zone-level non-regression) are NOT evaluated here.",
        "",
        "## Ablation Configurations",
        "",
        "| Config | Name | Features | Excluded Columns |",
        "|--------|------|----------|------------------|",
    ]

    for cid in sorted(ABLATION_CONFIGS.keys()):
        cfg = ABLATION_CONFIGS[cid]
        exclude_str = ", ".join(cfg["exclude"]) if cfg["exclude"] else "(none)"
        n_feat = 30 - len(cfg["exclude"])
        report_lines.append(
            f"| {cid} | {cfg['name']} | {n_feat} | {exclude_str} |"
        )

    report_lines.extend([
        "",
        "## Global Results (Out-of-Fold, GroupKFold by scenario)",
        "",
        "| Config | ML NDCG@3 | ML MRR | Heuristic NDCG@3 | Heuristic MRR | Δ NDCG@3 | Δ MRR |",
        "|--------|-----------|--------|------------------|---------------|----------|-------|",
    ])

    for cid in sorted(all_results.keys()):
        r = all_results[cid]["global"]
        report_lines.append(
            f"| {cid} | {r['ml_mean_ndcg3']:.4f} | {r['ml_mean_mrr']:.4f} | "
            f"{r['heuristic_mean_ndcg3']:.4f} | {r['heuristic_mean_mrr']:.4f} | "
            f"{r['delta_ndcg3']:+.4f} | {r['delta_mrr']:+.4f} |"
        )

    report_lines.extend([
        "",
        "## Leave-One-Archetype-Out Results (NDCG@3)",
        "",
        "| Config | ARCH_1 | ARCH_2 | ARCH_3 | ARCH_4 | ARCH_5 | ARCH_6 | Mean ML | Mean Heuristic | Δ |",
        "|--------|--------|--------|--------|--------|--------|--------|---------|----------------|---|",
    ])

    for cid in sorted(all_results.keys()):
        r = all_results[cid]["loao"]
        ml_vals = [r["ml"].get(a, float("nan")) for a in sorted(r["archetypes"])]
        heur_vals = [r["heuristic"].get(a, float("nan")) for a in sorted(r["archetypes"])]
        ml_mean = r["ml_mean"]
        heur_mean = r["heuristic_mean"]
        delta = r["delta"]
        vals_str = " | ".join(f"{v:.4f}" if not math.isnan(v) else "n/a" for v in ml_vals)
        report_lines.append(
            f"| {cid} | {vals_str} | {ml_mean:.4f} | {heur_mean:.4f} | {delta:+.4f} |"
        )

    report_lines.extend([
        "",
        "## ARCH_3 Detail (the regression case)",
        "",
        "| Config | ML NDCG@3 | Heuristic NDCG@3 | Δ |",
        "|--------|-----------|------------------|---|",
    ])

    for cid in sorted(all_results.keys()):
        r = all_results[cid]["loao"]
        ml_v = r["ml"].get("ARCH_3", float("nan"))
        heur_v = r["heuristic"].get("ARCH_3", float("nan"))
        report_lines.append(
            f"| {cid} | {ml_v:.4f} | {heur_v:.4f} | {ml_v - heur_v:+.4f} |"
        )

    report_lines.extend([
        "",
        "## Feature-Level Diagnosis",
        "",
        "### Config A (Full, 30 features) — Reference",
        f"- Global ML NDCG@3: {all_results['A']['global']['ml_mean_ndcg3']:.4f}",
        f"- LOAO ML mean NDCG@3: {all_results['A']['loao']['ml_mean']:.4f}",
        f"- LOAO ARCH_3: {all_results['A']['loao']['ml']['ARCH_3']:.4f} "
        f"(heuristic: {all_results['A']['loao']['heuristic']['ARCH_3']:.4f}, "
        f"delta: {all_results['A']['loao']['ml']['ARCH_3'] - all_results['A']['loao']['heuristic']['ARCH_3']:+.4f})",
        "",
        "### Config B (No heuristic_match, 29 features)",
        f"- Global ML NDCG@3: {all_results['B']['global']['ml_mean_ndcg3']:.4f}",
        f"- LOAO ML mean NDCG@3: {all_results['B']['loao']['ml_mean']:.4f}",
        f"- LOAO ARCH_3: {all_results['B']['loao']['ml']['ARCH_3']:.4f}",
        "",
        "### Config C (No archetype_id, 29 features)",
        f"- Global ML NDCG@3: {all_results['C']['global']['ml_mean_ndcg3']:.4f}",
        f"- LOAO ML mean NDCG@3: {all_results['C']['loao']['ml_mean']:.4f}",
        f"- LOAO ARCH_3: {all_results['C']['loao']['ml']['ARCH_3']:.4f}",
        "",
        "### Config D (No immediate_need, 29 features)",
        f"- Global ML NDCG@3: {all_results['D']['global']['ml_mean_ndcg3']:.4f}",
        f"- LOAO ML mean NDCG@3: {all_results['D']['loao']['ml_mean']:.4f}",
        f"- LOAO ARCH_3: {all_results['D']['loao']['ml']['ARCH_3']:.4f}",
        "",
        "### Config E (Combined, 27 features)",
        f"- Global ML NDCG@3: {all_results['E']['global']['ml_mean_ndcg3']:.4f}",
        f"- LOAO ML mean NDCG@3: {all_results['E']['loao']['ml_mean']:.4f}",
        f"- LOAO ARCH_3: {all_results['E']['loao']['ml']['ARCH_3']:.4f}",
        "",
        "## Interpretation",
        "",
        "- These are **exploratory** ablation results on single-annotator labels.",
        "- All configurations use identical GroupKFold folds and LOAO partitions.",
        "- No hyperparameter tuning was performed.",
        "- The `immediate_need_matches_heuristic_primary` feature directly encodes whether a "
          "scheme matches the heuristic's primary scheme for that immediate need; removing it "
          "tests whether the model is simply replicating heuristic judgments.",
        "- The `archetype_id` feature identifies which of six repeating scenario patterns a "
          "scenario belongs to; removing it tests archetype memorization.",
        "- The `immediate_need` feature is the text label of the scenario's primary need; "
          "removing it tests whether the model learns need-specific scheme preferences.",
        "- A config that performs worse than Config A on ARCH_3 LOAO suggests the removed "
          "features were important for that archetype's generalization.",
        "- A config that performs better suggests the removed features were causing "
          "overfitting to archetype patterns.",
        "",
        "## Outputs",
        "",
        f"- Ablation metadata: `{ABLATION_METADATA_PATH}`",
        f"- Ablation results: `{ABLATION_RESULTS_PATH}`",
        f"- Report: `{REPORT_OUT}`",
        "",
        "## Reproducibility",
        "",
        "- Random seed: 42",
        "- scikit-learn version: 1.8.0",
        "- All data loaded from repository sources (no external downloads)",
        "- v1.1.0 outputs preserved unchanged under data/benchmarks/v1.1/ml_experiment/",
        "",
        "---",
        "*Generated by ablate_ml_ranker_v1_1.py. Exploratory only — not a formal "
        "pre-registered evaluation.*",
    ])

    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"  Report: {REPORT_OUT}")

    print("\n" + "=" * 70)
    print("Feature-ablation experiment complete.")
    print("=" * 70)

    return all_results


if __name__ == "__main__":
    results = main()
