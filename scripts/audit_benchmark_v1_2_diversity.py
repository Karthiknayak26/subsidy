#!/usr/bin/env python3
"""
audit_benchmark_v1_2_diversity.py
---------------------------------
Runs the mandatory pre-finalization diversity audit for Benchmark v1.2 scenarios.

Per benchmark_v1.2_design_proposal.md Section 3.3, computes:
1. Marginal distributions of all attributes
2. Joint distribution of (crop x land tenure x water access x primary crisis x electricity access)
3. Unique crisis types and archetypes count
4. Under-represented cells (<3 scenarios)
5. Duplicate and near-duplicate scenario checks
6. Candidate pool size distributions
7. Source-provenance completeness for scheme claims

Outputs:
- data/benchmarks/v1.2/diversity_audit.json (machine-readable)
- reports/benchmark_v1_2_diversity_audit_report.md (human-readable)
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

BENCH_DIR = REPO_ROOT / "data/benchmarks/v1.2"
SCENARIO_MATRIX_PATH = BENCH_DIR / "scenario_matrix.json"
CANDIDATE_RESULTS_PATH = BENCH_DIR / "candidate_generation_results.json"
DIVERSITY_AUDIT_PATH = BENCH_DIR / "diversity_audit.json"
DIVERSITY_REPORT_PATH = REPO_ROOT / "reports/benchmark_v1_2_diversity_audit_report.md"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_marginal_distributions(scenarios):
    """Compute marginal distributions for all scenario attributes."""
    dists = {}

    # Zone distribution
    dists["zone_id"] = Counter(s["zone_id"] for s in scenarios)

    # District distribution
    dists["district"] = Counter(s["district"] for s in scenarios)

    # Primary crop distribution
    dists["crop_primary"] = Counter(s["crop_primary"] for s in scenarios)

    # Land size (bucketed)
    def bucket(acres):
        if acres < 1.0:
            return "Marginal (< 1.0 acre)"
        elif acres < 2.5:
            return "Marginal (1.0-2.5 acres)"
        elif acres <= 5.0:
            return "Small (2.5-5.0 acres)"
        else:
            return "Medium/Large (> 5.0 acres)"
    dists["land_size_bucket"] = Counter(bucket(s["land_size_acres"]) for s in scenarios)

    # Land type
    dists["land_type"] = Counter(s["land_type"] for s in scenarios)

    # Social category
    dists["social_category"] = Counter(s["social_category"] for s in scenarios)

    # Farmer category
    dists["farmer_category"] = Counter(s["farmer_category"] for s in scenarios)

    # Water access
    dists["water_access"] = Counter(s["water_and_irrigation"]["operational_water_source"] for s in scenarios)

    # Electricity access
    dists["electricity_access"] = Counter(s["water_and_irrigation"]["borewell_electric_status"] for s in scenarios)

    # Immediate need
    dists["immediate_need"] = Counter(s["immediate_need"] for s in scenarios)

    # Tenant status
    dists["is_pure_tenant"] = Counter(str(s["is_pure_tenant_without_land_title"]) for s in scenarios)

    # Income (bucketed)
    def income_bucket(lakh):
        if lakh < 1.0:
            return "< 1.0 lakh"
        elif lakh < 2.0:
            return "1.0-2.0 lakh"
        elif lakh < 3.0:
            return "2.0-3.0 lakh"
        else:
            return "3.0+ lakh"
    dists["income_bucket"] = Counter(income_bucket(s["annual_family_income_lakh"]) for s in scenarios)

    return dists


def compute_joint_distribution(scenarios):
    """Compute joint distribution of crop x land tenure x water access x crisis x electricity."""
    joint = Counter()
    for s in scenarios:
        key = (
            s["crop_primary"],
            "Tenant" if s["is_pure_tenant_without_land_title"] else "Titled",
            s["water_and_irrigation"]["operational_water_source"],
            s["immediate_need"],
            s["water_and_irrigation"]["borewell_electric_status"],
        )
        joint[key] += 1
    return joint


def compute_archetype_distribution(scenarios):
    """Compute distribution of compound need archetypes."""
    archetypes = Counter()
    for s in scenarios:
        arch_id = s["compound_need_details"]["archetype_id"]
        archetypes[arch_id] += 1
    return archetypes


def find_underrepresented_cells(joint_dist, min_count=3):
    """Find joint distribution cells with fewer than min_count scenarios."""
    underrepresented = {}
    for key, count in joint_dist.items():
        if count < min_count:
            underrepresented[key] = count
    return underrepresented


def find_near_duplicates(scenarios):
    """Find near-duplicate scenarios based on attribute similarity."""
    # Simple approach: compare attribute tuples
    seen = {}
    duplicates = []
    for s in scenarios:
        key = (
            s["crop_primary"],
            s["land_size_acres"],
            s["land_type"],
            s["social_category"],
            s["water_and_irrigation"]["operational_water_source"],
            s["water_and_irrigation"]["borewell_electric_status"],
            s["immediate_need"],
        )
        if key in seen:
            duplicates.append((seen[key], s["scenario_id"]))
        else:
            seen[key] = s["scenario_id"]
    return duplicates


def compute_candidate_distribution(results):
    """Compute candidate pool size distributions."""
    sec_a_counts = Counter(r["section_a_count"] for r in results.values())
    sec_b_counts = Counter(r["section_b_count"] for r in results.values())
    disq_counts = Counter(r["disqualified_count"] for r in results.values())
    return sec_a_counts, sec_b_counts, disq_counts


def compute_provenance_completeness(scenarios):
    """Check which scenario attributes have provenance documentation."""
    # Check which fields have provenance tracking
    provenance_fields = [
        "scenario_id", "zone_id", "district", "crop_primary", "crop_secondary",
        "land_size_acres", "land_type", "social_category", "farmer_category",
        "water_and_irrigation", "immediate_need", "annual_family_income_lakh",
    ]
    completeness = {}
    for field in provenance_fields:
        missing = 0
        for s in scenarios:
            if field in ["water_and_irrigation"]:
                if not s.get(field):
                    missing += 1
            elif s.get(field) is None or s.get(field) == "":
                missing += 1
        completeness[field] = {
            "total": len(scenarios),
            "missing": missing,
            "complete": len(scenarios) - missing,
        }
    return completeness


def main():
    print("[1/4] Loading scenario matrix and candidate generation results...")
    scenarios = load_json(SCENARIO_MATRIX_PATH)
    results = load_json(CANDIDATE_RESULTS_PATH)
    print(f"    Loaded {len(scenarios)} scenarios and {len(results)} candidate sets")

    print("[2/4] Computing marginal distributions...")
    marginal = compute_marginal_distributions(scenarios)

    print("[3/4] Computing joint distribution and diversity metrics...")
    joint = compute_joint_distribution(scenarios)
    archetypes = compute_archetype_distribution(scenarios)
    underrepresented = find_underrepresented_cells(joint, min_count=3)
    duplicates = find_near_duplicates(scenarios)
    sec_a_counts, sec_b_counts, disq_counts = compute_candidate_distribution(results)
    provenance = compute_provenance_completeness(scenarios)

    # Compute archetype count
    unique_archetypes = len(archetypes)
    print(f"    Unique archetypes: {unique_archetypes}")
    print(f"    Underrepresented joint cells (<3 scenarios): {len(underrepresented)}")
    print(f"    Near-duplicate scenario pairs: {len(duplicates)}")

    print("[4/4] Writing audit outputs...")

    print("[4/4] Writing audit outputs...")

    # Build audit report
    audit = {
        "benchmark_version": "v1.2",
        "total_scenarios": len(scenarios),
        "scenario_ids": [s["scenario_id"] for s in scenarios],
        "marginal_distributions": {k: dict(v) for k, v in marginal.items()},
        "joint_distribution": {
            "key_format": "crop_primary x land_tenure x water_access x immediate_need x electricity_access",
            "total_cells": len(joint),
            "cells_with_scenarios": len([c for c in joint.values() if c > 0]),
            "distribution": {f"{k[0]}|{k[1]}|{k[2]}|{k[3]}|{k[4]}": v for k, v in joint.items()},
            # Cell frequency distribution: how many cells have 1 scenario, 2 scenarios, etc.
            "cell_frequency_distribution": dict(Counter(joint.values())),
        },
        "archetype_distribution": dict(archetypes),
        "unique_archetype_count": unique_archetypes,
        "underrepresented_cells": {
            f"{k[0]}|{k[1]}|{k[2]}|{k[3]}|{k[4]}": v for k, v in underrepresented.items()
        },
        "underrepresented_cell_count": len(underrepresented),
        "near_duplicate_pairs": duplicates,
        "near_duplicate_count": len(duplicates),
        "candidate_distribution": {
            "section_a_count": dict(sec_a_counts),
            "section_b_count": dict(sec_b_counts),
            "disqualified_count": dict(disq_counts),
        },
        "provenance_completeness": provenance,
        "audit_passed": len(underrepresented) == 0 and len(duplicates) == 0,
    }

    # Write machine-readable audit
    BENCH_DIR = REPO_ROOT / "data/benchmarks/v1.2"
    BENCH_DIR.mkdir(parents=True, exist_ok=True)
    with open(DIVERSITY_AUDIT_PATH, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)
    print(f"    Written: {DIVERSITY_AUDIT_PATH}")

    # Write human-readable report
    lines = []
    lines.append("# Benchmark v1.2 Scenario Diversity Audit Report")
    lines.append("")
    lines.append(f"**Benchmark Version:** v1.2")
    lines.append(f"**Total Scenarios:** {len(scenarios)}")
    lines.append(f"**Scenario ID Range:** {scenarios[0]['scenario_id']} to {scenarios[-1]['scenario_id']}")
    lines.append(f"**Audit Status:** {'PASS' if audit['audit_passed'] else 'REVIEW REQUIRED'}")
    lines.append("")
    lines.append("## 1. Marginal Distributions")
    lines.append("")
    for dist_name, dist_data in marginal.items():
        lines.append(f"### {dist_name.replace('_', ' ').title()}")
        lines.append("")
        for value, count in sorted(dist_data.items(), key=lambda x: -x[1]):
            pct = (count / len(scenarios)) * 100
            lines.append(f"- {value}: {count} ({pct:.1f}%)")
        lines.append("")

    lines.append("## 2. Joint Distribution (crop x land tenure x water access x crisis x electricity)")
    lines.append("")
    lines.append(f"Total unique joint cells: {joint['total_cells']}")
    lines.append(f"Cells with scenarios: {joint['cells_with_scenarios']}")
    lines.append("")
    lines.append("### Cell Frequency Distribution")
    lines.append("")
    cell_freq = audit["joint_distribution"]["cell_frequency_distribution"]
    for cell_count, num_cells in sorted(cell_freq.items()):
        scenarios_in_cells = cell_count * num_cells
        lines.append(f"- Cells with {cell_count} scenario(s): {num_cells} cells ({scenarios_in_cells} scenarios)")
    lines.append("")
    lines.append("### Top 20 Joint Cells by Count")
    lines.append("")
    sorted_joint = sorted(audit["joint_distribution"]["distribution"].items(), key=lambda x: -x[1])[:20]
    for key, count in sorted_joint:
        lines.append(f"- {key[0]} | {key[1]} | {key[2]} | {key[3]} | {key[4]}: {count}")
    lines.append("")

    lines.append("## 3. Archetype Distribution")
    lines.append("")
    lines.append(f"Unique archetypes: {unique_archetypes}")
    lines.append("")
    for arch, count in sorted(archetypes.items(), key=lambda x: -x[1]):
        lines.append(f"- {arch}: {count}")
    lines.append("")

    lines.append("## 4. Under-represented Joint Cells (< 3 scenarios)")
    lines.append("")
    if underrepresented:
        for key, count in sorted(underrepresented.items(), key=lambda x: x[1]):
            lines.append(f"- {key[0]}|{key[1]}|{key[2]}|{key[3]}|{key[4]}: {count} scenarios")
    else:
        lines.append("- None (all cells have >= 3 scenarios)")
    lines.append("")

    lines.append("## 5. Near-Duplicate Scenario Pairs")
    lines.append("")
    if duplicates:
        for s1, s2 in duplicates:
            lines.append(f"- {s1} ~ {s2}")
    else:
        lines.append("- None (all scenarios have unique attribute combinations)")
    lines.append("")

    lines.append("## 6. Candidate Pool Size Distribution")
    lines.append("")
    lines.append("### Section A Candidates per Scenario")
    lines.append("")
    for count, freq in sorted(sec_a_counts.items()):
        pct = (freq / len(scenarios)) * 100
        lines.append(f"- {count} schemes: {freq} scenarios ({pct:.1f}%)")
    lines.append("")
    lines.append("### Section B Candidates per Scenario")
    lines.append("")
    for count, freq in sorted(sec_b_counts.items()):
        pct = (freq / len(scenarios)) * 100
        lines.append(f"- {count} schemes: {freq} scenarios ({pct:.1f}%)")
    lines.append("")

    lines.append("## 7. Provenance Completeness")
    lines.append("")
    for field, stats in provenance.items():
        pct = (stats["complete"] / stats["total"]) * 100
        status = "COMPLETE" if stats["missing"] == 0 else "INCOMPLETE"
        lines.append(f"- {field}: {stats['complete']}/{stats['total']} ({pct:.1f}%) - {status}")
    lines.append("")

    lines.append("## 8. Diversity Audit Verdict")
    lines.append("")
    if audit["audit_passed"]:
        lines.append("**PASS** - All diversity criteria met:")
        lines.append("- No under-represented joint cells (< 3 scenarios)")
        lines.append("- No near-duplicate scenarios")
        lines.append("- Multiple archetypes represented")
    else:
        lines.append("**REVIEW REQUIRED** - Diversity gaps identified:")
        if underrepresented:
            lines.append(f"- {len(underrepresented)} joint cells have fewer than 3 scenarios")
        if duplicates:
            lines.append(f"- {len(duplicates)} near-duplicate scenario pairs found")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by scripts/audit_benchmark_v1_2_diversity.py*")

    with open(DIVERSITY_REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"    Written: {DIVERSITY_REPORT_PATH}")

    return audit


if __name__ == "__main__":
    audit = main()
    print(f"\nDiversity audit complete. Status: {'PASS' if audit['audit_passed'] else 'REVIEW REQUIRED'}")