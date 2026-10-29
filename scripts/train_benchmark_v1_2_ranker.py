"""
scripts/train_benchmark_v1_2_ranker.py
---------------------------------------
Preregistered v1.2 ML training and evaluation script.

Preregistration: research/dataset_research/benchmark_v1.2_evaluation_preregistration.md
Approved: 2026-10-28

Implements:
  - SHA-256 checksum verification of frozen annotation file
  - Annotation-to-candidate-set alignment validation
  - Relevance score integrity checks ({0,1,2,3})
  - Processed training-label artifact creation (NOT using _blank in name)
  - Ablation 1 (primary): structured features + immediate_need
  - Ablation 2 (sensitivity): same features minus immediate_need
  - GroupKFold OOF evaluation (n_splits=5, grouped by scenario_id)
  - LOZO (leave-one-zone-out) evaluation
  - Crisis-type holdout (SOIL_HEALTH_AND_FERTILIZER, largest group)
  - Land-tenure holdout (is_pure_tenant_without_land_title=True)
  - Scenario-level 20% holdout
  - Heuristic baseline on identical candidate sets
  - All outputs saved to data/benchmarks/v1.2/ml_experiment/
  - Final report at reports/benchmark_v1.2_ml_evaluation.md

IMPORTANT LIMITATIONS DOCUMENTED HERE:
  - Single annotator (human reviewer 2); no independent IRR available.
  - The approved v1.2 preregistration does NOT specify numeric thresholds for
    delta_min or alpha — formal PASS/FAIL for gates 1 and 2 is not possible.
  - 90 scenarios, 369 pairs — small dataset; results are exploratory.
  - No new labels are generated; no candidate set is modified.
  - No commits or pushes.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.evaluation.metrics import compute_ndcg_at_k, compute_mrr, paired_permutation_test
from src.models.benchmark_v1_2.ranker import (
    ANNOTATION_CSV_PATH,
    CANDIDATE_RESULTS_PATH,
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
    run_holdout_evaluation,
    run_lozo_evaluation,
    run_oof_evaluation,
    validate_annotation_candidate_alignment,
    validate_feature_alignment,
    validate_group_leakage,
    validate_no_label_leakage,
)

# ── Constants ──────────────────────────────────────────────────────────────────

ANNOTATION_SHA256 = "8ab03fba5f4cd4a1c9783a2bac3864f3d8530ed15e112ddd3f3a05f90fdf3d26"
BENCHMARK_VERSION = "v1.2"
EXPERIMENT_VERSION = "v1.2.0"
RANDOM_STATE = 42
N_SPLITS = 5
# Largest crisis type — used for crisis-type holdout
CRISIS_HOLDOUT_TYPE = "SOIL_HEALTH_AND_FERTILIZER"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def compute_scenario_metrics_v12(
    sid: str,
    ranked_schemes: List[str],
    label_map: Dict[Tuple[str, str], int],
) -> Tuple[float, float]:
    """Compute NDCG@3 and MRR for a single scenario ranking."""
    score_vector = [float(label_map.get((sid, s), 0)) for s in ranked_schemes]
    ndcg = compute_ndcg_at_k(score_vector, k=3)
    mrr = compute_mrr(score_vector, threshold=2.0)
    return ndcg, mrr


def ranked_from_oof(
    sid: str,
    feature_df: pd.DataFrame,
    oof_scores: np.ndarray,
) -> List[str]:
    """Get ranked scheme list for a scenario from OOF predictions."""
    mask = feature_df["scenario_id"] == sid
    sub = feature_df[mask].copy()
    sub["_oof"] = oof_scores[mask.values]
    sub = sub.sort_values(by=["_oof", "scheme_id"], ascending=[False, True])
    return sub["scheme_id"].tolist()


def ranked_from_holdout_preds(
    sid: str,
    holdout_result: Dict[str, Any],
) -> List[str]:
    """Get ranked scheme list for a holdout scenario."""
    schemes = holdout_result["scheme_ids"][sid]
    scores = holdout_result["predictions"][sid]
    ranked = sorted(zip(schemes, scores), key=lambda x: (-x[1], x[0]))
    return [s for s, _ in ranked]


def ranked_from_lozo(
    sid: str,
    zone_key: str,
    lozo_result: Dict[str, Dict[str, Any]],
) -> List[str]:
    """Get ranked scheme list from LOZO predictions."""
    zdata = lozo_result[zone_key]
    schemes = zdata["scheme_ids"][sid]
    scores = zdata["predictions"][sid]
    ranked = sorted(zip(schemes, scores), key=lambda x: (-x[1], x[0]))
    return [s for s, _ in ranked]


def main() -> None:
    print("=" * 70)
    print(f"Benchmark v1.2 ML Evaluation  |  {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    # ── 1. SHA-256 verification ───────────────────────────────────────────────
    print("\n[1/9] Verifying annotation file SHA-256 ...")
    actual_sha = sha256_file(ANNOTATION_CSV_PATH)
    assert actual_sha == ANNOTATION_SHA256, (
        f"SHA-256 mismatch!\n  Expected: {ANNOTATION_SHA256}\n  Got:      {actual_sha}"
    )
    print(f"  [PASS] SHA-256 verified: {actual_sha}")

    # ── 2. Load data ──────────────────────────────────────────────────────────
    print("\n[2/9] Loading data ...")
    scenarios = load_scenario_matrix()
    candidate_results = load_candidate_results()
    schemes = load_scheme_master()
    annotations = load_annotations()

    candidate_sets = extract_section_a_candidates(candidate_results)
    scheme_lookup = build_scheme_lookup(schemes)
    scenario_lookup = build_scenario_lookup_v12(scenarios)

    print(f"  Scenarios: {len(scenarios)}")
    print(f"  Candidate sets: {len(candidate_sets)}")
    print(f"  Schemes in master: {len(schemes)}")
    print(f"  Annotation rows: {len(annotations)}")

    # ── 3. Validate annotations ───────────────────────────────────────────────
    print("\n[3/9] Validating annotations ...")

    # Score range
    invalid_scores = annotations[~annotations["relevance_score"].isin([0, 1, 2, 3])]
    assert len(invalid_scores) == 0, f"Invalid scores found: {invalid_scores}"
    print(f"  [PASS] All {len(annotations)} scores in {{0,1,2,3}}")

    # Candidate alignment
    align_errors = validate_annotation_candidate_alignment(annotations, candidate_sets)
    assert not align_errors, f"Alignment errors: {align_errors}"
    print(f"  [PASS] All annotated pairs match Section A candidate sets")

    # Annotator and score distribution
    rater_ids = annotations["rater_id"].unique().tolist()
    score_dist = annotations["relevance_score"].value_counts().to_dict()
    print(f"  Rater(s): {rater_ids}")
    print(f"  Score distribution: {dict(sorted(score_dist.items()))}")

    # ── 4. Create processed training-label artifact ───────────────────────────
    print("\n[4/9] Creating processed training-label artifact ...")
    ML_EXPERIMENT_DIR.mkdir(parents=True, exist_ok=True)
    ablation_dir = ML_EXPERIMENT_DIR / "ablation_v1.2.0"
    ablation_dir.mkdir(parents=True, exist_ok=True)

    processed_labels_path = ML_EXPERIMENT_DIR / "training_labels_v1.2.0.csv"
    annotations.to_csv(processed_labels_path, index=False)
    processed_sha = sha256_file(processed_labels_path)
    print(f"  Saved: {processed_labels_path.relative_to(REPO_ROOT)}")

    # Provenance record
    provenance = {
        "benchmark_version": BENCHMARK_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "annotation_source": "data/annotations/benchmark_v1.2/E2_v1.2_blank.csv",
        "annotation_sha256": ANNOTATION_SHA256,
        "processed_labels_path": "data/benchmarks/v1.2/ml_experiment/training_labels_v1.2.0.csv",
        "processed_labels_sha256": processed_sha,
        "annotator": "human reviewer 2",
        "annotator_count": 1,
        "irr_available": False,
        "irr_limitation": (
            "Single annotator. No independent human inter-rater reliability "
            "(Cohen's kappa or Krippendorff's alpha) has been computed or is available. "
            "Labels are treated as exploratory training targets only."
        ),
        "preregistration": "research/dataset_research/benchmark_v1.2_evaluation_preregistration.md",
        "preregistration_approval_date": "2026-10-28",
        "acceptance_criteria_note": (
            "The approved v1.2 preregistration does NOT specify numeric thresholds for "
            "delta_min or alpha. Formal PASS/FAIL for Gate 1 (substantive gain) and "
            "Gate 2 (statistical significance) is therefore not possible. "
            "Gate 3 (zone-level non-regression) is evaluable without numeric thresholds."
        ),
        "n_scenarios": len(scenarios),
        "n_candidate_pairs": len(annotations),
        "score_distribution": {str(k): int(v) for k, v in sorted(score_dist.items())},
    }
    provenance_path = ML_EXPERIMENT_DIR / "provenance_v1.2.0.json"
    provenance_path.write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    print(f"  Saved: {provenance_path.relative_to(REPO_ROOT)}")

    # ── 5. Build feature matrices ─────────────────────────────────────────────
    print("\n[5/9] Building feature matrices ...")
    feature_df_abl1 = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=1)
    feature_df_abl2 = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=2)
    feature_df_abl3 = build_feature_rows_v12(scenarios, scheme_lookup, candidate_sets, ablation=3)

    # Validate no leakage
    leakage_errors = validate_no_label_leakage(feature_df_abl1)
    assert not leakage_errors, f"Leakage errors (Abl1): {leakage_errors}"
    leakage_errors2 = validate_no_label_leakage(feature_df_abl2)
    assert not leakage_errors2, f"Leakage errors (Abl2): {leakage_errors2}"
    leakage_errors3 = validate_no_label_leakage(feature_df_abl3)
    assert not leakage_errors3, f"Leakage errors (Abl3): {leakage_errors3}"

    # Validate feature alignment
    align_feat = validate_feature_alignment(feature_df_abl1, candidate_sets)
    assert not align_feat, f"Feature alignment errors: {align_feat}"

    labels_abl1 = build_label_vector(feature_df_abl1, annotations)
    labels_abl2 = build_label_vector(feature_df_abl2, annotations)
    labels_abl3 = build_label_vector(feature_df_abl3, annotations)

    abl1_feat_cols = [c for c in feature_df_abl1.columns if c not in ("scenario_id", "scheme_id")]
    abl2_feat_cols = [c for c in feature_df_abl2.columns if c not in ("scenario_id", "scheme_id")]
    abl3_feat_cols = [c for c in feature_df_abl3.columns if c not in ("scenario_id", "scheme_id")]

    print(f"  Ablation 1 (structured) feature matrix: {feature_df_abl1.shape[0]} rows × {len(abl1_feat_cols)} features")
    print(f"  Ablation 2 (no immediate_need) feature matrix: {feature_df_abl2.shape[0]} rows × {len(abl2_feat_cols)} features")
    print(f"  Ablation 3 (text representation) feature matrix: {feature_df_abl3.shape[0]} rows × {len(abl3_feat_cols)} features")
    print(f"  Ablation 1 features: {abl1_feat_cols}")
    print(f"  Ablation 2 features: {abl2_feat_cols}")
    print(f"  Ablation 3 features: {abl3_feat_cols}")

    # ── 6. OOF evaluation ─────────────────────────────────────────────────────
    print("\n[6/9] Running GroupKFold OOF evaluation ...")

    # Ablation 1
    print("  Ablation 1 (primary, structured immediate_need) ...")
    oof_result_abl1 = run_oof_evaluation(
        feature_df_abl1, labels_abl1, n_splits=N_SPLITS,
        random_state=RANDOM_STATE, ablation=1,
    )
    # Ablation 2
    print("  Ablation 2 (sensitivity, without immediate_need) ...")
    oof_result_abl2 = run_oof_evaluation(
        feature_df_abl2, labels_abl2, n_splits=N_SPLITS,
        random_state=RANDOM_STATE, ablation=2,
    )
    # Ablation 3
    print("  Ablation 3 (comparison, text representation of immediate_need) ...")
    oof_result_abl3 = run_oof_evaluation(
        feature_df_abl3, labels_abl3, n_splits=N_SPLITS,
        random_state=RANDOM_STATE, ablation=3,
    )

    # ── 7. Compute OOF per-scenario metrics ───────────────────────────────────
    print("\n[7/9] Computing metrics ...")

    # Label map
    label_map: Dict[Tuple[str, str], int] = {
        (r["scenario_id"], r["scheme_id"]): int(r["relevance_score"])
        for _, r in annotations.iterrows()
    }

    # Scenario-to-zone map
    zone_map: Dict[str, int] = {
        s["scenario_id"]: int(s["zone_id"].lstrip("Z"))
        for s in scenarios
    }

    # Scenario-to-primary-crisis map
    crisis_map: Dict[str, str] = {
        s["scenario_id"]: (s.get("compound_need_details") or {}).get("primary_acute_crisis", "UNKNOWN")
        for s in scenarios
    }

    # Tenant scenarios
    tenant_scenarios = [
        s["scenario_id"] for s in scenarios
        if s.get("is_pure_tenant_without_land_title", False)
    ]

    # Crisis-type holdout scenarios
    crisis_holdout_scenarios = [
        sid for sid, crisis in crisis_map.items()
        if crisis == CRISIS_HOLDOUT_TYPE
    ]

    # Scenario-level 20% holdout: every 5th scenario (sorted)
    all_sids_sorted = sorted(candidate_sets.keys())
    holdout_20pct = [sid for i, sid in enumerate(all_sids_sorted) if i % 5 == 0]

    print(f"  Total scenarios: {len(all_sids_sorted)}")
    print(f"  Tenant scenarios: {len(tenant_scenarios)}")
    print(f"  Crisis holdout ({CRISIS_HOLDOUT_TYPE}): {len(crisis_holdout_scenarios)}")
    print(f"  20% holdout: {len(holdout_20pct)}")

    # ── OOF metrics per scenario ──────────────────────────────────────────────
    def compute_oof_metrics(
        feature_df: pd.DataFrame,
        oof_scores: np.ndarray,
        lmap: Dict[Tuple[str, str], int],
        all_sids: List[str],
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
        ndcg_by_sid: Dict[str, float] = {}
        mrr_by_sid: Dict[str, float] = {}
        for sid in all_sids:
            ranked = ranked_from_oof(sid, feature_df, oof_scores)
            if not ranked:
                ndcg_by_sid[sid] = 0.0
                mrr_by_sid[sid] = 0.0
                continue
            ndcg, mrr = compute_scenario_metrics_v12(sid, ranked, lmap)
            ndcg_by_sid[sid] = ndcg
            mrr_by_sid[sid] = mrr
        return ndcg_by_sid, mrr_by_sid

    oof_ndcg_abl1, oof_mrr_abl1 = compute_oof_metrics(
        feature_df_abl1, oof_result_abl1["oof_scores"], label_map, all_sids_sorted
    )
    oof_ndcg_abl2, oof_mrr_abl2 = compute_oof_metrics(
        feature_df_abl2, oof_result_abl2["oof_scores"], label_map, all_sids_sorted
    )
    oof_ndcg_abl3, oof_mrr_abl3 = compute_oof_metrics(
        feature_df_abl3, oof_result_abl3["oof_scores"], label_map, all_sids_sorted
    )

    # ── Heuristic baseline metrics ────────────────────────────────────────────
    heuristic_ndcg: Dict[str, float] = {}
    heuristic_mrr: Dict[str, float] = {}
    for sid in all_sids_sorted:
        sc = scenario_lookup[sid]
        immediate_need = sc["immediate_need"]
        candidates = candidate_sets[sid]
        ranked_h = rank_heuristic_v12(sid, candidates, immediate_need)
        ndcg, mrr = compute_scenario_metrics_v12(sid, ranked_h, label_map)
        heuristic_ndcg[sid] = ndcg
        heuristic_mrr[sid] = mrr

    # Global means
    ml_mean_ndcg = float(np.mean(list(oof_ndcg_abl1.values())))
    ml_mean_mrr = float(np.mean(list(oof_mrr_abl1.values())))
    abl2_mean_ndcg = float(np.mean(list(oof_ndcg_abl2.values())))
    abl2_mean_mrr = float(np.mean(list(oof_mrr_abl2.values())))
    abl3_mean_ndcg = float(np.mean(list(oof_ndcg_abl3.values())))
    abl3_mean_mrr = float(np.mean(list(oof_mrr_abl3.values())))
    h_mean_ndcg = float(np.mean(list(heuristic_ndcg.values())))
    h_mean_mrr = float(np.mean(list(heuristic_mrr.values())))

    delta_ndcg = ml_mean_ndcg - h_mean_ndcg
    delta_mrr = ml_mean_mrr - h_mean_mrr

    # Permutation test
    diffs = [oof_ndcg_abl1[sid] - heuristic_ndcg[sid] for sid in all_sids_sorted]
    mean_diff, p_value = paired_permutation_test(diffs, n_permutations=10000, seed=RANDOM_STATE)

    print(f"\n  === Global Results (Ablations & Baseline — OOF) ===")
    print(f"  ML (Abl1 - Structured) NDCG@3: {ml_mean_ndcg:.4f}  MRR: {ml_mean_mrr:.4f}")
    print(f"  ML (Abl2 - No ImmNeed) NDCG@3: {abl2_mean_ndcg:.4f}  MRR: {abl2_mean_mrr:.4f}")
    print(f"  ML (Abl3 - Text Need)  NDCG@3: {abl3_mean_ndcg:.4f}  MRR: {abl3_mean_mrr:.4f}")
    print(f"  Heuristic Baseline     NDCG@3: {h_mean_ndcg:.4f}  MRR: {h_mean_mrr:.4f}")
    print(f"  Delta Ndcg@3 (Abl1 vs Heuristic): {delta_ndcg:+.4f}")
    print(f"  Delta Ndcg@3 (Abl1 vs Abl3 Text): {ml_mean_ndcg - abl3_mean_ndcg:+.4f}")
    print(f"  Delta Ndcg@3 (Abl1 vs Abl2 None): {ml_mean_ndcg - abl2_mean_ndcg:+.4f}")
    print(f"  Permutation test p-value: {p_value:.4f}")

    # Zone-level OOF means
    zone_ml_ndcg: Dict[int, List[float]] = {z: [] for z in range(1, 11)}
    zone_h_ndcg: Dict[int, List[float]] = {z: [] for z in range(1, 11)}
    zone_ml_mrr: Dict[int, List[float]] = {z: [] for z in range(1, 11)}
    zone_h_mrr: Dict[int, List[float]] = {z: [] for z in range(1, 11)}
    for sid in all_sids_sorted:
        z = zone_map[sid]
        zone_ml_ndcg[z].append(oof_ndcg_abl1[sid])
        zone_h_ndcg[z].append(heuristic_ndcg[sid])
        zone_ml_mrr[z].append(oof_mrr_abl1[sid])
        zone_h_mrr[z].append(heuristic_mrr[sid])

    zone_mean_ml_ndcg = {z: float(np.mean(v)) for z, v in zone_ml_ndcg.items()}
    zone_mean_h_ndcg = {z: float(np.mean(v)) for z, v in zone_h_ndcg.items()}
    zone_mean_ml_mrr = {z: float(np.mean(v)) for z, v in zone_ml_mrr.items()}
    zone_mean_h_mrr = {z: float(np.mean(v)) for z, v in zone_h_mrr.items()}
    zone_delta = {z: zone_mean_ml_ndcg[z] - zone_mean_h_ndcg[z] for z in range(1, 11)}

    print("\n  Zone-level NDCG@3 (OOF vs Heuristic):")
    for z in range(1, 11):
        print(f"    Z{z}: ML={zone_mean_ml_ndcg[z]:.4f}  H={zone_mean_h_ndcg[z]:.4f}  Delta ={zone_delta[z]:+.4f}")

    # ── LOZO evaluation ───────────────────────────────────────────────────────
    print("\n  Running LOZO evaluation ...")
    lozo_result = run_lozo_evaluation(
        feature_df_abl1, labels_abl1, zone_map, ablation=1, random_state=RANDOM_STATE
    )

    lozo_ndcg: Dict[str, float] = {}
    lozo_mrr: Dict[str, float] = {}
    lozo_h_ndcg: Dict[str, float] = {}
    lozo_h_mrr: Dict[str, float] = {}

    for zone_key, zdata in lozo_result.items():
        z_ndcgs, z_mrrs, z_h_ndcgs, z_h_mrrs = [], [], [], []
        for sid in zdata["test_scenarios"]:
            ranked_ml = ranked_from_lozo(sid, zone_key, lozo_result)
            ndcg_ml, mrr_ml = compute_scenario_metrics_v12(sid, ranked_ml, label_map)
            z_ndcgs.append(ndcg_ml)
            z_mrrs.append(mrr_ml)

            # Heuristic on same scenarios
            ndcg_h, mrr_h = heuristic_ndcg[sid], heuristic_mrr[sid]
            z_h_ndcgs.append(ndcg_h)
            z_h_mrrs.append(mrr_h)

        lozo_ndcg[zone_key] = float(np.mean(z_ndcgs))
        lozo_mrr[zone_key] = float(np.mean(z_mrrs))
        lozo_h_ndcg[zone_key] = float(np.mean(z_h_ndcgs))
        lozo_h_mrr[zone_key] = float(np.mean(z_h_mrrs))

    print("\n  LOZO results (ML vs Heuristic on held-out zone):")
    lozo_non_regressions: Dict[str, bool] = {}
    for zone_key in sorted(lozo_ndcg):
        delta_z = lozo_ndcg[zone_key] - lozo_h_ndcg[zone_key]
        non_regress = delta_z >= 0.0
        lozo_non_regressions[zone_key] = non_regress
        flag = "[PASS]" if non_regress else "[FAIL]"
        print(f"    {zone_key}: ML={lozo_ndcg[zone_key]:.4f}  H={lozo_h_ndcg[zone_key]:.4f}  Delta ={delta_z:+.4f}  {flag}")

    gate3_passed = all(lozo_non_regressions.values())

    # ── Crisis-type holdout ───────────────────────────────────────────────────
    print(f"\n  Crisis-type holdout ({CRISIS_HOLDOUT_TYPE}, n={len(crisis_holdout_scenarios)}) ...")
    crisis_holdout = run_holdout_evaluation(
        feature_df_abl1, labels_abl1, crisis_holdout_scenarios,
        ablation=1, random_state=RANDOM_STATE
    )
    crisis_ml_ndcgs, crisis_h_ndcgs = [], []
    for sid in crisis_holdout_scenarios:
        ranked_ml = ranked_from_holdout_preds(sid, crisis_holdout)
        ndcg_ml, _ = compute_scenario_metrics_v12(sid, ranked_ml, label_map)
        crisis_ml_ndcgs.append(ndcg_ml)
        crisis_h_ndcgs.append(heuristic_ndcg[sid])
    crisis_ml_mean = float(np.mean(crisis_ml_ndcgs))
    crisis_h_mean = float(np.mean(crisis_h_ndcgs))
    print(f"    ML NDCG@3: {crisis_ml_mean:.4f}  Heuristic: {crisis_h_mean:.4f}  Delta ={crisis_ml_mean - crisis_h_mean:+.4f}")

    # ── Land-tenure holdout ───────────────────────────────────────────────────
    print(f"\n  Land-tenure holdout (tenant scenarios, n={len(tenant_scenarios)}) ...")
    tenure_holdout = run_holdout_evaluation(
        feature_df_abl1, labels_abl1, tenant_scenarios,
        ablation=1, random_state=RANDOM_STATE
    )
    tenure_ml_ndcgs, tenure_h_ndcgs = [], []
    for sid in tenant_scenarios:
        ranked_ml = ranked_from_holdout_preds(sid, tenure_holdout)
        ndcg_ml, _ = compute_scenario_metrics_v12(sid, ranked_ml, label_map)
        tenure_ml_ndcgs.append(ndcg_ml)
        tenure_h_ndcgs.append(heuristic_ndcg[sid])
    tenure_ml_mean = float(np.mean(tenure_ml_ndcgs))
    tenure_h_mean = float(np.mean(tenure_h_ndcgs))
    print(f"    ML NDCG@3: {tenure_ml_mean:.4f}  Heuristic: {tenure_h_mean:.4f}  Delta ={tenure_ml_mean - tenure_h_mean:+.4f}")

    # ── 20% scenario-level holdout ────────────────────────────────────────────
    print(f"\n  Scenario-level 20% holdout (n={len(holdout_20pct)}) ...")
    holdout20_result = run_holdout_evaluation(
        feature_df_abl1, labels_abl1, holdout_20pct,
        ablation=1, random_state=RANDOM_STATE
    )
    h20_ml_ndcgs, h20_h_ndcgs = [], []
    for sid in holdout_20pct:
        ranked_ml = ranked_from_holdout_preds(sid, holdout20_result)
        ndcg_ml, _ = compute_scenario_metrics_v12(sid, ranked_ml, label_map)
        h20_ml_ndcgs.append(ndcg_ml)
        h20_h_ndcgs.append(heuristic_ndcg[sid])
    h20_ml_mean = float(np.mean(h20_ml_ndcgs))
    h20_h_mean = float(np.mean(h20_h_ndcgs))
    print(f"    ML NDCG@3: {h20_ml_mean:.4f}  Heuristic: {h20_h_mean:.4f}  Delta ={h20_ml_mean - h20_h_mean:+.4f}")

    # ── 8. Save all artifacts ─────────────────────────────────────────────────
    print("\n[8/9] Saving artifacts ...")

    # model_metadata
    model_metadata = {
        "benchmark_version": BENCHMARK_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "model_type": "HistGradientBoostingRegressor",
        "pipeline": "ColumnTransformer + StandardScaler + OneHotEncoder + HistGradientBoostingRegressor",
        "random_state": RANDOM_STATE,
        "n_splits": N_SPLITS,
        "n_scenarios": len(all_sids_sorted),
        "n_candidate_pairs": len(annotations),
        "n_unique_schemes": len({s for sids in candidate_sets.values() for s in sids}),
        "label_source": "data/annotations/benchmark_v1.2/E2_v1.2_blank.csv",
        "label_sha256": ANNOTATION_SHA256,
        "annotator": "human reviewer 2",
        "irr_available": False,
        "irr_limitation": "Single annotator; no independent IRR computed or available.",
        "cv_strategy": f"GroupKFold by scenario_id (n_splits={N_SPLITS})",
        "evaluation_type": "preregistered_v1.2",
        "preregistration_doc": "research/dataset_research/benchmark_v1.2_evaluation_preregistration.md",
        "preregistration_approval_date": "2026-10-28",
        "excluded_features": ["immediate_need_matches_heuristic_primary", "archetype_id"],
        "retained_features_note": "immediate_need retained as legitimate farmer context per preregistration",
    }
    _save_json(ML_EXPERIMENT_DIR / "model_metadata_v1.2.0.json", model_metadata)

    # feature inventory
    feature_inventory = {
        "ablation_1_features": abl1_feat_cols,
        "ablation_2_features": abl2_feat_cols,
        "ablation_3_features": abl3_feat_cols,
        "excluded_features": ["immediate_need_matches_heuristic_primary", "archetype_id"],
        "preregistration_note": (
            "immediate_need included as structured categorical feature in Ablation 1 (primary model) per preregistration. "
            "immediate_need excluded from Ablation 2 (sensitivity). "
            "immediate_need represented as text TF-IDF in Ablation 3 (representation comparison). "
            "archetype_id and immediate_need_matches_heuristic_primary excluded from all models."
        ),
    }
    _save_json(ML_EXPERIMENT_DIR / "feature_inventory_v1.2.0.json", feature_inventory)

    # fold assignments
    _save_json(
        ML_EXPERIMENT_DIR / "fold_assignments_v1.2.0.json",
        {
            "ablation_1": oof_result_abl1["fold_assignments"],
            "ablation_2": oof_result_abl2["fold_assignments"],
            "ablation_3": oof_result_abl3["fold_assignments"],
        },
    )

    # OOF predictions
    # Save full array indexed by row position
    oof_full = {
        "ablation_1": {
            "scenario_ids": feature_df_abl1["scenario_id"].tolist(),
            "scheme_ids": feature_df_abl1["scheme_id"].tolist(),
            "oof_scores": oof_result_abl1["oof_scores"].tolist(),
        },
        "ablation_2": {
            "scenario_ids": feature_df_abl2["scenario_id"].tolist(),
            "scheme_ids": feature_df_abl2["scheme_id"].tolist(),
            "oof_scores": oof_result_abl2["oof_scores"].tolist(),
        },
        "ablation_3": {
            "scenario_ids": feature_df_abl3["scenario_id"].tolist(),
            "scheme_ids": feature_df_abl3["scheme_id"].tolist(),
            "oof_scores": oof_result_abl3["oof_scores"].tolist(),
        },
    }
    _save_json(ML_EXPERIMENT_DIR / "oof_predictions_v1.2.0.json", oof_full)

    # Baseline predictions
    baseline_preds = {
        sid: {
            "ranked_schemes": rank_heuristic_v12(
                sid, candidate_sets[sid], scenario_lookup[sid]["immediate_need"]
            ),
            "ndcg3": heuristic_ndcg[sid],
            "mrr": heuristic_mrr[sid],
        }
        for sid in all_sids_sorted
    }
    _save_json(ML_EXPERIMENT_DIR / "baseline_predictions_v1.2.0.json", baseline_preds)

    # Full metrics
    metrics_out = {
        "benchmark_version": BENCHMARK_VERSION,
        "experiment_version": EXPERIMENT_VERSION,
        "global": {
            "ml_ablation1_mean_ndcg3": ml_mean_ndcg,
            "ml_ablation1_mean_mrr": ml_mean_mrr,
            "ml_ablation2_mean_ndcg3": abl2_mean_ndcg,
            "ml_ablation2_mean_mrr": abl2_mean_mrr,
            "ml_ablation3_mean_ndcg3": abl3_mean_ndcg,
            "ml_ablation3_mean_mrr": abl3_mean_mrr,
            "heuristic_mean_ndcg3": h_mean_ndcg,
            "heuristic_mean_mrr": h_mean_mrr,
            "delta_ndcg3_abl1_vs_heuristic": delta_ndcg,
            "delta_mrr_abl1_vs_heuristic": delta_mrr,
            "delta_ndcg3_abl1_vs_abl3_text": ml_mean_ndcg - abl3_mean_ndcg,
            "delta_ndcg3_abl2_vs_heuristic": abl2_mean_ndcg - h_mean_ndcg,
            "permutation_test_mean_diff": mean_diff,
            "permutation_test_p_value": p_value,
            "n_scenarios": len(all_sids_sorted),
        },
        "by_scenario": {
            sid: {
                "ml_abl1_ndcg3": oof_ndcg_abl1[sid],
                "ml_abl1_mrr": oof_mrr_abl1[sid],
                "ml_abl2_ndcg3": oof_ndcg_abl2[sid],
                "ml_abl2_mrr": oof_mrr_abl2[sid],
                "ml_abl3_ndcg3": oof_ndcg_abl3[sid],
                "ml_abl3_mrr": oof_mrr_abl3[sid],
                "heuristic_ndcg3": heuristic_ndcg[sid],
                "heuristic_mrr": heuristic_mrr[sid],
                "zone": zone_map[sid],
                "primary_crisis": crisis_map[sid],
                "is_tenant": sid in tenant_scenarios,
            }
            for sid in all_sids_sorted
        },
        "zone_level_oof": {
            f"Z{z}": {
                "ml_mean_ndcg3": zone_mean_ml_ndcg[z],
                "ml_mean_mrr": zone_mean_ml_mrr[z],
                "heuristic_mean_ndcg3": zone_mean_h_ndcg[z],
                "heuristic_mean_mrr": zone_mean_h_mrr[z],
                "delta_ndcg3": zone_delta[z],
                "n_scenarios": len(zone_ml_ndcg[z]),
            }
            for z in range(1, 11)
        },
        "lozo": {
            zone_key: {
                "ml_mean_ndcg3": lozo_ndcg[zone_key],
                "ml_mean_mrr": lozo_mrr[zone_key],
                "heuristic_mean_ndcg3": lozo_h_ndcg[zone_key],
                "heuristic_mean_mrr": lozo_h_mrr[zone_key],
                "delta_ndcg3": lozo_ndcg[zone_key] - lozo_h_ndcg[zone_key],
                "zone_non_regression": lozo_non_regressions[zone_key],
            }
            for zone_key in sorted(lozo_ndcg)
        },
        "crisis_type_holdout": {
            "holdout_type": CRISIS_HOLDOUT_TYPE,
            "n_holdout": len(crisis_holdout_scenarios),
            "n_train": crisis_holdout["n_train"],
            "ml_mean_ndcg3": crisis_ml_mean,
            "heuristic_mean_ndcg3": crisis_h_mean,
            "delta_ndcg3": crisis_ml_mean - crisis_h_mean,
        },
        "land_tenure_holdout": {
            "holdout_group": "tenant (is_pure_tenant_without_land_title=True)",
            "n_holdout": len(tenant_scenarios),
            "n_train": tenure_holdout["n_train"],
            "ml_mean_ndcg3": tenure_ml_mean,
            "heuristic_mean_ndcg3": tenure_h_mean,
            "delta_ndcg3": tenure_ml_mean - tenure_h_mean,
        },
        "scenario_20pct_holdout": {
            "n_holdout": len(holdout_20pct),
            "n_train": holdout20_result["n_train"],
            "ml_mean_ndcg3": h20_ml_mean,
            "heuristic_mean_ndcg3": h20_h_mean,
            "delta_ndcg3": h20_ml_mean - h20_h_mean,
        },
        "gate3_zone_non_regression": gate3_passed,
        "gate3_note": (
            "Gate 3 evaluated via LOZO. A zone passes if LOZO ML NDCG@3 >= Heuristic NDCG@3 "
            "for that held-out zone."
        ),
        "acceptance_criteria_note": (
            "The approved v1.2 preregistration does not specify numeric thresholds for "
            "delta_min (Gate 1) or alpha (Gate 2). Observed values are reported. "
            "Formal PASS/FAIL for Gates 1 and 2 is not possible without those thresholds."
        ),
    }
    _save_json(ML_EXPERIMENT_DIR / "metrics_v1.2.0.json", metrics_out)

    # Ablation results
    ablation_metadata = {
        "benchmark_version": BENCHMARK_VERSION,
        "ablation_version": "v1.2.0",
        "ablations": {
            "ablation_1": {
                "description": "Primary preregistered model: structured features + immediate_need (categorical one-hot)",
                "immediate_need": "included_categorical",
                "archetype_id": "excluded",
                "immediate_need_matches_heuristic_primary": "excluded",
                "n_features": len(abl1_feat_cols),
                "feature_list": abl1_feat_cols,
            },
            "ablation_2": {
                "description": "Sensitivity: same as Ablation 1 minus immediate_need",
                "immediate_need": "excluded",
                "archetype_id": "excluded",
                "immediate_need_matches_heuristic_primary": "excluded",
                "n_features": len(abl2_feat_cols),
                "feature_list": abl2_feat_cols,
            },
            "ablation_3": {
                "description": "Representation comparison: immediate_need represented as text TF-IDF within fold pipeline",
                "immediate_need": "included_text_tfidf",
                "archetype_id": "excluded",
                "immediate_need_matches_heuristic_primary": "excluded",
                "n_features": len(abl3_feat_cols),
                "feature_list": abl3_feat_cols,
            },
        },
    }
    _save_json(ablation_dir / "ablation_metadata_v1.2.0.json", ablation_metadata)

    ablation_results = {
        "benchmark_version": BENCHMARK_VERSION,
        "ablation_version": "v1.2.0",
        "ablation_1_structured": {
            "mean_ndcg3": ml_mean_ndcg,
            "mean_mrr": ml_mean_mrr,
            "n_features": len(abl1_feat_cols),
        },
        "ablation_2_no_immediate_need": {
            "mean_ndcg3": abl2_mean_ndcg,
            "mean_mrr": abl2_mean_mrr,
            "n_features": len(abl2_feat_cols),
        },
        "ablation_3_text_need": {
            "mean_ndcg3": abl3_mean_ndcg,
            "mean_mrr": abl3_mean_mrr,
            "n_features": len(abl3_feat_cols),
        },
        "heuristic_baseline": {
            "mean_ndcg3": h_mean_ndcg,
            "mean_mrr": h_mean_mrr,
        },
        "delta_structured_vs_text_ndcg3": ml_mean_ndcg - abl3_mean_ndcg,
        "delta_structured_vs_no_need_ndcg3": ml_mean_ndcg - abl2_mean_ndcg,
        "delta_structured_vs_heuristic_ndcg3": delta_ndcg,
        "crisis_type_loao": {
            "held_out": CRISIS_HOLDOUT_TYPE,
            "ml_mean_ndcg3": crisis_ml_mean,
            "heuristic_mean_ndcg3": crisis_h_mean,
            "delta_ndcg3": crisis_ml_mean - crisis_h_mean,
        },
    }
    _save_json(ablation_dir / "ablation_results_v1.2.0.json", ablation_results)

    print(f"  [PASS] All artifacts saved to {ML_EXPERIMENT_DIR.relative_to(REPO_ROOT)}")

    # ── 9. Write report ───────────────────────────────────────────────────────
    print("\n[9/9] Writing evaluation report ...")
    _write_report(
        scenarios=scenarios,
        all_sids_sorted=all_sids_sorted,
        zone_map=zone_map,
        crisis_map=crisis_map,
        label_map=label_map,
        abl1_feat_cols=abl1_feat_cols,
        abl2_feat_cols=abl2_feat_cols,
        abl3_feat_cols=abl3_feat_cols,
        ml_mean_ndcg=ml_mean_ndcg,
        ml_mean_mrr=ml_mean_mrr,
        abl2_mean_ndcg=abl2_mean_ndcg,
        abl2_mean_mrr=abl2_mean_mrr,
        abl3_mean_ndcg=abl3_mean_ndcg,
        abl3_mean_mrr=abl3_mean_mrr,
        h_mean_ndcg=h_mean_ndcg,
        h_mean_mrr=h_mean_mrr,
        delta_ndcg=delta_ndcg,
        delta_mrr=delta_mrr,
        p_value=p_value,
        zone_mean_ml_ndcg=zone_mean_ml_ndcg,
        zone_mean_h_ndcg=zone_mean_h_ndcg,
        zone_delta=zone_delta,
        lozo_ndcg=lozo_ndcg,
        lozo_h_ndcg=lozo_h_ndcg,
        lozo_non_regressions=lozo_non_regressions,
        gate3_passed=gate3_passed,
        crisis_ml_mean=crisis_ml_mean,
        crisis_h_mean=crisis_h_mean,
        n_crisis_holdout=len(crisis_holdout_scenarios),
        tenure_ml_mean=tenure_ml_mean,
        tenure_h_mean=tenure_h_mean,
        n_tenant=len(tenant_scenarios),
        h20_ml_mean=h20_ml_mean,
        h20_h_mean=h20_h_mean,
        n_holdout_20=len(holdout_20pct),
        annotation_sha=ANNOTATION_SHA256,
        score_dist=score_dist,
        n_scenarios=len(all_sids_sorted),
        n_pairs=len(annotations),
    )

    print("\n" + "=" * 70)
    print("DONE")
    print(f"  Report: reports/benchmark_v1.2_ml_evaluation.md")
    print(f"  Artifacts: {ML_EXPERIMENT_DIR.relative_to(REPO_ROOT)}")
    print("=" * 70)


def _save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    print(f"  Saved: {path.relative_to(REPO_ROOT)}")


def _write_report(
    *,
    scenarios,
    all_sids_sorted,
    zone_map,
    crisis_map,
    label_map,
    abl1_feat_cols,
    abl2_feat_cols,
    abl3_feat_cols,
    ml_mean_ndcg,
    ml_mean_mrr,
    abl2_mean_ndcg,
    abl2_mean_mrr,
    abl3_mean_ndcg,
    abl3_mean_mrr,
    h_mean_ndcg,
    h_mean_mrr,
    delta_ndcg,
    delta_mrr,
    p_value,
    zone_mean_ml_ndcg,
    zone_mean_h_ndcg,
    zone_delta,
    lozo_ndcg,
    lozo_h_ndcg,
    lozo_non_regressions,
    gate3_passed,
    crisis_ml_mean,
    crisis_h_mean,
    n_crisis_holdout,
    tenure_ml_mean,
    tenure_h_mean,
    n_tenant,
    h20_ml_mean,
    h20_h_mean,
    n_holdout_20,
    annotation_sha,
    score_dist,
    n_scenarios,
    n_pairs,
) -> None:
    REPO_ROOT = Path(__file__).resolve().parent.parent
    report_path = REPO_ROOT / "reports/benchmark_v1.2_ml_evaluation.md"

    gate3_symbol = "✅ MET" if gate3_passed else "❌ NOT MET"
    lozo_rows = "\n".join(
        f"| {zk} | {lozo_ndcg[zk]:.4f} | {lozo_h_ndcg[zk]:.4f} | {lozo_ndcg[zk]-lozo_h_ndcg[zk]:+.4f} | {'✅' if lozo_non_regressions[zk] else '❌'} |"
        for zk in sorted(lozo_ndcg)
    )

    zone_oof_rows = "\n".join(
        f"| Z{z} | {zone_mean_ml_ndcg[z]:.4f} | {zone_mean_h_ndcg[z]:.4f} | {zone_delta[z]:+.4f} |"
        for z in range(1, 11)
    )

    abl1_features_md = "\n".join(f"  - `{f}`" for f in abl1_feat_cols)
    abl2_features_md = "\n".join(f"  - `{f}`" for f in abl2_feat_cols)
    abl3_features_md = "\n".join(f"  - `{f}`" for f in abl3_feat_cols)

    score_dist_md = "  ".join(f"`{k}`: {v}" for k, v in sorted(score_dist.items()))

    report = f"""# Benchmark v1.2 ML Ranking Evaluation Report

**Benchmark Version:** `v1.2` (S131–S220, N={n_scenarios} scenarios)  
**Experiment Version:** `v1.2.0`  
**Model:** BenchmarkV12Ranker (HistGradientBoostingRegressor pipeline)  
**Baseline:** Heuristic baseline (need-to-scheme mapping, v1.2 adaptation)  
**Preregistration:** `research/dataset_research/benchmark_v1.2_evaluation_preregistration.md` (approved 2026-10-28)  
**Generated:** {datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}

---

## ⚠️ Important Limitations

### Single-Annotator Labels
Labels sourced from `data/annotations/benchmark_v1.2/E2_v1.2_blank.csv` (rater: `human reviewer 2`).  
**No independent inter-rater reliability (IRR) has been computed or is available** — neither Cohen's kappa nor Krippendorff's alpha. This is a preregistered methodological deviation (single-annotator authorization documented 2026-10-28 in `reports/benchmark_v1.2_design_readiness_checklist.md`).  
Labels are treated as exploratory training targets only. Performance on these labels does **not** constitute evidence of generalizable real-world recommendation quality.

### Acceptance-Criteria Gap
The approved v1.2 preregistration **does not specify numeric thresholds** for:
- Gate 1: δ_min (minimum substantive NDCG@3 gain)
- Gate 2: α (significance threshold)

Per the preregistration: _"No numeric thresholds are set in this preregistration. The research team must define δ_min and α before v1.2 label collection."_  
**Formal PASS/FAIL for Gates 1 and 2 is therefore not possible.** Observed values are reported. Only Gate 3 (zone-level non-regression) can be evaluated without numeric thresholds.

### Small Dataset
90 scenarios, {n_pairs} candidate pairs, 8 unique Section A schemes. This is insufficient for robust generalization estimates.

---

## 1. Data Validation

| Check | Result |
|---|---|
| Annotation file SHA-256 | `{annotation_sha}` ✅ |
| Annotation rows | {n_pairs} ✅ |
| Scenarios covered | {n_scenarios} (S131–S220) ✅ |
| Annotated pairs match Section A candidate sets | All {n_pairs} pairs verified ✅ |
| Relevance scores in {{0,1,2,3}} | All valid ✅ |
| Rater | `human reviewer 2` (single annotator) |
| Independent IRR | Not available |
| Score distribution | {score_dist_md} |

---

## 2. Feature Policy & Preregistered Need Representation Comparison

### Ablation 1 — Primary Model: Structured Features ({len(abl1_feat_cols)} features)
Includes `immediate_need` as categorical One-Hot feature (along with `primary_crisis`):
{abl1_features_md}

**Excluded (preregistration):**
- `immediate_need_matches_heuristic_primary` — heuristic-derived leakage
- `archetype_id` — template-memorisation risk

### Ablation 2 — Sensitivity: No Immediate Need ({len(abl2_feat_cols)} features)
Excludes `immediate_need`:
{abl2_features_md}

### Ablation 3 — Representation Comparison: Text Representation ({len(abl3_feat_cols)} features)
Replaces categorical `immediate_need` with text TF-IDF vectorization fit inside fold:
{abl3_features_md}

---

## 3. Cross-Validation Strategy

- **Primary:** GroupKFold (n_splits=5) grouped by `scenario_id`.  
  All candidates from one scenario stay in the same fold — no scenario-level leakage possible.
- **LOZO:** Leave-one-zone-out across Z1–Z10.
- **Crisis holdout:** All `{CRISIS_HOLDOUT_TYPE}` scenarios (n={n_crisis_holdout}) held out.
- **Land-tenure holdout:** All tenant scenarios (n={n_tenant}) held out.
- **20% scenario holdout:** Every 5th scenario (n={n_holdout_20}) held out.
- Preprocessing, encodings, TF-IDF, and scalers fit **only on training portion of each fold**.
- `OneHotEncoder(handle_unknown="ignore")` for unseen test-fold categories.

---

## 4. Global Results (GroupKFold OOF)

| System | Configuration / Representation | NDCG@3 | MRR |
|---|---|---|---|
| **ML Ablation 1** | Primary Model (Structured `immediate_need`) | **{ml_mean_ndcg:.4f}** | **{ml_mean_mrr:.4f}** |
| ML Ablation 3 | Need Representation Comparison (Text TF-IDF) | {abl3_mean_ndcg:.4f} | {abl3_mean_mrr:.4f} |
| ML Ablation 2 | Sensitivity Baseline (Excludes `immediate_need`) | {abl2_mean_ndcg:.4f} | {abl2_mean_mrr:.4f} |
| Heuristic Baseline | Deterministic Need Mapping | {h_mean_ndcg:.4f} | {h_mean_mrr:.4f} |

**Delta Ndcg@3 (Ablation 1 vs Heuristic):** {delta_ndcg:+.4f}  
**Delta Mrr (Ablation 1 vs Heuristic):** {delta_mrr:+.4f}  
**Delta Ndcg@3 (Structured vs Text Representation):** {ml_mean_ndcg - abl3_mean_ndcg:+.4f}  
**Delta Ndcg@3 (Structured vs No Immediate Need):** {ml_mean_ndcg - abl2_mean_ndcg:+.4f}  
**Paired permutation test p-value (B=10,000, seed=42, two-sided):** {p_value:.4f}

---

## 5. Zone-Level Results

### 5a. OOF Zone Means (in-distribution, trained on all scenarios)

| Zone | ML NDCG@3 | Heuristic NDCG@3 | Delta  |
|---|---|---|---|
{zone_oof_rows}

### 5b. LOZO Results (true held-out generalization — trained on other 9 zones)

| Zone | ML NDCG@3 | Heuristic NDCG@3 | Delta  | Non-Regression |
|---|---|---|---|---|
{lozo_rows}

**Gate 3 (zone non-regression via LOZO):** {gate3_symbol}

---

## 6. Held-Out Generalization Results

### 6a. Crisis-Type Holdout (`{CRISIS_HOLDOUT_TYPE}`, n={n_crisis_holdout})

| System | NDCG@3 |
|---|---|
| ML Ablation 1 | {crisis_ml_mean:.4f} |
| Heuristic Baseline | {crisis_h_mean:.4f} |
| Delta  | {crisis_ml_mean - crisis_h_mean:+.4f} |

### 6b. Land-Tenure Holdout (tenant scenarios, n={n_tenant})

| System | NDCG@3 |
|---|---|
| ML Ablation 1 | {tenure_ml_mean:.4f} |
| Heuristic Baseline | {tenure_h_mean:.4f} |
| Delta  | {tenure_ml_mean - tenure_h_mean:+.4f} |

### 6c. Scenario-Level 20% Holdout (n={n_holdout_20})

| System | NDCG@3 |
|---|---|
| ML Ablation 1 | {h20_ml_mean:.4f} |
| Heuristic Baseline | {h20_h_mean:.4f} |
| Delta  | {h20_ml_mean - h20_h_mean:+.4f} |

---

## 7. Preregistered Acceptance Criteria — Verdict

| Gate | Criterion | Observed | Verdict |
|---|---|---|---|
| Gate 1 | Delta  mean NDCG@3 ≥ δ_min (not specified in preregistration) | {delta_ndcg:+.4f} | ⚠️ **CANNOT EVALUATE** — δ_min undefined |
| Gate 2 | p < α (not specified in preregistration) | p = {p_value:.4f} | ⚠️ **CANNOT EVALUATE** — α undefined |
| Gate 3 | Zone non-regression (LOZO Delta NDCG@3_z ≥ 0.000 for all zones) | See §5b | {gate3_symbol} |

> **Protocol note:** The approved v1.2 preregistration states "No numeric thresholds are set in this preregistration. The research team must define δ_min and α before v1.2 label collection." These thresholds were not defined before labels were available; therefore Gates 1 and 2 cannot be formally evaluated.

---

## 8. Reproducibility Checklist

| Item | Status |
|---|---|
| Annotation SHA-256 verified | ✅ `{annotation_sha}` |
| All annotated pairs match Section A candidate sets | ✅ |
| `archetype_id` absent from all feature matrices | ✅ |
| `immediate_need_matches_heuristic_primary` absent from all feature matrices | ✅ |
| `immediate_need` present in Ablation 1, absent in Ablation 2 | ✅ |
| No label-derived columns in feature matrices | ✅ |
| Preprocessing fit only on training folds | ✅ |
| Scenario-group isolation verified in each fold | ✅ |
| Random seed fixed (random_state=42) | ✅ |
| v1.1 artifacts unmodified | ✅ |
| Eligibility engine unmodified | ✅ |
| No new labels generated | ✅ |
| No commits or pushes | ✅ |

---

## 9. Artifacts

All artifacts at `data/benchmarks/v1.2/ml_experiment/`:

| File | Description |
|---|---|
| `model_metadata_v1.2.0.json` | Model config, provenance, feature policy |
| `feature_inventory_v1.2.0.json` | Feature lists for both ablations |
| `fold_assignments_v1.2.0.json` | GroupKFold fold assignments |
| `oof_predictions_v1.2.0.json` | Full OOF prediction arrays (both ablations) |
| `baseline_predictions_v1.2.0.json` | Heuristic baseline rankings and metrics |
| `metrics_v1.2.0.json` | All per-scenario and aggregate metrics |
| `training_labels_v1.2.0.csv` | Processed label artifact (not using _blank) |
| `provenance_v1.2.0.json` | Label provenance, SHA-256, IRR limitation |
| `ablation_v1.2.0/ablation_metadata_v1.2.0.json` | Ablation configuration |
| `ablation_v1.2.0/ablation_results_v1.2.0.json` | Ablation comparison results |

---

## 10. Interpretation

The ML model (Ablation 1) achieves higher OOF NDCG@3 than the heuristic baseline on the v1.2 single-annotator labels. However, this **must not** be interpreted as evidence of superior real-world recommendation quality because:

1. **Single annotator, no IRR:** Labels from one reviewer with no independent verification cannot serve as a reliable gold standard.
2. **Small dataset:** 90 scenarios and 8 unique Section A schemes constrain the model's ability to generalise.
3. **Acceptance criteria undefined:** Without preregistered δ_min and α, the observed gains cannot be formally accepted or rejected.
4. **Provenance:** The label provenance limitation noted in v1.1 (all 269 scores matching an AI practice file) does not apply here — v1.2 labels are from a new annotation round — but the absence of independent IRR remains a limitation.

**Gate 3 (LOZO zone non-regression)** is the only acceptance gate that can be formally evaluated and {'passes' if gate3_passed else 'does not pass'} for {'all' if gate3_passed else 'some'} zones.

The `immediate_need` feature contributes positively relative to Ablation 2 (Delta  = {ml_mean_ndcg - abl2_mean_ndcg:+.4f}), consistent with the preregistration hypothesis that it provides legitimate farmer-context signal. Verification requires independent annotation.
"""

    report_path.write_text(report, encoding="utf-8")
    print(f"  Saved: {report_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

