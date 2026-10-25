"""
compute_benchmark_agreement.py
-------------------------------
Benchmark v1.0.4 Expert Inter-Rater Reliability Runner.

Evaluates inter-rater agreement between independent expert raters E1 and E2
across the 60 benchmark scenarios (S011–S070) for all 283 Section A candidate pairs.

METRICS EVALUATED:
  1. Quadratic Weighted Cohen's Kappa (target: kappa_w >= 0.61)
  2. Genuine Ordinal Krippendorff's Alpha (Krippendorff 2004/2011, target: alpha >= 0.67)
     Uses standard cumulative marginal frequency distance:
     delta^2(g, h) = ( sum_{k=g}^h n_k - (n_g + n_h)/2 )^2
  3. Exact Percent Agreement (diagnostic)
  4. Adjacent Percent Agreement (|E1 - E2| <= 1, diagnostic)
  5. Disagreement Worksheet Extraction (|E1 - E2| >= 2, mandatory adjudication)

INPUTS SUPPORTED:
  - Paired pre-adjudication CSV (produced by ingest_benchmark_annotations.py)
  - Separate E1 and E2 submission files (paired automatically)
"""

import argparse
import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PAIRED_FILE = REPO_ROOT / "data/annotations/benchmark_v1.0.4/paired_annotations_pre_adjudication.csv"
DEFAULT_REPORT_FILE = REPO_ROOT / "reports/benchmark_v1.0.4_agreement_report.md"
TEMPLATE_FILE = REPO_ROOT / "data/annotations/benchmark_v1.0.4/E1_annotation_packet_blank.csv"

# Pre-registered agreement thresholds
TARGET_KAPPA_QUADRATIC = 0.61
TARGET_ORDINAL_ALPHA = 0.67


def compute_quadratic_weighted_kappa(
    rater1_scores: List[int],
    rater2_scores: List[int],
    min_rating: int = 0,
    max_rating: int = 3
) -> float:
    """
    Computes quadratic weighted Cohen's Kappa for two raters on an ordinal scale [0, 3].
    Weights w_{i,j} = (i - j)^2 / (max_rating - min_rating)^2.
    """
    if len(rater1_scores) != len(rater2_scores):
        raise ValueError("Score sequences must have identical lengths.")
    if len(rater1_scores) == 0:
        return float("nan")

    n_categories = max_rating - min_rating + 1
    weights = np.zeros((n_categories, n_categories), dtype=float)
    denom_w = float(n_categories - 1) ** 2
    for i in range(n_categories):
        for j in range(n_categories):
            weights[i, j] = ((i - j) ** 2) / denom_w

    obs = np.zeros((n_categories, n_categories), dtype=float)
    for r1, r2 in zip(rater1_scores, rater2_scores):
        obs[r1 - min_rating, r2 - min_rating] += 1.0

    total = obs.sum()
    if total == 0:
        return float("nan")
    obs /= total

    row_marginals = obs.sum(axis=1)
    col_marginals = obs.sum(axis=0)
    exp = np.outer(row_marginals, col_marginals)

    observed_disagreement = np.sum(weights * obs)
    expected_disagreement = np.sum(weights * exp)

    if expected_disagreement == 0:
        return 1.0 if observed_disagreement == 0 else float("nan")

    return 1.0 - (observed_disagreement / expected_disagreement)


def compute_ordinal_krippendorff_alpha(ratings_matrix: np.ndarray) -> float:
    """
    Computes genuine Ordinal Krippendorff's Alpha (Krippendorff 2004/2011, CASRAI standard).
    Uses the standard ordinal distance metric based on cumulative frequencies
    of ordered categories in the coincidence matrix:
        delta^2(g, h) = ( sum_{k=g}^h n_k - (n_g + n_h)/2 )^2
    
    ratings_matrix: shape (n_raters, n_items), with np.nan for missing ratings.
    """
    arr = np.asarray(ratings_matrix, dtype=float)
    valid_vals = arr[~np.isnan(arr)]
    if len(valid_vals) == 0:
        return float("nan")

    categories = np.sort(np.unique(valid_vals))
    m = len(categories)
    if m <= 1:
        return 1.0

    cat_to_idx = {c: i for i, c in enumerate(categories)}
    n_raters, n_items = arr.shape
    C = np.zeros((m, m), dtype=float)

    for j in range(n_items):
        col = arr[:, j]
        valid = col[~np.isnan(col)]
        m_u = len(valid)
        if m_u < 2:
            continue
        weight = 1.0 / (m_u - 1)
        for k in range(m_u):
            for l in range(m_u):
                if k != l:
                    ik = cat_to_idx[valid[k]]
                    il = cat_to_idx[valid[l]]
                    C[ik, il] += weight

    n_k = np.sum(C, axis=1)
    n = np.sum(n_k)
    if n <= 1:
        return float("nan")

    delta_sq = np.zeros((m, m), dtype=float)
    for g in range(m):
        for h in range(g + 1, m):
            inner_sum = np.sum(n_k[g : h + 1]) - (n_k[g] + n_k[h]) / 2.0
            d2 = inner_sum ** 2
            delta_sq[g, h] = d2
            delta_sq[h, g] = d2

    observed_disagreement = np.sum(C * delta_sq)
    expected_disagreement = np.sum(np.outer(n_k, n_k) * delta_sq) / (n - 1)

    if expected_disagreement == 0:
        return 1.0 if observed_disagreement == 0 else float("nan")

    return 1.0 - (observed_disagreement / expected_disagreement)


def load_canonical_template_pairs() -> List[Tuple[str, str]]:
    """Loads the canonical (scenario_id, scheme_id) pairs for Benchmark v1.0.4."""
    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError(f"Template file not found: {TEMPLATE_FILE}")
    pairs = []
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            pairs.append((r["scenario_id"], r["scheme_id"]))
    if len(pairs) != 283:
        raise ValueError(f"Expected exactly 283 template pairs, got {len(pairs)}")
    return pairs


def load_paired_annotations_from_csv(csv_path: Path) -> List[Dict[str, Any]]:
    """
    Loads and validates paired benchmark annotations from CSV.
    Validates:
      - Exactly 283 rows
      - Exact match to canonical candidate pairs S011-S070
      - Scores are integers in {0, 1, 2, 3}
      - No pilot scenarios S001-S010
      - Non-empty e1_rationale and e2_rationale (Protocol v1.1 audit trail requirement)
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Paired annotations file not found: {csv_path}")

    canonical_pairs = load_canonical_template_pairs()
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            sid = row.get("scenario_id", "").strip()
            scheme_id = row.get("scheme_id", "").strip()
            
            if not sid or not scheme_id:
                raise ValueError(f"Row {idx} missing scenario_id or scheme_id in {csv_path}")

            # Rejection of pilot scenarios S001-S010
            if sid.startswith("S00") or (sid.startswith("S") and sid[1:].isdigit() and int(sid[1:]) <= 10):
                raise ValueError(
                    f"Pilot scenario {sid} detected in row {idx}. "
                    f"Pilot scenarios S001-S010 must not be included in benchmark reliability evaluation."
                )

            # Rejection of out-of-benchmark scenarios
            if not (sid.startswith("S") and sid[1:].isdigit() and 11 <= int(sid[1:]) <= 70):
                raise ValueError(f"Invalid benchmark scenario ID {sid} in row {idx}. Must be S011-S070.")

            # Validate scores
            try:
                e1_score = int(row["e1_score"])
                e2_score = int(row["e2_score"])
            except (ValueError, KeyError, TypeError) as err:
                raise ValueError(f"Invalid or missing score in row {idx} for {sid}:{scheme_id}: {err}")

            if e1_score not in (0, 1, 2, 3) or e2_score not in (0, 1, 2, 3):
                raise ValueError(
                    f"Scores out of range {0, 1, 2, 3} in row {idx}: E1={e1_score}, E2={e2_score}"
                )

            # Validate rationale presence (Protocol v1.1: audit trail required for every judgment)
            e1_rat = row.get("e1_rationale", "").strip()
            e2_rat = row.get("e2_rationale", "").strip()
            if not e1_rat:
                raise ValueError(
                    f"Missing E1 rationale for row {idx} ({sid}:{scheme_id}). "
                    f"Protocol v1.1 requires an audit rationale for every relevance judgment."
                )
            if not e2_rat:
                raise ValueError(
                    f"Missing E2 rationale for row {idx} ({sid}:{scheme_id}). "
                    f"Protocol v1.1 requires an audit rationale for every relevance judgment."
                )

            rows.append({
                "scenario_id": sid,
                "scheme_id": scheme_id,
                "scheme_name": row.get("scheme_name", "").strip(),
                "e1_score": e1_score,
                "e2_score": e2_score,
                "score_delta": abs(e1_score - e2_score),
                "e1_rationale": e1_rat,
                "e2_rationale": e2_rat
            })

    if len(rows) != 283:
        raise ValueError(f"Expected exactly 283 paired rows, got {len(rows)}")

    submitted_pairs = [(r["scenario_id"], r["scheme_id"]) for r in rows]
    if submitted_pairs != canonical_pairs:
        missing = set(canonical_pairs) - set(submitted_pairs)
        extra = set(submitted_pairs) - set(canonical_pairs)
        raise ValueError(
            f"Candidate scheme pairs mismatch canonical Benchmark v1.0.4 template. "
            f"Missing: {len(missing)}, Extra: {len(extra)}"
        )

    return rows


def evaluate_benchmark_agreement(paired_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes comprehensive agreement statistics on validated paired benchmark ratings.
    """
    if len(paired_rows) != 283:
        raise ValueError(f"Expected 283 paired rows for Benchmark v1.0.4, got {len(paired_rows)}")

    e1_scores = [r["e1_score"] for r in paired_rows]
    e2_scores = [r["e2_score"] for r in paired_rows]

    # Quadratic Weighted Cohen's Kappa
    kappa_w = compute_quadratic_weighted_kappa(e1_scores, e2_scores, min_rating=0, max_rating=3)

    # Genuine Ordinal Krippendorff's Alpha
    ratings_matrix = np.array([e1_scores, e2_scores], dtype=float)
    alpha_ord = compute_ordinal_krippendorff_alpha(ratings_matrix)

    # Percent agreements
    exact_count = sum(1 for r in paired_rows if r["score_delta"] == 0)
    adjacent_count = sum(1 for r in paired_rows if r["score_delta"] <= 1)
    disagreements = [r for r in paired_rows if r["score_delta"] >= 2]

    exact_pct = exact_count / len(paired_rows)
    adjacent_pct = adjacent_count / len(paired_rows)

    kappa_passed = bool(kappa_w >= TARGET_KAPPA_QUADRATIC)
    alpha_passed = bool(alpha_ord >= TARGET_ORDINAL_ALPHA)
    reliability_passed = kappa_passed and alpha_passed

    # Distribution of ratings
    e1_dist = {s: e1_scores.count(s) for s in range(4)}
    e2_dist = {s: e2_scores.count(s) for s in range(4)}

    # Delta distribution
    delta_dist = {d: sum(1 for r in paired_rows if r["score_delta"] == d) for d in range(4)}

    return {
        "benchmark_version": "v1.0.4",
        "scenario_scope": "S011-S070",
        "total_pairs": len(paired_rows),
        "scenarios_covered": len(set(r["scenario_id"] for r in paired_rows)),
        "quadratic_weighted_kappa": kappa_w,
        "ordinal_krippendorff_alpha": alpha_ord,
        "exact_agreement_pct": exact_pct,
        "adjacent_agreement_pct": adjacent_pct,
        "kappa_passed": kappa_passed,
        "alpha_passed": alpha_passed,
        "reliability_passed": reliability_passed,
        "disagreements_count": len(disagreements),
        "disagreements": disagreements,
        "e1_distribution": e1_dist,
        "e2_distribution": e2_dist,
        "delta_distribution": delta_dist
    }


def generate_markdown_report(metrics: Dict[str, Any], output_path: Path) -> str:
    """Generates a structured, audit-ready Markdown report for Benchmark v1.0.4."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    passed_str = "PASS" if metrics["reliability_passed"] else "FAIL / REQUIRES_ADJUDICATION"

    lines = [
        "# Benchmark v1.0.4 Expert Inter-Rater Reliability Report",
        "",
        f"**Generated:** {ts}  ",
        f"**Benchmark Scope:** {metrics['scenario_scope']} (60 Scenarios, 10 Agro-Climatic Zones)  ",
        f"**Candidate Items Analyzed:** {metrics['total_pairs']} Section A Schemes (100% Coverage)  ",
        f"**Reliability Gate Status:** **{passed_str}**",
        "",
        "---",
        "",
        "## 1. Reliability Gate Summary",
        "",
        "| Metric | Observed Value | Pre-Registered Threshold | Status |",
        "| :--- | :---: | :---: | :---: |",
    ]
    status_kappa = "✅ PASS" if metrics["kappa_passed"] else "❌ FAIL"
    status_alpha = "✅ PASS" if metrics["alpha_passed"] else "❌ FAIL"
    status_dis = "⚠️ PENDING ADJUDICATION" if metrics["disagreements_count"] > 0 else "✅ ZERO"
    
    lines.append(f"| **Quadratic Weighted Cohen's Kappa (kappa_w)** | `{metrics['quadratic_weighted_kappa']:.4f}` | >= 0.61 | {status_kappa} |")
    lines.append(f"| **Ordinal Krippendorff's Alpha (alpha_ord)** | `{metrics['ordinal_krippendorff_alpha']:.4f}` | >= 0.67 | {status_alpha} |")
    lines.append(f"| **Exact Agreement** | `{metrics['exact_agreement_pct'] * 100:.2f}%` | Diagnostic | Informational |")
    lines.append(f"| **Adjacent Agreement (|Delta| <= 1)** | `{metrics['adjacent_agreement_pct'] * 100:.2f}%` | Diagnostic | Informational |")
    lines.append(f"| **Disagreements Requiring Adjudication (|Delta| >= 2)** | `{metrics['disagreements_count']}` | 0 unadjudicated | {status_dis} |")

    lines.extend([
        "",
        "---",
        "",
        "## 2. Rating Distributions",
        "",
        "### Score Marginal Frequencies (0–3 Scale)",
        "| Score | E1 Count | E1 Pct | E2 Count | E2 Pct |",
        "| :---: | :---: | :---: | :---: | :---: |"
    ])

    total = metrics["total_pairs"]
    for s in range(4):
        c1 = metrics["e1_distribution"][s]
        c2 = metrics["e2_distribution"][s]
        lines.append(f"| Score {s} | {c1} | {c1 / total * 100:.1f}% | {c2} | {c2 / total * 100:.1f}% |")

    lines.extend([
        "",
        "### Score Difference (|E1 - E2|) Distribution",
        "| Difference ($|\\Delta|$) | Pair Count | Percentage | Operational Meaning |",
        "| :---: | :---: | :---: | :--- |",
        f"| 0 | {metrics['delta_distribution'][0]} | {metrics['delta_distribution'][0] / total * 100:.1f}% | Exact consensus |",
        f"| 1 | {metrics['delta_distribution'][1]} | {metrics['delta_distribution'][1] / total * 100:.1f}% | Minor boundary variance (e.g. 1 vs 2) |",
        f"| 2 | {metrics['delta_distribution'][2]} | {metrics['delta_distribution'][2] / total * 100:.1f}% | Clinical divergence (Mandatory Adjudication) |",
        f"| 3 | {metrics['delta_distribution'][3]} | {metrics['delta_distribution'][3] / total * 100:.1f}% | Polar divergence (Mandatory Adjudication) |",
        "",
        "---",
        "",
        "## 3. Disagreement Inventory (|E1 - E2| >= 2)",
        ""
    ])

    if metrics["disagreements_count"] == 0:
        lines.append("No clinical disagreements (|E1 - E2| >= 2) observed. All 283 candidate ratings are within adjacent range.")
    else:
        lines.extend([
            f"Found {metrics['disagreements_count']} items with divergent clinical relevance assessments.",
            "These items must be resolved via the pre-registered adjudication protocol before consensus ground truth is frozen.",
            "",
            "| Scenario | Scheme ID | Scheme Name | E1 | E2 | Delta | E1 Rationale | E2 Rationale |",
            "| :---: | :---: | :--- | :---: | :---: | :---: | :--- | :--- |"
        ])
        for d in metrics["disagreements"]:
            e1_rat = d['e1_rationale'].replace("|", "\\|")
            e2_rat = d['e2_rationale'].replace("|", "\\|")
            lines.append(
                f"| {d['scenario_id']} | {d['scheme_id']} | {d['scheme_name']} | "
                f"{d['e1_score']} | {d['e2_score']} | {d['score_delta']} | "
                f"{e1_rat} | {e2_rat} |"
            )

    lines.extend([
        "",
        "---",
        "",
        "## 4. Methodological & Pre-Registration Safeguards",
        "1. **Distance Function**: Genuine Ordinal Krippendorff Alpha utilizes cumulative marginal frequencies $\\delta^2(g, h) = (\\sum_{k=g}^h n_k - \\frac{n_g + n_h}{2})^2$ instead of interval distance.",
        "2. **Permanent Calibration Isolation**: Pilot scenarios S001–S010 are strictly excluded from all Benchmark v1.0.4 reliability gates.",
        "3. **Section B Separation**: Section B policy review schemes are entirely excluded from numerical relevance scoring.",
        "4. **Fail-Closed Thresholds**: If either $\\kappa_w < 0.61$ or $\\alpha_{\\text{ord}} < 0.67$, downstream baseline ranking evaluation remains blocked until resolved.",
        ""
    ])

    report_content = "\n".join(lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    return report_content


def main():
    parser = argparse.ArgumentParser(description="Benchmark v1.0.4 Inter-Rater Reliability Runner")
    parser.add_argument(
        "--input-csv",
        type=Path,
        default=DEFAULT_PAIRED_FILE,
        help="Path to paired_annotations_pre_adjudication.csv"
    )
    parser.add_argument(
        "--output-report",
        type=Path,
        default=DEFAULT_REPORT_FILE,
        help="Path to output markdown report"
    )
    args = parser.parse_args()

    print(f"[RELIABILITY] Loading paired annotations: {args.input_csv}")
    paired_rows = load_paired_annotations_from_csv(args.input_csv)
    print(f"[VALIDATED] Loaded {len(paired_rows)} candidate pairs across S011-S070.")

    metrics = evaluate_benchmark_agreement(paired_rows)
    print(f"[METRICS] Quadratic Weighted Kappa: {metrics['quadratic_weighted_kappa']:.4f} (Target >= {TARGET_KAPPA_QUADRATIC})")
    print(f"[METRICS] Ordinal Krippendorff Alpha: {metrics['ordinal_krippendorff_alpha']:.4f} (Target >= {TARGET_ORDINAL_ALPHA})")
    print(f"[METRICS] Exact Agreement: {metrics['exact_agreement_pct']*100:.2f}% | Adjacent Agreement: {metrics['adjacent_agreement_pct']*100:.2f}%")
    print(f"[METRICS] Items Requiring Adjudication (|E1-E2| >= 2): {metrics['disagreements_count']}")

    generate_markdown_report(metrics, args.output_report)
    print(f"[REPORT] Saved Benchmark reliability report to {args.output_report}")

    if not metrics["reliability_passed"]:
        print("[WARNING] Benchmark inter-rater reliability did not achieve pre-registered acceptance thresholds.")
        sys.exit(1)
    else:
        print("[SUCCESS] All Benchmark v1.0.4 inter-rater reliability gates passed.")


if __name__ == "__main__":
    main()
