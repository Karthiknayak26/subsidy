# Data Dictionary & Schema Specification (Working Draft)

## 1. Farmer Profile Schema (Candidate Features)

| Feature Name | Data Type | Description | Allowed / Expected Values |
|--------------|-----------|-------------|---------------------------|
| `district` | Categorical | District of cultivation | Valid state districts (e.g., Tumkur, Raichur) |
| `taluk_block` | Categorical | Sub-district / Taluk / Block | Official administrative blocks |
| `land_size_acres` | Float | Operational agricultural land holding | Numeric >= 0.0 |
| `farmer_category` | Categorical | Land-holding classification | Marginal (<2.5 acres), Small (2.5-5 acres), Medium/Large (>5 acres) |
| `social_category` | Categorical | Social group classification (scheme-specific quotas) | General, OBC, SC, ST, Minorities |
| `primary_crop` | Categorical | Main cultivated crop for the season | Paddy, Maize, Banana, Tomato, Cotton, Ragi, etc. |
| `crop_category` | Categorical | Broad horticultural/agricultural category | Cereals, Pulses, Fruits, Vegetables, Oilseeds, Commercial |
| `season` | Categorical | Agricultural season | Kharif, Rabi, Summer, Perennial |
| `irrigation_type` | Categorical | Available irrigation infrastructure | Rainfed, Borewell, Canal, Drip/Sprinkler, Open Well |
| `current_need` | Categorical / Text | Primary immediate requirement or interest | Irrigation Equipment, Seed Subsidy, Machinery, Credit/Loan, Post-Harvest |

## 2. Scheme Master Schema (`scheme_master.xlsx`)

| Column | Description |
|---|---|
| `scheme_id` | Unique identifier (e.g., `SCH-KA-AGRI-001`) |
| `scheme_name` | Official scheme name |
| `government_level` | Central / State |
| `state` | State name (or "All India" for Central) |
| `nodal_department` | Ministry / Department managing the scheme |
| `objective_summary` | Official purpose and scope |
| `eligible_crops` | Crop restrictions (or "All") |
| `farmer_categories` | Eligible farmer classes (Small, Marginal, SC/ST, Women, All) |
| `land_criteria_acres` | Land size thresholds (min/max) |
| `irrigation_criteria` | Irrigation prerequisite (e.g., Borewell required, Rainfed only) |
| `benefit_type_and_subsidy_amount` | Benefit formula (e.g., 50% subsidy up to Rs. 25,000) |
| `eligibility_rules_summary` | Full human-readable verified criteria |
| `required_documents` | Required proof (Pahani/RTC, Aadhaar, Caste Cert, Bank Passbook) |
| `application_mode` | Online portal (K-Kisan, Seva Sindhu, DBT) / Offline office |
| `official_source_url` | Primary government URL verifying information |
| `verification_date` | Date verified against official portal |
| `verified_by` | Researcher/student responsible for verification |
| `remarks` | Special conditions, deadlines, or budgetary quotas |
