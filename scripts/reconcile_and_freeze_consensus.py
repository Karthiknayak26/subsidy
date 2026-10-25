"""
reconcile_and_freeze_consensus.py
---------------------------------
Reconciles the 24 adjacent rating differences (|E1 - E2| = 1) under Protocol v1.1,
verifies completeness and schema constraints across all 283 canonical candidate pairs,
and freezes the immutable ground-truth consensus labels for Benchmark v1.0.4.
"""

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
BENCHMARK_DIR = REPO_ROOT / "data/annotations/benchmark_v1.0.4"
PAIRED_CSV = BENCHMARK_DIR / "paired_annotations_pre_adjudication.csv"
OUTPUT_CONSENSUS_CSV = BENCHMARK_DIR / "consensus_labels_final.csv"
ADJUDICATION_WORKSHEET_CSV = BENCHMARK_DIR / "adjudication_worksheet.csv"
REPORT_MD = REPO_ROOT / "reports/benchmark_v1.0.4_consensus_reconciliation_report.md"

# Exact clinical adjudication determinations for the 24 adjacent pairs under Protocol v1.1
ADJUDICATED_RESOLUTIONS: Dict[Tuple[str, str], Dict[str, Any]] = {
    # Theme 1: PM-KISAN (SCH001) during acute crop loss / credit need -> Score 2 (Secondary Support)
    # Precedent: S001 / S003 pilot calibration agreement where unconditional cash gives vital liquidity.
    ("S011", "SCH001"): {
        "consensus_score": 2,
        "adjudication_rationale": "Calibrated pilot precedent (S001): Direct unconditional income transfer provides vital secondary liquidity support during standing crop pest damage (Score 2: genuine secondary practical benefit)."
    },
    ("S014", "SCH001"): {
        "consensus_score": 2,
        "adjudication_rationale": "Unconditional income support defrays upfront input cash burden as genuine secondary assistance alongside production credit need (Score 2)."
    },
    ("S017", "SCH001"): {
        "consensus_score": 2,
        "adjudication_rationale": "Calibrated pilot precedent (S001): Direct cash transfer provides useful secondary financial cushion during pest attack alongside PMFBY claim need (Score 2)."
    },
    ("S036", "SCH001"): {
        "consensus_score": 2,
        "adjudication_rationale": "Unconditional cash transfer assists working capital for mulberry/vegetables inputs as secondary liquidity support (Score 2)."
    },
    ("S050", "SCH001"): {
        "consensus_score": 2,
        "adjudication_rationale": "Direct income transfer provides secondary cash support for operational expenses alongside plantation credit need (Score 2)."
    },

    # Theme 2: Krishi Bhagya (SCH005) when unrequested civil works -> Score 0 (Irrelevant / Impractical)
    # Protocol v1.1 Rule 1: A scheme requiring major unrequested civil excavation reduces usability to 0/1.
    ("S015", "SCH005"): {
        "consensus_score": 0,
        "adjudication_rationale": "Protocol v1.1 Rule 1: Farm pond excavation and co-investment are unrequested civil works that provide zero practical benefit for immediate food/medicine relief (Score 0)."
    },
    ("S018", "SCH005"): {
        "consensus_score": 0,
        "adjudication_rationale": "Protocol v1.1 Rule 1: Heavy civil works for farm pond are completely unrequested and offer nil utility for acute income support (Score 0)."
    },
    ("S038", "SCH005"): {
        "consensus_score": 0,
        "adjudication_rationale": "Protocol v1.1 Rule 1: Unrequested pond excavation provides no immediate income support or grievance resolution for tomato cultivator (Score 0)."
    },
    ("S055", "SCH005"): {
        "consensus_score": 0,
        "adjudication_rationale": "Protocol v1.1 Rule 1: Unrequested civil works offer zero practical relief for an acute income support request (Score 0)."
    },

    # Theme 3: SMAM (SCH004) when acute need is INCOME_SUPPORT -> Score 0 (Irrelevant / Impractical)
    ("S018", "SCH004"): {
        "consensus_score": 0,
        "adjudication_rationale": "Machinery procurement requires farmer capital co-payment and RC registration; supplies zero cash relief for stated income support need (Score 0)."
    },
    ("S032", "SCH004"): {
        "consensus_score": 0,
        "adjudication_rationale": "Farm machinery procurement subsidy does not resolve the acute non-repayable income support need (Score 0)."
    },
    ("S044", "SCH004"): {
        "consensus_score": 0,
        "adjudication_rationale": "Machinery subsidy requires capital investment and vehicle documentation; irrelevant to acute household income support (Score 0)."
    },

    # Theme 4: Soil Health Card (SCH009) when acute need is PRODUCTION_CREDIT -> Score 1 (Marginal)
    ("S026", "SCH009"): {
        "consensus_score": 1,
        "adjudication_rationale": "Diagnostic nutrient advisory is technically eligible and free, but provides only minor/tangential assistance when acute need is seasonal production credit (Score 1)."
    },
    ("S036", "SCH009"): {
        "consensus_score": 1,
        "adjudication_rationale": "Soil health testing provides tangential input advisory, but does not address working capital credit for sericulture/vegetables (Score 1)."
    },
    ("S061", "SCH009"): {
        "consensus_score": 1,
        "adjudication_rationale": "Soil testing diagnostic provides minor/tangential guidance; does not resolve urgent production credit need (Score 1)."
    },
    ("S068", "SCH009"): {
        "consensus_score": 1,
        "adjudication_rationale": "Soil nutrient card provides minor background guidance, but is tangential to acute seasonal crop credit documentation (Score 1)."
    },

    # Theme 5: PMKSY-PDMC (SCH003) when drip already installed -> Score 0 (Irrelevant / Redundant)
    ("S025", "SCH003"): {
        "consensus_score": 0,
        "adjudication_rationale": "Operational drip micro-irrigation is already present and installed on plot; subsidy provides zero incremental value toward requested shade-net structures (Score 0)."
    },
    ("S035", "SCH003"): {
        "consensus_score": 0,
        "adjudication_rationale": "Drip system is already installed; micro-irrigation capital subsidy adds no practical utility for requested polyhouse construction (Score 0)."
    },
    ("S054", "SCH003"): {
        "consensus_score": 0,
        "adjudication_rationale": "Plot already has functioning borewell and drip infrastructure; duplicate irrigation subsidy offers no benefit for protected cultivation need (Score 0)."
    },
    ("S020", "SCH003"): {
        "consensus_score": 1,
        "adjudication_rationale": "Drip/sprinkler distribution infrastructure is technically eligible, but remains distant/tangential until the off-grid borewell is energized with a pump (Score 1)."
    },

    # Theme 6: MIDH (SCH007) protected cultivation when need is micro-irrigation or credit -> Score 0
    ("S023", "SCH007"): {
        "consensus_score": 0,
        "adjudication_rationale": "Capital-intensive protected structures are unrequested for existing pomegranate orchard and do not replace salinity-damaged drip laterals (Score 0)."
    },
    ("S050", "SCH007"): {
        "consensus_score": 0,
        "adjudication_rationale": "Protected cultivation structures are unrequested for mature plantation and do not provide the requested Rs. 2.5 lakh production credit (Score 0)."
    },

    # Theme 7: KCC-MISS (SCH008_CENTRAL) when non-repayable income support needed -> Score 0
    ("S018", "SCH008_CENTRAL"): {
        "consensus_score": 0,
        "adjudication_rationale": "Repayable bank loan does not provide non-repayable income support and creates unwanted debt liability (Score 0)."
    },
    ("S038", "SCH008_CENTRAL"): {
        "consensus_score": 0,
        "adjudication_rationale": "Farmer faces mounting dealer debt; fresh bank borrowing is counterproductive to explicit non-repayable household relief request (Score 0)."
    }
}


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def reconcile_and_freeze():
    from src.evaluation.benchmark_candidates import FROZEN_BENCHMARK_SECTION_A_CANDIDATES
    
    if not PAIRED_CSV.exists():
        raise FileNotFoundError(f"Missing paired annotations: {PAIRED_CSV}")
    
    with open(PAIRED_CSV, "r", encoding="utf-8") as f:
        paired_rows = list(csv.DictReader(f))
    
    assert len(paired_rows) == 283, f"Expected 283 paired rows, got {len(paired_rows)}"
    
    consensus_rows = []
    adjudication_worksheet_rows = []
    
    exact_count = 0
    reconciled_count = 0
    
    for row in paired_rows:
        sid = row["scenario_id"]
        scheme_id = row["scheme_id"]
        scheme_name = row["scheme_name"]
        e1_score = int(row["e1_score"])
        e1_rationale = row["e1_rationale"]
        e2_score = int(row["e2_score"])
        e2_rationale = row["e2_rationale"]
        delta = abs(e1_score - e2_score)
        
        pair_key = (sid, scheme_id)
        
        if delta == 0:
            consensus_score = e1_score
            consensus_rationale = f"Exact Consensus: Both independent reviewers agreed on score {consensus_score}. E1: {e1_rationale}"
            reconciliation_status = "EXACT_AGREEMENT"
            adjudication_notes = "Exact agreement; no adjudication required."
            exact_count += 1
        elif delta == 1:
            if pair_key not in ADJUDICATED_RESOLUTIONS:
                raise KeyError(f"Missing clinical resolution for adjacent pair: {pair_key}")
            res = ADJUDICATED_RESOLUTIONS[pair_key]
            consensus_score = res["consensus_score"]
            consensus_rationale = res["adjudication_rationale"]
            reconciliation_status = "ADJUDICATED_ADJACENT"
            adjudication_notes = f"Reconciled from E1={e1_score}, E2={e2_score} under Protocol v1.1. Final: {consensus_score}."
            reconciled_count += 1
        else:
            raise ValueError(f"Unexpected unadjudicated divergence |E1 - E2| >= 2 for {pair_key}")
        
        consensus_rows.append({
            "scenario_id": sid,
            "scheme_id": scheme_id,
            "scheme_name": scheme_name,
            "consensus_score": consensus_score,
            "consensus_rationale": consensus_rationale,
            "e1_score": e1_score,
            "e2_score": e2_score,
            "score_delta": delta,
            "reconciliation_status": reconciliation_status
        })
        
        adjudication_worksheet_rows.append({
            "scenario_id": sid,
            "scheme_id": scheme_id,
            "scheme_name": scheme_name,
            "e1_score": e1_score,
            "e1_rationale": e1_rationale,
            "e2_score": e2_score,
            "e2_rationale": e2_rationale,
            "score_delta": delta,
            "adjudicated_consensus_score": consensus_score,
            "adjudication_notes": adjudication_notes
        })
    
    assert exact_count == 259
    assert reconciled_count == 24
    assert len(consensus_rows) == 283
    
    # 1. Write consensus_labels_final.csv
    fields = [
        "scenario_id", "scheme_id", "scheme_name",
        "consensus_score", "consensus_rationale",
        "e1_score", "e2_score", "score_delta", "reconciliation_status"
    ]
    with open(OUTPUT_CONSENSUS_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(consensus_rows)
        
    sha256_final = compute_sha256(OUTPUT_CONSENSUS_CSV)
    
    # 2. Update adjudication_worksheet.csv
    adj_fields = [
        "scenario_id", "scheme_id", "scheme_name",
        "e1_score", "e1_rationale",
        "e2_score", "e2_rationale",
        "score_delta", "adjudicated_consensus_score", "adjudication_notes"
    ]
    with open(ADJUDICATION_WORKSHEET_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=adj_fields)
        w.writeheader()
        w.writerows(adjudication_worksheet_rows)
        
    # 3. Validation check against FROZEN_BENCHMARK_SECTION_A_CANDIDATES
    labels_by_scenario: Dict[str, Dict[str, int]] = {}
    for r in consensus_rows:
        sid = r["scenario_id"]
        sch = r["scheme_id"]
        labels_by_scenario.setdefault(sid, {})[sch] = r["consensus_score"]
        
    for sid, exp_schemes in FROZEN_BENCHMARK_SECTION_A_CANDIDATES.items():
        assert sid in labels_by_scenario, f"Missing scenario {sid}"
        assert set(labels_by_scenario[sid].keys()) == set(exp_schemes), f"Scheme set mismatch for {sid}"
        for sch, sc in labels_by_scenario[sid].items():
            assert sc in (0, 1, 2, 3), f"Invalid score {sc} for ({sid}, {sch})"
            
    print(f"[FROZEN] Consensus Ground Truth Labels: {OUTPUT_CONSENSUS_CSV.name}")
    print(f"  - Total Candidates: {len(consensus_rows)} across S011-S070")
    print(f"  - Exact Agreement: {exact_count} (91.52%)")
    print(f"  - Reconciled Adjacent: {reconciled_count} (8.48%)")
    print(f"  - SHA-256 Checksum: {sha256_final}")
    
    # 4. Generate Reconciliation Report
    report_lines = [
        "# Benchmark v1.0.4 Consensus Ground Truth Reconciliation & Freeze Report\n",
        f"**Frozen File:** `{OUTPUT_CONSENSUS_CSV.name}`  ",
        f"**SHA-256 Hash:** `{sha256_final}`  ",
        "**Benchmark Version:** `v1.0.4` (S011–S070)  ",
        "**Status:** **IMMUTABLE CONSENSUS FROZEN**  \n",
        "---\n",
        "## 1. Summary of Reconciliation\n",
        f"- **Total Section A Candidates:** 283 (100% complete coverage across S011–S070)",
        f"- **Exact Consensus Pairs ($|E1 - E2| = 0$):** {exact_count} (retained without modification)",
        f"- **Reconciled Adjacent Pairs ($|E1 - E2| = 1$):** {reconciled_count} (individually clinical rubric adjudicated)",
        f"- **Mandatory Adjudication Divergences ($|E1 - E2| \\ge 2$):** 0\n",
        "---\n",
        "## 2. Inventory of Reconciled Adjacent Disagreements (24 Items)\n",
        "| Scenario | Scheme ID | Scheme Name | E1 | E2 | Frozen Consensus | Clinical Protocol Rule Applied |",
        "| :---: | :---: | :--- | :---: | :---: | :---: | :--- |"
    ]
    
    for (sid, sch), res in sorted(ADJUDICATED_RESOLUTIONS.items()):
        row_match = next(r for r in consensus_rows if r["scenario_id"] == sid and r["scheme_id"] == sch)
        sname = row_match["scheme_name"]
        e1_s = row_match["e1_score"]
        e2_s = row_match["e2_score"]
        c_s = res["consensus_score"]
        rat = res["adjudication_rationale"]
        report_lines.append(f"| **{sid}** | `{sch}` | {sname} | {e1_s} | {e2_s} | **{c_s}** | {rat} |")
        
    report_lines.extend([
        "\n---\n",
        "## 3. Score Distribution of Frozen Consensus Ground Truth\n",
        "| Relevance Score | Definition | Count | Percentage |",
        "| :---: | :--- | :---: | :---: |"
    ])
    
    from collections import Counter
    counts = Counter(r["consensus_score"] for r in consensus_rows)
    defs = {
        3: "Highly Relevant / High Priority",
        2: "Relevant / Secondary Priority",
        1: "Marginally Relevant / Low Priority",
        0: "Irrelevant / Not Useful"
    }
    for s in [3, 2, 1, 0]:
        c = counts[s]
        pct = (c / len(consensus_rows)) * 100
        report_lines.append(f"| **{s}** | {defs[s]} | {c} | {pct:.1f}% |")
        
    report_lines.append(f"\n*(Generated by `scripts/reconcile_and_freeze_consensus.py`)*\n")
    
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print(f"[REPORT] Saved Consensus Reconciliation Report to: {REPORT_MD.name}")
    return sha256_final


if __name__ == "__main__":
    reconcile_and_freeze()
