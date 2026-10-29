with open('scripts/audit_benchmark_v1_2_diversity.py', 'r') as f:
    content = f.read()

content = content.replace('joint_dist', 'joint')

with open('scripts/audit_benchmark_v1_2_diversity.py', 'w') as f:
    f.write(content)

print("Fixed all joint_dist references to joint")
