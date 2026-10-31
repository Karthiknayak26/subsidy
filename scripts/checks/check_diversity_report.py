import json

with open('data/benchmarks/v1.2/diversity_audit.json') as f:
    audit = json.load(f)

# Check the joint distribution cell frequency
cell_freq = audit["joint_distribution"]["cell_frequency_distribution"]
print("Cell frequency distribution:", cell_freq)

# Check the report text
with open('reports/benchmark_v1_2_diversity_audit_report.md') as f:
    content = f.read()

# Find the cell frequency section
in_cell_freq = False
for line in content.split('\n'):
    if '### Cell Frequency Distribution' in line:
        in_cell_freq = True
    if in_cell_freq:
        print(line)
        if line.startswith('###') and 'Cell Frequency' not in line:
            break
