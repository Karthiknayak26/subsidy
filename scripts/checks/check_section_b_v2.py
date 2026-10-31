import csv
with open('data/annotations/benchmark_v1.2/section_b_qualitative_review_packet.csv') as f:
    reader = csv.DictReader(f)
    print(f"Columns: {reader.fieldnames}")
    print(f"Has relevance_score: {'relevance_score' in reader.fieldnames}")
    print(f"Total rows: {sum(1 for _ in f) + 1}")
