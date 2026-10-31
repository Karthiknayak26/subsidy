import json
import csv

# Check dossier
with open('data/annotations/benchmark_v1.2/scenario_context_dossier.csv') as f:
    rows = list(csv.DictReader(f))
print(f'Dossier: {len(rows)} rows')
print(f'Columns: {list(rows[0].keys())}')
print(f'First row scenario_id: {rows[0]["scenario_id"]}')
print(f'First row immediate_need: {rows[0]["immediate_need"]}')

# Check E1
with open('data/annotations/benchmark_v1.2/E1_v1.2_blank.csv') as f:
    e1 = list(csv.DictReader(f))
print(f'E1: {len(e1)} rows')
print(f'E1 columns: {list(e1[0].keys())}')
print(f'E1 first row rater_id: {e1[0]["rater_id"]}')
print(f'E1 first row score: "{e1[0]["relevance_score"]}"')
print(f'E1 all blank scores: {all(r["relevance_score"]=="" for r in e1)}')
print(f'E1 all blank rationale: {all(r["relevance_rationale"]=="" for r in e1)}')
print(f'E1 all blank notes: {all(r["complementarity_notes"]=="" for r in e1)}')

# Check E2
with open('data/annotations/benchmark_v1.2/E2_v1.2_blank.csv') as f:
    e2 = list(csv.DictReader(f))
print(f'E2: {len(e2)} rows')
print(f'E2 first row rater_id: {e2[0]["rater_id"]}')
print(f'E2 all blank scores: {all(r["relevance_score"]=="" for r in e2)}')

# Check E1/E2 identical pairs
e1_pairs = [(r["scenario_id"], r["scheme_id"]) for r in e1]
e2_pairs = [(r["scenario_id"], r["scheme_id"]) for r in e2]
print(f'E1/E2 pairs identical: {e1_pairs == e2_pairs}')

# Check Section B
with open('data/annotations/benchmark_v1.2/section_b_qualitative_review_packet.csv') as f:
    sb = list(csv.DictReader(f))
print(f'Section B: {len(sb)} rows')
print(f'Section B has relevance_score column: {"relevance_score" in sb[0]}')
print(f'Section B all blank score: {all(r["relevance_score"]=="" for r in sb)}')

# Check scheme evidence
with open('data/annotations/benchmark_v1.2/scheme_evidence.csv') as f:
    ev = list(csv.DictReader(f))
print(f'Scheme evidence: {len(ev)} rows')
for row in ev:
    print(f'  {row["scheme_id"]}: {row["scheme_name"][:50]} | source: {row["source_references"][:80]}...')

# Check no duplicate pairs in E1
e1_pairs_set = set(e1_pairs)
print(f'E1 unique pairs: {len(e1_pairs_set)} (should equal {len(e1_pairs)})')
