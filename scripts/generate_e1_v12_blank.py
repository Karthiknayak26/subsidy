import csv
import json
from pathlib import Path

REPO_ROOT = Path("C:/Users/User/Desktop/subsidy/farmer-benefit-ml")

# Load v1.2 candidate generation results
with open(REPO_ROOT / "data/benchmarks/v1.2/candidate_generation_results.json", 'r') as f:
    candidate_results = json.load(f)

TEMPLATE_COLUMNS = [
    "scenario_id", "scheme_id", "scheme_name", "rater_id",
    "relevance_score", "relevance_rationale", "complementarity_notes",
]

# Generate E1 blank template
e1_rows = []
for sid in sorted(candidate_results.keys()):
    r = candidate_results[sid]
    for c in r.get("section_a_candidates", []):
        e1_rows.append({
            "scenario_id": sid,
            "scheme_id": c["scheme_id"],
            "scheme_name": c["scheme_name"],
            "rater_id": "E1",
            "relevance_score": "",
            "relevance_rationale": "",
            "complementarity_notes": "",
        })

e1_path = REPO_ROOT / "data" / "annotations" / "benchmark_v1.2" / "E1_v1.2_blank.csv"
with open(e1_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=TEMPLATE_COLUMNS)
    writer.writeheader()
    writer.writerows(e1_rows)
print(f"Wrote {e1_path} ({len(e1_rows)} rows)")
