import hashlib
from pathlib import Path

ann_dir = Path("C:/Users/User/Desktop/subsidy/farmer-benefit-ml/data/annotations/benchmark_v1.2")
files = [
    "E2_v1.2_blank.csv",
    "scenario_context_dossier.csv",
    "scheme_evidence.csv",
    "section_b_qualitative_review_packet.csv",
    "raw/E2_v1.2_blank.csv",
]

for f in ann_dir.iterdir():
    if f.is_file():
        sha256 = hashlib.sha256()
        with open(f, "rb") as fh:
            for chunk in iter(lambda: fh.read(8192), b""):
                sha256.update(chunk)
        print(f"{sha256.hexdigest()}  {f.name}")
