"""
Workshop scenario: industrial warehouse fire with toxic plume (simulated).

Site, inventory, neighbours, wind, and hospital loads are fiction. The loop is
site-first, then adjacent-risk lookup — not a pre-chosen suburb as the product.
"""

from typing import Dict, Any
from ..models.bio_chem import ThreatType, SampleType, BiologicalSample


FIRE_SITREP = BiologicalSample(
    sample_id="INC-2026-FIRE-EP-01",
    sample_type=SampleType.SITREP_TEXT,
    name="Erskine Park warehouse fire sitrep (simulated)",
    raw_payload=(
        "SIMULATED INCIDENT SITREP — not a live CAD or fire-service product.\n"
        "Site: plastics and solvent warehouse, Erskine Park industrial estate, "
        "western Sydney, adjacent to the M7. First 000 at 02:14 local.\n"
        "Fuel (example on-site DG): styrene, mixed solvents, polyurethane foam. "
        "Offensive attack in progress; black smoke, possible HCN/isocyanate mix.\n"
        "Weather (example BOM): night inversion, wind SW 8 kt, forecast shift to SE "
        "after 06:00. HYSPLIT-shaped planning contour is simulated, not a live run.\n"
        "Conflict: planning contour 3.2 km ENE; EPA handheld / public smell reports "
        "along a creek line at ~4.5 km. Adjacent tank farm inventory not confirmed."
    ),
    source_location="Erskine Park industrial estate (beside M7), New South Wales",
    collection_date="2026-04-03",
    submitting_lab="FRNSW Incident Management (workshop fiction)",
    metadata={
        "hazard": "Industrial warehouse fire / toxic smoke plume",
        "site_name": "Pacific Polymer & Solvents warehouse",
        "warning_level": "Watch and Act — toxic smoke",
        "wind_dir": "SW",
        "wind_kt": 8,
        "stability": "night inversion",
        "forecast_shift": "SE after 06:00",
        "provenance": "simulated",
    },
)


INDUSTRIAL_WAREHOUSE_FIRE_SCENARIO: Dict[str, Any] = {
    "scenario_id": "scen_industrial_warehouse_fire",
    "name": "Erskine Park warehouse fire — toxic plume (simulated)",
    "threat_type": ThreatType.INDUSTRIAL_FIRE,
    "description": (
        "Workshop fiction: a plastics and solvent warehouse fire beside the M7. "
        "The pathway starts at the site, looks up adjacent occupancies (including an "
        "unconfirmed tank farm), offers a simulated HYSPLIT-shaped contour, and pauses "
        "for shelter / motorway / hospital-diversion approval. Second eyes only; not a "
        "replacement for fire, EPA, or ambulance protocols."
    ),
    "sample": FIRE_SITREP.model_dump(),
    "identification": {
        "agent_name": "Industrial warehouse fire / mixed solvent and polymer smoke",
        "clade_or_lineage": "Erskine Park estate — M7 corridor",
        "taxonomy": "Industrial fire / toxic plume",
        "host_tropism": "Downwind residents, motorway users, school, district hospital",
        "genomic_mutations_detected": [],
        "alignment_confidence": None,
        "warning_level": "Watch and Act — toxic smoke",
        "provenance": "simulated",
    },
    "site": {
        "name": "Pacific Polymer & Solvents warehouse",
        "address": "Erskine Park industrial estate, NSW (workshop location)",
        "materials_declared": ["styrene", "mixed solvents", "polyurethane foam"],
        "possible_combustion_products": ["hydrogen cyanide", "isocyanates", "dense black smoke"],
        "provenance": "simulated",
    },
    "adjacent_sites": [
        {
            "name": "Western Sydney tank farm (neighbour)",
            "bearing": "SSW 180 m",
            "occupancy": "Bulk flammable liquids",
            "inventory_status": "unknown",
            "note": "Operator has not confirmed contents in the first hour.",
            "risk": "domino / BLEVE if fire spreads",
        },
        {
            "name": "Cold-store logistics shed",
            "bearing": "W 90 m",
            "occupancy": "Food logistics",
            "inventory_status": "declared — ammonia refrigeration",
            "note": "Secondary toxic risk if involved.",
            "risk": "ammonia release",
        },
        {
            "name": "Erskine Park public school",
            "bearing": "ENE 1.8 km",
            "occupancy": "School",
            "inventory_status": "n/a",
            "note": "Inside the example planning contour after the forecast wind shift.",
            "risk": "shelter or delayed start",
        },
        {
            "name": "Wianamatta District Hospital (example)",
            "bearing": "ENE 4.1 km",
            "occupancy": "District ED",
            "inventory_status": "n/a",
            "note": "Default receiving hospital sits near the field-report plume axis.",
            "risk": "divert ambulance; walk-in decon",
        },
    ],
    "weather": {
        "source": "BOM example product",
        "wind_dir": "SW",
        "wind_kt": 8,
        "stability": "night inversion",
        "forecast_shift": "SE 6–8 kt after 06:00",
        "provenance": "simulated",
    },
    "plume_model": {
        "method": "HYSPLIT-shaped planning contour (simulated — not a live NOAA run)",
        "planning_distance_km": 3.2,
        "direction": "ENE",
        "assumptions": [
            "60-minute release of mixed combustion products",
            "night inversion, wind SW 8 kt",
            "no rain washout",
        ],
        "provenance": "simulated",
    },
    "conflicting_reports": {
        "model": "Planning contour 3.2 km ENE from the warehouse.",
        "field": "EPA handheld and public smell reports along a creek line at about 4.5 km.",
        "inventory": "Adjacent tank farm contents still unknown.",
        "provenance": "simulated",
    },
    "impact_assessment": {
        "population_at_risk_estimate": 12000,
        "critical_sites": [
            "M7 carriageway past the estate",
            "Erskine Park public school",
            "Wianamatta District Hospital (example)",
        ],
        "road_status": "M7 still open into the example plume axis",
        "hospital_status": "Default ED is near the field-report axis; diversion not yet approved",
        "provenance": "simulated",
    },
    "threat_assessment": {
        "hazard_class": "Industrial fire / toxic smoke",
        "ssba_tier": None,
        "protective_action": (
            "Shelter-in-place east of site, M7 do-not-enter, divert ambulance from "
            "Wianamatta District Hospital — pending Incident Controller"
        ),
        "containment_level_required": "Not applicable",
        "provenance": "simulated",
    },
}
