"""
Benchmark v1.0.4 Committed Artifact Integrity Validator.
Comprehensive cross-zone integrity validator that verifies all 60 committed scenario profiles,
batch scenarios, and execution result files on disk.

Validates:
1. Version Consistency: Every scenario, batch file, and execution result declares v1.0.4.
2. Profile Completeness & Schema: All required fields present, parseable by FarmerScenario model.
3. Assignment Matrix Fidelity: Attributes match the canonical 60-scenario matrix in validate_benchmark_matrix.py.
4. Statutory Succession Contract: S039, S049, S064, S069 contain structured succession details with §§5.2–5.3.3(i) vs §5.3.3(ii).
5. Execution Results & Governance Presentation:
   - 16 raw evaluations per scenario.
   - Parent deduplication (SCH008, SCH010 suppressed when concrete children are actionable).
   - Governance status, presentation section, and scoring flag consistency:
     * Section A: allow_numerical_scoring == True, governance_status == ELIGIBLE.
     * Section B: allow_numerical_scoring == False, governance_status in [REQUIRES_VERIFICATION, INELIGIBLE].
     * Disqualified: allow_numerical_scoring == False, governance_status == INELIGIBLE.
   - PMFBY routed to Section B with scoring disabled across all 60 scenarios.
   - Pure tenants (S026, S042, S044, S061, S068) excluded from PM-KISAN and KCC in Section B.
   - Unknown titles (S048, S056, S062, S070) preserved in Section B without scoring.
   - Provisional corporation schemes quarantined in Section B.
   - Availability state decoupling: all determinations have AVAILABILITY_UNKNOWN.
"""

import os
import sys
import json
from typing import List, Dict, Any, Tuple

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, WORKSPACE_ROOT)

from src.eligibility.models import FarmerScenario, EligibilityStatus, AvailabilityState
from research.dataset_research.validate_benchmark_matrix import scenarios, HA_PER_ACRE

REQUIRED_SCENARIO_KEYS = [
    "scenario_id", "benchmark_version", "zone_id", "agro_climatic_zone",
    "district", "crop_primary", "land_size_acres", "land_type",
    "social_category", "farmer_category", "existing_assets",
    "annual_family_income_lakh", "immediate_need",
    "paid_income_tax_last_assessment_year", "govt_employee_category",
    "superannuated_pensioner_monthly_amount", "pensioner_is_mts_exempt",
    "registered_professional", "land_ownership_cutoff_pre_feb_2019",
    "is_pure_tenant_without_land_title", "borewell_electric_status",
    "landholding_details", "water_and_irrigation", "statutory_flags",
    "attribute_provenance", "intended_test_purpose", "unresolved_dependencies"
]

INHERITANCE_SIDS = {"S039", "S049", "S064", "S069"}
PURE_TENANT_SIDS = {"S026", "S042", "S044", "S061", "S068"}
UNKNOWN_TITLE_SIDS = {"S048", "S056", "S062", "S070"}
PROVISIONAL_SCHEMES = {"SCH008_KA_COOP", "SCH010_VALMIKI", "SCH010_DEVARAJ_URS", "SCH010_KMDC"}


def validate_all_benchmark_artifacts() -> Tuple[bool, List[str]]:
    """Runs all integrity checks across committed benchmark files. Returns (success, list_of_errors)."""
    errors = []
    matrix_by_id = {s["sid"]: s for s in scenarios}

    all_profiles: Dict[str, Dict[str, Any]] = {}
    all_executions: Dict[str, Dict[str, Any]] = {}

    print("\n--- 1. Checking File Existence & Loading Profiles ---")
    expected_sids = [f"S{i:03d}" for i in range(11, 71)]
    assert len(expected_sids) == 60

    for z in range(1, 11):
        z_dir = os.path.join(WORKSPACE_ROOT, "data", "benchmarks", f"z{z}")
        if not os.path.exists(z_dir):
            errors.append(f"Zone directory missing: {z_dir}")
            continue

        batch_file = os.path.join(z_dir, f"z{z}_scenarios.json")
        exec_file = os.path.join(z_dir, f"z{z}_execution_results.json")
        report_file = os.path.join(WORKSPACE_ROOT, "reports", f"zone_z{z}_execution_report.md")

        if not os.path.exists(batch_file):
            errors.append(f"Missing batch scenario file: {batch_file}")
        if not os.path.exists(exec_file):
            errors.append(f"Missing execution results file: {exec_file}")
        if not os.path.exists(report_file):
            errors.append(f"Missing report file: {report_file}")

        # Load batch scenarios
        if os.path.exists(batch_file):
            with open(batch_file, "r", encoding="utf-8") as f:
                batch_data = json.load(f)
            if len(batch_data) != 6:
                errors.append(f"Zone Z{z} batch file contains {len(batch_data)} profiles (expected 6)")
            for p in batch_data:
                sid = p.get("scenario_id")
                all_profiles[sid] = p

        # Load execution results
        if os.path.exists(exec_file):
            with open(exec_file, "r", encoding="utf-8") as f:
                exec_data = json.load(f)
            all_executions[f"Z{z}"] = exec_data

        # Check individual JSON and MD files
        z_start = (z - 1) * 6 + 11
        for sid_num in range(z_start, z_start + 6):
            sid = f"S{sid_num:03d}"
            ind_json = os.path.join(z_dir, f"{sid}.json")
            ind_md = os.path.join(z_dir, f"{sid}.md")
            if not os.path.exists(ind_json):
                errors.append(f"Missing individual scenario JSON: {ind_json}")
            if not os.path.exists(ind_md):
                errors.append(f"Missing individual scenario MD: {ind_md}")

    print(f"Total scenario profiles loaded: {len(all_profiles)} / 60")
    if set(all_profiles.keys()) != set(expected_sids):
        errors.append(f"Scenario IDs mismatch: missing {set(expected_sids) - set(all_profiles.keys())}")

    print("\n--- 2. Checking Version Consistency (v1.0.4) ---")
    for sid, p in all_profiles.items():
        ver = p.get("benchmark_version")
        if ver != "v1.0.4":
            errors.append(f"{sid}: declared benchmark_version is '{ver}' (expected 'v1.0.4')")

    for zid, ed in all_executions.items():
        ver = ed.get("benchmark_version")
        if ver != "v1.0.4":
            errors.append(f"{zid} execution results: benchmark_version is '{ver}' (expected 'v1.0.4')")
        for res in ed.get("results", []):
            # execution results store the profile under 'scenario' key (not 'profile')
            scenario_block = res.get("scenario") or res.get("profile") or {}
            prof_ver = scenario_block.get("benchmark_version")
            sid_in_res = scenario_block.get("scenario_id") or res.get("scenario_id")
            if prof_ver != "v1.0.4":
                errors.append(f"{zid} - {sid_in_res}: profile in results has version '{prof_ver}' (expected 'v1.0.4')")

    print("\n--- 3. Checking Profile Required Fields & Domain Schema ---")
    for sid, p in all_profiles.items():
        for k in REQUIRED_SCENARIO_KEYS:
            if k not in p:
                errors.append(f"{sid}: missing required key '{k}'")

        # Verify FarmerScenario domain model instantiation
        try:
            engine_keys = {
                "scenario_id", "agro_climatic_zone", "district", "crop_primary",
                "land_size_acres", "land_type", "social_category", "farmer_category",
                "existing_assets", "annual_family_income_lakh", "immediate_need",
                "paid_income_tax_last_assessment_year", "govt_employee_category",
                "superannuated_pensioner_monthly_amount", "pensioner_is_mts_exempt",
                "registered_professional", "land_ownership_cutoff_pre_feb_2019",
                "is_pure_tenant_without_land_title", "borewell_electric_status",
                "prior_micro_irrigation_subsidy_years_ago", "prior_farm_pond_subsidy_years_ago",
                "prior_machinery_subsidy_years_ago", "prior_ganga_kalyana_in_family",
                "community_pool_acres", "community_pool_beneficiaries_count",
                "crop_secondary", "farming_stage", "season", "kcc_query_text_example"
            }
            filtered = {k: p[k] for k in engine_keys if k in p}
            sc_obj = FarmerScenario.from_dict(filtered)
            assert sc_obj.scenario_id == sid
        except Exception as e:
            errors.append(f"{sid}: Failed to instantiate FarmerScenario domain model: {str(e)}")

    print("\n--- 4. Checking Assignment Matrix Alignment ---")
    for sid, p in all_profiles.items():
        mat = matrix_by_id.get(sid)
        if not mat:
            errors.append(f"{sid}: Not found in canonical assignment matrix")
            continue

        if p["district"] != mat["dist"]:
            errors.append(f"{sid}: district '{p['district']}' != matrix '{mat['dist']}'")

        expected_crop = "Paddy" if mat["crop"] == "Coastal Paddy" else mat["crop"]
        if p["crop_primary"] != expected_crop:
            errors.append(f"{sid}: crop '{p['crop_primary']}' != matrix '{expected_crop}'")

        if p["land_size_acres"] != mat["total_holding"]:
            errors.append(f"{sid}: land_size_acres {p['land_size_acres']} != matrix {mat['total_holding']}")

        if p["immediate_need"] != mat["need"]:
            errors.append(f"{sid}: immediate_need '{p['immediate_need']}' != matrix '{mat['need']}'")

        qual_ac = p.get("landholding_details", {}).get("qualifying_parcel_acres")
        if qual_ac != mat["qual_parcel"]:
            errors.append(f"{sid}: qualifying_parcel_acres {qual_ac} != matrix {mat['qual_parcel']}")

        # Physical capacity cross-field check
        req_ha = p.get("landholding_details", {}).get("requested_subsidized_area_ha")
        if req_ha is not None:
            max_ha = qual_ac * HA_PER_ACRE
            if req_ha > (max_ha + 1e-4):
                errors.append(f"{sid}: requested_subsidized_area_ha {req_ha} > parcel capacity {max_ha:.4f} ha")

    print("\n--- 5. Checking Structured Statutory Succession Contract (S039, S049, S064, S069) ---")
    for sid in INHERITANCE_SIDS:
        p = all_profiles.get(sid)
        if not p:
            continue
        if "statutory_succession_details" not in p:
            errors.append(f"{sid}: Missing top-level 'statutory_succession_details' contract")
            continue
        ssd = p["statutory_succession_details"]
        if ssd.get("transfer_basis") != "INHERITANCE_DUE_TO_DEATH":
            errors.append(f"{sid}: transfer_basis must be 'INHERITANCE_DUE_TO_DEATH', found '{ssd.get('transfer_basis')}'")
        if not ssd.get("parent_demise_date"):
            errors.append(f"{sid}: parent_demise_date missing")
        if not ssd.get("death_certificate_number"):
            errors.append(f"{sid}: death_certificate_number missing")
        if not ssd.get("legal_heir_certificate_number"):
            errors.append(f"{sid}: legal_heir_certificate_number missing")
        if not ssd.get("mutation_extract_form_16"):
            errors.append(f"{sid}: mutation_extract_form_16 missing")
        auth = ssd.get("statutory_authority", "")
        if "5.2" not in auth or "5.3.3(i)" not in auth:
            errors.append(f"{sid}: statutory_authority must cite §§5.2–5.3.3(i), found '{auth}'")
        dist = ssd.get("statutory_distinction", "")
        if "5.3.3(ii)" not in dist or "partition" not in dist.lower():
            errors.append(f"{sid}: statutory_distinction must cite §5.3.3(ii) and distinguish partition deeds, found '{dist}'")

    print("\n--- 6. Checking Execution Results & Governance Decoupling ---")
    for zid, ed in all_executions.items():
        results = ed.get("results", [])
        if len(results) != 6:
            errors.append(f"{zid}: results list has {len(results)} items (expected 6)")

        for res in results:
            # scenario_id may be top-level or nested inside the 'scenario' block
            scenario_block = res.get("scenario") or res.get("profile") or {}
            sid = scenario_block.get("scenario_id") or res.get("scenario_id")
            raw_dets = res.get("raw_determinations", [])
            act_dets = res.get("actionable_determinations", [])

            if len(raw_dets) != 16:
                errors.append(f"{sid}: Evaluated {len(raw_dets)} raw determinations (expected exactly 16)")

            if len(act_dets) not in [14, 15]:
                errors.append(f"{sid}: Actionable determinations count is {len(act_dets)} (expected 14 or 15)")

            act_schemes = {d["scheme_id"] for d in act_dets}

            # Parent deduplication check:
            # SCH008 must always be suppressed because SCH008_CENTRAL is always actionable (SA or SB)
            if "SCH008" in act_schemes:
                errors.append(f"{sid}: Abstract parent SCH008 must be suppressed from actionable determinations")

            # SCH010 parent suppression check: suppressed when any corporation child is ELIGIBLE or REQUIRES_VERIFICATION
            corp_children = {"SCH010_AMBEDKAR", "SCH010_VALMIKI", "SCH010_DEVARAJ_URS", "SCH010_KMDC"}
            has_actionable_corp_child = any(
                d["scheme_id"] in corp_children and d["raw_engine_status"] in ["ELIGIBLE", "REQUIRES_VERIFICATION"]
                for d in act_dets
            )
            if has_actionable_corp_child and "SCH010" in act_schemes:
                errors.append(f"{sid}: Abstract parent SCH010 must be suppressed when actionable corporation child is present")
            elif not has_actionable_corp_child and "SCH010" not in act_schemes:
                errors.append(f"{sid}: Ineligible parent SCH010 must be retained in Disqualified when no child is actionable")

            for d in act_dets:
                scheme_id = d.get("scheme_id")
                sec = d.get("presentation_section", "")
                scoring = d.get("allow_numerical_scoring")
                gov_status = d.get("governance_status")
                raw_status = d.get("raw_engine_status")
                avail_state = d.get("availability_state")

                # Availability check: must be AVAILABILITY_UNKNOWN
                if avail_state != AvailabilityState.AVAILABILITY_UNKNOWN.value:
                    errors.append(f"{sid} - {scheme_id}: Expected AVAILABILITY_UNKNOWN, got '{avail_state}'")

                # Section & Scoring consistency
                if sec.startswith("Section A"):
                    if scoring is not True:
                        errors.append(f"{sid} - {scheme_id}: Section A must have allow_numerical_scoring=True")
                    if gov_status != "ELIGIBLE":
                        errors.append(f"{sid} - {scheme_id}: Section A must have governance_status=ELIGIBLE, got '{gov_status}'")
                elif sec.startswith("Section B"):
                    if scoring is not False:
                        errors.append(f"{sid} - {scheme_id}: Section B must have allow_numerical_scoring=False")
                    if gov_status not in ["REQUIRES_VERIFICATION", "INELIGIBLE"]:
                        errors.append(f"{sid} - {scheme_id}: Section B must have REQUIRES_VERIFICATION/INELIGIBLE, got '{gov_status}'")
                elif sec.startswith("Disqualified"):
                    if scoring is not False:
                        errors.append(f"{sid} - {scheme_id}: Disqualified must have allow_numerical_scoring=False")
                    if gov_status != "INELIGIBLE":
                        errors.append(f"{sid} - {scheme_id}: Disqualified must have governance_status=INELIGIBLE, got '{gov_status}'")
                else:
                    errors.append(f"{sid} - {scheme_id}: Unknown presentation_section '{sec}'")

                # PMFBY check
                if scheme_id == "SCH002":
                    if not sec.startswith("Section B") or scoring is not False or gov_status != "REQUIRES_VERIFICATION":
                        errors.append(f"{sid}: PMFBY (SCH002) must be in Section B as REQUIRES_VERIFICATION with scoring disabled")

                # Provisional schemes check
                if scheme_id in PROVISIONAL_SCHEMES:
                    if sec.startswith("Section A") or scoring is True:
                        errors.append(f"{sid} - {scheme_id}: Provisional scheme must NEVER be in Section A with scoring enabled")

                # Pure tenancy check
                if sid in PURE_TENANT_SIDS:
                    if scheme_id == "SCH001" and gov_status != "INELIGIBLE":
                        errors.append(f"{sid}: Pure tenant must be INELIGIBLE for PM-KISAN, got '{gov_status}'")
                    if scheme_id == "SCH008_CENTRAL" and (sec.startswith("Section A") or scoring is True):
                        errors.append(f"{sid}: Pure tenant Central KCC must be in Section B with scoring disabled")

                # Unknown title check
                if sid in UNKNOWN_TITLE_SIDS:
                    if scheme_id == "SCH001" and (sec.startswith("Section A") or scoring is True or gov_status != "REQUIRES_VERIFICATION"):
                        errors.append(f"{sid}: Unknown title PM-KISAN must be in Section B as REQUIRES_VERIFICATION without scoring")

    print("\n--------------------------------------------------")
    if not errors:
        print("OVERALL ARTIFACT INTEGRITY STATUS: ALL 60 SCENARIOS & ARTIFACTS PASS PERFECTLY (v1.0.4)!")
        return True, []
    else:
        print(f"OVERALL ARTIFACT INTEGRITY STATUS: {len(errors)} ERRORS DETECTED!")
        for err in errors[:20]:
            print(f"  - {err}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors")
        return False, errors


if __name__ == "__main__":
    success, errors = validate_all_benchmark_artifacts()
    sys.exit(0 if success else 1)
