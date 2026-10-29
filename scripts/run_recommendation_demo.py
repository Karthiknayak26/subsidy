"""
scripts/run_recommendation_demo.py
----------------------------------
Command-line demonstration runner for the Personalized Subsidy Recommender.
Enables instant demonstration of all synthetic benchmark profiles and
the two-desk triage architecture (frozen engine + v1.2 ML ranker).

Usage:
  python scripts/run_recommendation_demo.py --preset DEMO_S131
  python scripts/run_recommendation_demo.py --preset all
  python scripts/run_recommendation_demo.py --preset DEMO_EXCLUSION_BOUNDARY
  python scripts/run_recommendation_demo.py --preset DEMO_S131 --heuristic
"""

from __future__ import annotations

import argparse
import json
import os
import sys

# Suppress loky win32 core count warning on Windows
if "LOKY_MAX_CPU_COUNT" not in os.environ:
    os.environ["LOKY_MAX_CPU_COUNT"] = "4"

from pathlib import Path
from typing import Any, Dict

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.app.demo_profiles import DEMO_PROFILES
from src.app.service import RecommendationService


def print_banner() -> None:
    print("=" * 80)
    print("  KARNATAKA FARMER BENEFIT & SUBSIDY RECOMMENDATION SYSTEM")
    print("  Two-Desk Architecture: Deterministic Eligibility + Benchmark v1.2 ML Ranker")
    print("=" * 80)
    print("  DISCLAIMER: All demonstration profiles are SYNTHETIC BENCHMARK SCENARIOS.")
    print("  Recommendations do not guarantee statutory sanction or fund disbursement.")
    print("=" * 80)


def run_single_demo(
    svc: RecommendationService,
    preset_key: str,
    force_heuristic: bool = False,
    as_json: bool = False,
) -> bool:
    if preset_key not in DEMO_PROFILES:
        print(f"[ERROR] Preset '{preset_key}' not found. Available presets: {list(DEMO_PROFILES.keys())}")
        return False

    demo_info = DEMO_PROFILES[preset_key]
    profile = demo_info["profile"]

    print(f"\n>>> Running Demonstration Scenario: {preset_key}")
    print(f"    Title: {demo_info['title']}")
    print(f"    Context: {demo_info['description']}")
    print("-" * 80)

    result = svc.recommend(profile, force_heuristic=force_heuristic)

    if as_json:
        print(json.dumps(result, indent=2))
        return result["success"]

    if not result["success"]:
        print("[FAIL] Validation failed:")
        for err in result["errors"]:
            print(f"  - {err}")
        return False

    summary = result["profile_summary"]
    counts = result["counts"]

    print(f"  Profile Summary:")
    print(f"    District / Zone:    {summary['district']} / {summary['zone']}")
    print(f"    Landholding:        {summary['land_size_acres']} acres ({summary['land_type']})")
    print(f"    Crops:              {summary['crop']}")
    print(f"    Farmer Category:    {summary['farmer_category']} | Social: {summary['social_category']}")
    print(f"    Stated Immediate Need: {summary['immediate_need']}")
    print(f"    Family Income:      Rs. {summary['annual_income_lakh']} Lakhs/year")
    print(f"    Land Tenure:        {'Pure Tenant (No Title)' if summary['pure_tenant'] else 'Titleholder / Owner'}")

    print(f"\n  Two-Desk Triage Counts (Total Schemes Evaluated: {counts['total']}):")
    print(f"    [Desk 1] Section A Actionable: {counts['section_a']}")
    print(f"    [Desk 1] Section B Advisory:   {counts['section_b']}")
    print(f"    [Desk 1] Disqualified:        {counts['disqualified']}")
    print(f"    [Desk 2] Ranking Method:      {result['ranking_method']}")

    # Section A
    print("\n  " + "=" * 76)
    print("  SECTION A: CONFIRMED ACTIONABLE SCHEMES (Ranked by Personalization Model)")
    print("  " + "=" * 76)

    if not result["section_a"]:
        print("    No schemes qualified for Section A under statutory rules.")
    else:
        for item in result["section_a"]:
            print(f"\n    Rank #{item['rank']}: {item['scheme_name']} ({item['scheme_id']})")
            print(f"      Relevance Score:   {item['score']:.4f}")
            print(f"      Department:        {item['department']}")
            print(f"      Benefit Structure: {item['benefit_type']} | {item['benefit_rate']}")
            print("      Ranking Rationale:")
            for r in item["ranking_rationale"]:
                print(f"        * {r}")
            print(f"      Statutory Caveat:  {item['statutory_disclaimer'][:90]}...")

    # Section B
    print("\n  " + "-" * 76)
    print("  SECTION B: QUALITATIVE ADVISORY (Numerical Scoring Disabled)")
    print("  " + "-" * 76)

    if not result["section_b"]:
        print("    None.")
    else:
        for item in result["section_b"]:
            print(f"\n    * {item['scheme_name']} ({item['scheme_id']})")
            print(f"      Advisory Status:   {item['presentation_section']}")
            print(f"      Pending Evidence:  {'; '.join(item['missing_verifications']) if item['missing_verifications'] else 'None'}")
            print(f"      Governance Note:   {item['governance_note'][:100]}...")

    # Disqualified summary
    print("\n  " + "-" * 76)
    print(f"  DISQUALIFIED SCHEMES ({counts['disqualified']} schemes barred by statutory criteria)")
    print("  " + "-" * 76)
    disq_sample = result["disqualified"][:3]
    for item in disq_sample:
        reasons = "; ".join(item["disqualifying_factors"][:2])
        print(f"    * {item['scheme_name']}: {reasons}")
    if len(result["disqualified"]) > 3:
        print(f"      ... and {len(result['disqualified']) - 3} other schemes barred by statutory rules.")

    print("\n" + "=" * 80)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run demonstration of Personalized Scheme Recommendation System."
    )
    parser.add_argument(
        "--preset",
        type=str,
        default="DEMO_S131",
        help="Preset key to demonstrate (e.g. DEMO_S131, DEMO_S132, DEMO_S136, DEMO_S137, DEMO_EXCLUSION_BOUNDARY, or 'all').",
    )
    parser.add_argument(
        "--heuristic",
        action="store_true",
        help="Force heuristic baseline ranking instead of Benchmark v1.2 ML model.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON response.",
    )

    args = parser.parse_args()

    print_banner()
    svc = RecommendationService()
    print(f"  Service initialized. Model active: {svc.has_ml_model}")
    if not svc.has_ml_model:
        print(f"  Model load notice: {svc.model_load_error}")

    if args.preset.lower() == "all":
        success = True
        for pkey in DEMO_PROFILES:
            ok = run_single_demo(svc, pkey, force_heuristic=args.heuristic, as_json=args.json)
            if not ok:
                success = False
        sys.exit(0 if success else 1)
    else:
        ok = run_single_demo(svc, args.preset, force_heuristic=args.heuristic, as_json=args.json)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

