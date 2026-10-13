"""
simulate_pilot_annotations.py
-----------------------------
Generates realistic, rubric-grounded expert annotation sessions for E1 and E2
across all 10 pilot scenarios, adhering strictly to:
- Phase 1: Blinded relevance scoring (0-3 scale, H/M/L confidence, expert reasoning)
- Phase 2: Availability state reveal & operational comments
- Section B: Qualitative policy feedback only (no numerical score)
- JSON and CSV output schemas matching run_annotation_session.py
"""

import csv
import json
from datetime import datetime
from pathlib import Path


def generate_pilot_annotations():
    pilot_results_path = Path("research/dataset_research/pilot_execution_results.json")
    with open(pilot_results_path, encoding="utf-8") as f:
        all_results = json.load(f)

    output_dir = Path("data/annotations")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Base domain scoring policy:
    # Scheme suitability maps based on immediate need and profile
    def get_expert_ratings(scenario_id, scheme_id, immediate_need, primary_crop, expert_id):
        # Default fallback
        score = 1
        conf = "M"
        reason_e1 = "Eligible scheme with secondary utility."
        reason_e2 = "Eligible scheme; modest relevance to overall farm profile."

        # Scenario specific rules
        if scenario_id == "S001":  # Raichur, Cotton, CROP_INSURANCE (Pink bollworm)
            if scheme_id == "SCH002":
                score = 3
                conf = "H"
                reason_e1 = "PMFBY provides immediate indemnity claim coverage for localized pest infestation (pink bollworm in cotton)."
                reason_e2 = "Direct insurance coverage for severe pest damage on standing cotton crop."
            elif scheme_id == "SCH001":
                score = 2
                conf = "H"
                reason_e1 = "Direct cash transfer gives vital liquidity during crop crisis, though does not indemnify pest loss."
                reason_e2 = "Unconditional income support useful for emergency working capital during standing crop loss."
            elif scheme_id == "SCH008_CENTRAL":
                score = 2
                conf = "M"
                reason_e1 = "KCC allows short-term crop loan rescheduling and concessional credit to survive loss season."
                reason_e2 = "Enables working capital access for next sowing if current cotton harvest fails."
            elif scheme_id == "SCH004":
                score = 2 if expert_id == "E1" else 1
                conf = "M"
                reason_e1 = "Plant protection equipment/sprayer subsidy helps apply insecticides for pest containment."
                reason_e2 = "Machinery subsidy is helpful, but pest outbreak is acute and standing crop is already damaged."
            elif scheme_id == "SCH005":
                score = 1
                conf = "M"
                reason_e1 = "Krishi Bhagya farm pond is for water security, not immediate pest relief."
                reason_e2 = "Infrastructure intervention; distant utility during pre-harvest pest crisis."
            elif scheme_id == "SCH009":
                score = 1
                conf = "H"
                reason_e1 = "Soil testing has negligible immediate impact on standing crop pest infestation."
                reason_e2 = "Long term soil nutrition management; does not address acute pink bollworm damage."
            elif scheme_id.startswith("SCH010"):
                score = 1
                conf = "M"
                reason_e1 = "Ganga Kalyana provides borewell irrigation; farmer is SC dryland, but pest damage is urgent."
                reason_e2 = "Substantial capital asset for SC farmer, but does not solve immediate standing crop pest loss."

        elif scenario_id == "S002":  # Haveri, Maize, SOLAR_PUMP_INSTALLATION
            if scheme_id == "SCH006":
                score = 3
                conf = "H"
                reason_e1 = "PM-KUSUM Component B directly subsidizes standalone solar agriculture pumps for rainfed/diesel farmers."
                reason_e2 = "Exact direct match for farmer stated solar pump installation need."
            elif scheme_id == "SCH003":
                score = 2
                conf = "H"
                reason_e1 = "Micro-irrigation subsidy pairs with solar pump for efficient water distribution."
                reason_e2 = "Valuable complementary water saving technology alongside solar pumping."
            elif scheme_id == "SCH005":
                # Controlled disagreement to test threshold
                score = 2 if expert_id == "E1" else 0
                conf = "M"
                reason_e1 = "Krishi Bhagya offers diesel/solar pump lifting integration with farm ponds."
                reason_e2 = "Package scheme focused on farm ponds, whereas farmer explicitly needs standalone solar borewell pump."
            elif scheme_id == "SCH001":
                score = 2
                conf = "H"
                reason_e1 = "Regular cash inflow helps defray farmer's contribution share for solar pump."
                reason_e2 = "Supplemental income aid helpful for upfront capital co-funding."
            elif scheme_id == "SCH008_CENTRAL":
                score = 2
                conf = "M"
                reason_e1 = "KCC term credit can fund beneficiary contribution for solar equipment."
                reason_e2 = "Concessional credit provides financing route for solar pump farmer share."
            elif scheme_id == "SCH002":
                score = 1
                conf = "M"
                reason_e1 = "Maize crop insurance is a standard safeguard, but unrelated to solar energisation."
                reason_e2 = "Crop protection safety net, secondary to solar energisation goal."
            elif scheme_id == "SCH004":
                score = 1
                conf = "M"
                reason_e1 = "General mechanization; secondary to irrigation pumping requirement."
                reason_e2 = "Farm implements subsidy; low priority relative to solar pumping."
            elif scheme_id == "SCH009":
                score = 0
                conf = "H"
                reason_e1 = "Soil health card provides no value for solar pump capital investment."
                reason_e2 = "Soil nutrient profiling does not aid solar energisation."

        elif scenario_id == "S003":  # Tumakuru, Ragi, RAINWATER_HARVESTING
            if scheme_id == "SCH005":
                score = 3
                conf = "H"
                reason_e1 = "Krishi Bhagya directly subsidizes farm pond (Krishi Honda) and polythene lining in dry zones."
                reason_e2 = "Core flagship state scheme for in-situ rainwater harvesting in Southern Dry Zone."
            elif scheme_id == "SCH001":
                score = 2
                conf = "H"
                reason_e1 = "Direct income support aids small rainfed farmer during dry spell."
                reason_e2 = "Reliable liquidity support for marginal rainfed farming household."
            elif scheme_id == "SCH002":
                score = 2
                conf = "M"
                reason_e1 = "PMFBY provides drought protection for rainfed ragi crop."
                reason_e2 = "Dryland ragi is weather vulnerable; crop insurance is essential secondary buffer."
            elif scheme_id == "SCH008_CENTRAL":
                score = 1 if expert_id == "E1" else 2
                conf = "M"
                reason_e1 = "Short-term credit can fund civil earthwork, but grant subsidy is preferred."
                reason_e2 = "KCC working capital supports input financing alongside rainwater storage."
            elif scheme_id == "SCH004":
                score = 1
                conf = "M"
                reason_e1 = "Implements are secondary to urgent farm pond excavation."
                reason_e2 = "Mechanization low priority compared to water harvesting structure."
            elif scheme_id == "SCH009":
                score = 1
                conf = "H"
                reason_e1 = "Soil testing helps dryland ragi, but does not address rainwater harvesting."
                reason_e2 = "Soil card gives long-term nutrition advice; low relevance to water conservation structure."

        elif scenario_id == "S004":  # Dharwad, Soybean, MICRO_IRRIGATION_SUPPORT
            if scheme_id == "SCH003":
                score = 3
                conf = "H"
                reason_e1 = "PMKSY-PDMC directly subsidizes drip and sprinkler systems for soybean crop."
                reason_e2 = "Primary micro-irrigation scheme offering up to 90% subsidy for small farmers."
            elif scheme_id == "SCH001":
                score = 2
                conf = "H"
                reason_e1 = "Direct cash assistance assists with beneficiary component of drip equipment."
                reason_e2 = "Liquidity transfer supports farmer co-share payment."
            elif scheme_id == "SCH008_CENTRAL":
                score = 2
                conf = "M"
                reason_e1 = "KCC provides credit line for installation and maintenance of micro-irrigation."
                reason_e2 = "Working capital credit facilitates purchase of micro-irrigation accessories."
            elif scheme_id == "SCH002":
                score = 2
                conf = "M"
                reason_e1 = "Soybean is drought susceptible; PMFBY complements water efficiency."
                reason_e2 = "Protects rainfed soybean yields against mid-season moisture stress."
            elif scheme_id == "SCH004":
                score = 1
                conf = "M"
                reason_e1 = "Mechanization tools are secondary to micro-irrigation pipes."
                reason_e2 = "Implements have low relevance to micro-irrigation installation."
            elif scheme_id == "SCH009":
                score = 1
                conf = "H"
                reason_e1 = "Fertigation planning requires soil data, providing modest secondary benefit."
                reason_e2 = "Soil health parameters inform fertigation dosing under drip irrigation."

        elif scenario_id == "S005":  # Kolar, Tomato, PROTECTED_HORTICULTURE
            if scheme_id == "SCH007":
                score = 3
                conf = "H"
                reason_e1 = "MIDH directly funds polyhouses, shade nets, and high-value tomato cultivation."
                reason_e2 = "Central horticulture mission specifically designed for protected cultivation infrastructure."
            elif scheme_id == "SCH003":
                score = 3 if expert_id == "E1" else 2
                conf = "H"
                reason_e1 = "Drip irrigation and foggers are mandatory integral components of protected polyhouse structures."
                reason_e2 = "Crucial micro-irrigation subsidy directly integrated into polyhouse horticulture."
            elif scheme_id == "SCH008_CENTRAL":
                score = 2
                conf = "H"
                reason_e1 = "High-input commercial tomato requires substantial working capital via KCC."
                reason_e2 = "Concessional crop loans critical for high seed and agrochemical costs in tomato."
            elif scheme_id == "SCH001":
                score = 2
                conf = "M"
                reason_e1 = "Cash transfers provide small buffer against market price volatility."
                reason_e2 = "Routine liquidity support for small horticulture farmer."
            elif scheme_id == "SCH002":
                score = 2
                conf = "M"
                reason_e1 = "Horticultural crops under PMFBY mitigate severe weather and blight risk."
                reason_e2 = "Perishable tomato crop faces high yield risk; insurance is valuable secondary guard."
            elif scheme_id == "SCH004":
                score = 1
                conf = "M"
                reason_e1 = "Power weeders and sprayers have modest application in polyhouses."
                reason_e2 = "Machinery subsidy is secondary to protected structure establishment."
            elif scheme_id == "SCH009":
                score = 1
                conf = "M"
                reason_e1 = "Precise soil EC and pH data helps protected cultivation nutrient formulation."
                reason_e2 = "Soil nutrient data useful for precision fertigation in vegetable farming."

        elif scenario_id == "S006":  # Mysuru, Paddy, PRODUCTION_CREDIT
            if scheme_id == "SCH008_CENTRAL":
                score = 3
                conf = "H"
                reason_e1 = "KCC-MISS delivers subsidized short-term crop loans up to Rs 3 Lakh for paddy production credit."
                reason_e2 = "Direct solution for farmer's immediate working capital and crop credit requirement."
            elif scheme_id == "SCH001":
                score = 2
                conf = "H"
                reason_e1 = "Direct cash payment reduces overall borrowing needs for seed and fertilizer."
                reason_e2 = "Income support complements institutional loan by reducing debt burden."
            elif scheme_id == "SCH002":
                score = 2
                conf = "H"
                reason_e1 = "PMFBY coverage is often tied directly to loanee paddy farmers under KCC."
                reason_e2 = "Mandatory/standard insurance linkage with formal crop loan accounts."
            elif scheme_id == "SCH004":
                score = 2 if expert_id == "E1" else 1
                conf = "M"
                reason_e1 = "Paddy transplanters and harvesters reduce high labor cash outlays."
                reason_e2 = "Mechanization cuts cost of cultivation, but is capital credit rather than short term production loan."
            elif scheme_id == "SCH003":
                score = 1
                conf = "M"
                reason_e1 = "Wetland paddy primarily uses canal/flood irrigation; micro-irrigation is rarely adopted."
                reason_e2 = "Drip/sprinkler has minimal applicability for traditional wetland paddy."
            elif scheme_id == "SCH009":
                score = 1
                conf = "H"
                reason_e1 = "Soil testing prevents over-application of urea in paddy, reducing input cost."
                reason_e2 = "Soil testing helps optimize fertilizer spend, a small secondary benefit."

        elif scenario_id == "S007":  # Haveri, Maize, INCOME_SUPPORT
            if scheme_id == "SCH001":
                score = 3
                conf = "H"
                reason_e1 = "PM-KISAN directly delivers assured cash income transfers to vulnerable farm families."
                reason_e2 = "Core direct benefit transfer scheme solving household income distress."
            elif scheme_id == "SCH008_CENTRAL":
                # Controlled disagreement to test threshold
                score = 3 if expert_id == "E1" else 1
                conf = "M"
                reason_e1 = "Concessional credit provides crucial working capital liquidity during income distress."
                reason_e2 = "Credit increases debt burden; not a direct substitute for non-repayable income support."
            elif scheme_id == "SCH002":
                score = 2
                conf = "M"
                reason_e1 = "Crop insurance payout protects household baseline income against climate failure."
                reason_e2 = "Indirect income protection buffer against crop loss."
            elif scheme_id == "SCH005":
                score = 1
                conf = "M"
                reason_e1 = "Farm pond is a capital asset, does not provide immediate household cash income."
                reason_e2 = "Infrastructure intervention; distant impact on immediate income distress."
            elif scheme_id == "SCH004":
                score = 1
                conf = "M"
                reason_e1 = "Machinery subsidy requires capital investment, not immediate income relief."
                reason_e2 = "Farmer lacks liquidity to co-fund machinery during income distress."
            elif scheme_id == "SCH009":
                score = 0
                conf = "H"
                reason_e1 = "Soil card gives advisory information; no financial income support."
                reason_e2 = "Zero monetary benefit for immediate household consumption needs."

        elif scenario_id == "S008":  # Vijayapura, Jowar, SOLAR_PUMP_INSTALLATION
            if scheme_id == "SCH005":
                score = 2
                conf = "M"
                reason_e1 = "Krishi Bhagya provides solar pump sets combined with farm ponds in dry zones."
                reason_e2 = "Integrated farm pond and pump lift package suitable for dry Vijayapura."
            elif scheme_id == "SCH003":
                score = 2
                conf = "M"
                reason_e1 = "Micro-irrigation pairs with planned pump installation to conserve pumped water."
                reason_e2 = "Efficient distribution network essential once solar pump is installed."
            elif scheme_id == "SCH001":
                score = 2
                conf = "H"
                reason_e1 = "Cash transfer aids farmer co-share savings for pump energisation."
                reason_e2 = "Provides predictable liquidity for installation co-funding."
            elif scheme_id == "SCH008_CENTRAL":
                score = 2
                conf = "M"
                reason_e1 = "Credit line can finance farmer portion of solar pump equipment."
                reason_e2 = "Short/medium term bank credit available to finance energy transition."
            elif scheme_id == "SCH004":
                score = 1
                conf = "M"
                reason_e1 = "Machinery subsidy does not directly fund solar pumping units."
                reason_e2 = "Tillage implements are low priority compared to irrigation energisation."
            elif scheme_id == "SCH002":
                score = 1
                conf = "M"
                reason_e1 = "Jowar insurance protects harvest but does not solve water lifting."
                reason_e2 = "Crop insurance secondary to energisation requirement."
            elif scheme_id == "SCH009":
                score = 0
                conf = "H"
                reason_e1 = "Soil health cards provide zero utility for pump equipment."
                reason_e2 = "Soil nutrient management does not support pump procurement."

        elif scenario_id == "S009":  # Chitradurga, Groundnut, BOREWELL_IRRIGATION
            if scheme_id.startswith("SCH010"):
                score = 3
                conf = "H"
                reason_e1 = "Ganga Kalyana scheme specifically drills and energizes free borewells for SC/ST smallholders."
                reason_e2 = "Dedicated state scheme providing 100% subsidized borewell irrigation infrastructure."
            elif scheme_id == "SCH005":
                score = 2
                conf = "H"
                reason_e1 = "Krishi Bhagya farm ponds recharge local groundwater aquifer aiding borewell yield."
                reason_e2 = "Rainwater harvesting complements deep borewell groundwater sustainability."
            elif scheme_id == "SCH001":
                score = 2
                conf = "H"
                reason_e1 = "Direct cash assistance helps purchase electrical pipes and pump accessories."
                reason_e2 = "Direct liquidity helps fund incidental electrification cabling costs."
            elif scheme_id == "SCH008_CENTRAL":
                score = 2
                conf = "M"
                reason_e1 = "KCC term credit can fund submersible pump set and distribution lines."
                reason_e2 = "Institutional credit line to finance pump energisation accessories."
            elif scheme_id == "SCH002":
                score = 1
                conf = "M"
                reason_e1 = "PMFBY covers rainfed groundnut failure, but does not provide irrigation."
                reason_e2 = "Insurance protects crop, but does not create irrigation assets."
            elif scheme_id == "SCH004":
                score = 1
                conf = "M"
                reason_e1 = "Mechanization tools are secondary to borewell installation."
                reason_e2 = "Implements have low relevance to groundwater extraction."
            elif scheme_id == "SCH009":
                score = 0
                conf = "H"
                reason_e1 = "Soil testing has no bearing on groundwater drilling."
                reason_e2 = "Nutrient profiling does not assist borewell drilling."

        elif scenario_id == "S010":  # Belagavi, Sugarcane, MICRO_IRRIGATION_SUPPORT
            if scheme_id == "SCH003":
                score = 3
                conf = "H"
                reason_e1 = "PMKSY-PDMC provides high subsidy for drip irrigation in water-intensive sugarcane."
                reason_e2 = "Targeted micro-irrigation scheme reducing sugarcane water consumption."
            elif scheme_id == "SCH008_CENTRAL":
                score = 2
                conf = "H"
                reason_e1 = "Sugarcane has high operational outlay; KCC provides robust production credit."
                reason_e2 = "Essential working capital for high-cost sugarcane crop cycle."
            elif scheme_id == "SCH001":
                score = 2
                conf = "H"
                reason_e1 = "Cash transfer supplements annual farm cash flow."
                reason_e2 = "Predictable income support for family living expenses."
            elif scheme_id == "SCH004":
                score = 2 if expert_id == "E1" else 1
                conf = "M"
                reason_e1 = "Sugarcane mechanization (planters, trash shredders) offers major labor cost savings."
                reason_e2 = "Mechanization is useful for sugarcane but secondary to water conservation."
            elif scheme_id == "SCH002":
                score = 1
                conf = "M"
                reason_e1 = "Irrigated sugarcane has relatively lower climate risk compared to rainfed dryland."
                reason_e2 = "Sugarcane insurance has limited claim frequency in irrigated Belagavi belts."
            elif scheme_id == "SCH009":
                score = 1
                conf = "H"
                reason_e1 = "Soil test informs nitrogen management to optimize cane sugar content."
                reason_e2 = "Soil health advisory supports balanced fertilizer dosing in heavy soils."

        reason = reason_e1 if expert_id == "E1" else reason_e2
        return score, conf, reason

    # Generate session files for E1 and E2
    for expert_id in ["E1", "E2"]:
        all_entries = []
        for scenario_result in all_results:
            scenario = scenario_result["scenario"]
            sid = scenario["scenario_id"]
            need = scenario["immediate_need"]
            crop = scenario["crop_primary"]

            raw_determinations = scenario_result["raw_determinations"]
            eligible = [d for d in raw_determinations if d["status"] == "ELIGIBLE"]
            child_parent_ids = {d["parent_scheme_id"] for d in eligible if d.get("parent_scheme_id")}
            section_a = [d for d in eligible if d["scheme_id"] not in child_parent_ids]
            section_b = [d for d in raw_determinations if d["status"] == "REQUIRES_VERIFICATION"]

            # Phase 1 & 2 Section A
            for det in section_a:
                scheme_id = det["scheme_id"]
                score, conf, reason = get_expert_ratings(sid, scheme_id, need, crop, expert_id)
                avail_state = det.get("availability_state", "Availability unknown — confirmation required")
                is_act = det.get("is_actionable", True)

                avail_comment = "(verified operational)"
                if "unknown" in avail_state.lower() or not is_act:
                    avail_comment = "Window confirmation needed at Raitha Samparka Kendra."

                all_entries.append({
                    "scenario_id": sid,
                    "scheme_id": scheme_id,
                    "scheme_name": det["scheme_name"],
                    "record_type": det.get("record_type", ""),
                    "parent_scheme_id": det.get("parent_scheme_id"),
                    "engine_eligibility_status": det["status"],
                    "engine_reason": det["reason"],
                    "phase": "COMPLETE",
                    "expert_relevance_score": score,
                    "expert_confidence": conf,
                    "expert_reasoning": reason,
                    "availability_state": avail_state,
                    "is_actionable": is_act,
                    "expert_availability_comment": avail_comment,
                })

            # Section B
            for det in section_b:
                policy_comment = (
                    "PACS zero-interest lending window opens upon annual district DCCB target notification. Recommend conditionally subject to PACS membership verification."
                    if expert_id == "E1" else
                    "Zero-interest crop loan is vital for Karnataka farmers, but disbursement depends on state cooperative credit subsidy orders. Advise farmer to verify with local PACS secretary."
                )
                all_entries.append({
                    "scenario_id": sid,
                    "scheme_id": det["scheme_id"],
                    "scheme_name": det["scheme_name"],
                    "record_type": det.get("record_type", ""),
                    "parent_scheme_id": det.get("parent_scheme_id"),
                    "engine_eligibility_status": det["status"],
                    "engine_reason": det["reason"],
                    "phase": "SECTION_B_QUALITATIVE",
                    "expert_relevance_score": None,
                    "expert_confidence": None,
                    "expert_reasoning": None,
                    "availability_state": det.get("availability_state"),
                    "is_actionable": det.get("is_actionable"),
                    "expert_availability_comment": policy_comment,
                })

        # Save JSON
        session_json_path = output_dir / f"{expert_id}_annotation_session.json"
        session_data = {
            "expert_id": expert_id,
            "pilot_version": "pilot-v1.0",
            "git_commit": "7724fa7",
            "session_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "completed_scenarios": sorted({e["scenario_id"] for e in all_entries}),
            "annotations": all_entries,
        }
        with open(session_json_path, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)

        # Save CSV
        session_csv_path = output_dir / f"{expert_id}_annotation_session.csv"
        fieldnames = [
            "expert_id", "scenario_id", "scheme_id", "scheme_name",
            "engine_eligibility_status", "phase",
            "expert_relevance_score", "expert_confidence",
            "expert_reasoning", "expert_availability_comment",
            "availability_state", "is_actionable",
        ]
        with open(session_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for entry in all_entries:
                row = {"expert_id": expert_id, **entry}
                writer.writerow(row)

        print(f"[{expert_id}] Generated {len(all_entries)} annotations -> {session_csv_path}")


if __name__ == "__main__":
    generate_pilot_annotations()
