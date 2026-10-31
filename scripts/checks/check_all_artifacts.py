import csv
import os

# Check scheme evidence with utf-8-sig encoding
print("=== Scheme Evidence ===")
with open('data/annotations/benchmark_v1.2/scheme_evidence.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"Total rows: {len(rows)}")
    print(f"Columns: {reader.fieldnames}")
    for row in rows:
        print(f"  {row['scheme_id']}: {row['scheme_name'][:50]} | source: {row['source_references'][:80]}...")

# Check scenario dossier
print("\n=== Scenario Dossier ===")
with open('data/annotations/benchmark_v1.2/scenario_context_dossier.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"Total rows: {len(rows)}")
    print(f"Columns: {reader.fieldnames}")
    print(f"First row scenario_id: {rows[0]['scenario_id']}")
    print(f"First row immediate_need: {rows[0]['immediate_need']}")
    print(f"First row primary_acute_crisis: {rows[0]['primary_acute_crisis']}")
    print(f"First row secondary_constraints: {rows[0]['secondary_constraints'][:80]}...")
    print(f"First row provenance_synthetic_attributes: {rows[0]['provenance_synthetic_attributes']}")
    print(f"First row provenance_source_attributes: {rows[0]['provenance_source_attributes']}")

# Check Section B packet
print("\n=== Section B Packet ===")
with open('data/annotations/benchmark_v1.2/section_b_qualitative_review_packet.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"Total rows: {len(rows)}")
    print(f"Columns: {reader.fieldnames}")
    if 'relevance_score' in reader.fieldnames:
        print("WARNING: Section B has relevance_score column!")
    else:
        print("OK: No relevance_score column in Section B")
