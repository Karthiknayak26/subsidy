"""
generate_benchmark_annotation_packet.py
----------------------------------------
Generates blinded, independent Expert Annotation Packets for Benchmark v1.0.4 (S011–S070)
in strict compliance with Annotation Protocol v1.1.

SAFEGUARDS & ENFORCEMENTS:
1. Benchmark Scope: Evaluates only scenarios S011–S070 (60 scenarios across 10 zones).
   Pilot scenarios S001–S010 are strictly excluded and preserved as calibration data.
2. Section A Numerical Scoring Isolation:
   - Only schemes classified in Section A (confirmed actionable candidates with allow_numerical_scoring=True)
     are included in the numerical scoring templates.
   - Blank template rows generated: scenario_id, scheme_id, rater_id, relevance_score, rationale.
   - Scores are left BLANK (no automated labels, no default values, no baseline leakage).
3. Two-Phase Availability Blinding:
   - Operational availability states, portal window timestamps, model rankings,
     and baseline scores are completely hidden from the relevance packet.
4. Section B Score Exclusion:
   - All Section B items (provisional schemes, unconfirmed title / corporation cases,
     PMFBY seasonal unit reviews) are routed to a separate qualitative policy review packet.
   - Numerical scoring is strictly disabled for Section B.
"""

import csv
import json
import os
from pathlib import Path
from typing import Dict, List, Any


def get_zone_for_scenario(scenario_idx: int) -> int:
    """Returns zone 1 to 10 for scenario index 11 to 70."""
    return (scenario_idx - 11) // 6 + 1


def load_benchmark_data(repo_root: Path) -> List[Dict[str, Any]]:
    """
    Loads scenario profiles from individual Sxxx.json files and execution results
    from zX_execution_results.json for all 60 scenarios S011–S070.
    """
    scenarios = []

    for sid_num in range(11, 71):
        sid = f"S{sid_num:03d}"
        zone = get_zone_for_scenario(sid_num)
        
        profile_path = repo_root / f"data/benchmarks/z{zone}/{sid}.json"
        if not profile_path.exists():
            raise FileNotFoundError(f"Missing scenario profile: {profile_path}")
        
        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)

        # Also load execution determinations from zone execution file
        exec_file = repo_root / f"data/benchmarks/z{zone}/z{zone}_execution_results.json"
        with open(exec_file, "r", encoding="utf-8") as f:
            exec_data = json.load(f)
            exec_results = exec_data.get("results", [])
            target_res = None
            for r in exec_results:
                r_sid = r.get("scenario_id") or (r.get("profile") or r.get("scenario", {})).get("scenario_id")
                if r_sid == sid:
                    target_res = r
                    break
            if not target_res:
                raise ValueError(f"Could not find execution results for {sid} in {exec_file}")

        scenarios.append({
            "scenario_id": sid,
            "zone": zone,
            "profile": profile,
            "actionable_determinations": target_res.get("actionable_determinations", []),
            "raw_determinations": target_res.get("raw_determinations", [])
        })

    return scenarios


def generate_packets():
    repo_root = Path(__file__).resolve().parent.parent
    output_dir = repo_root / "data/annotations/benchmark_v1.0.4"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    dossier_path = repo_root / "research/dataset_research/benchmark_v1.0.4_blinded_annotation_dossier.md"

    scenarios = load_benchmark_data(repo_root)
    assert len(scenarios) == 60, f"Expected 60 scenarios, got {len(scenarios)}"
    assert scenarios[0]["scenario_id"] == "S011"
    assert scenarios[-1]["scenario_id"] == "S070"

    e1_rows = []
    e2_rows = []
    combined_rows = []
    section_b_rows = []

    dossier_lines = [
        "# Benchmark v1.0.4 — Blinded Expert Relevance Annotation Dossier",
        "",
        "**Benchmark Version:** `v1.0.4`  ",
        "**Annotation Protocol:** `annotation-protocol-v1.1`  ",
        "**Target Benchmark:** S011–S070 (60 production scenarios across 10 agro-climatic zones)  ",
        "**Calibration Set:** S001–S010 (strictly partitioned and held separate)  ",
        "",
        "---",
        "",
        "## 1. Instructions & Rating Rubric (0–3 Scale)",
        "",
        "Please evaluate each candidate scheme presented under **Section A** based *strictly* on the farmer's stated need, crop, and farm asset profile.",
        "Operational portal availability has been blinded for this phase. Do not lower or adjust scores based on whether an application window is open or closed.",
        "",
        "| Score | Rating Level | Definition & Clinical Decision Rule |",
        "|:---:|:---|:---|",
        "| **3** | **Highly Relevant / High Priority** | Directly addresses the farmer's primary stated need with immediate, high-impact benefit. Should be a top recommendation. |",
        "| **2** | **Relevant / Secondary Priority** | Provides genuine practical benefit and valuable secondary support, but does not directly solve the immediate acute crisis. |",
        "| **1** | **Marginally Relevant / Low Priority** | Technically applicable and eligible, but offers minor, distant, or tangential value in the current context. |",
        "| **0** | **Irrelevant / Not Useful** | Despite passing statutory eligibility, provides no meaningful practical benefit given the farmer's specific circumstances. |",
        "",
        "### Protocol v1.1 Guardrail Rules:",
        "1. **Infrastructure & Civil Works Complexity:** A scheme must NOT receive a high score solely because it includes an eligible sub-component. If obtaining the benefit requires major unrequested civil works (e.g. farm pond excavation) that reduce practical usability, score **1** or **0**.",
        "2. **Income Support vs. Repayable Credit:** Repayable crop credit / loans (e.g. KCC-MISS, PACS credit) must NOT receive score **3** when the farmer's stated need is purely non-repayable income relief (`INCOME_SUPPORT`), unless the farmer explicitly requests borrowing or loan rescheduling.",
        "3. **Section B (Provisional Schemes):** Section B schemes (e.g. PACS zero-interest credit requiring annual GO verification, unconfirmed title cases) are **strictly excluded from numerical scoring (0–3)**. They appear only in the qualitative review section.",
        "",
        "---",
        "",
        "## 2. Farmer Scenarios & Section A Candidate Schemes (Blinded)",
        ""
    ]

    for sc_info in scenarios:
        sid = sc_info["scenario_id"]
        zone_num = sc_info["zone"]
        prof = sc_info["profile"]
        dets = sc_info["actionable_determinations"]

        sec_a = [d for d in dets if "Section A" in d.get("presentation_section", "") and d.get("allow_numerical_scoring") is True]
        sec_b = [d for d in dets if "Section B" in d.get("presentation_section", "")]

        # Build CSV rows
        for d in sec_a:
            scheme_id = d["scheme_id"]
            e1_rows.append({
                "scenario_id": sid,
                "scheme_id": scheme_id,
                "scheme_name": d["scheme_name"],
                "rater_id": "E1",
                "relevance_score": "",
                "rationale": ""
            })
            e2_rows.append({
                "scenario_id": sid,
                "scheme_id": scheme_id,
                "scheme_name": d["scheme_name"],
                "rater_id": "E2",
                "relevance_score": "",
                "rationale": ""
            })
            combined_rows.append({
                "scenario_id": sid,
                "scheme_id": scheme_id,
                "scheme_name": d["scheme_name"],
                "rater_id": "E1",
                "relevance_score": "",
                "rationale": ""
            })
            combined_rows.append({
                "scenario_id": sid,
                "scheme_id": scheme_id,
                "scheme_name": d["scheme_name"],
                "rater_id": "E2",
                "relevance_score": "",
                "rationale": ""
            })

        for d in sec_b:
            section_b_rows.append({
                "scenario_id": sid,
                "scheme_id": d["scheme_id"],
                "scheme_name": d["scheme_name"],
                "governance_status": d.get("governance_status", "REQUIRES_VERIFICATION"),
                "governance_note": d.get("governance_note", ""),
                "expert_policy_comment": ""
            })

        # Scenario attributes for dossier
        land_str = f"{prof.get('land_size_acres')} acres ({prof.get('farmer_category', 'N/A')}) | Land Type: {prof.get('land_type', 'N/A')}"
        crops_str = prof.get('crop_primary', 'N/A')
        if prof.get('crop_secondary') and prof.get('crop_secondary') != 'None':
            crops_str += f", {prof.get('crop_secondary')}"
        
        water_details = prof.get('water_and_irrigation', {})
        water_source = water_details.get('operational_water_source') or prof.get('land_type', 'N/A')
        electric_status = prof.get('borewell_electric_status', 'N/A')

        assets_val = prof.get('existing_assets', [])
        assets_str = ', '.join(assets_val) if isinstance(assets_val, list) and assets_val else str(assets_val)

        tenure_type = prof.get('statutory_flags', {}).get('tenure_type', 'Registered Owner')
        farmer_query = prof.get('kcc_query_text_example') or prof.get('intended_test_purpose', 'N/A')

        dossier_lines.extend([
            f"### Scenario {sid} (Zone {zone_num} — {prof.get('agro_climatic_zone', 'N/A')})",
            f"- **Location:** {prof.get('district', 'N/A')} District (Zone {zone_num})",
            f"- **Social Category & Tenure:** {prof.get('social_category', 'N/A')} | Tenure: {tenure_type}",
            f"- **Landholding & Land Type:** {land_str}",
            f"- **Crops:** {crops_str}",
            f"- **Water Infrastructure:** {water_source} | Power/Grid: {electric_status}",
            f"- **Existing Assets:** {assets_str}",
            f"- **PRIMARY STATED NEED:** **`{prof.get('immediate_need', 'N/A')}`**",
            f"- **Farmer Narrative / Stated Circumstance:** *\"{farmer_query}\"*",
            "",
            "#### Section A: Eligible Candidates for Numerical Relevance Scoring (0–3)",
            "| Scheme ID | Scheme Name | Statutory Eligibility Reason | Rater Score (0–3) | Rationale |",
            "|:---|:---|:---|:---:|:---|"
        ])

        for d in sec_a:
            clean_reason = d.get('reason', '').replace('\n', ' ')
            dossier_lines.append(f"| `{d['scheme_id']}` | **{d['scheme_name']}** | {clean_reason} | | |")

        if sec_b:
            dossier_lines.extend([
                "",
                "#### Section B: Provisional Schemes (Score-Disabled — Qualitative Review Only)",
                "| Scheme ID | Scheme Name | Governance Flag | Policy & Verification Note |",
                "|:---|:---|:---|:---|"
            ])
            for d in sec_b:
                clean_note = d.get('governance_note', '').replace('\n', ' ')
                dossier_lines.append(f"| `{d['scheme_id']}` | **{d['scheme_name']}** | `{d.get('governance_status', 'REQUIRES_VERIFICATION')}` | {clean_note} |")

        dossier_lines.append("")
        dossier_lines.append("---")
        dossier_lines.append("")

    # Write CSV files
    fieldnames = ["scenario_id", "scheme_id", "scheme_name", "rater_id", "relevance_score", "rationale"]
    
    e1_file = output_dir / "E1_annotation_packet_blank.csv"
    with open(e1_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(e1_rows)

    e2_file = output_dir / "E2_annotation_packet_blank.csv"
    with open(e2_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(e2_rows)

    combined_file = output_dir / "E1_E2_combined_packet_blank.csv"
    with open(combined_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined_rows)

    sec_b_file = output_dir / "section_b_policy_review_packet.csv"
    sec_b_fields = ["scenario_id", "scheme_id", "scheme_name", "governance_status", "governance_note", "expert_policy_comment"]
    with open(sec_b_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sec_b_fields)
        writer.writeheader()
        writer.writerows(section_b_rows)

    # Write Markdown Dossier
    with open(dossier_path, "w", encoding="utf-8") as f:
        f.write("\n".join(dossier_lines))

    print(f"[SUCCESS] Packets generated successfully in {output_dir}:")
    print(f"  - E1 blank packet: {len(e1_rows)} candidate rows ({e1_file.name})")
    print(f"  - E2 blank packet: {len(e2_rows)} candidate rows ({e2_file.name})")
    print(f"  - E1/E2 combined packet: {len(combined_rows)} candidate rows ({combined_file.name})")
    print(f"  - Section B qualitative review packet: {len(section_b_rows)} candidate rows ({sec_b_file.name})")
    print(f"  - Blinded annotation dossier: {dossier_path.name}")


if __name__ == "__main__":
    generate_packets()
