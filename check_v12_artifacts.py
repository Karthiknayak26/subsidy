import csv
from pathlib import Path

ann_dir = Path("C:/Users/User/Desktop/subsidy/farmer-benefit-ml/data/annotations/benchmark_v1.2")

# Check E2 completed annotation file
print("=== E2_v1.2_blank.csv ===")
with open(ann_dir / "E2_v1.2_blank.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"Total rows: {len(rows)}")
    print(f"Columns: {reader.fieldnames}")
    print(f"First row: {dict(list(rows[0].items())[:6])}")
    scores = [r["relevance_score"] for r in rows]
    print(f"Unique scores: {sorted(set(scores))}")
    blank_scores = sum(1 for r in rows if r["relevance_score"].strip() == "")
    print(f"Blank scores: {blank_scores}")
    blank_rat = sum(1 for r in rows if r["relevance_rationale"].strip() == "")
    print(f"Blank rationales: {blank_rat}")
    pairs = [(r["scenario_id"], r["scheme_id"]) for r in rows]
    print(f"Total pairs: {len(pairs)}, Unique pairs: {len(set(pairs))}")
    sids = set(r["scenario_id"] for r in rows)
    print(f"Unique scenarios: {len(sids)}")
    print(f"Scenario range: {min(sids)} to {max(sids)}")

# Check scenario dossier
print("\n=== Scenario Context Dossier ===")
with open(ann_dir / "scenario_context_dossier.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"Total rows: {len(rows)}")
    print(f"Columns: {reader.fieldnames}")
    print(f"First row scenario_id: {rows[0]['scenario_id']}")
    print(f"First row immediate_need: {rows[0]['immediate_need']}")
    print(f"First row provenance_synthetic_attributes: {rows[0]['provenance_synthetic_attributes'][:80]}...")

# Check scheme evidence
print("\n=== Scheme Evidence ===")
with open(ann_dir / "scheme_evidence.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"Total rows: {len(rows)}")
    print(f"Columns: {reader.fieldnames}")
    for row in rows:
        print(f"  {row['scheme_id']}: {row['scheme_name'][:50]} | source: {row['source_references'][:80]}...")

# Check Section B packet
print("\n=== Section B Packet ===")
with open(ann_dir / "section_b_qualitative_review_packet.csv", 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"Total rows: {len(rows)}")
    print(f"Columns: {reader.fieldnames}")
    if 'relevance_score' in reader.fieldnames:
        print("WARNING: Section B has relevance_score column!")
    else:
        print("OK: No relevance_score column in Section B")
