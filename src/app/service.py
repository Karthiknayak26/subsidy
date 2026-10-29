"""
src/app/service.py
------------------
Recommendation service connecting the deterministic EligibilityEngine,
statutory governance safeguard pipeline, and Benchmark v1.2 ML model
(with heuristic baseline fallback).

Key Principles:
1. Reuses the frozen EligibilityEngine and governance pipeline without duplicate rules.
2. Numerical scoring is strictly restricted to Section A candidates.
3. Section B candidates are qualitative advisory only (numerical scoring disabled).
4. Discloses whether ranking was produced by the v1.2 ML model or heuristic baseline.
5. All recommendations include official citations, document requirements, and disclaimers.
"""

from __future__ import annotations

import os

# Suppress loky win32 core count warning on Windows
if "LOKY_MAX_CPU_COUNT" not in os.environ:
    os.environ["LOKY_MAX_CPU_COUNT"] = "4"

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd

from src.eligibility.engine import EligibilityEngine
from src.eligibility.governance import PROVISIONAL_SCHEMES, apply_governance_safeguard
from src.eligibility.models import (
    BorewellElectricStatus,
    EligibilityStatus,
    FarmerScenario,
    GovtEmployeeCategory,
)
from src.models.benchmark_v1_2.ranker import (
    BenchmarkV12Ranker,
    build_feature_rows_v12,
    build_scheme_lookup,
    compute_heuristic_score_v12,
    rank_heuristic_v12,
)
from src.app.demo_profiles import (
    DISTRICTS,
    DISTRICT_TO_ZONE,
    ZONE_TO_NAME,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_SCHEME_MASTER = REPO_ROOT / "scheme_database" / "processed" / "scheme_master.json"
DEFAULT_MODEL_PATH = (
    REPO_ROOT / "data" / "benchmarks" / "v1.2" / "ml_experiment" / "model_v1.2.0.joblib"
)


class RecommendationService:
    """End-to-end recommendation service for personalized farmer scheme advisory."""

    def __init__(
        self,
        scheme_master_path: Optional[str | Path] = None,
        model_path: Optional[str | Path] = None,
    ):
        self.scheme_master_path = Path(scheme_master_path or DEFAULT_SCHEME_MASTER)
        self.model_path = Path(model_path or DEFAULT_MODEL_PATH)

        # Initialize deterministic eligibility engine
        self.engine = EligibilityEngine(str(self.scheme_master_path))
        self.schemes: List[Dict[str, Any]] = self.engine.schemes
        self.scheme_lookup: Dict[str, Dict[str, Any]] = build_scheme_lookup(self.schemes)
        self.scheme_master_by_id: Dict[str, Dict[str, Any]] = {
            s["scheme_id"]: s for s in self.schemes
        }

        # Attempt to load Benchmark v1.2 ML model
        self.ml_model: Optional[BenchmarkV12Ranker] = None
        self.model_load_error: Optional[str] = None
        self._load_model()

    def _load_model(self) -> None:
        """Load the trained Benchmark v1.2 ML model artifact if available."""
        if not self.model_path.exists():
            self.model_load_error = f"Model artifact not found at {self.model_path}"
            return
        try:
            loaded = joblib.load(self.model_path)
            if isinstance(loaded, BenchmarkV12Ranker) and getattr(loaded, "is_fitted_", False):
                self.ml_model = loaded
                self.model_load_error = None
            else:
                self.model_load_error = (
                    f"Loaded object of type {type(loaded)} is not a fitted BenchmarkV12Ranker"
                )
        except Exception as e:
            self.model_load_error = f"Error loading model artifact: {e}"

    @property
    def has_ml_model(self) -> bool:
        return self.ml_model is not None

    def validate_inputs(
        self, raw_profile: Dict[str, Any]
    ) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Validate and normalize input fields.
        Ensures required fields are present and valid, and statutory attributes
        are not silently invented or inferred.
        """
        errors: List[str] = []
        cleaned: Dict[str, Any] = dict(raw_profile)

        # 1. District and Zone
        district = str(cleaned.get("district", "")).strip()
        if not district:
            errors.append("District is required.")
        elif district not in DISTRICT_TO_ZONE and district not in DISTRICTS:
            errors.append(f"Unknown or unsupported district '{district}'.")
        else:
            cleaned["district"] = district
            if not cleaned.get("zone_id"):
                cleaned["zone_id"] = DISTRICT_TO_ZONE.get(district, "Z1")
            if not cleaned.get("agro_climatic_zone"):
                cleaned["agro_climatic_zone"] = ZONE_TO_NAME.get(
                    cleaned["zone_id"], "Unknown Zone"
                )

        # 2. Primary Crop
        crop_primary = str(cleaned.get("crop_primary", "")).strip()
        if not crop_primary:
            errors.append("Primary crop is required.")
        else:
            cleaned["crop_primary"] = crop_primary

        # 3. Land Size
        land_size = cleaned.get("land_size_acres")
        if land_size is None or land_size == "":
            errors.append("Land size (acres) is required.")
        else:
            try:
                val = float(land_size)
                if val < 0.0:
                    errors.append("Land size cannot be negative.")
                else:
                    cleaned["land_size_acres"] = val
            except (ValueError, TypeError):
                errors.append(f"Invalid land size: '{land_size}'. Must be a number.")

        # 4. Land Type
        land_type = str(cleaned.get("land_type", "")).strip()
        if not land_type:
            errors.append("Land type is required.")
        else:
            cleaned["land_type"] = land_type

        # 5. Social Category
        social_cat = str(cleaned.get("social_category", "")).strip()
        if not social_cat:
            errors.append("Social category is required.")
        else:
            cleaned["social_category"] = social_cat

        # 6. Farmer Category
        farmer_cat = str(cleaned.get("farmer_category", "")).strip()
        if not farmer_cat:
            errors.append("Farmer category is required.")
        else:
            cleaned["farmer_category"] = farmer_cat

        # 7. Immediate Need
        immediate_need = str(cleaned.get("immediate_need", "")).strip()
        if not immediate_need:
            errors.append("Immediate farming need is required.")
        else:
            cleaned["immediate_need"] = immediate_need

        # 8. Annual Family Income
        income = cleaned.get("annual_family_income_lakh")
        if income is not None and income != "":
            try:
                val = float(income)
                if val < 0.0:
                    errors.append("Annual family income cannot be negative.")
                else:
                    cleaned["annual_family_income_lakh"] = val
            except (ValueError, TypeError):
                errors.append(f"Invalid annual family income: '{income}'. Must be a number.")
        else:
            cleaned["annual_family_income_lakh"] = 0.0

        # 9. Existing Assets
        assets = cleaned.get("existing_assets")
        if assets is None:
            cleaned["existing_assets"] = []
        elif isinstance(assets, str):
            cleaned["existing_assets"] = [a.strip() for a in assets.split(",") if a.strip()]

        # 10. Scenario ID
        if not cleaned.get("scenario_id"):
            cleaned["scenario_id"] = "FARMER_USER_001"

        # 11. Normalize Borewell electric status to match enum
        b_status = cleaned.get("borewell_electric_status")
        w_status = (cleaned.get("water_and_irrigation") or {}).get("borewell_electric_status")
        chosen_status = b_status or w_status
        if chosen_status in ["Non-energized (off-grid)", "UNENERGIZED_OFF_GRID", "Off-grid"]:
            cleaned["borewell_electric_status"] = "UNENERGIZED_OFF_GRID"
        elif chosen_status in [
            "Grid-connected IP set",
            "GRID_CONNECTED_IP_SET",
            "Grid-connected borewell",
        ]:
            cleaned["borewell_electric_status"] = "GRID_CONNECTED_IP_SET"
        elif chosen_status in ["No electricity", "NONE", "Rainfed (no source)"]:
            cleaned["borewell_electric_status"] = "NONE"
        elif chosen_status == "UNKNOWN" or chosen_status is None:
            cleaned["borewell_electric_status"] = "UNKNOWN"
        else:
            cleaned["borewell_electric_status"] = "NONE"

        # Water source dictionary
        if "water_and_irrigation" not in cleaned or not isinstance(
            cleaned["water_and_irrigation"], dict
        ):
            cleaned["water_and_irrigation"] = {
                "operational_water_source": cleaned.get(
                    "operational_water_source", "Rainfed (no source)"
                ),
                "borewell_electric_status": cleaned["borewell_electric_status"],
            }
        else:
            cleaned["operational_water_source"] = cleaned["water_and_irrigation"].get(
                "operational_water_source", "Rainfed (no source)"
            )

        # Compound need details
        if "compound_need_details" not in cleaned or not isinstance(
            cleaned["compound_need_details"], dict
        ):
            cleaned["compound_need_details"] = {
                "primary_acute_crisis": cleaned.get("primary_acute_crisis")
                or cleaned.get("immediate_need", ""),
                "secondary_constraints": cleaned.get("secondary_constraints", []),
                "narrative": cleaned.get("narrative", ""),
            }

        return (len(errors) == 0, errors, cleaned)

    def recommend(
        self,
        raw_profile: Dict[str, Any],
        force_heuristic: bool = False,
    ) -> Dict[str, Any]:
        """
        End-to-end evaluation and recommendation pipeline:
        1. Validate inputs.
        2. Execute frozen deterministic EligibilityEngine.
        3. Apply statutory governance safeguards (Section A vs B vs Disqualified).
        4. Rank Section A candidates using v1.2 ML model (or heuristic baseline fallback).
        5. Generate explainability notes and legal disclaimers.
        """
        valid, errors, profile = self.validate_inputs(raw_profile)
        if not valid:
            return {
                "success": False,
                "errors": errors,
                "scenario_id": raw_profile.get("scenario_id", "UNKNOWN"),
                "ranking_method": "None (Input Validation Failed)",
                "section_a": [],
                "section_b": [],
                "disqualified": [],
                "counts": {"section_a": 0, "section_b": 0, "disqualified": 0, "total": 0},
            }

        sid = profile["scenario_id"]

        # Filter fields for FarmerScenario dataclass
        import dataclasses
        valid_fields = {f.name for f in dataclasses.fields(FarmerScenario)}
        scenario_dict = {k: v for k, v in profile.items() if k in valid_fields}

        # Instantiate FarmerScenario
        scenario_obj = FarmerScenario.from_dict(scenario_dict)

        # Run frozen deterministic engine
        determinations = self.engine.evaluate_scenario(scenario_obj)

        # Process determinations through governance safeguard
        section_a_raw: List[Dict[str, Any]] = []
        section_b_raw: List[Dict[str, Any]] = []
        disqualified_raw: List[Dict[str, Any]] = []

        for d in determinations:
            is_prov = d.scheme_id in PROVISIONAL_SCHEMES
            gov = apply_governance_safeguard(d, sid, profile, is_prov=is_prov)

            if gov["allow_numerical_scoring"] and gov["presentation_section"].startswith(
                "Section A"
            ):
                section_a_raw.append(gov)
            elif gov["presentation_section"].startswith("Section B"):
                section_b_raw.append(gov)
            else:
                disqualified_raw.append(gov)

        # Rank Section A candidates
        sec_a_scheme_ids = [item["scheme_id"] for item in section_a_raw]
        ranking_method = "None"
        ml_used = False

        if sec_a_scheme_ids:
            if self.has_ml_model and not force_heuristic:
                try:
                    # Construct feature matrix for Section A candidates
                    candidate_sets = {sid: sec_a_scheme_ids}
                    feature_df = build_feature_rows_v12(
                        [profile], self.scheme_lookup, candidate_sets, ablation=1
                    )
                    preds = self.ml_model.predict(feature_df)
                    score_map = dict(zip(feature_df["scheme_id"], preds))

                    # Attach predicted score to items
                    for item in section_a_raw:
                        item["score"] = float(score_map.get(item["scheme_id"], 0.0))

                    # Sort by score descending, then scheme_id ascending
                    section_a_raw.sort(
                        key=lambda x: (-x.get("score", 0.0), x["scheme_id"])
                    )
                    ranking_method = "Benchmark v1.2 ML Model (HistGradientBoostingRegressor)"
                    ml_used = True
                except Exception as e:
                    # Fallback to heuristic if prediction fails
                    ranking_method = f"Heuristic Baseline (Fallback — Error in ML inference: {e})"
                    h_ranked = rank_heuristic_v12(
                        sid, sec_a_scheme_ids, profile["immediate_need"]
                    )
                    for item in section_a_raw:
                        item["score"] = float(
                            compute_heuristic_score_v12(
                                item["scheme_id"], profile["immediate_need"]
                            )
                        )
                    section_a_raw.sort(
                        key=lambda x: (
                            -compute_heuristic_score_v12(
                                x["scheme_id"], profile["immediate_need"]
                            ),
                            x["scheme_id"],
                        )
                    )
            else:
                # Use heuristic baseline
                fallback_reason = (
                    "User requested heuristic baseline"
                    if force_heuristic
                    else f"ML model unavailable ({self.model_load_error})"
                )
                ranking_method = f"Heuristic Baseline (Fallback — {fallback_reason})"
                for item in section_a_raw:
                    item["score"] = float(
                        compute_heuristic_score_v12(
                            item["scheme_id"], profile["immediate_need"]
                        )
                    )
                section_a_raw.sort(
                    key=lambda x: (
                        -compute_heuristic_score_v12(
                            x["scheme_id"], profile["immediate_need"]
                        ),
                        x["scheme_id"],
                    )
                )

        # Enrich Section A recommendations with metadata and explainability
        section_a_enriched: List[Dict[str, Any]] = []
        for idx, item in enumerate(section_a_raw, start=1):
            sch_meta = self.scheme_master_by_id.get(item["scheme_id"], {})
            sch_lookup = self.scheme_lookup.get(item["scheme_id"], {})

            rationale = self._generate_ranking_rationale(
                profile=profile,
                scheme_id=item["scheme_id"],
                sch_meta=sch_meta,
                sch_lookup=sch_lookup,
                ml_used=ml_used,
                score=item.get("score", 0.0),
            )

            # Combine statutory general disclaimer with any specific claim clause
            base_claim = sch_meta.get("claim_disclaimer") or ""
            statutory_notice = (
                "Statutory Disclaimer: Recommendation does not guarantee subsidy approval "
                "or fund disbursement. Sanction is contingent on official taluk-level application "
                "verification, biometric e-KYC, and budget quota availability."
            )
            if base_claim and base_claim != "None":
                full_disclaimer = f"{statutory_notice} (Scheme note: {base_claim})"
            else:
                full_disclaimer = statutory_notice

            section_a_enriched.append(
                {
                    "rank": idx,
                    "scheme_id": item["scheme_id"],
                    "scheme_name": item["scheme_name"],
                    "score": round(item.get("score", 0.0), 4),
                    "department": sch_meta.get("department", "Not specified"),
                    "benefit_type": sch_meta.get("benefit_type", "Not specified"),
                    "benefit_rate": sch_meta.get("benefit_rate", "As per guidelines"),
                    "maximum_benefit": sch_meta.get("maximum_benefit", "As per guidelines"),
                    "official_source_url": sch_meta.get("official_source_url", ""),
                    "official_document_url": sch_meta.get("official_document_url", ""),
                    "required_documents": sch_meta.get("required_documents", []),
                    "application_period": sch_meta.get("application_period", "Ongoing / Seasonal"),
                    "ranking_rationale": rationale,
                    "governance_note": item.get("governance_note", ""),
                    "statutory_disclaimer": full_disclaimer,
                }
            )

        # Enrich Section B advisory candidates (NO numerical scores)
        section_b_enriched: List[Dict[str, Any]] = []
        for item in section_b_raw:
            sch_meta = self.scheme_master_by_id.get(item["scheme_id"], {})
            section_b_enriched.append(
                {
                    "scheme_id": item["scheme_id"],
                    "scheme_name": item["scheme_name"],
                    "score": None,  # Strictly numerical scoring disabled
                    "presentation_section": item["presentation_section"],
                    "department": sch_meta.get("department", "Not specified"),
                    "benefit_type": sch_meta.get("benefit_type", "Not specified"),
                    "official_source_url": sch_meta.get("official_source_url", ""),
                    "governance_note": item.get("governance_note", ""),
                    "missing_verifications": item.get("missing_verifications", []),
                    "required_documents": sch_meta.get("required_documents", []),
                    "advisory_warning": (
                        "Section B Advisory Only: Numerical scoring is disabled under benchmark governance "
                        "safeguards because statutory documentation (e.g. Bhoomi mutation, death certificate, "
                        "seasonal notified unit order, or corporation administrative circular) is pending."
                    ),
                }
            )

        # Enrich Disqualified candidates
        disqualified_enriched: List[Dict[str, Any]] = []
        for item in disqualified_raw:
            sch_meta = self.scheme_master_by_id.get(item["scheme_id"], {})
            disqualified_enriched.append(
                {
                    "scheme_id": item["scheme_id"],
                    "scheme_name": item["scheme_name"],
                    "disqualifying_factors": item.get("disqualifying_factors", []),
                    "rule_keys_fired": item.get("rule_keys_fired", []),
                    "official_source_url": sch_meta.get("official_source_url", ""),
                }
            )

        return {
            "success": True,
            "scenario_id": sid,
            "profile_summary": {
                "district": profile["district"],
                "zone": f"{profile['zone_id']} ({profile['agro_climatic_zone']})",
                "crop": f"{profile['crop_primary']} (Secondary: {profile.get('crop_secondary') or 'None'})",
                "land_size_acres": profile["land_size_acres"],
                "land_type": profile["land_type"],
                "farmer_category": profile["farmer_category"],
                "social_category": profile["social_category"],
                "immediate_need": profile["immediate_need"],
                "annual_income_lakh": profile["annual_family_income_lakh"],
                "pure_tenant": profile.get("is_pure_tenant_without_land_title", False),
            },
            "ranking_method": ranking_method,
            "counts": {
                "total": len(determinations),
                "section_a": len(section_a_enriched),
                "section_b": len(section_b_enriched),
                "disqualified": len(disqualified_enriched),
            },
            "section_a": section_a_enriched,
            "section_b": section_b_enriched,
            "disqualified": disqualified_enriched,
        }

    def _generate_ranking_rationale(
        self,
        profile: Dict[str, Any],
        scheme_id: str,
        sch_meta: Dict[str, Any],
        sch_lookup: Dict[str, Any],
        ml_used: bool,
        score: float,
    ) -> List[str]:
        """
        Generate explainable ranking factors based on verified agronomic,
        economic, and operational compatibility.
        """
        factors: List[str] = []
        immediate_need = profile.get("immediate_need", "")
        cnd = profile.get("compound_need_details", {}) or {}
        acute_crisis = cnd.get("primary_acute_crisis", "")
        secondary_constraints = cnd.get("secondary_constraints", [])
        land_size = profile.get("land_size_acres", 0.0)
        water_source = (profile.get("water_and_irrigation") or {}).get(
            "operational_water_source", ""
        )

        # 1. Immediate need alignment
        need_keywords = {
            "RAINWATER_HARVESTING": ["SCH005"],
            "SOIL_HEALTH_AND_FERTILIZER": ["SCH009"],
            "FARM_MECHANIZATION": ["SCH004"],
            "CROP_INSURANCE": ["SCH002"],
            "SOLAR_PUMP_INSTALLATION": ["SCH006"],
            "DEBT_RELIEF": ["SCH008_KA_COOP", "SCH008_CENTRAL_KCC_MISS", "SCH008_KCC_MISS"],
            "PROTECTED_HORTICULTURE": ["SCH007"],
            "POST_HARVEST_STORAGE": ["SCH007"],
        }
        matching_schemes = need_keywords.get(immediate_need, [])
        if scheme_id in matching_schemes:
            factors.append(
                f"Directly targets the farmer's stated immediate need ({immediate_need.replace('_', ' ').title()})."
            )

        # 2. Acute crisis alignment (if different from immediate need)
        if acute_crisis and acute_crisis != immediate_need:
            crisis_schemes = need_keywords.get(acute_crisis, [])
            if scheme_id in crisis_schemes:
                factors.append(
                    f"Addresses the underlying acute agronomic crisis ({acute_crisis.replace('_', ' ').title()})."
                )

        # 3. Landholding fit
        min_land = sch_lookup.get("min_land_acres")
        max_land = sch_lookup.get("max_land_acres")
        if min_land is not None or max_land is not None:
            min_str = f"{min_land} ac" if min_land is not None else "0 ac"
            max_str = f"{max_land} ac" if max_land is not None else "No ceiling"
            factors.append(
                f"Applicant's operational holding ({land_size} acres) cleanly aligns with scheme bounds [{min_str} - {max_str}]."
            )
        else:
            factors.append("Universal land eligibility — applies to all operational landholding sizes.")

        # 4. Water and irrigation compatibility
        irrig_req = sch_meta.get("irrigation_requirements", "")
        if "None" in irrig_req or "Rainfed" in irrig_req:
            factors.append("Suitable for rainfed/dryland cultivation without mandatory energized borewell.")
        elif any(x in water_source for x in ["Borewell", "Open well", "Canal"]):
            factors.append(f"Compatible with farmer's available water source ({water_source}).")

        # 5. Secondary constraint mitigation
        if secondary_constraints:
            if scheme_id == "SCH001" and any("working capital" in str(sc).lower() or "liquidity" in str(sc).lower() for sc in secondary_constraints):
                factors.append("Unconditional cash transfer assists in mitigating acute working capital depletion.")
            elif scheme_id in ["SCH008_CENTRAL_KCC_MISS", "SCH008_KA_COOP"] and any("credit" in str(sc).lower() for sc in secondary_constraints):
                factors.append("Subsidized crop credit mitigates secondary credit market constraints.")

        # 6. Scoring note
        if ml_used:
            factors.append(
                f"Ranked by Benchmark v1.2 ML model (Predicted relevance score: {score:.3f} on 0-3 scale)."
            )
        else:
            factors.append(
                f"Ranked by registered heuristic baseline priority (Heuristic score: {score:.1f})."
            )

        return factors
