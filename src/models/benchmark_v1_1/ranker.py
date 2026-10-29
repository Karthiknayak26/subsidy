"""
Benchmark v1.1 ML-based personalized scheme recommender.

Experimental ML ranking model for farmer-scheme recommendation.
Implements a scikit-learn pipeline that predicts relevance scores
for (scenario, scheme) candidate pairs and ranks them accordingly.

IMPORTANT LIMITATIONS:
- Trained on single-annotator labels from human_reviewer_annotations.csv.
- All 269 annotation scores exactly match an earlier AI practice file
  (documented provenance limitation). Labels are treated as exploratory
  training targets only, NOT verified independent human gold labels.
- Small dataset: 60 scenarios, 269 candidate pairs. Results are exploratory.
- No claim of novelty is made for this model implementation.
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
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# Paths to repository data sources
SCENARIO_MATRIX_PATH = REPO_ROOT / "data/benchmarks/v1.1/scenario_matrix.json"
CANDIDATE_RESULTS_PATH = REPO_ROOT / "data/benchmarks/v1.1/candidate_generation_results.json"
SCHEME_MASTER_PATH = REPO_ROOT / "scheme_database/processed/scheme_master.json"
ANNOTATION_CSV_PATH = REPO_ROOT / "data/annotations/benchmark_v1.1/human_reviewer_annotations.csv"

# Output paths (versioned v1.1-specific)
ML_EXPERIMENT_DIR = REPO_ROOT / "data/benchmarks/v1.1/ml_experiment"
MODEL_METADATA_PATH = ML_EXPERIMENT_DIR / "model_metadata_v1.1.0.json"
OOF_PREDICTIONS_PATH = ML_EXPERIMENT_DIR / "oof_predictions_v1.1.0.json"
METRICS_OUTPUT_PATH = ML_EXPERIMENT_DIR / "metrics_v1.1.0.json"


# Feature column definitions
SCENARIO_NUMERIC_FEATURES = [
    "land_size_acres",
    "annual_family_income_lakh",
    "secondary_constraint_count",
]

SCENARIO_CATEGORICAL_FEATURES = [
    "zone_id",
    "district",
    "crop_primary",
    "crop_secondary",
    "land_type",
    "social_category",
    "farmer_category",
    "operational_water_source",
    "borewell_electric_status",
    "immediate_need",
    "archetype_id",
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

INTERACTION_FEATURES = [
    "land_size_within_scheme_range",
    "water_source_compatible",
    "immediate_need_matches_heuristic_primary",
]

# All feature column names used in the model pipeline
ALL_FEATURE_COLUMNS = (
    SCENARIO_NUMERIC_FEATURES
    + SCENARIO_CATEGORICAL_FEATURES
    + SCENARIO_BOOLEAN_FEATURES
    + SCHEME_NUMERIC_FEATURES
    + SCHEME_CATEGORICAL_FEATURES
    + INTERACTION_FEATURES
)

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
]


def load_scenario_matrix(path: Path = SCENARIO_MATRIX_PATH) -> List[Dict[str, Any]]:
    """Load v1.1 scenario matrix."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_candidate_results(path: Path = CANDIDATE_RESULTS_PATH) -> Dict[str, Any]:
    """Load v1.1 candidate generation results."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_scheme_master(path: Path = SCHEME_MASTER_PATH) -> List[Dict[str, Any]]:
    """Load scheme master registry."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_annotations(path: Path = ANNOTATION_CSV_PATH) -> pd.DataFrame:
    """Load single-annotator relevance labels."""
    return pd.read_csv(path)


def extract_min_land_acres(min_land_str: str) -> Optional[float]:
    """Extract numeric minimum land value from scheme_master min_land string."""
    if not min_land_str or not isinstance(min_land_str, str):
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", min_land_str)
    return float(match.group(1)) if match else None


def extract_max_land_acres(max_land_str: str) -> Optional[float]:
    """Extract numeric maximum land value from scheme_master max_land string."""
    if not max_land_str or not isinstance(max_land_str, str):
        return None
    # Handle "No limit" cases
    if "No limit" in max_land_str or "Universal" in max_land_str:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", max_land_str)
    return float(match.group(1)) if match else None


def build_scheme_lookup(schemes: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Build scheme_id -> scheme metadata lookup with derived numeric features."""
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
            "min_land_acres": extract_min_land_acres(s.get("min_land", "")),
            "max_land_acres": extract_max_land_acres(s.get("max_land", "")),
        }
    return lookup


def build_scenario_lookup(scenarios: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Build scenario_id -> scenario context lookup with derived features."""
    lookup: Dict[str, Dict[str, Any]] = {}
    for s in scenarios:
        sid = s["scenario_id"]
        cnd = s.get("compound_need_details", {}) or {}
        wtr = s.get("water_and_irrigation", {}) or {}
        secondary = cnd.get("secondary_constraints", [])
        if isinstance(secondary, list):
            secondary_count = len(secondary)
        else:
            secondary_count = 1 if secondary else 0

        reg_prof = s.get("registered_professional", "NONE") or "NONE"
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
            "borewell_electric_status": s.get("borewell_electric_status", "") or wtr.get("borewell_electric_status", ""),
            "immediate_need": s.get("immediate_need", ""),
            "archetype_id": cnd.get("archetype_id", ""),
            "secondary_constraint_count": float(secondary_count),
            "annual_family_income_lakh": float(s.get("annual_family_income_lakh", 0.0) or 0.0),
            "is_pure_tenant_without_land_title": bool(s.get("is_pure_tenant_without_land_title", False)),
            "land_ownership_cutoff_pre_feb_2019": bool(s.get("land_ownership_cutoff_pre_feb_2019", False)),
            "paid_income_tax_last_assessment_year": bool(s.get("paid_income_tax_last_assessment_year", False)),
            "pensioner_is_mts_exempt": bool(s.get("pensioner_is_mts_exempt", False)),
            "registered_professional_is_none": reg_prof in {"NONE", "None", "", None},
        }
    return lookup


def get_heuristic_primary_scheme(immediate_need: str) -> str:
    """Return the heuristic primary scheme for an immediate need."""
    primary_map = {
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
    }
    return primary_map.get(immediate_need, "")


def build_feature_rows(
    scenarios: List[Dict[str, Any]],
    scheme_lookup: Dict[str, Dict[str, Any]],
    candidate_sets: Dict[str, List[str]],
) -> pd.DataFrame:
    """Build a feature DataFrame with one row per (scenario, scheme) candidate pair.

    No label columns are included. All features are derived from scenario context
    and scheme metadata only.
    """
    scenario_lookup = build_scenario_lookup(scenarios)
    rows: List[Dict[str, Any]] = []

    for sid, scheme_ids in candidate_sets.items():
        if sid not in scenario_lookup:
            continue
        sc = scenario_lookup[sid]
        immediate_need = sc["immediate_need"]
        heuristic_primary = get_heuristic_primary_scheme(immediate_need)

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

            # Scenario categorical features
            for col in SCENARIO_CATEGORICAL_FEATURES:
                row[col] = sc.get(col, "")

            # Scenario boolean features
            for col in SCENARIO_BOOLEAN_FEATURES:
                row[col] = bool(sc.get(col, False))

            # Scheme numeric features
            for col in SCHEME_NUMERIC_FEATURES:
                row[col] = sch.get(col, np.nan)

            # Scheme categorical features
            for col in SCHEME_CATEGORICAL_FEATURES:
                row[col] = sch.get(col, "")

            # Interaction features
            land_size = sc.get("land_size_acres", 0.0)
            min_land = sch.get("min_land_acres")
            max_land = sch.get("max_land_acres")
            land_in_range = True
            if min_land is not None and land_size < min_land:
                land_in_range = False
            if max_land is not None and land_size > max_land:
                land_in_range = False
            row["land_size_within_scheme_range"] = land_in_range

            # Water source compatibility: simple heuristic
            water_source = sc.get("operational_water_source", "")
            irrig_req = sch.get("irrigation_requirements", "")
            water_compatible = True
            if "None" in irrig_req or "Rainfed" in irrig_req:
                water_compatible = True
            elif "Borewell" in water_source or "Open Well" in water_source or "Canal" in water_source:
                water_compatible = True
            else:
                water_compatible = False
            row["water_source_compatible"] = water_compatible

            row["immediate_need_matches_heuristic_primary"] = sch_id == heuristic_primary

            rows.append(row)

    return pd.DataFrame(rows)


def build_label_vector(
    feature_df: pd.DataFrame,
    annotations: pd.DataFrame,
) -> pd.Series:
    """Build relevance score labels aligned with feature rows.

    Returns a Series indexed by feature_df index. Missing labels default to 0.
    """
    label_map: Dict[Tuple[str, str], int] = {}
    for _, row in annotations.iterrows():
        label_map[(row["scenario_id"], row["scheme_id"])] = int(row["relevance_score"])

    labels = []
    for _, row in feature_df.iterrows():
        key = (row["scenario_id"], row["scheme_id"])
        labels.append(label_map.get(key, 0))

    return pd.Series(labels, index=feature_df.index, name="relevance_score")


class BenchmarkV11Ranker(BaseEstimator, RegressorMixin):
    """ML ranking model for Benchmark v1.1.

    Wraps a scikit-learn pipeline that predicts relevance scores for
    (scenario, scheme) candidate pairs. Rankings are derived by sorting
    candidates by predicted score within each scenario.

    Uses GroupKFold cross-validation grouped by scenario_id to prevent
    data leakage across candidates from the same scenario.
    """

    def __init__(
        self,
        random_state: int = 42,
        n_splits: int = 5,
        max_iter: int = 200,
    ):
        self.random_state = random_state
        self.n_splits = n_splits
        self.max_iter = max_iter
        self.pipeline_: Optional[Pipeline] = None
        self.feature_columns_: List[str] = []
        self.is_fitted_: bool = False

    def _build_pipeline(self) -> Pipeline:
        """Build the scikit-learn preprocessing + model pipeline."""
        numeric_features = [
            c for c in SCENARIO_NUMERIC_FEATURES + SCHEME_NUMERIC_FEATURES + INTERACTION_FEATURES
            if c in self.feature_columns_
        ]
        categorical_features = [
            c for c in SCENARIO_CATEGORICAL_FEATURES + SCHEME_CATEGORICAL_FEATURES + SCENARIO_BOOLEAN_FEATURES
            if c in self.feature_columns_
        ]

        # Separate boolean from categorical for proper handling
        bool_features = [
            c for c in categorical_features if c in SCENARIO_BOOLEAN_FEATURES
        ]
        cat_features = [
            c for c in categorical_features if c not in SCENARIO_BOOLEAN_FEATURES
        ]

        transformers: List[Tuple[str, Any, List[str]]] = []

        if numeric_features:
            transformers.append(
                ("num", StandardScaler(), numeric_features)
            )
        if cat_features:
            transformers.append(
                ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_features)
            )
        if bool_features:
            transformers.append(
                ("bool", OneHotEncoder(handle_unknown="ignore", sparse_output=False, drop="if_binary"), bool_features)
            )

        preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")

        model = HistGradientBoostingRegressor(
            max_iter=self.max_iter,
            random_state=self.random_state,
        )

        return Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])

    def fit(self, X: pd.DataFrame, y: pd.Series, groups: Optional[pd.Series] = None) -> "BenchmarkV11Ranker":
        """Fit the model on all data (no CV). For final model training."""
        self.feature_columns_ = [c for c in X.columns if c not in ("scenario_id", "scheme_id")]
        self.pipeline_ = self._build_pipeline()
        self.pipeline_.fit(X[self.feature_columns_], y)
        self.is_fitted_ = True
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict relevance scores for feature rows."""
        if not self.is_fitted_:
            raise ValueError("Model is not fitted. Call fit() first.")
        feature_cols = [c for c in self.feature_columns_ if c in X.columns]
        return self.pipeline_.predict(X[feature_cols])

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Not supported for regressor. Returns predicted scores reshaped."""
        return self.predict(X).reshape(-1, 1)

    def rank_scenario(
        self,
        scenario_id: str,
        candidate_schemes: List[str],
        X_full: pd.DataFrame,
    ) -> List[str]:
        """Rank candidate schemes for a single scenario by predicted score."""
        if not self.is_fitted_:
            raise ValueError("Model is not fitted. Call fit() first.")

        subset = X_full[X_full["scenario_id"] == scenario_id].copy()
        if subset.empty:
            return list(candidate_schemes)

        # Ensure only valid candidates are included
        valid_candidates = [s for s in candidate_schemes if s in set(subset["scheme_id"])]
        if not valid_candidates:
            return list(candidate_schemes)

        scores = self.predict(subset)
        subset = subset.copy()
        subset["predicted_score"] = scores

        # Sort by predicted score descending, tie-break by scheme_id ascending
        ranked = subset.sort_values(
            by=["predicted_score", "scheme_id"],
            ascending=[False, True],
        )
        return ranked["scheme_id"].tolist()


def run_out_of_fold_evaluation(
    feature_df: pd.DataFrame,
    labels: pd.Series,
    n_splits: int = 5,
    random_state: int = 42,
) -> Dict[str, Any]:
    """Run out-of-fold evaluation grouped by scenario_id.

    For each fold, train on all scenarios except the held-out ones,
    predict on held-out scenarios, and collect out-of-fold predictions.

    Returns a dict with per-scenario predictions and overall metrics.
    """
    from src.evaluation.metrics import compute_ndcg_at_k, compute_mrr

    scenario_ids = feature_df["scenario_id"].unique()
    gkf = GroupKFold(n_splits=n_splits)

    # Map scenario_id to group index for GroupKFold
    group_map = {sid: i for i, sid in enumerate(sorted(scenario_ids))}
    groups = feature_df["scenario_id"].map(group_map).values

    oof_predictions: Dict[str, np.ndarray] = {}  # scenario_id -> predicted scores aligned with rows
    oof_indices: Dict[str, np.ndarray] = {}  # scenario_id -> row indices

    model = BenchmarkV11Ranker(random_state=random_state, n_splits=n_splits)

    for fold_idx, (train_idx, test_idx) in enumerate(gkf.split(feature_df, labels, groups=groups)):
        train_df = feature_df.iloc[train_idx]
        train_labels = labels.iloc[train_idx]
        test_df = feature_df.iloc[test_idx]

        # Train on fold training data
        fold_model = BenchmarkV11Ranker(random_state=random_state)
        fold_model.fit(train_df, train_labels)

        # Predict on held-out data
        test_subset = test_df.copy()
        test_subset.loc[:, "predicted_score"] = fold_model.predict(test_subset)

        # Store predictions by scenario
        for sid in test_subset["scenario_id"].unique():
            sid_rows = test_subset[test_subset["scenario_id"] == sid]
            if sid not in oof_predictions:
                oof_predictions[sid] = []
                oof_indices[sid] = []
            oof_predictions[sid].extend(sid_rows["predicted_score"].values)
            oof_indices[sid].extend(sid_rows.index.values)

    # Reassemble full OOF prediction vector aligned with feature_df
    oof_scores = np.full(len(feature_df), np.nan)
    for sid, scores in oof_predictions.items():
        idx = oof_indices[sid]
        oof_scores[idx] = scores

    return {
        "oof_scores": oof_scores,
        "n_splits": n_splits,
    }


def compute_scenario_metrics(
    sid: str,
    ranked_schemes: List[str],
    labels_dict: Dict[Tuple[str, str], int],
) -> Tuple[float, float, List[float]]:
    """Compute NDCG@3 and MRR for a single scenario ranking."""
    from src.evaluation.metrics import compute_ndcg_at_k, compute_mrr

    score_vector = [float(labels_dict.get((sid, s), 0)) for s in ranked_schemes]
    ndcg = compute_ndcg_at_k(score_vector, k=3)
    mrr = compute_mrr(score_vector, threshold=2.0)
    return ndcg, mrr, score_vector


def validate_no_label_leakage(feature_df: pd.DataFrame) -> List[str]:
    """Check that no forbidden label columns are present in features."""
    errors = []
    for col in FORBIDDEN_FEATURE_COLUMNS:
        if col in feature_df.columns:
            errors.append(f"Forbidden label column present in features: {col}")
    # Check that scenario_id and scheme_id are present (identifiers, not features)
    if "scenario_id" not in feature_df.columns:
        errors.append("Missing scenario_id column")
    if "scheme_id" not in feature_df.columns:
        errors.append("Missing scheme_id column")
    return errors


def validate_feature_alignment(
    feature_df: pd.DataFrame,
    candidate_sets: Dict[str, List[str]],
) -> List[str]:
    """Validate that feature rows match candidate sets exactly."""
    errors = []

    # Build expected pairs from candidate sets
    expected_pairs: set = set()
    for sid, scheme_ids in candidate_sets.items():
        for sch_id in scheme_ids:
            expected_pairs.add((sid, sch_id))

    # Build actual pairs from feature_df
    actual_pairs: set = set()
    for _, row in feature_df.iterrows():
        actual_pairs.add((row["scenario_id"], row["scheme_id"]))

    missing = expected_pairs - actual_pairs
    extra = actual_pairs - expected_pairs

    if missing:
        errors.append(f"Missing candidate pairs in features: {sorted(list(missing))[:10]}")
    if extra:
        errors.append(f"Extra candidate pairs in features: {sorted(list(extra))[:10]}")

    return errors


def validate_group_leakage(
    feature_df: pd.DataFrame,
    train_indices: np.ndarray,
    test_indices: np.ndarray,
) -> List[str]:
    """Validate that no scenario appears in both train and test sets."""
    errors = []
    train_scenarios = set(feature_df.iloc[train_indices]["scenario_id"])
    test_scenarios = set(feature_df.iloc[test_indices]["scenario_id"])
    overlap = train_scenarios & test_scenarios
    if overlap:
        errors.append(f"Scenario leakage between train and test: {sorted(overlap)}")
    return errors

