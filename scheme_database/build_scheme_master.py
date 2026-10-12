import os
import json
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

base_dir = r"c:\Users\User\Desktop\subsidy\farmer-benefit-ml\scheme_database"
raw_dir = os.path.join(base_dir, "raw")
proc_dir = os.path.join(base_dir, "processed")
os.makedirs(raw_dir, exist_ok=True)
os.makedirs(proc_dir, exist_ok=True)

schemes = [
    # =========================================================================
    # SCH001: PM-KISAN (STANDALONE)
    # =========================================================================
    {
        "scheme_id": "SCH001",
        "scheme_name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "record_type": "STANDALONE",
        "parent_scheme_id": None,
        "government_level": "Central",
        "department": "Department of Agriculture and Farmers Welfare (DA&FW), Ministry of Agriculture & Farmers Welfare",
        "benefit_type": "Direct Benefit Transfer (DBT) / Income Support",
        "target_crops": "All crops (Crop-agnostic)",
        "target_activities": "Crop cultivation, agricultural input procurement, domestic household support",
        "state": "All India (including Karnataka)",
        "district_scope": "All districts",
        "farmer_categories": "All cultivable landholding farmer families (Marginal, Small, Medium, Large landholders)",
        "min_land": "> 0 acres",
        "max_land": "No limit (Universal coverage for all cultivable landholding families)",
        "irrigation_requirements": "None (Rainfed or Irrigated)",
        "existing_asset_requirements": "None",
        "eligible_conditions": "Landholding farmer family having cultivable land registered in state land records (e.g., FRUITS/Bhoomi in Karnataka) with land ownership title recorded on or before February 1, 2019 (or transferred via succession/inheritance upon death of titleholder); active bank account seeded with Aadhaar and NPCI mapping; mandatory e-KYC completed. Pure tenant farmers, oral lessees, and landless agricultural laborers without recorded land titles are ineligible.",
        "excluded_conditions": "Institutional landholders; Farmer families where one or more members belong to statutory exclusion categories: (a) Former/present constitutional post holders; (b) Former/present Ministers, State Ministers, MPs, MLAs, MLCs, Mayors of Municipal Corporations, Chairpersons of Zilla Panchayats; (c) Serving or retired officers and employees of Central/State Govt Ministries/Offices/Departments, Central/State PSEs and Attached offices/Autonomous Institutions under Govt, and regular employees of Local Bodies — EXCLUDING Multi-Tasking Staff (MTS) / Class IV / Group D employees (who remain eligible); (d) Superannuated/retired pensioners whose monthly pension is Rs. 10,000 or more (EXCLUDING MTS/Class IV/Group D pensioners); (e) Persons who paid Income Tax in the last assessment year (statutory ITR filing, not inferred from gross agricultural income); (f) Registered professionals (Doctors, Engineers, Lawyers, Chartered Accountants, Architects) carrying out active practice.",
        "benefit_rate": "Rs. 6,000 per year per eligible farmer family",
        "maximum_benefit": "Rs. 6,000 per annum",
        "benefit_formula": "3 equal installments of Rs. 2,000 released every 4 months (April-July, August-November, December-March) directly via DBT PFMS",
        "upfront_benefit_support": "Direct cash grant of Rs. 6,000 per annum in 3 four-monthly DBT installments of Rs. 2,000 each.",
        "contingent_benefit_clause": "None (Non-contingent direct income support)",
        "claim_disclaimer": "None (Entitlement-based income support; contingent upon e-KYC and land ownership verification).",
        "application_period": "Open year-round (continuous enrollment)",
        "application_method": "Online self-registration via PM-KISAN Portal (pmkisan.gov.in) / mobile app, Common Service Centres (CSC), or State nodal entry via Karnataka FRUITS portal",
        "required_documents": "Aadhaar card, Land ownership record (RTC/Pahani/Khata recorded on/before 01.02.2019 or inheritance deed), Aadhaar-linked Bank Passbook/NPCI mandate, Mobile number",
        "official_source_url": "https://pmkisan.gov.in/",
        "official_document_url": "https://pmkisan.gov.in/Documents/Revised_Operational_Guidelines_of_PM_KISAN.pdf",
        "audit_status": "VERIFIED",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH002: PMFBY (STANDALONE)
    # =========================================================================
    {
        "scheme_id": "SCH002",
        "scheme_name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "record_type": "STANDALONE",
        "parent_scheme_id": None,
        "government_level": "Central-State Co-sponsored (50:50 premium subsidy)",
        "department": "Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Agriculture, Govt of Karnataka",
        "benefit_type": "Crop Insurance Premium Subsidy (Upfront) & Risk Indemnity (Contingent)",
        "target_crops": "Notified food crops (Cereals, Millets, Pulses), Oilseeds, and Annual Commercial / Horticultural crops (e.g., Paddy, Maize, Ragi, Groundnut, Cotton, Arecanut, Chilli, Turmeric)",
        "target_activities": "Comprehensive crop insurance against yield losses, prevented sowing, mid-season adversity, post-harvest localized losses, and widespread calamities",
        "state": "Karnataka",
        "district_scope": "Notified insurance units (Gram Panchayat / Hobli level) across all districts of Karnataka",
        "farmer_categories": "All categories (Loanee and Non-loanee farmers, sharecroppers, tenant farmers cultivating notified crops in notified areas; voluntary enrollment since Kharif 2020)",
        "min_land": "> 0 acres",
        "max_land": "Up to insurable cropped area on RTC / cultivation certificate",
        "irrigation_requirements": "None (Covers both Irrigated and Rainfed crops under separate sum insured and actuarial premium rate tables)",
        "existing_asset_requirements": "None",
        "eligible_conditions": "Must cultivate a notified crop in a notified insurance unit for the season (Kharif or Rabi); crop must be insured before seasonal cut-off date; FRUITS ID / land ownership (RTC) or registered tenancy / sowing certificate required.",
        "excluded_conditions": "Losses arising out of war and nuclear risks; malicious damage and preventable risks (poor farm management, theft); sowing after designated seasonal cut-off date; non-notified crops or non-notified insurance units.",
        "benefit_rate": "Farmer premium statutorily capped at: 2.0% of Sum Insured for Kharif food and oilseed crops; 1.5% of Sum Insured for Rabi food and oilseed crops; 5.0% of Sum Insured for Annual commercial/horticultural crops. Balance actuarial premium subsidized 50:50 by Central and State Governments.",
        "maximum_benefit": "Maximum risk coverage equals 100% of Sum Insured per hectare (as determined by District Level Technical Committee based on cost of cultivation)",
        "benefit_formula": "Upfront Premium Subsidy = (Actuarial_Premium_Rate - Farmer_Capped_Rate) * Sum_Insured. Contingent Claim Indemnity = Max(0, (Threshold_Yield - Actual_Yield) / Threshold_Yield) * Sum_Insured.",
        "upfront_benefit_support": "Government Premium Support = (Actuarial_Premium_Rate - Farmer_Capped_Rate) * Sum_Insured. Actuarial rate is determined dynamically per tender notice for the specific crop, district, and season.",
        "contingent_benefit_clause": "Contingent Shortfall Indemnity Claim = Max(0, (Threshold_Yield - Actual_Yield) / Threshold_Yield) * Sum_Insured (Area approach via CCEs). Localized calamities and prevented sowing assessed per surveyed loss percentage.",
        "claim_disclaimer": "CLAIM INDEMNITY IS NEVER GUARANTEED. Claim payouts are strictly contingent upon surveyed natural crop loss, localized calamities, prevented sowing, or harvest yield shortfalls exceeding the threshold in notified insurance units. Under normal yields, no claim payout is made.",
        "application_period": "Seasonal cut-off dates (Kharif cut-off typically July 31; Rabi cut-off November 30 / December 31 depending on notified crop)",
        "application_method": "Karnataka Samrakshane Portal (samrakshane.karnataka.gov.in), PMFBY National Portal (pmfby.gov.in), Commercial Banks / RRBs / PACS, or CSCs",
        "required_documents": "Aadhaar card, RTC / Pahani (Land records) or Tenancy agreement, Sowing certificate / Self-declaration of crop sown, Bank passbook, FRUITS ID",
        "official_source_url": "https://pmfby.gov.in/",
        "official_document_url": "https://pmfby.gov.in/pdf/Revised_Operational_Guidelines.pdf",
        "audit_status": "VERIFIED",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH003: PMKSY-PDMC (STANDALONE)
    # =========================================================================
    {
        "scheme_id": "SCH003",
        "scheme_name": "Pradhan Mantri Krishi Sinchayee Yojana - Per Drop More Crop (PMKSY-PDMC)",
        "record_type": "STANDALONE",
        "parent_scheme_id": None,
        "government_level": "Central-State Co-sponsored (60:40 Centre:State + Karnataka State Top-up)",
        "department": "Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW / Department of Horticulture & Agriculture, Govt of Karnataka",
        "benefit_type": "Capital Subsidy on Micro-Irrigation Equipment",
        "target_crops": "Horticulture crops, Sugarcane, Cotton, Vegetables, Fruits, Flowers, Plantation crops, Field crops",
        "target_activities": "Installation of Drip Irrigation and Sprinkler Irrigation systems",
        "state": "Karnataka",
        "district_scope": "All districts of Karnataka",
        "farmer_categories": "Small & Marginal Farmers (<= 2 ha / 5 acres), Other / Large Farmers (> 2 ha), SC/ST farmers",
        "min_land": "0.2 hectares (approx. 0.5 acres)",
        "max_land": "5.0 hectares (approx. 12.35 acres per beneficiary family)",
        "irrigation_requirements": "Must have an assured water source (Borewell, Open well, Canal, Farm pond, River lift) capable of supplying micro-irrigation",
        "existing_asset_requirements": "Must possess an operational water pump set / source; land parcel must not have received micro-irrigation subsidy in the past 7 years",
        "eligible_conditions": "Ownership of cultivable land with valid RTC/Pahani; valid FRUITS ID; assured source of irrigation on the farm; selection of BIS-certified micro-irrigation system from empanelled manufacturers.",
        "excluded_conditions": "Farmers without an assured water source; applicants who availed micro-irrigation subsidy for the same land parcel within the previous 7 years; non-agricultural land.",
        "benefit_rate": "Central base subsidy: 55% of indicative unit cost for Small/Marginal Farmers (<= 2 ha) and 45% for Other Farmers (> 2 ha). Karnataka provides additional state top-up subsidy, raising total assistance up to 90% for SC/ST farmers and ~70-75% for General SMF under state program components.",
        "maximum_benefit": "Capped by area (up to 5 ha / 12.35 acres) and crop-spacing specific unit cost norms (e.g., Rs. 1,00,000 to Rs. 1,30,000 per ha for closely spaced crops, Rs. 45,000 to Rs. 65,000 per ha for wide spaced fruit crops)",
        "benefit_formula": "Subsidy = Indicative_Cost_per_ha(crop_spacing, land_area) * Effective_Subsidy_Rate (55%/45% Central base + State top-up)",
        "upfront_benefit_support": "Capital cost subsidy credited via DBT to empanelled vendor / farmer account upon installation inspection and geo-tagging.",
        "contingent_benefit_clause": "None (Capital equipment procurement subsidy)",
        "claim_disclaimer": "None (Disbursement contingent upon physical field verification, GPS geo-tagging, and 7-year non-duplication check).",
        "application_period": "Annual financial year cycle (typically opening in April-May; ongoing till district target allocation exhausted)",
        "application_method": "Online via Karnataka Horticulture/Agriculture DBT portal / Raitha Mitra / Seva Sindhu, or offline via Senior Assistant Director of Horticulture (SADH) / RSK",
        "required_documents": "Aadhaar card, FRUITS ID, RTC/Pahani, Water source proof (borewell/well certificate/NOC), Soil and water testing report, Bank passbook, Land sketch/map, Caste certificate (for SC/ST 90% top-up)",
        "official_source_url": "https://pmksy.gov.in/",
        "official_document_url": "https://pmksy.gov.in/pdms/Guidelines/Operational_Guidelines_PDMC.pdf",
        "audit_status": "VERIFIED",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH004: SMAM (STANDALONE)
    # =========================================================================
    {
        "scheme_id": "SCH004",
        "scheme_name": "Sub-Mission on Agricultural Mechanization (SMAM)",
        "record_type": "STANDALONE",
        "parent_scheme_id": None,
        "government_level": "Central-State Co-sponsored (60:40 Centre:State)",
        "department": "Mechanization and Technology Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka",
        "benefit_type": "Capital Subsidy on Farm Machinery Procurement & Custom Hiring Centers",
        "target_crops": "All crops (Paddy, Ragi, Maize, Pulses, Cotton, Sugarcane, Oilseeds, Horticulture)",
        "target_activities": "Procurement of tractors, power tillers, rotavators, multi-crop threshers, reapers, seed-cum-fertilizer drills, crop transplanters, laser land levelers, power weeders, sprayers",
        "state": "Karnataka",
        "district_scope": "All districts of Karnataka",
        "farmer_categories": "Small & Marginal Farmers (<= 2 ha), Women farmers, SC/ST farmers, General / Large farmers (> 2 ha)",
        "min_land": "> 0 acres (For tractor subsidy: min 2 to 3 acres cultivable land depending on horsepower)",
        "max_land": "No upper ceiling (Subsidy percentage differs: 50% for SMF/Women/SC/ST vs 40% for General)",
        "irrigation_requirements": "None",
        "existing_asset_requirements": "For tractor-drawn implements: applicant must own a registered tractor (RC book required in applicant's name); no prior subsidy for the same machine category within last 5 to 7 years",
        "eligible_conditions": "Cultivating farmer with verified land ownership in Karnataka; valid FRUITS ID; valid driving license (if applying for self-propelled machinery); purchase from authorized empanelled dealers through DBT.",
        "excluded_conditions": "Applicants who availed subsidy for the same equipment type in the last 5 years; non-agricultural entities; lack of registered tractor RC for tractor-drawn implements; failure to provide manufacturer invoice with FMTTI testing certificate.",
        "benefit_rate": "50% of machine cost (subject to category cap) for SC, ST, Small & Marginal farmers, and Women; 40% of machine cost (subject to category cap) for Other / General farmers.",
        "maximum_benefit": "Specific per-machine caps: e.g., Power Tiller (8 HP and above) max Rs. 85,000; Rotavator max Rs. 42,000 to Rs. 50,000; Multi-crop thresher max Rs. 1,00,000; Tractor (up to 40 PTO HP) max Rs. 1,25,000 to Rs. 2,00,000 depending on model norm.",
        "benefit_formula": "Subsidy = Min(Cost * Subsidy_Percentage, Max_Cap_for_Equipment_Type)",
        "upfront_benefit_support": "DBT subsidy disbursed to empanelled dealer / farmer bank account against purchase invoice and physical machinery inspection.",
        "contingent_benefit_clause": "None (Machinery procurement subsidy)",
        "claim_disclaimer": "None (Disbursement contingent upon physical machine inspection, chassis/serial number verification, and budget quota availability).",
        "application_period": "Financial year notification window (April to October, or till district budget quota is exhausted)",
        "application_method": "Online via National Farmech portal (agrimachinery.nic.in) or Karnataka Agriculture DBT / Raitha Mitra portal",
        "required_documents": "Aadhaar card, FRUITS ID, RTC/Pahani copy, Bank passbook, Caste certificate (SC/ST), Tractor RC book (mandatory for tractor-driven implements), Passport photo",
        "official_source_url": "https://agrimachinery.nic.in/",
        "official_document_url": "https://agrimachinery.nic.in/Files/Guidelines/SMAM_Guidelines.pdf",
        "audit_status": "VERIFIED",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH005: Krishi Bhagya (STANDALONE)
    # =========================================================================
    {
        "scheme_id": "SCH005",
        "scheme_name": "Krishi Bhagya Yojana",
        "record_type": "STANDALONE",
        "parent_scheme_id": None,
        "government_level": "State (Government of Karnataka)",
        "department": "Department of Agriculture, Government of Karnataka",
        "benefit_type": "Integrated Capital Subsidy Package (Farm Pond, Polythene Lining, Pump, Micro-irrigation)",
        "target_crops": "Dryland / Rainfed crops (Millets, Pulses, Oilseeds, Cotton, Maize, Groundnut, Red gram)",
        "target_activities": "Rainwater harvesting via Farm Pond (Krishi Honda), polythene film lining to prevent percolation, water lifting diesel/solar pump sets, micro-irrigation (drip/sprinkler), and shade net/fence protection",
        "state": "Karnataka",
        "district_scope": "Rainfed and drought-prone taluks across Karnataka (specifically focused on 131+ dryland taluks in Northern & Central Karnataka / Bayaluseeme)",
        "farmer_categories": "SC / ST Farmers, General Category Small & Marginal Farmers, General Large Farmers",
        "min_land": "1.0 acre (minimum catchment area to sustain farm pond runoff)",
        "max_land": "5.0 hectares (approx. 12.35 acres; farm pond sizing scaled to holding size)",
        "irrigation_requirements": "Must be dryland / rainfed agricultural land without assured perennial canal or river irrigation",
        "existing_asset_requirements": "Suitable slope/catchment on the land for runoff collection; applicant must not have an existing funded farm pond on the same plot",
        "eligible_conditions": "Dryland farmer holding land in designated rainfed taluks; possess valid FRUITS ID; agree to construct farm pond as per standardized departmental specifications (e.g., 10x10x3m, 12x12x3m, or 15x15x3m); provide site feasibility access for GPS geo-tagging and field verification.",
        "excluded_conditions": "Farmers with existing perennial canal irrigation; command areas of major irrigation projects; farmers who already received Krishi Bhagya subsidy within the previous 5 years.",
        "benefit_rate": "90% subsidy for SC and ST farmers; 80% subsidy for General category dryland farmers across all package components.",
        "maximum_benefit": "Component-wise caps: Krishi Honda (construction) max Rs. 25,000-Rs. 40,000 depending on dimensions; Polythene lining max Rs. 50,000-Rs. 80,000; Pump set max Rs. 18,000-Rs. 25,000; Total integrated package assistance up to Rs. 1,25,000 to Rs. 1,75,000 per farm unit.",
        "benefit_formula": "Package Subsidy = Sum_over_components(Min(Component_Cost, Standard_Norm) * Subsidy_Rate [0.90 for SC/ST, 0.80 for General])",
        "upfront_benefit_support": "Staged DBT reimbursement after geo-tagged inspection of excavation, polythene film laying, and pump installation.",
        "contingent_benefit_clause": "None (Integrated infrastructure subsidy)",
        "claim_disclaimer": "None (Disbursement contingent upon stage-wise geo-tagged site photographs: pre-work, excavation, and completed lining).",
        "application_period": "Pre-monsoon season window (typically April to July) to enable excavation before rainfall",
        "application_method": "Raitha Samparka Kendra (RSK) at Hobli level, Assistant Director of Agriculture (ADA) office, or online via Raitha Mitra / Seva Sindhu",
        "required_documents": "Aadhaar card, FRUITS ID, RTC/Pahani, Caste certificate (for SC/ST 90% rate), Bank passbook, Geo-tagged site photographs",
        "official_source_url": "https://raitamitra.karnataka.gov.in/",
        "official_document_url": "https://raitamitra.karnataka.gov.in/page/Programmes/Krishi+Bhagya/en",
        "audit_status": "VERIFIED",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH006: PM-KUSUM Component B (STANDALONE)
    # =========================================================================
    {
        "scheme_id": "SCH006",
        "scheme_name": "PM-KUSUM Component B (Standalone Solar Agriculture Pumps)",
        "record_type": "STANDALONE",
        "parent_scheme_id": None,
        "government_level": "Central-State Co-sponsored (30% Central CFA + 30% State Subsidy + 40% Farmer share/loan)",
        "department": "Ministry of New and Renewable Energy (MNRE), Govt of India / Karnataka Renewable Energy Development Limited (KREDL), Govt of Karnataka",
        "benefit_type": "Capital Subsidy on Solar Powered Water Pumping Systems",
        "target_crops": "All crops (Horticulture, plantation, cash crops, cereals)",
        "target_activities": "Installation of standalone DC or AC solar powered surface or submersible agriculture pumps (up to 7.5 HP) in off-grid areas",
        "state": "Karnataka",
        "district_scope": "All districts of Karnataka (priority in non-electrified off-grid agricultural pockets and dark/critical groundwater zones for replacement)",
        "farmer_categories": "Individual farmers, group of farmers, Water User Associations, FPOs",
        "min_land": "0.5 acres (adequate land for cultivation and solar array installation)",
        "max_land": "No ceiling (capacity allocated based on land area and water requirement up to 7.5 HP)",
        "irrigation_requirements": "Requires an existing borewell, dug well, open well, or farm pond with adequate water yield; water source must NOT have an existing grid-connected electric pump connection",
        "existing_asset_requirements": "Must have an existing drilled water source (borewell/well); must NOT already possess a grid-connected electric pump set (DISCOM IP set) on the same borewell; shade-free area for solar PV panel installation",
        "eligible_conditions": "Farmer with cultivable land and an available un-energized water source (borewell/open well); no existing grid electricity connection (DISCOM IP set) for the proposed water source; valid FRUITS ID and land RTC; willingness to contribute 10-40% beneficiary share or take bank loan.",
        "excluded_conditions": "Borewells with existing grid electricity connections (covered under Component C instead); areas where groundwater extraction is legally prohibited/banned by Central Ground Water Authority; barren land without water source; requests to drill new borewells (scheme does not fund drilling).",
        "benefit_rate": "60% total subsidy (30% Central CFA + 30% State Subsidy from Karnataka Govt / KREDL); Farmer pays balance 40% (can obtain bank loan for up to 30%, cash contribution 10%).",
        "maximum_benefit": "Capped on benchmark cost per HP rating: 3 HP Pump benchmark cost ~Rs. 1.80 Lakh (Subsidy ~Rs. 1.08 Lakh); 5 HP Pump benchmark ~Rs. 2.60 Lakh (Subsidy ~Rs. 1.56 Lakh); 7.5 HP Pump benchmark ~Rs. 3.50 Lakh (Subsidy ~Rs. 2.10 Lakh).",
        "benefit_formula": "Subsidy = 0.60 * Min(Tender_Cost, MNRE_Benchmark_Cost_up_to_7.5_HP)",
        "upfront_benefit_support": "Direct subsidy contribution toward solar pump system procurement, reducing farmer payable share to 10-40%.",
        "contingent_benefit_clause": "None (Capital equipment installation subsidy)",
        "claim_disclaimer": "None (Installation contingent upon water yield feasibility and ESCOM non-energization certification).",
        "application_period": "Notification-based tender rounds issued by KREDL (typically annual rounds)",
        "application_method": "Online application via KREDL Portal (kredl.karnataka.gov.in) / PM-KUSUM National Portal (pmkusum.mnre.gov.in)",
        "required_documents": "Aadhaar card, FRUITS ID, RTC/Pahani, Water source feasibility/yield certificate, Certificate from Electricity Supply Company (ESCOM - BESCOM/HESCOM/GESCOM/MESCOM/CESC) confirming no grid connection, Bank passbook",
        "official_source_url": "https://pmkusum.mnre.gov.in/",
        "official_document_url": "https://mnre.gov.in/img/documents/uploads/file_f-1678881261327.pdf",
        "audit_status": "VERIFIED",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH007: MIDH (STANDALONE)
    # =========================================================================
    {
        "scheme_id": "SCH007",
        "scheme_name": "Mission for Integrated Development of Horticulture (MIDH)",
        "record_type": "STANDALONE",
        "parent_scheme_id": None,
        "government_level": "Central-State Co-sponsored (60:40 Centre:State)",
        "department": "Horticulture Division, DA&FW, MoA&FW / Department of Horticulture, Government of Karnataka",
        "benefit_type": "Capital Subsidy for Protected Cultivation and High-Value Crop Infrastructure",
        "target_crops": "Horticultural crops: Fruits (Mango, Banana, Pomegranate, Grapes, Papaya), Vegetables (Capsicum, Tomato, Cucumber), Flowers (Roses, Gerbera, Carnation), Spices, Aromatic plants",
        "target_activities": "Construction of Naturally Ventilated Polyhouse, Shade Net House, Plastic Mulching, Pack house, Cold storage, and new high-density orchard establishment",
        "state": "Karnataka",
        "district_scope": "All 31 districts of Karnataka covered under State Horticulture Mission (SHM)",
        "farmer_categories": "All landholding farmers (Small, Marginal, Large), FPOs, cooperatives",
        "min_land": "1,000 square meters (0.25 acres) for protected structures",
        "max_land": "4,000 square meters (approx. 1.0 acre) per beneficiary family for polyhouse/shade net structures; up to 4 ha for orchard establishment",
        "irrigation_requirements": "Mandatory assured source of irrigation (borewell/water harvesting pond) with micro-irrigation system installed",
        "existing_asset_requirements": "Availability of contiguous suitable soil land parcel; micro-irrigation setup; road accessibility for material transportation",
        "eligible_conditions": "Farmer must own cultivable land with valid RTC; valid FRUITS ID; construction must adhere strictly to MIDH technical design specifications; structure must be built by empanelled agencies approved by Karnataka State Horticulture Mission.",
        "excluded_conditions": "Farmers without assured irrigation source; projects started before formal administrative sanction letter from District Horticulture Officer; availing duplicate subsidy from NHB or other agency for same structure.",
        "benefit_rate": "50% of cost norm for protected cultivation structures (Naturally Ventilated Polyhouse, Shade Net House) and planting material.",
        "maximum_benefit": "Cost norm for Naturally Ventilated Polyhouse is Rs. 844 to Rs. 1,060 per sq. meter (Subsidy: Rs. 422 to Rs. 530/sq.m; max ~Rs. 16.88 Lakh for 4,000 sq.m); Shade Net House cost norm Rs. 710/sq.m (Subsidy Rs. 355/sq.m; max ~Rs. 14.20 Lakh for 4,000 sq.m).",
        "benefit_formula": "Subsidy = 0.50 * Area_in_sq_m * MIDH_Cost_Norm_per_sq_m",
        "upfront_benefit_support": "Direct back-ended subsidy released in stages to bank account / vendor upon physical verification of structure completion.",
        "contingent_benefit_clause": "None (Protected infrastructure capital subsidy)",
        "claim_disclaimer": "None (Prior administrative sanction before commencing construction is mandatory; unapproved work is strictly ineligible).",
        "application_period": "Opening of annual action plan window (April-June) and continuous submission to Senior Assistant Director of Horticulture (SADH)",
        "application_method": "Online via Karnataka Horticulture DBT / Seva Sindhu or offline application at Senior Assistant Director of Horticulture (SADH) office at Taluk level",
        "required_documents": "Aadhaar card, FRUITS ID, RTC/Pahani copy, Water and soil testing certificates, Blueprint/estimate from empanelled vendor, Bank passbook, Prior sanction letter",
        "official_source_url": "https://midh.gov.in/",
        "official_document_url": "https://midh.gov.in/PDF/MIDH_Guidelines_English.pdf",
        "audit_status": "VERIFIED",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH008: Agricultural Credit (PARENT CATEGORY)
    # =========================================================================
    {
        "scheme_id": "SCH008",
        "scheme_name": "Kisan Credit Card (KCC) & Concessional Crop Credit Schemes (Parent Category)",
        "record_type": "PARENT",
        "parent_scheme_id": None,
        "government_level": "Central & State Implementation Routes",
        "department": "DA&FW, MoA&FW, RBI, NABARD / Department of Cooperation, Govt of Karnataka",
        "benefit_type": "Interest Subvention on Short-Term Production Credit",
        "target_crops": "All crops (Cereals, pulses, oilseeds, cash crops, horticulture) + Animal Husbandry, Dairy, Fisheries",
        "target_activities": "Short-term seasonal crop cultivation expenses, post-harvest maintenance, farm asset working capital",
        "state": "All India & Karnataka",
        "district_scope": "All districts of Karnataka",
        "farmer_categories": "All categories: Owner cultivators, tenant farmers, oral lessees, sharecroppers, SHGs, JLGs",
        "min_land": "> 0 acres",
        "max_land": "No limit (Credit limit calculated using Scale of Finance * Cultivated Area + 10% post-harvest + 20% maintenance)",
        "irrigation_requirements": "None (Scale of finance accounts for rainfed vs irrigated crops separately)",
        "existing_asset_requirements": "None (Collateral-free loans up to statutory limits: Rs. 1.60 Lakh Central, Rs. 2.00 Lakh tie-up)",
        "eligible_conditions": "Parent umbrella category covering: (1) Central KCC-MISS via Commercial Banks/RRBs (4% effective interest up to Rs. 3 Lakh); (2) Karnataka Cooperative Credit via PACS/DCCBs (0% interest up to Rs. 5 Lakh). See child records SCH008_CENTRAL and SCH008_KA_COOP.",
        "excluded_conditions": "Willful defaulters on agricultural loans; non-agricultural entities; non-repayment within one year forfeits prompt repayment incentive.",
        "benefit_rate": "Central route: 4.0% effective interest p.a. (via 2% IS + 3% PRI); Karnataka Cooperative route: 0.0% interest p.a. (subject to annual state GO).",
        "maximum_benefit": "Central route: Up to Rs. 3,00,000; Karnataka Cooperative route: Up to Rs. 5,00,000.",
        "benefit_formula": "Annual Interest Saving = Loan_Disbursed * (Normal_Market_Rate [e.g. 9-11%] - Concessional_Rate [4% or 0%])",
        "upfront_benefit_support": "Concessional credit access with upfront subsidized interest rate and prompt repayment rebate.",
        "contingent_benefit_clause": "None (Subsidized working capital loan facility)",
        "claim_disclaimer": "None (Benefit contingent upon prompt repayment within 365 days / due date; default reverts to commercial lending rates).",
        "application_period": "Open year-round (Revolving credit card valid for 5 years with annual review)",
        "application_method": "Commercial banks, Regional Rural Banks (KGB, KVGB), or Primary Agricultural Credit Societies (PACS) / DCCBs",
        "required_documents": "Aadhaar card, FRUITS ID / RTC (Pahani), Proof of crop sown, Bank passbook, No-dues certificate (if loan exceeds threshold)",
        "official_source_url": "https://www.rbi.org.in/ / https://cooperation.karnataka.gov.in/",
        "official_document_url": "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/NOTI76B66FA126C39744EE81F9DBB4A346CF87.PDF",
        "audit_status": "PARENT_CATEGORY",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH008_CENTRAL: KCC-MISS Central Route (CHILD of SCH008)
    # =========================================================================
    {
        "scheme_id": "SCH008_CENTRAL",
        "scheme_name": "Kisan Credit Card - Modified Interest Subvention Scheme (Central KCC-MISS via Commercial Banks / RRBs)",
        "record_type": "CHILD",
        "parent_scheme_id": "SCH008",
        "government_level": "Central",
        "department": "Department of Agriculture and Farmers Welfare (DA&FW), MoA&FW in collaboration with RBI and NABARD",
        "benefit_type": "Interest Subvention on Short-Term Concessional Production Credit",
        "target_crops": "All crops (Cereals, pulses, oilseeds, cash crops, horticulture) + Animal Husbandry, Dairy, Fisheries",
        "target_activities": "Short-term seasonal crop cultivation expenses, post-harvest maintenance, farm asset working capital",
        "state": "All India (including Karnataka)",
        "district_scope": "All districts of Karnataka via Commercial Banks and Regional Rural Banks (Karnataka Gramin Bank, KVGB)",
        "farmer_categories": "All categories: Owner cultivators, tenant farmers, oral lessees, sharecroppers, SHGs and Joint Liability Groups (JLGs)",
        "min_land": "> 0 acres",
        "max_land": "No limit (Credit limit calculated using Scale of Finance * Cultivated Area + 10% post-harvest + 20% maintenance)",
        "irrigation_requirements": "None (Scale of finance accounts for rainfed vs irrigated crops separately)",
        "existing_asset_requirements": "None (No collateral required for loans up to Rs. 1.60 Lakh; raised to Rs. 2.00 Lakh for dairy/fisheries)",
        "eligible_conditions": "Farmer cultivating crops or allied activity; satisfactory credit bureau (CIBIL) score with no default on existing loans; Aadhaar-linked savings bank account; valid land records (RTC) / registered tenancy certificate. Disbursed via Commercial Banks and RRBs.",
        "excluded_conditions": "Willful defaulters on earlier agricultural loans; individuals without agricultural cultivation or allied activity; non-repayment within 365 days forfeits the 3% prompt repayment incentive.",
        "benefit_rate": "Standard lending rate 9% subsidized down to 7% p.a. (2% subvention to lending bank). Additional 3% Prompt Repayment Incentive (PRI) for repayment on or before due date, making the effective rate of interest 4.0% per annum on short-term crop loans up to Rs. 3,00,000.",
        "maximum_benefit": "Applicable on short-term crop loans up to Rs. 3,00,000 (sub-limit of Rs. 2,00,000 for animal husbandry/dairy/fisheries within the Rs. 3 Lakh cap).",
        "benefit_formula": "Effective_Interest_Rate = 7% - 3% (PRI for prompt repayment within 365 days) = 4.0% p.a. (Annual interest saving: 5% of disbursed loan amount up to Rs. 3 Lakh = up to Rs. 15,000/year).",
        "upfront_benefit_support": "Immediate access to 7% nominal lending rate, with additional 3% rebate credited upon prompt repayment.",
        "contingent_benefit_clause": "None (Concessional credit facility)",
        "claim_disclaimer": "None (4% effective interest is contingent upon prompt repayment within 365 days; baseline established under MoA&FW / RBI Circular; formal activation for FY 2026-27 requires annual MoA&FW/RBI interest subvention circular verification).",
        "application_period": "Open year-round (Revolving credit card valid for 5 years with annual review)",
        "application_method": "Any Commercial Bank branch (SBI, Canara, etc.), Regional Rural Bank (Karnataka Gramin Bank, Karnataka Vikas Grameena Bank), or JanSamarth portal",
        "required_documents": "Aadhaar card, FRUITS ID / RTC (Pahani), Proof of crop sown, Passport photo, No-dues certificate (if loan exceeds Rs. 1.60 Lakh)",
        "official_source_url": "https://www.rbi.org.in/",
        "official_document_url": "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/NOTI76B66FA126C39744EE81F9DBB4A346CF87.PDF",
        "audit_status": "VERIFIED_HISTORICAL_BASELINE",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH008_KA_COOP: Karnataka Cooperative Credit Route (CHILD of SCH008)
    # =========================================================================
    {
        "scheme_id": "SCH008_KA_COOP",
        "scheme_name": "Karnataka Zero-Interest Agricultural Crop Loan Scheme (Baddi Rahitha Bele Sala via PACS / DCCBs)",
        "record_type": "CHILD",
        "parent_scheme_id": "SCH008",
        "government_level": "State (Government of Karnataka)",
        "department": "Department of Cooperation, Government of Karnataka, in collaboration with DCCBs, Apex Bank, and PACS",
        "benefit_type": "100% State Interest Subvention (Zero-Interest Production Credit)",
        "target_crops": "All food, commercial, and horticultural crops notified by the Department of Agriculture / Cooperation",
        "target_activities": "Short-term seasonal agricultural operations and crop cultivation expenses",
        "state": "Karnataka",
        "district_scope": "All districts of Karnataka via Primary Agricultural Credit Societies (PACS) and District Central Cooperative Banks (DCCBs)",
        "farmer_categories": "All landholding farmer members of PACS / Cooperative societies in Karnataka (Small, Marginal, Medium, Large)",
        "min_land": "> 0 acres",
        "max_land": "No limit (Credit limit calculated per Scale of Finance determined by DLTC for cooperative sector)",
        "irrigation_requirements": "None (Scale of finance accounts for rainfed vs irrigated crops separately)",
        "existing_asset_requirements": "Membership in local Primary Agricultural Credit Society (PACS); no default on prior cooperative borrowings",
        "eligible_conditions": "Farmer resident of Karnataka who is a shareholder/member of local PACS; possesses valid RTC/Pahani and FRUITS ID; timely repayment of earlier cooperative loans. Short-term crop loans up to Rs. 5,00,000 are provided at 0% (zero) interest if repaid on or before the due date.",
        "excluded_conditions": "Non-members of PACS; borrowers who fail to repay within the scheduled repayment date (interest subvention is forfeited and normal DCCB interest applies); overdue cooperative defaulters.",
        "benefit_rate": "0.0% (Zero) effective interest per annum. Government of Karnataka provides 100% interest subvention on short-term crop loans up to Rs. 5,00,000 upon prompt repayment.",
        "maximum_benefit": "Zero interest on short-term crop loans up to Rs. 5,00,000 (Rs. 5.00 Lakh, enhanced from Rs. 3 Lakh in recent Karnataka state budgets). Medium-term loans up to Rs. 15 Lakh provided at 3% interest.",
        "benefit_formula": "Annual Interest Saving = Disbursed_Loan_up_to_5_Lakh * Full_Market_Interest_Rate (~10-12% p.a. saved = up to Rs. 50,000 - Rs. 60,000/year).",
        "upfront_benefit_support": "Zero percent interest charged on crop loans disbursed through PACS, fully borne by state cooperative interest subsidy.",
        "contingent_benefit_clause": "None (Subsidized cooperative credit facility)",
        "claim_disclaimer": "None (Zero percent interest is strictly contingent upon 100% prompt repayment within the due date; PROVISIONAL: Maintained in provisional status pending verification of active financial year Government Order and budgetary allocation from Cooperation Department, Govt of Karnataka).",
        "application_period": "Kharif and Rabi seasonal disbursement cycles via local PACS",
        "application_method": "Local Primary Agricultural Credit Society (PACS) at Village/Gram Panchayat level or District Central Cooperative Bank (DCCB) branch",
        "required_documents": "Aadhaar card, FRUITS ID, Land RTC (Pahani), PACS Membership certificate, Sowing certificate from Village Accountant / Revenue department, Bank passbook",
        "official_source_url": "https://cooperation.karnataka.gov.in/",
        "official_document_url": "https://cooperation.karnataka.gov.in/",
        "audit_status": "PROVISIONAL_PENDING_ANNUAL_GO",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH009: Soil Health Card (STANDALONE)
    # =========================================================================
    {
        "scheme_id": "SCH009",
        "scheme_name": "Soil Health Card Scheme",
        "record_type": "STANDALONE",
        "parent_scheme_id": None,
        "government_level": "Central-State Co-sponsored (60:40 Centre:State)",
        "department": "Integrated Nutrient Management Division, DA&FW, MoA&FW / Department of Agriculture, Govt of Karnataka",
        "benefit_type": "Free Technical Service & Soil Nutrient Diagnostic Card",
        "target_crops": "All crops (Field crops, pulses, oilseeds, commercial crops, horticulture)",
        "target_activities": "Soil sampling, scientific lab testing of 12 chemical and physical soil parameters, generation of customized fertilizer and bio-fertilizer dosage recommendations",
        "state": "Karnataka",
        "district_scope": "All 31 districts of Karnataka",
        "farmer_categories": "All farmer categories (Marginal, Small, Medium, Large)",
        "min_land": "> 0 acres",
        "max_land": "No limit (Grid sampling: 2.5 ha grid in irrigated areas, 10 ha grid in rainfed areas)",
        "irrigation_requirements": "None",
        "existing_asset_requirements": "None",
        "eligible_conditions": "Operational farming household in Karnataka; registered under FRUITS database; agricultural land parcel accessible for geo-referenced soil sample extraction.",
        "excluded_conditions": "Non-agricultural land; uncultivated barren rocky terrain.",
        "benefit_rate": "100% free government diagnostic service. Direct testing cost (Rs. 150-Rs. 300 per sample) is fully borne by government.",
        "maximum_benefit": "Free diagnostic test and customized crop-specific fertilizer advisory card issued every 2 to 3 years; potential saving of 15-25% on chemical fertilizer costs through balanced application.",
        "benefit_formula": "Free Diagnostic Benefit = Cost of 12-parameter soil test (Rs. 300 value) + customized nutrient dosage advisory matrix per crop",
        "upfront_benefit_support": "Free scientific soil testing and customized fertilizer recommendation card delivered directly to the farmer.",
        "contingent_benefit_clause": "None (Diagnostic service)",
        "claim_disclaimer": "None (Universal free technical diagnostic advisory).",
        "application_period": "Post-harvest sampling window (typically February to May, before Kharif sowing, when fields are cleared)",
        "application_method": "Raitha Samparka Kendra (RSK) at Hobli level, Village Agriculture Assistant (VAA), or online portal check at soilhealth.dac.gov.in",
        "required_documents": "Aadhaar card, FRUITS ID, Land RTC (Survey number and Hissa number), Field location / coordinates",
        "official_source_url": "https://soilhealth.dac.gov.in/",
        "official_document_url": "https://soilhealth.dac.gov.in/Content/Guideline_Soil_Health_Card.pdf",
        "audit_status": "VERIFIED",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH010: Ganga Kalyana Umbrella (PARENT CATEGORY)
    # =========================================================================
    {
        "scheme_id": "SCH010",
        "scheme_name": "Ganga Kalyana Scheme (Parent Category / Umbrella Free Borewell Infrastructure Package)",
        "record_type": "PARENT",
        "parent_scheme_id": None,
        "government_level": "State (Government of Karnataka)",
        "department": "Administered across multiple statutory Caste/Community Development Corporations (Dr. B.R. Ambedkar, Valmiki, D. Devaraj Urs, KMDC)",
        "benefit_type": "100% Subsidized Infrastructure (Borewell Drilling, Submersible Pump Set, Accessories, and Power Energization)",
        "target_crops": "All crops (Paddy, sugarcane, vegetables, arecanut, maize, pulses)",
        "target_activities": "Drilling of irrigation borewell, supply and installation of submersible pump set with control panel and accessories, and power energization through ESCOMs",
        "state": "Karnataka",
        "district_scope": "All 31 districts of Karnataka (Unit cost higher in water-scarce districts like Kolar, Chikkaballapur, Bengaluru Rural, Tumakuru, Ramanagara)",
        "farmer_categories": "Small and Marginal dryland farmers belonging to Scheduled Castes (SC), Scheduled Tribes (ST), Backward Classes (Cat 1, 2A, 3A, 3B), and Religious Minorities",
        "min_land": "Individual Route: 1.0 ac (Coastal/Malnad) / 1.20 ac (Plains); Community Route: 8.0 ac pooled (group of 2+ farmers)",
        "max_land": "Individual Route: 5.0 ac; Community Route: 15.0 ac pooled",
        "irrigation_requirements": "Land must be exclusively dryland (kushki) without any existing irrigation borewell, open well, or perennial canal facility",
        "existing_asset_requirements": "Farmer must not already possess a working borewell or energized pump set on the RTC land parcel",
        "eligible_conditions": "Umbrella parent scheme covering 100% free borewell and pump infrastructure. Distinct eligibility rules apply across specific implementing corporations (SCH010_AMBEDKAR for SC, SCH010_VALMIKI for ST, SCH010_DEVARAJ_URS for OBC, SCH010_KMDC for Minorities). Both Individual (1.20-5.0 ac) and Community (8-15 ac pooled) routes are supported. Note: Additional corporations also implement Ganga Kalyana variants (e.g. Arya Vysya, Brahmin, Veerashaiva-Lingayat, Maratha, Kadugolla Dev Corps) not covered in these 4 primary records.",
        "excluded_conditions": "General Merit category farmers; farmers owning more than 5.0 acres dryland for individual borewells; land parcels with existing irrigation facilities; family members of government employees or previous Ganga Kalyana beneficiaries in the household.",
        "benefit_rate": "100% government subsidized infrastructure package (zero financial investment required from the beneficiary).",
        "maximum_benefit": "Total package assistance up to Rs. 3,75,000 in water-scarce districts and up to Rs. 2,50,000 in other districts (includes drilling, pump, starter, pipes, and Rs. 50,000 deposit to ESCOM for electrification).",
        "benefit_formula": "Full Grant Package = Drilling_Cost + Pump_and_Accessories_Cost + Electrification_Deposit (Up to Rs. 2.50L or Rs. 3.75L depending on district hydro-geological zone)",
        "upfront_benefit_support": "100% fully funded infrastructure asset installed directly on the farmer's field with zero beneficiary capital contribution.",
        "contingent_benefit_clause": "None (Capital infrastructure grant)",
        "claim_disclaimer": "None (Execution contingent upon hydro-geological groundwater survey feasibility, corporation annual budget quota, and ESCOM power grid infrastructure).",
        "application_period": "Annual application cycle announced via gazette notification (typically July to September)",
        "application_method": "Online via Karnataka Seva Sindhu portal (sevasindhu.karnataka.gov.in) routed to respective Corporation District Managers",
        "required_documents": "Aadhaar card, FRUITS ID, Land RTC (Pahani) showing dryland status, Caste certificate with RD number, Income certificate with RD number, Small/Marginal Farmer certificate from Tahsildar, Bank passbook, Self-declaration of no existing borewell",
        "official_source_url": "https://sevasindhu.karnataka.gov.in/",
        "official_document_url": "https://kmdc.karnataka.gov.in/storage/pdf-files/Ganga%20kalyana%20Guidelines.pdf",
        "audit_status": "PARENT_CATEGORY",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH010_AMBEDKAR: Ganga Kalyana SC Route (CHILD of SCH010)
    # =========================================================================
    {
        "scheme_id": "SCH010_AMBEDKAR",
        "scheme_name": "Ganga Kalyana Scheme — Dr. B.R. Ambedkar Development Corporation (SC)",
        "record_type": "CHILD",
        "parent_scheme_id": "SCH010",
        "government_level": "State (Government of Karnataka)",
        "department": "Dr. B.R. Ambedkar Development Corporation Limited, Social Welfare Department, Govt of Karnataka",
        "benefit_type": "100% Subsidized Infrastructure (Borewell Drilling, Submersible Pump Set, and Power Energization)",
        "target_crops": "All agricultural crops",
        "target_activities": "Drilling of irrigation borewell, supply and installation of submersible pump set with accessories, and electrification through ESCOMs",
        "state": "Karnataka",
        "district_scope": "All 31 districts of Karnataka",
        "farmer_categories": "Small and Marginal dryland farmers belonging exclusively to Scheduled Castes (SC)",
        "min_land": "Individual Route: 1.50 ac (1 acre 20 guntas); Community Route: 8.0 ac pooled (group of 3+ SC beneficiaries)",
        "max_land": "Individual Route: 5.0 ac; Community Route: 15.0 ac pooled",
        "irrigation_requirements": "Land must be dryland (kushki) without any existing irrigation borewell, open well, or canal facility",
        "existing_asset_requirements": "Farmer must not already possess a working borewell or energized pump set on the RTC land parcel",
        "eligible_conditions": "Permanent resident of Karnataka; belonging strictly to Scheduled Castes (SC) with valid RD-numbered caste certificate; family annual income from all sources within corporation limit (historically Rs. 1.50L-Rs. 2.00L; provisional pending active annual notice); owning dryland between 1.50 and 5.0 acres for Individual Route, OR group of 3+ SC farmers pooling 8.0 to 15.0 acres for Community Route (Samooha Kola Bavi); valid FRUITS ID.",
        "excluded_conditions": "Non-SC farmers; General Merit, OBC, and Minority applicants (must apply to their respective corporations); farmers owning > 5 acres dryland for individual route; individual dryland holdings below 1.5 acres (unless pooling >= 8.0 acres with >= 3 SC beneficiaries); land with existing irrigation facilities; family members of government employees or prior Ganga Kalyana beneficiaries in the household.",
        "benefit_rate": "100% government grant (zero farmer contribution).",
        "maximum_benefit": "Total package up to Rs. 3,75,000 in water-scarce districts and up to Rs. 2,50,000 in other districts.",
        "benefit_formula": "Full Grant Package = Drilling_Cost + Pump_and_Accessories_Cost + Electrification_Deposit (Up to Rs. 2.50L or Rs. 3.75L)",
        "upfront_benefit_support": "100% fully funded borewell and pump installation executed directly by Dr. B.R. Ambedkar Development Corporation contractors.",
        "contingent_benefit_clause": "None (Capital infrastructure grant)",
        "claim_disclaimer": "None (Execution contingent upon hydro-geological groundwater survey feasibility, corporation annual budget quota, and ESCOM power grid infrastructure).",
        "application_period": "Annual application cycle announced via gazette notification (typically July to September)",
        "application_method": "Online via Karnataka Seva Sindhu portal (sevasindhu.karnataka.gov.in) under Dr. B.R. Ambedkar Development Corporation service menu",
        "required_documents": "Aadhaar card, FRUITS ID, Land RTC (Pahani) showing dryland status, SC Caste certificate with RD number, Income certificate with RD number, Small/Marginal Farmer certificate from Tahsildar, Bank passbook, Self-declaration of no existing borewell",
        "official_source_url": "https://adcl.karnataka.gov.in/ / https://sevasindhu.karnataka.gov.in/",
        "official_document_url": "https://adcl.karnataka.gov.in/",
        "audit_status": "VERIFIED",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH010_VALMIKI: Ganga Kalyana ST Route (CHILD of SCH010)
    # =========================================================================
    {
        "scheme_id": "SCH010_VALMIKI",
        "scheme_name": "Ganga Kalyana Scheme — Karnataka Maharshi Valmiki ST Development Corporation (ST)",
        "record_type": "CHILD",
        "parent_scheme_id": "SCH010",
        "government_level": "State (Government of Karnataka)",
        "department": "Karnataka Maharshi Valmiki Scheduled Tribes Development Corporation, Scheduled Tribes Welfare Department, Govt of Karnataka",
        "benefit_type": "100% Subsidized Infrastructure (Borewell Drilling, Submersible Pump Set, and Power Energization)",
        "target_crops": "All agricultural crops",
        "target_activities": "Drilling of irrigation borewell, supply and installation of submersible pump set with accessories, and electrification through ESCOMs",
        "state": "Karnataka",
        "district_scope": "All 31 districts of Karnataka",
        "farmer_categories": "Small and Marginal dryland farmers belonging exclusively to Scheduled Tribes (ST)",
        "min_land": "Individual Route: 1.0/1.20 to 5.0 ac; Community Route: 8.0 to 15.0 ac pooled (Provisional — pending corporation-specific guidelines audit)",
        "max_land": "Individual Route: 5.0 ac; Community Route: 15.0 ac pooled",
        "irrigation_requirements": "Land must be dryland (kushki) without any existing irrigation borewell, open well, or canal facility",
        "existing_asset_requirements": "Farmer must not already possess a working borewell or energized pump set on the RTC land parcel",
        "eligible_conditions": "Permanent resident of Karnataka; belonging strictly to Scheduled Tribes (ST) with valid RD-numbered caste certificate; family annual income from all sources within corporation limit (historically Rs. 1.50L-Rs. 2.00L; provisional pending active annual notice); owning dryland within corporation individual/community limits; valid FRUITS ID.",
        "excluded_conditions": "Non-ST farmers; General Merit, SC, OBC, and Minority applicants (must apply to their respective corporations); farmers owning > 5 acres dryland for individual route; land with existing irrigation facilities; family members of government employees or prior Ganga Kalyana beneficiaries in the household.",
        "benefit_rate": "100% government grant (zero farmer contribution).",
        "maximum_benefit": "Total package up to Rs. 3,75,000 in water-scarce districts and up to Rs. 2,50,000 in other districts.",
        "benefit_formula": "Full Grant Package = Drilling_Cost + Pump_and_Accessories_Cost + Electrification_Deposit (Up to Rs. 2.50L or Rs. 3.75L)",
        "upfront_benefit_support": "100% fully funded borewell and pump installation executed directly by Maharshi Valmiki ST Development Corporation contractors.",
        "contingent_benefit_clause": "None (Capital infrastructure grant)",
        "claim_disclaimer": "None (Execution contingent upon hydro-geological groundwater survey feasibility, corporation annual budget quota, and ESCOM power grid infrastructure).",
        "application_period": "Annual application cycle announced via gazette notification (typically July to September)",
        "application_method": "Online via Karnataka Seva Sindhu portal (sevasindhu.karnataka.gov.in) under Maharshi Valmiki ST Development Corporation service menu",
        "required_documents": "Aadhaar card, FRUITS ID, Land RTC (Pahani) showing dryland status, ST Caste certificate with RD number, Income certificate with RD number, Small/Marginal Farmer certificate from Tahsildar, Bank passbook, Self-declaration of no existing borewell",
        "official_source_url": "https://valmikicorporation.karnataka.gov.in/ / https://sevasindhu.karnataka.gov.in/",
        "official_document_url": "https://valmikicorporation.karnataka.gov.in/",
        "audit_status": "PROVISIONAL",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH010_DEVARAJ_URS: Ganga Kalyana OBC Route (CHILD of SCH010)
    # =========================================================================
    {
        "scheme_id": "SCH010_DEVARAJ_URS",
        "scheme_name": "Ganga Kalyana Scheme — D. Devaraj Urs Backward Classes Development Corporation (OBC)",
        "record_type": "CHILD",
        "parent_scheme_id": "SCH010",
        "government_level": "State (Government of Karnataka)",
        "department": "D. Devaraj Urs Backward Classes Development Corporation, Backward Classes Welfare Department, Govt of Karnataka",
        "benefit_type": "100% Subsidized Infrastructure (Borewell Drilling, Submersible Pump Set, and Power Energization)",
        "target_crops": "All agricultural crops",
        "target_activities": "Drilling of irrigation borewell, supply and installation of submersible pump set with accessories, and electrification through ESCOMs",
        "state": "Karnataka",
        "district_scope": "All 31 districts of Karnataka",
        "farmer_categories": "Small and Marginal dryland farmers belonging to Backward Classes (Category 1, 2A, 3A, 3B - excluding religious minorities)",
        "min_land": "Individual Route: 1.0/1.20 to 5.0 ac; Community Route: 8.0 to 15.0 ac pooled (Provisional — pending corporation-specific guidelines audit)",
        "max_land": "Individual Route: 5.0 ac; Community Route: 15.0 ac pooled",
        "irrigation_requirements": "Land must be dryland (kushki) without any existing irrigation borewell, open well, or canal facility",
        "existing_asset_requirements": "Farmer must not already possess a working borewell or energized pump set on the RTC land parcel",
        "eligible_conditions": "Permanent resident of Karnataka; belonging to notified Backward Classes (Cat 1, 2A, 3A, 3B) with valid RD-numbered caste certificate; family annual income within corporation limit (historically Rs. 1.50L-Rs. 2.00L; provisional pending active annual notice); owning dryland within corporation individual/community limits; valid FRUITS ID.",
        "excluded_conditions": "General Merit farmers; SC, ST, and Religious Minority applicants (must apply to their respective corporations); farmers owning > 5 acres dryland for individual route; land with existing irrigation facilities; family members of government employees or prior Ganga Kalyana beneficiaries in the household.",
        "benefit_rate": "100% government grant (zero farmer contribution).",
        "maximum_benefit": "Total package up to Rs. 3,75,000 in water-scarce districts and up to Rs. 2,50,000 in other districts.",
        "benefit_formula": "Full Grant Package = Drilling_Cost + Pump_and_Accessories_Cost + Electrification_Deposit (Up to Rs. 2.50L or Rs. 3.75L)",
        "upfront_benefit_support": "100% fully funded borewell and pump installation executed directly by D. Devaraj Urs BC Development Corporation contractors.",
        "contingent_benefit_clause": "None (Capital infrastructure grant)",
        "claim_disclaimer": "None (Execution contingent upon hydro-geological groundwater survey feasibility, corporation annual budget quota, and ESCOM power grid infrastructure).",
        "application_period": "Annual application cycle announced via gazette notification (typically July to September)",
        "application_method": "Online via Karnataka Seva Sindhu portal (sevasindhu.karnataka.gov.in) under D. Devaraj Urs BC Development Corporation service menu",
        "required_documents": "Aadhaar card, FRUITS ID, Land RTC (Pahani) showing dryland status, Backward Classes Caste certificate with RD number, Income certificate with RD number, Small/Marginal Farmer certificate from Tahsildar, Bank passbook, Self-declaration of no existing borewell",
        "official_source_url": "https://dbcdc.karnataka.gov.in/ / https://sevasindhu.karnataka.gov.in/",
        "official_document_url": "https://dbcdc.karnataka.gov.in/",
        "audit_status": "PROVISIONAL",
        "verification_date": "2026-09-15"
    },

    # =========================================================================
    # SCH010_KMDC: Ganga Kalyana Minority Route (CHILD of SCH010)
    # =========================================================================
    {
        "scheme_id": "SCH010_KMDC",
        "scheme_name": "Ganga Kalyana Scheme — Karnataka Minorities Development Corporation (KMDC)",
        "record_type": "CHILD",
        "parent_scheme_id": "SCH010",
        "government_level": "State (Government of Karnataka)",
        "department": "Karnataka Minorities Development Corporation Limited (KMDC), Minority Welfare Department, Govt of Karnataka",
        "benefit_type": "100% Subsidized Infrastructure (Borewell Drilling, Submersible Pump Set, and Power Energization)",
        "target_crops": "All agricultural crops",
        "target_activities": "Drilling of irrigation borewell, supply and installation of submersible pump set with accessories, and electrification through ESCOMs",
        "state": "Karnataka",
        "district_scope": "All 31 districts of Karnataka",
        "farmer_categories": "Small and Marginal dryland farmers belonging to Religious Minorities (Muslims, Christians, Jains, Buddhists, Sikhs, Parsis)",
        "min_land": "Individual Route: 1.0/1.20 to 5.0 ac; Community Route: 8.0 to 15.0 ac pooled (Provisional — pending corporation-specific guidelines audit)",
        "max_land": "Individual Route: 5.0 ac; Community Route: 15.0 ac pooled",
        "irrigation_requirements": "Land must be dryland (kushki) without any existing irrigation borewell, open well, or canal facility",
        "existing_asset_requirements": "Farmer must not already possess a working borewell or energized pump set on the RTC land parcel",
        "eligible_conditions": "Permanent resident of Karnataka; belonging to recognized Religious Minority communities (Muslims, Christians, Jains, Buddhists, Sikhs, Parsis) with valid RD-numbered minority certificate; family annual income from all sources within corporation limit (up to Rs. 6.00 Lakh in KMDC recent guidelines; provisional pending active annual notice); owning dryland within corporation individual/community limits; valid FRUITS ID.",
        "excluded_conditions": "Non-minority farmers; General Merit, SC, ST, and general OBC applicants (must apply to their respective corporations); farmers owning > 5 acres dryland for individual route; land with existing irrigation facilities; family members of government employees or prior Ganga Kalyana beneficiaries in the household.",
        "benefit_rate": "100% government grant (zero farmer contribution).",
        "maximum_benefit": "Total package up to Rs. 3,75,000 in water-scarce districts and up to Rs. 2,50,000 in other districts.",
        "benefit_formula": "Full Grant Package = Drilling_Cost + Pump_and_Accessories_Cost + Electrification_Deposit (Up to Rs. 2.50L or Rs. 3.75L)",
        "upfront_benefit_support": "100% fully funded borewell and pump installation executed directly by KMDC contractors.",
        "contingent_benefit_clause": "None (Capital infrastructure grant)",
        "claim_disclaimer": "None (Execution contingent upon hydro-geological groundwater survey feasibility, corporation annual budget quota, and ESCOM power grid infrastructure).",
        "application_period": "Annual application cycle announced via gazette notification (typically July to September)",
        "application_method": "Online via Karnataka Seva Sindhu portal (sevasindhu.karnataka.gov.in) / KMDC Online Portal routed to KMDC District Managers",
        "required_documents": "Aadhaar card, FRUITS ID, Land RTC (Pahani) showing dryland status, Minority Community / Caste certificate with RD number, Income certificate with RD number, Small/Marginal Farmer certificate from Tahsildar, Bank passbook, Self-declaration of no existing borewell",
        "official_source_url": "https://kmdc.karnataka.gov.in/ / https://sevasindhu.karnataka.gov.in/",
        "official_document_url": "https://kmdc.karnataka.gov.in/storage/pdf-files/Ganga%20kalyana%20Guidelines.pdf",
        "audit_status": "PROVISIONAL",
        "verification_date": "2026-09-15"
    }
]

# Validation assertions
parents = [s['scheme_id'] for s in schemes if s['record_type'] in ['STANDALONE', 'PARENT']]
assert len(parents) == 10, f"Expected 10 parent/standalone schemes, got {len(parents)}"
assert len(set([s['scheme_id'] for s in schemes])) == len(schemes), "Duplicate scheme_id found!"

children = [s for s in schemes if s['record_type'] == 'CHILD']
for c in children:
    assert c['parent_scheme_id'] in parents, f"Child {c['scheme_id']} has invalid parent {c['parent_scheme_id']}"

# Explicit mapping of raw file names
raw_filenames = {
    "SCH001": "SCH001_PM_KISAN.json",
    "SCH002": "SCH002_PMFBY.json",
    "SCH003": "SCH003_PMKSY_PDMC.json",
    "SCH004": "SCH004_SMAM.json",
    "SCH005": "SCH005_Krishi_Bhagya.json",
    "SCH006": "SCH006_PM_KUSUM_B.json",
    "SCH007": "SCH007_MIDH.json",
    "SCH008": "SCH008_KCC_MISS.json",
    "SCH009": "SCH009_Soil_Health_Card.json",
    "SCH010": "SCH010_Ganga_Kalyana.json",
    "SCH008_CENTRAL": "SCH008_CENTRAL_KCC_MISS.json",
    "SCH008_KA_COOP": "SCH008_KA_COOP_Zero_Interest.json",
    "SCH010_AMBEDKAR": "SCH010_AMBEDKAR_Ganga_Kalyana.json",
    "SCH010_VALMIKI": "SCH010_VALMIKI_Ganga_Kalyana.json",
    "SCH010_DEVARAJ_URS": "SCH010_DEVARAJ_URS_Ganga_Kalyana.json",
    "SCH010_KMDC": "SCH010_KMDC_Ganga_Kalyana.json"
}

# 1. Save Raw JSON files
for s in schemes:
    fname = raw_filenames.get(s['scheme_id'], f"{s['scheme_id']}.json")
    raw_file = os.path.join(raw_dir, fname)
    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2, ensure_ascii=False)
print(f"Generated {len(schemes)} raw JSON files in {raw_dir}")

# 2. Save Processed JSON and CSV
proc_json = os.path.join(proc_dir, "scheme_master.json")
with open(proc_json, "w", encoding="utf-8") as f:
    json.dump(schemes, f, indent=2, ensure_ascii=False)

df = pd.DataFrame(schemes)
proc_csv = os.path.join(proc_dir, "scheme_master.csv")
df.to_csv(proc_csv, index=False, encoding="utf-8")
print(f"Generated processed JSON and CSV ({len(df)} records) in {proc_dir}")

# 3. Save Formatted Excel file
excel_path = os.path.join(base_dir, "scheme_master.xlsx")
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Scheme Master (16 Schemes)"

# Header styling
header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid") # Elegant Navy Blue
header_font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

thin_border = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9")
)

headers = list(df.columns)
ws.append(headers)

for col_idx, cell in enumerate(ws[1], 1):
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = header_align
    cell.border = thin_border
ws.row_dimensions[1].height = 28

# Zebra data rows
zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
body_font = Font(name="Segoe UI", size=9)
body_align = Alignment(vertical="top", wrap_text=True)
id_align = Alignment(horizontal="center", vertical="top")

center_cols = ["scheme_id", "record_type", "parent_scheme_id", "audit_status", "verification_date"]
center_indices = [headers.index(c) + 1 for c in center_cols if c in headers]

for row_idx, row in enumerate(df.values.tolist(), start=2):
    ws.append(row)
    fill = zebra_fill if row_idx % 2 == 0 else white_fill
    for col_idx, cell in enumerate(ws[row_idx], start=1):
        cell.fill = fill
        cell.font = body_font
        cell.border = thin_border
        if col_idx in center_indices:
            cell.alignment = id_align
        else:
            cell.alignment = body_align
    ws.row_dimensions[row_idx].height = 80

col_widths = {
    "scheme_id": 16,
    "scheme_name": 32,
    "record_type": 14,
    "parent_scheme_id": 16,
    "government_level": 22,
    "department": 30,
    "benefit_type": 26,
    "target_crops": 28,
    "target_activities": 30,
    "state": 18,
    "district_scope": 22,
    "farmer_categories": 28,
    "min_land": 16,
    "max_land": 20,
    "irrigation_requirements": 24,
    "existing_asset_requirements": 25,
    "eligible_conditions": 36,
    "excluded_conditions": 36,
    "benefit_rate": 28,
    "maximum_benefit": 28,
    "benefit_formula": 32,
    "upfront_benefit_support": 30,
    "contingent_benefit_clause": 30,
    "claim_disclaimer": 30,
    "application_period": 22,
    "application_method": 30,
    "required_documents": 32,
    "official_source_url": 28,
    "official_document_url": 30,
    "audit_status": 22,
    "verification_date": 16
}

for col_idx, header in enumerate(headers, 1):
    col_letter = get_column_letter(col_idx)
    ws.column_dimensions[col_letter].width = col_widths.get(header, 25)

ws.freeze_panes = "B2"

wb.save(excel_path)
print(f"Successfully generated {excel_path} with {len(schemes)} schemes and {len(headers)} columns.")
