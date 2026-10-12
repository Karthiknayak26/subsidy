"""
Smoke-test: generate synthetic two-expert annotations from pilot_execution_results.json
and run them through compute_agreement.py to verify the full pipeline works end-to-end.
Writes synthetic CSVs to data/annotations/ then calls generate_report() directly.

This is a development-only test; delete synthetic files before real annotation.
"""
import csv
import json
import random
import sys
from pathlib import Path

# Ensure project root on path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.compute_agreement import load_annotation_csvs, extract_section_a_ratings, generate_report

PILOT_RESULTS = Path("research/dataset_research/pilot_execution_results.json")
ANN_DIR = Path("data/annotations")
ANN_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)

with open(PILOT_RESULTS, encoding="utf-8") as f:
    all_results = json.load(f)

FIELDNAMES = [
    "expert_id", "scenario_id", "scheme_id", "scheme_name",
    "engine_eligibility_status", "phase",
    "expert_relevance_score", "expert_confidence",
    "expert_reasoning", "expert_availability_comment",
    "availability_state", "is_actionable",
]


def gen_score(true_score: int, noise: int = 1) -> int:
    """Generate a score close to true_score with some noise."""
    return max(0, min(3, true_score + random.randint(-noise, noise)))


# Assign a synthetic "ground truth" per (scenario, scheme)
ground_truth = {}
for result in all_results:
    sid = result["scenario"]["scenario_id"]
    need = result["scenario"]["immediate_need"]
    for det in result["raw_determinations"]:
        if det["status"] != "ELIGIBLE":
            continue
        # Rough heuristic: score based on need-scheme match
        scheme_id = det["scheme_id"]
        score = 1  # default marginal
        if need == "CROP_INSURANCE" and "PMFBY" in scheme_id:
            score = 3
        elif need == "SOLAR_PUMP_INSTALLATION" and "KUSUM" in scheme_id:
            score = 3
        elif need == "MICRO_IRRIGATION_SUPPORT" and "SCH003" in scheme_id:
            score = 3
        elif need == "PRODUCTION_CREDIT" and "KCC" in scheme_id:
            score = 3
        elif need == "RAINWATER_HARVESTING" and "SCH005" in scheme_id:
            score = 3
        elif need == "BOREWELL_IRRIGATION" and "AMBEDKAR" in scheme_id:
            score = 3
        elif need == "PROTECTED_HORTICULTURE" and "MIDH" in scheme_id:
            score = 3
        elif need == "INCOME_SUPPORT" and "SCH001" in scheme_id:
            score = 3
        elif "SCH009" in scheme_id:
            score = 1  # SHC is always low priority
        elif "SCH004" in scheme_id:
            score = 1  # machinery not urgent
        ground_truth[(sid, scheme_id)] = score


def write_synthetic_csv(expert_id: str, noise: int):
    rows = []
    for result in all_results:
        sid = result["scenario"]["scenario_id"]
        # Eligible non-parent schemes only
        eligible = [d for d in result["raw_determinations"] if d["status"] == "ELIGIBLE"]
        child_parents = {d["parent_scheme_id"] for d in eligible if d.get("parent_scheme_id")}
        section_a = [d for d in eligible if d["scheme_id"] not in child_parents]

        for det in section_a:
            key = (sid, det["scheme_id"])
            true_score = ground_truth.get(key, 1)
            expert_score = gen_score(true_score, noise)
            rows.append({
                "expert_id": expert_id,
                "scenario_id": sid,
                "scheme_id": det["scheme_id"],
                "scheme_name": det["scheme_name"],
                "engine_eligibility_status": "ELIGIBLE",
                "phase": "COMPLETE",
                "expert_relevance_score": expert_score,
                "expert_confidence": random.choice(["H", "M", "M", "L"]),
                "expert_reasoning": f"Synthetic reasoning for {det['scheme_id']}",
                "expert_availability_comment": "",
                "availability_state": det.get("availability_state", ""),
                "is_actionable": det.get("is_actionable", True),
            })

        # Section B
        for det in result["raw_determinations"]:
            if det["status"] == "REQUIRES_VERIFICATION":
                rows.append({
                    "expert_id": expert_id,
                    "scenario_id": sid,
                    "scheme_id": det["scheme_id"],
                    "scheme_name": det["scheme_name"],
                    "engine_eligibility_status": "REQUIRES_VERIFICATION",
                    "phase": "SECTION_B_QUALITATIVE",
                    "expert_relevance_score": None,
                    "expert_confidence": None,
                    "expert_reasoning": None,
                    "expert_availability_comment": "Should be conditionally recommended pending GO verification.",
                    "availability_state": det.get("availability_state", ""),
                    "is_actionable": None,
                })

    out_path = ANN_DIR / f"{expert_id}_annotation_session.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Written: {out_path} ({len(rows)} rows)")
    return rows


print("Generating synthetic annotations for E1 (low noise) and E2 (medium noise)...")
write_synthetic_csv("E1", noise=0)
write_synthetic_csv("E2", noise=1)

# Run agreement pipeline
print("\nRunning agreement computation...")
expert_data = load_annotation_csvs(str(ANN_DIR))
expert_ratings = extract_section_a_ratings(expert_data)
generate_report(expert_ratings, expert_data, "reports/pilot_agreement_report_SYNTHETIC_TEST.md")
print("\nSmoke test PASSED. Review: reports/pilot_agreement_report_SYNTHETIC_TEST.md")
print("Delete data/annotations/E1* and E2* before real expert annotation begins.")
