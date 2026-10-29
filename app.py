"""
app.py
------
Streamlit Web Application: ML-Based Personalized Government Scheme and Subsidy
Recommendation System for Farmers in Karnataka.

End-to-End Demonstrable Application featuring:
- Two-Desk Architecture: Deterministic Eligibility Triage + Benchmark v1.2 ML Ranker
- Strict Section A vs Section B Governance Safeguards
- Explainable Personalization Factors & Official Statutory Citations
- Synthetic Benchmark Presets for Guide Demonstration
"""

import json
import os
from typing import Any, Dict, List

# Suppress loky win32 core count warning on Windows
if "LOKY_MAX_CPU_COUNT" not in os.environ:
    os.environ["LOKY_MAX_CPU_COUNT"] = "4"

import streamlit as st

from src.app.demo_profiles import (
    CROPS,
    DEMO_PROFILES,
    DISTRICTS,
    DISTRICT_TO_ZONE,
    ELECTRICITY_STATUSES,
    FARMER_CATEGORIES,
    IMMEDIATE_NEEDS,
    LAND_TYPES,
    SECONDARY_CONSTRAINTS,
    SOCIAL_CATEGORIES,
    WATER_SOURCES,
    ZONE_TO_NAME,
)
from src.app.service import RecommendationService


st.set_page_config(
    page_title="Karnataka Farmer Subsidy Recommender",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_service() -> RecommendationService:
    """Initialize recommendation service (cached across sessions)."""
    return RecommendationService()


svc = get_service()

# ── Sidebar: Mode & Preset Loader ─────────────────────────────────────────────
st.sidebar.title("🌾 Navigation & Presets")
st.sidebar.markdown(
    """
    **Project Guide Demonstration**
    Select a pre-configured synthetic scenario or enter custom farm data.
    """
)

preset_choice = st.sidebar.selectbox(
    "Choose Profile Preset:",
    options=["Custom Profile"] + list(DEMO_PROFILES.keys()),
    format_func=lambda x: "Custom / Manual Entry"
    if x == "Custom Profile"
    else DEMO_PROFILES[x]["title"],
)

force_heuristic = st.sidebar.checkbox(
    "Force Heuristic Baseline Fallback",
    value=False,
    help="Disables the v1.2 ML ranker to demonstrate comparative baseline fallback behavior.",
)

st.sidebar.markdown("---")
st.sidebar.subheader("System Architecture")
st.sidebar.markdown(
    """
    - **Desk 1: Statutory Eligibility**: Frozen deterministic rule engine (`src/eligibility/engine.py`).
    - **Desk 2: Clinical Ranking**: Benchmark v1.2 HistGradientBoostingRegressor ML model.
    - **Governance Safeguard**: Decouples Section A (actionable) from Section B (advisory).
    """
)
st.sidebar.markdown(
    """
    > **Academic Research Disclaimer**: All demonstration profiles are synthetic benchmark
    scenarios. Recommendations do not constitute legal guarantee of subsidy sanction.
    """
)


# ── Load Preset Data or Defaults ──────────────────────────────────────────────
if preset_choice != "Custom Profile":
    preset_data = DEMO_PROFILES[preset_choice]
    prof = preset_data["profile"]
    st.sidebar.info(f"**Loaded Preset:** {preset_data['description']}")
else:
    # Sensible defaults for manual entry
    prof = {
        "scenario_id": "CUSTOM_FARMER_001",
        "district": "Yadgir",
        "zone_id": "Z1",
        "crop_primary": "Bengalgram",
        "crop_secondary": "Chilli",
        "land_size_acres": 2.0,
        "land_type": "Dryland (Rainfed)",
        "social_category": "General (OC)",
        "farmer_category": "Marginal (1.0-2.5 acres)",
        "existing_assets": [],
        "annual_family_income_lakh": 1.2,
        "immediate_need": "RAINWATER_HARVESTING",
        "paid_income_tax_last_assessment_year": False,
        "govt_employee_category": "NONE",
        "superannuated_pensioner_monthly_amount": 0.0,
        "pensioner_is_mts_exempt": False,
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": True,
        "is_pure_tenant_without_land_title": False,
        "borewell_electric_status": "No electricity",
        "water_and_irrigation": {
            "operational_water_source": "Rainfed (no source)",
            "borewell_electric_status": "No electricity",
        },
        "compound_need_details": {
            "primary_acute_crisis": "CROP_INSURANCE",
            "secondary_constraints": [],
            "narrative": "Farmer seeking government scheme guidance.",
        },
    }

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🌾 Personalized Government Scheme & Subsidy Recommendation System")
st.markdown(
    """
    **State of Karnataka Agricultural Welfare & Subsidy Engine**  
    *Integrates Statutory Eligibility Verification, Governance Safeguards, and Benchmark v1.2 ML Ranking.*
    """
)

# Notification banner regarding ML model state
if svc.has_ml_model:
    st.success(
        "✅ **Benchmark v1.2 ML Ranker Active**: HistGradientBoostingRegressor model loaded from `model_v1.2.0.joblib`."
    )
else:
    st.warning(
        f"⚠️ **Heuristic Fallback Active**: ML model unavailable ({svc.model_load_error}). System will use registered heuristic baseline."
    )


# ── Farmer Profile Input Form ────────────────────────────────────────────────
with st.form("farmer_profile_form"):
    st.subheader("1. Farmer Profile & Agro-Ecological Context")
    st.caption("Fields marked with an asterisk (*) are required for statutory assessment.")

    c1, c2, c3 = st.columns(3)
    with c1:
        dist_idx = (
            DISTRICTS.index(prof["district"])
            if prof.get("district") in DISTRICTS
            else 0
        )
        selected_district = st.selectbox("District *", options=DISTRICTS, index=dist_idx)
        detected_zone = DISTRICT_TO_ZONE.get(selected_district, "Z1")
        st.text_input(
            "Agro-Climatic Zone",
            value=f"{detected_zone}: {ZONE_TO_NAME.get(detected_zone, '')}",
            disabled=True,
            help="Determined automatically by Karnataka agricultural zone classification.",
        )

    with c2:
        social_idx = (
            SOCIAL_CATEGORIES.index(prof["social_category"])
            if prof.get("social_category") in SOCIAL_CATEGORIES
            else 0
        )
        selected_social = st.selectbox(
            "Social Category *",
            options=SOCIAL_CATEGORIES,
            index=social_idx,
            help="Required for corporation-specific schemes (Dr. B.R. Ambedkar, Valmiki, Devaraj Urs, KMDC).",
        )

        farmer_cat_idx = (
            FARMER_CATEGORIES.index(prof["farmer_category"])
            if prof.get("farmer_category") in FARMER_CATEGORIES
            else 0
        )
        selected_farmer_cat = st.selectbox(
            "Farmer Category *",
            options=FARMER_CATEGORIES,
            index=farmer_cat_idx,
            help="Official GoK landholding classification.",
        )

    with c3:
        income_val = float(prof.get("annual_family_income_lakh", 1.0) or 1.0)
        selected_income = st.number_input(
            "Annual Family Income (₹ Lakhs) *",
            min_value=0.0,
            max_value=100.0,
            value=income_val,
            step=0.1,
            help="Used for means-tested income ceilings (e.g. Ganga Kalyana ₹1.5L - ₹2.0L limits).",
        )

    st.markdown("---")
    st.subheader("2. Landholding & Agronomic Details")
    l1, l2, l3 = st.columns(3)

    with l1:
        land_val = float(prof.get("land_size_acres", 2.0) or 2.0)
        selected_land_size = st.number_input(
            "Operational Landholding (Acres) *",
            min_value=0.0,
            max_value=200.0,
            value=land_val,
            step=0.1,
            help="Exact acreage under cultivation.",
        )

    with l2:
        land_type_idx = (
            LAND_TYPES.index(prof["land_type"])
            if prof.get("land_type") in LAND_TYPES
            else 0
        )
        selected_land_type = st.selectbox(
            "Land Type *",
            options=LAND_TYPES,
            index=land_type_idx,
            help="Dryland (Rainfed / Kushki) vs Canal-irrigated (Tari).",
        )

    with l3:
        crop_primary_idx = (
            CROPS.index(prof["crop_primary"])
            if prof.get("crop_primary") in CROPS
            else 0
        )
        selected_crop_primary = st.selectbox(
            "Primary Crop *",
            options=CROPS,
            index=crop_primary_idx,
        )
        crop_sec_idx = (
            CROPS.index(prof.get("crop_secondary"))
            if prof.get("crop_secondary") in CROPS
            else 0
        )
        selected_crop_secondary = st.selectbox(
            "Secondary Crop (Optional)",
            options=["None"] + CROPS,
            index=crop_sec_idx + 1 if prof.get("crop_secondary") in CROPS else 0,
        )

    st.markdown("---")
    st.subheader("3. Water, Energy & Existing Assets")
    w1, w2, w3 = st.columns(3)

    with w1:
        current_water = (prof.get("water_and_irrigation") or {}).get(
            "operational_water_source", "Rainfed (no source)"
        )
        water_idx = (
            WATER_SOURCES.index(current_water)
            if current_water in WATER_SOURCES
            else 0
        )
        selected_water = st.selectbox(
            "Operational Water Source *",
            options=WATER_SOURCES,
            index=water_idx,
        )

    with w2:
        current_elec = prof.get("borewell_electric_status", "No electricity")
        elec_idx = (
            ELECTRICITY_STATUSES.index(current_elec)
            if current_elec in ELECTRICITY_STATUSES
            else 0
        )
        selected_elec = st.selectbox(
            "Borewell / Electricity Status *",
            options=ELECTRICITY_STATUSES,
            index=elec_idx,
            help="Crucial prerequisite for PM-KUSUM Component B (strictly requires off-grid / unenergized status).",
        )

    with w3:
        current_assets = prof.get("existing_assets", [])
        asset_options = ["Tractor", "Borewell", "Farm pond", "Drip irrigation", "Sprinkler set", "Power tiller"]
        selected_assets = st.multiselect(
            "Existing Farm Assets",
            options=asset_options,
            default=[a for a in current_assets if a in asset_options],
        )

    st.markdown("---")
    st.subheader("4. Farming Needs & Operational Context")
    n1, n2 = st.columns(2)

    with n1:
        imm_idx = (
            IMMEDIATE_NEEDS.index(prof["immediate_need"])
            if prof.get("immediate_need") in IMMEDIATE_NEEDS
            else 0
        )
        selected_immediate_need = st.selectbox(
            "Immediate Stated Need *",
            options=IMMEDIATE_NEEDS,
            index=imm_idx,
            format_func=lambda x: x.replace("_", " ").title(),
            help="Farmer's primary self-identified operational priority.",
        )

    with n2:
        current_secondary = (prof.get("compound_need_details") or {}).get(
            "secondary_constraints", []
        )
        selected_secondary = st.multiselect(
            "Secondary Operational Constraints (Optional)",
            options=SECONDARY_CONSTRAINTS,
            default=[s for s in current_secondary if s in SECONDARY_CONSTRAINTS],
            help="Compound constraints used for contextual explainability.",
        )

    st.markdown("---")
    st.subheader("5. Statutory Governance & Exclusion Audit")
    st.caption("Statutory verification checks under official scheme operational guidelines.")

    s1, s2, s3 = st.columns(3)
    with s1:
        tax_val = bool(prof.get("paid_income_tax_last_assessment_year", False))
        paid_tax = st.radio(
            "Paid Income Tax in Last Assessment Year? *",
            options=[False, True],
            index=1 if tax_val else 0,
            format_func=lambda x: "Yes (Income Tax Payee)" if x else "No (Non-Taxpayer)",
            help="Statutory disqualification under PM-KISAN Operational Guidelines §2(d).",
        )

        pure_tenant_val = bool(prof.get("is_pure_tenant_without_land_title", False))
        is_pure_tenant = st.radio(
            "Is Pure Tenant without Land Title? *",
            options=[False, True],
            index=1 if pure_tenant_val else 0,
            format_func=lambda x: "Yes (Pure Tenant — No Land Title)" if x else "No (Land Owner / Title Holder)",
            help="Excludes from landholder-tied subsidies; routes credit needs to tenant crop loan guidelines.",
        )

    with s2:
        govt_emp_val = prof.get("govt_employee_category", "NONE")
        govt_emp_options = ["NONE", "MTS_CLASS_IV_GROUP_D", "OFFICER_REGULAR", "ELECTED_REPRESENTATIVE"]
        govt_idx = govt_emp_options.index(govt_emp_val) if govt_emp_val in govt_emp_options else 0
        govt_emp = st.selectbox(
            "Government Employment Category *",
            options=govt_emp_options,
            index=govt_idx,
            format_func=lambda x: {
                "NONE": "None / Private Sector",
                "MTS_CLASS_IV_GROUP_D": "Multi-Tasking Staff / Group D (Statutorily Exempt)",
                "OFFICER_REGULAR": "Regular Officer / Serving Govt Employee (Excluded)",
                "ELECTED_REPRESENTATIVE": "Constitutional Post / Elected Representative (Excluded)",
            }.get(x, x),
        )

        pension_val = float(prof.get("superannuated_pensioner_monthly_amount", 0.0) or 0.0)
        pension_amt = st.number_input(
            "Superannuated Monthly Pension (₹)",
            min_value=0.0,
            max_value=200000.0,
            value=pension_val,
            step=1000.0,
            help="Pension >= ₹10,000/mo triggers PM-KISAN exclusion unless recipient is exempt MTS/Group D.",
        )

    with s3:
        cutoff_val = bool(prof.get("land_ownership_cutoff_pre_feb_2019", True))
        title_pre_2019 = st.radio(
            "Land Title Acquired on or Before 01.02.2019? *",
            options=[True, False],
            index=0 if cutoff_val else 1,
            format_func=lambda x: "Yes (Pre-01.02.2019)" if x else "No (Post-01.02.2019 Transfer)",
            help="Post-cutoff transfers require succession/death verification under PM-KISAN §5.2.",
        )

        prior_gk = st.checkbox(
            "Family Member Previously Benefited from Ganga Kalyana",
            value=bool(prof.get("prior_ganga_kalyana_in_family", False)),
            help="Strict statutory single-beneficiary-per-family bar under corporation rules.",
        )

    submit_button = st.form_submit_button(
        "🔍 Evaluate Eligibility & Rank Subsidies", type="primary"
    )


# ── Execution and Output Presentation ─────────────────────────────────────────
if submit_button:
    # Build complete profile dictionary
    submitted_profile = {
        "scenario_id": prof.get("scenario_id", "DEMO_USER_001"),
        "benchmark_version": "v1.2",
        "district": selected_district,
        "zone_id": detected_zone,
        "agro_climatic_zone": ZONE_TO_NAME.get(detected_zone, "Unknown Zone"),
        "crop_primary": selected_crop_primary,
        "crop_secondary": None if selected_crop_secondary == "None" else selected_crop_secondary,
        "land_size_acres": selected_land_size,
        "land_type": selected_land_type,
        "social_category": selected_social,
        "farmer_category": selected_farmer_cat,
        "existing_assets": selected_assets,
        "annual_family_income_lakh": selected_income,
        "immediate_need": selected_immediate_need,
        "paid_income_tax_last_assessment_year": paid_tax,
        "is_pure_tenant_without_land_title": is_pure_tenant,
        "govt_employee_category": govt_emp,
        "superannuated_pensioner_monthly_amount": pension_amt,
        "pensioner_is_mts_exempt": govt_emp == "MTS_CLASS_IV_GROUP_D",
        "registered_professional": "NONE",
        "land_ownership_cutoff_pre_feb_2019": title_pre_2019,
        "prior_ganga_kalyana_in_family": prior_gk,
        "borewell_electric_status": selected_elec,
        "water_and_irrigation": {
            "operational_water_source": selected_water,
            "borewell_electric_status": selected_elec,
        },
        "compound_need_details": {
            "primary_acute_crisis": selected_immediate_need,
            "secondary_constraints": selected_secondary,
            "narrative": f"Farmer profile in {selected_district} with {selected_land_size} acres.",
        },
    }

    # Run recommendation service
    with st.spinner("Executing statutory eligibility engine and clinical ranker..."):
        results = svc.recommend(submitted_profile, force_heuristic=force_heuristic)

    if not results["success"]:
        st.error("Input Validation Errors Encountered:")
        for err in results["errors"]:
            st.error(f"- {err}")
    else:
        counts = results["counts"]

        # Metrics Banner
        st.markdown("### 📊 Recommendation Summary")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Evaluated Schemes", counts["total"])
        m2.metric("Section A Actionable", counts["section_a"])
        m3.metric("Section B Advisory", counts["section_b"])
        m4.metric("Disqualified", counts["disqualified"])

        # Ranking Method Indicator Badge
        st.info(f"**Ranking Method:** `{results['ranking_method']}`")

        # Result Tabs
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                f"🏆 Ranked Actionable Subsidies ({counts['section_a']})",
                f"📋 Advisory & Unresolved Evidence ({counts['section_b']})",
                f"🚫 Disqualified Schemes ({counts['disqualified']})",
                "🛠️ Engine Debug & Audit Trace",
            ]
        )

        with tab1:
            st.subheader("Section A: Confirmed Actionable Recommendations")
            st.caption(
                "Statutotily eligible schemes ordered by personalized relevance score. "
                "Numerical scoring strictly applies only to this section."
            )

            if not results["section_a"]:
                st.warning("No actionable schemes identified matching all statutory criteria.")
            else:
                for item in results["section_a"]:
                    with st.container():
                        st.markdown(
                            f"### #{item['rank']} {item['scheme_name']} "
                            f"`Relevance Score: {item['score']:.4f}`"
                        )
                        st.markdown(
                            f"**Department:** {item['department']} | **Benefit Type:** {item['benefit_type']}"
                        )

                        col_left, col_right = st.columns([2, 1])

                        with col_left:
                            st.markdown("#### 💡 Ranking Rationale & Fit Analysis")
                            for r in item["ranking_rationale"]:
                                st.markdown(f"- {r}")

                            st.markdown(
                                f"**Benefit Rate:** {item['benefit_rate']}  \n"
                                f"**Maximum Benefit:** {item['maximum_benefit']}"
                            )

                        with col_right:
                            st.markdown("#### 📄 Required Documentation")
                            docs = item.get("required_documents") or []
                            if docs:
                                for d in docs:
                                    st.markdown(f"- {d}")
                            else:
                                st.caption("Standard Aadhaar, RTC extract, and bank passbook.")

                            if item.get("official_source_url"):
                                st.markdown(f"🔗 [Official Guidelines Reference]({item['official_source_url']})")

                        # Statutory Disclaimer Box
                        st.warning(
                            f"⚠️ **Statutory Caveat**: {item['statutory_disclaimer']}"
                        )
                        st.markdown("---")

        with tab2:
            st.subheader("Section B: Qualitative Advisory & Pending Verification")
            st.caption(
                "Schemes requiring administrative circular, Government Order, or field evidence verification. "
                "Per benchmark governance safeguards, numerical ranking is disabled for these schemes."
            )

            if not results["section_b"]:
                st.info("No candidates routed to Section B for this profile.")
            else:
                for b in results["section_b"]:
                    with st.expander(f"📋 {b['scheme_name']} ({b['presentation_section']})", expanded=True):
                        st.markdown(f"**Department:** {b['department']}")
                        st.error(f"**Advisory Notice:** {b['advisory_warning']}")
                        st.markdown(f"**Governance Findings:** {b['governance_note']}")

                        if b["missing_verifications"]:
                            st.markdown("**Pending Verifications Required:**")
                            for mv in b["missing_verifications"]:
                                st.markdown(f"- ⏳ {mv}")

                        if b.get("official_source_url"):
                            st.markdown(f"🔗 [Official Guidelines Reference]({b['official_source_url']})")

        with tab3:
            st.subheader("Disqualified / Non-Actionable Candidates")
            st.caption("Schemes statutorily barred due to legal exclusions, landholding ceilings, or categorical restrictions.")

            if not results["disqualified"]:
                st.info("No disqualified schemes.")
            else:
                for d in results["disqualified"]:
                    with st.expander(f"🚫 {d['scheme_name']}"):
                        st.markdown("**Disqualification Reasons:**")
                        for reason in d["disqualifying_factors"]:
                            st.markdown(f"- ❌ {reason}")

                        if d["rule_keys_fired"]:
                            st.markdown(
                                f"**Statutory Rule Keys Fired:** `{', '.join(d['rule_keys_fired'])}`"
                            )
                        if d.get("official_source_url"):
                            st.markdown(f"🔗 [Official Reference]({d['official_source_url']})")

        with tab4:
            st.subheader("Diagnostic Trace & Audit Payload")
            st.caption("Raw engine output and feature payload for technical defense and academic audit.")
            st.json(results)

