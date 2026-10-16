"""
Validation script for Benchmark v1.0.4 Scenario Assignment Matrix.
Tests all target quotas and statutory definitions:
- Total scenarios: 60 (S011-S070)
- Zones: 10 zones, 6 each
- Landholding classes: 22 Marginal, 20 Small, 12 Medium, 6 Large
- Social categories: 15 SC, 10 ST, 10 OBC, 8 Minority, 17 GM
- Primary needs: 6 for each of 10 categories
- Tenure statuses: 47 Pre-Feb 2019, 4 Post-Feb 2019 Statutory Inheritance (succession upon death), 5 Pure Tenant, 4 Unknown Title Status
- PM-KISAN Statutory Succession Definition Check (v1.0.4): S039, S049, S064, S069 explicitly distinguish succession upon death from ineligible partition/sale/gift deeds
- Community pool: 3 Yes (S028, S052, S066), 57 No
- Land types: 28 Dryland, 10 Canal-irrigated, 12 Borewell-irrigated, 6 Wetland/valley, 4 Hilly/terraced
- Boundaries: 2.5 ac, 5.0 ac, 10.0 ac, 5.0 ha PMKSY, Rs 10k pension
- Cross-field area consistency: requested subsidized area (ha) <= qualifying parcel (ha)
- Solar pump prerequisites: explicit water source and grid electric status (preserving REQUIRES_VERIFICATION when UNKNOWN)
"""

import sys
from collections import Counter

HA_PER_ACRE = 0.40468564224

scenarios = [
    # --- ZONE 1: North Eastern Transition Zone (Bidar, Kalaburagi) ---
    {
        "sid": "S011", "zone": "Z1", "dist": "Bidar", "crop": "Redgram",
        "need": "CROP_INSURANCE", "land_type": "Dryland",
        "total_holding": 1.8, "qual_parcel": 1.8, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "OBC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed (None)", "electric_status": "NONE",
        "policy": "Standard multi-need rainfed pulse profile; OBC category"
    },
    {
        "sid": "S012", "zone": "Z1", "dist": "Kalaburagi", "crop": "Maize",
        "need": "SOLAR_PUMP_INSTALLATION", "land_type": "Dryland",
        "total_holding": 3.0, "qual_parcel": 3.0, "subsidized_ha": "—",
        "lclass": "Small", "social": "SC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Non-energized)", "electric_status": "UNENERGIZED_OFF_GRID",
        "policy": "**Challenge 1:** Standalone solar pump vs. Krishi Bhagya package; water source: unenergized borewell; electric status: UNENERGIZED_OFF_GRID; eligible for PM-KUSUM B"
    },
    {
        "sid": "S013", "zone": "Z1", "dist": "Bidar", "crop": "Sugarcane",
        "need": "SOIL_HEALTH_AND_FERTILIZER", "land_type": "Canal-irrigated",
        "total_holding": 5.0, "qual_parcel": 5.0, "subsidized_ha": "—",
        "lclass": "Small", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Canal Outlet", "electric_status": "NONE",
        "policy": "**Boundary test:** Exactly 5.0 acres (Small/Medium boundary, <= 5.0 is Small); SHC nutrient advisory"
    },
    {
        "sid": "S014", "zone": "Z1", "dist": "Kalaburagi", "crop": "Soybean",
        "need": "PRODUCTION_CREDIT", "land_type": "Dryland",
        "total_holding": 2.2, "qual_parcel": 2.2, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "ST", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed (None)", "electric_status": "NONE",
        "policy": "**Challenge 6:** Central KCC-MISS commercial credit vs. State PACS zero-interest credit"
    },
    {
        "sid": "S015", "zone": "Z1", "dist": "Bidar", "crop": "Jowar",
        "need": "INCOME_SUPPORT", "land_type": "Dryland",
        "total_holding": 1.5, "qual_parcel": 1.5, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "SC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed (None)", "electric_status": "NONE",
        "policy": "**Challenge 2:** Relief vs. debt; KCC must not receive score 3 for income support"
    },
    {
        "sid": "S016", "zone": "Z1", "dist": "Kalaburagi", "crop": "Redgram",
        "need": "BOREWELL_IRRIGATION", "land_type": "Dryland",
        "total_holding": 4.5, "qual_parcel": 4.5, "subsidized_ha": "—",
        "lclass": "Small", "social": "SC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "None (Dryland kushki)", "electric_status": "NONE",
        "policy": "Ganga Kalyana individual borewell (Ambedkar Corp); SC dryland within <= 5.0 ac ceiling"
    },

    # --- ZONE 2: North Eastern Dry Zone (Kalaburagi, Yadgir, Raichur) ---
    {
        "sid": "S017", "zone": "Z2", "dist": "Yadgir", "crop": "Cotton",
        "need": "CROP_INSURANCE", "land_type": "Dryland",
        "total_holding": 6.0, "qual_parcel": 6.0, "subsidized_ha": "—",
        "lclass": "Medium", "social": "ST", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed (None)", "electric_status": "NONE",
        "policy": "Dryland cotton PMFBY coverage; medium holding (6.0 ac); notified area pest risk"
    },
    {
        "sid": "S018", "zone": "Z2", "dist": "Raichur", "crop": "Sunflower",
        "need": "INCOME_SUPPORT", "land_type": "Dryland",
        "total_holding": 2.0, "qual_parcel": 2.0, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed (None)", "electric_status": "NONE",
        "policy": "**Challenge 3:** Pensioner at exactly ₹10,000/month; PM-KISAN exclusion threshold test"
    },
    {
        "sid": "S019", "zone": "Z2", "dist": "Kalaburagi", "crop": "Bajra",
        "need": "RAINWATER_HARVESTING", "land_type": "Dryland",
        "total_holding": 1.2, "qual_parcel": 1.2, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "OBC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed Catchment", "electric_status": "NONE",
        "policy": "Krishi Bhagya farm-pond primary need; dryland Bajra in rainfed dry zone"
    },
    {
        "sid": "S020", "zone": "Z2", "dist": "Yadgir", "crop": "Redgram",
        "need": "SOLAR_PUMP_INSTALLATION", "land_type": "Dryland",
        "total_holding": 6.5, "qual_parcel": 6.5, "subsidized_ha": "—",
        "lclass": "Medium", "social": "SC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Unconfirmed)", "electric_status": "UNKNOWN",
        "policy": "**Challenge 4:** Solar pump requested; borewell electric status UNKNOWN -> triggers REQUIRES_VERIFICATION for PM-KUSUM B; income tax status UNKNOWN -> triggers REQUIRES_VERIFICATION for PM-KISAN"
    },
    {
        "sid": "S021", "zone": "Z2", "dist": "Raichur", "crop": "Cotton",
        "need": "FARM_MECHANIZATION", "land_type": "Canal-irrigated",
        "total_holding": 4.0, "qual_parcel": 4.0, "subsidized_ha": "—",
        "lclass": "Small", "social": "Minority", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Canal Distributary", "electric_status": "NONE",
        "policy": "SMAM sprayer/equipment subsidy; canal command cotton; Minority category"
    },
    {
        "sid": "S022", "zone": "Z2", "dist": "Kalaburagi", "crop": "Sunflower",
        "need": "SOIL_HEALTH_AND_FERTILIZER", "land_type": "Dryland",
        "total_holding": 1.8, "qual_parcel": 1.8, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed (None)", "electric_status": "NONE",
        "policy": "Soil Health Card diagnostic profiling, dryland sunflower, GM category"
    },

    # --- ZONE 3: Northern Dry Zone (Vijayapura, Bagalkot, Gadag, Koppal) ---
    {
        "sid": "S023", "zone": "Z3", "dist": "Vijayapura", "crop": "Pomegranate",
        "need": "MICRO_IRRIGATION_SUPPORT", "land_type": "Borewell-irrigated",
        "total_holding": 3.5, "qual_parcel": 3.5, "subsidized_ha": 1.41,
        "lclass": "Small", "social": "Minority", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "PMKSY-PDMC drip for high-value horticulture; requested 1.41 ha <= 3.5 ac (1.416 ha); Minority category"
    },
    {
        "sid": "S024", "zone": "Z3", "dist": "Bagalkot", "crop": "Maize",
        "need": "SOLAR_PUMP_INSTALLATION", "land_type": "Canal-irrigated",
        "total_holding": 2.0, "qual_parcel": 2.0, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "ST", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Non-energized)", "electric_status": "UNENERGIZED_OFF_GRID",
        "policy": "**Challenge 1:** Standalone solar pump vs. Krishi Bhagya package; water source: unenergized borewell; electric status: UNENERGIZED_OFF_GRID; eligible for PM-KUSUM B"
    },
    {
        "sid": "S025", "zone": "Z3", "dist": "Gadag", "crop": "Onion",
        "need": "PROTECTED_HORTICULTURE", "land_type": "Borewell-irrigated",
        "total_holding": 1.5, "qual_parcel": 1.5, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "SC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "MIDH shade-net structure for commercial onion; SC marginal holding"
    },
    {
        "sid": "S026", "zone": "Z3", "dist": "Koppal", "crop": "Bengalgram",
        "need": "PRODUCTION_CREDIT", "land_type": "Canal-irrigated",
        "total_holding": 2.5, "qual_parcel": 2.5, "subsidized_ha": "—",
        "lclass": "Small", "social": "GM", "tenure": "Pure Tenant",
        "pool": "No",
        "water_source": "Canal Command", "electric_status": "NONE",
        "policy": "**Challenge 5 & Boundary test:** Exactly 2.5 ac (Small); Pure tenant; KCC tenant rules, PM-KISAN ineligible"
    },
    {
        "sid": "S027", "zone": "Z3", "dist": "Vijayapura", "crop": "Pomegranate",
        "need": "RAINWATER_HARVESTING", "land_type": "Dryland",
        "total_holding": 6.5, "qual_parcel": 6.5, "subsidized_ha": "—",
        "lclass": "Medium", "social": "SC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed Catchment", "electric_status": "NONE",
        "policy": "Krishi Bhagya farm pond; SC dryland horticulture holding (6.5 ac)"
    },
    {
        "sid": "S028", "zone": "Z3", "dist": "Bagalkot", "crop": "Onion",
        "need": "BOREWELL_IRRIGATION", "land_type": "Dryland",
        "total_holding": 10.0, "qual_parcel": 3.0, "subsidized_ha": "—",
        "lclass": "Medium", "social": "OBC", "tenure": "Pre-Feb 2019",
        "pool": "Yes (3 farmers, 9.0 ac pooled, contiguous)",
        "water_source": "None (Dryland kushki)", "electric_status": "NONE",
        "policy": "**Challenge 7 & Boundary test:** Exactly 10.0 ac (Medium); individual dryland > 5 ac ineligible for indiv borewell; community pool route (3 farmers, 9.0 ac pooled contiguous dryland, qualifying parcel 3.0 ac); REQUIRES_VERIFICATION (provisional Devaraj Urs corporation rules)"
    },

    # --- ZONE 4: Central Dry Zone (Chitradurga, Davanagere, Tumakuru) ---
    {
        "sid": "S029", "zone": "Z4", "dist": "Chitradurga", "crop": "Groundnut",
        "need": "BOREWELL_IRRIGATION", "land_type": "Dryland",
        "total_holding": 2.0, "qual_parcel": 2.0, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "SC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "None (Dryland kushki)", "electric_status": "NONE",
        "policy": "Ganga Kalyana individual borewell (Ambedkar Corp); marginal dryland SC farmer"
    },
    {
        "sid": "S030", "zone": "Z4", "dist": "Davanagere", "crop": "Maize",
        "need": "SOLAR_PUMP_INSTALLATION", "land_type": "Canal-irrigated",
        "total_holding": 3.8, "qual_parcel": 3.8, "subsidized_ha": "—",
        "lclass": "Small", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Non-energized)", "electric_status": "UNENERGIZED_OFF_GRID",
        "policy": "**Challenge 1:** Standalone solar pump vs. Krishi Bhagya package; water source: unenergized borewell; electric status: UNENERGIZED_OFF_GRID; eligible for PM-KUSUM B"
    },
    {
        "sid": "S031", "zone": "Z4", "dist": "Tumakuru", "crop": "Ragi",
        "need": "RAINWATER_HARVESTING", "land_type": "Dryland",
        "total_holding": 1.8, "qual_parcel": 1.8, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "ST", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed Catchment", "electric_status": "NONE",
        "policy": "Krishi Bhagya farm pond; ST dryland farmer in Central Dry Zone"
    },
    {
        "sid": "S032", "zone": "Z4", "dist": "Chitradurga", "crop": "Groundnut",
        "need": "INCOME_SUPPORT", "land_type": "Dryland",
        "total_holding": 2.5, "qual_parcel": 2.5, "subsidized_ha": "—",
        "lclass": "Small", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed (None)", "electric_status": "NONE",
        "policy": "**Challenge 3 & Boundary test:** Exactly 2.5 ac (Small); income tax payer -> PM-KISAN INELIGIBLE"
    },
    {
        "sid": "S033", "zone": "Z4", "dist": "Davanagere", "crop": "Arecanut",
        "need": "FARM_MECHANIZATION", "land_type": "Borewell-irrigated",
        "total_holding": 7.5, "qual_parcel": 7.5, "subsidized_ha": "—",
        "lclass": "Medium", "social": "OBC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "SMAM machinery subsidy for arecanut cultivation; Medium holding (7.5 ac); OBC"
    },
    {
        "sid": "S034", "zone": "Z4", "dist": "Tumakuru", "crop": "Maize",
        "need": "MICRO_IRRIGATION_SUPPORT", "land_type": "Borewell-irrigated",
        "total_holding": 11.0, "qual_parcel": 11.0, "subsidized_ha": 4.45,
        "lclass": "Large", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "**Challenge 8:** Large holding (11.0 ac); PMKSY-PDMC evaluated against 5-ha (~12.36 ac) ceiling; requested 4.45 ha <= 11.0 ac (4.451 ha) and <= 5.00 ha ceiling"
    },

    # --- ZONE 5: Eastern Dry Zone (Kolar, Chikkaballapura, Bengaluru Rural) ---
    {
        "sid": "S035", "zone": "Z5", "dist": "Kolar", "crop": "Tomato",
        "need": "PROTECTED_HORTICULTURE", "land_type": "Borewell-irrigated",
        "total_holding": 1.5, "qual_parcel": 1.5, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "SC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "MIDH polyhouse structure; SC marginal horticulture farmer"
    },
    {
        "sid": "S036", "zone": "Z5", "dist": "Chikkaballapura", "crop": "Mulberry",
        "need": "PRODUCTION_CREDIT", "land_type": "Borewell-irrigated",
        "total_holding": 3.0, "qual_parcel": 3.0, "subsidized_ha": "—",
        "lclass": "Small", "social": "Minority", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "**Challenge 6:** KCC commercial credit vs. PACS cooperative credit for sericulture; Minority"
    },
    {
        "sid": "S037", "zone": "Z5", "dist": "Bengaluru Rural", "crop": "Mango",
        "need": "MICRO_IRRIGATION_SUPPORT", "land_type": "Borewell-irrigated",
        "total_holding": 2.5, "qual_parcel": 2.5, "subsidized_ha": 1.01,
        "lclass": "Small", "social": "ST", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "**Boundary test:** Exactly 2.5 ac (Small); PMKSY-PDMC drip for mango orchard; requested 1.01 ha <= 2.5 ac (1.012 ha)"
    },
    {
        "sid": "S038", "zone": "Z5", "dist": "Kolar", "crop": "Tomato",
        "need": "INCOME_SUPPORT", "land_type": "Dryland",
        "total_holding": 1.2, "qual_parcel": 1.2, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed (None)", "electric_status": "NONE",
        "policy": "**Challenge 2:** Post-harvest price collapse distress; KCC debt must not receive score 3"
    },
    {
        "sid": "S039", "zone": "Z5", "dist": "Chikkaballapura", "crop": "Ragi",
        "need": "CROP_INSURANCE", "land_type": "Dryland",
        "total_holding": 2.0, "qual_parcel": 2.0, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "SC", "tenure": "Post-Feb 2019 Inheritance",
        "pool": "No",
        "water_source": "Rainfed (None)", "electric_status": "NONE",
        "policy": "PM-KISAN statutory succession exemption test; land title acquired post-cutoff strictly via inheritance following death of landowner (father deceased Aug 2021; Death Cert & Bhoomi mutation Form 12 verified; transfer_basis=INHERITANCE_DUE_TO_DEATH); distinct from post-cutoff partition deeds"
    },
    {
        "sid": "S040", "zone": "Z5", "dist": "Bengaluru Rural", "crop": "Mango",
        "need": "FARM_MECHANIZATION", "land_type": "Borewell-irrigated",
        "total_holding": 5.0, "qual_parcel": 5.0, "subsidized_ha": "—",
        "lclass": "Small", "social": "OBC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "**Boundary test:** Exactly 5.0 acres (Small/Medium boundary, <= 5.0 is Small); SMAM orchard implements"
    },

    # --- ZONE 6: Southern Dry Zone (Mandya, Mysuru, Chamarajanagar) ---
    {
        "sid": "S041", "zone": "Z6", "dist": "Mandya", "crop": "Sugarcane",
        "need": "MICRO_IRRIGATION_SUPPORT", "land_type": "Canal-irrigated",
        "total_holding": 6.5, "qual_parcel": 6.5, "subsidized_ha": 2.50,
        "lclass": "Medium", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Canal & Storage Tank", "electric_status": "NONE",
        "policy": "PMKSY-PDMC drip irrigation in irrigated sugarcane canal command; requested 2.50 ha <= 6.5 ac (2.630 ha); Medium holding (6.5 ac)"
    },
    {
        "sid": "S042", "zone": "Z6", "dist": "Mysuru", "crop": "Paddy",
        "need": "CROP_INSURANCE", "land_type": "Wetland/valley",
        "total_holding": 3.5, "qual_parcel": 3.5, "subsidized_ha": "—",
        "lclass": "Small", "social": "SC", "tenure": "Pure Tenant",
        "pool": "No",
        "water_source": "Canal Flow", "electric_status": "NONE",
        "policy": "**Challenge 5:** Pure tenant paddy; PMFBY coverage with tenancy documentation verification"
    },
    {
        "sid": "S043", "zone": "Z6", "dist": "Chamarajanagar", "crop": "Banana",
        "need": "BOREWELL_IRRIGATION", "land_type": "Dryland",
        "total_holding": 1.8, "qual_parcel": 1.8, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "ST", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "None (Dryland kushki)", "electric_status": "NONE",
        "policy": "Ganga Kalyana individual borewell (Valmiki Corp); ST marginal dryland farmer; REQUIRES_VERIFICATION (provisional corporation rules)"
    },
    {
        "sid": "S044", "zone": "Z6", "dist": "Mandya", "crop": "Paddy",
        "need": "INCOME_SUPPORT", "land_type": "Wetland/valley",
        "total_holding": 2.0, "qual_parcel": 2.0, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "OBC", "tenure": "Pure Tenant",
        "pool": "No",
        "water_source": "Canal Flow", "electric_status": "NONE",
        "policy": "**Challenge 2 & Challenge 5:** Pure tenant wetland paddy; PM-KISAN INELIGIBLE due to lack of land title; relief vs. credit"
    },
    {
        "sid": "S045", "zone": "Z6", "dist": "Mysuru", "crop": "Ragi",
        "need": "RAINWATER_HARVESTING", "land_type": "Dryland",
        "total_holding": 1.5, "qual_parcel": 1.5, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "SC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed Catchment", "electric_status": "NONE",
        "policy": "Krishi Bhagya farm pond; SC dryland farmer in Southern Dry Zone"
    },
    {
        "sid": "S046", "zone": "Z6", "dist": "Chamarajanagar", "crop": "Sugarcane",
        "need": "SOIL_HEALTH_AND_FERTILIZER", "land_type": "Canal-irrigated",
        "total_holding": 7.0, "qual_parcel": 7.0, "subsidized_ha": "—",
        "lclass": "Medium", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Canal Command", "electric_status": "NONE",
        "policy": "Soil Health Card soil profiling for medium sugarcane holding (7.0 ac); GM"
    },

    # --- ZONE 7: Southern Transition Zone (Hassan, Shivamogga, Chikkamagaluru Plains) ---
    {
        "sid": "S047", "zone": "Z7", "dist": "Hassan", "crop": "Maize",
        "need": "FARM_MECHANIZATION", "land_type": "Canal-irrigated",
        "total_holding": 5.5, "qual_parcel": 5.5, "subsidized_ha": "—",
        "lclass": "Medium", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Canal Command", "electric_status": "NONE",
        "policy": "SMAM tractor/thresher implements subsidy; Medium holding (5.5 ac); GM"
    },
    {
        "sid": "S048", "zone": "Z7", "dist": "Shivamogga", "crop": "Ginger",
        "need": "PROTECTED_HORTICULTURE", "land_type": "Borewell-irrigated",
        "total_holding": 2.0, "qual_parcel": 2.0, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "ST", "tenure": "Unknown Title Status",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "**Challenge 4:** Pension MTS exemption unknown & title status UNKNOWN -> REQUIRES_VERIFICATION for land-dependent schemes"
    },
    {
        "sid": "S049", "zone": "Z7", "dist": "Chikkamagaluru", "crop": "Potato",
        "need": "PROTECTED_HORTICULTURE", "land_type": "Borewell-irrigated",
        "total_holding": 4.5, "qual_parcel": 4.5, "subsidized_ha": "—",
        "lclass": "Small", "social": "GM", "tenure": "Post-Feb 2019 Inheritance",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "MIDH shade-net structure for commercial seed potato; post-2019 statutory succession exemption test (transfer_basis=INHERITANCE_DUE_TO_DEATH; father deceased May 2022; Death Cert, legal heir order, Bhoomi mutation Form 16 verified; land_ownership_cutoff_pre_feb_2019=True engine input); distinct from non-qualifying partition deed"
    },
    {
        "sid": "S050", "zone": "Z7", "dist": "Hassan", "crop": "Arecanut",
        "need": "PRODUCTION_CREDIT", "land_type": "Borewell-irrigated",
        "total_holding": 3.5, "qual_parcel": 3.5, "subsidized_ha": "—",
        "lclass": "Small", "social": "OBC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "**Challenge 6:** KCC commercial credit vs. PACS cooperative credit; arecanut garden"
    },
    {
        "sid": "S051", "zone": "Z7", "dist": "Shivamogga", "crop": "Maize",
        "need": "SOLAR_PUMP_INSTALLATION", "land_type": "Dryland",
        "total_holding": 2.5, "qual_parcel": 2.5, "subsidized_ha": "—",
        "lclass": "Small", "social": "Minority", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Non-energized)", "electric_status": "UNENERGIZED_OFF_GRID",
        "policy": "**Boundary test:** Exactly 2.5 ac (Small); water source: unenergized borewell; electric status: UNENERGIZED_OFF_GRID; PM-KUSUM B solar pump; Minority"
    },
    {
        "sid": "S052", "zone": "Z7", "dist": "Chikkamagaluru", "crop": "Potato",
        "need": "BOREWELL_IRRIGATION", "land_type": "Dryland",
        "total_holding": 9.5, "qual_parcel": 4.0, "subsidized_ha": "—",
        "lclass": "Medium", "social": "OBC", "tenure": "Pre-Feb 2019",
        "pool": "Yes (3 farmers, 12.0 ac pooled, contiguous)",
        "water_source": "None (Dryland kushki)", "electric_status": "NONE",
        "policy": "**Challenge 7:** Individual dryland > 5 ac ineligible for indiv borewell; community pool route (3 farmers, 12.0 ac pooled contiguous dryland, qualifying parcel 4.0 ac); REQUIRES_VERIFICATION (provisional Devaraj Urs corporation rules)"
    },

    # --- ZONE 8: Northern Transition Zone (Dharwad, Belagavi, Haveri) ---
    {
        "sid": "S053", "zone": "Z8", "dist": "Dharwad", "crop": "Soybean",
        "need": "RAINWATER_HARVESTING", "land_type": "Dryland",
        "total_holding": 5.5, "qual_parcel": 5.5, "subsidized_ha": "—",
        "lclass": "Medium", "social": "Minority", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed Catchment", "electric_status": "NONE",
        "policy": "Krishi Bhagya farm pond; medium holding (5.5 ac); Northern Transition Zone; Minority"
    },
    {
        "sid": "S054", "zone": "Z8", "dist": "Belagavi", "crop": "Chilli",
        "need": "PROTECTED_HORTICULTURE", "land_type": "Wetland/valley",
        "total_holding": 1.5, "qual_parcel": 1.5, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "SC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Open Well / Stream Lift", "electric_status": "NONE",
        "policy": "MIDH shade-net structure for high-value chilli; SC marginal farmer"
    },
    {
        "sid": "S055", "zone": "Z8", "dist": "Haveri", "crop": "Cotton",
        "need": "INCOME_SUPPORT", "land_type": "Dryland",
        "total_holding": 3.0, "qual_parcel": 3.0, "subsidized_ha": "—",
        "lclass": "Small", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed (None)", "electric_status": "NONE",
        "policy": "**Challenge 3:** Regular government officer -> PM-KISAN INELIGIBLE statutory exclusion"
    },
    {
        "sid": "S056", "zone": "Z8", "dist": "Dharwad", "crop": "Wheat",
        "need": "SOIL_HEALTH_AND_FERTILIZER", "land_type": "Dryland",
        "total_holding": 4.0, "qual_parcel": 4.0, "subsidized_ha": "—",
        "lclass": "Small", "social": "ST", "tenure": "Unknown Title Status",
        "pool": "No",
        "water_source": "Rainfed (None)", "electric_status": "NONE",
        "policy": "**Challenge 4:** Land title UNKNOWN -> SHC accessible; title-dependent schemes trigger REQUIRES_VERIFICATION"
    },
    {
        "sid": "S057", "zone": "Z8", "dist": "Belagavi", "crop": "Sugarcane",
        "need": "FARM_MECHANIZATION", "land_type": "Canal-irrigated",
        "total_holding": 12.0, "qual_parcel": 12.0, "subsidized_ha": "—",
        "lclass": "Large", "social": "OBC", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Canal Command", "electric_status": "NONE",
        "policy": "**Challenge 8:** Large holding (12.0 ac); SMAM evaluated per scheme machinery tier; no blanket exclusion"
    },
    {
        "sid": "S058", "zone": "Z8", "dist": "Haveri", "crop": "Soybean",
        "need": "MICRO_IRRIGATION_SUPPORT", "land_type": "Borewell-irrigated",
        "total_holding": 12.5, "qual_parcel": 12.5, "subsidized_ha": 5.00,
        "lclass": "Large", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "**Challenge 8 & Boundary test:** Large holding (12.5 ac holding & qualifying parcel); PMKSY-PDMC boundary test at exactly 5.00 ha (~12.36 ac) statutory ceiling; 5.00 ha <= 12.5 ac (5.059 ha)"
    },

    # --- ZONE 9: Hilly Zone (Kodagu, Chikkamagaluru Ghats, Uttara Kannada Ghats) ---
    {
        "sid": "S059", "zone": "Z9", "dist": "Kodagu", "crop": "Coffee",
        "need": "SOIL_HEALTH_AND_FERTILIZER", "land_type": "Hilly/terraced",
        "total_holding": 4.5, "qual_parcel": 4.5, "subsidized_ha": "—",
        "lclass": "Small", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Hillside Stream Catchment", "electric_status": "NONE",
        "policy": "Soil Health Card soil testing for plantation coffee in Hilly Zone"
    },
    {
        "sid": "S060", "zone": "Z9", "dist": "Chikkamagaluru", "crop": "Cardamom",
        "need": "RAINWATER_HARVESTING", "land_type": "Hilly/terraced",
        "total_holding": 2.0, "qual_parcel": 2.0, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "ST", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Hillside Stream Catchment", "electric_status": "NONE",
        "policy": "Water harvesting storage structure for hillside cardamom plantation; ST"
    },
    {
        "sid": "S061", "zone": "Z9", "dist": "Uttara Kannada", "crop": "Paddy",
        "need": "PRODUCTION_CREDIT", "land_type": "Wetland/valley",
        "total_holding": 3.0, "qual_parcel": 3.0, "subsidized_ha": "—",
        "lclass": "Small", "social": "SC", "tenure": "Pure Tenant",
        "pool": "No",
        "water_source": "Valley Natural Flow", "electric_status": "NONE",
        "policy": "**Challenge 5:** Hill zone valley paddy pure tenant; KCC tenant route; PMFBY verification"
    },
    {
        "sid": "S062", "zone": "Z9", "dist": "Kodagu", "crop": "Black Pepper",
        "need": "CROP_INSURANCE", "land_type": "Hilly/terraced",
        "total_holding": 1.8, "qual_parcel": 1.8, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "GM", "tenure": "Unknown Title Status",
        "pool": "No",
        "water_source": "Hillside Rainfed", "electric_status": "NONE",
        "policy": "**Challenge 4:** Land title UNKNOWN -> land-dependent schemes trigger REQUIRES_VERIFICATION"
    },
    {
        "sid": "S063", "zone": "Z9", "dist": "Chikkamagaluru", "crop": "Coffee",
        "need": "SOLAR_PUMP_INSTALLATION", "land_type": "Hilly/terraced",
        "total_holding": 2.5, "qual_parcel": 2.5, "subsidized_ha": "—",
        "lclass": "Small", "social": "Minority", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Borewell (Non-energized)", "electric_status": "UNENERGIZED_OFF_GRID",
        "policy": "**Boundary test:** Exactly 2.5 ac (Small); water source: unenergized borewell; electric status: UNENERGIZED_OFF_GRID; PM-KUSUM B solar pump for off-grid plantation; Minority"
    },
    {
        "sid": "S064", "zone": "Z9", "dist": "Uttara Kannada", "crop": "Paddy",
        "need": "FARM_MECHANIZATION", "land_type": "Canal-irrigated",
        "total_holding": 8.0, "qual_parcel": 8.0, "subsidized_ha": "—",
        "lclass": "Medium", "social": "OBC", "tenure": "Post-Feb 2019 Inheritance",
        "pool": "No",
        "water_source": "Canal Command", "electric_status": "NONE",
        "policy": "SMAM power tiller/paddy transplanter subsidy; medium holding (8.0 ac); post-2019 statutory inheritance upon demise of parent (transfer_basis=INHERITANCE_DUE_TO_DEATH, legal heir cert & mutation verified; distinct from ineligible partition deed)"
    },

    # --- ZONE 10: Coastal Zone (Dakshina Kannada, Udupi, Uttara Kannada Coast) ---
    {
        "sid": "S065", "zone": "Z10", "dist": "Dakshina Kannada", "crop": "Coconut",
        "need": "SOIL_HEALTH_AND_FERTILIZER", "land_type": "Dryland",
        "total_holding": 14.0, "qual_parcel": 14.0, "subsidized_ha": "—",
        "lclass": "Large", "social": "GM", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed Coastal", "electric_status": "NONE",
        "policy": "Soil Health Card universal diagnostic service for large coastal plantation (14.0 ac); GM"
    },
    {
        "sid": "S066", "zone": "Z10", "dist": "Udupi", "crop": "Arecanut",
        "need": "BOREWELL_IRRIGATION", "land_type": "Dryland",
        "total_holding": 5.5, "qual_parcel": 3.5, "subsidized_ha": "—",
        "lclass": "Medium", "social": "SC", "tenure": "Pre-Feb 2019",
        "pool": "Yes (4 farmers, 14.0 ac pooled, contiguous)",
        "water_source": "None (Dryland kushki)", "electric_status": "NONE",
        "policy": "**Challenge 7:** Individual holding 5.5 ac exceeds 5.0 ac individual Ambedkar ceiling; community pool route valid with 4 SC farmers, 14.0 ac pooled contiguous dryland, qualifying parcel 3.5 ac; requires verification of parcel contiguity & groundwater clearance"
    },
    {
        "sid": "S067", "zone": "Z10", "dist": "Dakshina Kannada", "crop": "Cashew",
        "need": "CROP_INSURANCE", "land_type": "Dryland",
        "total_holding": 2.0, "qual_parcel": 2.0, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "ST", "tenure": "Pre-Feb 2019",
        "pool": "No",
        "water_source": "Rainfed Coastal", "electric_status": "NONE",
        "policy": "PMFBY cashew crop insurance in coastal plantation belt; ST marginal farmer"
    },
    {
        "sid": "S068", "zone": "Z10", "dist": "Udupi", "crop": "Coastal Paddy",
        "need": "PRODUCTION_CREDIT", "land_type": "Wetland/valley",
        "total_holding": 1.5, "qual_parcel": 1.5, "subsidized_ha": "—",
        "lclass": "Marginal", "social": "Minority", "tenure": "Pure Tenant",
        "pool": "No",
        "water_source": "Wetland Inflow", "electric_status": "NONE",
        "policy": "**Challenge 5:** Pure tenant coastal wetland paddy; KCC crop loan & PMFBY insurance proof check; Minority"
    },
    {
        "sid": "S069", "zone": "Z10", "dist": "Dakshina Kannada", "crop": "Coconut",
        "need": "PROTECTED_HORTICULTURE", "land_type": "Dryland",
        "total_holding": 13.0, "qual_parcel": 13.0, "subsidized_ha": "—",
        "lclass": "Large", "social": "Minority", "tenure": "Post-Feb 2019 Inheritance",
        "pool": "No",
        "water_source": "Open Well / Rainfed", "electric_status": "NONE",
        "policy": "MIDH coastal nursery / shade-net; Large holding (13.0 ac); Minority; post-2019 statutory inheritance upon demise of parent (transfer_basis=INHERITANCE_DUE_TO_DEATH, legal heir cert & mutation verified; distinct from ineligible partition deed)"
    },
    {
        "sid": "S070", "zone": "Z10", "dist": "Udupi", "crop": "Arecanut",
        "need": "MICRO_IRRIGATION_SUPPORT", "land_type": "Wetland/valley",
        "total_holding": 12.5, "qual_parcel": 12.5, "subsidized_ha": 4.80,
        "lclass": "Large", "social": "SC", "tenure": "Unknown Title Status",
        "pool": "No",
        "water_source": "Borewell (Grid-connected)", "electric_status": "GRID_CONNECTED_IP_SET",
        "policy": "**Challenge 8:** Large holding (12.5 ac); PMKSY-PDMC requested 4.80 ha <= 12.5 ac (5.059 ha) and <= 5.00 ha ceiling; title status UNKNOWN -> REQUIRES_VERIFICATION"
    }
]

def validate_matrix(data):
    print("==================================================")
    print("BENCHMARK V1.0.4 MATRIX VALIDATION REPORT")
    print("==================================================")
    failures = []
    
    # 1. Total count
    total = len(data)
    print(f"Total Scenarios: {total} (Target: 60) -> {'PASS' if total == 60 else 'FAIL'}")
    if total != 60:
        failures.append(f"Total scenarios count {total} != 60")

    # 2. IDs continuity
    expected_ids = [f"S{i:03d}" for i in range(11, 71)]
    actual_ids = [s["sid"] for s in data]
    id_match = (actual_ids == expected_ids)
    print(f"Scenario IDs Continuous S011-S070: {'PASS' if id_match else 'FAIL'}")
    if not id_match:
        failures.append("Scenario IDs not continuous S011-S070")

    # 3. Zones: 10 zones, 6 each
    zones = Counter(s["zone"] for s in data)
    zone_targets = {f"Z{i}": 6 for i in range(1, 11)}
    zone_pass = (zones == zone_targets)
    print(f"Zones Distribution (6 per zone Z1-Z10): {'PASS' if zone_pass else 'FAIL'}")
    for z in [f"Z{i}" for i in range(1, 11)]:
        cnt = zones.get(z, 0)
        print(f"  {z}: {cnt} / 6")
        if cnt != 6:
            failures.append(f"Zone {z} count {cnt} != 6")

    # 4. Land Classes: 22 Marginal, 20 Small, 12 Medium, 6 Large
    lclass_counter = Counter()
    for s in data:
        acres = s["total_holding"]
        declared = s["lclass"]
        if acres < 2.5:
            expected = "Marginal"
        elif 2.5 <= acres <= 5.0:
            expected = "Small"
        elif 5.0 < acres <= 10.0:
            expected = "Medium"
        else:
            expected = "Large"
        if declared != expected:
            failures.append(f"{s['sid']}: declared {declared} but {acres} ac is {expected}")
        lclass_counter[declared] += 1

    lc_targets = {"Marginal": 22, "Small": 20, "Medium": 12, "Large": 6}
    lc_pass = (lclass_counter == lc_targets and len(failures) == 0)
    print(f"\nLandholding Classes (Marginal 22, Small 20, Medium 12, Large 6): {'PASS' if lc_pass else 'FAIL'}")
    for lc, tgt in lc_targets.items():
        cnt = lclass_counter.get(lc, 0)
        print(f"  {lc}: {cnt} / {tgt}")
        if cnt != tgt:
            failures.append(f"Land class {lc} count {cnt} != {tgt}")

    boundary_2_5 = [s["sid"] for s in data if s["total_holding"] == 2.5]
    boundary_5_0 = [s["sid"] for s in data if s["total_holding"] == 5.0]
    boundary_10_0 = [s["sid"] for s in data if s["total_holding"] == 10.0]
    print(f"  Boundary 2.5 ac (classified Small): {len(boundary_2_5)} scenarios ({', '.join(boundary_2_5)})")
    print(f"  Boundary 5.0 ac (classified Small): {len(boundary_5_0)} scenarios ({', '.join(boundary_5_0)})")
    print(f"  Boundary 10.0 ac (classified Medium): {len(boundary_10_0)} scenarios ({', '.join(boundary_10_0)})")

    # 5. Social Categories: SC 15, ST 10, OBC 10, Minority 8, GM 17
    social_counter = Counter(s["social"] for s in data)
    soc_targets = {"SC": 15, "ST": 10, "OBC": 10, "Minority": 8, "GM": 17}
    soc_pass = (social_counter == soc_targets)
    print(f"\nSocial Categories (SC 15, ST 10, OBC 10, Minority 8, GM 17): {'PASS' if soc_pass else 'FAIL'}")
    for sc, tgt in soc_targets.items():
        cnt = social_counter.get(sc, 0)
        print(f"  {sc}: {cnt} / {tgt}")
        if cnt != tgt:
            failures.append(f"Social category {sc} count {cnt} != {tgt}")

    # 6. Primary Needs: 6 per category (10 categories)
    need_counter = Counter(s["need"] for s in data)
    all_needs = [
        "CROP_INSURANCE", "SOLAR_PUMP_INSTALLATION", "RAINWATER_HARVESTING",
        "MICRO_IRRIGATION_SUPPORT", "PROTECTED_HORTICULTURE", "PRODUCTION_CREDIT",
        "FARM_MECHANIZATION", "BOREWELL_IRRIGATION", "INCOME_SUPPORT", "SOIL_HEALTH_AND_FERTILIZER"
    ]
    need_targets = {n: 6 for n in all_needs}
    need_pass = (need_counter == need_targets)
    print(f"\nPrimary Needs (6 per need, 10 needs): {'PASS' if need_pass else 'FAIL'}")
    for n in all_needs:
        cnt = need_counter.get(n, 0)
        print(f"  {n}: {cnt} / 6")
        if cnt != 6:
            failures.append(f"Need {n} count {cnt} != 6")

    # 7. Tenure Statuses: Pre-Feb 2019: 47, Post-Feb 2019 Inheritance: 4, Pure Tenant: 5, Unknown Title Status: 4
    tenure_counter = Counter(s["tenure"] for s in data)
    tenure_targets = {
        "Pre-Feb 2019": 47,
        "Post-Feb 2019 Inheritance": 4,
        "Pure Tenant": 5,
        "Unknown Title Status": 4
    }
    tenure_pass = (tenure_counter == tenure_targets)
    print(f"\nTenure Statuses (Pre-Feb 2019: 47, Inheritance: 4, Pure Tenant: 5, Unknown: 4): {'PASS' if tenure_pass else 'FAIL'}")
    for t, tgt in tenure_targets.items():
        cnt = tenure_counter.get(t, 0)
        print(f"  {t}: {cnt} / {tgt}")
        if cnt != tgt:
            failures.append(f"Tenure status {t} count {cnt} != {tgt}")

    # 7b. Post-Feb 2019 Statutory Succession vs. Partition Definition Check (v1.0.4)
    inheritance_scenarios = [s for s in data if s["tenure"] == "Post-Feb 2019 Inheritance"]
    inherit_ids = [s["sid"] for s in inheritance_scenarios]
    expected_inherit_ids = ["S039", "S049", "S064", "S069"]
    inherit_ids_pass = (inherit_ids == expected_inherit_ids)
    print(f"\nPost-Feb 2019 Statutory Inheritance Definitions Check (v1.0.4): {'PASS' if inherit_ids_pass else 'FAIL'}")
    if not inherit_ids_pass:
        failures.append(f"Inheritance scenario IDs {inherit_ids} != {expected_inherit_ids}")
    for s in inheritance_scenarios:
        pol = s["policy"].lower()
        has_death = ("death" in pol or "demise" in pol)
        has_distinction = ("distinct from" in pol or "partition" in pol)
        if not (has_death and has_distinction):
            failures.append(f"{s['sid']} policy must distinguish statutory succession upon death from partition deeds")
            print(f"  {s['sid']}: FAIL - missing statutory succession upon death vs partition distinction")
        else:
            print(f"  {s['sid']}: PASS - explicit statutory succession upon demise verified")

    # 8. Community Pool: 3 Yes, 57 No
    pool_counter = Counter("Yes" if s["pool"].startswith("Yes") else "No" for s in data)
    pool_targets = {"Yes": 3, "No": 57}
    pool_pass = (pool_counter == pool_targets)
    print(f"\nCommunity Pool (3 Yes, 57 No): {'PASS' if pool_pass else 'FAIL'}")
    print(f"  Yes: {pool_counter.get('Yes', 0)} / 3")
    print(f"  No: {pool_counter.get('No', 0)} / 57")
    pool_ids = [s["sid"] for s in data if s["pool"].startswith("Yes")]
    print(f"  Pool Scenario IDs: {pool_ids}")
    if pool_ids != ["S028", "S052", "S066"]:
        failures.append(f"Community pool IDs {pool_ids} != ['S028', 'S052', 'S066']")

    # 9. Land Types: 28 Dryland, 10 Canal-irrigated, 12 Borewell-irrigated, 6 Wetland/valley, 4 Hilly/terraced
    lt_counter = Counter(s["land_type"] for s in data)
    lt_targets = {
        "Dryland": 28,
        "Canal-irrigated": 10,
        "Borewell-irrigated": 12,
        "Wetland/valley": 6,
        "Hilly/terraced": 4
    }
    lt_pass = (lt_counter == lt_targets)
    print(f"\nLand Types (Dryland: 28, Canal: 10, Borewell: 12, Wetland: 6, Hilly: 4): {'PASS' if lt_pass else 'FAIL'}")
    for lt, tgt in lt_targets.items():
        cnt = lt_counter.get(lt, 0)
        print(f"  {lt}: {cnt} / {tgt}")
        if cnt != tgt:
            failures.append(f"Land type {lt} count {cnt} != {tgt}")

    # 10. Cross-Field Area Validation: Subsidized Area (ha) <= Qualifying Parcel (ha)
    print("\nCross-Field Area Validation (Requested Subsidized Area ha <= Qualifying Parcel ha):")
    area_checked = 0
    area_failures = []
    for s in data:
        if s["subsidized_ha"] != "—":
            area_checked += 1
            req_ha = float(s["subsidized_ha"])
            max_phys_ha = s["qual_parcel"] * HA_PER_ACRE
            # Allow 1e-4 tolerance for floating point
            if req_ha > (max_phys_ha + 1e-4):
                area_failures.append(
                    f"{s['sid']}: requested {req_ha:.2f} ha exceeds physical capacity of qualifying parcel {s['qual_parcel']} ac ({max_phys_ha:.4f} ha)"
                )
                print(f"  {s['sid']}: req={req_ha:.2f} ha > qual_parcel={s['qual_parcel']} ac ({max_phys_ha:.4f} ha) -> FAIL")
            else:
                print(f"  {s['sid']}: req={req_ha:.2f} ha <= qual_parcel={s['qual_parcel']} ac ({max_phys_ha:.4f} ha) -> PASS")

    print(f"Total Subsidized Area Cases Verified: {area_checked}")
    if area_failures:
        failures.extend(area_failures)

    # 11. Solar Pump Prerequisite Attributes Validation
    print("\nSolar Pump Prerequisite Validation (Water Source & Grid Electric Status):")
    solar_checked = 0
    solar_failures = []
    for s in data:
        if s["need"] == "SOLAR_PUMP_INSTALLATION":
            solar_checked += 1
            ws = s.get("water_source", "")
            es = s.get("electric_status", "")
            if not ws or ws == "Rainfed (None)":
                solar_failures.append(f"{s['sid']}: Solar pump requires valid water source, found '{ws}'")
            if not es:
                solar_failures.append(f"{s['sid']}: Solar pump requires explicit electric_status")
            if s["sid"] == "S020":
                if es != "UNKNOWN" or "REQUIRES_VERIFICATION" not in s["policy"]:
                    solar_failures.append(f"{s['sid']}: S020 must have electric_status UNKNOWN and policy REQUIRES_VERIFICATION")
            elif es != "UNENERGIZED_OFF_GRID":
                solar_failures.append(f"{s['sid']}: Off-grid solar pump requires UNENERGIZED_OFF_GRID, found '{es}'")
            print(f"  {s['sid']}: water_source='{ws}', electric_status='{es}', status={'PASS' if not solar_failures else 'CHECK'}")

    print(f"Total Solar Pump Cases Verified: {solar_checked} / 6")
    if solar_failures:
        failures.extend(solar_failures)

    print("\n--------------------------------------------------")
    if not failures:
        print("OVERALL STATUS: ALL DIMENSIONS & CROSS-FIELD CHECKS PASSED PERFECTLY!")
        return True
    else:
        print(f"OVERALL STATUS: {len(failures)} FAILURES DETECTED!")
        for f in failures:
            print(f"  - {f}")
        return False

if __name__ == "__main__":
    success = validate_matrix(scenarios)
    sys.exit(0 if success else 1)
