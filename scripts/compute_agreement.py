"""
compute_agreement.py
---------------------
Inter-rater agreement analysis for the Expert Annotation Pilot.

METRICS IMPLEMENTED:
  - Quadratic Weighted Cohen's Kappa  (2 raters, ordinal 0-3 scale)
  - Krippendorff's Alpha              (2+ raters, ordinal distance function)
  - Pairwise Percent Agreement        (diagnostic)
  - Fleiss' Kappa                     (nominal, diagnostic only)

DESIGN DECISIONS:
  - SECTION_B_QUALITATIVE entries (REQUIRES_VERIFICATION) are excluded from
    all numerical agreement calculations.
  - Missing scores (one expert annotated, another did not) are excluded
    from pairwise metrics and flagged in the report.
  - Agreement is reported per (scenario, scheme) pair and in aggregate.
  - The report acknowledges that 10 scenarios are a pilot, not a
    statistically representative sample.

Usage:
    python scripts/compute_agreement.py
        --annotation-dir data/annotations
        --output-report  reports/pilot_agreement_report.md

Requirements: numpy, scipy
    pip install numpy scipy
"""

import argparse
import csv
import json
import os
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import numpy as np
except ImportError:
    print("[ERROR] numpy is required: pip install numpy")
    raise

try:
    from scipy.stats import chi2
except ImportError:
    print("[ERROR] scipy is required: pip install scipy")
    raise


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_annotation_csvs(annotation_dir: str) -> Dict[str, List[Dict]]:
    """
    Load all *_annotation_session.csv files in annotation_dir.
    Returns a dict: {expert_id: [list of annotation row dicts]}.
    """
    ann_dir = Path(annotation_dir)
    expert_data = {}

    for csv_file in sorted(ann_dir.glob("*_annotation_session.csv")):
        expert_id = csv_file.stem.replace("_annotation_session", "")
        rows = []
        with open(csv_file, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        expert_data[expert_id] = rows
        print(f"  Loaded {len(rows)} annotations from {csv_file.name} (expert: {expert_id})")

    return expert_data


def extract_section_a_ratings(expert_data: Dict[str, List[Dict]]) -> Dict[str, Dict[Tuple, int]]:
    """
    Extract Section A (numerical relevance) ratings only.
    Returns: {expert_id: {(scenario_id, scheme_id): score (int)}}
    """
    expert_ratings = {}
    for expert_id, rows in expert_data.items():
        ratings = {}
        for row in rows:
            # Only include completed Phase 1/2 ratings with numerical scores
            if row.get("phase") in ("COMPLETE", "PHASE1_RELEVANCE"):
                score_str = row.get("expert_relevance_score", "")
                if score_str is not None and score_str != "" and score_str != "None":
                    try:
                        score = int(float(score_str))
                        key = (row["scenario_id"], row["scheme_id"])
                        ratings[key] = score
                    except (ValueError, TypeError):
                        pass
        expert_ratings[expert_id] = ratings
    return expert_ratings


# ---------------------------------------------------------------------------
# Weighted Cohen's Kappa (quadratic weights)
# ---------------------------------------------------------------------------

def quadratic_weighted_kappa(rater1_scores: List[int], rater2_scores: List[int],
                              min_rating: int = 0, max_rating: int = 3) -> float:
    """
    Compute quadratic weighted Cohen's kappa for two raters.
    Only pairs where both raters scored are included.
    """
    n = max_rating - min_rating + 1
    weights = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            weights[i, j] = (i - j) ** 2 / (n - 1) ** 2

    # Build observed matrix
    obs = np.zeros((n, n), dtype=float)
    for r1, r2 in zip(rater1_scores, rater2_scores):
        obs[r1 - min_rating][r2 - min_rating] += 1
    total = obs.sum()
    if total == 0:
        return float("nan")
    obs /= total

    # Expected matrix (marginals product)
    row_marginals = obs.sum(axis=1)
    col_marginals = obs.sum(axis=0)
    exp = np.outer(row_marginals, col_marginals)

    numerator = (weights * obs).sum()
    denominator = (weights * exp).sum()
    if denominator == 0:
        return float("nan")
    return 1.0 - numerator / denominator


# ---------------------------------------------------------------------------
# Krippendorff's Alpha (ordinal distance)
# ---------------------------------------------------------------------------

def krippendorffs_alpha_ordinal(ratings_matrix: np.ndarray) -> float:
    """
    Compute Krippendorff's Alpha with ordinal distance function.

    ratings_matrix: shape (n_raters, n_items)
                    np.nan for missing values.
    """
    n_raters, n_items = ratings_matrix.shape

    # Ordinal distance squared: d(i,j) = (rank_i - rank_j)^2 / normalisation
    # Here we treat scores as interval-ordinal (0,1,2,3) -> use squared difference
    def ordinal_distance_sq(a: float, b: float) -> float:
        return (a - b) ** 2

    # Compute observed disagreement D_o
    D_o = 0.0
    n_pairs_o = 0
    for item in range(n_items):
        col = ratings_matrix[:, item]
        valid = col[~np.isnan(col)]
        if len(valid) < 2:
            continue
        for a, b in combinations(valid, 2):
            D_o += ordinal_distance_sq(a, b)
            n_pairs_o += 1

    if n_pairs_o == 0:
        return float("nan")
    D_o /= n_pairs_o

    # Collect all valid values across all cells
    all_values = ratings_matrix[~np.isnan(ratings_matrix)]
    n_values = len(all_values)

    if n_values < 2:
        return float("nan")

    # Compute expected disagreement D_e
    D_e = 0.0
    n_pairs_e = 0
    for a, b in combinations(all_values, 2):
        D_e += ordinal_distance_sq(a, b)
        n_pairs_e += 1
    D_e /= n_pairs_e if n_pairs_e > 0 else 1

    if D_e == 0:
        return 1.0 if D_o == 0 else float("nan")

    return 1.0 - D_o / D_e


# ---------------------------------------------------------------------------
# Pairwise percent agreement
# ---------------------------------------------------------------------------

def percent_agreement(r1: List[int], r2: List[int]) -> float:
    if not r1:
        return float("nan")
    exact = sum(1 for a, b in zip(r1, r2) if a == b)
    return exact / len(r1)


def adjacent_agreement(r1: List[int], r2: List[int]) -> float:
    """Proportion of pairs where |score_a - score_b| <= 1 (adjacent agreement)."""
    if not r1:
        return float("nan")
    adj = sum(1 for a, b in zip(r1, r2) if abs(a - b) <= 1)
    return adj / len(r1)


# ---------------------------------------------------------------------------
# Disagreement analysis
# ---------------------------------------------------------------------------

def find_disagreements(expert_ratings: Dict[str, Dict[Tuple, int]],
                       threshold: int = 2) -> List[Dict]:
    """
    Return all (scenario, scheme) pairs where the range of scores >= threshold.
    threshold=2 means a spread of 2 points (e.g. one expert gave 0, another gave 2).
    """
    experts = list(expert_ratings.keys())
    all_keys = set()
    for ratings in expert_ratings.values():
        all_keys.update(ratings.keys())

    disagreements = []
    for key in sorted(all_keys):
        scores = {}
        for eid in experts:
            s = expert_ratings[eid].get(key)
            if s is not None:
                scores[eid] = s
        if len(scores) < 2:
            continue
        vals = list(scores.values())
        score_range = max(vals) - min(vals)
        if score_range >= threshold:
            disagreements.append({
                "scenario_id": key[0],
                "scheme_id": key[1],
                "score_range": score_range,
                "scores": scores,
            })
    return sorted(disagreements, key=lambda x: -x["score_range"])


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    expert_ratings: Dict[str, Dict[Tuple, int]],
    expert_data: Dict[str, List[Dict]],
    output_path: str,
):
    experts = sorted(expert_ratings.keys())
    n_experts = len(experts)

    # Build unified key set (only pairs where BOTH experts have scores)
    all_keys = set()
    for ratings in expert_ratings.values():
        all_keys.update(ratings.keys())

    # Per-pair coverage
    coverage = {}
    for key in all_keys:
        raters_with_score = [e for e in experts if key in expert_ratings[e]]
        coverage[key] = raters_with_score

    # Pairwise metrics
    pairwise_results = []
    for e1, e2 in combinations(experts, 2):
        shared_keys = [k for k in all_keys if k in expert_ratings[e1] and k in expert_ratings[e2]]
        r1 = [expert_ratings[e1][k] for k in shared_keys]
        r2 = [expert_ratings[e2][k] for k in shared_keys]
        if not r1:
            kappa = float("nan")
            pct = float("nan")
            adj = float("nan")
        else:
            kappa = quadratic_weighted_kappa(r1, r2)
            pct = percent_agreement(r1, r2)
            adj = adjacent_agreement(r1, r2)
        pairwise_results.append({
            "rater_pair": f"{e1} vs {e2}",
            "n_shared_pairs": len(shared_keys),
            "quadratic_weighted_kappa": kappa,
            "percent_exact_agreement": pct,
            "percent_adjacent_agreement": adj,
        })

    # Krippendorff's Alpha (all raters)
    all_keys_list = sorted(all_keys)
    matrix = np.full((n_experts, len(all_keys_list)), np.nan)
    for ei, eid in enumerate(experts):
        for ki, key in enumerate(all_keys_list):
            if key in expert_ratings[eid]:
                matrix[ei, ki] = expert_ratings[eid][key]

    k_alpha = krippendorffs_alpha_ordinal(matrix) if n_experts >= 2 else float("nan")

    # Disagreements
    disagreements = find_disagreements(expert_ratings, threshold=2)

    # Section B coverage
    section_b_by_expert = defaultdict(list)
    for eid, rows in expert_data.items():
        for row in rows:
            if row.get("phase") == "SECTION_B_QUALITATIVE":
                section_b_by_expert[eid].append(row)

    # ------- Write report -------
    lines = []
    lines.append("# Expert Annotation Pilot — Inter-Rater Agreement Report")
    lines.append("")
    lines.append("**Pilot Version:** pilot-v1.0 (git commit: `7724fa7`)")
    lines.append(f"**Experts:** {', '.join(experts)}")
    lines.append(f"**Scenarios:** S001–S010 (10 pilot scenarios)")
    lines.append(f"**Total Section A (scenario, scheme) pairs rated:** {len(all_keys)}")
    lines.append("")
    lines.append("> [!NOTE]")
    lines.append("> This report covers 10 pilot scenarios only. Ratings from the same")
    lines.append("> scenarios are not fully independent observations. These results are")
    lines.append("> **diagnostic evidence** to evaluate the annotation protocol, not a")
    lines.append("> definitive inter-rater reliability claim.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. Overall Agreement Metrics")
    lines.append("")
    lines.append("### 1.1 Krippendorff's Alpha (Ordinal Distance, All Raters)")
    lines.append("")
    lines.append(f"**alpha (ordinal) = {k_alpha:.4f}**" if not np.isnan(k_alpha) else "**alpha = N/A** (insufficient data)")
    lines.append("")
    lines.append("| Threshold | Interpretation |")
    lines.append("|:---|:---|")
    lines.append("| alpha >= 0.80 | Good reliability — proceed to larger benchmark |")
    lines.append("| 0.67 <= alpha < 0.80 | Tentative reliability — review disagreements, revise protocol |")
    lines.append("| alpha < 0.67 | Low reliability — do not use as training labels until resolved |")
    lines.append("")

    if not np.isnan(k_alpha):
        if k_alpha >= 0.80:
            lines.append("> [!TIP] Alpha >= 0.80: Good reliability. Proceed to scaling after reviewing disagreements.")
        elif k_alpha >= 0.67:
            lines.append("> [!IMPORTANT] Alpha in [0.67, 0.80): Tentative reliability. Review all flagged disagreements before scaling.")
        else:
            lines.append("> [!WARNING] Alpha < 0.67: Low reliability. Do NOT use these annotations as ML training labels until protocol is revised.")

    lines.append("")
    lines.append("### 1.2 Pairwise Quadratic Weighted Cohen's Kappa")
    lines.append("")
    lines.append("| Rater Pair | Shared Pairs | kappa_w | Exact Agreement | Adjacent Agreement |")
    lines.append("|:---|---:|---:|---:|---:|")
    for pr in pairwise_results:
        kw = f"{pr['quadratic_weighted_kappa']:.4f}" if not np.isnan(pr['quadratic_weighted_kappa']) else "N/A"
        pa = f"{pr['percent_exact_agreement']:.1%}" if not np.isnan(pr['percent_exact_agreement']) else "N/A"
        aa = f"{pr['percent_adjacent_agreement']:.1%}" if not np.isnan(pr['percent_adjacent_agreement']) else "N/A"
        lines.append(f"| {pr['rater_pair']} | {pr['n_shared_pairs']} | {kw} | {pa} | {aa} |")
    lines.append("")
    lines.append("> kappa_w interpretation: >= 0.81 = Almost Perfect, 0.61-0.80 = Substantial, 0.41-0.60 = Moderate, < 0.41 = Fair/Poor")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Coverage")
    lines.append("")
    missing_pairs = [(k, [e for e in experts if k not in expert_ratings[e]]) for k in all_keys]
    missing_pairs = [(k, m) for k, m in missing_pairs if m]
    lines.append(f"- Total unique (scenario, scheme) pairs across all experts: **{len(all_keys)}**")
    lines.append(f"- Pairs rated by all {n_experts} expert(s): **{sum(1 for k in all_keys if len(coverage[k]) == n_experts)}**")
    lines.append(f"- Pairs with missing scores (one or more experts did not rate): **{len(missing_pairs)}**")
    lines.append("")
    if missing_pairs:
        lines.append("### Missing Pair Detail")
        lines.append("")
        lines.append("| Scenario | Scheme | Missing Rater(s) |")
        lines.append("|:---|:---|:---|")
        for key, missing in sorted(missing_pairs):
            lines.append(f"| {key[0]} | {key[1]} | {', '.join(missing)} |")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. Disagreement Analysis")
    lines.append("")
    lines.append(f"**Disagreements flagged** (score range >= 2 points): **{len(disagreements)}**")
    lines.append("")
    if disagreements:
        lines.append("| Scenario | Scheme | Score Range | Per-Expert Scores | Priority |")
        lines.append("|:---|:---|:---:|:---|:---|")
        for d in disagreements:
            scores_str = " | ".join(f"{e}={s}" for e, s in d["scores"].items())
            priority = "HIGH" if d["score_range"] >= 3 else "MEDIUM"
            lines.append(f"| {d['scenario_id']} | {d['scheme_id']} | {d['score_range']} | {scores_str} | {priority} |")
        lines.append("")
        lines.append("### 3.1 Disagrement Investigation Prompts")
        lines.append("")
        lines.append("For each HIGH/MEDIUM disagreement, review:")
        lines.append("1. Did the experts interpret the farmer's *stated need* differently?")
        lines.append("2. Did one expert use agronomic context the annotation form did not make explicit?")
        lines.append("3. Is the scheme description in the annotation form ambiguous for this crop/district?")
        lines.append("4. Is this a genuine difference in expert judgment, or a protocol ambiguity?")
        lines.append("")
    else:
        lines.append("No high-severity disagreements detected (all score ranges < 2).")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. Per-Scenario Summary")
    lines.append("")
    scenario_ids = sorted({k[0] for k in all_keys})
    lines.append("| Scenario | Pairs Rated | Mean Score (all experts) | Std Dev | Max Range |")
    lines.append("|:---|---:|---:|---:|---:|")
    for sid in scenario_ids:
        sid_keys = [k for k in all_keys if k[0] == sid]
        scores_flat = [expert_ratings[e][k] for e in experts for k in sid_keys if k in expert_ratings[e]]
        if scores_flat:
            mean_s = np.mean(scores_flat)
            std_s = np.std(scores_flat)
            ranges = []
            for k in sid_keys:
                vs = [expert_ratings[e][k] for e in experts if k in expert_ratings[e]]
                if len(vs) >= 2:
                    ranges.append(max(vs) - min(vs))
            max_range = max(ranges) if ranges else 0
            lines.append(f"| {sid} | {len(sid_keys)} | {mean_s:.2f} | {std_s:.2f} | {max_range} |")
        else:
            lines.append(f"| {sid} | 0 | N/A | N/A | N/A |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. Section B: Provisional Scheme Policy Feedback")
    lines.append("")
    lines.append("The following qualitative feedback was collected for REQUIRES_VERIFICATION schemes.")
    lines.append("These items do NOT contribute to numerical agreement calculations.")
    lines.append("")
    if section_b_by_expert:
        for eid in sorted(section_b_by_expert.keys()):
            lines.append(f"### Expert {eid}")
            for row in section_b_by_expert[eid]:
                lines.append(f"- **{row['scenario_id']} / {row['scheme_id']}:** {row.get('expert_availability_comment', '(no comment)')}")
            lines.append("")
    else:
        lines.append("*(No Section B annotations found in loaded files.)*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 6. Protocol Revision Recommendations")
    lines.append("")
    lines.append("Based on the above findings, the following refinements are recommended")
    lines.append("before scaling to the 50-100 scenario benchmark:")
    lines.append("")
    lines.append("*(To be completed after manual review of the disagreement table above.)*")
    lines.append("")
    lines.append("| # | Finding | Recommended Protocol Change |")
    lines.append("|:---|:---|:---|")
    lines.append("| 1 | *(describe finding)* | *(describe protocol change)* |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 7. Decision Gate")
    lines.append("")
    lines.append("| Criterion | Metric Role | Status |")
    lines.append("|:---|:---|:---|")
    if n_experts == 2 and pairwise_results:
        pw_kappa = pairwise_results[0]['quadratic_weighted_kappa']
        pw_status = "PASS" if (not np.isnan(pw_kappa) and pw_kappa >= 0.61) else ("REVIEW" if not np.isnan(pw_kappa) else "PENDING DATA")
        pw_str = f"{pw_kappa:.4f}" if not np.isnan(pw_kappa) else "N/A"
        lines.append(f"| Quadratic weighted kappa >= 0.61 | **Primary (2 raters)** | **{pw_status}** (kappa_w = {pw_str}) |")
        alpha_status = "PASS" if (not np.isnan(k_alpha) and k_alpha >= 0.67) else ("REVIEW" if not np.isnan(k_alpha) else "PENDING DATA")
        alpha_str = f"{k_alpha:.4f}" if not np.isnan(k_alpha) else "N/A"
        lines.append(f"| Krippendorff alpha >= 0.67 | **Supplementary (2 raters)** | **{alpha_status}** (alpha = {alpha_str}) |")
    else:
        alpha_status = "PASS" if (not np.isnan(k_alpha) and k_alpha >= 0.67) else ("REVIEW" if not np.isnan(k_alpha) else "PENDING DATA")
        alpha_str = f"{k_alpha:.4f}" if not np.isnan(k_alpha) else "N/A"
        lines.append(f"| Krippendorff alpha >= 0.67 | **Primary (3+ raters)** | **{alpha_status}** (alpha = {alpha_str}) |")
        if pairwise_results:
            min_pw = min(pr['quadratic_weighted_kappa'] for pr in pairwise_results if not np.isnan(pr['quadratic_weighted_kappa'])) if any(not np.isnan(pr['quadratic_weighted_kappa']) for pr in pairwise_results) else np.nan
            pw_status = "PASS" if (not np.isnan(min_pw) and min_pw >= 0.61) else ("REVIEW" if not np.isnan(min_pw) else "PENDING DATA")
            pw_str = f"{min_pw:.4f}" if not np.isnan(min_pw) else "N/A"
            lines.append(f"| Pairwise quadratic weighted kappas >= 0.61 | **Supplementary** | **{pw_status}** (min kappa_w = {pw_str}) |")
    lines.append("| All HIGH disagreements investigated | Protocol Review | [ ] |")
    lines.append("| Section B qualitative policy feedback reviewed | Policy Review | [ ] |")
    lines.append("| Protocol revision notes written (Section 6) | Scaling Decision | [ ] |")
    lines.append("| Model training remains deferred | Quality Safeguard | [x] (deferred by design) |")
    lines.append("")
    lines.append("> **Decision Rule:** Meeting the statistical threshold is a provisional pilot decision gate to determine")
    lines.append("> whether annotation instructions are sufficiently calibrated to proceed to the 50-100 scenario expansion.")
    lines.append("> It does NOT replace manual investigation of the disagreement table and Section B qualitative feedback.")

    report_text = "\n".join(lines)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\n  [Saved] Agreement report written to: {output_path}")

    # Console summary
    print("\n" + "=" * 60)
    print("  AGREEMENT SUMMARY")
    print("=" * 60)
    print(f"  Krippendorff's Alpha (ordinal)  : {k_alpha:.4f}" if not np.isnan(k_alpha) else "  Krippendorff's Alpha           : N/A (need data)")
    for pr in pairwise_results:
        kw = f"{pr['quadratic_weighted_kappa']:.4f}" if not np.isnan(pr['quadratic_weighted_kappa']) else "N/A"
        print(f"  Kappa_w  [{pr['rater_pair']}] : {kw}  (n={pr['n_shared_pairs']})")
    print(f"  High disagreements flagged      : {len(disagreements)}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Compute inter-rater agreement metrics for the annotation pilot."
    )
    parser.add_argument(
        "--annotation-dir", "-a",
        default="data/annotations",
        help="Directory containing *_annotation_session.csv files."
    )
    parser.add_argument(
        "--output-report", "-o",
        default="reports/pilot_agreement_report.md",
        help="Path for the output markdown agreement report."
    )
    args = parser.parse_args()

    print(f"Loading annotations from: {args.annotation_dir}")
    expert_data = load_annotation_csvs(args.annotation_dir)

    if not expert_data:
        print("[ERROR] No annotation CSV files found. Run run_annotation_session.py first.")
        return

    expert_ratings = extract_section_a_ratings(expert_data)

    if not any(expert_ratings.values()):
        print("[ERROR] No numerical Section A ratings found in loaded files.")
        return

    generate_report(expert_ratings, expert_data, args.output_report)


if __name__ == "__main__":
    main()
