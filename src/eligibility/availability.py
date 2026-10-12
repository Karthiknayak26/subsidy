"""
Availability Filtering and Implementation Gate.

Decouples statutory eligibility from dynamic administrative availability.
Classifies recommendations into exactly four discrete availability states:
1. Verified available now (Only state allowed under user-facing Available Now)
2. Eligible, but currently closed
3. Upcoming, with an officially confirmed date
4. Availability unknown — confirmation required
"""

import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

from .models import SchemeDetermination, AvailabilityState


class AvailabilityFilter:
    """Manages dynamic operational availability status without contaminating statutory logic."""

    def __init__(self, availability_csv_path: Optional[str] = None):
        if availability_csv_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            availability_csv_path = os.path.join(base_dir, "scheme_database", "processed", "scheme_availability_template.csv")
        
        self.availability_csv_path = availability_csv_path
        self.records: Dict[str, Dict[str, Any]] = {}
        self._load_records()

    def _load_records(self):
        if os.path.exists(self.availability_csv_path):
            try:
                df = pd.read_csv(self.availability_csv_path)
                if not df.empty and "scheme_id" in df.columns:
                    for _, row in df.iterrows():
                        self.records[str(row["scheme_id"])] = row.to_dict()
            except Exception:
                self.records = {}

    def apply_availability(
        self,
        determinations: List[SchemeDetermination],
        as_of_date: Optional[str] = None
    ) -> List[SchemeDetermination]:
        """
        Enriches eligibility determinations with operational availability states.
        Enforces guardrail: only official dated notices can activate 'Verified available now'.
        """
        if as_of_date is None:
            as_of_date = datetime.now().strftime("%Y-%m-%d")

        for det in determinations:
            rec = self.records.get(det.scheme_id)

            if not rec:
                # Default safe state when no active circular is attached
                det.availability_state = AvailabilityState.AVAILABILITY_UNKNOWN
                det.availability_evidence = {
                    "status_note": "No active seasonal notification currently indexed. Verification with RSK / Department required.",
                    "checked_at": as_of_date
                }
                continue

            app_status = str(rec.get("application_status", "")).strip().upper()
            notice_url = rec.get("official_notice_url")
            pub_date = rec.get("source_published_date")

            if app_status == "OPEN" and notice_url and pub_date:
                det.availability_state = AvailabilityState.VERIFIED_AVAILABLE_NOW
            elif app_status == "CLOSED":
                det.availability_state = AvailabilityState.ELIGIBLE_BUT_CLOSED
            elif app_status == "UPCOMING" and rec.get("application_open_date"):
                det.availability_state = AvailabilityState.UPCOMING_CONFIRMED
            else:
                det.availability_state = AvailabilityState.AVAILABILITY_UNKNOWN

            det.availability_evidence = {
                "application_status": app_status,
                "official_notice_url": notice_url,
                "source_published_date": pub_date,
                "checked_at": as_of_date
            }

        return determinations

    @staticmethod
    def partition_by_presentation(
        determinations: List[SchemeDetermination]
    ) -> Dict[str, List[SchemeDetermination]]:
        """Partitions determinations into User-Facing Presentation sections."""
        available_now = []
        timing_or_verification_required = []
        ineligible = []

        for d in determinations:
            if not d.is_eligible:
                ineligible.append(d)
            elif d.availability_state == AvailabilityState.VERIFIED_AVAILABLE_NOW:
                available_now.append(d)
            else:
                timing_or_verification_required.append(d)

        return {
            "available_now": available_now,
            "timing_or_verification_required": timing_or_verification_required,
            "ineligible": ineligible
        }
