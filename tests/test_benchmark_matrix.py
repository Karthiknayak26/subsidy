"""
Unit test for Benchmark v1.0.2 Scenario Assignment Matrix.
Validates all 8 quota and boundary dimensions:
1. Scenario count and ID continuity (60 scenarios, S011-S070)
2. Agro-climatic zone distribution (10 zones, 6 each)
3. Landholding classes (22 Marginal, 20 Small, 12 Medium, 6 Large) and exact boundaries
4. Social categories (15 SC, 10 ST, 10 OBC, 8 Minority, 17 GM)
5. Primary needs (6 each across 10 categories)
6. Tenure statuses (47 Pre-Feb 2019, 4 Post-Feb 2019 Inheritance, 5 Pure Tenant, 4 Unknown Title Status)
7. Community pool membership (3 Yes: S028, S052, S066; 57 No)
8. Land types (28 Dryland, 10 Canal-irrigated, 12 Borewell-irrigated, 6 Wetland/valley, 4 Hilly/terraced)
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath("."))
from research.dataset_research.validate_benchmark_matrix import scenarios, validate_matrix


def test_benchmark_matrix_all_dimensions():
    """Verify that the benchmark v1.0.2 matrix satisfies all declared quotas."""
    success = validate_matrix(scenarios)
    assert success is True, "Benchmark v1.0.2 assignment matrix failed one or more quota checks."


def test_boundary_cases_preserved():
    """Verify explicit boundary test cases are present and classified correctly."""
    # 2.5 acre boundary -> Small (>= 2.5 and <= 5.0)
    boundary_2_5 = [s for s in scenarios if s["total_holding"] == 2.5]
    assert len(boundary_2_5) >= 3, f"Expected >= 3 boundary test cases at 2.5 acres, found {len(boundary_2_5)}"
    for s in boundary_2_5:
        assert s["lclass"] == "Small", f"{s['sid']} at 2.5 ac must be classified Small"

    # 5.0 acre boundary -> Small (>= 2.5 and <= 5.0)
    boundary_5_0 = [s for s in scenarios if s["total_holding"] == 5.0]
    assert len(boundary_5_0) >= 2, f"Expected >= 2 boundary test cases at 5.0 acres, found {len(boundary_5_0)}"
    for s in boundary_5_0:
        assert s["lclass"] == "Small", f"{s['sid']} at 5.0 ac must be classified Small"

    # 10.0 acre boundary -> Medium (> 5.0 and <= 10.0)
    boundary_10_0 = [s for s in scenarios if s["total_holding"] == 10.0]
    assert len(boundary_10_0) >= 1, f"Expected >= 1 boundary test cases at 10.0 acres, found {len(boundary_10_0)}"
    for s in boundary_10_0:
        assert s["lclass"] == "Medium", f"{s['sid']} at 10.0 ac must be classified Medium"


def test_community_pool_clarifications():
    """Verify S028, S052, S066 community pool attributes and provisional status labeling."""
    pool_scenarios = {s["sid"]: s for s in scenarios if s["pool"].startswith("Yes")}
    assert set(pool_scenarios.keys()) == {"S028", "S052", "S066"}

    # S028: Devaraj Urs (OBC) provisional
    s028 = pool_scenarios["S028"]
    assert s028["social"] == "OBC"
    assert "Devaraj Urs" in s028["policy"]
    assert "REQUIRES_VERIFICATION" in s028["policy"]
    assert s028["qual_parcel"] == 3.0
    assert "9.0 ac" in s028["pool"]

    # S052: Devaraj Urs (OBC) provisional
    s052 = pool_scenarios["S052"]
    assert s052["social"] == "OBC"
    assert "Devaraj Urs" in s052["policy"]
    assert "REQUIRES_VERIFICATION" in s052["policy"]
    assert s052["qual_parcel"] == 4.0
    assert "12.0 ac" in s052["pool"]

    # S066: Ambedkar (SC)
    s066 = pool_scenarios["S066"]
    assert s066["social"] == "SC"
    assert "Ambedkar" in s066["policy"]
    assert s066["qual_parcel"] == 3.5
    assert "14.0 ac" in s066["pool"]
