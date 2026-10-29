import csv
from pathlib import Path
from collections import Counter

REPO_ROOT = Path("C:/Users/User/Desktop/subsidy/farmer-benefit-ml")
ann_dir = REPO_ROOT / "data" / "annotations" / "benchmark_v1.2"

print("=== E2 Blank Template Analysis ===")
with open(ann_dir / "E2_v1.2_blank.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    
print(f"Total rows: {len(rows)}")
print(f"Columns: {reader.fieldnames}")

# Check rater IDs
rater_ids = set(r["rater_id"] for r in rows)
print(f"Rater IDs: {rater_ids}")

# Check score values
scores = [r["relevance_score"] for r in rows]
score_counts = Counter(scores)
print(f"Score distribution: {dict(score_counts)}")
print(f"All scores valid (0-3): {all(s in ('0','1','2','3') for s in scores)}")

# Check for blank scores
blank_scores = [r for r in rows if r["relevance_score"].strip() == ""]
print(f"Blank scores: {len(blank_scores)}")

# Check for missing rationales
blank_rat = [r for r in rows if r["relevance_rationale"].strip() == ""]
print(f"Blank rationales: {len(blank_rat)}")

# Check for duplicate pairs
pairs = [(r["scenario_id"], r["scheme_id"]) for r in rows]
print(f"Total pairs: {len(pairs)}, Unique pairs: {len(set(pairs))}")
duplicates = len(pairs) - len(set(pairs))
print(f"Duplicate pairs: {duplicates}")

# Check scenario range
scenario_ids = sorted(set(r["scenario_id"] for r in rows))
print(f"Unique scenarios: {len(scenario_ids)}")
print(f"Scenario ID range: {scenario_ids[0]} to {scenario_ids[-1]}")
print(f"Sequential IDs: {scenario_ids == [f'S{i:03d}' for i in range(131, 131+len(scenario_ids))]}")
