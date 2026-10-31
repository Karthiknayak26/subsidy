import csv

with open('data/annotations/benchmark_v1.2/section_b_qualitative_review_packet.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)
    print(f"Total rows: {len(rows)}")
    if rows:
        print(f"First row: {rows[0]}")
        print(f"Num columns: {len(rows[0])}")
    # Check if first row looks like a header
    print(f"Is header row: {rows[0][0] if rows else 'N/A'}")
