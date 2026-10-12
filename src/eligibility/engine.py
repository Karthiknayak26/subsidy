"""
Deterministic Eligibility Engine for Agricultural Welfare & Subsidy Schemes.

Translates verified official government guidelines into deterministic rule functions.
Implements:
- Three-Valued Logic: ELIGIBLE, INELIGIBLE, REQUIRES_VERIFICATION
- Statutory exclusion evaluation with statutory exemptions (e.g. MTS exemption)
- Corporation-specific rules for Ganga Kalyana (Ambedkar 1.5-5.0 ac & >=3 pooled beneficiaries)
- Deduplication of parent records from actionable recommendations
- Transparent tracking of rule keys fired and missing information
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple

from .models import (
    FarmerScenario,
    SchemeDetermination,
    EligibilityStatus,
    GovtEmployeeCategory,
    BorewellElectricStatus,
    AvailabilityState
)


RAINFED_DRYLAND_DISTRICTS = {
    "Raichur", "Haveri", "Tumakuru", "Vijayapura", "Chitradurga", "Belagavi",
    "Kalaburagi", "Koppal", "Bagalkote", "Gadag", "Ballari", "Vijayanagara",
    "Davanagere", "Kolar", "Chikkaballapur", "Bidar", "Yadgir", "Ramanagara",
    "Chamarajanagar", "Mandya", "Mysuru", "Hassan", "Dharwad"
}

COASTAL_MALNAD_DISTRICTS = {
    "Dakshina Kannada", "Udupi", "Uttara Kannada", "Kodagu", "Chikkamagaluru", "Shivamogga"
}

HORTICULTURE_CROPS = {
    "Tomato", "Onion", "Chilli", "Turmeric", "Banana", "Mango", "Arecanut",
    "Coconut", "Papaya", "Pomegranate", "Grapes", "Capsicum", "Cucumber",
    "Flowers", "Vegetables", "Spices"
}

NOTIFIED_PMFBY_CROPS = {
    "Paddy", "Maize", "Ragi", "Jowar", "Groundnut", "Redgram", "Cotton",
    "Sugarcane", "Arecanut", "Chilli", "Turmeric", "Sunflower", "Soybean",
    "Bengalgram", "Onion", "Tomato"
}


class EligibilityEngine:
    """Evaluates farmer scenarios against the verified 16-scheme database."""

    def __init__(self, scheme_master_path: Optional[str] = None):
        if scheme_master_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            scheme_master_path = os.path.join(base_dir, "scheme_database", "processed", "scheme_master.json")
        
        self.scheme_master_path = scheme_master_path
        self.schemes: List[Dict[str, Any]] = []
        self.schemes_by_id: Dict[str, Dict[str, Any]] = {}
        self._load_scheme_master()

    def _load_scheme_master(self):
        if os.path.exists(self.scheme_master_path):
            with open(self.scheme_master_path, "r", encoding="utf-8") as f:
                self.schemes = json.load(f)
            self.schemes_by_id = {s["scheme_id"]: s for s in self.schemes}
        else:
            raise FileNotFoundError(f"Scheme master not found at {self.scheme_master_path}")

    def evaluate_scenario(
        self,
        scenario: FarmerScenario,
        include_children: bool = True
    ) -> List[SchemeDetermination]:
        """
        Evaluate a farmer scenario across all schemes in the database.
        Returns a list of SchemeDetermination objects with status and reasons.
        """
        determinations: List[SchemeDetermination] = []

        for scheme in self.schemes:
            record_type = scheme.get("record_type", "STANDALONE")
            if not include_children and record_type == "CHILD":
                continue

            det = self.evaluate_scheme(scenario, scheme["scheme_id"])
            determinations.append(det)

        return determinations

    def evaluate_scheme(
        self,
        scenario: FarmerScenario,
        scheme_id: str
    ) -> SchemeDetermination:
        """Evaluate a farmer scenario against a single scheme record."""
        scheme = self.schemes_by_id.get(scheme_id)
        if not scheme:
            raise ValueError(f"Scheme ID {scheme_id} not recognized in master database.")

        evaluator_method = getattr(self, f"_eval_{scheme_id.lower()}", None)
        if evaluator_method is None:
            if scheme.get("parent_scheme_id") == "SCH010":
                status, reason, disq, missing, rules = self._eval_ganga_kalyana_child(scenario, scheme)
            elif scheme.get("parent_scheme_id") == "SCH008":
                status, reason, disq, missing, rules = self._eval_credit_child(scenario, scheme)
            else:
                status = EligibilityStatus.REQUIRES_VERIFICATION
                reason = "No explicit rule evaluator implemented for this scheme."
                disq, missing, rules = [], ["Implementation verification"], ["RULE_NOT_IMPLEMENTED"]
        else:
            status, reason, disq, missing, rules = evaluator_method(scenario, scheme)

        return SchemeDetermination(
            scheme_id=scheme["scheme_id"],
            scheme_name=scheme["scheme_name"],
            record_type=scheme.get("record_type", "STANDALONE"),
            parent_scheme_id=scheme.get("parent_scheme_id"),
            status=status,
            reason=reason,
            disqualifying_factors=disq,
            missing_verifications=missing,
            rule_keys_fired=rules,
            upfront_benefit_support=scheme.get("upfront_benefit_support"),
            contingent_benefit_clause=scheme.get("contingent_benefit_clause"),
            claim_disclaimer=scheme.get("claim_disclaimer"),
            audit_status=scheme.get("audit_status")
        )

    def resolve_actionable_determinations(
        self,
        determinations: List[SchemeDetermination]
    ) -> List[SchemeDetermination]:
        """
        Deduplicates parent records from actionable recommendation output.
        Automated check: Ensures abstract parent records (such as SCH010 or SCH008)
        do NOT appear alongside their selected child as duplicate actionable recommendations.
        """
        # Find which parent IDs have eligible or requires_verification children
        child_parents_with_actionable_children = set()
        for d in determinations:
            if d.record_type == "CHILD" and d.status in [EligibilityStatus.ELIGIBLE, EligibilityStatus.REQUIRES_VERIFICATION]:
                if d.parent_scheme_id:
                    child_parents_with_actionable_children.add(d.parent_scheme_id)

        actionable = []
        for d in determinations:
            # If this determination is an abstract PARENT, and one of its CHILD records is actionable,
            # suppress the abstract parent to prevent duplicate recommendation cards.
            if d.record_type == "PARENT" and d.scheme_id in child_parents_with_actionable_children:
                continue
            actionable.append(d)

        return actionable

    # =========================================================================
    # SCH001: PM-KISAN
    # =========================================================================
    def _eval_sch001(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        disq = []
        missing = []
        rules = []

        # 1. Cultivable landholding required
        if s.land_size_acres <= 0:
            disq.append("Farmer must hold cultivable agricultural land (land_size_acres > 0).")
            rules.append("PMKISAN_LAND_SIZE_LEQ_ZERO")
        else:
            rules.append("PMKISAN_LAND_SIZE_POSITIVE")

        # 2. Pure tenant exclusion
        if s.is_pure_tenant_without_land_title:
            disq.append("Pure tenant farmers / sharecroppers without recorded land title are statutorily ineligible.")
            rules.append("PMKISAN_PURE_TENANT_EXCLUSION")

        # 3. Cut-off date check (01.02.2019)
        if s.land_ownership_cutoff_pre_feb_2019 is None:
            missing.append("Verification of land ownership title record date (must be on or before 01.02.2019 or inherited).")
            rules.append("PMKISAN_CUTOFF_DATE_UNKNOWN")
        elif s.land_ownership_cutoff_pre_feb_2019 is False:
            disq.append("Land ownership acquired after 01.02.2019 without succession/inheritance is ineligible.")
            rules.append("PMKISAN_CUTOFF_DATE_POST_FEB_2019")
        else:
            rules.append("PMKISAN_CUTOFF_DATE_VERIFIED")

        # 4. Paid Income Tax in last assessment year (explicit flag)
        if s.paid_income_tax_last_assessment_year is None:
            missing.append("Verification of income tax assessment status for farmer family members.")
            rules.append("PMKISAN_INCOME_TAX_UNKNOWN")
        elif s.paid_income_tax_last_assessment_year is True:
            disq.append("Member of the scheme-defined farmer family paid income tax in the last assessment year.")
            rules.append("PMKISAN_PAID_INCOME_TAX_EXCLUSION")
        else:
            rules.append("PMKISAN_NO_INCOME_TAX_PAID")

        # 5. Public service & constitutional posts exclusions (with MTS exemption)
        if s.govt_employee_category == GovtEmployeeCategory.UNKNOWN:
            missing.append("Verification of government employment post category for family members.")
            rules.append("PMKISAN_GOVT_EMPLOYEE_UNKNOWN")
        elif s.govt_employee_category == GovtEmployeeCategory.CONSTITUTIONAL_POST:
            disq.append("Family member holds or held a constitutional post.")
            rules.append("PMKISAN_CONSTITUTIONAL_POST_EXCLUSION")
        elif s.govt_employee_category == GovtEmployeeCategory.ELECTED_REPRESENTATIVE:
            disq.append("Family member is a former/present Minister, MP, MLA, MLC, Mayor, or ZP Chairperson.")
            rules.append("PMKISAN_ELECTED_REPRESENTATIVE_EXCLUSION")
        elif s.govt_employee_category == GovtEmployeeCategory.OFFICER_REGULAR:
            disq.append("Family member is a serving/retired officer or regular employee of Central/State Govt/PSE/Local body.")
            rules.append("PMKISAN_REGULAR_OFFICER_EXCLUSION")
        elif s.govt_employee_category == GovtEmployeeCategory.MTS_CLASS_IV_GROUP_D:
            rules.append("PMKISAN_MTS_EXEMPTION_APPLIED")

        # 6. Superannuated pensioner (>= Rs. 10,000 monthly, unless MTS exempt)
        if s.superannuated_pensioner_monthly_amount is None:
            missing.append("Verification of monthly pension amount for family members.")
            rules.append("PMKISAN_PENSION_UNKNOWN")
        elif s.superannuated_pensioner_monthly_amount >= 10000:
            if s.pensioner_is_mts_exempt:
                rules.append("PMKISAN_MTS_PENSION_EXEMPTION_APPLIED")
            else:
                disq.append(f"Family member receives monthly pension of Rs. {s.superannuated_pensioner_monthly_amount:,.0f} (>= Rs. 10,000 threshold).")
                rules.append("PMKISAN_PENSION_OVER_10K_EXCLUSION")
        else:
            rules.append("PMKISAN_PENSION_UNDER_10K_OR_NONE")

        # 7. Registered practicing professionals
        if s.registered_professional and s.registered_professional not in {"NONE", "None"}:
            if s.registered_professional == "UNKNOWN":
                missing.append("Verification of professional council registration status.")
                rules.append("PMKISAN_PROFESSIONAL_UNKNOWN")
            else:
                disq.append(f"Family member is a practicing registered professional ({s.registered_professional}).")
                rules.append("PMKISAN_PROFESSIONAL_EXCLUSION")
        else:
            rules.append("PMKISAN_NO_PROFESSIONAL_EXCLUSION")

        if disq:
            return EligibilityStatus.INELIGIBLE, f"Disqualified under PM-KISAN exclusion criteria: {'; '.join(disq)}", disq, missing, rules
        if missing:
            return EligibilityStatus.REQUIRES_VERIFICATION, f"Requires verification of statutory documents: {'; '.join(missing)}", disq, missing, rules

        return EligibilityStatus.ELIGIBLE, "Qualifies for PM-KISAN: Landholding family registered in land records with no disqualifying exclusions.", [], [], rules

    # =========================================================================
    # SCH002: PMFBY
    # =========================================================================
    def _eval_sch002(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        disq = []
        missing = []
        rules = []

        if s.land_size_acres <= 0:
            disq.append("Must have insurable cultivable cropped land area.")
            rules.append("PMFBY_NO_CROPPED_LAND")

        if s.crop_primary not in NOTIFIED_PMFBY_CROPS:
            disq.append(f"Primary crop '{s.crop_primary}' is not among notified food, oilseed, or commercial crops in Karnataka insurance units.")
            rules.append("PMFBY_NON_NOTIFIED_CROP")
        else:
            rules.append("PMFBY_NOTIFIED_CROP_VERIFIED")

        if disq:
            return EligibilityStatus.INELIGIBLE, f"Ineligible for PMFBY: {'; '.join(disq)}", disq, missing, rules

        return EligibilityStatus.ELIGIBLE, f"Qualifies for PMFBY crop insurance for {s.crop_primary}. Premium subsidized by Center & State; claim indemnity contingent upon surveyed loss.", [], [], rules

    # =========================================================================
    # SCH003: PMKSY-PDMC
    # =========================================================================
    def _eval_sch003(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        disq = []
        missing = []
        rules = []

        if s.land_size_acres < 0.5:
            disq.append(f"Landholding ({s.land_size_acres} ac) is below minimum threshold of 0.2 hectares (~0.5 acres).")
            rules.append("PMKSY_LAND_BELOW_0_2_HA")
        elif s.land_size_acres > 12.35:
            disq.append(f"Landholding ({s.land_size_acres} ac) exceeds maximum subsidized limit of 5.0 hectares (~12.35 acres).")
            rules.append("PMKSY_LAND_ABOVE_5_HA")
        else:
            rules.append("PMKSY_LAND_RANGE_VALID")

        has_water_source = any(a in s.existing_assets for a in ["Borewell (Non-energized)", "Borewell (Grid-connected)", "Open Well", "Diesel Pump Set", "Electric Pump Set", "Solar Pump"]) or "Irrigated" in s.land_type
        if not has_water_source:
            disq.append("Must possess an assured operational water source with pump machinery.")
            rules.append("PMKSY_NO_WATER_SOURCE")
        else:
            rules.append("PMKSY_WATER_SOURCE_VERIFIED")

        if s.prior_micro_irrigation_subsidy_years_ago is not None:
            if s.prior_micro_irrigation_subsidy_years_ago < 7.0:
                disq.append(f"Land parcel availed micro-irrigation subsidy {s.prior_micro_irrigation_subsidy_years_ago} years ago (7-year lock-in period applies).")
                rules.append("PMKSY_SEVEN_YEAR_LOCKIN_BREACHED")
            else:
                rules.append("PMKSY_LOCKIN_EXPIRED")
        else:
            rules.append("PMKSY_NO_PRIOR_SUBSIDY")

        if disq:
            return EligibilityStatus.INELIGIBLE, f"Ineligible for PMKSY-PDMC: {'; '.join(disq)}", disq, missing, rules

        return EligibilityStatus.ELIGIBLE, "Qualifies for PMKSY Micro-Irrigation capital subsidy (Drip/Sprinkler). Assured water source verified.", [], [], rules

    # =========================================================================
    # SCH004: SMAM
    # =========================================================================
    def _eval_sch004(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        disq = []
        missing = []
        rules = []

        if s.land_size_acres <= 0:
            disq.append("Must possess verified agricultural landholding in Karnataka.")
            rules.append("SMAM_NO_LAND")

        if s.prior_machinery_subsidy_years_ago is not None:
            if s.prior_machinery_subsidy_years_ago < 5.0:
                disq.append(f"Applicant availed machinery subsidy {s.prior_machinery_subsidy_years_ago} years ago (5-year lock-in applies).")
                rules.append("SMAM_FIVE_YEAR_LOCKIN_BREACHED")
            else:
                rules.append("SMAM_LOCKIN_EXPIRED")
        else:
            rules.append("SMAM_NO_PRIOR_SUBSIDY")

        if disq:
            return EligibilityStatus.INELIGIBLE, f"Ineligible for SMAM: {'; '.join(disq)}", disq, missing, rules

        return EligibilityStatus.ELIGIBLE, "Qualifies for SMAM farm machinery procurement subsidy. (Tractor RC required for tractor-drawn implements).", [], [], rules

    # =========================================================================
    # SCH005: Krishi Bhagya
    # =========================================================================
    def _eval_sch005(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        disq = []
        missing = []
        rules = []

        if s.land_type != "Dryland (Rainfed)":
            disq.append(f"Krishi Bhagya is strictly restricted to dryland rainfed holdings (current land_type: {s.land_type}).")
            rules.append("KRISHI_BHAGYA_NOT_DRYLAND")
        else:
            rules.append("KRISHI_BHAGYA_DRYLAND_VERIFIED")

        if s.district not in RAINFED_DRYLAND_DISTRICTS:
            disq.append(f"District '{s.district}' is outside the notified rainfed / Bayaluseeme taluks for Krishi Bhagya.")
            rules.append("KRISHI_BHAGYA_DISTRICT_NOT_RAINFED")
        else:
            rules.append("KRISHI_BHAGYA_DISTRICT_NOTIFIED")

        if s.land_size_acres < 1.0:
            disq.append(f"Landholding ({s.land_size_acres} ac) is below minimum catchment area requirement of 1.0 acre.")
            rules.append("KRISHI_BHAGYA_BELOW_1_ACRE")
        elif s.land_size_acres > 12.35:
            disq.append(f"Landholding ({s.land_size_acres} ac) exceeds maximum ceiling of 5.0 hectares (~12.35 acres).")
            rules.append("KRISHI_BHAGYA_EXCEEDS_5_HA")
        else:
            rules.append("KRISHI_BHAGYA_ACREAGE_VALID")

        if "Farm Pond (Existing/Funded)" in s.existing_assets:
            disq.append("Land parcel already has an existing funded farm pond on the same plot.")
            rules.append("KRISHI_BHAGYA_EXISTING_POND_EXCLUSION")

        if s.prior_farm_pond_subsidy_years_ago is not None and s.prior_farm_pond_subsidy_years_ago < 5.0:
            disq.append(f"Applicant availed farm pond subsidy {s.prior_farm_pond_subsidy_years_ago} years ago (5-year lock-in applies).")
            rules.append("KRISHI_BHAGYA_LOCKIN_BREACHED")

        if disq:
            return EligibilityStatus.INELIGIBLE, f"Ineligible for Krishi Bhagya: {'; '.join(disq)}", disq, missing, rules

        rate_text = "90% for SC/ST" if s.social_category in ["SC", "ST"] else "80% for General dryland"
        return EligibilityStatus.ELIGIBLE, f"Qualifies for Krishi Bhagya integrated package ({rate_text} subsidy for Krishi Honda, lining, pump).", [], [], rules

    # =========================================================================
    # SCH006: PM-KUSUM Component B
    # =========================================================================
    def _eval_sch006(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        disq = []
        missing = []
        rules = []

        if s.land_size_acres < 0.5:
            disq.append("Landholding must be at least 0.5 acres for cultivation and solar array placement.")
            rules.append("KUSUM_B_LAND_BELOW_0_5_AC")

        has_drilled_source = any(a in s.existing_assets for a in ["Borewell (Non-energized)", "Borewell (Grid-connected)", "Open Well"])
        if not has_drilled_source:
            disq.append("Must possess an existing drilled water source (borewell or open well). Scheme does not fund borewell drilling.")
            rules.append("KUSUM_B_NO_WATER_SOURCE")
        else:
            rules.append("KUSUM_B_WATER_SOURCE_PRESENT")

        if s.borewell_electric_status == BorewellElectricStatus.GRID_CONNECTED_IP_SET or "Borewell (Grid-connected)" in s.existing_assets:
            disq.append("Borewell already has an energized electric grid connection (DISCOM IP set). Component B strictly targets off-grid sources. (Related option to verify: PM-KUSUM Component C; not evaluated as an active benefit).")
            rules.append("KUSUM_B_GRID_CONNECTED_DISQUALIFIED")
        elif s.borewell_electric_status == BorewellElectricStatus.UNKNOWN:
            missing.append("Certificate from ESCOM confirming no grid electricity connection exists for this water source.")
            rules.append("KUSUM_B_GRID_STATUS_UNKNOWN")
        else:
            rules.append("KUSUM_B_OFF_GRID_VERIFIED")

        if disq:
            return EligibilityStatus.INELIGIBLE, f"Ineligible for PM-KUSUM Component B: {'; '.join(disq)}", disq, missing, rules
        if missing:
            return EligibilityStatus.REQUIRES_VERIFICATION, f"Requires verification: {'; '.join(missing)}", disq, missing, rules

        return EligibilityStatus.ELIGIBLE, "Qualifies for PM-KUSUM Component B standalone solar agriculture pump (60% subsidy up to 7.5 HP).", [], [], rules

    # =========================================================================
    # SCH007: MIDH
    # =========================================================================
    def _eval_sch007(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        disq = []
        missing = []
        rules = []

        if s.crop_primary not in HORTICULTURE_CROPS and (s.crop_secondary not in HORTICULTURE_CROPS if s.crop_secondary else True):
            disq.append(f"Primary crop '{s.crop_primary}' is not a recognized horticultural crop under MIDH.")
            rules.append("MIDH_NON_HORTICULTURE_CROP")
        else:
            rules.append("MIDH_HORTICULTURE_CROP_VERIFIED")

        if s.land_size_acres < 0.25:
            disq.append(f"Landholding ({s.land_size_acres} ac) is below minimum structure area of 1,000 sq. meters (~0.25 acres).")
            rules.append("MIDH_LAND_BELOW_0_25_AC")
        else:
            rules.append("MIDH_LAND_MIN_MET")

        has_micro_irrig = any(a in s.existing_assets for a in ["Drip Irrigation (Installed)", "Sprinkler (Installed)"])
        if not has_micro_irrig:
            disq.append("MIDH protected cultivation strictly mandates existing operational micro-irrigation facility on the plot.")
            rules.append("MIDH_NO_MICRO_IRRIGATION")
        else:
            rules.append("MIDH_MICRO_IRRIGATION_VERIFIED")

        if disq:
            return EligibilityStatus.INELIGIBLE, f"Ineligible for MIDH: {'; '.join(disq)}", disq, missing, rules

        return EligibilityStatus.ELIGIBLE, "Qualifies for MIDH Protected Cultivation subsidy (50% cost norm for Polyhouse / Shade Net up to 4,000 m²).", [], [], rules

    # =========================================================================
    # SCH008: Credit Category (PARENT)
    # =========================================================================
    def _eval_sch008(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        if s.land_size_acres <= 0:
            return EligibilityStatus.INELIGIBLE, "Ineligible: Must cultivate operational agricultural land.", ["No landholding"], [], ["CREDIT_NO_LAND"]
        return EligibilityStatus.ELIGIBLE, "Qualifies for Agricultural Production Credit umbrella. Evaluated via Central KCC-MISS (4%) and Karnataka Cooperative routes (0% provisional).", [], [], ["CREDIT_PARENT_ELIGIBLE"]

    def _eval_credit_child(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        if s.land_size_acres <= 0:
            return EligibilityStatus.INELIGIBLE, "Must have operational cultivable land.", ["No operational holding"], [], ["CREDIT_CHILD_NO_LAND"]

        if m["scheme_id"] == "SCH008_CENTRAL":
            return EligibilityStatus.ELIGIBLE, "Qualifies for Central KCC-MISS via Commercial Banks/RRBs (4.0% effective interest up to Rs. 3 Lakh upon prompt repayment).", [], [], ["KCC_CENTRAL_COMMERCIAL_ELIGIBLE"]
        elif m["scheme_id"] == "SCH008_KA_COOP":
            return EligibilityStatus.REQUIRES_VERIFICATION, "Qualifies in principle for Karnataka Zero-Interest Credit via PACS/DCCBs (0% up to Rs. 5 Lakh). Marked PROVISIONAL pending active financial year Government Order verification.", [], ["Annual Cooperative Department GO verification"], ["KCC_KA_COOP_PROVISIONAL_PENDING_GO"]

        return EligibilityStatus.ELIGIBLE, "Credit route eligible.", [], [], ["CREDIT_CHILD_ELIGIBLE"]

    # =========================================================================
    # SCH009: Soil Health Card
    # =========================================================================
    def _eval_sch009(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        if s.land_size_acres <= 0:
            return EligibilityStatus.INELIGIBLE, "Must possess accessible agricultural land for soil sampling.", ["Non-agricultural land"], [], ["SHC_NO_LAND"]
        return EligibilityStatus.ELIGIBLE, "Qualifies for 100% free Soil Health Card diagnostic service and crop nutrient recommendations.", [], [], ["SHC_UNIVERSAL_ACCESS_VERIFIED"]

    # =========================================================================
    # SCH010: Ganga Kalyana (PARENT)
    # =========================================================================
    def _eval_sch010(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        disq = []
        missing = []
        rules = []

        if s.social_category == "General (OC)":
            disq.append("Ineligible for all four Ganga Kalyana implementation records currently represented in the registry (SCH010_AMBEDKAR, SCH010_VALMIKI, SCH010_DEVARAJ_URS, SCH010_KMDC) because applicant (General Merit) does not meet covered corporation-category requirements. This result does not establish ineligibility for every Ganga Kalyana-related programme in Karnataka.")
            rules.append("GK_PARENT_REGISTRY_CORPORATION_MISMATCH")

        if s.land_type != "Dryland (Rainfed)":
            disq.append(f"Land must be exclusively dryland (kushki). Current land_type '{s.land_type}' is disqualified.")
            rules.append("GK_PARENT_NOT_DRYLAND")

        has_existing_borewell = any(a in s.existing_assets for a in ["Borewell (Non-energized)", "Borewell (Grid-connected)"])
        if has_existing_borewell:
            disq.append("Land parcel already possesses an existing borewell.")
            rules.append("GK_PARENT_EXISTING_BOREWELL_EXCLUSION")

        if s.prior_ganga_kalyana_in_family:
            disq.append("A family member in the household previously received Ganga Kalyana assistance.")
            rules.append("GK_PARENT_PRIOR_BENEFICIARY_EXCLUSION")

        # Range bounds for umbrella
        indiv_eligible = (1.0 <= s.land_size_acres <= 5.0)
        comm_eligible = (s.community_pool_acres is not None and 8.0 <= s.community_pool_acres <= 15.0)

        if not indiv_eligible and not comm_eligible:
            if s.land_size_acres > 5.0:
                disq.append(f"Landholding ({s.land_size_acres} ac) exceeds maximum ceiling of 5.0 acres for Individual Borewells.")
                rules.append("GK_PARENT_EXCEEDS_5_ACRES")
            else:
                disq.append(f"Landholding ({s.land_size_acres} ac) below minimum threshold, and community pool acres is not satisfied.")
                rules.append("GK_PARENT_BELOW_MIN_ACREAGE")

        if disq:
            return EligibilityStatus.INELIGIBLE, f"Ineligible for Ganga Kalyana: {'; '.join(disq)}", disq, missing, rules

        corp_child = self._map_social_category_to_gk_child(s.social_category)
        rules.append(f"GK_PARENT_ROUTES_TO_{corp_child}")
        return EligibilityStatus.ELIGIBLE, f"Qualifies for Ganga Kalyana parent umbrella. Routes to {corp_child} based on {s.social_category} social category.", [], [], rules

    # =========================================================================
    # Ganga Kalyana Corporation Children (Priority 1 Validations)
    # =========================================================================
    def _eval_ganga_kalyana_child(self, s: FarmerScenario, m: Dict[str, Any]) -> Tuple[EligibilityStatus, str, List[str], List[str], List[str]]:
        disq = []
        missing = []
        rules = []
        cid = m["scheme_id"]

        # 1. Social category match
        target_child = self._map_social_category_to_gk_child(s.social_category)
        if cid != target_child:
            disq.append(f"Applicant social category '{s.social_category}' does not fall under {m['department']}. (Routes to {target_child} instead).")
            rules.append(f"GK_{cid}_SOCIAL_CATEGORY_MISMATCH")

        # 2. Dryland requirement
        if s.land_type != "Dryland (Rainfed)":
            disq.append(f"Must be exclusively dryland (kushki). Land type '{s.land_type}' is disqualified.")
            rules.append(f"GK_{cid}_NOT_DRYLAND")

        # 3. No existing borewell
        if any(a in s.existing_assets for a in ["Borewell (Non-energized)", "Borewell (Grid-connected)"]):
            disq.append("Land parcel already possesses an existing borewell.")
            rules.append(f"GK_{cid}_EXISTING_BOREWELL")

        # 4. Family prior beneficiary check
        if s.prior_ganga_kalyana_in_family:
            disq.append("Family member previously received Ganga Kalyana assistance.")
            rules.append(f"GK_{cid}_PRIOR_BENEFICIARY")

        # 5. Corporation-Specific Landholding & Route Rules
        if cid == "SCH010_AMBEDKAR":
            # Priority 1: Official Ambedkar Corp rules require 1.5-5.0 acres individual;
            # Community/Lift route requires 8-15 pooled acres with THREE (3) or more beneficiaries.
            min_indiv = 1.5
            indiv_eligible = (min_indiv <= s.land_size_acres <= 5.0)
            
            comm_eligible = False
            if s.community_pool_acres is not None and 8.0 <= s.community_pool_acres <= 15.0:
                if s.community_pool_beneficiaries_count >= 3:
                    comm_eligible = True
                    rules.append("GK_AMBEDKAR_COMMUNITY_ROUTE_VALID")
                else:
                    disq.append(f"Community lift/borewell route under Ambedkar Corporation requires at least 3 pooled SC beneficiaries (provided: {s.community_pool_beneficiaries_count}).")
                    rules.append("GK_AMBEDKAR_COMMUNITY_MIN_BENEFICIARIES_FAILED")

            if indiv_eligible:
                rules.append("GK_AMBEDKAR_INDIVIDUAL_ROUTE_VALID")

            if not indiv_eligible and not comm_eligible and not ("GK_AMBEDKAR_COMMUNITY_MIN_BENEFICIARIES_FAILED" in rules):
                if s.land_size_acres > 5.0:
                    disq.append(f"Individual landholding ({s.land_size_acres} ac) exceeds Ambedkar Corporation individual ceiling of 5.0 acres.")
                    rules.append("GK_AMBEDKAR_INDIVIDUAL_OVER_5_AC")
                else:
                    disq.append(f"Individual landholding ({s.land_size_acres} ac) is below Ambedkar Corporation minimum threshold of 1.5 acres (1 acre 20 guntas), and community pooled route was not satisfied.")
                    rules.append("GK_AMBEDKAR_INDIVIDUAL_UNDER_1_5_AC")

        else:
            # Other corporations (Valmiki, Devaraj Urs, KMDC):
            # Check individual thresholds (Malnad/coastal 1.0 ac vs plains 1.2 ac)
            is_coastal_malnad = s.district in COASTAL_MALNAD_DISTRICTS
            min_indiv = 1.0 if is_coastal_malnad else 1.2
            indiv_eligible = (min_indiv <= s.land_size_acres <= 5.0)
            comm_eligible = (s.community_pool_acres is not None and 8.0 <= s.community_pool_acres <= 15.0 and s.community_pool_beneficiaries_count >= 2)

            if indiv_eligible:
                rules.append(f"GK_{cid}_INDIVIDUAL_ROUTE_VALID")
            elif comm_eligible:
                rules.append(f"GK_{cid}_COMMUNITY_ROUTE_VALID")
            else:
                if s.land_size_acres > 5.0:
                    disq.append(f"Individual landholding ({s.land_size_acres} ac) exceeds maximum 5.0 acres ceiling.")
                    rules.append(f"GK_{cid}_EXCEEDS_5_AC")
                else:
                    disq.append(f"Landholding ({s.land_size_acres} ac) is below minimum {min_indiv} acres for Individual Route, and community pool requirement (8-15 ac) is not met.")
                    rules.append(f"GK_{cid}_UNDER_MIN_ACREAGE")

        if disq:
            return EligibilityStatus.INELIGIBLE, f"Ineligible for {m['scheme_name']}: {'; '.join(disq)}", disq, missing, rules

        route_desc = "Community Pooled Route (Samooha Kola Bavi)" if comm_eligible else "Individual Borewell Route"
        return EligibilityStatus.ELIGIBLE, f"Qualifies for {m['scheme_name']} under {route_desc}. 100% subsidized borewell, pump, and electrification package.", [], [], rules

    def _map_social_category_to_gk_child(self, social_category: str) -> str:
        if social_category == "SC":
            return "SCH010_AMBEDKAR"
        elif social_category == "ST":
            return "SCH010_VALMIKI"
        elif social_category in ["OBC (2A)", "OBC (2B)", "OBC (3A)", "OBC (3B)"]:
            return "SCH010_DEVARAJ_URS"
        elif social_category in ["Minority (Muslim)", "Minority (Christian)"]:
            return "SCH010_KMDC"
        return "NONE"
