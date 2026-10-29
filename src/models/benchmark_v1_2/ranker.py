"""
Benchmark v1.2 ML-based personalized scheme recommender.

Implements the preregistered v1.2 feature policy:
  - EXCLUDED: immediate_need_matches_heuristic_primary (heuristic-derived)
  - EXCLUDED: archetype_id (template memorisation risk)
  - RETAINED: immediate_need as legitimate farmer context
  - Ablation 1: structured features INCLUDING immediate_need (primary model)
  - Ablation 2: same feature set WITHOUT immediate_need (sensitivity)

IMPORTANT LIMITATIONS:
  - Trained on single-annotator labels (human reviewer 2).
  - Single annotator; no independent inter-rater reliability available.
  - 90 scenarios, 369 candidate pairs — small dataset; results are
    exploratory and not evidence of production-quality generalization.
  - No claim of novelty is made for this model implementation.

Preregistration reference:
  research/dataset_research/benchmark_v1.2_evaluation_preregistration.md
  (approved 2026-10-28)
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# ── v1.2 data paths ──────────────────────────────────────────────────────────
SCENARIO_MATRIX_PATH = REPO_ROOT / "data/benchmarks/v1.2/scenario_matrix.json"
CANDIDATE_RESULTS_PATH = REPO_ROOT / "data/benchmarks/v1.2/candidate_generation_results.json"
SCHEME_MASTER_PATH = REPO_ROOT / "scheme_database/processed/scheme_master.json"
ANNOTATION_CSV_PATH = (
    REPO_ROOT / "data/annotations/benchmark_v1.2/E2_v1.2_blank.csv"
)

# v1.2 output directory
ML_EXPERIMENT_DIR = REPO_ROOT / "data/benchmarks/v1.2/ml_experiment"

# ── Feature column definitions ────────────────────────────────────────────────

SCENARIO_NUMERIC_FEATURES = [
    "land_size_acres",
    "annual_family_income_lakh",
    "secondary_constraint_count",
]

# Ablation 1 scenario categorical features (includes immediate_need)
SCENARIO_CATEGORICAL_FEATURES_ABL1 = [
    "zone_id",
    "district",
    "crop_primary",
    "crop_secondary",
    "land_type",
    "social_category",
    "farmer_category",
    "operational_water_source",
    "borewell_electric_status",
    "immediate_need",   # legitimate farmer context — preregistered
    "primary_crisis",  # from compound_need_details.primary_acute_crisis
    # archetype_id EXCLUDED per preregistration
]

# Ablation 2 scenario categorical features (without immediate_need)
SCENARIO_CATEGORICAL_FEATURES_ABL2 = [
    "zone_id",
    "district",
    "crop_primary",
    "crop_secondary",
    "land_type",
    "social_category",
    "farmer_category",
    "operational_water_source",
    "borewell_electric_status",
    "primary_crisis",
    # immediate_need EXCLUDED for sensitivity ablation
    # archetype_id EXCLUDED per preregistration
]

# Ablation 3 (text representation): immediate_need represented as text, not categorical
SCENARIO_CATEGORICAL_FEATURES_ABL3 = [
    "zone_id",
    "district",
    "crop_primary",
    "crop_secondary",
    "land_type",
    "social_category",
    "farmer_category",
    "operational_water_source",
    "borewell_electric_status",
    "primary_crisis",
]

SCENARIO_BOOLEAN_FEATURES = [
    "is_pure_tenant_without_land_title",
    "land_ownership_cutoff_pre_feb_2019",
    "paid_income_tax_last_assessment_year",
    "pensioner_is_mts_exempt",
    "registered_professional_is_none",
]

SCHEME_NUMERIC_FEATURES = [
    "min_land_acres",
    "max_land_acres",
]

SCHEME_CATEGORICAL_FEATURES = [
    "scheme_id",
    "government_level",
    "benefit_type",
    "target_crops",
    "irrigation_requirements",
    "record_type",
    "parent_scheme_id",
]

# Interaction features — immediate_need_matches_heuristic_primary EXCLUDED
INTERACTION_FEATURES = [
    "land_size_within_scheme_range",
    "water_source_compatible",
    # immediate_need_matches_heuristic_primary EXCLUDED per preregistration
]

# Columns that must NOT appear as features (label leakage protection)
FORBIDDEN_FEATURE_COLUMNS = [
    "relevance_score",
    "relevance_rationale",
    "complementarity_notes",
    "heuristic_score",
    "heuristic_rank",
    "model_score",
    "model_prediction",
    "ai_rationale",
    "consensus_label",
    "prior_label",
    "prior_relevance",
    "immediate_need_matches_heuristic_primary",  # heuristic-derived
]

# archetype_id must never appear in any primary or ablation model
EXCLUDED_FEATURES = ["archetype_id", "immediate_need_matches_heuristic_primary"]


# ── Data loading helpers ──────────────────────────────────────────────────────

def load_scenario_matrix(path: Path = SCENARIO_MATRIX_PATH) -> List[Dict[str, Any]]:
    """Load v1.2 scenario matrix."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_candidate_results(path: Path = CANDIDATE_RESULTS_PATH) -> Dict[str, Any]:
    """Load v1.2 candidate generation results."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_scheme_master(path: Path = SCHEME_MASTER_PATH) -> List[Dict[str, Any]]:
    """Load scheme master registry."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_annotations(path: Path = ANNOTATION_CSV_PATH) -> pd.DataFrame:
    """Load v1.2 single-annotator relevance labels."""
    return pd.read_csv(path)


def extract_section_a_candidates(
    candidate_results: Dict[str, Any],
) -> Dict[str, List[str]]:
    """Extract section_a scheme_id lists per scenario from candidate results."""
    out: Dict[str, List[str]] = {}
    for sid, data in candidate_results.items():
        out[sid] = [c["scheme_id"] for c in data["section_a_candidates"]]
    return out


# ── Scheme / scenario lookup builders ────────────────────────────────────────

def _extract_min_land(min_land_str: Any) -> Optional[float]:
    if not min_land_str or not isinstance(min_land_str, str):
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", min_land_str)
    return float(m.group(1)) if m else None


def _extract_max_land(max_land_str: Any) -> Optional[float]:
    if not max_land_str or not isinstance(max_land_str, str):
        return None
    if "No limit" in max_land_str or "Universal" in max_land_str:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", max_land_str)
    return float(m.group(1)) if m else None


def build_scheme_lookup(schemes: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Build scheme_id -> metadata lookup with numeric land fields."""
    lookup: Dict[str, Dict[str, Any]] = {}
    for s in schemes:
        sid = s["scheme_id"]
        lookup[sid] = {
            "scheme_id": sid,
            "scheme_name": s.get("scheme_name", ""),
            "government_level": s.get("government_level", ""),
            "benefit_type": s.get("benefit_type", ""),
            "target_crops": s.get("target_crops", ""),
            "irrigation_requirements": s.get("irrigation_requirements", ""),
            "record_type": s.get("record_type", ""),
            "parent_scheme_id": s.get("parent_scheme_id") or "",
            "min_land_acres": _extract_min_land(s.get("min_land", "")),
            "max_land_acres": _extract_max_land(s.get("max_land", "")),
        }
    return lookup


def build_scenario_lookup_v12(
    scenarios: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """Build scenario_id -> feature lookup for v1.2 scenarios.

    Extracts compound_need_details.primary_acute_crisis as primary_crisis.
    Does NOT include archetype_id (preregistration exclusion).
    """
    lookup: Dict[str, Dict[str, Any]] = {}
    for s in scenarios:
        sid = s["scenario_id"]
        cnd = s.get("compound_need_details", {}) or {}
        wtr = s.get("water_and_irrigation", {}) or {}
        secondary = cnd.get("secondary_constraints", [])
        secondary_count = len(secondary) if isinstance(secondary, list) else (1 if secondary else 0)

        reg_prof = s.get("registered_professional", "NONE") or "NONE"
        borewell_status = (
            s.get("borewell_electric_status", "")
            or wtr.get("borewell_electric_status", "")
            or ""
        )

        lookup[sid] = {
            "scenario_id": sid,
            "zone_id": s.get("zone_id", ""),
            "district": s.get("district", ""),
            "crop_primary": s.get("crop_primary", ""),
            "crop_secondary": s.get("crop_secondary", "") or "",
            "land_size_acres": float(s.get("land_size_acres", 0.0) or 0.0),
            "land_type": s.get("land_type", ""),
            "social_category": s.get("social_category", ""),
            "farmer_category": s.get("farmer_category", ""),
            "operational_water_source": wtr.get("operational_water_source", ""),
            "borewell_electric_status": borewell_status,
            "immediate_need": s.get("immediate_need", ""),
            "immediate_need_text": str(s.get("immediate_need", "")).lower().replace("_", " "),
            "primary_crisis": cnd.get("primary_acute_crisis", ""),
            # archetype_id intentionally omitted
            "secondary_constraint_count": float(secondary_count),
            "annual_family_income_lakh": float(
                s.get("annual_family_income_lakh", 0.0) or 0.0
            ),
            "is_pure_tenant_without_land_title": bool(
                s.get("is_pure_tenant_without_land_title", False)
            ),
            "land_ownership_cutoff_pre_feb_2019": bool(
                s.get("land_ownership_cutoff_pre_feb_2019", False)
            ),
            "paid_income_tax_last_assessment_year": bool(
                s.get("paid_income_tax_last_assessment_year", False)
            ),
            "pensioner_is_mts_exempt": bool(s.get("pensioner_is_mts_exempt", False)),
            "registered_professional_is_none": reg_prof in {"NONE", "None", "", None},
        }
    return lookup


# ── Feature matrix builder ────────────────────────────────────────────────────

def build_feature_rows_v12(
    scenarios: List[Dict[str, Any]],
    scheme_lookup: Dict[str, Dict[str, Any]],
    candidate_sets: Dict[str, List[str]],
    ablation: int = 1,
) -> pd.DataFrame:
    """Build feature DataFrame for v1.2.

    ablation=1 → include immediate_need (primary preregistered model)
    ablation=2 → exclude immediate_need (sensitivity comparison)

    Never includes immediate_need_matches_heuristic_primary or archetype_id.
    """
    if ablation == 1:
        cat_features = SCENARIO_CATEGORICAL_FEATURES_ABL1
    elif ablation == 2:
        cat_features = SCENARIO_CATEGORICAL_FEATURES_ABL2
    elif ablation == 3:
        cat_features = SCENARIO_CATEGORICAL_FEATURES_ABL3
    else:
        cat_features = SCENARIO_CATEGORICAL_FEATURES_ABL1

    scenario_lookup = build_scenario_lookup_v12(scenarios)
    rows: List[Dict[str, Any]] = []

    for sid, scheme_ids in candidate_sets.items():
        if sid not in scenario_lookup:
            continue
        sc = scenario_lookup[sid]

        for sch_id in scheme_ids:
            if sch_id not in scheme_lookup:
                continue
            sch = scheme_lookup[sch_id]

            row: Dict[str, Any] = {
                "scenario_id": sid,
                "scheme_id": sch_id,
            }

            # Scenario numeric features
            for col in SCENARIO_NUMERIC_FEATURES:
                row[col] = sc.get(col, 0.0)

            # Scenario categorical features (ablation-dependent)
            for col in cat_features:
                row[col] = sc.get(col, "")

            # Scenario text features for text ablation
            if ablation == 3:
                row["immediate_need_text"] = sc.get("immediate_need_text", "")

            # Scenario boolean features
            for col in SCENARIO_BOOLEAN_FEATURES:
                row[col] = bool(sc.get(col, False))

            # Scheme numeric features
            for col in SCHEME_NUMERIC_FEATURES:
                row[col] = sch.get(col, np.nan)

            # Scheme categorical features
            for col in SCHEME_CATEGORICAL_FEATURES:
                row[col] = sch.get(col, "")

            # Interaction features (NO immediate_need_matches_heuristic_primary)
            land_size = sc.get("land_size_acres", 0.0)
            min_land = sch.get("min_land_acres")
            max_land = sch.get("max_land_acres")
            land_in_range = True
            if min_land is not None and land_size < min_land:
                land_in_range = False
            if max_land is not None and land_size > max_land:
                land_in_range = False
            row["land_size_within_scheme_range"] = land_in_range

            water_source = sc.get("operational_water_source", "")
            irrig_req = sch.get("irrigation_requirements", "")
            if "None" in irrig_req or "Rainfed" in irrig_req:
                water_compat = True
            elif any(x in water_source for x in ("Borewell", "Open Well", "Canal", "well", "canal")):
                water_compat = True
            else:
                water_compat = False
            row["water_source_compatible"] = water_compat

            rows.append(row)

    return pd.DataFrame(rows)


# ── Label builder ─────────────────────────────────────────────────────────────

def build_label_vector(
    feature_df: pd.DataFrame,
    annotations: pd.DataFrame,
) -> pd.Series:
    """Build relevance label vector aligned with feature rows.

    Missing labels default to 0 (conservative).
    """
    label_map: Dict[Tuple[str, str], int] = {}
    for _, row in annotations.iterrows():
        label_map[(row["scenario_id"], row["scheme_id"])] = int(row["relevance_score"])

    labels = [
        label_map.get((row["scenario_id"], row["scheme_id"]), 0)
        for _, row in feature_df.iterrows()
    ]
    return pd.Series(labels, index=feature_df.index, name="relevance_score")


# ── Heuristic baseline (v1.2 adaptation) ─────────────────────────────────────

# Mapping from immediate_need to primary scheme (same as v1.1 heuristic)
_HEURISTIC_PRIMARY: Dict[str, str] = {
    "SOLAR_PUMP_INSTALLATION": "SCH006",
    "SOIL_HEALTH_AND_FERTILIZER": "SCH009",
    "PRODUCTION_CREDIT": "SCH008_CENTRAL",
    "INCOME_SUPPORT": "SCH001",
    "BOREWELL_IRRIGATION": "SCH010_AMBEDKAR",
    "RAINWATER_HARVESTING": "SCH005",
    "FARM_MECHANIZATION": "SCH004",
    "MICRO_IRRIGATION_SUPPORT": "SCH003",
    "PROTECTED_HORTICULTURE": "SCH007",
    "CROP_INSURANCE": "SCH001",
    "DEBT_RELIEF": "SCH008_CENTRAL",
    "POST_HARVEST_STORAGE": "SCH009",
}

_HEURISTIC_SECONDARY: Dict[str, set] = {
    "CROP_INSURANCE": {"SCH001", "SCH008_CENTRAL"},
    "PRODUCTION_CREDIT": {"SCH001"},
    "SOLAR_PUMP_INSTALLATION": {"SCH003", "SCH008_CENTRAL"},
    "RAINWATER_HARVESTING": {"SCH003"},
    "MICRO_IRRIGATION_SUPPORT": {"SCH005", "SCH008_CENTRAL"},
    "BOREWELL_IRRIGATION": {"SCH003", "SCH008_CENTRAL"},
    "DEBT_RELIEF": {"SCH001", "SCH009"},
    "POST_HARVEST_STORAGE": {"SCH001", "SCH008_CENTRAL"},
}


def compute_heuristic_score_v12(scheme_id: str, immediate_need: str) -> float:
    """Compute heuristic relevance score (0–3) for v1.2 scenarios."""
    primary = _HEURISTIC_PRIMARY.get(immediate_need, "")
    if scheme_id == primary:
        return 3.0
    if scheme_id in _HEURISTIC_SECONDARY.get(immediate_need, set()):
        return 2.0
    if scheme_id in {"SCH001", "SCH009"}:
        return 1.0
    return 0.0


def rank_heuristic_v12(
    scenario_id: str,
    candidate_schemes: List[str],
    immediate_need: str,
) -> List[str]:
    """Rank candidates for a v1.2 scenario using the heuristic baseline."""
    return sorted(
        candidate_schemes,
        key=lambda s: (-compute_heuristic_score_v12(s, immediate_need), s),
    )


# ── ML Ranker ─────────────────────────────────────────────────────────────────

class BenchmarkV12Ranker(BaseEstimator, RegressorMixin):
    """ML ranking model for Benchmark v1.2.

    Ablation 1 (primary): retains immediate_need, excludes archetype_id
                          and immediate_need_matches_heuristic_primary.
    Ablation 2 (sensitivity): same minus immediate_need.
    """

    def __init__(
        self,
        random_state: int = 42,
        n_splits: int = 5,
        max_iter: int = 200,
        ablation: int = 1,
    ):
        self.random_state = random_state
        self.n_splits = n_splits
        self.max_iter = max_iter
        self.ablation = ablation
        self.pipeline_: Optional[Pipeline] = None
        self.feature_columns_: List[str] = []
        self.is_fitted_: bool = False

    def _build_pipeline(self) -> Pipeline:
        all_numeric = SCENARIO_NUMERIC_FEATURES + SCHEME_NUMERIC_FEATURES + INTERACTION_FEATURES
        if self.ablation == 1:
            cat_base = SCENARIO_CATEGORICAL_FEATURES_ABL1
        elif self.ablation == 2:
            cat_base = SCENARIO_CATEGORICAL_FEATURES_ABL2
        elif self.ablation == 3:
            cat_base = SCENARIO_CATEGORICAL_FEATURES_ABL3
        else:
            cat_base = SCENARIO_CATEGORICAL_FEATURES_ABL1

        all_cat = cat_base + SCHEME_CATEGORICAL_FEATURES

        numeric_features = [c for c in all_numeric if c in self.feature_columns_]
        bool_features = [c for c in SCENARIO_BOOLEAN_FEATURES if c in self.feature_columns_]
        cat_features = [c for c in all_cat if c in self.feature_columns_]

        # Verify no forbidden features slipped in
        for col in EXCLUDED_FEATURES:
            assert col not in numeric_features + bool_features + cat_features, (
                f"Forbidden feature {col!r} found in pipeline"
            )

        transformers = []
        if numeric_features:
            transformers.append(("num", StandardScaler(), numeric_features))
        if cat_features:
            transformers.append(
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features)
            )
        if bool_features:
            transformers.append(
                (
                    "bool",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False, drop="if_binary"),
                    bool_features,
                )
            )
        if self.ablation == 3 and "immediate_need_text" in self.feature_columns_:
            transformers.append(
                ("text", TfidfVectorizer(), "immediate_need_text")
            )

        preprocessor = ColumnTransformer(
            transformers=transformers,
            remainder="drop",
            sparse_threshold=0,
        )
        model = HistGradientBoostingRegressor(
            max_iter=self.max_iter,
            random_state=self.random_state,
        )
        return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])

    def fit(self, X: pd.DataFrame, y: pd.Series, groups: Optional[pd.Series] = None) -> "BenchmarkV12Ranker":
        self.feature_columns_ = [
            c for c in X.columns if c not in ("scenario_id", "scheme_id")
        ]
        # Enforce excluded features are absent
        for col in EXCLUDED_FEATURES:
            if col in self.feature_columns_:
                self.feature_columns_.remove(col)
        self.pipeline_ = self._build_pipeline()
        self.pipeline_.fit(X[self.feature_columns_], y)
        self.is_fitted_ = True
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted_:
            raise ValueError("Model not fitted. Call fit() first.")
        feature_cols = [c for c in self.feature_columns_ if c in X.columns]
        return self.pipeline_.predict(X[feature_cols])

    def rank_scenario(
        self,
        scenario_id: str,
        candidate_schemes: List[str],
        X_full: pd.DataFrame,
    ) -> List[str]:
        """Rank candidate schemes for a single scenario by predicted score."""
        if not self.is_fitted_:
            raise ValueError("Model not fitted. Call fit() first.")

        subset = X_full[X_full["scenario_id"] == scenario_id].copy()
        if subset.empty:
            return list(candidate_schemes)

        valid_candidates = [s for s in candidate_schemes if s in set(subset["scheme_id"])]
        if not valid_candidates:
            return list(candidate_schemes)

        scores = self.predict(subset)
        subset = subset.copy()
        subset["predicted_score"] = scores

        ranked = subset.sort_values(
            by=["predicted_score", "scheme_id"],
            ascending=[False, True],
        )
        return ranked["scheme_id"].tolist()


# ── Out-of-fold evaluation ────────────────────────────────────────────────────

def run_oof_evaluation(
    feature_df: pd.DataFrame,
    labels: pd.Series,
    n_splits: int = 5,
    random_state: int = 42,
    ablation: int = 1,
) -> Dict[str, Any]:
    """GroupKFold OOF evaluation grouped by scenario_id."""
    scenario_ids = feature_df["scenario_id"].unique()
    gkf = GroupKFold(n_splits=n_splits)
    group_map = {sid: i for i, sid in enumerate(sorted(scenario_ids))}
    groups = feature_df["scenario_id"].map(group_map).values

    oof_scores = np.full(len(feature_df), np.nan)
    fold_assignments: List[Dict[str, Any]] = []

    for fold_idx, (train_idx, test_idx) in enumerate(
        gkf.split(feature_df, labels, groups=groups)
    ):
        train_df = feature_df.iloc[train_idx]
        train_labels = labels.iloc[train_idx]
        test_df = feature_df.iloc[test_idx]

        fold_model = BenchmarkV12Ranker(
            random_state=random_state, ablation=ablation, max_iter=200
        )
        fold_model.fit(train_df, train_labels)
        preds = fold_model.predict(test_df)
        oof_scores[test_idx] = preds

        train_scenarios = sorted(feature_df.iloc[train_idx]["scenario_id"].unique().tolist())
        test_scenarios = sorted(feature_df.iloc[test_idx]["scenario_id"].unique().tolist())
        fold_assignments.append({
            "fold": fold_idx,
            "train_scenarios": train_scenarios,
            "test_scenarios": test_scenarios,
        })

    return {
        "oof_scores": oof_scores,
        "fold_assignments": fold_assignments,
        "n_splits": n_splits,
        "ablation": ablation,
    }


# ── LOZO and holdout helpers ──────────────────────────────────────────────────

def run_lozo_evaluation(
    feature_df: pd.DataFrame,
    labels: pd.Series,
    scenario_to_zone: Dict[str, int],
    ablation: int = 1,
    random_state: int = 42,
) -> Dict[str, Dict[str, Any]]:
    """Leave-one-zone-out evaluation."""
    results: Dict[str, Dict[str, Any]] = {}
    zones = sorted(set(scenario_to_zone.values()))

    for held_zone in zones:
        test_sids = {s for s, z in scenario_to_zone.items() if z == held_zone}
        train_mask = ~feature_df["scenario_id"].isin(test_sids)
        test_mask = feature_df["scenario_id"].isin(test_sids)

        train_df = feature_df[train_mask]
        train_labels = labels[train_mask]
        test_df = feature_df[test_mask]

        fold_model = BenchmarkV12Ranker(random_state=random_state, ablation=ablation)
        fold_model.fit(train_df, train_labels)
        preds = fold_model.predict(test_df)

        test_df = test_df.copy()
        test_df["predicted_score"] = preds

        results[f"Z{held_zone}"] = {
            "held_zone": held_zone,
            "test_scenarios": sorted(test_sids),
            "predictions": {
                sid: test_df[test_df["scenario_id"] == sid]["predicted_score"].tolist()
                for sid in test_sids
            },
            "scheme_ids": {
                sid: test_df[test_df["scenario_id"] == sid]["scheme_id"].tolist()
                for sid in test_sids
            },
        }

    return results


def run_holdout_evaluation(
    feature_df: pd.DataFrame,
    labels: pd.Series,
    holdout_scenario_ids: List[str],
    ablation: int = 1,
    random_state: int = 42,
) -> Dict[str, Any]:
    """Train on non-holdout scenarios, evaluate on holdout."""
    holdout_set = set(holdout_scenario_ids)
    train_mask = ~feature_df["scenario_id"].isin(holdout_set)
    test_mask = feature_df["scenario_id"].isin(holdout_set)

    train_df = feature_df[train_mask]
    train_labels = labels[train_mask]
    test_df = feature_df[test_mask].copy()

    model = BenchmarkV12Ranker(random_state=random_state, ablation=ablation)
    model.fit(train_df, train_labels)
    preds = model.predict(test_df)
    test_df["predicted_score"] = preds

    return {
        "holdout_scenarios": sorted(holdout_scenario_ids),
        "n_train": int(train_mask.sum()),
        "n_test": int(test_mask.sum()),
        "predictions": {
            sid: test_df[test_df["scenario_id"] == sid]["predicted_score"].tolist()
            for sid in holdout_scenario_ids
        },
        "scheme_ids": {
            sid: test_df[test_df["scenario_id"] == sid]["scheme_id"].tolist()
            for sid in holdout_scenario_ids
        },
    }


# ── Validation helpers ────────────────────────────────────────────────────────

def validate_no_label_leakage(feature_df: pd.DataFrame) -> List[str]:
    """Check no forbidden columns are in the feature matrix."""
    errors = []
    for col in FORBIDDEN_FEATURE_COLUMNS + EXCLUDED_FEATURES:
        if col in feature_df.columns:
            errors.append(f"Forbidden column present: {col!r}")
    if "scenario_id" not in feature_df.columns:
        errors.append("Missing scenario_id column")
    if "scheme_id" not in feature_df.columns:
        errors.append("Missing scheme_id column")
    return errors


def validate_feature_alignment(
    feature_df: pd.DataFrame,
    candidate_sets: Dict[str, List[str]],
) -> List[str]:
    """Validate feature rows exactly match candidate sets."""
    errors = []
    expected = {(sid, sch) for sid, sids in candidate_sets.items() for sch in sids}
    actual = {(r["scenario_id"], r["scheme_id"]) for _, r in feature_df.iterrows()}
    missing = expected - actual
    extra = actual - expected
    if missing:
        errors.append(f"Missing pairs: {sorted(missing)[:10]}")
    if extra:
        errors.append(f"Extra pairs: {sorted(extra)[:10]}")
    return errors


def validate_group_leakage(
    feature_df: pd.DataFrame,
    train_indices: np.ndarray,
    test_indices: np.ndarray,
) -> List[str]:
    """Validate no scenario appears in both train and test."""
    errors = []
    train_sids = set(feature_df.iloc[train_indices]["scenario_id"])
    test_sids = set(feature_df.iloc[test_indices]["scenario_id"])
    overlap = train_sids & test_sids
    if overlap:
        errors.append(f"Scenario leakage: {sorted(overlap)}")
    return errors


def validate_annotation_candidate_alignment(
    annotations: pd.DataFrame,
    candidate_sets: Dict[str, List[str]],
) -> List[str]:
    """Validate every annotated pair belongs to that scenario's Section A set."""
    errors = []
    for _, row in annotations.iterrows():
        sid = row["scenario_id"]
        sch_id = row["scheme_id"]
        if sid not in candidate_sets:
            errors.append(f"Scenario {sid!r} not in candidate sets")
            continue
        if sch_id not in candidate_sets[sid]:
            errors.append(f"Scheme {sch_id!r} not in Section A for {sid!r}")
    return errors

