import csv
import os
from pathlib import Path

REPO_ROOT = Path("C:/Users/User/Desktop/subsidy/farmer-benefit-ml")
ann_dir = REPO_ROOT / "data" / "annotations" / "benchmark_v1.2"

# Check what files exist
print("=== Files in benchmark_v1.2/annotations ===")
for f in sorted(ann_dir.iterdir()):
    print(f"  {f.name}: {f.stat().st_size} bytes")

# Check E2 file
print("\n=== E2 Blank Template Analysis ===")
with open(ann_dir / "E2_v1.2_blank.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"  Total rows: {len(rows)}")
    print(f"  Columns: {reader.fieldnames}")
    
    # Check rater IDs
    rater_ids = set(r["rater_id"] for r in rows)
    print(f"  Rater IDs: {rater_ids}")
    
    # Check score values
    scores = [r["relevance_score"] for r in rows]
    score_counts = {}
    for s in scores:
        score_counts[s] = score_counts.get(s, 0) + 1
    print(f"  Score distribution: {score_counts}")
    
    # Check for missing/empty scores
    blank_scores = [r for r in e1_rows if r["relevance_score"].strip() == ""]
    print(f"  Blank scores: {len(blank_scores)}")
    
    # Check for missing rationales
    blank_rat = [r for r in e1_rows if r["relevance_rationale"].strip() == ""]
    print(f"  Blank rationales: {len(blank_rat)}")
    
    # Check for duplicate pairs
    pairs = [(r["scenario_id"], r["scheme_id"]) for r in e1_rows]
    dups = len(pairs) - len(set(pairs))
    print(f"  Total pairs: {len(pairs)}, Unique pairs: {len(set(pairs))}, Duplicates: {dups}")
    
    # Check scenario range
    scenario_ids = set(r["scenario_id"] for r in e1_rows)
    print(f"  Unique scenarios: {len(scenario_ids)}")
    print(f"  Scenario ID range: {min(scenario_ids)} to {max(scenario_id)}")
