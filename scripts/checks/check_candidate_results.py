import json
from collections import Counter

# Load candidate generation results
with open('data/benchmarks/v1.2/candidate_generation_results.json') as f:
    results = json.load(f)

# Collect all distinct Section A schemes
section_a_schemes = Counter()
section_b_schemes = Counter()
total_section_a = 0
total_section_b = 0

for sid, data in results.items():
    for c in data.get('section_a_candidates', []):
        section_a_schemes[c['scheme_id']] += 1
        total_section_a += 1
    for c in data.get('section_b_candidates', []):
        section_b_schemes[c['scheme_id']] += 1
        total_section_b += 1

print(f"Total scenarios: {len(results)}")
print(f"Total Section A candidate rows: {total_section_a}")
print(f"Total Section B candidate rows: {total_section_b}")
print()
print("=== DISTINCT SECTION A SCHEMES ===")
for sid, count in sorted(section_a_schemes.items(), key=lambda x: x[0]):
    print(f"  {sid}: {count} scenarios")
print()
print(f"Distinct Section A schemes: {len(section_a_schemes)}")
print()
print("=== SECTION B SCHEMES ===")
for sid, count in sorted(section_b_schemes.items(), key=lambda x: x[0]):
    print(f"  {sid}: {count} scenarios")
print()
print(f"Distinct Section B schemes: {len(section_b_schemes)}")
print()

# Check for scenarios with no Section A candidates
no_section_a = [sid for sid, r in results.items() if r['section_a_count'] == 0]
print(f"Scenarios with no Section A candidates: {len(no_section_a)}")
if no_section_a:
    print(f"  IDs: {no_section_a}")

# Check scenarios with only 1 Section A candidate
single_section_a = [(sid, r['section_a_count']) for sid, r in results.items() if r['section_a_count'] == 1]
print(f"\nScenarios with only 1 Section A candidate: {len(single_section_a)}")
for sid, count in single_section_a[:10]:
    print(f"  {sid}: {count} candidates")
