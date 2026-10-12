# Scheme Availability Data Layer

## Purpose

This is a time-sensitive status layer separate from `scheme_master.xlsx` / `scheme_master.json`. It records whether a scheme is currently actionable for a specified geography, crop/activity, and application period. It is intentionally blank until status can be verified against current official government evidence.

## File

- `scheme_availability_template.csv`: header-only template. No scheme status has been filled or assumed.
- Target repository location: `scheme_database/processed/scheme_availability.csv`

## Allowed values

- `program_status`: `ACTIVE`, `PAUSED`, `DISCONTINUED`, `UNKNOWN`
- `application_status`: `OPEN`, `UPCOMING`, `CLOSED`, `YEAR_ROUND`, `NOT_APPLICABLE`, `UNKNOWN`
- `funding_status`: `AVAILABLE_CONFIRMED`, `EXHAUSTED_CONFIRMED`, `NOT_PUBLISHED`, `NOT_APPLICABLE`, `UNKNOWN`
- `availability_disposition` (derived by code): `AVAILABLE_NOW`, `UPCOMING`, `CLOSED`, `PAUSED_OR_DISCONTINUED`, `FUNDING_EXHAUSTED`, `UNVERIFIED`

## Required operational rules

1. Each record must link to a scheme in the verified scheme master.
2. Record the exact geography/crop/activity/period to which the official notice applies. Use multiple rows when scope or status differs.
3. `official_status_source_url`, `checked_at`, and a concise `evidence_note` are required before a record can be considered verified.
4. Dates or funding availability must not be inferred from old announcements or third-party summaries.
5. `ACTIVE` does not mean applications are open. `OPEN` does not prove funds remain. Keep program, application-window and funding status separate.
6. Do not show a scheme under “Available now” unless current official evidence supports the relevant application status and geographic/eligibility scope. When limited funds/targets are relevant, do not claim funds are confirmed available unless official evidence supports that status.
7. `UNKNOWN`, missing, stale or conflicting status means `UNVERIFIED`; do not show it as confirmed available.
8. A scheme that is closed or unverified is not assigned relevance score 0. It is excluded before the relevance annotation/ranking stage.
9. Preserve prior snapshots or versioned files used in benchmark runs so that evaluation can be reproduced after status changes.
10. The prototype should check status on user request. Future proactive SMS/IVR notifications must be opt-in, triggered by a verified change, and deduplicated to avoid repeatedly messaging the same status.

## Suggested derived decision logic

A code-derived `AVAILABLE_NOW` should require official evidence that:

- program is `ACTIVE`;
- application status is `OPEN` or explicitly `YEAR_ROUND`;
- geographic and crop/activity scope match;
- the record is not stale and has not been superseded; and
- where limited allocation matters, no exhaustion notice applies and current funding is confirmed when the official source publishes that fact at the necessary level.

If funding status is `NOT_PUBLISHED`, do not claim “funds available”. At most, present a separately labeled status such as “application window reported open; funding availability not published” if that caveat is useful and verified. For this project’s strict “Available now” list, retain only records that satisfy the defined current-actionability rule.

## Important limitation

The template defines the schema, not the current status of any actual scheme. Populate it only after checking the responsible official department/portal or a current official notice. Negilu may help discover the scheme/source but is not the primary evidence for current availability.
