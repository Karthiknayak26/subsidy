#!/usr/bin/env python3
"""Benchmark v1.1 annotation validation + inter-rater agreement pipeline.

Standalone (pandas + numpy only). Implements the protocol in
benchmark_v1.1_calibration_rubric.md:
  * context-completeness validation (fails closed)
  * template / submission / candidate-pair validation
  * Section B numeric-score rejection
  * |E1-E2| >= 2 escalation list
  * quadratic weighted Cohen's kappa and ordinal Krippendorff's alpha on the
    ORIGINAL independent ratings (never adjudicated scores)
  * consensus ledger written separately, never into a raw/ directory

Thresholds are the preregistered values and are not configurable via CLI.
This script never generates ratings.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# ---- Preregistered constants (do not alter) --------------------------------
KAPPA_W_THRESHOLD = 0.610
ALPHA_ORD_THRESHOLD = 0.670
SCORE_LEVELS = (0, 1, 2, 3)
ESCALATION_DELTA = 2

TEMPLATE_COLUMNS = [
    "scenario_id", "scheme_id", "scheme_name", "rater_id",
    "relevance_score", "relevance_rationale", "complementarity_notes",
]
# Context the rubric needs a reviewer to have (income is optional: "where recorded").
SCENARIO_REQUIRED = [
    "scenario_id", "zone", "district", "primary_crop", "land_size", "land_type",
    "social_category", "farmer_category", "water_access", "electricity_access",
    "immediate_need", "primary_acute_crisis", "secondary_constraints", "urgency",
]
SCENARIO_OPTIONAL = ["annual_family_income", "timing_notes", "statutory_flags", "other_constraints"]
SCHEME_REQUIRED = [
    "scheme_id", "scheme_name", "purpose", "intervention",
    "eligibility_requirements", "assistance_type", "source_references",
]
# Anything that leaks model/heuristic/label information to annotators.
FORBIDDEN_CONTEXT_COLUMNS = [
    "model_score", "model_prediction", "heuristic_rank", "rank", "prior_label",
    "prior_relevance", "relevance_score", "ai_rationale", "consensus_label",
]


class ValidationReport:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors

    def merge(self, other: "ValidationReport") -> None:
        self.errors += other.errors
        self.warnings += other.warnings


def _blank(series: pd.Series) -> pd.Series:
    return series.isna() | (series.astype(str).str.strip() == "")


# ---- Context completeness --------------------------------------------------
def validate_context(scenarios: pd.DataFrame, schemes: pd.DataFrame,
                     packet: pd.DataFrame) -> ValidationReport:
    r = ValidationReport()
    for name, df, req in (("scenario dossier", scenarios, SCENARIO_REQUIRED),
                          ("scheme evidence", schemes, SCHEME_REQUIRED)):
        missing = [c for c in req if c not in df.columns]
        if missing:
            r.err(f"{name}: missing required columns {missing}")
            continue
        for c in req:
            n = int(_blank(df[c]).sum())
            if n:
                r.err(f"{name}: column '{c}' blank in {n} row(s)")
        leaked = [c for c in FORBIDDEN_CONTEXT_COLUMNS if c in df.columns]
        if leaked:
            r.err(f"{name}: contains forbidden label/model columns {leaked}")
    if "scenario_id" in scenarios.columns and scenarios["scenario_id"].duplicated().any():
        r.err("scenario dossier: duplicate scenario_id rows")
    if "scheme_id" in schemes.columns and schemes["scheme_id"].duplicated().any():
        r.err("scheme evidence: duplicate scheme_id rows")
    if "scenario_id" in scenarios.columns:
        gap = set(packet["scenario_id"]) - set(scenarios["scenario_id"])
        if gap:
            r.err(f"packet scenarios with no dossier row: {sorted(gap)[:10]}")
    if "scheme_id" in schemes.columns:
        gap = set(packet["scheme_id"]) - set(schemes["scheme_id"])
        if gap:
            r.err(f"packet schemes with no evidence row: {sorted(gap)}")
    return r


# ---- Template / submission validation --------------------------------------
def validate_columns(df: pd.DataFrame, label: str) -> ValidationReport:
    r = ValidationReport()
    if list(df.columns) != TEMPLATE_COLUMNS:
        r.err(f"{label}: columns {list(df.columns)} != required {TEMPLATE_COLUMNS}")
    return r


def validate_template(df: pd.DataFrame, rater: str) -> ValidationReport:
    """A blank template: correct columns, rater_id, empty scoring fields, no duplicates."""
    r = validate_columns(df, f"{rater} template")
    if not r.ok:
        return r
    if (df["rater_id"] != rater).any():
        r.err(f"{rater} template: rater_id not uniformly '{rater}'")
    for c in ("relevance_score", "relevance_rationale", "complementarity_notes"):
        if not _blank(df[c]).all():
            r.err(f"{rater} template: '{c}' is not blank")
    if df.duplicated(["scenario_id", "scheme_id"]).any():
        r.err(f"{rater} template: duplicate (scenario_id, scheme_id) pairs")
    return r


def _pairs(df: pd.DataFrame) -> set:
    return set(zip(df["scenario_id"], df["scheme_id"]))


def validate_submission(df: pd.DataFrame, rater: str,
                        expected_pairs: set) -> ValidationReport:
    r = validate_columns(df, f"{rater} submission")
    if not r.ok:
        return r
    if (df["rater_id"] != rater).any():
        r.err(f"{rater}: rater_id not uniformly '{rater}'")
    dup = df.duplicated(["scenario_id", "scheme_id"], keep=False)
    if dup.any():
        r.err(f"{rater}: {int(dup.sum())} duplicate-pair row(s)")
    got = _pairs(df)
    if got - expected_pairs:
        r.err(f"{rater}: {len(got - expected_pairs)} unexpected pair(s), e.g. {sorted(got - expected_pairs)[:3]}")
    if expected_pairs - got:
        r.err(f"{rater}: {len(expected_pairs - got)} missing pair(s), e.g. {sorted(expected_pairs - got)[:3]}")
    for i, v in df["relevance_score"].items():
        if pd.isna(v) or str(v).strip() == "":
            r.err(f"{rater}: row {i + 2} missing relevance_score")
            continue
        try:
            f = float(v)
        except ValueError:
            r.err(f"{rater}: row {i + 2} non-numeric score {v!r}")
            continue
        if f != int(f) or int(f) not in SCORE_LEVELS:
            r.err(f"{rater}: row {i + 2} score {v!r} not an integer in 0-3")
    n_blank_rat = int(_blank(df["relevance_rationale"]).sum())
    if n_blank_rat:
        r.err(f"{rater}: {n_blank_rat} row(s) missing relevance_rationale")
    return r


def validate_pair_match(e1: pd.DataFrame, e2: pd.DataFrame) -> ValidationReport:
    r = ValidationReport()
    a, b = _pairs(e1), _pairs(e2)
    if a != b:
        r.err(f"E1/E2 candidate pairs differ: only-E1={len(a - b)}, only-E2={len(b - a)}")
    return r


def validate_section_b(df: pd.DataFrame) -> ValidationReport:
    """Section B is qualitative only: no numeric relevance score may be present."""
    r = ValidationReport()
    for col in df.columns:
        lc = col.lower()
        if "score" in lc or ("relevance" in lc and "rationale" not in lc):
            if not _blank(df[col]).all():
                r.err(f"Section B: numeric/relevance field '{col}' is populated")
    return r


# ---- Statistics ------------------------------------------------------------
def merge_ratings(e1: pd.DataFrame, e2: pd.DataFrame) -> pd.DataFrame:
    """Align on pair. Scores coerced to float; invalid -> NaN (handled explicitly)."""
    def prep(df, suffix):
        d = df[["scenario_id", "scheme_id", "relevance_score"]].copy()
        d["relevance_score"] = pd.to_numeric(d["relevance_score"], errors="coerce")
        d.loc[~d["relevance_score"].isin(SCORE_LEVELS), "relevance_score"] = np.nan
        return d.rename(columns={"relevance_score": f"score_{suffix}"})
    return prep(e1, "E1").merge(prep(e2, "E2"), on=["scenario_id", "scheme_id"], how="outer")


def quadratic_weighted_kappa(a: np.ndarray, b: np.ndarray):
    """Returns (kappa or None, reason)."""
    if len(a) == 0:
        return None, "no pairs with both ratings"
    k = len(SCORE_LEVELS)
    O = np.zeros((k, k))
    for x, y in zip(a.astype(int), b.astype(int)):
        O[x, y] += 1
    E = np.outer(O.sum(1), O.sum(0)) / O.sum()
    idx = np.arange(k)
    W = (idx[:, None] - idx[None, :]) ** 2 / (k - 1) ** 2
    denom = (W * E).sum()
    if denom == 0:
        return None, "undefined: no score variance in at least one rater"
    return float(1 - (W * O).sum() / denom), "ok"


def krippendorff_alpha_ordinal(a: np.ndarray, b: np.ndarray):
    """Two-rater ordinal alpha from the coincidence matrix. Returns (alpha or None, reason)."""
    if len(a) == 0:
        return None, "no pairs with both ratings"
    k = len(SCORE_LEVELS)
    o = np.zeros((k, k))
    for x, y in zip(a.astype(int), b.astype(int)):
        o[x, y] += 1
        o[y, x] += 1
    n_c = o.sum(1)
    n = n_c.sum()
    delta = np.zeros((k, k))
    for c in range(k):
        for d in range(k):
            lo, hi = min(c, d), max(c, d)
            delta[c, d] = (n_c[lo:hi + 1].sum() - (n_c[c] + n_c[d]) / 2) ** 2
    d_e = (np.outer(n_c, n_c) * delta).sum()
    if d_e == 0:
        return None, "undefined: all ratings identical (no expected disagreement)"
    return float(1 - (n - 1) * (o * delta).sum() / d_e), "ok"


def agreement_report(e1: pd.DataFrame, e2: pd.DataFrame) -> dict:
    m = merge_ratings(e1, e2)
    both = m.dropna(subset=["score_E1", "score_E2"])
    a, b = both["score_E1"].to_numpy(), both["score_E2"].to_numpy()
    kappa, k_reason = quadratic_weighted_kappa(a, b)
    alpha, a_reason = krippendorff_alpha_ordinal(a, b)
    delta = (both["score_E1"] - both["score_E2"]).abs()
    esc = both[delta >= ESCALATION_DELTA].copy()
    esc["abs_delta"] = delta[delta >= ESCALATION_DELTA].astype(int)
    return {
        "n_pairs_total": int(len(m)),
        "n_pairs_rated_by_both": int(len(both)),
        "n_pairs_excluded_missing_or_invalid": int(len(m) - len(both)),
        "exact_agreement_rate": float((delta == 0).mean()) if len(both) else None,
        "n_adjacent_disagreements": int((delta == 1).sum()),
        "n_mandatory_adjudication": int((delta >= ESCALATION_DELTA).sum()),
        "quadratic_weighted_kappa": kappa, "kappa_status": k_reason,
        "kappa_threshold": KAPPA_W_THRESHOLD,
        "kappa_meets_threshold": None if kappa is None else bool(kappa >= KAPPA_W_THRESHOLD),
        "krippendorff_alpha_ordinal": alpha, "alpha_status": a_reason,
        "alpha_threshold": ALPHA_ORD_THRESHOLD,
        "alpha_meets_threshold": None if alpha is None else bool(alpha >= ALPHA_ORD_THRESHOLD),
        "escalation_pairs": esc[["scenario_id", "scheme_id", "score_E1", "score_E2", "abs_delta"]]
                            .to_dict("records"),
    }


# ---- Consensus ledger (separate from raw) -----------------------------------
def write_consensus_ledger(e1: pd.DataFrame, e2: pd.DataFrame, out_path: Path) -> pd.DataFrame:
    """Exact agreements retained; all disagreements left PENDING for human discussion.
    Refuses to write inside any 'raw' directory. Never modifies inputs."""
    if "raw" in {p.lower() for p in out_path.parts}:
        raise ValueError("Consensus ledger must not be written under a raw/ directory")
    m = merge_ratings(e1, e2)
    d = (m["score_E1"] - m["score_E2"]).abs()
    status = np.where(m["score_E1"].isna() | m["score_E2"].isna(), "PENDING_MISSING_RATING",
             np.where(d == 0, "AGREED",
             np.where(d == 1, "PENDING_CONSENSUS_DISCUSSION", "PENDING_ADJUDICATION_PANEL")))
    m["status"] = status
    m["consensus_score"] = np.where(m["status"] == "AGREED", m["score_E1"], np.nan)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    m.to_csv(out_path, index=False)
    return m


# ---- CLI --------------------------------------------------------------------
def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("audit-packets", help="check blank templates + context completeness")
    t.add_argument("--e1", required=True); t.add_argument("--e2", required=True)
    t.add_argument("--scenarios", help="scenario dossier CSV"); t.add_argument("--schemes", help="scheme evidence CSV")
    s = sub.add_parser("agreement", help="validate returned files and compute reliability")
    s.add_argument("--e1", required=True); s.add_argument("--e2", required=True)
    s.add_argument("--template", required=True, help="blank template defining expected pairs")
    s.add_argument("--consensus-out"); s.add_argument("--report-out")
    sb = sub.add_parser("section-b", help="reject numeric scores in Section B")
    sb.add_argument("--file", required=True)
    args = p.parse_args(argv)

    rep = ValidationReport()
    if args.cmd == "audit-packets":
        e1, e2 = pd.read_csv(args.e1), pd.read_csv(args.e2)
        rep.merge(validate_template(e1, "E1")); rep.merge(validate_template(e2, "E2"))
        if rep.ok:
            rep.merge(validate_pair_match(e1, e2))
        if not (args.scenarios and args.schemes):
            rep.err("context dossier/evidence not supplied: packets are NOT answerable (fail closed)")
        else:
            rep.merge(validate_context(pd.read_csv(args.scenarios), pd.read_csv(args.schemes), e1))
    elif args.cmd == "section-b":
        rep.merge(validate_section_b(pd.read_csv(args.file)))
    else:
        e1, e2 = pd.read_csv(args.e1), pd.read_csv(args.e2)
        expected = _pairs(pd.read_csv(args.template))
        rep.merge(validate_submission(e1, "E1", expected)); rep.merge(validate_submission(e2, "E2", expected))
        rep.merge(validate_pair_match(e1, e2))
        if rep.ok:
            res = agreement_report(e1, e2)
            print(json.dumps(res, indent=2, default=str))
            if args.report_out:
                Path(args.report_out).write_text(json.dumps(res, indent=2, default=str))
            if args.consensus_out:
                write_consensus_ledger(e1, e2, Path(args.consensus_out))
    for w in rep.warnings:
        print("WARN:", w)
    for e in rep.errors:
        print("ERROR:", e)
    print("RESULT:", "PASS" if rep.ok else "FAIL")
    return 0 if rep.ok else 1


if __name__ == "__main__":
    sys.exit(main())
