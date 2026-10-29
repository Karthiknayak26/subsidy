import csv

with open('data/annotations/benchmark_v1.2/scheme_evidence.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    print(f"Columns: {reader.fieldnames}")
    for row in reader:
        print(f"{row['scheme_id']}: {row['scheme_name'][:50]} | source: {row.get('source_references', '')[:80]}...")
