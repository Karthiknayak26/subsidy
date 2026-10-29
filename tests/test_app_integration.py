"""
tests/test_app_integration.py
------------------------------
End-to-end integration tests for the Farmer Scheme Recommendation Application layer:
1. RecommendationService lifecycle and model loading
2. Input validation (positive paths and rejection of invalid/negative inputs)
3. End-to-end recommendation flow across all synthetic demo profiles
4. Strict Section A vs Section B governance decoupling (scoring disabled in Section B)
5. Statutory exclusion boundary enforcement (income tax, grid IP set, pure tenancy)
6. Heuristic baseline fallback mechanism (forced and graceful when model missing)
7. Candidate set disjointness invariants
"""

from pathlib import Path
from typing import Any, Dict

import pytest

from src.app.demo_profiles import DEMO_PROFILES
from src.app.service import RecommendationService


@pytest.fixture(scope="module")
def service() -> RecommendationService:
    return RecommendationService()


# ── 1. Lifecycle and Initialization ──────────────────────────────────────────

def test_service_initialization(service: RecommendationService):
    """Test that the service initializes engine, schemes, and loads v1.2 model."""
    assert len(service.schemes) == 16
    assert len(service.scheme_lookup) == 16
    assert service.has_ml_model is True
    assert service.model_load_error is None


# ── 2. Input Validation ───────────────────────────────────────────────────────

def test_input_validation_positive(service: RecommendationService):
    """Test that valid input passes validation and is properly normalized."""
    raw = {
        "district": "Yadgir",
        "crop_primary": "Bengalgram",
        "land_size_acres": 2.5,
        "land_type": "Dryland (Rainfed)",
        "social_category": "SC",
        "farmer_category": "Small (2.5-5.0 acres)",
        "immediate_need": "RAINWATER_HARVESTING",
        "annual_family_income_lakh": 1.2,
    }
    valid, errors, cleaned = service.validate_inputs(raw)
    assert valid is True
    assert len(errors) == 0
    assert cleaned["zone_id"] == "Z1"
    assert cleaned["land_size_acres"] == 2.5
    assert cleaned["annual_family_income_lakh"] == 1.2
    assert cleaned["scenario_id"] == "FARMER_USER_001"


def test_input_validation_negative_land(service: RecommendationService):
    """Test that negative land size is rejected."""
    raw = {
        "district": "Yadgir",
        "crop_primary": "Bengalgram",
        "land_size_acres": -1.5,
        "land_type": "Dryland (Rainfed)",
        "social_category": "SC",
        "farmer_category": "Small (2.5-5.0 acres)",
        "immediate_need": "RAINWATER_HARVESTING",
    }
    valid, errors, _ = service.validate_inputs(raw)
    assert valid is False
    assert any("negative" in e.lower() and "land" in e.lower() for e in errors)


def test_input_validation_negative_income(service: RecommendationService):
    """Test that negative income is rejected."""
    raw = {
        "district": "Bidar",
        "crop_primary": "Paddy",
        "land_size_acres": 2.0,
        "land_type": "Canal-irrigated",
        "social_category": "General (OC)",
        "farmer_category": "Marginal (1.0-2.5 acres)",
        "immediate_need": "SOIL_HEALTH_AND_FERTILIZER",
        "annual_family_income_lakh": -0.5,
    }
    valid, errors, _ = service.validate_inputs(raw)
    assert valid is False
    assert any("negative" in e.lower() and "income" in e.lower() for e in errors)


def test_input_validation_missing_required_fields(service: RecommendationService):
    """Test that omitting required fields generates specific errors."""
    raw: Dict[str, Any] = {}
    valid, errors, _ = service.validate_inputs(raw)
    assert valid is False
    err_text = " ".join(errors).lower()
    assert "district is required" in err_text
    assert "crop is required" in err_text
    assert "land size" in err_text
    assert "land type" in err_text
    assert "social category" in err_text
    assert "farmer category" in err_text
    assert "immediate" in err_text


# ── 3. End-to-End Recommendations Across Demo Profiles ────────────────────────

@pytest.mark.parametrize("preset_key", list(DEMO_PROFILES.keys()))
def test_demo_profiles_end_to_end(service: RecommendationService, preset_key: str):
    """Test full recommendation pipeline for each pre-configured demo scenario."""
    profile = DEMO_PROFILES[preset_key]["profile"]
    res = service.recommend(profile, force_heuristic=False)

    assert res["success"] is True, f"Failed for preset {preset_key}: {res.get('errors')}"
    counts = res["counts"]
    assert counts["total"] == 16
    assert counts["section_a"] + counts["section_b"] + counts["disqualified"] == 16
    assert "HistGradientBoostingRegressor" in res["ranking_method"]

    # Invariants for Section A
    sec_a = res["section_a"]
    for idx, item in enumerate(sec_a, start=1):
        assert item["rank"] == idx
        assert isinstance(item["score"], float)
        assert item["scheme_name"]
        assert item["department"]
        assert len(item["ranking_rationale"]) > 0
        assert "statutory" in item["statutory_disclaimer"].lower()

    # Invariants for Section B
    sec_b = res["section_b"]
    for b in sec_b:
        assert b["score"] is None, "Section B must NEVER have numerical scores!"
        assert "Section B" in b["presentation_section"]
        assert "advisory" in b["advisory_warning"].lower()
        assert b["governance_note"]

    # Invariants for Disqualified
    disq = res["disqualified"]
    for d in disq:
        assert len(d["disqualifying_factors"]) > 0 or len(d["rule_keys_fired"]) > 0


# ── 4. Statutory Exclusion Boundary Tests ─────────────────────────────────────

def test_exclusion_boundary_tax_and_grid(service: RecommendationService):
    """
    Test negative exclusion boundary:
    Income tax payer with grid IP set MUST be barred from PM-KISAN and PM-KUSUM B.
    """
    profile = DEMO_PROFILES["DEMO_EXCLUSION_BOUNDARY"]["profile"]
    res = service.recommend(profile)
    assert res["success"] is True

    sec_a_ids = [s["scheme_id"] for s in res["section_a"]]
    disq_ids = [s["scheme_id"] for s in res["disqualified"]]

    # PM-KISAN must be disqualified due to income tax
    assert "SCH001" not in sec_a_ids, "PM-KISAN must not be in Section A for tax payer"
    assert "SCH001" in disq_ids, "PM-KISAN must be disqualified for tax payer"

    pmk_item = next(d for d in res["disqualified"] if d["scheme_id"] == "SCH001")
    assert any("income tax" in f.lower() for f in pmk_item["disqualifying_factors"])

    # PM-KUSUM B must be disqualified due to grid connectivity
    assert "SCH006" not in sec_a_ids, "PM-KUSUM B must not be in Section A for grid-connected farmer"
    assert "SCH006" in disq_ids, "PM-KUSUM B must be disqualified for grid-connected farmer"


def test_tenant_statutory_exclusion(service: RecommendationService):
    """
    Test that pure tenants without land title (DEMO_S131) are excluded from PM-KISAN
    and tenant credit is routed to Section B.
    """
    profile = DEMO_PROFILES["DEMO_S131"]["profile"]
    res = service.recommend(profile)
    assert res["success"] is True

    sec_a_ids = [s["scheme_id"] for s in res["section_a"]]
    sec_b_ids = [s["scheme_id"] for s in res["section_b"]]
    disq_ids = [s["scheme_id"] for s in res["disqualified"]]

    # PM-KISAN barred for pure tenant
    assert "SCH001" not in sec_a_ids
    assert "SCH001" in disq_ids
    pmk_item = next(d for d in res["disqualified"] if d["scheme_id"] == "SCH001")
    assert any("pure tenant" in f.lower() or "sharecropper" in f.lower() for f in pmk_item["disqualifying_factors"])

    # Central KCC tenant route in Section B
    assert "SCH008_CENTRAL" in sec_b_ids


# ── 5. Heuristic Fallback Mechanism ───────────────────────────────────────────

def test_forced_heuristic_fallback(service: RecommendationService):
    """Test that forcing heuristic baseline disables ML and reports heuristic method."""
    profile = DEMO_PROFILES["DEMO_S131"]["profile"]
    res_heuristic = service.recommend(profile, force_heuristic=True)

    assert res_heuristic["success"] is True
    assert "Heuristic Baseline" in res_heuristic["ranking_method"]
    assert "HistGradientBoostingRegressor" not in res_heuristic["ranking_method"]

    # Scores must be computed from heuristic function
    for item in res_heuristic["section_a"]:
        assert isinstance(item["score"], float)


def test_model_missing_graceful_fallback(tmp_path: Path):
    """Test that when model artifact does not exist, service falls back gracefully."""
    fake_model_path = tmp_path / "non_existent_model.joblib"
    fallback_svc = RecommendationService(model_path=fake_model_path)

    assert fallback_svc.has_ml_model is False
    assert "not found" in fallback_svc.model_load_error.lower()

    profile = DEMO_PROFILES["DEMO_S132"]["profile"]
    res = fallback_svc.recommend(profile)

    assert res["success"] is True
    assert "Heuristic Baseline" in res["ranking_method"]
    assert len(res["section_a"]) > 0


# ── 6. Candidate Set Disjointness ─────────────────────────────────────────────

def test_presentation_sections_are_strictly_disjoint(service: RecommendationService):
    """
    Every evaluated scheme must belong to EXACTLY ONE category:
    Section A, Section B, or Disqualified.
    """
    for preset_key, pdata in DEMO_PROFILES.items():
        res = service.recommend(pdata["profile"])
        a_ids = set(s["scheme_id"] for s in res["section_a"])
        b_ids = set(s["scheme_id"] for s in res["section_b"])
        d_ids = set(s["scheme_id"] for s in res["disqualified"])

        assert a_ids.isdisjoint(b_ids), f"{preset_key}: Section A and Section B overlap: {a_ids & b_ids}"
        assert a_ids.isdisjoint(d_ids), f"{preset_key}: Section A and Disqualified overlap: {a_ids & d_ids}"
        assert b_ids.isdisjoint(d_ids), f"{preset_key}: Section B and Disqualified overlap: {b_ids & d_ids}"
        assert len(a_ids | b_ids | d_ids) == 16, f"{preset_key}: Total schemes != 16"

