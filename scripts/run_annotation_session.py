"""
run_annotation_session.py
-------------------------
Availability-blinded expert annotation CLI for the Farmer Scheme Recommendation Pilot.

PROTOCOL (enforced by this script):
  Phase 1 - Relevance scoring (availability information is HIDDEN)
    For each scenario, expert reads the farmer profile and each eligible scheme,
    then assigns a relevance score (0-3) and a confidence level (H/M/L).
    Scores are locked before Phase 2 begins.

  Phase 2 - Availability & policy review (availability revealed AFTER Phase 1 lock)
    The availability state is shown, and the expert reviews Section B
    (provisional / REQUIRES_VERIFICATION schemes) with qualitative feedback only.

Usage:
    python scripts/run_annotation_session.py --expert-id E1 --pilot-results research/dataset_research/pilot_execution_results.json

Output:
    data/annotations/<expert_id>_annotation_session.json
    data/annotations/<expert_id>_annotation_session.csv  (flat, for agreement analysis)
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Rating Rubric (read-only display)
# ---------------------------------------------------------------------------
RUBRIC = """
=============================================================
  RELEVANCE RATING RUBRIC (0-3 scale)
=============================================================
  3 - HIGHLY RELEVANT / HIGH PRIORITY
      Directly addresses the farmer's primary stated need.
      Provides immediate, high-impact practical benefit.
      Should appear in the top-3 recommendation cards.

  2 - RELEVANT / SECONDARY PRIORITY
      Provides genuine practical benefit, but does not directly
      solve the urgent stated need. Valuable secondary recommendation.

  1 - MARGINALLY RELEVANT / LOW PRIORITY
      Technically applicable and eligible, but provides minor or
      distant value in the current context.

  0 - IRRELEVANT / NOT USEFUL
      Despite passing statutory eligibility, this scheme provides
      no meaningful practical benefit given the farmer's specific
      asset profile, crop, or situation.

IMPORTANT:
  - Score based on the farmer's stated need and profile ONLY.
  - Do NOT lower a score because the application window is closed.
  - Do NOT score schemes in Section B (REQUIRES_VERIFICATION).
=============================================================
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def prompt_score(prompt: str) -> int:
    """Prompt for a 0-3 integer score with validation."""
    while True:
        raw = input(prompt).strip()
        if raw in ("0", "1", "2", "3"):
            return int(raw)
        print("  [!] Please enter 0, 1, 2, or 3.")


def prompt_confidence(prompt: str) -> str:
    """Prompt for H / M / L confidence."""
    while True:
        raw = input(prompt).strip().upper()
        if raw in ("H", "M", "L", "HIGH", "MEDIUM", "LOW"):
            return raw[0]
        print("  [!] Please enter H (High), M (Medium), or L (Low).")


def prompt_text(prompt: str) -> str:
    raw = input(prompt).strip()
    return raw if raw else "(no comment)"


def print_separator(char: str = "-", width: int = 70):
    print(char * width)


def print_farmer_profile(scenario: Dict[str, Any]):
    print_separator("=")
    print(f"  FARMER SCENARIO PROFILE: {scenario['scenario_id']}")
    print_separator("=")
    print(f"  Location      : {scenario['district']}, Karnataka")
    print(f"  Primary Crop  : {scenario['crop_primary']}", end="")
    if scenario.get("crop_secondary"):
        print(f" | Secondary: {scenario['crop_secondary']}", end="")
    print()
    print(f"  Landholding   : {scenario['land_size_acres']} acres | {scenario['land_type']}")
    print(f"  Social Cat.   : {scenario['social_category']} | {scenario['farmer_category']}")
    assets = scenario.get("existing_assets", [])
    print(f"  Existing Assets: {', '.join(assets) if assets else 'None'}")
    print(f"  Annual Income  : Rs.{scenario['annual_family_income_lakh']} Lakh")
    print(f"  Farming Stage  : {scenario.get('farming_stage', 'N/A')} | {scenario.get('season', 'N/A')}")
    print(f"  Stated Need    : {scenario['immediate_need']}")
    print(f"  Farmer Query   : \"{scenario.get('kcc_query_text_example', '')}\"")
    print_separator("=")


def build_eligible_section_a(raw_determinations: List[Dict]) -> List[Dict]:
    """Return only ELIGIBLE schemes (not REQUIRES_VERIFICATION, not INELIGIBLE).
    Parent records are excluded if a child is ELIGIBLE (deduplication).
    Availability state is stripped for Phase 1."""
    eligible = [d for d in raw_determinations if d["status"] == "ELIGIBLE"]
    # Remove parent abstracts if any child is present
    child_parent_ids = {d["parent_scheme_id"] for d in eligible if d.get("parent_scheme_id")}
    section_a = [d for d in eligible if d["scheme_id"] not in child_parent_ids]
    return section_a


def build_requires_verification(raw_determinations: List[Dict]) -> List[Dict]:
    return [d for d in raw_determinations if d["status"] == "REQUIRES_VERIFICATION"]


# ---------------------------------------------------------------------------
# Phase 1: Relevance Scoring (availability-blinded)
# ---------------------------------------------------------------------------

def run_phase1(scenario_result: Dict) -> List[Dict]:
    """
    Presents Section A schemes WITHOUT availability information.
    Expert enters relevance score + confidence + reasoning.
    Returns list of annotation entries (relevance only, no availability).
    """
    scenario = scenario_result["scenario"]
    print_farmer_profile(scenario)
    print(RUBRIC)

    section_a = build_eligible_section_a(scenario_result["raw_determinations"])

    if not section_a:
        print("  [!] No ELIGIBLE schemes for this scenario in Section A.")
        return []

    print(f"\n  PHASE 1 — RELEVANCE SCORING (Availability is hidden)")
    print(f"  {len(section_a)} eligible scheme(s) to rate for {scenario['scenario_id']}\n")

    annotations = []
    for i, det in enumerate(section_a, 1):
        print_separator()
        print(f"  [{i}/{len(section_a)}] Scheme: {det['scheme_id']} — {det['scheme_name']}")
        print(f"  Engine Eligibility Rationale: {det['reason']}")
        print()

        score = prompt_score("  Your Relevance Score (0/1/2/3): ")
        confidence = prompt_confidence("  Your Confidence (H / M / L): ")
        reasoning = prompt_text("  Expert Reasoning (1-2 sentences): ")
        print()

        annotations.append({
            "scenario_id": scenario["scenario_id"],
            "scheme_id": det["scheme_id"],
            "scheme_name": det["scheme_name"],
            "record_type": det.get("record_type", ""),
            "parent_scheme_id": det.get("parent_scheme_id"),
            "engine_eligibility_status": det["status"],
            "engine_reason": det["reason"],
            # Phase 1 outputs
            "phase": "PHASE1_RELEVANCE",
            "expert_relevance_score": score,
            "expert_confidence": confidence,
            "expert_reasoning": reasoning,
            # Phase 2 fields — filled in later
            "availability_state": None,
            "is_actionable": None,
            "expert_availability_comment": None,
        })

    print(f"\n  [Phase 1 complete for {scenario['scenario_id']}]")
    print(f"  Scores entered: {[a['expert_relevance_score'] for a in annotations]}")

    confirm = input("  Lock these scores and proceed to Phase 2? (yes/no): ").strip().lower()
    while confirm not in ("yes", "no", "y", "n"):
        confirm = input("  Please type 'yes' or 'no': ").strip().lower()
    if confirm in ("no", "n"):
        print("  [!] Phase 1 NOT locked. Repeating scoring for this scenario.")
        return run_phase1(scenario_result)  # recursive retry

    return annotations


# ---------------------------------------------------------------------------
# Phase 2: Availability reveal + Section B review
# ---------------------------------------------------------------------------

def run_phase2(scenario_result: Dict, phase1_annotations: List[Dict]) -> List[Dict]:
    """
    Reveals availability states for Section A schemes already scored.
    Presents Section B (REQUIRES_VERIFICATION) for qualitative feedback only.
    Updates phase1_annotations in-place and appends Section B entries.
    """
    scenario = scenario_result["scenario"]
    raw = scenario_result["raw_determinations"]

    # Build availability lookup from raw results
    avail_lookup = {d["scheme_id"]: d for d in raw}

    print_separator("=")
    print(f"  PHASE 2 — AVAILABILITY REVEAL + SECTION B REVIEW")
    print(f"  Scenario: {scenario['scenario_id']}")
    print_separator("=")
    print("  Your Phase 1 relevance scores are now LOCKED.\n")
    print("  Now we reveal the current operational availability for each scheme you scored.")
    print("  You may add a short comment on availability implications.\n")

    all_entries = []

    # Update availability for Section A schemes
    for ann in phase1_annotations:
        det = avail_lookup.get(ann["scheme_id"], {})
        avail_state = det.get("availability_state", "Availability unknown — confirmation required")
        is_actionable = det.get("is_actionable", None)

        print_separator()
        print(f"  Scheme: {ann['scheme_id']} — {ann['scheme_name']}")
        print(f"  Your Phase 1 Relevance Score: {ann['expert_relevance_score']} ({['Irrelevant','Marginal','Relevant','Highly Relevant'][ann['expert_relevance_score']]})")
        print(f"  [REVEALED] Availability State: {avail_state}")
        print(f"  [REVEALED] Is Actionable Now : {'Yes' if is_actionable else 'No/Unknown'}")
        print()

        avail_comment = prompt_text("  Availability comment (press Enter to skip): ")

        updated = dict(ann)
        updated["phase"] = "COMPLETE"
        updated["availability_state"] = avail_state
        updated["is_actionable"] = is_actionable
        updated["expert_availability_comment"] = avail_comment
        all_entries.append(updated)

    # Section B — REQUIRES_VERIFICATION
    section_b = build_requires_verification(scenario_result["raw_determinations"])
    if section_b:
        print_separator("=")
        print(f"  SECTION B: REQUIRES_VERIFICATION SCHEMES (do NOT assign a relevance score)")
        print_separator("=")
        for det in section_b:
            print(f"\n  Scheme: {det['scheme_id']} — {det['scheme_name']}")
            print(f"  Engine Note: {det['reason']}")
            print()
            policy_feedback = prompt_text(
                "  Policy feedback (should this be conditionally recommended pending verification?): "
            )
            all_entries.append({
                "scenario_id": scenario["scenario_id"],
                "scheme_id": det["scheme_id"],
                "scheme_name": det["scheme_name"],
                "record_type": det.get("record_type", ""),
                "parent_scheme_id": det.get("parent_scheme_id"),
                "engine_eligibility_status": det["status"],
                "engine_reason": det["reason"],
                "phase": "SECTION_B_QUALITATIVE",
                "expert_relevance_score": None,  # Never scored numerically
                "expert_confidence": None,
                "expert_reasoning": None,
                "availability_state": det.get("availability_state"),
                "is_actionable": det.get("is_actionable"),
                "expert_availability_comment": policy_feedback,
            })

    return all_entries


# ---------------------------------------------------------------------------
# Main session runner
# ---------------------------------------------------------------------------

def run_session(expert_id: str, pilot_results_path: str, resume_from: Optional[int] = None):
    """Run a complete annotation session for all 10 pilot scenarios."""
    with open(pilot_results_path, encoding="utf-8") as f:
        all_results = json.load(f)

    output_dir = Path("data/annotations")
    output_dir.mkdir(parents=True, exist_ok=True)

    session_json_path = output_dir / f"{expert_id}_annotation_session.json"
    session_csv_path = output_dir / f"{expert_id}_annotation_session.csv"

    # Load existing session if resuming
    completed_scenarios = set()
    all_entries: List[Dict] = []
    if session_json_path.exists():
        with open(session_json_path, encoding="utf-8") as f:
            existing = json.load(f)
        all_entries = existing.get("annotations", [])
        completed_scenarios = {e["scenario_id"] for e in all_entries}
        print(f"\n  [Resume] Found existing session for {expert_id}.")
        print(f"  Completed scenarios: {sorted(completed_scenarios)}")

    print_separator("=")
    print(f"  EXPERT ANNOTATION SESSION")
    print(f"  Expert ID   : {expert_id}")
    print(f"  Date (IST)  : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Pilot Freeze: pilot-v1.0 (commit 7724fa7)")
    print(f"  Scenarios   : {len(all_results)}")
    print_separator("=")
    print()
    print("  PROTOCOL REMINDER:")
    print("  1. Score relevance independently of whether the scheme is currently open.")
    print("  2. Availability information will be hidden until you lock Phase 1 scores.")
    print("  3. Do not discuss scores with other annotators before submitting.")
    print("  4. Section B items get qualitative feedback only — no numerical score.")
    print()
    input("  Press Enter to begin...\n")

    start_idx = 0
    if resume_from is not None:
        start_idx = resume_from

    for idx, scenario_result in enumerate(all_results):
        sid = scenario_result["scenario"]["scenario_id"]

        if sid in completed_scenarios:
            print(f"\n  [Skip] {sid} already annotated. Skipping.")
            continue

        print(f"\n\n{'#'*70}")
        print(f"  SCENARIO {idx + 1} of {len(all_results)}: {sid}")
        print(f"{'#'*70}\n")

        # Phase 1: relevance (availability blinded)
        phase1_anns = run_phase1(scenario_result)

        # Phase 2: availability reveal + Section B
        complete_anns = run_phase2(scenario_result, phase1_anns)

        all_entries.extend(complete_anns)

        # Save after each scenario (checkpoint)
        session_data = {
            "expert_id": expert_id,
            "pilot_version": "pilot-v1.0",
            "git_commit": "7724fa7",
            "session_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed_scenarios": sorted({e["scenario_id"] for e in all_entries}),
            "annotations": all_entries,
        }
        with open(session_json_path, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        print(f"\n  [Saved] Checkpoint saved to {session_json_path}")

    # Write flat CSV
    if all_entries:
        fieldnames = [
            "expert_id", "scenario_id", "scheme_id", "scheme_name",
            "engine_eligibility_status", "phase",
            "expert_relevance_score", "expert_confidence",
            "expert_reasoning", "expert_availability_comment",
            "availability_state", "is_actionable",
        ]
        with open(session_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for entry in all_entries:
                row = {"expert_id": expert_id, **entry}
                writer.writerow(row)
        print(f"\n  [Done] Flat CSV saved to {session_csv_path}")

    print_separator("=")
    print(f"  SESSION COMPLETE — {expert_id}")
    phase1_only = [e for e in all_entries if e.get("phase") == "COMPLETE" and e.get("expert_relevance_score") is not None]
    print(f"  Total Section A ratings  : {len(phase1_only)}")
    print(f"  Scenarios annotated      : {len({e['scenario_id'] for e in all_entries})}")
    print_separator("=")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Availability-blinded expert annotation CLI for the Farmer Scheme Pilot."
    )
    parser.add_argument(
        "--expert-id", "-e", required=True,
        help="Unique expert identifier (e.g. E1, E2, E3). Used to name the output file."
    )
    parser.add_argument(
        "--pilot-results", "-p",
        default="research/dataset_research/pilot_execution_results.json",
        help="Path to pilot_execution_results.json."
    )
    parser.add_argument(
        "--resume-from", "-r", type=int, default=None,
        help="Zero-based scenario index to resume from (skips already-annotated scenarios automatically)."
    )
    args = parser.parse_args()

    if not os.path.exists(args.pilot_results):
        print(f"[ERROR] Pilot results file not found: {args.pilot_results}")
        sys.exit(1)

    run_session(args.expert_id, args.pilot_results, args.resume_from)


if __name__ == "__main__":
    main()
