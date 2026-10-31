import json

# Check scenario matrix
with open('data/benchmarks/v1.2/scenario_matrix.json') as f:
    scenarios = json.load(f)
print(f'Total scenarios: {len(scenarios)}')
if len(scenarios) > 0:
    print(f'First: {scenarios[0]["scenario_id"]}')
    print(f'Last: {scenarios[-1]["scenario_id"]}')
# Check all scenario IDs
sid_list = [s["scenario_id"] for s in scenarios]
expected = [f"S{i:03d}" for i in range(131, 221)]
missing = set(expected) - set(sid_list)
extra = set(sid_list) - set(expected)
print(f'Missing IDs: {missing}')
print(f'Extra IDs: {extra}')
print(f'Sequential: {sid_list == expected}')

# Check candidate generation results
with open('data/benchmarks/v1.2/candidate_generation_results.json') as f:
    cand = json.load(f)
print(f'\nTotal scenarios with candidates: {len(cand)}')
section_a_total = sum(len(r.get('section_a_candidates', [])) for r in cand.values())
section_b_total = sum(len(r.get('section_b_candidates', [])) for r in cand.values())
print(f'Total Section A candidates: {section_a_total}')
print(f'Total Section B candidates: {section_b_total}')
scenario_ids = list(cand.keys())
missing_cand = set(expected) - set(scenario_ids)
extra_cand = set(scenario_ids) - set(expected)
print(f'Missing from candidates: {missing_cand}')
print(f'Extra in candidates: {extra_cand}')

# Check diversity audit
with open('data/benchmarks/v1.2/diversity_audit.json') as f:
    div = json.load(f)
print(f'\nDiversity audit:')
print(f'  Total scenarios: {div.get("total_scenarios")}')
print(f'Unique archetypes: {div.get("unique_archetype_count")}')
print(f'Underrepresented cells: {div.get("underrepresented_cell_count")}')
print(f'Near-duplicate pairs: {div.get("near_duplicate_count")}')
print(f'Audit passed: {audit.get("audit_passed")}')
print()
print('Marginal distributions:')
for k, v in audit.get('marginal_distributions', {}).items():
    print(f'  {k}:')
    for val, cnt in sorted(v.items(), key=lambda x: -x[1])[:5]:
        print(f'    {val}: {cnt}')
