import csv
import json
from pathlib import Path
from collections import Counter

REPO_ROOT = Path("C:/Users/User/Desktop/subsidy/farmer-benefit-ml")

# Load v1.2 candidate generation results
with open(REPO_ROOT / "data/benchmarks/v1.2/candidate_generation_results.json", 'r') as f:
    candidate_results = json.load(f)

TEMPLATE_COLUMNS = [
    "scenario_id",
    "scheme_id",
    "scheme_name",
    "rater_id",
    "relevance_score",
    "relevance_rationale",
    "complementarity_notes",
]

def build_blank_template(candidate_results: dict, rater_id: str) -> list[dict]:
    """Build a blank scoring template for a reviewer."""
    rows = []
    for sid in sorted(candidate_results.keys()):
        r = candidate_results[sid]
        for c in r.get("section_a_candidates", []):
            rows.append({
                "scenario_id": sid,
                "scheme_id": c["scheme_id"],
                "scheme_name": c["scheme_name"],
                "rater_id": rater_id,
                "relevance_score": "",
                "relevance_rationale": "",
                "complementarity_notes": "",
            })
    return rows

# Generate E1 blank template (E1 never submitted)
e1_rows = build_blank_template(candidate_results, "E1")
e1_path = REPO_ROOT / "data" / "annotations" / "benchmark_v1.2" / "E1_v1.2_blank.csv"
with open(e1_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=TEMPLATE_COLUMNS)
    writer.writeheader()
    writer.writerows(e1_rows)
print(f"Wrote {e1_path} ({len(e1_rows)} rows)")

# Generate E2 blank template (if E2 didn't submit)
e2_rows = build_blank_template(candidate_results, "E2")
e2_path = REPO_ROOT / "data" / "annotations" / "benchmark_v1.1" / "E2_v1.1_blank.csv"
with open(e2_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=TEMPLATE_COLUMNS)
    writer.writeheader()
    writer.writerows(e2_rows)
print(f"Wrote {e2_path} ({len(e2_rows)} rows)")

print(f"\nSummary:")
print(f"  E1 template rows: {len(e1_rows)}")
print(f"  E2 template rows: {len(e2_rows)}")
