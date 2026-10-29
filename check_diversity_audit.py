import json

with open('data/benchmarks/v1.2/diversity_audit.json') as f:
    audit = json.load(f)

print(f'Total scenarios: {audit["total_scenarios"]}')
print(f'Joint dist total_cells: {audit["joint_distribution"]["total_cells"]}')
print(f'Cells with scenarios: {audit["joint_distribution"]["cells_with_scenarios"]}')
print(f'Cell frequency distribution: {audit["joint_distribution"]["cell_frequency_distribution"]}')
print(f'Underrepresented cells: {audit["underrepresented_cell_count"]}')
print(f'Near-duplicate pairs: {audit["near_duplicate_count"]}')
print(f'Audit passed: {audit["audit_passed"]}')

# Verify: sum of cell_count * num_cells should equal total scenarios
cell_freq = audit["joint_distribution"]["cell_frequency_distribution"]
total_scenarios_from_cells = sum(int(k) * v for k, v in cell_freq.items())
print(f'Scenarios accounted for in cell frequency: {total_scenarios_from_cells}')
print(f'Matches total scenarios: {total_scenarios_from_cells == audit["total_scenarios"]}')

# List all underrepresented cells
print(f'\nUnderrepresented cells ({len(audit["underrepresented_cells"])}):')
for key, count in sorted(audit["underrepresented_cells"].items(), key=lambda x: -x[1]):
    print(f'  {key}: {count} scenario(s)')