import json

with open('data/benchmarks/v1.2/scenario_matrix.json') as f:
    scenarios = json.load(f)

with open('data/benchmarks/v1.2/candidate_generation_results.json') as f:
    results = json.load(f)

print(f'Scenarios: {len(scenarios)}')
print(f'First: {scenarios[0]["scenario_id"]}')
print(f'Last: {scenarios[-1]["scenario_id"]}')
print(f'Results entries: {len(results)}')

s0 = scenarios[0]
print(f'\nSample scenario {s0["scenario_id"]}:')
print(f'  Zone: {s0["zone_id"]}, District: {s0["district"]}')
print(f'  Crop: {s0["crop_primary"]}/{s0["crop_secondary"]}')
print(f'  Land: {s0["land_size_acres"]} ac, {s0["land_type"]}')
print(f'  Social: {s0["social_category"]}, {s0["farmer_category"]}')
print(f'  Water: {s0["water_and_irrigation"]["operational_water_source"]}')
print(f'  Electricity: {s0["water_and_irrigation"]["borewell_electric_status"]}')
print(f'  Immediate need: {s0["immediate_need"]}')
print(f'  Income: {s0["annual_family_income_lakh"]} lakh')
print(f'  Tenant: {s0["is_pure_tenant_without_land_title"]}')

r0 = results[s0['scenario_id']]
print(f'  Section A: {len(r0["section_a_candidates"])} schemes')
print(f'  Section B: {len(r0["section_b_candidates"])} schemes')
print(f'  Disqualified: {len(r0["disqualified_candidates"])} schemes')
sa_schemes = [c['scheme_id'] for c in r0['section_a_candidates']]
print(f'  Section A scheme IDs: {sa_schemes}')

s1 = scenarios[1]
r1 = results[s1['scenario_id']]
print(f'\nSample scenario {s1["scenario_id"]}:')
print(f'  Zone: {s1["zone_id"]}, District: {s1["district"]}')
print(f'  Crop: {s1["crop_primary"]}/{s1["crop_secondary"]}')
print(f'  Land: {s1["land_size_acres"]} ac, {s1["land_type"]}')
print(f'  Social: {s1["social_category"]}, {s1["farmer_category"]}')
print(f'  Water: {s1["water_and_irrigation"]["operational_water_source"]}')
print(f'  Immediate need: {s1["immediate_need"]}')
sa_schemes1 = [c['scheme_id'] for c in r1['section_a_candidates']]
print(f'  Section A scheme IDs: {sa_schemes1}')

# Count section A candidate distribution
from collections import Counter
sec_a_counts = [r["section_a_count"] for r in results.values()]
print(f'\nSection A candidate count distribution:')
for c in sorted(set(sec_a_counts)):
    pct = (sec_a_counts.count(c) / len(sec_a_counts)) * 100
    print(f'  {c} schemes: {sec_a_counts.count(c)} scenarios ({pct:.1f}%)')
print(f'  Mean: {sum(sec_a_counts)/len(sec_a_counts):.1f}')
print(f'  Range: {min(sec_a_counts)} to {max(sec_a_counts)}')

# Check scenario ID range
ids = [s["scenario_id"] for s in scenarios]
print(f'\nScenario ID range: {ids[0]} to {ids[-1]}')
print(f'Expected: S131 to S{130 + len(scenarios)}')