"""
Data models and enumerations for the Deterministic Eligibility Engine.
Implements Three-Valued Logic (ELIGIBLE, INELIGIBLE, REQUIRES_VERIFICATION)
and statutory farmer/household attributes.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class EligibilityStatus(str, Enum):
    ELIGIBLE = "ELIGIBLE"
    INELIGIBLE = "INELIGIBLE"
    REQUIRES_VERIFICATION = "REQUIRES_VERIFICATION"


class AvailabilityState(str, Enum):
    VERIFIED_AVAILABLE_NOW = "Verified available now"
    ELIGIBLE_BUT_CLOSED = "Eligible, but currently closed"
    UPCOMING_CONFIRMED = "Upcoming, with an officially confirmed date"
    AVAILABILITY_UNKNOWN = "Availability unknown — confirmation required"


class GovtEmployeeCategory(str, Enum):
    NONE = "NONE"
    MTS_CLASS_IV_GROUP_D = "MTS_CLASS_IV_GROUP_D"  # Statutorily EXEMPT from exclusion
    OFFICER_REGULAR = "OFFICER_REGULAR"            # Excluded
    CONSTITUTIONAL_POST = "CONSTITUTIONAL_POST"    # Excluded
    ELECTED_REPRESENTATIVE = "ELECTED_REPRESENTATIVE"  # Excluded (Ministers, MPs, MLAs, Mayors, ZP Chairpersons)
    UNKNOWN = "UNKNOWN"


class BorewellElectricStatus(str, Enum):
    NONE = "NONE"
    UNENERGIZED_OFF_GRID = "UNENERGIZED_OFF_GRID"      # Eligible for PM-KUSUM B
    GRID_CONNECTED_IP_SET = "GRID_CONNECTED_IP_SET"    # Disqualified for PM-KUSUM B (Component C instead)
    UNKNOWN = "UNKNOWN"


@dataclass
class FarmerScenario:
    """Represents a structured farmer profile for eligibility evaluation."""
    scenario_id: str
    agro_climatic_zone: str
    district: str
    crop_primary: str
    land_size_acres: float
    land_type: str
    social_category: str
    farmer_category: str
    existing_assets: List[str]
    annual_family_income_lakh: float
    immediate_need: str

    # Statutory Exclusion & Operational Flags
    paid_income_tax_last_assessment_year: Optional[bool] = None  # None / UNKNOWN triggers REQUIRES_VERIFICATION
    govt_employee_category: GovtEmployeeCategory = GovtEmployeeCategory.NONE
    superannuated_pensioner_monthly_amount: Optional[float] = 0.0
    pensioner_is_mts_exempt: bool = False
    registered_professional: Optional[str] = "NONE"
    land_ownership_cutoff_pre_feb_2019: Optional[bool] = True
    is_pure_tenant_without_land_title: bool = False
    borewell_electric_status: BorewellElectricStatus = BorewellElectricStatus.NONE
    prior_micro_irrigation_subsidy_years_ago: Optional[float] = None
    prior_farm_pond_subsidy_years_ago: Optional[float] = None
    prior_machinery_subsidy_years_ago: Optional[float] = None
    prior_ganga_kalyana_in_family: Optional[bool] = False
    community_pool_acres: Optional[float] = 0.0
    community_pool_beneficiaries_count: int = 0  # Number of pooled beneficiaries (e.g. >= 3 for Ambedkar Corp)
    crop_secondary: Optional[str] = None
    farming_stage: Optional[str] = None
    season: Optional[str] = None
    kcc_query_text_example: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FarmerScenario":
        """Construct a FarmerScenario safely from a dictionary."""
        d = dict(data)
        if "govt_employee_category" in d and isinstance(d["govt_employee_category"], str):
            try:
                d["govt_employee_category"] = GovtEmployeeCategory(d["govt_employee_category"])
            except ValueError:
                d["govt_employee_category"] = GovtEmployeeCategory.UNKNOWN

        if "borewell_electric_status" in d and isinstance(d["borewell_electric_status"], str):
            try:
                d["borewell_electric_status"] = BorewellElectricStatus(d["borewell_electric_status"])
            except ValueError:
                d["borewell_electric_status"] = BorewellElectricStatus.UNKNOWN

        # Handle string "UNKNOWN" or None for boolean and optional fields
        if d.get("paid_income_tax_last_assessment_year") == "UNKNOWN":
            d["paid_income_tax_last_assessment_year"] = None
        if d.get("land_ownership_cutoff_pre_feb_2019") == "UNKNOWN":
            d["land_ownership_cutoff_pre_feb_2019"] = None
        if d.get("prior_ganga_kalyana_in_family") == "UNKNOWN":
            d["prior_ganga_kalyana_in_family"] = None
        if d.get("superannuated_pensioner_monthly_amount") == "UNKNOWN":
            d["superannuated_pensioner_monthly_amount"] = None

        return cls(**d)


@dataclass
class SchemeDetermination:
    """The result of evaluating a farmer against a specific scheme record."""
    scheme_id: str
    scheme_name: str
    record_type: str
    parent_scheme_id: Optional[str]
    status: EligibilityStatus
    reason: str
    disqualifying_factors: List[str] = field(default_factory=list)
    missing_verifications: List[str] = field(default_factory=list)
    rule_keys_fired: List[str] = field(default_factory=list)
    upfront_benefit_support: Optional[str] = None
    contingent_benefit_clause: Optional[str] = None
    claim_disclaimer: Optional[str] = None
    audit_status: Optional[str] = None
    availability_state: AvailabilityState = AvailabilityState.AVAILABILITY_UNKNOWN
    availability_evidence: Optional[Dict[str, Any]] = None

    @property
    def is_eligible(self) -> bool:
        return self.status == EligibilityStatus.ELIGIBLE
